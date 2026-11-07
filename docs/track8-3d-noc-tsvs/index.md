# Track 8: Three-Dimensional NoC (3D-NoC) & TSVs

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 08</div>
  <h1>Three-Dimensional NoC (3D-NoC) & TSVs</h1>
  <p class="subtitle">Through-Silicon Vias (TSVs), Keep-Out Zones (KOZ), thermo-mechanical stress, 7-port 3D crossbars, vertical serialization, and 3D thermal stacking.</p>
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
      <span>📚 Aligned with Chapter 8 of Official 12-Chapter Textbook</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Explore complete theoretical derivations, physical scaling parameters, and microarchitectural proofs in <strong>Chapter 8</strong>.
    </div>
  </div>
  <a href="../textbook/ch08-3d-noc-tsvs/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Read Chapter 8 in Textbook →</span>
  </a>
</div>


---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track 8 connect across the physical and protocol layers:

```mermaid
graph TD
  TSVPhysics['TSV Parasitics & KOZ'] --> Microarch3D['7-Port 3D Router Microarch']
  Microarch3D --> ThermalStacking['3D Thermal Stacking Bottlenecks']
  ThermalStacking --> Deadlock3D['3D Deadlock Freedom']
```

---

## 📚 Syllabus & Lessons in Track 8

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 8.1</span>
      <div class="noc-track-title">3D Integration & Through-Silicon Via (TSV) Physics</div>
      <div class="noc-track-desc">TSV aspect ratios, capacitive parasitics, microbump arrays, and vertical link scaling.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> TSV Parasitic & Delay Explorer
      </div>
    </div>
    <a href="01-3d-tsv-interconnects/" class="noc-track-link">Launch Lesson 8.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 8.2</span>
      <div class="noc-track-title">TSV Keep-Out Zones (KOZ) & Stress Fields</div>
      <div class="noc-track-desc">Thermo-mechanical mismatch (Cu vs Si), piezoresistive mobility shifts, and KOZ floorplanning.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> KOZ Stress Field Visualizer
      </div>
    </div>
    <a href="02-tsv-parasitics-koz/" class="noc-track-link">Launch Lesson 8.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 8.3</span>
      <div class="noc-track-title">3D Router Microarchitecture & 7-Port Crossbars</div>
      <div class="noc-track-desc">Up/Down vertical port allocation, asymmetric vertical serialization, and 3D arbiters.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> 7-Port 3D Router SystemVerilog RTL
      </div>
    </div>
    <a href="03-3d-router-microarchitecture/" class="noc-track-link">Launch Lesson 8.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 8.4</span>
      <div class="noc-track-title">3D Topologies, Thermal Stacking & Routing Deadlock</div>
      <div class="noc-track-desc">Vertical heat dissipation bottlenecks, true 3D deadlock models, and dimension-order extensions.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> TSV Titan 3D Architecture Lab
      </div>
    </div>
    <a href="04-3d-topologies-thermal-deadlock/" class="noc-track-link">Launch Lesson 8.4 →</a>
  </div>

</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track 8 using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc-lab:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
