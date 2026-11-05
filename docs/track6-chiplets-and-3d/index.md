# Track 6: Chiplets, 3D NoC & Emerging Frontiers

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 06</div>
  <h1>Chiplets, 3D Integration &amp; Emerging Physical Frontiers</h1>
  <p class="subtitle">
    Master the microarchitecture and physics of spatial interconnects beyond monolithic 2D copper. From Through-Silicon Vias (TSVs) and Keep-Out Zone (KOZ) piezoresistive stress modeling to 2.5D Multi-Die packaging, the Universal Chiplet Interconnect Express (UCIe) protocol stack, 3D thermal stacking &amp; deadlock-free XYZ dimension-order routing, to nanophotonic silicon waveguides and millimeter-wave wireless shortcuts.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ 4 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🔬 4 Interactive Simulators &amp; Tools</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">💻 4 Synthesizable Verilog RTL Modules</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">📦 UCIe 1.0/2.0 &amp; TSV Standards</span>
</div>

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>📚 Aligned with Official Textbook Chapters 8, 9 &amp; 10</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Read <strong>Chapter 8 (3D-NoC &amp; TSVs)</strong> for vertical parasitics, 7-port crossbars, and thermal trapping. Read <strong>Chapter 9 (Chiplets &amp; UCIe)</strong> for Murphy yield economics, 2.5D interposers, and In/Outbound swap deadlock recovery. Read <strong>Chapter 10 (Optical &amp; Wireless NoC)</strong> for silicon photonics, MRRs, and 60 GHz wireless transceivers.
    </div>
  </div>
  <div style="display: flex; gap: 8px; flex-wrap: wrap;">
    <a href="../textbook/ch08-3d-noc-tsvs/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 14px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
      <span>Read Chapter 8 →</span>
    </a>
    <a href="../textbook/ch09-chiplets-ucie/" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 8px 14px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
      <span>Read Chapter 9 →</span>
    </a>
    <a href="../textbook/ch10-optical-wireless/" style="display: inline-flex; align-items: center; gap: 6px; background: #ec4899; color: #ffffff; padding: 8px 14px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
      <span>Read Chapter 10 →</span>
    </a>
  </div>
</div>

---

## 🗺️ 3D & Chiplet Architecture Roadmap

The roadmap below visualizes how physical scaling limits in monolithic silicon drive 3D vertical integration, 2.5D modular chiplet standards, and emerging optical and wireless transmission media:

```mermaid
graph TD
  subgraph Moore ["1. Monolithic Scaling Bottlenecks"]
    A["Reticle Limit (858 mm²)<br/>Defect Density & Yield Collapse"]
    B["RC Copper Delay Wall<br/>Capacitive Charging & Attenuation Limits"]
  end

  subgraph Stacking ["2. 3D Integration & Vertical TSVs"]
    C["Through-Silicon Vias (TSVs)<br/>Sub-10 ps Vertical Latency"]
    D["7-Port 3D Switch Allocator<br/>XYZ Dimension-Order Routing"]
    E["3D Thermal Stacking Dilemma<br/>Dielectric Adhesive Resistance Chains"]
  end

  subgraph Chiplets ["3. 2.5D Packaging & Open Protocols"]
    F["Advanced Packaging<br/>CoWoS, EMIB & Microbumps"]
    G["UCIe 1.0/2.0 Protocol Stack<br/>D2D Adapter, RDI, PHY (>1300 Gbps/mm)"]
    H["Sliding Window Link Retransmission<br/>Credit Queue Latency-Bandwidth Sizing"]
  end

  subgraph Frontiers ["4. Emerging Physical Frontiers"]
    I["Photonic NoC (ONoC)<br/>Waveguides, Micro-Ring Resonators, WDM"]
    J["Wireless NoC (WNoC)<br/>On-Chip Antennas & Sub-THz Shortcuts"]
  end

  A --> C
  A --> F
  B --> I
  B --> J
  C --> D --> E
  F --> G --> H

  classDef physStyle fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px,color:#991b1b;
  classDef stackStyle fill:#e0f2fe,stroke:#0284c7,stroke-width:1.5px,color:#075985;
  classDef chipStyle fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#92400e;
  classDef frontStyle fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#166534;

  class A,B physStyle;
  class C,D,E stackStyle;
  class F,G,H chipStyle;
  class I,J frontStyle;
```

---

