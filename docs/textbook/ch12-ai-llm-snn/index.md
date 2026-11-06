# Chapter 12: Domain-Specific NoCs for LLMs, Transformers & Neuromorphic SNNs

[![Companion Platform](https://img.shields.io/badge/Interactive%20Arcade-Transformer%20Titan-9333ea?logo=gamepad&logoColor=white)](https://network-on-chip.github.io/learning/interactive/transformer/)
[![Neuromorphic Lab](https://img.shields.io/badge/Companion%20Lab-Neuromorphic%20Nexus-7e22ce?logo=bookstack&logoColor=white)](https://network-on-chip.github.io/learning/interactive/neuromorphic/)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%209%3A%20AI%20Interconnects-indigo)](https://network-on-chip.github.io/learning/track9-ai-interconnects/)
[![Hardware RTL](https://img.shields.io/badge/SystemVerilog%20RTL-in__network__reduction__router.sv-success)](code/in_network_reduction_router.sv)
[![Reference Papers](https://img.shields.io/badge/IEEE%20TVLSI%202026-PAC--NoC%20%7C%20HammerBlade-blue)](https://doi.org/10.1109/TVLSI.2026.3684311)

---

## Chapter Introduction

In the first two decades of Network-on-Chip history, interconnects were optimized for symmetric multi-core processors executing cache-coherent memory hierarchies and stochastic, uniform traffic. Today, computer architecture has entered the era of **Generative Artificial Intelligence (AI)** and **Bio-Inspired Neuromorphic Computing**. Large Language Models (LLMs) featuring hundreds of billions of parameters (e.g., Llama, GPT, DeepSeek) and event-driven Spiking Neural Networks (SNNs) impose communication patterns fundamentally alien to conventional CPU/GPU meshes:

1. **Massive Collective Synchronizations:** Transformer multi-head attention and distributed weight training require massive, synchronous **All-Reduce**, **All-to-All**, and **Reduce-Scatter** collectives across thousands of tensor cores. In conventional NoCs, transmitting unreduced floating-point tensors back and forth across planar meshes saturates bisection bandwidth, leaving compute ALUs idle in severe pipeline bubbles.
2. **The Memory Wall in LLM Serving:** Auto-regressive token generation is heavily memory-bandwidth bound. Large Language Models require continuous loading of multi-gigabyte KV-cache tensors, creating severe **memory silos** when off-chip memory interfaces (HBM/DDR) become congested.
3. **Sparse Event-Driven Multicast in SNNs:** Biological brain models communicate via asynchronous, binary action potentials (spikes) using Address-Event Representation (AER). Rather than high-throughput streaming, neuromorphic NoCs require **ultra-low-latency 1-to-$N$ multicast trees** that fan out single axon spikes to hundreds of target post-synaptic neurons across the silicon die.

To overcome these communication bottlenecks, architects are moving beyond standard packet switching to deploy **In-Network Computing** (performing gradient aggregation directly inside router crossbars), **Wafer-Scale & Ruche wire-maximal topologies**, **3D Face-to-Face Hybrid Bonding**, and **Spike-Sharing graph partitioning**.

```
+---------------------------------------------------------------------------------------+
|                              CHAPTER 12 CONCEPTUAL LANDSCAPE                          |
+---------------------------------------------------------------------------------------+
|  Generative AI Workloads       Hardware Acceleration Paradigms   Neuromorphic Interconnect|
|  - Tensor Parallel All-Reduce  - In-Network Crossbar ALU Reduction - 1-to-N Multicast Trees |
|  - KV-Cache Memory Silos       - Ruche Wire-Maximal Express Links  - Address-Event Rep (AER)|
|  - MoE Token Routing           - 3D Face-to-Face Hybrid Bonding    - Spike-Sharing Partition|
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                           SILICON REALIZATION & PPA TRADEOFFS                         |
+---------------------------------------------------------------------------------------+
|  Memory Bandwidth Scaling     Wafer-Scale Defect Bypass        Pipeline Bubble Ratio  |
|  - >16 TB/s via 3µm Cu pillars- Cross-reticle asynchronous links- 1 - N / (N + P - 1) |
|  - SiloBreaker co-scheduling  - HammerBlade 2048-core tapeout  - PAC-NoC tree speedup |
+---------------------------------------------------------------------------------------+
```

### Learning Objectives
- **Deconstruct AI Collective Communication**: Mathematically formulate Ring-AllReduce vs. Hierarchical Tree-AllReduce and calculate communication latency as a function of model tensor size and node count.
- **Architect In-Network Reduction Crossbars**: Design router microarchitectures that perform in-flight fixed-point and floating-point gradient aggregation directly inside the switching fabric (**PAC-NoC**, TVLSI 2026).
- **Evaluate Wafer-Scale & Wire-Maximal Topologies**: Analyze the physical trade-offs of Ruche networks and cross-reticle defect bypass in 2,048-core silicon processors (**HammerBlade in Silicon**, TVLSI 2026; **Theseus**, TCAD 2025).
- **Overcome Memory Silos with 3D Hybrid Bonding**: Evaluate face-to-face copper pillar bonding (3 µm pitch, >16 TB/s vertical DRAM bandwidth) and co-design memory scheduling for low-batch on-device LLM inference (**SiloBreaker**, TCAD 2026).
- **Optimize Spiking Neuromorphic Multicasts**: Implement spike-sharing graph partitioning algorithms that collapse redundant axon transmissions in large neuromorphic arrays (**SparrowSNN**, **SNNcut**, TCAD 2026).
- **Interactive Simulations**: Master AI collective acceleration in the [`Transformer Titan Arcade`](https://network-on-chip.github.io/learning/interactive/transformer/) and spike multicasting in [`Neuromorphic Nexus`](https://network-on-chip.github.io/learning/interactive/neuromorphic/).

---

## 12.1 The Generative AI Communication Bottleneck

In distributed Large Language Model training and inference, execution is divided across multiple dimensions of parallelism:
- **Tensor Parallelism (TP):** Individual matrix multiplications (GEMM) are split across cores, requiring an **All-Reduce** after every linear projection layer.
- **Pipeline Parallelism (PP):** Successive Transformer layers are partitioned across nodes, transferring intermediate activation tensors and generating idle compute bubbles.
- **Mixture-of-Experts (MoE):** Tokens are dynamically routed to specialized expert accelerators via sparse gating functions, creating severe, bursty all-to-all communication patterns.

```
Conventional Multi-Core vs. AI In-Network Computing

Conventional NoC (Store-and-Forward to Memory):
[ Core 0 ] --(Flit 0)--> [ Router ] 
[ Core 1 ] --(Flit 1)--> [ Router ] ===> [ Memory / Cache ] ===> [ Core 0 receives Reduced Sum ]
(Memory bandwidth bottleneck: 2N transfers across mesh)

In-Network Computing NoC (PAC-NoC):
[ Core 0 ] --(Flit 0)----\
                          (+) Router Crossbar ALU ===> [ Parent Core receives Sum ]
[ Core 1 ] --(Flit 1)----/
(In-flight reduction: 50% bandwidth reduction, zero memory overhead!)
```

---

## 12.2 In-Network Computing & Hierarchical Aggregation Trees

In **PAC-NoC** (TVLSI 2026), the router crossbar is augmented with a dedicated reduction arithmetic unit:

1. **Tag-Matching Accumulator:** When flits carrying the identical collective reduction tag arrive from competing input ports (e.g. North, East, South, West), the router's input arbiters lock the buffer entries.
2. **In-Flight Accumulation:** Rather than writing multiple flits into output virtual channels, the crossbar adds incoming gradient values on the fly:
   $$V_{\text{accum}} = \sum_{p \in \text{Participating Ports}} V_p$$
3. **Bandwidth Savings:** A 4-ary aggregation tree reduces the total flit volume transmitted across the interconnect by up to $75\%$, cutting multi-head attention latency by more than $2\times$.

---

## 12.3 Wafer-Scale Engines & Ruche Wire-Maximal Networks

Scaling LLM acceleration to extreme dimensions requires transcending single-reticle silicon limits. Two landmark approaches demonstrate wafer-scale and megacore physical scaling:

### 1. Wafer-Scale Architecture (Theseus)
In **Theseus** (TCAD 2025), entire 300 mm silicon wafers are patterned as continuous computational engines. To survive manufacturing defects across reticle boundaries, the NoC integrates:
- Redundant cross-reticle interconnect links with hardware-based bypass multiplexers.
- Asynchronous Globally Asynchronous Locally Synchronous (GALS) clock boundaries to eliminate wafer-scale clock skew.

### 2. HammerBlade in Silicon: Ruche Networks
In **HammerBlade** (TVLSI 2026), a $99\text{ mm}^2$, 12-nm FinFET processor integrates **2,048 RISC-V cores** using **Ruche Networks**:
- **Wire-Maximal Principle:** High metal layers (M7/M8) possess lower resistance and capacitance than lower routing tracks. Ruche networks deploy long, multi-hop wires that physically skip over intermediate routers (e.g., jumping 2 or 4 hops in a single cycle) without adding extra ports to router crossbars.
- **World-Record Efficiency:** Achieves record-setting CoreMark performance, demonstrating that physical wire layout must be co-designed with routing topology.

---

## 12.4 3D Hybrid Bonding & Memory Silo Breaking

Large Language Model inference is notoriously memory-bound: evaluating every token requires streaming the full weight matrices and KV-cache through the compute cores.

In **SiloBreaker** (TCAD 2026), conventional microbump-based TSVs are replaced by **3D Face-to-Face Copper-Pillar Hybrid Bonding**:
- **High-Density Interconnect:** Pitch sizes as small as $3\text{ }\mu\text{m}$ enable over **110,000 vertical connections per mm²**.
- **Massive Bandwidth:** Delivers **>16 TB/s vertical DRAM bandwidth**, shattering the memory wall for on-device LLM inference.
- **Resource Silo Co-Design:** By scheduling compute tasks to match the physical vertical memory channels, SiloBreaker eliminates memory starvation bubbles while keeping thermal dissipation within mobile form-factor envelopes.

---

## 12.5 Neuromorphic Spiking Interconnects (SNNcut & SparrowSNN)

In Spiking Neural Networks (SNNs), computation is event-driven: neurons fire binary spikes ($S \in \{0, 1\}$) only when membrane potential exceeds a threshold.

### The Fanout Problem
A single cortical neuron connects to thousands of post-synaptic targets. In a multi-core neuromorphic chip (e.g. Intel Loihi, TrueNorth), transmitting thousands of individual unicast packets for a single spike saturates router buffers.

### Spike-Sharing Partitioning (SNNcut)
In **SNNcut** (TCAD 2026) and **SparrowSNN** (TCAD 2026), neuromorphic networks are partitioned using hypergraph cut formulations:
- Neurons that share overlapping post-synaptic targets are grouped onto the same core.
- A single multi-cast spike flit is broadcast to the target core, where local fanout logic expands the spike to all local synapses, cutting inter-core NoC traffic by over $60\%$.

---

## 12.6 Synthesizable SystemVerilog In-Network Reduction Crossbar

Below is the synthesizable SystemVerilog RTL for the in-network reduction router ([`in_network_reduction_router.sv`](code/in_network_reduction_router.sv)):

```systemverilog
module in_network_reduction_router #(
    parameter DATA_WIDTH  = 32, // Gradient payload
    parameter NUM_PORTS   = 4,  // N, E, S, W
    parameter TAG_WIDTH   = 8   // Collective identifier
)(
    input  wire                               clk,
    input  wire                               rst_n,
    input  wire [NUM_PORTS-1:0]               flit_valid_in,
    input  wire [NUM_PORTS-1:0]               is_reduction_in,
    input  wire [NUM_PORTS*TAG_WIDTH-1:0]     reduction_tag_in,
    input  wire [NUM_PORTS*DATA_WIDTH-1:0]    flit_data_in,
    output wire [NUM_PORTS-1:0]               flit_ready_out,
    
    output reg                                flit_valid_out,
    output reg  [TAG_WIDTH-1:0]               reduction_tag_out,
    output reg  [DATA_WIDTH-1:0]              flit_data_out,
    input  wire                               flit_ready_in,
    output reg  [15:0]                        reductions_completed
);
    // In-flight gradient accumulator tree
    // Full synthesizable RTL in code/in_network_reduction_router.sv
endmodule
```

---

## 12.7 Interactive Lab Challenges

Experience generative AI collective acceleration and spiking neural routing firsthand in our interactive browser laboratories:

1. ⚡ [**Transformer Titan: LLM Collective Accelerator Arcade**](../../interactive/transformer.md)
   - Orchestrate All-Reduce and attention communication for a 100B+ LLM.
   - Switch between **Hierarchical PAC Trees** (`1`), **Ruche Express Links** (`2`), and **Ring-AllReduce** (`3`).
   - Trigger In-Network Reduction Bursts (`Space`) to eliminate pipeline bubbles!

2. 🧠 [**Neuromorphic Nexus: Spiking Neural NoC**](../../interactive/neuromorphic.md)
   - Balance Leaky-Integrate-and-Fire membrane potentials.
   - Deploy hardware multicast trees to distribute AER spike flits across neural cores.

---

## 12.8 Checkpoint Assessment

1. **How does In-Network Computing (e.g. PAC-NoC) reduce memory bandwidth pressure during Transformer training?**
   - *Answer:* Rather than transmitting individual gradient tensors from all cores back to central memory or through a multi-hop ring, routers accumulate gradients on the fly inside the crossbar. By performing the reduction during transit, the volume of traffic reaching the destination is reduced by a factor proportional to the tree fan-in (up to $75\%$ in a 4-ary tree).
2. **What is the key principle of Ruche Networks demonstrated in the 12-nm 2048-core HammerBlade silicon SoC?**
   - *Answer:* Ruche networks exploit thick, low-resistance upper metal routing layers to create multi-hop express links that bypass intermediate routers without adding crossbar ports to intermediate tiles, dramatically cutting network diameter and hop count with zero increase in router radix.
3. **Why is 3D hybrid bonding superior to conventional TSVs for on-device LLM inference?**
   - *Answer:* Hybrid bonding uses direct face-to-face copper pillar bonding with pitches as small as $3\text{ }\mu\text{m}$ (>110,000 interconnects/mm²), providing over $16\text{ TB/s}$ of vertical DRAM bandwidth without consuming dedicated device silicon area required by through-silicon vias.
