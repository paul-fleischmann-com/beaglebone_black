package main

import (
	"bytes"
	"fmt"
	"os"

	"gopkg.in/yaml.v2"
)

// Variable mirrors Drone's secret-or-value environment type.
type Variable struct {
	Value  string
	Secret string
}

func (v *Variable) UnmarshalYAML(unmarshal func(interface{}) error) error {
	var s string
	if err := unmarshal(&s); err == nil {
		v.Value = s
		return nil
	}
	var m map[string]string
	if err := unmarshal(&m); err == nil {
		v.Secret = m["from_secret"]
		return nil
	}
	return fmt.Errorf("invalid variable (expected string or {from_secret: name})")
}

// Parameter mirrors Drone's plugin settings type.
type Parameter struct {
	Value  interface{}
	Secret string
}

func (p *Parameter) UnmarshalYAML(unmarshal func(interface{}) error) error {
	var s string
	if err := unmarshal(&s); err == nil {
		p.Value = s
		return nil
	}
	var m map[string]string
	if err := unmarshal(&m); err == nil {
		p.Secret = m["from_secret"]
		return nil
	}
	var i interface{}
	if err := unmarshal(&i); err == nil {
		p.Value = i
		return nil
	}
	return fmt.Errorf("invalid parameter")
}

// Constraint mirrors Drone's include/exclude trigger constraint.
type Constraint struct {
	Include []string
	Exclude []string
}

func (c *Constraint) UnmarshalYAML(unmarshal func(interface{}) error) error {
	var list []string
	if err := unmarshal(&list); err == nil {
		c.Include = list
		return nil
	}
	var m struct {
		Include []string `yaml:"include"`
		Exclude []string `yaml:"exclude"`
	}
	if err := unmarshal(&m); err == nil {
		c.Include = m.Include
		c.Exclude = m.Exclude
		return nil
	}
	return fmt.Errorf("invalid constraint (expected list or {include: [...], exclude: [...]})")
}

type Step struct {
	Name        string                `yaml:"name"`
	Image       string                `yaml:"image"`
	Commands    []string              `yaml:"commands"`
	Environment map[string]*Variable  `yaml:"environment"`
	Settings    map[string]*Parameter `yaml:"settings"`
}

type Pipeline struct {
	Kind    string `yaml:"kind"`
	Name    string `yaml:"name"`
	Steps   []Step `yaml:"steps"`
	Trigger struct {
		Event  Constraint `yaml:"event"`
		Branch Constraint `yaml:"branch"`
		Paths  Constraint `yaml:"paths"`
		Ref    Constraint `yaml:"ref"`
		Target Constraint `yaml:"target"`
	} `yaml:"trigger"`
}

func main() {
	path := ".drone.yml"
	if len(os.Args) > 1 {
		path = os.Args[1]
	}

	data, err := os.ReadFile(path)
	if err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: cannot read %s: %v\n", path, err)
		os.Exit(1)
	}

	parts := splitDocs(data)
	failures := 0
	pipelineCount := 0

	for i, part := range parts {
		var p Pipeline
		if err := yaml.Unmarshal(part, &p); err != nil {
			fmt.Printf("FAIL: document %d: %v\n", i+1, err)
			failures++
			continue
		}
		if p.Kind == "" {
			if len(bytes.TrimSpace(part)) > 0 {
				fmt.Printf("FAIL: document %d: missing 'kind'\n", i+1)
				failures++
			}
			continue
		}
		pipelineCount++
		fmt.Printf("OK:   document %d — kind=%s name=%s\n", pipelineCount, p.Kind, p.Name)
	}

	fmt.Println()
	if failures > 0 {
		fmt.Printf("%d error(s) found in %s\n", failures, path)
		os.Exit(1)
	}
	fmt.Printf("All %d pipeline(s) in %s are valid.\n", pipelineCount, path)
}

func splitDocs(data []byte) [][]byte {
	var parts [][]byte
	cur := []byte{}
	for _, line := range bytes.Split(data, []byte("\n")) {
		if bytes.Equal(line, []byte("---")) {
			if len(bytes.TrimSpace(cur)) > 0 {
				parts = append(parts, cur)
			}
			cur = []byte{}
		} else {
			cur = append(cur, line...)
			cur = append(cur, '\n')
		}
	}
	if len(bytes.TrimSpace(cur)) > 0 {
		parts = append(parts, cur)
	}
	return parts
}
