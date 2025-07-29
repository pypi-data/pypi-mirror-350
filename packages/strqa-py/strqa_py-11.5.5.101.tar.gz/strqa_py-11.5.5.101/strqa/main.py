import logging
import os
from dataclasses import dataclass, field
from datetime import datetime

from mstrio.connection import Connection
from mstrio.project_objects import OlapCube, SuperCube

from strqa.objects_tester.cube_tester import CubeTester
from strqa.utils.baseline_creation import create_json_baseline_file
from strqa.utils.html_creation import generate_tests_summary_html
from strqa.utils.object_mapper import map_objects
from strqa.utils.types import SupportedTypes

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """General settings for the StrQA class.

    Attributes:
        cube_config (CubeConfig): Configuration for cube comparison.
        map_objects_by_id (bool): Whether to map objects by ID.
        map_objects_by_location (bool): Whether to map objects by location.
        map_objects_manually (bool): Whether to manually map objects.
        create_matching_sql_file (bool): Whether to create a matching SQL file.
    """

    @dataclass
    class CubeConfig:
        """Settings for the cube testing.

        Attributes:
            sql (bool): Whether to include SQL in the comparison.
            sql_case_sensitive (bool): Whether the SQL comparison should be
                case-sensitive.
        """

        sql: bool = True
        sql_case_sensitive: bool = True

    cube_config: CubeConfig = field(default_factory=CubeConfig)
    map_objects_by_id: bool = True
    map_objects_by_location: bool = True
    map_objects_manually: bool = False
    create_matching_sql_file: bool = False


class StrQA:
    """Main class for comparing objects.

    Attributes:
        objects (list[SupportedTypes] |
            list[tuple[SupportedTypes, SupportedTypes]]): List of objects
            to compare.
            If manually mapping, provide a list of tuples (source, target).
        config (Config): Configuration object for the comparison.
        path (str): Path to store the results.
    """

    def __init__(
        self,
        objects: list[SupportedTypes] | list[tuple[SupportedTypes, SupportedTypes]],
        config: Config,
        path: str,
    ) -> None:
        """Initialize the StrQA class.

        Args:
            objects (list[SupportedTypes] |
                list[tuple[SupportedTypes, SupportedTypes]]
            ): List of objects to compare. If manually mapping, provide a list
                of tuples (source, target).
            config (Config): Configuration object for the comparison.
            path (str): Root folder path where the results will be stored.
        """
        if not objects:
            raise ValueError("Objects list cannot be empty.")

        self.objects = objects
        self.config = config
        self.path = path
        self._mapped_objects: list[tuple[SupportedTypes, SupportedTypes | None]] = []
        self._root_folder: str | None = None
        self._results: list[dict] = []

    def _create_root_folder(self) -> None:
        """Check if the user-provided path is correct and create a root folder
        with the current datetime as its name.
        """

        # Convert to an absolute path before any operations
        absolute_path = os.path.abspath(self.path)

        # Check if the provided path exists
        if not os.path.exists(absolute_path):
            raise FileNotFoundError(
                f"The specified path does not exist: {absolute_path}"
            )

        # Check if the provided path is a directory
        if not os.path.isdir(absolute_path):
            raise NotADirectoryError(
                f"The specified path is not a directory: {absolute_path}"
            )

        # Create folder with current datetime as name (format: YYYYMMDD_HHMMSS)
        folder_name = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_path = os.path.join(absolute_path, folder_name)

        # Create the folder
        os.makedirs(folder_path)

        # Store the created folder path for further use
        self._root_folder = folder_path

    def _get_object_tester(
        self,
        source_obj: SupportedTypes,
        target_obj: SupportedTypes | None,
    ) -> CubeTester:
        """Return the appropriate tester class based on an object type.

        This method maps different Strategy object types to their
        corresponding tester classes.
        Currently, supports OlapCube and SuperCube.

        Args:
            source_obj (SupportedTypes): Source object to test
            target_obj (SupportedTypes | None):
                Target object to compare against (or None)

        Returns:
            Appropriate tester instance for the object type

        Raises:
            ValueError: If the object type is not supported
        """
        # Later more object types will be added
        if isinstance(source_obj, (OlapCube, SuperCube)):
            return CubeTester(
                source_obj,
                target_obj,
                self._root_folder,
                self.config,
            )

        raise ValueError(f"Unsupported object type: {type(source_obj).__name__}")

    def create_baseline(self) -> None:
        """Create a baseline file."""

        self._create_root_folder()

        filepath = os.path.join(self._root_folder, 'baseline_source.json')
        create_json_baseline_file(self.objects, self.config, filepath)

    def _create_baseline_files(self):
        """Create JSON baseline files for the source object and, if applicable,
        the target object."""
        source_objs = [source for source, _ in self._mapped_objects]
        target_objs = [
            target for _, target in self._mapped_objects if target is not None
        ]

        baseline_path = os.path.join(self._root_folder, 'baseline_{}.json')

        create_json_baseline_file(
            source_objs, self.config, baseline_path.format('source')
        )

        # Only create target baseline if we have targets
        if target_objs:
            create_json_baseline_file(
                target_objs, self.config, baseline_path.format('target')
            )

    def project_vs_project(self, target_connection: Connection) -> bool:
        """Compare objects between two projects.

        Args:
            target_connection (Connection): Connection to the target Strategy
                environment.

        Returns:
            bool: True if all tests passed, False otherwise
        """

        # Create the root folder for results
        self._create_root_folder()

        # Map objects to compare
        if not self.config.map_objects_manually:
            self._mapped_objects = map_objects(
                self.objects, target_connection, self.config
            )
        else:
            # Ensure objects are in the expected format when manually mapped
            if any(not isinstance(item, tuple) for item in self.objects):
                msg = (
                    "With map_objects_manually=True, all objects must be "
                    "(source, target) tuples"
                )
                raise ValueError(msg)

            self._mapped_objects = self.objects

        # Create JSON baseline files for source and target objects
        self._create_baseline_files()

        # Run tests for each pair of mapped objects
        for source_obj, target_obj in self._mapped_objects:
            tester = self._get_object_tester(source_obj, target_obj)
            obj_test_results = tester.run_all_tests()

            self._results.append(
                {
                    'source_obj': source_obj,
                    'target_obj': target_obj,
                    'obj_test_results': obj_test_results,
                }
            )

        # Calculate tests statistics
        total_tests = sum(len(result['obj_test_results']) for result in self._results)
        successful_tests = sum(
            test['is_equal']
            for result in self._results
            for test in result['obj_test_results']
        )
        failed_tests = total_tests - successful_tests

        logger.info(
            f"Total Executions: {total_tests},\n"
            f"Matched tests: {successful_tests},\n"
            f"Not-Matched tests: {failed_tests}"
        )

        output_file_summary = os.path.join(self._root_folder, 'tests_summary.html')

        generate_tests_summary_html(
            {
                'total': total_tests,
                'successful': successful_tests,
                'failed': failed_tests,
            },
            self._results,
            output_file_summary,
        )

        if failed_tests != 0:
            logger.error(
                f"{failed_tests} test(s) failed. "
                f"Please check the results for more details: {output_file_summary}"
            )
            return False

        logger.info("All tests passed successfully!")
        return True
