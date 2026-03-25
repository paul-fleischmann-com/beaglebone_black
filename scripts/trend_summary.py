#!/usr/bin/env python3
"""Schreibt den Test-Trend als Markdown in $GITHUB_STEP_SUMMARY."""
import json
import os
import sys


def main():
    trend_file = os.path.join(
        os.path.dirname(__file__), "..", "reports", "test_trend.json"
    )
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")

    if not summary_file:
        print("GITHUB_STEP_SUMMARY nicht gesetzt – kein Output", file=sys.stderr)
        return

    if not os.path.exists(trend_file):
        print(f"Keine Trend-Daten unter {trend_file}", file=sys.stderr)
        return

    trend = json.load(open(trend_file))
    if not trend:
        return

    cur  = trend[-1]
    prev = trend[-2] if len(trend) >= 2 else None

    def delta(key):
        if not prev:
            return ""
        d = round(cur.get(key, 0) - prev.get(key, 0), 1)
        if d == 0:
            return " _(±0)_"
        arrow = "▲" if d > 0 else "▼"
        return f" _({arrow} {'+' if d > 0 else ''}{d})_"

    def status_icon(value, green=90, yellow=75):
        return "🟢" if value >= green else "🟡" if value >= yellow else "🔴"

    # Sparkline der letzten 10 Builds
    blocks = " ▁▂▃▄▅▆▇█"
    recent = [e.get("erfolgsrate", 0) for e in trend[-10:]]
    lo, hi = min(recent), max(recent)
    span   = hi - lo if hi != lo else 1
    spark  = "".join(blocks[round((v - lo) / span * 8)] for v in recent)

    lines = [
        "---",
        "## 📉 Test-Trend",
        "",
        "| | Aktuell | Vorheriger Build |",
        "|---|---|---|",
        f"| {status_icon(cur.get('erfolgsrate', 0))} **Erfolgsrate** "
        f"| **{cur.get('erfolgsrate', 0)}%**{delta('erfolgsrate')} "
        f"| {prev.get('erfolgsrate', 0) if prev else '–'}% |",
        f"| {status_icon(cur.get('avg_coverage', 0), green=75, yellow=50)} **Ø Coverage** "
        f"| **{cur.get('avg_coverage', 0)}%**{delta('avg_coverage')} "
        f"| {prev.get('avg_coverage', 0) if prev else '–'}% |",
        f"| 🧪 **Tests** "
        f"| **{cur.get('total_tests', 0)}** "
        f"| {prev.get('total_tests', 0) if prev else '–'} |",
        "",
        f"Letzte {len(recent)} Builds (Erfolgsrate): `{spark}`",
        "",
        "<details><summary>📋 Build History (letzte 10 Runs)</summary>",
        "",
        "| Run | Commit | Branch | Tests | Erfolgsrate | Coverage |",
        "|---|---|---|---|---|---|",
    ]

    for e in reversed(trend[-10:]):
        s   = e.get("erfolgsrate", 0)
        cov = e.get("avg_coverage", 0)
        lines.append(
            f"| #{e.get('build', '?')} _{e.get('timestamp', '')[:10]}_ "
            f"| `{e.get('commit', '')[:7]}` "
            f"| `{e.get('branch', 'main')}` "
            f"| {e.get('total_tests', 0)} "
            f"| {status_icon(s)} {s}% "
            f"| {status_icon(cov, green=75, yellow=50)} {cov}% |"
        )

    lines += ["", "</details>", ""]

    with open(summary_file, "a") as f:
        f.write("\n".join(lines))

    print(
        f"✅ Trend Summary geschrieben "
        f"({len(trend)} Einträge, Sparkline: {spark})"
    )


if __name__ == "__main__":
    main()
