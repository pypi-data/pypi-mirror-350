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
from typing import Iterable, Tuple

import numpy as np
from wulfric import TORADIANS, absolute_to_relative

from magnopy.spinham.hamiltonian import SpinHamiltonian
from magnopy.units.inside import ENERGY
from magnopy.units.si import BOHR_MAGNETON

_logger = logging.getLogger(__name__)

__all__ = ["Energy"]

# Convert to the internal units of energy
BOHR_MAGNETON /= ENERGY

################################################################################
#                  Functions that check or make initial guess                  #
#                                                                              #
# The idea is to call it in the generalized way and obtain a vector for the    #
# minimization                                                                 #
#                                                                              #
#                   _starting(n_spins, initial_guess) -> x                     #
#                                                                              #
# Nature of the returned x depends on the type of the ground state (as well    #
# as nature of initial_guess), but nature of x has to match the one of the     #
# corresponding _update function                                               #
################################################################################


def _starting_ferro(n_spins, initial_guess=None):
    # Construct or check initial guess
    if initial_guess is None:
        spin_orientation = np.random.random((n_spins, 3))
    else:
        # Check that the input is correct
        try:
            spin_orientation = np.array(initial_guess, dtype=float)
        except:
            raise ValueError(f"spin_orientation is not array-like: {spin_orientation}")

        if spin_orientation.shape[-1] != 3:
            raise ValueError(
                f"spin_orientation has to have the last dimension of "
                f"size 3, got {spin_orientation.shape[-1]}"
            )

        # Make the input array have (I,3) shape for I = 1
        if n_spins == 1 and spin_orientation.shape == (3,):
            spin_orientation = np.array([spin_orientation])

        if n_spins != spin_orientation.shape[0]:
            raise ValueError(
                f"Expected {n_spins} spins in initial guess, "
                f"got {spin_orientation.shape[0]}"
            )

    for i in range(n_spins):
        spin_orientation[i] /= np.linalg.norm(spin_orientation[i])

    return spin_orientation


def _starting_antiferro(n_spins, antiferro_q, initial_guess=None):
    if initial_guess is not None and len(initial_guess) != 2:
        raise ValueError(
            "If initial guess is not None, then tuple with two elements "
            "is expected: (spin_orientation, cone_axis), "
            f"got {len(initial_guess)} elements."
        )

    # Get spin_orientation
    if initial_guess is None or initial_guess[0] is None:
        spin_orientation = _starting_ferro(n_spins)
    else:
        spin_orientation = _starting_ferro(n_spins, initial_guess[0])

    # Get cone_axis
    if initial_guess is None or initial_guess[1] is None:
        cone_axis = np.random.random(3)
    else:
        # Check that the input is correct
        try:
            cone_axis = np.array(initial_guess[1], dtype=float)
        except:
            raise ValueError(
                f"Initial guess for cone_axis is not array-like: " f"{initial_guess[1]}"
            )
        if cone_axis.shape != (3,):
            raise ValueError(
                f"Initial guess for cone_axis should have shape "
                f"of (3,), got: {cone_axis.shape}"
            )

    # Normalize cone axis:
    cone_axis /= np.linalg.norm(cone_axis)

    # Check that the input is correct
    try:
        spiral_vector = np.array(antiferro_q, dtype=float)
    except:
        raise ValueError(f"Spiral_vector is not array-like: " f"{antiferro_q}")
    if spiral_vector.shape != (3,):
        raise ValueError(
            f"Spiral_vector should have shape " f"of (3,), got: {spiral_vector.shape}"
        )

    return [np.concatenate((spin_orientation, [cone_axis]), axis=0), spiral_vector]


def _starting_spiral(n_spins, initial_guess=None):
    if initial_guess is not None and len(initial_guess) != 3:
        raise ValueError(
            "If initial guess is not None, then tuple with three elements "
            "is expected: (spin_orientation, cone_axis, spiral_vector), "
            f"got {len(initial_guess)} elements."
        )

    # Get spin_orientation
    if initial_guess is None or initial_guess[0] is None:
        spin_orientation = _starting_ferro(n_spins)
    else:
        spin_orientation = _starting_ferro(n_spins, initial_guess[0])

    # Get cone_axis
    if initial_guess is None or initial_guess[1] is None:
        cone_axis = np.random.random(3)
    else:
        # Check that the input is correct
        try:
            cone_axis = np.array(initial_guess[1], dtype=float)
        except:
            raise ValueError(
                f"Initial guess for cone_axis is not array-like: " f"{initial_guess[1]}"
            )
        if cone_axis.shape != (3,):
            raise ValueError(
                f"Initial guess for cone_axis should have shape "
                f"of (3,), got: {cone_axis.shape}"
            )

    # Normalize cone axis:
    cone_axis /= np.linalg.norm(cone_axis)

    if initial_guess is None or initial_guess[2] is None:
        spiral_vector = np.random.random(3)
    else:
        # Check that the input is correct
        try:
            spiral_vector = np.array(initial_guess[2], dtype=float)
        except:
            raise ValueError(
                f"Initial guess for spiral_vector is not array-like: "
                f"{initial_guess[2]}"
            )
        if spiral_vector.shape != (3,):
            raise ValueError(
                f"Initial guess for spiral_vector should have shape "
                f"of (3,), got: {spiral_vector.shape}"
            )

    return [np.concatenate((spin_orientation, [cone_axis]), axis=0), spiral_vector]


################################################################################
#                      Functions that update the argument                      #
#                                                                              #
#   The idea is to call it in the generalized way: x_new = _update(x)          #
################################################################################
def _update_x_ferro(x, search_direction, step=1):
    r"""
    Update the variables for the next step in the ferro case.

    Parameters
    ----------
    x : (I, 3) :numpy:`ndarray`
        Orientation of the spin vectors.
    search_direction : (I*3,) :numpy:`ndarray`
        Search direction computed in L-BFGS step
    step : float
        Size of the step along the search direction.
    """
    x = x.copy()
    a12 = search_direction[::3] * step
    a13 = search_direction[1::3] * step
    a23 = search_direction[2::3] * step

    thetas = np.sqrt(a12**2 + a13**2 + a23**2)

    r = []
    for i in range(len(thetas)):
        theta = thetas[i]

        if theta < np.finfo(float).eps:
            continue

        r = (np.array([-a23[i], a13[i], -a12[i]])) / theta

        x[i] = (
            np.cos(theta) * x[i]
            + np.sin(theta) * np.cross(r, x[i])
            + (1 - np.cos(theta)) * r * (r @ x[i])
        )

    return x


