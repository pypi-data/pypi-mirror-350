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

from magnopy.energy.checkers import (
    _check_cone_axis,
    _check_directions,
    _check_spiral_vector,
)
from magnopy.energy.optimize import _bfgs as _optimize
from magnopy.spinham.hamiltonian import SpinHamiltonian
from magnopy.units.inside import ENERGY
from magnopy.units.si import BOHR_MAGNETON

_logger = logging.getLogger(__name__)

__all__ = ["C1", "C2", "C5"]  # , "C3", "C4"]

# Convert to the internal units of energy
BOHR_MAGNETON = BOHR_MAGNETON / ENERGY


class _Energy:
    r"""
    Generic energy class.
    """

    def __init__(self, spinham: SpinHamiltonian):
        self._magnetic_field = None
        # Parameters of the Hamiltonian, private
        self._atom_indices = dict(
            [(atom, i) for i, atom in enumerate(spinham.magnetic_atoms)]
        )
        self._g_factors = [atom.g_factor for atom in spinham.magnetic_atoms]
        self._spins = [atom.spin for atom in spinham.magnetic_atoms]

        self._I = len(self._spins)

        self._cell = spinham.cell

        # Force double counting notation
        previous_dc = spinham.double_counting
        previous_factor = spinham.exchange_factor
        previous_spin_normalized = spinham.spin_normalized
        spinham.double_counting = True
        spinham.exchange_factor = 0.5
        spinham.spin_normalized = True

        # Get all bonds of the Hamiltonian.
        self._bonds = []
        for atom1, atom2, R, J in spinham.exchange_like:
            i = self._atom_indices[atom1]
            j = self._atom_indices[atom2]
            d = R @ spinham.cell
            self._bonds.append([i, j, d, J])

        # Return original notation of SpinHamiltonian
        spinham.double_counting = previous_dc
        spinham.exchange_factor = previous_factor
        spinham.spin_normalized = previous_spin_normalized

    @property
    def magnetic_field(self):
        r"""
        Magnetic field vector.
        """
        return self._magnetic_field

    @magnetic_field.setter
    def magnetic_field(self, new_value):
        # Check that the input is array-like and convertible to floats
        try:
            new_value = np.array(new_value, dtype=float)
        except:
            raise ValueError(f"Magnetic field is not array-like: {new_value}.")

        # Check that the shape and size are correct
        if new_value.shape != (3,):
            raise ValueError(
                f"Magnetic field has to have shape (3,), got {new_value.shape}."
            )

        self._magnetic_field = new_value

    @property
    def spiral_vector(self):
        raise RuntimeError(
            f"Discrete spiral vector is not defined for the energy type "
            f"{self.__class__.__name__}."
        )

    @spiral_vector.setter
    def spiral_vector(self, new_value):
        raise RuntimeError(
            f"Discrete spiral vector is not defined for the energy type "
            f"{self.__class__.__name__}."
        )

    def energy(*args, **kwargs):
        raise NotImplementedError

    def gradient(*args, **kwargs):
        raise NotImplementedError

    def _F(*args, **kwargs):
        raise NotImplementedError

    def _grad_F(*args, **kwargs):
        raise NotImplementedError

    def _to_x(true_variables):
        raise NotImplementedError

    def _update(true_variables, x):
        raise NotImplementedError

    def _update_difference(func_k, func_kp1, grad_kp1):
        raise NotImplementedError

    def optimize(*args, **kwargs):
        raise NotImplementedError


