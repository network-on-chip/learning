# 🎮 Interactive Labs & Arcade Simulator Hub

<div class="noc-hero">
  <div class="noc-track-badge">✨ 15 Hands-On Simulators, Mini-Games & Architectural Toolkits</div>
  <h1>Interactive NoC Laboratory & Arcade</h1>
  <p class="subtitle">
    Explore the inner workings of Network-on-Chip systems through 15 real-time, browser-native simulations and arcade challenges. Experience how packet collisions occur, dynamically balance thermal dissipation across silicon floorplans, route around permanent link defects, and design multi-die 2.5D/3D chiplet interconnects.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">🔬 15 Interactive Simulators</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">⚡ 100% Client-Side Canvas &amp; Audio</span>
    <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">💾 Synthesizable Verilog Mapped</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">🏆 Local &amp; Global Leaderboard Linked</span>
    <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #ec4899; border-color: rgba(236, 72, 153, 0.2);">📖 10 Textbook Chapters Aligned</span>
  </div>
</div>

<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">15</span>
    <span class="noc-stat-label">Hands-On Labs &amp; Games</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">5</span>
    <span class="noc-stat-label">Architectural Domains</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">0 ms</span>
    <span class="noc-stat-label">Server Latency (Zero Installs)</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">100%</span>
    <span class="noc-stat-label">Open Source &amp; Reproducible</span>
  </div>
</div>

---

## 🏛️ Categorized Laboratory Directory

Every simulator below is paired with formal mathematical models, synthesizable SystemVerilog implementations, and chapter sections from our official textbook.

### 1. Router Microarchitecture & Flow Control

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">Visualizer • Chapter 1 &amp; 3</span>
      <h3>2D Mesh Routing Visualizer</h3>
      <p>Inject synthetic traffic (Uniform, Bit-Complement, Transpose, Hotspot) across an $N \times N$ mesh. Observe flit progression through input buffers, route computation, and crossbar traversals in real time.</p>
    </div>
    <a href="visualizer/" class="noc-track-link">Launch 2D Mesh Visualizer →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">Interactive Lab • Chapter 3</span>
      <h3>Arbiter Arena: Crossbar Clash</h3>
      <p>Schedule competing packet requests across $5 \times 5$ crossbar switches. Compare Strict Priority, Round-Robin, Matrix Arbiter, and McKeown's iSLIP algorithm under adversarial traffic patterns.</p>
    </div>
    <a href="arbiter/" class="noc-track-link">Enter Arbiter Arena →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">Arcade Challenge • Chapter 2</span>
      <h3>Credit Commander: Flow Control Defense</h3>
      <p>Manage upstream credit tokens under sudden packet injection bursts. Prevent buffer overflows, eliminate credit-exhaustion bubbles, and optimize round-trip turnaround times ($B_{\min} \ge \text{RTT}$).</p>
    </div>
    <a href="credits/" class="noc-track-link">Play Credit Commander →</a>
  </div>
</div>

---

### 2. Routing Algorithms & Deadlock Theory

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">Action Arcade • Chapter 5</span>
      <h3>Deadlock Buster: Knots &amp; Escape VCs</h3>
      <p>Spot cyclic buffer dependency cycles before the entire interconnect freezes! Inject Duato escape channels, apply Dally turn models, and clear routing deadlocks across escalating challenge waves.</p>
    </div>
    <a href="game/" class="noc-track-link">Play Deadlock Buster →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">Logic Puzzle • Chapter 4 &amp; 5</span>
      <h3>Packet Master: Routing Puzzle</h3>
      <p>Guide flit trains through constrained router networks. Solve step-by-step spatial routing problems, avoid Head-of-Line blocking, and satisfy turn prohibition rules with minimal hop latency.</p>
    </div>
    <a href="puzzle/" class="noc-track-link">Solve Routing Puzzles →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(59, 130, 246, 0.15); color: #1d4ed8; border-color: rgba(59, 130, 246, 0.3);">Microarchitecture • Chapter 6</span>
      <h3>Deflection Duel: Bufferless NoC</h3>
      <p>Eliminate input buffer power using hot-potato deflection routing (BLESS/CHIPPER). Experience how deflection eliminates buffer area while managing deflection loops and livelock freedom under high load.</p>
    </div>
    <a href="deflection/" class="noc-track-link">Play Deflection Duel →</a>
  </div>
</div>

---

