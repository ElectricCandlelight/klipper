// src/avr/ac_tft.c
#include <avr/interrupt.h>
#include <avr/io.h>
#include "command.h"
#include "sched.h"
#include "basecmd.h"
#include "internal.h" // For timer_read_time
#include "board/misc.h" // For timer_from_us

#define UART3_BAUD 115200
#define UART_BUF_SIZE 64

struct uart3_s {
    uint8_t oid;
    char receive_buf[UART_BUF_SIZE];
    uint8_t receive_pos;
    uint32_t last_activity;
};

static struct uart3_s uart3_state;

void
command_config_uart3(uint32_t *args)
{
    struct uart3_s *uart3 = &uart3_state;
    uart3->oid = args[0];
    uart3->receive_pos = 0;
    uart3->last_activity = timer_read_time();
}
DECL_COMMAND(command_config_uart3, "config_uart3 oid=%c");

void
command_uart3_write(uint32_t *args)
{
    struct uart3_s *uart3 = &uart3_state;
    uint8_t data_len = args[1];
    uint8_t *data = command_decode_ptr(args[2]);
    
    for (uint8_t i = 0; i < data_len; i++) {
        uint32_t timeout = timer_read_time() + timer_from_us(5000);
        while (!(UCSR3A & (1<<UDRE3))) {
            if (timer_read_time() > timeout)
                shutdown("UART3 write timeout");
        }
        UDR3 = data[i];
    }
    uart3->last_activity = timer_read_time();
}
DECL_COMMAND(command_uart3_write, "uart3_write oid=%c data=%*s");

void
uart3_init(void)
{
    // Calculate baud rate divisor
    #define CPU_FREQ 16000000
    uint32_t div = CPU_FREQ / (16 * UART3_BAUD) - 1;
    UBRR3H = div >> 8;
    UBRR3L = div;
    // Enable RX, TX and RX interrupt
    UCSR3B = (1 << RXEN3) | (1 << TXEN3) | (1 << RXCIE3);
    // Set 8N1
    UCSR3C = (1 << UCSZ31) | (1 << UCSZ30);
}
DECL_INIT(uart3_init);

// UART3 receive interrupt
ISR(USART3_RX_vect)
{
    uint8_t data = UDR3;
    struct uart3_s *uart3 = &uart3_state;
    
    if (uart3->receive_pos < UART_BUF_SIZE - 1) {
        uart3->receive_buf[uart3->receive_pos++] = data;
        uart3->last_activity = timer_read_time();
        
        if (data == '\n' || uart3->receive_pos >= UART_BUF_SIZE - 1) {
            uart3->receive_buf[uart3->receive_pos] = '\0';
            sendf("uart3_rx msg=%s", uart3->receive_buf);
            uart3->receive_pos = 0;
        }
    }
}

// Reserve UART3 pins
DECL_CONSTANT_STR("RESERVE_PINS_uart3", "PJ0,PJ1");