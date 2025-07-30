"""
Module to provide the common functionality used by application packages.
"""

import logging
import os
import runpy
import sys
import traceback
from typing import List, Optional, Tuple

from cookieslicer.application_return_code import ApplicationReturnCode
from cookieslicer.cookieslicer_argument_parser import CookieslicerArgumentParser

LOGGER = logging.getLogger(__name__)


class ApplicationBase:
    """
    Class to provide the common functionality used by application packages.
    """

    def __init__(self) -> None:
        self.__stack_trace = False
        self.__parsed_arguments: Optional[CookieslicerArgumentParser] = None

    @staticmethod
    def __get_program_info() -> Tuple[str, str]:
        file_path = __file__
        assert os.path.isabs(file_path)
        file_path = file_path.replace(os.sep, "/")
        last_index = file_path.rindex("/")
        file_path = f"{file_path[: last_index + 1]}version.py"
        version_meta = runpy.run_path(file_path)
        return str(version_meta["__project_name__"]), str(
            version_meta["__description__"]
        )

    def __parse_arguments(
        self, direct_args: Optional[List[str]]
    ) -> CookieslicerArgumentParser:
        project_name, project_one_liner = self.__get_program_info()
        self.__parsed_arguments = CookieslicerArgumentParser(
            prog=project_name, description=project_one_liner, underscores_to_dashes=True
        )

        try:
            self.__parsed_arguments.parse_args(args=direct_args)
            self._post_parse_arguments(self.__parsed_arguments)
        except ValueError as this_exception:
            self._handle_application_error(
                f"Argument validation failed: {this_exception}",
                this_exception,
                ApplicationReturnCode.ARGPARSE_FAILURE.value,
            )

        self.__stack_trace = self.__parsed_arguments.stack_trace
        return self.__parsed_arguments

    @property
    def parsed_arguments(self) -> CookieslicerArgumentParser:
        """
        Get the arguments parsed from the command line.
        """
        assert self.__parsed_arguments is not None
        return self.__parsed_arguments

    def _handle_application_error(
        self,
        formatted_error: str,
        thrown_error: Optional[Exception] = None,
        return_code: int = ApplicationReturnCode.GENERAL_FAILURE.value,
    ) -> None:
        LOGGER.warning(formatted_error, exc_info=thrown_error)
        stack_trace = "\n" + traceback.format_exc() if self.__stack_trace else ""
        print(f"\n\n{formatted_error}{stack_trace}", file=sys.stderr)
        sys.exit(return_code)

    def _post_parse_arguments(
        self, parse_arguments: CookieslicerArgumentParser
    ) -> None:
        # To be implemented by child class.
        #
        # Provides for the ability to do any post-processing of command line arguments.
        _ = parse_arguments

    def _run(self, parse_arguments: CookieslicerArgumentParser) -> None:
        # To be implemented by child class.
        #
        # Bulk of the processing will be done in here.
        _ = parse_arguments

    # pylint: disable=broad-exception-caught
    def main(self, direct_args: Optional[List[str]] = None) -> None:
        """
        Main entrance point.
        """
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

        try:
            parse_arguments = self.__parse_arguments(direct_args)

            self._run(parse_arguments)
        except SystemExit as this_exception:
            LOGGER.info("Application exited with return code %d.", this_exception.code)
            sys.exit(this_exception.code)
        except Exception as this_exception:
            self._handle_application_error(
                f"Unhandled exception '{type(this_exception).__name__}' caused program to terminate.\n"
                + "For more information, run the application again with the '--stack-trace' option.",
                this_exception,
            )
        # pylint: enable=broad-exception-caught

        sys.exit(ApplicationReturnCode.SUCCESS.value)
