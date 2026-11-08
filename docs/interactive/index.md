# 🔬 Interactive NoC Engineering CAD & Simulation Workbenches

<div class="noc-hero">
  <div class="noc-track-badge">✨ 20 Engineering-Grade EDA Simulators, CAD Workbenches &amp; Microarchitecture Toolkits</div>
  <h1>Interactive NoC Laboratory &amp; Architecture Workbench</h1>
  <p class="subtitle">
    Explore the inner workings of Network-on-Chip (NoC) systems through 20 browser-native, client-side engineering simulators and Web EDA environments. Model distributed RLC transmission lines, compute Graph Laplacian spectra and Fiedler algebraic connectivity, verify Channel Dependency Graphs (CDG) with Tarjan SCC cycles, simulate 2D Fourier heat diffusion and Dark Silicon power gating, and benchmark 100B+ LLM collective accelerators.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">🔬 20 Engineering CAD Workbenches</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">⚡ 100% Client-Side Canvas &amp; Math</span>
    <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">💾 Synthesizable Verilog &amp; SPICE Export</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">📐 Formal SMT &amp; Invariant Proofs</span>
    <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #ec4899; border-color: rgba(236, 72, 153, 0.2);">📖 12 Textbook Chapters Aligned</span>
  </div>
</div>

<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">20</span>
    <span class="noc-stat-label">Engineering Simulators</span>
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
  <div class="noc-track-card" style="border: 1px solid rgba(59, 130, 246, 0.45); background: linear-gradient(135deg, rgba(30, 58, 138, 0.12), rgba(15, 23, 42, 0.25));">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.15); color: #3b82f6; border-color: rgba(37, 99, 235, 0.3);">💻 In-Browser Virtual Bash • All Chapters</span>
      <h3>Web EDA Unix Terminal &amp; Workbench</h3>
      <p>A full-fledged in-browser command-line environment for NoC architecture. Execute <code>run-sim</code> discrete-event sweeps, <code>verify-deadlock</code> SMT proofs, Nangate45 <code>sta-timing</code> closure, and TCAD '26 HeatSense &amp; BuffeRS benchmarks.</p>
    </div>
    <a href="terminal/" class="noc-track-link" style="color: #60a5fa; font-weight: 700;">Launch Web EDA Terminal →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">Physical Interconnect • Chapter 1</span>
      <h3>Nanoscale Wire Physics &amp; Repeater CAD</h3>
      <p>Simulate distributed RLC transmission lines from 180nm down to 3nm GAA. Insert optimal Bakoglu repeaters, model copper scattering resistivity, and simulate transient step response ODEs.</p>
    </div>
    <a href="wire/" class="noc-track-link">Launch Wire Simulator →</a>
  </div>

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
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">Microarchitecture • Chapter 3</span>
      <h3>Switch Allocation &amp; Crossbar Arbiter Simulator</h3>
      <p>Schedule competing packet requests across $5 \times 5$ crossbar switches. Compare Strict Priority, Round-Robin, Matrix Arbiter, and McKeown's iSLIP algorithm under Karol's 58.6% HOL limit.</p>
    </div>
    <a href="arbiter/" class="noc-track-link">Launch Arbiter Simulator →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">Flow Control • Chapter 2</span>
      <h3>Credit-Based Flow Control &amp; Buffer Sizing CAD</h3>
      <p>Simulate credit loop round-trip latency ($B_{\min} = \lceil \text{RTT} \cdot \text{BW} \rceil$), space-time timing ladder progression, and credit bubble elimination under bursty traffic.</p>
    </div>
    <a href="credits/" class="noc-track-link">Launch Credit Simulator →</a>
  </div>
</div>

---

