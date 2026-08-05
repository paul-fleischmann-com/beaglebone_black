package main

import (
	"encoding/json"
	"errors"
	"myproject/pkg/e2edemo"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// fakeTransport lets temperatureHandler be tested without a real SocketCAN
// interface — it just remembers what was sent and returns a canned response.
type fakeTransport struct {
	sentID       uint32
	sentData     []byte
	responseID   uint32
	responseData []byte
	responseErr  error
}

func (f *fakeTransport) Send(id uint32, data []byte) error {
	f.sentID = id
	f.sentData = data
	return nil
}

func (f *fakeTransport) Receive(timeout time.Duration) (uint32, []byte, error) {
	if f.responseErr != nil {
		return 0, nil, f.responseErr
	}
	return f.responseID, f.responseData, nil
}

func TestTemperatureHandlerSuccess(t *testing.T) {
	ft := &fakeTransport{
		responseID:   e2edemo.ResponseCANID,
		responseData: e2edemo.EncodeResponse(23.45),
	}
	gw := &gateway{transport: ft, timeout: time.Second}

	req := httptest.NewRequest(http.MethodGet, "/temperature", nil)
	rec := httptest.NewRecorder()
	gw.temperatureHandler(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("erwartete 200, bekam %d (%s)", rec.Code, rec.Body.String())
	}
	if ft.sentID != e2edemo.RequestCANID {
		t.Errorf("erwartete gesendete Request-ID 0x%X, bekam 0x%X", e2edemo.RequestCANID, ft.sentID)
	}

	var body struct {
		Temperature float32 `json:"temperature"`
		Backend     string  `json:"backend"`
	}
	if err := json.NewDecoder(rec.Body).Decode(&body); err != nil {
		t.Fatalf("Antwort konnte nicht dekodiert werden: %v", err)
	}
	if body.Temperature != 23.45 {
		t.Errorf("erwartete Temperatur 23.45, bekam %v", body.Temperature)
	}
	if body.Backend != "e2e-demo" {
		t.Errorf("erwartetes Backend 'e2e-demo', bekam %q", body.Backend)
	}
}

func TestTemperatureHandlerTimeout(t *testing.T) {
	ft := &fakeTransport{responseErr: errors.New("kein Frame empfangen")}
	gw := &gateway{transport: ft, timeout: time.Second}

	req := httptest.NewRequest(http.MethodGet, "/temperature", nil)
	rec := httptest.NewRecorder()
	gw.temperatureHandler(rec, req)

	if rec.Code != http.StatusGatewayTimeout {
		t.Fatalf("erwartete 504, bekam %d", rec.Code)
	}
}

func TestTemperatureHandlerUnexpectedResponseID(t *testing.T) {
	ft := &fakeTransport{responseID: 0x999, responseData: e2edemo.EncodeResponse(1)}
	gw := &gateway{transport: ft, timeout: time.Second}

	req := httptest.NewRequest(http.MethodGet, "/temperature", nil)
	rec := httptest.NewRecorder()
	gw.temperatureHandler(rec, req)

	if rec.Code != http.StatusBadGateway {
		t.Fatalf("erwartete 502, bekam %d", rec.Code)
	}
}

func TestTemperatureHandlerInvalidPayload(t *testing.T) {
	ft := &fakeTransport{responseID: e2edemo.ResponseCANID, responseData: []byte{1, 2}}
	gw := &gateway{transport: ft, timeout: time.Second}

	req := httptest.NewRequest(http.MethodGet, "/temperature", nil)
	rec := httptest.NewRecorder()
	gw.temperatureHandler(rec, req)

	if rec.Code != http.StatusBadGateway {
		t.Fatalf("erwartete 502, bekam %d", rec.Code)
	}
}
