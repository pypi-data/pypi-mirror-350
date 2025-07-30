"""
Module with the more complex set of tests for the cookieslicer project.
"""

import os
from test.cookieslicer_proxy import CookieslicerProxy
from test.pytest_directories import TestDirectories
from test.pytest_helpers import TestHelpers

from cookieslicer.cookieslicer_constants import CookieslicerConstants

__COPY_ERROR_SUFFIX = (
    "\n\n"
    + "Updating output directory with template was interupted part way.\n\nAfter diagnosing the reported issue, a backup of the output directory should be used to revert the directory to a known good state before trying to address the diagnosed issue."
)


def test_with_more_complex_structure_once() -> None:
    """
    Test using the template_three template which combines a number of things together.
    """
    with TestDirectories("template_three", delete_when_done=True) as test_dirs:
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
            before_snapshot, after_snapshot, "something\\inner_file.txt"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_more_complex_structure_once_with_input_directory() -> None:
    """
    Test using the template_three template which combines a number of things together,
    but also add the specification of the input directory.
    """
    with TestDirectories("template_three", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_input_directory=True
        )

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
            before_snapshot, after_snapshot, "something\\inner_file.txt"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_more_complex_structure_once_existing_file_prevents_directory() -> None:
    """
    Test using the template_three template with a file "something" that is already in the
    place of where the template says the "something" directory should go.
    """
    with TestDirectories("template_three", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)
        file_path = TestHelpers.write_to_output_file(test_dirs, "something", "blah")
        create_path = os.path.join(file_path, "inner_file.txt")

        expected_return_code = 1
        expected_output = ""
        expected_error = f"Output directory file '{file_path}' conflicts with creating a directory named '{file_path}' to hold file '{create_path}'.{__COPY_ERROR_SUFFIX}"

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_even_more_complex_structure_with_templated_directories() -> None:
    """
    Test using the template_nine template to make sure that the cookiecutter templated
    directory is used to determine the configuration file, not before.
    """
    with TestDirectories("template_nine", delete_when_done=True) as test_dirs:
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
number_copied = 7
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
            before_snapshot, after_snapshot, "my_properties\\text.attention"
        )
        TestHelpers.assert_file_is_new(
            before_snapshot, after_snapshot, "my_properties\\text.normal"
        )
        TestHelpers.assert_file_is_new(
            before_snapshot, after_snapshot, "my_properties\\text.once"
        )
        TestHelpers.assert_file_is_new(
            before_snapshot, after_snapshot, "my_properties\\my_properties.attention"
        )
        TestHelpers.assert_file_is_new(
            before_snapshot, after_snapshot, "my_properties\\my_properties.normal"
        )
        TestHelpers.assert_file_is_new(
            before_snapshot, after_snapshot, "my_properties\\my_properties.once"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_even_more_complex_structure_with_templated_directories_list_only() -> (
    None
):
    """
    Test following the test_with_even_more_complex_structure_with_templated_directories
    but with only listing enabled.
    """
    with TestDirectories("template_nine", delete_when_done=True) as test_dirs:
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
File 'README.md' copied.
File 'my_properties/my_properties.attention' copied.
File 'my_properties/my_properties.attention' marked as needing special attention.
File 'my_properties/my_properties.normal' copied.
File 'my_properties/my_properties.once' copied.
File 'my_properties/text.attention' copied.
File 'my_properties/text.attention' marked as needing special attention.
File 'my_properties/text.normal' copied.
File 'my_properties/text.once' copied.
File 'text.remove' was marked for removal but does not exist.  Skipping file.
File 'my_properties/text.remove' was marked for removal but does not exist.  Skipping file.
File 'my_properties/my_properties.remove' was marked for removal but does not exist.  Skipping file.
attention_files = []
number_copied = 7
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

        # Because the application was invoked in list only mode, no file changes
        # should be made to the output directory. The only thing that should be
        # there is the cookiecutter-config.yaml file that we expect to be there
        # already.
        TestHelpers.assert_file_was_not_changed(
            before_snapshot,
            after_snapshot,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_even_more_complex_structure_with_templated_directories_again() -> None:
    """
    Test using the template_nine template to make sure that the cookiecutter templated
    directory is used to determine the configuration file, not before.  This is applying
    the same template again with a force and with changed files, which should cause the
    once file and the attention file handling to kick in.
    """
    with TestDirectories("template_nine", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)
        slicer_proxy.invoke_main(arguments=supplied_arguments)

        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_force=True
        )

        # Arrange - Append text to these files to make the different and allow
        #           copying to occur if needed.
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\text.attention", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\text.normal", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\text.once", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\my_properties.attention", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\my_properties.normal", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\my_properties.once", "\nbob\n"
        )

        attention_file1_path = os.path.join(
            test_dirs.output_directory, "my_properties", "my_properties.attention"
        ).replace("\\", "\\\\")
        attention_file2_path = os.path.join(
            test_dirs.output_directory, "my_properties", "text.attention"
        ).replace("\\", "\\\\")

        expected_return_code = 0
        expected_output = """attention_files = ['{file_1}', '{file_2}']
number_copied = 4
number_skipped = 1
number_skipped_once = 2
number_system = 1
num_removed = 0""".replace(
            "{file_1}", attention_file1_path
        ).replace(
            "{file_2}", attention_file2_path
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
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "README.md"
        )
        TestHelpers.assert_file_was_changed(
            before_snapshot, after_snapshot, "my_properties\\text.attention"
        )
        TestHelpers.assert_file_was_changed(
            before_snapshot, after_snapshot, "my_properties\\text.normal"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.once"
        )
        TestHelpers.assert_file_was_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.attention"
        )
        TestHelpers.assert_file_was_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.normal"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.once"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_even_more_complex_structure_with_templated_directories_again_list_only() -> (
    None
):
    """
    Test following the test_with_even_more_complex_structure_with_templated_directories_again
    but with only listing enabled.
    """
    with TestDirectories("template_nine", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)
        slicer_proxy.invoke_main(arguments=supplied_arguments)

        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_force=True, include_list=True
        )

        # Arrange - Append text to these files to make the different and allow
        #           copying to occur if needed.
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\text.attention", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\text.normal", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\text.once", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\my_properties.attention", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\my_properties.normal", "\nbob\n"
        )
        TestHelpers.append_to_output_file(
            test_dirs, "my_properties\\my_properties.once", "\nbob\n"
        )

        attention_file1_path = os.path.join(
            test_dirs.output_directory, "my_properties", "my_properties.attention"
        ).replace("\\", "\\\\")
        attention_file2_path = os.path.join(
            test_dirs.output_directory, "my_properties", "text.attention"
        ).replace("\\", "\\\\")

        expected_return_code = 0
        expected_output = """File 'cookieslicer.json' is a system file.  Skipping file.
File 'README.md' and destination file are equal.  Skipping file.
File 'my_properties/my_properties.attention' copied.
File 'my_properties/my_properties.attention' marked as needing special attention.
File 'my_properties/my_properties.normal' copied.
File 'my_properties/my_properties.once' is marked as copy-once and already exists at destination.  Skipping file.
File 'my_properties/text.attention' copied.
File 'my_properties/text.attention' marked as needing special attention.
File 'my_properties/text.normal' copied.
File 'my_properties/text.once' is marked as copy-once and already exists at destination.  Skipping file.
File 'text.remove' was marked for removal but does not exist.  Skipping file.
File 'my_properties/text.remove' was marked for removal but does not exist.  Skipping file.
File 'my_properties/my_properties.remove' was marked for removal but does not exist.  Skipping file.
attention_files = ['{file_1}', '{file_2}']
number_copied = 4
number_skipped = 1
number_skipped_once = 2
number_system = 1
num_removed = 0""".replace(
            "{file_1}", attention_file1_path
        ).replace(
            "{file_2}", attention_file2_path
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
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "README.md"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.attention"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.normal"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.once"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.attention"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.normal"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.once"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_even_more_complex_structure_with_templated_directories_redux() -> None:
    """
    Test using the template_nine template to make sure that the cookiecutter templated
    directory is used to determine the configuration file, not before.  This time, when
    applying the template for a second time, we do not change any of the templated output
    files, but introduce the files that were marked for removal.
    """
    with TestDirectories("template_nine", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)
        slicer_proxy.invoke_main(arguments=supplied_arguments)

        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_force=True
        )

        # Arrange - Create files marked for removal.
        TestHelpers.write_to_output_file(test_dirs, "text.remove", "\nbob\n")
        TestHelpers.write_to_output_file(
            test_dirs, "my_properties\\text.remove", "\nbob\n"
        )
        TestHelpers.write_to_output_file(
            test_dirs, "my_properties\\my_properties.remove", "\nbob\n"
        )

        expected_return_code = 0
        expected_output = """attention_files = []
number_copied = 0
number_skipped = 5
number_skipped_once = 2
number_system = 1
num_removed = 3"""
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
        TestHelpers.assert_file_was_removed(
            before_snapshot, after_snapshot, "text.remove"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.attention"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.normal"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.once"
        )
        TestHelpers.assert_file_was_removed(
            before_snapshot, after_snapshot, "my_properties\\text.remove"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.attention"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.normal"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.once"
        )
        TestHelpers.assert_file_was_removed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.remove"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)


