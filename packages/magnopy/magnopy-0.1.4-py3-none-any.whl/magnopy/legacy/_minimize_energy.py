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
from argparse import ArgumentParser

import numpy as np

from magnopy._osfix import _winwait
from magnopy._package_info import logo
from magnopy.energy.sub_types import C1, C2, C5
from magnopy.io import load_spinham

_logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="log.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


def _minimize_C1(energy, spinham, seedname, output_file, spin_output_file):
    output_file.write(
        f"Start to minimize assuming C1 ground state type.\n"
        "Variation with respect to the direction vectors.\n"
    )
    direction_vectors = energy.optimize()
    output_file.write(
        "Minimization for C1 sub-type is done.\n"
        "Spin orientations in the minimum configuration:\n"
    )
    output_file.write(
        f"  {'name':>5} {'r1':>11} {'r2':>11} {'r3':>11} {'sx':>11} {'sy':>11} {'sz':>11}\n"
    )
    for i, spin in enumerate(direction_vectors):
        pos = spinham.magnetic_atoms[i].position
        line = (
            f"  {spinham.magnetic_atoms[i].name:>5} "
            f"{pos[0]:11.8f} {pos[1]:11.8f} {pos[2]:11.8f} "
            f"{spin[0]:11.8f} {spin[1]:11.8f} {spin[2]:11.8f}\n"
        )
        output_file.write(line)
        spin_output_file.write(line)
    direction_vectors /= np.linalg.norm(direction_vectors, axis=1)[:, np.newaxis]
    output_file.write(f"\n Energy: {energy.energy(direction_vectors)}\n")


def _minimize_C2(energy, spinham, seedname, output_file, spin_output_file):
    output_file.write(
        f"Start to minimize assuming C2 ground state type.\n"
        "Variation with respect to the direction vectors, cone axis and spiral vector.\n"
    )
    direction_vectors, cone_axis = energy.optimize()
    output_file.write(
        "Minimization for C2 sub-type is done.\n"
        "Spin orientations in the minimum configuration:\n"
    )
    output_file.write(
        f"  {'name':>5} {'r1':>11} {'r2':>11} {'r3':>11} {'sx':>11} {'sy':>11} {'sz':>11}\n"
    )
    for i, spin in enumerate(direction_vectors):
        pos = spinham.magnetic_atoms[i].position
        line = (
            f"  {spinham.magnetic_atoms[i].name:>5} "
            f"{pos[0]:11.8f} {pos[1]:11.8f} {pos[2]:11.8f} "
            f"{spin[0]:11.8f} {spin[1]:11.8f} {spin[2]:11.8f}\n"
        )
        output_file.write(line)
        spin_output_file.write(line)
    direction_vectors /= np.linalg.norm(direction_vectors, axis=1)[:, np.newaxis]
    output_file.write(
        f"Cone axis: {cone_axis[0]:12.8f} {cone_axis[1]:12.8f} {cone_axis[2]:12.8f}\n"
    )
    output_file.write(f"\n Energy: {energy.energy(direction_vectors, cone_axis)}\n")


def _minimize_C5(energy, spinham, seedname, output_file, spin_output_file):
    output_file.write(
        f"Start to minimize assuming C5 ground state type.\n"
        "Variation with respect to the direction vectors, cone axis and spiral vector.\n"
    )
    direction_vectors, cone_axis, spiral_vector = energy.optimize()
    output_file.write(
        "Minimization for C5 sub-type is done.\n"
        "Spin orientations in the minimum configuration:\n"
    )
    output_file.write(
        f"  {'name':>5} {'r1':>11} {'r2':>11} {'r3':>11} {'sx':>11} {'sy':>11} {'sz':>11}\n"
    )
    for i, spin in enumerate(direction_vectors):
        pos = spinham.magnetic_atoms[i].position
        line = (
            f"  {spinham.magnetic_atoms[i].name:>5} "
            f"{pos[0]:11.8f} {pos[1]:11.8f} {pos[2]:11.8f} "
            f"{spin[0]:11.8f} {spin[1]:11.8f} {spin[2]:11.8f}\n"
        )
        output_file.write(line)
        spin_output_file.write(line)
    direction_vectors /= np.linalg.norm(direction_vectors, axis=1)[:, np.newaxis]
    output_file.write(
        f"Cone axis: {cone_axis[0]:12.8f} {cone_axis[1]:12.8f} {cone_axis[2]:12.8f}\n"
    )
    output_file.write(
        f"Spiral vector: {spiral_vector[0]:12.8f} {spiral_vector[1]:12.8f} {spiral_vector[2]:12.8f}\n"
    )
    output_file.write(
        f"\n Energy: {energy.energy(direction_vectors, cone_axis, spiral_vector)}\n"
    )


def manager(
    spinham,
    spinham_format=None,
    ground_state_type=None,
    magnetic_field=None,
    output_seedname="minim",
):
    # Open main output file
    output_file = open(f"{output_seedname}-results", "w")
    spin_output_file = open(f"{output_seedname}-spins.txt", "w")
    # Write a logo
    output_file.write(logo(date_time=True) + "\n")

    # Load spin Hamiltonian from the input file
    spinham = load_spinham(spinham, spinham_format=spinham_format)

    # Decide which ground state types to minimize
    if "all" in ground_state_type:
        gs_to_minimize = [f"C{i}" for i in range(1, 6)]
    else:
        gs_to_minimize = ground_state_type

    energies = []
    for gs in gs_to_minimize:
        if gs == "C1":
            # Create an instance of the energy class
            energy = C1(spinham)

            # Put some magnetic field into it
            if magnetic_field is not None:
                energy.magnetic_field = magnetic_field
            energies.append(
                _minimize_C1(
                    energy, spinham, output_seedname, output_file, spin_output_file
                )
            )
        elif gs == "C2":
            # Create an instance of the energy class
            energy = C2(spinham)

            # Put some magnetic field into it
            if magnetic_field is not None:
                energy.magnetic_field = magnetic_field
            energies.append(
                _minimize_C2(
                    energy, spinham, output_seedname, output_file, spin_output_file
                )
            )
        elif gs == "C5":
            # Create an instance of the energy class
            energy = C5(spinham)

            # Put some magnetic field into it
            if magnetic_field is not None:
                energy.magnetic_field = magnetic_field
            energies.append(
                _minimize_C5(
                    energy, spinham, output_seedname, output_file, spin_output_file
                )
            )
        else:
            output_file.write(
                f"Minimization for {gs} ground state type is not implemented yet.\n"
            )

    output_file.write("All minimization routines are finished\n")


def create_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-sh",
        "--spinham",
        type=str,
        required=True,
        help="Relative or absolute path to the file with spin Hamiltonian, "
        "including the name and extension of the file. ",
    )
    parser.add_argument(
        "-shf",
        "--spinham-format",
        type=str,
        choices=["txt", "hdf5", "tb2j"],
        default=None,
        help="Format of the file with spin Hamiltonian.",
    )
    parser.add_argument(
        "-gst",
        "--ground-state-type",
        nargs="*",
        type=str,
        choices=["all", "C1", "C2", "C3", "C4", "C5"],
        default="all",
        help="Type of the ground state to be assumed for the minimization.",
    )
    parser.add_argument(
        "-mf",
        "--magnetic_field",
        default=None,
        type=float,
        nargs=3,
        help="External magnetic field.",
        metavar="Hx Hy Hz",
    )
    parser.add_argument(
        "-os",
        "--output-seedname",
        type=str,
        default="minim",
        help="Seedname for output files",
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    manager(**vars(args))
    _winwait()


if __name__ == "__main__":
    main()
