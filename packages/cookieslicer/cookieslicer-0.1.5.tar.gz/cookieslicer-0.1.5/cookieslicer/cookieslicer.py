"""
Module to provide the core functionality of the cookieslicer package.
"""

import logging
import os
import tempfile

from cookieslicer.cookieslicer_argument_parser import CookieslicerArgumentParser
from cookieslicer.cookieslicer_constants import CookieslicerConstants
from cookieslicer.cookieslicer_processor import CookieslicerProcessor
from cookieslicer.main import ApplicationBase

LOGGER = logging.getLogger(__name__)


class Cookieslicer(ApplicationBase):
    """
    Class to provide the core functionality of the cookieslicer package.
    """

    # pylint: disable=useless-parent-delegation
    def __init__(self) -> None:
        super().__init__()

    # pylint: enable=useless-parent-delegation

    def _post_parse_arguments(
        self, parse_arguments: CookieslicerArgumentParser
    ) -> None:
        super()._post_parse_arguments(parse_arguments)
        _ = parse_arguments

    def _run(self, parse_arguments: CookieslicerArgumentParser) -> None:
        super()._run(parse_arguments)

        config_file = os.path.join(
            self.parsed_arguments.output_directory,
            CookieslicerConstants.get_cutter_output_settings_file(),
        )

        processor = CookieslicerProcessor(
            self.parsed_arguments, self._handle_application_error
        )

        # Ensure that the proper configuration files are present.
        processor.ensure_cookieslicer_output_config_present(config_file)
        processor.ensure_cookieslicer_source_config_present()

        # Check to see if the specified version of the template has already been
        # applied.  If so, this function will perform a sys.exit to shortcut everything else.
        (
            existing_configuration,
            _,
        ) = processor.check_for_apply_template_permission()

        # As an option, the "input" directory can be specified as an intermediate directory
        # to contain the cookiecutter results.  Not that in this case, the user is responsible
        # for deleting this directory between runs to avoid "noise".
        if self.parsed_arguments.input_directory:
            processor.apply_templating(
                (
                    self.parsed_arguments.input_directory
                    if self.parsed_arguments.input_directory.endswith(os.sep)
                    else self.parsed_arguments.input_directory + os.sep
                ),
                existing_configuration,
                config_file,
            )

        # Otherwise, just create a temporary directory to store the templated cookiecutter output in.
        else:
            with tempfile.TemporaryDirectory() as temporary_directory:
                processor.apply_templating(
                    (
                        temporary_directory
                        if temporary_directory.endswith(os.sep)
                        else temporary_directory + os.sep
                    ),
                    existing_configuration,
                    config_file,
                )
