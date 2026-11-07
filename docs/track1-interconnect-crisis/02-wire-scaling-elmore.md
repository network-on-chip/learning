# Lesson 1.2: Nanoscale Wire Physics & Elmore RC Delay

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

Under classical Dennard scaling, transistor gate delay improves by a factor of $1/S$ with each process generation ($S pprox 1.4$). In contrast, an unbuffered global wire of length $L$ traversing across the chip exhibits an intrinsic delay governed by the distributed $RC$ product:

$$
\tau_{\text{wire}} = \frac{1}{2} r c L^2
$$

where $r$ is the wire resistance per unit length ($\Omega/\mu\text{m}$) and $c$ is the wire capacitance per unit length ($\text{fF}/\mu\text{m}$).

When wire cross-section shrinks ($W \to W/S$ and $H \to H/S$), resistance per unit length increases quadratically:

$$
r = \frac{\rho}{W \cdot H} \propto S^2
$$

While capacitance per unit length $c$ remains roughly constant ($\approx 0.2\text{ fF}/\mu\text{m}$) due to fringing fields, the intrinsic delay of a fixed-length global wire increases as $O(S^2)$. Consequently, crossing an $8\text{ mm}$ die in modern sub-5nm technology requires over $12\text{ clock cycles}$ at $2\text{ GHz}$.

---

## 2. Elmore Delay Calculation for Buffered Interconnects

For a distributed wire driven by an inverter with output resistance $R_d$ and driving load capacitance $C_L$, the 50% propagation delay is modeled via the Elmore delay metric:

$$
T_{50\%} = 0.69 \cdot R_d (C_{\text{wire}} + C_L) + 0.38 \cdot R_{\text{wire}} C_{\text{wire}} + 0.69 \cdot R_{\text{wire}} C_L
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

**Question 1:** If wire width and thickness both scale down by $1.4\times$, what happens to wire resistance per unit length?  
*Answer:* Resistance increases by approximately $(1.4)^2 \approx 2.0\times$ (doubles).

**Question 2:** Why does wire capacitance per unit length NOT scale down proportionally with wire width?  
*Answer:* Sidewall coupling capacitance and fringing electric fields to adjacent metal tracks dominate over parallel-plate ground capacitance.

**Question 3:** How does Elmore delay scale with wire length $L$ for an unbuffered wire?  
*Answer:* Delay scales quadratically as $O(L^2)$ because both total resistance ($rL$) and total capacitance ($cL$) increase linearly with length.

---

👉 **Next: [Lesson 1.3: Optimal Repeater Insertion & Scattering Physics](03-repeater-insertion.md)**
