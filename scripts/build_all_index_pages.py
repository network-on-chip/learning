#!/usr/bin/env python3
"""Builds index.md files for all 13 tracks with proper links, roadmaps, and syllabus.
"""

from pathlib import Path

LEARNING_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = LEARNING_DIR / "docs"

def write(rel, text):
    p = DOCS_DIR / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"Generated Index: {rel}")

def build_all_indexes():
    tracks_meta = [
        (1, "track1-interconnect-crisis", "Interconnect Crisis & Wire Physics",
         "Why shared buses failed. Dennard scaling breakdown, quantum tunneling, RC wire delays, Mayadas-Shatzkes scattering, and optimal repeater spacing.",
         1, "ch01-interconnect-crisis",
         [
             (1, "Why Network-on-Chip?", "Evolution from shared bus bottlenecks to point-to-point packet routing.", "01-why-noc", "Interactive Bus Contention Simulator & RTL"),
             (2, "Nanoscale Wire Physics & Elmore RC Delay", "Distributed Elmore RC delay formula and copper resistivity inflation down to 3nm.", "02-wire-scaling-elmore", "Interactive Wire Wizard Simulator"),
             (3, "Optimal Repeater Insertion & Scattering Physics", "Linearize quadratic wire delay via Bakoglu spacing and Fuchs-Sondheimer surface scattering.", "03-repeater-insertion", "Analytical Repeater Spacing Calculator"),
             (4, "Global Interconnect Energy & Physical Limits", "Interconnect dynamic energy CV^2f scaling and the definitive death of shared buses.", "04-energy-limits-interconnect", "Energy Dissipation Model & Chapter Quiz")
         ],
         "graph TD\n  RC['Elmore RC Wire Delay'] --> BusBottleneck['Shared Bus Breakdown']\n  BusBottleneck --> Repeater['Bakoglu Repeater Insertion']\n  Repeater --> NoC['Network-on-Chip Paradigm']"),

        (2, "track2-switching-flow-control", "Switching, Flow Control & Buffers",
         "Wormhole vs VCT switching, flits/phits, credit turnaround latency loops, Virtual Channel buffers, and AXI4/TileLink NI packetization.",
         2, "ch02-switching-flow-control",
         [
             (1, "Packets, Flits & Phits", "Hierarchy of data transmission: Messages, Packets, Flits, and physical wire Phits.", "01-packet-switching-flits", "Flit Packetization Simulator"),
             (2, "Switching Mechanisms: SAF, VCT & Wormhole", "Deep dive into Store-and-Forward, Virtual Cut-Through, and Wormhole buffer allocation.", "02-switching-mechanisms", "Zero-Load Latency Equation Explorer"),
             (3, "Flow Control & Credit Turnaround Loops", "Lossless backpressure, credit turnaround latency loops, and minimum buffer sizing B_min >= RTT.", "03-flow-control-credit", "Credit Commander Flow Control Simulator"),
             (4, "Network Interfaces & AXI Packetization", "Translating CPU memory requests (AXI4/TileLink) into on-chip flit streams.", "04-network-interface-packetization", "Synthesizable NI Verilog RTL")
         ],
         "graph TD\n  Data['Messages & Packets'] --> Flits['Flits & Phits']\n  Flits --> Switching['Wormhole Switching']\n  Switching --> Credits['Credit Loop Flow Control']"),

        (3, "track3-router-microarchitecture", "Router Microarchitecture & Arbitration",
         "Canonical 4-stage pipeline, speculative parallel VA/SA allocation, matrix & wavefront arbiters (sub-200ps LRU), and SMART bypass routers.",
         3, "ch03-router-microarchitecture",
         [
             (1, "Canonical Router Pipeline Stages", "5-stage pipeline: Buffer Write, Route Computation, Virtual Channel Allocation, Switch Allocation, Traversal.", "01-pipeline-stages", "Pipeline Timing Simulator & Verilog RTL"),
             (2, "Virtual Channel (VC) Management", "Eliminating head-of-line blocking by multiplexing multiple logical FIFOs onto single physical links.", "02-virtual-channels", "VC Queue State Visualizer"),
             (3, "Arbitration & Crossbar Switching", "Fast sub-200ps matrix arbiters, round-robin priority encoders, and crossbar scheduling.", "03-arbitration-crossbar", "Arbiter Arena Challenge & Verilog"),
             (4, "Low-Latency & SMART Bypass Routers", "Single-cycle multi-hop bypass networks (SMART) traversing up to 8 hops per cycle.", "04-low-latency-bypass-routers", "SMART Bypass Route Analyzer")
         ],
         "graph TD\n  BW['Buffer Write'] --> RC['Route Computation']\n  RC --> VA['Virtual Channel Alloc']\n  VA --> SA['Switch Allocation']\n  SA --> ST['Switch Traversal & Bypass']"),

        (4, "track4-topologies-and-metrics", "Direct, Indirect & High-Radix Topologies",
         "Direct (Mesh, Torus), Indirect (Clos, Fat-Tree, cMesh), and High-Radix (Dragonfly, Flattened Butterfly). Mathematical derivations of T0, Theta_sat, and bisection bandwidth.",
         4, "ch04-topologies-and-metrics",
         [
             (1, "Direct Topologies: Mesh & Torus", "Cartesian topologies, wrap-around links, Folded Torus layout, and bisection bandwidth proofs.", "01-direct-topologies", "Interactive 2D Mesh & Torus Simulator"),
             (2, "Indirect & Concentrated Networks", "Clos networks, Fat-Trees, and node concentration (cMesh) reducing router count.", "02-indirect-hierarchical", "Concentrated Mesh Floorplanner"),
             (3, "Interconnect Metrics & Traffic Patterns", "Bisection bandwidth, network diameter, zero-load latency T0, and synthetic traffic patterns.", "03-metrics-traffic-patterns", "Throughput & Latency Curve Analyzer"),
             (4, "High-Radix Networks: Dragonfly & Flattened Butterfly", "Exploiting high-radix routers to minimize network diameter, coupled with UGAL adaptive routing.", "04-high-radix-topologies", "Dragonfly Group Routing Simulator")
         ],
         "graph TD\n  Mesh['2D Mesh & Torus'] --> cMesh['Concentrated cMesh']\n  cMesh --> HighRadix['High-Radix Dragonfly']\n  HighRadix --> Metrics['Bisection & Saturation Metrics']"),

        (5, "track5-routing-deadlock", "Deadlock Theory, Turn Models & Routing",
         "Deterministic DOR (XY), Glass & Ni turn model, Chiu odd-even, Duato escape channels, Channel Dependency Graphs, and VNET protocol isolation.",
         5, "ch05-routing-deadlock-theory",
         [
             (1, "Deterministic Dimension-Order Routing (DOR)", "Proof of deadlock freedom for XY routing in 2D meshes via monotonic coordinate order.", "01-deterministic-dor", "Dimension-Order Routing Visualizer"),
             (2, "Turn Models: West-First, North-Last & Odd-Even", "Prohibiting specific turns to break cycles in CDG without sacrificing connectivity.", "02-adaptive-turn-model", "Adaptive Turn Model Explorer"),
             (3, "Channel Dependency Graphs & Duato's Theorem", "Formal CDG cycle-free condition and escaping deadlock using a minimal set of escape VCs.", "03-deadlock-theory-cdg", "SMT CDG Cycle Verifier & RTL"),
             (4, "Fault-Tolerant Routing & Protocol Deadlocks", "Handling link/router faults with Up*/Down* routing, and resolving request-reply protocol deadlocks.", "04-fault-tolerant-protocol-deadlock", "Deadlock Buster Arcade Game")
         ],
         "graph TD\n  DOR['Dimension-Order XY'] --> TurnModels['Turn Models (Odd-Even)']\n  TurnModels --> Duato['Duato Escape Channels']\n  Duato --> FaultTolerant['Fault-Tolerant VNETs']"),

        (6, "track6-low-power-dark-silicon", "Low-Power Architectures & Dark Silicon",
         "Dark silicon physics, Thermal Design Power (TDP) budgets, Voltage/Frequency Islands (VFIs), fine-grained power gating, and L*di/dt emergencies.",
         6, "ch06-low-power-dark-silicon",
         [
             (1, "Dark Silicon Physics & TDP Scaling Limits", "Why Dennard scaling death leaves up to 80% of silicon unpowered at 3nm.", "01-dark-silicon-physics", "Dark Silicon Floorplan Calculator"),
             (2, "Voltage & Frequency Islands (VFIs) and DVFS", "Multi-domain voltage scaling, asynchronous FIFO clock-domain crossings, and energy-delay product.", "02-dvfs-voltage-islands", "Volt Vortex Interactive Lab"),
             (3, "Router Microarchitectural Power Gating", "Sleep transistors, wake-up latency penalties, lookahead credit power wakeup, and zero-leakage state.", "03-power-gating-router", "Synthesizable Power Gating FSM RTL"),
             (4, "Voltage Emergencies & Energy-Efficient Encoding", "Inductive L*di/dt resonance, decap allocation, bus-invert coding, and energy-delay optimization.", "04-voltage-emergencies-energy", "L-di/dt Noise Analyzer")
         ],
         "graph TD\n  Dennard['Dennard Breakdown'] --> DarkSilicon['Dark Silicon Floorplans']\n  DarkSilicon --> DVFS['Voltage/Frequency Islands']\n  DVFS --> PowerGating['Router Micro Power Gating']"),

        (7, "track7-thermal-fault-tolerance", "Thermal Modeling & Fault Tolerance",
         "Fourier heat conduction, compact thermal RC models (HotSpot), Regional Congestion Awareness (RCA), ML thermal forecasting, and sensor placement.",
         7, "ch07-thermal-fault-tolerance",
         [
             (1, "Silicon Thermal Physics & Compact RC Modeling", "Fourier heat diffusion, silicon thermal conductivity, compact RC ladder networks, and HotSpot.", "01-thermal-physics-rc-modeling", "Interactive RC Thermal Network Model"),
             (2, "Congestion Awareness & Dynamic Thermal Throttling", "Regional Congestion Awareness (RCA), hot-carrier injection degradation, and source throttling.", "02-congestion-detection-throttling", "Hotspot Hero Thermal Defense Arcade"),
             (3, "Proactive Machine-Learning Hotspot Prediction", "Lightweight online regression predictors anticipating thermal runaway before critical Tj_max.", "03-hotspot-prediction-ml", "ML Hotspot Forecast Explorer"),
             (4, "Optimal Sensor Placement & Field Reconstruction", "Reconstructing full-die thermal fields from sparse sensors under non-Gaussian noise.", "04-thermal-sensor-placement", "Thermal Sensor Grid Reconstructor")
         ],
         "graph TD\n  Fourier['Fourier Thermal Physics'] --> RC['Compact RC HotSpot Model']\n  RC --> RCA['Regional Congestion Awareness']\n  RCA --> MLHotspot['ML Proactive Thermal Defense']"),

        (8, "track8-3d-noc-tsvs", "Three-Dimensional NoC (3D-NoC) & TSVs",
         "Through-Silicon Vias (TSVs), Keep-Out Zones (KOZ), thermo-mechanical stress, 7-port 3D crossbars, vertical serialization, and 3D thermal stacking.",
         8, "ch08-3d-noc-tsvs",
         [
             (1, "3D Integration & Through-Silicon Via (TSV) Physics", "TSV aspect ratios, capacitive parasitics, microbump arrays, and vertical link scaling.", "01-3d-tsv-interconnects", "TSV Parasitic & Delay Explorer"),
             (2, "TSV Keep-Out Zones (KOZ) & Stress Fields", "Thermo-mechanical mismatch (Cu vs Si), piezoresistive mobility shifts, and KOZ floorplanning.", "02-tsv-parasitics-koz", "KOZ Stress Field Visualizer"),
             (3, "3D Router Microarchitecture & 7-Port Crossbars", "Up/Down vertical port allocation, asymmetric vertical serialization, and 3D arbiters.", "03-3d-router-microarchitecture", "7-Port 3D Router SystemVerilog RTL"),
             (4, "3D Topologies, Thermal Stacking & Routing Deadlock", "Vertical heat dissipation bottlenecks, true 3D deadlock models, and dimension-order extensions.", "04-3d-topologies-thermal-deadlock", "TSV Titan 3D Architecture Lab")
         ],
         "graph TD\n  TSVPhysics['TSV Parasitics & KOZ'] --> Microarch3D['7-Port 3D Router Microarch']\n  Microarch3D --> ThermalStacking['3D Thermal Stacking Bottlenecks']\n  ThermalStacking --> Deadlock3D['3D Deadlock Freedom']"),

        (9, "track9-chiplets-ucie", "Multi-Chiplet Interconnects & UCIe",
         "2.5D packaging (CoWoS, EMIB), negative binomial yield economics, UCIe 1.0/2.0 standard, In/Outbound swap deadlock recovery, and BuffeRS bypassing.",
         9, "ch09-chiplets-ucie",
         [
             (1, "2.5D Packaging Economics & Reticle Limits", "Disaggregation economics, negative binomial yield models, CoWoS silicon interposers, and EMIB bridges.", "01-25d-packaging-economics", "Chiplet Tycoon Advanced Packaging"),
             (2, "UCIe Protocol Stack & D2D Physical Layer", "Universal Chiplet Interconnect Express (UCIe) standard, D2D physical adapter, and die-to-die streaming protocols.", "02-chiplets-ucie-interconnects", "UCIe Protocol Frame Inspector"),
             (3, "Cross-Die Boundary Deadlock Recovery", "Boundary interface deadlocks, cyclic subpath proofs, and TCAD '26 In/Outbound backtracking swap.", "03-cross-die-deadlock-recovery", "In/Outbound Swap Deadlock Solver"),
             (4, "Multi-Chiplet Router Bypassing & BuffeRS", "Near wire-speed inter-die transit, TCAD '26 BuffeRS scheduling, and dynamic vertical link selection.", "04-multichiplet-router-bypassing", "Web EDA BuffeRS Evaluator")
         ],
         "graph TD\n  YieldEconomics['Negative Binomial Yield'] --> UCIeStack['UCIe 1.0/2.0 D2D Standard']\n  UCIeStack --> BoundaryDeadlock['Cross-Die Deadlock Recovery']\n  BoundaryDeadlock --> BuffeRS['BuffeRS Wire-Speed Bypassing']"),

        (10, "track10-optical-wireless", "Optical & Wireless Networks-on-Chip",
         "Silicon nanophotonics, microring resonators (MRRs), wavelength-routed ONoC (WRONoC), laser power-gating, and on-chip mmWave/THz wireless antennas.",
         10, "ch10-optical-wireless",
         [
             (1, "Silicon Nanophotonics & Microring Resonators", "Waveguides, microring resonators (MRRs), electro-optic modulation, and zero-capacitance light flight.", "01-silicon-nanophotonics-mrrs", "Photon Pilot Optical Grid"),
             (2, "Wavelength-Routed Optical NoC (WRONoC)", "Dense Wavelength-Division Multiplexing (DWDM), non-blocking optical crossbar matrices, and insertion loss.", "02-wronoc-optical-crossbars", "Optical Insertion Loss Analyzer"),
             (3, "Laser Power-Gating & Thermal Drift Compensation", "Silicon thermo-optic coefficients (0.10 nm/K), Automated Phase Control (APC), and laser power efficiency.", "03-laser-power-gating-apc", "APC Thermal Drift Simulator"),
             (4, "On-Chip Wireless NoC (WiNoC) Frontiers", "Millimeter-wave and terahertz on-chip antennas, zig-zag transceivers, and small-world global shortcuts.", "04-wireless-noc-frontiers", "Wireless Wave mmWave Explorer")
         ],
         "graph TD\n  Photonics['Silicon Nanophotonics & MRRs'] --> WRONoC['Dense WDM Optical Crossbars']\n  WRONoC --> LaserPower['Laser Power-Gating & APC']\n  LaserPower --> WiNoC['On-Chip mmWave/THz Wireless']"),

        (11, "track11-security", "Hardware Security & Trust in On-Chip Networks",
         "Multi-tenant threat models, thermal and timing covert channels, online WMA anomaly filtering (TCAD '26 HeatSense), and Physical Unclonable Functions (PUFs).",
         11, "ch11-security",
         [
             (1, "Security Threat Models in On-Chip Networks", "Multi-tenant SoCs, untrusted third-party IPs, buffer-flooding DoS, and eavesdropping taxonomy.", "01-security-threat-models", "Silicon Sentinel Defense Arcade"),
             (2, "Thermal & Timing Covert Channels", "Packet inter-arrival delay modulation, substrate thermal conduction leakage, and 256-bit AES exfiltration.", "02-thermal-timing-covert-channels", "Timing Jitter Covert Channel Analyzer"),
             (3, "Online WMA Anomaly Detection (HeatSense)", "Hardware-friendly fixed-point EWMA tracking, adaptive threshold bounds, and IEEE TCAD '26 HeatSense.", "03-heatsense-wma-anomaly-detection", "Synthesizable WMA Verilog RTL"),
             (4, "Hardware Trojan Defense & Zero-Trust Quarantine", "Autonomous clock gating, packet deflection, and intrinsic interconnect wire-delay PUF authentication.", "04-trojan-defense-quarantine", "Web EDA HeatSense Verification")
         ],
         "graph TD\n  ThreatModel['Multi-Tenant Threat Models'] --> CovertChannels['Thermal & Timing Covert Channels']\n  CovertChannels --> HeatSense['Online WMA Anomaly Detection']\n  HeatSense --> Quarantine['Zero-Trust Autonomous Quarantine']"),

        (12, "track12-ai-llm-snn", "Domain-Specific NoCs for LLMs, Transformers & SNNs",
         "Generative AI communication collectives, in-network reduction crossbars (PAC-NoC), wafer-scale Ruche express links, and neuromorphic spike multicasting.",
         12, "ch12-ai-llm-snn",
         [
             (1, "LLM Collective Communication Bottlenecks", "All-Reduce, All-to-All, and Ring-Attention communication bounds in 100B+ parameter models.", "01-llm-collective-communication", "Transformer Titan Accelerator Arcade"),
             (2, "In-Network Reduction Crossbars (PAC-NoC)", "In-flight gradient accumulation inside router crossbars, halving memory bandwidth demand (IEEE TVLSI '26).", "02-in-network-reduction-crossbars", "In-Network Reduction Verilog RTL"),
             (3, "Wafer-Scale Fabrics & Ruche Express Links", "2,048-core Cerebras-class wafer-scale fabrics, upper-metal express links, and defect bypass grids.", "03-wafer-scale-ruche-fabrics", "Ruche Express Link Simulator"),
             (4, "Neuromorphic Event-Driven Spike Multicasting", "Address-Event Representation (AER), event-driven multicast trees, and SNNcut hypergraph partitioning.", "04-neuromorphic-snn-multicast", "Neuromorphic Nexus Spike Router")
         ],
         "graph TD\n  LLMCollectives['LLM All-Reduce Communication'] --> PACNoC['In-Network Reduction Crossbars']\n  PACNoC --> Ruche['Wafer-Scale Ruche Express Links']\n  Ruche --> Neuromorphic['AER Spiking Multicast Trees']"),

        (13, "track13-capstone", "Capstone: Landmark Silicon Case Studies & System Synthesis",
         "Seminal taped-out silicon case studies (Intel SCC 48-Core, NVIDIA Simba 36-Die MCM, 3D Optical NoC) and the Grand Synthesis MoE Accelerator Challenge.",
         13, "index",
         [
             (1, "The Manycore Milestone: Intel 48-Core SCC", "Intel Labs 45nm tapeout, message-passing buffers (MPB), 2-TB/s mesh, and Wrapped Wave-Front Allocation.", "01-intel-scc-mesh", "Intel SCC Mesh Simulator & RTL"),
             (2, "The Multi-Chiplet Revolution: NVIDIA Simba", "36-chiplet 2.5D MCM deep learning accelerator, 0.54 pJ/bit Ground-Referenced Signaling (GRS), and multicast.", "02-nvidia-simba-mcm", "Simba MCM Explorer & Multicast RTL"),
             (3, "3D Optical NoC for MPSoCs", "Reduced-MRR non-blocking crossbars, Automated Phase Control (APC), and hybrid 3D integration.", "03-3d-optical-noc", "3D Optical Crossbar Simulator"),
             (4, "In-Network Computing Neuromorphic Router", "Silicon-verified partial-sum in-flight reduction delivering 1.63 pJ/SOP for bio-inspired neuromorphic chips.", "04-in-network-neuromorphic", "Neuromorphic INC Crossbar RTL"),
             (5, "Capstone Challenge: Zero-Trust MoE Accelerator", "The Grand Synthesis: 16-chiplet active interposer fabric, All-Reduce collective tree, WMA Trojan defense, and STA.", "05-grand-synthesis-moe", "Web EDA Automated Capstone Grading")
         ],
         "graph TD\n  SCC['Intel 48-Core SCC'] --> Simba['NVIDIA Simba 36-Chiplet MCM']\n  Simba --> Optical3D['3D Optical & In-Network Computing']\n  Optical3D --> CapstoneMoE['Grand Synthesis: Zero-Trust MoE Accelerator Top']")
    ]

    for track_num, dir_name, title, subtitle, ch_num, ch_slug, lessons, mermaid in tracks_meta:
        idx_content = generate_track_index(track_num, dir_name, title, subtitle, ch_num, ch_slug, lessons, mermaid)
        write(f"{dir_name}/index.md", idx_content)

    print("All 13 track index files generated successfully.")

