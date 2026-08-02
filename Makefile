# [SDOC_LINK: SWR-009]
# [SDOC_LINK: SWR-012]
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

cli-arm:
	cd tools/cli && GOOS=linux GOARCH=arm GOARM=7 CGO_ENABLED=0 \
	  go build -o ../../bin/bbcli-linux-arm .

yocto-image:
	./scripts/build_yocto.sh

pru-fw:
	./scripts/build_pru_firmware.sh

test:
	./scripts/test.sh

test-ci:
	./scripts/test.sh -ci

test-cover:
	./scripts/test.sh -cover -html

check-drone-yml:
	cd scripts/drone-lint && go run check_drone_yml.go ../../.drone.yml

shellcheck-report:
	@mkdir -p reports
	@TOTAL=0; FAILURES=0; \
	JUNIT=reports/shellcheck-junit.xml; \
	> reports/shellcheck.txt; \
	{ \
	  echo '<?xml version="1.0" encoding="UTF-8"?>'; \
	  echo '<testsuites>'; \
	  for f in scripts/*.sh; do \
	    findings=$$(shellcheck -f gcc "$$f" 2>&1 || true); \
	    count=$$(echo "$$findings" | grep -c '.' 2>/dev/null || echo 0); \
	    TOTAL=$$((TOTAL + 1)); \
	    name=$$(basename "$$f"); \
	    if [ "$$count" -eq 0 ]; then \
	      echo "  <testsuite name=\"shellcheck\" tests=\"1\" failures=\"0\"><testcase name=\"$$name\" classname=\"shellcheck\"/></testsuite>"; \
	    else \
	      FAILURES=$$((FAILURES + 1)); \
	      safe=$$(echo "$$findings" | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g'); \
	      echo "  <testsuite name=\"shellcheck\" tests=\"1\" failures=\"1\"><testcase name=\"$$name\" classname=\"shellcheck\"><failure message=\"$$count finding(s)\">$$safe</failure></testcase></testsuite>"; \
	    fi; \
	    echo "$$findings" >> reports/shellcheck.txt; \
	  done; \
	  echo '</testsuites>'; \
	} > "$$JUNIT"; \
	echo "--- ShellCheck Summary: $$FAILURES/$$TOTAL scripts with findings ---"; \
	[ -s reports/shellcheck.txt ] && cat reports/shellcheck.txt || echo "No findings."

lint:
	cd project/go-api && go vet ./pkg/hal/ ./pkg/hal/mock/ ./pkg/hal/config/
	cd tools/cli && go mod tidy && go vet ./...
	cd tools/tui && go mod tidy && go vet ./...
	test -z "$$(gofmt -l project/go-api/ tools/)" || (echo "❌ Formatierung prüfen: gofmt -w ." && exit 1)
	@echo "✅ Lint OK"

test-python:
	pytest tests/api/ -v --timeout=10


traceability:
	python3 scripts/gen_traceability_matrix.py --output docs/requirements/traceability_matrix.md

traceability-check:
	python3 scripts/gen_traceability_matrix.py --check

aspice-report:
	python3 scripts/gen_aspice_report.py --output docs/reports/aspice_report.md

velocity-report:
	bash scripts/gen_velocity_report.sh --output docs/reports/velocity_report.md

reports: traceability aspice-report velocity-report
	@echo "Alle Reports generiert in docs/reports/"

test-report:
	./scripts/report.sh

test-report-open:
	./scripts/report.sh --open

# CLI running on BBB : 	scp bin/bbcli-linux-arm debian@192.168.7.2:/app/bbcli
deploy:
	scp bin/embedded project/go-api/libs/libhardware.so project/go-api/libs/libhardware_rs.so \
	  debian@192.168.7.2:/app/
	ssh debian@192.168.7.2 "systemctl restart embedded-sw"

req-tracing:
	strictdoc --debug export . --formats html,html2pdf,excel,reqif-sdoc,json --output-dir output/strictdoc
	python3 scripts/req_tracing_summary.py --json output/strictdoc/json/index.json
	cd output && zip -r out_strictdoc.zip strictdoc/
	@echo "✅ output/out_strictdoc.zip erstellt"

install-java:
	sudo apt-get update -qq
	sudo apt-get install -y openjdk-17-jre-headless
	@echo "✅ Java installiert: $$(java -version 2>&1 | head -1)"

install-asciidoctor:
	sudo apt-get update -qq
	sudo apt-get install -y ruby ruby-dev build-essential
	sudo gem install asciidoctor asciidoctor-pdf asciidoctor-diagram asciidoctor-diagram-plantuml rouge
	@echo "✅ Asciidoctor installiert: $$(asciidoctor --version)"

setup-env: install-java install-asciidoctor
	@echo "✅ Entwicklungsumgebung bereit"

adoc-build:
	ROOT_DIR=. OUTPUT_DIR=build/docs bash scripts/build_adoc.sh

adoc-summary:
	OUTPUT_DIR=$${OUTPUT_DIR:-build/docs} bash scripts/adoc_summary.sh

build-arm:
	@echo "=== ARM cross-build (requires generic-builder container) ==="
	mkdir -p bin
	mkdir -p $${HOME}/.cargo/registry $${HOME}/.cargo/git $${HOME}/go/pkg/mod
	podman run --rm \
	  -v "$(CURDIR):/src" \
	  -v "$(CURDIR)/bin:/output" \
	  -v "$${HOME}/.cargo/registry:/root/.cargo/registry" \
	  -v "$${HOME}/.cargo/git:/root/.cargo/git" \
	  -v "$${HOME}/go/pkg/mod:/root/go/pkg/mod" \
	  generic-builder \
	  -c "bash /src/scripts/build-arm.sh"

checksums:
	./scripts/ci-checksums.sh

publish-allure:
	@if [ -z "$(PIPELINE)" ]; then echo "PIPELINE not set"; exit 1; fi
	chmod -R 777 /var/www/downloads/$(PIPELINE) 2>/dev/null || true
	rm -rf /var/www/downloads/$(PIPELINE)
	mkdir -p /var/www/downloads/$(PIPELINE)
	unzip -o allure-report.zip -d /var/www/downloads/$(PIPELINE)/
	cp allure-report.zip /var/www/downloads/$(PIPELINE)/allure-report.zip

report-all:
	bash scripts/run-all-reports.sh

release-candidate:
	VERSION=$(VERSION) ./scripts/ci-release-candidate.sh

prepend-changelog:
	./scripts/ci-prepend-changelog.sh

clean:
	$(MAKE) -C c-lib clean
	cd project/rust-lib && cargo clean
	rm -f bin/embedded bin/bbcli-*

version:
	@echo "$(VERSION)"

info:
	@echo ""
	@echo "BeagleBone Black — Available Make Targets"
	@echo "=========================================="
	@echo ""
	@echo "Build"
	@echo "  all              Build C lib + Rust lib + Go API"
	@echo "  c-lib            Build C shared library (libhardware.so)"
	@echo "  rust-lib         Build Rust shared library (libhardware_rs.so)"
	@echo "  go-api           Build REST API server → bin/embedded"
	@echo "  cli              Build CLI tool (amd64) → bin/bbcli-linux-amd64"
	@echo "  cli-arm          Build CLI tool (ARM) → bin/bbcli-linux-arm"
	@echo "  build-arm        ARM cross-build via generic-builder container"
	@echo "  yocto-image      Build Yocto (Kirkstone) image incl. BME280 layer"
	@echo "  pru-fw           Build PRU1-RPMsg-GPIO-Firmware → bin/pru/bbb-pru1-gpio-ctrl.elf"
	@echo ""
	@echo "Test"
	@echo "  test             Run Go unit tests"
	@echo "  test-ci          Run Go unit tests (CI mode)"
	@echo "  test-cover       Run tests with HTML coverage report"
	@echo "  test-python      Run Python API integration tests"
	@echo "  test-report      Generate test report"
	@echo "  test-report-open Generate and open test report in browser"
	@echo ""
	@echo "Lint & Validation"
	@echo "  lint             Run go vet + gofmt check"
	@echo "  check-drone-yml  Validate .drone.yml syntax"
	@echo ""
	@echo "Reports & Documentation"
	@echo "  reports          Generate all reports (traceability + aspice + velocity)"
	@echo "  traceability     Generate traceability matrix → docs/requirements/"
	@echo "  traceability-check  Check traceability coverage (exit 1 if gaps)"
	@echo "  aspice-report    Generate ASPICE report → docs/reports/"
	@echo "  velocity-report  Generate sprint velocity report → docs/reports/"
	@echo "  req-tracing      Full StrictDoc export (HTML, PDF, Excel, JSON)"
	@echo "  adoc-build       Build AsciiDoc documentation → build/docs/"
	@echo "  adoc-summary     Print AsciiDoc build summary"
	@echo ""
	@echo "CI & Release"
	@echo "  publish-allure   Publish Allure report (PIPELINE=<name> required)"
	@echo "  report-all       Run reporting chain for all pipelines (CI: Pipeline 15)"
	@echo "  checksums        Generate build artifact checksums"
	@echo "  release-candidate  Create release candidate"
	@echo "  prepend-changelog  Prepend latest changelog entry"
	@echo ""
	@echo "Deploy & Setup"
	@echo "  deploy           Deploy to BeagleBone (192.168.7.2)"
	@echo "  setup-env        Install Java + Asciidoctor"
	@echo "  install-java     Install OpenJDK 17"
	@echo "  install-asciidoctor  Install Asciidoctor + plugins"
	@echo ""
	@echo "Misc"
	@echo "  version          Print current project version ($(VERSION))"
	@echo "  clean            Remove build artifacts"
	@echo "  info             Show this help"
	@echo ""

.PHONY: all c-lib rust-lib go-api cli cli-arm yocto-image pru-fw test test-ci test-cover lint shellcheck-report test-python test-report test-report-open traceability traceability-check aspice-report velocity-report reports deploy clean req-tracing version adoc-build adoc-summary build-arm checksums release-candidate prepend-changelog install-java install-asciidoctor setup-env info publish-allure report-all
