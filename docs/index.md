<div class="noc-hero">
  <div class="noc-track-badge">✨ Open-Source Curriculum & Research Lab</div>
  <h1>Network-on-Chip Learning Hub</h1>
  <p class="subtitle">
    An interactive, scholarly curriculum bridging theoretical computer architecture, silicon router microarchitecture, and open-source reproducible research. Grounded in 541 curated IEEE papers and verified hardware simulations.
  </p>
  <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
    <a href="track1-fundamentals/" class="noc-sim-btn" style="text-decoration: none;">🚀 Start Learning</a>
    <a href="quiz/" class="noc-sim-btn" style="text-decoration: none; background: #0284c7;">🎯 Take Certification Quiz</a>
    <a href="interactive/game/" class="noc-sim-btn" style="text-decoration: none; background: #ea580c;">👾 Play Deadlock Buster</a>
    <a href="interactive/puzzle/" class="noc-sim-btn" style="text-decoration: none; background: #8b5cf6;">🧩 Packet Master Puzzle</a>
    <a href="interactive/visualizer/" class="noc-sim-btn secondary" style="text-decoration: none;">🎮 2D Mesh Simulator</a>
    <a href="leaderboard/" class="noc-sim-btn secondary" style="text-decoration: none;">🏆 Leaderboard</a>
    <a href="glossary/" class="noc-sim-btn secondary" style="text-decoration: none;">📖 Glossary</a>
  </div>
</div>

<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">541</span>
    <span class="noc-stat-label">Curated IEEE Papers</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">37,400+</span>
    <span class="noc-stat-label">Extracted Figures & RTL</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">7</span>
    <span class="noc-stat-label">Mastery Tracks</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">100%</span>
    <span class="noc-stat-label">Open & Reproducible</span>
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
        ⚡ 4 Interactive Simulators &amp; High-Radix Analyzer
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
        ⚡ 4 Interactive Simulators &amp; Lookahead Verilog RTL
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
        ⚡ 4 Interactive Simulators &amp; In-Lab ML Research
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
        ⚡ 4 Interactive Simulators &amp; UCIe Trade-Off Engine
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
        ⚡ 4 Interactive Silicon Simulators &amp; Ground Truth Papers
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
Begin your journey with [Track 1: Interconnect Fundamentals](track1-fundamentals/) or try out the [Interactive Simulator](interactive/visualizer/)!
