# Lesson 10.3: Laser Power-Gating & Thermal Drift Compensation

<div class="noc-hero">
  <div class="noc-track-badge">Track 10 • Lesson 03</div>
  <h1>Off-Chip Laser Efficiency, Thermal Ring Drift &amp; Automated Phase Control</h1>
  <p class="subtitle">
    Overcome the thermal sensitivity of microring resonators ($\sim 0.1	ext{ nm/K}$), and evaluate laser power-gating techniques to maintain high wall-plug efficiency.
  </p>
</div>

---

## 1. Thermal Drift in Silicon Microrings

Silicon exhibits a high thermo-optic coefficient ($dn/dT \approx 1.86 \times 10^{-4}\text{ K}^{-1}$). As neighboring processor cores heat up and cool down ($40^\circ\text{C} \to 90^\circ\text{C}$), the resonant wavelength of MRRs drifts:

$$
\frac{d\lambda}{dT} = \frac{\lambda}{n_g} \frac{dn_{\text{eff}}}{dT} \approx 0.10\text{ nm/K}
$$

A temperature rise of just $8^\circ\text{C}$ shifts the resonance completely off the laser carrier wavelength, causing optical signal blackout. Mitigation requires integrated micro-heaters driven by **Automated Phase Control (APC)** closed-loop feedback circuits.

---

👉 **Next: [Lesson 10.4: On-Chip Wireless NoC (WiNoC) Frontiers](04-wireless-noc-frontiers.md)**
