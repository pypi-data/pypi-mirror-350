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

_all_ = []

_logger = logging.getLogger(__name__)


class _FailedToVerifyTxtModelFile(Exception):
    R"""
    Raise if the format of the model input file is invalid.
    """

    def __init__(self, message):
        super().__init__(message)


TRUE_KEYWORDS = ["true", "t", "yes", "y", "1"]
FALSE_KEYWORDS = ["false", "f", "no", "n", "0"]


################################################################################
#                              Data type checkers                              #
################################################################################
def _is_float(word) -> bool:
    r"""
    Check if the ``word`` can be converted to ``float``

    Returns
    -------
    bool
        Whether the word can be converted to a float.
    """
    try:
        word = float(word)
        return True
    except ValueError:
        return False


def _is_integer(word) -> bool:
    r"""
    Check if the ``word`` can be converted to ``int``

    Returns
    -------
    bool
        Whether the word can be converted to an integer.
    """

    try:
        word = int(word)
        return True
    except ValueError:
        return False


def _is_bool(word) -> bool:
    r"""
    Check if the ``word`` is one of the supported keywords for boolean values.

    Returns
    -------
    bool
        Whether the word is one of the supported keywords for boolean values.
    """
    return word.lower() in TRUE_KEYWORDS + FALSE_KEYWORDS


################################################################################
#                                Common checker                                #
################################################################################
def _verify_atom_name(word, line_index) -> bool:
    r"""
    Check if the ``word`` is a valid atom's name.

    Parameters
    ----------
    word : str
        The word to check.
    line_index : int
        Original line number, before filtering.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """
    # Atom's name has to start from a number or a letter and should not contain any "#".abs
    # Atom's name should not start nor end with double underscore "__"
    if (
        not (str.isalnum(word[0]) and word.count("#") == 0)
        or word.startswith("__")
        or word.endswith("__")
    ):
        _logger.error(
            " ".join(
                [
                    f"Line {line_index}: Atom names have to start with a",
                    'letter or a number and should not contain any "#" symbols',
                    'and should not start nor end with double underscore "__",',
                    f'got "{word}"',
                ]
            )
        )
        return True
    return False


def _verify_section_header(line, line_index, units_names) -> bool:
    r"""
    Check the section header.

    Parameters
    ----------
    line : str
        The first line of the section.
    line_index : int
        Original line number, before filtering.
    units_names : list of str
        List of the supported units names for the section.
        It is check if the units start with one of the names from the list.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.

    Notes
    -----
    The section name is checked at the other place.
    """
    # There are no errors yet
    errors = False

    # Checker for the atom's coordinate units
    def is_units_keyword(word):
        for entry in units_names:
            if word.lower().startswith(entry):
                return True

        return False

    # Both section name and units are case insensitive
    line = line.lower().split()
    section_name = line[0]

    # If <units> are present, then line has 2 blocks:
    # Section_name <units>
    if len(line) == 2:
        # Check that units are expected
        if len(units_names) == 0:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_index}: expected only the section name",
                        f'and no <units>, got "{" ".join(line)}".',
                    ]
                )
            )
        # If units are expected check that they are one of the supported ones
        elif not is_units_keyword(line[1]):
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_index}, block 2: expected word starting from",
                        ", ".join([f'"{i}"' for i in units_names]),
                        f'got "{line[1]}".',
                    ]
                )
            )
    # If <units> are not present, then the line has only one block:
    # section_name
    elif len(line) != 1:
        # If optional units are expected
        if len(units_names) > 0:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f'Line {line_index}: expected "{section_name}" keyword',
                        f'and/or <units>, got "{" ".join(line)}".',
                    ]
                )
            )
        # If no units are expected
        else:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f'Line {line_index}: expected "{section_name}" keyword',
                        f'and no <units>, got "{" ".join(line)}".',
                    ]
                )
            )

    return errors


