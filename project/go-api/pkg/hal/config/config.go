package config

import (
	"os"
	"strconv"
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

func getEnvUint8(key string, fallback uint8) uint8 {
	if v := os.Getenv(key); v != "" {
		if parsed, err := strconv.ParseUint(strings.TrimPrefix(v, "0x"), 16, 8); err == nil {
			return uint8(parsed)
		}
	}
	return fallback
}

// LoadConfig liest Konfiguration ausschließlich aus Umgebungsvariablen (SWR-008).
// Unterstützte Variablen: HW_BACKEND, HW_I2C, HW_BME280_ADDR, HW_UART
func LoadConfig() *Config {
	return &Config{
		Backend:    strings.ToLower(getEnv("HW_BACKEND", "auto")),
		I2CBus:     getEnv("HW_I2C", "/dev/i2c-1"),
		BME280Addr: getEnvUint8("HW_BME280_ADDR", 0x76),
		UARTPort:   getEnv("HW_UART", "/dev/ttyO1"),
		UARTBaud:   115200,
		SPIDevice:  "/dev/spidev0.0",
		SPISpeed:   1000000,
		Timeout:    10 * time.Second,
	}
}
