"""
Module with the attention set of tests for the cookieslicer project.
"""

import os
import sys
from test.cookieslicer_proxy import CookieslicerProxy
from test.pytest_directories import TestDirectories
from test.pytest_helpers import TestHelpers

from cookieslicer.cookieslicer_constants import CookieslicerConstants

__EXTRA_TEXT_TO_APPEND_TO_FILES = "New Line\n\n"


def test_with_attention_file_applied_once() -> None:
    """
    Test using the template_attention template which include a file marked as needing attention.
    """
    with TestDirectories("template_attention", delete_when_done=True) as test_dirs:
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


def test_with_attention_file_applied_twice_without_modification() -> None:
    """
    Test using the template_attention template which includes a file marked as needing attention, and
    try applying the template a second time without modifying that file.
    """
    with TestDirectories("template_attention", delete_when_done=True) as test_dirs:
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
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_attention_file_applied_twice_with_modification() -> None:
    """
    Test using the template_attention template which includes a file marked as needing attention, and
    try applying the template a second time after modifying that file.
    """
    with TestDirectories("template_attention", delete_when_done=True) as test_dirs:
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
            test_dirs, "README.md", __EXTRA_TEXT_TO_APPEND_TO_FILES
        )
        readme_path = os.path.join(test_dirs.output_directory, "README.md")
        if sys.platform.startswith("win"):
            readme_path = readme_path.replace("\\", "\\\\")

        expected_return_code = 0
        expected_output = """attention_files = ['{readme}']
number_copied = 1
number_skipped = 0
number_skipped_once = 0
number_system = 1
num_removed = 0""".replace(
            "{readme}", readme_path
        )
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
        TestHelpers.assert_file_was_changed(
            before_snapshot, after_snapshot, "README.md"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)