def _verify_numerical_data_block(lines, data_specs, line_indices, keyword=None) -> bool:
    r"""
    Verify one data block.

    Data block starts with the keyword (only the first letter is compared) and might be followed
    by any number of lines with numbers. ``data_specs`` is a list of amount of numbers on each line.
    ``data_specs[0]`` - amount of numbers in the same line as the keyword.
    ``data_specs[1:]`` - amount of numbers in the following lines.

    Parameters
    ----------
    lines : list of str
        List of the data block lines from the input file.
        ``len(lines) == len(line_indices) == len(data_specs) > 0``.
    data_specs : list of (int or list of int)
        List of the amount of numbers on each line.
        ``len(data_specs) == len(line_indices) == len(lines) > 0``.
        if ``data_specs[i]`` is a list, then the line has to have one of the amounts of numbers
        from the list.
    line_indices : list of int
        Original line numbers, before filtering.
        ``len(line_indices) == len(data_specs) == len(lines) > 0``.
    keyword : str, optional
        The keyword of the data block. Case insensitive.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """

    # There are no errors yet
    errors = False

    # Check the amount of lines
    if len(lines) != len(data_specs):
        errors = True
        _logger.error(
            " ".join(
                [
                    f"Line {line_indices[0]}: Expected to have {len(data_specs)} lines,"
                    f"got {len(lines)} lines",
                ]
            )
        )

    # Check that every line
    for l_i, line in enumerate(lines):
        line = line.lower().split()

        keyword_error_addition = ""

        # If the keyword is present in the first line
        if l_i == 0 and keyword is not None:
            # Check that the keyword is the expected one
            if keyword.lower()[0] != line[0][0]:
                errors = True
                _logger.error(
                    " ".join(
                        [
                            f"Line {line_indices[l_i]}: expected to have the",
                            f'"{keyword}" keyword (only first letter is checked),'
                            f'got "{line[0][0]}"',
                        ]
                    )
                )
            # Remove the keyword from the line
            line = line[1:]
            # Add the keyword to the error message
            keyword_error_addition = f'"{keyword}" keyword followed by'

        # Check the amount of numbers in the line
        if isinstance(data_specs[l_i], int):
            amount_is_correct = len(line) == data_specs[l_i]
            possible_amounts = str(data_specs[l_i])
        else:
            amount_is_correct = False
            for amount in data_specs[l_i]:
                if len(line) == amount:
                    amount_is_correct = True
                    break
            possible_amounts = " or ".join([str(i) for i in data_specs[l_i]])

        if not amount_is_correct:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_indices[l_i]}: expected to have",
                        keyword_error_addition,
                        f"{possible_amounts} numbers, got {len(line)} numbers",
                    ]
                )
            )
        # Check that every number is convertible to a float
        for n_i, number in enumerate(line):
            if not _is_float(number):
                errors = True
                _logger.error(
                    " ".join(
                        [
                            f"Line {line_indices[l_i]}, block {n_i+1}: expected a number,",
                            f'got "{number}"',
                        ]
                    )
                )

    return errors


def _verify_size_of_section(
    section_name, lines, line_index, expected_lines, exact=True
) -> bool:
    r"""
    Verify the size of the section.

    Parameters
    ----------
    section_name : str
        Name of the section. Is used just for the error message, nothing is checked.
    lines : list of str
        List of the section lines from the input file.
        Without comments and blank lines.
    line_index : int
        Original line number of the first line of the section, before filtering.
    expected_lines : int or list of int
        Expected amount of lines in the section. If list, then the section has to have
        one of the amounts of lines from the list.
    exact : bool, default True
        Whether the section has to have exactly ``expected_lines`` lines.

        * If True, then the section has to have exactly ``expected_lines`` lines.
        * If False, then the section has to have at least ``expected_lines`` lines.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """

    # There are no errors yet
    errors = False

    # Check that the section has an exact amount of lines
    if exact:
        # If only one option is provided
        if isinstance(expected_lines, int):
            amount_is_correct = len(lines) == expected_lines
            possible_amounts = str(expected_lines)
        # If multiple options are provided
        else:
            amount_is_correct = False
            for amount in expected_lines:
                if len(lines) == amount:
                    amount_is_correct = True
                    break
            possible_amounts = " or ".join([str(i) for i in expected_lines])
        # If the amount is not correct
        if not amount_is_correct:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_index}: expected to have {section_name} section with",
                        f"exactly {possible_amounts} lines, got {len(lines)} lines",
                    ]
                )
            )
    # Check that the section has at least the expected amount of lines
    else:
        # Meaningful error message for the programmer
        if not isinstance(expected_lines, int):
            raise RuntimeError(
                "_verify_size_of_section: If exact is False, then expected_lines has to be an integer"
            )
        if len(lines) < expected_lines:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_index}: expected to have {section_name} section with",
                        f"at least {expected_lines} lines, got {len(lines)} lines",
                    ]
                )
            )

    return errors


def _verify_short_separator(line, line_index, symbol) -> bool:
    r"""
    Check if the separator is too short.

    Parameters
    ----------
    line : str
        The line to check.
    line_index : int
        Original line number, before filtering.
    symbol : str
        The symbol of the separator.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """
    # There are no errors yet
    errors = False
    if len(line.strip()) < 10 and len(line.strip()) == line.count(symbol):
        errors = True
        _logger.error(
            " ".join(
                [
                    f"Line {line_index}: Potential separator is too short",
                    f'(expected 10 or more "{symbol}" symbols),',
                    f'got {line.count(symbol)} "{symbol}" symbols.',
                ]
            )
        )
    return errors


