# Lesson 6.2: DVFS Islands & Mixed-Clock Synchronization

<div class="noc-hero">
  <div class="noc-track-badge">Track 06 • Lesson 02</div>
  <h1>Dynamic Voltage &amp; Frequency Scaling (DVFS) in Multi-Core NoCs</h1>
  <p class="subtitle">
    Partition chips into independent Voltage-Frequency Islands (VFIs) and implement dual-clock asynchronous FIFO credit synchronizers without metastability hazards.
  </p>
</div>

---

## 1. Voltage-Frequency Islands (VFIs)

Rather than operating an entire multi-core processor at a single worst-case supply voltage and frequency, chips are partitioned into independent **Voltage-Frequency Islands (VFIs)**:

$$
P_{\text{tile}} = \alpha C V_{\text{tile}}^2 f_{\text{tile}} + V_{\text{tile}} I_{\text{leak}}
$$

Reducing frequency by $50\%$ enables a $30\%$ voltage drop, delivering over $75\%$ dynamic power savings on idle compute cores.

---

## 2. Mixed-Clock Domain Synchronization

When packet flits travel across disparate clock domains (e.g., Tile Core at $1.2\text{ GHz}$ $\to$ NoC Router at $800\text{ MHz}$), two-flip-flop synchronizers or dual-clock Gray-code FIFOs prevent metastability:

$$
\text{MTBF} = \frac{e^{t_{\text{resolve}}/\tau}}{T_{\text{clk}} \cdot f_{\text{data}} \cdot T_w}
$$

where $\text{MTBF}$ is the Mean Time Between Failures.

---

## 3. Synthesizable Verilog: Power-Gating Router FSM

```verilog
--8<-- "docs/textbook/ch06-low-power-dark-silicon/code/power_gating_router_fsm.v"
```

---

👉 **Next: [Lesson 6.3: Fine-Grained Router Power Gating](03-power-gating-router.md)**
