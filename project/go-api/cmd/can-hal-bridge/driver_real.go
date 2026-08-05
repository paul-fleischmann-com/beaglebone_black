//go:build hwreal

package main

import (
	"myproject/pkg/hal"
	"myproject/pkg/hal/config"
	"myproject/pkg/hal/loader"
)

// newDriver returns a real HAL driver (c/rust/auto, selected via HW_BACKEND
// like cmd/main.go) — requires CGO_ENABLED=1 and the cross-built
// libhardware.so/libhardware_rs.so (see `make can-hal-bridge-hw`).
func newDriver() (hal.HardwareDriver, error) {
	cfg := config.LoadConfig()
	return loader.NewDriver(cfg)
}
