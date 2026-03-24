// [SDOC_LINK: HW-API-007]
package api_test

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"

	"myproject/pkg/api"
	mock "myproject/pkg/hal/mock"

	"github.com/gorilla/mux"
)

func newTestServer(t *testing.T) *api.Server {
	t.Helper()
	d := mock.New()
	if err := d.Init(); err != nil {
		t.Fatalf("mock init: %v", err)
	}
	return &api.Server{HW: d, HWMu: &sync.Mutex{}}
}

func routerFor(s *api.Server) *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/api/v1/gpio/{pin}", s.GPIOWriteHandler).Methods("POST")
	r.HandleFunc("/api/v1/uart/config", s.UARTConfigHandler).Methods("POST")
	r.HandleFunc("/api/v1/uart/send", s.UARTSendHandler).Methods("POST")
	r.HandleFunc("/api/v1/spi/transfer", s.SPITransferHandler).Methods("POST")
	return r
}

// nonFlushingWriter ist ein ResponseWriter ohne http.Flusher — für Issue #27.
// Implementiert nur http.ResponseWriter, NICHT http.Flusher.
type nonFlushingWriter struct {
	header http.Header
	code   int
	body   strings.Builder
}

func newNonFlushingWriter() *nonFlushingWriter {
	return &nonFlushingWriter{header: make(http.Header)}
}
func (w *nonFlushingWriter) Header() http.Header         { return w.header }
func (w *nonFlushingWriter) Write(b []byte) (int, error) { return w.body.Write(b) }
func (w *nonFlushingWriter) WriteHeader(code int)        { w.code = code }

// ── Regression Tests: Issue #27 ─────────────────────────────────────────────
// BME280StreamHandler muss 500 zurückgeben wenn ResponseWriter kein Flusher ist.

func TestBME280Stream_NoFlusher_Returns500(t *testing.T) {
	s := newTestServer(t)
	req := httptest.NewRequest("GET", "/api/v1/bme280/stream", nil)
	w := newNonFlushingWriter()
	s.BME280StreamHandler(w, req)
	if w.code != http.StatusInternalServerError {
		t.Errorf("BME280StreamHandler no flusher: got %d, want 500", w.code)
	}
}

// ── Regression Tests: Issue #31 ─────────────────────────────────────────────
// HW-API-007: POST-Handler müssen bei ungültigem JSON 400 zurückgeben.

func TestGPIOWrite_InvalidJSON_Returns400(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("POST", "/api/v1/gpio/60", strings.NewReader("KEIN_JSON"))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusBadRequest {
		t.Errorf("gpioWriteHandler: got %d, want 400", w.Code)
	}
}

func TestUARTConfig_InvalidJSON_Returns400(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("POST", "/api/v1/uart/config", strings.NewReader("{invalid"))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusBadRequest {
		t.Errorf("uartConfigHandler: got %d, want 400", w.Code)
	}
}

func TestUARTConfig_EmptyPort_Returns400(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("POST", "/api/v1/uart/config",
		strings.NewReader(`{"port":"","baud":115200}`))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusBadRequest {
		t.Errorf("uartConfigHandler empty port: got %d, want 400", w.Code)
	}
}

func TestUARTConfig_ZeroBaud_Returns400(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("POST", "/api/v1/uart/config",
		strings.NewReader(`{"port":"/dev/ttyO1","baud":0}`))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusBadRequest {
		t.Errorf("uartConfigHandler zero baud: got %d, want 400", w.Code)
	}
}

func TestUARTSend_InvalidJSON_Returns400(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("POST", "/api/v1/uart/send", strings.NewReader("!!!"))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusBadRequest {
		t.Errorf("uartSendHandler: got %d, want 400", w.Code)
	}
}

func TestSPITransfer_InvalidJSON_Returns400(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("POST", "/api/v1/spi/transfer", strings.NewReader("BAD"))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusBadRequest {
		t.Errorf("spiTransferHandler: got %d, want 400", w.Code)
	}
}

// ── Happy-Path Tests ─────────────────────────────────────────────────────────

func TestGPIOWrite_ValidJSON_Returns200(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("POST", "/api/v1/gpio/60",
		strings.NewReader(`{"value":1}`))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Errorf("gpioWriteHandler valid: got %d, want 200", w.Code)
	}
}

func TestUARTConfig_ValidJSON_Returns200(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("POST", "/api/v1/uart/config",
		strings.NewReader(`{"port":"/dev/ttyO1","baud":115200}`))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Errorf("uartConfigHandler valid: got %d, want 200", w.Code)
	}
}
