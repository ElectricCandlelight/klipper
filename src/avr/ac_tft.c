// UART3 monitoring code
//
// Copyright (C) 2024 <Your Name>
// This file may be distributed under the terms of the GNU GPLv3 license.

#include <avr/interrupt.h>
#include "command.h"  // sendf
#include "sched.h"    // DECL_INIT
#include "autoconf.h" // CONFIG_CLOCK_FREQ

#define UART3_BAUD 115200
#define UART_BUF_SIZE 64

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

// Register uart3_rx response
DECL_CONSTANT_STR("RESERVE_PINS_uart3", "PJ0,PJ1");

void command_uart3_write(uint32_t *args)
{
    uint8_t oid = args[0];
    uint8_t data_len = args[1];
    uint8_t *data = command_decode_ptr(args[2]);
    
    // Write data to UART3
    for (int i = 0; i < data_len; i++) {
        while (!(UCSR3A & (1<<UDRE3))); // Wait for empty transmit buffer
        UDR3 = data[i];
    }
}
DECL_COMMAND(command_uart3_write, "uart3_write oid=%c data=%*s");