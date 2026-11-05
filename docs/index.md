<div class="noc-hero">
  <div class="noc-track-badge">✨ Open-Source Curriculum & Research Lab</div>
  <h1>Network-on-Chip Learning Hub</h1>
  <p class="subtitle">
    An interactive, scholarly curriculum bridging theoretical computer architecture, silicon router microarchitecture, and open-source reproducible research. Grounded in 542 curated IEEE/ACM papers, 10 definitive textbook chapters, and verified hardware simulations.
  </p>
  <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
    <a href="textbook/" class="noc-sim-btn" style="text-decoration: none; background: #2563eb;">📖 Read Official Textbook (10 Chaps)</a>
    <a href="assets/book.pdf" target="_blank" class="noc-sim-btn" style="text-decoration: none; background: #0284c7;">📥 Download PDF (132 Pages)</a>
    <a href="track1-fundamentals/" class="noc-sim-btn secondary" style="text-decoration: none;">🚀 Start Curriculum</a>
    <a href="quiz/" class="noc-sim-btn secondary" style="text-decoration: none;">🎯 Certification Quiz</a>
    <a href="interactive/game/" class="noc-sim-btn" style="text-decoration: none; background: #ea580c;">👾 Deadlock Buster</a>
    <a href="interactive/visualizer/" class="noc-sim-btn secondary" style="text-decoration: none;">🎮 2D Mesh Simulator</a>
    <a href="leaderboard/" class="noc-sim-btn secondary" style="text-decoration: none;">🏆 Leaderboard</a>
    <a href="glossary/" class="noc-sim-btn secondary" style="text-decoration: none;">📖 Glossary</a>
  </div>
</div>

<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">10</span>
    <span class="noc-stat-label">Core Textbook Chapters</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">542+</span>
    <span class="noc-stat-label">Curated IEEE Papers</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">15</span>
    <span class="noc-stat-label">Interactive Labs & Games</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">100%</span>
    <span class="noc-stat-label">Open & Reproducible</span>
  </div>
</div>

---

## 📖 Official Open Textbook (10 Chapters)

Explore the definitive 10-chapter textbook **"Network-on-Chip and Advanced Interconnects: Architecture, Co-Design & Emerging Frontiers"**, published under open access and designed to be accessible from high school students to research architects.

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.35), rgba(15, 23, 42, 0.65)); border: 1px solid rgba(59, 130, 246, 0.5); border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #93c5fd; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;">
      <span>📘 Camera-Ready Monograph PDF Available</span>
    </div>
    <div style="font-size: 0.92rem; color: #e2e8f0; margin-top: 6px; max-width: 800px; line-height: 1.5;">
      Formatted in Springer Nature <code>svmono</code> layout (132 pages). Covers Elmore RC wire delays, router pipelines, high-radix topologies, turn model deadlock freedom, dark silicon DVFS, HotSpot thermal models, 3D TSVs, UCIe chiplets, and silicon nanophotonics.
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="textbook/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Read Online Hub →</span>
    </a>
    <a href="assets/book.pdf" target="_blank" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Download PDF (132 Pages) ↓</span>
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
</div>

---

## 📚 Curriculum Tracks

