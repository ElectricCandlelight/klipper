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
        self.logger = logging.getLogger('klippy')
        print("UART3Monitor initialized") # Debug print
        
    def _handle_uart3_rx(self, params):
        print("Handle UART3 called with:", params) # Debug print
        try:
            message = params['msg'].decode('utf-8').strip()
            # Log to klippy.log
            self.logger.info("UART3: %s", message)
            # Display in Mainsail console using reactor
            self.printer.get_reactor().process_message("UART3: " + message)
        except Exception as e:
            print("Error in handle_uart3:", str(e)) # Debug print
            self.logger.error("UART3 error: %s", str(e))

def load_config(config):
    return Uart3Monitor(config)