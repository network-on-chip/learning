# Lesson 9.4: Multi-Chiplet Router Bypassing & BuffeRS

<div class="noc-hero">
  <div class="noc-track-badge">Track 09 • Lesson 04</div>
  <h1>Near Wire-Speed Inter-Die Transit &amp; Buffer Reservation Scheduling</h1>
  <p class="subtitle">
    Eliminate multi-cycle store-and-forward penalties across chiplet boundaries using buffer-reserved router bypassing, achieving single-cycle transit across intermediate dies.
  </p>
</div>

---

## 1. The Inter-Die Latency Penalty

Traversing across a multi-chiplet package typically requires:
$$
T_{\text{transit}} = N_{\text{local}} \cdot t_{\text{router}} + T_{\text{D2D}} + N_{\text{remote}} \cdot t_{\text{router}}
$$
Where each intermediate router adds 3–4 pipeline cycles. For a 4-hop packet traversing two chiplets, latency exceeds $14\text{ clock cycles}$.

---

## 2. The BuffeRS Architecture (IEEE TCAD '26)

Grounded in IEEE TCAD 2026 (*BuffeRS: A Buffer Reservation Scheduling Strategy for Router Bypassing in NoCs and Multichiplet Systems*):
* Upstream chiplet routers pre-reserve switch allocation slots at the downstream die bridge.
* Flits bypass intermediate router input buffers and crossbar arbitration in a **single clock cycle**, achieving near wire-speed transit across package boundaries.

Test this directly in our Web EDA Terminal:
```bash
guest@noc-lab:~$ buffers-eval --hops 4 --bypass-slots 2
```

---

👉 **Advance to [Track 10: Optical & Wireless Networks-on-Chip](../track10-optical-wireless/index.md)**
