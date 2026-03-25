/*
 * bbb_smoke.c — C smoke test binary for BeagleBone Black deployment.
 *
 * Only tests BME280 null-pointer behaviour (pure software logic, no hardware
 * access).  Does NOT use assert() so it never aborts — exits 0 on success,
 * 1 on failure.  GPIO / UART sysfs tests live in test_c_lib.c which is for
 * CI-only environments without real hardware.
 */
#include "bme280.h"
#include <stdio.h>
#include <string.h>

int main(void) {
    int failed = 0;

    printf("C BME280 smoke tests\n");
    printf("============================================================\n");

    struct bme280_dev dev;
    struct bme280_uncomp_data uncomp;

    memset(&dev, 0, sizeof(dev));
    if (bme280_init(&dev) >= 0) {
        printf("  FAIL test_bme280_init_null_ptrs\n");
        failed++;
    } else {
        printf("  PASS test_bme280_init_null_ptrs\n");
    }

    memset(&dev, 0, sizeof(dev));
    if (bme280_get_sensor_data(7, NULL, &dev) >= 0) {
        printf("  FAIL test_bme280_get_sensor_data_null_output\n");
        failed++;
    } else {
        printf("  PASS test_bme280_get_sensor_data_null_output\n");
    }

    memset(&dev, 0, sizeof(dev));
    if (bme280_set_sensor_settings(0, NULL, &dev) >= 0) {
        printf("  FAIL test_bme280_set_sensor_settings_null_settings\n");
        failed++;
    } else {
        printf("  PASS test_bme280_set_sensor_settings_null_settings\n");
    }

    memset(&uncomp, 0, sizeof(uncomp));
    if (bme280_compensate_data(7, &uncomp, NULL, NULL) >= 0) {
        printf("  FAIL test_bme280_compensate_null_data\n");
        failed++;
    } else {
        printf("  PASS test_bme280_compensate_null_data\n");
    }

    printf("============================================================\n");
    if (failed == 0) {
        printf("Alle Tests bestanden.\n");
        return 0;
    }
    printf("%d Test(s) fehlgeschlagen.\n", failed);
    return 1;
}
