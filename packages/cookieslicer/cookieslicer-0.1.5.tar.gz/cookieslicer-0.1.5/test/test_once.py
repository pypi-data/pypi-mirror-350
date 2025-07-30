"""
Module with the once set of tests for the cookieslicer project.
"""

from test.cookieslicer_proxy import CookieslicerProxy
from test.pytest_directories import TestDirectories
from test.pytest_helpers import TestHelpers

from cookieslicer.cookieslicer_constants import CookieslicerConstants

__EXTRA_TEXT_TO_APPEND_TO_FILES = "New Line\n\n"
__TEMPLATE_ONCE__ONCE_FILE_NAME = "once.txt"


def test_with_once_file_applied_once() -> None:
    """
    Test using the template_once template which include a file to be copied once.
    """
    with TestDirectories("template_once", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)

        expected_return_code = 0
        expected_output = """attention_files = []
number_copied = 2
number_skipped = 0
number_skipped_once = 0
number_system = 1
num_removed = 0"""
        expected_error = ""

        # Act
        before_snapshot = TestHelpers.capture_output_directory_snapshot(test_dirs)
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)
        after_snapshot = TestHelpers.capture_output_directory_snapshot(test_dirs)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )

        TestHelpers.assert_file_was_not_changed(
            before_snapshot,
            after_snapshot,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )
        TestHelpers.assert_file_is_new(
            before_snapshot,
            after_snapshot,
            CookieslicerConstants.get_slicer_output_configuration_file(),
        )
        TestHelpers.assert_file_is_new(before_snapshot, after_snapshot, "README.md")
        TestHelpers.assert_file_is_new(
            before_snapshot, after_snapshot, __TEMPLATE_ONCE__ONCE_FILE_NAME
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_once_file_applied_twice() -> None:
    """
    Test using the template_once template which include a file to be copied once, and
    try applying the template a second time.
    """
    with TestDirectories("template_once", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_force=True
        )
        slicer_proxy.invoke_main(arguments=supplied_arguments)
        TestHelpers.append_to_output_file(
            test_dirs, __TEMPLATE_ONCE__ONCE_FILE_NAME, __EXTRA_TEXT_TO_APPEND_TO_FILES
        )

        expected_return_code = 0
        expected_output = """attention_files = []
number_copied = 0
number_skipped = 1
number_skipped_once = 1
number_system = 1
num_removed = 0"""
        expected_error = ""

        # Act
        before_snapshot = TestHelpers.capture_output_directory_snapshot(test_dirs)
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)
        after_snapshot = TestHelpers.capture_output_directory_snapshot(test_dirs)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )

        TestHelpers.assert_file_was_not_changed(
            before_snapshot,
            after_snapshot,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot,
            after_snapshot,
            CookieslicerConstants.get_slicer_output_configuration_file(),
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "README.md"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, __TEMPLATE_ONCE__ONCE_FILE_NAME
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)
