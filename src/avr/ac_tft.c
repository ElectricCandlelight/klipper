// UART3 monitoring code
//
// Copyright (C) 2024 <Your Name>
// This file may be distributed under the terms of the GNU GPLv3 license.

#include <avr/interrupt.h>
#include "command.h"  // sendf
#include "sched.h"    // DECL_INIT
#include "autoconf.h" // CONFIG_CLOCK_FREQ

#define UART3_BAUD 115200

void
uart3_init(void)
{
    // Calculate baud rate divisor
    uint32_t cm = 16;
    uint32_t div = DIV_ROUND_CLOSEST(CONFIG_CLOCK_FREQ, cm * UART3_BAUD) - 1UL;
    UBRR3H = div >> 8;
    UBRR3L = div;
    // Enable transmitter and receiver
    UCSR3B = (1 << RXEN3) | (1 << TXEN3) | (1 << RXCIE3);
    // Set 8N1 frame format
    UCSR3C = (1 << UCSZ31) | (1 << UCSZ30);
}
DECL_INIT(uart3_init);

// Interrupt handler for UART3 receive
ISR(USART3_RX_vect) 
{
    // Read the received byte
    uint8_t data = UDR3;
    sendf("uart3_rx byte=%c", data);
}

// Register uart3_rx response
DECL_CONSTANT_STR("RESERVE_PINS_uart3", "PJ0,PJ1");