## Beschreibung

<!-- Was wurde geändert und warum? -->

Fixes #<!-- Issue Nummer -->

## Art der Änderung

- [ ] 🐛 Bugfix
- [ ] ✨ Neues Feature
- [ ] ♻️  Refactoring
- [ ] 📚 Dokumentation
- [ ] 🧪 Tests
- [ ] 🔧 CI/CD
- [ ] ⚡ Performance

## Betroffene Komponenten

- [ ] C Library (`c-lib/`)
- [ ] Rust Library (`project/rust-lib/`)
- [ ] Go REST API (`project/go-api/`)
- [ ] HAL Wrapper (`project/go-api/pkg/hal/`)
- [ ] CLI Tools (`tools/cli/`)
- [ ] TUI (`tools/tui/`)
- [ ] Desktop GUI (`tools/desktop-gui/`)
- [ ] Web GUI (`tools/web-gui/`)
- [ ] Tests (`tests/`)
- [ ] CI/CD (`.drone.yml`, `.github/workflows/`)
- [ ] Dokumentation (`arch/`, `reports/`)

## Testen

```bash
# Wie wurde getestet?
cd go-api && go test ./pkg/hal/... -v

# Hardware Tests (falls zutreffend)
BEAGLE_HOST=192.168.7.2 pytest tests/hardware/ -v
```

- [ ] Unit Tests bestehen (`go test ./...`)
- [ ] Race Condition Tests bestehen (`go test -race`)
- [ ] API Tests bestehen (`pytest tests/api/`)
- [ ] Hardware Tests getestet (falls zutreffend)

## Checkliste

- [ ] Code ist formatiert (`gofmt -w .`)
- [ ] Dokumentation aktualisiert (falls nötig)
- [ ] CHANGELOG.md ergänzt
- [ ] Neue HAL-Funktionen → Mock Driver aktualisiert
- [ ] Breaking Changes dokumentiert
