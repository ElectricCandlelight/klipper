#include <avr/interrupt.h>
#include "command.h"  // sendf
#include "sched.h"    // DECL_INIT
#include "autoconf.h" // CONFIG_CLOCK_FREQ

#define UART3_BAUD 115200
#define UART_BUF_SIZE 64

void uart3_init(void)
{
    uint32_t cm = 16;
    uint32_t div = DIV_ROUND_CLOSEST(CONFIG_CLOCK_FREQ, cm * UART3_BAUD) - 1UL;
    UBRR3H = div >> 8;
    UBRR3L = div;
    UCSR3B = (1 << RXEN3) | (1 << TXEN3) | (1 << RXCIE3);
    UCSR3C = (1 << UCSZ31) | (1 << UCSZ30);
    sendf("UART3 initialized with baud rate %u", UART3_BAUD);
}
DECL_INIT(uart3_init);

static char uart_buf[UART_BUF_SIZE];
static uint8_t buf_pos;

// Interrupt handler for UART3 receive
ISR(USART3_RX_vect) 
{
    uint8_t data = UDR3;
    
    if (buf_pos < UART_BUF_SIZE-1) {
        uart_buf[buf_pos++] = data;
    }
    
    if (data == '\n' || buf_pos >= UART_BUF_SIZE-1) {
        uart_buf[buf_pos] = '\0';
        sendf("uart3_rx msg=%s", uart_buf);
        buf_pos = 0;
    }
}

DECL_CONSTANT_STR("RESERVE_PINS_uart3", "PJ0,PJ1");

void command_uart3_test_custom(uint32_t *args) {
    uint8_t oid = args[0];
    sendf("uart3_test_custom command received with oid=%d", oid);
    sendf("uart3_rx msg=%s", "UART3 test message with custom command"); 
}
DECL_COMMAND(command_uart3_test_custom, "uart3_test_custom oid=%c");