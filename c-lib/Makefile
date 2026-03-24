CC      = arm-linux-gnueabihf-gcc
CFLAGS  = -Wall -Wextra -O2 -fPIC -Iinclude
LDFLAGS = -lm -shared
SRCS    = src/bme280.c src/gpio.c src/uart.c src/spi.c
OBJS    = $(SRCS:.c=.o)
TARGET  = libhardware.so
all: $(TARGET)
$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<
install:
	cp $(TARGET) ../project/go-api/libs/
	cp include/*.h ../project/go-api/libs/include/
clean:
	rm -f $(OBJS) $(TARGET) tests/test_runner src/**/*.gcda src/**/*.gcno src/**/*.gcov
# ── Coverage (nativer gcc, kein ARM-Cross-Compiler) ──────────────────────────
COV_CC     = gcc
COV_CFLAGS = -Wall -Wextra -O2 -Iinclude -fprofile-arcs -ftest-coverage
COV_LDFLAGS = -lm --coverage
TEST_BIN   = tests/test_runner
coverage: $(TEST_BIN)
$(TEST_BIN): $(SRCS) tests/test_c_lib.c
	$(COV_CC) $(COV_CFLAGS) -o $@ $^ $(COV_LDFLAGS)
test: $(TEST_BIN)
	./$(TEST_BIN)
.PHONY: all install clean coverage test