def _update_x_antiferro(x, search_direction, step=1):
    r"""
    Update the variables for the next step in the ferro case.

    Parameters
    ----------
    x : list of two elements: (I+1, 3) :numpy:`ndarray` and (3,) :numpy:`ndarray`
        First element:
            * 0 - I-1:  Orientation of the spin vectors
            * I: cone axis
        Second element: spiral vector
    search_direction : (I*3+6,) :numpy:`ndarray`
        Search direction computed in L-BFGS step
    step : float
        Size of the step along the search direction.
    """
    x_0 = x[0].copy()
    x_1 = x[1]
    a12 = search_direction[:-3:3] * step
    a13 = search_direction[1:-3:3] * step
    a23 = search_direction[2:-3:3] * step

    thetas = np.sqrt(a12**2 + a13**2 + a23**2)

    r = []
    for i in range(len(thetas)):
        theta = thetas[i]

        if theta < np.finfo(float).eps:
            continue

        r = (np.array([-a23[i], a13[i], -a12[i]])) / theta

        x_0[i] = (
            np.cos(theta) * x_0[i]
            + np.sin(theta) * np.cross(r, x_0[i])
            + (1 - np.cos(theta)) * r * (r @ x_0[i])
        )

    return [x_0, x_1]


def _update_x_spiral(x, search_direction, step=1):
    r"""
    Update the variables for the next step in the ferro case.

    Parameters
    ----------
    x : list of two elements: (I+1, 3) :numpy:`ndarray` and (3,) :numpy:`ndarray`
        First element:
            * 0 - I-1:  Orientation of the spin vectors
            * I: cone axis
        Second element: spiral vector
    search_direction : (I*3+6,) :numpy:`ndarray`
        Search direction computed in L-BFGS step
    step : float
        Size of the step along the search direction.
    """
    x_0 = x[0].copy()
    x_1 = x[1].copy()
    a12 = search_direction[:-3:3] * step
    a13 = search_direction[1:-3:3] * step
    a23 = search_direction[2:-3:3] * step

    thetas = np.sqrt(a12**2 + a13**2 + a23**2)

    r = []
    for i in range(len(thetas)):
        theta = thetas[i]

        if theta < np.finfo(float).eps:
            continue

        r = (np.array([-a23[i], a13[i], -a12[i]])) / theta

        x_0[i] = (
            np.cos(theta) * x_0[i]
            + np.sin(theta) * np.cross(r, x_0[i])
            + (1 - np.cos(theta)) * r * (r @ x_0[i])
        )

    x_1 += search_direction[-3:] * step

    return [x_0, x_1]


################################################################################
#                      Functions that unpack the argument                      #
#                                                                              #
# The idea is to call it in the generalized way as                             #
#                                                                              #
#                                  _unpack(x)                                  #
#                                                                              #
# and pass the result to the energy or gradient functions:                     #
#                                                                              #
#                  energy(*_unpack(x)) and _grad(*_unpack(x))                  #
################################################################################
def _unpack_ferro(x):
    r"""
    Unpack the coordinate for the feromagnetic case

    Parameters
    ----------
    x : (I, 3) :numpy:`ndarray`
        Orientation of the spin vectors.

    Returns
    -------
    spin_orientation : (I, 3) :numpy:`ndarray`
        Orientation of the spin vectors.
    """
    return (x,)


def _unpack_antiferro(x):
    r"""
    Unpack parameters for the antiferro case.

    Parameters
    ----------
    x : list of two elements: (I+1, 3) :numpy:`ndarray` and (3,) :numpy:`ndarray`
        First element:
            * 0 - I-1:  Orientation of the spin vectors
            * I: cone axis
        Second element: spiral vector

    Returns
    -------
    spin_orientation : (I, 3) :numpy:`ndarray`
        Orientation of the spin vectors.
    cone_axis : (3,)
        Cone axis.
    spiral_vector : (3,)
        Spiral vector.
    """
    return x[0][:-1], x[0][-1], x[1]


def _unpack_spiral(x):
    r"""
    Unpack parameters for the spiral case.

    Parameters
    ----------
    x : list of two elements: (I+1, 3) :numpy:`ndarray` and (3,) :numpy:`ndarray`
        First element:
            * 0 - I-1:  Orientation of the spin vectors
            * I: cone axis
        Second element: spiral vector

    Returns
    -------
    spin_orientation : (I, 3) :numpy:`ndarray`
        Orientation of the spin vectors.
    cone_axis : (3,)
        Cone axis.
    spiral_vector : (3,)
        Spiral vector.
    """
    return x[0][:-1], x[0][-1], x[1]


################################################################################
#                    Functions that compute torque targets                     #
#                                                                              #
# The idea is to call it in the generalized way as                             #
#                                                                              #
#               torque_targets = _compute_torque_targets(torques)              #
################################################################################


def _compute_torque_target_ferro(torques):
    return (np.linalg.norm(torques, axis=1).max(),)


def _compute_torque_target_antiferro(torques):
    return np.linalg.norm(torques[:-1], axis=1).max(), np.linalg.norm(torques[-1])


def _compute_torque_target_spiral(torques):
    return np.linalg.norm(torques[:-1], axis=1).max(), np.linalg.norm(torques[-1])


################################################################################
#                         Functions that output history                        #
################################################################################


def _default_history_processor_ferro(history, filename=None, nspins=None):
    # Output header
    if history is None:
        if nspins is None:
            _logger.error("If history is None, then nspins is required.")
            raise RunTimeError("If history is None, then nspins is required.")
        header = f"{'Energy':>15} {'Torque':>11}"

        for i in range(nspins):
            header += f" {f'S{i+1}_x':>11} {f'S{i+1}_y':>11} {f'S{i+1}_z':>11}"
        if filename is None:
            print(header, flush=True)
        else:
            with open(filename, "a") as file:
                file.write(header)
    else:
        for i in range(len(history)):
            history[i] = (
                f"{history[i][0]:15.8e} "
                + " ".join([f"{a:11.8f}" for a in history[i][1]])
                + " "
                + " ".join([f"{a:11.8f}" for a in history[i][2].flatten()])
            )
        if filename is None:
            print("\n".join(history), flush=True)
        else:
            with open(filename, "a") as file:
                file.write("\n" + "\n".join(history))


def _default_history_processor_antiferro(history, filename=None, nspins=None):
    # Output header
    if history is None:
        if nspins is None:
            _logger.error("If history is None, then nspins is required.")
            raise RunTimeError("If history is None, then nspins is required.")
        header = f"{'Energy':>15} {'Torque':>11} {'Torque_n':>11}"

        for i in range(nspins):
            header += f" {f'S{i+1}_x':>11} {f'S{i+1}_y':>11} {f'S{i+1}_z':>11}"

        header += f" {'n_x':>11} {'n_y':>11} {'n_z':>11}"
        header += f" {'q_x':>11} {'q_y':>11} {'q_z':>11}"

        if filename is None:
            print(header, flush=True)
        else:
            with open(filename, "a") as file:
                file.write(header)
    else:
        for i in range(len(history)):
            history[i] = (
                # energy
                f"{history[i][0]:15.8e} "
                # torques
                + " ".join([f"{a:11.8f}" for a in history[i][1]])
                + " "
                # I spin vectors and cone axis
                + " ".join([f"{a:11.8f}" for a in history[i][2][0].flatten()])
                + " "
                # spiral vector
                + " ".join([f"{a:11.8f}" for a in history[i][2][1]])
            )
        if filename is None:
            print("\n".join(history), flush=True)
        else:
            with open(filename, "a") as file:
                file.write("\n" + "\n".join(history))


