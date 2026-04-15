package cmd

import (
	"encoding/json"
	"fmt"
	"github.com/spf13/cobra"
	"net/http"
	"time"
)

var bme280Cmd = &cobra.Command{Use: "bme280", Short: "BME280 Sensor"}

// [SDOC_LINK: SWR-013]
var bme280ReadCmd = &cobra.Command{
	Use: "read", Short: "BME280 lesen",
	RunE: func(cmd *cobra.Command, args []string) error {
		resp, err := http.Get(apiURL() + "/api/v1/bme280")
		if err != nil {
			return err
		}
		defer resp.Body.Close()
		var d map[string]interface{}
		json.NewDecoder(resp.Body).Decode(&d)
		fmt.Printf("🌡  Temperatur:      %.2f °C\n", d["temperature"])
		fmt.Printf("💧 Luftfeuchtigkeit: %.2f %%\n", d["humidity"])
		fmt.Printf("🔵 Luftdruck:        %.2f hPa\n", d["pressure"])
		fmt.Printf("⛰  Höhe:             %.1f m\n", d["altitude"])
		fmt.Printf("🔧 Backend:          %s\n", d["backend"])
		return nil
	},
}

var bme280StreamCmd = &cobra.Command{
	Use: "stream", Short: "BME280 live streamen",
	RunE: func(cmd *cobra.Command, args []string) error {
		fmt.Println("📡 Stream (Ctrl+C)...")
		for range time.Tick(2 * time.Second) {
			resp, err := http.Get(apiURL() + "/api/v1/bme280")
			if err != nil {
				continue
			}
			var d map[string]interface{}
			json.NewDecoder(resp.Body).Decode(&d)
			resp.Body.Close()
			fmt.Printf("\r🌡 %.2f°C  💧%.1f%%  🔵%.1fhPa  ⛰%.0fm   ",
				d["temperature"], d["humidity"], d["pressure"], d["altitude"])
		}
		return nil
	},
}

func init() {
	rootCmd.AddCommand(bme280Cmd)
	bme280Cmd.AddCommand(bme280ReadCmd)
	bme280Cmd.AddCommand(bme280StreamCmd)
}