### 2. Routing Algorithms & Deadlock Theory

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">Deadlock Verification • Chapter 5</span>
      <h3>Deadlock Verification &amp; CDG Escape Channel Engine</h3>
      <p>Construct Channel Dependency Graphs (CDG) and detect circular wait cycles using Tarjan's SCC algorithm. Verify Dally &amp; Seitz and Duato escape virtual channel theorems.</p>
    </div>
    <a href="game/" class="noc-track-link">Launch Deadlock Engine →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">Routing Optimization • Chapter 4 &amp; 5</span>
      <h3>Turn-Model Routing Restrictions &amp; Path Optimizer</h3>
      <p>Evaluate Glass &amp; Ni turn models (West-First, North-Last, Negative-First) and Chiu's Odd-Even model on 2D meshes. Explore legal routing cones and bypass defect obstacles.</p>
    </div>
    <a href="puzzle/" class="noc-track-link">Launch Turn-Model Optimizer →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(59, 130, 246, 0.15); color: #1d4ed8; border-color: rgba(59, 130, 246, 0.3);">Microarchitecture • Chapter 6</span>
      <h3>Bufferless Deflection Routing (BLESS &amp; CHIPPER)</h3>
      <p>Eliminate input buffer static power using hot-potato deflection routing. Evaluate deflection rate curves, oldest-first age priority livelock freedom, and saturation knee thresholds.</p>
    </div>
    <a href="deflection/" class="noc-track-link">Launch Deflection Simulator →</a>
  </div>
</div>

---

### 3. Physical Constraints: Thermal, Power &amp; Fault Resilience

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.2);">Thermal Physics • Chapter 7</span>
      <h3>Silicon Thermal &amp; DTM Finite-Difference Solver</h3>
      <p>Model 2D transient Fourier heat diffusion ($C_{th} \frac{dT}{dt} + \frac{T - T_{amb}}{R_{th}} = P$) coupled with exponential subthreshold leakage runaway. Deploy closed-loop PI-DVFS and TAAR thermal-aware routing.</p>
    </div>
    <a href="hotspot/" class="noc-track-link">Launch Thermal Solver →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">Low-Power Circuits • Chapter 6</span>
      <h3>Dark Silicon Physics &amp; Power Gating CAD</h3>
      <p>Calculate utilization wall bounds from Dennard scaling breakdown ($\chi \propto \theta^{-\alpha}$). Size header/footer sleep transistors, simulate inrush currents, and export UPF specifications.</p>
    </div>
    <a href="power/" class="noc-track-link">Launch Power Gating CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(245, 158, 11, 0.1); color: #d97706; border-color: rgba(245, 158, 11, 0.2);">Reliability • Chapter 7</span>
      <h3>Silicon Fault Tolerance &amp; Resilient Routing CAD</h3>
      <p>Inject permanent link and router faults. Evaluate ZoneDefense convex perimeter detour routing, assess survivability curves under random failure rates, and export BIST diagnostics.</p>
    </div>
    <a href="faults/" class="noc-track-link">Launch Fault Tolerance CAD →</a>
  </div>
</div>

---

### 4. Advanced Packaging &amp; High-Radix Topologies

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">3D Silicon • Chapter 8</span>
      <h3>3D-NoC TSV Thermo-Mechanical Stress CAD Analyzer</h3>
      <p>Solve Lamé stress tensor equations, calculate piezoresistive carrier mobility Keep-Out Zones (KOZ), and model multi-tier vertical heat diffusion with dummy thermal TSVs.</p>
    </div>
    <a href="tsv3d/" class="noc-track-link">Launch TSV 3D CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">Packaging Architecture • Chapter 9</span>
      <h3>2.5D/3D Multi-Die Chiplet CAD &amp; Yield Optimizer</h3>
      <p>Model Murphy wafer yield, evaluate UCIe D2D physical latency and shoreline bandwidth density, and solve multi-die thermal coupling on active and passive interposers.</p>
    </div>
    <a href="chiplet/" class="noc-track-link">Launch Chiplet Optimizer →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(59, 130, 246, 0.1); color: #2563eb; border-color: rgba(59, 130, 246, 0.2);">Graph Theory • Chapter 4</span>
      <h3>Interconnect Topology CAD &amp; Spectral Graph Analyzer</h3>
      <p>Compute Graph Laplacian eigenvalues, evaluate algebraic connectivity (Fiedler vector $\lambda_2$), bisection bandwidth, and diameter across 2D Torus, Hypercubes, and Dragonfly topologies.</p>
    </div>
    <a href="topology/" class="noc-track-link">Launch Topology CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">Coherence &amp; Scheduling • Chapter 5</span>
      <h3>Mixed-Criticality Multi-VNET QoS &amp; Packet Scheduler</h3>
      <p>Prevent cache-coherence protocol deadlocks across isolated virtual networks (VNETs). Simulate Weighted Fair Queuing (WFQ) and Deficit Round Robin (DRR) schedulers.</p>
    </div>
    <a href="qos/" class="noc-track-link">Launch QoS Scheduler →</a>
  </div>
