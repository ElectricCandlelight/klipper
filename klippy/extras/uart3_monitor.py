class Uart3Monitor:
    def __init__(self, config):
        self.printer = config.get_printer()
        # Register handler for uart3_rx messages
        self.mcu = self.printer.lookup_object('mcu')
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx byte=%c")
        
    def _handle_uart3_rx(self, params):
        # Get byte from response
        byte = params['byte'].decode('utf-8')
        # Log to console
        self.printer.get_reactor().process_message("uart3_rx: " + byte)

def load_config(config):
    return Uart3Monitor(config)