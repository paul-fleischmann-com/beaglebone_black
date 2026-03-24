Guide for adding a new hardware driver/interface to the BeagleBone Black project.

The user wants to add a new hardware feature: $ARGUMENTS

Follow these steps in order:

1. **C library** (`c-lib/include/` + `c-lib/src/`): Add the header and implementation for the new hardware interface.

2. **Rust library** (`project/rust-lib/src/`): Add a new module (e.g. `newfeature.rs`) and export the functions via FFI in `lib.rs` using `#[no_mangle] pub extern "C"`.

3. **HAL interface** (`project/go-api/pkg/hal/interface.go`): Add the new methods to the `HardwareDriver` interface.

4. **C driver** (`project/go-api/pkg/hal/c/driver.go`): Implement the new interface methods using CGO bindings to the C library.

5. **Rust driver** (`project/go-api/pkg/hal/rust/driver.go`): Implement the new interface methods using FFI bindings to the Rust library.

6. **Mock driver** (`project/go-api/pkg/hal/mock/driver.go`): Add stub implementations returning test data.

7. **API handler** (`project/go-api/pkg/api/`): Add HTTP handler and register new route in `cmd/main.go`.

8. **Tests**: Add unit tests in `project/go-api/pkg/hal/hal_test.go` using the mock driver.

Remind the user: hardware access must only happen in C and Rust, never directly in Go.