## 📚 Syllabus & Chapters in Track 6

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 6.1</span>
      <div class="noc-track-title">3D TSV Interconnects &amp; Microarchitecture</div>
      <div class="noc-track-desc">
        Cylindrical TSV parasitics ($R_{tsv}, C_{tsv}$), keep-out zones (KOZ) from thermo-mechanical stress ($\sigma_{vm} \propto \Delta \alpha \cdot \Delta T$), 7-port 3D router crossbars ($7\times 7$, $+96\%$ area overhead), and sub-micron copper-copper hybrid bonding.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive 3D TSV Mesh &amp; 7-Port Router Architecture Visualizer, Synthesizable Verilog RTL (`router_3d_7port_allocator.v`), 3-Question Self-Check Quiz, Arcade Linkages (Topology Titans &amp; Arbiter Arena).
      </div>
    </div>
    <a href="01-3d-tsv-interconnects/" class="noc-track-link">Launch Lesson 6.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 6.2</span>
      <div class="noc-track-title">Multi-Chiplet Interconnects &amp; UCIe Standard</div>
      <div class="noc-track-desc">
        Reticle economics, negative binomial yield models, packaging technologies (Organic vs CoWoS vs EMIB), the Universal Chiplet Interconnect Express (UCIe) 3-layer stack, sliding-window replay buffers, shoreline bandwidth scaling ($>1300\text{ Gbps/mm}$), and credit queue round-trip latency sizing.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive Multi-Chiplet D2D Packaging &amp; UCIe Explorer, Synthesizable Verilog RTL (`ucie_d2d_link_adapter.v`), 3-Question Self-Check Quiz, Arcade Linkages (Chiplet Tycoon &amp; Credit Commander).
      </div>
    </div>
    <a href="02-chiplets-ucie-interconnects/" class="noc-track-link">Launch Lesson 6.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 6.3</span>
      <div class="noc-track-title">3D Topologies, Thermal Stacking &amp; Deadlock</div>
      <div class="noc-track-desc">
        Symmetric vs asymmetric/sparse 3D NoC topologies, 1D thermal resistance chains ($\Delta T_{stack} = \sum P_i R_i$), 3D Channel Dependency Graphs (CDGs), and formal proof of deadlock freedom under XYZ Dimension-Order Routing.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive 3D Thermal Stacking &amp; CDG Deadlock Simulator, Synthesizable Verilog RTL (`xyz_3d_dor_router.v`), 3-Question Self-Check Quiz, Arcade Linkages (Hotspot Hero &amp; Deadlock Buster).
      </div>
    </div>
    <a href="03-3d-topologies-thermal-deadlock/" class="noc-track-link">Launch Lesson 6.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 6.4</span>
      <div class="noc-track-title">Emerging Interconnect Frontiers: ONoC &amp; WNoC</div>
      <div class="noc-track-desc">
        RC copper delay walls, Optical NoC (silicon waveguides, micro-ring resonators, WDM, thermo-optic wavelength drift), delta-sigma digital micro-heater feedback control, on-chip mm-Wave Wireless NoC antennas, and comparative physical trade-offs.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive Silicon Micro-Ring Resonator (MRR) WDM &amp; Spectrum Tuner, Synthesizable Verilog RTL (`onoc_mrr_thermal_tuner.v`), 3-Question Self-Check Quiz, Arcade Linkages (Photon Pilot &amp; Wireless Wave).
      </div>
    </div>
    <a href="04-optical-wireless-frontiers/" class="noc-track-link">Launch Lesson 6.4 →</a>
  </div>
</div>

---

## 🎯 Track Learning Objectives

Upon completing Track 6, you will be able to:

1. **Calculate Electrical Parasitics of TSVs:** Compute lumped resistance, capacitance, and Elmore delay for vertical silicon vias, and quantify the silicon area tax imposed by piezo-resistive Keep-Out Zones (KOZ).
2. **Model Multi-Chiplet Yield & Packaging Economics:** Apply the negative binomial yield model to prove why multi-chiplet partitioning slashes manufacturing costs by $40\text{–}60\%$ on bleeding-edge nodes despite packaging overheads.
3. **Analyze the UCIe Standard:** Trace packets from high-level NoC protocols (AXI, CHI) through the UCIe D2D Adapter (CRC, parity, retry buffers) down to the Physical Layer (AFE, forwarded clock, lane reversal).
4. **Solve 3D Deadlock & Heat Dissipation Challenges:** Prove the acyclic nature of 3D Channel Dependency Graphs under XYZ DOR and calculate inter-tier thermal gradients across stacked logic and memory tiers.
5. **Evaluate Next-Generation Optical & Wireless Frontiers:** Analyze optical power budgets, insertion losses, and thermal tuning requirements for Silicon Micro-Ring Resonators, and evaluate wireless sub-THz shortcuts.
