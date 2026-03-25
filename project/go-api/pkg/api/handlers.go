// Package api provides the HTTP handler logic for the BeagleBone Black REST API.
// Handlers are methods on Server, accepting a hal.HardwareDriver interface —
// this makes them testable without CGO or real hardware.
package api

import (
	"encoding/json"
	"fmt"
	"myproject/pkg/hal"
	"net/http"
	"sync"
	"time"

	"github.com/gorilla/mux"
)

const errInvalidBody = "invalid request body: "

// Server holds the shared state for all HTTP handlers.
type Server struct {
	HW   hal.HardwareDriver
	HWMu *sync.Mutex
}

func cors(w http.ResponseWriter) {
	w.Header().Set("Content-Type", "application/json")
}

func (s *Server) HealthHandler(w http.ResponseWriter, r *http.Request) {
	cors(w)
	s.HWMu.Lock()
	hw := s.HW
	s.HWMu.Unlock()
	json.NewEncoder(w).Encode(map[string]string{
		"status": "ok", "backend": string(hw.Backend()), "driver": hw.Name(), "arch": "armv7",
	})
}

func (s *Server) BME280Handler(w http.ResponseWriter, r *http.Request) {
	cors(w)
	s.HWMu.Lock()
	hw := s.HW
	s.HWMu.Unlock()
	data, err := hw.BME280Read()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(data)
}

func (s *Server) BME280StreamHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "streaming unsupported", http.StatusInternalServerError)
		return
	}
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()
	for {
		select {
		case <-r.Context().Done():
			return
		case <-ticker.C:
			s.HWMu.Lock()
			m, err := s.HW.BME280Read()
			s.HWMu.Unlock()
			if err != nil {
				continue
			}
			data, _ := json.Marshal(m)
			fmt.Fprintf(w, "data: %s\n\n", data)
			flusher.Flush()
		}
	}
}

func (s *Server) GPIOAllHandler(w http.ResponseWriter, r *http.Request) {
	cors(w)
	s.HWMu.Lock()
	hw := s.HW
	s.HWMu.Unlock()
	pins := []uint32{60, 61, 66, 67}
	var results []interface{}
	for _, pin := range pins {
		data, err := hw.GPIORead(pin)
		if err == nil {
			results = append(results, data)
		}
	}
	json.NewEncoder(w).Encode(map[string]interface{}{"pins": results})
}

func (s *Server) GPIOReadHandler(w http.ResponseWriter, r *http.Request) {
	cors(w)
	s.HWMu.Lock()
	hw := s.HW
	s.HWMu.Unlock()
	var pin uint32
	fmt.Sscanf(mux.Vars(r)["pin"], "%d", &pin)
	data, err := hw.GPIORead(pin)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(data)
}

func (s *Server) GPIOWriteHandler(w http.ResponseWriter, r *http.Request) {
	cors(w)
	var pin uint32
	fmt.Sscanf(mux.Vars(r)["pin"], "%d", &pin)
	var req struct {
		Value int `json:"value"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, errInvalidBody+err.Error(), http.StatusBadRequest)
		return
	}
	s.HWMu.Lock()
	err := s.HW.GPIOWrite(pin, req.Value)
	s.HWMu.Unlock()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(map[string]interface{}{"pin": pin, "value": req.Value, "status": "ok"})
}

func (s *Server) UARTConfigHandler(w http.ResponseWriter, r *http.Request) {
	cors(w)
	var req struct {
		Port string `json:"port"`
		Baud uint32 `json:"baud"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, errInvalidBody+err.Error(), http.StatusBadRequest)
		return
	}
	if req.Port == "" {
		http.Error(w, "missing required field: port", http.StatusBadRequest)
		return
	}
	if req.Baud == 0 {
		http.Error(w, "missing required field: baud must be > 0", http.StatusBadRequest)
		return
	}
	s.HWMu.Lock()
	err := s.HW.UARTOpen(req.Port, req.Baud)
	s.HWMu.Unlock()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func (s *Server) UARTSendHandler(w http.ResponseWriter, r *http.Request) {
	cors(w)
	var req struct {
		Data []byte `json:"data"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, errInvalidBody+err.Error(), http.StatusBadRequest)
		return
	}
	s.HWMu.Lock()
	n, err := s.HW.UARTWrite(req.Data)
	s.HWMu.Unlock()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(map[string]int{"bytes_sent": n})
}

func (s *Server) UARTReceiveHandler(w http.ResponseWriter, r *http.Request) {
	cors(w)
	s.HWMu.Lock()
	data, err := s.HW.UARTRead(1000)
	s.HWMu.Unlock()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(data)
}

func (s *Server) SPITransferHandler(w http.ResponseWriter, r *http.Request) {
	cors(w)
	var req struct {
		Device string `json:"device"`
		Speed  uint32 `json:"speed"`
		TX     []byte `json:"tx"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, errInvalidBody+err.Error(), http.StatusBadRequest)
		return
	}
	s.HWMu.Lock()
	data, err := s.HW.SPITransfer(req.Device, req.Speed, req.TX)
	s.HWMu.Unlock()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(data)
}