def _default_history_processor_spiral(history, filename=None, nspins=None):
    # Output header
    if history is None:
        if nspins is None:
            _logger.error("If history is None, then nspins is required.")
            raise RunTimeError("If history is None, then nspins is required.")
        header = f"{'Energy':>15} {'Torque':>11} {'Torque_n':>11}"

        for i in range(nspins):
            header += f" {f'S{i+1}_x':>11} {f'S{i+1}_y':>11} {f'S{i+1}_z':>11}"

        header += f" {'n_x':>11} {'n_y':>11} {'n_z':>11}"
        header += f" {'q_x':>11} {'q_y':>11} {'q_z':>11}"

        if filename is None:
            print(header, flush=True)
        else:
            with open(filename, "a") as file:
                file.write(header)
    else:
        for i in range(len(history)):
            history[i] = (
                # energy
                f"{history[i][0]:15.8e} "
                # torques
                + " ".join([f"{a:11.8f}" for a in history[i][1]])
                + " "
                # I spin vectors and cone axis
                + " ".join([f"{a:11.8f}" for a in history[i][2][0].flatten()])
                + " "
                # spiral vector
                + " ".join([f"{a:11.8f}" for a in history[i][2][1]])
            )
        if filename is None:
            print("\n".join(history), flush=True)
        else:
            with open(filename, "a") as file:
                file.write("\n" + "\n".join(history))


