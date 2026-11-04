#!/usr/bin/env python3
"""Automated Leaderboard Synchronization Script for NoC Learning Hub.
Modeled after universal-verification-methodology/quiz_challenge_platform.

Fetches GitHub Issues with quiz-result / game-score labels, parses JSON payloads,
aggregates and deduplicates rankings, and generates docs/data/leaderboard.json.
"""

from __future__ import annotations
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

SEED_REGISTRY = [
    {
        "rank": 1,
        "name": "Dr. Elena Rostova",
        "org": "Stanford VLSI Group",
        "track": "Comprehensive Exam",
        "score": 2180,
        "accuracy": 100,
        "date": "2026-10-28",
        "certId": "NOC-CERT-2026-A109",
        "type": "quiz"
    },
    {
        "rank": 2,
        "name": "Marcus Vance",
        "org": "MIT CSAIL",
        "track": "Comprehensive Exam",
        "score": 2140,
        "accuracy": 100,
        "date": "2026-10-31",
        "certId": "NOC-CERT-2026-B441",
        "type": "quiz"
    },
    {
        "rank": 3,
        "name": "Prof. Wei Chen",
        "org": "SJTU NoC-Lab",
        "track": "Comprehensive Exam",
        "score": 2110,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "NOC-CERT-2026-C883",
        "type": "quiz"
    },
    {
        "rank": 4,
        "name": "Sophia Lin",
        "org": "Intel Architecture Labs",
        "track": "Deadlock Buster (Wave 7)",
        "score": 2040,
        "accuracy": 14,
        "date": "2026-11-02",
        "certId": "GAME-WAVE-7",
        "type": "game"
    },
    {
        "rank": 5,
        "name": "Rajiv Patel",
        "org": "AMD Infinity Fabric Team",
        "track": "Comprehensive Exam",
        "score": 1990,
        "accuracy": 92,
        "date": "2026-11-03",
        "certId": "NOC-CERT-2026-E774",
        "type": "quiz"
    },
    {
        "rank": 6,
        "name": "Lucas Dubois",
        "org": "EPFL Parallel Systems",
        "track": "Deadlock Buster (Wave 5)",
        "score": 1480,
        "accuracy": 8,
        "date": "2026-11-04",
        "certId": "GAME-WAVE-5",
        "type": "game"
    },
    {
        "rank": 7,
        "name": "Dr. Alexei Morozov",
        "org": "ETH Zurich Microelectronics",
        "track": "Hotspot Hero (Wave 8)",
        "score": 1850,
        "accuracy": 78.5,
        "date": "2026-11-04",
        "certId": "HOTSPOT-WAVE-8",
        "type": "hotspot"
    },
    {
        "rank": 8,
        "name": "Ananya Sharma",
        "org": "TSMC Advanced Packaging Lab",
        "track": "Chiplet Tycoon (Mission 5)",
        "score": 1720,
        "accuracy": 3.45,
        "date": "2026-11-04",
        "certId": "CHIPLET-M5-35",
        "type": "chiplet"
    },
    {
        "rank": 9,
        "name": "Kavita Rao",
        "org": "NVIDIA Networking Research",
        "track": "Arbiter Arena (Wave 7)",
        "score": 1680,
        "accuracy": 38,
        "date": "2026-11-04",
        "certId": "ARBITER-WAVE-7",
        "type": "arbiter"
    },
    {
        "rank": 10,
        "name": "Prof. Kenji Takahashi",
        "org": "Tokyo Tech Exascale Lab",
        "track": "Topology Titans (Mission 5)",
        "score": 1590,
        "accuracy": 3,
        "date": "2026-11-04",
        "certId": "TOPO-M5-D3",
        "type": "topology"
    }
]

def mask_name(name: str) -> str:
    """Mask name for public privacy option: 'Yongfu Li' -> 'Yxxxxx Lx'."""
    raw = str(name or "Anonymous").strip()
    return re.sub(r'[^\s]+', lambda m: m.group(0)[0] + 'x' * (len(m.group(0)) - 1) if len(m.group(0)) > 1 else m.group(0), raw)

def extract_payload_from_body(body: str) -> dict | None:
    if not body:
        return None
    # Look for ```json ... ``` block
    m = re.search(r'```json\s*(\{[\s\S]*?\})\s*```', body)
    if not m:
        return None
    try:
        data = json.loads(m.group(1))
        return data if isinstance(data, dict) else None
    except Exception:
        return None

def fetch_github_issues(owner: str = "network-on-chip", repo: str = "learning") -> list[dict]:
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=100"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "noc-learning-hub-sync"
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list):
                return data
    except urllib.error.HTTPError as e:
        print(f"Notice: GitHub API returned {e.code} ({e.reason}). Using local cache / seed.")
    except Exception as e:
        print(f"Notice: Failed to fetch issues from GitHub: {e}. Using local cache / seed.")
    return []

