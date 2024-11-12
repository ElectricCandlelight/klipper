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
        self.mcu.register_config_callback(self.build_config)
        logging.warning("UART3Monitor initialized")

    def build_config(self):
        logging.debug("Adding uart3_test command to config")
        self.mcu.add_config_cmd("uart3_test oid=%c" % self.oid)

    def send_test(self):
        logging.debug(f"Sending test command with oid: {self.oid}")
        self.cmd_test.send([self.oid])

    def _handle_uart3_rx(self, params):
        message = params['msg'].decode('utf-8').strip()
        # Log to klippy.log
        logging.debug(f"Received UART3 message: {message}")
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

def load_config(config):
    return Uart3Monitor(config)