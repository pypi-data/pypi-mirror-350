"""
Module to provide for a template that cookieslicer can apply.
"""

import inspect
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class CookieslicerTemplate:
    """
    Class to provide for a template that cookieslicer can apply.
    """

    slicer_version: int
    slicer_config_version: int
    once: List[str]
    remove: List[str]
    attention: List[str]

    def as_dict(self) -> Dict[str, Any]:
        """
        Translate the object into a dictionary object.
        """
        return {
            "slicer_version": self.slicer_version,
            "slicer_config_version": self.slicer_config_version,
            "once": self.once,
            "attention": self.attention,
            "remove": self.remove,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CookieslicerTemplate":
        """
        Translate a dictionary object into a CookieslicerTemplate object.
        """
        return CookieslicerTemplate(
            **{
                key: (
                    data[key]
                    if val.default == val.empty
                    else data.get(key, val.default)
                )
                for key, val in inspect.signature(
                    CookieslicerTemplate
                ).parameters.items()
            }
        )

    def __post_init__(self) -> None:
        assert isinstance(self.slicer_version, int)
        assert self.slicer_version == 1

        assert isinstance(self.slicer_config_version, int)
        assert self.slicer_config_version > 0

        assert isinstance(self.once, list)
        for i in self.once:
            assert isinstance(i, str)

        assert isinstance(self.attention, list)
        for i in self.attention:
            assert isinstance(i, str)

        assert isinstance(self.remove, list)
        for i in self.remove:
            assert isinstance(i, str)
