// Package e2edemo implements the minimal REST → CAN → ACF-CAN (IEEE 1722) →
// CAN → BME280 demo chain from Issue #270. It intentionally defines only a
// single request/response pair for the temperature — a full BME280 CAN
// protocol (humidity/pressure/altitude) is a possible future extension, not
// part of this MVP.
package e2edemo

import (
	"encoding/binary"
	"fmt"
	"math"
)

const (
	// RequestCANID is sent by the REST↔CAN-Gateway (D2) with an empty
	// payload to request the current temperature.
	RequestCANID uint32 = 0x100
	// ResponseCANID carries the temperature as a big-endian float32 (4
	// bytes) back from the CAN→HAL-Bridge (D5).
	ResponseCANID uint32 = 0x101
)

// EncodeResponse serializes a temperature reading into the 4-byte
// big-endian float32 payload used on ResponseCANID.
func EncodeResponse(temperature float32) []byte {
	buf := make([]byte, 4)
	binary.BigEndian.PutUint32(buf, math.Float32bits(temperature))
	return buf
}

// DecodeResponse parses the payload of a ResponseCANID frame back into a
// temperature value.
func DecodeResponse(data []byte) (float32, error) {
	if len(data) != 4 {
		return 0, fmt.Errorf("ungültige Antwort-Payload-Länge: %d Byte (erwartet 4)", len(data))
	}
	return math.Float32frombits(binary.BigEndian.Uint32(data)), nil
}
