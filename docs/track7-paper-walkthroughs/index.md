# Track 7: Landmark Paper Deep Dives

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 07</div>
  <h1>Landmark IEEE Paper Deep Dives &amp; Silicon Case Studies</h1>
  <p class="subtitle">
    Bridge theoretical NoC principles with real-world taped-out silicon from our curated archive of 541 IEEE journal papers. Strip away academic jargon to dissect the microarchitectures of milestone processors: from Intel's 48-Core Single-Chip Cloud Computer (SCC) with per-tile DVFS, to NVIDIA's 36-chiplet Simba MCM accelerator with Ground-Referenced Signaling (GRS), 3D Optical NoC with reduced-MRR crossbars, and in-network computing neuromorphic partial-sum routers.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ 4 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🔬 4 Interactive Simulators &amp; Tools</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">💻 4 Synthesizable Verilog RTL Modules</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">📜 4 Landmark IEEE / ACM Seminal Papers</span>
  </div>
</div>

<div class="noc-callout" style="background: rgba(15, 118, 110, 0.08); border-left: 4px solid #0f766e; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 8px 8px 0;">
  <div style="font-weight: 700; color: #0f766e; margin-bottom: 0.25rem;">📖 Official Companion Textbook Chapter Available</div>
  <div style="color: #334155; font-size: 0.95rem;">
    For comprehensive physical analysis of silicon nanophotonics, Crossing vs. Parallel Switching Elements (CSE vs. PSE), WDM laser link budgets, micro-ring resonator thermal drift, and 60 GHz / sub-THz on-chip wireless transceivers, read <strong><a href="https://github.com/network-on-chip/book/blob/main/chapters/ch10-optical-wireless/index.md" target="_blank" rel="noopener">Chapter 10: Optical &amp; Wireless Networks-on-Chip (ONoC / WNoC)</a></strong>.
  </div>
</div>

---

## 🗺️ Featured Landmark Paper Studies

The diagram below maps the historical evolution of interconnect architecture breakthroughs studied in this track:

```mermaid
graph TD
  subgraph Manycore ["1. The Manycore Milestone"]
    SCC["Intel 48-Core SCC (JSSC 2011)<br/>6x4 2D Mesh | 2-TB/s | Per-Tile DVFS | WWFA"]
  end

  subgraph Chiplet ["2. The Multi-Chiplet Revolution"]
    Simba["NVIDIA Simba (JSSC 2020)<br/>36-Chiplet MCM-NoC | GRS Links | Hardware Multicast"]
  end

  subgraph Stacking ["3. Stacking the 3rd Dimension"]
    ONoC3D["3D Optical NoC (TCAD 2013)<br/>Through-Silicon Vias + 26-MRR Crossbar + APC"]
  end

  subgraph InNetwork ["4. In-Network Computing"]
    Neuro["Neuromorphic P-Sum Router (JSSC 2023)<br/>1.63 pJ/SOP | In-Flight Arithmetic Reduction"]
  end

  SCC --> Simba
  SCC --> ONoC3D
  Simba --> Neuro
  ONoC3D --> Neuro

  classDef sccStyle fill:#e0f2fe,stroke:#0284c7,stroke-width:1.5px,color:#075985;
  classDef simbaStyle fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#92400e;
  classDef onocStyle fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#166534;
  classDef neuroStyle fill:#f3e8ff,stroke:#9333ea,stroke-width:1.5px,color:#581c87;

  class SCC sccStyle;
  class Simba simbaStyle;
  class ONoC3D onocStyle;
  class Neuro neuroStyle;
```

---

