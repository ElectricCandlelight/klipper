# Support for AnyCubic Mega Screen
#
# Copyright (C) 2024  Electric Candlelight
#
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging


class AnyCubicMegaScreen:
    def __init__(self, config):
        self.printer = config.get_printer()
        logging.warning(f"Printer: {self.printer}")
        self.mcu = self.printer.lookup_object('mcu')
        logging.warning(f"MCU: {self.mcu}")
        self.oid = self.mcu.create_oid()
        logging.warning(f"Created oid: {self.oid}")
        self.mcu.register_config_callback(self.build_config)
        self.uart3_send_cmd = None
        self.printer.register_event_handler("klippy:ready", self.handle_ready)

    def build_config(self):
        self.mcu.add_config_cmd("config_uart3 oid=%d" % (self.oid))
        logging.warning(f"Build oid: {self.oid}")
        cmd_queue = self.mcu.alloc_command_queue()
        self.uart3_send_cmd = self.mcu.lookup_query_command(
            "uart3_send oid=%c", "uart3_result oid=%c success=%c", oid=self.oid, cq=cmd_queue)


    def handle_ready(self):
        scmd = self.uart3_send_cmd.send
        params = scmd([self.oid])
        logging.warning(f"Params: {params}")

    def send_test(self):
        self.uart3_send_cmd.send([self.oid])


def load_config(config):
    return AnyCubicMegaScreen(config)
