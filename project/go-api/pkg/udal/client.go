// Package udalclient integrates the BeagleBone Black Go API with a UDAL
// Gateway using the UDAL Go SDK (device-side push, udal#47 "Weg 2").
//
// Enabled by setting UDAL_GATEWAY_URL. If the variable is empty the package
// is a no-op — the existing REST API is completely unaffected.
package udalclient

import (
	"context"
	"fmt"
	"log"
	"math"
	"os"
	"sync"
	"time"

	udal "github.com/paulefl/udal/code/sdk/go"
	"myproject/pkg/hal"
)

// Config holds UDAL connection settings.
//
// Environment variables:
//
//	UDAL_GATEWAY_URL  gRPC address, e.g. "192.168.2.55:50051" (required to enable)
//	UDAL_API_KEY      API key (matches UDAL_BOOTSTRAP_API_KEY on the gateway)
//	UDAL_DEVICE_ID    stable device id; defaults to "beaglebone-01"
//	UDAL_CAPABILITY   capability schema ref; defaults to "beaglebone-bme280@1.0.0"
//	UDAL_INTERVAL     publish interval, e.g. "2s"; defaults to "5s"
type Config struct {
	GatewayURL string
	APIKey     string
	DeviceID   string
	Capability string
	Interval   time.Duration
}

// LoadConfig reads UDAL settings from environment variables.
// Returns nil when UDAL_GATEWAY_URL is not set (feature disabled).
func LoadConfig() *Config {
	url := os.Getenv("UDAL_GATEWAY_URL")
	if url == "" {
		return nil
	}
	interval := 5 * time.Second
	if v := os.Getenv("UDAL_INTERVAL"); v != "" {
		if d, err := time.ParseDuration(v); err == nil {
			interval = d
		}
	}
	deviceID := os.Getenv("UDAL_DEVICE_ID")
	if deviceID == "" {
		deviceID = "beaglebone-01"
	}
	capability := os.Getenv("UDAL_CAPABILITY")
	if capability == "" {
		capability = "beaglebone-bme280@1.0.0"
	}
	return &Config{
		GatewayURL: url,
		APIKey:     os.Getenv("UDAL_API_KEY"),
		DeviceID:   deviceID,
		Capability: capability,
		Interval:   interval,
	}
}

// Run connects to the UDAL Gateway, registers the device, starts the BME280
// publish loop and registers a GPIO command handler.
//
// Run blocks until ctx is cancelled. Start it in a goroutine alongside the
// HTTP server — the REST API runs independently.
func Run(ctx context.Context, cfg *Config, hw hal.HardwareDriver, hwMu *sync.Mutex) error {
	device, err := udal.NewDevice(udal.Config{
		GatewayURL: cfg.GatewayURL,
		DeviceID:   cfg.DeviceID,
		Name:       cfg.DeviceID,
		Capability: cfg.Capability,
		Transport:  "grpc",
		APIKey:     cfg.APIKey,
		// TLSConfig nil → insecure (plaintext); set for production deployments
	})
	if err != nil {
		return fmt.Errorf("udal: dial %s: %w", cfg.GatewayURL, err)
	}
	defer device.Close()

	// GPIO USR0 (pin 60) write command received from the gateway side
	device.OnCommand("set_gpio_usr0", func(params udal.Params) (any, error) {
		val := int(params.Float("value"))
		hwMu.Lock()
		err := hw.GPIOWrite(60, val)
		hwMu.Unlock()
		if err != nil {
			return nil, fmt.Errorf("gpio write pin 60: %w", err)
		}
		return map[string]any{"pin": 60, "value": val}, nil
	})

	// BME280 publish loop — runs concurrently with device.Run's command stream
	go func() {
		ticker := time.NewTicker(cfg.Interval)
		defer ticker.Stop()
		for {
			select {
			case <-ctx.Done():
				return
			case <-ticker.C:
				hwMu.Lock()
				data, err := hw.BME280Read()
				hwMu.Unlock()
				if err != nil {
					log.Printf("udal: BME280Read: %v", err)
					continue
				}
				pub := func(path string, v float64) {
					if math.IsNaN(v) || math.IsInf(v, 0) {
						return
					}
					if err := device.PublishProperty(ctx, path, v); err != nil {
						log.Printf("udal: PublishProperty %s: %v", path, err)
					}
				}
				pub("temperature", data.Temperature)
				pub("humidity", data.Humidity)
				pub("pressure", data.Pressure)
			}
		}
	}()

	log.Printf("udal: connected to %s  device=%s  interval=%s",
		cfg.GatewayURL, cfg.DeviceID, cfg.Interval)
	return device.Run(ctx)
}
