<div class="noc-hero">
  <div class="noc-track-badge">✨ Open-Source Curriculum & Research Lab</div>
  <h1>Network-on-Chip Learning Hub</h1>
  <p class="subtitle">
    An interactive, scholarly curriculum bridging theoretical computer architecture, silicon router microarchitecture, and open-source reproducible research. Grounded in 12 definitive textbook chapters, hands-on hardware simulations, and verified silicon research.
  </p>
  <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
    <a href="textbook/" class="noc-sim-btn" style="text-decoration: none; background: #2563eb;">📖 Read Official Textbook (12 Chaps)</a>
    <a href="tracks/" class="noc-sim-btn" style="text-decoration: none; background: #7c3aed;">📚 All 13 Curriculum Tracks</a>
    <a href="assets/book.pdf?v=266" target="_blank" class="noc-sim-btn" style="text-decoration: none; background: #0284c7;">📥 Download PDF (266 Pages)</a>
    <a href="interactive/terminal/" class="noc-sim-btn" style="text-decoration: none; background: #059669;">💻 Web EDA Terminal</a>
    <a href="track1-interconnect-crisis/" class="noc-sim-btn secondary" style="text-decoration: none;">🚀 Start Curriculum</a>
    <a href="quiz/" class="noc-sim-btn secondary" style="text-decoration: none;">🎯 Certification Quiz</a>
    <a href="interactive/game/" class="noc-sim-btn" style="text-decoration: none; background: #ea580c;">🔒 Deadlock Verifier</a>
    <a href="interactive/visualizer/" class="noc-sim-btn secondary" style="text-decoration: none;">🎮 2D Mesh Simulator</a>
    <a href="leaderboard/" class="noc-sim-btn secondary" style="text-decoration: none;">🏆 Leaderboard</a>
    <a href="glossary/" class="noc-sim-btn secondary" style="text-decoration: none;">📖 Glossary</a>
  </div>
</div>

<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">12</span>
    <span class="noc-stat-label">Core Textbook Chapters</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">266</span>
    <span class="noc-stat-label">Monograph Pages</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">13</span>
    <span class="noc-stat-label">Curriculum Tracks</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">53</span>
    <span class="noc-stat-label">Lessons &amp; RTL Cores</span>
  </div>
</div>

---

## 📖 Official Open Textbook (12 Chapters)

Explore the definitive 12-chapter textbook **"Network-on-Chip and Advanced Interconnects: Architecture, Co-Design & Emerging Frontiers"**, published under open access and designed to be accessible from engineering students to research architects.

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.35), rgba(15, 23, 42, 0.65)); border: 1px solid rgba(59, 130, 246, 0.5); border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #93c5fd; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;">
      <span>📘 Camera-Ready Monograph PDF Available</span>
    </div>
    <div style="font-size: 0.92rem; color: #e2e8f0; margin-top: 6px; max-width: 800px; line-height: 1.5;">
      Formatted in Springer Nature <code>svmono</code> layout (266 camera-ready pages). Covers Elmore RC wire delays, router pipelines, high-radix topologies, turn model deadlock freedom, dark silicon DVFS, HotSpot thermal models, 3D TSVs, UCIe chiplets, silicon nanophotonics, zero-trust hardware security, and AI/LLM collective accelerators.
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="textbook/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Read Online Hub →</span>
    </a>
    <a href="assets/book.pdf?v=266" target="_blank" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Download PDF (266 Pages) ↓</span>
    </a>
  </div>
