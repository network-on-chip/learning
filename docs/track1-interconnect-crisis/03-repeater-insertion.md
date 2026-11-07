# Lesson 1.3: Optimal Repeater Insertion & Scattering Physics

<div class="noc-hero">
  <div class="noc-track-badge">Track 01 • Lesson 03</div>
  <h1>Bakoglu Repeater Insertion &amp; Copper Resistivity Limits</h1>
  <p class="subtitle">
    Linearize quadratic wire delay by deriving Bakoglu's optimal repeater spacing, and understand why electron scattering at grain boundaries breaks classical bulk conductivity.
  </p>
</div>

---

## 1. Bakoglu's Optimal Repeater Spacing

To convert the quadratic $O(L^2)$ delay of long wires into a linear $O(L)$ relationship, repeaters (inverters or buffers) are inserted at uniform intervals $l_{\text{opt}}$:

$$
l_{\text{opt}} = \sqrt{\frac{2 R_0 C_0}{r c}}
$$

$$
s_{\text{opt}} = \sqrt{\frac{R_0 c}{r C_0}}
$$

where $R_0$ and $C_0$ are the effective output resistance and input capacitance of a minimum-sized inverter, and $s_{\text{opt}}$ is the optimal buffer sizing factor.

Under optimal repeater insertion, the propagation delay per unit length becomes linear:

$$
\frac{T}{L} = 2 \sqrt{r c R_0 C_0}
$$

However, repeaters consume substantial silicon area and active/leakage power. In high-performance SoCs, repeaters can consume upwards of $35\%$ of total chip routing power.

---

## 2. Mayadas-Shatzkes Scattering in Nanoscale Copper

When copper interconnect dimensions drop below the electron mean free path ($\lambda_{\text{mfp}} \approx 39\text{ nm}$ at $300\text{ K}$), bulk resistivity $\rho_0 = 1.68\ \mu\Omega\cdot\text{cm}$ increases drastically due to two physical scattering mechanisms:

1. **Fuchs-Sondheimer Surface Scattering:** Electrons collide with wire sidewalls and the high-resistivity diffusion barrier liner (e.g., TaN, Ru, Co).
2. **Mayadas-Shatzkes Grain Boundary Scattering:** Polycrystalline copper grain sizes shrink with wire dimensions, creating potential barriers that scatter conducting electrons:

$$
\frac{\rho}{\rho_0} = 3 \left[ \frac{1}{3} - \frac{1}{2} \alpha + \alpha^2 - \alpha^3 \ln\left(1 + \frac{1}{\alpha}\right) \right]^{-1}, \quad \alpha = \frac{\lambda_{\text{mfp}}}{d} \frac{R}{1 - R}
$$

where $d$ is average grain diameter and $R$ is grain boundary reflection coefficient ($R \approx 0.2\text{--}0.4$).

---

## 3. Self-Check Assessment

**Question 1:** What is the primary purpose of inserting repeaters along a global on-chip wire?  
*Answer:* To break the quadratic $O(L^2)$ delay dependence into a linear $O(L)$ delay.

**Question 2:** What is the electron mean free path of copper at room temperature?  
*Answer:* Approximately $39\text{ nm}$.

**Question 3:** What happens to repeater power consumption as wires scale into sub-5nm nodes?  
*Answer:* It escalates rapidly because higher wire resistance requires repeaters to be placed closer together ($l_{\text{opt}}$ shrinks).

---

👉 **Next: [Lesson 1.4: Global Interconnect Energy & Physical Scaling Limits](04-energy-limits-interconnect.md)**
