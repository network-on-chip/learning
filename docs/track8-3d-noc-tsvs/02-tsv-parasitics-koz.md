# Lesson 8.2: TSV Parasitics & Keep-Out Zones (KOZ)

<div class="noc-hero">
  <div class="noc-track-badge">Track 08 • Lesson 02</div>
  <h1>Through-Silicon Via (TSV) Parasitic Modeling &amp; Thermal Stress</h1>
  <p class="subtitle">
    Model copper-to-silicon thermal expansion mismatch, extract high-frequency TSV parasitic resistance and capacitance, and design keep-out zones to protect CMOS channel mobility.
  </p>
</div>

---

## 1. Electrical Modeling of TSVs

Through-Silicon Vias (TSVs) provide vertical interconnects across thinned silicon dies ($30\text{--}50\ \mu\text{m}$ thickness). A cylindrical TSV of diameter $D$ and height $H$ with dielectric liner thickness $t_{\text{ox}}$ is modeled as a lumped $RLC$ circuit:

$$
R_{\text{tsv}} = \frac{4 \rho_{\text{Cu}} H}{\pi D^2}
$$

$$
C_{\text{tsv}} = \frac{2 \pi \epsilon_{\text{ox}} H}{\ln\left(1 + \frac{2 t_{\text{ox}}}{D}\right)}
$$

For typical dimensions ($D = 5\ \mu\text{m}, H = 40\ \mu\text{m}, t_{\text{ox}} = 200\text{ nm}$), a TSV exhibits $R_{\text{tsv}} \approx 35\text{ m}\Omega$ and $C_{\text{tsv}} \approx 45\text{ fF}$.

---

## 2. Thermo-Mechanical Stress & Keep-Out Zones (KOZ)

Copper has a coefficient of thermal expansion ($	ext{CTE} \approx 17\text{ ppm/K}$) significantly higher than silicon ($	ext{CTE} \approx 2.6\text{ ppm/K}$). Thermal cycling during manufacturing induces severe residual shear stress in the surrounding silicon lattice:

* **Piezoresistive Effect:** Compressive and tensile stresses alter silicon band structure, shifting PMOS and NMOS threshold voltages by up to $15\%$ and degrading mobility.
* **Keep-Out Zone (KOZ):** Active transistors must be excluded from a circular region around the TSV (typically $R_{\text{KOZ}} = 3\text{--}5\times D$) to prevent timing skew and circuit variability.

---

👉 **Next: [Lesson 8.3: 7-Port 3D Router Microarchitectures](03-3d-router-microarchitecture.md)**
