#!/usr/bin/env python3
"""BeagleBone Black - Report Generator
Erzeugt: HTML Dashboard, JSON Export, Markdown Report, PDF Report
"""
import json
import os
import sys
import argparse
from datetime import datetime
from collections import defaultdict

# ── CLI-Argumente ──────────────────────────
_parser = argparse.ArgumentParser(description="BeagleBone Black Report Generator")
_parser.add_argument("--output", default=os.path.dirname(__file__) or ".",
                     help="Ausgabeverzeichnis (default: Verzeichnis dieses Scripts)")
_parser.add_argument("--trend", default=None,
                     help="Pfad zur test_trend.json Datei (optional)")
_parser.add_argument("--requirements", default=None,
                     help="Pfad zur requirements.json (default: reports/requirements.json)")
_parser.add_argument("--results", default=None,
                     help="Pfad zur test_results.json (default: reports/test_results.json)")
_args, _unknown = _parser.parse_known_args()

OUTPUT_DIR   = _args.output
TREND_FILE   = _args.trend

_repo_root   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIREMENTS = _args.requirements or os.path.join(_repo_root, "reports", "requirements.json")
RESULTS_FILE = _args.results      or os.path.join(_repo_root, "reports", "test_results.json")

# ── Daten laden ──────────────────────────
if not os.path.exists(REQUIREMENTS):
    print(f"❌ requirements.json nicht gefunden: {REQUIREMENTS}", file=sys.stderr)
    sys.exit(1)
with open(REQUIREMENTS) as f:
    data = json.load(f)

# test_results.json laden (dynamischer Teil, optional)
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE) as f:
        data["test_ergebnisse"] = json.load(f).get("test_ergebnisse", [])
    print(f"📥 Test-Ergebnisse geladen: {RESULTS_FILE} ({len(data['test_ergebnisse'])} Einträge)")
else:
    data.setdefault("test_ergebnisse", [])
    print(f"⚠️  test_results.json nicht gefunden — Dashboard zeigt ❓ für alle Tests")

# ── Trend-Daten laden (optional) ──────────
TREND_DATA = []
_trend_sources = [
    TREND_FILE,
    os.path.join(os.path.dirname(__file__) or ".", "test_trend.json"),
    "/trend/test_trend.json",
]
for _ts in _trend_sources:
    if _ts and os.path.exists(_ts):
        with open(_ts) as _f:
            TREND_DATA = json.load(_f)
        print(f"📈 Trend-Daten geladen: {_ts} ({len(TREND_DATA)} Einträge)")
        break

DATUM     = datetime.now().strftime("%d.%m.%Y %H:%M")
PROJEKT   = data["projekt"]
VERSION   = data["version"]
KATEGORIEN = data["kategorien"]
TESTS      = data["test_ergebnisse"]

# ── Statistiken berechnen ─────────────────
def calc_stats():
    total_reqs = sum(len(k["requirements"]) for k in KATEGORIEN)
    impl_reqs  = sum(
        sum(1 for r in k["requirements"] if r["status"] == "IMPLEMENTIERT")
        for k in KATEGORIEN)
    offen_reqs = total_reqs - impl_reqs

    total_tests    = len(TESTS)
    bestanden      = sum(1 for t in TESTS if t["status"] == "BESTANDEN")
    fehlgeschlagen = sum(1 for t in TESTS if t["status"] == "FEHLGESCHLAGEN")
    uebersprungen  = sum(1 for t in TESTS if t["status"] == "ÜBERSPRUNGEN")

    avg_coverage = (sum(
        r["abdeckung"]
        for k in KATEGORIEN for r in k["requirements"]
    ) / total_reqs) if total_reqs else 0.0

    total_dauer = sum(t["dauer_ms"] for t in TESTS)

    return {
        "total_reqs":      total_reqs,
        "impl_reqs":       impl_reqs,
        "offen_reqs":      offen_reqs,
        "req_coverage":    round(impl_reqs / total_reqs * 100, 1) if total_reqs else 0.0,
        "total_tests":     total_tests,
        "bestanden":       bestanden,
        "fehlgeschlagen":  fehlgeschlagen,
        "uebersprungen":   uebersprungen,
        "test_rate":       round(bestanden / total_tests * 100, 1) if total_tests else 0.0,
        "avg_coverage":    round(avg_coverage, 1) if total_reqs else 0.0,
        "total_dauer_ms":  total_dauer,
        "total_dauer_s":   round(total_dauer / 1000, 2),
    }

STATS = calc_stats()

# ════════════════════════════════════════
# 1. JSON Export
# ════════════════════════════════════════
def generate_json():
    export = {
        "meta": {
            "projekt":   PROJEKT,
            "version":   VERSION,
            "datum":     DATUM,
            "generator": "BeagleBone Black Report Generator"
        },
        "statistiken": STATS,
        "kategorien":  KATEGORIEN,
        "test_ergebnisse": TESTS,
        "tracing": generate_tracing_data()
    }
    path = os.path.join(OUTPUT_DIR, "bb_report.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON Export: {path}")

def generate_tracing_data():
    tracing = []
    for kat in KATEGORIEN:
        for req in kat["requirements"]:
            test_results = []
            for t in req["tests"]:
                result = next(
                    (x for x in TESTS if x["name"] == t), None)
                test_results.append({
                    "name":   t,
                    "status": result["status"] if result else "NICHT GEFUNDEN",
                    "dauer_ms": result["dauer_ms"] if result else 0
                })
            tracing.append({
                "req_id":       req["id"],
                "titel":        req["titel"],
                "kategorie":    kat["id"],
                "status":       req["status"],
                "prioritaet":   req["prioritaet"],
                "abdeckung":    req["abdeckung"],
                "tests":        test_results,
                "test_count":   len(req["tests"]),
                "tests_ok":     sum(1 for t in test_results
                                    if t["status"] == "BESTANDEN"),
            })
    return tracing

