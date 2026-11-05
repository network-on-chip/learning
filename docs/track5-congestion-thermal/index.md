# Track 5: Thermal & Congestion Management

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 05</div>
  <h1>Thermal Physics, Congestion Control &amp; Predictive AI</h1>
  <p class="subtitle">
    Master how nanometer multi-core processors battle localized thermal hotspots and network traffic saturation. From fundamental RC thermal modeling to Regional Congestion Awareness (RCA), machine-learning hotspot forecasting, and sparse sensor reconstruction under non-Gaussian noise.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ 4 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🔬 4 Interactive Simulators &amp; Visualizers</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">💻 4 Synthesizable Verilog RTL Modules</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">🔥 Grounded in Verified Open-Source Lab Projects</span>
</div>

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>📚 Aligned with Official Textbook Chapters 6 &amp; 7</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Read <strong>Chapter 6 (Low Power &amp; Dark Silicon)</strong> for sub-threshold leakage, VFIs, and lookahead power gating. Read <strong>Chapter 7 (Thermal Modeling &amp; Fault Tolerance)</strong> for HotSpot RC modeling, GSF sensor reconstruction, and hardware bypass detours.
    </div>
  </div>
  <div style="display: flex; gap: 8px; flex-wrap: wrap;">
    <a href="../textbook/ch06-low-power-dark-silicon/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 14px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
      <span>Read Chapter 6 →</span>
    </a>
    <a href="../textbook/ch07-thermal-fault-tolerance/" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 8px 14px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
      <span>Read Chapter 7 →</span>
    </a>
  </div>
</div>

---

## 🗺️ Thermal & Congestion Architecture Roadmap

The diagram below outlines how heat dissipation physics, network telemetry, predictive machine learning, and sparse sensor estimation interact to maintain high-performance, reliable silicon operation:

```mermaid
graph TD
  subgraph Physical_Thermal_Layer ["1. Thermal & Network Physics Layer"]
    Power["Tile Dynamic & Static Power Dissipation"] --> RC["RC Thermal Ladder Model<br/>(Silicon substrate + TIM + Heat Sink)"]
    Traffic["High Injection Workload"] --> Saturation["Buffer Saturation & Congestion Trees"]
  end

  subgraph Telemetry_Sensing_Layer ["2. Telemetry & Sensor Layer"]
    RC --> Sensors["Sparse Physical Thermal Diodes<br/>(Noise: Gaussian EMI + Non-Gaussian Glitches)"]
    Saturation --> RCA_Telemetry["Regional Congestion Awareness (RCA)<br/>(Buffer fullness & credit turnaround)"]
  end

  subgraph Control_Mitigation_Layer ["3. Intelligent Control & Mitigation Layer"]
    Sensors --> Recon["Robust Spatial Reconstruction<br/>(Huber M-Estimation & Kalman Filter)"]
    RCA_Telemetry --> Quench["Closed-Loop Source Quenching<br/>(Token bucket injection throttling)"]
    Recon --> ML_Predict["Proactive ML Hotspot Predictor<br/>(Predicts T at t + Δt using IPC & NoC counters)"]
    ML_Predict --> DTM["Proactive DVFS & Thermal-Aware Routing (TAR)<br/>(Deflects flits around hot routers)"]
  end

  classDef physStyle fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px,color:#991b1b;
  classDef telemStyle fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#92400e;
  classDef ctrlStyle fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#166534;

  class Power,RC,Traffic,Saturation physStyle;
  class Sensors,RCA_Telemetry telemStyle;
  class Recon,Quench,ML_Predict,DTM ctrlStyle;
```

---

