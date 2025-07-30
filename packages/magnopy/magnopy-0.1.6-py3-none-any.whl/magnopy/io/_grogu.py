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
from magnopy._spinham._hamiltonian import SpinHamiltonian

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def load_grogu(filename) -> SpinHamiltonian:
    r"""
    Load a SpinHamiltonian object from a .txt file produced by GROGU.

    Parameters
    ----------
    filename : str
        Filename to load SpinHamiltonian object from.

    Returns
    -------
    spinham :py:class:`.SpinHamiltonian`
        SpinHamiltonian object loaded from file.
    """

    # Read the content of the file
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while "Cell Angstrom" not in lines[i]:
        i += 1

    i += 1

    cell = [
        list(map(float, lines[i].split())),
        list(map(float, lines[i + 1].split())),
        list(map(float, lines[i + 2].split())),
    ]
    i += 2

    while "Atoms Angstrom" not in lines[i]:
        i += 1

    i += 2
    line = lines[i]
    atoms = dict(names=[], positions=[], spins=[], g_factors=[])
    index_map = {}
    atom_index = 0
    while len(lines[i].split()) > 0:
        line = lines[i].split()

        atoms["names"].append(line[0])
        atoms["positions"].append(list(map(float, line[1:4])))
        atoms["spins"].append(np.linalg.norm(list(map(float, line[5:8]))))
        atoms["g_factors"].append(2)
        index_map[line[0]] = atom_index
        atom_index += 1

        i += 1

    convention = Convention(
        multiple_counting=True, spin_normalized=True, c22=0.5, c21=1
    )

    # Construct spin Hamiltonian:
    spinham = SpinHamiltonian(convention=convention, cell=cell, atoms=atoms)

    while "Exchange tensor meV" not in lines[i]:
        i += 1

    i += 4
    while len(lines[i].split()) > 0:
        line = lines[i].split()

        alpha = index_map[line[0]]
        beta = index_map[line[1]]

        nu = tuple(list(map(int, line[2:5])))

        i += 2

        parameter = [
            list(map(float, lines[i].split())),
            list(map(float, lines[i + 1].split())),
            list(map(float, lines[i + 2].split())),
        ]

        i += 4

        spinham.add_22(alpha=alpha, beta=beta, nu=nu, parameter=parameter, replace=True)

    while "Intra-atomic anisotropy tensor meV" not in lines[i]:
        i += 1

    i += 2
    while i < len(lines) and len(lines[i].split()) > 0:
        line = lines[i].split()

        alpha = index_map[line[0]]

        i += 2

        parameter = [
            list(map(float, lines[i].split())),
            list(map(float, lines[i + 1].split())),
            list(map(float, lines[i + 2].split())),
        ]

        i += 4

        spinham.add_21(alpha=alpha, parameter=parameter)

    return spinham


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
