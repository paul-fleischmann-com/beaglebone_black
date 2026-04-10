// Run `go mod tidy` once to generate go.sum before first build.
module myproject/tools/c_test_runner

go 1.23.0

require github.com/ozontech/allure-go/pkg/allure v0.6.12

require (
	github.com/google/uuid v1.6.0 // indirect
	github.com/pkg/errors v0.9.0 // indirect
)
