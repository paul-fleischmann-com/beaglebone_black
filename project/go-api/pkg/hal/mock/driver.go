// [SDOC_LINK: SWR-003]
package mockdriver

import (
	"fmt"
	"myproject/pkg/hal"
	"sync"
	"time"
)

type MockDriver struct {
	mu          sync.RWMutex
	gpioValues  map[uint32]int
	uartBuffer  []byte
	Calls       []string
	BME280Error error
	GPIOError   error
	UARTError   error
	SPIError    error
}

func New() *MockDriver                     { return &MockDriver{gpioValues: make(map[uint32]int)} }
func (d *MockDriver) record(c string)      { d.mu.Lock(); d.Calls = append(d.Calls, c); d.mu.Unlock() }
func (d *MockDriver) Name() string         { return "Mock Driver" }
func (d *MockDriver) Backend() hal.Backend { return "mock" }
func (d *MockDriver) Init() error          { d.record("Init"); return nil }
func (d *MockDriver) Close()               { d.record("Close") }

func (d *MockDriver) BME280Read() (*hal.BME280Data, error) {
	d.record("BME280Read")
	if d.BME280Error != nil {
		return nil, d.BME280Error
	}
	return &hal.BME280Data{Temperature: 23.45, Humidity: 48.72,
		Pressure: 1013.25, Altitude: 89.3, Timestamp: time.Now(), Backend: "mock"}, nil
}
func (d *MockDriver) GPIOExport(pin uint32) error {
	d.record(fmt.Sprintf("GPIOExport(%d)", pin))
	if d.GPIOError != nil {
		return d.GPIOError
	}
	d.mu.Lock()
	d.gpioValues[pin] = 0
	d.mu.Unlock()
	return nil
}
func (d *MockDriver) GPIOSetDirection(pin uint32, out bool) error {
	d.record(fmt.Sprintf("GPIOSetDir(%d,%v)", pin, out))
	return d.GPIOError
}
func (d *MockDriver) GPIORead(pin uint32) (*hal.GPIOData, error) {
	d.record(fmt.Sprintf("GPIORead(%d)", pin))
	if d.GPIOError != nil {
		return nil, d.GPIOError
	}
	d.mu.RLock()
	v := d.gpioValues[pin]
	d.mu.RUnlock()
	return &hal.GPIOData{Pin: pin, Value: v, Backend: "mock"}, nil
}
func (d *MockDriver) GPIOWrite(pin uint32, value int) error {
	d.record(fmt.Sprintf("GPIOWrite(%d,%d)", pin, value))
	if d.GPIOError != nil {
		return d.GPIOError
	}
	d.mu.Lock()
	d.gpioValues[pin] = value
	d.mu.Unlock()
	return nil
}
func (d *MockDriver) UARTOpen(port string, baud uint32) error {
	d.record(fmt.Sprintf("UARTOpen(%s,%d)", port, baud))
	return d.UARTError
}
func (d *MockDriver) UARTWrite(data []byte) (int, error) {
	d.record(fmt.Sprintf("UARTWrite(%d)", len(data)))
	if d.UARTError != nil {
		return 0, d.UARTError
	}
	d.mu.Lock()
	d.uartBuffer = append(d.uartBuffer, data...)
	d.mu.Unlock()
	return len(data), nil
}
func (d *MockDriver) UARTRead(ms int) (*hal.UARTData, error) {
	d.record(fmt.Sprintf("UARTRead(%d)", ms))
	if d.UARTError != nil {
		return nil, d.UARTError
	}
	d.mu.Lock()
	data := make([]byte, len(d.uartBuffer))
	copy(data, d.uartBuffer)
	d.uartBuffer = []byte{}
	d.mu.Unlock()
	return &hal.UARTData{Data: data, Length: len(data), Backend: "mock"}, nil
}
func (d *MockDriver) UARTClose() { d.record("UARTClose") }
func (d *MockDriver) SPITransfer(dev string, speed uint32, tx []byte) (*hal.SPIData, error) {
	d.record(fmt.Sprintf("SPI(%s,%d,%d)", dev, speed, len(tx)))
	if d.SPIError != nil {
		return nil, d.SPIError
	}
	rx := make([]byte, len(tx))
	copy(rx, tx)
	return &hal.SPIData{RxBuf: rx, Length: len(rx), Backend: "mock"}, nil
}
func (d *MockDriver) WasCalled(m string) bool {
	d.mu.RLock()
	defer d.mu.RUnlock()
	for _, c := range d.Calls {
		if c == m {
			return true
		}
	}
	return false
}
func (d *MockDriver) Reset() {
	d.mu.Lock()
	defer d.mu.Unlock()
	d.Calls = nil
	d.gpioValues = make(map[uint32]int)
	d.uartBuffer = nil
	d.BME280Error = nil
	d.GPIOError = nil
	d.UARTError = nil
	d.SPIError = nil
}
