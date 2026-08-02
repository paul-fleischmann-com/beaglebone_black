package cmd

import (
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"syscall"

	"github.com/spf13/cobra"
)

// acf-can-bridge (Open1722 User-Space-Tool, siehe Issue #257) läuft NICHT
// über die REST-API/HAL — anders als alle anderen bbcli-Kommandos in diesem
// Paket startet/stoppt dieser Befehl direkt einen lokalen Subprozess auf dem
// Gerät, auf dem bbcli ausgeführt wird (auf der BeagleBone Black selbst,
// analog zur SSH-Ausführung von bbcli in tests/hardware/test_uart.py).

const acfCanPidFile = "/tmp/bbcli-acf-can-bridge.pid"
const acfCanLogFile = "/tmp/bbcli-acf-can-bridge.log"

var acfCanBinary string
var acfCanEthIf string
var acfCanCanIf string
var acfCanDstMac string
var acfCanTalkerStreamID string
var acfCanListenerStreamID string

var acfCanCmd = &cobra.Command{Use: "acf-can", Short: "Open1722 ACF-CAN-Tunneling (Issue #256/#257)"}

var acfCanBridgeCmd = &cobra.Command{Use: "bridge", Short: "acf-can-bridge Prozess verwalten"}

var acfCanBridgeStartCmd = &cobra.Command{
	Use:   "start",
	Short: "Startet acf-can-bridge im Hintergrund",
	RunE: func(cmd *cobra.Command, args []string) error {
		if pid, alive := acfCanBridgeRunning(); alive {
			return fmt.Errorf("acf-can-bridge läuft bereits (PID %d) — zuerst 'bbcli acf-can bridge stop'", pid)
		}
		if acfCanEthIf == "" || acfCanCanIf == "" || acfCanDstMac == "" {
			return fmt.Errorf("--ethif, --canif und --dst-mac sind erforderlich")
		}

		bridgeArgs := []string{"-i", acfCanEthIf, "--canif", acfCanCanIf, "-d", acfCanDstMac}
		if acfCanTalkerStreamID != "" {
			bridgeArgs = append(bridgeArgs, "--talker-stream-id", acfCanTalkerStreamID)
		}
		if acfCanListenerStreamID != "" {
			bridgeArgs = append(bridgeArgs, "--listener-stream-id", acfCanListenerStreamID)
		}

		logFile, err := os.OpenFile(acfCanLogFile, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0644)
		if err != nil {
			return fmt.Errorf("Log-Datei %s konnte nicht angelegt werden: %w", acfCanLogFile, err)
		}
		defer logFile.Close()

		proc := exec.Command(acfCanBinary, bridgeArgs...)
		proc.Stdout = logFile
		proc.Stderr = logFile
		proc.SysProcAttr = &syscall.SysProcAttr{Setsid: true}

		if err := proc.Start(); err != nil {
			return fmt.Errorf("acf-can-bridge konnte nicht gestartet werden: %w", err)
		}
		if err := os.WriteFile(acfCanPidFile, []byte(strconv.Itoa(proc.Process.Pid)), 0644); err != nil {
			return fmt.Errorf("PID-Datei %s konnte nicht geschrieben werden: %w", acfCanPidFile, err)
		}

		fmt.Printf("✅ acf-can-bridge gestartet (PID %d): %s %s\n", proc.Process.Pid, acfCanBinary, strings.Join(bridgeArgs, " "))
		fmt.Printf("   Log: %s\n", acfCanLogFile)
		return nil
	},
}

var acfCanBridgeStopCmd = &cobra.Command{
	Use:   "stop",
	Short: "Stoppt eine laufende acf-can-bridge",
	RunE: func(cmd *cobra.Command, args []string) error {
		pid, alive := acfCanBridgeRunning()
		if !alive {
			return fmt.Errorf("keine laufende acf-can-bridge gefunden (%s)", acfCanPidFile)
		}
		if err := syscall.Kill(-pid, syscall.SIGTERM); err != nil {
			return fmt.Errorf("acf-can-bridge (PID %d) konnte nicht beendet werden: %w", pid, err)
		}
		os.Remove(acfCanPidFile)
		fmt.Printf("✅ acf-can-bridge (PID %d) gestoppt\n", pid)
		return nil
	},
}

var acfCanBridgeStatusCmd = &cobra.Command{
	Use:   "status",
	Short: "Zeigt, ob acf-can-bridge läuft",
	RunE: func(cmd *cobra.Command, args []string) error {
		if pid, alive := acfCanBridgeRunning(); alive {
			fmt.Printf("🔧 acf-can-bridge läuft (PID %d)\n", pid)
		} else {
			fmt.Println("⏹️  acf-can-bridge läuft nicht")
		}
		return nil
	},
}

// acfCanBridgeRunning prüft anhand der PID-Datei, ob der Prozess noch lebt
// (Signal 0 löst keine tatsächliche Zustellung aus, nur eine Existenzprüfung).
func acfCanBridgeRunning() (int, bool) {
	data, err := os.ReadFile(acfCanPidFile)
	if err != nil {
		return 0, false
	}
	pid, err := strconv.Atoi(strings.TrimSpace(string(data)))
	if err != nil {
		return 0, false
	}
	if err := syscall.Kill(pid, 0); err != nil {
		os.Remove(acfCanPidFile)
		return 0, false
	}
	return pid, true
}

func init() {
	rootCmd.AddCommand(acfCanCmd)
	acfCanCmd.AddCommand(acfCanBridgeCmd)
	acfCanBridgeCmd.AddCommand(acfCanBridgeStartCmd)
	acfCanBridgeCmd.AddCommand(acfCanBridgeStopCmd)
	acfCanBridgeCmd.AddCommand(acfCanBridgeStatusCmd)

	acfCanBridgeStartCmd.Flags().StringVar(&acfCanBinary, "binary", "/app/open1722/acf-can-bridge", "Pfad zur acf-can-bridge-Binary")
	acfCanBridgeStartCmd.Flags().StringVar(&acfCanEthIf, "ethif", "", "Ethernet-Interface (erforderlich)")
	acfCanBridgeStartCmd.Flags().StringVar(&acfCanCanIf, "canif", "", "CAN-Interface, z.B. vcan0/can0 (erforderlich)")
	acfCanBridgeStartCmd.Flags().StringVar(&acfCanDstMac, "dst-mac", "", "Ziel-MAC-Adresse der Gegenstelle (erforderlich)")
	acfCanBridgeStartCmd.Flags().StringVar(&acfCanTalkerStreamID, "talker-stream-id", "", "Talker-Stream-ID (hex, optional)")
	acfCanBridgeStartCmd.Flags().StringVar(&acfCanListenerStreamID, "listener-stream-id", "", "Listener-Stream-ID (hex, optional)")
}