class C1(_Energy):
    def __init__(self, spinham: SpinHamiltonian):
        super().__init__(spinham)

        self.J = np.zeros((self._I, self._I, 3, 3), dtype=float)

        for i, j, _, J in self._bonds:
            self.J[i, j] += J.matrix

    def energy(self, directions, check_input=True) -> float:
        r"""
        Compute the energy of the system with respect to the provided directions of
        spins. Computed according to the formula FIXME of FIXME.

        Parameters
        ----------
        directions : (I, 3) or (3,) |array-like|_
            Orientation of the spin vectors.
            If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are accepted.
            The vectors are normalized to one, i.e. only the direction of the vectors
            is important.
        check_input : bool, default=True
            Whether to check the correctness of the input. Better keep it ``True``
            always, unless you need to compute energy thousands of times and you control
            the input correctness externally.

        Returns
        -------
        energy : float
            Energy of the system.
        """

        if check_input:
            directions = _check_directions(self._I, directions)

        energy = 0

        # Compute exchange and single-ion-like anisotropy energy
        energy += 0.5 * np.einsum(
            "i,j,ix,jy,ijxy",
            self._spins,
            self._spins,
            directions,
            directions,
            self.J,
        )

        # Compute zeeman energy
        if self.magnetic_field is not None:
            energy += BOHR_MAGNETON * np.einsum(
                "i,i,j,ij",
                self._g_factors,
                self._spins,
                self.magnetic_field,
                directions,
            )

        return energy

    def gradient(self, directions, check_input=True) -> np.ndarray:
        r"""
        Compute the gradient of the energy with respect to the provided directions of
        spins. Computed according to the formula FIXME of FIXME.

        Parameters
        ----------
        directions : (I, 3) or (3,) |array-like|_
            Orientation of the spin vectors.
            If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are accepted.
            The vectors are normalized to one, i.e. only the direction of the vectors
            is important.
        check_input : bool, default=True
            Whether to check the correctness of the input. Better keep it ``True``
            always, unless you need to compute energy thousands of times and you control
            the input correctness externally.

        Returns
        -------
        gradient : (I,3) :numpy:`ndarray`
            Gradient of the energy. Form:

            .. code-block:: python

                [
                    [ dE/de1x, dE/de1y, dE/de1z ],
                    [ dE/de2x, dE/de2y, dE/de2z ],
                    ...
                    [ dE/deIx, dE/deIy, dE/deIz ]
                ]
        """

        if check_input:
            directions = _check_directions(self._I, directions)

        gradient = np.zeros_like(directions, dtype=float)

        # Derivative of the Zeeman term
        if self.magnetic_field is not None:
            gradient += BOHR_MAGNETON * np.einsum(
                "b,b,x->bx",
                self._g_factors,
                self._spins,
                self.magnetic_field,
            )

        # Derivative of bilinear term
        gradient += np.einsum(
            "ak,a,b,abkx->bx",
            directions,
            self._spins,
            self._spins,
            self.J,
        )

        return gradient

    def _F(self, true_variables) -> float:
        # Remove input check as this function is specific for the minimization procedure
        return self.energy(true_variables, check_input=False)

    def _grad_F(self, true_variables) -> np.ndarray:
        r"""
        Compute the gradient of the energy as a function of
        :math:`(a^x_1, a^y_1, a^z_1, ..., a^x_I, a^y_I, a^z_I)` for the C1 sub-type.

        Parameters
        ----------
        true_variables : (I, 3) :numpy:`ndarray`
            Directions of the spin vectors.

        Returns
        -------
        gradient : (I*3,) :numpy:`ndarray`
            Gradient of the energy. Form:

            .. code-block:: python

                [ dF/da1x, dF/da1y, dF/da1z, ..., dF/daIx, dF/daIy, dF/daIz ]
        """

        directions = true_variables

        # Remove input check as this function is specific for the minimization procedure
        gradient = self.gradient(directions, check_input=False)

        torque = np.cross(directions, gradient)

        return torque.flatten()

    def _to_x(self, true_variables):
        r"""

        Parameters
        ----------
        true_variables : (I, 3) :numpy:`ndarray`
            Original direction of the spin vectors.

        Returns
        -------
        x : (I*3,) :numpy:`ndarray`
            Direction of the spin vectors parameterized with the skew-symmetric matrix.
        """

        return np.zeros(true_variables.size, dtype=float)

    def _update(self, true_variables, x):
        r"""

        Parameters
        ----------
        true_variables : (I, 3) :numpy:`ndarray`
            Original direction of the spin vectors.
        x : (I*3,) :numpy:`ndarray`
            Direction of the spin vectors parameterized with the skew-symmetric matrix.

        Returns
        -------
        directions : (I, 3) :numpy:`ndarray`
            Rotated set of direction vectors.
        """

        directions = true_variables.copy()

        ax = x[::3]
        ay = x[1::3]
        az = x[2::3]

        thetas = np.sqrt(ax**2 + ay**2 + az**2)

        r = []
        for i in range(len(thetas)):
            theta = thetas[i]

            if theta < np.finfo(float).eps:
                continue

            r = np.array([ax[i], ay[i], az[i]]) / theta

            directions[i] = (
                np.cos(theta) * directions[i]
                + np.sin(theta) * np.cross(r, directions[i])
                + (1 - np.cos(theta)) * r * (r @ directions[i])
            )

        return directions

    def _update_difference(self, func_k, func_kp1, grad_kp1):
        r"""
        Computes the difference between two consecutive steps of the optimization.

        Parameters
        ----------
        func_k : float
            Energy at the current step.
        func_kp1 : float
            Energy at the next step.
        grad_kp1 : (I*3,) :numpy:`ndarray`
            Gradient of the energy at the next state.

        Returns
        -------
        difference : (2,) :numpy:`ndarray`
            Difference between the two consecutive steps of the optimization.
        """

        return np.array(
            [
                abs(func_kp1 - func_k),
                np.linalg.norm(grad_kp1.reshape(grad_kp1.size // 3, 3), axis=1).max(),
            ]
        )

    def _hessian(self, true_variables):
        h = 1e-6

        x_0 = self._to_x(true_variables)

        hessian = np.zeros((x_0.size, x_0.size), dtype=float)

        for i in range(x_0.size):
            for j in range(x_0.size):
                x_pp = x_0.copy()
                x_pm = x_0.copy()
                x_mp = x_0.copy()
                x_mm = x_0.copy()

                x_pp[i] += h
                x_pp[j] += h

                x_pm[i] += h
                x_pm[j] -= h

                x_mp[i] -= h
                x_mp[j] += h

                x_mm[i] -= h
                x_mm[j] -= h

                tv_pp = self._update(true_variables, x_pp)
                tv_pm = self._update(true_variables, x_pm)
                tv_mp = self._update(true_variables, x_mp)
                tv_mm = self._update(true_variables, x_mm)

                hessian[i, j] = (
                    (self._F(tv_pp) - self._F(tv_pm) - self._F(tv_mp) + self._F(tv_mm))
                    / 4
                    / h
                    / h
                )

        return hessian

    def optimize(
        self, directions_ig=None, energy_tolerance=1e-5, torque_tolerance=1e-5
    ):
        r"""
        Optimize the energy with respect to the directions of spins in the unit cell.

        Parameters
        ----------
        directions_ig : (I, 3) or (3,) |array-like|_, optional
            Initial guess for the direction of the spin vectors.
        energy_tolerance : float, default 1e-5
            Energy tolerance for the two consecutive steps of the optimization.
        torque_tolerance : float, default 1e-5
            Torque tolerance for the two consecutive steps of the optimization.

        Returns
        -------
        optimized_directions : (I, 3) :numpy:`ndarray`
            Optimized direction of the spin vectors.
        """

        if directions_ig is None:
            directions_ig = np.random.uniform(low=-1, high=1, size=(self._I, 3))
            _logger.debug("Initial guess for the optimization is random (C1).")

        # Check the input correctness and normalize vectors.
        directions = _check_directions(self._I, directions_ig)

        hessian = self._hessian(directions)

        print(hessian)

        optimized_directions = _optimize(
            self,
            true_variables_0=directions,
            hessian_0=hessian,
            tolerance=np.array([energy_tolerance, torque_tolerance]),
            func=self._F,
            grad=self._grad_F,
            update=self._update,
            to_x=self._to_x,
            update_difference=self._update_difference,
        )

        return optimized_directions


class C2(_Energy):
    def __init__(self, spinham: SpinHamiltonian):
        super().__init__(spinham)

        self._spiral_vector = None
        self.spiral_vector = np.ones(3, dtype=float) / 2

    @property
    def spiral_vector(self):
        return self._spiral_vector

    @spiral_vector.setter
    def spiral_vector(self, new_value):
        # Check that the input is array-like and convertible to floats
        try:
            new_value = np.array(new_value, dtype=float)
        except:
            raise ValueError(f"spiral_vector is not array-like: {new_value}.")

        # Check that the shape and size are correct
        if new_value.shape != (3,):
            raise ValueError(
                f"spiral_vector has to have shape (3,), got {new_value.shape}."
            )

        self._spiral_vector = new_value

    def energy(self, directions, cone_axis, check_input=True) -> float:
        r"""
        Compute the energy of the system with respect to the provided directions of
        spins, cone axis and spiral vector. Computed according to the formula FIXME of FIXME.

        Parameters
        ----------
        directions : (I, 3) or (3,) |array-like|_
            Orientation of the spin vectors.
            If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are accepted.
            The vectors are normalized to one, i.e. only the direction of the vectors
            is important.
        cone_axis : (3,) |array-like|_
            Cone axis of the spiral cone state.
        check_input : bool, default=True
            Whether to check the correctness of the input. Better keep it ``True``
            always, unless you need to compute energy thousands of times and you control
            the input correctness externally.

        Returns
        -------
        energy : float
            Energy of the system.
        """

        if check_input:
            directions = _check_directions(self._I, directions)
            cone_axis = _check_cone_axis(cone_axis=cone_axis)

        energy = 0

        T = np.eye(3, dtype=float) - np.outer(cone_axis, cone_axis)
        P = np.array(
            [
                [0, cone_axis[2], -cone_axis[1]],
                [-cone_axis[2], 0, cone_axis[0]],
                [cone_axis[1], -cone_axis[0], 0],
            ],
            dtype=float,
        )

        for i, j, R, J in self._bonds:
            sin_qr = np.sin(2 * np.pi * (self.spiral_vector @ R))
            cos_qr = np.cos(2 * np.pi * (self.spiral_vector @ R))
            T_nu = -sin_qr * P + cos_qr * T
            P_nu = sin_qr * T + cos_qr * P
            energy += (
                0.5
                * self._spins[i]
                * self._spins[j]
                * (
                    (cone_axis @ directions[i])
                    * (cone_axis @ J.matrix @ cone_axis)
                    * (cone_axis @ directions[j])
                    + (
                        np.einsum(
                            "i,j,kl,ki,lj",
                            directions[i],
                            directions[j],
                            J.matrix,
                            T,
                            T_nu,
                        )
                    )
                )
            )

        # Compute zeeman energy
        if self.magnetic_field is not None:
            hn = self.magnetic_field @ cone_axis
            for i in range(self._I):
                energy += (
                    BOHR_MAGNETON
                    * self._g_factors[i]
                    * hn
                    * self._spins[i]
                    * (cone_axis @ directions[i])
                )

        return energy

    def gradient(self, directions, cone_axis, check_input=True) -> np.ndarray:
        r"""
        Compute the gradient of the energy with respect to the provided directions of
        spins. Computed according to the formula FIXME of FIXME.

        Parameters
        ----------
        directions : (I, 3) or (3,) |array-like|_
            Orientation of the spin vectors.
            If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are accepted.
            The vectors are normalized to one, i.e. only the direction of the vectors
            is important.
        cone_axis : (3,) |array-like|_
            Cone axis of the spiral cone state.
        check_input : bool, default=True
            Whether to check the correctness of the input. Better keep it ``True``
            always, unless you need to compute energy thousands of times and you control
            the input correctness externally.

        Returns
        -------
        gradient : (I,3) :numpy:`ndarray`
            Gradient of the energy. Form:

            .. code-block:: python

                [
                    [ dE/de1x, dE/de1y, dE/de1z ],
                    [ dE/de2x, dE/de2y, dE/de2z ],
                    ...
                    [ dE/deIx, dE/deIy, dE/deIz ],
                    [dE/dnx, dE/dny, dE/dnz]
                ]
        """

        if check_input:
            directions = _check_directions(self._I, directions)
            cone_axis = _check_cone_axis(cone_axis=cone_axis)

        gradient = np.zeros((self._I + 1, 3), dtype=float)

        T = np.eye(3, dtype=float) - np.outer(cone_axis, cone_axis)
        P = np.array(
            [
                [0, cone_axis[2], -cone_axis[1]],
                [-cone_axis[2], 0, cone_axis[0]],
                [cone_axis[1], -cone_axis[0], 0],
            ],
            dtype=float,
        )
        for i, j, R, J in self._bonds:
            sin_qr = np.sin(2 * np.pi * (self.spiral_vector @ R))
            cos_qr = np.cos(2 * np.pi * (self.spiral_vector @ R))
            T_nu = -sin_qr * P + cos_qr * T
            P_nu = sin_qr * T + cos_qr * P

            gradient[j] += (
                self._spins[i]
                * self._spins[j]
                * (
                    (cone_axis @ directions[i])
                    * (cone_axis @ J.matrix @ cone_axis)
                    * cone_axis
                    + cos_qr
                    * (np.einsum("i,kl,ki,lx->x", directions[i], J.matrix, T, T))
                )
            )

            gradient[-1] += (
                self._spins[i]
                * self._spins[j]
                * np.einsum(
                    "k,kx->x",
                    (
                        cone_axis * (cone_axis @ directions[i])
                        - cos_qr * np.einsum("ki,i->k", T, directions[i])
                    ),
                    (
                        np.einsum("x,kj,j->kx", directions[j], J.matrix, cone_axis)
                        + np.einsum("j,kx,j->kx", directions[j], J.matrix, cone_axis)
                    ),
                )
            )

        # Zeeman
        if self.magnetic_field is not None:
            hn = self.magnetic_field @ cone_axis
            for i in range(self._I):
                gradient[i] = (
                    BOHR_MAGNETON * self._g_factors[i] * self._spins * hn * cone_axis
                )

                gradient[-1] += (
                    BOHR_MAGNETON
                    * self._g_factors[i]
                    * self._spins[i]
                    * (
                        self.magnetic_field * (cone_axis @ directions[i])
                        + directions[i] * hn
                    )
                )

        return gradient

    def _F(self, true_variables) -> float:
        # Remove input check as this function is specific for the minimization procedure
        return self.energy(
            directions=true_variables[0],
            cone_axis=true_variables[1],
            check_input=False,
        )

    def _grad_F(self, true_variables) -> np.ndarray:
        r"""
        Compute the gradient of the energy as a function of
        :math:`(a^x_1, a^y_1, a^z_1, ..., a^x_I, a^y_I, a^z_I)` for the C1 sub-type.

        Parameters
        ----------
        true_variables : (I, 3) :numpy:`ndarray`
            Directions of the spin vectors.

        Returns
        -------
        gradient : (I*3,) :numpy:`ndarray`
            Gradient of the energy. Form:

            .. code-block:: python

                [ dF/da1x, dF/da1y, dF/da1z, ..., dF/daIx, dF/daIy, dF/daIz ]
        """

        directions = true_variables[0]
        cone_axis = true_variables[1]

        # Remove input check as this function is specific for the minimization procedure
        gradient = self.gradient(directions, cone_axis, check_input=False)

        torque_directions = np.cross(directions, gradient[:-1])
        torque_cone_axis = np.cross(cone_axis, gradient[-1])

        new_grad = np.zeros(3 * gradient.shape[0], dtype=float)
        new_grad[:-3] = torque_directions.flatten()
        new_grad[-3:] = torque_cone_axis

        return new_grad

    def _to_x(self, true_variables):
        r"""

        Parameters
        ----------
        true_variables : (I, 3) :numpy:`ndarray`
            Original direction of the spin vectors.

        Returns
        -------
        x : ((I+2)*3,) :numpy:`ndarray`
            Direction of the spin vectors parameterized with the skew-symmetric matrix.
        """

        return np.zeros(true_variables[0].size + 3, dtype=float)

    def _update(self, true_variables, x):
        r"""

        Parameters
        ----------
        true_variables : (I, 3) :numpy:`ndarray`
            Original direction of the spin vectors.
        x : (I*3,) :numpy:`ndarray`
            Direction of the spin vectors parameterized with the skew-symmetric matrix.

        Returns
        -------
        directions : (I, 3) :numpy:`ndarray`
            Rotated set of direction vectors.
        """

        directions = true_variables[0].copy()

        ax = x[:-6:3]
        ay = x[1:-6:3]
        az = x[2:-6:3]

        thetas = np.sqrt(ax**2 + ay**2 + az**2)

        for i in range(len(thetas)):
            theta = thetas[i]

            if theta < np.finfo(float).eps:
                continue

            r = np.array([ax[i], ay[i], az[i]]) / theta

            directions[i] = (
                np.cos(theta) * directions[i]
                + np.sin(theta) * np.cross(r, directions[i])
                + (1 - np.cos(theta)) * r * (r @ directions[i])
            )

        cone_axis = true_variables[1].copy()

        ax = x[-6]
        ay = x[-5]
        az = x[-4]

        theta = np.sqrt(ax**2 + ay**2 + az**2)

        if not (theta < np.finfo(float).eps):
            r = np.array([ax, ay, az]) / theta

            cone_axis = (
                np.cos(theta) * cone_axis
                + np.sin(theta) * np.cross(r, cone_axis)
                + (1 - np.cos(theta)) * r * (r @ cone_axis)
            )

        return [directions, cone_axis]

    def _update_difference(self, func_k, func_kp1, grad_kp1):
        r"""
        Computes the difference between two consecutive steps of the optimization.

        Parameters
        ----------
        func_k : float
            Energy at the current step.
        func_kp1 : float
            Energy at the next step.
        grad_kp1 : (I*3,) :numpy:`ndarray`
            Gradient of the energy at the next state.

        Returns
        -------
        difference : (2,) :numpy:`ndarray`
            Difference between the two consecutive steps of the optimization.
        """

        grad_directions = grad_kp1[:-6]
        grad_cone_axis = grad_kp1[-6:-3]
        return np.array(
            [
                abs(func_kp1 - func_k),
                np.linalg.norm(
                    grad_directions.reshape(grad_directions.size // 3, 3), axis=1
                ).max(),
                np.linalg.norm(grad_cone_axis),
            ]
        )

    def optimize(
        self,
        directions_ig=None,
        cone_axis_ig=None,
        energy_tolerance=1e-5,
        torque_tolerance=1e-5,
        ca_torque_tolerance=1e-5,
    ):
        r"""
        Optimize the energy with respect to the directions of spins in the unit cell.

        Parameters
        ----------
        directions_ig : (I, 3) or (3,) |array-like|_, optional
            Initial guess for the direction of the spin vectors.
        energy_tolerance : float, default 1e-5
            Energy tolerance for the two consecutive steps of the optimization.
        torque_tolerance : float, default 1e-5
            Torque tolerance for the two consecutive steps of the optimization.


        Returns
        -------
        optimized_directions : (I, 3) :numpy:`ndarray`
            Optimized direction of the spin vectors.
        """

        if directions_ig is None:
            directions_ig = np.random.uniform(low=-1, high=1, size=(self._I, 3))
            _logger.debug("Initial guess for the optimization is random (C5).")

        if cone_axis_ig is None:
            cone_axis_ig = np.random.uniform(low=-1, high=1, size=3)

        # Check the input correctness and normalize vectors.
        directions = _check_directions(self._I, directions_ig)

        cone_axis = _check_cone_axis(cone_axis=cone_axis_ig)

        optimized_directions = _optimize(
            self,
            true_variables_0=[directions, cone_axis],
            tolerance=np.array(
                [energy_tolerance, torque_tolerance, ca_torque_tolerance]
            ),
            func=self._F,
            grad=self._grad_F,
            update=self._update,
            to_x=self._to_x,
            update_difference=self._update_difference,
        )

        return optimized_directions


class C5(_Energy):
    def __init__(self, spinham: SpinHamiltonian):
        super().__init__(spinham)

    def energy(self, directions, cone_axis, spiral_vector, check_input=True) -> float:
        r"""
        Compute the energy of the system with respect to the provided directions of
        spins, cone axis and spiral vector. Computed according to the formula FIXME of FIXME.

        Parameters
        ----------
        directions : (I, 3) or (3,) |array-like|_
            Orientation of the spin vectors.
            If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are accepted.
            The vectors are normalized to one, i.e. only the direction of the vectors
            is important.
        cone_axis : (3,) |array-like|_
            Cone axis of the spiral cone state.
        spiral_vector : (3,) |array-like|_
            Spiral vector of the spiral cone state.
            Relative to the three reciprocal lattice vectors.
        check_input : bool, default=True
            Whether to check the correctness of the input. Better keep it ``True``
            always, unless you need to compute energy thousands of times and you control
            the input correctness externally.

        Returns
        -------
        energy : float
            Energy of the system.
        """

        if check_input:
            directions = _check_directions(self._I, directions)
            cone_axis = _check_cone_axis(cone_axis=cone_axis)
            spiral_vector = _check_spiral_vector(spiral_vector=spiral_vector)

        energy = 0

        T = np.eye(3, dtype=float) - np.outer(cone_axis, cone_axis)
        P = np.array(
            [
                [0, cone_axis[2], -cone_axis[1]],
                [-cone_axis[2], 0, cone_axis[0]],
                [cone_axis[1], -cone_axis[0], 0],
            ],
            dtype=float,
        )

        for i, j, R, J in self._bonds:
            sin_qr = np.sin(2 * np.pi * (spiral_vector @ R))
            cos_qr = np.cos(2 * np.pi * (spiral_vector @ R))
            T_nu = -sin_qr * P + cos_qr * T
            P_nu = sin_qr * T + cos_qr * P
            energy += (
                0.5
                * self._spins[i]
                * self._spins[j]
                * (
                    (cone_axis @ directions[i])
                    * (cone_axis @ J.matrix @ cone_axis)
                    * (cone_axis @ directions[j])
                    + 0.5
                    * (
                        np.einsum(
                            "i,j,kl,ki,lj",
                            directions[i],
                            directions[j],
                            J.matrix,
                            T,
                            T_nu,
                        )
                        + np.einsum(
                            "i,j,kl,ki,lj",
                            directions[i],
                            directions[j],
                            J.matrix,
                            P,
                            P_nu,
                        )
                    )
                )
            )

        # Compute zeeman energy
        if self.magnetic_field is not None:
            hn = self.magnetic_field @ cone_axis
            for i in range(self._I):
                energy += (
                    BOHR_MAGNETON
                    * self._g_factors[i]
                    * hn
                    * self._spins[i]
                    * (cone_axis @ directions[i])
                )

        return energy

    def gradient(
        self, directions, cone_axis, spiral_vector, check_input=True
    ) -> np.ndarray:
        r"""
        Compute the gradient of the energy with respect to the provided directions of
        spins. Computed according to the formula FIXME of FIXME.

        Parameters
        ----------
        directions : (I, 3) or (3,) |array-like|_
            Orientation of the spin vectors.
            If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are accepted.
            The vectors are normalized to one, i.e. only the direction of the vectors
            is important.
        cone_axis : (3,) |array-like|_
            Cone axis of the spiral cone state.
        spiral_vector : (3,) |array-like|_
            Spiral vector of the spiral cone state.
            Relative to the three reciprocal lattice vectors.
        check_input : bool, default=True
            Whether to check the correctness of the input. Better keep it ``True``
            always, unless you need to compute energy thousands of times and you control
            the input correctness externally.

        Returns
        -------
        gradient : (I,3) :numpy:`ndarray`
            Gradient of the energy. Form:

            .. code-block:: python

                [
                    [ dE/de1x, dE/de1y, dE/de1z ],
                    [ dE/de2x, dE/de2y, dE/de2z ],
                    ...
                    [ dE/deIx, dE/deIy, dE/deIz ],
                    [dE/dnx, dE/dny, dE/dnz],
                    [dE/dqx, dE/dqy, dE/dqz],
                ]
        """

        if check_input:
            directions = _check_directions(self._I, directions)
            cone_axis = _check_cone_axis(cone_axis=cone_axis)
            spiral_vector = _check_spiral_vector(spiral_vector=spiral_vector)

        gradient = np.zeros((self._I + 2, 3), dtype=float)

        T = np.eye(3, dtype=float) - np.outer(cone_axis, cone_axis)
        P = np.array(
            [
                [0, cone_axis[2], -cone_axis[1]],
                [-cone_axis[2], 0, cone_axis[0]],
                [cone_axis[1], -cone_axis[0], 0],
            ],
            dtype=float,
        )
        for i, j, R, J in self._bonds:
            sin_qr = np.sin(2 * np.pi * (spiral_vector @ R))
            cos_qr = np.cos(2 * np.pi * (spiral_vector @ R))
            T_nu = -sin_qr * P + cos_qr * T
            P_nu = sin_qr * T + cos_qr * P

            gradient[j] += (
                self._spins[i]
                * self._spins[j]
                * (
                    (cone_axis @ directions[i])
                    * (cone_axis @ J.matrix @ cone_axis)
                    * cone_axis
                    + 0.5
                    * (
                        np.einsum("i,kl,ki,lx->x", directions[i], J.matrix, T, T_nu)
                        + np.einsum("i,kl,ki,lx->x", directions[i], J.matrix, P, P_nu)
                    )
                )
            )

            gradient[-2] += (
                self._spins[i]
                * self._spins[j]
                * (
                    np.einsum(
                        "xl,l->x",
                        (
                            np.einsum("x,k,kl->xl", directions[i], cone_axis, J.matrix)
                            + np.einsum(
                                "k,k,xl->xl", directions[i], cone_axis, J.matrix
                            )
                        ),
                        (
                            cone_axis * (cone_axis @ directions[j])
                            - 0.5 * np.einsum("lj,j->l", T_nu, directions[j])
                        ),
                    )
                    - np.cross(
                        directions[i],
                        np.einsum("kl,lj,j -> k", J.matrix, P_nu, directions[j]),
                    )
                )
            )

            gradient[-1] += (
                0.25
                * self._spins[i]
                * self._spins[j]
                * (R @ self._cell)
                * (
                    np.einsum(
                        "i,j,kl,ki,lj", directions[i], directions[j], J.matrix, P, T_nu
                    )
                    - np.einsum(
                        "i,j,kl,ki,lj", directions[i], directions[j], J.matrix, T, P_nu
                    )
                )
            )

        # Zeeman
        if self.magnetic_field is not None:
            hn = self.magnetic_field @ cone_axis
            for i in range(self._I):
                gradient[i] = (
                    BOHR_MAGNETON * self._g_factors[i] * self._spins * hn * cone_axis
                )

                gradient[-2] += (
                    BOHR_MAGNETON
                    * self._g_factors[i]
                    * self._spins[i]
                    * (
                        self.magnetic_field * (cone_axis @ directions[i])
                        + directions[i] * hn
                    )
                )

        return gradient

    def _F(self, true_variables) -> float:
        # Remove input check as this function is specific for the minimization procedure
        return self.energy(
            directions=true_variables[0],
            cone_axis=true_variables[1],
            spiral_vector=true_variables[2],
            check_input=False,
        )

    def _grad_F(self, true_variables) -> np.ndarray:
        r"""
        Compute the gradient of the energy as a function of
        :math:`(a^x_1, a^y_1, a^z_1, ..., a^x_I, a^y_I, a^z_I)` for the C1 sub-type.

        Parameters
        ----------
        true_variables : (I, 3) :numpy:`ndarray`
            Directions of the spin vectors.

        Returns
        -------
        gradient : (I*3,) :numpy:`ndarray`
            Gradient of the energy. Form:

            .. code-block:: python

                [ dF/da1x, dF/da1y, dF/da1z, ..., dF/daIx, dF/daIy, dF/daIz ]
        """

        directions = true_variables[0]
        cone_axis = true_variables[1]
        spiral_vector = true_variables[2]

        # Remove input check as this function is specific for the minimization procedure
        gradient = self.gradient(
            directions, cone_axis, spiral_vector, check_input=False
        )

        torque_directions = np.cross(directions, gradient[:-2])
        torque_cone_axis = np.cross(cone_axis, gradient[-2])

        new_grad = np.zeros(3 * gradient.shape[0], dtype=float)
        new_grad[:-6] = torque_directions.flatten()
        new_grad[-6:-3] = torque_cone_axis
        new_grad[-3:] = gradient[-1]

        return new_grad

    def _to_x(self, true_variables):
        r"""

        Parameters
        ----------
        true_variables : (I, 3) :numpy:`ndarray`
            Original direction of the spin vectors.

        Returns
        -------
        x : ((I+2)*3,) :numpy:`ndarray`
            Direction of the spin vectors parameterized with the skew-symmetric matrix.
        """

        return np.concatenate(
            (np.zeros(true_variables[0].size + 3, dtype=float), true_variables[-1])
        )

    def _update(self, true_variables, x):
        r"""

        Parameters
        ----------
        true_variables : (I, 3) :numpy:`ndarray`
            Original direction of the spin vectors.
        x : (I*3,) :numpy:`ndarray`
            Direction of the spin vectors parameterized with the skew-symmetric matrix.

        Returns
        -------
        directions : (I, 3) :numpy:`ndarray`
            Rotated set of direction vectors.
        """

        directions = true_variables[0].copy()

        ax = x[:-6:3]
        ay = x[1:-6:3]
        az = x[2:-6:3]

        thetas = np.sqrt(ax**2 + ay**2 + az**2)

        for i in range(len(thetas)):
            theta = thetas[i]

            if theta < np.finfo(float).eps:
                continue

            r = np.array([ax[i], ay[i], az[i]]) / theta

            directions[i] = (
                np.cos(theta) * directions[i]
                + np.sin(theta) * np.cross(r, directions[i])
                + (1 - np.cos(theta)) * r * (r @ directions[i])
            )

        cone_axis = true_variables[1].copy()

        ax = x[-6]
        ay = x[-5]
        az = x[-4]

        theta = np.sqrt(ax**2 + ay**2 + az**2)

        if not (theta < np.finfo(float).eps):
            r = np.array([ax, ay, az]) / theta

            cone_axis = (
                np.cos(theta) * cone_axis
                + np.sin(theta) * np.cross(r, cone_axis)
                + (1 - np.cos(theta)) * r * (r @ cone_axis)
            )

        spiral_vector = true_variables[2] + x[-3:]

        return [directions, cone_axis, spiral_vector]

    def _update_difference(self, func_k, func_kp1, grad_kp1):
        r"""
        Computes the difference between two consecutive steps of the optimization.

        Parameters
        ----------
        func_k : float
            Energy at the current step.
        func_kp1 : float
            Energy at the next step.
        grad_kp1 : (I*3,) :numpy:`ndarray`
            Gradient of the energy at the next state.

        Returns
        -------
        difference : (2,) :numpy:`ndarray`
            Difference between the two consecutive steps of the optimization.
        """

        grad_directions = grad_kp1[:-6]
        grad_cone_axis = grad_kp1[-6:-3]
        return np.array(
            [
                abs(func_kp1 - func_k),
                np.linalg.norm(
                    grad_directions.reshape(grad_directions.size // 3, 3), axis=1
                ).max(),
                np.linalg.norm(grad_cone_axis),
            ]
        )

    def optimize(
        self,
        directions_ig=None,
        cone_axis_ig=None,
        spiral_vector_ig=None,
        energy_tolerance=1e-5,
        torque_tolerance=1,
        ca_torque_tolerance=1,
    ):
        r"""
        Optimize the energy with respect to the directions of spins in the unit cell.

        Parameters
        ----------
        directions_ig : (I, 3) or (3,) |array-like|_, optional
            Initial guess for the direction of the spin vectors.
        energy_tolerance : float, default 1e-5
            Energy tolerance for the two consecutive steps of the optimization.
        torque_tolerance : float, default 1e-5
            Torque tolerance for the two consecutive steps of the optimization.


        Returns
        -------
        optimized_directions : (I, 3) :numpy:`ndarray`
            Optimized direction of the spin vectors.
        """

        if directions_ig is None:
            directions_ig = np.random.uniform(low=-1, high=1, size=(self._I, 3))
            _logger.debug("Initial guess for the optimization is random (C5).")

        if cone_axis_ig is None:
            cone_axis_ig = np.random.uniform(low=-1, high=1, size=3)

        if spiral_vector_ig is None:
            spiral_vector_ig = np.random.uniform(low=-1, high=1, size=3)

        # Check the input correctness and normalize vectors.
        directions = _check_directions(self._I, directions_ig)

        cone_axis = _check_cone_axis(cone_axis=cone_axis_ig)
        spiral_vector = _check_spiral_vector(spiral_vector=spiral_vector_ig)

        optimized_directions = _optimize(
            self,
            true_variables_0=[directions, cone_axis, spiral_vector],
            tolerance=np.array(
                [energy_tolerance, torque_tolerance, ca_torque_tolerance]
            ),
            func=self._F,
            grad=self._grad_F,
            update=self._update,
            to_x=self._to_x,
            update_difference=self._update_difference,
        )

        return optimized_directions
