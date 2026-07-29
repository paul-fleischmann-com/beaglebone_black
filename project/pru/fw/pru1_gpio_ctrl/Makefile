# Baut die PRU1-Firmware (RPMsg-GPIO-Kommandoprotokoll) mit der GNU-PRU-
# Toolchain. Voraussetzung: scripts/setup_pru_toolchain.sh wurde ausgeführt
# (setzt PRU_TOOLCHAIN_DIR, Default $(REPO_ROOT)/toolchain/pru). Siehe #252.

REPO_ROOT      := $(abspath ../../../..)
PRU_TOOLCHAIN_DIR ?= $(REPO_ROOT)/toolchain/pru
PRU_GCC_BIN    ?= $(PRU_TOOLCHAIN_DIR)/gnupru/pru-elf/bin
PSSP_DIR       ?= $(PRU_TOOLCHAIN_DIR)/pssp
CROSS_COMPILE  := $(PRU_GCC_BIN)/pru-

CFLAGS  += -g -Os -Wall -Wextra -Wno-array-bounds
CFLAGS  += -I$(PSSP_DIR)/include -I$(PSSP_DIR)/include/am335x
CFLAGS  += -I$(REPO_ROOT)/project/c/include
CFLAGS  += -minrt -mmcu=am335x.pru1

SRC := main.c \
       $(PSSP_DIR)/lib/src/rpmsg_lib/pru_rpmsg.c \
       $(PSSP_DIR)/lib/src/rpmsg_lib/pru_virtqueue.c

OUT := out
ELF := $(OUT)/pru1_gpio_ctrl.elf

all: $(ELF)
	@echo "Erfolg: $^"

$(OUT):
	mkdir -p $(OUT)

$(ELF): $(SRC) main.c resource_table.h intc_map_1.h | $(OUT)
	$(CROSS_COMPILE)gcc $(CFLAGS) $(SRC) $(LDFLAGS) -o $@

clean:
	rm -rf $(OUT)

.PHONY: all clean
