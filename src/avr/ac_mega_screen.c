#include <avr/interrupt.h>
#include "command.h"  // sendf
#include "sched.h"    // DECL_INIT
#include "autoconf.h" // CONFIG_CLOCK_FREQ

#define UART3_BAUD 115200
#define UART_BUF_SIZE 64
#define LED_PIN PB7 

void uart3_init(void)
{
    DDRB |= (1 << LED_PIN); 
    PORTB ^= (1 << LED_PIN); 
}


DECL_COMMAND(uart3_init, "config_uart3 oid=%c");
