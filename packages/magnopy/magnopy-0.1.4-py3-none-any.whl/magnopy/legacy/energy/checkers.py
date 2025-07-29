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


def _check_directions(n_spins: int, directions):
    r"""
    Check the input correctness for the directional vectors and normalize them.

    Parameters
    ----------
    n_spins : int
        Number of spins in the unit cell (I).
    directions : (I, 3) or (3,) |array-like|_
        Direction of the spin vectors.

    Raises
    ------
    ValueError
        If the input is not correct.

    Notes
    -----
    The vectors are normalized to one, i.e. only the direction of the vectors
    is important.

    Returns
    -------
    directions : (I, 3) :numpy:`ndarray`
        Normalized direction vectors.
    """

    # Check that the input is array-like and convertible to floats
    try:
        directions = np.array(directions, dtype=float)
    except:
        raise ValueError(f"directions is not array-like: {directions}.")

    # Check that the last dimension is 3
    if directions.shape[-1] != 3:
        raise ValueError(
            f"directions has to have last dimension of size 3, "
            f"got {directions.shape[-1]}."
        )

    # Make the input array to have (I,3) shape for I = 1
    if n_spins == 1 and directions.shape == (3,):
        directions = np.array([directions])

    # Check that right amount of direction vectors is given
    if n_spins != directions.shape[0]:
        raise ValueError(
            f"Expected {n_spins} direction vectors, " f"got {directions.shape[0]}."
        )

    # Ensure shape of the form (I,3)
    if directions.shape != (n_spins, 3):
        raise ValueError(
            f"Expected direction vectors to have shape ({n_spins}, 3), "
            f"got {directions.shape}."
        )

    # Normalize direction vectors
    _logger.debug(
        f"Normalized directions, pre-normalized length minimum: "
        f"{np.linalg.norm(directions, axis=1).min():.10f} "
        f"maximum: {np.linalg.norm(directions, axis=1).max():.10f}."
    )
    directions /= np.linalg.norm(directions, axis=1)[..., np.newaxis]

    return directions


def _check_cone_axis(cone_axis):
    r"""
    Check the input correctness for the cone axis and normalize it.

    Parameters
    ----------
    cone_axis : (3,) |array-like|_
        Axis of the spiral cone rotation.

    Raises
    ------
    ValueError
        If the input is not correct.

    Returns
    -------
    cone_axis : (3,) :numpy:`ndarray`
        Normalized cone axis.
    """

    # Check that the input is array-like and convertible to floats
    try:
        cone_axis = np.array(cone_axis, dtype=float)
    except:
        raise ValueError(f"cone_axis is not array-like: {cone_axis}.")

    # Check that the shape and size are correct
    if cone_axis.shape != (3,):
        raise ValueError(f"cone_axis has to have shape (3,), got {cone_axis.shape}.")

    # Normalize cone axis
    _logger.debug(
        f"Normalize cone axis, pre-normalized length "
        f"maximum: {np.linalg.norm(cone_axis):.10f}."
    )
    cone_axis /= np.linalg.norm(cone_axis)

    return cone_axis


def _check_spiral_vector(spiral_vector):
    r"""
    Check the input correctness for the spiral vector.

    Parameters
    ----------
    spiral_vector : (3,) |array-like|_
        Spiral vector.

    Raises
    ------
    ValueError
        If the input is not correct.

    Returns
    -------
    spiral_vector : (3,) :numpy:`ndarray`
        Spiral vector.
    """

    # Check that the input is array-like and convertible to floats
    try:
        spiral_vector = np.array(spiral_vector, dtype=float)
    except:
        raise ValueError(f"spiral_vector is not array-like: {spiral_vector}.")

    # Check that the shape and size are correct
    if spiral_vector.shape != (3,):
        raise ValueError(
            f"spiral_vector has to have shape (3,), got {spiral_vector.shape}."
        )

    return spiral_vector
