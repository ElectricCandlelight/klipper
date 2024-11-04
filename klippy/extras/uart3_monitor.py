# UART3 monitoring for Klipper
#
# Copyright (C) 2024 <Your Name>
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging

class Uart3Monitor:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu = self.printer.lookup_object('mcu')
        # Simple response registration - no OID needed
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx")
        logging.warning("UART3Monitor initialized")
        
    def _handle_uart3_rx(self, params):
        logging.warning("Made it to _handle_uart3_rx")
        message = params['msg'].decode('utf-8').strip()
        # Log to klippy.log
        logging.warning("UART3 received: %s", message)
        # Display in Mainsail console correctly

def load_config(config):
    return Uart3Monitor(config)