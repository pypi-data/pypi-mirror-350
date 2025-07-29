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

from magnopy.energy.line_search import _line_search

_logger = logging.getLogger(__name__)

__all__ = []


def _bfgs(
    self,
    true_variables_0,
    hessian_0,
    tolerance,
    func,
    grad,
    update,
    to_x,
    update_difference,
):
    r"""
    Generalized optimization function. It's implementation is a little complicated as
    we need to track both general vector parameter :math:`\boldsymbol{x}` and the true
    variables of the energy function (i.e. spin directions, cone axis, spiral vector).

    Parameters
    ----------
    true_variables_0 : ...
        Initial guess for the true variables. Form and type depends on the
        ground state sub-type. The calls of ``to_x(true_variables_0)``,
        ``func(true_variables_0)``, ``grad(true_variables_0)`` have to be valid.
    hessian_0 : ...
        Initial guess for the hessian matrix.
    tolerance : (N, ) :numpy:`ndarray`
        One dimensional array of tolerance targets for the optimization.
        Exact amount of elements depends on the ground state sub-type.
    func : callable
        Energy function. The call ``func(true_variables_0)`` has to be valid.
    grad : callable
        Gradient of the energy function. The call ``grad(true_variables_0)`` has
        to be valid.
    update : callable
        Function that update the true variables to the new state defined by the
        :math:`\boldsymbol{x}` vector. The call ``update(true_variables_0, x)``
        has to be valid.
    to_x : callable
        Function that converts true variables to the generalized vector argument. The
        call ``to_x(true_variables_0)`` has to be valid.
    update_difference : callable
        Function that computes the difference between two consecutive steps of the
        optimization. The call ``update_difference(func_k, func_kp1, grad_k, grad_kp1)``
        has to be valid. Where ``func_k = func(true_variables_k)`` and
        ``grad_k = grad(true_variables_k)``.

    Returns
    -------
    true_variables : ...
        Optimized true variables.
    """

    difference = tolerance.copy() * 2
    true_variables_k = true_variables_0.copy()
    x_k = to_x(true_variables_k)
    hessian_size = x_k.size
    # hessian = np.eye(hessian_size, dtype=float)

    hessian = np.linalg.inv(hessian_0)

    func_k = func(true_variables_k)
    grad_k = grad(true_variables_k)

    step_counter = 0
    first_run = True
    while (difference > tolerance).any():
        search_direction = -hessian @ grad_k

        alphas = np.linspace(0, 1.5, 300)

        energies = []
        for alpha in alphas:
            tmp_x = x_k + alpha * search_direction
            tmp_tv = update(true_variables_k, tmp_x)

            energies.append(func(tmp_tv))

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(20, 4))

        ax.plot(alphas, energies, lw=2, color="black")

        # Fix it tomorrow
        alpha_k = _line_search(
            x_k=x_k,
            true_variables_k=true_variables_k,
            search_direction=search_direction,
            func=func,
            grad=grad,
            update=update,
            func_0=func_k,
            grad_0=grad_k,
        )

        ax.vlines(
            [0, alpha_k], 0, 1, lw=0.5, color="grey", transform=ax.get_xaxis_transform()
        )
        ax.hlines(
            energies[0], 0, 1, lw=0.5, color="grey", transform=ax.get_yaxis_transform()
        )
        ax.set_title(
            R"$\alpha = " f"{alpha_k:.8f}$",
            fontsize=20,
        )

        plt.show()
        plt.close()

        x_kp1 = x_k + alpha_k * search_direction
        true_variables_kp1 = update(true_variables_k, x_kp1)

        grad_kp1 = grad(true_variables_kp1)
        func_kp1 = func(true_variables_kp1)

        difference = update_difference(func_k, func_kp1, grad_kp1)

        print(difference)
        step_counter += 1

        if (difference < tolerance).all():
            break

        s_k = x_kp1 - x_k
        y_k = grad_kp1 - grad_k

        rho_k = 1 / (y_k @ s_k)

        EYE = np.eye(hessian_size, dtype=float)
        OUTER = np.outer(y_k, s_k)

        # if first_run:
        #     first_run = False
        #     hessian = (s_k @ y_k) / (y_k @ y_k) * hessian

        hessian = (EYE - rho_k * OUTER.T) @ hessian @ (
            EYE - rho_k * OUTER
        ) + rho_k * np.outer(s_k, s_k)

        grad_k = grad_kp1
        func_k = func_kp1
        x_k = to_x(true_variables_kp1)
        true_variables_k = true_variables_kp1

    _logger.info(f"Optimization finished in {step_counter} steps.")

    return true_variables_kp1
