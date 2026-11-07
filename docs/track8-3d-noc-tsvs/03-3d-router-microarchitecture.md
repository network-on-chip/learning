# Lesson 8.3: 7-Port 3D Router Microarchitectures

<div class="noc-hero">
  <div class="noc-track-badge">Track 08 • Lesson 03</div>
  <h1>7-Port Crossbars, Vertical Serialization &amp; Asymmetric Buffering</h1>
  <p class="subtitle">
    Expand planar 5-port routers to 7 ports (N, S, E, W, Up, Down, Local) while containing crossbar area explosion $O(P^2)$ and managing vertical TSV pitch constraints.
  </p>
</div>

---

## 1. The 7-Port Crossbar Challenge

Adding vertical dimensions increases the router radix from 5 to 7. A conventional monolithic crossbar matrix scales as $O(P^2)$: a $7 \times 7$ switch requires $49$ crosspoints compared to $25$ in a 2D router ($+96\%$ area increase).

To mitigate crossbar silicon overhead:
1. **Dimension-Decoupled Crossbars:** Separate planar traffic (N, S, E, W) from vertical traffic (Up, Down).
2. **Asymmetric Buffer Allocation:** Vertical links have near-zero wire flight latency compared to horizontal RC lines, permitting shallower vertical virtual channel buffers ($B_{\text{vertical}} < B_{\text{horizontal}}$).

---

👉 **Next: [Lesson 8.4: 3D Topologies, Thermal Stacking & Vertical Deadlock](04-3d-topologies-thermal-deadlock.md)**
