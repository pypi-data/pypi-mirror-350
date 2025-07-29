import os
from datetime import datetime
from typing import TYPE_CHECKING

from mstrio.helpers import IServerError

from strqa.utils.html_creation import generate_sql_diff_html
from strqa.utils.sql_comparison import compare_sql
from strqa.utils.types import SupportedCubes

if TYPE_CHECKING:
    from strqa import Config


class CubeTester:
    """
    Class for comparing cubes.
    This class is responsible for comparing the properties of two cubes
        and generating a visual HTML diff report.
    Attributes:
        source_cube (SupportedCubes): The source cube to compare.
        target_cube (SupportedCubes | None): The target cube to compare.
        root_folder (str): The root folder where the results will be stored.
        config (Config): Configuration object for the comparison.
        cube_config (Config.CubeConfig): Configuration settings for cube
            comparison.
        results (list[dict]): List of results from the comparison tests.
    """

    def __init__(
        self,
        source_cube: SupportedCubes,
        target_cube: SupportedCubes | None,
        root_folder: str,
        config: 'Config',
    ) -> None:
        self.source_cube = source_cube
        self.target_cube = target_cube
        self.root_folder = root_folder
        self.config = config
        self.cube_config = config.cube_config
        self.results: list[dict] = []

    def run_all_tests(self) -> list[dict]:
        """Run all tests on the source and target cubes."""
        if self.cube_config.sql:
            is_equal, is_error, output_file = self.compare_cubes_sql()
            self.results.append(
                {
                    'test_name': 'sql_check',
                    'is_equal': is_equal,
                    'is_error': is_error,
                    'output_file': output_file,
                }
            )

        return self.results

    def compare_cubes_sql(self) -> tuple[bool, bool, str]:
        """Compare SQL statements of two cubes and generate a visual HTML
        diff report.

        Returns:
            tuple[bool, bool, str]: A tuple containing:
                - is_equal (bool): True if the SQL statements are equivalent,
                    False otherwise
                - is_error (bool): True if there was an error extracting SQL
                    from either cube
                - output_file (str): Path to the generated HTML diff report
        """
        source_cube_sql, target_cube_sql = '', ''
        is_error = False
        try:
            source_cube_sql = self.source_cube.export_sql_view()
        except IServerError:
            is_error = True

        if self.target_cube:
            try:
                target_cube_sql = self.target_cube.export_sql_view()
            except IServerError:
                is_error = True

        diff_lines_1, diff_lines_2, is_equal = compare_sql(
            sql1=source_cube_sql,
            sql2=target_cube_sql,
            case_sensitive=self.cube_config.sql_case_sensitive,
            is_error=is_error,
        )

        # SQL cannot be considered equal if there was an error
        if is_error:
            is_equal = False

        # Skip HTML generation if not needed
        if not self.config.create_matching_sql_file and is_equal:
            return is_equal, is_error, ''

        # Include milliseconds in the timestamp to prevent filename conflicts
        current_date = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        output_file_comp = os.path.join(
            self.root_folder,
            f'sql_diff_{self.source_cube.id}_{current_date}.html',
        )

        generate_sql_diff_html(
            diff_lines_1,
            diff_lines_2,
            is_equal,
            output_file_comp,
            self.source_cube.name,
            self.target_cube.name if self.target_cube else None,
        )

        return is_equal, is_error, output_file_comp
