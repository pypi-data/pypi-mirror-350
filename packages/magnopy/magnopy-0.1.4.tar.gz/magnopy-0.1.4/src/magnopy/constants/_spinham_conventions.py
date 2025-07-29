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


R"""Pre-defined conventions of spin Hamiltonian"""

# (multiple_counting, spin_normalized, c21, c22, c31, c32, c33, c41, c421, c422, c43, c44)
_CONVENTIONS = {
    "tb2j": (True, True, -1, -1, None, None, None, None, None, None, None, None),
    "spinw": (True, False, 1, 1, None, None, None, None, None, None, None, None),
    "vampire": (True, True, -1, -0.5, None, None, None, None, None, None, None, None),
}
