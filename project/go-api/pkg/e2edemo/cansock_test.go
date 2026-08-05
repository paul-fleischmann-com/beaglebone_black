package e2edemo

import (
	"testing"
	"time"
)

// TestConnSendReceiveRoundtrip exercises Open/Send/Receive against a real
// SocketCAN interface. It is skipped wherever that isn't available (e.g. in
// this repo's default CI containers, which have neither the "can"/"vcan"
// kernel modules loaded nor CAP_NET_RAW) — the protocol-level logic is
// already fully covered without hardware in protocol_test.go. To run this
// locally: `sudo modprobe vcan && sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan0`.
func TestConnSendReceiveRoundtrip(t *testing.T) {
	const testIface = "vcan0"

	sender, err := Open(testIface)
	if err != nil {
		t.Skipf("SocketCAN-Interface %q nicht verfügbar, überspringe: %v", testIface, err)
	}
	defer sender.Close()

	receiver, err := Open(testIface)
	if err != nil {
		t.Skipf("zweite Verbindung zu %q fehlgeschlagen, überspringe: %v", testIface, err)
	}
	defer receiver.Close()

	payload := EncodeResponse(23.45)
	if err := sender.Send(ResponseCANID, payload); err != nil {
		t.Fatalf("Send fehlgeschlagen: %v", err)
	}

	id, data, err := receiver.Receive(2 * time.Second)
	if err != nil {
		t.Fatalf("Receive fehlgeschlagen: %v", err)
	}
	if id != ResponseCANID {
		t.Errorf("erwartete ID 0x%X, bekam 0x%X", ResponseCANID, id)
	}
	temp, err := DecodeResponse(data)
	if err != nil {
		t.Fatalf("DecodeResponse fehlgeschlagen: %v", err)
	}
	if temp != 23.45 {
		t.Errorf("erwartete Temperatur 23.45, bekam %v", temp)
	}
}
