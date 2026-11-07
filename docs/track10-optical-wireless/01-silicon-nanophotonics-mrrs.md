# Lesson 10.1: Silicon Nanophotonics & Microring Resonators

<div class="noc-hero">
  <div class="noc-track-badge">Track 10 • Lesson 01</div>
  <h1>Optical Waveguides, Microring Resonators &amp; Light Modulation</h1>
  <p class="subtitle">
    Transport data at the speed of light in silicon using single-mode optical waveguides, resonance condition tuning, and electro-optic microring modulators.
  </p>
</div>

---

## 1. Photonic Waveguides & The Speed of Light

Silicon optical waveguides ($450\text{ nm} \times 220\text{ nm}$) exploit the high refractive index contrast between silicon ($n_{\text{Si}} \approx 3.45$) and silicon dioxide cladding ($n_{\text{SiO2}} \approx 1.45$) to achieve Total Internal Reflection (TIR). Optical propagation speed is:

$$
v_{\text{opt}} = \frac{c}{n_g} \approx \frac{3 \times 10^8\text{ m/s}}{4.0} = 7.5 \times 10^7\text{ m/s} = 75\ \mu\text{m/ps}
$$

Light traverses a $10\text{ mm}$ silicon interposer in just $133\text{ ps}$ (less than half an electrical clock cycle at $3\text{ GHz}$), with zero dynamic $CV^2f$ capacitive charging dissipation along the waveguide length!

---

## 2. Microring Resonators (MRRs)

A microring resonator consists of a circular waveguide looped adjacent to a straight bus waveguide. Constructive interference occurs at resonant wavelengths $\lambda_m$:

$$
m \cdot \lambda_m = 2 \pi R \cdot n_{\text{eff}}
$$

Applying a voltage across an embedded PN junction injects free carriers, shifting $n_{\text{eff}}$ and modulating the optical carrier to encode data bits.

---

👉 **Next: [Lesson 10.2: Wavelength-Routed Optical NoC (WRONoC) Crossbars](02-wronoc-optical-crossbars.md)**
