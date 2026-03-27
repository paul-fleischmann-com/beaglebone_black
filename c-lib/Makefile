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
	rm -f $(OBJS) $(TARGET) \
	  ../project/c/test/test_runner \
	  ../project/c/test/*.gcda \
	  ../project/c/test/*.gcno \
	  ../project/c/test/*.gcov \
	  ../project/c/test/unity.c \
	  ../project/c/test/unity.h \
	  ../project/c/test/unity_internals.h

# ── Unity test framework ──────────────────────────────────────────────────────
UNITY_VERSION  = v2.6.0
UNITY_BASE_URL = https://raw.githubusercontent.com/ThrowTheSwitch/Unity/$(UNITY_VERSION)/src
UNITY_DIR      = ../project/c/test
UNITY_SRC      = $(UNITY_DIR)/unity.c
UNITY_HDR      = $(UNITY_DIR)/unity.h $(UNITY_DIR)/unity_internals.h

$(UNITY_SRC):
	wget -q "$(UNITY_BASE_URL)/unity.c"         -O $(UNITY_DIR)/unity.c
	wget -q "$(UNITY_BASE_URL)/unity.h"         -O $(UNITY_DIR)/unity.h
	wget -q "$(UNITY_BASE_URL)/unity_internals.h" -O $(UNITY_DIR)/unity_internals.h

# ── Coverage (nativer gcc, kein ARM-Cross-Compiler) ──────────────────────────
COV_CC      = gcc
COV_CFLAGS  = -Wall -Wextra -O2 \
              -I../project/c/include \
              -I$(UNITY_DIR) \
              -fprofile-arcs -ftest-coverage
COV_LDFLAGS = -lm --coverage
TEST_BIN    = ../project/c/test/test_runner
JUNIT_OUT   = ../reports/c-unity-junit.xml

coverage: $(UNITY_SRC) $(TEST_BIN)

$(TEST_BIN): $(UNITY_SRC) $(SRCS) ../project/c/test/test_c_lib.c
	$(COV_CC) $(COV_CFLAGS) -o $@ $^ $(COV_LDFLAGS)

test-bin: $(UNITY_SRC) $(TEST_BIN)

test: test-bin
	mkdir -p ../reports
	./$(TEST_BIN) | tee /tmp/unity-output.txt; \
	  python3 ../scripts/unity_to_junit.py c-unity < /tmp/unity-output.txt > $(JUNIT_OUT); \
	  echo "JUnit XML written to $(JUNIT_OUT)"

# Run via pytest+allure-pytest wrapper (writes to allure-results/)
test-pytest: test-bin
	cd .. && python3 -m pytest tests/c_lib/ --alluredir=allure-results -v

# Run via Go wrapper (writes to allure-results/)
test-go: test-bin
	cd ../tools/c_test_runner && go test -v ./... -count=1

.PHONY: all install clean coverage test test-bin test-pytest test-go
