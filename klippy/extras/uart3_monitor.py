# File: klippy/extras/uart3_monitor.py

class Uart3Monitor:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu = self.printer.lookup_object('mcu')
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx msg=%s")
        # Get correct logger instance
        self.logger = config.get_printer().get_start_args()['log_file']
        
    def _handle_uart3_rx(self, params):
        # Convert bytes to string and strip CR/LF
        message = params['msg'].decode('utf-8').strip()
        # Log to klippy.log
        print("UART3:", message, file=self.logger)
        # Optional console display
        self.printer.get_reactor().process_message("uart3_rx: " + message)

def load_config(config):
    return Uart3Monitor(config)