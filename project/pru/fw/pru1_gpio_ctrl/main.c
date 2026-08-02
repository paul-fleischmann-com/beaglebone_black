/*
 * Copyright (C) 2016-2021 Texas Instruments Incorporated - http://www.ti.com/
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *	* Redistributions of source code must retain the above copyright
 *	  notice, this list of conditions and the following disclaimer.
 *
 *	* Redistributions in binary form must reproduce the above copyright
 *	  notice, this list of conditions and the following disclaimer in the
 *	  documentation and/or other materials provided with the
 *	  distribution.
 *
 *	* Neither the name of Texas Instruments Incorporated nor the names of
 *	  its contributors may be used to endorse or promote products derived
 *	  from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * Transport-Setup (RPMsg-Handshake, Channel-Announce, Interrupt-Handling)
 * übernommen aus dem PRU_RPMsg_Echo_Interrupt1-Beispiel
 * (dinuxbg/pru-software-support-package, GCC-Port). Die Payload-Behandlung
 * wurde vom reinen Echo auf das projekteigene GPIO-Kommandoprotokoll
 * (project/c/include/pru_protocol.h) umgestellt: PRU1 setzt/liest ein Bit in
 * R30/R31 (0-15) auf Kommando aus dem Linux-Userspace, statt Nachrichten nur
 * zurückzuspiegeln. Siehe Issue #252.
 */

#include <stdint.h>
#include <pru_cfg.h>
#include <pru_intc.h>
#include <rsc_types.h>
#include <pru_rpmsg.h>
#include <pru/io.h>
#include "resource_table.h"
#include "intc_map_1.h"
#include "pru_protocol.h"

/* Host-1 Interrupt setzt Bit 31 in R31, wenn Linux die PRU "kickt" */
#define HOST_INT ((uint32_t)1 << 31)

/* PRU-ICSS System-Events für RPMsg auf PRU1 (siehe intc_map_1.h) */
#define TO_ARM_HOST 18
#define FROM_ARM_HOST 19

/*
 * "rpmsg-raw" wird vom generischen rpmsg_char-Treiber im Kernel gebunden und
 * erzeugt ein /dev/rpmsg_pru*-Zeichengerät ohne treiberspezifisches Kernel-
 * Modul (siehe project/c/src/pru.c für die Host-Seite).
 */
#define CHAN_NAME "rpmsg-raw"
#define CHAN_PORT 31

#define VIRTIO_CONFIG_S_DRIVER_OK 4

static uint8_t payload[RPMSG_MESSAGE_SIZE];

static void handle_command(pru_msg_t *msg) {
    if (msg->opcode == PRU_CMD_GPIO_SET) {
        if (msg->pin > PRU_GPIO_PIN_MAX) {
            msg->status = PRU_STATUS_E_PIN;
            return;
        }
        if (msg->value) {
            __R30 |= ((uint32_t)1 << msg->pin);
        } else {
            __R30 &= ~((uint32_t)1 << msg->pin);
        }
        msg->status = PRU_STATUS_OK;
    } else if (msg->opcode == PRU_CMD_GPIO_GET) {
        if (msg->pin > PRU_GPIO_PIN_MAX) {
            msg->status = PRU_STATUS_E_PIN;
            return;
        }
        msg->value = (__R31 >> msg->pin) & 1U;
        msg->status = PRU_STATUS_OK;
    } else {
        msg->status = PRU_STATUS_E_OPCODE;
    }
}

int main(void) {
    struct pru_rpmsg_transport transport;
    uint16_t src, dst, len;
    volatile uint8_t *status;

    /* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
    CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

    /* Clear the status of the PRU-ICSS system event that ARM uses to 'kick' us */
    CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;

    /* Warten bis die Linux-RPMsg-Treiber bereit sind */
    status = &resourceTable.rpmsg_vdev.status;
    while (!(*status & VIRTIO_CONFIG_S_DRIVER_OK)) {
    }

    pru_rpmsg_init(&transport, &resourceTable.rpmsg_vring0, &resourceTable.rpmsg_vring1, TO_ARM_HOST, FROM_ARM_HOST);

    while (pru_rpmsg_channel(RPMSG_NS_CREATE, &transport, CHAN_NAME, CHAN_PORT) != PRU_RPMSG_SUCCESS) {
    }

    while (1) {
        if (__R31 & HOST_INT) {
            CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;

            while (pru_rpmsg_receive(&transport, &src, &dst, payload, &len) == PRU_RPMSG_SUCCESS) {
                if (len >= PRU_MSG_LEN) {
                    handle_command((pru_msg_t *)payload);
                    pru_rpmsg_send(&transport, dst, src, payload, PRU_MSG_LEN);
                }
            }
        }
    }
}
