package e2edemo

import "testing"

func TestEncodeDecodeResponseRoundtrip(t *testing.T) {
	cases := []float32{0, 23.45, -12.3, 1000000.5}
	for _, temp := range cases {
		encoded := EncodeResponse(temp)
		if len(encoded) != 4 {
			t.Fatalf("EncodeResponse(%v): erwartet 4 Byte, bekommen %d", temp, len(encoded))
		}
		decoded, err := DecodeResponse(encoded)
		if err != nil {
			t.Fatalf("DecodeResponse(%v) fehlgeschlagen: %v", temp, err)
		}
		if decoded != temp {
			t.Errorf("Roundtrip: erwartet %v, bekommen %v", temp, decoded)
		}
	}
}

func TestDecodeResponseWrongLength(t *testing.T) {
	for _, data := range [][]byte{nil, {}, {1, 2, 3}, {1, 2, 3, 4, 5}} {
		if _, err := DecodeResponse(data); err == nil {
			t.Errorf("DecodeResponse(%v): erwarteter Fehler bei falscher Länge, bekam nil", data)
		}
	}
}

func TestCANIDsAreDistinctStandardIDs(t *testing.T) {
	if RequestCANID == ResponseCANID {
		t.Fatal("RequestCANID und ResponseCANID müssen unterschiedlich sein")
	}
	const canSFFMask = 0x7FF // 11-bit Standard-CAN-ID
	if RequestCANID > canSFFMask || ResponseCANID > canSFFMask {
		t.Fatal("beide CAN-IDs müssen als 11-bit Standard-IDs darstellbar sein")
	}
}
