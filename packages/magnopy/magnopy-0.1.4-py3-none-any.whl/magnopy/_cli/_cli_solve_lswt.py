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
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

import numpy as np

from magnopy._package_info import logo
from magnopy.io._spin_directions import read_spin_directions
from magnopy.scenarios._solve_lswt import solve_lswt


def manager():
    parser = get_parser()

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if len(args.spin_directions) == 1:
        args.spin_directions = read_spin_directions(filename=args.spin_directions)
    else:
        args.spin_directions = np.array(args.spin_directions)
        args.spin_directions = args.spin_directions.reshape(
            (len(args.spin_directions) // 3, 3)
        )

    if args.spins is not None:
        args.spins = [float(tmp) for tmp in args.spins]

    kpoints = []
    if args.kpoints is not None:
        with open(args.kpoints, "r") as f:
            for line in f:
                # Remove comment lines
                if line.startswith("#"):
                    continue
                # Remove inline comments and leading/trailing whitespaces
                line = line.split("#")[0].strip()
                # Check for empty lines empty lines
                if line:
                    line = line.split()
                    if len(line) != 3:
                        raise ValueError(
                            f"Expected three numbers per line (in line{i}),"
                            f"got: {len(line)}."
                        )

                    kpoints.append(list(map(float, line)))

        args.kpoints = kpoints

    solve_lswt(**vars(args))


def get_parser():
    parser = ArgumentParser(
        description=logo()
        + "\n\nThis script solves the spin Hamiltonian at the level of "
        "Linear Spin Wave Theory (LSWT) and outputs (almost) every possible quantity.",
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-sf",
        "--spinham-filename",
        type=str,
        metavar="filename",
        default=None,
        required=True,
        help="Path to the spin Hamiltonian file, from where the parameters would be read.",
    )
    parser.add_argument(
        "-ss",
        "--spinham-source",
        type=str,
        metavar="name",
        default=None,
        required=True,
        choices=["GROGU", "TB2J"],
        help='Source of the spin Hamiltonian. Either "GROGU" or "TB2J"',
    )
    parser.add_argument(
        "-sd",
        "--spin-directions",
        nargs="*",
        type=str,
        required=True,
        metavar="S1_x S2_y S3_z ...",
        help="To fully define the system for the calculations of magnons one need the "
        "information about the ground state in addition to the parameters of the "
        "Hamiltonian. There are two ways to give this information to magnopy:\n"
        " * Give a path to the file. In the file there should be M lines with three "
        "numbers in each. The order of the lines would match the order of magnetic "
        "atoms in the spin Hamiltonian."
        " * Give a sequence of 3*M numbers directly to this parameter.",
    )
    parser.add_argument(
        "-s",
        "--spins",
        nargs="*",
        type=str,
        metavar="S1 S2 S3 ...",
        help="In the case when the parameters of spin Hamiltonian comes from TB2J, one "
        "might want to change the values of spins to be closer to half-integers. This "
        "option allows that. Order of the M numbers should match the order of magnetic "
        "atoms in the spin Hamiltonian.",
    )
    parser.add_argument(
        "-kp",
        "--k-path",
        default=None,
        metavar="G-X-S|G-Y",
        type=str,
        help="Path of high symmetry k-points for the plots of dispersion and other "
        "quantities.",
    )
    parser.add_argument(
        "-kps",
        "--kpoints",
        type=str,
        default=None,
        help="Alternatively one could provide an explicit list of k-points for calculation. "
        "In that case provide a path to the file, in which each k-point is given in a "
        "separate line with three numbers per line.",
    )
    parser.add_argument(
        "-r",
        "--relative",
        default=False,
        action="store_true",
        help="When an explicit list of k-points is given, this option specify whether "
        "to consider them as relative or absolute coordinates. Absolute by default.",
    )
    parser.add_argument(
        "-mf",
        "--magnetic-field",
        default=None,
        nargs=3,
        type=float,
        help="Vector of external magnetic field, given in the units of Tesla.",
    )
    parser.add_argument(
        "-of",
        "--output-folder",
        type=str,
        default="magnopy-results",
        help="Folder where all output files of magnopy wil be saved.",
    )
    parser.add_argument(
        "-np",
        "--number-processors",
        type=int,
        default=None,
        help="Number of processes for multithreading. Uses all available processors by "
        "default. Pass 1 to run in serial.",
    )

    return parser
