"""
Module with the generate config set of tests for the cookieslicer project.
"""

import os
from test.cookieslicer_proxy import CookieslicerProxy
from test.pytest_directories import TestDirectories
from test.pytest_execute import InProcessResult
from test.pytest_helpers import TestHelpers

from cookieslicer.cookieslicer_constants import CookieslicerConstants


def test_with_parameters_output_directory_config_not_exists_and_generate() -> None:
    """
    Make sure that the application can generate a default configuration file to
    be used by the application as a starting point.
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
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_generate=True
        )

        expected_return_code = 9
        expected_output = ""
        expected_error = ""
        expected_config_contents = """default_context:
  other_name: default_other_name
  project_name: default_name"""

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert os.path.exists(config_path)
        act = TestHelpers.read_from_output_file(test_dirs, config_path)
        InProcessResult.compare_versus_expected(
            "configuration file", act, expected_config_contents
        )


def test_with_parameters_output_directory_config_not_exists_and_generate_include_with_copy_without_render() -> (
    None
):
    """
    Make sure that the application ignores a _copy_without_render key in the configuration.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories("template_four") as test_dirs:
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
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_generate=True
        )

        expected_return_code = 9
        expected_output = ""
        expected_error = ""
        expected_config_contents = """default_context:
  other_name: default_other_name
  project_name: default_name"""

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert os.path.exists(config_path)
        act = TestHelpers.read_from_output_file(test_dirs, config_path)
        InProcessResult.compare_versus_expected(
            "configuration file", act, expected_config_contents
        )


def test_with_parameters_output_directory_config_not_exists_and_generate_include_with_extensions_declaration() -> (
    None
):
    """
    Make sure that the application fails if any `_extensions` key is provided
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories("template_five") as test_dirs:
        assert test_dirs.output_directory is not None

        config_path = os.path.join(
            test_dirs.output_directory,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )
        original_configuration_path = os.path.join(
            test_dirs.source_directory,
            CookieslicerConstants.get_cutter_source_configuration_file(),
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
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_generate=True
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = f"Cookie cutter configuration file '{original_configuration_path}' contains an '_extensions' key that is not supported by cookieslicer."

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_parameters_output_directory_config_not_exists_and_generate_include_with_extensions_use_a() -> (
    None
):
    """
    Make sure that the application fails if the {% sequence is present in any part
    of the input configuration file used to generate the cutter configuration YAML file.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories("template_six_a") as test_dirs:
        assert test_dirs.output_directory is not None

        config_path = os.path.join(
            test_dirs.output_directory,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )
        original_configuration_path = os.path.join(
            test_dirs.source_directory,
            CookieslicerConstants.get_cutter_source_configuration_file(),
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
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_generate=True
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = (
            f"Cookie cutter configuration file '{original_configuration_path}' contains "
            + "template extension '{%' or '{{' sequences."
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_parameters_output_directory_config_not_exists_and_generate_include_with_extensions_use_b() -> (
    None
):
    """
    Make sure that the application fails if the {{ sequence is present in any part
    of the input configuration file used to generate the cutter configuration YAML file.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories("template_six_b") as test_dirs:
        assert test_dirs.output_directory is not None

        config_path = os.path.join(
            test_dirs.output_directory,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )
        original_configuration_path = os.path.join(
            test_dirs.source_directory,
            CookieslicerConstants.get_cutter_source_configuration_file(),
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
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_generate=True
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = (
            f"Cookie cutter configuration file '{original_configuration_path}' contains "
            + "template extension '{%' or '{{' sequences."
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_parameters_output_directory_config_not_exists_and_generate_include_with_choices() -> (
    None
):
    """
    Make sure that the application reacts properly to a list of strings as a property value by selecting
    the first value in the list as the default.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories("template_seven") as test_dirs:
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
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_generate=True
        )

        expected_return_code = 9
        expected_output = ""
        expected_error = ""
        expected_config_contents = """default_context:
  license: MIT
  other_name: default_other_name
  project_name: default_name"""

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert os.path.exists(config_path)
        act = TestHelpers.read_from_output_file(test_dirs, config_path)
        InProcessResult.compare_versus_expected(
            "configuration file", act, expected_config_contents
        )


def test_with_parameters_output_directory_config_not_exists_and_generate_include_with_dict() -> (
    None
):
    """
    Make sure that the application reacts properly to a property value that is a dictionary.
    """

    # Arrange
    project_name = "wilma"
    with TestDirectories("template_eight") as test_dirs:
        assert test_dirs.output_directory is not None

        config_path = os.path.join(
            test_dirs.output_directory,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )
        original_configuration_path = os.path.join(
            test_dirs.source_directory,
            CookieslicerConstants.get_cutter_source_configuration_file(),
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
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_generate=True
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = f"Cookie cutter configuration file '{original_configuration_path}' contains an 'dict' value that is not supported by cookieslicer."

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_with_parameters_output_directory_config_exists_and_generate() -> None:
    """
    Make sure that the application displays an error if asked to generate a configuration
    file that already exists.
    """

    # Arrange
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
        (
            project_name,
            _,
        ) = TestHelpers.write_default_cutter_settings_file(test_dirs)
        supplied_arguments = test_dirs.initialize_argument_list(
            project_name, include_generate=True
        )

        expected_return_code = 1
        expected_output = ""
        expected_error = """The settings configuration file '{config}' already exists in the output directory.

The -g/--generate option combined with that settings configuration file has resulted in a conflict that cannot be automatically resolved.""".replace(
            "{config}", config_path
        )

        # Act
        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
