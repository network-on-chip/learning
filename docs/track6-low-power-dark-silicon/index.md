# Track 6: Low-Power Architectures & Dark Silicon

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 06</div>
  <h1>Low-Power Architectures & Dark Silicon</h1>
  <p class="subtitle">Dark silicon physics, Thermal Design Power (TDP) budgets, Voltage/Frequency Islands (VFIs), fine-grained power gating, and L*di/dt emergencies.</p>
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
      <span>📚 Aligned with Chapter 6 of Official 12-Chapter Textbook</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Explore complete theoretical derivations, physical scaling parameters, and microarchitectural proofs in <strong>Chapter 6</strong>.
    </div>
  </div>
  <a href="../textbook/ch06-low-power-dark-silicon/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Read Chapter 6 in Textbook →</span>
  </a>
</div>


---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track 6 connect across the physical and protocol layers:

```mermaid
graph TD
  Dennard['Dennard Breakdown'] --> DarkSilicon['Dark Silicon Floorplans']
  DarkSilicon --> DVFS['Voltage/Frequency Islands']
  DVFS --> PowerGating['Router Micro Power Gating']
```

---

## 📚 Syllabus & Lessons in Track 6

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 6.1</span>
      <div class="noc-track-title">Dark Silicon Physics & TDP Scaling Limits</div>
      <div class="noc-track-desc">Why Dennard scaling death leaves up to 80% of silicon unpowered at 3nm.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Dark Silicon Floorplan Calculator
      </div>
    </div>
    <a href="01-dark-silicon-physics/" class="noc-track-link">Launch Lesson 6.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 6.2</span>
      <div class="noc-track-title">Voltage & Frequency Islands (VFIs) and DVFS</div>
      <div class="noc-track-desc">Multi-domain voltage scaling, asynchronous FIFO clock-domain crossings, and energy-delay product.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Volt Vortex Interactive Lab
      </div>
    </div>
    <a href="02-dvfs-voltage-islands/" class="noc-track-link">Launch Lesson 6.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 6.3</span>
      <div class="noc-track-title">Router Microarchitectural Power Gating</div>
      <div class="noc-track-desc">Sleep transistors, wake-up latency penalties, lookahead credit power wakeup, and zero-leakage state.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable Power Gating FSM RTL
      </div>
    </div>
    <a href="03-power-gating-router/" class="noc-track-link">Launch Lesson 6.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 6.4</span>
      <div class="noc-track-title">Voltage Emergencies & Energy-Efficient Encoding</div>
      <div class="noc-track-desc">Inductive L*di/dt resonance, decap allocation, bus-invert coding, and energy-delay optimization.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> L-di/dt Noise Analyzer
      </div>
    </div>
    <a href="04-voltage-emergencies-energy/" class="noc-track-link">Launch Lesson 6.4 →</a>
  </div>

</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track 6 using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc-lab:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