### 3. Physical Constraints: Thermal, Power &amp; Fault Resilience

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.2);">Thermal Physics • Chapter 7</span>
      <h3>Hotspot Hero: Thermal Defense</h3>
      <p>Model transient heat diffusion ($C_{th} \frac{dT}{dt} + \frac{T - T_{amb}}{R_{th}} = P$) in real time. Deploy dynamic voltage/frequency scaling (DVFS), thermal throttling, and cooling fans to prevent thermal runaway ($T_{\max} \le 85^\circ\text{C}$).</p>
    </div>
    <a href="hotspot/" class="noc-track-link">Play Hotspot Hero →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">Low-Power Circuits • Chapter 6</span>
      <h3>Volt Vortex: Dark Silicon Power</h3>
      <p>Control multi-core Voltage-Frequency Islands (VFIs) and sleep transistor power gating under strict Thermal Design Power (TDP) budgets. Minimize leakage power while maintaining system throughput.</p>
    </div>
    <a href="power/" class="noc-track-link">Launch Volt Vortex →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(245, 158, 11, 0.1); color: #d97706; border-color: rgba(245, 158, 11, 0.2);">Reliability • Chapter 7</span>
      <h3>Fault Defender: Silicon Resilience</h3>
      <p>Simulate electromigration, TDDB gate wearout, and permanent link severance. Reconfigure routing tables with Vicman bypass channels and verify fault recovery without system deadlocks.</p>
    </div>
    <a href="faults/" class="noc-track-link">Enter Fault Defender →</a>
  </div>
</div>

---

### 4. Advanced Packaging &amp; High-Radix Topologies

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">Packaging Architecture • Chapter 8 &amp; 9</span>
      <h3>Chiplet Tycoon: 2.5D/3D Multi-Die</h3>
      <p>Design next-generation heterogenous processors across passive silicon interposers, active interposers, and 3D TSV vertical stacks. Balance wafer yield ($Y$), UCIe D2D physical latency, and package thermal gradients.</p>
    </div>
    <a href="chiplet/" class="noc-track-link">Play Chiplet Tycoon →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(59, 130, 246, 0.1); color: #2563eb; border-color: rgba(59, 130, 246, 0.2);">Graph Theory • Chapter 4</span>
      <h3>Topology Titans: Graph Architect</h3>
      <p>Construct high-performance interconnection networks: 2D Torus, Hypercube, Flattened Butterfly, Dragonfly, and Slim Fly. Optimize network diameter, bisection bandwidth, and router radix within pin limits.</p>
    </div>
    <a href="topology/" class="noc-track-link">Build Network Graphs →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">Coherence &amp; Scheduling • Chapter 5</span>
      <h3>QoS Gladiator: Traffic Arbiter</h3>
      <p>Prevent protocol deadlocks in shared-memory multiprocessors. Separate request, forward, and response coherence message classes into isolated Virtual Networks (VNETs) and enforce strict SLA deadlines.</p>
    </div>
    <a href="qos/" class="noc-track-link">Enter QoS Gladiator →</a>
  </div>
</div>

---

### 5. Emerging Frontiers: Optical, Wireless &amp; Neuromorphic

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #db2777; border-color: rgba(236, 72, 153, 0.2);">Nanophotonics • Chapter 10</span>
      <h3>Photon Pilot: Optical NoC Grid</h3>
      <p>Route optical signals through silicon micro-ring resonators (MRRs) and WDM waveguides. Compensate for thermal drift ($0.1\text{ nm}/^\circ\text{C}$), balance optical insertion loss, and tune laser pump powers.</p>
    </div>
    <a href="optical/" class="noc-track-link">Navigate Photon Pilot →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(14, 165, 233, 0.1); color: #0284c7; border-color: rgba(14, 165, 233, 0.2);">Sub-THz RF • Chapter 10</span>
      <h3>Wireless Wave: mmWave &amp; THz NoC</h3>
      <p>Deploy 60 GHz and 140 GHz on-chip wireless transceivers. Broadcast coherence invalidations and barrier synchronizations across large die areas in a single clock cycle, bypassing multi-hop wire delay.</p>
    </div>
    <a href="wireless/" class="noc-track-link">Transmit Wireless Waves →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(168, 85, 247, 0.1); color: #7e22ce; border-color: rgba(168, 85, 247, 0.2);">Bio-Inspired Silicon • Track 7</span>
      <h3>Neuromorphic Nexus: SNN Spikes</h3>
      <p>Route Address-Event Representation (AER) neural spike packets across spiking neural networks. Measure multicast fanout, burst jitter, and synaptic routing efficiency in neuromorphic architectures.</p>
    </div>
    <a href="neuromorphic/" class="noc-track-link">Connect Neuromorphic Nexus →</a>
  </div>
</div>

---

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 20px 24px; margin-top: 2rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
      <span>🎯 Ready for Certification?</span>
    </div>
    <div style="font-size: 0.9rem; color: #cbd5e1; margin-top: 4px; max-width: 650px;">
      Put your architectural mastery to the test with our 3-tier <strong>Comprehensive Certification Exam</strong>, or review high-score baselines in the <strong>Hall of Fame</strong>.
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="../quiz/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Take Certification Exam →</span>
    </a>
    <a href="../leaderboard/" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>View Public Leaderboard →</span>
    </a>
  </div>
</div>
