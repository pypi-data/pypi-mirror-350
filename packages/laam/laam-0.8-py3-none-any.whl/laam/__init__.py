# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import argparse
import os
import sys

import requests
import yaml

from laam.commands import (
    dut,
    files,
    identities,
    laacli,
    network,
    serials,
    services,
    system,
    usbs,
    workers,
)

#############
# Constants #
#############
__version__ = 0.8


###########
# Helpers #
###########
def load_config(identity):
    # Build the path to the configuration file
    config_dir = os.environ.get("XDG_CONFIG_HOME", "~/.config")
    config_filename = os.path.expanduser(os.path.join(config_dir, "laam.yaml"))

    try:
        with open(config_filename, encoding="utf-8") as f_conf:
            config = yaml.safe_load(f_conf.read())
        return config[identity]
    except (FileNotFoundError, KeyError, TypeError):
        return {}


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="laam", description="Linaro Automation Appliance Manager"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s, v{__version__}"
    )

    # identity or url
    url = parser.add_argument_group("identity").add_mutually_exclusive_group()
    url.add_argument("--uri", type=str, default=None, help="URI of the LAA API")
    url.add_argument(
        "--token",
        metavar="TOKEN",
        type=str,
        default=None,
        help="Token for the LAA API",
    )
    url.add_argument(
        "--identity",
        "-i",
        metavar="ID",
        type=str,
        default="default",
        help="Identity stored in the configuration",
    )

    sub = parser.add_subparsers(
        dest="cmd", help="Command", title="Command", required=True
    )
    COMMANDS = {
        "identities": identities,
        "dut": dut,
        "files": files,
        "laacli": laacli,
        "network": network,
        "serials": serials,
        "services": services,
        "system": system,
        "usbs": usbs,
        "workers": workers,
    }
    for name, cls in COMMANDS.items():
        cmd_parser = sub.add_parser(name, help=cls.help_string())
        cls.configure_parser(cmd_parser)

    return parser


##############
# Entrypoint #
##############
def main() -> int:
    # Parse arguments
    parser = setup_parser()
    options = parser.parse_args()

    # Skip when sub_command is "identities"
    if options.cmd != "identities":
        if (
            options.uri is None
        ):  # --identity is not provided since it's mutually exclusive
            config = load_config(options.identity)
            if config.get("uri") is None:
                print("Unknown identity '%s'" % options.identity, file=sys.stderr)
                return 1
            token = config.get("token")
            if token is None:
                print("Token is missing from identity config file", file=sys.stderr)
                return 1
            options.uri = config["uri"]
            options.token = token
        elif options.token is None:
            print("Token is mandatory", file=sys.stderr)
            return 1
        options.ws_url = (
            options.uri.replace("http://", "ws://").replace("https://", "wss://")
            + "/ws/"
        )
        options.uri = options.uri + "/api/v1"

    session = requests.Session()
    session.headers.update(
        {
            "Accept-Encoding": "",
            "Authorization": f"Bearer {options.token}",
            "User-Agent": f"laam v{__version__}",
        }
    )

    return options.func(options, session)
