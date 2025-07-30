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

    # "dockerfile"
    workers_dockerfile = ssub.add_parser("dockerfile", help="LAVA worker Dockerfile")
    workers_dockerfile.set_defaults(func=handle_dockerfile)
    workers_dockerfile.add_argument("id", type=int, help="Worker id")

    # "list"
    workers_list = ssub.add_parser("list", help="List workers")
    workers_list.set_defaults(func=handle_list)
    workers_list.add_argument("--json", action="store_true", help="Output in json")

    # "logs"
    workers_logs = ssub.add_parser("logs", help="Worker logs")
    workers_logs.set_defaults(func=handle_logs)
    workers_logs.add_argument("id", type=int, help="Worker id")
    workers_logs.add_argument("--json", action="store_true", help="Output in json")

    # "show"
    workers_show = ssub.add_parser("show", help="Worker details")
    workers_show.set_defaults(func=handle_show)
    workers_show.add_argument("id", type=int, help="Worker id")
    workers_show.add_argument("--json", action="store_true", help="Output in json")

    # "test"
    workers_test = ssub.add_parser("test", help="Test connection to server")
    workers_test.set_defaults(func=handle_test)
    workers_test.add_argument("id", type=int, help="Worker id")
    workers_test.add_argument("--json", action="store_true", help="Output in json")


def handle_dockerfile(options, session) -> int:
    ret = session.get(f"{options.uri}/workers/{options.id}/dockerfile")
    if print_error(ret):
        return 1
    print(ret.text)


def handle_list(options, session) -> int:
    ret = session.get(f"{options.uri}/workers")
    if print_error(ret):
        return 1
    if options.json:
        print(json.dumps(ret.json()["items"]))
    else:
        print("workers:")
        for w in ret.json()["items"]:
            print(f"* {w['id']}: {w['name']}")


def handle_logs(options, session) -> int:
    ret = session.get(f"{options.uri}/workers/{options.id}/logs")
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

    return 0


def handle_show(options, session) -> int:
    ret = session.get(f"{options.uri}/workers/{options.id}")
    if print_error(ret):
        return 1
    if options.json:
        print(ret.text)
    else:
        w = ret.json()
        print(f"id        : {w['id']}")
        print(f"name      : {w['name']}")
        print(f"running   : {w['running']}")
        print(f"server url: {w['server_url']}")
        print(f"token     : {w['token']}")


def handle_test(options, session) -> int:
    ret = session.get(f"{options.uri}/workers/{options.id}/test")
    if print_error(ret):
        return 1
    if options.json:
        print(ret.text)
    return 0 if ret.json()["connected"] else 1


def help_string():
    return "Manage workers"
