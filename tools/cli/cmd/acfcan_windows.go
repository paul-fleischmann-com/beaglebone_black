//go:build windows

package cmd

import (
	"errors"
	"os/exec"
)

// acf-can-bridge (Open1722 User-Space-Tool, siehe Issue #257) ist ein
// Linux-Subprozess, der auf der BeagleBone Black bzw. einem Linux-Devhost
// läuft — es gibt kein acf-can-bridge-Binary für Windows. Windows ist nur
// ein Cross-Build-Target für bbcli selbst (siehe Issue #275); die
// syscall.Setsid/syscall.Kill-basierte Prozessgruppen-Verwaltung aus
// acfcan_unix.go existiert unter Windows nicht, deshalb hier Stubs, die den
// Build nicht brechen, den Befehl zur Laufzeit aber klar ablehnen.

var errAcfCanBridgeUnsupported = errors.New("acf-can-bridge wird unter Windows nicht unterstützt (kein Windows-Binary, siehe Issue #257)")

func acfCanBridgeSupported() error { return errAcfCanBridgeUnsupported }

func setDetachedProcAttr(proc *exec.Cmd) {}

func killProcessGroup(pid int) error { return errAcfCanBridgeUnsupported }

func processAlive(pid int) bool { return false }