################################################################################
#                             Cell section checker                             #
################################################################################
def _verify_cell(lines, line_indices) -> bool:
    r"""
    Check that the found "cell" section is following the input file specification.

    Parameters
    ----------
    lines : list of str
        List of the "cell" section lines from the input file.
        Without comments and blank lines.
        ``len(lines) == len(line_indices)``
    line_indices : list of int
        Original line numbers, before filtering.
        ``len(line_indices) == len(lines)``

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """
    # At the beginning we assume that the first line starts with the
    # case-insensitive word "cell", followed by the next line symbol or a space.

    # There are no errors yet
    errors = False

    # Check size of the cell section it has to have exactly 4 or 5 lines
    if _verify_size_of_section("cell", lines, line_indices[0], [4, 5], exact=True):
        # Do not proceed with the rest of the checks,
        # since the behavior of the rest of the checks is unpredictable
        return True

    # Starting from this line it is assumed that the section has exactly 4 or 5 lines

    # Check the section header
    errors = errors or _verify_section_header(lines[0], line_indices[0], ["a", "b"])

    # If scale factor is present
    if len(lines) == 5:
        scale_errors = _verify_numerical_data_block(
            [lines[1]], [[1, 3]], [line_indices[1]]
        )
        errors = errors or scale_errors
        scale = lines[1].split()
        if not scale_errors and len(scale) == 1 and float(scale[0]) == 0:
            errors = True
            _logger.error("Scale can not be zero")
        if (
            not scale_errors
            and len(scale) == 3
            and (float(scale[0]) <= 0 or float(scale[1]) <= 0 or float(scale[2]) <= 0)
        ):
            errors = True
            _logger.error(
                f'Scale as three numbers - all have to be positive, got "{scale}"'
            )

        cell_lines = lines[2:]
        cell_lines_indices = line_indices[2:]
    # If no scale factor is present
    else:
        cell_lines = lines[1:]
        cell_lines_indices = line_indices[1:]

    # Check that every lattice vector is provided as three numbers separated by spaces.
    errors = errors or _verify_numerical_data_block(
        cell_lines, [3, 3, 3], cell_lines_indices
    )

    return errors


################################################################################
#                            Atoms section checker                             #
################################################################################
def _verify_vector_keyword(keywords, liter, line_index) -> bool:
    r"""
    Check that one of the three sets is provided:

    * s
    * sx sy sz
    * st sp s

    Parameters
    ----------
    keywords : list of str
        List of the keywords.
    liter : int
        liter of the value (i.e. "s", "l" or "j").
    line_index : int
        Original line number, before filtering.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """

    # Sorted keywords
    # <liter>
    # or
    # <liter>x <liter>y <liter>z
    # or
    # <liter> <liter>p <liter>t
    # or nothing
    # or any combination of those variants that keeps unique keywords
    keywords.sort()

    if not (
        keywords == [f"{liter}x", f"{liter}y", f"{liter}z"]
        or keywords == [liter, f"{liter}p", f"{liter}t"]
        or keywords == [liter]
        or keywords == [liter, f"{liter}x", f"{liter}y", f"{liter}z"]
        or keywords
        == [liter, f"{liter}p", f"{liter}t", f"{liter}x", f"{liter}y", f"{liter}z"]
        or not keywords
    ):
        _logger.error(
            " ".join(
                [
                    f"Line {line_index}: expected to have full combination or",
                    "several full combinations of vector keywords or nothing",
                    f'got "{" ".join(keywords)}".',
                    "Check atoms section of documentation for the correct format.",
                ]
            )
        )
        return True

    return False


