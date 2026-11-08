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
        "name": "Golden Key: Architecture Exam",
        "org": "NoC Golden Model Verifier",
        "track": "Comprehensive Exam",
        "score": 2200,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-GOLDEN-EXAM-100",
        "type": "quiz"
    },
    {
        "rank": 2,
        "name": "DOR-XY Deterministic Baseline",
        "org": "Reference Microarchitecture Model",
        "track": "Deadlock Buster (Wave 10)",
        "score": 2000,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-DOR-XY-W10",
        "type": "game"
    },
    {
        "rank": 3,
        "name": "Odd-Even Adaptive Router Baseline",
        "org": "Reference Turn Model Engine",
        "track": "Deadlock Buster (Wave 8)",
        "score": 1850,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-ODD-EVEN-W8",
        "type": "game"
    },
    {
        "rank": 4,
        "name": "HotSpot 7.0 3D Thermal Baseline",
        "org": "Compact RC Thermal Engine",
        "track": "Hotspot Hero (Wave 8)",
        "score": 1800,
        "accuracy": 82.4,
        "date": "2026-11-01",
        "certId": "REF-HOTSPOT-7.0",
        "type": "hotspot"
    },
    {
        "rank": 5,
        "name": "UCIe 1.1 Standard Retimer Baseline",
        "org": "UCIe Consortium Specification",
        "track": "Chiplet Tycoon (Mission 5)",
        "score": 1750,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-UCIE-1.1",
        "type": "chiplet"
    },
    {
        "rank": 6,
        "name": "iSLIP Canonical 4x4 Arbiter Baseline",
        "org": "McKeown Reference Scheduler",
        "track": "Arbiter Arena (Wave 7)",
        "score": 1700,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-ISLIP-4X4",
        "type": "arbiter"
    },
    {
        "rank": 7,
        "name": "Slim Fly MMS Extremal Graph Baseline",
        "org": "ETH Zurich Reference Topology",
        "track": "Topology Titans (Mission 5)",
        "score": 1650,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-SLIM-FLY",
        "type": "topology"
    },
    {
        "rank": 8,
        "name": "Corona MWSR Photonic Crossbar Baseline",
        "org": "HP Labs Photonic Reference",
        "track": "Photon Pilot (Wave 6)",
        "score": 1600,
        "accuracy": 64,
        "date": "2026-11-01",
        "certId": "REF-CORONA-MWSR",
        "type": "optical"
    },
    {
        "rank": 9,
        "name": "Dally-Seitz Credit VC Flow Control Baseline",
        "org": "Canonical VC Credit Engine",
        "track": "Credit Commander (Wave 7)",
        "score": 1550,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-CREDIT-VC",
        "type": "credit"
    },
    {
        "rank": 10,
        "name": "BLESS Bufferless Deflection Router Baseline",
        "org": "SAFARI Reference Engine",
        "track": "Deflection Duel (Wave 6)",
        "score": 1500,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-BLESS-DEFLECTION",
        "type": "deflection"
    },
    {
        "rank": 11,
        "name": "Vicman Fault-Tolerant Reconfiguration Baseline",
        "org": "Fault-Resilient Architecture Model",
        "track": "Fault Defender (Wave 6)",
        "score": 1450,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-VICMAN-FAULT",
        "type": "fault"
    },
    {
        "rank": 12,
        "name": "Multi-VNET Coherence QoS Baseline",
        "org": "MOESI Directory Reference",
        "track": "QoS Gladiator (Wave 6)",
        "score": 1400,
        "accuracy": 100,
        "date": "2026-11-01",
        "certId": "REF-MOESI-QOS",
        "type": "qos"
    },
    {
        "rank": 13,
        "name": "Autonomous VFI PID DVFS Controller Baseline",
        "org": "Dark Silicon DVFS Reference",
        "track": "Volt Vortex (Wave 6)",
        "score": 1380,
        "accuracy": 45,
        "date": "2026-11-01",
        "certId": "REF-DVFS-PID",
        "type": "power"
    },
    {
        "rank": 14,
        "name": "Sub-THz 140 GHz Wireless Transceiver Baseline",
        "org": "Shahmoradi Transceiver Model",
        "track": "Wireless Wave (Wave 6)",
        "score": 1350,
        "accuracy": 7,
        "date": "2026-11-01",
        "certId": "REF-140GHZ-TRX",
        "type": "wireless"
    },
    {
        "rank": 15,
        "name": "AER Multicast SNN NoC Baseline",
        "org": "In-Network Computing Reference",
        "track": "Neuromorphic Nexus (Wave 6)",
        "score": 1320,
        "accuracy": 99.8,
        "date": "2026-11-01",
        "certId": "REF-SNN-NEXUS",
        "type": "neuromorphic"
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
            email = payload.get("email", "")
            country = payload.get("country", "")
            location = payload.get("location", "")
            ip = payload.get("ip", "")
            org = country if country and country != "Unknown Country" else payload.get("org", "Independent")
            score = int(payload.get("score", 0))
            accuracy = float(payload.get("accuracy", 100))
            cert_id = payload.get("certId", f"NOC-CERT-{issue.get('number', 0)}")
            date_str = payload.get("date", issue.get("created_at", "")[:10])
            mode = payload.get("mode", "comprehensive")
            track = "Grandmaster (Tier 3)" if mode == "grandmaster" else ("Fundamentals Sprint" if mode == "tier1_sprint" else "Comprehensive Exam")

            extracted_records.append({
                "name": name,
                "email": email,
                "org": org,
                "country": country,
                "location": location,
                "ip": ip,
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
        elif item_type == "optical":
            name = payload.get("player", payload.get("name", "Photon Pilot"))
            org = payload.get("org", "Silicon Photonics Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            guided = int(payload.get("guided", 0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Photon Pilot (Wave {wave})",
                "score": score,
                "accuracy": guided,
                "certId": f"PHOTON-WAVE-{wave}",
                "date": date_str,
                "type": "optical",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "credit":
            name = payload.get("player", payload.get("name", "Credit Commander"))
            org = payload.get("org", "Interconnect Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            delivered = int(payload.get("delivered", 0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Credit Commander (Wave {wave})",
                "score": score,
                "accuracy": delivered,
                "certId": f"CREDIT-WAVE-{wave}",
                "date": date_str,
                "type": "credit",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "deflection":
            name = payload.get("player", payload.get("name", "Deflection Ace"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            delivered = int(payload.get("delivered", 0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Deflection Duel (Wave {wave})",
                "score": score,
                "accuracy": delivered,
                "certId": f"DEFLECT-WAVE-{wave}",
                "date": date_str,
                "type": "deflection",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "fault":
            name = payload.get("player", payload.get("name", "Silicon Defender"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            rescued = int(payload.get("rescued", 0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Fault Defender (Wave {wave})",
                "score": score,
                "accuracy": rescued,
                "certId": f"FAULT-WAVE-{wave}",
                "date": date_str,
                "type": "fault",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "qos":
            name = payload.get("player", payload.get("name", "QoS Commander"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            delivered = int(payload.get("delivered", 0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"QoS Gladiator (Wave {wave})",
                "score": score,
                "accuracy": delivered,
                "certId": f"QOS-WAVE-{wave}",
                "date": date_str,
                "type": "qos",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "power":
            name = payload.get("player", payload.get("name", "Volt Maestro"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            saved_joules = float(payload.get("saved_joules", 0.0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Volt Vortex (Wave {wave})",
                "score": score,
                "accuracy": saved_joules,
                "certId": f"POWER-WAVE-{wave}",
                "date": date_str,
                "type": "power",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "wireless":
            name = payload.get("player", payload.get("name", "RF Navigator"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            speedup = float(payload.get("speedup", 1.0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Wireless Wave (Wave {wave})",
                "score": score,
                "accuracy": speedup,
                "certId": f"WIRELESS-WAVE-{wave}",
                "date": date_str,
                "type": "wireless",
                "issue_url": issue.get("html_url")
            })
        elif item_type == "neuromorphic":
            name = payload.get("player", payload.get("name", "Neuromorphic Pioneer"))
            org = payload.get("org", "Silicon Lab")
            score = int(payload.get("score", 0))
            wave = int(payload.get("wave", 1))
            firings = int(payload.get("firings", 0))
            date_str = payload.get("date", issue.get("created_at", "")[:10])

            extracted_records.append({
                "name": name,
                "org": org,
                "track": f"Neuromorphic Nexus (Wave {wave})",
                "score": score,
                "accuracy": firings,
                "certId": f"SNN-WAVE-{wave}",
                "date": date_str,
                "type": "neuromorphic",
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
