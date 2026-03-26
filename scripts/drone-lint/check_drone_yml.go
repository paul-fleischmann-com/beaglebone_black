package main

import (
	"bytes"
	"fmt"
	"os"
	"strings"

	"gopkg.in/yaml.v2"
)

// ---------------------------------------------------------------------------
// Types mirroring Drone's internal YAML schema
// ---------------------------------------------------------------------------

// Variable handles both plain string values and {from_secret: name} maps.
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
	return fmt.Errorf("expected string or {from_secret: name}")
}

// Parameter handles plugin settings values and {from_secret: name} maps.
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

// Constraint handles both a plain list and {include:[...], exclude:[...]} maps.
// Drone's Constraint type supports both formats.
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
	return fmt.Errorf("expected list or {include:[...], exclude:[...]}")
}

type Step struct {
	Name        string                `yaml:"name"`
	Image       string                `yaml:"image"`
	Commands    []string              `yaml:"commands"`
	Environment map[string]*Variable  `yaml:"environment"`
	Settings    map[string]*Parameter `yaml:"settings"`
	DependsOn   []string              `yaml:"depends_on"`
}

type Trigger struct {
	Event  Constraint `yaml:"event"`
	Branch Constraint `yaml:"branch"`
	Paths  Constraint `yaml:"paths"`
	Ref    Constraint `yaml:"ref"`
	Target Constraint `yaml:"target"`
	Cron   Constraint `yaml:"cron"`
	Repo   Constraint `yaml:"repo"`
	Status Constraint `yaml:"status"`
}

type Pipeline struct {
	Kind      string   `yaml:"kind"`
	Name      string   `yaml:"name"`
	DependsOn []string `yaml:"depends_on"`
	Trigger   Trigger  `yaml:"trigger"`
	Steps     []Step   `yaml:"steps"`
}

// ---------------------------------------------------------------------------
// Semantic checks
// ---------------------------------------------------------------------------

type failure struct {
	pipeline string
	msg      string
}

// checkMultilinePlainScalars scans the raw YAML text for sequence items that
// use multi-line plain scalars (continuation lines more indented than the `- `
// indicator). Some YAML parsers (including certain Drone versions) misparse
// these and report "mapping values are not allowed in this context".
// Safe alternatives: single line, or `| ` block scalar with `\` continuation.
func checkMultilinePlainScalars(data []byte) []failure {
	lines := strings.Split(string(data), "\n")
	var out []failure
	for i := 0; i < len(lines)-1; i++ {
		line := lines[i]
		// Match a block-sequence item: leading spaces, then "- ", then content
		trimmed := strings.TrimLeft(line, " \t")
		if !strings.HasPrefix(trimmed, "- ") {
			continue
		}
		indent := len(line) - len(trimmed) // column of '-'
		content := strings.TrimSpace(trimmed[2:])
		if content == "" {
			continue
		}
		// Skip safe YAML starters: block scalars, quoted strings, flow nodes
		first := content[0]
		if first == '|' || first == '>' || first == '\'' || first == '"' ||
			first == '{' || first == '[' || first == '!' || first == '&' || first == '*' {
			continue
		}
		// Check if next non-empty line is a continuation (more indented)
		for j := i + 1; j < len(lines); j++ {
			next := lines[j]
			if strings.TrimSpace(next) == "" {
				break
			}
			nextIndent := len(next) - len(strings.TrimLeft(next, " \t"))
			if nextIndent > indent+2 {
				out = append(out, failure{
					pipeline: fmt.Sprintf("line %d", i+1),
					msg: fmt.Sprintf(
						"multi-line plain scalar (continuation at line %d) — "+
							"some Drone parsers report 'mapping values are not allowed in this context'. "+
							"Fix: join to one line or use '| ' block scalar with shell '\\' continuation.\n"+
							"          %s\n          %s",
						j+1, strings.TrimSpace(line), strings.TrimSpace(next)),
				})
			}
			break
		}
	}
	return out
}

// checkStepDeps verifies that every step-level depends_on references a step
// that exists in the same pipeline.
func checkStepDeps(p Pipeline) []failure {
	stepNames := make(map[string]bool, len(p.Steps))
	for _, s := range p.Steps {
		stepNames[s.Name] = true
	}
	var out []failure
	for _, step := range p.Steps {
		for _, dep := range step.DependsOn {
			if dep != "" && !stepNames[dep] {
				out = append(out, failure{
					pipeline: p.Name,
					msg:      fmt.Sprintf("step %q depends_on unknown step %q", step.Name, dep),
				})
			}
		}
	}
	return out
}

// checkPipelineDeps verifies pipeline-level depends_on:
//  1. Referenced pipeline name must exist in the file.
//  2. Referenced pipeline must not have trigger.paths — a paths filter makes
//     a pipeline conditional, so it may not run in every build, causing Drone
//     to report "invalid or unknown pipeline dependency".
func checkPipelineDeps(pipelines []Pipeline) []failure {
	byName := make(map[string]*Pipeline, len(pipelines))
	for i := range pipelines {
		byName[pipelines[i].Name] = &pipelines[i]
	}
	var out []failure
	for _, p := range pipelines {
		for _, dep := range p.DependsOn {
			target, ok := byName[dep]
			if !ok {
				out = append(out, failure{
					pipeline: p.Name,
					msg:      fmt.Sprintf("depends_on: pipeline %q does not exist", dep),
				})
				continue
			}
			if len(target.Trigger.Paths.Include) > 0 || len(target.Trigger.Paths.Exclude) > 0 {
				out = append(out, failure{
					pipeline: p.Name,
					msg: fmt.Sprintf(
						"depends_on: %q has trigger.paths — it may not run in every build, "+
							"making this dependency unresolvable (Drone: 'invalid or unknown pipeline dependency')",
						dep),
				})
			}
		}
	}
	return out
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

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
	totalFail := 0
	var pipelines []Pipeline

	// Pass 1: YAML parse with Drone-accurate types.
	// Catches: missing kind, !!map-into-string (plain scalars containing ': ',
	// wrong paths/env format), invalid constraint structure.
	fmt.Println("=== Pass 1: YAML parse (yaml.v2, Drone schema) ===")
	for i, part := range parts {
		var p Pipeline
		if err := yaml.Unmarshal(part, &p); err != nil {
			fmt.Printf("FAIL [doc %2d]: %v\n", i+1, err)
			totalFail++
			continue
		}
		if p.Kind == "" {
			if len(bytes.TrimSpace(part)) > 0 {
				fmt.Printf("FAIL [doc %2d]: missing 'kind'\n", i+1)
				totalFail++
			}
			continue
		}
		fmt.Printf("OK   [doc %2d] kind=%-10s name=%s\n", i+1, p.Kind, p.Name)
		pipelines = append(pipelines, p)
	}

	// Pass 2: semantic checks not expressible in the type system.
	fmt.Println("\n=== Pass 2: semantic checks ===")
	var semFails []failure
	for _, p := range pipelines {
		semFails = append(semFails, checkStepDeps(p)...)
	}
	semFails = append(semFails, checkPipelineDeps(pipelines)...)

	if len(semFails) == 0 {
		fmt.Println("OK   no semantic issues found")
	}
	for _, f := range semFails {
		fmt.Printf("FAIL [%-20s] %s\n", f.pipeline, f.msg)
		totalFail++
	}

	// Summary
	fmt.Println()
	if totalFail > 0 {
		fmt.Printf("RESULT: %d error(s) — %s\n", totalFail, path)
		os.Exit(1)
	}
	fmt.Printf("RESULT: all %d pipeline(s) valid — %s\n", len(pipelines), path)
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

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
