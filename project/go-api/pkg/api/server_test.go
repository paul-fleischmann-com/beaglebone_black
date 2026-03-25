// [SDOC_LINK: SWR-006]
package api_test

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"myproject/pkg/api"
)

// Regression Test für Issue #21:
// NewHTTPServer muss einen http.Server mit konfigurierten Timeouts zurückgeben.
func TestNewHTTPServer_HasTimeouts(t *testing.T) {
	srv := api.NewHTTPServer(":5000", http.NewServeMux())

	if srv.ReadTimeout == 0 {
		t.Error("ReadTimeout ist 0 — muss > 0 sein")
	}
	if srv.WriteTimeout == 0 {
		t.Error("WriteTimeout ist 0 — muss > 0 sein")
	}
	if srv.IdleTimeout == 0 {
		t.Error("IdleTimeout ist 0 — muss > 0 sein")
	}
}

func TestNewHTTPServer_TimeoutValues(t *testing.T) {
	srv := api.NewHTTPServer(":5000", http.NewServeMux())

	if srv.ReadTimeout < 5*time.Second {
		t.Errorf("ReadTimeout zu kurz: %v (min 5s)", srv.ReadTimeout)
	}
	if srv.WriteTimeout < 10*time.Second {
		t.Errorf("WriteTimeout zu kurz: %v (min 10s)", srv.WriteTimeout)
	}
	if srv.IdleTimeout < 30*time.Second {
		t.Errorf("IdleTimeout zu kurz: %v (min 30s)", srv.IdleTimeout)
	}
}

func TestNewHTTPServer_AddrAndHandler(t *testing.T) {
	mux := http.NewServeMux()
	srv := api.NewHTTPServer(":5000", mux)

	if srv.Addr != ":5000" {
		t.Errorf("Addr: got %q, want %q", srv.Addr, ":5000")
	}
	if srv.Handler != mux {
		t.Error("Handler nicht korrekt gesetzt")
	}
}

// Regression Tests für Issue #22: CORS OPTIONS Preflight

func TestCORSMiddleware_SetsHeaders(t *testing.T) {
	handler := api.CORSMiddleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))

	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rr := httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if got := rr.Header().Get("Access-Control-Allow-Origin"); got != "*" {
		t.Errorf("Access-Control-Allow-Origin: got %q, want %q", got, "*")
	}
	if got := rr.Header().Get("Access-Control-Allow-Methods"); got == "" {
		t.Error("Access-Control-Allow-Methods fehlt")
	}
	if got := rr.Header().Get("Access-Control-Allow-Headers"); got == "" {
		t.Error("Access-Control-Allow-Headers fehlt")
	}
}

func TestCORSMiddleware_OptionsReturns200(t *testing.T) {
	handler := api.CORSMiddleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusMethodNotAllowed)
	}))

	req := httptest.NewRequest(http.MethodOptions, "/api/v1/gpio/60", nil)
	rr := httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Errorf("OPTIONS: got %d, want %d", rr.Code, http.StatusOK)
	}
}

func TestCORSMiddleware_OptionsDoesNotCallNext(t *testing.T) {
	called := false
	handler := api.CORSMiddleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		called = true
	}))

	req := httptest.NewRequest(http.MethodOptions, "/", nil)
	rr := httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if called {
		t.Error("Next handler wurde bei OPTIONS aufgerufen — darf nicht passieren")
	}
}
