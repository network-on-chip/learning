# Track 1: Interconnect Fundamentals

<div class="noc-hero">
  <div class="noc-track-badge">Foundational Curriculum • Module 01</div>
  <h1>Interconnect Fundamentals &amp; Network-on-Chip Paradigm</h1>
  <p class="subtitle">
    Master the physical and architectural principles that govern on-chip communication. Explore why shared buses collapsed under Moore's Law, how packetized flow control revolutionized multi-core silicon, and how nanometer wires transport gigabytes of data every clock cycle.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ 4 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🔬 4 Interactive Simulators</span>
    <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">💾 Synthesizable Verilog RTL</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">🎯 3-Question Quizzes</span>
    <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #ec4899; border-color: rgba(236, 72, 153, 0.2);">🎮 Arcade Game Linkages</span>
  </div>
</div>

---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the concepts in Track 1 connect the physics of silicon wires to the protocol layers of on-chip routers:

```mermaid
graph TD
  subgraph Physical_Layer ["1. Physical Limits & Scaling Crisis"]
    RC["Elmore RC Wire Delay<br/>& Scattering Physics"] --> BusBottleneck["Shared Bus Breakdown<br/>(Serialization & Capacitance)"]
    CrossbarLimit["Crossbar O(N²) Area<br/>& Wiring Congestion"] --> BusBottleneck
  end

  subgraph Network_Paradigm ["2. Network-on-Chip Paradigm"]
    BusBottleneck --> NoCSolution["Route Packets, Not Wires<br/>(Short P2P Links, Concurrent Bandwidth)"]
    NoCSolution --> DataHierarchy["Data Hierarchy<br/>Message → Packet → Flit → Phit"]
  end

  subgraph Switching_FlowControl ["3. Switching & Flow Control"]
    DataHierarchy --> Switching["Switching Techniques<br/>Store-and-Forward vs VCT vs Wormhole"]
    Switching --> FlowCtrl["Lossless Flow Control<br/>Credit-Based vs On/Off Backpressure"]
    FlowCtrl --> BufferSizing["Credit RTT Loop &<br/>Minimum Buffer Sizing B_min ≥ RTT"]
  end

  subgraph System_Integration ["4. SoC Boundary & Interfacing"]
    BufferSizing --> NI["Network Interface (NI)<br/>AXI/TileLink Packetization & CDC FIFOs"]
    NI --> ProtoDeadlock["Protocol Deadlock Avoidance<br/>(Request/Response VNETs)"]
    ProtoDeadlock --> NextTrack["👉 Track 2: Router Microarchitecture"]
  end

  classDef phys fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px,color:#991b1b;
  classDef para fill:#e0e7ff,stroke:#6366f1,stroke-width:1.5px,color:#3730a3;
  classDef switch fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#166534;
  classDef sys fill:#fef3c7,stroke:#f59e0b,stroke-width:1.5px,color:#92400e;

  class RC,CrossbarLimit,BusBottleneck phys;
  class NoCSolution,DataHierarchy para;
  class Switching,FlowCtrl,BufferSizing switch;
  class NI,ProtoDeadlock,NextTrack sys;
```

---

