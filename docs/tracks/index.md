# 📚 Network-on-Chip Curriculum: 13 Comprehensive Tracks

<div class="noc-hero">
  <div class="noc-track-badge">✨ Official Comprehensive Syllabus • 13 Modules • 53 Lessons</div>
  <h1>Network-on-Chip & Advanced Interconnects Curriculum</h1>
  <p class="subtitle">
    A rigorous, university-grade curriculum mapping 1:1 to the 12 definitive textbook chapters of the official monograph, culminating in a full-scale Capstone System Synthesis challenge. Designed for undergraduate students, graduate researchers, and silicon computer architects.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">📖 12 Textbook Chapters</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🏆 13 Structured Tracks</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">⚡ 53 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">💻 Synthesizable SystemVerilog RTL</span>
  </div>
</div>

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 18px 22px; margin: 24px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>📘 Complete 1:1 Book &amp; Hardware Alignment</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px; max-width: 800px; line-height: 1.5;">
      Every track corresponds directly to an official textbook chapter. Each lesson provides theoretical derivations, synthesizable SystemVerilog cores verified against Nangate45 open-cell libraries, and interactive browser-based simulation workbenches.
    </div>
  </div>
  <a href="../textbook/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Explore Textbook (12 Chaps) →</span>
  </a>
</div>

---

## 🗺️ Master Curriculum Architecture Roadmap

The 13 tracks form an end-to-end stack spanning nanoscale silicon physics to exascale collective accelerators:

```mermaid
graph TD
  subgraph Tier1["Tier 1: Physical & Data-Link Fundamentals"]
    T1["Track 1: Interconnect Crisis & Wire Physics<br/>(Elmore RC, Repeater Spacing)"]
    T2["Track 2: Switching, Flow Control & Buffers<br/>(Wormhole, Credit Loops, AXI)"]
    T1 --> T2
  end

  subgraph Tier2["Tier 2: Router Microarchitecture & Topologies"]
    T3["Track 3: Router Microarchitecture & Arbitration<br/>(5-Stage Pipeline, SMART Bypass)"]
    T4["Track 4: Direct, Indirect & High-Radix Topologies<br/>(Mesh, Torus, Dragonfly, Clos)"]
    T2 --> T3
    T3 --> T4
  end

  subgraph Tier3["Tier 3: Deadlock Theory & Physical Constraints"]
    T5["Track 5: Deadlock Theory & Adaptive Routing<br/>(Turn Models, CDG, Duato Escapes)"]
    T6["Track 6: Low-Power Architectures & Dark Silicon<br/>(VFIs, Power-Gating, L*di/dt)"]
    T7["Track 7: Thermal Modeling & Fault Tolerance<br/>(RC HotSpot, RCA, ML Hotspots)"]
    T4 --> T5
    T5 --> T6
    T6 --> T7
  end

  subgraph Tier4["Tier 4: Advanced Packaging & 3D Integration"]
    T8["Track 8: 3D-NoC & Through-Silicon Vias<br/>(TSV Parasitics, KOZ, 7-Port Crossbars)"]
    T9["Track 9: Multi-Chiplet Interconnects & UCIe<br/>(2.5D Yield, UCIe D2D, In/Outbound Swap)"]
    T7 --> T8
    T8 --> T9
  end

  subgraph Tier5["Tier 5: Emerging Frontiers & Capstone Synthesis"]
    T10["Track 10: Optical & Wireless Networks-on-Chip<br/>(MRRs, WRONoC, APC Loops, mmWave)"]
    T11["Track 11: Hardware Security & Trust in NoCs<br/>(Covert Channels, HeatSense EWMA, Quarantine)"]
    T12["Track 12: Domain-Specific NoCs for AI & LLMs<br/>(All-Reduce Reduction, Ruche, SNNs)"]
    T13["Track 13: Capstone System Synthesis<br/>(Intel SCC, Simba, 3D Optical, Zero-Trust MoE)"]
    T9 --> T10
    T10 --> T11
    T11 --> T12
    T12 --> T13
  end
```

