// UART3 monitoring code for Anycubic TFT
//
// Copyright (C) 2024 <Your Name>
// This file may be distributed under the terms of the GNU GPLv3 license.

#include <avr/interrupt.h>
#include <avr/io.h>
#include "command.h"
#include "sched.h"
#include "autoconf.h"

#define UART3_BAUD 115200
#define UART_BUF_SIZE 64

// State structure
struct uart3_s {
    uint8_t oid;
    char receive_buf[UART_BUF_SIZE];
    uint8_t receive_pos;
};

static struct uart3_s uart3_state;

// Config command registration
void
config_uart3(uint32_t *args)
{
    struct uart3_s *uart3 = &uart3_state;
    uart3->oid = args[0];
    uart3->receive_pos = 0;
}
DECL_COMMAND(config_uart3, "config_uart3 oid=%c");

// Initialize UART3
void
uart3_init(void)
{
    // Calculate baud rate divisor for 16MHz clock
    uint32_t cm = 16;
    uint32_t div = DIV_ROUND_CLOSEST(CONFIG_CLOCK_FREQ, cm * UART3_BAUD) - 1UL;
    
    // Set baud rate registers
    UBRR3H = div >> 8;
    UBRR3L = div;
    
    // Enable receiver, transmitter and receive interrupt
    UCSR3B = (1 << RXEN3) | (1 << TXEN3) | (1 << RXCIE3);
    
    // Set frame format: 8 data bits, 1 stop bit, no parity
    UCSR3C = (1 << UCSZ31) | (1 << UCSZ30);
}
DECL_INIT(uart3_init);

// Write command handler
void
command_uart3_write(uint32_t *args)
{
    uint8_t oid = args[0];
    uint8_t data_len = args[1];
    uint8_t *data = (uint8_t*)args[2];
    
    // Send each byte
    for (uint8_t i = 0; i < data_len; i++) {
        while (!(UCSR3A & (1<<UDRE3))); // Wait for empty transmit buffer
        UDR3 = data[i];
    }
}
DECL_COMMAND(command_uart3_write, "uart3_write oid=%c data=%*s");

// UART3 receive interrupt handler
ISR(USART3_RX_vect)
{
    struct uart3_s *uart3 = &uart3_state;
    uint8_t data = UDR3;
    
    if (uart3->receive_pos < UART_BUF_SIZE - 1) {
        uart3->receive_buf[uart3->receive_pos++] = data;
        
        // Check for end of message (newline or buffer full)
        if (data == '\n' || uart3->receive_pos >= UART_BUF_SIZE - 1) {
            uart3->receive_buf[uart3->receive_pos] = '\0';
            sendf("uart3_rx msg=%s", uart3->receive_buf);
            uart3->receive_pos = 0;
        }
    }
}

// Reserve UART3 pins
DECL_CONSTANT_STR("RESERVE_PINS_uart3", "PJ0,PJ1");