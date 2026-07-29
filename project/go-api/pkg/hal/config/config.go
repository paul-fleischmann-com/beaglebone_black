package config

import (
	"os"
	"strconv"
	"strings"
	"time"
)

type Config struct {
	Backend      string
	I2CBus       string
	BME280Addr   uint8
	UARTPort     string
	UARTBaud     uint32
	SPIDevice    string
	SPISpeed     uint32
	Timeout      time.Duration
	PRUCore      int
	PRURpmsgPort uint32
	PRUFirmware  string
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

func getEnvInt(key string, fallback int) int {
	if v := os.Getenv(key); v != "" {
		if parsed, err := strconv.Atoi(v); err == nil {
			return parsed
		}
	}
	return fallback
}

func getEnvUint32(key string, fallback uint32) uint32 {
	if v := os.Getenv(key); v != "" {
		if parsed, err := strconv.ParseUint(v, 10, 32); err == nil {
			return uint32(parsed)
		}
	}
	return fallback
}

// LoadConfig liest Konfiguration ausschließlich aus Umgebungsvariablen (SWR-008).
// Unterstützte Variablen: HW_BACKEND, HW_I2C, HW_BME280_ADDR, HW_UART,
// HW_PRU_CORE, HW_PRU_RPMSG_PORT, HW_PRU_FIRMWARE
func LoadConfig() *Config {
	return &Config{
		Backend:      strings.ToLower(getEnv("HW_BACKEND", "auto")),
		I2CBus:       getEnv("HW_I2C", "/dev/i2c-1"),
		BME280Addr:   getEnvUint8("HW_BME280_ADDR", 0x76),
		UARTPort:     getEnv("HW_UART", "/dev/ttyO1"),
		UARTBaud:     115200,
		SPIDevice:    "/dev/spidev0.0",
		SPISpeed:     1000000,
		Timeout:      10 * time.Second,
		PRUCore:      getEnvInt("HW_PRU_CORE", 1),
		PRURpmsgPort: getEnvUint32("HW_PRU_RPMSG_PORT", 31),
		PRUFirmware:  getEnv("HW_PRU_FIRMWARE", "bbb-pru1-gpio-ctrl.elf"),
	}
}