def generate_track_index(track_num, track_slug, title, subtitle, ch_num, ch_slug, lessons_data, mermaid_graph):
    lessons_html = ""
    for l_num, l_title, l_desc, l_file, l_feat in lessons_data:
        lessons_html += f"""
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson {track_num}.{l_num}</span>
      <div class="noc-track-title">{l_title}</div>
      <div class="noc-track-desc">{l_desc}</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> {l_feat}
      </div>
    </div>
    <a href="{l_file}/" class="noc-track-link">Launch Lesson {track_num}.{l_num} →</a>
  </div>
"""

    ch_link_block = f"""
<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>📚 Aligned with Chapter {ch_num} of Official 12-Chapter Textbook</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Explore complete theoretical derivations, physical scaling parameters, and microarchitectural proofs in <strong>Chapter {ch_num}</strong>.
    </div>
  </div>
  <a href="../textbook/{ch_slug}/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Read Chapter {ch_num} in Textbook →</span>
  </a>
</div>
""" if ch_num <= 12 else f"""
<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>🏆 Capstone System Synthesis: Grounded in Chapters 1–12</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Synthesize wire physics (Ch 1–3), topologies & deadlock (Ch 4–5), thermal/power defense (Ch 6–7), 3D & chiplets (Ch 8–9), and emerging frontiers (Ch 10–12).
    </div>
  </div>
  <a href="../textbook/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Explore Official 12-Chapter Textbook →</span>
  </a>
</div>
"""

    return f"""# Track {track_num}: {title}

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module {track_num:02d}</div>
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ {len(lessons_data)} In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🔬 Interactive Simulators &amp; Tools</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">💻 Synthesizable Verilog RTL</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">📜 Grounded in Official Monograph</span>
  </div>
</div>

{ch_link_block}

---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track {track_num} connect across the physical and protocol layers:

```mermaid
{mermaid_graph}
```

---

## 📚 Syllabus & Lessons in Track {track_num}

<div class="noc-tracks-grid">
{lessons_html}
</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track {track_num} using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
"""

if __name__ == "__main__":
    build_all_indexes()