Explore our structured learning pathways designed for undergraduate and graduate students, computer architects, and hardware designers.

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 1</span>
      <div class="noc-track-title">Interconnect Fundamentals</div>
      <div class="noc-track-desc">
        Why shared buses failed. Packets, flits, and phits. Store-and-Forward vs Virtual Cut-Through vs Wormhole switching, credit turnaround latency loops, and Network Interface (NI) AXI packetization.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Interactive Simulators &amp; Calculators
      </div>
    </div>
    <a href="track1-fundamentals/" class="noc-track-link">Explore Track 1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 2</span>
      <div class="noc-track-title">Router Microarchitecture</div>
      <div class="noc-track-desc">
        Canonical 5-stage router pipelines (BW-RC-VA-SA-ST), Virtual Channel allocation, sub-200ps LRU matrix arbiters, and SMART single-cycle multi-hop bypass routers.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Interactive Simulators &amp; Verilog RTL
      </div>
    </div>
    <a href="track2-router-architecture/" class="noc-track-link">Explore Track 2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 3</span>
      <div class="noc-track-title">Topologies &amp; Interconnect Metrics</div>
      <div class="noc-track-desc">
        Direct (Mesh, Torus, Folded Torus), Indirect (Clos, Fat-Tree, cMesh), and High-Radix (Dragonfly, Flattened Butterfly). Mathematical derivations of $T_0$, $\Theta_{sat}$, bisection bandwidth, and UGAL adaptive routing.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; High-Radix Analyzer
      </div>
    </div>
    <a href="track3-topologies/" class="noc-track-link">Explore Track 3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 4</span>
      <div class="noc-track-title">Routing &amp; Deadlock Avoidance</div>
      <div class="noc-track-desc">
        Deterministic Dimension-Order Routing (DOR), Glass &amp; Ni's Turn Model, Chiu's Odd-Even algorithm, Duato's Escape Channels, Up*/Down* tree routing, and Cache Coherence VNET isolation.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; Arcade Links
      </div>
    </div>
    <a href="track4-routing-deadlock/" class="noc-track-link">Explore Track 4 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 5</span>
      <div class="noc-track-title">Thermal &amp; Congestion Management</div>
      <div class="noc-track-desc">
        Fourier heat diffusion, compact RC ladder models, Regional Congestion Awareness (RCA), source quenching, proactive ML hotspot forecasting, and sparse sensor reconstruction under non-Gaussian noise.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; Arcade Links
      </div>
    </div>
    <a href="track5-congestion-thermal/" class="noc-track-link">Explore Track 5 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 6</span>
      <div class="noc-track-title">Chiplets, 3D NoC &amp; Frontiers</div>
      <div class="noc-track-desc">
        Through-Silicon Vias (TSVs), 7-port 3D routers, negative binomial yield economics, 2.5D packaging (CoWoS, EMIB), the UCIe standard stack, 3D thermal stacking, Optical NoC (ONoC), and Wireless NoC (WNoC).
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; Arcade Links
      </div>
    </div>
    <a href="track6-chiplets-and-3d/" class="noc-track-link">Explore Track 6 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 7</span>
      <div class="noc-track-title">Landmark Paper Deep Dives</div>
      <div class="noc-track-desc">
        Undergraduate-readable walkthroughs of seminal IEEE JSSC, TCAD, and TVLSI papers: Intel 48-Core SCC (2-TB/s DVFS Mesh), NVIDIA Simba (36-chiplet GRS MCM), 3D Optical NoC (TSVs + Micro-Rings), and In-Network Computing neuromorphic routers.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; Arcade Links
      </div>
    </div>
    <a href="track7-paper-walkthroughs/" class="noc-track-link">Explore Track 7 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(234, 88, 12, 0.1); color:#ea580c; border-color:rgba(234, 88, 12, 0.2);">Arcade Game</span>
      <div class="noc-track-title">Deadlock Buster Challenge</div>
      <div class="noc-track-desc">
        Act as the router arbiter under heavy traffic bursts. Flush escape channels using Duato's Theorem and prevent buffer lockups before time expires!
      </div>
    </div>
    <a href="interactive/game/" class="noc-track-link">Play Deadlock Buster →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(139, 92, 246, 0.1); color:#8b5cf6; border-color:rgba(139, 92, 246, 0.2);">Architect Puzzle</span>
      <div class="noc-track-title">Packet Master Puzzle</div>
      <div class="noc-track-desc">
        Configure turning preferences, resolve crossbar collisions, and route around faulty cores to solve 5 increasingly difficult routing puzzle levels!
      </div>
    </div>
    <a href="interactive/puzzle/" class="noc-track-link">Play Packet Master →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(239, 68, 68, 0.1); color:#ef4444; border-color:rgba(239, 68, 68, 0.2);">Thermal Defense</span>
      <div class="noc-track-title">Hotspot Hero Arcade</div>
      <div class="noc-track-desc">
        Control Dynamic Voltage &amp; Frequency Scaling (DVFS), migrate boiling workloads, and deploy microfluidic cryo pulses to prevent thermal runaway meltdown!
      </div>
    </div>
    <a href="interactive/hotspot/" class="noc-track-link">Play Hotspot Hero →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(16, 185, 129, 0.1); color:#10b981; border-color:rgba(16, 185, 129, 0.2);">Packaging Tycoon</span>
      <div class="noc-track-title">Chiplet Tycoon Architect</div>
      <div class="noc-track-desc">
        Construct modular multi-die Superchips on silicon interposers with UCIe and 3D TSVs. Balance bisection bandwidth, latency, yield economics, and packaging costs!
      </div>
    </div>
    <a href="interactive/chiplet/" class="noc-track-link">Play Chiplet Tycoon →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(234, 88, 12, 0.1); color:#ea580c; border-color:rgba(234, 88, 12, 0.2);">Microarchitecture Clash</span>
      <div class="noc-track-title">Arbiter Arena Clash</div>
      <div class="noc-track-desc">
        Arbitrate a 5×5 crossbar switch in real time! Bypass Head-of-Line (HOL) blocking using Virtual Channels and deploy iSLIP scheduling before FIFOs overflow.
      </div>
    </div>
    <a href="interactive/arbiter/" class="noc-track-link">Play Arbiter Arena →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(59, 130, 246, 0.1); color:#3b82f6; border-color:rgba(59, 130, 246, 0.2);">Graph Architect</span>
      <div class="noc-track-title">Topology Titans Exascale</div>
      <div class="noc-track-desc">
        Wire exascale supercomputing topologies (Hypercube, Torus, Dragonfly, Fat-Tree). Minimize diameter and hop latency under physical radix and wire cost budgets!
      </div>
    </div>
    <a href="interactive/topology/" class="noc-track-link">Play Topology Titans →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(236, 72, 153, 0.1); color:#ec4899; border-color:rgba(236, 72, 153, 0.2);">Silicon Photonics</span>
      <div class="noc-track-title">Photon Pilot Optical Grid</div>
      <div class="noc-track-desc">
        Steer multi-wavelength laser beams ($\lambda_1 \dots \lambda_4$) through silicon waveguides! Tune micro-ring resonators, manage WDM, and counter thermal drift.
      </div>
    </div>
    <a href="interactive/optical/" class="noc-track-link">Play Photon Pilot →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(16, 185, 129, 0.1); color:#10b981; border-color:rgba(16, 185, 129, 0.2);">Flow Control Defense</span>
      <div class="noc-track-title">Credit Commander Link</div>
      <div class="noc-track-desc">
        Govern link-level flow control across flight delays ($RTT=5$ cycles)! Track credit counters, batch credit returns, and defend against buffer overflow.
      </div>
    </div>
    <a href="interactive/credits/" class="noc-track-link">Play Credit Commander →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(234, 179, 8, 0.1); color:#ca8a04; border-color:rgba(234, 179, 8, 0.2);">Bufferless Blitz</span>
      <div class="noc-track-title">Deflection Duel NoC</div>
      <div class="noc-track-desc">
        Eliminate input buffers entirely! Steer hot-potato flits, arbitrate deflection conflicts, unleash Golden Flit surges, and avoid livelock drops.
      </div>
    </div>
    <a href="interactive/deflection/" class="noc-track-link">Play Deflection Duel →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(99, 102, 241, 0.1); color:#6366f1; border-color:rgba(99, 102, 241, 0.2);">Silicon Resilience</span>
      <div class="noc-track-title">Fault Defender BIST</div>
      <div class="noc-track-desc">
        Combat electromigration and cosmic ray strikes! Fire BIST radar pulses, establish Fault-Ring perimeter detours, and activate hot-spare interconnects.
      </div>
    </div>
    <a href="interactive/faults/" class="noc-track-link">Play Fault Defender →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(239, 68, 68, 0.1); color:#ef4444; border-color:rgba(239, 68, 68, 0.2);">Real-Time QoS</span>
      <div class="noc-track-title">QoS Gladiator MCS</div>
      <div class="noc-track-desc">
        Arbiter autonomous safety flits against bulk AI DMA transfers! Tune Weighted Fair Queuing (WFQ) and fire emergency preemption interrupts before deadlines expire.
      </div>
    </div>
    <a href="interactive/qos/" class="noc-track-link">Play QoS Gladiator →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(2, 132, 199, 0.1); color:#0284c7; border-color:rgba(2, 132, 199, 0.2);">Dark Silicon</span>
      <div class="noc-track-title">Volt Vortex Power</div>
      <div class="noc-track-desc">
        Power-gate idle router corridors to slash leakage! Navigate wake-up penalties, fire rail power surges, and prevent exceeding thermal design power (TDP) envelopes.
      </div>
    </div>
    <a href="interactive/power/" class="noc-track-link">Play Volt Vortex →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(14, 165, 233, 0.1); color:#0284c7; border-color:rgba(14, 165, 233, 0.2);">Wireless NoC</span>
      <div class="noc-track-title">Wireless Wave WNoC</div>
      <div class="noc-track-desc">
        Beam packets across silicon in 1 single cycle! Transmit on 60 GHz mmWave patch antennas, navigate FDMA channels, and avoid multi-access RF collisions.
      </div>
    </div>
    <a href="interactive/wireless/" class="noc-track-link">Play Wireless Wave →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(168, 85, 247, 0.1); color:#a855f7; border-color:rgba(168, 85, 247, 0.2);">Neuromorphic SNN</span>
      <div class="noc-track-title">Neuromorphic Nexus</div>
      <div class="noc-track-desc">
        Orchestrate event-driven bio-spikes (AER)! Build 1-to-N hardware multicast trees, integrate Leaky-Integrate-and-Fire membrane potentials, and trigger STDP surges.
      </div>
    </div>
    <a href="interactive/neuromorphic/" class="noc-track-link">Play Neuromorphic Nexus →</a>
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
  A["Theory & Literature<br/>(541 IEEE Papers)"] --> B["Curriculum Modules<br/>(Tracks 1–7)"]
  B --> C["Interactive Browser Lab<br/>(Canvas Routing Simulator)"]
  B --> D["Hardware Implementations<br/>(projects/ in Verilog & Python)"]
  D --> E["Benchmarking & Silicon Data<br/>(Thermal, Latency, Energy)"]
```

### Ready to Start?
Begin your journey with [Track 1: Interconnect Fundamentals](track1-fundamentals/index.md) or try out the [Interactive Simulator](interactive/visualizer.md)!
