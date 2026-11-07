# Lesson 9.3: Cross-Die Boundary Deadlock Recovery

<div class="noc-hero">
  <div class="noc-track-badge">Track 09 • Lesson 03</div>
  <h1>Boundary Interfaces, Cyclic Subpaths &amp; In/Outbound Swap</h1>
  <p class="subtitle">
    Analyze why connecting individually deadlock-free chiplets frequently induces catastrophic cross-die deadlocks, and implement backtracking swap mechanisms grounded in IEEE TCAD 2026.
  </p>
</div>

---

## 1. The Multi-Chiplet Deadlock Paradox

Even when every individual chiplet implements a provably deadlock-free routing algorithm (such as Dimension-Order Routing), interconnecting them across passive/active interposers creates **Cyclic Channel Dependencies across die boundary interfaces**.

Boundary bridge buffers frequently stall because outbound flits wait for downstream chiplet buffer credits while holding local inbound buffer resources, forming a global cyclic resource wait.

---

## 2. In/Outbound Backtracking Swap (TCAD '26)

Grounded in IEEE TCAD 2026 (*In/Outbound Swap: A Backtracking-based Deadlock Recovery Mechanism for Multi-Chiplet Networks*), deadlocks are resolved without wasting dedicated virtual channel buffers:
* **Detection:** Routers detect when boundary buffers remain stalled beyond an adaptive timeout window $T_{\text{deadlock}}$.
* **Backtracking Swap:** Flit dependencies are dynamically swapped at the boundary router port, routing stalled packets onto localized escape paths and dissolving the cyclic dependency graph.

---

👉 **Next: [Lesson 9.4: Multi-Chiplet Router Bypassing (BuffeRS)](04-multichiplet-router-bypassing.md)**
