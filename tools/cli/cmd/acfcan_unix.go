//go:build !windows

package cmd

import (
	"os/exec"
	"syscall"
)

// acfCanBridgeSupported meldet, ob acf-can-bridge auf diesem GOOS grundsätzlich
// unterstützt wird — auf unix-artigen Systemen ja (siehe acfcan_windows.go).
func acfCanBridgeSupported() error { return nil }

// setDetachedProcAttr startet acf-can-bridge in einer eigenen Session
// (Setsid), damit ein SIGTERM an die Prozessgruppe (killProcessGroup) auch
// von bbcli selbst beendeten Terminal-Sessions nicht mit heruntergefahren wird.
func setDetachedProcAttr(proc *exec.Cmd) {
	proc.SysProcAttr = &syscall.SysProcAttr{Setsid: true}
}

// killProcessGroup sendet SIGTERM an die gesamte Prozessgruppe von pid
// (negative PID = Prozessgruppen-Adressierung unter POSIX).
func killProcessGroup(pid int) error {
	return syscall.Kill(-pid, syscall.SIGTERM)
}

// processAlive prüft per Signal 0 (löst keine tatsächliche Zustellung aus,
// nur eine Existenzprüfung), ob pid noch lebt.
func processAlive(pid int) bool {
	return syscall.Kill(pid, 0) == nil
}
