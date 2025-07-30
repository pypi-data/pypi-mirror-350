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


from functools import cmp_to_key

import numpy as np
from numpy.linalg import LinAlgError

from magnopy._exceptions import ColpaFailed

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _check_grand_dynamical_matrix(D):
    r"""
    Check that grand dynamical matrix is (2N, 2N) matrix

    Parameters
    ----------
    D : |array-like|_
        Candidate for the grand dynamical matrix

    Returns
    -------
    D : (2N, 2N) :numpy:`ndarray`
        Grand dynamical matrix.
    N : int

    Raises
    ------
    ValueError
        If the check is not passed
    """

    D = np.array(D)

    if len(D.shape) != 2:
        raise ValueError(f"Grand dynamical matrix is not 2-dimensional, got {D.shape}.")

    if D.shape[0] != D.shape[1]:
        raise (f"Grand dynamical matrix is not square, got {D.shape}.")

    if D.shape[0] % 2 != 0:
        raise (f"Size of the grand dynamical matrix is not even, got {D.shape}.")

    return D, D.shape[0] // 2


def _inverse_by_colpa(matrix):
    # Compute G from G^-1 following Colpa, see equation (3.7) for details
    matrix = np.conjugate(matrix).T
    matrix[:N, N:] *= -1
    matrix[N:, :N] *= -1

    return matrix


def solve_via_colpa(D, return_inverse=False):
    r"""
    Diagonalize grand-dynamical matrix following the method of Colpa [1]_.

    Algorithm is described in section 3, remark 1 of [1]_.

    Solves the Bogoliubov Hamiltonian of the form:

    .. math::

        \hat{H} = \sum_{r^{\prime}, r = 1}^m
        a_{r^{\prime}}^{\dagger}\boldsymbol{\Delta}_1^{r^{\prime}r}a_r +
        a_{r^{\prime}}^{\dagger}\boldsymbol{\Delta}_2^{r^{\prime}r}a_{m+r}^{\dagger} +
        a_{m+r^{\prime}}^{\dagger}\boldsymbol{\Delta}_3^{r^{\prime}r}a_r +
        a_{m+r^{\prime}}^{\dagger}\boldsymbol{\Delta}_4^{r^{\prime}r}a_{m+r}^{\dagger}

    In a matrix form the Hamiltonian is:

    .. math::

        \hat{H} = \boldsymbol{\cal A}^{\dagger} \boldsymbol{D} \boldsymbol{\cal A}

    where

    .. math::

        \boldsymbol{\cal A} =
        \begin{pmatrix}
            a_1 \\
            \cdots \\
            a_m \\
            a_{m+1} \\
            \cdots \\
            a_{2m} \\
        \end{pmatrix}

    After diagonalization the Hamiltonian is:

    .. math::

        \hat{H}
        =
        \boldsymbol{\cal B}^{\dagger} \boldsymbol{\mathcal{E}} \boldsymbol{\cal B}

    Parameters
    ----------
    D : (2N, 2N) |array-like|_
        Grand dynamical matrix. If it is Hermitian and positive-defined, then obtained
        eigenvalues are positive and real.

        .. math::

            \boldsymbol{\mathcal{D}} = \begin{pmatrix}
                \boldsymbol{\Delta_1} & \boldsymbol{\Delta_2} \\
                \boldsymbol{\Delta_3} & \boldsymbol{\Delta_4}
            \end{pmatrix}
    return_inverse : bool, default False
        Whether to return :math:`(\boldsymbol{G}^{\dagger})^{-1}` instead of
        :math:`\boldsymbol{G}^{\dagger}`.

    Returns
    -------
    E : (2N,) :numpy:`ndarray`
        The eigenvalues.
        It is an array of the diagonal elements of the
        diagonal matrix :math:`\boldsymbol{\mathcal{E}}` of the diagonalized Hamiltonian.
        First N elements correspond to the
        :math:`b^{\dagger}(\boldsymbol{k})b(\boldsymbol{k})` and last N elements - to
        the :math:`b(-\boldsymbol{k})b^{\dagger}(-\boldsymbol{k})`.

        Eigenvalues are sorted individually for the first N and the last N elements,
        based on the transformation matrix and not on the values of E itself.

        It is a diagonal of the matrix

        .. math::

            \boldsymbol{\mathcal{E}}
            =
            (\boldsymbol{G}^{\dagger})^{-1} \boldsymbol{D} \boldsymbol{G}^{-1}

    G : (2N, 2N) :numpy:`ndarray`
        Transformation matrix, which changes the basis from the original set of bosonic
        operators :math:`\boldsymbol{a}` to the set of new bosonic operators
        :math:`\boldsymbol{b}` which diagonalize the Hamiltonian:

        .. math::

            \boldsymbol{\cal A} = \boldsymbol{G} \boldsymbol{\cal B}

            \boldsymbol{\cal B} = \boldsymbol{G}^{-1} \boldsymbol{\cal A}

        The rows are ordered in the same way as the eigenvalues.

        If ``return_inverse == False``, then :math:`\boldsymbol{G}^{\dagger}` is
        returned.

        If ``return_inverse == True``, then :math:`(\boldsymbol{G}^{\dagger})^{-1}` is
        returned.

    Raises
    ------
    ColpaFailed
        If the algorithm fails. Typically it means that the grand dynamical matrix
        :math:`\boldsymbol{D}` is not positive-defined.
    ValueError
        If the grand dynamical matrix is not square or its shape is not even.

    References
    ----------
    .. [1] Colpa, J.H.P., 1978.
        Diagonalization of the quadratic boson hamiltonian.
        Physica A: Statistical Mechanics and its Applications,
        93(3-4), pp.327-353.
    """

    D, N = _check_grand_dynamical_matrix(D)

    g = np.diag(np.concatenate((np.ones(N), -np.ones(N))))

    try:
        # In Colpa article decomposition is K^{\dag}K, while numpy gives KK^{\dag}
        K = np.conjugate(np.linalg.cholesky(D)).T
    except LinAlgError:
        raise ColpaFailed

    L, U = np.linalg.eig(K @ g @ np.conjugate(K).T)

    # Sort with respect to L, in descending order
    U = np.concatenate((L[:, None], U.T), axis=1).T
    # U = np.concatenate((L[np.newaxis, :], U), axis=0)
    U = U[:, np.argsort(U[0])]
    L = U[0, ::-1]
    U = U[1:, ::-1]
    E = g @ L

    G_minus_one = np.linalg.inv(K) @ U @ np.sqrt(np.diag(E))

    # Sort first N and second N individually based on the transformation matrix
    tmp = np.concatenate((E[:, np.newaxis], G_minus_one), axis=1)

    def compare(array1, array2):
        difference = np.round(array1 - array2, decimals=15)
        if np.allclose(difference, np.zeros(difference.shape)):
            return 0.0

        return difference[np.nonzero(difference)[0][0]]

    upper_part = np.array(sorted(tmp[:N], key=cmp_to_key(compare)))
    lower_part = np.array(sorted(tmp[N:], key=cmp_to_key(compare)))

    E = np.concatenate((upper_part[:, 0], lower_part[:, 0]))
    G_minus_one = np.concatenate((upper_part[:, 1:], lower_part[:, 1:]), axis=0)

    if return_inverse:
        return E, G_minus_one

    return E, _inverse_by_colpa(G_minus_one)


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
