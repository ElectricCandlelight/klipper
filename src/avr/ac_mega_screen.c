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