---

## 📚 All 13 Curriculum Tracks

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 1 • Aligned with Chapter 1</span>
      <div class="noc-track-title">Interconnect Crisis &amp; Wire Physics</div>
      <div class="noc-track-desc">
        Why shared buses failed. Dennard scaling breakdown, wire aspect ratios, Elmore distributed RC delay modeling, Fuchs-Sondheimer scattering, and optimal repeater insertion.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Synthesizable Elmore Verilog • Interactive Wire Simulator
      </div>
    </div>
    <a href="../track1-interconnect-crisis/" class="noc-track-link">Explore Track 1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 2 • Aligned with Chapter 2</span>
      <div class="noc-track-title">Switching, Flow Control &amp; Buffers</div>
      <div class="noc-track-desc">
        Packets, flits, and phits. Store-and-Forward vs Virtual Cut-Through vs Wormhole switching, credit turnaround latency loops, Virtual Channel FIFO buffers, and AXI4/TileLink NI packetization.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Credit Counter RTL • Credit Commander Simulator
      </div>
    </div>
    <a href="../track2-switching-flow-control/" class="noc-track-link">Explore Track 2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 3 • Aligned with Chapter 3</span>
      <div class="noc-track-title">Router Microarchitecture &amp; Arbitration</div>
      <div class="noc-track-desc">
        Canonical 5-stage router pipelines (BW-RC-VA-SA-ST), Virtual Channel allocation, sub-200ps LRU matrix arbiters, wavefront scheduling, and SMART single-cycle multi-hop bypass routers.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • 5-Stage SystemVerilog Router • Arbiter Arena Lab
      </div>
    </div>
    <a href="../track3-router-microarchitecture/" class="noc-track-link">Explore Track 3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 4 • Aligned with Chapter 4</span>
      <div class="noc-track-title">Direct, Indirect &amp; High-Radix Topologies</div>
      <div class="noc-track-desc">
        Direct (Mesh, Torus, Folded Torus), Indirect (Clos, Fat-Tree, cMesh), and High-Radix (Dragonfly, Flattened Butterfly). Mathematical derivations of $T_0$, $\Theta_{sat}$, and UGAL routing.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Topology Graph Metrics RTL • Interactive Topology Architect
      </div>
    </div>
    <a href="../track4-topologies-and-metrics/" class="noc-track-link">Explore Track 4 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 5 • Aligned with Chapter 5</span>
      <div class="noc-track-title">Deadlock Theory, Turn Models &amp; Routing</div>
      <div class="noc-track-desc">
        Deterministic Dimension-Order Routing (DOR), Glass &amp; Ni's Turn Model, Chiu's Odd-Even algorithm, Duato's Escape Channels, CDG acyclic proofs, and Cache Coherence VNET isolation.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • SMT CDG Verifier • Deadlock Buster Arcade Game
      </div>
    </div>
    <a href="../track5-routing-deadlock/" class="noc-track-link">Explore Track 5 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 6 • Aligned with Chapter 6</span>
      <div class="noc-track-title">Low-Power Architectures &amp; Dark Silicon</div>
      <div class="noc-track-desc">
        Dark silicon physics, Thermal Design Power (TDP), multiple voltage/frequency domains (V/F islands), microarchitectural power gating, sleep state wakeups, and inductive $L\cdot di/dt$ emergencies.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Power Gating FSM RTL • Volt Vortex Simulator
      </div>
    </div>
    <a href="../track6-low-power-dark-silicon/" class="noc-track-link">Explore Track 6 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 7 • Aligned with Chapter 7</span>
      <div class="noc-track-title">Thermal Modeling &amp; Fault Tolerance</div>
      <div class="noc-track-desc">
        Fourier heat diffusion, compact RC ladder models, Regional Congestion Awareness (RCA), source quenching, proactive ML hotspot forecasting, and sparse sensor reconstruction.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Thermal Deflection RTL • Hotspot Hero &amp; Fault Defender
      </div>
    </div>
    <a href="../track7-thermal-fault-tolerance/" class="noc-track-link">Explore Track 7 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 8 • Aligned with Chapter 8</span>
      <div class="noc-track-title">3D Networks-on-Chip (3D-NoC) &amp; TSVs</div>
      <div class="noc-track-desc">
        Through-Silicon Vias (TSVs), Keep-Out Zones (KOZ), thermo-mechanical stress, 7-port 3D crossbars, vertical serialization, and 3D thermal stacking mitigation.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • 7-Port 3D Crossbar RTL • TSV Titan Simulator
      </div>
    </div>
    <a href="../track8-3d-noc-tsvs/" class="noc-track-link">Explore Track 8 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 9 • Aligned with Chapter 9</span>
      <div class="noc-track-title">Multi-Chiplet Interconnects &amp; UCIe</div>
      <div class="noc-track-desc">
        2.5D packaging economics, negative binomial yield, UCIe standard physical &amp; D2D adapter stacks, In/Outbound Swap deadlock recovery, and multi-chiplet bypassing.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • In/Outbound Swap RTL • Chiplet Tycoon Lab
      </div>
    </div>
    <a href="../track9-chiplets-ucie/" class="noc-track-link">Explore Track 9 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 10 • Aligned with Chapter 10</span>
      <div class="noc-track-title">Optical &amp; Wireless Networks-on-Chip</div>
      <div class="noc-track-desc">
        Silicon nanophotonic microring resonators (MRRs), wavelength-routed ONoCs (WRONoCs), laser power gating with APC loops, and on-chip mmWave/THz fabrics.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Photonic MRR Switch RTL • Photon Pilot &amp; Wireless Wave
      </div>
    </div>
    <a href="../track10-optical-wireless/" class="noc-track-link">Explore Track 10 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 11 • Aligned with Chapter 11</span>
      <div class="noc-track-title">Hardware Security &amp; Trust in NoCs</div>
      <div class="noc-track-desc">
        On-chip threat models: eavesdropping, spoofing, and DoS. Timing, buffer, and thermal covert channels. HeatSense zero-multiplier EWMA thermal Trojan detection and silicon quarantine.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • HeatSense EWMA Verilog • Silicon Sentinel Arcade
      </div>
    </div>
    <a href="../track11-security/" class="noc-track-link">Explore Track 11 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 12 • Aligned with Chapter 12</span>
      <div class="noc-track-title">Domain-Specific NoCs for AI &amp; LLMs</div>
      <div class="noc-track-desc">
        Large Language Models &amp; Collective Communication (AllReduce, AllGather). In-Network Reduction Routers, ultra-dense wafer-scale Ruche fabrics, and SNN multicasting.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • In-Network Reduction SystemVerilog • Transformer Titan Lab
      </div>
    </div>
    <a href="../track12-ai-llm-snn/" class="noc-track-link">Explore Track 12 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border-color: rgba(16, 185, 129, 0.3);">Track 13 • Capstone Synthesis</span>
      <div class="noc-track-title">Capstone: Landmark Systems &amp; MoE Synthesis</div>
      <div class="noc-track-desc">
        Walkthroughs of seminal chips (Intel SCC 48-Core, NVIDIA Simba 36-Chiplet, 3D Optical NoC, In-Network TVLSI) culminating in the Grand Capstone: Zero-Trust Multi-Chiplet MoE Accelerator.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 5 Lessons • Full SystemVerilog SoC RTL • Web EDA Auto-Grader Verification
      </div>
    </div>
    <a href="../track13-capstone/" class="noc-track-link">Explore Capstone Track 13 →</a>
  </div>

</div>

---

## 💻 Interactive Web EDA Unix Terminal

All 13 tracks are preloaded with SystemVerilog RTL modules and executable CLI simulation tools directly in your browser:

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