def _verify_atoms_data_header(line, line_index):
    r"""
    Check the data header of the "atoms" section.

    Parameters
    ----------
    line : str
        The second line of the "atoms" section.
    line_index : int
        Original line number, before filtering.

    Returns
    -------
    N : int
        Number of blocks in the data header.
    name_index : int or None
        Index of the block with the atom's name.
        If None, then the atom's name is not present.
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """

    # There are no errors yet
    errors = False
    name_index = None
    N = len(line.split())

    keywords = line.lower().split()

    # Check that every block of the header is unique:
    if not len(keywords) == len(set(keywords)):
        errors = True
        _logger.error(
            " ".join(
                [
                    f"Line {line_index}: expected unique blocks in the data header,",
                    f'got "{" ".join(keywords)}"',
                ]
            )
        )

    # Check that the required "name" keyword is present in the data header
    if "name" in keywords:
        name_index = keywords.index("name")
        keywords.remove("name")
    else:
        errors = True
        _logger.error(
            " ".join(
                [
                    f"Line {line_index}: expected to have the atom's name",
                    "in the data header, got none",
                ]
            )
        )

    # Remove charge keywords from the list
    if "q" in keywords:
        keywords.remove("q")
    # Remove g-factor keywords from the list
    if "g" in keywords:
        keywords.remove("g")

    position_keywords = []
    spin_keywords = []
    orbital_moment_keywords = []
    total_moment_keywords = []

    # Categorized keywords
    for keyword in keywords:
        if keyword.startswith("r") or keyword in "xyz":
            position_keywords.append(keyword)
        elif keyword.startswith("s"):
            spin_keywords.append(keyword)
        elif keyword.startswith("l"):
            orbital_moment_keywords.append(keyword)
        elif keyword.startswith("j"):
            total_moment_keywords.append(keyword)

    # Sort the lists
    position_keywords.sort()

    # Check position keywords
    if not (
        position_keywords == ["r1", "r2", "r3"]
        or position_keywords == ["x", "y", "z"]
        or position_keywords == ["r1", "r2", "r3", "x", "y", "z"]
    ):
        errors = True
        _logger.error(
            " ".join(
                [
                    f"Line {line_index}: expected to have three or six position keywords.",
                    f'Either "r1 r2 r3" or "x y z" or both, got "{" ".join(position_keywords)}"',
                ]
            )
        )
    # Remove position keywords from the list
    for keyword in position_keywords:
        keywords.remove(keyword)

    # Check spin keywords
    errors = errors or _verify_vector_keyword(spin_keywords, "s", line_index)
    # Remove spin keywords from the list
    for keyword in spin_keywords:
        keywords.remove(keyword)

    # Check orbital moment keywords
    errors = errors or _verify_vector_keyword(orbital_moment_keywords, "l", line_index)

    # Remove orbital moment keywords from the list
    for keyword in orbital_moment_keywords:
        keywords.remove(keyword)

    # Check total moment keywords
    errors = errors or _verify_vector_keyword(total_moment_keywords, "j", line_index)

    # Remove total moment keywords from the list
    for keyword in total_moment_keywords:
        keywords.remove(keyword)

    # Check if there are any unsupported keywords left
    if keywords:
        _logger.warning(
            " ".join(
                [
                    f"Line {line_index}: unsupported keywords in the data header:",
                    f'"{" ".join(keywords)}"',
                ]
            )
        )

    return N, name_index, errors


def _verify_atoms(lines, line_indices):
    r"""
    Check that the found "atoms" section is following the input file specification.

    Parameters
    ----------
    lines : list of str
        List of the "atoms" section lines from the input file.
        Without comments and blank lines.
        ``len(lines) == len(line_indices)``
    line_indices : list of int
        Original line numbers, before filtering.
        ``len(line_indices) == len(lines)``

    Returns
    -------
    allowed_atoms : set of str
        Set of the allowed atom's names.
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """

    allowed_atoms = set()
    # At the beginning we assume that the first line starts with the
    # case-insensitive word "atoms", followed by the next line symbol or a space.

    # There are no errors yet
    errors = False
    # Check size of the atoms section it has to have at least 3 lines: section header,
    # data header and at least one atom
    size_error = _verify_size_of_section(
        "atoms", lines, line_indices[0], 3, exact=False
    )
    if _verify_size_of_section("atoms", lines, line_indices[0], 3, exact=False):
        return set(), True

    # Starting from this line it is assumed that the section has at least 3 lines

    # Check the section header
    errors = errors or _verify_section_header(lines[0], line_indices[0], ["a", "b"])

    # Check the data header
    N, name_index, data_header_errors = _verify_atoms_data_header(
        lines[1], line_indices[1]
    )
    errors = errors or data_header_errors

    # Check each atom line
    for i in range(2, len(lines)):
        line = lines[i].split()

        # Check the amount of blocks
        if len(lines[i].split()) != N:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_indices[i]}: expected to have {N} blocks",
                        f'as per data header, got "{lines[i]}"',
                    ]
                )
            )

        # Check atom's names if any
        if name_index is not None:
            errors = errors or _verify_atom_name(line[name_index], line_indices[i])
            allowed_atoms.add(line[name_index])

        # Check other data fields
        for b_i, block in enumerate(line):
            # Skip the name
            if name_index is not None and b_i == name_index:
                continue

            # All other blocks have to be numbers or "-" symbols (for missing data)
            if not _is_float(block) and block != "-":
                errors = True
                _logger.error(
                    " ".join(
                        [
                            f"Line {line_indices[i]}, block {b_i+1}: expected a number",
                            f'or "-" symbol, got "{block}"',
                        ]
                    )
                )

    if len(allowed_atoms) != len(lines) - 2:
        errors = True
        _logger.error(
            " ".join(
                [
                    f"Line {line_indices[2]}-{line_indices[-1]}: expected to have unique",
                    f"atom's names, got duplicates. {len(allowed_atoms)} unique names found.",
                ]
            )
        )

    return allowed_atoms, errors


