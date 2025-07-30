"""
Module with the extra set of tests for the cookieslicer project that do not fit anywhere else.
"""

import json
import os
from test.cookieslicer_proxy import CookieslicerProxy
from test.pytest_directories import TestDirectories
from test.pytest_helpers import TestHelpers

from cookieslicer.cookieslicer_constants import CookieslicerConstants
from cookieslicer.cookieslicer_template import CookieslicerTemplate


def test_translate_template_to_dictionary() -> None:
    # sourcery skip: extract-method
    """
    Make sure that we can express the slicer template as a dictionary, for debugging
    purposes.
    """
    with TestDirectories("template_one") as test_dirs:
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

        execute_results = slicer_proxy.invoke_main(arguments=supplied_arguments)
        assert execute_results.return_code == 0

        assert test_dirs.input_directory is not None
        input_file_name = os.path.join(
            test_dirs.input_directory,
            project_name,
            CookieslicerConstants.get_slicer_input_configuration_file(),
        )
        with open(input_file_name, "rt", encoding="utf-8") as input_file:
            loaded_template = CookieslicerTemplate.from_dict(json.load(input_file))

            assert loaded_template.slicer_version == 1
            assert loaded_template.slicer_config_version == 1
            assert not loaded_template.once
            assert not loaded_template.attention
            assert not loaded_template.remove

        loaded_template_dict = loaded_template.as_dict()
        assert loaded_template_dict["slicer_version"] == 1
        assert loaded_template_dict["slicer_config_version"] == 1
        assert not loaded_template_dict["once"]
        assert not loaded_template_dict["attention"]
        assert not loaded_template_dict["remove"]
