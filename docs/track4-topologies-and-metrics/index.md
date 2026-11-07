# Track 4: Direct, Indirect & High-Radix Topologies

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 04</div>
  <h1>Direct, Indirect & High-Radix Topologies</h1>
  <p class="subtitle">Direct (Mesh, Torus), Indirect (Clos, Fat-Tree, cMesh), and High-Radix (Dragonfly, Flattened Butterfly). Mathematical derivations of T0, Theta_sat, and bisection bandwidth.</p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ 4 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🔬 Interactive Simulators &amp; Tools</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">💻 Synthesizable Verilog RTL</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">📜 Grounded in Official Monograph</span>
  </div>
</div>


<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>📚 Aligned with Chapter 4 of Official 12-Chapter Textbook</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Explore complete theoretical derivations, physical scaling parameters, and microarchitectural proofs in <strong>Chapter 4</strong>.
    </div>
  </div>
  <a href="../textbook/ch04-topologies-and-metrics/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Read Chapter 4 in Textbook →</span>
  </a>
</div>


---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track 4 connect across the physical and protocol layers:

```mermaid
graph TD
  Mesh['2D Mesh & Torus'] --> cMesh['Concentrated cMesh']
  cMesh --> HighRadix['High-Radix Dragonfly']
  HighRadix --> Metrics['Bisection & Saturation Metrics']
```

---

## 📚 Syllabus & Lessons in Track 4

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 4.1</span>
      <div class="noc-track-title">Direct Topologies: Mesh & Torus</div>
      <div class="noc-track-desc">Cartesian topologies, wrap-around links, Folded Torus layout, and bisection bandwidth proofs.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive 2D Mesh & Torus Simulator
      </div>
    </div>
    <a href="01-direct-topologies/" class="noc-track-link">Launch Lesson 4.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 4.2</span>
      <div class="noc-track-title">Indirect & Concentrated Networks</div>
      <div class="noc-track-desc">Clos networks, Fat-Trees, and node concentration (cMesh) reducing router count.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Concentrated Mesh Floorplanner
      </div>
    </div>
    <a href="02-indirect-hierarchical/" class="noc-track-link">Launch Lesson 4.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 4.3</span>
      <div class="noc-track-title">Interconnect Metrics & Traffic Patterns</div>
      <div class="noc-track-desc">Bisection bandwidth, network diameter, zero-load latency T0, and synthetic traffic patterns.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Throughput & Latency Curve Analyzer
      </div>
    </div>
    <a href="03-metrics-traffic-patterns/" class="noc-track-link">Launch Lesson 4.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 4.4</span>
      <div class="noc-track-title">High-Radix Networks: Dragonfly & Flattened Butterfly</div>
      <div class="noc-track-desc">Exploiting high-radix routers to minimize network diameter, coupled with UGAL adaptive routing.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Dragonfly Group Routing Simulator
      </div>
    </div>
    <a href="04-high-radix-topologies/" class="noc-track-link">Launch Lesson 4.4 →</a>
  </div>

</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track 4 using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
