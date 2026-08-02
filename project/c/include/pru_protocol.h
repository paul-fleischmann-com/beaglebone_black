/*
 * Wire-Protokoll für die RPMsg-Kommunikation zwischen Linux-Userspace und der
 * PRU1-Firmware (project/pru/fw/pru1_gpio_ctrl). Wird von beiden Seiten
 * eingebunden (Host: project/c/src/pru.c via CGO/HAL; PRU: main.c über den
 * Include-Pfad in project/pru/fw/pru1_gpio_ctrl/Makefile), damit es nur eine
 * Quelle der Wahrheit für das Nachrichtenformat gibt. Siehe Issue #252.
 *
 * Nachricht (4 Bytes, request und response identisch aufgebaut):
 *   [0] opcode  — PRU_CMD_GPIO_SET oder PRU_CMD_GPIO_GET
 *   [1] pin     — Bit-Index 0-15 im PRU-Register R30 (SET) bzw. R31 (GET)
 *   [2] value   — SET: zu schreibender Wert (0/1). GET (Request): ignoriert,
 *                 (Response): gelesener Wert.
 *   [3] status  — nur in der Response gültig: PRU_STATUS_OK/PRU_STATUS_*
 */
#ifndef PRU_PROTOCOL_H
#define PRU_PROTOCOL_H

#include <stdint.h>

#define PRU_CMD_GPIO_SET ((uint8_t)1)
#define PRU_CMD_GPIO_GET ((uint8_t)2)

#define PRU_STATUS_OK ((uint8_t)0)
#define PRU_STATUS_E_OPCODE ((uint8_t)1)
#define PRU_STATUS_E_PIN ((uint8_t)2)

#define PRU_GPIO_PIN_MAX 15
#define PRU_MSG_LEN 4

typedef struct {
    uint8_t opcode;
    uint8_t pin;
    uint8_t value;
    uint8_t status;
} pru_msg_t;

#endif /* PRU_PROTOCOL_H */
