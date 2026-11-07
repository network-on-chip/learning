# Track 5: Deadlock Theory, Turn Models & Routing

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 05</div>
  <h1>Deadlock Theory, Turn Models & Routing</h1>
  <p class="subtitle">Deterministic DOR (XY), Glass & Ni turn model, Chiu odd-even, Duato escape channels, Channel Dependency Graphs, and VNET protocol isolation.</p>
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
      <span>📚 Aligned with Chapter 5 of Official 12-Chapter Textbook</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Explore complete theoretical derivations, physical scaling parameters, and microarchitectural proofs in <strong>Chapter 5</strong>.
    </div>
  </div>
  <a href="../textbook/ch05-routing-deadlock-theory/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Read Chapter 5 in Textbook →</span>
  </a>
</div>


---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track 5 connect across the physical and protocol layers:

```mermaid
graph TD
  DOR['Dimension-Order XY'] --> TurnModels['Turn Models (Odd-Even)']
  TurnModels --> Duato['Duato Escape Channels']
  Duato --> FaultTolerant['Fault-Tolerant VNETs']
```

---

## 📚 Syllabus & Lessons in Track 5

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 5.1</span>
      <div class="noc-track-title">Deterministic Dimension-Order Routing (DOR)</div>
      <div class="noc-track-desc">Proof of deadlock freedom for XY routing in 2D meshes via monotonic coordinate order.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Dimension-Order Routing Visualizer
      </div>
    </div>
    <a href="01-deterministic-dor/" class="noc-track-link">Launch Lesson 5.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 5.2</span>
      <div class="noc-track-title">Turn Models: West-First, North-Last & Odd-Even</div>
      <div class="noc-track-desc">Prohibiting specific turns to break cycles in CDG without sacrificing connectivity.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Adaptive Turn Model Explorer
      </div>
    </div>
    <a href="02-adaptive-turn-model/" class="noc-track-link">Launch Lesson 5.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 5.3</span>
      <div class="noc-track-title">Channel Dependency Graphs & Duato's Theorem</div>
      <div class="noc-track-desc">Formal CDG cycle-free condition and escaping deadlock using a minimal set of escape VCs.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> SMT CDG Cycle Verifier & RTL
      </div>
    </div>
    <a href="03-deadlock-theory-cdg/" class="noc-track-link">Launch Lesson 5.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 5.4</span>
      <div class="noc-track-title">Fault-Tolerant Routing & Protocol Deadlocks</div>
      <div class="noc-track-desc">Handling link/router faults with Up*/Down* routing, and resolving request-reply protocol deadlocks.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Deadlock Buster Arcade Game
      </div>
    </div>
    <a href="04-fault-tolerant-protocol-deadlock/" class="noc-track-link">Launch Lesson 5.4 →</a>
  </div>

</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track 5 using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
