# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import asyncio
import fnmatch
import json
import re
import sys
import termios
import tty
from contextlib import contextmanager

import aiohttp

from laam.utils import print_error


def configure_parser(parser):
    ssub = parser.add_subparsers(
        dest="sub_cmd", help="Sub command", title="Sub command", required=True
    )

    # "serials list"
    serials_list = ssub.add_parser("list", help="List serials")
    serials_list.set_defaults(func=handle_list)
    serials_list.add_argument("--filter", default=None, help="Filter by path")
    serials_list.add_argument("--json", action="store_true", help="Output in json")

    # "serials connect"
    serials_connect = ssub.add_parser("connect", help="Connect to serial")
    serials_connect.set_defaults(func=handle_connect)
    serials_connect.add_argument("name", help="name of the serial")

    # "serials show"
    serials_show = ssub.add_parser("show", help="Serial details")
    serials_show.set_defaults(func=handle_show)
    serials_show.add_argument("--json", action="store_true", help="Output in json")
    serials_show.add_argument("name", help="name of the serial")


async def stdin_reader(ws):
    try:
        with stream_as_raw(sys.stdin):
            loop = asyncio.get_event_loop()
            reader = asyncio.StreamReader()
            protocol = asyncio.StreamReaderProtocol(reader)
            await loop.connect_read_pipe(lambda: protocol, sys.stdin)

            while True:
                if ws.closed:
                    return
                c = await reader.read(1)
                c = c.decode("utf-8")
                await ws.send_str(c)
    except Exception as exc:
        print(exc)
        return


@contextmanager
def stream_as_raw(stream):
    original_stty = termios.tcgetattr(stream)
    try:
        tty.setcbreak(stream)
        yield
    finally:
        termios.tcsetattr(stream, termios.TCSANOW, original_stty)


async def handle_serials_connect(ws_url: str, port: int):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url, params={"port": port}, heartbeat=5) as ws:
            stdin_reader_task = asyncio.create_task(stdin_reader(ws))
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    sys.stdout.write(msg.data)
                    sys.stdout.flush()
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    await ws.close()
                    stdin_reader_task.cancel()
                    break


def handle_list(options, session) -> int:
    ret = session.get(f"{options.uri}/devices/serials")
    if print_error(ret):
        return 1

    serials = {}
    for s in ret.json()["items"]:
        baudrate = int(re.split("[neomsNEOMS]", s["speed"])[0])
        serials.setdefault(s["path"], {})[baudrate] = (s["name"], s["port"], s["speed"])

    if options.json:
        if options.filter:
            print(
                json.dumps(
                    [
                        k
                        for k in ret.json()["items"]
                        if fnmatch.fnmatch(k["path"], options.filter)
                    ]
                )
            )
        else:
            print(json.dumps([k for k in ret.json()["items"]]))
    else:
        print("Serials:")
        for s in sorted(serials):
            if options.filter and not fnmatch.fnmatch(s, options.filter):
                continue
            print(f"* {s}")
            for speed in sorted(serials[s]):
                d = serials[s][speed]
                print(f"  * {d[0]}")
                print(f"    - port : {d[1]}")
                print(f"    - speed: {d[2]}")


def handle_connect(options, session) -> int:
    ret = session.get(f"{options.uri}/devices/serials/{options.name}")
    if print_error(ret):
        return 1
    port = ret.json()["port"]
    print(f"Connecting to {options.ws_url} port {port}")
    try:
        asyncio.run(handle_serials_connect(options.ws_url, int(port)))
    except KeyboardInterrupt:
        print("\nLeaving...")
        return 1


def handle_show(options, session) -> int:
    ret = session.get(f"{options.uri}/devices/serials/{options.name}")
    if print_error(ret):
        return 1
    if options.json:
        print(ret.text)
    else:
        print(f"name : {ret.json()['name']}")
        print(f"path : {ret.json()['path']}")
        print(f"port : {ret.json()['port']}")
        print(f"speed:{ret.json()['speed']}")


def help_string():
    return "Manage DUT serials"