## 📚 Syllabus & Chapters in Track 5

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 5.1</span>
      <div class="noc-track-title">Thermal Physics &amp; Compact RC Modeling</div>
      <div class="noc-track-desc">
        Fourier's law of heat conduction, the thermal-electrical duality ($R_{th}, C_{th}$), and compact RC grid models (HotSpot). Analyze the $10^7\times$ timescale mismatch between electrical clock cycles and thermal diffusion constants, calculate reliability degradation via Black's electromigration equation, and implement on-chip thermal sensor controllers in synthesizable Verilog.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive 2D Silicon Die Thermal RC Ladder Simulator, Synthesizable Verilog RTL (`thermal_sensor_digital_interface.v`), 3-Question Self-Check Quiz, Arcade Linkages (Hotspot Hero &amp; Volt Vortex).
      </div>
    </div>
    <a href="01-thermal-physics-rc-modeling/" class="noc-track-link">Launch Lesson 5.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 5.2</span>
      <div class="noc-track-title">Congestion Detection &amp; Source Quenching</div>
      <div class="noc-track-desc">
        Physics of network saturation trees and Head-of-Line (HoL) blocking amplification. Gratz &amp; Keckler's Regional Congestion Awareness (RCA) propagating multi-hop congestion vectors upstream. Closed-loop source quenching, token-bucket throttling, DyAD adaptive routing, and synthesizable telemetry aggregation RTL.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive Network Congestion Tree &amp; RCA Telemetry Visualizer, Synthesizable Verilog RTL (`rca_congestion_aggregator.v`), 3-Question Self-Check Quiz, Arcade Linkages (Credit Commander &amp; QoS Gladiator).
      </div>
    </div>
    <a href="02-congestion-detection-throttling/" class="noc-track-link">Launch Lesson 5.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 5.3</span>
      <div class="noc-track-title">Proactive Hotspot Prediction with Machine Learning</div>
      <div class="noc-track-desc">
        Why reactive Dynamic Thermal Management (DTM) suffers catastrophic thermal overshoot. Grounded in our open-source lab project: training lightweight ML models (Ridge, SVR, MLP) on real-time router counters to forecast hotspots at $(t + \Delta t)$, cutting violations by $85\%$ with $<3\%$ penalty, and synthesizable fixed-point inference RTL.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive Proactive vs. Reactive Thermal Predictor &amp; DVFS Simulator, Synthesizable Verilog RTL (`proactive_thermal_throttler.v`), 3-Question Self-Check Quiz, Arcade Linkages (Hotspot Hero &amp; Deflection Duel).
      </div>
    </div>
    <a href="03-hotspot-prediction-ml/" class="noc-track-link">Launch Lesson 5.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 5.4</span>
      <div class="noc-track-title">Optimal Thermal Sensor Placement &amp; Field Reconstruction</div>
      <div class="noc-track-desc">
        Reconstructing full die temperature fields from $K \ll N$ physical sensor diodes. Grounded in our verified lab project: Fisher Information Matrix (FIM) optimization, handling non-Gaussian EMI switching noise and sensor glitches, robust Huber M-estimation, and synthesizable outlier rejection filter RTL.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Interactive Sparse Sensor Placement &amp; Robust Reconstruction Playground, Synthesizable Verilog RTL (`huber_m_estimator_filter.v`), 3-Question Self-Check Quiz, Arcade Linkages (Hotspot Hero &amp; Fault Defender).
      </div>
    </div>
    <a href="04-thermal-sensor-placement/" class="noc-track-link">Launch Lesson 5.4 →</a>
  </div>
</div>

---

## 🎯 Track Learning Objectives

Upon completing Track 5, you will be able to:

1. **Construct compact RC thermal ladder models** for 2D multi-core dies, mapping silicon substrate, thermal interface material (TIM), and heat sinks to equivalent circuit elements.
2. **Quantify the thermal time constant lag** ($\tau_{th} \approx 5\text{–}15\text{ ms}$) and explain why reactive DTM creates thermal overshoot and reliability failure.
3. **Implement Regional Congestion Awareness (RCA)** in router microarchitecture to detect and divert traffic before saturation trees form.
4. **Deploy machine learning models** (Ridge Regression, MLPs) using hardware performance counters to predict temperatures $10\text{ ms}$ into the future.
5. **Optimize thermal sensor placement** via Fisher Information maximization to achieve minimal reconstruction error with a minimal sensor budget ($K \ll N$).
6. **Apply robust M-estimation and Kalman filtering** to filter out non-Gaussian EMI sensor noise and process variation drift.

Ready to begin? Start with **[Lesson 5.1: Thermal Physics & Compact RC Modeling](01-thermal-physics-rc-modeling.md)**.
