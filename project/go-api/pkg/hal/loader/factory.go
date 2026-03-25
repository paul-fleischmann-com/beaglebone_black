// Package loader creates HAL driver instances based on configuration.
// It is intentionally separate from package hal to break the import cycle:
//
//	pkg/hal (interface + types) ← pkg/hal/c ← pkg/hal/loader
package loader

import (
	"fmt"
	"log"
	"myproject/pkg/hal"
	cdriver "myproject/pkg/hal/c"
	"myproject/pkg/hal/config"
	rustdriver "myproject/pkg/hal/rust"
)

func NewDriver(cfg *config.Config) (hal.HardwareDriver, error) {
	switch cfg.Backend {
	case "c":
		d := cdriver.New(cfg)
		if err := d.Init(); err != nil {
			return nil, fmt.Errorf("C Driver: %w", err)
		}
		log.Printf("✅ Backend: C Library")
		return d, nil
	case "rust":
		d := rustdriver.New(cfg)
		if err := d.Init(); err != nil {
			return nil, fmt.Errorf("Rust Driver: %w", err)
		}
		log.Printf("✅ Backend: Rust Library")
		return d, nil
	case "auto":
		return newAutoDriver(cfg)
	default:
		return nil, fmt.Errorf("unbekanntes Backend: %s", cfg.Backend)
	}
}

type autoDriver struct {
	primary   hal.HardwareDriver
	secondary hal.HardwareDriver
}

func newAutoDriver(cfg *config.Config) (hal.HardwareDriver, error) {
	primary := cdriver.New(cfg)
	if err := primary.Init(); err != nil {
		log.Printf("⚠️  C Driver fehlgeschlagen: %v → Rust Fallback", err)
		secondary := rustdriver.New(cfg)
		if err2 := secondary.Init(); err2 != nil {
			return nil, fmt.Errorf("beide Backends fehlgeschlagen")
		}
		return secondary, nil
	}
	secondary := rustdriver.New(cfg)
	secondary.Init()
	log.Printf("✅ Backend: C (primär) + Rust (Backup)")
	return &autoDriver{primary: primary, secondary: secondary}, nil
}

func (d *autoDriver) Name() string         { return "Auto Driver (C→Rust)" }
func (d *autoDriver) Backend() hal.Backend { return hal.BackendAuto }
func (d *autoDriver) Init() error          { return nil }
func (d *autoDriver) Close()               { d.primary.Close(); d.secondary.Close() }

func (d *autoDriver) BME280Read() (*hal.BME280Data, error) {
	if data, err := d.primary.BME280Read(); err == nil {
		return data, nil
	}
	log.Printf("⚠️  C BME280 fehlgeschlagen → Rust")
	return d.secondary.BME280Read()
}
func (d *autoDriver) GPIOExport(pin uint32) error {
	if err := d.primary.GPIOExport(pin); err == nil {
		return nil
	}
	return d.secondary.GPIOExport(pin)
}
func (d *autoDriver) GPIOSetDirection(pin uint32, out bool) error {
	if err := d.primary.GPIOSetDirection(pin, out); err == nil {
		return nil
	}
	return d.secondary.GPIOSetDirection(pin, out)
}
func (d *autoDriver) GPIORead(pin uint32) (*hal.GPIOData, error) {
	if data, err := d.primary.GPIORead(pin); err == nil {
		return data, nil
	}
	return d.secondary.GPIORead(pin)
}
func (d *autoDriver) GPIOWrite(pin uint32, value int) error {
	if err := d.primary.GPIOWrite(pin, value); err == nil {
		return nil
	}
	return d.secondary.GPIOWrite(pin, value)
}
func (d *autoDriver) UARTOpen(port string, baud uint32) error {
	if err := d.primary.UARTOpen(port, baud); err == nil {
		return nil
	}
	return d.secondary.UARTOpen(port, baud)
}
func (d *autoDriver) UARTWrite(data []byte) (int, error) {
	if n, err := d.primary.UARTWrite(data); err == nil {
		return n, nil
	}
	return d.secondary.UARTWrite(data)
}
func (d *autoDriver) UARTRead(ms int) (*hal.UARTData, error) {
	if data, err := d.primary.UARTRead(ms); err == nil {
		return data, nil
	}
	return d.secondary.UARTRead(ms)
}
func (d *autoDriver) UARTClose() { d.primary.UARTClose(); d.secondary.UARTClose() }
func (d *autoDriver) SPITransfer(dev string, speed uint32, tx []byte) (*hal.SPIData, error) {
	if data, err := d.primary.SPITransfer(dev, speed, tx); err == nil {
		return data, nil
	}
	return d.secondary.SPITransfer(dev, speed, tx)
}