</div>

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">Part I • Ch 1</span>
      <div class="noc-track-title">Interconnect Crisis &amp; Wire Physics</div>
      <div class="noc-track-desc">
        Why shared buses failed. Dennard scaling collapse, quantum tunneling, RC wire delays, Mayadas-Shatzkes scattering, and optimal repeater spacing.
      </div>
    </div>
    <a href="textbook/ch01-interconnect-crisis/" class="noc-track-link">Read Chapter 1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">Part I • Ch 2</span>
      <div class="noc-track-title">Switching, Flow Control &amp; Buffers</div>
      <div class="noc-track-desc">
        Wormhole vs VCT switching, flits/phits, credit turnaround latency loops ($RTT$), Virtual Channel buffers, and AXI4/TileLink NI packetization.
      </div>
    </div>
    <a href="textbook/ch02-switching-flow-control/" class="noc-track-link">Read Chapter 2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">Part I • Ch 3</span>
      <div class="noc-track-title">Router Microarchitecture &amp; Arbitration</div>
      <div class="noc-track-desc">
        Canonical 4-stage pipeline, speculative parallel VA/SA allocation, matrix &amp; wavefront arbiters (sub-200ps LRU), and SMART bypass routers.
      </div>
    </div>
    <a href="textbook/ch03-router-microarchitecture/" class="noc-track-link">Read Chapter 3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">Part II • Ch 4</span>
      <div class="noc-track-title">Direct, Indirect &amp; High-Radix Topologies</div>
      <div class="noc-track-desc">
        Graph metrics, 2D Mesh, Torus, Folded Torus, cMesh, Clos networks, Fat-Trees, Flattened Butterfly, and Dragonfly exascale topologies.
      </div>
    </div>
    <a href="textbook/ch04-topologies-and-metrics/" class="noc-track-link">Read Chapter 4 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">Part II • Ch 5</span>
      <div class="noc-track-title">Deadlock Theory, Turn Models &amp; Routing</div>
      <div class="noc-track-desc">
        Channel Dependency Graphs (CDG), Dally-Seitz theorem, Glass-Ni turn models, Chiu's Odd-Even, Duato's escape VCs, and coherence VNET isolation.
      </div>
    </div>
    <a href="textbook/ch05-routing-deadlock-theory/" class="noc-track-link">Read Chapter 5 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">Part III • Ch 6</span>
      <div class="noc-track-title">Low-Power Architectures &amp; Dark Silicon</div>
      <div class="noc-track-desc">
        Dynamic switching power, sub-threshold leakage, dark silicon budget ($>20\%$), Voltage-Frequency Islands (VFIs), and lookahead power gating.
      </div>
    </div>
    <a href="textbook/ch06-low-power-dark-silicon/" class="noc-track-link">Read Chapter 6 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">Part III • Ch 7</span>
      <div class="noc-track-title">Thermal Modeling &amp; Fault Tolerance</div>
      <div class="noc-track-desc">
        Fourier heat equation, compact RC ladders (HotSpot), thermal throttling, Gaussian-Sum Filter (GSF) sensor placement, and bypass fault detours.
      </div>
    </div>
    <a href="textbook/ch07-thermal-fault-tolerance/" class="noc-track-link">Read Chapter 7 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">Part IV • Ch 8</span>
      <div class="noc-track-title">Three-Dimensional NoC (3D-NoC) &amp; TSVs</div>
      <div class="noc-track-desc">
        Vertical TSVs, capacitive parasitics, Keep-Out Zones, 7-port 3D crossbars, arbitration-free vertical fast-paths, and vertical heat dissipation.
      </div>
    </div>
    <a href="textbook/ch08-3d-noc-tsvs/" class="noc-track-link">Read Chapter 8 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">Part IV • Ch 9</span>
      <div class="noc-track-title">Multi-Chiplet Interconnects &amp; UCIe</div>
      <div class="noc-track-desc">
        Optical reticle limit, Murphy yield economics (the Giant Pizza Problem), 2.5D interposers, the UCIe stack, and In/Outbound Swap deadlock recovery.
      </div>
    </div>
    <a href="textbook/ch09-chiplets-ucie/" class="noc-track-link">Read Chapter 9 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #ec4899; border-color: rgba(236, 72, 153, 0.2);">Part V • Ch 10</span>
      <div class="noc-track-title">Optical &amp; Wireless Networks-on-Chip</div>
      <div class="noc-track-desc">
        Silicon nanophotonics, micro-ring resonators (MRRs), PSE/CSE switching, thermo-optic drift ($0.10\text{ nm/}^\circ\text{C}$), and 60 GHz on-chip wireless RF transceivers.
      </div>
    </div>
    <a href="textbook/ch10-optical-wireless/" class="noc-track-link">Read Chapter 10 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(225, 29, 72, 0.1); color: #e11d48; border-color: rgba(225, 29, 72, 0.2);">Part V • Ch 11</span>
      <div class="noc-track-title">Hardware Security &amp; Trust in NoCs</div>
      <div class="noc-track-desc">
        Zero-trust interconnect security, thermal Hardware Trojans, Weighted Moving Average (WMA) anomaly detection, intrinsic delay PUFs, and timing covert channel jitter masking.
      </div>
    </div>
    <a href="textbook/ch11-security/" class="noc-track-link">Read Chapter 11 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(2, 132, 199, 0.1); color: #0284c7; border-color: rgba(2, 132, 199, 0.2);">Part V • Ch 12</span>
      <div class="noc-track-title">Domain-Specific NoCs for LLMs &amp; SNNs</div>
      <div class="noc-track-desc">
        Generative AI communication collectives, in-network reduction crossbars, wafer-scale defect bypass, 2,048-core Ruche express links, 3D hybrid bonding memory silos, and SNN spike multicasting.
      </div>
    </div>
    <a href="textbook/ch12-ai-llm-snn/" class="noc-track-link">Read Chapter 12 →</a>
  </div>
