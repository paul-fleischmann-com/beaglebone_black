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
#include "pru.h"

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

/* ── pru ──────────────────────────────────────────────────────────────── */

void test_pru_load_fails_no_remoteproc(void) {
    int ret = pru_load(1, "bbb-pru1-gpio-ctrl.elf");
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "pru_load should fail without /sys/class/remoteproc pru1");
}

void test_pru_open_fails_no_rpmsg(void) {
    pru_dev_t dev;
    memset(&dev, 0, sizeof(dev));
    int ret = pru_open(&dev, 31);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "pru_open should fail without a matching /sys/class/rpmsg device");
}

void test_pru_command_fails_invalid_fd(void) {
    pru_dev_t dev;
    dev.fd = -1;
    pru_msg_t msg = {.opcode = PRU_CMD_GPIO_SET, .pin = 0, .value = 1, .status = 0};
    int ret = pru_command(&dev, &msg, 100);
    TEST_ASSERT_TRUE_MESSAGE(ret < 0, "pru_command should fail with an invalid fd");
}

void test_pru_close_invalid_fd(void) {
    pru_dev_t dev;
    dev.fd = -1;
    pru_close(&dev);
    TEST_PASS_MESSAGE("pru_close with fd=-1 did not crash");
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
    RUN_TEST(test_pru_load_fails_no_remoteproc);
    RUN_TEST(test_pru_open_fails_no_rpmsg);
    RUN_TEST(test_pru_command_fails_invalid_fd);
    RUN_TEST(test_pru_close_invalid_fd);

    return UNITY_END();
}
