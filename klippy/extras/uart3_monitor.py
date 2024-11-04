# File: klippy/extras/uart3_monitor.py

class Uart3Monitor:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu = self.printer.lookup_object('mcu')
        # Register for complete messages instead of bytes
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx msg=%s")
        
    def _handle_uart3_rx(self, params):
        # Get complete message
        message = params['msg']
        # Display message
        self.printer.get_reactor().process_message("uart3_rx: " + message)

def load_config(config):
    return Uart3Monitor(config)