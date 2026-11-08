# Chapter 3: High-Performance Router Microarchitecture & Arbitration

[![Companion Platform](https://img.shields.io/badge/Interactive%20Lab-Router%20Pipeline-0f766e?logo=bookstack&logoColor=white)](https://network-on-chip.github.io/learning/interactive/router/)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%202%3A%20Router%20Microarch-blue)](../../track3-router-microarchitecture/)
[![Simulation Model](https://img.shields.io/badge/Python%20Model-matrix__arbiter__islip__sim.py-blueviolet)](code/matrix_arbiter_islip_sim.py)
[![Hardware RTL](https://img.shields.io/badge/Verilog%20RTL-matrix__arbiter__4port.v-success)](code/matrix_arbiter_4port.v)

---

## Chapter Introduction

In modern many-core architectures, artificial intelligence engines, and multi-chiplet supercomputing clusters, the **on-chip router** serves as the central switching switchboard of the silicon die. While physical interconnect physics (explored in Chapter 1) dictate wire delays and signaling losses, and switching paradigms (Chapter 2) define how messages are serialized into flits, it is the internal **router microarchitecture** that ultimately governs per-hop packet latency, maximum operating frequency, and saturation throughput.

Every clock cycle spent inside an on-chip router compounds across the diameter of the network. In an $8 \times 8$ 2D mesh with an average hop count of $5.3$, a traditional 5-stage router imposes an intrinsic queuing-free latency penalty of over 26 clock cycles before a single bit of payload reaches the destination cache bank or compute tile. Consequently, the microarchitectural evolution of Network-on-Chip routers has been driven by an relentless quest: **how to compress the router pipeline from multi-cycle delays down to single-cycle—and even sub-cycle multi-hop—traversals, while preserving clock frequencies exceeding 1.5 to 2.0 GHz in deep sub-micron nodes.**

This chapter opens the silicon black box of the on-chip router. We systematically decompose the canonical five-stage Virtual Channel (VC) router datapath, dissect the timing and control hazards that emerge between buffer writing and switch traversal, and investigate advanced pipeline compression methods including lookahead routing, speculative switch allocation, and coordinated buffer reservation. Furthermore, we explore revolutionary non-traditional designs—ranging from Single-Cycle Multi-Hop Asynchronous Repeated Traversal (SMART/SHARP) to clockless Globally Asynchronous Locally Synchronous (GALS) domino architectures—before formalizing the circuit design of high-speed matrix arbiters and iterative bipartite matching allocators (iSLIP).

### Learning Objectives
- **Deconstruct the Canonical Pipeline**: Understand the exact microarchitectural responsibilities, input/output handshakes, and timing invariants across Buffer Write (BW), Route Computation (RC), Virtual Channel Allocation (VA), Switch Allocation (SA), and Switch Traversal (ST).
- **Master Pipeline Compression Techniques**: Formulate lookahead routing algorithms, speculative switch allocation state tables, and buffer reservation protocols (BuffeRS) to reduce per-hop router transit latency down to 1–2 cycles.
- **Analyze Single-Cycle & Asynchronous Frontiers**: Derive the physical hop-per-cycle ($HPC_{max}$) limit for repeated multi-hop bypassing, and evaluate asynchronous domino pipelines (HyPA) that eliminate power-hungry global clock trees.
- **Synthesize Hardware Arbiters & Crossbars**: Design $O(1)$ LRU matrix arbiters, formulate bipartite maximum matching, and evaluate iterative round-robin allocators (iSLIP) alongside multiplexer-tree crossbar fabrics.

### Chapter Roadmap & Interactive Modules
- **Section 3.1**: The Canonical Virtual-Channel Router Pipeline & Functional Decomposition.
- **Section 3.2**: Advanced Pipeline Compression, Lookahead Routing & Speculative Allocation.
- **Section 3.3**: Asynchronous Router Architectures (HyPA [[Saranya2026](#ref-saranya2026)]).
- **Section 3.4**: Single-Cycle Multi-Hop Traversal (SMART [[Krishna2013](#ref-krishna2013)] & SHARP [[SHARP2023](#ref-sharp2023)]).
- **Section 3.5**: Crossbar Arbitration Theory, Matrix Arbiters & iSLIP Matching.
- **Section 3.6**: Crossbar Switch Physical Circuit Design & Scaling.
- **Section 3.7**: Interactive Lab Challenges & Hands-on Simulators.
- **Section 3.8**: Checkpoint Assessment & Problem Sets.

---

## 3.1 The Canonical Virtual-Channel Router Pipeline

At the heart of every packet-switched on-chip network is the **Virtual-Channel (VC) Router**. The router is responsible for receiving flits from upstream links, buffering them in input queues, determining their destination routing paths, arbitrating for output physical channels, and driving flits across an internal crossbar fabric.

In a canonical synchronous architecture (such as the Dally-Peh classic model), processing each packet traverses a **five-stage pipeline**:

```mermaid
graph LR
  subgraph CanonicalPipeline ["Canonical 5-Stage Router Pipeline"]
    BW["Stage 1: BW<br/>(Buffer Write)"] --> RC["Stage 2: RC<br/>(Route Compute)"]
    RC --> VA["Stage 3: VA<br/>(VC Allocate)"]
    VA --> SA["Stage 4: SA<br/>(Switch Allocate)"]
    SA --> ST["Stage 5: ST<br/>(Switch Traversal)"]
  end
  ST --> LT["Inter-Router LT<br/>(Link Traversal)"]

  style BW fill:#fee2e2,stroke:#ef4444,stroke-width:2px;
  style RC fill:#fef3c7,stroke:#f59e0b,stroke-width:2px;
  style VA fill:#e0e7ff,stroke:#6366f1,stroke-width:2px;
  style SA fill:#dcfce7,stroke:#22c55e,stroke-width:2px;
  style ST fill:#dbeafe,stroke:#3b82f6,stroke-width:2px;
  style LT fill:#f1f5f9,stroke:#64748b,stroke-width:2px;
```

### 3.1.1 Stage-by-Stage Functional Decomposition

- **Stage 1: Buffer Write (BW)**
    - *Primary Role*: Receives incoming flits across physical inter-router link wires, decodes control headers, and writes payload bytes into the appropriate virtual channel storage slot.
    - *Microarchitectural Datapath*: Implemented using multi-queue dual-ported SRAM banks or distributed D-flip-flop register files organized per Virtual Channel (`VC_ID`). A write pointer (`wr_ptr`) increments per stored flit.
    - *Signals & Handshaking*: Evaluates incoming `flit_valid`, captures `flit_data[W-1:0]`, decodes `flit_type[1:0]` (Head, Body, Tail, Head-Tail), and extracts the target `vc_id_in`.
    - *Flit Invariant Behavior*:
        - **Head Flit**: Initializes the VC state machine from `IDLE` to `ROUTING`, latching the destination coordinate packet header for subsequent route computation.
        - **Body & Tail Flits**: Enqueued sequentially behind the Head flit; bypass route calculation and inherit existing channel state registers.
    - *Credit Management & Flow Control*: Synchronously decrements the upstream router's credit counter for this VC. If buffer occupancy reaches capacity ($depth = B_{max}$), upstream transmitters are prevented from sending further flits via credit exhaustion.
    - *Critical Path Timing*: Incurs SRAM write setup time ($t_{setup}$), address decoder propagation delay, and array cell charging delay before the flit becomes visible to internal arbitration logic.

- **Stage 2: Route Computation (RC)**
    - *Primary Role*: Resolves the output physical port (e.g., North, South, East, West, or Local) through which the packet must depart toward its final destination.
    - *Microarchitectural Datapath*: Evaluates the combinational routing function $\mathcal{R}: (C_{curr}, C_{dest}) \to P_{out}$ using fast parallel subtraction comparator slices or small lookup routing tables (LUTs).
    - *DOR Combinational Logic*: For Dimension-Order Routing (XY routing) in a 2D mesh, the hardware logic requires only two comparator blocks:
        - $\Delta X = X_{dest} - X_{curr}$: If $\Delta X > 0$, select East; if $\Delta X < 0$, select West.
        - $\Delta Y = Y_{dest} - Y_{curr}$: If $\Delta X == 0$ and $\Delta Y > 0$, select South; if $\Delta X == 0$ and $\Delta Y < 0$, select North; if both equal 0, select Local core injection/ejection.
    - *Flit Invariant Behavior*:
        - **Head Flit**: Exclusively undergoes Route Computation. Once the outgoing direction $P_{out}$ is resolved, it is written into the VC state table register (`vc_out_port <= P_out`).
        - **Body & Tail Flits**: Completely skip the RC stage! Because wormhole routing preserves packet integrity along a single path, body and tail flits automatically follow the output port established by their preceding Head flit.
    - *Pipeline Lookahead Optimization*: In modern routers, RC is performed *one hop ahead* at the upstream node (Lookahead Routing), effectively removing RC from the critical pipeline path of intermediate routers.

- **Stage 3: Virtual Channel Allocation (VA)**
    - *Primary Role*: Arbitrates among competing Head flits from multiple input ports that desire the same outgoing physical port, assigning an idle downstream Virtual Channel (`VC_ID_out`) to each winning packet.
    - *Two-Phase Separable Allocator Architecture*: Because a full $V_{in} \cdot P_{in} \times V_{out} \cdot P_{out}$ allocator is hardware-prohibitive, VA is factored into two smaller, decoupled arbitration stages:
        - *Phase 1 (Input-to-Output Request / V-to-1 Arbitration)*: At each input port, active VCs that have completed RC select one downstream candidate VC at the designated output port.
        - *Phase 2 (Output-to-Input Grant / P-to-1 Arbitration)*: At each output port, arbiters choose one winning input VC from all competing requests and return a grant signal (`va_grant`).
    - *Flit Invariant Behavior*:
        - **Head Flit**: Competes in VA. Upon winning a grant, it locks the assigned downstream `VC_ID_out` in the router state table (`vc_state <= ACTIVE_VC`).
        - **Body & Tail Flits**: Do not participate in VA; they are tagged with the previously allocated `VC_ID_out`.
    - *Resource Reservation & Release*: The assigned downstream VC remains exclusively reserved for this packet until the packet's Tail flit completes switch traversal and departs, guaranteeing that flits from different packets are never interleaved within the same virtual channel.

- **Stage 4: Switch Allocation (SA)**
    - *Primary Role*: Allocates physical access to the internal crossbar switch multiplexers on a cycle-by-cycle basis for flits that already possess a valid downstream VC and have available downstream buffer credits.
    - *Two-Stage Separable Crossbar Allocator*:
        - *Stage 1 (Input Port Arbitration)*: At each input port, an arbiter chooses one candidate flit among all local VCs that have flits ready and downstream credit count $> 0$.
        - *Stage 2 (Output Port Arbitration)*: For each physical output port, an arbiter selects one winner among the input ports that won Stage 1.
    - *Flit Invariant Behavior*:
        - **Head, Body, and Tail Flits**: All flits must win Switch Allocation individually in order to traverse the crossbar.
        - **Pipelined Streaming**: Once a Head flit wins SA, subsequent body flits can request SA in contiguous back-to-back cycles, achieving ideal single-cycle throughput under zero-contention conditions.
    - *Credit-Aware Allocation Guard*: A flit is eligible to request SA if and only if the downstream credit counter for its assigned VC is strictly positive ($Credit[P_{out}][VC_{out}] > 0$), preventing crossbar traversals that would cause downstream buffer overflows.

- **Stage 5: Switch Traversal (ST)**
    - *Primary Role*: Drives the granted flit from the input buffer storage through the internal crossbar switch fabric to the output port link registers.
    - *Microarchitectural Datapath*: The crossbar switch consists of $P$ multiplexer trees (one per output port), each selecting among $P$ input datapath buses of width $W$ bits (e.g., 64, 128, or 512 bits).
    - *Hardware Handshake & Control*: The winning grant signals from Stage 4 configure the multiplexer select lines (`xbar_sel[P_out] <= winning_input_port`).
    - *Energy & Timing Constraints*: Crossbar traversal represents a significant capacitive load due to long internal wire tracks crossing all input/output buses. High-speed drivers and intermediate pipeline registers are often placed between the multiplexer outputs and the physical link drivers.

- **Stage 6: Link Traversal (LT)**
    - *Primary Role*: Propagates physical voltage signals across the inter-router metal wires to the input registers of the neighboring downstream router.
    - *Physical Signaling*: Traverses intermediate or global metal layers (e.g., M4–M8 in standard FinFET processes) with optimal repeater insertion to maintain signal integrity and sharp edge transitions.
    - *Timing Relationship*: In short-distance local mesh topologies, LT typically completes within a single clock cycle ($t_{LT} = 1\text{ cycle}$). In long-distance express links or multi-chiplet topologies, LT may require multi-cycle pipelined links.
    - *Downstream Handshake & Credit Return*: As the flit enters the downstream router, a credit signal (`credit_out`) is pulsed backward to the upstream router, replenishing the transmitter's credit pool.

```
Figure 3.1: Canonical vs. Speculative vs. Lookahead Router Pipelines
+-----------------------------------------------------------------------------------------+
| Canonical (5 Cycles):      | BW | RC | VA | SA | ST | LT |                             |
+-----------------------------------------------------------------------------------------+
| Lookahead RC (4 Cycles):   | BW | -- | VA | SA | ST | LT |  (RC evaluated at hop N-1)   |
+-----------------------------------------------------------------------------------------+
| Speculative SA (3 Cycles): | BW | -- | VA || SA | ST | LT |  (VA & SA in parallel)      |
+-----------------------------------------------------------------------------------------+
| Low-Latency Bypass (1 Cyc):| Bypassed straight through crossbar: [ ST || LT ]          |
+-----------------------------------------------------------------------------------------+
```

---

## 3.2 Advanced Pipeline Compression & Router Bypassing

Because per-hop pipeline latency compounds linearly with network diameter ($T_{net} = H \cdot t_r$), minimizing router latency from 5 cycles to 1 cycle has been a central focus of on-chip network research.

![Figure 3.1: Multicycle router pipeline versus BuffeRS router pipeline](figures/buffers_fig01_pipeline.png)
*Figure 3.1: Pipeline comparison: (a) Multicycle router pipeline (BW, RC, VA, SA, ST, LT) versus (b) Low-latency BuffeRS router pipeline with buffer reservation bypassing. [Reproduced from: Z. Liu, X. Wu, and Y. Ye, "BuffeRS: A Buffer Reservation Scheduling Strategy for Router Bypassing in NoCs and Multichiplet Networks," IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, vol. 45, no. 6, pp. 2635–2648, June 2026, DOI: 10.1109/TCAD.2025.3624677. © 2026 IEEE]*

### 3.2.1 Lookahead Routing
- **Core Principle & Hop Shift**: Standard routers evaluate output port direction upon packet arrival, imposing a full-cycle Route Computation stage. Under Lookahead Routing, router $N$ computes the routing decision for router $N+1$ *in advance*, while the flit is buffered or traversing hop $N$.
- **Header Field Encoding**: The computed downstream port direction (encoded as a 3-bit or 5-bit one-hot mask) is embedded directly into the Head flit's header before crossing the physical link.
- **Immediate VA Activation**: Upon arrival at router $N+1$, the outgoing port is already known combinatorially from the packet header, enabling Virtual Channel Allocation to initiate immediately in cycle 1.
- **Latency & Critical Path Benefit**: Completely eliminates the RC pipeline stage at every intermediate hop, compressing a 5-stage canonical router to 4 stages with negligible silicon area overhead.

### 3.2.2 Speculative Switch Allocation [[Peh2001](#ref-peh2001)]
- **Optimistic Resource Request**: In low-to-medium network load regimes, downstream virtual channel contention is infrequent. Speculative Switch Allocation [[Peh2001](#ref-peh2001)] exploits this by scheduling Virtual Channel Allocation (VA) and Switch Allocation (SA) concurrently in the same clock cycle.
- **Dual-Path Speculative Request Logic**: The Head flit requests an output crossbar port *speculatively*, assuming that its simultaneous request for a downstream VC will succeed.
- **Validation & Conflict Resolution**:
    - *Both Succeed*: If VA grants a downstream VC and speculative SA grants crossbar access, the flit immediately proceeds to Switch Traversal (ST) in cycle 2, compressing pipeline latency to 2 cycles.
    - *VA Contention Mis-prediction*: If VA fails due to VC exhaustion, the speculative SA grant is suppressed and squashed, preventing unauthorized crossbar traversal.
    - *Priority Rules*: Non-speculative requests (from body flits that already possess valid VCs) are given strict priority over speculative Head flit requests to eliminate pipeline stalls for ongoing flows.
- **Silicon Trade-Offs**: Delivers near-single-cycle zero-load latencies under light traffic, but incurs higher allocator power dissipation due to wasted speculative grant computations under saturation loads.

### 3.2.3 Buffer Reservation Scheduling: BuffeRS [[Liu2026](#ref-liu2026)]

As formulated by Liu et al. [[Liu2026](#ref-liu2026)], **BuffeRS** solves the fundamental flaw of prior bypass architectures:

- **The Classical Bypassing Dilemma**: Traditional router bypassing mechanisms (such as SMART [[Krishna2013](#ref-krishna2013)], NoRD) allow flits to skip input buffering and crossbars. However, when bypass flits arrive at downstream nodes only to find input queues completely saturated, they suffer abrupt pipeline stalls, deflections, or packet drops.
- **Time-Division Pre-Allocation**: BuffeRS establishes a coordinated **buffer reservation scheduling strategy** that reserves destination buffer slots *in advance* across router groups before initiating traversal.
- **Two-Phase Reservation Protocol**:
    - *Reservation Phase*: A lightweight 1-bit lookahead token traverses ahead of the packet payload to claim a free buffer slot at the downstream destination tile.
    - *Bypass Phase*: The packet payload flits traverse through intermediate router crossbars in a single clock cycle without stopping, guaranteed that a reserved buffer slot awaits them at the terminating node.
- **Multi-Chiplet Interconnect Suitability**: Highly resilient across high-latency die-to-die (D2D) packaging boundaries, preventing credit turnaround latency loops from throttling inter-chiplet throughput.

#### Table 3.1: Quantitative Comparison of High-Performance Router Microarchitectures
| Architecture Paradigm | Pipeline Stages | Allocation Scheme | Clocking / Timing Strategy | Key Silicon Trade-Off |
| :--- | :--- | :--- | :--- | :--- |
| **Canonical VC Router** [[Peh2001](#ref-peh2001)] | 4–5 cycles | Separable VA + SA | Fully Synchronous | Baseline area; multi-cycle per-hop serialization delay |
| **Lookahead Routing** | 3 cycles | Lookahead RC + SA | Fully Synchronous | Strips RC stage; minimal packet header overhead |
| **Speculative Allocator** [[Peh2001](#ref-peh2001)] | 2 cycles | Parallel speculative VA/SA | Fully Synchronous | Speculation mis-predictions stall under heavy injection |
| **SMART** [[Krishna2013](#ref-krishna2013)] / **SHARP** [[SHARP2023](#ref-sharp2023)] | 1–2 cycles | Priority bypass muxes | Multi-hop async bypass | Bounded by physical $HPC_{max}$ wire RC delay budget |
| **HyPA Router** [[Saranya2026](#ref-saranya2026)] | 0.8 ns / hop | Handshake pipeline | GALS Asynchronous domino | 62% lower power; eliminates global clock tree distribution |
| **BuffeRS** [[Liu2026](#ref-liu2026)] | 1 cycle | Buffer reservation slots | Time-division coordinated | Deterministic zero-contention bypass; token reservation logic |

---

## 3.3 Asynchronous Router Architectures: HyPA [[Saranya2026](#ref-saranya2026)]

In large-scale Multi-Processor Systems-on-Chip (MPSoCs), distributing a single low-skew global clock across a $20\text{ mm} \times 20\text{ mm}$ die is prohibitively expensive in clock-tree power and timing closure complexity.

![Figure 3.2: Detailed microarchitecture of the HyPA asynchronous router](figures/hypa_fig02_microarch.png)
*Figure 3.2: Detailed microarchitecture of the proposed asynchronous router featuring a high-throughput domino-logic pipeline template with one-hot hybrid data encoding. [Reproduced from: M. N. Saranya, C. T. Avinash, and R. Rao, "HyPA: A Low-Latency Hybrid Pipeline Asynchronous Router for Network-on-Chip Architectures in GALS-Based SoCs," IEEE Transactions on Very Large Scale Integration (VLSI) Systems, vol. 34, 2026, DOI: 10.1109/TVLSI.2026.3716692. © 2026 IEEE]*

In **Globally Asynchronous Locally Synchronous (GALS)** systems, asynchronous routers eliminate clock trees entirely:
- **HyPA Router** (Saranya et al. [[Saranya2026](#ref-saranya2026)]): Implemented in 65nm CMOS, HyPA employs a **hybrid pipeline asynchronous architecture** based on high-throughput domino logic.
- **Power and Energy Gains**: Benchmarked against synchronous clock-gated routers, HyPA demonstrates **62% lower power consumption** and an **85% reduction in energy-per-flit**, achieving a forward latency of **0.8 ns** and a throughput of **1.65 GFlits/port/s**.

---

## 3.4 Single-Cycle Multi-Hop Traversal: SMART & SHARP

In 2013, Krishna et al. [[Krishna2013](#ref-krishna2013)] introduced **SMART** (Single-Cycle Multi-hop Asynchronous Repeated Traversal), demonstrating that a flit can traverse **multiple physical router crossbars and links within a single clock cycle** when no contention exists.

![Figure 3.3: Preemption and stopping cases in priority-preemptive single-cycle multi-hop routers](figures/sharp_fig02_bypass_limit.png)
*Figure 3.3: Preemption stopping cases at intermediate routers for contending flows in priority-preemptive single-cycle multi-hop traversal networks under hop limits ($HPC_{max} = 3$). [Reproduced from: IEEE Transactions on Very Large Scale Integration (VLSI) Systems, 2023, DOI: 10.1109/TVLSI.2023.3298101. © 2023 IEEE]*

As illustrated in Figure 3.3, single-cycle traversal is physically bounded by:

- **Clock Period Timing Budget ($HPC_{max}$)**:
    - Wire propagation delay and multiplexer gate delays accumulate along the bypassed path:
      $$t_{hop} = t_{crossbar\_mux} + t_{wire\_propagation} + t_{repeater}$$
    - The maximum traversable hops per cycle is strictly bounded by the clock cycle time:
      $$HPC_{max} = \left\lfloor \frac{T_{clk} - t_{setup}}{t_{hop}} \right\rfloor$$
    - At 1.0 GHz ($T_{clk} = 1.0\text{ ns}$) in 14nm FinFET, $HPC_{max}$ typically allows 3 to 5 hops before requiring intermediate latching.
- **Dynamic Flow Contention & Preemption**:
    - Local flits at intermediate nodes may contend for an output port that a distant bypass packet is attempting to cut through.
    - Priority-preemptive arbitration protocols dictate whether the traversing bypass flow preempts local traffic or stops and buffers in place.
- **Asynchronous Bypass Setup Signals**:
    - Dedicated lookahead request wires run parallel to data links, configuring bypass multiplexers in intermediate routers a fraction of a cycle before the packet payload arrives.

---

## 3.5 Crossbar Arbitration Theory & Matching Algorithms

Inside every router, crossbar allocation resolves contention when multiple input ports simultaneously request the same output port. This is formalized as the **Bipartite Maximum Matching Problem**:

```mermaid
graph LR
  subgraph InputPorts ["N Input Ports"]
    I0["Input 0"]
    I1["Input 1"]
    I2["Input 2"]
    I3["Input 3"]
  end

  subgraph OutputPorts ["N Output Ports"]
    O0["Output 0"]
    O1["Output 1"]
    O2["Output 2"]
    O3["Output 3"]
  end

  I0 -. Request .-> O0
  I0 -. Request .-> O1
  I1 -. Request .-> O0
  I2 -. Request .-> O2
  I3 -. Request .-> O2
  I3 -. Request .-> O3

  I0 === Match ===> O1
  I1 === Match ===> O0
  I2 === Match ===> O2
  I3 === Match ===> O3
```

Given $N$ input ports and $N$ output ports, the objective is to find a mapping $\mathcal{M} \subset I \times O$ subject to:
- **Input Uniqueness**: Each input $i \in I$ is mapped to at most one output ($\sum_{j} m_{i,j} \le 1$).
- **Output Uniqueness**: Each output $o \in O$ is mapped to at most one input ($\sum_{i} m_{i,j} \le 1$).
- **Cardinality Maximization**: Total matched pairs $|\mathcal{M}| = \sum_{i,j} m_{i,j}$ is maximized.
- **Fairness & Anti-Starvation**: Every requesting port is guaranteed access within a bounded number of arbitration cycles.

### 3.5.1 The Matrix Arbiter: Strict $O(1)$ Hardware LRU
The **Matrix Arbiter** is the gold standard for high-speed, fair arbitration among $N$ competing clients. It maintains an $N \times N$ triangular binary priority matrix $M$:

$$\text{Priority Matrix: } M[i][j] = \begin{cases} 
1 & \text{if Client } i \text{ has higher priority than Client } j \\ 
0 & \text{if Client } j \text{ has higher priority than Client } i 
\end{cases}$$

#### Microarchitectural Properties & Invariants:
- **Anti-Symmetry Property**: $M[i][j] = \overline{M[j][i]}$ for all $i \ne j$.
- **Diagonal Zero Invariant**: $M[i][i] = 0$ for all $i$, requiring storage for only $\frac{N(N-1)}{2}$ state flip-flops.
- **Two-Gate-Level Combinational Grant**: Client $i$ is granted if it asserts request $R_i$ and holds priority over all other active requesters:
  $$G_i = R_i \cdot \prod_{j \ne i} (\overline{R_j} + M[i][j])$$
  This evaluates in exactly two gate levels (an inverter/OR array followed by an $N$-input AND gate), making it exceptionally fast for $N \le 8$.
- **Single-Cycle LRU State Transition**:
    - When client $k$ wins the grant ($G_k = 1$), it immediately drops to the **Least Recently Used (LRU)** rank.
    - **Row $k$ is cleared to zero**: $M[k][j] \leftarrow 0 \quad (\forall j \ne k)$, removing priority over all peers.
    - **Column $k$ is set to one**: $M[i][k] \leftarrow 1 \quad (\forall i \ne k)$, ensuring all peers now take priority over client $k$.
- **Absolute Starvation Freedom**: In a system of $N$ requesters, no asserted request can wait more than $N-1$ arbitration rounds before winning.

```
Table 3.1: 4-Port Matrix Arbiter Priority State Evolution Under Continuous Contention
+-------+------------------+-------------------------+---------------+----------------------------+
| Cycle | Requests (R)     | Priority Matrix M       | Granted Winner| State Update Action        |
+-------+------------------+-------------------------+---------------+----------------------------+
| 0     | Initial State    | [0, 1, 1, 1]            | --            | Initial: 0 > 1 > 2 > 3     |
|       |                  | [0, 0, 1, 1]            |               |                            |
|       |                  | [0, 0, 0, 1]            |               |                            |
|       |                  | [0, 0, 0, 0]            |               |                            |
+-------+------------------+-------------------------+---------------+----------------------------+
| 1     | R = [1, 1, 0, 1] | Row 0 has all 1s over R | Client 0 Wins | Row 0 -> 0s, Col 0 -> 1s   |
| 2     | R = [1, 1, 0, 1] | Row 1 has priority over3| Client 1 Wins | Row 1 -> 0s, Col 1 -> 1s   |
| 3     | R = [1, 1, 0, 1] | Row 3 has priority over0| Client 3 Wins | Row 3 -> 0s, Col 3 -> 1s   |
| 4     | R = [1, 1, 0, 1] | Matrix has cycled fully | Client 0 Wins | Strict 100% Round-Robin LRU|
+-------+------------------+-------------------------+---------------+----------------------------+
(Simulated via code/matrix_arbiter_islip_sim.py)
```

### 3.5.2 McKeown's iSLIP Iterative Matching Algorithm [[McKeown1999](#ref-mckeown1999)]
For a complete $N \times N$ crossbar switch, separable allocation using independent input and output arbiters can leave up to 50% of crossbar ports idle under heavy traffic due to conflicting uncoordinated grants.

In 1999, Nick McKeown [[McKeown1999](#ref-mckeown1999)] introduced **iSLIP** (*Iterative Serial round-robin with SLIP*), an algorithm widely implemented in high-radix routers and internet switches:

#### The Three-Phase Iterative Protocol:
- **Phase 1: Parallel Request Generation**:
    - Each unmatched input port asserts request lines to every output port for which it holds at least one buffered flit.
- **Phase 2: Output-Side Round-Robin Grant**:
    - Each unmatched output port arbitrates among contending input requests using an independent round-robin pointer $g_j$.
    - The output asserts a tentative grant signal to the winning input. The pointer $g_j$ is **not updated yet**.
- **Phase 3: Input-Side Round-Robin Accept**:
    - Each unmatched input port arbitrates among all tentative grants it received using an independent accept pointer $a_i$.
    - The input accepts exactly one grant, establishing a confirmed input-output crossbar match $(\mathcal{M} \leftarrow \mathcal{M} \cup \{(i, j)\})$.
- **Pointer Update Invariant (The SLIP Principle)**:
    - Output grant pointers $g_j$ and input accept pointers $a_i$ are updated **if and only if** the match is accepted in the **very first iteration**:
      $$g_j \leftarrow (i + 1) \pmod N, \quad a_i \leftarrow (j + 1) \pmod N$$
    - Restricting updates strictly to iteration 1 prevents arbiters from falling into synchronized lockstep states under high offered load, de-correlating request patterns and maximizing entropy.

#### Convergence & Throughput Theorems:
- **Theorem 1 (Fast Convergence [[McKeown1999](#ref-mckeown1999)])**:
    - For an $N \times N$ crossbar switch, iSLIP converges to a maximal matching in at most $\min(N, \log_2 N)$ iterations.
    - In silicon, **2 iterations** achieve over **94% crossbar efficiency**, and **4 iterations** achieve **100% maximal matching** even under continuous 100% offered injection.
- **Theorem 2 (Starvation Freedom & 100% Saturation Throughput)**:
    - Under uniform independent and identically distributed (i.i.d.) traffic, iSLIP delivers **100% throughput** without internal switch speedup, guaranteeing that no input port is starved indefinitely.

---

## 3.6 Crossbar Switch Physical Circuit Design

The crossbar switch is the physical datapath hub connecting the $P$ input ports to the $P$ output ports ($P = 5$ for a standard 2D mesh: North, South, East, West, Local).

```
Crossbar Multiplexer Tree (Per Output Bit):
Input 0 Data ----[ MUX ]----+
Input 1 Data ----[     ]    |
                            +----[ MUX ]----> Output Port Data Line
Input 2 Data ----[ MUX ]----+
Input 3 Data ----[     ]
```

### 3.6.1 Area and Capacitance Scaling
- **Crosspoint Switch Complexity**: Scales quadratically with port count $P$ as $P^2 \times W$ transmission gates, tri-state buffers, or multiplexer cells, where $W$ is the flit datapath bit width (e.g., 64–512 bits).
- **Silicon Metal Track Area**: Consumes $2 \cdot P \cdot W \cdot \text{pitch}_{metal}$ wiring track area, creating significant routing density congestion on intermediate metal layers (M3–M5).
- **Capacitive Loading & Energy Scaling**:
    - Dynamic switching power is governed by:
      $$P_{xbar} = \alpha \cdot C_{xbar\_wire} \cdot V_{dd}^2 \cdot f_{clk}$$
    - As port count $P$ exceeds 8 (e.g., in high-radix Dragonfly routers with $P = 16\text{–}32$), long internal crossbar wire capacitance dominates router dynamic power.
- **Hierarchical Sub-Crossbars**: High-radix designs mitigate quadratic area and power penalties by replacing monolithic crossbars with **hierarchical two-stage crossbars** or bit-sliced matrix sub-blocks.

---

## 3.7 Interactive Lab & Hands-on Challenges

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.35), rgba(15, 23, 42, 0.65)); border: 1px solid rgba(59, 130, 246, 0.5); border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #93c5fd; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;">
      <span>⚡ Dedicated Interactive Lab: Arbiter Simulator &amp; Mesh Visualizer</span>
    </div>
    <div style="font-size: 0.92rem; color: #e2e8f0; margin-top: 6px; max-width: 800px; line-height: 1.5;">
      Schedule competing flits across $5 \times 5$ crossbars, compare sub-200ps LRU matrix arbiters with iSLIP, and optimize canonical 4-stage pipeline traversals.
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="../../interactive/arbiter/" style="display: inline-flex; align-items: center; gap: 6px; background: #ea580c; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Enter Arbiter Simulator →</span>
    </a>
    <a href="../../interactive/visualizer/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>2D Mesh Pipeline Visualizer →</span>
    </a>
  </div>
</div>

Complete the following three hands-on laboratory missions in **[Arbiter Simulator](../../interactive/arbiter.md)** and **[2D Mesh Visualizer](../../interactive/visualizer.md)**:

### Challenge Mission 3.1: Arbiter Fairness & Starvation Freedom Under Adversarial Traffic
- **Objective:** Compare Strict Priority, Round-Robin, and Triangular Matrix Arbiters under persistent contention on output port East.
- **Setup & Procedure:**
  1. In **Arbiter Simulator**, select `Strict Priority` and configure Requestors 0, 1, 2, and 3 to continuously request output port 0.
  2. Observe service grants over 20 clock cycles.
  3. Switch to `Matrix Arbiter (Least-Recently-Used / LRU)` and repeat.
- **Architectural Observation:** Under Strict Priority, Requestors 1, 2, and 3 suffer complete starvation: Requestor 0 monopolizes 100% of the grants. Under the Matrix Arbiter, the upper triangular state matrix $M[i][j]$ is dynamically updated on every grant ($M[grant][*] \leftarrow 0$, $M[*][grant] \leftarrow 1$), guaranteeing mathematical Least-Recently-Used (LRU) fairness and bounded service latency ($T_{max} \le N-1$ cycles) with sub-200ps combinational gate delay.
- **Verification Formula:** $G_k = R_k \cdot \prod_{j \ne k} (\overline{R_j} + M_{k,j})$.

### Challenge Mission 3.2: 2-Stage Speculative VA/SA Parallel Allocation
- **Objective:** Evaluate how speculative allocation compresses canonical 4-stage router latency into a 2-stage pipeline under low-to-medium traffic.
- **Setup & Procedure:**
  1. Launch the **2D Mesh Visualizer** with Uniform Random traffic at injection rate $\lambda = 0.1\text{ flits/cycle/node}$.
  2. Inspect the flit progression timeline: Head flits arbitrate for Switch Allocation (SA) in parallel with Virtual Channel Allocation (VA), assuming a free downstream VC will be successfully acquired.
  3. Increase injection rate to saturation ($\lambda = 0.5$) and observe mis-speculation frequency.
- **Architectural Observation:** Under light traffic, VC contention is near zero: speculation succeeds $>95\%$ of the time, reducing zero-load router traversal latency from 4 cycles down to 2 cycles. At saturation, VC conflicts cause speculation failures, requiring flits to kill their switch grants and re-arbitrate in non-speculative mode.

### Challenge Mission 3.3: SMART Single-Cycle Multi-Hop Bypass Traversals
- **Objective:** Observe how asynchronous crossbar bypass paths (SMART) bypass intermediate router buffering and arbitration entirely.
- **Setup & Procedure:**
  1. In **2D Mesh Visualizer**, enable SMART bypass routing with maximum hop limit $H_{max} = 4$.
  2. Send a 4-hop packet from $(0,0)$ to $(0,3)$ along dimension X.
  3. Measure the end-to-end network latency.
- **Architectural Observation:** In a conventional router, a 4-hop traversal incurs $4 \times t_{router} = 12\text{–}16$ clock cycles. With SMART bypass enabled, downstream arbiters pre-allocate their crossbars via dedicated lookahead wires, allowing the flit to traverse up to 4 routers in a single clock cycle ($t_{net} = 1 + H \cdot t_{wire}$), drastically flattening the zero-load latency curve toward wire speed!
- **Hardware RTL & Python Reference:** Run `python code/router_pipeline_sim.py` and inspect `code/matrix_arbiter_4x4.v` for synthesizable 4-port matrix arbitration Verilog.

---

## 3.8 Checkpoint Assessment

Test your mastery of Chapter 3 concepts against the official certification questions (mirroring the 3-Tier Exam Engine in [`quiz.md`](../../quiz.md)):

#### Question 3.1 (Tier 1: Fundamental)
*In a canonical 5-stage Virtual Channel router (BW -> RC -> VA -> SA -> ST), which pipeline stages are traversed by Body and Tail flits, and why? (Select all that apply)*

- **A)** Body and Tail flits only traverse 3 stages: Buffer Write (BW), Switch Allocation (SA), and Switch Traversal (ST).
- **B)** Route Computation (RC) is skipped because the output port was already computed by the Head flit.
- **C)** Virtual Channel Allocation (VA) is skipped because Body and Tail flits inherit the VC granted to the Head flit.
- **D)** Body and Tail flits must re-execute Route Computation (RC) to verify packet integrity.

??? success "Reveal Answer & Full Solution"
    **Correct Answer: Option A, B, C**

    **1. Step-by-Step Architectural & Mathematical Derivation:**
    In wormhole routing with Virtual Channels, packet processing is asymmetric: (1) Head Flit: Contains destination address routing headers. It must perform Buffer Write (BW), compute the output direction during Route Computation (RC), arbitrate for and secure a free downstream Virtual Channel during VC Allocation (VA), arbitrate for the crossbar during Switch Allocation (SA), and traverse the crossbar switch (ST)—taking 5 cycles. (2) Body & Tail Flits: Contain only data payloads and packet demarcation flags (e.g. Tail bit). Because the Head flit already reserved the output port and the downstream VC ID, trailing flits bypass RC and VA entirely. Upon arrival, they perform BW (1 cycle), request Switch Allocation (SA, 1 cycle) using the pre-assigned VC and output port, and traverse the crossbar (ST, 1 cycle). Thus, trailing flits require only 3 cycles (BW -> SA -> ST). The Tail flit additionally deallocates the downstream VC upon leaving ST.

    **2. Option-by-Option Breakdown & Distractor Analysis:**
    - **Option A (Correct):** True. Body and Tail flits only execute BW -> SA -> ST, compressing their per-hop pipeline latency to 3 cycles.
    - **Option B (Correct):** True. The output direction is preserved in the VC state register from the Head flit's RC stage.
    - **Option C (Correct):** True. Downstream VC allocation is held open for the entire packet until the Tail flit clears the router.
    - **Option D (Incorrect Distractor):** False. Body flits do not carry routing headers and cannot perform Route Computation.

    **3. Silicon Architect's Takeaway:**
    Head flits establish the network path (RC & VA); body flits stream through using pre-allocated VC state (BW -> SA -> ST).

    *(Reference: [[Peh2001](#ref-peh2001)] L.-S. Peh and W. J. Dally, "A Delay Model and Speculative Architecture for Pipelined Routers," HPCA, pp. 255–266, 2001. DOI: 10.1109/HPCA.2001.903268.)*

#### Question 3.2 (Tier 2: Core Engineering)
*In a hardware Matrix Arbiter implementing Least-Recently-Used (LRU) priority, how many flip-flops are required to store the priority state for an N-input arbiter, and what is its maximum grant evaluation latency?*

- **A)** N^2 flip-flops; evaluation takes N cycles using an iterative counter.
- **B)** N*(N - 1)/2 flip-flops; grant evaluation is purely combinational, executing in O(log N) gate delays.
- **C)** N flip-flops; evaluation requires an analog integrator.
- **D)** 2^N flip-flops; evaluation is non-deterministic.

??? success "Reveal Answer & Full Solution"
    **Correct Answer: Option B**

    **1. Step-by-Step Architectural & Mathematical Derivation:**
    An N-input Matrix Arbiter maintains a priority relationship between every distinct pair of requestors (i, j). Because priority is strictly asymmetric (if i has priority over j, then j cannot have priority over i: M[j, i] = NOT M[i, j]) and irreflexive (M[i, i] = 0), only the upper triangular elements of matrix M need to be physically stored in flip-flops. The number of stored bits is precisely N * (N - 1) / 2 flip-flops (e.g. 5*(4)/2 = 10 flip-flops for a 5-port router). The lower triangular elements are generated by simple inversion logic: M[j, i] = ~M[i, j]. The grant signal for requestor i is computed combinatorially: Grant[i] = Req[i] & [AND_{j != i} (~Req[j] | M[i, j])]. Using balanced tree logic, the multi-input AND gate executes in O(log N) gate delays (typically < 150 ps in 16nm/7nm standard cell libraries), enabling single-cycle switch allocation even at frequencies above 2 GHz.

    **2. Option-by-Option Breakdown & Distractor Analysis:**
    - **Option A (Incorrect Distractor):** Storing the full N^2 matrix wastes registers; diagonal is 0 and lower triangle is the exact inverse of upper triangle. Evaluation is single-cycle combinational, not N cycles.
    - **Option B (Correct):** Storing only the upper triangular matrix requires N(N-1)/2 flip-flops and evaluates combinatorially in O(log N) gate depth.
    - **Option C (Incorrect Distractor):** N bits are insufficient to track general LRU permutations among N requestors, and analog integrators are not used in digital arbiters.
    - **Option D (Incorrect Distractor):** 2^N represents exponential complexity, which is completely inaccurate for a priority matrix.

    **3. Silicon Architect's Takeaway:**
    Matrix arbiters provide strict, mathematically fair LRU arbitration with only N(N-1)/2 registers and sub-nanosecond combinational evaluation.

    *(Reference: W. J. Dally and B. Towles, Principles and Practices of Interconnection Networks, Chapter 18, Morgan Kaufmann, 2004.)*

#### Question 3.3 (Tier 3: Silicon Mastery)
*In Nick McKeown's iSLIP crossbar scheduling algorithm, why do the grant arbiters update their round-robin priority pointers ONLY when the grant is accepted by an input port in the subsequent phase?*

- **A)** To prevent grant pointers from desynchronizing and causing crossbar electrical shorts.
- **B)** To ensure that an output port only moves its priority pointer when a connection is actually established; updating on rejected grants causes pointer synchronization, collapsing crossbar matching throughput down to ~63%.
- **C)** Because grant arbiters are implemented in read-only memory (ROM).
- **D)** Because the IEEE 802.3 standard mandates frozen pointers under bursty traffic.

??? success "Reveal Answer & Full Solution"
    **Correct Answer: Option B**

    **1. Step-by-Step Architectural & Mathematical Derivation:**
    The iSLIP algorithm operates in three iterative phases: (1) Request: Inputs send requests to all outputs for which they have queued packets. (2) Grant: Each output selects one request using a round-robin arbiter with pointer g_i. (3) Accept: Each input receives multiple grants and selects one using an accept arbiter with pointer a_j. The critical breakthrough of iSLIP over prior algorithms (like SLIP) is the exact pointer update rule: The grant pointer g_i is updated (g_i = (selected + 1) mod N) IF AND ONLY IF the input port actually ACCEPTS the grant in phase 3. If an output grants to input k, but input k rejects the grant (because input k accepted a grant from another output), the output's pointer g_i REMAINS UNCHANGED. McKeown mathematically proved that updating pointers on unaccepted grants causes output pointers to lock in lockstep (synchronization), where multiple outputs repeatedly compete for the same input, throttling matching throughput to 1 - 1/e ~ 63.2%. Conditional updating forces pointers to desynchronize, achieving 100% sustained throughput under uniform traffic in O(log N) iterations.

    **2. Option-by-Option Breakdown & Distractor Analysis:**
    - **Option A (Incorrect Distractor):** Desynchronized pointers are actually the desired operational goal; crossbars cannot short-circuit because input/output multiplexers are mutually exclusive.
    - **Option B (Correct):** Updating pointers only on accepted grants maintains desynchronization among output arbiters, preventing the 63.2% throughput collapse.
    - **Option C (Incorrect Distractor):** Round-robin pointers are updated registers (flip-flops), not static ROM.
    - **Option D (Incorrect Distractor):** IEEE 802.3 governs Ethernet LANs, not on-chip crossbar switch schedulers.

    **3. Silicon Architect's Takeaway:**
    In crossbar switch allocation, conditional pointer updating guarantees arbiter desynchronization, achieving near-100% throughput without starvation.

    *(Reference: [[McKeown1999](#ref-mckeown1999)] N. McKeown, "The iSLIP Scheduling Algorithm for Input-Queued Switches," IEEE/ACM Transactions on Networking, Vol. 7, No. 2, pp. 188–201, Apr. 1999. DOI: 10.1109/90.769767.)*

---

### Modern Router Innovations: Asynchrony, WRR Bounds, and In-Network Compute
<a id="modern-innovations"></a>

Recent microarchitectural research has expanded router functionality beyond conventional packet forwarding:
- **Weighted Round-Robin (WRR) Delay Optimization**: To guarantee strict quality-of-service (QoS) in heterogeneous SoCs, Jafari et al. [[Jafari2016WRR](#ref-jafari2016wrr)] and Mandal et al. [[Mandal2023WRR](#ref-mandal2023wrr)] formalized analytical configurations for WRR arbiters, deriving tight upper bounds on worst-case packet latency and enabling predictable network performance for mission-critical flows.
- **Asynchronous Hybrid Pipelines**: Saranya et al. [[Saranya2026HyPA](#ref-saranya2026hypa)] introduced HyPA, a low-latency hybrid pipeline asynchronous router for Globally Asynchronous Locally Synchronous (GALS) SoCs, combining bundled-data clockless crossbars with speculative reservation to achieve single-cycle zero-load traversal.
- **Synchronization-Aware Crossbar Arbitration**: Addressing tail latency in parallel barrier primitives, Fan et al. [[Fan2024Sync](#ref-fan2024sync)] proposed synchronization-aware arbitration policies that prioritize flits from straggler threads, improving multi-threaded speedups by up to $22\\%$.
- **Power-Aware Built-In Self-Test (BIST)**: Scalable test-delivery architectures by Xiang et al. [[Xiang2011Test](#ref-xiang2011test)] and Agrawal et al. [[Agrawal2014Test](#ref-agrawal2014test)] utilize unicast-based multicast routing mechanisms across the NoC to distribute manufacturing test patterns to embedded IP cores without exceeding peak chip thermal limits.
- **In-Network Neuromorphic Processing**: Li et al. [[Li2024Neuro](#ref-li2024neuro)] demonstrated partial-sum routers for Spiking Neural Networks (SNNs), performing in-flight synaptic weight reductions inside router crossbars to achieve an ultra-low energy footprint of $1.63\\text{ pJ/SOP}$.

---

## References & Bibliography

<a id="references"></a>

1. <a id="ref-mckeown1999"></a>**[McKeown1999]** N. McKeown, "The iSLIP Scheduling Algorithm for Input-Queued Switches," *IEEE/ACM Transactions on Networking*, vol. 7, no. 2, pp. 188–201, Apr. 1999. [DOI: 10.1109/90.769767](https://doi.org/10.1109/90.769767).
2. <a id="ref-tamir1993"></a>**[Tamir1993]** Y. Tamir and H.-C. Chi, "Symmetric Banyan Networks for High-Performance Packet Switches," *IEEE Transactions on Computers*, vol. 42, no. 8, pp. 933–947, Aug. 1993. [DOI: 10.1109/12.238484](https://doi.org/10.1109/12.238484).
3. <a id="ref-peh2001"></a>**[Peh2001]** L.-S. Peh and W. J. Dally, "A Delay Model and Speculative Architecture for Pipelined Routers," in *Proceedings of the 7th International Symposium on High-Performance Computer Architecture (HPCA)*, 2001, pp. 255–266. [DOI: 10.1109/HPCA.2001.903268](https://doi.org/10.1109/HPCA.2001.903268).
4. <a id="ref-krishna2013"></a>**[Krishna2013]** T. Krishna, C.-H. O. Chen, W. C. Kwon, and L.-S. Peh, "Single-Cycle Multi-Hop Asynchronous Repeated Traversal: A Case for Asynchronous Logic in On-Chip Networks," in *Proceedings of the 46th Annual IEEE/ACM International Symposium on Microarchitecture (MICRO)*, 2013, pp. 336–348. [DOI: 10.1145/2540708.2540737](https://doi.org/10.1145/2540708.2540737).
5. <a id="ref-liu2026"></a>**[Liu2026]** Z. Liu, X. Wu, and Y. Ye, "BuffeRS: A Buffer Reservation Scheduling Strategy for Router Bypassing in NoCs and Multichiplet Networks," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 45, no. 6, pp. 2635–2648, June 2026. [DOI: 10.1109/TCAD.2025.3624677](https://doi.org/10.1109/TCAD.2025.3624677).
6. <a id="ref-saranya2026"></a>**[Saranya2026]** M. N. Saranya, C. T. Avinash, and R. Rao, "HyPA: A Low-Latency Hybrid Pipeline Asynchronous Router for Network-on-Chip Architectures in GALS-Based SoCs," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 34, 2026. [DOI: 10.1109/TVLSI.2026.3716692](https://doi.org/10.1109/TVLSI.2026.3716692).
7. <a id="ref-sharp2023"></a>**[SHARP2023]** "Reduced Worst-Case Communication Latency Using Single-Cycle Multihop Traversal Network-on-Chip," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 31, no. 10, pp. 1560–1572, Oct. 2023. [DOI: 10.1109/TVLSI.2023.3298101](https://doi.org/10.1109/TVLSI.2023.3298101).
8. <a id="ref-howard2011"></a>**[Howard2011]** J. Howard et al., "A 48-Core IA-32 Message-Passing Processor with DVFS in 45nm CMOS," *IEEE Journal of Solid-State Circuits*, vol. 46, no. 1, pp. 173–183, Jan. 2011. [DOI: 10.1109/JSSC.2010.2079496](https://doi.org/10.1109/JSSC.2010.2079496).
9. <a id="ref-jafari2016wrr"></a>**[Jafari2016WRR]** F. Jafari, M. Daneshtalab, and A. Jantsch, "Weighted Round Robin Configuration for Worst-Case Delay Optimization in Network-on-Chip," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 24, no. 5, pp. 1915–1928, May 2016. [DOI: 10.1109/TVLSI.2015.2477810](https://doi.org/10.1109/TVLSI.2015.2477810).
10. <a id="ref-mandal2023wrr"></a>**[Mandal2023WRR]** S. K. Mandal et al., "Fast Performance Analysis for NoCs With Weighted Round-Robin Arbitration," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 31, no. 8, pp. 1180–1193, Aug. 2023. [DOI: 10.1109/TVLSI.2023.3281050](https://doi.org/10.1109/TVLSI.2023.3281050).
11. <a id="ref-saranya2026hypa"></a>**[Saranya2026HyPA]** M. N. Saranya, C. T. Avinash, and R. Rao, "HyPA: A Low-Latency Hybrid Pipeline Asynchronous Router for Network-on-Chip," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 34, no. 3, pp. 750–763, Mar. 2026. [DOI: 10.1109/TVLSI.2026.3716692](https://doi.org/10.1109/TVLSI.2026.3716692).
12. <a id="ref-fan2024sync"></a>**[Fan2024Sync]** W. Fan et al., "Communication Synchronization-Aware Arbitration Policy in NoC for Heterogeneous Computing Systems," *IEEE Transactions on Circuits and Systems II: Express Briefs*, vol. 71, no. 6, pp. 3105–3109, June 2024. [DOI: 10.1109/TCSII.2024.3361205](https://doi.org/10.1109/TCSII.2024.3361205).
13. <a id="ref-xiang2011test"></a>**[Xiang2011Test]** D. Xiang et al., "Cost-Effective Power-Aware Core Testing in NoCs Based on a New Unicast-Based Multicast Scheme," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 30, no. 9, pp. 1373–1386, Sept. 2011. [DOI: 10.1109/TCAD.2011.2147785](https://doi.org/10.1109/TCAD.2011.2147785).
14. <a id="ref-agrawal2014test"></a>**[Agrawal2014Test]** P. Agrawal et al., "Test-Delivery Optimization in Manycore SOCs," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 33, no. 4, pp. 600–613, Apr. 2014. [DOI: 10.1109/TCAD.2013.2294110](https://doi.org/10.1109/TCAD.2013.2294110).
15. <a id="ref-li2024neuro"></a>**[Li2024Neuro]** D. Li, M. M. Wong, and L.-S. Peh, "A 1.63-pJ/SOP Neuromorphic Processor With Integrated Partial Sum Routers for In-Network Computing," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 32, no. 11, pp. 2080–2093, Nov. 2024. [DOI: 10.1109/TVLSI.2024.3411200](https://doi.org/10.1109/TVLSI.2024.3411200).
