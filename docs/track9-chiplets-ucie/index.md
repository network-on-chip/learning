# Track 9: Multi-Chiplet Interconnects & UCIe

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 09</div>
  <h1>Multi-Chiplet Interconnects & UCIe</h1>
  <p class="subtitle">2.5D packaging (CoWoS, EMIB), negative binomial yield economics, UCIe 1.0/2.0 standard, In/Outbound swap deadlock recovery, and BuffeRS bypassing.</p>
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
      <span>📚 Aligned with Chapter 9 of Official 12-Chapter Textbook</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Explore complete theoretical derivations, physical scaling parameters, and microarchitectural proofs in <strong>Chapter 9</strong>.
    </div>
  </div>
  <a href="../textbook/ch09-chiplets-ucie/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Read Chapter 9 in Textbook →</span>
  </a>
</div>


---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track 9 connect across the physical and protocol layers:

```mermaid
graph TD
  YieldEconomics['Negative Binomial Yield'] --> UCIeStack['UCIe 1.0/2.0 D2D Standard']
  UCIeStack --> BoundaryDeadlock['Cross-Die Deadlock Recovery']
  BoundaryDeadlock --> BuffeRS['BuffeRS Wire-Speed Bypassing']
```

---

## 📚 Syllabus & Lessons in Track 9

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 9.1</span>
      <div class="noc-track-title">2.5D Packaging Economics & Reticle Limits</div>
      <div class="noc-track-desc">Disaggregation economics, negative binomial yield models, CoWoS silicon interposers, and EMIB bridges.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Chiplet Tycoon Advanced Packaging
      </div>
    </div>
    <a href="01-25d-packaging-economics/" class="noc-track-link">Launch Lesson 9.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 9.2</span>
      <div class="noc-track-title">UCIe Protocol Stack & D2D Physical Layer</div>
      <div class="noc-track-desc">Universal Chiplet Interconnect Express (UCIe) standard, D2D physical adapter, and die-to-die streaming protocols.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> UCIe Protocol Frame Inspector
      </div>
    </div>
    <a href="02-chiplets-ucie-interconnects/" class="noc-track-link">Launch Lesson 9.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 9.3</span>
      <div class="noc-track-title">Cross-Die Boundary Deadlock Recovery</div>
      <div class="noc-track-desc">Boundary interface deadlocks, cyclic subpath proofs, and TCAD '26 In/Outbound backtracking swap.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> In/Outbound Swap Deadlock Solver
      </div>
    </div>
    <a href="03-cross-die-deadlock-recovery/" class="noc-track-link">Launch Lesson 9.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 9.4</span>
      <div class="noc-track-title">Multi-Chiplet Router Bypassing & BuffeRS</div>
      <div class="noc-track-desc">Near wire-speed inter-die transit, TCAD '26 BuffeRS scheduling, and dynamic vertical link selection.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Web EDA BuffeRS Evaluator
      </div>
    </div>
    <a href="04-multichiplet-router-bypassing/" class="noc-track-link">Launch Lesson 9.4 →</a>
  </div>

</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track 9 using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc-lab:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