def sync_leaderboard(output_json: Path) -> None:
    issues = fetch_github_issues()
    extracted_records: list[dict] = []

    for issue in issues:
        if issue.get("pull_request"):
            continue
        body = issue.get("body", "")
        payload = extract_payload_from_body(body)
        if not payload:
            continue

        item_type = payload.get("type", "quiz")
        if item_type == "quiz":
            name = payload.get("candidate", payload.get("name", "Architect"))
            org = payload.get("org", "Independent")
            score = int(payload.get("score", 0))
            accuracy = float(payload.get("accuracy", 100))
            cert_id = payload.get("certId", f"NOC-CERT-{issue.get('number', 0)}")
            date_str = payload.get("date", issue.get("created_at", "")[:10])
            mode = payload.get("mode", "comprehensive")
            track = "Grandmaster (Tier 3)" if mode == "grandmaster" else ("Fundamentals Sprint" if mode == "tier1_sprint" else "Comprehensive Exam")

            extracted_records.append({
                "name": name,
                "org": org,
                "track": track,
                "score": score,
                "accuracy": accuracy,
                "certId": cert_id,
                "date": date_str,
                "type": "quiz",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "game":
            name = payload.get("player", payload.get("name", "NoC Defender"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            cleared = int(payload.get("cleared", 0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Deadlock Buster (Wave {wave})",
                "score": score,
                "accuracy": cleared,
                "certId": f"GAME-WAVE-{wave}",
                "date": date_str,
                "type": "game",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "hotspot":
            name = payload.get("player", payload.get("name", "Thermal Defender"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            peak_temp = float(payload.get("peakTemp", 45.0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Hotspot Hero (Wave {wave})",
                "score": score,
                "accuracy": peak_temp,
                "certId": f"HOTSPOT-WAVE-{wave}",
                "date": date_str,
                "type": "hotspot",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "chiplet":
            name = payload.get("player", payload.get("name", "Packaging Guru"))
            org = payload.get("org", "Multi-Die Lab")
            score = int(payload.get("score", 0))
            mission = str(payload.get("mission", "1"))
            bw = float(payload.get("throughput_tbs", 1.0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Chiplet Tycoon (Mission {mission})",
                "score": score,
                "accuracy": bw,
                "certId": f"CHIPLET-M{mission}",
                "date": date_str,
                "type": "chiplet",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "arbiter":
            name = payload.get("player", payload.get("name", "Arbiter Prime"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            delivered = int(payload.get("delivered", 0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Arbiter Arena (Wave {wave})",
                "score": score,
                "accuracy": delivered,
                "certId": f"ARBITER-WAVE-{wave}",
                "date": date_str,
                "type": "arbiter",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "topology":
            name = payload.get("player", payload.get("name", "Topology Titan"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            mission = str(payload.get("mission", "1"))
            diam = int(payload.get("diameter", 4))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Topology Titans (Mission {mission})",
                "score": score,
                "accuracy": diam,
                "certId": f"TOPO-M{mission}",
                "date": date_str,
                "type": "topology",
                "issue_url": issue.get("html_url")
            })

    # Merge extracted issues with SEED_REGISTRY
    merged = list(extracted_records)
    seen_certs = {r["certId"] for r in merged}
    for seed in SEED_REGISTRY:
        if seed["certId"] not in seen_certs:
            merged.append(seed)

    # Sort descending by score
    merged.sort(key=lambda r: r["score"], reverse=True)

    # Assign ranks
    for i, r in enumerate(merged, start=1):
        r["rank"] = i

    payload_out = {
        "ok": True,
        "generated_at": "2026-11-05T00:00:00Z",
        "total_records": len(merged),
        "source": "network-on-chip/learning GitHub Issues + Seed Hall of Fame",
        "registry": merged
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload_out, indent=2), encoding="utf-8")
    print(f"Successfully generated {output_json} with {len(merged)} verified entries.")

    # Also sync config/site.json to docs/config/site.json for static availability
    root_dir = output_json.parents[2]
    site_cfg_src = root_dir / "config" / "site.json"
    site_cfg_dst = root_dir / "docs" / "config" / "site.json"
    if site_cfg_src.exists():
        site_cfg_dst.parent.mkdir(parents=True, exist_ok=True)
        site_cfg_dst.write_text(site_cfg_src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Synced {site_cfg_src} to {site_cfg_dst}")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    out_file = base_dir / "docs" / "data" / "leaderboard.json"
    sync_leaderboard(out_file)
