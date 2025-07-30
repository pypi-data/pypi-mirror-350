"""
Module to provide a base class for any argument parsers.
"""

from tap import Tap


class ApplicationBaseArgumentParser(Tap):
    """
    Class to provide a base class for any argument parsers.
    """

    stack_trace: bool = False

    def configure(self) -> None:
        self.add_argument(
            "--stack_trace",
            help="if an error occurs, print out the stack trace for debug purposes",
        )
