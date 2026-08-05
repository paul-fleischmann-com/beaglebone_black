// can-hal-bridge is device D5 of the Issue #270 end-to-end demo
// (REST → CAN → ACF-CAN → CAN → BME280): it listens on a CAN interface for
// e2edemo.RequestCANID, reads the temperature through the existing HAL
// (pkg/hal, mock by default — see driver_mock.go/driver_real.go) and sends
// it back as e2edemo.ResponseCANID. This is the only component in the demo
// that touches sensor hardware, and it does so exclusively via the existing
// HAL — never directly (see Hardware-Regel in CLAUDE.md).
package main

import (
	"flag"
	"log"
	"myproject/pkg/e2edemo"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	canIf := flag.String("canif", envOrDefault("CANHAL_BRIDGE_CANIF", ""), "CAN-Interface, auf dem D5 lauscht (z.B. vxcan-d5)")
	pollTimeout := flag.Duration("poll-timeout", 1*time.Second, "wie lange Receive() maximal auf ein Frame wartet, bevor auf Shutdown geprüft wird")
	flag.Parse()

	if *canIf == "" {
		log.Fatal("--canif (oder CANHAL_BRIDGE_CANIF) ist erforderlich")
	}

	driver, err := newDriver()
	if err != nil {
		log.Fatalf("HAL-Treiber konnte nicht initialisiert werden: %v", err)
	}
	defer driver.Close()
	log.Printf("D5 can-hal-bridge: HAL-Treiber %q (Backend %s)", driver.Name(), driver.Backend())

	conn, err := e2edemo.Open(*canIf)
	if err != nil {
		log.Fatalf("CAN-Interface %q konnte nicht geöffnet werden: %v", *canIf, err)
	}
	defer conn.Close()
	log.Printf("D5 can-hal-bridge: lausche auf %q (Request-ID 0x%X)", *canIf, e2edemo.RequestCANID)

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)

	for {
		select {
		case <-stop:
			log.Print("D5 can-hal-bridge: beende")
			return
		default:
		}

		id, _, err := conn.Receive(*pollTimeout)
		if err != nil {
			// Erwarteter Fall bei jedem Poll-Timeout ohne eingehendes Frame.
			continue
		}
		if id != e2edemo.RequestCANID {
			continue
		}

		log.Printf("D5 can-hal-bridge: Anfrage empfangen (ID 0x%X) → HAL.BME280Read()", id)
		data, err := driver.BME280Read()
		if err != nil {
			log.Printf("D5 can-hal-bridge: BME280Read fehlgeschlagen: %v", err)
			continue
		}

		payload := e2edemo.EncodeResponse(float32(data.Temperature))
		if err := conn.Send(e2edemo.ResponseCANID, payload); err != nil {
			log.Printf("D5 can-hal-bridge: Antwort konnte nicht gesendet werden: %v", err)
			continue
		}
		log.Printf("D5 can-hal-bridge: Antwort gesendet (ID 0x%X, Temperatur %.2f°C, Backend %s)",
			e2edemo.ResponseCANID, data.Temperature, data.Backend)
	}
}

func envOrDefault(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
