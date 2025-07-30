# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import argparse
import dataclasses
import json
import shlex
import subprocess
import sys
from typing import Literal

import pexpect
import yaml

from laam.utils import Color, print_error


##############
# Data model #
##############
class Base:
    def as_dict(self):
        return dataclasses.asdict(self)

    def as_json(self):
        return json.dumps(self.as_dict())

    def as_yaml(self):
        return yaml.safe_dump(self.as_dict())

    @classmethod
    def new(cls, **kwargs):
        fields_names = [f.name for f in dataclasses.fields(cls)]
        i_kwargs = {}
        v_kwargs = {}
        for k in kwargs:
            if k in fields_names:
                v_kwargs[k] = kwargs[k]
            else:
                i_kwargs[k] = kwargs[k]

        assert not i_kwargs
        return cls(**v_kwargs)


@dataclasses.dataclass(kw_only=True)
class Device(Base):
    @dataclasses.dataclass(kw_only=True)
    class Power(Base):
        on: list[str] = dataclasses.field(default_factory=list)
        off: list[str] = dataclasses.field(default_factory=list)
        reset: list[str] = dataclasses.field(default_factory=list)

    name: str = "dtb name"
    bootloader: Literal["u-boot"] = "u-boot"
    interrupt: bool = True
    power: Power = dataclasses.field(default_factory=Power)
    serial: str = "ttymxc3"
    prompt: str = "=> "

    def __post_init__(self):
        if self.bootloader != "u-boot":
            raise NotImplementedError("u-boot is the only supported bootloader")
        if isinstance(self.power, dict):
            self.power = Device.Power(**self.power)


def configure_parser(parser):
    ssub = parser.add_subparsers(
        dest="sub_cmd", help="Sub command", title="Sub command", required=True
    )

    # "check"
    dut_check = ssub.add_parser("check", help="Check the configuration")
    dut_check.set_defaults(func=handle_check)
    dut_check.add_argument(
        "config", type=argparse.FileType("r"), help="Configuration file"
    )

    # "new"
    dut_new = ssub.add_parser(
        "new",
        help="Create a device configuration file",
    )
    dut_new.set_defaults(func=handle_new)
    dut_new.add_argument(
        "config", type=argparse.FileType("w"), help="Configuration file"
    )

    # "render"
    dut_render = ssub.add_parser(
        "render", help="Render device-type template and device dict"
    )
    dut_render.set_defaults(func=handle_render)
    dut_render.add_argument(
        "config", type=argparse.FileType("r"), help="Configuration file"
    )
    dut_render.add_argument(
        "dt_template", type=argparse.FileType("w"), help="Device-type template"
    )
    dut_render.add_argument(
        "device_dict", type=argparse.FileType("w"), help="Device dictionary"
    )

    # "test"
    dut_test = ssub.add_parser("test", help="Boot test the DUT")
    dut_test.set_defaults(func=handle_test)
    dut_test.add_argument(
        "--usbg-ms", type=argparse.FileType("r"), help="Image for USB gadget MS"
    )
    dut_test.add_argument(
        "config", type=argparse.FileType("r"), help="Configuration file"
    )


def handle_check(options, session) -> int:
    try:
        Device.new(**yaml.safe_load(options.config.read()))
        return 0
    except Exception as exc:
        print(f"Invalid configuration: {exc}")
        return 1


def handle_new(options, session) -> int:
    device = Device()
    print("Create a new device configuration (u-boot only)")
    device.name = input("dtb name> ")
    options.config.write(device.as_yaml())
    return 0


def handle_render(options, session) -> int:
    config = Device.new(**yaml.safe_load(options.config.read()))

    ret = session.get(f"{options.uri}/devices/serials/{config.serial}")
    if print_error(ret):
        return 1
    port = ret.json()["port"]

    print(
        f"Device-type template: '{options.dt_template.name}' (should be called '{config.name}.jinja2')"
    )
    options.dt_template.write(
        f"""{{% extends 'base-uboot.jinja2' %}}

{{% set uboot_needs_interrupt = uboot_needs_interrupt | default({config.interrupt}) %}}
{{% set bootloader_prompt = bootloader_prompt | default('{config.prompt}') %}}
"""
    )

    hard_reset = "',\n    '".join(config.power.reset).replace("laam ", "")
    power_on = "',\n    '".join(config.power.on).replace("laam ", "")
    power_off = "',\n    '".join(config.power.off).replace("laam ", "")
    print(f"Device dictionary: '{options.device_dict.name}'")
    options.device_dict.write(
        f"""{{% extends '{config.name}.jinja2' %}}

{{% set hard_reset_command = [
    '{hard_reset}'
] %}}
{{% set power_off_command = [
    '{power_off}'
] %}}
{{% set power_on_command =  [
    '{power_on}'
] %}}

{{% set connection_command = 'telnet localhost {port}' %}}

{{% set usbg_ms_commands = {{
    'disable': ['laacli', 'usbg-ms', 'off'],
    'enable': ['laacli', 'usbg-ms', 'on', '{{IMAGE}}']
}} %}}
{{% set docker_shell_extra_arguments = [
    '--add-host=lava-worker.internal:host-gateway',
    '--volume=/usr/bin/laacli:/usr/bin/laacli:ro',
    '--volume=/usr/bin/lsibcli:/usr/bin/lsibcli:ro',
    '--volume=/run/dbus/system_bus_socket:/run/dbus/system_bus_socket:rw'
] %}}
"""
    )


