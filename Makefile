# ── Version ───────────────────────────────────────────────────────────────────
# Source of truth for the project version.
# Bump manually ONLY when creating an official GitHub Release (git tag vX.Y.Z).
# CI uses this value for build artifacts and release notes.
VERSION = 1.1.0

# ── Cross-compilation ─────────────────────────────────────────────────────────
CROSS   = arm-linux-gnueabihf-
CC      = $(CROSS)gcc
TARGET  = armv7-unknown-linux-musleabihf

all: c-lib rust-lib go-api

c-lib:
	$(MAKE) -C c-lib CC=$(CC)
	cp c-lib/libhardware.so project/go-api/libs/ 2>/dev/null || true

rust-lib:
	cd project/rust-lib && cross build --release --target $(TARGET)
	cp project/rust-lib/target/$(TARGET)/release/libhardware_rs.so project/go-api/libs/ 2>/dev/null || true
	cbindgen --config project/rust-lib/cbindgen.toml --output project/go-api/libs/include/hardware_rs.h 2>/dev/null || true

go-api: c-lib rust-lib
	cd project/go-api && GOOS=linux GOARCH=arm GOARM=7 CGO_ENABLED=1 CC=$(CC) \
	  go build -ldflags="-s -w" -o ../../bin/embedded ./cmd/

cli:
	cd tools/cli && GOOS=linux GOARCH=amd64 CGO_ENABLED=0 \
	  go build -o ../../bin/bbcli-linux-amd64 .

test:
	./scripts/test.sh

test-ci:
	./scripts/test.sh -ci

test-cover:
	./scripts/test.sh -cover -html

lint:
	cd project/go-api && go vet ./pkg/hal/ ./pkg/hal/mock/ ./pkg/hal/config/
	cd tools/cli && go mod tidy && go vet ./...
	cd tools/tui && go mod tidy && go vet ./...
	test -z "$$(gofmt -l project/go-api/ tools/)" || (echo "❌ Formatierung prüfen: gofmt -w ." && exit 1)
	@echo "✅ Lint OK"

test-python:
	pytest tests/api/ -v --timeout=10

tooling-download:
	@echo "⬇️  Tooling herunterladen von beaglebone-tooling (latest release)..."
	mkdir -p tooling
	@curl -sL "https://api.github.com/repos/paulefl/beaglebone-tooling/releases/latest" \
	  | python3 -c "import sys,json; data=json.load(sys.stdin); \
	    asset=next(a for a in data['assets'] if 'tooling-' in a['name']); \
	    print(asset['browser_download_url'])" \
	  | xargs curl -sL | tar xz -C tooling
	chmod +x tooling/*.sh tooling/bausteinsicht
	@echo "✅ Tooling in tooling/ bereit"

test-report:
	./scripts/report.sh

test-report-open:
	./scripts/report.sh --open

deploy:
	scp bin/embedded project/go-api/libs/libhardware.so project/go-api/libs/libhardware_rs.so \
	  debian@192.168.7.2:/app/
	ssh debian@192.168.7.2 "systemctl restart embedded-sw"

req-tracing: tooling-download
	strictdoc --debug export . --formats html     --output-dir output/strictdoc
	strictdoc --debug export . --formats html2pdf --output-dir output/strictdoc
	strictdoc --debug export . --formats excel    --output-dir output/strictdoc
	strictdoc --debug export . --formats reqif-sdoc --output-dir output/strictdoc
	python3 tooling/req_tracing_summary.py

clean:
	$(MAKE) -C c-lib clean
	cd project/rust-lib && cargo clean
	rm -f bin/embedded bin/bbcli-*

version:
	@echo "$(VERSION)"

.PHONY: all c-lib rust-lib go-api cli test test-ci test-cover lint test-python tooling-download test-report test-report-open deploy clean req-tracing version
