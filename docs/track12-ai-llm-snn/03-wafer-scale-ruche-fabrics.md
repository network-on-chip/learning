# Lesson 12.3: Wafer-Scale Fabrics & Ruche Express Links

<div class="noc-hero">
  <div class="noc-track-badge">Track 12 • Lesson 03</div>
  <h1>2,048-Core Cerebras-Class Fabrics &amp; Long Ruche Interconnects</h1>
  <p class="subtitle">
    Overcome 2D mesh diameter latency across full wafer-scale chips using high-radix long express bypass links (Ruche networks) without expanding crossbar switch radix.
  </p>
</div>

---

## 1. The Wafer-Scale Latency Problem

In wafer-scale processors (e.g., Cerebras WSE with $850,000$ cores on a single silicon wafer), average hop distance on a standard 2D mesh exceeds hundreds of cycles.

**Ruche networks** exploit upper metal layers ($M_{10}\text{--}M_{12}$) to create direct express links spanning $K = 4\text{--}8$ routers. Packets traverse across the die in single hops, bypassing intermediate input buffers while maintaining low router port count.

---

👉 **Next: [Lesson 12.4: Neuromorphic Event-Driven Spike Multicasting](04-neuromorphic-snn-multicast.md)**
