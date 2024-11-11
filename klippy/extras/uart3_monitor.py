# klippy/extras/uart3_monitor.py
import logging

class Uart3Monitor:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu = self.printer.lookup_object('mcu')
        self.oid = self.mcu.create_oid()
        # Register configuration callback
        self.mcu.register_config_callback(self.build_config)
        self.cmd_uart3_write = None
        # Register response handler
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx msg=%s")
        logging.info("UART3Monitor initialized")
        
    def build_config(self):
        self.mcu.add_config_cmd("config_uart3 oid=%d" % (self.oid,))
        cmd_queue = self.mcu.alloc_command_queue()
        self.cmd_uart3_write = self.mcu.lookup_command(
            "uart3_write oid=%c data=%*s", cq=cmd_queue)
        
    def send_uart3(self, data):
        """Send data to UART3"""
        if not data.endswith('\n'):
            data += '\n'
        self.cmd_uart3_write.send([self.oid, len(data), data])
        
    def _handle_uart3_rx(self, params):
        """Handle received UART3 data"""
        message = params['msg'].decode('utf-8').strip()
        logging.info("UART3 received: %s", message)
        
        # Handle specific messages
        match message:
            case "A0":
                temp_str = "A0V 132\r\n"
                self.send_uart3(temp_str)
            case "A1":
                logging.info("Target extruder temperature")
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
                logging.info("Unknown command: %s", message)

def load_config(config):
    return Uart3Monitor(config)