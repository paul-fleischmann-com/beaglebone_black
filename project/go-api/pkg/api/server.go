package api

import (
	"net/http"
	"time"
)

// CORSMiddleware setzt CORS-Header auf alle Responses und beantwortet OPTIONS-Preflight
// mit 200 OK, damit Browser Cross-Origin POST/PUT-Requests durchlassen.
func CORSMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}
		next.ServeHTTP(w, r)
	})
}

// NewHTTPServer erstellt einen http.Server mit konfigurierten Timeouts (SWR-006).
// Verhindert Ressourcenerschöpfung durch hängende Verbindungen auf eingebetteten Systemen.
func NewHTTPServer(addr string, handler http.Handler) *http.Server {
	return &http.Server{
		Addr:         addr,
		Handler:      handler,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 30 * time.Second,
		IdleTimeout:  60 * time.Second,
	}
}
