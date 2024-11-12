# UART3 monitoring for Klipper
#
# Copyright (C) 2024 <Your Name>
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging


class Uart3Monitor:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu = self.printer.lookup_object('mcu')
        self.oid = self.mcu.create_oid()
        cmd_queue = self.mcu.alloc_command_queue()
        self.cmd_test = self.mcu.lookup_command(
            "uart3_test oid=%c",
            cq=cmd_queue
        )
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx")
        logging.warning("UART3Monitor initialized")

    def send_test(self):
        self.cmd_test.send([self.oid])

    def _handle_uart3_rx(self, params):
        message = params['msg'].decode('utf-8').strip()
        # Log to klippy.log
        match message:
            case "A0":
                logging.warning("Extruder temperature")
                self.send_test()
            case "A1":
                logging.warning("Target extruder temperature")
            case "A2":
                logging.warning("Bed temperature")
            case "A3":
                logging.warning("Target bed temperature")
            case "A4":
                logging.warning("Fan speed")
            case "A5":
                logging.warning("Co-ordinates")
            case "A6":
                logging.warning("Print progress")
            case "A7":
                logging.warning("Print time")
            case "A8":
                logging.warning("Print list")
            case "A9":
                logging.warning("Pause print")
            case "A10":
                logging.warning("Resume print")
            case "A11":
                logging.warning("Cancel print")
            case "A12":
                logging.warning("Emergency stop")
            case "A13":
                logging.warning("Select file")
            case "A14":
                logging.warning("Reprint")
            case "A15":
                logging.warning("Breakpoint resume")
            case "A16":
                logging.warning("Set extruder temperature")
            case "A17":
                logging.warning("Set bed temperature")
            case "A18":
                logging.warning("Set fan speed")
            case "A19":
                logging.warning("Turn off motors")
            case "A20":
                logging.warning("Set print speed")
            case "A21":
                logging.warning("Reset")
            case "A22":
                logging.warning("Move axis")
            case "A23":
                logging.warning("Preheat PLA")
            case "A24":
                logging.warning("Preheat ABS")
            case "A25":
                logging.warning("Cooling")
            case "A26":
                logging.warning("Refresh print list")
            case _:
                logging.warning("Unknown command: %s", message)
        # Display in Mainsail console correctly


def load_config(config):
    return Uart3Monitor(config)
