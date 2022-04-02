#!/usr/bin/env python3

"""Entry point for the porclr script."""

# Third party imports
from elevate import elevate

# Local imports
import cli
from __init__ import __app_name__, __app_version__


def main():
    elevate()
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