################################################################################
#                          Convention section checker                          #
################################################################################
def _verify_notation(
    lines,
    line_indices,
    expect_exchange_factor=True,
    expect_on_site_factor=True,
    expect_double_counting=True,
    expect_spin_normalized=True,
) -> bool:
    r"""
    Check that the found "notation" section is following the input file specification.

    Parameters
    ----------
    lines : list of str
        List of the "notation" section lines from the input file.
        Without comments and blank lines.
        ``len(lines) == len(line_indices)``
    line_indices : list of int
        Original line numbers, before filtering.
        ``len(line_indices) == len(lines)``
    expect_exchange_factor : bool, default: True
        Whether the exchange factor is expected to be present.
    expect_on_site_factor : bool, default: True
        Whether the on-site factor is expected to be present.
    expect_double_counting : bool, default: True
        Whether the double-counting property is expected to be present.
    expect_spin_normalized : bool, default: True
        Whether the spin-normalized property is expected to be present.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """
    # There are no errors yet
    errors = False
    # Check condition about the size of the section the minimum amount of lines is
    # defined by expected keys
    errors = errors or _verify_size_of_section(
        "notation",
        lines,
        line_indices[0],
        int(expect_exchange_factor)
        + int(expect_on_site_factor)
        + int(expect_double_counting)
        + int(expect_spin_normalized)
        + 1,
        exact=False,
    )

    # Check the section header
    errors = errors or _verify_section_header(lines[0], line_indices[0], [])

    # Dictionary of the found properties
    found_properties = {}
    for i in range(1, len(lines)):
        line = lines[i].lower().split()
        if len(line) != 2:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_indices[i]}: expected to have two blocks,",
                        f'separated by spaces, got "{lines[i]}"',
                    ]
                )
            )
        else:
            # Only first letter is checked
            if line[0][0] in found_properties:
                errors = True
                _logger.error(
                    " ".join(
                        [
                            f"Line {line_indices[i]}: found more than one entry of",
                            f'the "{line[0]}" property (only first letter is checked)',
                        ]
                    )
                )
            else:
                found_properties[line[0][0]] = (line[1], i)

    recognized_properties = ["d", "s", "e", "o"]
    expected = {
        "d": expect_double_counting,
        "s": expect_spin_normalized,
        "e": expect_exchange_factor,
        "o": expect_on_site_factor,
    }
    full_names = {
        "d": "double-counting",
        "s": "spin-normalized",
        "e": "exchange-factor",
        "o": "on-site-factor",
    }
    verify_functions = {
        "d": _is_bool,
        "s": _is_bool,
        "e": _is_float,
        "o": _is_float,
    }
    error_expect = {
        "d": "boolean",
        "s": "boolean",
        "e": "number",
        "o": "number",
    }

    # Check that every recognized property is present if it is expected
    # and that it has the correct value
    for prop in recognized_properties:
        # If the property is not found
        if prop not in found_properties:
            # But it is expected
            if expected[prop]:
                errors = True
                _logger.error(
                    f"Line {line_indices[0]}: did not "
                    f'find the "{full_names[prop]}" property in the notation section'
                )
        # If the property is found
        else:
            # Verify it
            if not verify_functions[prop](found_properties[prop][0]):
                errors = True
                _logger.error(
                    " ".join(
                        [
                            f"Line {line_indices[found_properties[prop][1]]}:",
                            f"expected to have a {error_expect[prop]},",
                            f'got "{found_properties[prop][0]}"',
                        ]
                    )
                )
            del found_properties[prop]

    # Issue a warning if there are any unrecognized properties
    if found_properties:
        _logger.warning(
            " ".join(
                [
                    f"Found unrecognized properties in the notation section:",
                    f'{" ".join(found_properties.keys())}',
                ]
            )
        )

    return errors


