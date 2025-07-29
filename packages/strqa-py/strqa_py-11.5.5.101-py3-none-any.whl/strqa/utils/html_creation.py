import html
import typing as t
from functools import cache
from itertools import zip_longest
from pathlib import Path

from strqa.utils.types import SupportedCubes

TEMPLATES_FOLDER = Path(__file__).parent / 'templates'
CSS_CLASSES = {'+': 'diff_add', '-': 'diff_sub', '?': 'diff_chg'}


class Template:
    """Class to handle HTML templates for SQL diff generation.

    This class reads a template file and provides methods to fill it with
    data. It uses Python's string formatting to replace placeholders in the
    template with actual values."""

    _content: str

    def __init__(self, template: str | Path):
        self._content = Template._get_file_data(template)

    def get_raw(self) -> str:
        """Get the raw content of the template.

        _For templates without any values to fill in dynamically._"""
        return self._content

    def fill_with(self, **kwargs: str | int) -> str:
        """Fill the template with provided keyword arguments.

        Each key in `kwargs` should match a placeholder in the template.
        The placeholders should be in the format `{key}`.
        The method replaces the placeholders with the corresponding values
        from `kwargs`."""
        return self._content.format(**kwargs)

    def fill_many_with(self, *args: dict[str, str | int]) -> str:
        """Create multiple entries from this template
        and concatenate them into one string.

        Each `arg` should be a valid `kwargs` for `self.fill_with(...)`.
        """
        return ''.join(self.fill_with(**kwargs) for kwargs in args)

    @staticmethod
    def join(items: list[str] | tuple[str, ...]) -> str:
        """Join a list of template strings into a single string.

        Args:
            items (list[str] | tuple[str, ...]): List or tuple of
                template strings to join.

        Returns:
            str: Joined string.
        """
        return ''.join(items)

    @staticmethod
    @cache
    def _get_file_data(path: str | Path) -> str:
        """Read the content of a file and return it as a string.

        Caches the output based on a path to avoid re-reading the file
            multiple times.

        Args:
            path (str | Path): The path to the file.

        Returns:
            str: The content of the file.
        """
        with open(path, encoding='utf-8') as file:
            return file.read()


def generate_sql_diff_html(
    diff_lines_1: list[str],
    diff_lines_2: list[str],
    is_match: bool,
    output_file: str,
    object_1_name: str | None = None,
    object_2_name: str | None = None,
) -> None:
    """Generate an HTML file with side-by-side diff comparison of SQL statements

    Creates an HTML page that displays the differences between two SQL
    statements in a side-by-side format with line numbers and color coding
    for additions, deletions.

    Args:
        diff_lines_1 (list[str]): List of formatted diff lines for the first
            SQL statement
        diff_lines_2 (list[str]): List of formatted diff lines for the second
            SQL statement
        is_match (bool): Indicates whether the two SQL statements match
        output_file (str): Path to the output HTML file
        object_1_name (str, optional): Name of the first object being compared.
        object_2_name (str, optional): Name of the second object being compared.

    Returns:
        None. The HTML content is written to the specified output file.
    """
    _css_styles = Template(TEMPLATES_FOLDER / 'templates-styling.css').get_raw()

    def format_line(line: str, idx: int) -> dict[str, str]:
        if not line or line == '#':
            return {
                f'line_number{idx}': '',
                f'change_type{idx}': '',
                f'content{idx}': '',
            }

        prefix, content = line[:1], line[1:]
        class_name = CSS_CLASSES.get(prefix, '')
        line_number, text = content.split(' ', 1) if ' ' in content else ('', content)

        # Prevent XSS attacks by escaping HTML characters
        escaped_text = html.escape(text)

        return {
            f'line_number{idx}': line_number,
            f'change_type{idx}': class_name,
            f'content{idx}': escaped_text,
        }

    def format_lines(lines1: list[str], lines2: list[str]) -> str:
        return Template(
            TEMPLATES_FOLDER / 'comparison-row.html.template'
        ).fill_many_with(
            *(
                format_line(line1, 1) | format_line(line2, 2)
                for line1, line2 in zip_longest(lines1, lines2, fillvalue='')
            )
        )

    # Prevent XSS attacks by escaping HTML characters
    escaped_object_1_name = html.escape(object_1_name or 'Object 1')
    escaped_object_2_name = html.escape(object_2_name or 'Object 2')

    rows = format_lines(diff_lines_1, diff_lines_2)
    html_content = Template(TEMPLATES_FOLDER / 'comparison.html.template').fill_with(
        _css_styles=_css_styles,
        # template requires no spaces in below param
        result='MATCHED' if is_match else 'NOT-MATCHED',
        rows=rows,
        object1_name=escaped_object_1_name,
        object2_name=escaped_object_2_name,
    )

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)


