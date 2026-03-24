#!/usr/bin/env python3
"""
BeagleBone Black — SW Architektur + CI Report Integration
Erzeugt: Architektur HTML + Architektur PDF + erweitertes Drone YAML
"""
import os
from datetime import datetime

DATUM   = datetime.now().strftime("%d.%m.%Y")
VERSION = "1.0.0"
PROJEKT = "BeagleBone Black Embedded SW"

os.makedirs("/mnt/user-data/outputs", exist_ok=True)

# ════════════════════════════════════════
# 1. SW ARCHITEKTUR HTML
# ════════════════════════════════════════
def generate_arch_html():
    html = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>SW Architektur — BeagleBone Black</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');
  :root {
    --bg:     #060a10;
    --surface:#0d1520;
    --card:   #111c2a;
    --border: #1e3048;
    --blue:   #38bdf8;
    --green:  #4ade80;
    --purple: #c084fc;
    --orange: #fb923c;
    --red:    #f87171;
    --yellow: #fbbf24;
    --gray:   #475569;
    --light:  #94a3b8;
    --white:  #e2e8f0;
  }
  * { box-sizing:border-box; margin:0; padding:0; }
  body {
    font-family:'Syne',sans-serif;
    background:var(--bg); color:var(--white);
    min-height:100vh; overflow-x:hidden;
  }

  /* ── Header ── */
  header {
    padding:2rem 3rem 1.5rem;
    border-bottom:1px solid var(--border);
    display:flex; justify-content:space-between;
    align-items:flex-end;
    background:linear-gradient(180deg,#0a1628 0%,var(--bg) 100%);
  }
  header h1 {
    font-size:1.6rem; font-weight:800;
    background:linear-gradient(135deg,var(--blue),var(--purple));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    letter-spacing:-0.02em;
  }
  .badge {
    font-family:'JetBrains Mono',monospace;
    font-size:0.7rem; color:var(--gray);
    border:1px solid var(--border);
    padding:4px 10px; border-radius:20px;
  }

  main { padding:2rem 3rem; max-width:1400px; margin:0 auto; }

  /* ── Schichten ── */
  .arch-container {
    display:flex; flex-direction:column; gap:0;
    position:relative;
  }

  .layer {
    border:1px solid var(--border);
    border-radius:12px;
    overflow:hidden;
    margin-bottom:0;
    position:relative;
    transition:transform 0.2s;
  }
  .layer:hover { transform:translateX(4px); }

  .layer-header {
    padding:0.6rem 1.25rem;
    display:flex; align-items:center;
    gap:0.75rem; font-size:0.8rem;
    font-weight:700; letter-spacing:0.08em;
    text-transform:uppercase;
  }
  .layer-body {
    padding:1rem 1.25rem 1.25rem;
    display:flex; flex-wrap:wrap; gap:0.75rem;
  }

  /* Layer Farben */
  .l-client  { border-color:#1e3a5f; }
  .l-client  .layer-header { background:#0a1f38; color:var(--blue); }
  .l-tools   { border-color:#2d1b69; }
  .l-tools   .layer-header { background:#170f35; color:var(--purple); }
  .l-api     { border-color:#064e3b; }
  .l-api     .layer-header { background:#022c22; color:var(--green); }
  .l-hal     { border-color:#7c2d12; }
  .l-hal     .layer-header { background:#431407; color:var(--orange); }
  .l-hw      { border-color:#1e1b4b; }
  .l-hw      .layer-header { background:#0f0d2b; color:#818cf8; }
  .l-ci      { border-color:#374151; }
  .l-ci      .layer-header { background:#1f2937; color:var(--yellow); }
  .l-device  { border-color:#4a1942; }
  .l-device  .layer-header { background:#2d0f29; color:#f0abfc; }

  /* ── Komponenten Karten ── */
  .comp {
    background:var(--card);
    border:1px solid var(--border);
    border-radius:8px;
    padding:0.6rem 0.9rem;
    min-width:140px;
    position:relative;
    cursor:default;
    transition:all 0.2s;
  }
  .comp:hover {
    border-color:var(--blue);
    background:#162032;
    transform:translateY(-2px);
    box-shadow:0 4px 20px rgba(56,189,248,0.15);
  }
  .comp-title {
    font-family:'JetBrains Mono',monospace;
    font-size:0.75rem; font-weight:700;
    color:var(--white); margin-bottom:0.2rem;
  }
  .comp-sub {
    font-size:0.65rem; color:var(--gray);
    line-height:1.4;
  }
  .comp-tag {
    position:absolute; top:6px; right:6px;
    font-size:0.55rem; padding:1px 5px;
    border-radius:10px; font-weight:700;
    text-transform:uppercase;
    font-family:'JetBrains Mono',monospace;
  }
  .tag-go     { background:#0d2e1a; color:var(--green); }
  .tag-c      { background:#1a1505; color:var(--yellow); }
  .tag-rust   { background:#2d1206; color:var(--orange); }
  .tag-py     { background:#1a2040; color:var(--blue); }
  .tag-ts     { background:#1a2040; color:#60a5fa; }
  .tag-sh     { background:#1a1a1a; color:var(--light); }
  .tag-yaml   { background:#1a2830; color:#67e8f9; }
  .tag-hw     { background:#2d1b4e; color:var(--purple); }

  /* ── Pfeile zwischen Schichten ── */
  .arrow-row {
    display:flex; justify-content:center;
    align-items:center; padding:0.3rem 0;
    gap:2rem; color:var(--gray);
    font-size:0.7rem; font-family:'JetBrains Mono',monospace;
  }
  .arrow-item {
    display:flex; flex-direction:column;
    align-items:center; gap:2px;
  }
  .arrow-line {
    width:2px; height:20px;
    background:linear-gradient(180deg,
      var(--border),var(--gray));
    position:relative;
  }
  .arrow-line::after {
    content:'▼'; position:absolute;
    bottom:-12px; left:50%;
    transform:translateX(-50%);
    font-size:10px; color:var(--gray);
  }
  .arrow-label { font-size:0.6rem; color:var(--gray); }

  /* ── Datenfluss Legende ── */
  .legend {
    display:flex; flex-wrap:wrap; gap:1rem;
    margin-top:1.5rem;
    padding:1rem 1.25rem;
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:10px;
  }
  .legend-item {
    display:flex; align-items:center;
    gap:0.5rem; font-size:0.75rem;
    color:var(--light);
  }
  .leg-dot {
    width:10px; height:10px;
    border-radius:50%;
    flex-shrink:0;
  }

  /* ── Statistiken ── */
  .stats-row {
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
    gap:1rem; margin-bottom:1.5rem;
  }
  .stat {
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:10px;
    padding:1rem;
    text-align:center;
  }
  .stat-val {
    font-size:1.8rem; font-weight:800;
    font-family:'JetBrains Mono',monospace;
    line-height:1;
  }
  .stat-lbl {
    font-size:0.7rem; color:var(--gray);
    margin-top:4px; text-transform:uppercase;
    letter-spacing:0.05em;
  }

  /* ── Kommunikation Matrix ── */
  .matrix { margin-top:2rem; }
  .matrix h2 {
    font-size:0.9rem; font-weight:700;
    color:var(--light); letter-spacing:0.1em;
    text-transform:uppercase; margin-bottom:1rem;
  }
  .flow-grid {
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
    gap:0.75rem;
  }
  .flow-card {
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:8px;
    padding:0.75rem 1rem;
  }
  .flow-title {
    font-size:0.75rem; font-weight:700;
    color:var(--blue); margin-bottom:0.4rem;
    font-family:'JetBrains Mono',monospace;
  }
  .flow-desc {
    font-size:0.7rem; color:var(--light);
    line-height:1.5;
  }
  .flow-proto {
    display:inline-block;
    margin-top:0.3rem;
    font-size:0.6rem; font-family:'JetBrains Mono',monospace;
    padding:1px 6px; border-radius:4px;
    background:var(--card); color:var(--yellow);
  }

  .section-title {
    font-size:0.8rem; font-weight:700;
    color:var(--gray); letter-spacing:0.12em;
    text-transform:uppercase;
    margin:1.5rem 0 0.75rem;
    padding-left:0.5rem;
    border-left:3px solid var(--blue);
  }
</style>
</head>
<body>

<header>
  <div>
    <h1>BeagleBone Black — SW Architektur</h1>
    <div style="font-size:0.8rem;color:var(--gray);margin-top:4px">
      Embedded SW · HAL Wrapper · REST API · Tools · CI/CD
    </div>
  </div>
  <div style="display:flex;gap:0.5rem;flex-wrap:wrap;justify-content:flex-end">
    <span class="badge">v""" + VERSION + """</span>
    <span class="badge">ARMv7 Cortex-A8</span>
    <span class="badge">""" + DATUM + """</span>
  </div>
</header>

<main>

  <!-- Statistiken -->
  <div class="stats-row" style="margin-top:1.5rem">
    <div class="stat">
      <div class="stat-val" style="color:var(--blue)">3</div>
      <div class="stat-lbl">Sprachen (Go/C/Rust)</div>
    </div>
    <div class="stat">
      <div class="stat-val" style="color:var(--green)">5</div>
      <div class="stat-lbl">Schichten</div>
    </div>
    <div class="stat">
      <div class="stat-val" style="color:var(--purple)">6</div>
      <div class="stat-lbl">Pipelines</div>
    </div>
    <div class="stat">
      <div class="stat-val" style="color:var(--orange)">4</div>
      <div class="stat-lbl">HW Schnittstellen</div>
    </div>
    <div class="stat">
      <div class="stat-val" style="color:var(--yellow)">37</div>
      <div class="stat-lbl">Requirements</div>
    </div>
    <div class="stat">
      <div class="stat-val" style="color:var(--green)">97%</div>
      <div class="stat-lbl">Test Erfolg</div>
    </div>
  </div>

  <div class="section-title">Systemarchitektur</div>

  <!-- Architektur Schichten -->
  <div class="arch-container">

    <!-- Schicht 1: Client / Tools -->
    <div class="layer l-client">
      <div class="layer-header">
        <span>01</span>
        <span>Client Layer — Benutzeroberflächen</span>
      </div>
      <div class="layer-body">
        <div class="comp">
          <span class="comp-tag tag-ts">TS</span>
          <div class="comp-title">Web GUI</div>
          <div class="comp-sub">HTML/CSS/JS<br>Browser · Port 8090</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">Desktop GUI</div>
          <div class="comp-sub">Fyne Framework<br>Linux · Tabs</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">Terminal TUI</div>
          <div class="comp-sub">BubbleTea<br>Multi-Plattform</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">CLI (bbcli)</div>
          <div class="comp-sub">Cobra Framework<br>Shell Completion</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-py">PY</span>
          <div class="comp-title">Test Suite</div>
          <div class="comp-sub">pytest + requests<br>Hardware Tests</div>
        </div>
      </div>
    </div>

    <div class="arrow-row">
      <div class="arrow-item">
        <div class="arrow-label">REST API</div>
        <div class="arrow-line"></div>
      </div>
      <div class="arrow-item">
        <div class="arrow-label">SSE Stream</div>
        <div class="arrow-line"></div>
      </div>
      <div class="arrow-item">
        <div class="arrow-label">HTTP/JSON</div>
        <div class="arrow-line"></div>
      </div>
    </div>

    <!-- Schicht 2: API Layer -->
    <div class="layer l-api">
      <div class="layer-header">
        <span>02</span>
        <span>API Layer — Go REST Server · Port 5000</span>
      </div>
      <div class="layer-body">
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">Router</div>
          <div class="comp-sub">gorilla/mux<br>REST + SSE</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">BME280 Handler</div>
          <div class="comp-sub">/api/v1/bme280<br>GET · Stream</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">GPIO Handler</div>
          <div class="comp-sub">/api/v1/gpio/{pin}<br>GET · POST</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">UART Handler</div>
          <div class="comp-sub">/api/v1/uart<br>send · receive</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">SPI Handler</div>
          <div class="comp-sub">/api/v1/spi<br>transfer</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">Backend Handler</div>
          <div class="comp-sub">/api/v1/backend<br>C · Rust · Auto</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">Health Handler</div>
          <div class="comp-sub">/health<br>Status · Driver</div>
        </div>
      </div>
    </div>

    <div class="arrow-row">
      <div class="arrow-item">
        <div class="arrow-label">CGO (C→Go)</div>
        <div class="arrow-line"></div>
      </div>
      <div class="arrow-item">
        <div class="arrow-label">FFI (Rust→Go)</div>
        <div class="arrow-line"></div>
      </div>
    </div>

    <!-- Schicht 3: HAL -->
    <div class="layer l-hal">
      <div class="layer-header">
        <span>03</span>
        <span>HAL Layer — Hardware Abstraction Layer</span>
      </div>
      <div class="layer-body">
        <div class="comp" style="border-color:#7c2d12">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">HAL Interface</div>
          <div class="comp-sub">HardwareDriver<br>Interface + Factory</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-c">C</span>
          <div class="comp-title">C Driver</div>
          <div class="comp-sub">CGO Bindings<br>libhardware.so</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-rust">RS</span>
          <div class="comp-title">Rust Driver</div>
          <div class="comp-sub">FFI Bindings<br>libhardware_rs.so</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">Auto Driver</div>
          <div class="comp-sub">C→Rust Fallback<br>Laufzeit-Wahl</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-go">GO</span>
          <div class="comp-title">Mock Driver</div>
          <div class="comp-sub">Unit Tests<br>Fehler-Injektion</div>
        </div>
      </div>
    </div>

    <div class="arrow-row">
      <div class="arrow-item">
        <div class="arrow-label">sysfs/ioctl</div>
        <div class="arrow-line"></div>
      </div>
      <div class="arrow-item">
        <div class="arrow-label">I2C/SPI/UART</div>
        <div class="arrow-line"></div>
      </div>
      <div class="arrow-item">
        <div class="arrow-label">Linux Kernel</div>
        <div class="arrow-line"></div>
      </div>
    </div>

    <!-- Schicht 4: HW Libraries -->
    <div class="layer l-hw">
      <div class="layer-header">
        <span>04</span>
        <span>Library Layer — Hardware Implementierungen</span>
      </div>
      <div class="layer-body">
        <div class="comp">
          <span class="comp-tag tag-c">C</span>
          <div class="comp-title">libbme280.c</div>
          <div class="comp-sub">I2C · Bosch Algo<br>Kalibrierung</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-c">C</span>
          <div class="comp-title">libgpio.c</div>
          <div class="comp-sub">sysfs GPIO<br>Export · R/W</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-c">C</span>
          <div class="comp-title">libuart.c</div>
          <div class="comp-sub">termios<br>Serial Port</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-c">C</span>
          <div class="comp-title">libspi.c</div>
          <div class="comp-sub">spidev ioctl<br>Mode 0-3</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-rust">RS</span>
          <div class="comp-title">bme280.rs</div>
          <div class="comp-sub">linux-embedded-hal<br>I2C Safe</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-rust">RS</span>
          <div class="comp-title">gpio.rs</div>
          <div class="comp-sub">sysfs Rust<br>Memory Safe</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-rust">RS</span>
          <div class="comp-title">uart.rs</div>
          <div class="comp-sub">serialport crate<br>Async Ready</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-rust">RS</span>
          <div class="comp-title">spi.rs</div>
          <div class="comp-sub">spidev crate<br>Transfer</div>
        </div>
      </div>
    </div>

    <div class="arrow-row">
      <div class="arrow-item">
        <div class="arrow-label">USB/Ethernet</div>
        <div class="arrow-line"></div>
      </div>
      <div class="arrow-item">
        <div class="arrow-label">SSH Deploy</div>
        <div class="arrow-line"></div>
      </div>
    </div>

    <!-- Schicht 5: Hardware -->
    <div class="layer l-device">
      <div class="layer-header">
        <span>05</span>
        <span>Hardware Layer — BeagleBone Black (ARMv7 Cortex-A8 · 1GHz · 512MB)</span>
      </div>
      <div class="layer-body">
        <div class="comp">
          <span class="comp-tag tag-hw">HW</span>
          <div class="comp-title">BME280</div>
          <div class="comp-sub">I2C Bus 1 · 0x76<br>Temp/Hum/Press</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-hw">HW</span>
          <div class="comp-title">GPIO Pins</div>
          <div class="comp-sub">P8/P9 Header<br>sysfs Interface</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-hw">HW</span>
          <div class="comp-title">UART (ttyO1)</div>
          <div class="comp-sub">P9_24/P9_26<br>115200 Baud</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-hw">HW</span>
          <div class="comp-title">SPI (spidev0.0)</div>
          <div class="comp-sub">P9_17/P9_21/P9_22<br>bis 48 MHz</div>
        </div>
        <div class="comp">
          <span class="comp-tag tag-hw">HW</span>
          <div class="comp-title">Linux (Debian)</div>
          <div class="comp-sub">Kernel 5.x<br>ARMv7 HF</div>
        </div>
      </div>
    </div>

  </div><!-- arch-container -->

  <!-- Kommunikationsflüsse -->
  <div class="matrix">
    <div class="section-title">Kommunikationsflüsse</div>
    <div class="flow-grid">
      <div class="flow-card">
        <div class="flow-title">Browser → BeagleBone</div>
        <div class="flow-desc">Web GUI sendet REST Requests und empfängt SSE Streams direkt vom Go API Server</div>
        <span class="flow-proto">HTTP/REST + SSE</span>
      </div>
      <div class="flow-card">
        <div class="flow-title">Go API → HAL</div>
        <div class="flow-desc">Handler rufen HAL Interface auf. Factory wählt C oder Rust Driver zur Laufzeit</div>
        <span class="flow-proto">Go Interface / CGO / FFI</span>
      </div>
      <div class="flow-card">
        <div class="flow-title">HAL → Linux Kernel</div>
        <div class="flow-desc">C und Rust Libraries greifen über sysfs und ioctl auf Hardware zu</div>
        <span class="flow-proto">sysfs · ioctl · /dev/i2c</span>
      </div>
      <div class="flow-card">
        <div class="flow-title">Drone CI → BeagleBone</div>
        <div class="flow-desc">Pipeline deployt via SSH, startet Systemd Service neu und führt Hardware Tests aus</div>
        <span class="flow-proto">SSH · SCP · systemctl</span>
      </div>
      <div class="flow-card">
        <div class="flow-title">CLI → API</div>
        <div class="flow-desc">bbcli/bbtui/bbgui senden HTTP Requests an Go API. Config aus ~/.bbcli.yaml</div>
        <span class="flow-proto">HTTP/JSON</span>
      </div>
      <div class="flow-card">
        <div class="flow-title">C ↔ Rust Fallback</div>
        <div class="flow-desc">Auto Driver probiert C primär. Bei Fehler automatischer Wechsel auf Rust Backend</div>
        <span class="flow-proto">Go Strategy Pattern</span>
      </div>
    </div>
  </div>

  <!-- CI/CD Schicht -->
  <div class="section-title" style="margin-top:2rem">CI/CD Pipeline</div>
  <div class="layer l-ci" style="margin-bottom:1.5rem">
    <div class="layer-header">
      <span>CI</span>
      <span>Drone CI — 6 Pipelines · Podman Rootless · Gitea</span>
    </div>
    <div class="layer-body">
      <div class="comp">
        <span class="comp-tag tag-yaml">YAML</span>
        <div class="comp-title">1-Libraries</div>
        <div class="comp-sub">C + Rust bauen<br>Unit Tests</div>
      </div>
      <div class="comp">
        <span class="comp-tag tag-go">GO</span>
        <div class="comp-title">2-Embedded SW</div>
        <div class="comp-sub">HAL Tests · API<br>QEMU · Hardware</div>
      </div>
      <div class="comp">
        <span class="comp-tag tag-go">GO</span>
        <div class="comp-title">3-Tools</div>
        <div class="comp-sub">CLI/TUI/GUI<br>Multi-Plattform</div>
      </div>
      <div class="comp">
        <span class="comp-tag tag-ts">TS</span>
        <div class="comp-title">4-WebApp</div>
        <div class="comp-sub">Frontend<br>Build + Test</div>
      </div>
      <div class="comp">
        <span class="comp-tag tag-yaml">YAML</span>
        <div class="comp-title">5-Release</div>
        <div class="comp-sub">Docker · Gitea<br>Checksums</div>
      </div>
      <div class="comp">
        <span class="comp-tag tag-py">PY</span>
        <div class="comp-title">6-Nightly</div>
        <div class="comp-sub">HW Tests täglich<br>Slack Notify</div>
      </div>
      <div class="comp">
        <span class="comp-tag tag-py">PY</span>
        <div class="comp-title">7-Reports</div>
        <div class="comp-sub">HTML · PDF · MD<br>Req. Tracing</div>
      </div>
    </div>
  </div>

  <!-- Legende -->
  <div class="legend">
    <div class="legend-item">
      <div class="leg-dot" style="background:var(--green)"></div>
      <span>Go — API, HAL Interface, CLI/GUI Tools</span>
    </div>
    <div class="legend-item">
      <div class="leg-dot" style="background:var(--yellow)"></div>
      <span>C — Hardware Libraries (CGO)</span>
    </div>
    <div class="legend-item">
      <div class="leg-dot" style="background:var(--orange)"></div>
      <span>Rust — Hardware Libraries (FFI)</span>
    </div>
    <div class="legend-item">
      <div class="leg-dot" style="background:var(--blue)"></div>
      <span>TypeScript/JS — Web GUI, Frontend</span>
    </div>
    <div class="legend-item">
      <div class="leg-dot" style="background:#60a5fa"></div>
      <span>Python — Tests, Report Generator</span>
    </div>
    <div class="legend-item">
      <div class="leg-dot" style="background:var(--purple)"></div>
      <span>Hardware — BeagleBone Black, Sensoren</span>
    </div>
  </div>

</main>
</body>
</html>"""
    path = "/mnt/user-data/outputs/sw_architektur.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ SW Architektur HTML: {path}")

# ════════════════════════════════════════
# 2. SW ARCHITEKTUR PDF
# ════════════════════════════════════════
def generate_arch_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table,
        TableStyle, HRFlowable, PageBreak)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    path = "/mnt/user-data/outputs/sw_architektur.pdf"
    doc  = SimpleDocTemplate(
        path, pagesize=A4,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        leftMargin=1.5*cm, rightMargin=1.5*cm)

    # Farben
    C_BG     = colors.HexColor("#060a10")
    C_CARD   = colors.HexColor("#0d1520")
    C_SURF   = colors.HexColor("#111c2a")
    C_BLUE   = colors.HexColor("#38bdf8")
    C_GREEN  = colors.HexColor("#4ade80")
    C_ORANGE = colors.HexColor("#fb923c")
    C_PURPLE = colors.HexColor("#c084fc")
    C_YELLOW = colors.HexColor("#fbbf24")
    C_RED    = colors.HexColor("#f87171")
    C_GRAY   = colors.HexColor("#475569")
    C_LIGHT  = colors.HexColor("#94a3b8")
    C_WHITE  = colors.HexColor("#e2e8f0")
    C_BORDER = colors.HexColor("#1e3048")

    def S(name, **kw):
        styles = getSampleStyleSheet()
        return ParagraphStyle(name,
            parent=styles["Normal"], **kw)

    sTitle = S("T", fontSize=18, textColor=C_BLUE,
               spaceAfter=4, fontName="Helvetica-Bold",
               alignment=TA_CENTER)
    sSub   = S("S", fontSize=9, textColor=C_GRAY,
               spaceAfter=2, alignment=TA_CENTER)
    sH1    = S("H1", fontSize=11, textColor=C_BLUE,
               spaceBefore=10, spaceAfter=6,
               fontName="Helvetica-Bold")
    sH2    = S("H2", fontSize=9, textColor=C_LIGHT,
               spaceBefore=6, spaceAfter=4,
               fontName="Helvetica-Bold")
    sBody  = S("B", fontSize=8, textColor=C_LIGHT,
               spaceAfter=3, leading=12)
    sSmall = S("SM", fontSize=7, textColor=C_GRAY,
               leading=10)
    sMono  = S("M", fontSize=7, textColor=C_GREEN,
               fontName="Courier")

    def layer_table(title, num, color, rows):
        """Erstellt eine Schicht-Tabelle"""
        header = [[
            Paragraph(f"<b>{num}  {title}</b>",
                S("LH", fontSize=8, textColor=color,
                  fontName="Helvetica-Bold"))
        ]]
        ht = Table(header, colWidths=[17*cm])
        ht.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), C_SURF),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("BOX", (0,0), (-1,-1), 1, color),
        ]))
        # Komponenten Tabelle
        ct = Table(rows, colWidths=[3.4*cm]*5)
        ct.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), C_CARD),
            ("TEXTCOLOR",  (0,0), (-1,-1), C_LIGHT),
            ("FONTSIZE",   (0,0), (-1,-1), 7),
            ("GRID",       (0,0), (-1,-1), 0.3, C_BORDER),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING", (0,0), (-1,-1), 5),
            ("VALIGN",     (0,0), (-1,-1), "TOP"),
        ]))
        return [ht, ct]

    def comp_cell(title, subtitle, lang_color, lang):
        return Paragraph(
            f'<font color="#{lang_color[1:]}">'
            f'<b>[{lang}]</b></font> '
            f'<b>{title}</b><br/>'
            f'<font color="#475569">{subtitle}</font>',
            S("CC", fontSize=7, textColor=C_LIGHT,
              leading=11))

    story = []

    # Hintergrund Funktion
    def bg(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(C_BG)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(C_GRAY)
        canvas.drawString(1.5*cm, 0.8*cm,
            f"{PROJEKT} — SW Architektur v{VERSION}")
        canvas.drawRightString(
            A4[0]-1.5*cm, 0.8*cm,
            f"Seite {doc.page}  |  {DATUM}")
        canvas.restoreState()

    # ── Titel ──
    story += [
        Paragraph("SW Architektur", sTitle),
        Paragraph(PROJEKT, sSub),
        Paragraph(
            f"Version {VERSION}  |  ARMv7 Cortex-A8  |  {DATUM}",
            sSub),
        Spacer(1, 0.4*cm),
        HRFlowable(width="100%", color=C_BLUE, thickness=2),
        Spacer(1, 0.4*cm),
    ]

    # ── Systemübersicht ──
    story.append(Paragraph("Systemübersicht", sH1))

    # KPI Tabelle
    kpi = [
        ["Metrik", "Wert", "Metrik", "Wert"],
        ["Programmiersprachen", "3 (Go/C/Rust)",
         "HW Schnittstellen", "4 (I2C/GPIO/UART/SPI)"],
        ["Architektur-Schichten", "5",
         "CI/CD Pipelines", "6 + Nightly"],
        ["Test Coverage", "83.8% Ø",
         "Test Erfolgsrate", "97.2%"],
        ["Requirements", "37 (94.6% impl.)",
         "Zielplattform", "ARMv7 Cortex-A8"],
        ["Container Runtime", "Podman (rootless)",
         "Git Provider", "Gitea"],
    ]
    kt = Table(kpi, colWidths=[4.25*cm,4*cm,4.25*cm,4*cm])
    kt.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0),  C_SURF),
        ("TEXTCOLOR",   (0,0),(-1,0),  C_BLUE),
        ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 8),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_BG,C_CARD]),
        ("TEXTCOLOR",   (0,1),(-1,-1), C_LIGHT),
        ("GRID",        (0,0),(-1,-1), 0.5, C_BORDER),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
        ("TEXTCOLOR",   (1,1),(-1,-1), C_GREEN),
    ]))
    story += [kt, Spacer(1, 0.5*cm)]

    # ── Schicht Diagramm ──
    story.append(Paragraph("Architektur-Schichten", sH1))

    # Schicht 1: Client
    layers = [
        ("01 — Client Layer", C_BLUE, [
            [comp_cell("Web GUI","HTML/JS · :8090","#38bdf8","TS"),
             comp_cell("Desktop GUI","Fyne · Linux","#4ade80","GO"),
             comp_cell("Terminal TUI","BubbleTea","#4ade80","GO"),
             comp_cell("CLI (bbcli)","Cobra · Completion","#4ade80","GO"),
             comp_cell("Test Suite","pytest · Hardware","#60a5fa","PY")],
        ]),
        ("02 — API Layer (Go REST :5000)", C_GREEN, [
            [comp_cell("Router","gorilla/mux · REST","#4ade80","GO"),
             comp_cell("BME280","GET · Stream","#4ade80","GO"),
             comp_cell("GPIO","GET · POST","#4ade80","GO"),
             comp_cell("UART","send · receive","#4ade80","GO"),
             comp_cell("Backend","C·Rust·Auto","#4ade80","GO")],
        ]),
        ("03 — HAL Layer (Hardware Abstraction)", C_ORANGE, [
            [comp_cell("HAL Interface","Go Interface","#4ade80","GO"),
             comp_cell("C Driver","CGO Bindings","#fbbf24","C"),
             comp_cell("Rust Driver","FFI Bindings","#fb923c","RS"),
             comp_cell("Auto Driver","C→Rust Fallback","#4ade80","GO"),
             comp_cell("Mock Driver","Unit Tests","#4ade80","GO")],
        ]),
        ("04 — Library Layer (C + Rust)", colors.HexColor("#818cf8"), [
            [comp_cell("libbme280","I2C · Bosch Algo","#fbbf24","C"),
             comp_cell("libgpio","sysfs · R/W","#fbbf24","C"),
             comp_cell("libuart","termios","#fbbf24","C"),
             comp_cell("libspi","spidev ioctl","#fbbf24","C"),
             comp_cell("bme280.rs","linux-emb-hal","#fb923c","RS")],
            [comp_cell("gpio.rs","sysfs Rust","#fb923c","RS"),
             comp_cell("uart.rs","serialport","#fb923c","RS"),
             comp_cell("spi.rs","spidev crate","#fb923c","RS"),
             Paragraph("", sSmall),
             Paragraph("", sSmall)],
        ]),
        ("05 — Hardware Layer (ARMv7 · 1GHz · 512MB)", colors.HexColor("#f0abfc"), [
            [comp_cell("BME280","I2C-1 · 0x76","#c084fc","HW"),
             comp_cell("GPIO","P8/P9 · sysfs","#c084fc","HW"),
             comp_cell("UART","ttyO1 · 115200","#c084fc","HW"),
             comp_cell("SPI","spidev0.0","#c084fc","HW"),
             comp_cell("Linux Debian","Kernel 5.x ARMv7","#c084fc","HW")],
        ]),
    ]

    for title, color, rows in layers:
        # Layer Header
        hdr = Table([[
            Paragraph(f"<b>{title}</b>",
                S("LH", fontSize=8, textColor=color,
                  fontName="Helvetica-Bold",
                  backColor=C_SURF))
        ]], colWidths=[17*cm])
        hdr.setStyle(TableStyle([
            ("BACKGROUND", (0,0),(-1,-1), C_SURF),
            ("TOPPADDING", (0,0),(-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("LEFTPADDING", (0,0),(-1,-1), 8),
            ("BOX",        (0,0),(-1,-1), 1.5, color),
        ]))
        story.append(hdr)

        # Komponenten
        for row in rows:
            ct = Table([row], colWidths=[3.4*cm]*5)
            ct.setStyle(TableStyle([
                ("BACKGROUND", (0,0),(-1,-1), C_CARD),
                ("GRID",       (0,0),(-1,-1), 0.3, C_BORDER),
                ("TOPPADDING", (0,0),(-1,-1), 5),
                ("BOTTOMPADDING",(0,0),(-1,-1), 5),
                ("LEFTPADDING", (0,0),(-1,-1), 5),
                ("VALIGN",     (0,0),(-1,-1), "TOP"),
                ("BOX",        (0,0),(-1,-1), 1, color),
            ]))
            story.append(ct)

        # Pfeil nach unten (außer letzte Schicht)
        if title != "05 — Hardware Layer (ARMv7 · 1GHz · 512MB)":
            proto = ("CGO/FFI" if "HAL" in title
                     else "HTTP/REST/SSE" if "API" in title
                     else "sysfs/ioctl" if "Library" in title
                     else "SSH/Deploy")
            arrow_data = [[
                Paragraph(
                    f'<font color="#475569">▼ {proto}</font>',
                    S("A", fontSize=7, textColor=C_GRAY,
                      alignment=TA_CENTER))
            ]]
            at = Table(arrow_data, colWidths=[17*cm])
            at.setStyle(TableStyle([
                ("BACKGROUND", (0,0),(-1,-1), C_BG),
                ("TOPPADDING", (0,0),(-1,-1), 2),
                ("BOTTOMPADDING",(0,0),(-1,-1), 2),
            ]))
            story.append(at)

    story += [Spacer(1, 0.5*cm), PageBreak()]

    # ── Seite 2: Kommunikation + CI/CD ──
    story.append(Paragraph("Kommunikationsflüsse", sH1))

    flows = [
        ["Verbindung", "Protokoll", "Richtung", "Beschreibung"],
        ["Browser → API",      "HTTP/REST+SSE", "bidirektional",
         "Web GUI sendet Requests, empfängt SSE Streams"],
        ["CLI/TUI/GUI → API",  "HTTP/JSON",     "bidirektional",
         "Tools konfigurieren via REST, Config aus ~/.bbcli.yaml"],
        ["Go API → HAL",       "Go Interface",  "synchron",
         "Handler → Factory → C oder Rust Driver"],
        ["HAL → C Library",    "CGO",           "direkt",
         "Go ruft C Funktionen via cgo Bindings auf"],
        ["HAL → Rust Library", "FFI",           "direkt",
         "Go ruft Rust Funktionen via extern C FFI auf"],
        ["C/Rust → Kernel",    "sysfs/ioctl",   "direkt",
         "/sys/class/gpio, /dev/i2c-1, /dev/ttyO1"],
        ["Drone → BeagleBone", "SSH/SCP",       "push",
         "CI deployt Binary + Libraries, restart systemd"],
        ["C ↔ Rust Fallback",  "Go Strategy",  "auto",
         "Auto Driver: Fehler → automatischer Wechsel"],
    ]
    ft = Table(flows, colWidths=[3.5*cm,3*cm,3*cm,7.5*cm])
    ft.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0),  C_SURF),
        ("TEXTCOLOR",   (0,0),(-1,0),  C_BLUE),
        ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 8),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_BG,C_CARD]),
        ("TEXTCOLOR",   (0,1),(-1,-1), C_LIGHT),
        ("GRID",        (0,0),(-1,-1), 0.5, C_BORDER),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
    ]))
    story += [ft, Spacer(1, 0.5*cm)]

    # ── CI/CD ──
    story.append(Paragraph("CI/CD Pipelines", sH1))
    ci_data = [
        ["Pipeline", "Trigger", "Schritte", "Artefakte"],
        ["1-Libraries",  "push/PR/tag",
         "build-c, build-rust, test-c, test-rust",
         "libhardware.so, libhardware_rs.so"],
        ["2-Embedded SW","push/PR/tag",
         "HAL Tests, build-api, QEMU, HW Deploy+Test",
         "embedded-armv7"],
        ["3-Tools",      "push/PR/tag",
         "lint, test, build CLI/TUI/GUI/Web (4 OS)",
         "bbcli/bbtui/bbgui (4 Plattformen)"],
        ["4-WebApp",     "push/PR/tag",
         "test, build, package",
         "webapp.zip"],
        ["5-Release",    "tag only",
         "Docker build, Gitea Release",
         "Alle Artefakte + Checksums"],
        ["6-Nightly",    "cron 02:00",
         "HW Tests C+Rust+Auto, Slack Notify",
         "Test Bericht"],
        ["7-Reports",    "push/tag",
         "Requirements, Tracing, Coverage",
         "HTML, PDF, MD, JSON"],
    ]
    cit = Table(ci_data, colWidths=[3*cm,2.5*cm,6*cm,5.5*cm])
    cit.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0),  C_SURF),
        ("TEXTCOLOR",   (0,0),(-1,0),  C_YELLOW),
        ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 7),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_BG,C_CARD]),
        ("TEXTCOLOR",   (0,1),(-1,-1), C_LIGHT),
        ("GRID",        (0,0),(-1,-1), 0.5, C_BORDER),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING", (0,0),(-1,-1), 5),
        ("TEXTCOLOR",   (1,1),(1,-1),  C_GREEN),
    ]))
    story += [cit, Spacer(1, 0.5*cm)]

    # ── Technologie Stack ──
    story.append(Paragraph("Technologie Stack", sH1))
    stack = [
        ["Kategorie", "Technologie", "Version", "Zweck"],
        ["API Server",    "Go + gorilla/mux",    "1.22",    "REST API, SSE, Routing"],
        ["HW Library C",  "C + libmicrohttpd",   "gcc 12",  "BME280, GPIO, UART, SPI"],
        ["HW Library RS", "Rust + actix-web",    "1.77",    "Memory-safe HW Zugriff"],
        ["CGO Bridge",    "Go CGO",              "builtin", "C Library → Go"],
        ["FFI Bridge",    "cbindgen + extern C",  "0.26",   "Rust Library → Go"],
        ["Desktop GUI",   "Fyne",                "v2",      "Cross-platform Desktop"],
        ["Terminal TUI",  "BubbleTea",           "v0.25",   "Terminal UI"],
        ["CLI",           "Cobra + Viper",       "v1.8",    "Command Line Interface"],
        ["CI/CD",         "Drone CI",            "v2",      "Pipeline Automation"],
        ["Container",     "Podman (rootless)",   "v4",      "Container Runtime"],
        ["Git Server",    "Gitea",               "latest",  "Source + Releases"],
        ["Test Framework","pytest + requests",   "3.12",    "Integration + HW Tests"],
        ["Report Gen",    "Python + ReportLab",  "3.12",    "PDF/HTML/MD Reports"],
    ]
    st = Table(stack, colWidths=[3.5*cm,4*cm,2.5*cm,7*cm])
    st.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0),  C_SURF),
        ("TEXTCOLOR",   (0,0),(-1,0),  C_BLUE),
        ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 7),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_BG,C_CARD]),
        ("TEXTCOLOR",   (0,1),(-1,-1), C_LIGHT),
        ("GRID",        (0,0),(-1,-1), 0.5, C_BORDER),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING", (0,0),(-1,-1), 5),
        ("TEXTCOLOR",   (2,1),(2,-1),  C_YELLOW),
    ]))
    story.append(st)

    doc.build(story, onFirstPage=bg, onLaterPages=bg)
    print(f"✅ SW Architektur PDF: {path}")

# ════════════════════════════════════════
# 3. DRONE CI — REPORT PIPELINE ERWEITERUNG
# ════════════════════════════════════════
def generate_drone_report_pipeline():
    yaml_content = """# ════════════════════════════════════════════════════════
# PIPELINE 7 — Reports & Architektur
# Automatisch generiert bei jedem Push und Tag
# ════════════════════════════════════════════════════════
---
kind: pipeline
type: docker
name: 7-reports

trigger:
  event: [push, pull_request, tag]
  paths:
    include:
      - tests/**
      - requirements.json
      - go-api/**
      - tools/**
      - .drone.yml

depends_on:
  - 2-embedded-sw
  - 3-tools

steps:

  # ── Test Ergebnisse sammeln ───────────
  - name: collect-test-results
    image: python:3.12-alpine
    volumes:
      - name: report-data
        path: /data
    environment:
      BEAGLE_HOST:
        from_secret: beagle_host
    commands:
      - pip install pytest pytest-json-report
          requests --break-system-packages -q
      # HAL Unit Tests
      - cd go-api && go test ./pkg/hal/...
          -v -json > /data/hal_tests.json || true
      # API Integration Tests
      - pytest tests/api/ -v
          --json-report
          --json-report-file=/data/api_tests.json
          --timeout=30 || true
      # Test Resultate zusammenführen
      - python3 - << 'EOF'
import json, os, glob
from datetime import datetime

results = []
# pytest JSON Reports
for f in glob.glob("/data/*_tests.json"):
    try:
        with open(f) as fp:
            data = json.load(fp)
        for t in data.get("tests", []):
            comp = "HAL" if "hal" in f else "API"
            results.append({
                "name":       t["nodeid"].split("::")[-1],
                "status":     t["outcome"].upper()
                              .replace("PASSED","BESTANDEN")
                              .replace("FAILED","FEHLGESCHLAGEN")
                              .replace("SKIPPED","ÜBERSPRUNGEN"),
                "dauer_ms":   int(t.get("duration",0)*1000),
                "komponente": comp
            })
    except Exception as e:
        print(f"Fehler: {e}")

with open("/data/collected_tests.json","w") as f:
    json.dump({"tests": results,
               "timestamp": datetime.now().isoformat()}, f)
print(f"✅ {len(results)} Tests gesammelt")
EOF

  # ── Requirements laden & validieren ───
  - name: validate-requirements
    image: python:3.12-alpine
    volumes:
      - name: report-data
        path: /data
    commands:
      - pip install jsonschema --break-system-packages -q
      - python3 - << 'EOF'
import json, sys

with open("requirements.json") as f:
    reqs = json.load(f)

total = sum(len(k["requirements"])
            for k in reqs["kategorien"])
impl  = sum(
    sum(1 for r in k["requirements"]
        if r["status"] == "IMPLEMENTIERT")
    for k in reqs["kategorien"])

print(f"Requirements: {impl}/{total} implementiert")
print(f"Coverage:     {impl/total*100:.1f}%")

if impl / total < 0.80:
    print("❌ WARNUNG: Weniger als 80% implementiert!")
    sys.exit(1)
print("✅ Requirements Validierung OK")
EOF

  # ── Reports generieren ────────────────
  - name: generate-reports
    image: python:3.12
    volumes:
      - name: report-data
        path: /data
    commands:
      - pip install reportlab jinja2
          --break-system-packages -q
      # Report Generator ausführen
      - python3 scripts/generate_reports.py
      # Architektur generieren
      - python3 arch/generate_arch.py
      # Alle Reports auflisten
      - echo "=== Generierte Reports ==="
      - ls -lh reports/output/
      - echo "==========================="

  # ── Coverage Schwellenwert prüfen ─────
  - name: check-coverage-threshold
    image: python:3.12-alpine
    volumes:
      - name: report-data
        path: /data
    commands:
      - python3 - << 'EOF'
import json, sys

with open("requirements.json") as f:
    data = json.load(f)

all_reqs = [r for k in data["kategorien"]
              for r in k["requirements"]]
avg_cov  = sum(r["abdeckung"] for r in all_reqs) / len(all_reqs)
min_cov  = min(r["abdeckung"] for r in all_reqs)

print(f"Ø Coverage:  {avg_cov:.1f}%")
print(f"Min Coverage: {min_cov}%")

# Schwellenwerte
THRESHOLD_AVG = 75.0
THRESHOLD_MIN = 50.0

failed = []
if avg_cov < THRESHOLD_AVG:
    failed.append(f"Ø Coverage {avg_cov:.1f}% < {THRESHOLD_AVG}%")
if min_cov < THRESHOLD_MIN:
    failed.append(f"Min Coverage {min_cov}% < {THRESHOLD_MIN}%")

if failed:
    for f in failed:
        print(f"❌ {f}")
    sys.exit(1)

print("✅ Coverage Schwellenwerte OK")
EOF

  # ── Test Trend speichern ──────────────
  - name: save-test-trend
    image: python:3.12-alpine
    volumes:
      - name: report-data
        path: /data
    commands:
      - python3 - << 'EOF'
import json, os
from datetime import datetime

trend_file = "reports/test_trend.json"

# Aktuelle Statistiken
with open("requirements.json") as f:
    data = json.load(f)
if os.path.exists("/workspace/test_results.json"):
    with open("/workspace/test_results.json") as f:
        data["test_ergebnisse"] = json.load(f).get("test_ergebnisse", [])
else:
    data.setdefault("test_ergebnisse", [])

tests      = data["test_ergebnisse"]
total      = len(tests)
bestanden  = sum(1 for t in tests if t["status"] == "BESTANDEN")
all_reqs   = [r for k in data["kategorien"]
                for r in k["requirements"]]
avg_cov    = sum(r["abdeckung"] for r in all_reqs) / len(all_reqs)

entry = {
    "timestamp":    datetime.now().isoformat(),
    "commit":       os.getenv("DRONE_COMMIT_SHA","")[:8],
    "branch":       os.getenv("DRONE_BRANCH","main"),
    "total_tests":  total,
    "bestanden":    bestanden,
    "erfolgsrate":  round(bestanden/total*100, 1),
    "avg_coverage": round(avg_cov, 1),
}

# Trend laden oder neu erstellen
trend = []
if os.path.exists(trend_file):
    with open(trend_file) as f:
        trend = json.load(f)

trend.append(entry)
# Nur letzte 50 Einträge behalten
trend = trend[-50:]

with open(trend_file, "w") as f:
    json.dump(trend, f, indent=2)

print(f"✅ Trend gespeichert: {entry['erfolgsrate']}%"
      f" | {entry['avg_coverage']}% Coverage")
EOF

  # ── Reports in Gitea hochladen ────────
  - name: publish-reports
    image: alpine
    volumes:
      - name: report-data
        path: /data
    environment:
      GITEA_TOKEN:
        from_secret: gitea_token
      GITEA_URL:
        from_secret: gitea_url
    commands:
      - apk add --no-cache curl
      # Reports als Wiki-Seite hochladen
      - |
        if [ -f reports/output/bb_report.md ]; then
          curl -sX POST
            "$GITEA_URL/api/v1/repos/admin/beaglebone/wiki/pages"
            -H "Authorization: token $GITEA_TOKEN"
            -H "Content-Type: application/json"
            -d "{
              \\"title\\": \\"Test Report $(date +%Y-%m-%d)\\",
              \\"content_format\\": \\"markdown\\",
              \\"content\\": $(jq -Rs . < reports/output/bb_report.md)
            }" || echo "Wiki Upload übersprungen"
        fi
      - echo "✅ Reports veröffentlicht"
    when:
      branch: [main]
      event:  [push]

  # ── Slack Benachrichtigung ────────────
  - name: notify-reports
    image: plugins/slack
    depends_on:
      - generate-reports
      - check-coverage-threshold
    settings:
      webhook:
        from_secret: slack_webhook
      channel: builds
      template: |
        *{{ repo.name }}* — Report Build {{build.number}}
        Branch: `{{build.branch}}` | Status: *{{build.status}}*
        Reports: HTML Dashboard, PDF, Markdown, JSON
        {{build.link}}
    when:
      status: [success, failure]
      branch: [main]
      event:  [push]

# ════════════════════════════════════════
# Volumes
# ════════════════════════════════════════
volumes:
  - name: report-data
    temp: {}
"""
    path = "/mnt/user-data/outputs/drone_pipeline_reports.yml"
    with open(path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    print(f"✅ Drone Report Pipeline: {path}")

# ════════════════════════════════════════
# Main
# ════════════════════════════════════════
if __name__ == "__main__":
    print(f"\n🏗  Generiere SW Architektur & CI Pipeline...")
    generate_arch_html()
    generate_arch_pdf()
    generate_drone_report_pipeline()
    print(f"\n✅ Alle Dateien erstellt!")