# ════════════════════════════════════════
# 2. Markdown Report
# ════════════════════════════════════════
def generate_markdown():
    s = STATS
    lines = []
    lines.append(f"# {PROJEKT} — Test & Requirements Report")
    lines.append(f"\n**Version:** {VERSION}  |  **Datum:** {DATUM}")
    lines.append("\n---\n")

    # Zusammenfassung
    lines.append("## Zusammenfassung\n")
    lines.append("### Anforderungen")
    lines.append(f"| Metrik | Wert |")
    lines.append(f"|--------|------|")
    lines.append(f"| Gesamt | {s['total_reqs']} |")
    lines.append(f"| Implementiert | {s['impl_reqs']} |")
    lines.append(f"| Offen | {s['offen_reqs']} |")
    lines.append(f"| Abdeckung | **{s['req_coverage']}%** |")
    lines.append("")
    lines.append("### Tests")
    lines.append(f"| Metrik | Wert |")
    lines.append(f"|--------|------|")
    lines.append(f"| Gesamt | {s['total_tests']} |")
    lines.append(f"| ✅ Bestanden | {s['bestanden']} |")
    lines.append(f"| ❌ Fehlgeschlagen | {s['fehlgeschlagen']} |")
    lines.append(f"| ⚠️ Übersprungen | {s['uebersprungen']} |")
    lines.append(f"| Erfolgsrate | **{s['test_rate']}%** |")
    lines.append(f"| Gesamtdauer | {s['total_dauer_s']}s |")
    lines.append(f"| Ø Code Coverage | **{s['avg_coverage']}%** |")
    lines.append("")

    # Pro Kategorie
    lines.append("---\n")
    lines.append("## Requirements pro Komponente\n")
    for kat in KATEGORIEN:
        reqs = kat["requirements"]
        impl = sum(1 for r in reqs if r["status"] == "IMPLEMENTIERT")
        avg  = sum(r["abdeckung"] for r in reqs) / len(reqs)
        lines.append(f"### {kat['id']} — {kat['name']}")
        lines.append(f"**{impl}/{len(reqs)} implementiert** | "
                     f"Ø Coverage: {avg:.1f}%\n")
        lines.append("| ID | Titel | Priorität | Status | Coverage | Tests |")
        lines.append("|----|-------|-----------|--------|----------|-------|")
        for req in reqs:
            icon = "✅" if req["status"] == "IMPLEMENTIERT" else "🔴"
            lines.append(
                f"| {req['id']} | {req['titel']} | "
                f"{req['prioritaet']} | {icon} {req['status']} | "
                f"{req['abdeckung']}% | {len(req['tests'])} |")
        lines.append("")

    # Requirement Tracing
    lines.append("---\n")
    lines.append("## Requirement Tracing\n")
    for kat in KATEGORIEN:
        lines.append(f"### {kat['name']}\n")
        for req in kat["requirements"]:
            icon = "✅" if req["status"] == "IMPLEMENTIERT" else "🔴"
            lines.append(f"#### {icon} {req['id']} — {req['titel']}")
            lines.append(f"**Beschreibung:** {req['beschreibung']}  ")
            lines.append(f"**Priorität:** {req['prioritaet']} | "
                         f"**Coverage:** {req['abdeckung']}%\n")
            if req["tests"]:
                lines.append("**Verknüpfte Tests:**")
                for t in req["tests"]:
                    result = next(
                        (x for x in TESTS if x["name"] == t), None)
                    if result:
                        icon_t = ("✅" if result["status"] == "BESTANDEN"
                                  else "❌" if result["status"] == "FEHLGESCHLAGEN"
                                  else "⚠️")
                        lines.append(
                            f"- {icon_t} `{t}` "
                            f"({result['dauer_ms']}ms)")
                    else:
                        lines.append(f"- ❓ `{t}` (kein Ergebnis)")
            else:
                lines.append("**Verknüpfte Tests:** *Keine Tests definiert*")
            lines.append("")

    # Fehlgeschlagene Tests
    failed = [t for t in TESTS if t["status"] == "FEHLGESCHLAGEN"]
    if failed:
        lines.append("---\n")
        lines.append("## ❌ Fehlgeschlagene Tests\n")
        lines.append("| Test | Komponente | Dauer |")
        lines.append("|------|------------|-------|")
        for t in failed:
            lines.append(
                f"| `{t['name']}` | {t['komponente']} | "
                f"{t['dauer_ms']}ms |")
        lines.append("")

    # Code Coverage
    lines.append("---\n")
    lines.append("## Code Coverage\n")
    lines.append("| Komponente | Ø Coverage | Status |")
    lines.append("|------------|------------|--------|")
    for kat in KATEGORIEN:
        reqs = kat["requirements"]
        avg  = sum(r["abdeckung"] for r in reqs) / len(reqs)
        icon = "🟢" if avg >= 90 else "🟡" if avg >= 75 else "🔴"
        lines.append(
            f"| {kat['name']} | {avg:.1f}% | {icon} |")

    path = os.path.join(OUTPUT_DIR, "bb_report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Markdown Report: {path}")

