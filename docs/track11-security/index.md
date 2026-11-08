# Track 11: Hardware Security & Trust in On-Chip Networks

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 11</div>
  <h1>Hardware Security & Trust in On-Chip Networks</h1>
  <p class="subtitle">Multi-tenant threat models, thermal and timing covert channels, online WMA anomaly filtering (TCAD '26 HeatSense), and Physical Unclonable Functions (PUFs).</p>
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
      <span>📚 Aligned with Chapter 11 of Official 12-Chapter Textbook</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Explore complete theoretical derivations, physical scaling parameters, and microarchitectural proofs in <strong>Chapter 11</strong>.
    </div>
  </div>
  <a href="../textbook/ch11-security/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Read Chapter 11 in Textbook →</span>
  </a>
</div>


---

## 🗺️ Architectural Learning Roadmap

The diagram below outlines how the core concepts in Track 11 connect across the physical and protocol layers:

```mermaid
graph TD
  ThreatModel['Multi-Tenant Threat Models'] --> CovertChannels['Thermal & Timing Covert Channels']
  CovertChannels --> HeatSense['Online WMA Anomaly Detection']
  HeatSense --> Quarantine['Zero-Trust Autonomous Quarantine']
```

---

## 📚 Syllabus & Lessons in Track 11

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 11.1</span>
      <div class="noc-track-title">Security Threat Models in On-Chip Networks</div>
      <div class="noc-track-desc">Multi-tenant SoCs, untrusted third-party IPs, buffer-flooding DoS, and eavesdropping taxonomy.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> NoC Hardware Security CAD Defense Arcade
      </div>
    </div>
    <a href="01-security-threat-models/" class="noc-track-link">Launch Lesson 11.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 11.2</span>
      <div class="noc-track-title">Thermal & Timing Covert Channels</div>
      <div class="noc-track-desc">Packet inter-arrival delay modulation, substrate thermal conduction leakage, and 256-bit AES exfiltration.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Timing Jitter Covert Channel Analyzer
      </div>
    </div>
    <a href="02-thermal-timing-covert-channels/" class="noc-track-link">Launch Lesson 11.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 11.3</span>
      <div class="noc-track-title">Online WMA Anomaly Detection (HeatSense)</div>
      <div class="noc-track-desc">Hardware-friendly fixed-point EWMA tracking, adaptive threshold bounds, and IEEE TCAD '26 HeatSense.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable WMA Verilog RTL
      </div>
    </div>
    <a href="03-heatsense-wma-anomaly-detection/" class="noc-track-link">Launch Lesson 11.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 11.4</span>
      <div class="noc-track-title">Hardware Trojan Defense & Zero-Trust Quarantine</div>
      <div class="noc-track-desc">Autonomous clock gating, packet deflection, and intrinsic interconnect wire-delay PUF authentication.</div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Web EDA HeatSense Verification
      </div>
    </div>
    <a href="04-trojan-defense-quarantine/" class="noc-track-link">Launch Lesson 11.4 →</a>
  </div>

</div>

---

## 💻 Web EDA Unix Workbench Quick Launch

Simulate, verify, and inspect the synthesizable SystemVerilog implementations for Track 11 using our integrated in-browser terminal:

<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; margin: 16px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: #e2e8f0;">
  <span style="color: #38bdf8; font-weight: 700;">guest@noc:~$</span> run-sim --topo mesh4x4 --algo xy --inj 0.05<br/>
  <span style="color: #64748b;">[SIM-EXEC] Progress: [========================================] 100% (Zero-load latency: 4.85 cyc)</span>
</div>

👉 **[Launch Interactive Web EDA Unix Terminal &amp; Visualizer](../interactive/terminal/)**
