# Support for AnyCubic Mega Screen
#
# Copyright (C) 2024  Electric Candlelight 
#
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging

class AnyCubicMegaScreen:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu = self.printer.lookup_object('mcu')
        self.oid = self.mcu.create_oid()
        self.mcu.register_config_callback(self.build_config)
        self.uart3_send_cmd = None
        self.printer.register_event_handler("klippy:connect", self.send_data)

def load_config(config):
    return AnyCubicMegaScreen(config)