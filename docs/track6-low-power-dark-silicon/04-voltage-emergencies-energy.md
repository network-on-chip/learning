# Lesson 6.4: Voltage Emergencies & Energy-Proportional Interconnects

<div class="noc-hero">
  <div class="noc-track-badge">Track 06 • Lesson 04</div>
  <h1>Inductive Noise ($L \cdot di/dt$), Resonant Links &amp; Energy Scaling</h1>
  <p class="subtitle">
    Mitigate catastrophic supply voltage droop caused by rapid traffic surges, and evaluate resonant clocking and low-swing differential transceivers for ultra-low power routing.
  </p>
</div>

---

## 1. The $L \cdot di/dt$ Inductive Voltage Droop Crisis

When a burst of packets arrives simultaneously at multiple routers, thousands of crossbar output drivers switch within a sub-nanosecond window. The rapid rate of current change ($di/dt$) through parasitic package bondwire inductances ($L_{\text{pkg}}$) induces severe voltage droop:

$$
\Delta V = L_{\text{pkg}} \frac{di}{dt}
$$

A voltage droop exceeding $10\%$ causes setup timing violations and bit corruption across router pipeline registers. Mitigation techniques include **Phase-Staggered Switch Allocation** and **Dynamic Decoupling Capacitors (Decaps)**.

---

👉 **Advance to [Track 7: Thermal Modeling, Hotspots & Fault Tolerance](../track7-thermal-fault-tolerance/index.md)**
