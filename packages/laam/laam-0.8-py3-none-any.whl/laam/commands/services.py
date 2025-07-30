# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import contextlib
import json

from laam.utils import Color, get_color, print_error


def configure_parser(parser):
    ssub = parser.add_subparsers(
        dest="sub_cmd", help="Sub command", title="Sub command", required=True
    )

    # "services list"
    services_list = ssub.add_parser("list", help="List services")
    services_list.set_defaults(func=handle_list)
    services_list.add_argument("--json", action="store_true", help="Output in json")

    # "services logs"
    services_logs = ssub.add_parser("logs", help="Services logs")
    services_logs.set_defaults(func=handle_logs)
    services_logs.add_argument("name", help="name of the services")
    services_logs.add_argument("--json", action="store_true", help="Output in json")


def handle_list(options, session) -> int:
    ret = session.get(f"{options.uri}/services")
    if print_error(ret):
        return 1
    if options.json:
        print(json.dumps(ret.json()["items"]))
    else:
        print("Services:")
        for s in ret.json()["items"]:
            print(f"* {s['name']}: {s['status']}")


def handle_logs(options, session) -> int:
    ret = session.get(f"{options.uri}/services/{options.name}/logs")
    if print_error(ret):
        return 1
    if options.json:
        print(ret.text)
    else:
        for l in ret.json():
            msg = l["dt_iso"]
            priority = 6
            with contextlib.suppress(ValueError):
                priority = int(l.get("priority", 6))
            if l.get("pid"):
                msg += f" [{l['pid']}]"
            if l.get("logger"):
                msg += f" [{l['logger']}]"
            msg += f" {get_color(priority)}{l['message']}{Color.end.value}"
            print(msg)


def help_string():
    return "Manage services"