def generate_tests_summary_html(
    test_results: dict[str, int],
    final_data: list[dict[str, t.Any]],
    output_file: str,
) -> None:
    """Generate an HTML file with side-by-side info about compared objects
    and the test results.

    Args:
        test_results (dict[str, int]): Dictionary containing the test results
            summary with keys 'total', 'failed' and 'successful'.
        final_data (list[dict[str, Any]]): List of dictionaries containing
            information about the compared objects. Each dictionary should
            contain the keys 'source_obj', 'target_obj' and 'obj_test_results'.
        output_file (str): Path to the output HTML file.
    """
    _css_styles = Template(TEMPLATES_FOLDER / 'templates-styling.css').get_raw()

    def format_table(
        item1: SupportedCubes,
        item2: SupportedCubes | None,
        sql_url: str,
        is_sql_matched: bool,
    ) -> str:
        """Generate an HTML table for the comparison of two objects.

        Args:
            item1 (SupportedCubes): The first object to compare.
            item2 (SupportedCubes | None): The second object to compare.
            sql_url (str): URL for the SQL comparison file.
            is_sql_matched (bool): Indicates whether the two objects SQL match.

        Returns:
            str: HTML string representing the comparison table.
        """

        def safe_attr(
            obj: SupportedCubes | None,
            attr: str,
            escape: bool = False,
            default: str = 'N/A',
        ) -> str:
            """Safely access an attribute of an object and escape it for HTML.

            Args:
                obj (SupportedCubes | None): The object to access.
                attr (str): The attribute name to access.
                escape (bool): Whether to escape the attribute value for HTML.
                default (str): Default value to return if the attribute is not
                    found.

            Returns:
                str: The escaped attribute value or the default value.
            """
            if obj is None:
                return default
            value = getattr(obj, attr, None)
            if value is None:
                return default
            return html.escape(str(value)) if escape else str(value)

        # Define attributes to display in the table
        attributes = [
            {'param': 'ObjectID', 'attr': 'id', 'escape': False},
            {'param': 'Name', 'attr': 'name', 'escape': True},
            {'param': 'Type', 'attr': 'type', 'escape': False},
            {'param': 'SubType', 'attr': 'subtype', 'escape': False},
            {'param': 'ExtendedType', 'attr': 'ext_type', 'escape': False},
            {'param': 'Path', 'attr': 'path', 'escape': True},
        ]

        # Extract item names for reuse
        item1_name = safe_attr(item1, 'name', escape=True)
        item2_name = safe_attr(item2, 'name', escape=True)

        # Generate data rows consistently
        data_rows = [
            {
                'parameter': attr['param'],
                'value1': safe_attr(item1, attr['attr'], attr['escape']),
                'value2': safe_attr(item2, attr['attr'], attr['escape']),
            }
            for attr in attributes
        ]

        rows = Template(
            TEMPLATES_FOLDER / 'tests-summary-table-row.html.template'
        ).fill_many_with(*data_rows)

        sql_url_template = ''
        if sql_url:
            sql_url_template = Template(
                TEMPLATES_FOLDER / 'tests-summary-table-sql-row.html.template'
            ).fill_with(sql_url=sql_url)

        return Template(
            TEMPLATES_FOLDER / 'tests-summary-table.html.template'
        ).fill_with(
            # template requires no spaces in below param
            result='MATCHED' if is_sql_matched else 'NOT-MATCHED',
            object1_name=item1_name,
            object2_name=item2_name,
            rows=rows,
            sql_url=sql_url_template,
        )

    tests_summary_tables = [
        format_table(
            item1=entry['source_obj'],
            item2=entry['target_obj'],
            # TODO: currently `entry['obj_test_results']` has
            # only one element in it, but it will change in the future
            # and this approach will require rework
            sql_url=entry['obj_test_results'][0]['output_file'],
            is_sql_matched=entry['obj_test_results'][0]['is_equal'],
        )
        for entry in final_data
    ]

    html_content = Template(TEMPLATES_FOLDER / 'tests-summary.html.template').fill_with(
        _css_styles=_css_styles,
        exec_count=test_results['total'],
        success_count=test_results['successful'],
        failed_count=test_results['failed'],
        tests_summary_tables=Template.join(tests_summary_tables),
    )

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
