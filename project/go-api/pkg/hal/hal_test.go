// [SDOC_LINK: SWR-003]
// [SDOC_LINK: HW-DRV-001]
// [SDOC_LINK: HW-DRV-002]
// [SDOC_LINK: HW-DRV-003]
// [SDOC_LINK: HW-DRV-004]
package hal_test

import (
	"errors"
	"myproject/pkg/hal"
	mock "myproject/pkg/hal/mock"
	"testing"
)

func setupMock(t *testing.T) *mock.MockDriver {
	t.Helper()
	d := mock.New()
	if err := d.Init(); err != nil {
		t.Fatalf("Init: %v", err)
	}
	return d
}

// ── BME280 ──────────────────────────────────────────────
func TestBME280Read_Erfolg(t *testing.T) {
	d := setupMock(t)
	data, err := d.BME280Read()
	if err != nil {
		t.Fatalf("Fehler: %v", err)
	}
	if data.Temperature < -40 || data.Temperature > 85 {
		t.Errorf("Temp: %.2f", data.Temperature)
	}
	if data.Humidity < 0 || data.Humidity > 100 {
		t.Errorf("Hum: %.2f", data.Humidity)
	}
	if data.Pressure < 300 || data.Pressure > 1100 {
		t.Errorf("Press: %.2f", data.Pressure)
	}
	if !d.WasCalled("BME280Read") {
		t.Error("BME280Read nicht aufgerufen")
	}
}
func TestBME280Read_Fehler(t *testing.T) {
	d := setupMock(t)
	d.BME280Error = errors.New("I2C Fehler")
	_, err := d.BME280Read()
	if err == nil {
		t.Fatal("Fehler erwartet")
	}
}

// ── GPIO ────────────────────────────────────────────────
func TestGPIO_SchreibenLesen(t *testing.T) {
	d := setupMock(t)
	d.GPIOExport(60)
	d.GPIOWrite(60, 1)
	data, err := d.GPIORead(60)
	if err != nil {
		t.Fatalf("GPIORead: %v", err)
	}
	if data.Value != 1 {
		t.Errorf("Wert: %d", data.Value)
	}
}
func TestGPIO_Tabelle(t *testing.T) {
	tests := []struct {
		pin       uint32
		val       int
		wantErr   bool
		injectErr error
	}{
		{60, 1, false, nil}, {60, 0, false, nil}, {61, 1, false, nil},
		{60, 1, true, errors.New("GPIO Fehler")},
	}
	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			d := setupMock(t)
			d.GPIOError = tt.injectErr
			d.GPIOExport(tt.pin)
			err := d.GPIOWrite(tt.pin, tt.val)
			if (err != nil) != tt.wantErr {
				t.Errorf("wantErr=%v", tt.wantErr)
			}
		})
	}
}

// ── UART ────────────────────────────────────────────────
func TestUART_SendEmpfangen(t *testing.T) {
	d := setupMock(t)
	d.UARTOpen("/dev/ttyO1", 115200)
	msg := []byte("Hallo BeagleBone!")
	n, err := d.UARTWrite(msg)
	if err != nil {
		t.Fatalf("Write: %v", err)
	}
	if n != len(msg) {
		t.Errorf("n=%d", n)
	}
	data, err := d.UARTRead(100)
	if err != nil {
		t.Fatalf("Read: %v", err)
	}
	if string(data.Data) != string(msg) {
		t.Errorf("Daten: %s", data.Data)
	}
}

// ── SPI ─────────────────────────────────────────────────
func TestSPI_Loopback(t *testing.T) {
	d := setupMock(t)
	tx := []byte{0x01, 0x02, 0x03, 0xFF}
	data, err := d.SPITransfer("/dev/spidev0.0", 1000000, tx)
	if err != nil {
		t.Fatalf("SPI: %v", err)
	}
	for i, b := range tx {
		if data.RxBuf[i] != b {
			t.Errorf("rx[%d]=%X", i, data.RxBuf[i])
		}
	}
}

// ── Interface Compliance ────────────────────────────────
func TestInterface_Compliance(t *testing.T) {
	var _ hal.HardwareDriver = (*mock.MockDriver)(nil)
}

// ── Driver Metadaten ─────────────────────────────────────────────────────────
func TestDriver_Name(t *testing.T) {
	d := setupMock(t)
	if d.Name() == "" {
		t.Error("Name() sollte nicht leer sein")
	}
}
func TestDriver_Backend(t *testing.T) {
	d := setupMock(t)
	if d.Backend() == "" {
		t.Error("Backend() sollte nicht leer sein")
	}
}
func TestDriver_Close(t *testing.T) {
	d := setupMock(t)
	d.Close()
	if !d.WasCalled("Close") {
		t.Error("Close wurde nicht aufgerufen")
	}
}

// ── GPIO SetDirection ────────────────────────────────────────────────────────
func TestGPIO_SetDirection(t *testing.T) {
	d := setupMock(t)
	if err := d.GPIOSetDirection(60, true); err != nil {
		t.Errorf("SetDirection out: %v", err)
	}
	if err := d.GPIOSetDirection(60, false); err != nil {
		t.Errorf("SetDirection in: %v", err)
	}
	if !d.WasCalled("GPIOSetDir(60,true)") {
		t.Error("GPIOSetDir nicht aufgerufen")
	}
}

// ── UART Close ───────────────────────────────────────────────────────────────
func TestUART_Close(t *testing.T) {
	d := setupMock(t)
	d.UARTClose()
	if !d.WasCalled("UARTClose") {
		t.Error("UARTClose wurde nicht aufgerufen")
	}
}

// ── Mock Reset ───────────────────────────────────────────────────────────────
func TestMock_Reset(t *testing.T) {
	d := setupMock(t)
	d.BME280Read()
	d.Reset()
	if len(d.Calls) != 0 {
		t.Errorf("Calls nach Reset nicht leer: %v", d.Calls)
	}
	if d.WasCalled("BME280Read") {
		t.Error("WasCalled nach Reset sollte false sein")
	}
}

// ── Fallback ────────────────────────────────────────────────────────────────
// [SDOC_LINK: SWR-005]
func TestFallback_PrimaerFehler(t *testing.T) {
	primary := mock.New()
	primary.Init()
	secondary := mock.New()
	secondary.Init()
	primary.BME280Error = errors.New("ausgefallen")
	_, err := primary.BME280Read()
	if err == nil {
		t.Fatal("Primary sollte fehlschlagen")
	}
	_, err = secondary.BME280Read()
	if err != nil {
		t.Fatalf("Secondary: %v", err)
	}
}
