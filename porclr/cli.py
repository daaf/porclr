#!/usr/bin/env python3
"""
Create links to Portainer's Docker Compose files in a specified directory.

Usage:
    porclr -l [<path>] | --link [<path>]

Options:
    -h --help   Show this help documentation.
    -l --link   Link Compose files
"""

# Third party imports
from docopt import docopt
from decouple import config

# Local imports
from link_portainer_compose_files import link


def init():
    args = docopt(__doc__, version="0.1")
    portainer_compose_dir = config("PORTAINER_COMPOSE_DIR")

    if args["<path>"]:
        local_repo = args["<path>"]
    else:
        local_repo = config("LINK_PARENT_DIR")

    if args["--link"]:
        link(portainer_compose_dir, local_repo)
