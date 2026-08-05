// rest-can-gateway is device D2 of the Issue #270 end-to-end demo
// (REST → CAN → ACF-CAN → CAN → BME280): it exposes a plain
// "GET /temperature" REST endpoint, encodes it as a CAN request frame on the
// CAN interface facing D3, waits (with a timeout) for the CAN response frame
// and answers with JSON — the caller never sees that the value travelled via
// CAN/ACF-CAN/CAN and the HAL underneath.
package main

import (
	"encoding/json"
	"flag"
	"log"
	"myproject/pkg/e2edemo"
	"net/http"
	"os"
	"sync"
	"time"
)

// canTransport is the subset of *e2edemo.Conn the gateway needs — kept as an
// interface so temperatureHandler can be tested with a fake CAN connection
// (see main_test.go) instead of a real SocketCAN interface.
type canTransport interface {
	Send(id uint32, data []byte) error
	Receive(timeout time.Duration) (id uint32, data []byte, err error)
}

type gateway struct {
	transport canTransport
	timeout   time.Duration
	// mu serializes request/response cycles on the shared CAN connection —
	// without it, concurrent HTTP requests could cross-read each other's
	// CAN responses.
	mu sync.Mutex
}

func (g *gateway) temperatureHandler(w http.ResponseWriter, r *http.Request) {
	log.Print("D2 rest-can-gateway: REST-Anfrage GET /temperature empfangen → sende CAN-Anfrage")

	g.mu.Lock()
	defer g.mu.Unlock()

	if err := g.transport.Send(e2edemo.RequestCANID, nil); err != nil {
		log.Printf("D2 rest-can-gateway: CAN-Anfrage fehlgeschlagen: %v", err)
		http.Error(w, "CAN-Anfrage fehlgeschlagen", http.StatusBadGateway)
		return
	}

	id, data, err := g.transport.Receive(g.timeout)
	if err != nil {
		log.Printf("D2 rest-can-gateway: keine CAN-Antwort innerhalb von %s: %v", g.timeout, err)
		http.Error(w, "Timeout beim Warten auf CAN-Antwort", http.StatusGatewayTimeout)
		return
	}
	if id != e2edemo.ResponseCANID {
		log.Printf("D2 rest-can-gateway: unerwartete CAN-Antwort-ID 0x%X", id)
		http.Error(w, "unerwartete CAN-Antwort-ID", http.StatusBadGateway)
		return
	}

	temperature, err := e2edemo.DecodeResponse(data)
	if err != nil {
		log.Printf("D2 rest-can-gateway: CAN-Antwort konnte nicht dekodiert werden: %v", err)
		http.Error(w, "ungültige CAN-Antwort", http.StatusBadGateway)
		return
	}

	log.Printf("D2 rest-can-gateway: CAN-Antwort erhalten (Temperatur %.2f°C) → JSON", temperature)
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]any{
		"temperature": temperature,
		"backend":     "e2e-demo",
	})
}

func main() {
	canIf := flag.String("canif", envOrDefault("GATEWAY_CANIF", ""), "CAN-Interface Richtung D3 (z.B. vxcan-d2)")
	httpAddr := flag.String("http-addr", envOrDefault("GATEWAY_HTTP_ADDR", ":8080"), "Adresse, auf der GET /temperature bereitgestellt wird")
	canTimeout := flag.Duration("can-timeout", 3*time.Second, "wie lange auf die CAN-Antwort gewartet wird")
	flag.Parse()

	if *canIf == "" {
		log.Fatal("--canif (oder GATEWAY_CANIF) ist erforderlich")
	}

	conn, err := e2edemo.Open(*canIf)
	if err != nil {
		log.Fatalf("CAN-Interface %q konnte nicht geöffnet werden: %v", *canIf, err)
	}
	defer conn.Close()

	gw := &gateway{transport: conn, timeout: *canTimeout}
	mux := http.NewServeMux()
	mux.HandleFunc("GET /temperature", gw.temperatureHandler)

	log.Printf("D2 rest-can-gateway: höre auf %s (CAN-Interface %q)", *httpAddr, *canIf)
	log.Fatal(http.ListenAndServe(*httpAddr, mux))
}

func envOrDefault(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
