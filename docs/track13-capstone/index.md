# Track 13: Capstone: Landmark Silicon Case Studies & System Synthesis

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 13</div>
  <h1>Capstone: Landmark Silicon Case Studies & System Synthesis</h1>
  <p class="subtitle">Seminal taped-out silicon case studies (Intel SCC 48-Core, NVIDIA Simba 36-Die MCM, 3D Optical NoC) and the Grand Synthesis MoE Accelerator Challenge.</p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ 5 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🔬 Interactive Simulators &amp; Tools</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">💻 Synthesizable Verilog RTL</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">📜 Grounded in Official Monograph</span>
  </div>
</div>


<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>🏆 Capstone System Synthesis: Grounded in Chapters 1–12</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Synthesize wire physics (Ch 1–3), topologies & deadlock (Ch 4–5), thermal/power defense (Ch 6–7), 3D & chiplets (Ch 8–9), and emerging frontiers (Ch 10–12).
    </div>
  </div>
  <a href="../textbook/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Explore Official 12-Chapter Textbook →</span>
  </a>
</div>


---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track 13 connect across the physical and protocol layers:

```mermaid
graph TD
  SCC['Intel 48-Core SCC'] --> Simba['NVIDIA Simba 36-Chiplet MCM']
  Simba --> Optical3D['3D Optical & In-Network Computing']
  Optical3D --> CapstoneMoE['Grand Synthesis: Zero-Trust MoE Accelerator Top']
```

---

## 📚 Syllabus & Lessons in Track 13

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 13.1</span>
      <div class="noc-track-title">The Manycore Milestone: Intel 48-Core SCC</div>
      <div class="noc-track-desc">Intel Labs 45nm tapeout, message-passing buffers (MPB), 2-TB/s mesh, and Wrapped Wave-Front Allocation.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Intel SCC Mesh Simulator & RTL
      </div>
    </div>
    <a href="01-intel-scc-mesh/" class="noc-track-link">Launch Lesson 13.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 13.2</span>
      <div class="noc-track-title">The Multi-Chiplet Revolution: NVIDIA Simba</div>
      <div class="noc-track-desc">36-chiplet 2.5D MCM deep learning accelerator, 0.54 pJ/bit Ground-Referenced Signaling (GRS), and multicast.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Simba MCM Explorer & Multicast RTL
      </div>
    </div>
    <a href="02-nvidia-simba-mcm/" class="noc-track-link">Launch Lesson 13.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 13.3</span>
      <div class="noc-track-title">3D Optical NoC for MPSoCs</div>
      <div class="noc-track-desc">Reduced-MRR non-blocking crossbars, Automated Phase Control (APC), and hybrid 3D integration.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> 3D Optical Crossbar Simulator
      </div>
    </div>
    <a href="03-3d-optical-noc/" class="noc-track-link">Launch Lesson 13.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 13.4</span>
      <div class="noc-track-title">In-Network Computing Neuromorphic Router</div>
      <div class="noc-track-desc">Silicon-verified partial-sum in-flight reduction delivering 1.63 pJ/SOP for bio-inspired neuromorphic chips.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Neuromorphic INC Crossbar RTL
      </div>
    </div>
    <a href="04-in-network-neuromorphic/" class="noc-track-link">Launch Lesson 13.4 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 13.5</span>
      <div class="noc-track-title">Capstone Challenge: Zero-Trust MoE Accelerator</div>
      <div class="noc-track-desc">The Grand Synthesis: 16-chiplet active interposer fabric, All-Reduce collective tree, WMA Trojan defense, and STA.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Web EDA Automated Capstone Grading
      </div>
    </div>
    <a href="05-grand-synthesis-moe/" class="noc-track-link">Launch Lesson 13.5 →</a>
  </div>

</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track 13 using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc-lab:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
