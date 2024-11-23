#include <avr/interrupt.h>
#include "command.h"  // sendf
#include "sched.h"    // DECL_INIT
#include "autoconf.h" // CONFIG_CLOCK_FREQ
#include <avr/io.h>

#define UART3_BAUD 115200
#define UART_BUF_SIZE 64

void uart3_init(void)
{
    DDRB |= (1 << PB7); 
    PORTB &= ~(1 << PB7);
}

DECL_COMMAND(uart3_init, "config_uart3 oid=%c");

void uart3_send(uint8_t *args)
{
    uint8_t oid = args[0];
    PORTB |= (1 << PB7);
    sendf("uart3_result oid=%c success=%c", oid, 1);
}

DECL_COMMAND(uart3_send, "uart3_send oid=%c");
