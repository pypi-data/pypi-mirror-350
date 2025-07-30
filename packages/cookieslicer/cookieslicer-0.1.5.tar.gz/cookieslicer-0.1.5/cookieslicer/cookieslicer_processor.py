"""
Module to provide for the processor for the cookieslicer application.
"""

import hashlib
import json
import logging
import os
import shutil
import sys
from typing import Callable, List, Optional, Tuple

import cookiecutter.exceptions
import cookiecutter.main
import yaml

from cookieslicer.application_return_code import ApplicationReturnCode
from cookieslicer.cookieslicer_argument_parser import CookieslicerArgumentParser
from cookieslicer.cookieslicer_configuration import CookieslicerConfiguration
from cookieslicer.cookieslicer_constants import CookieslicerConstants
from cookieslicer.cookieslicer_template import CookieslicerTemplate

LOGGER = logging.getLogger(__name__)


class CookieslicerProcessor:
    """
    Class to provide for the processor for the cookieslicer application.
    """

    __PIPFILE = "Pipfile"

    __DEFAULT_ENCODING = "utf-8"
    __HASH_BLOCK_SIZE = 65536

    def __init__(
        self,
        parsed_arguments: CookieslicerArgumentParser,
        error_handler: Callable[[str, Optional[Exception], int], None],
    ) -> None:
        self.parsed_arguments = parsed_arguments
        self.__error_handler = error_handler

    # pylint: disable=broad-exception-caught
    def __load_slicer_template_from_file(
        self, load_directory: str
    ) -> CookieslicerTemplate:
        try:
            input_file_name = os.path.join(
                load_directory,
                CookieslicerConstants.get_slicer_output_configuration_file(),
            )
            with open(
                input_file_name, "rt", encoding=CookieslicerProcessor.__DEFAULT_ENCODING
            ) as input_file:
                slicer_template_object = json.load(input_file)
        except Exception as this_exception:
            self.__handle_application_error(
                f"Cookieslicer template file '{input_file_name}' was not loaded.",
                this_exception,
            )
        return CookieslicerTemplate.from_dict(slicer_template_object)

    # pylint: enable=broad-exception-caught

    # pylint: disable=broad-exception-caught
    def __load_destination_slicer_file_if_present(
        self,
    ) -> Optional[CookieslicerConfiguration]:
        try:
            input_file_name = os.path.join(
                self.parsed_arguments.output_directory,
                CookieslicerConstants.get_slicer_output_configuration_file(),
            )
            if not os.path.isfile(input_file_name):
                return None
            with open(
                input_file_name, "rt", encoding=CookieslicerProcessor.__DEFAULT_ENCODING
            ) as input_file:
                slicer_config_object = json.load(input_file)
        except Exception as this_exception:
            self.__handle_application_error(
                f"Cookieslicer output file '{input_file_name}' was not loaded.",
                this_exception,
            )
        return CookieslicerConfiguration.from_dict(slicer_config_object)

    # pylint: enable=broad-exception-caught

    def __calculate_file_hash(self, file_path: str) -> str:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as binary_input_file:
            file_buffer = binary_input_file.read(
                CookieslicerProcessor.__HASH_BLOCK_SIZE
            )
            while len(file_buffer) > 0:
                hasher.update(file_buffer)
                file_buffer = binary_input_file.read(
                    CookieslicerProcessor.__HASH_BLOCK_SIZE
                )
        return hasher.hexdigest()

    def __process_copy_file(
        self, next_relative_file: str, next_input_file: str, next_output_file: str
    ) -> Tuple[bool, bool]:
        return self.__copy_file_with_log_message(
            "Encountered unmarked file '%s'. Copying file.",
            next_relative_file,
            next_output_file,
            next_input_file,
        )

    def __process_once_file(
        self, next_relative_file: str, next_input_file: str, next_output_file: str
    ) -> Tuple[bool, bool]:
        if not os.path.exists(next_output_file):
            return self.__copy_file_with_log_message(
                "Encountered file '%s' marked as once and does not exist at destination. Copying file.",
                next_relative_file,
                next_output_file,
                next_input_file,
            )
        LOGGER.debug(
            "File '%s' marked as once and already exists at destination.  Skipping file.",
            next_relative_file,
        )
        if self.parsed_arguments.list_only:
            print(
                f"File '{next_relative_file}' is marked as copy-once and already exists at destination.  Skipping file."
            )
        return False, False

    def __process_attention_file(
        self,
        next_relative_file: str,
        next_input_file: str,
        next_output_file: str,
        attention_files: List[str],
    ) -> Tuple[bool, bool]:
        was_present_before = os.path.exists(next_output_file)
        did_copy_file, did_skip_copy = self.__copy_file_with_log_message(
            "Encountered file '%s' marked as requiring attention. Copying file.",
            next_relative_file,
            next_output_file,
            next_input_file,
        )
        if not did_skip_copy and was_present_before:
            attention_files.append(next_output_file)
        if self.parsed_arguments.list_only and did_copy_file and not did_skip_copy:
            print(f"File '{next_relative_file}' marked as needing special attention.")
        return did_copy_file, did_skip_copy

    def __handle_copy_error(self, error_message: str) -> None:
        error_message += (
            "\n\nUpdating output directory with template was interupted part way.\n\n"
            + "After diagnosing the reported issue, a backup of the output directory should be used to revert "
            + "the directory to a known good state before trying to address the diagnosed issue."
        )
        self.__handle_application_error(error_message)

    def __copy_file_with_log_message(
        self,
        log_messsage_format: str,
        next_relative_file: str,
        next_output_file: str,
        next_input_file: str,
    ) -> Tuple[bool, bool]:
        LOGGER.debug(log_messsage_format, next_relative_file)

        output_file_directory = os.path.dirname(next_output_file)
        if not os.path.isdir(output_file_directory):
            LOGGER.debug(
                "Destination directory '%s' does not exist.  Creating.",
                output_file_directory,
            )
            if os.path.isfile(output_file_directory):
                self.__handle_copy_error(
                    f"Output directory file '{output_file_directory}' conflicts with creating a directory named '{output_file_directory}' to hold file '{next_output_file}'."
                )
            os.makedirs(output_file_directory, exist_ok=False)

        do_file_copy = self.__calculate_whether_to_copy_file(
            next_output_file, next_input_file
        )

        if do_file_copy:
            if self.parsed_arguments.list_only:
                print(f"File '{next_relative_file}' copied.")
            else:
                LOGGER.debug(
                    "Copying template file '%s' to destination file '%s'.",
                    next_relative_file,
                    next_output_file,
                )
                shutil.copy(next_input_file, next_output_file)
        else:
            if self.parsed_arguments.list_only:
                print(
                    f"File '{next_relative_file}' and destination file are equal.  Skipping file."
                )
            LOGGER.debug(
                "Template file '%s' and destination file '%s' equal.  Skipping file.",
                next_relative_file,
                next_output_file,
            )
        return True, not do_file_copy

    def __calculate_whether_to_copy_file(
        self, next_output_file: str, next_input_file: str
    ) -> bool:
        do_file_copy = True
        if os.path.exists(next_output_file):
            if os.path.isdir(next_output_file):
                self.__handle_copy_error(
                    f"Output directory '{next_output_file}' conflicts with creating a file named '{next_output_file}'."
                )
            destination_digest = self.__calculate_file_hash(next_output_file)
            template_digest = self.__calculate_file_hash(next_input_file)
            LOGGER.debug("Template digest: %s", template_digest)
            LOGGER.debug("Destination digest: %s", destination_digest)
            do_file_copy = destination_digest != template_digest
        return do_file_copy

    # pylint: disable=too-many-arguments
    def __process_found_files(
        self,
        file_template: CookieslicerTemplate,
        next_relative_file: str,
        next_input_file: str,
        next_output_file: str,
        attention_files: List[str],
    ) -> Tuple[bool, bool]:
        # TODO turn off? pre-process?
        if "\\" in next_relative_file:
            next_relative_file = next_relative_file.replace("\\", "/")

        did_copy_file = False
        did_skip_copy = False
        if (
            next_relative_file
            == CookieslicerConstants.get_slicer_input_configuration_file()
        ):
            LOGGER.debug(
                "Encountered configuration file '%s'.  Skipping file.",
                next_relative_file,
            )
            if self.parsed_arguments.list_only:
                print(f"File '{next_relative_file}' is a system file.  Skipping file.")
            did_skip_copy = True
        elif next_relative_file in file_template.remove:
            LOGGER.debug(
                "Encountered file '%s' marked for removal.  Skipping file.",
                next_relative_file,
            )
            if self.parsed_arguments.list_only:
                print(
                    f"File '{next_relative_file}' marked for removal.  Skipping file."
                )
            did_copy_file = did_skip_copy = True
        elif next_relative_file in file_template.once:
            did_copy_file, did_skip_copy = self.__process_once_file(
                next_relative_file, next_input_file, next_output_file
            )
        elif next_relative_file in file_template.attention:
            did_copy_file, did_skip_copy = self.__process_attention_file(
                next_relative_file, next_input_file, next_output_file, attention_files
            )
        else:
            did_copy_file, did_skip_copy = self.__process_copy_file(
                next_relative_file, next_input_file, next_output_file
            )
        return did_copy_file, did_skip_copy

    # pylint: enable=too-many-arguments

    def __process_remove_files(self, file_template: CookieslicerTemplate) -> int:
        num_removed = 0
        for next_relative_file in file_template.remove:
            next_output_file = os.path.join(
                self.parsed_arguments.output_directory, next_relative_file
            )
            LOGGER.debug(
                "File '%s' marked for removal at destination.",
                next_relative_file,
            )
            if os.path.exists(next_output_file):
                if self.parsed_arguments.list_only:
                    print(
                        f"File '{next_relative_file}' was marked for removal.  Removing file."
                    )
                LOGGER.debug(
                    "File '%s' encountered at destination.  Removing.",
                    next_output_file,
                )
                os.remove(next_output_file)
                num_removed += 1
            elif self.parsed_arguments.list_only:
                print(
                    f"File '{next_relative_file}' was marked for removal but does not exist.  Skipping file."
                )

        return num_removed

    # pylint: disable=too-many-locals
    def __process_tempalted_files(
        self, file_template: CookieslicerTemplate, template_directory: str
    ) -> Tuple[List[str], int, int, int, int, int]:
        attention_files: List[str] = []

        # The "cookiecutter-config.yaml" file is automatically omitted when creating
        # the "input" directory, so we start the number of system files at 1 to make
        # this make more sense.
        number_copied = 0
        number_skipped = 0
        number_skipped_once = 0
        number_system = 0

        for walk_directory, _, walk_files in os.walk(template_directory):
            for next_file in walk_files:
                next_input_file = os.path.join(walk_directory, next_file)
                next_relative_file = next_input_file[len(template_directory) :]
                next_output_file = os.path.join(
                    self.parsed_arguments.output_directory, next_relative_file
                )

                LOGGER.debug(next_relative_file)
                did_copy, did_skip = self.__process_found_files(
                    file_template,
                    next_relative_file,
                    next_input_file,
                    next_output_file,
                    attention_files,
                )
                LOGGER.debug(
                    "did_copy = %s,did_skip = %s", str(did_copy), str(did_skip)
                )
                LOGGER.debug(
                    "number_skipped = %d,number_copied = %d,number_system = %d,number_skipped_once = %d",
                    number_skipped,
                    number_copied,
                    number_system,
                    number_skipped_once,
                )
                if did_copy:
                    if did_skip:
                        number_skipped += 1
                    else:
                        number_copied += 1
                elif did_skip:
                    number_system += 1
                else:
                    number_skipped_once += 1
                LOGGER.debug(
                    "number_skipped = %d,number_copied = %d,number_system = %d,number_skipped_once = %d",
                    number_skipped,
                    number_copied,
                    number_system,
                    number_skipped_once,
                )

        num_removed = self.__process_remove_files(file_template)
        return (
            attention_files,
            number_copied,
            number_skipped,
            number_skipped_once,
            num_removed,
            number_system,
        )

    # pylint: enable=too-many-locals

    def __apply_cookie_cutter(
        self,
        cookiecutter_source_directory: str,
        config_file: str,
        nested_directory_name: str,
        template_directory: str,
    ) -> str:
        try:
            cookiecutter.main.cookiecutter(
                cookiecutter_source_directory,
                output_dir=template_directory,
                config_file=config_file,
                no_input=True,
                overwrite_if_exists=True,
            )
        except cookiecutter.exceptions.CookiecutterException as this_exception:
            self.__handle_application_error(
                f"General error with cookiecutter: {this_exception}", this_exception
            )

        return os.path.join(template_directory, nested_directory_name) + os.sep

    def check_for_apply_template_permission(
        self,
    ) -> Tuple[Optional[CookieslicerConfiguration], str]:
        """
        Check to see if it is okay to go ahead and apply the template. If the
        template version is already where it needs to be, this function will
        simply use sys.exit to terminate.
        """

        if existing_configuration := self.__load_destination_slicer_file_if_present():
            LOGGER.info(
                "Local cookieslicer configuration loaded with config version %d.",
                existing_configuration.config_version,
            )
        else:
            LOGGER.info("Cookieslicer configuration does not yet exist.")

        project_directory = os.path.join(
            self.parsed_arguments.source_directory,
            CookieslicerConstants.get_cutter_source_template_directory(),
        )
        file_template = self.__load_slicer_template_from_file(project_directory)
        LOGGER.info(
            "Templated cookieslicer version is %d.", file_template.slicer_version
        )
        LOGGER.info(
            "Templated cookieslicer configuration version is %d.",
            file_template.slicer_config_version,
        )

        if (
            existing_configuration
            and not self.parsed_arguments.force
            and file_template.slicer_config_version
            == existing_configuration.config_version
        ):
            print(
                f"Cookie slicer destination version '{existing_configuration.config_version}' is equal to the template version."
            )
            print("No templating required.")
            sys.exit(ApplicationReturnCode.SUCCESS.value)

        return existing_configuration, project_directory

    def __write_cookieslicer_configuration(
        self,
        existing_configuration: Optional[CookieslicerConfiguration],
        file_template: CookieslicerTemplate,
    ) -> None:
        if existing_configuration:
            CookieslicerConfiguration.update_config_version(
                existing_configuration, file_template.slicer_config_version
            )
            updated_configuration = CookieslicerConfiguration.update_config_version(
                existing_configuration, file_template.slicer_config_version
            )
        else:
            updated_configuration = CookieslicerConfiguration(1)

        output_file_name = os.path.join(
            self.parsed_arguments.output_directory, "cookieslicer.json"
        )
        with open(
            output_file_name, "wt", encoding=CookieslicerProcessor.__DEFAULT_ENCODING
        ) as output_file:
            json.dump(updated_configuration.as_dict(), output_file)

    def __generate_configuration_file(self) -> None:
        cutter_config_file = os.path.join(
            self.parsed_arguments.source_directory,
            CookieslicerConstants.get_cutter_source_configuration_file(),
        )
        with open(
            cutter_config_file, "rt", encoding=CookieslicerProcessor.__DEFAULT_ENCODING
        ) as input_file:
            cutter_configuration_dict = json.load(input_file)

        default_context = {}
        for item_key, item_value in cutter_configuration_dict.items():
            if item_key == "_copy_without_render":
                # Since this only affects the output format, this has no bearing
                # on the configuration files.
                continue
            if item_key == "_extensions":
                # Changes how the configuration file is interpretted.
                self.__handle_application_error(
                    f"Cookie cutter configuration file '{cutter_config_file}' contains an '_extensions' key that is not supported by cookieslicer."
                )
            if isinstance(item_value, dict):
                # Changes how the configuration file is interpretted.
                self.__handle_application_error(
                    f"Cookie cutter configuration file '{cutter_config_file}' contains an 'dict' value that is not supported by cookieslicer."
                )
            if (
                "{%" in item_key
                or "{%" in item_value
                or "{{" in item_key
                or "{{" in item_value
            ):
                # Changes how the configuration file is interpretted.
                self.__handle_application_error(
                    f"Cookie cutter configuration file '{cutter_config_file}' contains "
                    + "template extension '{%' or '{{' sequences."
                )
            if isinstance(item_value, list):
                default_context[item_key] = item_value[0]
            else:
                default_context[item_key] = item_value

        full_configuration = {"default_context": default_context}
        slicer_cutter_config_file = os.path.join(
            self.parsed_arguments.output_directory,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )
        with open(
            slicer_cutter_config_file,
            "wt",
            encoding=CookieslicerProcessor.__DEFAULT_ENCODING,
        ) as output_file:
            yaml.dump(full_configuration, output_file, indent=2)

        sys.exit(ApplicationReturnCode.CONFIG_GENERATED.value)

    # pylint: disable=broad-exception-caught
    def apply_templating(
        self,
        template_directory: str,
        existing_configuration: Optional[CookieslicerConfiguration],
        config_file_path: str,
    ) -> None:
        """
        Do the work to actually apply the templating.
        """

        # Apply cookiecutter itself, placing its results into the template_directory
        # directory for examination.
        template_directory = self.__apply_cookie_cutter(
            self.parsed_arguments.source_directory,
            config_file_path,
            self.parsed_arguments.project_name,
            template_directory,
        )

        file_template = self.__load_slicer_template_from_file(template_directory)

        try:
            self.__apply_actual_templating(
                existing_configuration, file_template, template_directory
            )
        except Exception as this_exception:
            self.__handle_application_error(
                f"Error '{type(this_exception).__name__}' occurred applying template: {this_exception}\nRevert output directory to previous well-known state before continuing.",
                this_exception,
            )

    # pylint: enable=broad-exception-caught

    def __apply_actual_templating(
        self,
        existing_configuration: Optional[CookieslicerConfiguration],
        file_template: CookieslicerTemplate,
        template_directory: str,
    ) -> None:
        before_pipfile_hash = None
        output_pipfile_path = os.path.join(
            self.parsed_arguments.output_directory, CookieslicerProcessor.__PIPFILE
        )
        if os.path.isfile(output_pipfile_path):
            before_pipfile_hash = self.__calculate_file_hash(output_pipfile_path)

        (
            attention_files,
            number_copied,
            number_skipped,
            number_skipped_once,
            num_removed,
            number_system,
        ) = self.__process_tempalted_files(file_template, template_directory)
        print(f"attention_files = {attention_files}")
        print(f"number_copied = {number_copied}")
        print(f"number_skipped = {number_skipped}")
        print(f"number_skipped_once = {number_skipped_once}")
        print(f"number_system = {number_system}")
        print(f"num_removed = {num_removed}")

        if self.parsed_arguments.list_only:
            return

        self.__write_cookieslicer_configuration(existing_configuration, file_template)

        if before_pipfile_hash and os.path.isfile(output_pipfile_path):
            after_pipfile_hash = self.__calculate_file_hash(output_pipfile_path)
            if after_pipfile_hash != before_pipfile_hash:
                sys.exit(ApplicationReturnCode.PIP_UPDATED.value)

    def ensure_cookieslicer_output_config_present(self, config_file_path: str) -> None:
        """
        Ensure that the output configuration is present.
        """
        if os.path.isfile(config_file_path):
            if self.parsed_arguments.generate_config:
                self.__handle_application_error(
                    f"The settings configuration file '{config_file_path}' already exists in the output directory.\n\n"
                    + "The -g/--generate option combined with that settings configuration file has resulted in a conflict that cannot be automatically resolved."
                )
            return
        if not os.path.isdir(config_file_path):
            if self.parsed_arguments.generate_config:
                self.__generate_configuration_file()
            self.__handle_application_error(
                f"Settings configuration file '{config_file_path}' was not found within the output directory.\n\n"
                + "To generate a default settings configuration file, execute the command line again with the -g/--generate option."
            )
        else:
            self.__handle_application_error(
                f"Settings configuration file '{config_file_path}' cannot be a directory."
            )

    def ensure_cookieslicer_source_config_present(self) -> None:
        """
        Make sure that the source configuration is present.
        """
        project_directory = os.path.join(
            self.parsed_arguments.source_directory,
            CookieslicerConstants.get_cutter_source_template_directory(),
        )
        if not os.path.isdir(project_directory):
            self.__handle_application_error(
                f"Source directory '{self.parsed_arguments.source_directory}' does not contain a '{CookieslicerConstants.get_cutter_source_template_directory()}' subdirectory."
            )

        input_file_name = os.path.join(
            project_directory,
            CookieslicerConstants.get_slicer_output_configuration_file(),
        )
        if not os.path.isfile(input_file_name):
            self.__handle_application_error(
                f"Source template directory '{project_directory}' does not contain a '{CookieslicerConstants.get_slicer_output_configuration_file()}' file."
            )

    def __handle_application_error(
        self,
        formatted_error: str,
        thrown_error: Optional[Exception] = None,
    ) -> None:
        self.__error_handler(
            formatted_error, thrown_error, ApplicationReturnCode.GENERAL_FAILURE.value
        )
