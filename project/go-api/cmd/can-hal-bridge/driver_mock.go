//go:build !hwreal

package main

import (
	"myproject/pkg/hal"
	mockdriver "myproject/pkg/hal/mock"
)

// newDriver returns the CGO-free mock HAL driver — the default build of
// can-hal-bridge (Issue #270: "Mock als Default für CI"). Build with
// `-tags hwreal` (see driver_real.go) to talk to real BME280 hardware
// instead.
func newDriver() (hal.HardwareDriver, error) {
	d := mockdriver.New()
	if err := d.Init(); err != nil {
		return nil, err
	}
	return d, nil
}
