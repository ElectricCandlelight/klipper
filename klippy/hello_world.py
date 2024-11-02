# Basic hello world command for Klipper
#
# Copyright (C) 2023  <Your Name>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

class HelloWorld:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        # Register HELLO command
        self.gcode.register_command('HELLO', self.cmd_HELLO, desc="Sends HELLO command to MCU")
        # Setup MCU
        self.mcu = self.printer.lookup_object('mcu')

    def cmd_HELLO(self, gcmd):
        # Send command to MCU
        params = self.mcu.lookup_query_command(
            "hello_world",
            "hello_response value=%s"
        ).send()
        # Respond to user
        gcmd.respond_info(params['value'])

def load_config(config):
    return HelloWorld(config)