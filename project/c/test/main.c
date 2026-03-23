#include "bme280.h"
#include <stdio.h>
#include <assert.h>
#include <string.h>


#define TEST(name) do { \
    printf("  %-50s", #name); \
    int _ret = (name()); \
    assert(_ret == 0); \
    printf("OK\n"); \
} while(0)


static int test_bme280_init_no_hardware(void);

int main(void) {
    printf("BME280 C dummy binary running\n");
    printf("c-lib Tests (CI-Modus: Hardware-Fehlerpfade)\n");
    printf("============================================================\n");
    TEST(test_bme280_init_no_hardware);
    printf("============================================================\n");
    printf("Alle Tests bestanden.\n");
    return 0;
}

static int test_bme280_init_no_hardware(void) {
    bme280_dev_t dev;
    memset(&dev, 0, sizeof(dev));
    /* Kein /dev/i2c-1 in CI → open() schlägt fehl → Rückgabe < 0 */
    int ret = bme280_init(&dev);
    return (ret < 0) ? 0 : -1;
}