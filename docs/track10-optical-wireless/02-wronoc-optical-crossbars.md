# Lesson 10.2: Wavelength-Routed Optical NoC (WRONoC)

<div class="noc-hero">
  <div class="noc-track-badge">Track 10 • Lesson 02</div>
  <h1>Wavelength-Division Multiplexing (WDM) &amp; Non-Blocking Optical Crossbars</h1>
  <p class="subtitle">
    Multiply interconnect bandwidth using dense WDM optical carriers, design non-blocking MRR crossbar matrices, and minimize optical insertion loss.
  </p>
</div>

---

## 1. Wavelength-Division Multiplexing (WDM)

By coupling $K$ laser wavelengths (e.g., $\lambda_1 = 1550\text{ nm}, \lambda_2 = 1550.8\text{ nm}, \dots$) onto a single shared optical waveguide, total link bandwidth scales linearly without increasing physical metal wire count:

$$
\text{Bandwidth} = K \cdot f_{\text{mod}}
$$

With $K = 64$ wavelengths modulating at $25\text{ Gb/s}$, a single waveguide carries **$1.6\text{ TB/s}$ of bi-directional data**.

---

👉 **Next: [Lesson 10.3: Laser Power-Gating & Automated Phase Control](03-laser-power-gating-apc.md)**
