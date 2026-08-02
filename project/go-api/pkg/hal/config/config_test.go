// [SDOC_LINK: SWR-008]
package config

import (
	"flag"
	"testing"
)

// Regression Test für Issue #26:
// LoadConfig() darf flag.CommandLine nicht verändern (kein flag.Parse() in Library).
func TestLoadConfig_DoesNotRegisterFlags(t *testing.T) {
	if flag.Lookup("backend") != nil {
		t.Error("LoadConfig() registriert flag 'backend' — darf nicht in Library-Package sein")
	}
	if flag.Lookup("uart") != nil {
		t.Error("LoadConfig() registriert flag 'uart' — darf nicht in Library-Package sein")
	}
	if flag.Lookup("i2c") != nil {
		t.Error("LoadConfig() registriert flag 'i2c' — darf nicht in Library-Package sein")
	}
}

func TestLoadConfig_Defaults(t *testing.T) {
	cfg := LoadConfig()
	if cfg.Backend != "auto" {
		t.Errorf("Backend default: %q", cfg.Backend)
	}
	if cfg.BME280Addr != 0x76 {
		t.Errorf("BME280Addr: %x", cfg.BME280Addr)
	}
	if cfg.UARTBaud != 115200 {
		t.Errorf("UARTBaud: %d", cfg.UARTBaud)
	}
	if cfg.SPISpeed != 1000000 {
		t.Errorf("SPISpeed: %d", cfg.SPISpeed)
	}
	if cfg.Timeout == 0 {
		t.Error("Timeout nicht gesetzt")
	}
}

func TestLoadConfig_EnvOverride(t *testing.T) {
	t.Setenv("HW_BACKEND", "rust")
	cfg := LoadConfig()
	if cfg.Backend != "rust" {
		t.Errorf("HW_BACKEND override: %q", cfg.Backend)
	}
}

func TestLoadConfig_I2CBus_EnvOverride(t *testing.T) {
	t.Setenv("HW_I2C", "/dev/i2c-2")
	cfg := LoadConfig()
	if cfg.I2CBus != "/dev/i2c-2" {
		t.Errorf("HW_I2C override: %q", cfg.I2CBus)
	}
}

func TestLoadConfig_UARTPort_EnvOverride(t *testing.T) {
	t.Setenv("HW_UART", "/dev/ttyO2")
	cfg := LoadConfig()
	if cfg.UARTPort != "/dev/ttyO2" {
		t.Errorf("HW_UART override: %q", cfg.UARTPort)
	}
}

func TestLoadConfig_PRUDefaults(t *testing.T) {
	cfg := LoadConfig()
	if cfg.PRUCore != 1 {
		t.Errorf("PRUCore default: %d", cfg.PRUCore)
	}
	if cfg.PRURpmsgPort != 31 {
		t.Errorf("PRURpmsgPort default: %d", cfg.PRURpmsgPort)
	}
	if cfg.PRUFirmware != "bbb-pru1-gpio-ctrl.elf" {
		t.Errorf("PRUFirmware default: %q", cfg.PRUFirmware)
	}
}

func TestLoadConfig_PRUCore_EnvOverride(t *testing.T) {
	t.Setenv("HW_PRU_CORE", "0")
	cfg := LoadConfig()
	if cfg.PRUCore != 0 {
		t.Errorf("HW_PRU_CORE override: %d", cfg.PRUCore)
	}
}
