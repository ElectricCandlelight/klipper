# UART3 monitoring for Klipper
#
# Copyright (C) 2024 <Your Name>
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging

class Uart3Monitor:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu = self.printer.lookup_object('mcu')
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx msg=%s")
        # Get base logger used by Klipper
        print("UART3Monitor initialized") # Debug print
        logging.warning("Starting UART3 monitor") # Log to klippy.log
        
    def _handle_uart3_rx(self, params):
            logging.warning("new message received") # Debug print
            message = params['msg'].decode('utf-8').strip()
            # Log to klippy.log
            logging.warning("UART3: %s", message)
            # Display in Mainsail console using reactor

def load_config(config):
    return Uart3Monitor(config)