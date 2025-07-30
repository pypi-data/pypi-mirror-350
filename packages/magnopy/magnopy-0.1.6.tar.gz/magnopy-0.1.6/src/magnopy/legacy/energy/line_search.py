# MAGNOPY - Python package for magnons.
# Copyright (C) 2023-2025 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging

import numpy as np

_logger = logging.getLogger(__name__)

__all__ = []


def _cubic_interpolation(alpha_l, alpha_h, f_l, f_h, fp_l, fp_h):
    r"""
    Computes the minimum of a cubic interpolation for the function f(alpha) with
    values f_l, f_h and derivatives fp_l, fp_h at the points alpha_l, alpha_h.

    Parameters
    ----------
    alpha_l : float
        Lower bound of the interval.
    alpha_h : float
        Upper bound of the interval.
    f_l : float
        Value of the function at alpha_l.
    f_h : float
        Value of the function at alpha_h.
    fp_l : float
        Derivative of the function at alpha_l.
    fp_h : float
        Derivative of the function at alpha_h.

    Returns
    -------
    alpha_min : float
        Position of the minimum of the cubic interpolation for the function f(alpha).
    """

    d_1 = fp_l + fp_h - 3 * (f_l - f_h) / (alpha_l - alpha_h)
    # # print(d_1, f_l, f_h, alpha_l, alpha_h, fp_l, fp_h)
    if d_1**2 - fp_l * fp_h < 0:
        return alpha_h
    d_2 = np.sign(alpha_h - alpha_l) * np.sqrt(d_1**2 - fp_l * fp_h)

    return alpha_h - (alpha_h - alpha_l) * (fp_h + d_2 - d_1) / (fp_h - fp_l + 2 * d_2)


def _zoom(
    x_k,
    true_variables_k,
    search_direction,
    func,
    grad,
    update,
    func_0,
    grad_0,
    alpha_lo,
    alpha_hi,
    c1,
    c2,
):
    r"""
    Zoom function for the line search with strong Wolfe conditions.

    Parameters
    ----------
    x_k : :numpy:`ndarray`
        Current parameterization of the true variables. Length of the array depends
        on the ground state sub-type. The call ``update(true_variables_k, x_k)``
        has to be valid.
    true_variables_k : ...
        Current true variables. Form and type depends on the ground state sub-type.
        Calls of ``func(true_variables_k)``, ``grad(true_variables_k)`` have to be valid.
    search_direction : :numpy:`ndarray`
        Search direction. Same shape and size as ``x_k``.
    func : callable
        Energy function. The call ``func(true_variables_k)`` has to be valid.
    grad : callable
        Gradient of the energy function. The call ``grad(true_variables_k)`` has
        to be valid.
    update : callable
        Function that update the true variables to the new state defined by the
        :math:`\boldsymbol{x}` vector. The call ``update(true_variables_k, x_k)``
        has to be valid.
    func_0 : float
        Energy at the current state: ``func(true_variables_k)``.
    grad_0 : :numpy:`ndarray`
        Gradient of the energy at the current state: ``grad(true_variables_k)``.
    alpha_lo : float
        Lower bound of the step length.
    alpha_hi : float
        Upper bound of the step length.
    c1 : float
        Parameter for the Wolfe conditions.
    c2 : float
        Parameter for the Wolfe conditions.
    """

    f_0 = func_0
    fp_0 = grad_0 @ search_direction

    true_variables_k_lo = update(true_variables_k, x_k + alpha_lo * search_direction)
    true_variables_k_hi = update(true_variables_k, x_k + alpha_hi * search_direction)

    f_lo = func(true_variables_k_lo)
    fp_lo = grad(true_variables_k_lo) @ search_direction
    f_hi = func(true_variables_k_hi)
    fp_hi = grad(true_variables_k_hi) @ search_direction
    f_j_min = None
    trial_steps = 0
    while True:
        if abs(alpha_hi - alpha_lo) < np.finfo(float).eps:
            return alpha_lo
        # print("in zoom")
        alpha_j = _cubic_interpolation(
            alpha_l=alpha_lo,
            alpha_h=alpha_hi,
            f_l=f_lo,
            f_h=f_hi,
            fp_l=fp_lo,
            fp_h=fp_hi,
        )

        true_variables_k_j = update(true_variables_k, x_k + alpha_j * search_direction)

        f_j = func(true_variables_k_j)
        if f_j_min is None:
            f_j_min = f_j
        else:
            if f_j < f_j_min:
                trial_steps = 0
                f_j_min = f_j
            elif trial_steps >= 10:
                return alpha_j
            else:
                trial_steps += 1

        # # print("zoom", alpha_lo, alpha_hi, alpha_j, f_j, f_lo, f_hi)

        if f_j > f_0 + c1 * alpha_j * fp_0 or f_j >= f_lo:
            alpha_hi = alpha_j
            f_hi = f_j
            fp_hi = grad(true_variables_k_j) @ search_direction
        else:
            fp_j = grad(true_variables_k_j) @ search_direction

            if abs(fp_j) <= -c2 * fp_0:
                return alpha_j

            if fp_j * (alpha_hi - alpha_lo) >= 0:
                alpha_hi = alpha_lo
                f_hi = f_lo
                fp_hi = fp_lo

            alpha_lo = alpha_j
            f_lo = f_j
            fp_lo = fp_j


