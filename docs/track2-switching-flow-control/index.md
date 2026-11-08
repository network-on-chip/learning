# Track 2: Switching, Flow Control & Buffers

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 02</div>
  <h1>Switching, Flow Control & Buffers</h1>
  <p class="subtitle">Wormhole vs VCT switching, flits/phits, credit turnaround latency loops, Virtual Channel buffers, and AXI4/TileLink NI packetization.</p>
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
      <span>📚 Aligned with Chapter 2 of Official 12-Chapter Textbook</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Explore complete theoretical derivations, physical scaling parameters, and microarchitectural proofs in <strong>Chapter 2</strong>.
    </div>
  </div>
  <a href="../textbook/ch02-switching-flow-control/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Read Chapter 2 in Textbook →</span>
  </a>
</div>


---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track 2 connect across the physical and protocol layers:

```mermaid
graph TD
  Data['Messages & Packets'] --> Flits['Flits & Phits']
  Flits --> Switching['Wormhole Switching']
  Switching --> Credits['Credit Loop Flow Control']
```

---

## 📚 Syllabus & Lessons in Track 2

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 2.1</span>
      <div class="noc-track-title">Packets, Flits & Phits</div>
      <div class="noc-track-desc">Hierarchy of data transmission: Messages, Packets, Flits, and physical wire Phits.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Flit Packetization Simulator
      </div>
    </div>
    <a href="01-packet-switching-flits/" class="noc-track-link">Launch Lesson 2.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 2.2</span>
      <div class="noc-track-title">Switching Mechanisms: SAF, VCT & Wormhole</div>
      <div class="noc-track-desc">Deep dive into Store-and-Forward, Virtual Cut-Through, and Wormhole buffer allocation.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Zero-Load Latency Equation Explorer
      </div>
    </div>
    <a href="02-switching-mechanisms/" class="noc-track-link">Launch Lesson 2.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 2.3</span>
      <div class="noc-track-title">Flow Control & Credit Turnaround Loops</div>
      <div class="noc-track-desc">Lossless backpressure, credit turnaround latency loops, and minimum buffer sizing B_min >= RTT.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Credit Flow Control CAD Flow Control Simulator
      </div>
    </div>
    <a href="03-flow-control-credit/" class="noc-track-link">Launch Lesson 2.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 2.4</span>
      <div class="noc-track-title">Network Interfaces & AXI Packetization</div>
      <div class="noc-track-desc">Translating CPU memory requests (AXI4/TileLink) into on-chip flit streams.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable NI Verilog RTL
      </div>
    </div>
    <a href="04-network-interface-packetization/" class="noc-track-link">Launch Lesson 2.4 →</a>
  </div>

</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track 2 using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
