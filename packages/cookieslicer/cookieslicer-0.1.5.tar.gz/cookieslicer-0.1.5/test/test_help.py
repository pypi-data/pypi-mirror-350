"""
Module with the help set of tests for the cookieslicer project.
"""

import os
from test.cookieslicer_proxy import CookieslicerProxy
from typing import List


def test_with_no_parameters() -> None:
    """
    Make sure that we get the right help response when we provide no parameters.
    """

    # Arrange
    slicer_proxy = CookieslicerProxy()
    supplied_arguments: List[str] = []
    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: cookieslicer [-f] [-g] [-l] [-i INPUT_DIRECTORY] -s SOURCE_DIRECTORY
                    -p PROJECT_NAME [-o OUTPUT_DIRECTORY] [--stack-trace] [-h]
cookieslicer: error: the following arguments are required: -s/--source-directory, -p/--project-name"""

    # Act
    execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_with_help_parameter() -> None:
    """
    Make sure that we get the right help response when we provide the help parameter.
    """

    # Arrange
    slicer_proxy = CookieslicerProxy()
    supplied_arguments = ["-h"]
    expected_return_code = 0
    expected_output = """usage: cookieslicer [-f] [-g] [-l] [-i INPUT_DIRECTORY] -s SOURCE_DIRECTORY
                    -p PROJECT_NAME [-o OUTPUT_DIRECTORY] [--stack-trace] [-h]

Apply advanced templating by smartly using CookieCutter.

options:
  -f, --force           force template to be applied
  -g, --generate-config
                        generate a default configuration file for the template
  -l, --list-only       list the changes from applying the template, but do
                        not make those changes
  -i, --input-directory INPUT_DIRECTORY
                        (debugging only) existing directory to use as a
                        temporary staging area
  -s, --source-directory SOURCE_DIRECTORY
                        directory containing the template to apply
  -p, --project-name PROJECT_NAME
                        name of the project
  -o, --output-directory OUTPUT_DIRECTORY
                        existing directory to store the results of the
                        templating in (default: '.')
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  -h, --help            show this help message and exit
"""
    expected_error = ""

    # Act
    execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_with_conflicting_list_and_generate() -> None:
    """
    Make sure that we get the right response when we try and list (no changes)
    and generate (creates new file).
    """

    # Arrange
    slicer_proxy = CookieslicerProxy()

    full_path = os.path.join(os.getcwd(), "test", "resources", "template_one")
    supplied_arguments = ["-l", "-g", "-s", full_path, "-p", "fred"]
    expected_return_code = 2
    expected_output = ""
    expected_error = "Argument validation failed: Arguments -g/--generate-config and -l/--list-only conflict."

    # Act
    execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
