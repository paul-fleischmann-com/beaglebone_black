// [SDOC_LINK: HW-API-007, API-001, API-002, API-003, API-004, API-005, API-006, API-007, API-008, API-009]
package api_test

import (
	"encoding/json"
	"errors"
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
	r.HandleFunc("/api/v1/health", s.HealthHandler).Methods("GET")
	r.HandleFunc("/api/v1/bme280", s.BME280Handler).Methods("GET")
	r.HandleFunc("/api/v1/gpio", s.GPIOAllHandler).Methods("GET")
	r.HandleFunc("/api/v1/gpio/{pin}", s.GPIOReadHandler).Methods("GET")
	r.HandleFunc("/api/v1/gpio/{pin}", s.GPIOWriteHandler).Methods("POST")
	r.HandleFunc("/api/v1/uart/config", s.UARTConfigHandler).Methods("POST")
	r.HandleFunc("/api/v1/uart/send", s.UARTSendHandler).Methods("POST")
	r.HandleFunc("/api/v1/uart/receive", s.UARTReceiveHandler).Methods("GET")
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

// ── API-001: HealthHandler ────────────────────────────────────────────────────

func TestHealthHandler_Returns200WithRequiredFields(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("GET", "/api/v1/health", nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("HealthHandler: got %d, want 200", w.Code)
	}
	var body map[string]string
	if err := json.NewDecoder(w.Body).Decode(&body); err != nil {
		t.Fatalf("HealthHandler: decode JSON: %v", err)
	}
	for _, field := range []string{"status", "backend", "driver", "arch"} {
		if _, ok := body[field]; !ok {
			t.Errorf("HealthHandler: missing field %q in response", field)
		}
	}
}

// ── API-002 / API-003: BME280Handler ─────────────────────────────────────────

func TestBME280Handler_Returns200WithSensorFields(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("GET", "/api/v1/bme280", nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("BME280Handler: got %d, want 200", w.Code)
	}
	var body map[string]interface{}
	if err := json.NewDecoder(w.Body).Decode(&body); err != nil {
		t.Fatalf("BME280Handler: decode JSON: %v", err)
	}
	for _, field := range []string{"temperature", "humidity", "pressure"} {
		if _, ok := body[field]; !ok {
			t.Errorf("BME280Handler: missing field %q in response", field)
		}
	}
}

func TestBME280Handler_DriverError_Returns500(t *testing.T) {
	d := mock.New()
	if err := d.Init(); err != nil {
		t.Fatalf("mock init: %v", err)
	}
	d.BME280Error = errors.New("sensor fault")
	s := &api.Server{HW: d, HWMu: &sync.Mutex{}}
	r := routerFor(s)
	req := httptest.NewRequest("GET", "/api/v1/bme280", nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusInternalServerError {
		t.Errorf("BME280Handler error: got %d, want 500", w.Code)
	}
}

// ── API-004: GPIOReadHandler ──────────────────────────────────────────────────

func TestGPIORead_Returns200WithGPIOFields(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("GET", "/api/v1/gpio/60", nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("GPIOReadHandler: got %d, want 200", w.Code)
	}
	var body map[string]interface{}
	if err := json.NewDecoder(w.Body).Decode(&body); err != nil {
		t.Fatalf("GPIOReadHandler: decode JSON: %v", err)
	}
	for _, field := range []string{"pin", "value", "backend"} {
		if _, ok := body[field]; !ok {
			t.Errorf("GPIOReadHandler: missing field %q in response", field)
		}
	}
}

// ── API-005: GPIOAllHandler ───────────────────────────────────────────────────

func TestGPIOAll_Returns200WithPinsArray(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("GET", "/api/v1/gpio", nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("GPIOAllHandler: got %d, want 200", w.Code)
	}
	var body map[string]interface{}
	if err := json.NewDecoder(w.Body).Decode(&body); err != nil {
		t.Fatalf("GPIOAllHandler: decode JSON: %v", err)
	}
	if _, ok := body["pins"]; !ok {
		t.Error("GPIOAllHandler: missing field \"pins\" in response")
	}
}

// ── API-006: UARTSendHandler ──────────────────────────────────────────────────

func TestUARTSend_ValidJSON_Returns200WithBytesSent(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	payload := `{"data":"aGVsbG8="}` // base64("hello")
	req := httptest.NewRequest("POST", "/api/v1/uart/send", strings.NewReader(payload))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("UARTSendHandler: got %d, want 200", w.Code)
	}
	var body map[string]interface{}
	if err := json.NewDecoder(w.Body).Decode(&body); err != nil {
		t.Fatalf("UARTSendHandler: decode JSON: %v", err)
	}
	if _, ok := body["bytes_sent"]; !ok {
		t.Error("UARTSendHandler: missing field \"bytes_sent\" in response")
	}
}

// ── API-007: UARTReceiveHandler ───────────────────────────────────────────────

func TestUARTReceive_Returns200(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	req := httptest.NewRequest("GET", "/api/v1/uart/receive", nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Errorf("UARTReceiveHandler: got %d, want 200", w.Code)
	}
}

// ── API-008: SPITransferHandler ───────────────────────────────────────────────

func TestSPITransfer_ValidJSON_Returns200WithRxBuf(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)
	payload := `{"device":"/dev/spidev0.0","speed":1000000,"tx":"AQID"}` // tx = base64([1,2,3])
	req := httptest.NewRequest("POST", "/api/v1/spi/transfer", strings.NewReader(payload))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("SPITransferHandler: got %d, want 200", w.Code)
	}
	var body map[string]interface{}
	if err := json.NewDecoder(w.Body).Decode(&body); err != nil {
		t.Fatalf("SPITransferHandler: decode JSON: %v", err)
	}
	if _, ok := body["rx_buf"]; !ok {
		t.Error("SPITransferHandler: missing field \"rx_buf\" in response")
	}
}

// ── API-009: Content-Type header ─────────────────────────────────────────────

func TestHandlers_ContentTypeJSON(t *testing.T) {
	s := newTestServer(t)
	r := routerFor(s)

	cases := []struct {
		method string
		path   string
		body   string
	}{
		{"GET", "/api/v1/health", ""},
		{"GET", "/api/v1/bme280", ""},
		{"GET", "/api/v1/gpio", ""},
		{"GET", "/api/v1/gpio/60", ""},
		{"POST", "/api/v1/gpio/60", `{"value":0}`},
		{"POST", "/api/v1/uart/send", `{"data":""}`},
		{"GET", "/api/v1/uart/receive", ""},
		{"POST", "/api/v1/spi/transfer", `{"device":"/dev/spidev0.0","speed":1000000,"tx":""}`},
	}

	for _, tc := range cases {
		var body *strings.Reader
		if tc.body != "" {
			body = strings.NewReader(tc.body)
		} else {
			body = strings.NewReader("")
		}
		req := httptest.NewRequest(tc.method, tc.path, body)
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()
		r.ServeHTTP(w, req)
		ct := w.Header().Get("Content-Type")
		if !strings.HasPrefix(ct, "application/json") {
			t.Errorf("%s %s: Content-Type = %q, want application/json", tc.method, tc.path, ct)
		}
	}
}