def _line_search(
    x_k,
    true_variables_k,
    search_direction,
    func,
    grad,
    update,
    func_0=None,
    grad_0=None,
    c1=1e-4,
    c2=0.9,
    max_iterations=10000,
    alpha_max=3.0,
):
    r"""
    Computes step length via line search with strong Wolfe conditions.

    Parameters
    ----------
    x_k : :numpy:`ndarray`
        Current parameterization of the true variables. Length of the array depends
        on the ground state sub-type. The call ``update(true_variables_k, x_k)``
        has to be valid.
    true_variables_k : ...
        Current true variables. Form and type depends on the ground state sub-type.
        Calls of ``func(true_variables_k)``, ``grad(true_variables_k)`` have to be valid.
    search_direction : :numpy:`ndarray`
        Search direction. Same shape and size as ``x_k``.
    func : callable
        Energy function. The call ``func(true_variables_k)`` has to be valid.
    grad : callable
        Gradient of the energy function. The call ``grad(true_variables_k)`` has
        to be valid.
    update : callable
        Function that update the true variables to the new state defined by the
        :math:`\boldsymbol{x}` vector. The call ``update(true_variables_k, x_k)``
        has to be valid.
    func_0 : float, optional
        Energy at the current state: ``func(true_variables_k)``.
    grad_0 : :numpy:`ndarray`, optional
        Gradient of the energy at the current state: ``grad(true_variables_k)``.
    c1 : float, default 1e-4
        Parameter for the Wolfe conditions.
    c2 : float, default 0.9
        Parameter for the Wolfe conditions.
    max_iterations : int, default 10000
        Maximum number of iterations.
    alpha_max: float, default 3.0
        Maximum step length.
    """

    if func_0 is None:
        func_0 = func(true_variables_k)

    if grad_0 is None:
        grad_0 = grad(true_variables_k)

    # Add pre-check of alpha = 1

    alpha_im1 = 0
    alpha_i = 1
    f_0 = func_0
    fp_0 = grad_0 @ search_direction
    f_im1 = f_0
    fp_im1 = fp_0

    for i in range(1, max_iterations):
        x_kpi = x_k + alpha_i * search_direction
        true_variables_k_i = update(true_variables_k, x_kpi)
        f_i = func(true_variables_k_i)

        if f_i > f_0 + c1 * alpha_i * fp_0 or (i > 1 and f_i >= f_im1):
            return _zoom(
                x_k=x_k,
                true_variables_k=true_variables_k,
                search_direction=search_direction,
                func=func,
                grad=grad,
                update=update,
                func_0=func_0,
                grad_0=grad_0,
                alpha_lo=alpha_im1,
                alpha_hi=alpha_i,
                c1=c1,
                c2=c2,
            )

        fp_i = grad(true_variables_k_i) @ search_direction

        if abs(fp_i) <= -c2 * fp_0:
            return alpha_i

        if fp_i >= 0:
            return _zoom(
                x_k=x_k,
                true_variables_k=true_variables_k,
                search_direction=search_direction,
                func=func,
                grad=grad,
                update=update,
                func_0=func_0,
                grad_0=grad_0,
                alpha_lo=alpha_i,
                alpha_hi=alpha_im1,
                c1=c1,
                c2=c2,
            )

        if abs(alpha_i - alpha_im1) < np.finfo(float).eps:
            return alpha_i
        # print("in line search")
        alpha_ip1 = _cubic_interpolation(
            alpha_l=alpha_im1,
            alpha_h=alpha_i,
            f_l=f_im1,
            f_h=f_i,
            fp_l=fp_im1,
            fp_h=fp_i,
        )

        if alpha_ip1 > alpha_max:
            _logger.warning(
                f"Step length exceeded maximum value of {alpha_max}. "
                "Returning maximum step length."
            )
            return alpha_max
        if alpha_ip1 < alpha_i:
            _logger.warning("Step length decreased. Keeping the previous step length.")

        alpha_im1 = alpha_i
        f_im1 = f_i
        fp_im1 = fp_i

        alpha_i = alpha_i

    raise ValueError(f"Line search failed after {max_iterations} iterations.")