# ════════════════════════════════════════
# 3. HTML Dashboard
# ════════════════════════════════════════
def generate_html():
    s = STATS
    # Farb-Hilfsfunktionen
    def status_badge(status):
        colors = {
            "IMPLEMENTIERT": ("#052e16","#22c55e"),
            "OFFEN":         ("#2d0101","#ef4444"),
        }
        bg, fg = colors.get(status, ("#1e293b","#94a3b8"))
        return (f'<span style="background:{bg};color:{fg};'
                f'padding:2px 8px;border-radius:12px;'
                f'font-size:0.75rem;font-weight:600">{status}</span>')

    def prio_badge(prio):
        colors = {
            "HOCH":    ("#7c2d12","#fb923c"),
            "MITTEL":  ("#713f12","#fbbf24"),
            "NIEDRIG": ("#1e3a5f","#60a5fa"),
        }
        bg, fg = colors.get(prio, ("#1e293b","#94a3b8"))
        return (f'<span style="background:{bg};color:{fg};'
                f'padding:2px 8px;border-radius:12px;'
                f'font-size:0.75rem">{prio}</span>')

    def cov_bar(pct):
        color = ("#22c55e" if pct >= 90
                 else "#f59e0b" if pct >= 75 else "#ef4444")
        return (f'<div style="display:flex;align-items:center;gap:8px">'
                f'<div style="flex:1;background:#1e293b;'
                f'border-radius:4px;height:8px">'
                f'<div style="width:{pct}%;background:{color};'
                f'height:8px;border-radius:4px"></div></div>'
                f'<span style="font-size:0.8rem;color:{color};'
                f'min-width:40px">{pct}%</span></div>')

    def test_icon(status):
        return {"BESTANDEN":"✅","FEHLGESCHLAGEN":"❌",
                "ÜBERSPRUNGEN":"⚠️"}.get(status,"❓")

    # Tracing Rows
    tracing_rows = ""
    for kat in KATEGORIEN:
        for req in kat["requirements"]:
            tests_html = ""
            for t in req["tests"]:
                result = next((x for x in TESTS if x["name"] == t), None)
                icon   = test_icon(result["status"]) if result else "❓"
                dur    = f"{result['dauer_ms']}ms" if result else "-"
                tests_html += (
                    f'<div style="font-size:0.75rem;padding:2px 0">'
                    f'{icon} <code style="color:#94a3b8">{t}</code> '
                    f'<span style="color:#475569">{dur}</span></div>')
            tracing_rows += f"""
            <tr>
              <td style="padding:10px 12px;white-space:nowrap">
                <code style="color:{kat['farbe']};font-size:0.85rem">
                  {req['id']}</code></td>
              <td style="padding:10px 12px">
                <div style="font-weight:500">{req['titel']}</div>
                <div style="font-size:0.75rem;color:#64748b;
                  margin-top:3px">{req['beschreibung'][:80]}...</div>
              </td>
              <td style="padding:10px 12px">{prio_badge(req['prioritaet'])}</td>
              <td style="padding:10px 12px">{status_badge(req['status'])}</td>
              <td style="padding:10px 12px;min-width:150px">
                {cov_bar(req['abdeckung'])}</td>
              <td style="padding:10px 12px">{tests_html if tests_html
                else '<span style="color:#475569;font-size:0.8rem">Keine</span>'}
              </td>
            </tr>"""

    # Kategorie Cards
    kat_cards = ""
    for kat in KATEGORIEN:
        reqs  = kat["requirements"]
        impl  = sum(1 for r in reqs if r["status"] == "IMPLEMENTIERT")
        avg   = sum(r["abdeckung"] for r in reqs) / len(reqs)
        pct   = round(impl / len(reqs) * 100)
        color = kat["farbe"]
        kat_cards += f"""
        <div style="background:#1e293b;border-radius:12px;padding:1.25rem;
          border:1px solid #334155;border-left:4px solid {color}">
          <div style="font-weight:700;color:{color};
            margin-bottom:0.75rem">{kat['id']} — {kat['name']}</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;
            font-size:0.85rem;margin-bottom:0.75rem">
            <div style="color:#94a3b8">Requirements</div>
            <div style="text-align:right">{impl}/{len(reqs)}</div>
            <div style="color:#94a3b8">Ø Coverage</div>
            <div style="text-align:right;color:{color}">{avg:.1f}%</div>
          </div>
          {cov_bar(pct)}
        </div>"""

    # Test Rows
    test_rows = ""
    for t in TESTS:
        icon  = test_icon(t["status"])
        color = ("#22c55e" if t["status"] == "BESTANDEN"
                 else "#ef4444" if t["status"] == "FEHLGESCHLAGEN"
                 else "#f59e0b")
        kat_color = next(
            (k["farbe"] for k in KATEGORIEN if k["id"] == t["komponente"]),
            "#94a3b8")
        test_rows += f"""
        <tr>
          <td style="padding:8px 12px">
            <code style="font-size:0.8rem">{t['name']}</code></td>
          <td style="padding:8px 12px">
            <span style="color:{kat_color};font-size:0.8rem">
              {t['komponente']}</span></td>
          <td style="padding:8px 12px">
            <span style="color:{color}">{icon} {t['status']}</span></td>
          <td style="padding:8px 12px;color:#94a3b8;font-size:0.8rem">
            {t['dauer_ms']} ms</td>
        </tr>"""

    # ── Trend-Tab Daten aufbereiten ──────────
    def _fmt_date(ts):
        try:
            return datetime.fromisoformat(ts).strftime("%d.%m.%y")
        except Exception:
            return ts[:10]

    if TREND_DATA:
        trend_labels    = json.dumps([_fmt_date(e["timestamp"]) for e in TREND_DATA])
        trend_success   = json.dumps([e.get("erfolgsrate", 0) for e in TREND_DATA])
        trend_coverage  = json.dumps([e.get("avg_coverage", 0) for e in TREND_DATA])
        trend_total     = json.dumps([e.get("total_tests", 0) for e in TREND_DATA])
        trend_builds    = json.dumps([f"#{e.get('build','?')} {e.get('commit','')[:7]}" for e in TREND_DATA])
        last  = TREND_DATA[-1]
        first = TREND_DATA[0]
        trend_delta_success  = round(last.get("erfolgsrate",0)  - first.get("erfolgsrate",0),  1)
        trend_delta_coverage = round(last.get("avg_coverage",0) - first.get("avg_coverage",0), 1)
        trend_delta_tests    = last.get("total_tests",0) - first.get("total_tests",0)
        def _delta_html(val, unit=""):
            color = "#22c55e" if val >= 0 else "#ef4444"
            arrow = "▲" if val >= 0 else "▼"
            sign  = "+" if val >= 0 else ""
            return f'<span style="color:{color};font-size:0.8rem">{arrow} {sign}{val}{unit}</span>'
        trend_delta_html_s = _delta_html(trend_delta_success, "%")
        trend_delta_html_c = _delta_html(trend_delta_coverage, "%")
        trend_delta_html_t = _delta_html(trend_delta_tests)
        trend_pane = f"""
  <!-- Trend -->
  <div id="pane-trend" class="pane">
    <div class="section" style="margin-bottom:1rem">
      <h3>📉 Trend über {len(TREND_DATA)} Builds
        <span style="font-weight:400;font-size:0.8rem;color:#64748b;margin-left:0.5rem">
          ({_fmt_date(TREND_DATA[0]["timestamp"])} – {_fmt_date(TREND_DATA[-1]["timestamp"])})
        </span>
      </h3>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1rem">
        <div style="background:#0f172a;border-radius:8px;padding:1rem;text-align:center">
          <div style="font-size:1.6rem;font-weight:800;color:#22c55e">
            {last.get("erfolgsrate",0)}%</div>
          <div style="font-size:0.75rem;color:#64748b;margin-top:2px">Erfolgsrate {trend_delta_html_s}</div>
        </div>
        <div style="background:#0f172a;border-radius:8px;padding:1rem;text-align:center">
          <div style="font-size:1.6rem;font-weight:800;color:#a78bfa">
            {last.get("avg_coverage",0)}%</div>
          <div style="font-size:0.75rem;color:#64748b;margin-top:2px">Ø Coverage {trend_delta_html_c}</div>
        </div>
        <div style="background:#0f172a;border-radius:8px;padding:1rem;text-align:center">
          <div style="font-size:1.6rem;font-weight:800;color:#3b82f6">
            {last.get("total_tests",0)}</div>
          <div style="font-size:0.75rem;color:#64748b;margin-top:2px">Tests Gesamt {trend_delta_html_t}</div>
        </div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:1.5rem">
      <div class="section">
        <h3 style="margin-bottom:1rem">✅ Erfolgsrate (%)</h3>
        <canvas id="chartSuccess" height="180"></canvas>
      </div>
      <div class="section">
        <h3 style="margin-bottom:1rem">🛡️ Code Coverage (%)</h3>
        <canvas id="chartCoverage" height="180"></canvas>
      </div>
    </div>
    <div class="section">
      <h3 style="margin-bottom:1rem">🧪 Test-Anzahl</h3>
      <canvas id="chartTests" height="120"></canvas>
    </div>
    <div class="section" style="margin-top:1.5rem">
      <h3 style="margin-bottom:0.75rem">Build History</h3>
      <div style="overflow-x:auto">
        <table>
          <thead><tr>
            <th>Build</th><th>Datum</th><th>Branch</th>
            <th>Tests</th><th>Erfolgsrate</th><th>Coverage</th>
          </tr></thead>
          <tbody>
            {"".join(f'''<tr>
              <td style="padding:8px 12px;font-family:monospace;color:#3b82f6">
                #{e.get("build","?")} <span style="color:#475569;font-size:0.75rem">{e.get("commit","")[:7]}</span></td>
              <td style="padding:8px 12px;color:#94a3b8;font-size:0.85rem">{_fmt_date(e["timestamp"])}</td>
              <td style="padding:8px 12px;color:#64748b;font-size:0.85rem">{e.get("branch","main")}</td>
              <td style="padding:8px 12px">{e.get("total_tests",0)}</td>
              <td style="padding:8px 12px;color:{"#22c55e" if e.get("erfolgsrate",0)>=90 else "#f59e0b" if e.get("erfolgsrate",0)>=75 else "#ef4444"};font-weight:600">
                {e.get("erfolgsrate",0)}%</td>
              <td style="padding:8px 12px;color:{"#22c55e" if e.get("avg_coverage",0)>=90 else "#a78bfa" if e.get("avg_coverage",0)>=75 else "#f59e0b"}">
                {e.get("avg_coverage",0)}%</td>
            </tr>''' for e in reversed(TREND_DATA))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<script>
(function(){{
  var labels   = {trend_labels};
  var builds   = {trend_builds};
  var success  = {trend_success};
  var coverage = {trend_coverage};
  var total    = {trend_total};
  var tip = {{
    callbacks: {{
      title: function(ctx) {{ return builds[ctx[0].dataIndex]; }},
    }}
  }};
  var gridColor = 'rgba(51,65,85,0.6)';
  var baseOpts = {{
    responsive: true,
    plugins: {{ legend: {{ display: false }}, tooltip: tip }},
    scales: {{
      x: {{ ticks: {{ color:'#64748b', font:{{size:11}} }}, grid: {{ color:gridColor }} }},
      y: {{ ticks: {{ color:'#94a3b8', font:{{size:11}} }}, grid: {{ color:gridColor }} }}
    }}
  }};
  function line(id, data, color, min, max) {{
    var ctx = document.getElementById(id);
    if (!ctx) return;
    new Chart(ctx, {{
      type: 'line',
      data: {{
        labels: labels,
        datasets: [{{
          data: data,
          borderColor: color,
          backgroundColor: color + '22',
          borderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
          tension: 0.3,
          fill: true
        }}]
      }},
      options: Object.assign({{}}, baseOpts, {{
        scales: Object.assign({{}}, baseOpts.scales, {{
          y: Object.assign({{}}, baseOpts.scales.y, {{
            min: min, max: max
          }})
        }})
      }})
    }});
  }}
  function bar(id, data, color) {{
    var ctx = document.getElementById(id);
    if (!ctx) return;
    new Chart(ctx, {{
      type: 'bar',
      data: {{
        labels: labels,
        datasets: [{{
          data: data,
          backgroundColor: color + '99',
          borderColor: color,
          borderWidth: 1,
          borderRadius: 4
        }}]
      }},
      options: baseOpts
    }});
  }}
  // Referenzlinien für Quality Gates
  function lineWithGate(id, data, color, gate, min, max) {{
    var ctx = document.getElementById(id);
    if (!ctx) return;
    new Chart(ctx, {{
      type: 'line',
      data: {{
        labels: labels,
        datasets: [
          {{
            label: 'Wert',
            data: data,
            borderColor: color,
            backgroundColor: color + '22',
            borderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            tension: 0.3,
            fill: true
          }},
          {{
            label: 'Quality Gate (' + gate + '%)',
            data: labels.map(function() {{ return gate; }}),
            borderColor: '#ef444466',
            borderWidth: 1,
            borderDash: [6,4],
            pointRadius: 0,
            fill: false
          }}
        ]
      }},
      options: Object.assign({{}}, baseOpts, {{
        plugins: Object.assign({{}}, baseOpts.plugins, {{
          legend: {{ display: true, labels: {{ color:'#64748b', font:{{size:11}} }} }}
        }}),
        scales: Object.assign({{}}, baseOpts.scales, {{
          y: Object.assign({{}}, baseOpts.scales.y, {{ min: min, max: max }})
        }})
      }})
    }});
  }}
  lineWithGate('chartSuccess',  success,  '#22c55e', 90, 60, 102);
  lineWithGate('chartCoverage', coverage, '#a78bfa', 75, 60, 102);
  bar('chartTests', total, '#3b82f6');
}})();
</script>"""
    else:
        trend_pane = """
  <!-- Trend -->
  <div id="pane-trend" class="pane">
    <div class="section" style="text-align:center;padding:3rem">
      <div style="font-size:3rem">📉</div>
      <h3 style="margin:1rem 0 0.5rem">Noch keine Trend-Daten vorhanden</h3>
      <p style="color:#64748b;font-size:0.9rem">
        Trend-Daten werden nach dem ersten CI-Build unter
        <code>/trend/test_trend.json</code> gespeichert.
      </p>
    </div>
  </div>"""

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{PROJEKT} — Test Report</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Segoe UI',system-ui,sans-serif;
    background:#0f172a;color:#e2e8f0;line-height:1.5}}
  h1{{font-size:1.5rem;color:#3b82f6}}
  h2{{font-size:1.1rem;color:#94a3b8;margin:0 0 1rem}}
  h3{{font-size:1rem;color:#e2e8f0;margin:0 0 0.75rem}}
  .header{{background:#1e293b;padding:1.5rem 2rem;
    border-bottom:2px solid #3b82f6;
    display:flex;justify-content:space-between;align-items:center}}
  .meta{{font-size:0.85rem;color:#64748b}}
  .main{{padding:1.5rem 2rem}}
  .kpi-grid{{display:grid;
    grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
    gap:1rem;margin-bottom:2rem}}
  .kpi{{background:#1e293b;border-radius:12px;padding:1.25rem;
    border:1px solid #334155;text-align:center}}
  .kpi .val{{font-size:2rem;font-weight:800;line-height:1}}
  .kpi .lbl{{font-size:0.75rem;color:#64748b;margin-top:0.25rem}}
  .section{{background:#1e293b;border-radius:12px;
    padding:1.5rem;margin-bottom:1.5rem;border:1px solid #334155}}
  table{{width:100%;border-collapse:collapse}}
  th{{padding:10px 12px;text-align:left;font-size:0.8rem;
    color:#64748b;border-bottom:1px solid #334155;
    text-transform:uppercase;letter-spacing:0.05em}}
  tr:hover td{{background:#ffffff08}}
  td{{border-bottom:1px solid #1e293b}}
  .tabs{{display:flex;gap:0.5rem;margin-bottom:1.5rem;
    flex-wrap:wrap}}
  .tab{{padding:0.5rem 1.25rem;border-radius:6px;
    border:1px solid #334155;background:#1e293b;
    color:#94a3b8;cursor:pointer;font-size:0.85rem;
    transition:all 0.2s}}
  .tab.active{{background:#3b82f6;color:white;border-color:#3b82f6}}
  .pane{{display:none}}
  .pane.active{{display:block}}
  .kat-grid{{display:grid;
    grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
    gap:1rem;margin-bottom:1.5rem}}
  code{{background:#0f172a;padding:1px 5px;border-radius:3px;
    font-size:0.85em}}
  @media(max-width:768px){{
    .kpi-grid{{grid-template-columns:repeat(2,1fr)}}
    .header{{flex-direction:column;gap:0.5rem}}
  }}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>🤖 {PROJEKT}</h1>
    <div class="meta">Version {VERSION} &nbsp;|&nbsp; {DATUM}</div>
  </div>
  <div style="text-align:right;font-size:0.85rem;color:#64748b">
    Test Report &amp; Requirements Tracing
  </div>
</div>

<div class="main">

  <!-- KPIs -->
  <div class="kpi-grid">
    <div class="kpi">
      <div class="val" style="color:#3b82f6">{s['total_reqs']}</div>
      <div class="lbl">Requirements Gesamt</div>
    </div>
    <div class="kpi">
      <div class="val" style="color:#22c55e">{s['impl_reqs']}</div>
      <div class="lbl">Implementiert</div>
    </div>
    <div class="kpi">
      <div class="val" style="color:#22c55e">{s['req_coverage']}%</div>
      <div class="lbl">Req. Abdeckung</div>
    </div>
    <div class="kpi">
      <div class="val" style="color:#3b82f6">{s['total_tests']}</div>
      <div class="lbl">Tests Gesamt</div>
    </div>
    <div class="kpi">
      <div class="val" style="color:#22c55e">{s['bestanden']}</div>
      <div class="lbl">Tests Bestanden</div>
    </div>
    <div class="kpi">
      <div class="val" style="color:#{'22c55e' if s['fehlgeschlagen']==0 else 'ef4444'}">{s['fehlgeschlagen']}</div>
      <div class="lbl">Fehlgeschlagen</div>
    </div>
    <div class="kpi">
      <div class="val" style="color:#22c55e">{s['test_rate']}%</div>
      <div class="lbl">Erfolgsrate</div>
    </div>
    <div class="kpi">
      <div class="val" style="color:#a78bfa">{s['avg_coverage']}%</div>
      <div class="lbl">Ø Code Coverage</div>
    </div>
    <div class="kpi">
      <div class="val" style="color:#64748b">{s['total_dauer_s']}s</div>
      <div class="lbl">Gesamtdauer</div>
    </div>
  </div>

  <!-- Tabs -->
  <div class="tabs">
    <div class="tab active" onclick="showTab('overview')">
      📊 Übersicht</div>
    <div class="tab" onclick="showTab('tracing')">
      🔗 Req. Tracing</div>
    <div class="tab" onclick="showTab('tests')">
      🧪 Test Ergebnisse</div>
    <div class="tab" onclick="showTab('coverage')">
      📈 Code Coverage</div>
    <div class="tab" onclick="showTab('trend')">
      📉 Trend</div>
  </div>

  <!-- Übersicht -->
  <div id="pane-overview" class="pane active">
    <h2>Komponenten Übersicht</h2>
    <div class="kat-grid">{kat_cards}</div>
  </div>

  <!-- Tracing -->
  <div id="pane-tracing" class="pane">
    <div class="section">
      <h3>🔗 Requirement Tracing Matrix</h3>
      <div style="overflow-x:auto">
        <table>
          <thead>
            <tr>
              <th>ID</th><th>Requirement</th><th>Priorität</th>
              <th>Status</th><th>Coverage</th><th>Tests</th>
            </tr>
          </thead>
          <tbody>{tracing_rows}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Tests -->
  <div id="pane-tests" class="pane">
    <div class="section">
      <h3>🧪 Test Ergebnisse ({s['total_tests']} Tests)</h3>
      <div style="overflow-x:auto">
        <table>
          <thead>
            <tr>
              <th>Test Name</th><th>Komponente</th>
              <th>Status</th><th>Dauer</th>
            </tr>
          </thead>
          <tbody>{test_rows}</tbody>
        </table>
      </div>
    </div>
  </div>

  {trend_pane}

  <!-- Coverage -->
  <div id="pane-coverage" class="pane">
    <div class="section">
      <h3>📈 Code Coverage pro Komponente</h3>
      {''.join(f"""
      <div style="margin-bottom:1.25rem">
        <div style="display:flex;justify-content:space-between;
          margin-bottom:0.4rem">
          <span style="color:{k['farbe']};font-weight:600">
            {k['id']} — {k['name']}</span>
          <span style="color:#94a3b8;font-size:0.85rem">
            {sum(r['abdeckung'] for r in k['requirements'])/len(k['requirements']):.1f}%</span>
        </div>
        <div style="background:#0f172a;border-radius:6px;height:12px">
          <div style="width:{sum(r['abdeckung'] for r in k['requirements'])/len(k['requirements']):.1f}%;
            background:{k['farbe']};height:12px;border-radius:6px;
            transition:width 1s"></div>
        </div>
        <div style="display:grid;
          grid-template-columns:repeat(auto-fill,minmax(200px,1fr));
          gap:0.4rem;margin-top:0.5rem">
          {''.join(f"""<div style="font-size:0.75rem;color:#64748b;
            display:flex;justify-content:space-between">
            <span>{r['id']}: {r['titel'][:25]}...</span>
            <span style="color:{'#22c55e' if r['abdeckung']>=90 else '#f59e0b' if r['abdeckung']>=75 else '#ef4444'}">{r['abdeckung']}%</span>
            </div>""" for r in k['requirements'])}
        </div>
      </div>""" for k in KATEGORIEN)}
    </div>
  </div>

</div>

<script>
function showTab(name) {{
  const names = ['overview','tracing','tests','coverage','trend'];
  document.querySelectorAll('.tab').forEach((t,i) => {{
    t.classList.toggle('active', names[i] === name);
  }});
  document.querySelectorAll('.pane').forEach(p => {{
    p.classList.remove('active');
  }});
  document.getElementById('pane-' + name).classList.add('active');
}}
</script>
</body>
</html>"""

    path = os.path.join(OUTPUT_DIR, "bb_dashboard.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML Dashboard: {path}")

# ════════════════════════════════════════
# 4. PDF Report
# ════════════════════════════════════════
def generate_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table,
        TableStyle, HRFlowable, PageBreak)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    path = os.path.join(OUTPUT_DIR, "bb_report.pdf")
    doc  = SimpleDocTemplate(
        path, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm)

    # Farben
    C_BG     = colors.HexColor("#0f172a")
    C_CARD   = colors.HexColor("#1e293b")
    C_BLUE   = colors.HexColor("#3b82f6")
    C_GREEN  = colors.HexColor("#22c55e")
    C_RED    = colors.HexColor("#ef4444")
    C_YELLOW = colors.HexColor("#f59e0b")
    C_PURPLE = colors.HexColor("#8b5cf6")
    C_GRAY   = colors.HexColor("#64748b")
    C_LIGHT  = colors.HexColor("#94a3b8")
    C_WHITE  = colors.white

    styles = getSampleStyleSheet()
    def S(name, **kw):
        return ParagraphStyle(name, parent=styles["Normal"], **kw)

    sTitle  = S("T", fontSize=22, textColor=C_BLUE,
                spaceAfter=6, fontName="Helvetica-Bold",
                alignment=TA_CENTER)
    sSub    = S("S", fontSize=10, textColor=C_GRAY,
                spaceAfter=4, alignment=TA_CENTER)
    sH1     = S("H1", fontSize=14, textColor=C_BLUE,
                spaceBefore=16, spaceAfter=8,
                fontName="Helvetica-Bold")
    sH2     = S("H2", fontSize=11, textColor=C_LIGHT,
                spaceBefore=10, spaceAfter=6,
                fontName="Helvetica-Bold")
    sBody   = S("B", fontSize=9, textColor=C_LIGHT,
                spaceAfter=4, leading=14)
    sSmall  = S("SM", fontSize=8, textColor=C_GRAY)
    sCode   = S("C", fontSize=8, textColor=C_GREEN,
                fontName="Courier", backColor=C_CARD)

    def TS(*cmds):
        return TableStyle([
            ("BACKGROUND",  (0,0), (-1,0),  C_CARD),
            ("TEXTCOLOR",   (0,0), (-1,0),  C_BLUE),
            ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
            ("FONTSIZE",    (0,0), (-1,-1), 8),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_BG, C_CARD]),
            ("TEXTCOLOR",   (0,1), (-1,-1), C_LIGHT),
            ("GRID",        (0,0), (-1,-1), 0.5, C_GRAY),
            ("TOPPADDING",  (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING",(0,0), (-1,-1), 6),
            ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ] + list(cmds))

    s = STATS
    story = []

    # ── Titelseite ──
    story += [
        Spacer(1, 3*cm),
        Paragraph(PROJEKT, sTitle),
        Paragraph("Test &amp; Requirements Report", sSub),
        Paragraph(f"Version {VERSION}  |  {DATUM}", sSub),
        Spacer(1, 1*cm),
        HRFlowable(width="100%", color=C_BLUE, thickness=2),
        Spacer(1, 1*cm),
    ]

    # KPI Tabelle
    kpi_data = [
        ["Metrik", "Wert", "Metrik", "Wert"],
        ["Requirements Gesamt", str(s["total_reqs"]),
         "Tests Gesamt",        str(s["total_tests"])],
        ["Implementiert",       str(s["impl_reqs"]),
         "Bestanden",           str(s["bestanden"])],
        ["Offen",               str(s["offen_reqs"]),
         "Fehlgeschlagen",      str(s["fehlgeschlagen"])],
        ["Req. Abdeckung",      f"{s['req_coverage']}%",
         "Erfolgsrate",         f"{s['test_rate']}%"],
        ["Ø Code Coverage",     f"{s['avg_coverage']}%",
         "Gesamtdauer",         f"{s['total_dauer_s']}s"],
    ]
    kpi_table = Table(kpi_data,
        colWidths=[4.5*cm, 3*cm, 4.5*cm, 3*cm])
    kpi_table.setStyle(TS(
        ("TEXTCOLOR", (1,1), (1,-1), C_GREEN),
        ("TEXTCOLOR", (3,1), (3,-1), C_GREEN),
        ("FONTNAME",  (1,1), (1,-1), "Helvetica-Bold"),
        ("FONTNAME",  (3,1), (3,-1), "Helvetica-Bold"),
    ))
    story += [kpi_table, PageBreak()]

    # ── Requirements pro Kategorie ──
    story.append(Paragraph("Requirements pro Komponente", sH1))
    story.append(HRFlowable(width="100%", color=C_BLUE,
                             thickness=1))

    for kat in KATEGORIEN:
        reqs  = kat["requirements"]
        impl  = sum(1 for r in reqs
                    if r["status"] == "IMPLEMENTIERT")
        avg   = sum(r["abdeckung"] for r in reqs) / len(reqs)
        color = colors.HexColor(kat["farbe"])

        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(
            f"{kat['id']} — {kat['name']}  "
            f"({impl}/{len(reqs)} implementiert  |  "
            f"Ø {avg:.1f}% Coverage)", sH2))

        tdata = [["ID", "Titel", "Prio", "Status", "Cov.", "Tests"]]
        for req in reqs:
            st_color = (C_GREEN if req["status"] == "IMPLEMENTIERT"
                        else C_RED)
            pr_color = (C_RED    if req["prioritaet"] == "HOCH"
                        else C_YELLOW if req["prioritaet"] == "MITTEL"
                        else C_BLUE)
            cv_color = (C_GREEN  if req["abdeckung"] >= 90
                        else C_YELLOW if req["abdeckung"] >= 75
                        else C_RED)
            tdata.append([
                req["id"],
                req["titel"][:40],
                req["prioritaet"],
                req["status"],
                f"{req['abdeckung']}%",
                str(len(req["tests"])),
            ])

        t = Table(tdata,
            colWidths=[1.8*cm,6*cm,1.8*cm,2.8*cm,1.5*cm,1.3*cm])
        style = TS()
        for i, req in enumerate(reqs, 1):
            st_c = (C_GREEN if req["status"] == "IMPLEMENTIERT"
                    else C_RED)
            pr_c = (C_RED    if req["prioritaet"] == "HOCH"
                    else C_YELLOW if req["prioritaet"] == "MITTEL"
                    else C_BLUE)
            cv_c = (C_GREEN  if req["abdeckung"] >= 90
                    else C_YELLOW if req["abdeckung"] >= 75
                    else C_RED)
            style.add("TEXTCOLOR", (0,i), (0,i), color)
            style.add("TEXTCOLOR", (2,i), (2,i), pr_c)
            style.add("TEXTCOLOR", (3,i), (3,i), st_c)
            style.add("TEXTCOLOR", (4,i), (4,i), cv_c)
        t.setStyle(style)
        story.append(t)

    story.append(PageBreak())

    # ── Requirement Tracing ──
    story.append(Paragraph("Requirement Tracing Report", sH1))
    story.append(HRFlowable(width="100%", color=C_BLUE,
                             thickness=1))

    for kat in KATEGORIEN:
        story.append(Spacer(1, 0.4*cm))
        color = colors.HexColor(kat["farbe"])
        story.append(Paragraph(
            f"{kat['id']} — {kat['name']}", sH2))

        for req in kat["requirements"]:
            icon = ("IMPLEMENTIERT" if req["status"] == "IMPLEMENTIERT"
                    else "OFFEN")
            story.append(Paragraph(
                f"<b>{req['id']}</b> — {req['titel']}  "
                f"[{req['prioritaet']}] [{req['abdeckung']}% Coverage]",
                sBody))
            story.append(Paragraph(req["beschreibung"], sSmall))

            if req["tests"]:
                t_rows = [["Test Name", "Status", "Dauer"]]
                for t in req["tests"]:
                    result = next(
                        (x for x in TESTS if x["name"] == t), None)
                    st = result["status"] if result else "NICHT GEFUNDEN"
                    ms = f"{result['dauer_ms']}ms" if result else "-"
                    t_rows.append([t, st, ms])

                tt = Table(t_rows,
                    colWidths=[8*cm, 3.5*cm, 2.5*cm])
                ts = TS()
                for i, t in enumerate(req["tests"], 1):
                    result = next(
                        (x for x in TESTS if x["name"] == t), None)
                    if result:
                        c = (C_GREEN  if result["status"] == "BESTANDEN"
                             else C_RED if result["status"] == "FEHLGESCHLAGEN"
                             else C_YELLOW)
                        ts.add("TEXTCOLOR", (1,i), (1,i), c)
                tt.setStyle(ts)
                story.append(tt)
            story.append(Spacer(1, 0.2*cm))

    story.append(PageBreak())

    # ── Code Coverage ──
    story.append(Paragraph("Code Coverage Report", sH1))
    story.append(HRFlowable(width="100%", color=C_BLUE,
                             thickness=1))
    story.append(Spacer(1, 0.5*cm))

    cov_data = [["Komponente", "Requirements", "Ø Coverage",
                 "Min", "Max", "Bewertung"]]
    for kat in KATEGORIEN:
        reqs = kat["requirements"]
        covs = [r["abdeckung"] for r in reqs]
        avg  = sum(covs) / len(covs)
        bew  = ("Sehr gut" if avg >= 90
                else "Gut" if avg >= 80
                else "Ausreichend" if avg >= 70
                else "Unzureichend")
        cov_data.append([
            f"{kat['id']} — {kat['name']}",
            str(len(reqs)),
            f"{avg:.1f}%",
            f"{min(covs)}%",
            f"{max(covs)}%",
            bew,
        ])

    ct = Table(cov_data,
        colWidths=[5.5*cm,2.5*cm,2.5*cm,1.5*cm,1.5*cm,3*cm])
    cs = TS()
    for i, kat in enumerate(KATEGORIEN, 1):
        covs = [r["abdeckung"] for r in kat["requirements"]]
        avg  = sum(covs) / len(covs)
        c    = (C_GREEN  if avg >= 90
                else C_YELLOW if avg >= 75 else C_RED)
        cs.add("TEXTCOLOR", (2,i), (2,i), c)
        cs.add("TEXTCOLOR", (5,i), (5,i), c)
    ct.setStyle(cs)
    story.append(ct)

    # Gesamt Coverage
    story += [
        Spacer(1, 1*cm),
        Paragraph("Gesamt-Bewertung", sH2),
        Paragraph(
            f"Gesamte Ø Code Coverage: <b>{s['avg_coverage']}%</b>  |  "
            f"Test Erfolgsrate: <b>{s['test_rate']}%</b>  |  "
            f"Requirements implementiert: <b>{s['req_coverage']}%</b>",
            sBody),
    ]

    # Build
    def first_page(c, doc):
        c.saveState()
        c.setFillColor(C_BG)
        c.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        c.restoreState()

    def later_pages(c, doc):
        c.saveState()
        c.setFillColor(C_BG)
        c.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        c.setFont("Helvetica", 8)
        c.setFillColor(C_GRAY)
        c.drawString(2*cm, 1*cm,
            f"{PROJEKT} v{VERSION} — Seite {doc.page}")
        c.drawRightString(A4[0]-2*cm, 1*cm, DATUM)
        c.restoreState()

    doc.build(story,
              onFirstPage=first_page,
              onLaterPages=later_pages)
    print(f"✅ PDF Report: {path}")

# ════════════════════════════════════════
# Main
# ════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\n📊 Generiere Reports für: {PROJEKT} v{VERSION}")
    print(f"   {STATS['total_reqs']} Requirements | "
          f"{STATS['total_tests']} Tests\n")
    generate_json()
    generate_markdown()
    generate_html()
    generate_pdf()
    print(f"\n✅ Alle Reports erstellt!")
    print(f"   Erfolgsrate:  {STATS['test_rate']}%")
    print(f"   Req. Coverage:{STATS['req_coverage']}%")
    print(f"   Ø Coverage:   {STATS['avg_coverage']}%")
