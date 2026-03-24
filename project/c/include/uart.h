#ifndef UART_H
#define UART_H
#include <stdint.h>
#include <stddef.h>
typedef struct { int fd; char port[64]; uint32_t baud; } uart_dev_t;
int  uart_open(uart_dev_t *dev, const char *port, uint32_t baud);
int  uart_write(uart_dev_t *dev, const uint8_t *buf, size_t len);
int  uart_read(uart_dev_t *dev, uint8_t *buf, size_t len, int timeout_ms);
int  uart_flush(uart_dev_t *dev);
void uart_close(uart_dev_t *dev);
#endif
