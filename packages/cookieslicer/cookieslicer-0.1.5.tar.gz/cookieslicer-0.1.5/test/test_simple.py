"""
Module with the simple set of tests for the cookieslicer project.
"""

import os
import shutil
import tempfile
from test.cookieslicer_proxy import CookieslicerProxy
from test.pytest_directories import TestDirectories
from test.pytest_helpers import TestHelpers

from cookieslicer.cookieslicer_constants import CookieslicerConstants

__EXTRA_TEXT_TO_APPEND_TO_FILES = "New Line\n\n"


def test_with_simple_application_no_modifications_x() -> None:
    """
    Make sure that a simple application of the project on the "default" test template works properly.
    """
    with TestDirectories("template_one", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            template_properties,
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
        TestHelpers.assert_output_slicer_updated(
            test_dirs.source_directory, test_dirs.output_directory
        )
        TestHelpers.assert_file_is_new(before_snapshot, after_snapshot, "README.md")
        TestHelpers.assert_file_was_templated_properly(
            test_dirs, "README.md", template_properties
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_simple_application_no_modifications_as_module() -> None:
    """
    Make sure that a simple application of the project on the "default" test template works properly.
    """
    with TestDirectories("template_one", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy(use_module=True, use_main=True)
        (
            project_name,
            template_properties,
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
        TestHelpers.assert_output_slicer_updated(
            test_dirs.source_directory, test_dirs.output_directory
        )
        TestHelpers.assert_file_is_new(before_snapshot, after_snapshot, "README.md")
        TestHelpers.assert_file_was_templated_properly(
            test_dirs, "README.md", template_properties
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_simple_application_extra_path_separator() -> None:
    """
    Make sure that a simple application of the project on the "default" test template works properly
    when invoked with a trailing path separator for any directories.
    """
    with TestDirectories(
        "template_one", delete_when_done=True, add_trailing_path_separator=True
    ) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            template_properties,
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
        TestHelpers.assert_output_slicer_updated(
            test_dirs.source_directory, test_dirs.output_directory
        )
        TestHelpers.assert_file_is_new(before_snapshot, after_snapshot, "README.md")
        TestHelpers.assert_file_was_templated_properly(
            test_dirs, "README.md", template_properties
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_simple_application_twice() -> None:
    """
    Make sure that repeating the simple action results in the proper notification.
    """
    with TestDirectories("template_one", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)
        slicer_proxy.invoke_main(arguments=supplied_arguments)
        TestHelpers.append_to_output_file(
            test_dirs, "README.md", __EXTRA_TEXT_TO_APPEND_TO_FILES
        )

        expected_return_code = 0
        expected_output = """Cookie slicer destination version '1' is equal to the template version.
No templating required."""
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


def test_with_simple_application_twice_with_force_normal() -> None:
    """
    Make sure that repeating the simple action with the addition of the force flag forces
    the templating to occur.
    """
    with TestDirectories("template_one", delete_when_done=True) as test_dirs:
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
        TestHelpers.assert_file_was_not_changed(
            before_snapshot,
            after_snapshot,
            CookieslicerConstants.get_slicer_output_configuration_file(),
        )
        TestHelpers.assert_file_was_changed(
            before_snapshot, after_snapshot, "README.md"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_simple_application_no_modifications_with_existing_directory_blocking_file() -> (
    None
):
    """
    Make sure that a simple application of the project with a file to be copied blocked
    by an existing directory works as intended.
    """
    with TestDirectories("template_one", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)

        create_path = os.path.join(test_dirs.output_directory, "README.md")
        os.makedirs(create_path, exist_ok=True)

        expected_return_code = 1
        expected_output = ""
        expected_error = """Output directory '{path}' conflicts with creating a file named '{path}'.

Updating output directory with template was interupted part way.

After diagnosing the reported issue, a backup of the output directory should be used to revert the directory to a known good state before trying to address the diagnosed issue.""".replace(
            "{path}", create_path
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_simple_application_with_updated_template_version() -> None:
    """
    Make sure that we can apply a template, bump the config_version is the template, and apply
    it again without any issues. At the end of this test, the cookieslicer config in the output
    must be the bumped config_version.

    Note that this relies on the testing done in test_with_simple_application_no_modifications_x
    for the first half of the function.
    """
    with TestDirectories("template_one", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None
        with tempfile.TemporaryDirectory() as source_directory_copy:
            # Arrange - Invoke the application for the first time.
            slicer_proxy = CookieslicerProxy()
            (
                project_name,
                _,
            ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
            supplied_arguments = test_dirs.initialize_argument_list(project_name)
            execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

            expected_return_code = 0
            expected_output = """attention_files = []
number_copied = 1
number_skipped = 0
number_skipped_once = 0
number_system = 1
num_removed = 0"""
            expected_error = ""

            # Arrange - Act and Assert for first invocation
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )
            TestHelpers.assert_output_slicer_updated(
                test_dirs.source_directory, test_dirs.output_directory
            )

            # Arrange for the second invoke - Create a copy of the source directory and bump
            # the configuration in that source directory up by 1.
            shutil.copytree(
                test_dirs.source_directory, source_directory_copy, dirs_exist_ok=True
            )
            TestHelpers.bump_configuration_file_version(source_directory_copy)
            supplied_arguments = test_dirs.initialize_argument_list(
                project_name, substitute_source_directory=source_directory_copy
            )

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
            TestHelpers.assert_file_was_changed(
                before_snapshot,
                after_snapshot,
                CookieslicerConstants.get_slicer_output_configuration_file(),
            )
            TestHelpers.assert_output_slicer_updated(
                source_directory_copy, test_dirs.output_directory
            )
            TestHelpers.assert_file_was_not_changed(
                before_snapshot, after_snapshot, "README.md"
            )
            TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)
