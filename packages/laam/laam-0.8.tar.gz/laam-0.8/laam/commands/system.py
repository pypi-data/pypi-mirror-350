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

    # "logs"
    system_logs = ssub.add_parser("logs", help="Appliance logs")
    system_logs.set_defaults(func=handle_logs)
    system_logs.add_argument("--json", action="store_true", help="Output in json")

    # "fleet"
    system_fleet = ssub.add_parser("fleet", help="Bakfleet Information")
    system_fleet.set_defaults(func=handle_fleet)
    system_fleet.add_argument("--json", action="store_true", help="Output in json")

    # "version"
    system_version = ssub.add_parser("version", help="Appliance Version")
    system_version.set_defaults(func=handle_version)
    system_version.add_argument("--json", action="store_true", help="Output in json")


def handle_version(options, session) -> int:
    ret = session.get(f"{options.uri}/system/version")
    if print_error(ret):
        if ret.status_code == 404:  # to be deleted after next LAA release (>v1.4.1)
            print("Not available in this version, please check available LAA updates")
        return 1
    if options.json:
        print(json.dumps(ret.json()))
    else:
        print(ret.json()["version"])


def handle_fleet(options, session) -> int:
    ret = session.get(f"{options.uri}/system/fleet")
    if print_error(ret):
        if ret.status_code == 404:  # to be deleted after next LAA release (>v1.4.1)
            print("Not available in this version, please check available LAA updates")
        return 1
    if options.json:
        print(json.dumps(ret.json()))
    else:
        print("Fleet:")
        data = ret.json()
        print(f"* online: {data['online']}")
        print(f"* serial: {data['serial']}")
        print(f"* org   : {data['organization']}")
        print(f"* token : {data['token']}")


def handle_logs(options, session) -> int:
    ret = session.get(f"{options.uri}/services/appliance/logs")
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
    return "Get LAA Info"
