/* Compile all C library sources as one translation unit for CGO.
 * CGO picks up every *.c file in the package directory automatically.
 * Paths are relative to this file (tools/c_cgo_test/). */
#include "../../project/c/src/gpio.c"
#include "../../project/c/src/uart.c"
#include "../../project/c/src/spi.c"
#include "../../project/c/src/bme280.c"
