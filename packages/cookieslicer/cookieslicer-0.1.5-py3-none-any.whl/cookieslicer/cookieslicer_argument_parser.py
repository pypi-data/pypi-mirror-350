"""
Module to provide an argument parser for the application.
"""

import argparse
import os
from typing import Optional, cast

from cookieslicer.application_base_argument_parser import ApplicationBaseArgumentParser
from cookieslicer.cookieslicer_constants import CookieslicerConstants


class CookieslicerArgumentParser(ApplicationBaseArgumentParser):
    """
    Class to provide an argument parser for the application.
    """

    force: bool = False
    generate_config: bool = False
    list_only: bool = False
    input_directory: Optional[str] = None
    source_directory: str
    project_name: str
    output_directory: str = "."

    def configure(self) -> None:
        super().configure()

        self.add_argument("-f", "--force", help="force template to be applied")
        self.add_argument(
            "-g",
            "--generate-config",
            help="generate a default configuration file for the template",
        )
        self.add_argument(
            "-l",
            "--list-only",
            help="list the changes from applying the template, but do not make those changes",
        )
        self.add_argument(
            "-i",
            "--input-directory",
            help="(debugging only) existing directory to use as a temporary staging area",
            type=CookieslicerArgumentParser.__validate_input_directory_existence,
        )
        self.add_argument(
            "-s",
            "--source-directory",
            help="directory containing the template to apply",
            type=CookieslicerArgumentParser.__validate_cookiecutter_directory_existence,
        )
        self.add_argument(
            "-p", "--project-name", help="name of the project"
        )  # no spaces?
        self.add_argument(
            "-o",
            "--output-directory",
            help="existing directory to store the results of the templating in (default: '.')",
            type=CookieslicerArgumentParser.__validate_output_directory_existence,
        )

    def process_args(self) -> None:
        if self.generate_config and self.list_only:
            raise ValueError(
                "Arguments -g/--generate-config and -l/--list-only conflict."
            )

        if self.input_directory and not self.input_directory.endswith(os.sep):
            self.input_directory += os.sep
        if not self.output_directory.endswith(os.sep):
            self.output_directory += os.sep

    @staticmethod
    def __validate_cookiecutter_directory_existence(input_value: str) -> str:
        if not os.path.isdir(input_value):
            raise argparse.ArgumentTypeError(
                f"Specified source directory '{input_value}' does not exist."
            )
        cutter_config_path = os.path.join(
            input_value, CookieslicerConstants.get_cutter_source_configuration_file()
        )
        if not os.path.isfile(cutter_config_path):
            raise argparse.ArgumentTypeError(
                f"Specified source directory '{input_value}' does not contain the required '{CookieslicerConstants.get_cutter_source_configuration_file()}' file."
            )
        return input_value

    @staticmethod
    def __validate_input_directory_existence(input_value: Optional[str]) -> str:
        if input_value is not None and not os.path.isdir(input_value):
            raise argparse.ArgumentTypeError(
                f"Specified input directory '{input_value}' does not exist."
            )
        return cast(str, input_value)

    @staticmethod
    def __validate_output_directory_existence(input_value: str) -> str:
        if not os.path.isdir(input_value):
            raise argparse.ArgumentTypeError(
                f"Specified output directory '{input_value}' does not exist."
            )
        return input_value
