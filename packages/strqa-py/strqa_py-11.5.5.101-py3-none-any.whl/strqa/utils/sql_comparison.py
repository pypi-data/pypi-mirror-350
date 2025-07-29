import difflib
from itertools import zip_longest

from strqa.utils.helpers import normalize_lines

ADDED = '+'
REMOVED = '-'
UNCHANGED = ' '
EMPTY_LINE = '#'


def _process_diff(
    replace_lines_1: list[str],
    replace_lines_2: list[str],
    start_line1: int,
    start_line2: int,
) -> tuple[list[str], list[str]]:
    """Process replaced lines for side-by-side diff comparison.

    Takes replaced segments from both SQL strings and formats them with
    line numbers and diff symbols for visual comparison.

    Args:
        replace_lines_1 (list[str]): Lines from the first SQL that were replaced
        replace_lines_2 (list[str]): Lines from the second SQL that replace the
            first ones
        start_line1 (int): Starting line number for the first SQL segment
        start_line2 (int): Starting line number for the second SQL segment

    Returns:
        tuple[list[str], list[str]]: A tuple containing:
            - diff_lines_1 (list[str]): Formatted diff lines for the first SQL
            - diff_lines_2 (list[str]): Formatted diff lines for the second SQL
    """
    diff_lines_1, diff_lines_2 = [], []

    # Add empty lines to the shorter list to keep the line numbers in sync
    for i, (old_line, new_line) in enumerate(
        zip_longest(replace_lines_1, replace_lines_2, fillvalue=EMPTY_LINE)
    ):
        diff_lines_1.append(
            # Empty line shouldn't have a prefix and line number
            f'{REMOVED}{start_line1 + i} {old_line}'
            if old_line != EMPTY_LINE
            else EMPTY_LINE
        )
        diff_lines_2.append(
            # Empty line shouldn't have a prefix and line number
            f'{ADDED}{start_line2 + i} {new_line}'
            if new_line != EMPTY_LINE
            else EMPTY_LINE
        )

    return diff_lines_1, diff_lines_2


def _process_error(
    original_lines_1: list[str], original_lines_2: list[str]
) -> tuple[list[str], list[str], bool]:
    """Process error state for side-by-side diff comparison.

    Takes original lines from both SQL strings and formats them with line
    numbers and diff symbols for visual comparison.
    This function is used
    when there was an error extracting SQL from either cube.

    Args:
        original_lines_1 (list[str]): Original lines from the first SQL
        original_lines_2 (list[str]): Original lines from the second SQL

    Returns:
        tuple[bool, bool, str]: A tuple containing:
            - diff_lines_1 (list[str]): Formatted diff lines for the first SQL
            - diff_lines_2 (list[str]): Formatted diff lines for the second SQL
            - is_equal (bool): Always False since there was an error
    """
    diff_lines_1, diff_lines_2 = [], []

    for i, (line1, line2) in enumerate(
        zip_longest(original_lines_1, original_lines_2, fillvalue=EMPTY_LINE)
    ):
        # Format line1 or use EMPTY_LINE if it's a placeholder
        diff_lines_1.append(
            f'{UNCHANGED}{i + 1} {line1}' if line1 != EMPTY_LINE else EMPTY_LINE
        )

        # Format line2 or use EMPTY_LINE if it's a placeholder
        diff_lines_2.append(
            f'{UNCHANGED}{i + 1} {line2}' if line2 != EMPTY_LINE else EMPTY_LINE
        )

    return diff_lines_1, diff_lines_2, False


def compare_sql(
    sql1: str, sql2: str, case_sensitive: bool = True, is_error: bool = False
) -> tuple[list[str], list[str], bool]:
    """Compare two SQL strings and generate formatted diff output.

    Analyzes two SQL statements and generates a line-by-line diff that
    highlights insertions, deletions, replacements, and unchanged lines.
    Each line is prefixed with a symbol indicating its status:
    - '+' for additions
    - '-' for deletions
    - ' ' for unchanged lines
    - '#' for empty lines
    followed by the line number and content.

    Args:
        sql1 (str): First SQL string to compare
        sql2 (str): Second SQL string to compare
        case_sensitive (bool, optional): Whether to perform case-sensitive
            comparison (default: True)
        is_error (bool, optional): Whether there was an error extracting SQL
            from either cube (default: False)

    Returns:
        tuple[list[str], list[str], bool]: A tuple containing:
            - diff_lines_1 (list[str]): Formatted diff lines for the first SQL
            - diff_lines_2 (list[str]): Formatted diff lines for the second SQL
            - is_equal (bool): True if the SQL statements are equivalent,
                False otherwise
    """
    # Always preserve an original case for display
    original_lines_1 = normalize_lines(sql1, case_sensitive=True)
    original_lines_2 = normalize_lines(sql2, case_sensitive=True)

    if is_error:
        return _process_error(original_lines_1, original_lines_2)

    # Use case sensitivity setting for comparison
    lines1 = normalize_lines(sql1, case_sensitive)
    lines2 = normalize_lines(sql2, case_sensitive)

    # Check for equality upfront based on comparison lines
    is_equal = lines1 == lines2

    # If statements are identical, we can create simple output without difflib
    if is_equal:
        diff_lines = [
            f'{UNCHANGED}{i + 1} {line}' for i, line in enumerate(original_lines_1)
        ]
        return diff_lines, diff_lines, is_equal

    diff_lines_1, diff_lines_2 = [], []
    matcher = difflib.SequenceMatcher(None, lines1, lines2)

    # Logic for the different tags can be found here:
    # https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.get_opcodes
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            replace_lines_1, replace_lines_2 = _process_diff(
                original_lines_1[i1:i2], original_lines_2[j1:j2], i1 + 1, j1 + 1
            )
            diff_lines_1.extend(replace_lines_1)
            diff_lines_2.extend(replace_lines_2)
        elif tag == 'delete':
            # Calculate the line number by adding the index (idx) to the
            # starting line number (i1) and then adding 1 to convert from
            # zero-based to one-based indexing.
            diff_lines_1.extend(
                [
                    f'{REMOVED}{i1 + idx + 1} {line}'
                    for idx, line in enumerate(original_lines_1[i1:i2])
                ]
            )
            # Add empty lines to the second list to keep the line numbers
            # in sync.
            diff_lines_2.extend([EMPTY_LINE for _ in range(i2 - i1)])
        elif tag == 'insert':
            # Add empty lines to the first list to keep the line numbers
            # in sync.
            diff_lines_1.extend([EMPTY_LINE for _ in range(j2 - j1)])
            # Calculate the line number by adding the index (idx) to the
            # starting line number (j1) and then adding 1 to convert from
            # zero-based to one-based indexing.
            diff_lines_2.extend(
                [
                    f'{ADDED}{j1 + idx + 1} {line}'
                    for idx, line in enumerate(original_lines_2[j1:j2])
                ]
            )
        elif tag == 'equal':
            # Calculate the line number by adding the index (idx) to the
            # starting line number (i1 or j1) and then adding 1 to convert
            # from zero-based to one-based indexing.
            diff_lines_1.extend(
                [
                    f'{UNCHANGED}{i1 + idx + 1} {line}'
                    for idx, line in enumerate(original_lines_1[i1:i2])
                ]
            )
            diff_lines_2.extend(
                [
                    f'{UNCHANGED}{j1 + idx + 1} {line}'
                    for idx, line in enumerate(original_lines_2[j1:j2])
                ]
            )

    return diff_lines_1, diff_lines_2, is_equal
