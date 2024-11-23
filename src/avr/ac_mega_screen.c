#include <avr/interrupt.h>
#include "command.h"  // sendf
#include "sched.h"    // DECL_INIT
#include "autoconf.h" // CONFIG_CLOCK_FREQ
#include <avr/io.h>
#include <string.h>

#define UART3_BAUD 115200
#define UART_BUF_SIZE 64

void uart3_init(void)
{
    DDRB |= (1 << PB7);
    PORTB &= ~(1 << PB7);
    uint32_t cm = 16;
    uint32_t div = DIV_ROUND_CLOSEST(CONFIG_CLOCK_FREQ, cm * UART3_BAUD) - 1UL;
    UBRR3H = div >> 8;
    UBRR3L = div;
    // Enable transmitter and receiver
    UCSR3B = (1 << RXEN3) | (1 << TXEN3) | (1 << RXCIE3);
    // Set 8N1 frame format
    UCSR3C = (1 << UCSZ31) | (1 << UCSZ30);

    const char *str = "A0V 123\r\n";
    while (*str)
    {
        while (!(UCSR3A & (1 << UDRE3)))
            ;          // Wait for the transmit buffer to be empty
        UDR3 = *str++; // Send the next character
    }
}

DECL_COMMAND(uart3_init, "config_uart3 oid=%c");

static char uart_buf[UART_BUF_SIZE];
static uint8_t buf_pos;

ISR(USART3_RX_vect)
{
    uint8_t data = UDR3;

    if (buf_pos < UART_BUF_SIZE - 1)
    {
        uart_buf[buf_pos++] = data;
    }

    if (data == '\n' || buf_pos >= UART_BUF_SIZE - 1)
    {
        uart_buf[buf_pos] = '\0';
        sendf("uart3_rx msg=%s", uart_buf);
        buf_pos = 0;
    }
}

void debug_message(uint8_t *bytes, int len) {
    if (len > 32) len = 32;
    if (!bytes) {
        output("debug=0");
        return;
    }
    
    output("debug_len=%u", len);
    for(int i = 0; i < len; i++) {
        output("debug=%u", (uint8_t)bytes[i]);
    }
}

void test_uart_send(const char *str) {
    if (!str) return;
    
    while (*str) {
        while (!(UCSR3A & (1 << UDRE3)));
        UDR3 = *str;
        output("byte=%u", (uint8_t)*str);
        str++;
    }
}

void command_uart3_tx(uint32_t *args)
{
    PORTB ^= (1 << PB7);

    // First arg (args[0]) is oid
    uint8_t oid = args[0];
    
    // Second arg (args[1]) is data pointer
    uint8_t *data = (uint8_t*)command_decode_ptr(args[1]);
    
    // Debug info
    output("oid=%u", oid);
    
    // Send bytes via UART
    for(uint8_t i = 0; data[i] && i < 32; i++) {
        while (!(UCSR3A & (1 << UDRE3)));
        UDR3 = data[i];
        output("tx_byte=%u", data[i]);
    }

    // Add line ending
    while (!(UCSR3A & (1 << UDRE3)));
    UDR3 = '\r';
    while (!(UCSR3A & (1 << UDRE3)));
    UDR3 = '\n';
}

DECL_COMMAND(command_uart3_tx, "uart3_write oid=%c data=%*s");