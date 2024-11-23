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
        self.uart3_write_cmd = None
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx")

    def build_config(self):
        self.mcu.add_config_cmd("config_uart3 oid=%d" % (self.oid))
        logging.warning(f"Build oid: {self.oid}")
        cmd_queue = self.mcu.alloc_command_queue()
        self.uart3_send_cmd = self.mcu.lookup_command(
            "uart3_send oid=%c", cq=cmd_queue)
        self.uart3_write_cmd = self.mcu.lookup_command(
            "uart3_write oid=%c data=%*s", cq=cmd_queue)
        
    def _handle_uart3_rx(self, params):
        message = params['msg'].decode('utf-8').strip()
        # Log to klippy.log
        match message:
            case "A0":
                logging.warning("Extruder temperature")
            case "A1":
                logging.warning("Target extruder temperature")
            case "A2":
                logging.warning("Bed temperature")
                logging.warning(f"Sending message: {message}")  # Debug log
                self.uart3_write_cmd.send([self.oid, b"A2V 60\r\n"])
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


    def handle_ready(self):
        logging.warning("toggle")
        logging.warning(f"Send oid: {self.oid}")
        scmd = self.uart3_send_cmd.send
        scmd([self.oid])

    def send_test(self):
        self.uart3_send_cmd.send([self.oid])


def load_config(config):
    return AnyCubicMegaScreen(config)
