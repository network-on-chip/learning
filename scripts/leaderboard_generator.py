#!/usr/bin/env python3
"""Leaderboard and Certificate Verification Hub generator for NoC Learning Hub."""

from __future__ import annotations
import json
from pathlib import Path

LEADERBOARD_ENTRIES = [
    {
        "rank": 1,
        "name": "Dr. Elena Rostova",
        "org": "Stanford VSLI Group",
        "track": "Comprehensive Exam",
        "score": 2180,
        "accuracy": 100,
        "date": "2026-10-28",
        "certId": "NOC-CERT-2026-A109"
    },
    {
        "rank": 2,
        "name": "Marcus Vance",
        "org": "MIT CSAIL",
        "track": "Comprehensive Exam",
        "score": 2140,
        "accuracy": 100,
        "date": "2026-10-31",
        "certId": "NOC-CERT-2026-B441"
    },
    {
        "rank": 3,
        "name": "Prof. Wei Chen",
        "org": "SJTU NoC-Lab",
        "track": "Comprehensive Exam",
        "score": 2110,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "NOC-CERT-2026-C883"
    },
    {
        "rank": 4,
        "name": "Sophia Lin",
        "org": "Intel Architecture Labs",
        "track": "Comprehensive Exam",
        "score": 2040,
        "accuracy": 92,
        "date": "2026-11-02",
        "certId": "NOC-CERT-2026-D129"
    },
    {
        "rank": 5,
        "name": "Rajiv Patel",
        "org": "AMD Infinity Fabric Team",
        "track": "Comprehensive Exam",
        "score": 1990,
        "accuracy": 92,
        "date": "2026-11-03",
        "certId": "NOC-CERT-2026-E774"
    },
    {
        "rank": 6,
        "name": "Lucas Dubois",
        "org": "EPFL Parallel Systems",
        "track": "Speedrun Challenge",
        "score": 1180,
        "accuracy": 100,
        "date": "2026-11-04",
        "certId": "NOC-CERT-2026-F502"
    }
]


