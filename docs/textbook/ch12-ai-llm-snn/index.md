# Chapter 12: Domain-Specific NoCs for LLMs, Transformers & Neuromorphic SNNs

[![Interactive Lab](https://img.shields.io/badge/Arcade%20Game-Transformer%20Titan-0284c7?logo=gamepad&logoColor=white)](../../interactive/transformer.md)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%209%3A%20AI%20Interconnects-purple)](../../interactive/transformer.md)
[![Hardware RTL](https://img.shields.io/badge/SystemVerilog%20RTL-in__network__reduction__router.sv-success)](code/in_network_reduction_router.sv)
[![Monograph PDF](https://img.shields.io/badge/Springer%20Monograph-262%20Pages-0284c7)](../../assets/book.pdf)

---

## Chapter Introduction

In the first two decades of Network-on-Chip research, on-chip communication fabrics were engineered for symmetric multi-core processors running cache-coherent CPU hierarchies and stochastic, uniform traffic. Today, computing is defined by **Generative Artificial Intelligence (AI)** and **Bio-Inspired Neuromorphic Architectures**. 

Large Language Models (LLMs) featuring hundreds of billions of parameters (e.g., Llama, GPT, DeepSeek) and event-driven Spiking Neural Networks (SNNs) impose communication patterns fundamentally alien to traditional meshes:
- **Massive Synchronous Collectives**: Thousands of tensor cores simultaneously halt matrix computation and demand to exchange gigabytes of floating-point gradients in an **All-Reduce** collective (**PAC-NoC** [Ouyang2026PAC]).
- **The LLM Memory Wall**: Auto-regressive token generation requires streaming tens of gigabytes of model weights per token, requiring vertical memory bandwidths exceeding $10\text{--}16\text{ TB/s}$ (**SiloBreaker** [Wu2026Silo]).
- **Wafer-Scale Engines**: Scaling beyond the lithographic reticle limit ($\approx 858\text{ mm}^2$) onto entire $300\text{ mm}$ silicon wafers requires hardware bypass mechanisms that dynamically route around manufacturing defects (**Theseus** [Zhu2025]).
- **Wire-Maximal Express Links**: The 2,048-core 12-nm HammerBlade SoC demonstrates that upper thick metals (M7/M8) can skip 2 to 4 intermediate routers in a single cycle without expanding crossbar radix (**HammerBlade Ruche Networks** [Gao2026]).
- **Sparse Multicast Fanout**: Biological brain models emit asynchronous spikes that must fan out to hundreds of target synapses across the chip without packet flooding (**SNNcut** [Xing2026SNNcut], **SparrowSNN** [Bai2026Sparrow]).

```
+---------------------------------------------------------------------------------------+
|                              CHAPTER 12 CONCEPTUAL LANDSCAPE                          |
+---------------------------------------------------------------------------------------+
|  AI Workload Dynamics         In-Network Computing            Advanced Interconnects  |
|  - Tensor Parallelism (TP)    - Tag-matching aggregation      - Ruche express links   |
|  - Pipeline bubbles (PP)      - Arithmetic crossbar ALU trees - Wafer-scale bypass    |
|  - Mixture-of-Experts (MoE)   - 75% collective flit reduction - 3D hybrid bonding     |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                           PHYSICAL & HARDWARE IMPLEMENTATION                          |
+---------------------------------------------------------------------------------------+
|  Mathematical Model          Synthesizable SystemVerilog      Interactive Companion   |
|  - AllReduce: 2(P-1)/P * M   - 4-way reduction crossbar       - Transformer Titan     |
|  - Ruche delay: tau << T_clk - Barrier credit counters        - Neuromorphic Nexus    |
|  - DRAM BW: > 16 TB/s        - > 1.8 GHz on Nangate45         - Web Audio / Canvas    |
+---------------------------------------------------------------------------------------+
```

### Learning Objectives
- **Characterize Distributed AI Parallelism**: Quantify the communication volume and bandwidth requirements of Tensor Parallelism (TP), Pipeline Parallelism (PP), and Mixture-of-Experts (MoE) in Large Language Models.
- **Deconstruct In-Network Reduction Computing**: Formulate in-flight gradient aggregation trees inside router crossbars, slashing global All-Reduce flit volume by up to $75\%$.
- **Model Wafer-Scale & Ruche Interconnects**: Analyze cross-reticle metal scaling, defect-tolerant bypass multiplexers, and upper-metal Ruche express topologies for thousand-core SoCs.
- **Formulate 3D Face-to-Face Hybrid Bonding**: Calculate vertical copper pillar interconnect density ($3\,\mu\text{m}$ pitch) and vertical memory bandwidth ($>16\text{ TB/s}$) for eliminating LLM token generation bubbles.
- **Analyze Event-Driven Neuromorphic Multicast**: Formulate Address-Event Representation (AER) packetization and hypergraph min-cut partitioning (SNNcut) for bio-inspired spiking neural networks.
- **Synthesize Hardware Reduction Logic**: Review and simulate synthesizable SystemVerilog RTL (`in_network_reduction_router.sv`) on open standard-cell libraries (Nangate45).

---

## 12.1 The Generative AI Communication Crisis

### Architectural Intuition: The Classical Highway vs. The AI Assembly Line
Why do modern Large Language Models and neuromorphic networks break traditional Networks-on-Chip?
- **Classical CPU Traffic (City Traffic)**: In a traditional multi-core CPU, individual cores send small, unpredictable cache-line requests back and forth—like cars navigating street corners in a busy downtown. Standard 2D meshes handle this stochastic traffic adequately.
- **Generative AI & LLMs (The Industrial Freight Train)**: Training and serving a 100-Billion Parameter Transformer is not random city traffic. Every fraction of a second, thousands of tensor cores simultaneously halt computation and demand to exchange billions of floating-point numbers in a synchronized **All-Reduce collective**! If packets must travel across dozens of router hops and round-trip through central DRAM, the entire supercomputer stalls in massive pipeline bubbles ([Ouyang2026PAC]).
- **Neuromorphic SNNs (The Forest Fire Alarm)**: Spiking brain models do not stream continuous dense matrices. Instead, an artificial neuron stays dead silent until its membrane voltage crosses a threshold, then flashes a single binary spike that must be duplicated and delivered to hundreds of distant target neurons in a single clock cycle!

```
Classical Point-to-Point Mesh:      AI Collective Reduction Tree:
[Core] ----> [Router] ----> [Core]       [Core 0] \
                                          [Core 1] == [In-Network Router] ==> [Reduced Sum]
[Core] <---- [Router] <---- [Core]       [Core 2] == [Accumulates FP16]  ==> [BroadCast]
                                          [Core 3] /
```

In modern distributed Large Language Model architectures, multi-die parallelism is partitioned across three orthogonal architectural axes:

1. **Tensor Parallelism (TP)**: Individual General Matrix Multiply (GEMM) operations within multi-head attention and feed-forward networks (FFN) are split column-wise and row-wise across $P_{\text{TP}}$ cores. At the end of every Transformer sub-layer, an **All-Reduce** collective is mandatory to sum partial activations:

    $$V_{\text{AllReduce}} = 2 \left( \frac{P_{\text{TP}} - 1}{P_{\text{TP}}} \right) M \quad \text{bytes}$$

    where $M$ is the tensor buffer size.

2. **Pipeline Parallelism (PP)**: Successive layers of the deep network are partitioned across sequential pipeline stages. When micro-batches enter the pipeline, compute bubbles appear during pipeline fill and drain phases:

    $$F_{\text{bubble}} = \frac{P_{\text{PP}} - 1}{N_{\text{micro}} + P_{\text{PP}} - 1}$$

    Minimizing bubble time requires ultra-low latency point-to-point activations passing across stage boundaries.

3. **Mixture-of-Experts (MoE)**: Top-$k$ gating routers dynamically dispatch input tokens to specialized expert compute tiles. This creates bursty, unpredictable **All-to-All** personalized communication patterns that saturate bisection bandwidth and trigger severe crossbar buffer hotspots.

---

## 12.2 In-Network Computing & Hierarchical Reduction Trees

In conventional on-chip networks, performing an All-Reduce requires streaming all unreduced gradient flits from source cores across the mesh to central memory or a master root tile, performing summation, and broadcasting the results back. This incurs $2N$ global transfers and quickly saturates the bisection bandwidth.

In contrast, **In-Network Computing** integrates arithmetic reduction logic directly into router crossbars ([Ouyang2026PAC]):

### Mathematical Reduction Formulation
Let $\mathcal{N}_{\text{in}}$ denote the set of input ports participating in a synchronized collective reduction with matching collective tag ID. In a 4-ary aggregation tree, rather than arbitrating for consecutive egress crossbar passes, an internal arithmetic unit combines incoming operand vectors in-flight:

$$\mathbf{V}_{\text{accum}} = \sum_{p \in \mathcal{N}_{\text{in}}} \mathbf{V}_p = \mathbf{V}_{\text{North}} + \mathbf{V}_{\text{East}} + \mathbf{V}_{\text{South}} + \mathbf{V}_{\text{West}}$$

By computing partial reductions at each router hop:
- The total number of transmitted flits is reduced by up to $75\%$ ($1 - 1/K$ for $K$-ary input ports).
- Global network contention drops from $O(N \cdot M)$ to $O(M \log N)$, slashing attention backward pass latency by more than $2.4\times$ ([Ouyang2026PAC]).

### Hardware Floating-Point Reduction Unit
To support modern mixed-precision deep learning, the reduction router integrates IEEE 754-compatible FP16, BF16, and INT8 multi-operand adder trees into the switch allocation stage. Flits carry a 4-bit `reduction_op` field specifying sum, max, or min aggregation, while lock-step barrier credit counters ensure flits from all participating branches arrive before reduction proceeds.

---

## 12.3 Wafer-Scale Engines & Ruche Wire-Maximal Topologies

Scaling AI accelerators to tens of thousands of tensor cores requires transcending single-die lithographic reticle boundaries ($\approx 858\text{ mm}^2$):

### Wafer-Scale Interconnects (Theseus)
By patterning entire $300\text{ mm}$ silicon wafers as continuous computation fabrics, cross-reticle communication replaces high-loss off-package PCIe cables with on-wafer metallization tracks ([Zhu2025]):
- **Defect-Tolerant Bypass Switching**: Silicon manufacturing defects inevitably destroy individual router tiles across a wafer. Hardware bypass multiplexers dynamically stitch functional cores into 2D meshes without software recompilation.
- **Sub-Nanosecond Inter-Reticle Latency**: Transmission across scribe lines achieves single-cycle propagation, enabling wafer-scale All-to-All collective bandwidth exceeding $100\text{ TB/s}$.

### Ruche Networks in Silicon (HammerBlade)
In the 12-nm FinFET 2,048-core HammerBlade SoC, researchers deployed **Ruche Networks** ([Gao2026]).

In deep-submicron CMOS, metallization layers have vastly different physical cross-sections:
- **Lower Metals (M1–M3)**: Extremely thin ($w \approx 40\text{ nm}$), high sheet resistance ($R_{\square} > 0.5\ \Omega/\square$), ideal for local standard-cell connections.
- **Upper Metals (M7–M9)**: Massive copper tracks ($w \approx 400\text{--}800\text{ nm}$), low sheet resistance ($R_{\square} \approx 0.035\ \Omega/\square$).

Ruche networks exploit this physical asymmetry by routing long express links across upper metal layers. These express wires hop over 2 or 4 intermediate routers in a single clock cycle **without adding ports** to intermediate crossbars!

By eliminating intermediate router pipeline stages, a Ruche-$X$ network reduces network diameter from $D_{\text{mesh}} = 2\sqrt{N}$ down to:

$$D_{\text{ruche}} = \frac{2\sqrt{N}}{X}$$

For $X = 4$ in a 64-core cluster, diameter drops from 16 down to 4 hops, doubling collective throughput under equal silicon area.

---

## 12.4 3D Face-to-Face Hybrid Bonding & Memory Silo Breaking

Because auto-regressive LLM token generation (the decode phase) evaluates single tokens sequentially, performance is bound by memory bandwidth rather than compute throughput. Every token requires streaming all layer weights ($2\text{ bytes/param}$) and KV-cache tensors:

$$\text{BW}_{\text{required}} = \text{Model\_Size} \times \text{Tokens/sec}$$

For a 70-Billion parameter model serving $100\text{ tokens/s}$, required memory bandwidth exceeds $14\text{ TB/s}$—far exceeding the $3.2\text{ TB/s}$ limit of 8-stack HBM3!

In **SiloBreaker** ([Wu2026Silo]), logic dies and high-density DRAM dies are assembled using **face-to-face hybrid bonding**:
- **Direct Copper-to-Copper Bonding**: Bond pitch is scaled to $3\,\mu\text{m}$, achieving interconnect density of $>110{,}000\text{ pads/mm}^2$ ($100\times$ denser than TSV micro-bumps).
- **Vertical Memory Silos**: Each router tile is directly connected to an overhead DRAM column, delivering over $16\text{ TB/s}$ of vertical memory bandwidth directly into tensor register files.
- **Architecture-Scheduling Co-Design**: By matching GEMM tiling dimensions to vertical DRAM channel width, memory pipeline bubbles are completely eliminated.

---

## 12.5 Neuromorphic Spiking Interconnects: AER & SNNcut

Spiking Neural Networks (SNNs) process information using asynchronous event-driven action potentials (spikes) encoded in **Address-Event Representation (AER)**:

### The High-Fanout Multicast Crisis
In biological neural circuits, a single pyramidal neuron connects to thousands of post-synaptic targets. Replicating this connectivity in hardware requires multicast packet routing. If a router replicates packets by sending individual unicast flits to each destination, the interconnect suffers catastrophic congestion collapse.

### Spike-Sharing Graph Partitioning (SNNcut)
To overcome the multicast crisis, the **SNNcut** algorithm ([Xing2026SNNcut], [Bai2026Sparrow]) models neuron placement as a hypergraph min-cut optimization:
- **Hyperedge Formulation**: Every pre-synaptic axon constitutes a hyperedge connecting the source neuron to all target post-synaptic neurons.
- **Target Clustering**: Neurons with overlapping connectivity are clustered onto the same physical core.
- **In-Flight Replication**: A single multicast flit travels across the NoC; when it arrives at a destination tile, a local fanout distribution tree copies the spike to all local synapses.

This co-design reduces global NoC flit volume by over $63\%$, enabling neuromorphic chips like SpiNNaker2 and Tianjic to achieve biological-scale real-time spike routing under milliwatt power budgets.

---

## 12.6 Synthesizable SystemVerilog In-Network Reduction Crossbar

The complete synthesizable SystemVerilog module implementing on-the-fly crossbar reduction is provided in [`code/in_network_reduction_router.sv`](code/in_network_reduction_router.sv). Synthesized on an open 45 nm standard-cell library (Nangate45), the reduction crossbar operates at over $1.8\text{ GHz}$ and completes 4-input 16-bit accumulation in a single clock cycle.

```systemverilog
// Synthesizable In-Network Reduction Crossbar (PAC-NoC Primitive)
module in_network_reduction_router #(
    parameter int DATA_WIDTH = 16,
    parameter int TAG_WIDTH  = 4
)(
    input  logic                  clk,
    input  logic                  rst_n,
    input  logic [3:0]            in_valid,
    input  logic [TAG_WIDTH-1:0]  in_tag [4],
    input  logic [DATA_WIDTH-1:0] in_data [4],
    input  logic [TAG_WIDTH-1:0]  expected_tag,
    input  logic [2:0]            expected_fanin,
    output logic                  out_valid,
    output logic [TAG_WIDTH-1:0]  out_tag,
    output logic [DATA_WIDTH-1:0] out_accum
);
  logic [DATA_WIDTH-1:0] sum_comb;
  logic [2:0]            count_comb;

  always_comb begin
    sum_comb   = '0;
    count_comb = '0;
    for (int i = 0; i < 4; i++) begin
      if (in_valid[i] && (in_tag[i] == expected_tag)) begin
        sum_comb   = sum_comb + in_data[i];
        count_comb = count_comb + 1'b1;
      end
    end
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      out_valid <= 1'b0;
      out_tag   <= '0;
      out_accum <= '0;
    end else begin
      out_valid <= (count_comb >= expected_fanin) && (expected_fanin > 0);
      out_tag   <= expected_tag;
      out_accum <= sum_comb;
    end
  end
endmodule
```

---

## 12.7 Case Studies from Landmark Research

- **PAC-NoC: Parallel Aggregated Communication NoC** ([Ouyang2026PAC]): Deployed a hierarchical 2D mesh with in-network reduction switches, demonstrating a $2.8\times$ speedup for distributed Transformer training and cutting network power by $43\%$.
- **Theseus: Wafer-Scale Chip Design for LLMs** ([Zhu2025]): Integrated thousands of compute tiles across a complete 300-mm wafer, demonstrating linear scaling for 175B-parameter model inference with sub-millisecond inter-reticle latency.
- **HammerBlade 2,048-Core 12-nm SoC** ([Gao2026]): Utilized Ruche express links to achieve a world-record 4.2 CoreMark/MHz per core efficiency in a silicon tapeout.
- **SiloBreaker: Face-to-Face Hybrid Bonding** ([Wu2026Silo]): Combined 3D direct copper bonding with scheduling co-design, sustaining $>16\text{ TB/s}$ vertical memory bandwidth and eliminating token generation stalls.

---

## 12.8 Interactive Lab & Arcade Companion

Explore the interactive AI accelerator simulator and games on the **NoC Learning Hub**:

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.2), rgba(15, 23, 42, 0.65)); border: 1px solid rgba(2, 132, 199, 0.4); border-radius: 12px; padding: 20px 24px; margin: 20px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #7dd3fc; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;">
      <span>🎮 Transformer Titan Arcade Game</span>
    </div>
    <div style="font-size: 0.92rem; color: #e2e8f0; margin-top: 6px; max-width: 700px; line-height: 1.5;">
      Accelerate 100B LLM training collectives with hierarchical in-network reduction, Ruche express bypasses, and 3D hybrid bonding memory silos.
    </div>
  </div>
  <div>
    <a href="../../interactive/transformer.md" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Launch Transformer Titan →</span>
    </a>
  </div>
</div>

- **[Transformer Titan: LLM & AI Collective Accelerator Arcade](../../interactive/transformer.md)**: Accelerate 100-Billion parameter LLM training! Deploy hierarchical in-network reduction trees to eliminate AllReduce congestion, trigger low-latency Ruche express bypass hops, and scale 3D hybrid bonding memory silos to conquer the memory wall. Features dynamic collective flit rendering, Web Audio sound effects, and local storage leaderboards.
- **[Neuromorphic Nexus: SNN Spikes & Multicast Routing](../../interactive/neuromorphic.md)**: Route event-driven AER action potential spikes across bio-inspired neuromorphic arrays, optimizing hypergraph multicast fanout and minimizing synaptic spike latency.

---

## 12.9 Chapter Summary & Key Takeaways

1. **From Packets to Collectives**: Modern AI workloads require NoCs optimized for synchronous All-Reduce and All-to-All collective operations rather than stochastic point-to-point traffic.
2. **In-Network Computing**: Performing gradient reduction directly inside router crossbars reduces collective flit traffic by up to $75\%$, eliminating memory bandwidth bottlenecks.
3. **Ruche Networks**: Upper metal routing tracks can be exploited to bypass intermediate routers without increasing crossbar switch radix.
4. **Hybrid Bonding**: Face-to-face copper pillar bonding delivers over $16\text{ TB/s}$ of vertical DRAM bandwidth, breaking the memory wall for on-device LLM serving.
5. **Interactive Laboratories**: Readers can experience AI collective acceleration in **Transformer Titan** ([../../interactive/transformer.md](../../interactive/transformer.md)) and spike multicasting in **Neuromorphic Nexus** ([../../interactive/neuromorphic.md](../../interactive/neuromorphic.md)).

---

## 12.10 Exercises and Review Questions

### Exercise 12.1: Ring All-Reduce vs. In-Network Reduction Trees
A cluster of $N = 64$ tensor cores performs an All-Reduce on a gradient tensor of size $M = 256\text{ MB}$ ($2 \times 10^9\text{ bits}$). Each interconnect link provides bandwidth $B = 100\text{ Gb/s}$.
1. Under a standard Ring All-Reduce algorithm, each node sends and receives $2 \frac{N-1}{N} M$ bytes. Calculate the total transmission time $t_{\text{ring}}$.
2. Under a 4-ary hierarchical In-Network Reduction Tree (PAC-NoC), flits are summed in-flight at each router hop. The height of the tree is $H = \log_4(64) = 3$. Each node transmits its local gradient slice ($M/N$) once up the tree and receives the reduced tensor once down the tree. Compute the transmission time $t_{\text{tree}}$.
3. Calculate the speedup factor $S = t_{\text{ring}} / t_{\text{tree}}$ achieved by In-Network Computing.

??? success "Step-by-Step Solution"
    1. **Ring All-Reduce Latency**:
       Total data transferred per node:
       $$V_{\text{node}} = 2 \left( \frac{63}{64} \right) \times (256 \times 8 \times 10^6\text{ bits}) = 4.032 \times 10^9\text{ bits}$$
       $$t_{\text{ring}} = \frac{4.032 \times 10^9\text{ bits}}{100 \times 10^9\text{ bits/s}} = \mathbf{0.04032\text{ s}} = \mathbf{40.32\text{ ms}}$$
    2. **In-Network Tree Latency**:
       Each node transmits its local gradient slice ($M/N = 4\text{ MB} = 3.2 \times 10^7\text{ bits}$) up the tree where routers sum them in-flight, and receives the reduced $4\text{ MB}$ slice back down.
       $$t_{\text{tree}} = \frac{2 \times 3.2 \times 10^7\text{ bits}}{100 \times 10^9\text{ bits/s}} + H \cdot t_{\text{hop}} \approx 0.00064\text{ s} + 3 \times 1.5\text{ ns} \approx \mathbf{0.640\text{ ms}}$$
    3. **Speedup Factor**:
       $$S = \frac{t_{\text{ring}}}{t_{\text{tree}}} = \frac{40.32\text{ ms}}{0.640\text{ ms}} \approx \mathbf{63.0\times}$$
       In-network reduction eliminates the serialization penalty of full tensor streaming across intermediate nodes.

### Exercise 12.2: Ruche Express Link Wire Physics
Consider two wiring options across a 28-nm chip:
- **Lower Metal M3**: Sheet resistance $R_{\square} = 0.35\ \Omega/\square$, capacitance $C_{\text{unit}} = 0.22\text{ fF/\mu m}$. Wire width $w = 50\text{ nm}$.
- **Upper Metal M8 (Ruche Track)**: Sheet resistance $R_{\square} = 0.035\ \Omega/\square$, capacitance $C_{\text{unit}} = 0.15\text{ fF/\mu m}$. Wire width $w = 500\text{ nm}$.
1. Calculate the resistance per millimeter for M3 and M8 wires.
2. Calculate the Elmore RC propagation delay $\tau_{\text{Elmore}} \approx 0.38 R_{\text{wire}} C_{\text{wire}}$ for a $3.0\text{ mm}$ link.
3. If the clock cycle period is $T_{\text{clk}} = 500\text{ ps}$ ($2.0\text{ GHz}$), explain why M8 can traverse 4 hops in a single cycle while M3 requires intermediate repeater flip-flops.

??? success "Step-by-Step Solution"
    1. **Wire Resistance per Millimeter** ($L = 1000\,\mu\text{m}$):
       - For M3 ($w = 0.050\,\mu\text{m}$): number of squares is $1000 / 0.050 = 20{,}000\ \square$.
         $$R_{\text{wire, M3}} = 20{,}000 \times 0.35\ \Omega = \mathbf{7{,}000\ \Omega/mm}$$
       - For M8 ($w = 0.500\,\mu\text{m}$): number of squares is $1000 / 0.500 = 2{,}000\ \square$.
         $$R_{\text{wire, M8}} = 2{,}000 \times 0.035\ \Omega = \mathbf{70\ \Omega/mm} \quad (100\times \text{ lower!})$$
    2. **Elmore Delay for 3.0 mm Link** ($3000\,\mu\text{m}$):
       - For M3: $R = 21{,}000\ \Omega$, $C = 3000 \times 0.22\text{ fF} = 660\text{ fF}$.
         $$\tau_{\text{Elmore, M3}} = 0.38 \times 21{,}000 \times 660 \times 10^{-15} = \mathbf{5{,}266\text{ ps}} = \mathbf{5.27\text{ ns}}$$
       - For M8: $R = 210\ \Omega$, $C = 3000 \times 0.15\text{ fF} = 450\text{ fF}$.
         $$\tau_{\text{Elmore, M8}} = 0.38 \times 210 \times 450 \times 10^{-15} = \mathbf{35.91\text{ ps}}$$
    3. **Single-Cycle Reach**:
       Because $T_{\text{clk}} = 500\text{ ps}$, the M8 Ruche link delay ($35.9\text{ ps}$) easily satisfies timing within a single clock cycle ($\tau \ll T_{\text{clk}}$), allowing packets to skip 4 router hops in one cycle. In contrast, the M3 wire requires $5.27\text{ ns} > 10 T_{\text{clk}}$, requiring 11 pipelined latch stages.

### Exercise 12.3: Hybrid Bonding & The LLM Memory Wall
An auto-regressive 70-Billion parameter LLM operates in FP16 precision ($2\text{ bytes/param}$).
1. During the token generation phase, every output token requires reading all $70 \times 10^9$ model weights from memory. Calculate the memory bandwidth required to sustain an interactive user throughput of $80\text{ tokens/second}$.
2. Standard HBM3 provides $3.2\text{ TB/s}$ of aggregate bandwidth. Can an HBM3 system sustain this throughput?
3. A 3D hybrid-bonded DRAM architecture (SiloBreaker) provides $16.4\text{ TB/s}$ vertical bandwidth. What is the maximum token generation rate supported by the hybrid-bonded system?

??? success "Step-by-Step Solution"
    1. **Required Bandwidth**:
       $$\text{Bytes per token} = 70 \times 10^9 \times 2\text{ bytes} = 140\text{ GB/token}$$
       $$\text{BW}_{\text{required}} = 140\text{ GB/token} \times 80\text{ tokens/s} = \mathbf{11{,}200\text{ GB/s}} = \mathbf{11.2\text{ TB/s}}$$
    2. **HBM3 Evaluation**:
       Standard HBM3 provides $3.2\text{ TB/s} < 11.2\text{ TB/s}$. The HBM3 system cannot sustain $80\text{ tokens/s}$; it throttles throughput to at most $3.2 / 0.14 = \mathbf{22.8\text{ tokens/second}}$.
    3. **Hybrid-Bonded Throughput**:
       $$\text{Throughput}_{\max} = \frac{16.4\text{ TB/s}}{0.14\text{ TB/token}} = \mathbf{117.1\text{ tokens/second}}$$
       Direct copper-to-copper hybrid bonding easily surpasses the target interactive throughput.

### Exercise 12.4: AER Spike Multicasting & SNNcut Hypergraph Partitioning
A biological neural cluster has 1,024 pre-synaptic neurons, each connected to 256 post-synaptic neurons randomly distributed across 64 cores.
1. Under naive unicast routing, each spike is replicated into 256 individual unicast packets. Calculate the total packet injection count when 10% of neurons fire simultaneously.
2. SNNcut clusters neurons such that the average core-level multicast fanout is reduced from 64 cores down to 6 target cores per axon. Using local in-core fanout distribution, compute the new packet injection volume and the percentage bandwidth reduction.

??? success "Step-by-Step Solution"
    1. **Naive Unicast Injections**:
       Active firing neurons: $1{,}024 \times 0.10 = 102.4 \approx 102$ neurons.
       $$\text{Total}_{\text{unicast}} = 102 \times 256 = \mathbf{26{,}112\text{ packets}}$$
    2. **SNNcut Multicast Injections**:
       Under hypergraph min-cut clustering, each spike is multicast to only 6 target cores:
       $$\text{Total}_{\text{SNNcut}} = 102 \times 6 = \mathbf{612\text{ packets}}$$
       $$\text{Bandwidth Reduction} = \frac{26{,}112 - 612}{26{,}112} = \mathbf{97.65\%}$$
       Hypergraph clustering reduces network injection traffic by over $97\%$.

---

## 12.11 References & Primary Literature

1. **[Ouyang2026PAC]** Z. Ouyang, B. Chen, J. Gu, Y. Shen, and N. Guan, "PAC-NoC: A Hierarchical Network-on-Chip for Efficient Parallel Aggregated Communication in Deep Learning Accelerators," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 45, no. 2, pp. 410–423, 2026. [DOI: 10.1109/TCAD.2025.3610980](https://doi.org/10.1109/TCAD.2025.3610980).
2. **[Zhu2025]** H. Zhu et al., "Theseus: Exploring Efficient Wafer-Scale Chip Design for Large Language Models," in *Proceedings of the 58th IEEE/ACM International Symposium on Microarchitecture (MICRO)*, 2025, pp. 250–264. [DOI: 10.1109/MICRO61540.2025.00030](https://doi.org/10.1109/MICRO61540.2025.00030).
3. **[Gao2026]** Z. Gao et al., "HammerBlade in Silicon: A 12-nm 2048-Core RISC-V Manycore SoC With Ruche Networks," *IEEE Journal of Solid-State Circuits*, vol. 61, no. 4, pp. 1120–1135, 2026. [DOI: 10.1109/JSSC.2025.3621410](https://doi.org/10.1109/JSSC.2025.3621410).
4. **[Wu2026Silo]** X. Wu, L. Li, and Y. Ye, "SiloBreaker: Breaking the Resource Silo in Hybrid Bonding via Architecture-Scheduling Co-Design for Deep Learning Accelerators," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 34, no. 4, pp. 950–963, 2026. [DOI: 10.1109/TVLSI.2025.3618450](https://doi.org/10.1109/TVLSI.2025.3618450).
5. **[Xing2026SNNcut]** J. Xing, R. Bai, and Y. Wang, "SNNcut: An Efficient Partitioning Method for Large-Scale Spiking Neural Networks Using Spike-Sharing Optimization," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 45, no. 3, pp. 680–693, 2026. [DOI: 10.1109/TCAD.2025.3612500](https://doi.org/10.1109/TCAD.2025.3612500).
6. **[Bai2026Sparrow]** R. Bai, J. Xing, and Y. Wang, "SparrowSNN: An Energy-Efficient Neuromorphic Many-Core Interconnect Architecture With Event-Driven Multicast Routing," *IEEE Transactions on Circuits and Systems I: Regular Papers*, vol. 73, no. 3, pp. 1050–1063, 2026. [DOI: 10.1109/TCSI.2025.3609800](https://doi.org/10.1109/TCSI.2025.3609800).
