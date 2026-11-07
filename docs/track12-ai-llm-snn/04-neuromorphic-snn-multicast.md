# Lesson 12.4: Neuromorphic Event-Driven Spike Multicasting

<div class="noc-hero">
  <div class="noc-track-badge">Track 12 • Lesson 04</div>
  <h1>Address-Event Representation (AER), Synaptic Fanout &amp; Hypergraph Cut</h1>
  <p class="subtitle">
    Route discrete axonal action potentials across millions of spiking neurons using Address-Event Representation (AER) and optimal hypergraph partitioning (SNNcut).
  </p>
</div>

---

## 1. Event-Driven Spiking Communication

Unlike synchronous clock-driven DNNs, Spiking Neural Networks (SNNs) communicate via discrete, sparse **action potential spikes**. Each spike is encoded using the **Address-Event Representation (AER)** protocol:

```text
┌────────────────────────┬────────────────────────┐
│  Source Neuron ID (16)  │  Timestamp Phase (16)  │
└────────────────────────┴────────────────────────┘
```

Because an axonal spike can have a synaptic fanout of $>10^3$ target dendrites, routers must support hardware **Multicast Replication Trees** without duplicating packet flits on shared physical links.

---

👉 **Advance to [Track 13: Capstone System Synthesis](../track13-capstone/index.md)**