def test_with_even_more_complex_structure_with_templated_directories_redux_list_only() -> (
    None
):
    """
    Test following the test_with_even_more_complex_structure_with_templated_directories_redux
    but with only listing enabled.
    """
    with TestDirectories("template_nine", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)
        slicer_proxy.invoke_main(arguments=supplied_arguments)

        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_force=True, include_list=True
        )

        # Arrange - Create files marked for removal.
        TestHelpers.write_to_output_file(test_dirs, "text.remove", "\nbob\n")
        TestHelpers.write_to_output_file(
            test_dirs, "my_properties\\text.remove", "\nbob\n"
        )
        TestHelpers.write_to_output_file(
            test_dirs, "my_properties\\my_properties.remove", "\nbob\n"
        )

        expected_return_code = 0
        expected_output = """File 'cookieslicer.json' is a system file.  Skipping file.
File 'README.md' and destination file are equal.  Skipping file.
File 'my_properties/my_properties.attention' and destination file are equal.  Skipping file.
File 'my_properties/my_properties.normal' and destination file are equal.  Skipping file.
File 'my_properties/my_properties.once' is marked as copy-once and already exists at destination.  Skipping file.
File 'my_properties/text.attention' and destination file are equal.  Skipping file.
File 'my_properties/text.normal' and destination file are equal.  Skipping file.
File 'my_properties/text.once' is marked as copy-once and already exists at destination.  Skipping file.
File 'text.remove' was marked for removal.  Removing file.
File 'my_properties/text.remove' was marked for removal.  Removing file.
File 'my_properties/my_properties.remove' was marked for removal.  Removing file.
attention_files = []
number_copied = 0
number_skipped = 5
number_skipped_once = 2
number_system = 1
num_removed = 3"""
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
        TestHelpers.assert_file_was_removed(
            before_snapshot, after_snapshot, "text.remove"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.attention"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.normal"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\text.once"
        )
        TestHelpers.assert_file_was_removed(
            before_snapshot, after_snapshot, "my_properties\\text.remove"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.attention"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.normal"
        )
        TestHelpers.assert_file_was_not_changed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.once"
        )
        TestHelpers.assert_file_was_removed(
            before_snapshot, after_snapshot, "my_properties\\my_properties.remove"
        )
        TestHelpers.assert_all_files_accounted_for(before_snapshot, after_snapshot)
