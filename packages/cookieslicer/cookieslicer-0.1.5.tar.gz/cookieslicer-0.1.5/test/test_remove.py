"""
Module with the remove file set of tests for the cookieslicer project.
"""

from test.cookieslicer_proxy import CookieslicerProxy
from test.pytest_directories import TestDirectories
from test.pytest_helpers import TestHelpers

from cookieslicer.cookieslicer_constants import CookieslicerConstants


def test_with_remove_file_applied_with_non_existing_file() -> None:
    """
    Test using the template_remove template which removes the README.md file with a destination
    directory not populated with that file.
    """
    with TestDirectories("template_remove", delete_when_done=True) as test_dirs:
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
number_copied = 1
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
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_remove_file_applied_with_existing_file() -> None:
    """
    Test using the template_remove template which removes the README.md file with a destination
    directory populated with that file.
    """
    with TestDirectories("template_remove", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)
        TestHelpers.write_to_output_file(test_dirs, "other.md", "default")

        expected_return_code = 0
        expected_output = """attention_files = []
number_copied = 1
number_skipped = 0
number_skipped_once = 0
number_system = 1
num_removed = 1"""
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
        TestHelpers.assert_file_was_removed(before_snapshot, after_snapshot, "other.md")
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_remove_file_applied_with_existing_template_file() -> None:
    """
    Test using the template_remove_two template which removes the README.md file where that
    file also appears in the template.
    """
    with TestDirectories("template_remove_two", delete_when_done=True) as test_dirs:
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
number_copied = 0
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
        TestHelpers.assert_file_is_new(
            before_snapshot,
            after_snapshot,
            CookieslicerConstants.get_slicer_output_configuration_file(),
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_remove_file_applied_with_existing_template_file_list_only() -> None:
    """
    Test using test_with_remove_file_applied_with_existing_template_file but only
    listing the changes that would be made, not actually making them.
    """
    with TestDirectories("template_remove_two", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_list=True
        )

        expected_return_code = 0
        expected_output = """File 'cookieslicer.json' is a system file.  Skipping file.
File 'README.md' marked for removal.  Skipping file.
File 'README.md' was marked for removal but does not exist.  Skipping file.
attention_files = []
number_copied = 0
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
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)