################################################################################
#                          Exchange section checker                            #
################################################################################
def _verify_bond(lines, line_indices, allowed_atoms) -> bool:
    R"""
    Check that the found "bond" section is following the input file specification.

    Parameters
    ----------
    lines : list of str
        List of the "bond" section lines from the input file.
        Without comments and blank lines.
        ``len(lines) == len(line_indices)``
    line_indices : list of int
        Original line numbers, before filtering.
        ``len(line_indices) == len(lines)``
    allowed_atoms : set of str
        Set of the allowed atom's names.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """
    # At the beginning we assume that the the bond has at least one line in it
    # with the atom's names and ijk.

    # There are no errors yet
    errors = False

    # We need to make sure that only one entry of the type exists.
    found_data = {"matrix": 0, "symmetric": 0, "dmi": 0, "iso": 0}

    line = lines[0].split()
    # Check that the header line
    # A1 A2 i j k
    if len(line) != 5:
        errors = True
        _logger.error(
            " ".join(
                [
                    f"Line {line_indices[0]}: expected two atom names",
                    f'and three integers separated by spaces, got "{" ".join(line)}"',
                ]
            )
        )
    else:
        # Check the atom names
        errors = errors or _verify_atom_name(line[0], line_indices[0])
        errors = errors or _verify_atom_name(line[1], line_indices[0])
        # Check that atom names are present in the atoms section
        for i in [0, 1]:
            if line[i] not in allowed_atoms:
                errors = True
                _logger.error(
                    " ".join(
                        [
                            f"Line {line_indices[0]}, block {i+1}: atom name {line[i]}",
                            "is not present in the atoms section",
                        ]
                    )
                )

        # Check i j k
        if not (_is_integer(line[2]) and _is_integer(line[3]) and _is_integer(line[4])):
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_indices[0]}: expected to have three integers,",
                        f'got "{" ".join(line[2:5])}"',
                    ]
                )
            )

    # Skip first line with atom's names and ijk.
    i = 1
    while i < len(lines):
        line = lines[i].lower().split()
        # If Isotropic keyword found - check isotropic exchange
        # Isotropic Jiso
        if line[0].startswith("i"):
            found_data["iso"] += 1
            # Isotropic line has to have two blocks: keyword and one number
            errors = errors or _verify_numerical_data_block(
                [lines[i]], [[1]], [line_indices[i]], keyword="isotropic"
            )

        # If DMI keyword found - check DMI
        # DMI Dx Dy Dz
        if line[0].startswith("d"):
            found_data["dmi"] += 1
            # DMI line has to have four blocks: keyword and three numbers
            errors = errors or _verify_numerical_data_block(
                [lines[i]], [[3]], [line_indices[i]], keyword="dmi"
            )

        # If symmetric-anisotropy keyword found - check it
        # Symmetric-anisotropy Sxx Syy Sxy Sxz Syz
        if line[0].startswith("s"):
            found_data["symmetric"] += 1
            # Symmetric-anisotropy line has to have six blocks: keyword and five numbers
            errors = errors or _verify_numerical_data_block(
                [lines[i]], [[5]], [line_indices[i]], keyword="symmetric-anisotropy"
            )

        # If Matrix keyword found - check matrix
        # Matrix
        # Jxx Jxy Jxz
        # Jyx Jyy Jyz
        # Jzx Jzy Jzz
        elif line[0].startswith("m"):
            found_data["matrix"] += 1
            errors = errors or _verify_numerical_data_block(
                lines[i : i + 4],
                [0, 3, 3, 3],
                line_indices[i : i + 4],
                keyword="matrix",
            )

        i += 1

    # Check that every type of value was found only once
    total_found_data = 0
    for key in found_data:
        total_found_data += found_data[key]
        if found_data[key] > 1:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f'Line {line_indices[0]}: found more than one "{key}" entry.',
                        f"Check the bond on lines {line_indices[0]}-{line_indices[-1]}",
                    ]
                )
            )

    # Check that at least some values were found
    if total_found_data == 0:
        errors = True
        _logger.error(
            " ".join(
                [
                    f"Line {line_indices[0]}: did not find any information about the parameter value.",
                    f"Check the bond on lines {line_indices[0]}-{line_indices[-1]}",
                ]
            )
        )

    return errors


