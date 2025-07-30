# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import argparse
import base64
import sys


def configure_parser(parser):
    ssub = parser.add_subparsers(
        dest="sub_cmd", help="Sub command", title="Sub command", required=True
    )

    # "button"
    btn = ssub.add_parser("button", help="Virtual buttons")
    btn.set_defaults(func=handle_button)
    btn.add_argument("button", choices=["1", "2", "power", "reset"], help="Button")
    btn.add_argument("state", choices=["on", "off"], help="State")
    btn.add_argument("--json", action="store_true", help="Output in json")

    # "led"
    led = ssub.add_parser("led", help="User LED")
    led.set_defaults(func=handle_led)
    led.add_argument("color", choices=["green", "off", "yellow"], help="LED color")
    led.add_argument("--json", action="store_true", help="Output in json")

    # "power"
    pwr = ssub.add_parser("power", help="Power rails")
    pwr.set_defaults(func=handle_power)
    pwr.add_argument("vbus", choices=["1v8", "3v3", "5v", "12v"], help="Rail")
    pwr.add_argument("state", choices=["on", "off", "reset"], help="State")
    pwr.add_argument("--json", action="store_true", help="Output in json")

    # "rev"
    rev = ssub.add_parser("rev", help="LAA revision")
    rev.set_defaults(func=handle_rev)
    rev.add_argument("--json", action="store_true", help="Output in json")

    # "screenshot"
    screenshot = ssub.add_parser("screenshot", help="OLED screenshot")
    screenshot.set_defaults(func=handle_screenshot)
    screenshot.add_argument(
        "filename", type=argparse.FileType("wb"), help="Store the screenshot bitmap"
    )

    # "temp"
    temp = ssub.add_parser("temp", help="Query temperature (°C)")
    temp.set_defaults(func=handle_temp)
    temp.add_argument("probe", choices=["amb", "dut", "sys"], help="Probe")
    temp.add_argument("--json", action="store_true", help="Output in json")

    # "usb"
    usb = ssub.add_parser("usb", help="USB hub")
    usb.set_defaults(func=handle_usb)
    usb.add_argument("port", type=int, help="USB port, 0 will be the hub itself")
    usb.add_argument("state", choices=["on", "off", "reset", "start"], help="State")
    usb.add_argument("--json", action="store_true", help="Output in json")

    # "usbg-ms"
    usbgms = ssub.add_parser("usbg-ms", help="USB Gadget Mass storage")
    usbgms.set_defaults(func=handle_usbg_ms)
    usbgms.add_argument("state", choices=["on", "off", "status"], help="State")
    usbgms.add_argument("filename", help="Disk image to mount", default="", nargs="?")
    usbgms.add_argument("--json", action="store_true", help="Output in json")

    # "watt"
    watt = ssub.add_parser("watt", help="Power consumption")
    watt.set_defaults(func=handle_watt)
    watt.add_argument("vbus", choices=["1v8", "3v3", "5v", "12v"], help="Rail")
    watt.add_argument("--json", action="store_true", help="Output in json")


def call(options, session, endpoint: str, arguments, raw=False) -> int:
    ret = session.post(f"{options.uri}{endpoint}", json=arguments)
    if ret.status_code != 200:
        print(f"Unable to call the appliance API: {ret.status_code}")
        return 1
    if raw:
        return ret
    data = ret.json()
    if getattr(options, "json", False):
        print(ret.text)
    else:
        if data["stdout"]:
            print(data["stdout"])
        if data["stderr"]:
            print(data["stderr"], file=sys.stderr)
    return data["code"]


def handle_button(options, session) -> int:
    return call(
        options,
        session,
        "/laacli/button",
        {"button": options.button, "state": options.state},
    )


def handle_led(options, session) -> int:
    return call(options, session, "/laacli/led", {"color": options.color})


def handle_power(options, session) -> int:
    return call(
        options,
        session,
        "/laacli/power",
        {"vbus": options.vbus, "state": options.state},
    )


def handle_rev(options, session) -> int:
    return call(options, session, f"/laacli/rev", {})


def handle_screenshot(options, session) -> int:
    ret = call(options, session, f"/laacli/screenshot", {}, raw=True)
    data = base64.b64decode(ret.json()["screenshot"])
    options.filename.write(data)
    return 0


def handle_temp(options, session) -> int:
    return call(options, session, "/laacli/temp", {"probe": options.probe})


def handle_usb(options, session) -> int:
    return call(
        options, session, "/laacli/usb", {"port": options.port, "state": options.state}
    )


def handle_usbg_ms(options, session) -> int:
    return call(
        options,
        session,
        "/laacli/usbg-ms",
        {"state": options.state, "filename": options.filename},
    )


def handle_watt(options, session) -> int:
    return call(options, session, "/laacli/watt", {"vbus": options.vbus})


def help_string():
    return "Run laacli commands on the LAA"
