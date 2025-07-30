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

    # "addresses"
    network_addresses = ssub.add_parser("addresses", help="List addresses")
    network_addresses.set_defaults(func=handle_addresses)
    network_addresses.add_argument("--json", action="store_true", help="Output in json")

    # "hostname"
    network_hostname = ssub.add_parser("hostname", help="Hostname")
    network_hostname.set_defaults(func=handle_hostname)

    # "interfaces"
    network_interfaces = ssub.add_parser("interfaces", help="List interfaces")
    network_interfaces.set_defaults(func=handle_interfaces)
    network_interfaces.add_argument(
        "--json", action="store_true", help="Output in json"
    )

    # "routes"
    network_routes = ssub.add_parser("routes", help="List routes")
    network_routes.set_defaults(func=handle_routes)
    network_routes.add_argument("--json", action="store_true", help="Output in json")

    # "settings"
    network_settings = ssub.add_parser("settings", help="Settings")
    network_settings.set_defaults(func=handle_settings)


def handle_addresses(options, session) -> int:
    ret = session.get(f"{options.uri}/network/addresses")
    if print_error(ret):
        return 1
    if options.json:
        print(ret.text)
    else:
        print("Addresses:")
        data = ret.json()
        for name in data:
            print(f"* {name}")
            for addr in data[name]:
                print(f"  * {addr['flags']}\t{addr['ip']}/{addr['prefix']}")


def handle_hostname(options, session) -> int:
    ret = session.get(f"{options.uri}/network/hostname")
    if print_error(ret):
        return 1
    print(ret.json()["hostname"])


def handle_interfaces(options, session) -> int:
    ret = session.get(f"{options.uri}/network/interfaces")
    if print_error(ret):
        return 1
    if options.json:
        print(json.dumps(ret.json()["items"]))
    else:
        print("Interfaces:")
        for s in ret.json()["items"]:
            if s["mac"]:
                print(f"* {s['name']} ({s['type']}): {s['status']} [{s['mac']}]")
            else:
                print(f"* {s['name']} ({s['type']}): {s['status']}")


def handle_routes(options, session) -> int:
    ret = session.get(f"{options.uri}/network/routes")
    if print_error(ret):
        return 1
    if options.json:
        print(ret.text)
    else:
        print("Routes:")
        data = ret.json()
        for name in data:
            if not data[name]:
                continue
            print(f"* {name}")
            for r in data[name]:
                if r["via"]:
                    print(
                        f"  * {r['src']} => {r['dst']}/{r['dst_prefix']} via {r['via']}"
                    )
                else:
                    print(f"  * {r['src']} => {r['dst']}/{r['dst_prefix']}")


def handle_settings(options, session) -> int:
    ret = session.get(f"{options.uri}/network/settings")
    if print_error(ret):
        return 1
    print(ret.text)


def help_string():
    return "Manage network"
