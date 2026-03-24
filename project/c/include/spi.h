#ifndef SPI_H
#define SPI_H
#include <stdint.h>
#include <stddef.h>
typedef struct { int fd; char device[64]; uint32_t speed; uint8_t mode,bits; } spi_dev_t;
int  spi_open(spi_dev_t *dev, const char *device, uint32_t speed, uint8_t mode);
int  spi_transfer(spi_dev_t *dev, const uint8_t *tx, uint8_t *rx, size_t len);
void spi_close(spi_dev_t *dev);
#endif
