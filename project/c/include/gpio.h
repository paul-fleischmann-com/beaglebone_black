#ifndef GPIO_H
#define GPIO_H
#include <stdint.h>
typedef enum { GPIO_INPUT=0, GPIO_OUTPUT=1 } gpio_direction_t;
int gpio_export(uint32_t pin);
int gpio_unexport(uint32_t pin);
int gpio_set_direction(uint32_t pin, gpio_direction_t dir);
int gpio_read(uint32_t pin, int *value);
int gpio_write(uint32_t pin, int value);
#endif
