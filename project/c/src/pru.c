#include "pru.h"
#include <dirent.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <unistd.h>

#define REMOTEPROC_CLASS "/sys/class/remoteproc"
#define RPMSG_CLASS "/sys/class/rpmsg"
#define RPMSG_CHAN_NAME "rpmsg-raw"

static int write_file(const char *path, const char *value) {
    int fd = open(path, O_WRONLY);
    if (fd < 0) return -1;
    ssize_t n = write(fd, value, strlen(value));
    close(fd);
    return (n < 0) ? -1 : 0;
}

static int read_file(const char *path, char *buf, size_t len) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) return -1;
    ssize_t n = read(fd, buf, len - 1);
    close(fd);
    if (n < 0) return -1;
    buf[n] = '\0';
    while (n > 0 && (buf[n - 1] == '\n' || buf[n - 1] == '\r')) buf[--n] = '\0';
    return 0;
}

/* Findet remoteprocN, dessen "name"-Attribut "pru<core>" enthält. Gibt N
 * (>=0) oder -1 zurück. */
static int find_remoteproc(int core) {
    DIR *d = opendir(REMOTEPROC_CLASS);
    if (!d) return -1;
    char needle[8];
    snprintf(needle, sizeof(needle), "pru%d", core);
    struct dirent *e;
    int found = -1;
    while ((e = readdir(d)) != NULL) {
        int n;
        if (sscanf(e->d_name, "remoteproc%d", &n) != 1) continue;
        char path[300], name[128];
        snprintf(path, sizeof(path), "%s/%s/name", REMOTEPROC_CLASS, e->d_name);
        if (read_file(path, name, sizeof(name)) != 0) continue;
        if (strstr(name, needle) != NULL) {
            found = n;
            break;
        }
    }
    closedir(d);
    return found;
}

int pru_load(int core, const char *firmware_name) {
    int n = find_remoteproc(core);
    if (n < 0) return -1;
    char path[128];
    snprintf(path, sizeof(path), "%s/remoteproc%d/state", REMOTEPROC_CLASS, n);
    write_file(path, "stop"); /* best-effort, kann fehlschlagen falls bereits gestoppt */
    snprintf(path, sizeof(path), "%s/remoteproc%d/firmware", REMOTEPROC_CLASS, n);
    if (write_file(path, firmware_name) != 0) return -1;
    snprintf(path, sizeof(path), "%s/remoteproc%d/state", REMOTEPROC_CLASS, n);
    if (write_file(path, "start") != 0) return -1;
    return 0;
}

int pru_stop(int core) {
    int n = find_remoteproc(core);
    if (n < 0) return -1;
    char path[128];
    snprintf(path, sizeof(path), "%s/remoteproc%d/state", REMOTEPROC_CLASS, n);
    return write_file(path, "stop");
}

/* Findet rpmsgN mit name=="rpmsg-raw" und src==port oder dst==port. */
static int find_rpmsg_dev(uint32_t port) {
    DIR *d = opendir(RPMSG_CLASS);
    if (!d) return -1;
    struct dirent *e;
    int found = -1;
    while ((e = readdir(d)) != NULL) {
        int n;
        if (sscanf(e->d_name, "rpmsg%d", &n) != 1) continue;
        char path[300], name[64], numbuf[16];
        snprintf(path, sizeof(path), "%s/%s/name", RPMSG_CLASS, e->d_name);
        if (read_file(path, name, sizeof(name)) != 0) continue;
        if (strcmp(name, RPMSG_CHAN_NAME) != 0) continue;
        snprintf(path, sizeof(path), "%s/%s/src", RPMSG_CLASS, e->d_name);
        uint32_t src = 0, dst = 0;
        if (read_file(path, numbuf, sizeof(numbuf)) == 0) src = (uint32_t)strtoul(numbuf, NULL, 10);
        snprintf(path, sizeof(path), "%s/%s/dst", RPMSG_CLASS, e->d_name);
        if (read_file(path, numbuf, sizeof(numbuf)) == 0) dst = (uint32_t)strtoul(numbuf, NULL, 10);
        if (src == port || dst == port) {
            found = n;
            break;
        }
    }
    closedir(d);
    return found;
}

int pru_open(pru_dev_t *dev, uint32_t port) {
    int n = find_rpmsg_dev(port);
    if (n < 0) return -1;
    char path[64];
    snprintf(path, sizeof(path), "/dev/rpmsg%d", n);
    dev->fd = open(path, O_RDWR);
    if (dev->fd < 0) return -1;
    return 0;
}

int pru_command(pru_dev_t *dev, pru_msg_t *msg, int timeout_ms) {
    if (dev->fd < 0) return -1;
    if (write(dev->fd, msg, PRU_MSG_LEN) != PRU_MSG_LEN) return -1;

    fd_set fds;
    struct timeval tv = {.tv_sec = timeout_ms / 1000, .tv_usec = (timeout_ms % 1000) * 1000};
    FD_ZERO(&fds);
    FD_SET(dev->fd, &fds);
    if (select(dev->fd + 1, &fds, NULL, NULL, &tv) <= 0) return -1;

    pru_msg_t resp;
    ssize_t n = read(dev->fd, &resp, sizeof(resp));
    if (n < (ssize_t)PRU_MSG_LEN) return -1;
    *msg = resp;
    return 0;
}

void pru_close(pru_dev_t *dev) {
    if (dev->fd >= 0) {
        close(dev->fd);
        dev->fd = -1;
    }
}
