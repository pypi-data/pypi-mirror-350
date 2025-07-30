"""
Module to provide for "-m cookieslicer" access to the module,
as if it was run from the console.
"""

from cookieslicer.cookieslicer import Cookieslicer


def main() -> None:
    """
    Main entry point.  Exposed in this manner so that the setup
    entry_points configuration has something to execute.
    """
    Cookieslicer().main()


if __name__ == "__main__":
    main()
