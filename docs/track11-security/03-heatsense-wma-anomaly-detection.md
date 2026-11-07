# Lesson 11.3: Online WMA Anomaly Detection (HeatSense)

<div class="noc-hero">
  <div class="noc-track-badge">Track 11 • Lesson 03</div>
  <h1>Hardware-Friendly Fixed-Point EWMA &amp; Shift-and-Add Arithmetic</h1>
  <p class="subtitle">
    Reproduce the landmark IEEE TCAD 2026 HeatSense architecture, implementing real-time thermal anomaly detection in synthesizable SystemVerilog with zero multiplier overhead.
  </p>
</div>

---

## 1. The HeatSense Architecture (IEEE TCAD '26)

Grounded in IEEE TCAD 2026 (*HeatSense: Intelligent Thermal Anomaly Detection for Securing NoC-Enabled MPSoCs*):
To detect thermal Trojans without burning power on 32-bit floating-point ALUs, HeatSense tracks baseline substrate temperature using a hardware-friendly **Exponentially Weighted Moving Average (EWMA)** where $\alpha$ is constrained to powers of two:

$$
\alpha = 2^{-S}
$$

$$
\mu[n] = \mu[n-1] + (T_{\text{sensor}}[n] - \mu[n-1]) \gg S
$$

$$
\sigma[n] = \sigma[n-1] + (|T_{\text{sensor}}[n] - \mu[n-1]| - \sigma[n-1]) \gg S
$$

Threshold violation condition:
$$
|T_{\text{sensor}}[n] - \mu[n]| > K \cdot \sigma[n]
$$
Setting $K = 3$ (approx $3\text{-sigma}$) is computed via $( \sigma \ll 1 ) + \sigma$, requiring **zero hardware multipliers**!

---

## 2. Synthesizable Verilog: WMA Detector

```systemverilog
--8<-- "docs/textbook/ch11-security/code/wma_thermal_detector.sv"
```

---

👉 **Next: [Lesson 11.4: Hardware Trojan Mitigation & Zero-Trust Quarantine](04-trojan-defense-quarantine.md)**