</div>

---

### 5. Emerging Frontiers: Optical, Wireless &amp; Neuromorphic

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #db2777; border-color: rgba(236, 72, 153, 0.2);">Nanophotonics • Chapter 10</span>
      <h3>Silicon Photonic &amp; Optical NoC (ONoC) Waveguide CAD</h3>
      <p>Model Lorentzian micro-ring resonator spectra, thermo-optic wavelength drift ($0.1\text{ nm}/^\circ\text{C}$), micro-heater closed-loop tuning, optical insertion loss waterfall, and link BER.</p>
    </div>
    <a href="optical/" class="noc-track-link">Launch Optical NoC CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(14, 165, 233, 0.1); color: #0284c7; border-color: rgba(14, 165, 233, 0.2);">Sub-THz RF • Chapter 10</span>
      <h3>On-Chip mmWave &amp; THz Wireless NoC (WiNoC) Simulator</h3>
      <p>Calculate Friis path loss through lossy doped silicon substrates ($G_{tx}, G_{rx}, \sigma_{Si}$). Simulate hybrid mesh-wireless routing and single-cycle barrier synchronization broadcast shortcuts.</p>
    </div>
    <a href="wireless/" class="noc-track-link">Launch Wireless NoC Simulator →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(168, 85, 247, 0.1); color: #7e22ce; border-color: rgba(168, 85, 247, 0.2);">Neuromorphic Silicon • Chapter 12</span>
      <h3>Spiking Neural Network (SNN) Multicast &amp; AER Router</h3>
      <p>Solve Leaky Integrate-and-Fire (LIF) membrane potential ODEs, simulate Address-Event Representation (AER) tree multicast, and measure fanout spike jitter in cortical arrays.</p>
    </div>
    <a href="neuromorphic/" class="noc-track-link">Launch Neuromorphic Simulator →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(239, 68, 68, 0.1); color: #dc2626; border-color: rgba(239, 68, 68, 0.2);">Hardware Security • Chapter 11</span>
      <h3>NoC Hardware Security &amp; Threat Defense CAD</h3>
      <p>Detect malicious Hardware Trojans via Shannon entropy profiling, cloak timing covert channels through traffic packet obfuscation, and mitigate DoS buffer flooding via PUF authentication.</p>
    </div>
    <a href="security/" class="noc-track-link">Launch Security CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #9333ea; border-color: rgba(139, 92, 246, 0.2);">AI Acceleration • Chapter 12</span>
      <h3>Distributed LLM AI Collective Accelerator &amp; 3D Memory</h3>
      <p>Model Ring AllReduce Scatter-Reduce and All-Gather token flows, evaluate Roofline arithmetic intensity, simulate 1F1B pipeline bubbles, and feed 16 TB/s HBM3e 3D memory stacks.</p>
    </div>
    <a href="transformer/" class="noc-track-link">Launch LLM Collective Simulator →</a>
  </div>
</div>

---

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 20px 24px; margin-top: 2rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
      <span>🎯 Ready for Certification?</span>
    </div>
    <div style="font-size: 0.9rem; color: #cbd5e1; margin-top: 4px; max-width: 650px;">
      Put your architectural mastery to the test with our 3-tier <strong>Comprehensive Certification Exam</strong>, covering physical packaging, routing theory, thermal modeling, and AI accelerators.
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="../quiz/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Take Certification Exam →</span>
    </a>
  </div>
</div>
