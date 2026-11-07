#!/usr/bin/env python3
"""Script to expand NoC learning curriculum from 7 tracks to 12 Core Tracks + Track 13 Capstone.
Ensures 1:1 parity with the 12 official textbook chapters.
"""

import os
import shutil
from pathlib import Path

LEARNING_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = LEARNING_DIR / "docs"

def main():
    print("=== Expanding NoC Curriculum to 12 Core Tracks + Track 13 Capstone ===")

    # Track directory mappings
    tracks = [
        ("track1-interconnect-crisis", "Track 1: Interconnect Crisis & Wire Physics", 1),
        ("track2-switching-flow-control", "Track 2: Switching, Flow Control & Buffers", 2),
        ("track3-router-microarchitecture", "Track 3: Router Microarchitecture & Arbitration", 3),
        ("track4-topologies-and-metrics", "Track 4: Direct, Indirect & High-Radix Topologies", 4),
        ("track5-routing-deadlock", "Track 5: Deadlock Theory, Turn Models & Adaptive Routing", 5),
        ("track6-low-power-dark-silicon", "Track 6: Low-Power Architectures & Dark Silicon", 6),
        ("track7-thermal-fault-tolerance", "Track 7: Thermal Modeling, Hotspots & Fault Tolerance", 7),
        ("track8-3d-noc-tsvs", "Track 8: Three-Dimensional NoC (3D-NoC) & TSVs", 8),
        ("track9-chiplets-ucie", "Track 9: Multi-Chiplet Interconnects & UCIe", 9),
        ("track10-optical-wireless", "Track 10: Optical & Wireless Networks-on-Chip", 10),
        ("track11-security", "Track 11: Hardware Security & Trust in On-Chip Networks", 11),
        ("track12-ai-llm-snn", "Track 12: Domain-Specific NoCs for LLMs, Transformers & SNNs", 12),
        ("track13-capstone", "Track 13: Capstone — Landmark Silicon Case Studies & System Synthesis", 13)
    ]

    for dir_name, title, num in tracks:
        p = DOCS_DIR / dir_name
        p.mkdir(parents=True, exist_ok=True)
        print(f"Created/Verified directory: {dir_name}")

    # Copy existing files into new structure
    # Track 1 -> track1-interconnect-crisis
    old_t1 = DOCS_DIR / "track1-fundamentals"
    if old_t1.exists():
        shutil.copy2(old_t1 / "01-why-noc.md", DOCS_DIR / "track1-interconnect-crisis" / "01-why-noc.md")
        shutil.copy2(old_t1 / "02-packet-switching-flits.md", DOCS_DIR / "track2-switching-flow-control" / "01-packet-switching-flits.md")
        shutil.copy2(old_t1 / "03-flow-control-credit.md", DOCS_DIR / "track2-switching-flow-control" / "03-flow-control-credit.md")
        shutil.copy2(old_t1 / "04-network-interface-packetization.md", DOCS_DIR / "track2-switching-flow-control" / "04-network-interface-packetization.md")
        print("Migrated old Track 1 files to Track 1 and Track 2.")

    # Track 2 -> track3-router-microarchitecture
    old_t2 = DOCS_DIR / "track2-router-architecture"
    if old_t2.exists():
        for f in old_t2.glob("0*.md"):
            shutil.copy2(f, DOCS_DIR / "track3-router-microarchitecture" / f.name)
        print("Migrated old Track 2 files to Track 3.")

    # Track 3 -> track4-topologies-and-metrics
    old_t3 = DOCS_DIR / "track3-topologies"
    if old_t3.exists():
        for f in old_t3.glob("0*.md"):
            shutil.copy2(f, DOCS_DIR / "track4-topologies-and-metrics" / f.name)
        print("Migrated old Track 3 files to Track 4.")

    # Track 4 -> track5-routing-deadlock
    old_t4 = DOCS_DIR / "track4-routing-deadlock"
    if old_t4.exists():
        for f in old_t4.glob("0*.md"):
            shutil.copy2(f, DOCS_DIR / "track5-routing-deadlock" / f.name)
        print("Migrated old Track 4 files to Track 5.")

    # Track 5 -> track7-thermal-fault-tolerance
    old_t5 = DOCS_DIR / "track5-congestion-thermal"
    if old_t5.exists():
        for f in old_t5.glob("0*.md"):
            shutil.copy2(f, DOCS_DIR / "track7-thermal-fault-tolerance" / f.name)
        print("Migrated old Track 5 files to Track 7.")

    # Track 6 -> Track 8, 9, 10
    old_t6 = DOCS_DIR / "track6-chiplets-and-3d"
    if old_t6.exists():
        shutil.copy2(old_t6 / "01-3d-tsv-interconnects.md", DOCS_DIR / "track8-3d-noc-tsvs" / "01-3d-tsv-interconnects.md")
        shutil.copy2(old_t6 / "03-3d-topologies-thermal-deadlock.md", DOCS_DIR / "track8-3d-noc-tsvs" / "04-3d-topologies-thermal-deadlock.md")
        shutil.copy2(old_t6 / "02-chiplets-ucie-interconnects.md", DOCS_DIR / "track9-chiplets-ucie" / "02-chiplets-ucie-interconnects.md")
        shutil.copy2(old_t6 / "04-optical-wireless-frontiers.md", DOCS_DIR / "track10-optical-wireless" / "04-wireless-noc-frontiers.md")
        print("Migrated old Track 6 files to Tracks 8, 9, and 10.")

    # Track 7 -> track13-capstone
    old_t7 = DOCS_DIR / "track7-paper-walkthroughs"
    if old_t7.exists():
        for f in old_t7.glob("0*.md"):
            shutil.copy2(f, DOCS_DIR / "track13-capstone" / f.name)
        print("Migrated old Track 7 files to Track 13 (Capstone).")

    print("Directory scaffolding and migration complete.")

if __name__ == "__main__":
    main()