## 📚 Syllabus & Chapters in Track 1

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 1.1</span>
      <div class="noc-track-title">Why Network-on-Chip?</div>
      <div class="noc-track-desc">
        Explore the breakdown of shared multi-drop buses (AMBA, Wishbone) and the quadratic area of crossbars. Learn Elmore wire delay models, electron scattering at sub-10nm nodes, repeater overheads, and the seminal 2001 breakthrough: <em>"Route packets, not wires."</em>
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive Bus vs Crossbar vs NoC Scalability Calculator, Intel TeraFLOPS &amp; SCC case studies, 3-Question Quiz, Arcade links to <em>Topology Titans</em> &amp; <em>2D Mesh Visualizer</em>.
      </div>
    </div>
    <a href="01-why-noc/" class="noc-track-link">Launch Lesson 1.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 1.2</span>
      <div class="noc-track-title">Packets, Flits &amp; Switching</div>
      <div class="noc-track-desc">
        Deconstruct application messages into Packets, Flits (Head, Body, Tail), and physical Phits. Compare Store-and-Forward (SAF), Virtual Cut-Through (VCT), and Wormhole (WH) switching with zero-load latency derivations, timing diagrams, and Head-of-Line blocking analysis.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive Switching Techniques Simulator with cycle-by-cycle animation, 3-Question Quiz, Arcade links to <em>Packet Master</em>, <em>Deflection Duel</em> &amp; <em>Arbiter Arena</em>.
      </div>
    </div>
    <a href="02-packet-switching-flits/" class="noc-track-link">Launch Lesson 1.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 1.3</span>
      <div class="noc-track-title">Flow Control &amp; Credit Mechanisms</div>
      <div class="noc-track-desc">
        Analyze lossless on-chip flow control protocols. Derive the Credit Round-Trip Time ($RTT$) loop and prove the fundamental buffer sizing condition ($B_{min} \ge RTT$) required to sustain 100% throughput line rate without pipeline bubbles.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable Verilog <code>credit_flow_control.v</code>, Interactive Credit Turnaround Loop Simulator, 3-Question Quiz, Arcade link to <em>Credit Commander</em>.
      </div>
    </div>
    <a href="03-flow-control-credit/" class="noc-track-link">Launch Lesson 1.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 1.4</span>
      <div class="noc-track-title">Network Interface (NI) Architecture</div>
      <div class="noc-track-desc">
        Bridge the gap between IP cores and routers. Understand how ARM AXI and RISC-V TileLink transactions are packetized, how dual-clock asynchronous FIFOs cross clock domains (CDC), and how Virtual Networks (VNETs) eliminate protocol deadlocks.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable Verilog <code>async_fifo_cdc.v</code>, Interactive AXI-to-Flit Packetizer Explorer, 3-Question Quiz, Arcade links to <em>QoS Gladiator</em> &amp; <em>Packet Master</em>.
      </div>
    </div>
    <a href="04-network-interface-packetization/" class="noc-track-link">Launch Lesson 1.4 →</a>
  </div>
</div>

---

## 🎯 Track Learning Objectives

Upon completing Track 1, you will be able to:

1. **Calculate wire delays and bandwidth limits** for multi-drop buses and identify when a design must transition to an on-chip network.
2. **Evaluate the tradeoffs** between Store-and-Forward, Virtual Cut-Through, and Wormhole switching regarding buffer silicon area, pipeline delay, and latency under zero load.
3. **Formulate flit header bit allocations** including routing IDs, Virtual Channel specifiers, Quality-of-Service priorities, and payload error-correcting codes.
4. **Dimension router input buffers** using the Credit Round-Trip Time ($RTT$) equation to ensure 100% sustained link utilization across varying wire delays.
5. **Architect a complete Network Interface (NI)** to convert memory bus bursts (AXI/TileLink) into flit streams, cross clock domains via asynchronous FIFOs, and prevent protocol-level fetch deadlocks.

---

## 🔬 Silicon Milestones at a Glance

The transition from buses to NoCs represents one of the most critical shifts in semiconductor history:

| Year | Architecture | Interconnect Mechanism | Significance |
| :--- | :--- | :--- | :--- |
| **1996** | ARM AMBA (AHB/APB) | Multi-drop Shared Bus | Defined early 2D SoC interconnect; hit severe limits beyond 4–8 masters. |
| **2001** | Benini &amp; De Micheli / Dally &amp; Towles | Theoretical NoC Framework | Seminal papers establishing the <em>"Route packets, not wires"</em> paradigm. |
| **2007** | Intel Polaris (TeraFLOPS) | 80-Tile 2D Mesh NoC | First silicon demonstration of 1.0+ TeraFLOPS at 62W with 5-port packet routers. |
| **2010** | Intel SCC | 48-Core 2D Mesh NoC | Single-Chip Cloud Computer proving message-passing on a $6 \times 4$ router grid. |
| **2011** | Tilera TILE-Gx | 64-Tile iMesh Architecture | Commercial multicore server chip with 5 independent parallel 2D mesh networks. |
| **2017** | Intel Skylake-SP | Scalable 2D Ring/Mesh Fabric | Replaced monolithic ring buses with a 2D mesh spanning 28+ server cores. |
| **2021** | Apple M1 Max / Ultra | UltraFusion 2.5 TB/s D2D NoC | High-density passive interposer linking dual dies with ultra-low latency packet fabric. |
| **2023** | AMD EPYC Genoa &amp; Zen 4 | Infinity Fabric NoC | Modular chiplet architecture connecting 12 CCDs through a centralized I/O die. |

Ready to begin? Start with **[Lesson 1.1: Why Network-on-Chip?](01-why-noc.md)**.
