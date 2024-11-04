# UART3 monitoring for Klipper
#
# Copyright (C) 2024 <Your Name>
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging

class Uart3Monitor:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu = self.printer.lookup_object('mcu')
        # Register response handler for uart3_rx messages
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx msg=%s")
        # Set up logging
        self.gcode = self.printer.lookup_object('gcode')
        
    def _handle_uart3_rx(self, params):
        # Convert bytes to string and strip CR/LF
        message = params['msg'].strip()
        # Log using Klipper's logging system
        logging.info("UART3: %s", message)
        # Also display in console
        self.gcode.respond_info("UART3: %s" % message)

def load_config(config):
    return Uart3Monitor(config)