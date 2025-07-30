# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import json

from laam.utils import print_error


def configure_parser(parser):
    ssub = parser.add_subparsers(
        dest="sub_cmd", help="Sub command", title="Sub command", required=True
    )

    # "usbs list"
    usbs_list = ssub.add_parser("list", help="List USB devices")
    usbs_list.set_defaults(func=handle_list)
    usbs_list.add_argument("--filter", default=None, help="Filter by path")
    usbs_list.add_argument("--json", action="store_true", help="Output in json")

    # "usbs show"
    usbs_show = ssub.add_parser("show", help="USB details")
    usbs_show.set_defaults(func=handle_show)
    usbs_show.add_argument("--json", action="store_true", help="Output in json")
    usbs_show.add_argument("bus", help="usb bus")
    usbs_show.add_argument("device", help="usb device")


def handle_list(options, session) -> int:
    ret = session.get(f"{options.uri}/devices/usbs")
    if print_error(ret):
        return 1

    if options.json:
        print(json.dumps(ret.json()["items"]))
    else:
        for u in ret.json()["items"]:
            print(f"Bus {u['bus']} Device {u['device']}: ID {u['id']} {u['tag']}")


def handle_show(options, session) -> int:
    ret = session.get(f"{options.uri}/devices/usbs/{options.bus}/{options.device}")
    if print_error(ret):
        return 1
    print(ret.text)


def help_string():
    return "List USB devices"
