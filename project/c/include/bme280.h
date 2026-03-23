#ifndef BME280_H
#define BME280_H
#include <stdint.h>
#define BME280_I2C_BUS  "/dev/i2c-1"
#define BME280_ADDR     0x76
#define SEA_LEVEL_PA    101325.0
typedef struct {
    uint16_t T1; int16_t T2,T3;
    uint16_t P1; int16_t P2,P3,P4,P5,P6,P7,P8,P9;
    uint8_t H1,H3; int16_t H2,H4,H5; int8_t H6;
} bme280_calib_t;
typedef struct {
    double temperature, humidity, pressure, altitude;
    uint64_t timestamp;
} bme280_data_t;
typedef struct { int fd; bme280_calib_t calib; int32_t t_fine; } bme280_dev_t;
int  bme280_init(bme280_dev_t *dev);
int  bme280_read(bme280_dev_t *dev, bme280_data_t *out);
void bme280_close(bme280_dev_t *dev);
#endif
