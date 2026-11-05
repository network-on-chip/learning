# Track 2: Router Microarchitecture

<div class="noc-hero">
  <div class="noc-track-badge">Silicon Microarchitecture • Module 02</div>
  <h1>On-Chip Router Microarchitecture &amp; Pipeline Design</h1>
  <p class="subtitle">
    Explore the internal anatomy of silicon on-chip routers. From the classic 5-stage canonical pipeline (BW-RC-VA-SA-ST) to 1-stage speculative bypass routers, matrix arbiters, and crossbar switches capable of switching terabits per second in sub-nanosecond cycle times.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ 4 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🔬 4 Interactive Simulators</span>
    <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">💾 5 Synthesizable Verilog Modules</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">🎯 3-Question Quizzes</span>
    <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #ec4899; border-color: rgba(236, 72, 153, 0.2);">🎮 Arcade Game Linkages</span>
  </div>
</div>

---

## 🗺️ Microarchitecture Roadmap

The diagram below illustrates how flit datapaths and control logic interact within a standard 5-port on-chip router:

```mermaid
graph TD
  subgraph Input_Unit ["1. Input Buffering & Routing"]
    InLink["Incoming Physical Link (North, South, East, West, Local)"] --> BW["Buffer Write (BW)<br/>Demux to Virtual Channel FIFOs"]
    BW --> VCFIFO["Virtual Channel FIFOs (VC 0 .. VC V-1)"]
    VCFIFO --> RC["Route Computation (RC)<br/>XY / Lookahead Pre-routing"]
  end

  subgraph Control_Allocation ["2. Arbitration & Allocation Engine"]
    RC --> VA["Virtual Channel Allocation (VA)<br/>Bids for Downstream VC"]
    VA --> SA["Switch Allocation (SA)<br/>Separable Input/Output Arbiters"]
    SA --> MatrixArb["Fast Matrix Arbiters<br/>(Sub-200ps LRU Matrix Logic)"]
  end

  subgraph Switch_Datapath ["3. Crossbar & Traversal"]
    MatrixArb --> XbarConfig["Crossbar Select Signals"]
    VCFIFO --> XbarMux["Crossbar Switch Multiplexers<br/>(5×5 Matrix / Mux Tree)"]
    XbarConfig --> XbarMux
    XbarMux --> ST["Switch Traversal (ST)"]
    ST --> OutLatch["Output Port Registers"]
    OutLatch --> LT["Link Traversal (LT) ➔ Adjacent Router"]
  end

  subgraph Bypass_Path ["4. Ultra-Low-Latency Optimizations"]
    BW -.->|"Empty Queue & No Conflict"| SpecBypass["1-Cycle Speculative Crossbar Bypass (SMART)"]
    SpecBypass -.-> OutLatch
  end

  classDef inunit fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px,color:#1e3a8a;
  classDef ctrl fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px,color:#991b1b;
  classDef data fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#166534;
  classDef bypass fill:#fef3c7,stroke:#f59e0b,stroke-width:1.5px,color:#92400e;

  class InLink,BW,VCFIFO,RC inunit;
  class VA,SA,MatrixArb ctrl;
  class XbarConfig,XbarMux,ST,OutLatch,LT data;
  class SpecBypass bypass;
```

---

## 📚 Syllabus & Chapters in Track 2

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 2.1</span>
      <div class="noc-track-title">Canonical Router Pipeline</div>
      <div class="noc-track-desc">
        Deconstruct the classical 5-stage router pipeline: Buffer Write (BW), Route Computation (RC), Virtual Channel Allocation (VA), Switch Allocation (SA), and Switch Traversal (ST). Learn how Head flits carve the path while Body/Tail flits bypass RC and VA.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable Verilog <code>lookahead_route_compute.v</code>, Interactive Pipeline Stepper, 3-Question Quiz, Arcade links to <em>Packet Master</em> &amp; <em>Deadlock Buster</em>.
      </div>
    </div>
    <a href="01-pipeline-stages.md" class="noc-track-link">Launch Lesson 2.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 2.2</span>
      <div class="noc-track-title">Virtual Channel (VC) Architecture</div>
      <div class="noc-track-desc">
        Eliminate Head-of-Line (HoL) blocking by multiplexing multiple logical FIFOs onto a shared physical link. Understand the VC finite state machine (IDLE, ROUTING, WAITING_VC, ACTIVE), dynamic buffer allocation, and Virtual Networks (VNETs).
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable Verilog <code>vc_fsm_allocator.v</code>, Interactive HoL Solver, 3-Question Quiz, Arcade links to <em>Arbiter Arena</em> &amp; <em>QoS Gladiator</em>.
      </div>
    </div>
    <a href="02-virtual-channels.md" class="noc-track-link">Launch Lesson 2.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 2.3</span>
      <div class="noc-track-title">Arbitration &amp; Crossbar Switching</div>
      <div class="noc-track-desc">
        Architect sub-nanosecond arbiters: Round-Robin vs Triangular Matrix Arbiters with Least Recently Used (LRU) updates. Solve the bipartite maximum matching bottleneck using Separable Input-First and Output-First Switch Allocators.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable Verilog <code>matrix_arbiter.v</code> &amp; <code>crossbar_5x5.v</code>, Interactive 4×4 Matrix Simulator, 3-Question Quiz, Arcade links to <em>Arbiter Arena</em> &amp; <em>Chiplet Tycoon</em>.
      </div>
    </div>
    <a href="03-arbitration-crossbar.md" class="noc-track-link">Launch Lesson 2.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 2.4</span>
      <div class="noc-track-title">Low-Latency &amp; Single-Cycle Routers</div>
      <div class="noc-track-desc">
        Explore aggressive microarchitectural optimizations: Speculative Switch Allocation (Peh &amp; Dally), 1-cycle direct crossbar bypass, and SMART (Single-cycle Multi-hop Asynchronous Repeated Traversal) for multi-hop zero-delay bypass.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable Verilog <code>smart_bypass_unit.v</code>, Interactive SMART Multi-Hop Simulator, 3-Question Quiz, Arcade links to <em>Deflection Duel</em> &amp; <em>Hotspot Hero</em>.
      </div>
    </div>
    <a href="04-low-latency-bypass-routers.md" class="noc-track-link">Launch Lesson 2.4 →</a>
  </div>
</div>

---

## 🎯 Track Learning Objectives

Upon completing Track 2, you will be able to:

1. **Trace the exact clock cycle timing** of Head, Body, and Tail flits through a pipelined router and compute the uncontended zero-load router latency.
2. **Design and configure Virtual Channel state machines** to completely eliminate Head-of-Line blocking and isolate cache coherence protocol traffic into independent Virtual Networks.
3. **Implement synthesizable Verilog RTL** for high-frequency Matrix Arbiters and explain how 2-gate-level triangular priority matrices enforce LRU fairness.
4. **Evaluate Separable Switch Allocators** (Input-First vs Output-First) and calculate bipartite matching efficiency under synthetic and real-world traffic patterns.
5. **Architect single-cycle speculative bypass routers** (SMART and lookahead routing) to compress per-hop traversal penalties from 5 clock cycles down to 1 clock cycle.

Ready to begin? Start with **[Lesson 2.1: Canonical Router Pipeline](01-pipeline-stages.md)**.
