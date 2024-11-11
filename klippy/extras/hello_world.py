# Basic hello world command for Klipper
#
# Copyright (C) 2023  <Your Name>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging

class HelloWorld:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.oid = self.mcu.create_oid()
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command('HELLO', self.cmd_HELLO, desc="Sends HELLO command to MCU")
        self.mcu = self.printer.lookup_object('mcu')
        logging.warning("Starting hello") # Log to klippy.log
        
    def cmd_HELLO(self, gcmd):
        
        params = self.mcu.lookup_query_command(
            "hello oid=%c",
            "hello_response oid=%c msg=%s",
            oid=self.oid
        ).send([self.oid])
        # Convert bytes to string before responding
        msg = params['msg'].decode('utf-8')
        gcmd.respond_info(msg)
        logging.warning("Starting hello %s", msg) # Log to klippy.log

def load_config(config):
    return HelloWorld(config)