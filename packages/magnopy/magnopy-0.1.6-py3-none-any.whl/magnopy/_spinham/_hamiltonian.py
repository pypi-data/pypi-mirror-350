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


from copy import deepcopy

import numpy as np
from wulfric import add_sugar
from wulfric.crystal import get_distance

from magnopy._spinham._c1 import _add_1, _p1, _remove_1
from magnopy._spinham._c21 import _add_21, _p21, _remove_21
from magnopy._spinham._c22 import _add_22, _p22, _remove_22
from magnopy._spinham._c31 import _add_31, _p31, _remove_31
from magnopy._spinham._c32 import _add_32, _p32, _remove_32
from magnopy._spinham._c33 import _add_33, _p33, _remove_33
from magnopy._spinham._c41 import _add_41, _p41, _remove_41
from magnopy._spinham._c43 import _add_43, _p43, _remove_43
from magnopy._spinham._c44 import _add_44, _p44, _remove_44
from magnopy._spinham._c421 import _add_421, _p421, _remove_421
from magnopy._spinham._c422 import _add_422, _p422, _remove_422
from magnopy._spinham._convention import Convention
from magnopy._spinham._validators import _validate_atom_index, _validate_unit_cell_index

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class SpinHamiltonian:
    r"""
    Spin Hamiltonian.

    Parameters
    ----------
    convention : :py:class:`.Convention` or str
        A convention of the spin Hamiltonian.
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
    atoms : dict
        Dictionary with atoms.

    """

    def __init__(self, cell, atoms, convention) -> None:
        self._cell = np.array(cell)

        self._atoms = add_sugar(atoms)

        # Only the magnetic sites
        self._magnetic_atoms = None
        self._map_to_magnetic = None
        self._map_to_all = None

        self._convention = convention

        # [[alpha, parameter], ...]
        self._1 = []

        # [[alpha, parameter], ...]
        self._21 = []

        # [[alpha, beta, nu, parameter], ...]
        self._22 = []

        # [[alpha, parameter], ...]
        self._31 = []

        # [[alpha, beta, nu, parameter], ...]
        self._32 = []

        # [[alpha, beta, gamma, nu, lambda, parameter], ...]
        self._33 = []

        # [[alpha, parameter], ...]
        self._41 = []

        # [[alpha, beta, nu, parameter], ...]
        self._421 = []

        # [[alpha, beta, nu, parameter], ...]
        self._422 = []

        # [[alpha, beta, gamma, nu, lambda, parameter], ...]
        self._43 = []

        # [[alpha, beta, gamma, epsilon, nu, lambda, rho, parameter], ...]
        self._44 = []

    ############################################################################
    #                              Cell and Atoms                              #
    ############################################################################

    @property
    def cell(self):
        r"""
        Cell of the crystal on which the Hamiltonian is build.

        Returns
        -------
        cell : (3, 3) :numpy:`ndarray`
            Matrix of the cell, rows are lattice vectors.

        Notes
        -----
        If is not recommended to change the ``cell`` property after the creation of
        :py:class:`.SpinHamiltonian`. In fact an attempt to do so will raise an
        ``AttributeError``:

        .. doctest::

            >>> import numpy as np
            >>> import magnopy
            >>> convention = magnopy.Convention()
            >>> spinham = magnopy.SpinHamiltonian(cell = np.eye(3), atoms={}, convention=convention)
            >>> spinham.cell = 2 * np.eye(3)
            Traceback (most recent call last):
            ...
            AttributeError: Change of the cell attribute is not supported after the creation of SpinHamiltonian instance. If you need to modify cell, then use pre-defined methods of SpinHamiltonian or create a new one.

        Use pre-defined methods of the :py:class:`.SpinHamiltonian` class to safely
        modify the cell.

        If you need to change the cell attribute, then use

        .. doctest::

            >>> import numpy as np
            >>> import magnopy
            >>> convention = magnopy.Convention()
            >>> spinham = magnopy.SpinHamiltonian(cell = np.eye(3), atoms={}, convention=convention)
            >>> spinham.cell
            array([[1., 0., 0.],
                   [0., 1., 0.],
                   [0., 0., 1.]])
            >>> spinham._cell = 2 * np.eye(3)
            >>> spinham.cell
            array([[2., 0., 0.],
                   [0., 2., 0.],
                   [0., 0., 2.]])


        In the latter case correct behavior of magnopy **is not** guaranteed. Use only
        if you have a deep understanding of the magnopy source code.
        """

        return self._cell

    @cell.setter
    def cell(self, new_value):
        raise AttributeError(
            f"Change of the cell attribute is not supported after "
            "the creation of SpinHamiltonian instance. If you need to modify cell, "
            "then use pre-defined methods of SpinHamiltonian or create a new one."
        )

    @property
    def atoms(self) -> dict:
        r"""
        Atoms of the crystal on which the Hamiltonian is build.

        Returns
        -------
        atoms : dict (with added sugar)
            Dictionary with the atoms.

        Notes
        -----
        If is not recommended to change the atoms property after the creation of
        :py:class:`.SpinHamiltonian`. In fact an attempt to do so will raise an
        ``AttributeError``:

        .. doctest::

            >>> import numpy as np
            >>> import magnopy
            >>> convention = magnopy.Convention()
            >>> spinham = magnopy.SpinHamiltonian(cell = np.eye(3), atoms={}, convention=convention)
            >>> spinham.atoms = {"names" : ["Cr"]}
            Traceback (most recent call last):
            ...
            AttributeError: Change of the atoms dictionary is not supported after the creation of SpinHamiltonian instance. If you need to modify atoms, then use pre-defined methods of SpinHamiltonian or create a new one.

        Use pre-defined methods of the :py:class:`.SpinHamiltonian` class to safely
        modify atoms.

        If you need to change the whole dictionary at once, then use

        .. doctest::

            >>> import numpy as np
            >>> import magnopy
            >>> convention = magnopy.Convention()
            >>> spinham = magnopy.SpinHamiltonian(cell = np.eye(3), atoms={}, convention=convention)
            >>> spinham.atoms
            {}
            >>> spinham._atoms = {"names" : ["Cr"]}
            >>> spinham.atoms
            {'names': ['Cr']}

        In the latter case correct behavior of magnopy **is not** guaranteed. Use only
        if you have a deep understanding of the magnopy source code.
        """

        return self._atoms

    @atoms.setter
    def atoms(self, new_value):
        raise AttributeError(
            f"Change of the atoms dictionary is not supported after "
            "the creation of SpinHamiltonian instance. If you need to modify atoms, "
            "then use pre-defined methods of SpinHamiltonian or create a new one."
        )

    def _reset_internals(self):
        self._map_to_magnetic = None
        self._map_to_all = None
        self._magnetic_atoms = None

    def _update_internals(self):
        # Identify magnetic sites
        indices = set()

        for alpha, _ in self._1:
            indices.add(alpha)

        for alpha, _ in self._21:
            indices.add(alpha)

        for alpha, beta, _, _ in self._22:
            indices.add(alpha)
            indices.add(beta)

        for alpha, _ in self._31:
            indices.add(alpha)

        for alpha, beta, _, _ in self._32:
            indices.add(alpha)
            indices.add(beta)

        for alpha, beta, gamma, _, _, _ in self._33:
            indices.add(alpha)
            indices.add(beta)
            indices.add(gamma)

        for alpha, _ in self._41:
            indices.add(alpha)

        for alpha, beta, _, _ in self._421:
            indices.add(alpha)
            indices.add(beta)

        for alpha, beta, _, _ in self._422:
            indices.add(alpha)
            indices.add(beta)

        for alpha, beta, gamma, _, _, _ in self._43:
            indices.add(alpha)
            indices.add(beta)
            indices.add(gamma)

        for alpha, beta, gamma, epsilon, _, _, _, _ in self._44:
            indices.add(alpha)
            indices.add(beta)
            indices.add(gamma)
            indices.add(epsilon)

        indices = sorted(list(indices))

        # Create index map from all to magnetic
        self._map_to_magnetic = [None for _ in range(len(self.atoms.names))]
        for i in range(len(indices)):
            self._map_to_magnetic[indices[i]] = i

        # Create index map from magnetic to all
        self._map_to_all = indices

        # Create magnetic atoms dictionary
        self._magnetic_atoms = add_sugar({})
        for key in self.atoms:
            self._magnetic_atoms[key] = []

            for full_index in indices:
                self._magnetic_atoms[key].append(self.atoms[key][full_index])

    @property
    def map_to_magnetic(self):
        r"""
        Index map from all atoms to the magnetic ones.

        Returns
        -------
        map_to_magnetic (L, ) list of int
            Index map. Integers. ``L = len(spinham.atoms.names)``
        """

        if self._map_to_magnetic is None:
            self._update_internals()

        return self._map_to_magnetic

    @property
    def map_to_all(self):
        r"""
        Index map from magnetic atoms to all atoms.

        Returns
        -------
        map_to_all (M, ) list of int
            Index map. Integers. ``M = len(spinham.magnetic_atoms.names)``
        """

        if self._map_to_all is None:
            self._update_internals()

        return self._map_to_all

    @property
    def magnetic_atoms(self):
        r"""
        Magnetic atoms of the spin Hamiltonian.

        Magnetic atom is defined as an atom with at least one parameter associated with
        it.

        This property is dynamically computed at every call.

        Returns
        -------
        magnetic_atoms : list of int
            Indices of magnetic atoms in the ``spinham.atoms``. Sorted.

        See Also
        --------
        M
        """

        if self._magnetic_atoms is None:
            self._update_internals()

        return self._magnetic_atoms

    @property
    def M(self):
        r"""
        Number of spins (magnetic atoms) in the unit cell.

        Returns
        -------
        M : int
            Number of spins (magnetic atoms) in the unit cell.

        See Also
        --------
        magnetic_atoms
        """

        return len(self.magnetic_atoms.names)

    ############################################################################
    #                          Convention properties                           #
    ############################################################################
    @property
    def convention(self) -> Convention:
        r"""
        Convention of the spin Hamiltonian.

        See Also
        --------
        Convention
        """

        return self._convention

    @convention.setter
    def convention(self, new_convention: Convention):
        self._set_multiple_counting(new_convention._multiple_counting)

        self._set_spin_normalization(new_convention._spin_normalized)

        self._set_c1(new_convention._c1)

        self._set_c21(new_convention._c21)
        self._set_c22(new_convention._c22)

        self._set_c31(new_convention._c31)
        self._set_c32(new_convention._c32)
        self._set_c33(new_convention._c33)

        self._set_c41(new_convention._c41)
        self._set_c421(new_convention._c421)
        self._set_c422(new_convention._c422)
        self._set_c43(new_convention._c43)
        self._set_c44(new_convention._c44)

        self._convention = new_convention

    def _set_multiple_counting(self, multiple_counting: bool) -> None:
        if multiple_counting is None or self.convention._multiple_counting is None:
            return

        multiple_counting = bool(multiple_counting)

        if self.convention.multiple_counting == multiple_counting:
            return

        # For (two spins & two sites)

        # It was absent before
        if multiple_counting:
            factor = 0.5
        # It was present before
        else:
            factor = 2.0

        for index in range(len(self._22)):
            self._22[index][3] = self._22[index][3] * factor

        # For (three spins & two sites)

        # It was absent before
        if multiple_counting:
            factor = 0.5
        # It was present before
        else:
            factor = 2.0

        for index in range(len(self._32)):
            self._32[index][3] = self._32[index][3] * factor

        # For (three spins & three sites)

        # It was absent before
        if multiple_counting:
            factor = 1 / 6
        # It was present before
        else:
            factor = 6

        for index in range(len(self._33)):
            self._33[index][5] = self._33[index][5] * factor

        # For (four spins & two sites (3+1))

        # It was absent before
        if multiple_counting:
            factor = 0.5
        # It was present before
        else:
            factor = 2.0

        for index in range(len(self._421)):
            self._421[index][3] = self._421[index][3] * factor

        # For (four spins & two sites (2+2))

        # It was absent before
        if multiple_counting:
            factor = 0.5
        # It was present before
        else:
            factor = 2.0

        for index in range(len(self._422)):
            self._422[index][3] = self._422[index][3] * factor

        # For (four spins & three sites)

        # It was absent before
        if multiple_counting:
            factor = 1 / 6
        # It was present before
        else:
            factor = 6

        for index in range(len(self._43)):
            self._43[index][5] = self._43[index][5] * factor

        # For (four spins & four sites)

        # It was absent before
        if multiple_counting:
            factor = 1 / 24
        # It was present before
        else:
            factor = 24

        for index in range(len(self._44)):
            self._44[index][7] = self._44[index][7] * factor

    def _set_spin_normalization(self, spin_normalized: bool) -> None:
        if spin_normalized is None or self.convention._spin_normalized is None:
            return

        spin_normalized = bool(spin_normalized)

        if self.convention.spin_normalized == spin_normalized:
            return

        # Before it was not normalized
        if spin_normalized:
            # For (one spin & one site)
            for index in range(len(self._1)):
                alpha = self._1[index][0]
                self._1[index][1] = self._1[index][1] * self.atoms.spins[alpha]
            # For (two spins & one site)
            for index in range(len(self._21)):
                alpha = self._21[index][0]
                self._21[index][1] = self._21[index][1] * self.atoms.spins[alpha] ** 2
            # For (two spins & two sites)
            for index in range(len(self._22)):
                alpha = self._22[index][0]
                beta = self._22[index][1]
                self._22[index][3] = self._22[index][3] * (
                    self.atoms.spins[alpha] * self.atoms.spins[beta]
                )
            # For (three spins & one site)
            for index in range(len(self._31)):
                alpha = self._31[index][0]
                self._31[index][1] = self._31[index][1] * self.atoms.spins[alpha] ** 3
            # For (three spins & two sites)
            for index in range(len(self._32)):
                alpha = self._32[index][0]
                beta = self._32[index][1]
                self._32[index][3] = self._32[index][3] * (
                    self.atoms.spins[alpha] ** 2 * self.atoms.spins[beta]
                )
            # For (three spins & three sites)
            for index in range(len(self._33)):
                alpha = self._33[index][0]
                beta = self._33[index][1]
                gamma = self._33[index][2]
                self._33[index][5] = self._33[index][5] * (
                    self.atoms.spins[alpha]
                    * self.atoms.spins[beta]
                    * self.atoms.spins[gamma]
                )
            # For (four spins & one site)
            for index in range(len(self._41)):
                alpha = self._41[index][0]
                self._41[index][1] = self._41[index][1] * self.atoms.spins[alpha] ** 4
            # For (four spins & two sites (3+1))
            for index in range(len(self._421)):
                alpha = self._421[index][0]
                beta = self._421[index][1]
                self._421[index][3] = self._421[index][3] * (
                    self.atoms.spins[alpha] ** 3 * self.atoms.spins[beta]
                )
            # For (four spins & two sites (2+2))
            for index in range(len(self._422)):
                alpha = self._422[index][0]
                beta = self._422[index][1]
                self._422[index][3] = self._422[index][3] * (
                    self.atoms.spins[alpha] ** 2 * self.atoms.spins[beta] ** 2
                )
            # For (four spins & three sites)
            for index in range(len(self._43)):
                alpha = self._43[index][0]
                beta = self._43[index][1]
                gamma = self._43[index][2]
                self._43[index][5] = self._43[index][5] * (
                    self.atoms.spins[alpha] ** 2
                    * self.atoms.spins[beta]
                    * self.atoms.spins[gamma]
                )
            # For (four spins & four sites)
            for index in range(len(self._44)):
                alpha = self._44[index][0]
                beta = self._44[index][1]
                gamma = self._44[index][2]
                epsilon = self._44[index][3]
                self._44[index][7] = self._44[index][7] * (
                    self.atoms.spins[alpha]
                    * self.atoms.spins[beta]
                    * self.atoms.spins[gamma]
                    * self.atoms.spins[epsilon]
                )
        # Before it was normalized
        else:
            # For (one spin & one site)
            for index in range(len(self._1)):
                alpha = self._1[index][0]
                self._1[index][1] = self._1[index][1] / self.atoms.spins[alpha]
            # For (two spins & one site)
            for index in range(len(self._21)):
                alpha = self._21[index][0]
                self._21[index][1] = self._21[index][1] / self.atoms.spins[alpha] ** 2
            # For (two spins & two sites)
            for index in range(len(self._22)):
                alpha = self._22[index][0]
                beta = self._22[index][1]
                self._22[index][3] = self._22[index][3] / (
                    self.atoms.spins[alpha] * self.atoms.spins[beta]
                )
            # For (three spins & one site)
            for index in range(len(self._31)):
                alpha = self._31[index][0]
                self._31[index][1] = self._31[index][1] / self.atoms.spins[alpha] ** 3
            # For (three spins & two sites)
            for index in range(len(self._32)):
                alpha = self._32[index][0]
                beta = self._32[index][1]
                self._32[index][3] = self._32[index][3] / (
                    self.atoms.spins[alpha] ** 2 * self.atoms.spins[beta]
                )
            # For (three spins & three sites)
            for index in range(len(self._33)):
                alpha = self._33[index][0]
                beta = self._33[index][1]
                gamma = self._33[index][2]
                self._33[index][5] = self._33[index][5] / (
                    self.atoms.spins[alpha]
                    * self.atoms.spins[beta]
                    * self.atoms.spins[gamma]
                )
            # For (four spins & one site)
            for index in range(len(self._41)):
                alpha = self._41[index][0]
                self._41[index][1] = self._41[index][1] / self.atoms.spins[alpha] ** 4
            # For (four spins & two sites (3+1))
            for index in range(len(self._421)):
                alpha = self._421[index][0]
                beta = self._421[index][1]
                self._421[index][3] = self._421[index][3] / (
                    self.atoms.spins[alpha] ** 3 * self.atoms.spins[beta]
                )
            # For (four spins & two sites (2+2))
            for index in range(len(self._422)):
                alpha = self._422[index][0]
                beta = self._422[index][1]
                self._422[index][3] = self._422[index][3] / (
                    self.atoms.spins[alpha] ** 2 * self.atoms.spins[beta] ** 2
                )
            # For (four spins & three sites)
            for index in range(len(self._43)):
                alpha = self._43[index][0]
                beta = self._43[index][1]
                gamma = self._43[index][2]
                self._43[index][5] = self._43[index][5] / (
                    self.atoms.spins[alpha] ** 2
                    * self.atoms.spins[beta]
                    * self.atoms.spins[gamma]
                )
            # For (four spins & four sites)
            for index in range(len(self._44)):
                alpha = self._44[index][0]
                beta = self._44[index][1]
                gamma = self._44[index][2]
                epsilon = self._44[index][3]
                self._44[index][7] = self._44[index][7] / (
                    self.atoms.spins[alpha]
                    * self.atoms.spins[beta]
                    * self.atoms.spins[gamma]
                    * self.atoms.spins[epsilon]
                )

    def _set_c1(self, new_c1: float) -> None:
        if new_c1 is None or self.convention._c1 is None:
            return

        new_c1 = float(new_c1)

        if self.convention.c1 == new_c1:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._1)):
            self._1[index][1] = self._1[index][1] * self.convention.c1 / new_c1

    def _set_c21(self, new_c21: float) -> None:
        if new_c21 is None or self.convention._c21 is None:
            return

        new_c21 = float(new_c21)

        if self.convention.c21 == new_c21:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._21)):
            self._21[index][1] = self._21[index][1] * self.convention.c21 / new_c21

    def _set_c22(self, new_c22: float) -> None:
        if new_c22 is None or self.convention._c22 is None:
            return

        new_c22 = float(new_c22)

        if self.convention.c22 == new_c22:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._22)):
            self._22[index][3] = self._22[index][3] * self.convention.c22 / new_c22

    def _set_c31(self, new_c31: float) -> None:
        if new_c31 is None or self.convention._c31 is None:
            return

        new_c31 = float(new_c31)

        if self.convention.c31 == new_c31:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._31)):
            self._31[index][1] = self._31[index][1] * self.convention.c31 / new_c31

    def _set_c32(self, new_c32: float) -> None:
        if new_c32 is None or self.convention._c32 is None:
            return

        new_c32 = float(new_c32)

        if self.convention.c32 == new_c32:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._32)):
            self._32[index][3] = self._32[index][3] * self.convention.c32 / new_c32

    def _set_c33(self, new_c33: float) -> None:
        if new_c33 is None or self.convention._c33 is None:
            return

        new_c33 = float(new_c33)

        if self.convention.c33 == new_c33:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._33)):
            self._33[index][5] = self._33[index][5] * self.convention.c33 / new_c33

    def _set_c41(self, new_c41: float) -> None:
        if new_c41 is None or self.convention._c41 is None:
            return

        new_c41 = float(new_c41)

        if self.convention.c41 == new_c41:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._41)):
            self._41[index][1] = self._41[index][1] * self.convention.c41 / new_c41

    def _set_c421(self, new_c421: float) -> None:
        if new_c421 is None or self.convention._c421 is None:
            return

        new_c421 = float(new_c421)

        if self.convention.c421 == new_c421:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._421)):
            self._421[index][3] = self._421[index][3] * self.convention.c421 / new_c421

    def _set_c422(self, new_c422: float) -> None:
        if new_c422 is None or self.convention._c422 is None:
            return

        new_c422 = float(new_c422)

        if self.convention.c422 == new_c422:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._422)):
            self._422[index][3] = self._422[index][3] * self.convention.c422 / new_c422

    def _set_c43(self, new_c43: float) -> None:
        if new_c43 is None or self.convention._c43 is None:
            return

        new_c43 = float(new_c43)

        if self.convention.c43 == new_c43:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._43)):
            self._43[index][5] = self._43[index][5] * self.convention.c43 / new_c43

    def _set_c44(self, new_c44: float) -> None:
        if new_c44 is None or self.convention._c44 is None:
            return

        new_c44 = float(new_c44)

        if self.convention.c44 == new_c44:
            return

        # If factor is changing one has to scale parameters.
        for index in range(len(self._44)):
            self._44[index][7] = self._44[index][7] * self.convention.c44 / new_c44

    def add_magnetic_field(self, h) -> None:
        r"""
        Adds external magnetic field to the Hamiltonian in the form of one spin
        parameters.

        .. math::

            \mu_B \boldsymbol{h}\cdot\sum_{\mu,\alpha} g_{\alpha} \boldsymbol{S}_{\mu,\alpha}

        Parameters
        ----------
        h : (3, ) |array-like|_
            Vector of magnetic field given in the units of Tesla.

        Notes
        -----
        If Hamiltonian read from TB2J or GROGU, then by default g factors are positive (=2).
        Therefore, to minimize the energy the magnetic moment will be aligned with the
        direction of the external field. But pin vector will be directed opposite to the
        direction of the magnetic field.

        Magnetic field is added *only* to the magnetic atoms. In other words, magnetic
        field is added only to the atoms that have at least one other parameter
        associated with them.
        """

        if self.convention._c1 is None:
            self.convention._c1 = 1.0

        h = np.array(h, dtype=float)

        BOHR_MAGNETON = 0.057883818060  # meV / Tesla

        new_1 = []

        for i in range(0, self.M):
            new_1.append(
                BOHR_MAGNETON
                * self.magnetic_atoms.g_factors[i]
                * h
                / self.convention.c1
            )

        for alpha, parameter in self._1:
            new_1[self.map_to_magnetic[alpha]] = (
                new_1[self.map_to_magnetic[alpha]] + parameter
            )

        self._1 = list(map(list, zip(range(self.M), new_1)))

    ############################################################################
    #                                Copy getter                               #
    ############################################################################
    def copy(self):
        R"""
        Returns a new, independent copy of the same Hamiltonian.

        Returns
        -------
        spinham : :py:class:`.SpinHamiltonian`
            A new instance of the same Hamiltonian.
        """

        return deepcopy(self)

    ############################################################################
    #                            One spin & one site                           #
    ############################################################################
    p1 = _p1
    add_1 = _add_1
    remove_1 = _remove_1

    ############################################################################
    #                           Two spins & one site                           #
    ############################################################################
    p21 = _p21
    add_21 = _add_21
    remove_21 = _remove_21

    ############################################################################
    #                           Two spins & two sites                          #
    ############################################################################
    p22 = _p22
    add_22 = _add_22
    remove_22 = _remove_22

    ############################################################################
    #                          Three spins & one site                          #
    ############################################################################
    p31 = _p31
    add_31 = _add_31
    remove_31 = _remove_31

    ############################################################################
    #                          Three spins & two sites                         #
    ############################################################################
    p32 = _p32
    add_32 = _add_32
    remove_32 = _remove_32

    ############################################################################
    #                         Three spins & three sites                        #
    ############################################################################
    p33 = _p33
    add_33 = _add_33
    remove_33 = _remove_33

    ############################################################################
    #                           Four spins & one site                          #
    ############################################################################
    p41 = _p41
    add_41 = _add_41
    remove_41 = _remove_41

    ############################################################################
    #                          Four spins & two sites (3+1)                    #
    ############################################################################
    p421 = _p421
    add_421 = _add_421
    remove_421 = _remove_421

    ############################################################################
    #                          Four spins & two sites (2+2)                    #
    ############################################################################
    p422 = _p422
    add_422 = _add_422
    remove_422 = _remove_422

    ############################################################################
    #                         Four spins & three sites                         #
    ############################################################################
    p43 = _p43
    add_43 = _add_43
    remove_43 = _remove_43

    ############################################################################
    #                          Four spins & four sites                         #
    ############################################################################
    p44 = _p44
    add_44 = _add_44
    remove_44 = _remove_44


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