def replace_laam(options, cmd: str) -> str:
    if options.identity:
        return shlex.split(cmd.replace("laam ", f"laam -i {options.identity} "))
    else:
        return shlex.split(
            cmd.replace("laam ", f"laam --uri {options.uri} --token {options.token} ")
        )


class PexpectLogfile:
    def __init__(self):
        self.line = ""

    def write(self, new_line):
        if not isinstance(new_line, str):
            new_line = str(new_line)
        lines = self.line + new_line

        # Print one full line at a time. A partial line is kept in memory.
        if "\n" in lines:
            last_ret = lines.rindex("\n")
            self.line = lines[last_ret + 1 :]
            lines = lines[:last_ret]
            for line in lines.split("\n"):
                sys.stdout.write(
                    f"{Color.grey.value}<serial> {Color.end.value}{line}\n"
                )
        else:
            self.line = lines

    def flush(self, force=False):
        if force and self.line:
            sys.stdout.write("\n")


def handle_test(options, session) -> int:
    config = Device.new(**yaml.safe_load(options.config.read()))

    print(f"{Color.green.value}Connect to serial{Color.end.value}")
    print(f" => {config.serial}")
    p = pexpect.spawn(
        shlex.join(replace_laam(options, f"laam serials connect {config.serial}")),
        codec_errors="replace",
        encoding="utf-8",
        timeout=100,
    )
    p.logfile_read = PexpectLogfile()

    if options.usbg_ms:
        print(f"\n{Color.green.value}Push USBG-MS file{Color.end.value}")
        subprocess.check_call(
            replace_laam(options, f"laam files push {options.usbg_ms.name} usbg.img")
        )
        subprocess.run(replace_laam(options, f"laam laacli usbg-ms off"))
        subprocess.check_call(replace_laam(options, f"laam laacli usbg-ms on usbg.img"))

    try:
        print(f"\n{Color.green.value}Reset the DUT{Color.end.value}")
        for cmd in config.power.reset:
            print(f" => {cmd}")
            subprocess.check_call(replace_laam(options, cmd))

        if config.interrupt:
            print(f"\n{Color.green.value}Interrupt bootloader{Color.end.value}")
            p.expect("Hit any key to stop autoboot:")
            p.sendline()
            print(
                f"\n{Color.green.value}Wait for prompt '{config.prompt}{Color.end.value}'"
            )
            p.expect(config.prompt)
        else:
            print(
                f"\n{Color.green.value}Wait for prompt '{config.prompt}{Color.end.value}'"
            )
            p.expect(config.prompt)
        print(f"\n{Color.green.value}Test USB support{Color.end.value}")
        p.sendline("usb start; usb info")
        ret = p.expect(["LAA USB Mass Storage Gadget", config.prompt])
        if ret != 0:
            print(f"{Color.red.value}!!! USB not working properly !!!{Color.end.value}")
        else:
            print(f"{Color.yellow.value}!!! USB ok !!!{Color.end.value}")
            p.expect(config.prompt)

        print(f"\n{Color.green.value}Test network support{Color.end.value}")
        p.sendline("dhcp; ping 198.18.0.1")
        ret = p.expect(["host 198.18.0.1 is alive", "ping failed"])
        if ret != 0:
            print(
                f"{Color.red.value}!!! Network not working properly !!!{Color.end.value}"
            )
        else:
            print(f"{Color.yellow.value}!!! Network ok !!!{Color.end.value}")
            p.expect(config.prompt)

    finally:
        print(f"\n{Color.green.value}Power off the DUT{Color.end.value}")
        for cmd in config.power.off:
            print(f" => {cmd}")
            subprocess.check_call(replace_laam(options, cmd))
        if options.usbg_ms:
            subprocess.run(replace_laam(options, f"laam laacli usbg-ms off"))

    return 0


def help_string():
    return "Enable attached DUT"
