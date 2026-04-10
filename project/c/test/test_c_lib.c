/*
 * c-lib Unit Tests mit Unity Framework
 * CI-kompatibel — keine Hardware erforderlich.
 * Strategie: Hardware-Funktionen schlagen in CI kontrolliert fehl
 * (kein /dev/i2c-1, /dev/ttyS*, /sys/class/gpio vorhanden).
 */
#include "unity.h"
#include <string.h>
#include "bme280.h"
#include "gpio.h"
#include "uart.h"

void setUp(void)    {}
void tearDown(void) {}

/* ── bme280 ──────────────────────────────────────────────────────────── */

void test_bme280_init_null_ptrs(void) {
    struct bme280_dev dev;
    memset(&dev, 0, sizeof(dev));
    /* NULL read/write/delay_us → null_ptr_check → BME280_E_NULL_PTR */
    int8_t ret = bme280_init(&dev);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "Expected error for null function pointers");
}

void test_bme280_get_sensor_data_null_output(void) {
    struct bme280_dev dev;
    memset(&dev, 0, sizeof(dev));
    int8_t ret = bme280_get_sensor_data(7 /* BME280_ALL */, NULL, &dev);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "Expected error for NULL comp_data");
}

void test_bme280_set_sensor_settings_null_settings(void) {
    struct bme280_dev dev;
    memset(&dev, 0, sizeof(dev));
    int8_t ret = bme280_set_sensor_settings(0, NULL, &dev);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "Expected error for NULL settings");
}

void test_bme280_compensate_null_data(void) {
    struct bme280_uncomp_data uncomp;
    memset(&uncomp, 0, sizeof(uncomp));
    int8_t ret = bme280_compensate_data(7, &uncomp, NULL, NULL);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "Expected error for NULL comp_data and calib_data");
}

/* ── gpio ─────────────────────────────────────────────────────────────── */

void test_gpio_export_fails_no_sysfs(void) {
    int ret = gpio_export(60);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "gpio_export should fail without /sys/class/gpio");
}

void test_gpio_read_fails_no_sysfs(void) {
    int value = 0;
    int ret = gpio_read(60, &value);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "gpio_read should fail without /sys/class/gpio");
}

void test_gpio_write_fails_no_sysfs(void) {
    int ret = gpio_write(60, 1);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "gpio_write should fail without /sys/class/gpio");
}

/* ── uart ─────────────────────────────────────────────────────────────── */

void test_uart_open_fails_no_device(void) {
    uart_dev_t dev;
    memset(&dev, 0, sizeof(dev));
    int ret = uart_open(&dev, "/dev/ttyS1", 115200);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "uart_open should fail without /dev/ttyS1");
}

void test_uart_close_invalid_fd(void) {
    uart_dev_t dev;
    memset(&dev, 0, sizeof(dev));
    dev.fd = -1;
    uart_close(&dev);
    TEST_PASS_MESSAGE("uart_close with fd=-1 did not crash");
}

/* ── main ─────────────────────────────────────────────────────────────── */

int main(void) {
    UNITY_BEGIN();

    RUN_TEST(test_bme280_init_null_ptrs);
    RUN_TEST(test_bme280_get_sensor_data_null_output);
    RUN_TEST(test_bme280_set_sensor_settings_null_settings);
    RUN_TEST(test_bme280_compensate_null_data);
    RUN_TEST(test_gpio_export_fails_no_sysfs);
    RUN_TEST(test_gpio_read_fails_no_sysfs);
    RUN_TEST(test_gpio_write_fails_no_sysfs);
    RUN_TEST(test_uart_open_fails_no_device);
    RUN_TEST(test_uart_close_invalid_fd);

    return UNITY_END();
}
