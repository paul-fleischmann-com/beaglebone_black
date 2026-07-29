// Package prudriver bindet den PRU1-RPMsg-Kommunikationskanal (project/c/src/pru.c)
// über CGO ein. Der Backend deckt ausschließlich deterministisches GPIO ab
// (R30/R31-Bit 0-15 der PRU, siehe project/pru/fw/pru1_gpio_ctrl) — BME280,
// UART und SPI laufen weiterhin über die c/rust-Backends. Siehe Issue #252.
package prudriver

/*
#cgo CFLAGS:  -I${SRCDIR}/../../../libs/include
#cgo LDFLAGS: -L${SRCDIR}/../../../libs -lhardware
#include "pru.h"
#include <stdlib.h>
*/
import "C"
import (
	"fmt"
	"myproject/pkg/hal"
	"myproject/pkg/hal/config"
	"unsafe"
)

type PRUDriver struct {
	dev C.pru_dev_t
	cfg *config.Config
}

func New(cfg *config.Config) *PRUDriver   { return &PRUDriver{cfg: cfg, dev: C.pru_dev_t{fd: -1}} }
func (d *PRUDriver) Name() string         { return "PRU Hardware Driver" }
func (d *PRUDriver) Backend() hal.Backend { return hal.BackendPRU }

func (d *PRUDriver) Init() error {
	fw := C.CString(d.cfg.PRUFirmware)
	defer C.free(unsafe.Pointer(fw))
	if ret := C.pru_load(C.int(d.cfg.PRUCore), fw); ret != 0 {
		return fmt.Errorf("PRU load (core %d, firmware %s): %d", d.cfg.PRUCore, d.cfg.PRUFirmware, ret)
	}
	if ret := C.pru_open(&d.dev, C.uint32_t(d.cfg.PRURpmsgPort)); ret != 0 {
		return fmt.Errorf("PRU rpmsg open (port %d): %d", d.cfg.PRURpmsgPort, ret)
	}
	return nil
}

func validatePin(pin uint32) error {
	if pin > C.PRU_GPIO_PIN_MAX {
		return fmt.Errorf("PRU GPIO pin %d außerhalb des gültigen Bereichs (0-%d, R30/R31-Bit)", pin, C.PRU_GPIO_PIN_MAX)
	}
	return nil
}

// GPIOExport ist für den PRU-Backend ein No-Op — PRU-Pins werden über
// Device-Tree-Pinmux freigegeben, nicht über Sysfs-Export.
func (d *PRUDriver) GPIOExport(pin uint32) error { return validatePin(pin) }

// GPIOSetDirection: Die Richtung eines PRU-Pins wird über den Device-Tree-
// Pinmux fest verdrahtet und kann nicht zur Laufzeit umgeschaltet werden.
func (d *PRUDriver) GPIOSetDirection(pin uint32, out bool) error {
	if err := validatePin(pin); err != nil {
		return err
	}
	if !out {
		return fmt.Errorf("PRU-Pin-Richtung ist Hardware-/Pinmux-fest (R30=Output), Umschalten zu Input zur Laufzeit nicht unterstützt")
	}
	return nil
}

func (d *PRUDriver) command(opcode, pin, value uint8) (uint8, error) {
	if err := validatePin(uint32(pin)); err != nil {
		return 0, err
	}
	msg := C.pru_msg_t{opcode: C.uint8_t(opcode), pin: C.uint8_t(pin), value: C.uint8_t(value)}
	timeoutMs := C.int(d.cfg.Timeout.Milliseconds())
	if ret := C.pru_command(&d.dev, &msg, timeoutMs); ret != 0 {
		return 0, fmt.Errorf("PRU rpmsg command (opcode %d, pin %d): %d", opcode, pin, ret)
	}
	if msg.status != C.PRU_STATUS_OK {
		return 0, fmt.Errorf("PRU meldet Fehler-Status %d für opcode %d, pin %d", msg.status, opcode, pin)
	}
	return uint8(msg.value), nil
}

func (d *PRUDriver) GPIOWrite(pin uint32, value int) error {
	v := uint8(0)
	if value != 0 {
		v = 1
	}
	_, err := d.command(C.PRU_CMD_GPIO_SET, uint8(pin), v)
	return err
}

func (d *PRUDriver) GPIORead(pin uint32) (*hal.GPIOData, error) {
	v, err := d.command(C.PRU_CMD_GPIO_GET, uint8(pin), 0)
	if err != nil {
		return nil, err
	}
	return &hal.GPIOData{Pin: pin, Value: int(v), Backend: "pru"}, nil
}

var errNotSupported = fmt.Errorf("PRU-Backend unterstützt nur deterministisches GPIO (R30/R31), siehe Issue #252")

func (d *PRUDriver) BME280Read() (*hal.BME280Data, error)    { return nil, errNotSupported }
func (d *PRUDriver) UARTOpen(port string, baud uint32) error { return errNotSupported }
func (d *PRUDriver) UARTWrite(data []byte) (int, error)      { return 0, errNotSupported }
func (d *PRUDriver) UARTRead(timeoutMs int) (*hal.UARTData, error) {
	return nil, errNotSupported
}
func (d *PRUDriver) UARTClose() {}
func (d *PRUDriver) SPITransfer(dev string, speed uint32, tx []byte) (*hal.SPIData, error) {
	return nil, errNotSupported
}

func (d *PRUDriver) Close() {
	C.pru_close(&d.dev)
	C.pru_stop(C.int(d.cfg.PRUCore))
}
