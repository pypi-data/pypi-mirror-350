"""
Module with the pipfile file set of tests for the cookieslicer project.
"""

from test.cookieslicer_proxy import CookieslicerProxy
from test.pytest_directories import TestDirectories
from test.pytest_helpers import TestHelpers

from cookieslicer.cookieslicer_constants import CookieslicerConstants

__EXTRA_TEXT_TO_APPEND_TO_FILES = "New Line\n\n"


def test_with_simple_application_twice_with_force_and_unchanged_pipfile() -> None:
    """
    A repeat of the `test_with_simple_application_twice_with_force` test scenario, but with
    a template that includes a Pipfile that we do not modify.
    """
    with TestDirectories("template_two", delete_when_done=True) as test_dirs:
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

        expected_return_code = 0
        expected_output = """attention_files = []
number_copied = 0
number_skipped = 2
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
        TestHelpers.assert_file_was_not_changed(
            before_snapshot,
            after_snapshot,
            CookieslicerConstants.get_slicer_output_configuration_file(),
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "README.md"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "Pipfile"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_simple_application_twice_with_force_and_changed_pipfile() -> None:
    """
    A repeat of the `test_with_simple_application_twice_with_force` test scenario, but with
    a template that includes a Pipfile that we will modify to look different for the
    second "force" call.
    """
    with TestDirectories("template_two", delete_when_done=True) as test_dirs:
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
            test_dirs, "Pipfile", __EXTRA_TEXT_TO_APPEND_TO_FILES
        )

        expected_return_code = 8
        expected_output = """attention_files = []
number_copied = 1
number_skipped = 1
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
        TestHelpers.assert_file_was_not_changed(
            before_snapshot,
            after_snapshot,
            CookieslicerConstants.get_slicer_output_configuration_file(),
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "README.md"
        )
        TestHelpers.assert_file_was_changed(before_snapshot, after_snapshot, "Pipfile")
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)
