#ifndef PRU_H
#define PRU_H
#include <stdint.h>
#include "pru_protocol.h"

typedef struct {
    int fd;
} pru_dev_t;

/* Schreibt firmware_name nach /sys/class/remoteproc/remoteprocN/firmware und
 * startet den Core (state=start). N wird über das "name"-Attribut jedes
 * remoteprocN-Verzeichnisses anhand von "pru<core>" ermittelt (core: 0 oder 1). */
int pru_load(int core, const char *firmware_name);
/* Stoppt den PRU-Core (state=stop). */
int pru_stop(int core);
/* Öffnet das rpmsg-Zeichengerät (Kanal "rpmsg-raw", gegebener Port) — sucht
 * das passende /dev/rpmsgN über die name/src-Attribute unter /sys/class/rpmsg. */
int pru_open(pru_dev_t *dev, uint32_t port);
/* Sendet ein Kommando (opcode/pin/value) und wartet bis timeout_ms auf die
 * Antwort. msg wird mit der Antwort überschrieben. */
int pru_command(pru_dev_t *dev, pru_msg_t *msg, int timeout_ms);
void pru_close(pru_dev_t *dev);
#endif