def _verify_exchange(lines, line_indices, allowed_atoms) -> bool:
    R"""
    Check that the found "exchange" section is following the input file specification.

    Parameters
    ----------
    lines : list of str
        List of the "exchange" section lines from the input file.
        Without comments and blank lines.
        ``len(lines) == len(line_indices)``
    line_indices : list of int
        Original line numbers, before filtering.
        ``len(line_indices) == len(lines)``
    allowed_atoms : set of str
        Set of the allowed atom's names.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """
    # At the beginning we assume that the the exchange section has at least one line in it
    # with the section header

    # There are no errors yet
    errors = False

    # Check the section header
    errors = errors or _verify_section_header(
        lines[0], line_indices[0], ["m", "e", "j", "k", "r"]
    )

    # Find all bonds.
    # Skip first line with the section header
    i = 1
    found_bonds = []
    while i < len(lines):
        # Skip all possible subsection separators or potential short separators
        while i < len(lines):
            short_separator_errors = _verify_short_separator(
                lines[i], line_indices[i], "-"
            )
            errors = errors or short_separator_errors
            if not (lines[i].startswith("-" * 10) or short_separator_errors):
                break
            i += 1

        # Check that some data is present
        if i >= len(lines):
            break

        bond_start = i
        while i < len(lines) and not lines[i].startswith("-" * 10):
            # Check if the separator is present, but too short
            errors = errors or _verify_short_separator(lines[i], line_indices[i], "-")

            i += 1
        bond_end = i

        found_bonds.append((bond_start, bond_end))

    # exchange section has to have at least one bond
    if len(found_bonds) == 0:
        errors = True
        _logger.error('Found 0 bonds in the "exchange" section, expected at least one')

    for bond in found_bonds:
        errors = errors or _verify_bond(
            lines[slice(*bond)], line_indices[slice(*bond)], allowed_atoms=allowed_atoms
        )

    return errors


################################################################################
#                           On-site section checker                            #
################################################################################
def _verify_on_site(lines, line_indices, allowed_atoms) -> bool:
    r"""
    Check that the found "on-site" section is following the input file specification.

    Parameters
    ----------
    lines : list of str
        List of the "on-site" section lines from the input file.
        Without comments and blank lines.
        ``len(lines) == len(line_indices)``
    line_indices : list of int
        Original line numbers, before filtering.
        ``len(line_indices) == len(lines)``
    allowed_atoms : set of str
        Set of the allowed atom's names.

    Returns
    -------
    errors : bool
        ``True`` if errors are found, ``False`` otherwise.
    """
    # At the beginning we assume that the the on-site section has at least one line in it
    # with the section header

    # There are no errors yet
    errors = False

    # Check the section header
    errors = errors or _verify_section_header(
        lines[0], line_indices[0], ["m", "e", "j", "k", "r"]
    )

    # Find all bonds.
    # Skip first line with the section header
    i = 1
    found_parameters = 0
    while i < len(lines):
        # Skip all possible subsection separators or potential short separators
        while i < len(lines):
            short_separator_errors = _verify_short_separator(
                lines[i], line_indices[i], "-"
            )
            errors = errors or short_separator_errors
            if not (lines[i].startswith("-" * 10) or short_separator_errors):
                break
            i += 1

        # Check that some data is present
        if i >= len(lines):
            break

        # Check that the atom's name is present
        if len(lines[i].split()) != 1:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_indices[i]}: expected only the atom's name,",
                        f'got "{lines[i]}"',
                    ]
                )
            )
        # Check the atom's name
        errors = errors or _verify_atom_name(lines[i].split()[0], line_indices[i])
        # Check that atom names are present in the atoms section
        if lines[i].split()[0] not in allowed_atoms:
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_indices[i]}: atom name {lines[i].split()[0]}",
                        "is not present in the atoms section",
                    ]
                )
            )

        # go to the next line
        i += 1
        # Check that the next line is present
        if i >= len(lines):
            errors = True
            _logger.error(
                " ".join(
                    [
                        f"Line {line_indices[i-1]}: Expected to have six numbers,",
                        "separated with spaces at the next line, got nothing",
                    ]
                )
            )
            break

        # Check that the next line contain six numbers
        errors = errors or _verify_numerical_data_block(
            [lines[i]], [6], [line_indices[i]]
        )

        # Go to the next line after verifying the matrix elements
        i += 1
        found_parameters += 1

    # on-site section has to have at least one bond
    if found_parameters == 0:
        errors = True
        _logger.error(
            'Found 0 parameters in the "on-site" section, expected at least one'
        )

    return errors


################################################################################
#                   Rules (check additional ones at the end)                   #
################################################################################

_REQUIRED_SECTIONS = ["cell", "atoms", "notation"]

_SUPPORTED_SECTIONS = {"cell", "atoms", "notation", "exchange", "on-site"}
################################################################################
#                      Mapping of verification functions                       #
################################################################################

