package config

import (
	"os"
	"strings"
	"time"
)

type Config struct {
	Backend    string
	I2CBus     string
	BME280Addr uint8
	UARTPort   string
	UARTBaud   uint32
	SPIDevice  string
	SPISpeed   uint32
	Timeout    time.Duration
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

// LoadConfig liest Konfiguration ausschließlich aus Umgebungsvariablen (SWR-008).
// Unterstützte Variablen: HW_BACKEND, HW_I2C, HW_UART
func LoadConfig() *Config {
	return &Config{
		Backend:    strings.ToLower(getEnv("HW_BACKEND", "auto")),
		I2CBus:     getEnv("HW_I2C", "/dev/i2c-1"),
		BME280Addr: 0x76,
		UARTPort:   getEnv("HW_UART", "/dev/ttyO1"),
		UARTBaud:   115200,
		SPIDevice:  "/dev/spidev0.0",
		SPISpeed:   1000000,
		Timeout:    10 * time.Second,
	}
}
