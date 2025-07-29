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


R"""
Functions for the common manipulation with the exchange parameters.
"""

import numpy as np

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_matrix_parameter(iso=None, aniso=None, dmi=None) -> np.ndarray:
    r"""
    Computes :math:`3 \times 3` matrix from different parts of it.

    Parameters
    ----------
    iso : int or float, optional
        Value of isotropic exchange parameter.
    aniso : (3, 3) |array-like|_, optional
        Traceless, symmetric 3 x 3 matrix of exchange anisotropy.
        Note: Input matrix is symmetrized and made traceless.
    dmi : (3,) |array-like|_, optional
        Dzyaroshinsky-Moria interaction vector :math:`(D_x, D_y, D_z)`.

    Returns
    -------
    matrix : (3, 3) :numpy:`ndarray`
        Full matrix of exchange parameter. If no input provided, then returns matrix of
        zeros.

    Notes
    -----
    Full matrix of the exchange parameter can be decomposed into three common parts:
    isotropic (``iso``), traceless symmetric anisotropy
    (``aniso``) and antisymmetric anisotropy (``dmi``)

    .. math::

        \boldsymbol{J}
        =
        \begin{pmatrix}
            J_{iso} & 0 & 0 \\
            0 & J_{iso} & 0 \\
            0 & 0 & J_{iso} \\
        \end{pmatrix}
        +
        \begin{pmatrix}
            S^{xx} & S^{xy} & S^{xz} \\
            S^{xy} & S^{yy} & S^{yz} \\
            S^{xz} & S^{yz} & S^{zz} \\
        \end{pmatrix}
        +
        \begin{pmatrix}
            0 & D^z & -D^y \\
            -D^z & 0 & D^x \\
            D^y & -D^x & 0 \\
        \end{pmatrix}

    Examples
    --------

    .. doctest::

        >>> import magnopy
        >>> magnopy._spinham.get_matrix_parameter(iso=1)
        array([[1., 0., 0.],
               [0., 1., 0.],
               [0., 0., 1.]])
        >>> magnopy._spinham.get_matrix_parameter(dmi = (1, 2, 0))
        array([[ 0.,  0., -2.],
               [ 0.,  0.,  1.],
               [ 2., -1.,  0.]])

    """

    matrix = np.zeros((3, 3), dtype=float)

    if iso is not None:
        matrix += iso * np.eye(3, dtype=float)

    if aniso is not None:
        aniso = np.array(aniso, dtype=float)

        # Make sure that it is traceless
        aniso -= np.eye(3) * np.linalg.trace(aniso) / 3

        # Make sure that is is symmetric
        aniso = (aniso + aniso.T) / 2

        matrix += aniso

    if dmi is not None:
        matrix += [
            [0, dmi[2], -dmi[1]],
            [-dmi[2], 0, dmi[0]],
            [dmi[1], -dmi[0], 0],
        ]

    return matrix


def get_isotropic_parameter(matrix, matrix_form=False):
    r"""
    Computes isotropic parameter from full matrix parameter.

    Parameters
    ----------
    matrix : (3, 3) |array-like|_
        Full matrix of the parameter.
    matrix_form : bool, default False
        Whether to return isotropic part of the matrix instead of isotropic parameter.

    Returns
    -------
    iso : float or (3, 3) :numpy:`ndarray`
        Isotropic parameter. If ``matrix_form == True``, then return a matrix.

    Notes
    -----

    Isotropic parameter is defined as

    .. math::

        J_{iso} = \dfrac{tr(\boldsymbol{J})}{3}

    In a matrix form it is

    .. math::

        \begin{pmatrix}
            J_{iso} & 0 & 0 \\
            0 & J_{iso} & 0 \\
            0 & 0 & J_{iso} \\
        \end{pmatrix}

    Examples
    --------

    .. doctest::

        >>> import magnopy
        >>> matrix = [[1, 3, 4], [-1, -2, 3], [4, 0, 10]]
        >>> magnopy._spinham.get_isotropic_parameter(matrix)
        3.0
        >>> magnopy._spinham.get_isotropic_parameter(matrix, matrix_form=True)
        array([[3., 0., 0.],
               [0., 3., 0.],
               [0., 0., 3.]])
    """

    iso = np.linalg.trace(matrix) / 3

    if matrix_form:
        return iso * np.eye(3, dtype=float)

    return float(iso)


def get_anisotropic_parameter(matrix):
    r"""
    Computes traceless, symmetric anisotropy from full matrix parameter.

    Parameters
    ----------
    matrix : (3, 3) |array-like|_
        Full matrix of the parameter.

    Returns
    -------
    aniso : float or (3, 3) :numpy:`ndarray`
        Matrix of a traceless, symmetric anisotropy.

    Notes
    -----

    Traceless, symmetric anisotropy is defined as

    .. math::

        \boldsymbol{J}_{S}
        =
        \dfrac{\boldsymbol{J} + \boldsymbol{J}.T}{2}
        -
        J_{iso} \cdot \boldsymbol{I}

    Examples
    --------

    .. doctest::

        >>> import magnopy
        >>> matrix = [[1, 3, 4], [-1, -2, 0], [4, 0, 10]]
        >>> magnopy._spinham.get_anisotropic_parameter(matrix)
        array([[-2.,  1.,  4.],
               [ 1., -5.,  0.],
               [ 4.,  0.,  7.]])
    """

    matrix = np.array(matrix)

    return (matrix + matrix.T) / 2 - get_isotropic_parameter(
        matrix=matrix, matrix_form=True
    )


def get_dmi(matrix, matrix_form=False):
    r"""
    Computes DMI parameter from full matrix parameter.

    Parameters
    ----------
    matrix : (3, 3) |array-like|_
        Full matrix of the parameter.
    matrix_form : bool, default False
        Whether to return dmi as a matrix instead of a vector form.

    Returns
    -------
    dmi : (3,) or (3, 3) :numpy:`ndarray`
        Antisymmetic exchange (DMI). If ``matrix_form == True``, then return a matrix.

    Notes
    -----

    Antisymmetric anisotropy is defined as

    .. math::

        \boldsymbol{J}_{A}
        =
        \dfrac{\boldsymbol{J}
        -
        \boldsymbol{J}.T}{2}
        =
        \begin{pmatrix}
            0 & D^z & -D^y \\
            -D^z & 0 & D^x \\
            D^y & -D^x & 0 \\
        \end{pmatrix}


    In a vector form it is

    .. math::

        \boldsymbol{D}
        =
        \begin{pmatrix}
        D^x \\
        D^y \\
        D^z \\
        \end{pmatrix}

    Examples
    --------

    .. doctest::

        >>> import magnopy
        >>> matrix = [[1, 3, 0], [-1, -2, 3], [0, 3, 9]]
        >>> magnopy._spinham.get_dmi(matrix)
        array([0., 0., 2.])
        >>> magnopy._spinham.get_dmi(matrix, matrix_form = True)
        array([[ 0.,  2.,  0.],
               [-2.,  0.,  0.],
               [ 0.,  0.,  0.]])
    """

    matrix = np.array(matrix)

    asymm_matrix = (matrix - matrix.T) / 2

    if matrix_form:
        return asymm_matrix

    return np.array(
        [asymm_matrix[1][2], asymm_matrix[2][0], asymm_matrix[0][1]],
        dtype=float,
    )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
