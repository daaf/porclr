#!/usr/bin/env python3

"""Entry point for the porclr script."""

# Third party imports
from elevate import elevate

# Standard library imports
import sys
import os

# Add project directory to PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Local imports
from porclr import cli, __app_name__, __version__


def main():
    elevate()
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
