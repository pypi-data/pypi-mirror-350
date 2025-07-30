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


import numpy as np

from magnopy._spinham._convention import Convention

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class Energy:
    r"""
    Ground state energy of the given spin Hamiltonian.

    This class is optimized for the computation of the energy for any spin
    directions for the given Hamiltonian.

    If the spin Hamiltonian is modified, then a new instance of the energy class
    should be created from it.

    Parameters
    ----------
    spinham : py:class:.SpinHamiltonian`
        Spin Hamiltonian for the calculation of energy.
    """

    def __init__(self, spinham):
        initial_convention = spinham.convention

        magnopy_convention = initial_convention.get_modified(
            spin_normalized=False, multiple_counting=False
        )

        spinham.convention = magnopy_convention

        self.spins = np.array(spinham.magnetic_atoms.spins, dtype=float)

        ########################################################################
        #                               One spin                               #
        ########################################################################

        self.J_1 = np.zeros((spinham.M, 3), dtype=float)

        for atom, parameter in spinham.p1:
            alpha = spinham.map_to_magnetic[atom]

            self.J_1[alpha] += spinham.convention.c1 * parameter

        ########################################################################
        #                               Two spins                              #
        ########################################################################

        self.J_21 = np.zeros((spinham.M, 3, 3), dtype=float)

        for atom, parameter in spinham.p21:
            alpha = spinham.map_to_magnetic[atom]

            self.J_21[alpha] += spinham.convention.c21 * parameter

        self.J_22 = {}

        for atom1, atom2, _, parameter in spinham.p22:
            alpha = spinham.map_to_magnetic[atom1]
            beta = spinham.map_to_magnetic[atom2]

            if (alpha, beta) not in self.J_22:
                self.J_22[(alpha, beta)] = np.zeros((3, 3), dtype=float)

            self.J_22[(alpha, beta)] += spinham.convention.c22 * parameter

        ########################################################################
        #                              Three spins                             #
        ########################################################################

        self.J_31 = np.zeros((spinham.M, 3, 3, 3), dtype=float)

        for atom, parameter in spinham.p31:
            alpha = spinham.map_to_magnetic[atom]

            self.J_31[alpha] += spinham.convention.c31 * parameter

        self.J_32 = {}

        for atom1, atom2, _, parameter in spinham.p32:
            alpha = spinham.map_to_magnetic[atom1]
            beta = spinham.map_to_magnetic[atom2]

            if (alpha, beta) not in self.J_32:
                self.J_32[(alpha, beta)] = np.zeros((3, 3, 3), dtype=float)

            self.J_32[(alpha, beta)] += spinham.convention.c32 * parameter

        self.J_33 = {}

        for atom1, atom2, atom3, _, _, parameter in spinham.p33:
            alpha = spinham.map_to_magnetic[atom1]
            beta = spinham.map_to_magnetic[atom2]
            gamma = spinham.map_to_magnetic[atom3]

            if (alpha, beta, gamma) not in self.J_33:
                self.J_33[(alpha, beta, gamma)] = np.zeros((3, 3, 3), dtype=float)

            self.J_33[(alpha, beta, gamma)] += spinham.convention.c33 * parameter

        ########################################################################
        #                              Four spins                              #
        ########################################################################

        self.J_41 = np.zeros((spinham.M, 3, 3, 3, 3), dtype=float)

        for atom, parameter in spinham.p41:
            alpha = spinham.map_to_magnetic[atom]

            self.J_41[alpha] += spinham.convention.c41 * parameter

        self.J_421 = {}

        for atom1, atom2, _, parameter in spinham.p421:
            alpha = spinham.map_to_magnetic[atom1]
            beta = spinham.map_to_magnetic[atom2]

            if (alpha, beta) not in self.J_421:
                self.J_421[(alpha, beta)] = np.zeros((3, 3, 3, 3), dtype=float)

            self.J_421[(alpha, beta)] += spinham.convention.c421 * parameter

        self.J_422 = {}

        for atom1, atom2, _, parameter in spinham.p422:
            alpha = spinham.map_to_magnetic[atom1]
            beta = spinham.map_to_magnetic[atom2]

            if (alpha, beta) not in self.J_422:
                self.J_422[(alpha, beta)] = np.zeros((3, 3, 3, 3), dtype=float)

            self.J_422[(alpha, beta)] += spinham.convention.c422 * parameter

        self.J_43 = {}

        for atom1, atom2, atom3, _, _, parameter in spinham.p43:
            alpha = spinham.map_to_magnetic[atom1]
            beta = spinham.map_to_magnetic[atom2]
            gamma = spinham.map_to_magnetic[atom3]

            if (alpha, beta, gamma) not in self.J_43:
                self.J_43[(alpha, beta, gamma)] = np.zeros((3, 3, 3, 3), dtype=float)

            self.J_43[(alpha, beta, gamma)] += spinham.convention.c43 * parameter

        self.J_44 = {}

        for atom1, atom2, atom3, atom4, _, _, _, parameter in spinham.p44:
            alpha = spinham.map_to_magnetic[atom1]
            beta = spinham.map_to_magnetic[atom2]
            gamma = spinham.map_to_magnetic[atom3]
            epsilon = spinham.map_to_magnetic[atom4]

            if (alpha, beta, gamma, epsilon) not in self.J_44:
                self.J_44[(alpha, beta, gamma, epsilon)] = np.zeros(
                    (3, 3, 3, 3), dtype=float
                )

            self.J_44[(alpha, beta, gamma, epsilon)] += (
                spinham.convention.c44 * parameter
            )

        spinham.convention = initial_convention

    def E_0(self, spin_directions) -> float:
        r"""

        Parameters
        ----------
        spin_directions : (M, 3) |array-like|_
            Directions of spin vectors. Only directions of vectors are used,
            modulus is ignored. ``M`` is the amount of magnetic atoms in the
            Hamiltonian. The order of spin directions is the same as the order
            of magnetic atoms in ``spinham.magnetic_atoms.spins``.

        Returns
        -------
        E_0 : float
            Classic energy of state with ``spin_directions``.
        """

        spin_directions = np.array(spin_directions, dtype=float)
        spin_directions /= np.linalg.norm(spin_directions, axis=1)[:, np.newaxis]
        spins = spin_directions * self.spins[:, np.newaxis]

        energy = 0

        energy += np.diag(self.J_1 @ spins.T).sum()

        energy += np.einsum("mij,mi,mj->m", self.J_21, spins, spins).sum()

        energy += np.einsum("miju,mi,mj,mu->m", self.J_31, spins, spins, spins).sum()

        energy += np.einsum(
            "mijuv,mi,mj,mu,mv->m", self.J_41, spins, spins, spins, spins
        ).sum()

        for alpha, beta in self.J_22:
            energy += spins[alpha] @ self.J_22[(alpha, beta)] @ spins[beta]

        for alpha, beta in self.J_32:
            energy += np.einsum(
                "iju,i,j,u",
                self.J_32[(alpha, beta)],
                spins[alpha],
                spins[alpha],
                spins[beta],
            )

        for alpha, beta in self.J_421:
            energy += np.einsum(
                "ijuv,i,j,u,v",
                self.J_421[(alpha, beta)],
                spins[alpha],
                spins[alpha],
                spins[alpha],
                spins[beta],
            )

        for alpha, beta in self.J_422:
            energy += np.einsum(
                "ijuv,i,j,u,v",
                self.J_422[(alpha, beta)],
                spins[alpha],
                spins[alpha],
                spins[beta],
                spins[beta],
            )

        for alpha, beta, gamma in self.J_33:
            energy += np.einsum(
                "iju,i,j,u",
                self.J_33[(alpha, beta, gamma)],
                spins[alpha],
                spins[beta],
                spins[gamma],
            )

        for alpha, beta, gamma in self.J_43:
            energy += np.einsum(
                "ijuv,i,j,u,v",
                self.J_43[(alpha, beta, gamma)],
                spins[alpha],
                spins[alpha],
                spins[beta],
                spins[gamma],
            )

        for alpha, beta, gamma, epsilon in self.J_44:
            energy += np.einsum(
                "ijuv,i,j,u,v",
                self.J_44[(alpha, beta, gamma, epsilon)],
                spins[alpha],
                spins[beta],
                spins[gamma],
                spins[epsilon],
            )

        return float(energy)


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
