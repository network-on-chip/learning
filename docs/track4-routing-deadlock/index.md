# Track 4: Routing Algorithms & Deadlock Avoidance

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 04</div>
  <h1>Routing Algorithms &amp; Formal Deadlock Avoidance</h1>
  <p class="subtitle">
    Master how packets navigate complex network topologies. From deterministic Dimension-Order Routing (DOR) to Glass &amp; Ni's Turn Model, Chiu's Odd-Even algorithm, and Duato's Escape Channels—learn to design high-throughput, adaptive, and provably deadlock-free routing engines.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ 4 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🔬 4 Interactive Simulators &amp; Visualizers</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">💻 4 Synthesizable Verilog RTL Modules</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">📐 Dally-Seitz &amp; Duato Formal Theorems</span>
  </div>
</div>

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>📚 Aligned with Official Textbook Chapter 5</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      For rigorous mathematical proofs of the Dally-Seitz theorem, Channel Dependency Graphs (CDG), Glass-Ni turn models, Duato's escape channels, and cache coherence VNET isolation, read <strong>Chapter 5: Deadlock Theory, Turn Models &amp; Adaptive Routing</strong>.
    </div>
  </div>
  <a href="../textbook/ch05-routing-deadlock-theory/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none; transition: background 0.2s;">
    <span>Read Chapter 5 Online →</span>
  </a>
</div>

---

## 🗺️ Routing Algorithms Taxonomy & Roadmap

The diagram below maps the algorithmic landscape of network routing, from simple hardware state machines to formally verified adaptive and fault-tolerant architectures:

```mermaid
graph TD
  subgraph Routing_Taxonomy ["Network-on-Chip Routing Taxonomy"]
    Root["Routing Algorithm"] --> Det["Deterministic<br/>(Single fixed path per flow)"]
    Root --> Obl["Oblivious<br/>(Path independent of network state)"]
    Root --> Adapt["Adaptive<br/>(Path responds to real-time congestion)"]
    Root --> Fault["Fault-Tolerant & Protocol<br/>(Resilient to Failures & Stalls)"]

    Det --> DOR["Dimension-Order Routing (DOR)<br/>XY, YX & e-cube"]
    Det --> Lookup["ROM / Table-Driven<br/>Arbitrary static topologies"]

    Obl --> VAL["Valiant's Algorithm (VAL)<br/>Random intermediate hop"]
    Obl --> ROMM["ROMM<br/>Randomized Minimal Paths"]

    Adapt --> TurnModel["The Turn Model (Glass & Ni)<br/>(West-First / North-Last / Neg-First)"]
    Adapt --> OddEven["Odd-Even Routing (Chiu)<br/>Column parity turn restriction"]
    Adapt --> Duato["Escape Channels (Duato)<br/>Acyclic C0 escape + adaptive C1"]

    Fault --> UpDown["Up*/Down* Tree Routing<br/>Acyclic graph on irregular topologies"]
    Fault --> VNETs["Virtual Networks (VNETs)<br/>Request-Reply protocol isolation"]
  end

  classDef detStyle fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px,color:#1e3a8a;
  classDef oblStyle fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#92400e;
  classDef adaptStyle fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#166534;
  classDef faultStyle fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px,color:#991b1b;

  class Det,DOR,Lookup detStyle;
  class Obl,VAL,ROMM oblStyle;
  class Adapt,TurnModel,OddEven,Duato adaptStyle;
  class Fault,UpDown,VNETs faultStyle;
```

---

