package main

import (
	"encoding/json"
	"log"
	"myproject/pkg/api"
	"myproject/pkg/hal/config"
	"myproject/pkg/hal/loader"
	"net/http"
	"sync"

	"github.com/gorilla/mux"
)

var (
	hw    interface{ Close() }
	hwMu  sync.Mutex
	hwCfg *config.Config
)

func main() {
	hwCfg = config.LoadConfig()
	driver, err := loader.NewDriver(hwCfg)
	if err != nil {
		log.Fatalf("HAL init: %v", err)
	}
	defer driver.Close()
	log.Printf("Driver: %s Backend: %s", driver.Name(), driver.Backend())

	srv := &api.Server{HW: driver, HWMu: &hwMu}
	hw = driver

	r := mux.NewRouter()
	r.HandleFunc("/health", srv.HealthHandler).Methods("GET")
	r.HandleFunc("/api/v1/bme280", srv.BME280Handler).Methods("GET")
	r.HandleFunc("/api/v1/bme280/stream", srv.BME280StreamHandler).Methods("GET")
	r.HandleFunc("/api/v1/gpio", srv.GPIOAllHandler).Methods("GET")
	r.HandleFunc("/api/v1/gpio/{pin}", srv.GPIOReadHandler).Methods("GET")
	r.HandleFunc("/api/v1/gpio/{pin}", srv.GPIOWriteHandler).Methods("POST")
	r.HandleFunc("/api/v1/uart/config", srv.UARTConfigHandler).Methods("POST")
	r.HandleFunc("/api/v1/uart/send", srv.UARTSendHandler).Methods("POST")
	r.HandleFunc("/api/v1/uart/receive", srv.UARTReceiveHandler).Methods("GET")
	r.HandleFunc("/api/v1/spi/transfer", srv.SPITransferHandler).Methods("POST")
	r.HandleFunc("/api/v1/backend", backendHandler(srv)).Methods("POST")

	log.Printf("API läuft auf :5000")
	httpSrv := api.NewHTTPServer(":5000", api.CORSMiddleware(r))
	log.Fatal(httpSrv.ListenAndServe())
}

// backendHandler bleibt in main, da er hw und hwCfg tauscht.
func backendHandler(srv *api.Server) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		var req struct {
			Backend string `json:"backend"`
		}
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "invalid JSON", http.StatusBadRequest)
			return
		}
		cfg := &config.Config{}
		*cfg = *hwCfg
		cfg.Backend = req.Backend
		newDriver, err := loader.NewDriver(cfg)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		hwMu.Lock()
		srv.HW.Close()
		srv.HW = newDriver
		hwMu.Unlock()
		json.NewEncoder(w).Encode(map[string]string{"backend": string(newDriver.Backend()), "status": "ok"})
	}
}