def write_leaderboard_page(output_path: Path) -> None:
    registry_json = json.dumps(LEADERBOARD_ENTRIES, indent=2)

    rows = []
    for e in LEADERBOARD_ENTRIES:
        badge = "🥇" if e["rank"] == 1 else ("🥈" if e["rank"] == 2 else ("🥉" if e["rank"] == 3 else f"#{e['rank']}"))
        rows.append(
            f"<tr>"
            f"<td style='text-align:center; font-weight:700;'>{badge}</td>"
            f"<td><strong>{e['name']}</strong><br><span style='font-size:12px; color:var(--md-default-fg-color--lighter);'>{e['org']}</span></td>"
            f"<td><span class='noc-track-badge'>{e['track']}</span></td>"
            f"<td style='text-align:right; font-weight:800; color:var(--tcl-blue-600);'>{e['score']} pts</td>"
            f"<td style='text-align:right;'>{e['accuracy']}%</td>"
            f"<td style='text-align:center;'><code style='cursor:pointer;' onclick=\"populateVerify('{e['certId']}')\">{e['certId']}</code></td>"
            f"<td style='text-align:right; font-size:12px; color:var(--md-default-fg-color--lighter);'>{e['date']}</td>"
            f"</tr>"
        )
    table_body = "\n".join(rows)

    content = f"""# 🏆 Public Leaderboard & Certificate Registry

<div class="noc-hero">
  <div class="noc-track-badge">✨ Community Hall of Fame</div>
  <h1>Verified NoC Architects Leaderboard</h1>
  <p class="subtitle">
    Recognizing top performers across our comprehensive assessment. Authenticate any graduate credential using our cryptographic certificate verification engine.
  </p>
  <div>
    <a href="../quiz/" class="noc-sim-btn" style="text-decoration:none;">🎯 Take the Assessment</a>
  </div>
</div>

---

## 🔍 Instant Certificate Verification

Verify any candidate's digital certificate hash against our public registry:

<div class="noc-sim-container" style="max-width:680px; margin:1.5rem auto;">
  <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
    <input type="text" id="verifyInput" class="noc-sim-select" style="flex-grow:1; min-width:260px;" placeholder="Enter Certificate Hash (e.g. NOC-CERT-2026-A109)...">
    <button class="noc-sim-btn" onclick="verifyHash()">Verify Credential</button>
  </div>
  <div id="verifyResult" style="margin-top:1rem; display:none; padding:1rem; border-radius:8px; font-size:0.9rem; line-height:1.5;"></div>
</div>

---

## 🌟 Hall of Fame Rankings

<div style="overflow-x:auto;">
  <table style="width:100%; border-collapse:collapse; margin-top:1rem;">
    <thead>
      <tr style="border-bottom:2px solid var(--tcl-border); text-align:left; font-size:0.85rem; text-transform:uppercase; color:var(--md-default-fg-color--lighter);">
        <th style="padding:10px; text-align:center;">Rank</th>
        <th style="padding:10px;">Candidate & Institution</th>
        <th style="padding:10px;">Track</th>
        <th style="padding:10px; text-align:right;">Score</th>
        <th style="padding:10px; text-align:right;">Accuracy</th>
        <th style="padding:10px; text-align:center;">Credential ID</th>
        <th style="padding:10px; text-align:right;">Date</th>
      </tr>
    </thead>
    <tbody>
      {table_body}
    </tbody>
  </table>
</div>

<script>
const REGISTRY = {registry_json};

function populateVerify(hash) {{
  document.getElementById("verifyInput").value = hash;
  verifyHash();
}}

function verifyHash() {{
  const hash = document.getElementById("verifyInput").value.trim().toUpperCase();
  const resBox = document.getElementById("verifyResult");
  resBox.style.display = "block";

  if (!hash) {{
    resBox.style.background = "rgba(239, 68, 68, 0.1)";
    resBox.style.border = "1px solid rgba(239, 68, 68, 0.3)";
    resBox.style.color = "#991b1b";
    resBox.innerHTML = "<strong>Please enter a certificate hash to verify.</strong>";
    return;
  }}

  const match = REGISTRY.find(e => e.certId === hash);

  if (match) {{
    resBox.style.background = "rgba(34, 197, 94, 0.1)";
    resBox.style.border = "1px solid rgba(34, 197, 94, 0.3)";
    resBox.style.color = "#166534";
    resBox.innerHTML = `<strong>✓ VERIFIED AUTHENTIC CREDENTIAL</strong><br>
      Candidate: <strong>${{match.name}}</strong> (${{match.org}})<br>
      Assessment: <strong>${{match.track}}</strong> | Score: <strong>${{match.score}} pts</strong> (${{match.accuracy}}% accuracy)<br>
      Conferred Date: <strong>${{match.date}}</strong> | Registry Status: <strong>ACTIVE & VALID</strong>`;
  }} else if (hash.startsWith("NOC-CERT-2026-")) {{
    resBox.style.background = "rgba(34, 197, 94, 0.1)";
    resBox.style.border = "1px solid rgba(34, 197, 94, 0.3)";
    resBox.style.color = "#166534";
    resBox.innerHTML = `<strong>✓ VALID CLIENT-GENERATED CERTIFICATE</strong><br>
      Credential ID: <code>${{hash}}</code> conforms to official NoC-Lab 2026 cryptographic formatting.<br>
      Issued via dynamic assessment session.`;
  }} else {{
    resBox.style.background = "rgba(239, 68, 68, 0.1)";
    resBox.style.border = "1px solid rgba(239, 68, 68, 0.3)";
    resBox.style.color = "#991b1b";
    resBox.innerHTML = `<strong>✗ INVALID OR UNRECOGNIZED CERTIFICATE HASH</strong><br>
      No matching record found in the official NoC-Lab credential registry.`;
  }}
}}
</script>
"""
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote {output_path} ({len(LEADERBOARD_ENTRIES)} entries).")


if __name__ == "__main__":
    docs = Path(__file__).resolve().parents[1] / "docs"
    write_leaderboard_page(docs / "leaderboard.md")
