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


import os

import numpy as np
import wulfric

from magnopy._energy import Energy
from magnopy._lswt import LSWT
from magnopy._package_info import logo
from magnopy._parallelization import multiprocess_over_k
from magnopy._spinham._hamiltonian import SpinHamiltonian
from magnopy.io._grogu import load_grogu
from magnopy.io._k_resolved import output_k_resolved, plot_k_resolved
from magnopy.io._spin_directions import read_spin_directions
from magnopy.io._tb2j import load_tb2j

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def solve_lswt(
    spinham_filename: str,
    spinham_source: str,
    spin_directions,
    spins=None,
    k_path=None,
    kpoints=None,
    relative=False,
    magnetic_field=None,
    output_folder="magnopy-results",
    number_processors=None,
) -> None:
    r"""
    Solves the spin Hamiltonian at the level of Linear Spin Wave theory.
    Outputs progress in the standart output (``print()``) and saves some data to
    the files on the disk.

    Parameters
    ----------
    spinham_filename : str
        File with the parameters of spin Hamiltonian.
    spinham_source : str
        Source of the parameters of the spin Hamiltonian.
        One of the "TB2J" or "GROGU". Case-insensitive.
    spin_directions : (M, 3) |array-like|_
        Directions of the local quantization axis for each spin. Magnitude of the vector
        is ignored, only the direction is considered.
    spins : (M, ) |array-like|_, optional
        Spin values. Optional if the spin Hamiltonian is loaded from |TB2J|_. Ignored if
        spin Hamiltonian is loaded from GROGU.
    k_path : str, optional
        Specification of the k-path. The format is "G-X-Y|G-Z" For more details
        on the format see documentation of |Wulfric|_. If nothing given, then the
        k-path is computed by |Wulfric|_ automatically based on the lattice type.
        Ignored if ``kpoints`` are given.
    kpoints : (N, 3) |array-like|_, optional
        Explicit list of k-points to be used instead of automatically generated.
    relative : bool, default False
        If ``relative == True``, then ``kpoints`` are interpreted as given relative to
        the reciprocal unit cell. Otherwise it is interpreted as given in absolute
        coordinates.
    magnetic_field : (3, ) |array-like|_
        Vector of external magnetic field, given in Tesla.
    output_folder : str, default "magnopy-results"
        Name for the folder where to save the output files. If the folder does not exist
        then it will be created.
    number_processors : int, optional
        Number of processors to be used in computation. By default magnopy uses all
        available processes. Use ``number_processors=1`` to run in serial mode.

    Raises
    ------
    ValueError
        If ``spinham_source`` is not supported.
    """

    all_good = True

    print(logo())
    print(f"\n{' Start LSWT ':=^90}\n")

    # Create the output directory if it does not exist
    os.makedirs(output_folder, exist_ok=True)

    # Load spin Hamiltonian
    if spinham_source.lower() == "tb2j":
        spinham = load_tb2j(filename=spinham_filename, spins=spins)
    elif spinham_source.lower() == "grogu":
        spinham = load_grogu(filename=spinham_filename)
    else:
        raise ValueError(
            'Supported sources of spin Hamiltonians are "GROGU" and "TB2J", '
            f'got "{spinham_source}".'
        )

    print(f'Source of the parameters is "{spinham_source.upper()}".')
    print(
        f"Loaded parameters of the spin Hamiltonian from the file\n  "
        f"{os.path.abspath(spinham_filename)}."
    )

    if magnetic_field is not None:
        spinham.add_magnetic_field(h=magnetic_field)

    # Treat kpoints
    if kpoints is not None:
        kpoints = np.array(kpoints, dtype=float)
        if relative:
            kpoints = kpoints @ wulfric.cell.get_reciprocal(cell=spinham.cell)
        kp = None
        flat_indices = None
    else:
        kp = wulfric.Kpoints.from_cell(cell=spinham.cell)
        # Set custom k path
        if k_path is not None:
            kp.path = k_path
        print(f"\n{wulfric.cell.get_variation(spinham.cell)} crystal detected.")
        kpoints = kp.points(relative=False)
        flat_indices = kp.flatten_points(relative=False)

        print("\nList of high symmetry k points")

        header_names = ["k_b1", "k_b2", "k_b3", "k_x", "k_y", "k_z"]
        print(
            " ".join(
                [f"{'name':<5}", f"{'label':>10}"]
                + [f"{tmp:>10}" for tmp in header_names]
            )
        )
        for n_i, name in enumerate(kp.hs_names):
            line = [f"{name:<5}", f"{kp.hs_labels[name]:>10}"]
            for comp in kp.hs_coordinates[name]:
                line.append(f"{comp:>10.6f}")
            rcell = wulfric.cell.get_reciprocal(cell=spinham.cell)
            for comp in kp.hs_coordinates[name] @ rcell:
                line.append(f"{comp:>10.6f}")
            print(" ".join(line))

        print(f'\nK path is "{kp.path_string}"')
        print("\nFlat indices and labels of the points in k path are")
        print(
            "  "
            + "\n  ".join(
                [
                    f"{label:<10} {tick:>12.8f}"
                    for (label, tick) in zip(kp.labels, kp.ticks(relative=False))
                ]
            )
        )

    # Treat spin directions
    spin_directions = np.array(spin_directions, dtype=float)
    spin_directions = (
        spin_directions / np.linalg.norm(spin_directions, axis=1)[:, np.newaxis]
    )

    E_0 = Energy(spinham=spinham).E_0(spin_directions=spin_directions)
    lswt = LSWT(spinham=spinham, spin_directions=spin_directions)

    print(
        f"\n{'Classic ground state energy (E_0)':<51} : "
        f"{E_0:>15.6f} meV\n"
        f"{'Correction to the classic ground state energy (E_2)':<50} : "
        f"{lswt.E_2:>15.6f} meV\n"
    )

    print(
        "Coefficient before one-operator terms (shall be zero if the ground state is correct)"
    )

    print("  " + "\n  ".join([f"{o:12.8f}" for o in lswt.O]))

    if not np.allclose(lswt.O, np.zeros(lswt.O.shape)):
        all_good = False
        print(f"\n{'  WARNING  ':!^90}")
        print(
            "Coefficients before the one-operator terms are not zero. It might indicate  that\n"
            "the ground state (spin directions) is not a ground state of the considered spin\n"
            "Hamiltonian. The results might not be meaningful."
        )
        print(f"{'  END OF WARNING  ':!^90}\n")

    print(f"\nStart calculations over k ... ", end="")
    # Shape (N, M)
    kwargs = dict(relative=relative)

    results = multiprocess_over_k(
        kpoints,
        function=lswt.diagonalize,
        relative=False,
        number_processors=number_processors,
    )

    omegas = np.array([i[0] for i in results])
    deltas = np.array([i[1] for i in results])
    transformation_matrices = np.array([i[2] for i in results])
    print("Done")

    filename = os.path.join(output_folder, "OMEGAS.txt")
    output_k_resolved(
        data=omegas.real,
        data_headers=[f"mode {i+1}" for i in range(len(omegas[0]))],
        output_filename=filename,
        kpoints=kpoints,
        relative=False,
        rcell=wulfric.cell.get_reciprocal(cell=spinham.cell),
        flat_indices=flat_indices,
        digits=6,
        scientific_notation=True,
    )
    print(f"\nOmegas are saved in file\n  {os.path.abspath(filename)}")

    filename = filename[:-4] + ".png"
    plot_k_resolved(
        data=omegas.real,
        kp=kp,
        output_filename=filename,
        ylabel=R"$\omega_{\alpha}(\boldsymbol{k})$, meV",
    )
    print(f"Plot is saved in file\n  {os.path.abspath(filename)}")

    if not np.allclose(omegas.imag, np.zeros(omegas.imag.shape)):
        all_good = False
        print(f"\n{'  WARNING  ':!^90}")
        print(
            "Eigenfrequiencies has non-zero imaginary component for some k vectors. It might\n"
            "indicate that the ground state (spin directions) is not a ground state of the\n"
            "considered spin Hamiltonian. The results might not be meaningful.\n"
        )
        filename = os.path.join(output_folder, "OMEGAS-IMAG.txt")
        output_k_resolved(
            data=omegas.imag,
            data_headers=[f"mode {i+1}" for i in range(len(omegas[0]))],
            output_filename=filename,
            kpoints=kpoints,
            relative=False,
            rcell=wulfric.cell.get_reciprocal(cell=spinham.cell),
            flat_indices=(flat_indices),
            digits=6,
            scientific_notation=True,
        )
        print(
            "Imaginary part of omegas is saved in file\n  "
            f"{os.path.abspath(filename)}"
        )

        filename = filename[:-4] + ".png"
        plot_k_resolved(
            data=omegas.imag,
            kp=kp,
            output_filename=filename,
            ylabel=R"$\mathcal{Im}(\omega_{\alpha}(\boldsymbol{k}))$, meV",
        )
        print(f"Plot of imaginary part is saved in file\n  {os.path.abspath(filename)}")
        print(f"{'  END OF WARNING  ':!^90}\n")

    filename = os.path.join(output_folder, "DELTAS.txt")
    output_k_resolved(
        data=deltas.real,
        data_headers=["Delta"],
        output_filename=filename,
        kpoints=kpoints,
        relative=False,
        rcell=wulfric.cell.get_reciprocal(cell=spinham.cell),
        flat_indices=flat_indices,
        digits=6,
        scientific_notation=True,
    )
    print(f"Deltas are saved in file\n  {os.path.abspath(filename)}")

    filename = filename[:-4] + ".png"
    plot_k_resolved(
        data=deltas.real,
        kp=kp,
        output_filename=filename,
        ylabel=R"$\Delta(\boldsymbol{k})$, meV",
    )
    print(f"Plot is saved in file\n  {os.path.abspath(filename)}")

    if all_good:
        print(f"\n{' Finished OK ':=^90}")
    else:
        print(f"\n{' Finished with WARNINGS ':=^90}")


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
