# Lesson 1.4: Global Interconnect Energy & Physical Limits

<div class="noc-hero">
  <div class="noc-track-badge">Track 01 • Lesson 04</div>
  <h1>Energy Dissipation Limits &amp; The Shared Bus Collapse</h1>
  <p class="subtitle">
    Quantify interconnect energy dissipation ($CV^2f$), contrast crossbar area explosion $O(N^2)$ against Network-on-Chip modularity, and understand the definitive death of shared on-chip buses.
  </p>
</div>

---

## 1. Dynamic Energy Dissipation on Silicon Wires

Every transition on an on-chip wire charges and discharges the lumped capacitance $C_{\text{wire}}$, dissipating dynamic energy:

$$
E_{\text{bit}} = \frac{1}{2} \alpha C_{\text{wire}} V_{DD}^2
$$

where $\alpha$ is the switching activity factor ($0 < \alpha \le 1$). For an unpipelined bus carrying $W = 64$ parallel bits across $L = 10\text{ mm}$, total wire capacitance can exceed $2\text{ pF}$, demanding $>2\text{ pJ/bit}$ per transfer at $1.0\text{ V}$.

---

## 2. The Shared Bus Serialization Bottleneck

In classical architectures (e.g., AMBA AHB, CoreConnect), all cores share a single set of broadcast wires arbitrated by a central arbiter. As the number of cores $N$ increases:

1. **Capacitive Loading:** Every attached master and slave adds parasitic transceiver capacitance ($C_{\text{bus}} = N \cdot C_{\text{port}} + C_{\text{wire}}$), driving clock frequencies down.
2. **Bandwidth Saturation:** Total bandwidth remains fixed at $B = W \cdot f_{\text{bus}}$, forcing per-core throughput to collapse as $O(1/N)$.
3. **Contention Latency:** Wait times scale quadratically under Poisson packet arrivals due to head-of-line bus locking.

---

## 3. Summary of Track 1 & Bridge to Track 2

| Metric | Shared Bus | Full Crossbar Switch | Network-on-Chip (NoC) |
|---|:---:|:---:|:---:|
| **Area Scaling** | $O(1)$ | $O(N^2)$ | $O(N)$ |
| **Aggregated Bandwidth** | $O(1)$ (Fixed) | $O(N)$ | $O(N)$ (Concurrent links) |
| **Wire Lengths** | $O(N)$ (Global) | $O(N^2)$ (Congested) | $O(1)$ (Short P2P hops) |
| **Energy per Transfer** | High ($C_{\text{bus}} V^2$) | High (Dense matrix) | Low (Hop-by-hop local wires) |

---

👉 **Advance to [Track 2: Switching, Flow Control & Buffers](../track2-switching-flow-control/index.md)**
