// [SDOC_LINK: SWR-001]
// [SDOC_LINK: SWR-004]
package hal

import "time"

type Backend string

const (
	BackendC    Backend = "c"
	BackendRust Backend = "rust"
	BackendAuto Backend = "auto"
)

type HardwareDriver interface {
	Name() string
	Backend() Backend
	BME280Read() (*BME280Data, error)
	GPIOExport(pin uint32) error
	GPIOSetDirection(pin uint32, out bool) error
	GPIORead(pin uint32) (*GPIOData, error)
	GPIOWrite(pin uint32, value int) error
	UARTOpen(port string, baud uint32) error
	UARTWrite(data []byte) (int, error)
	UARTRead(timeoutMs int) (*UARTData, error)
	UARTClose()
	SPITransfer(dev string, speed uint32, tx []byte) (*SPIData, error)
	Init() error
	Close()
}
type BME280Data struct {
	Temperature float64   `json:"temperature"`
	Humidity    float64   `json:"humidity"`
	Pressure    float64   `json:"pressure"`
	Altitude    float64   `json:"altitude"`
	Timestamp   time.Time `json:"timestamp"`
	Backend     string    `json:"backend"`
}
type GPIOData struct {
	Pin     uint32 `json:"pin"`
	Value   int    `json:"value"`
	Backend string `json:"backend"`
}
type UARTData struct {
	Data    []byte `json:"data"`
	Length  int    `json:"length"`
	Backend string `json:"backend"`
}
type SPIData struct {
	RxBuf   []byte `json:"rx_buf"`
	Length  int    `json:"length"`
	Backend string `json:"backend"`
}
