"""
Module to provide for constants used within the project.
"""


class CookieslicerConstants:
    """
    Class to provide for constants used within the project.
    """

    __CUTTER_SOURCE_CONFIGURATION_FILE = "cookiecutter.json"
    __SLICER_CONFIGURATION_FILE = "cookieslicer.json"
    __CUTTER_OUTPUT_SETTINGS_FILE = "cookiecutter-config.yaml"
    __SOURCE_TEMPLATE_SUBDIR = "{{cookiecutter.project_name}}"

    @staticmethod
    def get_cutter_source_template_directory() -> str:
        """
        Get the template subdirectory.
        """
        return CookieslicerConstants.__SOURCE_TEMPLATE_SUBDIR

    @staticmethod
    def get_cutter_source_configuration_file() -> str:
        """
        Get the cookiecutter.json file that lives in the source/template.
        """
        return CookieslicerConstants.__CUTTER_SOURCE_CONFIGURATION_FILE

    @staticmethod
    def get_slicer_input_configuration_file() -> str:
        """
        Get the cookieslicer.json file that lives in the "input" directory once the template has been applied to it.
        """
        return CookieslicerConstants.__SLICER_CONFIGURATION_FILE

    @staticmethod
    def get_cutter_output_settings_file() -> str:
        """
        Get the cookiecutter-config.yaml file that lives in the output.
        """
        return CookieslicerConstants.__CUTTER_OUTPUT_SETTINGS_FILE

    @staticmethod
    def get_slicer_output_configuration_file() -> str:
        """
        Get the cookieslicer.json file that lives in the "output" directory.
        """
        return CookieslicerConstants.__SLICER_CONFIGURATION_FILE
