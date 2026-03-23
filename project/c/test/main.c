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

static void run_all(void) {
    printf("c-lib Tests (CI-Modus: Hardware-Fehlerpfade)\n");
    printf("============================================================\n");
    TEST(test_bme280_init_no_hardware);
    printf("============================================================\n");
    printf("Alle Tests bestanden.\n");
}

int main(int argc, char *argv[]) {
    printf("BME280 C dummy binary running\n");
    if (argc >= 3 && strcmp(argv[1], "--test") == 0) {
        const char *name = argv[2];
        if (strcmp(name, "test_bme280_init_no_hardware") == 0)
            TEST(test_bme280_init_no_hardware);
        else {
            fprintf(stderr, "Unknown test: %s\n", name);
            return 1;
        }
    } else {
        run_all();
    }
    return 0;
}

static int test_bme280_init_no_hardware(void) {
    bme280_dev_t dev;
    memset(&dev, 0, sizeof(dev));
    /* Kein /dev/i2c-1 in CI → open() schlägt fehl → Rückgabe ist -1 */
    int ret = bme280_init(&dev);
    return (ret == -1) ? 0 : -1;
}