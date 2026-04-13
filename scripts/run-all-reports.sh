#!/bin/bash
# Run reporting chain for all pipelines that ran in this build.
# Requires: DRONE_BUILD_NUMBER, DEPLOY_HOST env vars
# Requires: pipeline-results volume at /pipeline-results
# Requires: www-downloads volume at /var/www/downloads

FAILED=0

report() {
  bash scripts/report-pipeline.sh "$@" || { echo "WARNING: report failed for $1"; FAILED=$((FAILED+1)); }
}

report 1-libraries       build-libraries test-c-lib-pytest test-c-lib-go test-c-lib-cgo test-rust-lib test-go
report 2-embedded-sw     test-hal-unit lint-go build-go-api test-hardware-all-backends
report 3-tools           lint-cli lint-tui build-cli-linux-amd64 build-cli-linux-arm build-cli-darwin-amd64 build-cli-darwin-arm64 build-cli-windows-amd64 build-tui-linux-amd64 build-tui-linux-armv7 build-tui-darwin-amd64 validate-web-gui shellcheck checksums
report 4-webapp          validate-html package-web-gui
report 5-release         build-arm build-tools build-web-gui checksums build-docker-image
report 6-nightly         test-all-backends
report 7-reports         go-tests-with-coverage python-tests python-security shellcheck c-coverage adoc-build strictdoc-export prepare-reports print-url strictdoc-coverage-gate traceability-check sonarqube-report sonarcloud-scan collect-and-report quality-gates package-artifacts
report 8-bausteinsicht   validate-model export-plantuml export-mermaid export-table export-png commit-exports
report 9-build-container build-generic-builder clone-bausteinsicht-repo build-bausteinsicht build-strictdoc
report 10-integration-tests download-release-assets test-hardware test-api test-uart-on-bbb test-cli-remote promote-to-stable
report 11-version-bump   bump-version
report 12-changelog      update-changelog

[ $FAILED -eq 0 ] || exit 1
