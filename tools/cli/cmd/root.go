package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"os"
)

var (
	cfgFile, host string
	port          int
	verbose       bool
)

var rootCmd = &cobra.Command{
	Use:   "bbcli",
	Short: "BeagleBone Black CLI",
	Long:  `BeagleBone Black Konfigurationstool`,
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
func init() {
	cobra.OnInitialize(initConfig)
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "Config Datei")
	rootCmd.PersistentFlags().StringVarP(&host, "host", "H", "192.168.7.2", "BeagleBone Host")
	rootCmd.PersistentFlags().IntVarP(&port, "port", "p", 5000, "API Port")
	rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "Ausführlich")
	viper.BindPFlag("host", rootCmd.PersistentFlags().Lookup("host"))
}
func initConfig() {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		home, _ := os.UserHomeDir()
		viper.AddConfigPath(home)
		viper.SetConfigName(".bbcli")
		viper.SetConfigType("yaml")
	}
	viper.AutomaticEnv()
	viper.ReadInConfig()
}

// [SDOC_LINK: SWR-013]
func apiURL() string { return fmt.Sprintf("http://%s:%d", host, port) }