</div>

---

## 📚 Curriculum Tracks

Explore our structured learning pathways designed for undergraduate and graduate students, computer architects, and hardware designers.

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 1</span>
      <div class="noc-track-title">Interconnect Crisis &amp; Wire Physics</div>
      <div class="noc-track-desc">
        Why shared buses failed. Wire scaling, Elmore RC delay modeling, optimal repeater insertion, and fundamental limits of on-chip energy and latency.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Synthesizable Elmore Verilog • Interactive Wire Simulator
      </div>
    </div>
    <a href="track1-interconnect-crisis/" class="noc-track-link">Explore Track 1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 2</span>
      <div class="noc-track-title">Switching, Flow Control &amp; Buffers</div>
      <div class="noc-track-desc">
        Packets, flits, and phits. Store-and-Forward vs Virtual Cut-Through vs Wormhole switching, credit turnaround latency loops, and Network Interface (NI) AXI packetization.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Credit Counter RTL • Credit-Based Flow Control & Buffer Sizing CAD
      </div>
    </div>
    <a href="track2-switching-flow-control/" class="noc-track-link">Explore Track 2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 3</span>
      <div class="noc-track-title">Router Microarchitecture &amp; Arbitration</div>
      <div class="noc-track-desc">
        Canonical 5-stage router pipelines (BW-RC-VA-SA-ST), Virtual Channel allocation, sub-200ps LRU matrix arbiters, and SMART single-cycle multi-hop bypass routers.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • 5-Stage SystemVerilog Router • Crossbar Switch Allocator & Arbiter Simulator
      </div>
    </div>
    <a href="track3-router-microarchitecture/" class="noc-track-link">Explore Track 3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 4</span>
      <div class="noc-track-title">Direct, Indirect &amp; High-Radix Topologies</div>
      <div class="noc-track-desc">
        Direct (Mesh, Torus, Folded Torus), Indirect (Clos, Fat-Tree, cMesh), and High-Radix (Dragonfly, Flattened Butterfly). Mathematical derivations of $T_0$, $\Theta_{sat}$, and UGAL routing.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Topology Graph Metrics RTL • Interactive Topology Architect
      </div>
    </div>
    <a href="track4-topologies-and-metrics/" class="noc-track-link">Explore Track 4 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 5</span>
      <div class="noc-track-title">Deadlock Theory, Turn Models &amp; Routing</div>
      <div class="noc-track-desc">
        Deterministic Dimension-Order Routing (DOR), Glass &amp; Ni's Turn Model, Chiu's Odd-Even algorithm, Duato's Escape Channels, CDG acyclic proofs, and VNET isolation.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • SMT CDG Verifier • Deadlock Verification & CDG Escape Engine
      </div>
    </div>
    <a href="track5-routing-deadlock/" class="noc-track-link">Explore Track 5 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 6</span>
      <div class="noc-track-title">Low-Power Architectures &amp; Dark Silicon</div>
      <div class="noc-track-desc">
        Dark silicon physics, Thermal Design Power (TDP), multiple V/F islands, microarchitectural power gating, sleep state wakeups, and inductive $L\cdot di/dt$ emergencies.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Power Gating FSM RTL • Dark Silicon Physics & Power Gating CAD
      </div>
    </div>
    <a href="track6-low-power-dark-silicon/" class="noc-track-link">Explore Track 6 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 7</span>
      <div class="noc-track-title">Thermal Modeling &amp; Fault Tolerance</div>
      <div class="noc-track-desc">
        Fourier heat diffusion, compact RC ladder models, Regional Congestion Awareness (RCA), source quenching, proactive ML hotspot forecasting, and sparse sensor reconstruction.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Thermal Deflection RTL • Silicon Thermal & Resilient Fault Routing CAD
      </div>
    </div>
    <a href="track7-thermal-fault-tolerance/" class="noc-track-link">Explore Track 7 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 8</span>
      <div class="noc-track-title">3D Networks-on-Chip (3D-NoC) &amp; TSVs</div>
      <div class="noc-track-desc">
        Through-Silicon Vias (TSVs), Keep-Out Zones (KOZ), thermo-mechanical stress, 7-port 3D crossbars, vertical serialization, and 3D thermal stacking mitigation.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • 7-Port 3D Crossbar RTL • TSV Titan Simulator
      </div>
    </div>
    <a href="track8-3d-noc-tsvs/" class="noc-track-link">Explore Track 8 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 9</span>
      <div class="noc-track-title">Multi-Chiplet Interconnects &amp; UCIe</div>
      <div class="noc-track-desc">
        2.5D packaging economics, negative binomial yield, UCIe standard physical &amp; D2D adapter stacks, In/Outbound Swap deadlock recovery, and multi-chiplet bypassing.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • In/Outbound Swap RTL • 2.5D/3D Multi-Die Chiplet CAD
      </div>
    </div>
    <a href="track9-chiplets-ucie/" class="noc-track-link">Explore Track 9 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 10</span>
      <div class="noc-track-title">Optical &amp; Wireless Networks-on-Chip</div>
      <div class="noc-track-desc">
        Silicon nanophotonic microring resonators (MRRs), wavelength-routed ONoCs (WRONoCs), laser power gating with APC loops, and on-chip mmWave/THz fabrics.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Photonic MRR Switch RTL • Optical NoC CAD &amp; On-Chip Wireless NoC Simulator
      </div>
    </div>
    <a href="track10-optical-wireless/" class="noc-track-link">Explore Track 10 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 11</span>
      <div class="noc-track-title">Hardware Security &amp; Trust in NoCs</div>
      <div class="noc-track-desc">
        On-chip threat models: eavesdropping, spoofing, and DoS. Timing, buffer, and thermal covert channels. HeatSense zero-multiplier EWMA thermal Trojan detection.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • HeatSense EWMA Verilog • NoC Hardware Security CAD
      </div>
    </div>
    <a href="track11-security/" class="noc-track-link">Explore Track 11 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 12</span>
      <div class="noc-track-title">Domain-Specific NoCs for AI &amp; LLMs</div>
      <div class="noc-track-desc">
        Large Language Models &amp; Collective Communication (AllReduce, AllGather). In-Network Reduction Routers, ultra-dense wafer-scale Ruche fabrics, and SNN multicasting.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • In-Network Reduction SystemVerilog • Distributed LLM Collective Accelerator Simulator Lab
      </div>
    </div>
    <a href="track12-ai-llm-snn/" class="noc-track-link">Explore Track 12 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border-color: rgba(16, 185, 129, 0.3);">Track 13 • Capstone</span>
      <div class="noc-track-title">Capstone: Landmark Systems &amp; MoE Synthesis</div>
      <div class="noc-track-desc">
        Walkthroughs of seminal chips (Intel SCC 48-Core, NVIDIA Simba 36-Chiplet, 3D Optical NoC, In-Network TVLSI) culminating in the Grand Capstone: Zero-Trust Multi-Chiplet MoE Accelerator.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 5 Lessons • Full SystemVerilog SoC RTL • Web EDA Auto-Grader Verification
      </div>
    </div>
    <a href="track13-capstone/" class="noc-track-link">Explore Capstone Track 13 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(234, 88, 12, 0.1); color:#ea580c; border-color:rgba(234, 88, 12, 0.2);">Deadlock Verification</span>
      <div class="noc-track-title">Deadlock Verification &amp; CDG Escape Engine</div>
      <div class="noc-track-desc">
        Construct Channel Dependency Graphs (CDG) and compute Tarjan Strongly Connected Components (SCC) to detect circular wait deadlocks and verify Duato escape channels.
      </div>
    </div>
    <a href="interactive/game/" class="noc-track-link">Launch Deadlock Engine →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(139, 92, 246, 0.1); color:#8b5cf6; border-color:rgba(139, 92, 246, 0.2);">Turn-Model Optimizer</span>
      <div class="noc-track-title">Turn-Model Routing Restrictions &amp; Path Optimizer</div>
      <div class="noc-track-desc">
        Explore Glass &amp; Ni turn models (West-First, North-Last, Negative-First) and Chiu Odd-Even column-parity restrictions. Evaluate legal routing cones and defect detours.
      </div>
    </div>
    <a href="interactive/puzzle/" class="noc-track-link">Launch Turn-Model Optimizer →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(239, 68, 68, 0.1); color:#ef4444; border-color:rgba(239, 68, 68, 0.2);">Thermal Physics</span>
      <div class="noc-track-title">Silicon Thermal &amp; DTM Finite-Difference Solver</div>
      <div class="noc-track-desc">
        Model 2D transient Fourier heat diffusion coupled with exponential leakage runaway. Deploy closed-loop PI-DVFS and TAAR thermal-aware routing.
      </div>
    </div>
    <a href="interactive/hotspot/" class="noc-track-link">Launch Thermal Solver →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(16, 185, 129, 0.1); color:#10b981; border-color:rgba(16, 185, 129, 0.2);">Packaging Architecture</span>
      <div class="noc-track-title">2.5D/3D Multi-Die Chiplet CAD &amp; Yield Optimizer</div>
      <div class="noc-track-desc">
        Model Murphy defect wafer yield, evaluate UCIe D2D physical latency and shoreline bandwidth density, and solve multi-die thermal coupling.
      </div>
    </div>
    <a href="interactive/chiplet/" class="noc-track-link">Launch Chiplet Optimizer →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(234, 88, 12, 0.1); color:#ea580c; border-color:rgba(234, 88, 12, 0.2);">Microarchitecture</span>
      <div class="noc-track-title">Switch Allocation &amp; Crossbar Arbiter Simulator</div>
      <div class="noc-track-desc">
        Arbitrate competing packet requests across 5x5 crossbar switches. Compare Strict Priority, Round-Robin, Matrix Arbiter, and McKeown iSLIP scheduling.
      </div>
    </div>
    <a href="interactive/arbiter/" class="noc-track-link">Launch Arbiter Simulator →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(59, 130, 246, 0.1); color:#3b82f6; border-color:rgba(59, 130, 246, 0.2);">Graph Theory</span>
      <div class="noc-track-title">Interconnect Topology CAD &amp; Spectral Graph Analyzer</div>
      <div class="noc-track-desc">
        Compute Graph Laplacian eigenvalues, evaluate algebraic connectivity (Fiedler lambda_2), bisection bandwidth, and diameter across 2D Torus, Hypercubes, and Dragonfly.
      </div>
    </div>
    <a href="interactive/topology/" class="noc-track-link">Launch Topology CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(236, 72, 153, 0.1); color:#ec4899; border-color:rgba(236, 72, 153, 0.2);">Nanophotonics</span>
      <div class="noc-track-title">Silicon Photonic &amp; Optical NoC (ONoC) Waveguide CAD</div>
      <div class="noc-track-desc">
        Model Lorentzian micro-ring resonator spectra, thermo-optic wavelength drift, micro-heater closed-loop tuning, optical insertion loss waterfall, and link BER.
      </div>
    </div>
    <a href="interactive/optical/" class="noc-track-link">Launch Optical CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(16, 185, 129, 0.1); color:#10b981; border-color:rgba(16, 185, 129, 0.2);">Flow Control</span>
      <div class="noc-track-title">Credit-Based Flow Control &amp; Buffer Sizing CAD</div>
      <div class="noc-track-desc">
        Simulate credit loop round-trip latency (B_min = ceil(RTT * BW)), space-time timing ladder progression, and credit bubble elimination.
      </div>
    </div>
    <a href="interactive/credits/" class="noc-track-link">Launch Credit CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(234, 179, 8, 0.1); color:#ca8a04; border-color:rgba(234, 179, 8, 0.2);">Bufferless Blitz</span>
      <div class="noc-track-title">Bufferless Deflection Simulator NoC</div>
      <div class="noc-track-desc">
        Eliminate input buffers entirely! Steer hot-potato flits, arbitrate deflection conflicts, unleash Golden Flit surges, and avoid livelock drops.
      </div>
    </div>
    <a href="interactive/deflection/" class="noc-track-link">Launch Deflection Simulator →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(99, 102, 241, 0.1); color:#6366f1; border-color:rgba(99, 102, 241, 0.2);">Silicon Resilience</span>
      <div class="noc-track-title">Silicon Fault Tolerance CAD BIST</div>
      <div class="noc-track-desc">
        Combat electromigration and cosmic ray strikes! Fire BIST radar pulses, establish Fault-Ring perimeter detours, and activate hot-spare interconnects.
      </div>
    </div>
    <a href="interactive/faults/" class="noc-track-link">Play Silicon Fault Tolerance CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(239, 68, 68, 0.1); color:#ef4444; border-color:rgba(239, 68, 68, 0.2);">Real-Time QoS</span>
      <div class="noc-track-title">Multi-VNET QoS Scheduler MCS</div>
      <div class="noc-track-desc">
        Arbiter autonomous safety flits against bulk AI DMA transfers! Tune Weighted Fair Queuing (WFQ) and fire emergency preemption interrupts before deadlines expire.
      </div>
    </div>
    <a href="interactive/qos/" class="noc-track-link">Play Multi-VNET QoS Scheduler →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(2, 132, 199, 0.1); color:#0284c7; border-color:rgba(2, 132, 199, 0.2);">Dark Silicon</span>
      <div class="noc-track-title">Dark Silicon Power Gating CAD Power</div>
      <div class="noc-track-desc">
        Power-gate idle router corridors to slash leakage! Navigate wake-up penalties, fire rail power surges, and prevent exceeding thermal design power (TDP) envelopes.
      </div>
    </div>
    <a href="interactive/power/" class="noc-track-link">Play Dark Silicon Power Gating CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(14, 165, 233, 0.1); color:#0284c7; border-color:rgba(14, 165, 233, 0.2);">Wireless NoC</span>
      <div class="noc-track-title">On-Chip Wireless NoC Simulator WNoC</div>
      <div class="noc-track-desc">
        Beam packets across silicon in 1 single cycle! Transmit on 60 GHz mmWave patch antennas, navigate FDMA channels, and avoid multi-access RF collisions.
      </div>
    </div>
    <a href="interactive/wireless/" class="noc-track-link">Play On-Chip Wireless NoC Simulator →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(168, 85, 247, 0.1); color:#a855f7; border-color:rgba(168, 85, 247, 0.2);">Neuromorphic SNN</span>
      <div class="noc-track-title">Neuromorphic SNN Multicast Simulator</div>
      <div class="noc-track-desc">
        Orchestrate event-driven bio-spikes (AER)! Build 1-to-N hardware multicast trees, integrate Leaky-Integrate-and-Fire membrane potentials, and trigger STDP surges.
      </div>
    </div>
    <a href="interactive/neuromorphic/" class="noc-track-link">Play Neuromorphic SNN Multicast Simulator →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(14, 165, 233, 0.1); color:#0284c7; border-color:rgba(14, 165, 233, 0.2);">Certification</span>
      <div class="noc-track-title">Architecture Assessment &amp; Quiz</div>
      <div class="noc-track-desc">
        Evaluate your knowledge across routing, microarchitecture, and deadlock theory. Download your official cryptographic SVG Certificate of Completion.
      </div>
    </div>
    <a href="quiz/" class="noc-track-link">Take Certification Quiz →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Hall of Fame</span>
      <div class="noc-track-title">Leaderboard &amp; Verification</div>
      <div class="noc-track-desc">
        Recognizing top scores from researchers and students globally. Features an instant cryptographic credential verification tool.
      </div>
    </div>
    <a href="leaderboard/" class="noc-track-link">View Leaderboard →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Encyclopedia</span>
      <div class="noc-track-title">Architecture Glossary</div>
      <div class="noc-track-desc">
        Instant searchable dictionary of 50+ NoC terms, from Flits and Wormhole Switching to Matrix Arbiters, TSVs, and UCIe interfaces.
      </div>
    </div>
    <a href="glossary/" class="noc-track-link">Browse Glossary →</a>
  </div>
</div>

---

## 🔬 Bridging Theory, Silicon, and Code

Every concept in this curriculum is paired with concrete, reproducible artifacts from our verified research suite:

```mermaid
graph LR
  A["Interconnect Theory<br/>& Architecture"] --> B["Curriculum Tracks<br/>(All 13 Tracks)"]
  B --> C["Interactive Browser Lab<br/>(Canvas Routing Simulator)"]
  B --> D["Hardware Implementations<br/>(projects/ in Verilog & Python)"]
  D --> E["Benchmarking & Silicon Data<br/>(Thermal, Latency, Energy)"]
```

### Ready to Start?
Explore [All 13 Curriculum Tracks](tracks/index.md), dive directly into [Track 1: Interconnect Crisis & Wire Physics](track1-interconnect-crisis/index.md), or launch the [Web EDA Unix Terminal](interactive/terminal.md)!
