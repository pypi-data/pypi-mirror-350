"""
Return codes for this application.
"""

import enum


class ApplicationReturnCode(enum.Enum):
    """
    Return codes for this application.
    """

    SUCCESS = 0
    GENERAL_FAILURE = 1
    ARGPARSE_FAILURE = 2
    PIP_UPDATED = 8
    CONFIG_GENERATED = 9