################################################################################
#                                 Energy class                                 #
#                                                                              #
# The idea is to create it from SpinHamiltonian as                             #
#                                                                              #
#                           energy = Energy(spinham)                           #
#                                                                              #
# and then have the routines for the energy optimization with the call         #
# signatures                                                                   #
#                                                                              #
#                energy.optimize(initial_guess, *args, **kwargs)               #
################################################################################
class Energy:
    r"""
    Energy of the :py:class:`.SpinHamiltonian`.

    Includes methods for energy optimization for three main types of the ground state
    and for the computation of the energy with the given spin arrangements.

    Being created from a given :py:class:`.SpinHamiltonian` it is completely independent
    from it. i.e. changes in the instance of the :py:class:`.SpinHamiltonian` class do
    not affect the instance of the :py:class:`.Energy` class.
    """

    def __init__(self, spinham: SpinHamiltonian):
        # Parameters of the Hamiltonian, private
        self._factor = spinham.exchange_factor
        self._atom_indices = dict(
            [(atom, i) for i, atom in enumerate(spinham.magnetic_atoms)]
        )

        # Parameters of the Hamiltonian, exposed to public as properties
        self._g_factors = [atom.g_factor for atom in spinham.magnetic_atoms]
        self._spins = [atom.spin for atom in spinham.magnetic_atoms]

        # Force double counting notation
        previous_dc = spinham.double_counting
        spinham.double_counting = True

        # Get all bonds of the Hamiltonian.
        self._bonds = []
        for atom1, atom2, R, J in spinham.exchange_like:
            i = self._atom_indices[atom1]
            j = self._atom_indices[atom2]
            d = R @ spinham.cell
            self._bonds.append([i, j, d, J])

        # Return original noatation of SpinHamiltonian
        spinham.double_counting = previous_dc

        # Minimisation settings, exposed to public as properties
        self._m = 10

        # Parameters for Wolfe conditions
        self._wolfe_iter_max = 10000
        self._wolfe_c1 = 1e-4
        self._wolfe_c2 = 0.9

        # Minimization settings, private
        # Gradient size depends on the expected ground state.
        self._gradient_size = None  # Have to be initialized at the beginning of every optimization function
        self._torques_size = None  # Have to be initialized at the beginning of every optimization function

        # External physical conditions
        self._magnetic_field = None

        # To be sorted
        self._d_vec = None  # Have to be initialized at the beginning of every optimization function
        self._y_vec = None  # Have to be initialized at the beginning of every optimization function
        self._rho = np.zeros((self._m), dtype=float)
        self._gamma = np.zeros((self._m), dtype=float)

    ################################################################################
    #                             Minimization settings                            #
    ################################################################################

    @property
    def m(self) -> int:
        r"""
        Amount of steps to keep in memory for the estimation of the Hessian matrix in
        L-BFGS algorithm.

        Returns
        -------
        m : int
        """

        return self._m

    @m.setter
    def m(self, new_value):
        try:
            new_m = int(new_value)
        except:
            raise ValueError(
                "New size of memory storage for L-BFGS is not "
                f"an integer:{new_value}."
            )
        self._m = new_m

    @property
    def wolfe_c1(self) -> float:
        r"""
        Parameter for the Wolfe conditions:

        .. math::
          f(\boldsymbol{x} + \lambda\boldsymbol{p})
          \le
          f(\boldsymbol{x})
          +
          c_1  \lambda \nabla_{\boldsymbol{x}}f(\boldsymbol{x}) \cdot \boldsymbol{p}

        Default value is :math:`10^{-4}`

        Returns
        -------
        c1 : float
        """

        return self._wolfe_c1

    @wolfe_c1.setter
    def wolfe_c1(self, new_value):
        try:
            new_c1 = float(new_value)
        except:
            raise ValueError(
                "New c1 coefficient for Wolfe conditions is not "
                f"a float:{new_value}."
            )
        self._wolfe_c1 = new_c1

    @property
    def wolfe_c2(self) -> float:
        r"""
        Parameter for the Wolfe conditions:


        .. math::
          -\nabla_{\boldsymbol{x}}f(\boldsymbol{x} + \lambda\boldsymbol{p}) \cdot \boldsymbol{p}
          \le
          -c_2
          \nabla_{\boldsymbol{x}}f(\boldsymbol{x}) \cdot \boldsymbol{p}

        Default value is :math:`0.9`

        Returns
        -------
        c2 : float
        """

        return self._wolfe_c1

    @wolfe_c2.setter
    def wolfe_c2(self, new_value):
        try:
            new_c2 = float(new_value)
        except:
            raise ValueError(
                "New c2 coefficient for Wolfe conditions is not "
                f"a float:{new_value}."
            )
        self._wolfe_c2 = new_c2

    ################################################################################
    #                         External physical conditions                         #
    ################################################################################

    @property
    def magnetic_field(self):
        r"""
        External magnetic field. Given in the units of Tesla.

        Returns
        =======
        magnetic_field : (3,) :numpy:`ndarray` or ``None``
            magnetic_field :math:`\boldsymbol{H}`.
        """
        return self._magnetic_field

    @magnetic_field.setter
    def magnetic_field(self, new_value):
        if new_value is None:
            self._magnetic_field = None
        else:
            try:
                new_field = np.array(new_value, dtype=float)
            except:
                raise ValueError(f"New magnetic field is not array-like: {new_value}")

            if new_field.shape != (3,):
                raise ValueError(
                    "New magnetic field has to be a 3 component vector, "
                    f"got {new_field.shape}"
                )

            self._magnetic_field = new_field

    ################################################################################
    #                         Parameters of the Hamiltonian                        #
    ################################################################################

    @property
    def g_factors(self):
        r"""
        g factor for all magnetic atoms.

        Returns
        -------
        g_factors : (I,) :numpy:`ndarray`
            Order is the same as in :py:attr:`.Energy.spins`.
        """
        return self._g_factors

    @g_factors.setter
    def g_factors(self, new_value):
        if not isinstance(Iterable):
            raise ValueError(f"New g factors must be an Iterable: {new_value}")

        if not len(new_value) == len(self._spins):
            raise ValueError(
                f"Expecten {len(self._spins)} g factors, got {len(new_value)}"
            )

        for i, g_factor in enumerate(new_value):
            try:
                new_value[i] = int(g_factor)
            except:
                raise ValueError(
                    f"One of the new g_factors (index {i}) is not "
                    f"an integer:{g_factor}."
                )
        self._g_factors = new_value

    @property
    def spins(self):
        r"""
        Value of spin for all magnetic atoms.

        Returns
        -------
        spins : (I,) :numpy:`ndarray`
            Order is the same as in :py:attr:`.SpinHamiltonian.magnetic_atoms`.
        """
        return self._spins

    @spins.setter
    def spins(self, new_value):
        if not isinstance(Iterable):
            raise ValueError(f"New spins must be an Iterable: {new_value}")

        if not len(new_value) == len(self._spins):
            raise ValueError(f"Expected {len(self._spins)} spins, got {len(new_value)}")

        for i, spin in enumerate(new_value):
            try:
                new_value[i] = int(spin)
            except:
                raise ValueError(
                    f"One of the new spins (index {i}) is not " f"an integer:{spin}."
                )
        self._spins = new_value

    ################################################################################
    #                              Gradients of energy                             #
    # The idea is to have functions that have a call signatures the same as        #
    # corresponding energy functions with two additional keyword arguments:        #
    # "gradient_vector" and "torques". If both gradient_vector and torques are     #
    # given, then the update is done in place and the function return nothing.     #
    # Otherwise it returns gradient_vector and torques, leaving the given part     #
    # intact.                                                                      #
    ################################################################################

    def _ferro_grad(self, spin_orientation, gradient_vector=None, torques=None):
        r"""
        Gradient of the ferro case looks like:

        [ t_0z, -t_0y, t_0x, ..., t_(I-1)z, -t_(I-1)y ]

        where t_ix, t_iy, t_iz - are components of torque for ith spin in the
        unit cell (i = 0, I-1).

        torques have the form:

        [
            [t_0x, t_0y, t_0z],
            ...,
            [t_(I-1)x, t_(I-1)y, t_(I-1)z]
        ]
        """
        if gradient_vector is None or torques is None:
            gradient_vector = np.zeros((self._gradient_size), dtype=float)
            torques = np.zeros((len(self._spins), 3), dtype=float)
            return_results = True
        else:
            return_results = False

        for i in range(len(spin_orientation)):
            h = 1e-4
            gradient = []
            for j in range(3):
                spin_orientation[i][j] -= h
                f_minus_h = self.ferro(spin_orientation)
                spin_orientation[i][j] += 2 * h
                f_plus_h = self.ferro(spin_orientation)
                gradient.append((f_plus_h - f_minus_h) / 2 / h)
                spin_orientation[i][j] -= h

            t = np.cross(spin_orientation[i], gradient)
            for j in range(0, 3):
                torques[i][j] = t[j]
            gradient_vector[3 * i] = t[2]
            gradient_vector[3 * i + 1] = -t[1]
            gradient_vector[3 * i + 2] = t[0]

        if return_results:
            return gradient_vector, torques

    def _antiferro_grad(
        self,
        spin_orientation,
        cone_axis,
        spiral_vector,
        gradient_vector=None,
        torques=None,
    ):
        r"""
        Gradient of the antiferro case looks like:

        [ t_0z, -t_0y, t_0x, ..., t_(I-1)z, -t_(I-1)y,
          t_(I-1)x, t_nz, -t_ny, t_nx]

        where t_ix, t_iy, t_iz - are components of torque for ith spin in the
        unit cell (i = 0, I-1); t_nx, t_ny, t_nz 0 - are the components of the "torque"
        on the cone axis.

        torques have the form:

        [
            [t_0x, t_0y, t_0z],
            ...,
            [t_(I-1)x, t_(I-1)y, t_(I-1)z],
            [t_nx, t_ny, t_nz]
        ]
        """

        if gradient_vector is None or torques is None:
            gradient_vector = np.zeros((self._gradient_size), dtype=float)
            torques = np.zeros((self._torque_size, 3), dtype=float)
            return_results = True
        else:
            return_results = False

        # Compute gradient for spin_orientation
        for i in range(len(spin_orientation)):
            h = 1e-4
            gradient = []
            for j in range(3):
                spin_orientation[i][j] -= h
                f_minus_h = self.antiferro(spin_orientation, cone_axis, spiral_vector)
                spin_orientation[i][j] += 2 * h
                f_plus_h = self.antiferro(spin_orientation, cone_axis, spiral_vector)
                gradient.append((f_plus_h - f_minus_h) / 2 / h)
                spin_orientation[i][j] -= h

            t = np.cross(spin_orientation[i], gradient)
            for j in range(0, 3):
                torques[i][j] = t[j]
            gradient_vector[3 * i] = t[2]
            gradient_vector[3 * i + 1] = -t[1]
            gradient_vector[3 * i + 2] = t[0]

        # Compute gradient for cone_axis
        h = 1e-4
        gradient = []
        for j in range(3):
            cone_axis[j] -= h
            f_minus_h = self.antiferro(spin_orientation, cone_axis, spiral_vector)
            cone_axis[j] += 2 * h
            f_plus_h = self.antiferro(spin_orientation, cone_axis, spiral_vector)
            gradient.append((f_plus_h - f_minus_h) / 2 / h)
            cone_axis[j] -= h

        t = np.cross(cone_axis, gradient)
        for j in range(0, 3):
            torques[-1][j] = t[j]
        gradient_vector[-6] = t[2]
        gradient_vector[-5] = -t[1]
        gradient_vector[-4] = t[0]

        if return_results:
            return gradient_vector, torques

    def _spiral_grad(
        self,
        spin_orientation,
        cone_axis,
        spiral_vector,
        gradient_vector=None,
        torques=None,
    ):
        r"""
        Gradient of the spiral case looks like:

        [ t_0z, -t_0y, t_0x, ..., t_(I-1)z, -t_(I-1)y,
          t_(I-1)x, t_nz, -t_ny, t_nx,
          dE/dq_x, dE/dq_y, dE/dq_z ]

        where t_ix, t_iy, t_iz - are components of torque for ith spin in the
        unit cell (i = 0, I-1); t_nx, t_ny, t_nz 0 - are the components of the "torque"
        on the cone axis and last three elements are just partial derivatives
        with respect to the components of the spiral vector (computed analytically).

        torques have the form:

        [
            [t_0x, t_0y, t_0z],
            ...,
            [t_(I-1)x, t_(I-1)y, t_(I-1)z],
            [t_nx, t_ny, t_nz]
        ]
        """

        if gradient_vector is None or torques is None:
            gradient_vector = np.zeros((self._gradient_size), dtype=float)
            torques = np.zeros((self._torque_size, 3), dtype=float)
            return_results = True
        else:
            return_results = False

        # Compute gradient for spin_orientation
        for i in range(len(spin_orientation)):
            h = 1e-4
            gradient = []
            for j in range(3):
                spin_orientation[i][j] -= h
                f_minus_h = self.spiral(spin_orientation, cone_axis, spiral_vector)
                spin_orientation[i][j] += 2 * h
                f_plus_h = self.spiral(spin_orientation, cone_axis, spiral_vector)
                gradient.append((f_plus_h - f_minus_h) / 2 / h)
                spin_orientation[i][j] -= h

            t = np.cross(spin_orientation[i], gradient)
            for j in range(0, 3):
                torques[i][j] = t[j]
            gradient_vector[3 * i] = t[2]
            gradient_vector[3 * i + 1] = -t[1]
            gradient_vector[3 * i + 2] = t[0]

        # Compute gradient for cone_axis
        h = 1e-4
        gradient = []
        for j in range(3):
            cone_axis[j] -= h
            f_minus_h = self.spiral(spin_orientation, cone_axis, spiral_vector)
            cone_axis[j] += 2 * h
            f_plus_h = self.spiral(spin_orientation, cone_axis, spiral_vector)
            gradient.append((f_plus_h - f_minus_h) / 2 / h)
            cone_axis[j] -= h

        t = np.cross(cone_axis, gradient)
        for j in range(0, 3):
            torques[-1][j] = t[j]
        gradient_vector[-6] = t[2]
        gradient_vector[-5] = -t[1]
        gradient_vector[-4] = t[0]

        # Compute gradient for spiral_vector
        K = np.array(
            [
                [0, -cone_axis[2], cone_axis[1]],
                [cone_axis[2], 0, -cone_axis[0]],
                [-cone_axis[1], cone_axis[0], 0],
            ]
        )
        K_sq = K @ K

        gradient = np.zeros(3, dtype=float)

        for i, j, d, J in self._bonds:
            C = -np.cos(spiral_vector @ d) / 2 * (
                K @ J.matrix @ K_sq + K_sq @ J.matrix @ K
            ) + np.sin(spiral_vector @ d) / 2 * (
                K @ J.matrix @ K - K_sq @ J.matrix @ K_sq
            )
            gradient += d * (
                self._factor
                * self._spins[i]
                * self._spins[j]
                * np.einsum("i,ij,j", spin_orientation[i], C, spin_orientation[j])
            )
        # print(f"\n\n{gradient}\n\n")

        gradient_vector[-3:] = gradient

        if return_results:
            return gradient_vector, torques

    ################################################################################
    #                                    Energy                                    #
    ################################################################################

    def ferro(self, spin_orientation):
        r"""
        Computes energy of the generalized ferromagnetic state for given
        ``spin_orientation``.

        Parameters
        ----------
        spin_orientation : (I, 3) or (3,) |array-like|_
            Orientation of the spin vectors.
            If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are accepted.
            The vectors are normalized to one, i.e. only direction of the vectors
            is important.

        Returns
        -------
        energy :  float.
            Energy of the Hamiltonian for the given ``spin_orientation``
        """

        # Check that the input is correct
        try:
            spin_orientation = np.array(spin_orientation, dtype=float)
        except:
            raise ValueError(f"spin_orientation is not array-like: {spin_orientation}")

        if spin_orientation.shape[-1] != 3:
            raise ValueError(
                f"spin_orientation has to have the last dimension of "
                f"size 3, got {spin_orientation.shape[-1]}"
            )

        # Make the input array have (I,3) shape for I = 1
        if len(self._spins) == 1 and spin_orientation.shape == (3,):
            spin_orientation = np.array([spin_orientation])

        if len(self._spins) != spin_orientation.shape[0]:
            raise ValueError(
                f"Expected {len(self._spins)} spin orientations, "
                f"got {spin_orientation.shape[0]}"
            )

        for i in range(len(spin_orientation)):
            spin_orientation[i] /= np.linalg.norm(spin_orientation[i])

        energy = 0

        # Compute exchange and single-ion-like anisotropy energy
        for i, j, _, J in self._bonds:
            energy += (
                self._factor
                * self._spins[i]
                * self._spins[j]
                * np.einsum(
                    "i,ij,j", spin_orientation[i], J.matrix, spin_orientation[j]
                )
            )

        # Compute zeeman energy
        if self.magnetic_field is not None:
            energy += BOHR_MAGNETON * np.einsum(
                "i,j,ij", self._g_factors, self.magnetic_field, spin_orientation
            )

        return energy

    def antiferro(self, spin_orientation, cone_axis, spiral_vector):
        r"""
        Computes energy of the antiferro cone state for given
        ``spin_orientation``, ``cone_axis`` and ``spiral_vector``.

        Parameters
        ----------
        spin_orientation : (I, 3) or (3,) |array-like|_
            Orientation of the spin vectors.
            If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are accepted.
            The vectors are normalized to one, i.e. only direction of the vectors
            is important.
        cone_axis : (3,) |array-like|_
            Orientation of the cone axis, only the direction is important.
        spiral_vector : (3,) |array-like|_
            Spiral vector.

        Returns
        -------
        energy :  float.
            Energy of the Hamiltonian for the given ``spin_orientation``, ``cone_axis``
            and ``spiral_vector``.

        Notes
        -----
        Spiral vector is restricted to :math:`2\boldsymbol{q}=\boldsymbol{G}`.
        """

        # Check that the input is correct (spins)
        try:
            spin_orientation = np.array(spin_orientation, dtype=float)
        except:
            raise ValueError(f"spin_orientation is not array-like: {spin_orientation}")

        if spin_orientation.shape[-1] != 3:
            raise ValueError(
                f"spin_orientation has to have the last dimension of "
                f"size 3, got {spin_orientation.shape[-1]}"
            )

        # Check that the input is correct (cone_axis)
        try:
            cone_axis = np.array(cone_axis, dtype=float)
        except:
            raise ValueError(f"cone_axis is not array-like: {cone_axis}")

        if cone_axis.shape != (3,):
            raise ValueError(
                f"cone_axis must have the shape of (3,) " f"got {cone_axis.shape}"
            )

        # Check that the input is correct (spiral vector)
        try:
            spiral_vector = np.array(spiral_vector, dtype=float)
        except:
            raise ValueError(f"spiral_vector is not array-like: {spiral_vector}")

        if spiral_vector.shape != (3,):
            raise ValueError(
                f"spiral_vector must have the shape of (3,) "
                f"got {spiral_vector.shape}"
            )

        # Make the input array have (I,3) shape for I = 1
        if len(self._spins) == 1 and spin_orientation.shape == (3,):
            spin_orientation = np.array([spin_orientation])

        if len(self._spins) != spin_orientation.shape[0]:
            raise ValueError(
                f"Expected {len(self._spins)} spin orientations, "
                f"got {spin_orientation.shape[0]}"
            )

        # Normalize spin orientations
        for i in range(len(spin_orientation)):
            spin_orientation[i] /= np.linalg.norm(spin_orientation[i])

        # Normalize cone axis
        cone_axis /= np.linalg.norm(cone_axis)

        K = np.array(
            [
                [0, -cone_axis[2], cone_axis[1]],
                [cone_axis[2], 0, -cone_axis[0]],
                [-cone_axis[1], cone_axis[0], 0],
            ]
        )
        K_sq = K @ K
        IK_sq = np.eye(3, dtype=float) + K_sq

        energy = 0

        # Compute exchange and single-ion-like anisotropy energy
        for i, j, d, J in self._bonds:
            C_dij = (
                IK_sq @ J.matrix @ IK_sq
                + K_sq @ J.matrix @ K_sq * np.cos(spiral_vector @ d)
                - K_sq @ J.matrix @ K * np.sin(spiral_vector @ d)
            )

            energy += (
                self._factor
                * self._spins[i]
                * self._spins[j]
                * np.einsum("i,ij,j", spin_orientation[i], C_dij, spin_orientation[j])
            )

        # Compute zeeman energy
        if self.magnetic_field is not None:
            so_prime = np.einsum(
                "jk,ik ->ij", (np.eye(3, dtype=float) + IK_sq), spin_orientation
            )
            energy += BOHR_MAGNETON * np.einsum(
                "i,j,ij", self._g_factors, self.magnetic_field, so_prime
            )

        return energy

    def spiral(self, spin_orientation, cone_axis, spiral_vector):
        r"""
        Computes energy of the spiral cone state for given
        ``spin_orientation``, ``cone_axis`` and ``spiral_vector``.

        Parameters
        ----------
        spin_orientation : (I, 3) or (3,) |array-like|_
            Orientation of the spin vectors.
            If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are accepted.
            The vectors are normalized to one, i.e. only direction of the vectors
            is important.
        cone_axis : (3,) |array-like|_
            Orientation of the cone axis, only the direction is important.
        spiral_vector : (3,) |array-like|_
            Spiral vector.

        Returns
        -------
        energy :  float.
            Energy of the Hamiltonian for the given ``spin_orientation``, ``cone_axis``
            and ``spiral_vector``.
        """

        # Check that the input is correct (spins)
        try:
            spin_orientation = np.array(spin_orientation, dtype=float)
        except:
            raise ValueError(f"spin_orientation is not array-like: {spin_orientation}")

        if spin_orientation.shape[-1] != 3:
            raise ValueError(
                f"spin_orientation has to have the last dimension of "
                f"size 3, got {spin_orientation.shape[-1]}"
            )

        # Check that the input is correct (cone_axis)
        try:
            cone_axis = np.array(cone_axis, dtype=float)
        except:
            raise ValueError(f"cone_axis is not array-like: {cone_axis}")

        if cone_axis.shape != (3,):
            raise ValueError(
                f"cone_axis must have the shape of (3,) " f"got {cone_axis.shape}"
            )

        # Check that the input is correct (spiral vector)
        try:
            spiral_vector = np.array(spiral_vector, dtype=float)
        except:
            raise ValueError(f"spiral_vector is not array-like: {spiral_vector}")

        if spiral_vector.shape != (3,):
            raise ValueError(
                f"spiral_vector must have the shape of (3,) "
                f"got {spiral_vector.shape}"
            )

        # Make the input array have (I,3) shape for I = 1
        if len(self._spins) == 1 and spin_orientation.shape == (3,):
            spin_orientation = np.array([spin_orientation])

        if len(self._spins) != spin_orientation.shape[0]:
            raise ValueError(
                f"Expected {len(self._spins)} spin orientations, "
                f"got {spin_orientation.shape[0]}"
            )

        # Normalize spin orientations
        for i in range(len(spin_orientation)):
            spin_orientation[i] /= np.linalg.norm(spin_orientation[i])

        # Normalize cone axis
        cone_axis /= np.linalg.norm(cone_axis)

        K = np.array(
            [
                [0, -cone_axis[2], cone_axis[1]],
                [cone_axis[2], 0, -cone_axis[0]],
                [-cone_axis[1], cone_axis[0], 0],
            ]
        )
        K_sq = K @ K
        IK_sq = np.eye(3, dtype=float) + K_sq

        energy = 0

        # Compute exchange and single-ion-like anisotropy energy
        for i, j, d, J in self._bonds:
            # print(
            #     spiral_vector @ d, np.sin(spiral_vector @ d), np.cos(spiral_vector @ d)
            # )
            C_dij = (
                IK_sq @ J.matrix @ IK_sq
                - (K @ J.matrix @ K - K_sq @ J.matrix @ K_sq)
                / 2
                * np.cos(spiral_vector @ d)
                - (K @ J.matrix @ K_sq + K_sq @ J.matrix @ K)
                / 2
                * np.sin(spiral_vector @ d)
            )

            energy += (
                self._factor
                * self._spins[i]
                * self._spins[j]
                * np.einsum("i,ij,j", spin_orientation[i], C_dij, spin_orientation[j])
            )

        # Compute zeeman energy
        if self.magnetic_field is not None:
            so_prime = np.einsum(
                "jk,ik ->ij", (np.eye(3, dtype=float) + IK_sq), spin_orientation
            )
            energy += BOHR_MAGNETON * np.einsum(
                "i,j,ij", self._g_factors, self.magnetic_field, so_prime
            )

        return energy

    ################################################################################
    #                             Optimization routines                            #
    ################################################################################

    def optimize(
        self,
        case,
        initial_guess=None,
        tolerance=None,
        max_iterations=None,
        save_history=False,
        history_filename=None,
        history_step=1000,
        antiferro_q=None,
    ):
        r"""
        Find the minima of the energy assuming the type of the ground state based on
        ``case`` argument.

        Parameters
        ----------
        case : str or int {"ferro", 0, "antiferro", 1, "spiral", 2}
            Three cases are supported:

            * Generalized ferromagnetic: ``"ferro"`` or ``0``
            * Generalized antiferromagnetic: ``"antiferro"`` or ``1``
            * Spiral cone: ``"spiral"`` or ``2``
        initial_guess : optional
            Initial guess for the relevant variables. Expected format depends on the
            ``case``:

            * ``case="ferro"`` spin_orientation

              spin_orientation : (I, 3) or (3,) |array-like|_ or None
                  Initial guess for the orientation of spin vectors.
                  If none provided, then random orientation is chosen.
                  The vectors are normalized to one, i.e. only direction of the vectors
                  is important.
                  If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are
                  accepted.

            * ``case ="antiferro"`` tuple of (spin_orientation, cone_axis)

              spin_orientation : (I, 3) or (3,) |array-like|_ or None
                  Initial guess for the orientation of spin vectors.
                  If none provided, then random orientation is chosen.
                  The vectors are normalized to one, i.e. only direction of the vectors
                  is important.
                  If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are
                  accepted.
              cone_axis : (3,) |array-like|_
                  Cone axis. Only direction is important.

            * ``case ="spiral"`` tuple of (spin_orientation, cone_axis, spiral_vector)

              spin_orientation : (I, 3) or (3,) |array-like|_ or None
                  Initial guess for the orientation of spin vectors.
                  If none provided, then random orientation is chosen.
                  The vectors are normalized to one, i.e. only direction of the vectors
                  is important.
                  If ``I = 1``, then both ``(1,3)`` and ``(3,)`` shaped inputs are
                  accepted.
              cone_axis : (3,) |array-like|_
                  Cone axis. Only direction is important.
              spiral_vector : (3,) |array-like|_
                  Spiral vector :math:`\boldsymbol{q}`. Both orientation and length are
                  important.

        tolerance : tuple of floats
            Tolerance parameters.

            * ``case="ferro"`` tuple of (tol_energy_diff, tol_torque_max)

              tol_energy_diff : float, default 1e-5
                  tolerance for the difference between the
                  energies of two consecutive minimization steps
              tol_torque_max : float, default 1e-5
                  Tolerance for the maximum torque among the spins of the unit cell.

            * ``case="antiferro"``
              FIXME

            * ``case="ferro"`` tuple of (tol_energy_diff, tol_torque_max, tol_torque_cone)

              tol_energy_diff : float, default 1e-5
                  tolerance for the difference between the
                  energies of two consecutive minimization steps
              tol_torque_max : float, default 1e-5
                  Tolerance for the maximum torque among the spins of the unit cell.
              tol_torque_cone : float, default 1e-5
                  Tolerance for the torque on the cone axis.

        max_iterations : int, optional
            Maximum amount of iterations for the minimization algorithm.
            By default the algorithm will run until the convergence is reached.
        save_history : bool, default False
            Whether to output the steps of the minimization algorithm.
        history_filename : str, optional
            Filename for saving history of the minimization. By default history is
            directed to ``sys.stdout`` via ``print()`` function.
        history_step : int, default 100
            The history is printed every ``history_step`` steps.

        antiferro_q : (3,) |array-like|_
            One of the 26 possible q vectors of the sntiferromagnetic case.


        Returns
        -------
        spin_orientation : (I, 3) :numpy:`ndarray`
            Spin orientation that corresponds to the found local minima of energy
            assuming generalized ferromagnetic state. Returned in every case.
        cone_axis : (3,) :numpy:`ndarray`
            Cone axis that correspond to the local minima of energy. Returned if
            ``case = "antiferro"`` or ``case = "spiral"``
        spiral_vector : (3,)  :numpy:`ndarray`
            Spiral vector that correspond to the local minima of energy. Returned if
            ``case = "spiral"``
        """

        # Check the correctness of the initial guess if any.
        # Make a random one otherwise.

        if case in [0, "ferro"]:
            x = _starting_ferro(len(self._spins), initial_guess)

            self._gradient_size = 3 * len(self._spins)
            self._torque_size = len(self._spins)

            energy = self.ferro
            _grad = self._ferro_grad
            _unpack = _unpack_ferro
            _update = _update_x_ferro
            _compute_torque_target = _compute_torque_target_ferro

            # Switch to the default history processor if necessary
            if save_history:
                history_processor = _default_history_processor_ferro

            if tolerance is None:
                tolerance = (1e-5, 1e-5)
            elif len(tolerance) != 2:
                raise ValueError(
                    f"Expected tuple of two floats for tolerance, got {tolerance}"
                )
        elif case in [1, "antiferro"]:
            x = _starting_antiferro(len(self._spins), antiferro_q, initial_guess)

            self._gradient_size = 3 * len(self._spins) + 3
            self._torque_size = len(self._spins) + 1

            energy = self.antiferro
            _grad = self._antiferro_grad
            _unpack = _unpack_antiferro
            _update = _update_x_antiferro
            _compute_torque_target = _compute_torque_target_antiferro

            # Switch to the default history processor if necessary
            if save_history:
                history_processor = _default_history_processor_antiferro
            if tolerance is None:
                tolerance = (1e-5, 1e-5, 1e-5)
            elif len(tolerance) != 3:
                raise ValueError(
                    f"Expected tuple of three floats for tolerance, got {tolerance}"
                )
        elif case in [2, "spiral"]:
            x = _starting_spiral(len(self._spins), initial_guess)

            self._gradient_size = 3 * len(self._spins) + 6
            self._torque_size = len(self._spins) + 1

            energy = self.spiral
            _grad = self._spiral_grad
            _unpack = _unpack_spiral
            _update = _update_x_spiral
            _compute_torque_target = _compute_torque_target_spiral

            # Switch to the default history processor if necessary
            if save_history:
                history_processor = _default_history_processor_spiral
            if tolerance is None:
                tolerance = (1e-5, 1e-5, 1e-5)
            elif len(tolerance) != 3:
                raise ValueError(
                    f"Expected tuple of three floats for tolerance, got {tolerance}"
                )
        else:
            raise ValueError(
                'case must be either "ferro" or "antiferro" or "spiral" or '
                f"0 or 1 or 2. Got {case}"
            )

        # Print header for the history
        if save_history:
            history_processor(None, nspins=len(self._spins), filename=history_filename)

        # Set the iterators
        # Note: iteration counter and k are distinct: k might be set to zero during
        # the algorithm's run.
        k = 0
        iteration_counter = 0

        # Set initial tracking variables
        step = None
        previous_gradient_vector = None
        previous_search_direction = None
        energy_prev = energy(*_unpack(x))
        self._d_vec = np.zeros((self._m, self._gradient_size), dtype=float)
        self._y_vec = np.zeros((self._m, self._gradient_size), dtype=float)
        torques = np.zeros((self._torque_size, 3), dtype=float)
        gradient_vector = np.zeros((self._gradient_size), dtype=float)
        search_direction = np.zeros((self._gradient_size), dtype=float)

        # Set initial convergence targets for torques so the loop will be started.
        # For the energy the track is done separately
        torque_targets = [2 * a for a in tolerance[1:]]
        energy_diff = tolerance[0] * 2

        # Compute condition for the loop
        condition = energy_diff > tolerance[0]
        for i in range(len(torque_targets)):
            condition = condition or torque_targets[i] > tolerance[i + 1]

        # Save initial guess and its energy, conv_targets are meaningless
        # but saved so the history will have the same format for each step
        if save_history:
            history = [[energy_prev, torque_targets, x]]

        while condition:
            # Check whether number of iterations is exceeded
            if max_iterations is not None and iteration_counter >= max_iterations:
                _logger.warning(
                    f"Maximum iteration is reached. "
                    f"Torques: {torque_targets}, "
                    f"Energy difference: {energy_diff:.5e}."
                )
                return _unpack(x)

            # Compute gradient and torques
            _grad(*_unpack(x), gradient_vector=gradient_vector, torques=torques)

            # Compute search direction
            k, search_direction = self._compute_search_direction(
                k,
                gradient_vector=gradient_vector,
                previous_lambda=step,
                previous_gradient_vector=previous_gradient_vector,
                previous_search_direction=previous_search_direction,
            )

            # Compute size of the step along the search direction
            step = self._lambda(
                x,
                search_direction,
                energy=energy,
                _unpack=_unpack,
                _update=_update,
                _grad=_grad,
            )

            # Update the generalized coordinate
            x = _update(x, search_direction, step)

            # Compute convergence targets
            energy_current = energy(*_unpack(x))
            energy_diff = abs(energy_prev - energy_current)
            torque_targets = _compute_torque_target(torques)

            # Compute condition for the loop
            condition = energy_diff > tolerance[0]
            for i in range(len(torque_targets)):
                condition = condition or torque_targets[i] > tolerance[i + 1]

            # Keep values for the next loop
            previous_gradient_vector = gradient_vector.copy()
            previous_search_direction = search_direction.copy()
            energy_prev = energy_current

            # Update iterators
            k += 1
            iteration_counter += 1

            if save_history:
                # Update history
                history.append(
                    [
                        energy_current,
                        torque_targets,
                        x,
                    ]
                )
                # Output history is required
                if iteration_counter % history_step == 0 and iteration_counter > 0:
                    history_processor(history, filename=history_filename)
                    history = []

        # Output remaining part of history
        if save_history:
            history_processor(history, filename=history_filename)

        # Return minimized configuration
        return _unpack(x)

    ################################################################################
    #                                 L-BFGS update                                #
    ################################################################################
    def _compute_search_direction(
        self,
        k,
        gradient_vector,
        previous_lambda=None,
        previous_gradient_vector=None,
        previous_search_direction=None,
    ):
        r"""
        Compute search direction with L-BFGS algorithm. The details of the
        implementation are taken from [1]_.
        Universal and does not depend on the choice of the ground state type.

        Parameters
        ----------
        k : int
            Index of the minimization cycle.
        gradient_vector : (M,) :numpy:`ndarray`
            Gradient vector.
        previous_gradient_vector : (M,) :numpy:`ndarray`
            Gradient vector for k-1.
        previous_search_direction : (M,) :numpy:`ndarray`
            Search direction for k-1.

        Returns
        -------
        k : int
            Index of the minimization cycle (can be set to 0 at some of the steps).
        search_direction : (M,)
            Search direction computed for the step k.

        References
        ----------
        .. [1] Ivanov, A.V., Uzdin, V.M. and Jónsson, H., 2021.
            Fast and robust algorithm for energy minimization of spin systems applied
            in an analysis of high temperature spin configurations in terms of skyrmion
            density.
            Computer Physics Communications, 260, p.107749.
        """

        if k != 0 and (
            previous_gradient_vector is None
            or previous_search_direction is None
            or previous_lambda is None
        ):
            raise ValueError("Need info about previous gradient and search direction")

        n = k % self._m

        if k == 0:
            self._d_vec = np.zeros((self._m, self._gradient_size), dtype=float)
            self._y_vec = np.zeros((self._m, self._gradient_size), dtype=float)
            self._rho = np.zeros((self._m), dtype=float)
            self._gamma = np.zeros((self._m), dtype=float)
            search_direction = gradient_vector
        else:
            self._d_vec[n] = previous_lambda * previous_search_direction
            self._y_vec[n] = gradient_vector - previous_gradient_vector
            self._rho[n] = 1 / (self._d_vec[n] @ self._y_vec[n])

            if self._rho[n] < 0:
                return (
                    0,
                    self._compute_search_direction(0, gradient_vector=gradient_vector)[
                        1
                    ],
                )

            q = gradient_vector.copy()

            for l in range(self._m - 1, -1):
                j = (l + n + 1) % self._m
                self._gamma[j] = self._rho[j] * (self._d_vec[j] @ q)
                q = q - self._gamma[j] * self._y_vec[j]
            search_direction = q / self._rho[n] / (np.linalg.norm(self._y_vec[n]))
            for l in range(0, self._m):
                if k < self._m:
                    j = l
                else:
                    j = (l + n + 1) % self._m
                search_direction = search_direction + self._d_vec[j] * (
                    self._gamma[j] - self._rho[j] * (self._y_vec[j] @ search_direction)
                )

        return k, search_direction

    ################################################################################
    #                   Inexact line search with Wolfe conditions                  #
    ################################################################################
    def _lambda(self, x, search_direction, energy, _unpack, _update, _grad):
        r"""
        Compute the step length across given search direction. Universal and does not
        depend on the choice of the ground state type.
        """
        step = 1
        fx = energy(*_unpack(x))
        x_new = _update(x, search_direction, step)
        nabla_new = _grad(*_unpack(x_new))[0]
        nabla = _grad(*_unpack(x))[0]
        i = 0
        tmp = [[], [], []]
        while energy(*_unpack(x_new)) > fx + (
            self._wolfe_c1 * step * nabla.T @ search_direction
        ) or abs(nabla_new.T @ search_direction) > abs(
            self._wolfe_c2 * nabla.T @ search_direction
        ):
            step *= 0.99
            x_new = _update(x, search_direction, step)
            nabla_new = _grad(*_unpack(x_new))[0]
            # print(
            #     energy(*_unpack(x_new)),
            #     fx,
            #     fx + self._wolfe_c1 * step * nabla.T @ search_direction,
            #     abs(nabla_new.T @ search_direction),
            #     abs(self._wolfe_c2 * nabla.T @ search_direction),
            # )
            tmp[0].append(step)
            tmp[1].append(energy(*_unpack(x_new)))
            tmp[2].append(fx + step * self._wolfe_c1 * nabla.T @ search_direction)
            if i > self._wolfe_iter_max:
                print("\n\n")
                # TODO go into the details and deal with the failing cases
                import matplotlib.pyplot as plt

                fig, ax = plt.subplots()
                ax.plot(tmp[0], tmp[1], lw=1, color="black")
                ax.plot(tmp[0], tmp[2], lw=1, color="tab:red")
                plt.savefig("tmp.png", dpi=300, bbox_inches="tight")
                plt.close()
                # return 1
                raise ValueError("Wolfe failed")
            i += 1
        return step
