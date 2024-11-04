# File: klippy/extras/uart3_monitor.py

class Uart3Monitor:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu = self.printer.lookup_object('mcu')
        self.mcu.register_response(self._handle_uart3_rx, "uart3_rx byte=%c")
        self.buffer = []
        
    def _handle_uart3_rx(self, params):
        byte = params['byte']
        
        # Convert numeric byte value to character
        if byte == 13:  # CR
            return
        if byte == 10:  # LF
            # Process complete message
            message = ''.join([chr(x) for x in self.buffer])
            self.printer.get_reactor().process_message("uart3_rx: " + message)
            self.buffer = []
            return
            
        # Add byte to buffer
        self.buffer.append(byte)

def load_config(config):
    return Uart3Monitor(config)