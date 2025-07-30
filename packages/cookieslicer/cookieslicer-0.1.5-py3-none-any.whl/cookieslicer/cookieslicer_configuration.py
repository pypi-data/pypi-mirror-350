"""
Module to provide for an encapsulation of the configuration.
"""

import inspect
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class CookieslicerConfiguration:
    """
    Class to provide for an encapsulation of the configuration.
    """

    config_version: int

    def as_dict(self) -> Dict[str, Any]:
        """
        Translate the object into a dictionary object.
        """
        return {"config_version": self.config_version}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CookieslicerConfiguration":
        """
        Translate a dictionary object into a CookieslicerTemplate object.
        """
        return CookieslicerConfiguration(
            **{
                key: (
                    data[key]
                    if val.default == val.empty
                    else data.get(key, val.default)
                )
                for key, val in inspect.signature(
                    CookieslicerConfiguration
                ).parameters.items()
            }
        )

    @staticmethod
    def update_config_version(
        existing_configuration: "CookieslicerConfiguration", config_version: int
    ) -> "CookieslicerConfiguration":
        """
        Update the configuration_version field, generating a new instance.
        """

        existing_configuration_as_dict = existing_configuration.as_dict()
        existing_configuration_as_dict["config_version"] = config_version
        return CookieslicerConfiguration.from_dict(existing_configuration_as_dict)

    def __post_init__(self) -> None:
        assert isinstance(self.config_version, int)
        assert self.config_version > 0
