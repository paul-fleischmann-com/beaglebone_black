CC      = arm-linux-gnueabihf-gcc
CFLAGS  = -Wall -Wextra -O2 -fPIC -I../project/c/include
LDFLAGS = -lm -shared
SRCS    = ../project/c/src/bme280.c ../project/c/src/gpio.c ../project/c/src/uart.c ../project/c/src/spi.c
OBJS    = $(SRCS:.c=.o)
TARGET  = libhardware.so
all: $(TARGET)
$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<
install:
	cp $(TARGET) ../project/go-api/libs/
	cp ../project/c/include/*.h ../project/go-api/libs/include/
clean:
	rm -f $(OBJS) $(TARGET) ../project/c/test/test_runner ../project/c/test/*.gcda ../project/c/test/*.gcno ../project/c/test/*.gcov
# ── Coverage (nativer gcc, kein ARM-Cross-Compiler) ──────────────────────────
COV_CC     = gcc
COV_CFLAGS = -Wall -Wextra -O2 -I../project/c/include -fprofile-arcs -ftest-coverage
COV_LDFLAGS = -lm --coverage
TEST_BIN   = ../project/c/test/test_runner
coverage: $(TEST_BIN)
$(TEST_BIN): $(SRCS) ../project/c/test/test_c_lib.c
	$(COV_CC) $(COV_CFLAGS) -o $@ $^ $(COV_LDFLAGS)
test: $(TEST_BIN)
	./$(TEST_BIN)
.PHONY: all install clean coverage test
