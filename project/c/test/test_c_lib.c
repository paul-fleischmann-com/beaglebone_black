/*
 * c-lib Unit Tests (CI-kompatibel, keine Hardware erforderlich)
 *
 * Strategie: Hardware-Funktionen schlagen in CI kontrolliert fehl
 * (keine /dev/i2c-1, /dev/ttyS*, /sys/class/gpio vorhanden).
 * Die Fehlerpfade werden explizit verifiziert → Coverage-Daten entstehen.
 */
#include <assert.h>
#include <stdio.h>
#include <string.h>

#include "bme280.h"
#include "gpio.h"
#include "uart.h"

#define TEST(name) printf("  %-50s", #name); name(); printf("OK\n")

/* ── bme280 ──────────────────────────────────────────────────────────────── */

static void test_bme280_init_null_ptrs(void) {
    struct bme280_dev dev;
    memset(&dev, 0, sizeof(dev));
    /* NULL read/write/delay_us → null_ptr_check → BME280_E_NULL_PTR (< 0) */
    int8_t ret = bme280_init(&dev);
    assert(ret < 0);
}

static void test_bme280_get_sensor_data_null_output(void) {
    struct bme280_dev dev;
    memset(&dev, 0, sizeof(dev));
    /* NULL comp_data argument → BME280_E_NULL_PTR (< 0) */
    int8_t ret = bme280_get_sensor_data(7 /* BME280_ALL */, NULL, &dev);
    assert(ret < 0);
}

static void test_bme280_set_sensor_settings_null_settings(void) {
    struct bme280_dev dev;
    memset(&dev, 0, sizeof(dev));
    /* NULL settings pointer → BME280_E_NULL_PTR (< 0) */
    int8_t ret = bme280_set_sensor_settings(0, NULL, &dev);
    assert(ret < 0);
}

static void test_bme280_compensate_null_data(void) {
    struct bme280_uncomp_data uncomp;
    memset(&uncomp, 0, sizeof(uncomp));
    /* NULL comp_data → BME280_E_NULL_PTR (< 0) */
    int8_t ret = bme280_compensate_data(7, &uncomp, NULL, NULL);
    assert(ret < 0);
}

/* ── gpio ────────────────────────────────────────────────────────────────── */

static void test_gpio_export_fails_no_sysfs(void) {
    /* Kein /sys/class/gpio in CI → schlägt fehl */
    int ret = gpio_export(60);
    assert(ret < 0);
}

static void test_gpio_read_fails_no_sysfs(void) {
    int value = 0;
    int ret = gpio_read(60, &value);
    assert(ret < 0);
}

static void test_gpio_write_fails_no_sysfs(void) {
    int ret = gpio_write(60, 1);
    assert(ret < 0);
}

/* ── uart ────────────────────────────────────────────────────────────────── */

static void test_uart_open_fails_no_device(void) {
    uart_dev_t dev;
    memset(&dev, 0, sizeof(dev));
    /* Kein /dev/ttyS1 in CI */
    int ret = uart_open(&dev, "/dev/ttyS1", 115200);
    assert(ret < 0);
}

static void test_uart_close_invalid_fd(void) {
    uart_dev_t dev;
    memset(&dev, 0, sizeof(dev));
    dev.fd = -1;
    uart_close(&dev); /* darf nicht abstürzen */
}

/* ── main ────────────────────────────────────────────────────────────────── */

int main(void) {
    printf("c-lib Tests (CI-Modus: Hardware-Fehlerpfade)\n");
    printf("============================================================\n");

    TEST(test_bme280_init_null_ptrs);
    TEST(test_bme280_get_sensor_data_null_output);
    TEST(test_bme280_set_sensor_settings_null_settings);
    TEST(test_bme280_compensate_null_data);
    TEST(test_gpio_export_fails_no_sysfs);
    TEST(test_gpio_read_fails_no_sysfs);
    TEST(test_gpio_write_fails_no_sysfs);
    TEST(test_uart_open_fails_no_device);
    TEST(test_uart_close_invalid_fd);

    printf("============================================================\n");
    printf("Alle Tests bestanden.\n");
    return 0;
}