## 📚 Syllabus & Chapters in Track 4

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 4.1</span>
      <div class="noc-track-title">Deterministic Dimension-Order Routing (DOR)</div>
      <div class="noc-track-desc">
        Algorithmic foundations of XY and YX routing. Single-cycle combinational Route Computation (RC), lookahead routing optimization, synthesizable Verilog RTL (`lookahead_route_comp.v`), and mathematical proof of deadlock-freedom via monotonic dimension traversal.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive XY / YX Path Stepper, Synthesizable Verilog RTL (`lookahead_route_comp.v`), 3-Question Self-Check Quiz, Arcade Linkages (Packet Master &amp; Deadlock Buster).
      </div>
    </div>
    <a href="01-deterministic-dor/" class="noc-track-link">Launch Lesson 4.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 4.2</span>
      <div class="noc-track-title">Adaptive Routing &amp; The Turn Model</div>
      <div class="noc-track-desc">
        Overcoming deterministic congestion bottlenecks. Christopher Glass and Lionel Ni's Turn Model: breaking all directed cycles by prohibiting only 2 out of 8 turns. West-First, North-Last, Ge-Ming Chiu's balanced Odd-Even turn model, and synthesizable dual-mode RTL (`turn_model_adaptive_router.v`).
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive Turn Model Playground, Synthesizable Verilog RTL (`turn_model_adaptive_router.v`), 3-Question Self-Check Quiz, Arcade Linkages (Packet Master &amp; Deadlock Buster).
      </div>
    </div>
    <a href="02-adaptive-turn-model/" class="noc-track-link">Launch Lesson 4.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 4.3</span>
      <div class="noc-track-title">Formal Deadlock Theory &amp; Duato's Escape Channels</div>
      <div class="noc-track-desc">
        Rigorous graph-theoretic foundations: Channel Dependency Graphs (CDGs). Dally &amp; Seitz's necessary and sufficient condition for deterministic routing. José Duato's breakthrough Escape Channel Theorem ($C = C_1 \cup C_0$), and synthesizable escape-channel VC allocator RTL (`duato_escape_vc_allocator.v`).
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive CDG Deadlock Simulator &amp; Escape Channel Flusher, Synthesizable Verilog RTL (`duato_escape_vc_allocator.v`), 3-Question Self-Check Quiz, Arcade Linkages (Deadlock Buster &amp; Arbiter Arena).
      </div>
    </div>
    <a href="03-deadlock-theory-cdg/" class="noc-track-link">Launch Lesson 4.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 4.4</span>
      <div class="noc-track-title">Fault-Tolerant Routing &amp; Protocol Deadlock Avoidance</div>
      <div class="noc-track-desc">
        Surviving hardware degradation and cache protocol stalls. Convex fault rings, Up*/Down* spanning tree routing for irregular and damaged topologies, deadlock recovery (DISHA token), hardware Virtual Networks (VNETs) to avoid MESI Request-Response deadlocks, and synthesizable VNET priority scheduler RTL (`vnet_protocol_isolator.v`).
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive VNET Isolation Visualizer, Synthesizable Verilog RTL (`vnet_protocol_isolator.v`), 3-Question Self-Check Quiz, Arcade Linkages (Fault Defender &amp; QoS Gladiator).
      </div>
    </div>
    <a href="04-fault-tolerant-protocol-deadlock/" class="noc-track-link">Launch Lesson 4.4 →</a>
  </div>
</div>

---

## 🎯 Track Learning Objectives

Upon completing Track 4, you will be able to:

1. **Implement single-cycle lookahead route computation** in synthesizable Verilog for Dimension-Order Routing (DOR).
2. **Apply Glass &amp; Ni's Turn Model** to eliminate clockwise and counter-clockwise cycles with minimal turn restrictions.
3. **Analyze Chiu's Odd-Even routing algorithm** to provide direction-balanced adaptivity without requiring dedicated virtual channels.
4. **Construct Channel Dependency Graphs (CDGs)** and apply the **Dally-Seitz** and **Duato Theorems** to mathematically prove deadlock-freedom.
5. **Architect Escape Virtual Channels** ($C = C_1 \cup C_0$) in router crossbars to enable aggressive adaptive routing without deadlock risk.
6. **Differentiate routing-level deadlock from cache coherence protocol-level deadlock**, and design multi-tier Virtual Networks (VNETs) to eliminate Request-Response dependency cycles.

Ready to begin? Start with **[Lesson 4.1: Deterministic Dimension-Order Routing (DOR)](01-deterministic-dor.md)**.