_VERIFY = {
    "cell": _verify_cell,
    "atoms": _verify_atoms,
    "notation": _verify_notation,
    "exchange": _verify_exchange,
    "on-site": _verify_on_site,
}


################################################################################
#                              Full file checker                               #
################################################################################
def verify_model_file(lines, line_indices, raise_on_fail=True, return_sections=False):
    r"""
    Verify the content of the input file with the model.

    The input file shall be filtered. See :py:func:`._filter_txt_file`.

    Parameters
    -------------
    lines : list of str
        List of the lines from the input file. Without comments and blank lines.
    line_indices : list of int
        Original line numbers, before filtering.
    raise_on_fail : bool, default True
        Whether to raise an Error if the file content is incorrect.
    return_sections : bool, default False
        Whether to return a dictionary with the positions of the found sections::

            {"keyword" : (start, end)}

        ``lines[start]`` is a first line of the section,
        ``lines[end-1]`` is the last line of the section.
    """

    # There are no errors yet
    errors = False

    # Tracker the found sections
    found_sections = {}

    # Start fir the first line
    i = 0
    while i < len(lines):
        # Skip all possible separators or potential short separators
        while i < len(lines):
            short_separator_errors = _verify_short_separator(
                lines[i], line_indices[i], "="
            )
            errors = errors or short_separator_errors
            if not (lines[i].startswith("=" * 10) or short_separator_errors):
                break
            i += 1

        # Check that there are some data present
        if i >= len(lines):
            break

        section_keyword = lines[i].split()[0].lower()
        section_start = i
        # Iterate until the next section separator is found
        # or the end of the file is reached
        while i < len(lines) and not lines[i].startswith("=" * 10):
            # Check if the separator is present, but too short
            errors = errors or _verify_short_separator(lines[i], line_indices[i], "=")

            i += 1
        section_end = i

        _logger.info(
            f'Found section "{section_keyword}" on lines '
            + f"{line_indices[section_start]}-{line_indices[section_end-1]}"
        )

        # Save the position of the found section
        found_sections[section_keyword] = (section_start, section_end)

    # Check if all required sections are found
    for r_section in _REQUIRED_SECTIONS:
        if r_section not in found_sections:
            errors = True
            _logger.error(f'File: failed to find required section "{r_section}"')

    # Verify atoms section in advance, since we need to know a set of allowed atoms.
    if "atoms" in found_sections:
        allowed_atoms, atoms_errors = _verify_atoms(
            lines[slice(*found_sections["atoms"])],
            line_indices[slice(*found_sections["atoms"])],
        )
        errors = errors or atoms_errors
    else:
        allowed_atoms = set()

    # Set up keywords for the custom verification calls
    kwargs = {}
    # Generic keywords
    for section in _SUPPORTED_SECTIONS:
        kwargs[section] = {}

    # Custom keywords for notation section
    kwargs["notation"]["expect_exchange_factor"] = "exchange" in found_sections
    kwargs["notation"]["expect_on_site_factor"] = "on-site" in found_sections
    kwargs["notation"]["expect_double_counting"] = "exchange" in found_sections
    kwargs["notation"]["expect_spin_normalized"] = (
        "exchange" in found_sections or "on-site" in found_sections
    )

    # Custom keywords for exchange section
    kwargs["exchange"]["allowed_atoms"] = allowed_atoms

    # Custom keywords for on-site section
    kwargs["on-site"]["allowed_atoms"] = allowed_atoms

    # Verify other found sections
    for section in found_sections:
        # Skip atoms section, because it was verified before
        if section == "atoms":
            continue
        # Only verify sections that are supported
        if section in _SUPPORTED_SECTIONS:
            # Check if the verification function is implemented
            if section in _VERIFY:
                errors = errors or _VERIFY[section](
                    lines[slice(*found_sections[section])],
                    line_indices[slice(*found_sections[section])],
                    **kwargs[section],
                )
            # If verification function is not implemented
            else:
                _logger.warning(
                    f"Verification function for the section '{section}' is not implemented."
                )
        # If the section is not supported
        else:
            _logger.warning(f"Section '{section}' is not supported.")

    # Finalize the check and raise an error if needed
    if not errors:
        _logger.info("Model file verification finished: PASSED")
    else:
        if raise_on_fail:
            _logger.info("Model file verification finished: FAILED")
            import sys

            sys.tracebacklimit = 0
            raise FailedToVerifyTxtModelFile("Check log files for the details")
        else:
            _logger.info("Model file verification finished: FAILED")

    if return_sections:
        return found_sections