## 📚 Syllabus & Chapters in Track 7

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 7.1</span>
      <div class="noc-track-title">The Manycore Milestone: Intel 48-Core SCC</div>
      <div class="noc-track-desc">
        Intel Labs 45-nm tapeout, message-passing buffers (MPB), 2-TB/s 2D mesh, 4-stage router pipeline with lookahead routing and Wrapped Wave-Front Allocation (WWFA), and 24 independent tile clock domains.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive Intel SCC 48-Core Mesh Simulator, Synthesizable Verilog RTL (`scc_mesh_router_wwfa.v`), 3-Question Self-Check Quiz, Arcade Linkages (Arbiter Arena &amp; Volt Vortex).
      </div>
    </div>
    <a href="01-intel-scc-mesh.md" class="noc-track-link">Launch Lesson 7.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 7.2</span>
      <div class="noc-track-title">The Multi-Chiplet Revolution: NVIDIA Simba</div>
      <div class="noc-track-desc">
        36-chiplet 2.5D MCM deep learning accelerator, $0.54\text{ pJ/bit}$ Ground-Referenced Signaling (GRS) at $100\ \mu\text{m}$ pitch, 2-level hierarchical NoC, and hardware multicast tree routing.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive NVIDIA Simba Hierarchical MCM-NoC Explorer, Synthesizable Verilog RTL (`simba_multicast_router.v`), 3-Question Self-Check Quiz, Arcade Linkages (Chiplet Tycoon &amp; QoS Gladiator).
      </div>
    </div>
    <a href="02-nvidia-simba-mcm.md" class="noc-track-link">Launch Lesson 7.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 7.3</span>
      <div class="noc-track-title">Stacking the 3rd Dimension: 3D Optical NoC</div>
      <div class="noc-track-desc">
        Monolithic vertical integration uniting copper TSVs for control signaling with silicon waveguides for terabit data flight, 26-MRR passive crossbars under XYZ DOR, and Adaptive Power Control (APC) laser current modulation.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive 3D Optical NoC WDM &amp; Thermal Budget Analyzer, Synthesizable Verilog RTL (`onoc_hybrid_3d_crossbar.v`), 3-Question Self-Check Quiz, Arcade Linkages (Photon Pilot &amp; Hotspot Hero).
      </div>
    </div>
    <a href="03-3d-optical-noc.md" class="noc-track-link">Launch Lesson 7.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 7.4</span>
      <div class="noc-track-title">In-Network Computing: Neuromorphic Router</div>
      <div class="noc-track-desc">
        $1.63\text{ pJ/SOP}$ neuromorphic processor, dual-plane spike and partial-sum routing, in-flight arithmetic accumulation inside crossbar buffers, and Leaky Integrate-and-Fire (LIF) threshold evaluation.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive In-Flight Partial-Sum Reduction Visualizer, Synthesizable Verilog RTL (`neuromorphic_psum_router.v`), 3-Question Self-Check Quiz, Arcade Linkages (Neuromorphic Nexus &amp; Packet Master).
      </div>
    </div>
    <a href="04-in-network-neuromorphic.md" class="noc-track-link">Launch Lesson 7.4 →</a>
  </div>
</div>

---

## 🎯 Track Learning Objectives

Upon completing Track 7, you will be able to:

1. **Analyze Commercial Manycore Architecture:** Dissect the Intel SCC pipeline, explain lookahead routing and wave-front arbitration, and quantify why message passing avoids directory cache coherence scaling walls.
2. **Evaluate Multi-Chiplet MCM Networks:** Calculate shoreline bandwidth and energy efficiency for Ground-Referenced Signaling (GRS) and implement hardware multicast routing trees for deep learning tensor dissemination.
3. **Design Heterogeneous 3D Optical Interconnects:** Optimize optical crossbar layouts to slash active micro-ring counts using dimension-order routing invariants, and compute link power budgets with Adaptive Power Control (APC).
4. **Implement In-Network Computing Engines:** Build in-flight arithmetic reduction routers that merge convergent neural flits directly inside crossbar datapaths, cutting memory traffic by $>50\%$.
5. **Bridge Academic Theory with Taped-Out Silicon:** Connect published silicon measurements from IEEE JSSC, TCAD, and TVLSI directly to your own Verilog designs and architectural simulations.

---

## 🗺️ Live Papers Catalog & Exploration Tools

Want to explore the entire literature archive?
- 🌐 **[Launch Interactive NoC Papers Map](https://network-on-chip.github.io/.github/)**
- 📂 **[Browse Curated Papers Directory on GitHub](https://github.com/network-on-chip/noc-lab/tree/main/papers)**
