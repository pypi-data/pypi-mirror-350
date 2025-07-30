"""
Module with the initial set of tests for the cookieslicer project.
"""

import os
from test.cookieslicer_proxy import CookieslicerProxy
from test.patches.patch_builtin_open import PatchBuiltinOpen
from test.patches.patch_os_path_isfile import PatchOsPathIsfile
from test.pytest_directories import TestDirectories
from test.pytest_helpers import TestHelpers

from cookieslicer.cookieslicer_constants import CookieslicerConstants

__BAD_TEMPLATE_DIRECTORY_NAME = "empty-file.txt"
__PIPFILE = "Pipfile"


def test_with_parameters_source_directory_not_exists() -> None:
    """
    Make sure that we expect the template source directory to exist.
    """

    project_name = "wilma"
    with TestDirectories(__BAD_TEMPLATE_DIRECTORY_NAME) as test_dirs:
        assert test_dirs.output_directory is not None
        assert test_dirs.input_directory is not None

        # Arrange
        assert not os.path.isdir(test_dirs.source_directory)
        assert os.path.isdir(test_dirs.output_directory)
        assert os.path.isdir(test_dirs.input_directory)

        slicer_proxy = CookieslicerProxy()
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_input_directory=True
        )

        expected_return_code = 2
        expected_output = ""
        expected_error = """usage: cookieslicer [-f] [-g] [-l] [-i INPUT_DIRECTORY] -s SOURCE_DIRECTORY
                    -p PROJECT_NAME [-o OUTPUT_DIRECTORY] [--stack-trace] [-h]
cookieslicer: error: argument -s/--source-directory: Specified source directory '{directory}' does not exist.""".replace(
            "{directory}", test_dirs.source_directory
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_parameters_source_directory_not_contain_source_config() -> None:
    """
    Make sure that we expect the template source directory to exist and contain a 'cookiecutter.json' file.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories() as test_dirs:
        assert test_dirs.output_directory is not None
        assert test_dirs.input_directory is not None

        assert os.path.isdir(test_dirs.source_directory)
        assert not os.path.isfile(
            os.path.join(
                test_dirs.source_directory,
                CookieslicerConstants.get_cutter_source_configuration_file(),
            )
        )
        assert os.path.isdir(test_dirs.output_directory)
        assert os.path.isdir(test_dirs.input_directory)

        slicer_proxy = CookieslicerProxy()
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_input_directory=True
        )

        expected_return_code = 2
        expected_output = ""
        expected_error = """usage: cookieslicer [-f] [-g] [-l] [-i INPUT_DIRECTORY] -s SOURCE_DIRECTORY
                    -p PROJECT_NAME [-o OUTPUT_DIRECTORY] [--stack-trace] [-h]
cookieslicer: error: argument -s/--source-directory: Specified source directory '{directory}' does not contain the required '{config}' file.""".replace(
            "{directory}", test_dirs.source_directory
        ).replace(
            "{config}", CookieslicerConstants.get_cutter_source_configuration_file()
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_parameters_input_directory_not_exists() -> None:
    """
    Make sure that if an input directory is specified, it exists.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories(
        "template_one",
        input_directory=TestDirectories.join_test_path(__BAD_TEMPLATE_DIRECTORY_NAME),
    ) as test_dirs:
        assert test_dirs.output_directory is not None
        assert test_dirs.input_directory is not None

        assert os.path.isdir(test_dirs.source_directory)
        assert os.path.isfile(
            os.path.join(
                test_dirs.source_directory,
                CookieslicerConstants.get_cutter_source_configuration_file(),
            )
        )
        assert not os.path.isdir(test_dirs.input_directory)
        assert os.path.isdir(test_dirs.output_directory)

        slicer_proxy = CookieslicerProxy()
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_input_directory=True
        )

        expected_return_code = 2
        expected_output = ""
        expected_error = """usage: cookieslicer [-f] [-g] [-l] [-i INPUT_DIRECTORY] -s SOURCE_DIRECTORY
                    -p PROJECT_NAME [-o OUTPUT_DIRECTORY] [--stack-trace] [-h]
cookieslicer: error: argument -i/--input-directory: Specified input directory '{directory}' does not exist.""".replace(
            "{directory}", test_dirs.input_directory
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_parameters_output_directory_not_exists() -> None:
    """
    Make sure that if an output directory is specified, that it exists.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories(
        "template_one",
        output_directory=TestDirectories.join_test_path(__BAD_TEMPLATE_DIRECTORY_NAME),
    ) as test_dirs:
        assert test_dirs.output_directory is not None
        assert test_dirs.input_directory is not None

        assert os.path.isdir(test_dirs.source_directory)
        assert os.path.isfile(
            os.path.join(
                test_dirs.source_directory,
                CookieslicerConstants.get_cutter_source_configuration_file(),
            )
        )
        assert os.path.isdir(test_dirs.input_directory)
        assert not os.path.isdir(test_dirs.output_directory)

        slicer_proxy = CookieslicerProxy()
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_input_directory=True
        )

        expected_return_code = 2
        expected_output = ""
        expected_error = """usage: cookieslicer [-f] [-g] [-l] [-i INPUT_DIRECTORY] -s SOURCE_DIRECTORY
                    -p PROJECT_NAME [-o OUTPUT_DIRECTORY] [--stack-trace] [-h]
cookieslicer: error: argument -o/--output-directory: Specified output directory '{directory}' does not exist.""".replace(
            "{directory}", test_dirs.output_directory
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_parameters_output_directory_config_is_directory() -> None:
    """
    Make sure that if we have a valid output directory, it does not contain a config directory instead of a file.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories(
        "template_one",
        output_directory=TestDirectories.join_test_path("bad_template_one"),
    ) as test_dirs:
        assert test_dirs.output_directory is not None
        assert test_dirs.input_directory is not None

        config_path = os.path.join(
            test_dirs.output_directory,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )

        assert os.path.isdir(test_dirs.source_directory)
        assert os.path.isfile(
            os.path.join(
                test_dirs.source_directory,
                CookieslicerConstants.get_cutter_source_configuration_file(),
            )
        )
        assert os.path.isdir(test_dirs.input_directory)
        assert os.path.isdir(test_dirs.output_directory)
        assert os.path.isdir(
            os.path.join(
                test_dirs.output_directory,
                CookieslicerConstants.get_cutter_output_settings_file(),
            )
        )

        slicer_proxy = CookieslicerProxy()
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_input_directory=True
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = """

Settings configuration file '{config}' cannot be a directory.""".replace(
            "{config}", config_path
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_parameters_output_directory_config_not_exists() -> None:
    """
    Make sure that we report not having a settings configuration.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories("template_one") as test_dirs:
        assert test_dirs.output_directory is not None

        config_path = os.path.join(
            test_dirs.output_directory,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )

        assert os.path.isdir(test_dirs.source_directory)
        assert os.path.isfile(
            os.path.join(
                test_dirs.source_directory,
                CookieslicerConstants.get_cutter_source_configuration_file(),
            )
        )
        assert os.path.isdir(test_dirs.output_directory)
        assert not os.path.exists(config_path)

        slicer_proxy = CookieslicerProxy()
        supplied_arguments = test_dirs.initialize_argument_list(project_name)

        expected_return_code = 1
        expected_output = ""
        expected_error = """

Settings configuration file '{config}' was not found within the output directory.

To generate a default settings configuration file, execute the command line again with the -g/--generate option.""".replace(
            "{config}", config_path
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_source_without_template_directory() -> None:
    """
    Make sure that a source directory without a nested template directory is called out.
    """

    with TestDirectories("bad_template_one") as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(project_name)

        expected_return_code = 1
        expected_output = ""
        expected_error = "Source directory '{directory}' does not contain a '{{cookiecutter.project_name}}' subdirectory.".replace(
            "{directory}", test_dirs.source_directory
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_source_with_template_directory_without_slicer_config_file() -> None:
    """
    Make sure that a source directory without a nested template directory containing a slicer file is reported.
    """
    with TestDirectories("bad_template_two") as test_dirs:
        assert test_dirs.output_directory is not None

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        template_path = os.path.join(
            test_dirs.source_directory,
            CookieslicerConstants.get_cutter_source_template_directory(),
        )
        supplied_arguments = test_dirs.initialize_argument_list(project_name)

        expected_return_code = 1
        expected_output = ""
        expected_error = f"Source template directory '{template_path}' does not contain a '{CookieslicerConstants.get_slicer_input_configuration_file()}' file."

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_bad_cookiecutter_configuration() -> None:
    """
    Test using the bad_template_three template which has a bad cookie cutter file.
    """
    with TestDirectories("bad_template_three", delete_when_done=True) as test_dirs:
        assert test_dirs.output_directory is not None
        cutter_config = os.path.join(test_dirs.source_directory, "cookiecutter.json")

        # Arrange
        slicer_proxy = CookieslicerProxy()
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_input_directory=True
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = f"General error with cookiecutter: JSON decoding error while loading '{cutter_config}'. Decoding error details: 'Expecting value: line 1 column 1 (char 0)'"

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


def test_with_simple_application_no_modifications_source_config_with_unhandled_exception() -> (
    None
):
    """
    Make sure that a simple application with a patch that causes an unhandled exception to occur.

    This patch is set up to trigger when the __ensure_cookieslicer_source_config_present function
    checks to see if the input_file_name is a file using os.path.isfile.

    Since this is a function that should "ALWAYS" return, capturing an unhandled exception is
    correct.
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

        source_slicer_config_file = os.path.join(
            test_dirs.source_directory,
            CookieslicerConstants.get_cutter_source_template_directory(),
            CookieslicerConstants.get_slicer_input_configuration_file(),
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = "Unhandled exception 'Exception' caused program to terminate.\nFor more information, run the application again with the '--stack-trace' option."

        # Act
        try:
            patch = PatchOsPathIsfile()
            patch.register_exception_for_file(
                source_slicer_config_file, Exception("blah")
            )
            patch.start()

            execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)
        finally:
            patch.stop(True)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_simple_application_no_modifications_source_config_with_with_file_exception() -> (
    None
):
    """
    Make sure that a simple application with a patch that causes an unhandled exception to occur.

    This patch is set up to trigger when the __ensure_cookieslicer_source_config_present function
    checks to see if the input_file_name is a file using os.path.isfile.
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

        source_slicer_config_file = os.path.join(
            test_dirs.source_directory,
            CookieslicerConstants.get_cutter_source_template_directory(),
            CookieslicerConstants.get_slicer_input_configuration_file(),
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = "Cookieslicer template file '{file}' was not loaded.".replace(
            "{file}", source_slicer_config_file
        )

        # Act
        try:
            patch = PatchBuiltinOpen()
            patch.register_exception_for_file(
                source_slicer_config_file, "rt", Exception("blah")
            )
            patch.start()

            execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)
        finally:
            patch.stop(print_action_comments=True)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_simple_application_no_modifications_ouput_config_with_unhandled_exception() -> (
    None
):
    """
    Make sure that a simple application with a patch that causes an unhandled exception to occur
    with the output configuration.
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

        output_slicer_config_file = os.path.join(
            test_dirs.output_directory,
            CookieslicerConstants.get_slicer_output_configuration_file(),
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = "Cookieslicer output file '{file}' was not loaded.".replace(
            "{file}", output_slicer_config_file
        )

        # Act
        try:
            patch = PatchOsPathIsfile()
            patch.register_exception_for_file(
                output_slicer_config_file, Exception("blah")
            )
            patch.start()

            execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)
        finally:
            patch.stop()

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_simple_application_no_modifications_pipfile() -> None:
    """
    Make sure that a simple application with a patch that causes an unhandled exception to occur
    when updating the pipfile.
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

        output_pipfile = os.path.join(
            test_dirs.output_directory,
            __PIPFILE,
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = """Error 'Exception' occurred applying template: blah
Revert output directory to previous well-known state before continuing."""

        # Act
        try:
            patch = PatchOsPathIsfile()
            patch.register_exception_for_file(output_pipfile, Exception("blah"))
            patch.start()

            execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)
        finally:
            patch.stop()

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
