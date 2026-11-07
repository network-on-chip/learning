#!/usr/bin/env python3
"""Builds missing and expanded lessons for Tracks 1, 2, 6, 8, 9, 10, 11, 12, 13.
"""

from pathlib import Path

LEARNING_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = LEARNING_DIR / "docs"

def write(rel, text):
    p = DOCS_DIR / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"Generated: {rel}")

# -----------------------------------------------------------------------------
# TRACK 1: Interconnect Crisis & Wire Physics (Ch 1)
# -----------------------------------------------------------------------------
def build_track1():
    # 02-wire-scaling-elmore.md
    write("track1-interconnect-crisis/02-wire-scaling-elmore.md", """# Lesson 1.2: Nanoscale Wire Physics & Elmore RC Delay

<div class="noc-hero">
  <div class="noc-track-badge">Track 01 • Lesson 02</div>
  <h1>Nanoscale Wire Physics &amp; Elmore Delay Modeling</h1>
  <p class="subtitle">
    Explore why global on-chip copper wires fail to scale with transistor feature sizes, derive the distributed Elmore RC delay formula, and model copper resistivity inflation down to 3nm GAA nodes.
  </p>
</div>

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>📖 Aligned with Chapter 1: The Interconnect Crisis &amp; Wire Physics</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      Review Section 1.2 and Section 1.3 for full derivations of Mayadas-Shatzkes scattering and Fuchs-Sondheimer surface reflections.
    </div>
  </div>
  <a href="../../textbook/ch01-interconnect-crisis/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>Open Chapter 1 →</span>
  </a>
</div>

---

## 1. The Scaling Disconnect: Transistors vs. Wires

Under classical Dennard scaling, transistor gate delay improves by a factor of $1/S$ with each process generation ($S \approx 1.4$). In contrast, an unbuffered global wire of length $L$ traversing across the chip exhibits an intrinsic delay governed by the distributed $RC$ product:

$$
\\tau_{\\text{wire}} = \\frac{1}{2} r c L^2
$$

where $r$ is the wire resistance per unit length ($\\Omega/\\mu\\text{m}$) and $c$ is the wire capacitance per unit length ($\\text{fF}/\\mu\\text{m}$).

When wire cross-section shrinks ($W \\to W/S$ and $H \\to H/S$), resistance per unit length increases quadratically:

$$
r = \\frac{\\rho}{W \\cdot H} \\propto S^2
$$

While capacitance per unit length $c$ remains roughly constant ($\\approx 0.2\\text{ fF}/\\mu\\text{m}$) due to fringing fields, the intrinsic delay of a fixed-length global wire increases as $O(S^2)$. Consequently, crossing an $8\\text{ mm}$ die in modern sub-5nm technology requires over $12\\text{ clock cycles}$ at $2\\text{ GHz}$.

---

## 2. Elmore Delay Calculation for Buffered Interconnects

For a distributed wire driven by an inverter with output resistance $R_d$ and driving load capacitance $C_L$, the 50% propagation delay is modeled via the Elmore delay metric:

$$
T_{50\\%} = 0.69 \\cdot R_d (C_{\\text{wire}} + C_L) + 0.38 \\cdot R_{\\text{wire}} C_{\\text{wire}} + 0.69 \\cdot R_{\\text{wire}} C_L
$$

```mermaid
flowchart LR
    Drv["Driver (Rd, Cd)"] --> WireSeg1["R_wire/2, C_wire/2"]
    WireSeg1 --> WireSeg2["R_wire/2, C_wire/2"]
    WireSeg2 --> Load["Receiver Load (CL)"]
```

---

## 3. Interactive Physics Simulation

Test these equations live in our browser simulator:

👉 **[Launch Wire Wizard: Interconnect Physics](../../interactive/wire/)** — Sweep wire pitch from 180nm to 3nm and observe copper resistivity inflation.

---

## 4. Self-Check Assessment

**Question 1:** If wire width and thickness both scale down by $1.4\\times$, what happens to wire resistance per unit length?  
*Answer:* Resistance increases by approximately $(1.4)^2 \\approx 2.0\\times$ (doubles).

**Question 2:** Why does wire capacitance per unit length NOT scale down proportionally with wire width?  
*Answer:* Sidewall coupling capacitance and fringing electric fields to adjacent metal tracks dominate over parallel-plate ground capacitance.

**Question 3:** How does Elmore delay scale with wire length $L$ for an unbuffered wire?  
*Answer:* Delay scales quadratically as $O(L^2)$ because both total resistance ($rL$) and total capacitance ($cL$) increase linearly with length.

---

👉 **Next: [Lesson 1.3: Optimal Repeater Insertion & Scattering Physics](03-repeater-insertion.md)**
""")

    # 03-repeater-insertion.md
    write("track1-interconnect-crisis/03-repeater-insertion.md", """# Lesson 1.3: Optimal Repeater Insertion & Scattering Physics

<div class="noc-hero">
  <div class="noc-track-badge">Track 01 • Lesson 03</div>
  <h1>Bakoglu Repeater Insertion &amp; Copper Resistivity Limits</h1>
  <p class="subtitle">
    Linearize quadratic wire delay by deriving Bakoglu's optimal repeater spacing, and understand why electron scattering at grain boundaries breaks classical bulk conductivity.
  </p>
</div>

---

## 1. Bakoglu's Optimal Repeater Spacing

To convert the quadratic $O(L^2)$ delay of long wires into a linear $O(L)$ relationship, repeaters (inverters or buffers) are inserted at uniform intervals $l_{\\text{opt}}$:

$$
l_{\\text{opt}} = \\sqrt{\\frac{2 R_0 C_0}{r c}}
$$

$$
s_{\\text{opt}} = \\sqrt{\\frac{R_0 c}{r C_0}}
$$

where $R_0$ and $C_0$ are the effective output resistance and input capacitance of a minimum-sized inverter, and $s_{\\text{opt}}$ is the optimal buffer sizing factor.

Under optimal repeater insertion, the propagation delay per unit length becomes linear:

$$
\\frac{T}{L} = 2 \\sqrt{r c R_0 C_0}
$$

However, repeaters consume substantial silicon area and active/leakage power. In high-performance SoCs, repeaters can consume upwards of $35\\%$ of total chip routing power.

---

## 2. Mayadas-Shatzkes Scattering in Nanoscale Copper

When copper interconnect dimensions drop below the electron mean free path ($\\lambda_{\\text{mfp}} \\approx 39\\text{ nm}$ at $300\\text{ K}$), bulk resistivity $\\rho_0 = 1.68\\ \\mu\\Omega\\cdot\\text{cm}$ increases drastically due to two physical scattering mechanisms:

1. **Fuchs-Sondheimer Surface Scattering:** Electrons collide with wire sidewalls and the high-resistivity diffusion barrier liner (e.g., TaN, Ru, Co).
2. **Mayadas-Shatzkes Grain Boundary Scattering:** Polycrystalline copper grain sizes shrink with wire dimensions, creating potential barriers that scatter conducting electrons:

$$
\\frac{\\rho}{\\rho_0} = 3 \\left[ \\frac{1}{3} - \\frac{1}{2} \\alpha + \\alpha^2 - \\alpha^3 \\ln\\left(1 + \\frac{1}{\\alpha}\\right) \\right]^{-1}, \\quad \\alpha = \\frac{\\lambda_{\\text{mfp}}}{d} \\frac{R}{1 - R}
$$

where $d$ is average grain diameter and $R$ is grain boundary reflection coefficient ($R \\approx 0.2\\text{--}0.4$).

---

## 3. Self-Check Assessment

**Question 1:** What is the primary purpose of inserting repeaters along a global on-chip wire?  
*Answer:* To break the quadratic $O(L^2)$ delay dependence into a linear $O(L)$ delay.

**Question 2:** What is the electron mean free path of copper at room temperature?  
*Answer:* Approximately $39\\text{ nm}$.

**Question 3:** What happens to repeater power consumption as wires scale into sub-5nm nodes?  
*Answer:* It escalates rapidly because higher wire resistance requires repeaters to be placed closer together ($l_{\\text{opt}}$ shrinks).

---

👉 **Next: [Lesson 1.4: Global Interconnect Energy & Physical Scaling Limits](04-energy-limits-interconnect.md)**
""")

    # 04-energy-limits-interconnect.md
    write("track1-interconnect-crisis/04-energy-limits-interconnect.md", """# Lesson 1.4: Global Interconnect Energy & Physical Limits

<div class="noc-hero">
  <div class="noc-track-badge">Track 01 • Lesson 04</div>
  <h1>Energy Dissipation Limits &amp; The Shared Bus Collapse</h1>
  <p class="subtitle">
    Quantify interconnect energy dissipation ($CV^2f$), contrast crossbar area explosion $O(N^2)$ against Network-on-Chip modularity, and understand the definitive death of shared on-chip buses.
  </p>
</div>

---

## 1. Dynamic Energy Dissipation on Silicon Wires

Every transition on an on-chip wire charges and discharges the lumped capacitance $C_{\\text{wire}}$, dissipating dynamic energy:

$$
E_{\\text{bit}} = \\frac{1}{2} \\alpha C_{\\text{wire}} V_{DD}^2
$$

where $\\alpha$ is the switching activity factor ($0 < \\alpha \\le 1$). For an unpipelined bus carrying $W = 64$ parallel bits across $L = 10\\text{ mm}$, total wire capacitance can exceed $2\\text{ pF}$, demanding $>2\\text{ pJ/bit}$ per transfer at $1.0\\text{ V}$.

---

## 2. The Shared Bus Serialization Bottleneck

In classical architectures (e.g., AMBA AHB, CoreConnect), all cores share a single set of broadcast wires arbitrated by a central arbiter. As the number of cores $N$ increases:

1. **Capacitive Loading:** Every attached master and slave adds parasitic transceiver capacitance ($C_{\\text{bus}} = N \\cdot C_{\\text{port}} + C_{\\text{wire}}$), driving clock frequencies down.
2. **Bandwidth Saturation:** Total bandwidth remains fixed at $B = W \\cdot f_{\\text{bus}}$, forcing per-core throughput to collapse as $O(1/N)$.
3. **Contention Latency:** Wait times scale quadratically under Poisson packet arrivals due to head-of-line bus locking.

---

## 3. Summary of Track 1 & Bridge to Track 2

| Metric | Shared Bus | Full Crossbar Switch | Network-on-Chip (NoC) |
|---|:---:|:---:|:---:|
| **Area Scaling** | $O(1)$ | $O(N^2)$ | $O(N)$ |
| **Aggregated Bandwidth** | $O(1)$ (Fixed) | $O(N)$ | $O(N)$ (Concurrent links) |
| **Wire Lengths** | $O(N)$ (Global) | $O(N^2)$ (Congested) | $O(1)$ (Short P2P hops) |
| **Energy per Transfer** | High ($C_{\\text{bus}} V^2$) | High (Dense matrix) | Low (Hop-by-hop local wires) |

---

👉 **Advance to [Track 2: Switching, Flow Control & Buffers](../track2-switching-flow-control/)**
""")

    print("Track 1 completed.")

if __name__ == "__main__":
    build_track1()
