# Track 10: Optical & Wireless Networks-on-Chip

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 10</div>
  <h1>Optical & Wireless Networks-on-Chip</h1>
  <p class="subtitle">Silicon nanophotonics, microring resonators (MRRs), wavelength-routed ONoC (WRONoC), laser power-gating, and on-chip mmWave/THz wireless antennas.</p>
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
      <span>📚 Aligned with Chapter 10 of Official 12-Chapter Textbook</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Explore complete theoretical derivations, physical scaling parameters, and microarchitectural proofs in <strong>Chapter 10</strong>.
    </div>
  </div>
  <a href="../textbook/ch10-optical-wireless/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Read Chapter 10 in Textbook →</span>
  </a>
</div>


---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track 10 connect across the physical and protocol layers:

```mermaid
graph TD
  Photonics['Silicon Nanophotonics & MRRs'] --> WRONoC['Dense WDM Optical Crossbars']
  WRONoC --> LaserPower['Laser Power-Gating & APC']
  LaserPower --> WiNoC['On-Chip mmWave/THz Wireless']
```

---

## 📚 Syllabus & Lessons in Track 10

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 10.1</span>
      <div class="noc-track-title">Silicon Nanophotonics & Microring Resonators</div>
      <div class="noc-track-desc">Waveguides, microring resonators (MRRs), electro-optic modulation, and zero-capacitance light flight.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Photon Pilot Optical Grid
      </div>
    </div>
    <a href="01-silicon-nanophotonics-mrrs/" class="noc-track-link">Launch Lesson 10.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 10.2</span>
      <div class="noc-track-title">Wavelength-Routed Optical NoC (WRONoC)</div>
      <div class="noc-track-desc">Dense Wavelength-Division Multiplexing (DWDM), non-blocking optical crossbar matrices, and insertion loss.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Optical Insertion Loss Analyzer
      </div>
    </div>
    <a href="02-wronoc-optical-crossbars/" class="noc-track-link">Launch Lesson 10.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 10.3</span>
      <div class="noc-track-title">Laser Power-Gating & Thermal Drift Compensation</div>
      <div class="noc-track-desc">Silicon thermo-optic coefficients (0.10 nm/K), Automated Phase Control (APC), and laser power efficiency.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> APC Thermal Drift Simulator
      </div>
    </div>
    <a href="03-laser-power-gating-apc/" class="noc-track-link">Launch Lesson 10.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 10.4</span>
      <div class="noc-track-title">On-Chip Wireless NoC (WiNoC) Frontiers</div>
      <div class="noc-track-desc">Millimeter-wave and terahertz on-chip antennas, zig-zag transceivers, and small-world global shortcuts.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Wireless Wave mmWave Explorer
      </div>
    </div>
    <a href="04-wireless-noc-frontiers/" class="noc-track-link">Launch Lesson 10.4 →</a>
  </div>

</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track 10 using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc-lab:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
