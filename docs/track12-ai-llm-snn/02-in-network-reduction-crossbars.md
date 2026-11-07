# Lesson 12.2: In-Network Reduction Crossbars (PAC-NoC)

<div class="noc-hero">
  <div class="noc-track-badge">Track 12 • Lesson 02</div>
  <h1>In-Flight Gradient Accumulation &amp; Arithmetic Router Microarchitecture</h1>
  <p class="subtitle">
    Embed floating-point and fixed-point reduction ALUs inside router crossbar switches, halving memory bandwidth demand based on IEEE TVLSI 2026.
  </p>
</div>

---

## 1. The PAC-NoC Concept (IEEE TVLSI '26)

Grounded in IEEE TVLSI 2026 (*PAC-NoC: A Hierarchical Network-on-Chip for Efficient Parallel Aggregated Communication in Transformer Accelerators*):
Instead of routing full gradient packets from all cores into DRAM for accumulation, router crossbars are augmented with **In-Flight Accumulators**:

$$
\text{Flit}_{\text{out}} = \sum_{i \in \text{Active Ports}} \text{Flit}_{\text{in}}[i]
$$

Flits arriving from North, East, South, and West ports are summed dynamically inside the crossbar, emitting a single reduced flit up the hierarchical tree. This **reduces total network flit traffic by up to $75\%$**!

---

## 2. Synthesizable Verilog: In-Network Reduction Router

```systemverilog
--8<-- "docs/textbook/ch12-ai-llm-snn/code/in_network_reduction_router.sv"
```

---

👉 **Next: [Lesson 12.3: Wafer-Scale Fabrics & Ruche Express Links](03-wafer-scale-ruche-fabrics.md)**
