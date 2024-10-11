package main

import (
	"fmt"
	"io/ioutil"
	"net"
	"strings"
	"time"
)

func main() {
	// Set the switch's IP address and credentials
	ipAddress := "192.168.1.1"
	username := "admin"
	password := "password"

	// Set the file path to save the configuration
	filePath := "switch_config.txt"

	// Connect to the switch via Telnet
	conn, err := net.Dial("tcp", ipAddress+":23")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer conn.Close()

	// Wait for the login prompt
	buf := make([]byte, 1024)
	conn.SetReadDeadline(time.Now().Add(10 * time.Second))
	_, err = conn.Read(buf)
	if err != nil {
		fmt.Println(err)
		return
	}

	// Send the username and password
	fmt.Fprintf(conn, "%s\n", username)
	fmt.Fprintf(conn, "%s\n", password)

	// Wait for the command prompt
	conn.SetReadDeadline(time.Now().Add(10 * time.Second))
	_, err = conn.Read(buf)
	if err != nil {
		fmt.Println(err)
		return
	}

	// Send the command to show the configuration
	fmt.Fprintf(conn, "show running-config\n")

	// Read the configuration
	var config strings.Builder
	for {
		conn.SetReadDeadline(time.Now().Add(10 * time.Second))
		_, err = conn.Read(buf)
		if err != nil {
			break
		}
		config.WriteString(string(buf))
	}

	// Save the configuration to a file
	err = ioutil.WriteFile(filePath, []byte(config.String()), 0644)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Printf("Configuration saved to %s\n", filePath)
}

