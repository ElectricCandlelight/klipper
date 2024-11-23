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
    // Validate length
    if (len > 32) len = 32;
    if (!bytes) {
        output("debug_msg=null");
        return;
    }
    
    output("debug_msg_len=%u", len);
    for(int i = 0; i < len; i++) {
        // Cast to uint8_t to ensure proper byte range
        uint8_t byte = bytes[i];
        output("debug_byte=0x%02x", byte);
    }
}

void test_uart_send(const char *str) {
    if (!str) return;
    
    while (*str) {
        while (!(UCSR3A & (1 << UDRE3)));
        UDR3 = *str;
        // Cast to uint8_t for proper byte display
        output("uart_byte=0x%02x", (uint8_t)*str);
        str++;
    }
}

void command_uart3_tx(uint32_t *args) {
    PORTB ^= (1 << PB7);

    uint8_t *bytes = (uint8_t*)command_decode_ptr(args[1]);
    debug_message(bytes, 32);
    test_uart_send("A1V 60\r\n");
}

DECL_COMMAND(command_uart3_tx, "uart3_write oid=%c data=%*s");