# Chapter 8: Three-Dimensional Networks-on-Chip (3D-NoC) & TSVs

[![Companion Platform](https://img.shields.io/badge/Interactive%20Lab-Chiplet%20Tycoon-0f766e?logo=bookstack&logoColor=white)](https://network-on-chip.github.io/learning/interactive/chiplet/)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%208%3A%203D%20TSVs-blue)](../../track8-3d-noc-tsvs/)
[![Simulation Model](https://img.shields.io/badge/Python%20Model-tsv__vertical__mesh__sim.py-blueviolet)](code/tsv_vertical_mesh_sim.py)
[![Hardware RTL](https://img.shields.io/badge/Verilog%20RTL-tsv__arbiter__3d.v-success)](code/tsv_arbiter_3d.v)

---

## Chapter Introduction

In planar two-dimensional (2D) integrated circuits, as processor core counts scale into the hundreds, interconnect wire lengths grow with the square root of the node count ($L_{\text{max}} \propto \sqrt{N}$). Consequently, global planar wires span centimeters of high-resistance, highly capacitive copper tracks, suffering quadratic Elmore RC delays and consuming massive dynamic driving energy.

Three-Dimensional Integrated Circuits (3D-ICs) break this planar constraint by stacking multiple thinned active silicon tiers vertically, interconnecting them through dense arrays of microscopic vertical pillars known as **Through-Silicon Vias (TSVs)**. By folding the planar communication volume into the vertical $Z$-dimension, 3D Networks-on-Chip (3D-NoCs) dramatically compress Manhattan distances, slashing average packet hop counts by over **$35\%$** and reducing longest wire spans by more than **$75\%$**.

However, vertical integration introduces a daunting trifecta of physical and microarchitectural challenges:
- **TSV Parasitics & Keep-Out Zones (KOZ)**: Although TSVs have tiny ohmic resistance ($<50\text{ m}\Omega$), their dielectric oxide liner capacitance ($20\text{--}50\text{ fF}$) and massive thermo-mechanical expansion mismatches create stress fields that shift adjacent transistor mobility by up to $\pm 30\%$, mandating strict silicon exclusion zones.
- **Microarchitectural Router Expansion**: Adding vertical Up ($+Z$) and Down ($-Z$) channels expands a canonical 5-port planar router into a **7-port 3D crossbar switch**, increasing internal crosspoint complexity quadratically from $5^2 = 25$ to $7^2 = 49$ ($+96\%$ switch area).
- **Vertical Thermal Trapping**: Because the system heat sink attaches only to the bottom or top tier, heat generated in intermediate and opposite tiers must conduct through multiple low-conductivity dielectric bonding interfaces, baking upper compute tiers in an "attic oven" with temperatures elevated by up to $+40^\circ\text{C}$.

This chapter delivers a rigorous, multidisciplinary exploration of 3D-NoC architecture and TSV physics. We derive the electrical lumped $\pi$-models of vertical TSVs, analyze thermo-mechanical stress and Keep-Out Zone rules, examine 7-port router microarchitectures alongside vertical arbitration-free fast-paths, formalize vertical heat trapping models, and evaluate 3D dimension-order routing (XYZ vs. ZXY) to balance communication throughput against thermal dissipation.

### Learning Objectives
- **Understand the 3D Topological Scaling Advantage**: Quantify the reduction in network diameter, average hop count ($\bar{h}$), and bisection metal tracks achieved by folding planar grids into 3D meshes.
- **Model TSV Electrical & Mechanical Parasitics**: Derive the ohmic resistance ($R_{\text{tsv}}$), coaxial oxide capacitance ($C_{\text{ox}}$), and piezoresistive Keep-Out Zone (KOZ) exclusion rules.
- **Design 3D Router Microarchitectures**: Evaluate 7-port full crossbars against partitioned hybrid routers, shared vertical pillars, and vertical arbitration-free fast-path datapaths.
- **Analyze Vertical Heat Trapping & Thermal Gradients**: Formulate multi-tier steady-state heat conduction equations across dielectric bonding layers and package heat spreaders.
- **Implement 3D Dimension-Order Routing**: Compare XYZ, ZXY, and thermally-aware routing algorithms in terms of TSV link utilization and hotspot avoidance.

### Chapter Roadmap & Interactive Modules
- **Section 8.1**: The Three-Dimensional Scaling Paradigm.
- **Section 8.2**: Through-Silicon Via (TSV) Physical Characteristics & Parasitics.
- **Section 8.3**: 3D Router Microarchitectures & Vertical Arbitration.
- **Section 8.4**: Thermal Stacking & Heat Trapping in 3D Silicon.
- **Section 8.5**: 3D Routing Algorithms: Dimension-Order & Thermal-Aware.
- **Section 8.6**: Hardware Microarchitecture: 7-Port Vertical Link Arbiter.
- **Section 8.7**: Simulation Model & Numerical Verification.
- **Section 8.8**: Summary & Cross-Disciplinary Synergies.
- **Section 8.9**: Interactive Lab & Hands-on Challenges.
- **Section 8.10**: Comprehensive Problem Set & Solutions.
- **Section 8.11**: Checkpoint Assessment & Certification Questions.

---

## 8.1 The Three-Dimensional Scaling Paradigm

> [!NOTE] 💡 Architectural Intuition: Sprawling Suburbs vs. City Skyscrapers
> Imagine a sprawling suburban town of 64 single-story houses spread across a massive county. If the person living in the bottom-left corner wants to visit the person in the top-right corner, they have to drive across 14 miles of crowded highways, hitting stoplights at every intersection!
>
> Now imagine taking those 64 houses and stacking them vertically into an **8-story skyscraper**!
> Instead of driving miles on flat roads, you step into a **high-speed elevator** (a Through-Silicon Via, or TSV). You reach the other person in just a few seconds!
>
> That is the magic of **3D Networks-on-Chip (3D-NoC)**: by stacking silicon floors on top of each other, we cut wire distances by **$75\%$** and hop latencies by over **$35\%$**!

In planar two-dimensional (2D) integrated circuits, as processor core counts scale into the hundreds, interconnect wire lengths grow with the square root of the node count ($L_{\text{max}} \propto \sqrt{N}$). Consequently, global planar wires span centimeters of high-resistance, highly capacitive copper tracks, suffering quadratic Elmore RC delays and consuming massive dynamic driving energy.

Three-Dimensional Integrated Circuits (3D-ICs) break this planar constraint by stacking multiple thinned active silicon tiers vertically, interconnecting them through dense arrays of microscopic vertical pillars known as **Through-Silicon Vias (TSVs)**.

```
       Planar 2D Integration (N=64 Cores)             3D-IC Stacking (4 Tiers x 16 Cores)
       +-------------------------------+              Tier 3: [ Core 48-63 | L2 Cache ]
       | C00 C01 C02 C03 ... C07       |                         |||||||| TSV Array
       | C08 C09 C10 C11 ... C15       |              Tier 2: [ Core 32-47 | L2 Cache ]
       |  ...   ...   ...   ...        |                         |||||||| TSV Array
       | C56 C57 C58 C59 ... C63       |              Tier 1: [ Core 16-31 | L2 Cache ]
       +-------------------------------+                         |||||||| TSV Array
       Max Manhattan Distance: 14 hops                Tier 0: [ Core 00-15 | Mem Ctrl ]
       Corner-to-Corner Wire: ~18 mm                  =================================
                                                              Copper Heat Spreader & Sink
                                                      Max Manhattan Distance: 6 hops
                                                      Max Wire Distance: ~4.5 mm (-75%)
```

### 8.1.1 Advantages of 3D Integration
- **Dramatically Shortened Interconnect Lengths**:
    - Replaces long, resistive horizontal metal wires with micrometer-scale vertical connections across stacked dies.
    - A $4 \times 4 \times 4$ 3D mesh containing 64 cores achieves a network diameter of only $(3 + 3 + 3) = 9$ hops, contrasted with $(7 + 7) = 14$ hops in a conventional $8 \times 8$ 2D mesh.
    - Slashes average packet hop counts and wire traversal latency by over **$35\%$**, significantly curbing total capacitive dynamic wire dissipation.
- **Heterogeneous Technology Stacking**:
    - Decouples process technology across functional tiers, allowing each die layer to be manufactured in its optimal, cost-effective semiconductor process.
    - Enables direct vertical stacking of an advanced leading-edge compute tier (e.g., 3nm FinFET/GAAFET) directly over dense memory tiers (e.g., 14nm eDRAM, High-Bandwidth Memory stacks) or analog/RF/sensor tiers.
    - Eliminates long off-chip PCB board traces and packaging parasitics, reducing I/O power and pad-ring footprint.
- **Massive Vertical Bandwidth Density**:
    - Delivers fine-pitch micro-bumps and Through-Silicon Vias (TSVs) yielding thousands of parallel vertical inter-tier channels.
    - Achieves multi-terabits-per-second inter-tier bisection bandwidth with ultra-low sub-100 picosecond propagation delays.
    - Bypasses traditional chip-edge I/O pin-count bottlenecks (Rent's rule off-chip pin limitations [[Pavlidis2009](#ref-pavlidis2009)]).
    - Explores complex vendor-independent design space allocations using hypergraph-genetic algorithms (Al-Alousi et al. [[AlAlousi2026](#ref-alalousi2026)]).

---

## 8.2 Through-Silicon Via (TSV) Physical Characteristics & Parasitics

A Through-Silicon Via is a microscopic copper plug etched vertically through the bulk silicon substrate of a thinned wafer (typically $20\ \mu\text{m}\text{ to }50\ \mu\text{m}$ thick) and insulated from the conductive silicon by a thin dielectric liner (such as $\text{SiO}_2$ or $\text{Si}_3\text{N}_4$) [[Loi2011](#ref-loi2011)].

![Figure 8.1: TSV bundle in bulk silicon technology showing Metal 1 landing pad routing. [Reproduced from: I. Loi et al., "Characterization and Implementation of Fault-Tolerant Vertical Links for 3-D Networks-on-Chip", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 30, No. 1, pp. 124-134, Jan. 2011, DOI: 10.1109/TCAD.2010.2065990. © 2011 IEEE]](figures/loi_fig02_tsv_bundle.png)

![Figure 8.2: Circuit-level lumped parasitic model of a multi-TSV bundle. [Reproduced from: I. Loi et al., "Characterization and Implementation of Fault-Tolerant Vertical Links for 3-D Networks-on-Chip", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 30, No. 1, pp. 124-134, Jan. 2011, DOI: 10.1109/TCAD.2010.2065990. © 2011 IEEE]](figures/loi_fig03_tsv_schematic.png)

### 8.2.1 Lumped Electrical Model
As characterized by I. Loi et al. [[Loi2011](#ref-loi2011)] and depicted in Figures 8.1 and 8.2, each TSV is modeled as an electrical lumped $\pi$-network parameterized by the following physical components:

- **Ohmic Resistance ($R_{\text{tsv}}$)**:
    - Governed by the electrical resistivity of electroplated copper ($\rho_{\text{Cu}} \approx 1.7 \times 10^{-8}\ \Omega\cdot\text{m}$):
    $$R_{\text{tsv}} = \rho_{\text{Cu}} \frac{h_{\text{tsv}}}{\pi (d_{\text{tsv}} / 2)^2}$$
    - For typical dimensions ($h_{\text{tsv}} = 30\ \mu\text{m}$, $d_{\text{tsv}} = 4\ \mu\text{m}$), $R_{\text{tsv}} \approx 30\text{ to }50\text{ m}\Omega$.
    - This resistance is negligible compared to planar millimeter-long on-chip wires ($>100\ \Omega$), rendering TSV RC line delay exceptionally low.
- **Insulator Oxide Capacitance ($C_{\text{ox}}$)**:
    - Formed across the cylindrical dielectric sleeve ($\text{SiO}_2$ with thickness $t_{\text{ox}} \approx 100\text{ to }200\text{ nm}$):
    $$C_{\text{ox}} = \frac{2 \pi \epsilon_{\text{ox}} \epsilon_0 h_{\text{tsv}}}{\ln\left(\frac{r_{\text{tsv}} + t_{\text{ox}}}{r_{\text{tsv}}}\right)} \approx 20\text{ to }50\text{ fF}$$
    - Constitutes the dominant capacitive load driven by vertical link buffers, establishing the minimum driver transistor sizing.
- **Substrate Conductance and Inter-TSV Coupling ($C_{\text{sub}}, G_{\text{sub}}$)**:
    - Arises from high-frequency electrostatic fields penetrating through the moderately conductive doped bulk silicon substrate between neighboring vertical conductors.
    - Induces dynamic cross-talk noise and signal integrity degradation on adjacent unshielded vertical signal lines.
    - Requires dedicated ground/power shielding TSVs or differential signaling topologies when dense vertical bundles switch simultaneously.

### 8.2.2 The Keep-Out Zone (KOZ)
Copper has a coefficient of thermal expansion ($\alpha_{\text{Cu}} \approx 17.0\text{ ppm/K}$) nearly an order of magnitude higher than silicon ($\alpha_{\text{Si}} \approx 2.6\text{ ppm/K}$). During thermal cycling from annealing ($350^\circ\text{C}$) to room temperature, the expanding copper exerts hundreds of megapascals of thermo-mechanical compressive stress onto the surrounding silicon crystal [[Pavlidis2009](#ref-pavlidis2009), [Loi2011](#ref-loi2011)].

Via the **piezoresistive effect**, this mechanical stress alters silicon band structure, shifting CMOS transistor mobility by up to **$\pm 30\%$** and inducing clock skew. Consequently, standard cells cannot be placed within a radial boundary of $3\ \mu\text{m}\text{ to }5\ \mu\text{m}$ surrounding each TSV—a silicon exclusion area known as the **Keep-Out Zone (KOZ)**.

---

## 8.3 3D Router Microarchitectures & Vertical Arbitration

In a planar 2D mesh, routers have 5 ports: North, South, East, West, and Local. Extending the network to 3D requires two additional ports: **Up** ($+Z$) and **Down** ($-Z$) [[More2018](#ref-more2018), [Seiculescu2010](#ref-seiculescu2010)].

![Figure 8.3: 3D Network-on-Chip router microarchitecture structures: 7-port full crossbar vs. hybrid partitioned routers. [Reproduced from: A. More et al., "Vertical Arbitration-Free 3-D NoCs", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 37, No. 9, pp. 1853-1866, Sept. 2018, DOI: 10.1109/TCAD.2017.2768415. © 2018 IEEE]](figures/more_fig01_3d_router_structs.png)

![Figure 8.4: Comparison of (a) traditional arbitrated vertical links versus (b) vertical arbitration-free fast-path designs. [Reproduced from: A. More et al., "Vertical Arbitration-Free 3-D NoCs", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 37, No. 9, pp. 1853-1866, Sept. 2018, DOI: 10.1109/TCAD.2017.2768415. © 2018 IEEE]](figures/more_fig04_arbitration_free.png)

### 8.3.1 The Silicon Area Penalty of Full 7-Port Crossbars
As shown in Figure 8.3, expanding a router crossbar from 5 to 7 ports increases internal crossbar multiplexer complexity quadratically:

$$\text{Crosspoints} = P^2 = 7^2 = 49 \quad \text{vs.} \quad 5^2 = 25 \quad (+96\% \text{ area})$$

Moreover, 7 input buffers demand significant silicon real estate and static leakage.

### 8.3.2 Shared Vertical Links & Vertical Arbitration Contention
To economize TSV footprint and routing area, many architectures deploy **shared vertical pillars** where multiple adjacent planar nodes share a single vertical TSV channel. However, as proven by A. More et al. [[More2018](#ref-more2018)]:
- Contending planar packets competing for the vertical pillar must undergo multi-cycle arbitration, adding substantial queuing delay.
- In their proposed **Vertical Arbitration-Free 3D-NoC** (Figure 8.4), dedicated unidirectional fast-paths eliminate vertical arbiters entirely, reducing vertical traversal delay to a single cycle while trimming router area by **$20\%$**.

---

## 8.4 Thermal Stacking & Heat Trapping

> [!WARNING] 💡 Architectural Intuition: The Attic Oven (Why the Top Floor is Boiling Hot!)
> Have you ever noticed that in a multi-story house, the top floor or attic is always scorching hot in the summer?
> 
> The exact same thing happens in a 3D chip! The heavy copper heat sink and cooling fan sit on the **bottom floor (Tier 0)**. Heat generated in the middle and top floors cannot easily escape: it gets trapped between layers of insulating glue and silicon. To reach the heat sink, heat from Tier 2 must crawl all the way down through Tier 1 and Tier 0.
> 
> As our simulation proves: while Tier 0 stays at a reasonable $97^\circ\text{C}$, Tier 2 gets baked at **$136.5^\circ\text{C}$**! Managing this "attic oven" is the biggest thermal challenge in 3D silicon design.

While 3D stacking slashes communication latency, it creates an acute physical challenge: **thermal trapping** [[Skadron2003](#ref-skadron2003), [Huang2006](#ref-huang2006), [Chao2013](#ref-chao2013)].

```
   Tier 2 (Top Stack):     [ High-Power Compute Cores ]  <-- T_max = 136.5°C (Extreme Heat Trapping)
   ----------------------------------------------------      Thermal Resistance: R_inter (Dielectric)
   Tier 1 (Middle Tier):   [ High-Power Compute Cores ]  <-- T = 123.7°C
   ----------------------------------------------------      Thermal Resistance: R_inter (Dielectric)
   Tier 0 (Bottom Tier):   [ Lower-Power Memory / IO  ]  <-- T = 97.2°C
   ====================================================      Thermal Resistance: R_hs (TIM + Spreader)
   [ COPPER HEAT SPREADER & EXTERNAL FORCED-AIR HEATSINK ]  <-- Ambient Air = 45.0°C
```

In standard single-die packaging, silicon sits directly on the package heat sink. In 3D-ICs, only **Tier 0** is directly adjacent to the heat spreader. Heat generated in **Tier 1** and **Tier 2** must conduct through intervening bulk silicon substrates and low-conductivity dielectric bonding interfaces ($\text{SiO}_2$ or polymer adhesive, $k_{\text{th}} \approx 0.2\text{ to }1.4\text{ W/(m}\cdot\text{K)}$) [[Chao2013](#ref-chao2013)].

As demonstrated by our simulation model, under equivalent uniform workloads, top-tier silicon reaches **$136.5^\circ\text{C}$**—an alarming **$+39.3^\circ\text{C}$ thermal stacking penalty** over bottom-tier silicon ($97.2^\circ\text{C}$).

---

## 8.5 TSV Defect Tolerance & Redundancy

TSV fabrication involves deep reactive-ion etching (DRIE), liner chemical vapor deposition, copper electroplating, chemical-mechanical polishing (CMP), and high-precision wafer bonding. A single physical void, seam, or micro-crack breaks the vertical link, ruining the entire multi-die stack [[Seiculescu2010](#ref-seiculescu2010)].

### 8.5.1 Redundancy Configurations
To achieve viable manufacturing yield, modern 3D-NoC designs deploy hardware redundancy:
- **Double-TSV Bundles**: Routing each critical signal bit through two parallel TSVs. If one suffers an open defect, the redundant path maintains continuity.
- **$N:1$ Spare TSV Multiplexing**: Grouping a 32-bit flit bus into 4 bundles of 8 bits, each protected by 1 spare TSV and a dynamic multiplexer steering network. As proved by Loi et al. [[Loi2011](#ref-loi2011)], this raises vertical link yield from **$66\%$ to $98\%$** with only a **$2.1\%$ router area overhead**.

---

## 8.6 Hardware Microarchitecture: 7-Port Vertical Link Arbiter

Below is the synthesizable Verilog implementation of the 3D router vertical link arbiter with runtime TSV defect bypass logic from [`code/tsv_arbiter_3d.v`](code/tsv_arbiter_3d.v), grounded in vertical link microarchitectures developed by I. Loi et al. [[Loi2011](#ref-loi2011)] and A. More et al. [[More2018](#ref-more2018)].

```verilog
// ============================================================================
// 3D-NoC 7-Port Router Vertical TSV Link Arbiter with Fault Bypass
// Grounded in I. Loi et al. (IEEE TCAD 2011) and A. More et al. (IEEE TCAD 2018)
// ============================================================================

`timescale 1ns / 1ps

module tsv_arbiter_3d #(
    parameter integer NUM_INPUTS = 5 // Local, North, South, East, West
)(
    input  wire                    clk,
    input  wire                    rst_n,
    input  wire [NUM_INPUTS-1:0]   req_up,
    input  wire [NUM_INPUTS-1:0]   req_down,
    input  wire                    tsv_up_faulty,
    input  wire                    tsv_down_faulty,
    output reg  [NUM_INPUTS-1:0]   grant_up,
    output reg  [NUM_INPUTS-1:0]   grant_down,
    output wire                    tsv_up_busy,
    output wire                    tsv_down_busy,
    output reg  [NUM_INPUTS-1:0]   bypass_planar_up,
    output reg  [NUM_INPUTS-1:0]   bypass_planar_down
);

    reg [2:0] priority_up_ptr, priority_down_ptr;
    assign tsv_up_busy   = (|grant_up);
    assign tsv_down_busy = (|grant_down);

    integer i;
    always @(*) begin
        grant_up         = {NUM_INPUTS{1'b0}};
        bypass_planar_up = {NUM_INPUTS{1'b0}};

        if (tsv_up_faulty) begin
            // TSV bundle is defective: steer packet along planar alternate route
            bypass_planar_up = req_up;
        end else if (|req_up) begin
            for (i = 0; i < NUM_INPUTS; i = i + 1) begin
                if (req_up[(priority_up_ptr + i) % NUM_INPUTS]) begin
                    grant_up[(priority_up_ptr + i) % NUM_INPUTS] = 1'b1;
                    i = NUM_INPUTS;
                end
            end
        end
    end

    integer j;
    always @(*) begin
        grant_down         = {NUM_INPUTS{1'b0}};
        bypass_planar_down = {NUM_INPUTS{1'b0}};

        if (tsv_down_faulty) begin
            bypass_planar_down = req_down;
        end else if (|req_down) begin
            for (j = 0; j < NUM_INPUTS; j = j + 1) begin
                if (req_down[(priority_down_ptr + j) % NUM_INPUTS]) begin
                    grant_down[(priority_down_ptr + j) % NUM_INPUTS] = 1'b1;
                    j = NUM_INPUTS;
                end
            end
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            priority_up_ptr   <= 3'd0;
            priority_down_ptr <= 3'd0;
        end else begin
            if (|grant_up) begin
                for (i = 0; i < NUM_INPUTS; i = i + 1)
                    if (grant_up[i]) priority_up_ptr <= (i + 1) % NUM_INPUTS;
            end
            if (|grant_down) begin
                for (j = 0; j < NUM_INPUTS; j = j + 1)
                    if (grant_down[j]) priority_down_ptr <= (j + 1) % NUM_INPUTS;
            end
        end
    end
endmodule
```

---

## 8.7 Simulation Model & Numerical Verification

The companion simulation script [`code/tsv_vertical_mesh_sim.py`](code/tsv_vertical_mesh_sim.py) evaluates a $4 \times 4 \times 3$ mesh (48 cores) under uniform random traffic [[Pavlidis2009](#ref-pavlidis2009), [More2018](#ref-more2018)] comparing **3D XYZ Dimension-Order Routing** and **ZXY Dimension-Order Routing**.

### 8.7.1 Simulation Execution & Results

```bash
$ python3 code/tsv_vertical_mesh_sim.py
=== 3D Network-on-Chip (3D-NoC) Simulation Results ===
Topology: 4x4x3 Mesh (48 Router Tiles across 3 Silicon Tiers)

--- Routing Algorithm: XYZ_DOR ---
  Average Packet Latency: 6.04 cycles
  Average Hop Distance:   3.47 hops
  Planar Hop Share:       74.0 %
  Vertical TSV Hop Share: 26.0 %
  Tier 0 Temp (Heatsink): 97.18 °C
  Tier 1 Temp (Middle):   123.66 °C
  Tier 2 Temp (Top Stack):136.53 °C (Thermal Trapping)

--- Routing Algorithm: ZXY_DOR ---
  Average Packet Latency: 5.95 cycles
  Average Hop Distance:   3.42 hops
  Planar Hop Share:       73.7 %
  Vertical TSV Hop Share: 26.3 %
  Tier 0 Temp (Heatsink): 96.96 °C
  Tier 1 Temp (Middle):   123.13 °C
  Tier 2 Temp (Top Stack):135.79 °C (Thermal Trapping)

Self-test passed successfully!
```

---

## 8.8 Summary & Cross-Disciplinary Synergies

- **Interconnect Volume Folding**:
    - 3D physical stacking replaces distributed, high-resistance horizontal planar wires with micro-scale vertical Through-Silicon Vias [[Pavlidis2009](#ref-pavlidis2009)].
    - Slashes average network diameter and hop counts by $>35\%$, enabling scalable communication across dozens of compute nodes without wire-scaling stalls.
- **TSV Parasitics & Keep-Out Zones (KOZ)**:
    - While TSV ohmic resistance is minimal ($<50\text{ m}\Omega$), capacitive coupling through the substrate ($30\text{ to }50\text{ fF}$) dominates buffer switching dynamics [[Loi2011](#ref-loi2011)].
    - Severe coefficient of thermal expansion mismatches between copper and bulk silicon generate intense thermo-mechanical stress, requiring $3\ \mu\text{m}\text{ to }5\ \mu\text{m}$ Keep-Out Zones to protect active transistor mobility [[Pavlidis2009](#ref-pavlidis2009)].
- **Crossbar Multiplexing & Microarchitecture Overheads**:
    - Full 7-port 3D crossbars nearly double internal multiplexing complexity ($P^2 = 49$ vs. $25$), escalating static leakage and router floorplan area [[Seiculescu2010](#ref-seiculescu2010)].
    - Vertical arbitration-free fast-paths and shared vertical channel pillars eliminate inter-tier arbitration delays and save router area [[More2018](#ref-more2018)].
- **Thermal Stacking & Multi-Tier Heat Trapping**:
    - Stacking active compute dies creates an "attic oven" effect where upper tiers undergo severe thermal penalties ($+39^\circ\text{C}$ in realistic stacks) due to cumulative inter-tier dielectric thermal resistance [[Chao2013](#ref-chao2013)].
    - Mandates thermal-aware 3D routing algorithms, vertical active throttling, and placement of low-power cache/memory tiers closer to the primary heat sink [[Skadron2003](#ref-skadron2003), [Huang2006](#ref-huang2006)].
- **Yield & Fault-Tolerant Redundancy**:
    - Micro-scale manufacturing defects in vertical vias can catastrophically disable an entire multi-die stack [[Seiculescu2010](#ref-seiculescu2010)].
    - Self-healing hardware crossbars, reconfigurable multiplexers, and 4:1 spare-wire repair networks restore link continuity transparently with zero flit loss [[Loi2011](#ref-loi2011)].

---

## 8.9 Interactive Lab & Hands-on Challenges

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.35), rgba(15, 23, 42, 0.65)); border: 1px solid rgba(59, 130, 246, 0.5); border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #93c5fd; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;">
      <span>🏢 Dedicated Interactive Lab: TSV Titan: 3D-NoC Architect</span>
    </div>
    <div style="font-size: 0.92rem; color: #e2e8f0; margin-top: 6px; max-width: 800px; line-height: 1.5;">
      Architect vertical Through-Silicon Via (TSV) interconnects across multi-tier silicon stacks, balance Keep-Out Zone (KOZ) stress boundaries, route 3D flits, and defeat thermal stacking traps using thermal dummy TSVs.
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="../../interactive/tsv3d/" style="display: inline-flex; align-items: center; gap: 6px; background: #8b5cf6; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Launch TSV Titan →</span>
    </a>
    <a href="../../interactive/chiplet/" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Chiplet CAD Optimizer →</span>
    </a>
  </div>
</div>

Complete the following three hands-on laboratory missions in **[TSV Titan: 3D-NoC Architect](../../interactive/tsv3d.md)**:

### Challenge Mission 8.1: TSV Physical Parameters & Keep-Out Zone (KOZ) Silicon Overhead
- **Objective:** Quantify the active silicon area penalty imposed by thermo-mechanical stress around copper TSVs across varying via pitches.
- **Setup & Procedure:**
  1. In **TSV Titan**, set 3D stack to 3 Tiers (Logic + SRAM + HBM).
  2. Inspect the TSV physical dimensions: diameter $d = 4\,\mu\text{m}$, height $h = 40\,\mu\text{m}$, pitch $p = 10\,\mu\text{m}$.
  3. Observe the calculated Keep-Out Zone radius ($r_{koz} \approx 8.8\,\mu\text{m}$) and active silicon area exclusion ratio.
- **Architectural Observation:** Copper's high coefficient of thermal expansion ($\text{CTE}_{Cu} \approx 17\times 10^{-6}/\text{K}$) versus silicon ($\text{CTE}_{Si} \approx 2.6\times 10^{-6}/\text{K}$) induces radial tensile stress exceeding $200\text{ MPa}$ near the via edge. To prevent threshold voltage shifts and drive-current degradation, standard cell transistors are prohibited inside the KOZ, consuming $4.8\%$ to $15\%$ of active tile silicon area!
- **Verification Formula:** $\sigma_r(r) = -\Delta\alpha \cdot \Delta T \cdot E \cdot \left(\frac{r_0}{r}\right)^2$.

### Challenge Mission 8.2: 3D Dimension-Order Routing ($Z-X-Y$ vs Elevator Routing)
- **Objective:** Verify deadlock freedom and vertical link utilization when routing cross-plane flits between Logic Tier 0 and HBM Tier 2.
- **Setup & Procedure:**
  1. Set routing algorithm to `Dimension-Order Z-X-Y (Vertical-First)`.
  2. Inject packets from Core $(1,1,0)$ on Tier 0 to Memory Controller $(3,3,2)$ on Tier 2.
  3. Switch algorithm to `Elevator Routing (Sparse TSV Pillars with Deflection)` and compare hop latency.
- **Architectural Observation:** Under $Z-X-Y$, flits traverse vertical TSV links immediately upon injection before executing planar X-Y routing. Because packets never transition from planar channels back to vertical channels, no vertical-horizontal dependency cycles can form in the 3D Channel Dependency Graph, guaranteeing deadlock-free routing. Under sparse Elevator Routing, packets deflect horizontally toward the nearest shared vertical TSV pillar, reducing total TSV area at the cost of $1.8$ extra average hops.

### Challenge Mission 8.3: Defeating the 3D Thermal Stacking Trap via Thermal Dummy TSVs
- **Objective:** Mitigate the severe "attic oven" thermal stacking effect where heat generated in lower/middle tiers is trapped by low-conductivity dielectric bonding layers.
- **Setup & Procedure:**
  1. Click **Toggle Mode** to enter **Mode B: 3D Thermal Stacking Profile**.
  2. Observe the peak temperature of Tier 1 ($>82^\circ\text{C}$) trapped beneath Inter-Layer Dielectric (ILD) oxide bonds ($k_{ILD} \approx 1.2\text{ W/m}\cdot\text{K}$).
  3. Deploy **Thermal TSV Conduits (Spacebar)** from 16 to 32 dummy TSVs.
- **Architectural Observation:** While silicon conducts heat efficiently ($k_{Si} \approx 140\text{ W/m}\cdot\text{K}$), ILD bonding layers act as thermal insulating blankets, trapping heat in active middle tiers. Inserting dummy copper TSVs ($k_{Cu} \approx 400\text{ W/m}\cdot\text{K}$) creates direct low-resistance vertical thermal conduits, shunting trapped heat directly down to the bottom heat sink and lowering peak junction temperature by $>14^\circ\text{C}$!
- **Hardware RTL & Python Reference:** Run `python code/tsv_rc_delay_model.py` and inspect `code/tsv_arbiter_3d.v` for synthesizable 3D crossbar arbitration RTL.

---

## 8.10 Comprehensive Problem Set & Solutions

### Problem 8.1: TSV Elmore Delay vs. Planar Intermediate Metal Wire [[Loi2011](#ref-loi2011), [Pavlidis2009](#ref-pavlidis2009)]
Compare the propagation delay of a vertical TSV link versus a planar intermediate metal layer (M5) wire in a 7nm technology node:
- **TSV Parameters**: Height $h_{\text{tsv}} = 40\ \mu\text{m}$, diameter $d_{\text{tsv}} = 4\ \mu\text{m}$, copper resistivity $\rho = 1.7 \times 10^{-8}\ \Omega\cdot\text{m}$, oxide liner thickness $t_{\text{ox}} = 150\text{ nm}$, $\epsilon_r = 3.9$, driver resistance $R_d = 400\ \Omega$.
- **Planar Wire Parameters**: Length $L_{\text{wire}} = 1.5\text{ mm}$ (spanning one router tile), resistance $r_{\text{wire}} = 80\ \Omega/\text{mm}$, capacitance $c_{\text{wire}} = 180\text{ fF/mm}$, driver resistance $R_d = 400\ \Omega$.
1. Calculate the resistance and capacitance of the TSV ($R_{\text{tsv}}, C_{\text{tsv}}$).
2. Calculate the Elmore delay of the TSV link: $\tau_{\text{tsv}} = R_d C_{\text{tsv}} + R_{\text{tsv}} C_{\text{tsv}} / 2$.
3. Calculate the Elmore delay of the planar wire: $\tau_{\text{planar}} = R_d C_{\text{wire}} + R_{\text{wire}} C_{\text{wire}} / 2$.
4. Determine the speedup of the vertical TSV link over the planar wire.

??? success "Reveal Detailed Solution"
    1. **TSV Resistance & Capacitance**:

        $$A_{\text{tsv}} = \pi \left(\frac{d_{\text{tsv}}}{2}\right)^2 = \pi \times (2 \times 10^{-6})^2 = 1.2566 \times 10^{-11}\text{ m}^2$$

        $$R_{\text{tsv}} = (1.7 \times 10^{-8}\ \Omega\cdot\text{m}) \times \frac{40 \times 10^{-6}\text{ m}}{1.2566 \times 10^{-11}\text{ m}^2} = 0.0541\ \Omega = 54.1\text{ m}\Omega$$

        $$C_{\text{tsv}} = \frac{2 \pi \epsilon_r \epsilon_0 h_{\text{tsv}}}{\ln\left(\frac{r + t_{\text{ox}}}{r}\right)} = \frac{2 \pi \times 3.9 \times (8.854 \times 10^{-12}) \times (40 \times 10^{-6})}{\ln\left(\frac{2.15}{2.00}\right)} = \frac{8.683 \times 10^{-15}}{0.07232} = 120.1\text{ fF}$$

    2. **TSV Elmore Delay**:

        $$\tau_{\text{tsv}} = R_d C_{\text{tsv}} + \frac{R_{\text{tsv}} C_{\text{tsv}}}{2} \approx (400\ \Omega) \times (120.1 \times 10^{-15}\text{ F}) = 48.04\text{ ps}$$

        (The $R_{\text{tsv}} C_{\text{tsv}} / 2$ term is $54.1 \times 10^{-3} \times 120.1 \times 10^{-15} / 2 = 3.25 \times 10^{-15}\text{ s} = 0.003\text{ ps}$, which is completely negligible).

    3. **Planar Wire Elmore Delay**:

        $$R_{\text{wire}} = 80\ \Omega/\text{mm} \times 1.5\text{ mm} = 120\ \Omega$$

        $$C_{\text{wire}} = 180\text{ fF/mm} \times 1.5\text{ mm} = 270\text{ fF}$$

        $$\tau_{\text{planar}} = R_d C_{\text{wire}} + \frac{R_{\text{wire}} C_{\text{wire}}}{2} = (400 \times 270 \times 10^{-15}) + \left(\frac{120 \times 270 \times 10^{-15}}{2}\right)$$

        $$\tau_{\text{planar}} = 108.0\text{ ps} + 16.2\text{ ps} = 124.2\text{ ps}$$

    4. **Speedup**:

        $$\text{Speedup} = \frac{\tau_{\text{planar}}}{\tau_{\text{tsv}}} = \frac{124.2\text{ ps}}{48.04\text{ ps}} \approx 2.59\times$$

        The vertical TSV transmits data **$2.59\times$ faster** than the planar wire, while consuming less than half the capacitive dynamic switching energy ($120\text{ fF}$ vs. $270\text{ fF}$).

---

### Problem 8.2: 3D-IC Stacking Thermal Gradient Calculation [[Skadron2003](#ref-skadron2003), [Huang2006](#ref-huang2006), [Chao2013](#ref-chao2013)]
A 3-tier 3D-IC stack dissipates power uniformly across each layer: $P_0 = P_1 = P_2 = 25.0\text{ W}$ ($P_{\text{total}} = 75.0\text{ W}$). The bottom tier (Tier 0) is attached to a forced-convection heat sink with thermal resistance $R_{\text{hs}} = 0.40\text{ K/W}$ to ambient air ($T_{\text{amb}} = 40.0^\circ\text{C}$). The inter-tier bonding interfaces each have an effective thermal resistance of $R_{\text{inter}} = 0.35\text{ K/W}$.
1. Derive the mathematical expressions for the steady-state temperature of each tier ($T_0, T_1, T_2$).
2. Compute the exact temperatures of Tier 0, Tier 1, and Tier 2.
3. What is the temperature differential between the top tier and bottom tier?

??? success "Reveal Detailed Solution"
    1. **Derivation**:
        - The total heat from all three tiers must pass through the heat sink:

            $$T_0 = T_{\text{amb}} + R_{\text{hs}} \cdot (P_0 + P_1 + P_2) = T_{\text{amb}} + R_{\text{hs}} \cdot P_{\text{total}}$$

        - The heat from Tier 1 and Tier 2 conducts down through the lower bonding interface into Tier 0:

            $$T_1 = T_0 + R_{\text{inter}} \cdot (P_1 + P_2)$$

        - The heat from Tier 2 conducts down through the upper bonding interface into Tier 1:

            $$T_2 = T_1 + R_{\text{inter}} \cdot P_2$$

    2. **Numerical Computation**:

        $$T_0 = 40.0^\circ\text{C} + (0.40\text{ K/W}) \times (75.0\text{ W}) = 40.0 + 30.0 = 70.0^\circ\text{C}$$

        $$T_1 = 70.0^\circ\text{C} + (0.35\text{ K/W}) \times (25.0 + 25.0\text{ W}) = 70.0 + (0.35 \times 50.0) = 70.0 + 17.5 = 87.5^\circ\text{C}$$

        $$T_2 = 87.5^\circ\text{C} + (0.35\text{ K/W}) \times (25.0\text{ W}) = 87.5 + 8.75 = 96.25^\circ\text{C}$$

    3. **Thermal Stacking Differential**:

        $$\Delta T = T_2 - T_0 = 96.25^\circ\text{C} - 70.0^\circ\text{C} = 26.25^\circ\text{C}$$

        The top tier operates **$26.25^\circ\text{C}$ hotter** than the bottom tier due entirely to vertical thermal resistance accumulation.

---

## 8.11 Checkpoint Assessment

Test your mastery of Chapter 8 concepts against the official certification questions (mirroring the 3-Tier Exam Engine in [`quiz.md`](../../quiz.md)):

#### Question 8.1 (Tier 1: Fundamental)
*What is a Through-Silicon Via (TSV) Keep-Out Zone (KOZ), and what physical phenomenon dictates its radius around copper TSVs?*

- **A)** Thermal expansion mismatch between copper (alpha_Cu ~ 17 ppm/K) and silicon (alpha_Si ~ 2.6 ppm/K) induces severe thermo-mechanical shear stress (>200 MPa) during post-bonding thermal cooling, altering transistor carrier mobility by up to 30%; the KOZ is a mandatory exclusion area where no active CMOS transistors may be placed.
- **B)** A software security zone preventing hackers from reading TSV voltages.
- **C)** A chemical buffer to prevent silicon from dissolving in water.
- **D)** A radioactive shielding perimeter to block cosmic rays.

??? success "Reveal Answer & Full Solution"
    **Correct Answer: Option A**

    **1. Step-by-Step Architectural & Mathematical Derivation:**
    Through-Silicon Vias (TSVs) provide vertical electrical interconnects across stacked silicon dies. Copper (Cu) is the industry-standard via fill material due to its high electrical conductivity. However, copper and silicon have dramatically different Coefficients of Thermal Expansion (CTE): alpha_Cu = 17 ppm/K vs. alpha_Si = 2.6 ppm/K (a 6.5x CTE mismatch). During post-bond annealing and cooling from 250°C to room temperature, copper contracts significantly more than the surrounding silicon matrix. This creates severe tensile radial stress (sigma_r) and compressive tangential stress (sigma_theta) in the silicon lattice exceeding 200–300 MPa near the TSV edge. Through the piezoresistive effect, this mechanical lattice strain shifts NMOS electron mobility (by up to -15%) and PMOS hole mobility (by up to +35%), inducing unacceptable threshold voltage (V_th) shifts and timing jitter. The TSV Keep-Out Zone (KOZ) defines a strict exclusion radius (typically 3–5 um around a 5 um diameter TSV) where standard cell transistors are prohibited from placement, directly impacting silicon area utilization.

    **2. Option-by-Option Breakdown & Distractor Analysis:**
    - **Option A (Correct):** Thermo-mechanical stress from the 6.5x CTE mismatch between copper and silicon alters carrier mobility via the piezoresistive effect, mandating a KOZ.
    - **Option B (Incorrect Distractor):** KOZ is a physical manufacturing and layout design rule, not a software security perimeter.
    - **Option C (Incorrect Distractor):** Silicon does not dissolve in water under standard operating conditions.
    - **Option D (Incorrect Distractor):** Standard TSVs do not emit or block radiation; the issue is thermo-mechanical stress.

    **3. Silicon Architect's Takeaway:**
    Copper TSVs induce localized lattice strain that shifts transistor mobility, requiring layout Keep-Out Zones (KOZ) of 3–5 um around each vertical via.

    *(Reference: A. Al-Alousi, M. Li, and H. Meng, 'Design Space Exploration and Resource Optimization for 3-D NoCs,' IEEE TCAD, Vol. 45, No. 5, pp. 2236–2248, May 2026. DOI: 10.1109/TCAD.2025.3616073.)*

#### Question 8.2 (Tier 2: Core Engineering)
*Why does expanding a 2D router (5 ports) to a fully symmetric 3D router (7 ports) almost double the crossbar switch area, and how do Vertical Arbitration-Free architectures mitigate this overhead?*

- **A)** Crossbar complexity scales quadratically with port count (P^2 = 49 crosspoints vs 25 crosspoints, a 96% increase); arbitration-free designs deploy dedicated unidirectional vertical links that eliminate vertical allocators and simplify the crossbar matrix.
- **B)** Crossbar area scales logarithmically with port count.
- **C)** Because 3D routers must be fabricated exclusively with diamond substrates.
- **D)** Arbitration-free architectures double the clock frequency to avoid adding vertical ports.

??? success "Reveal Answer & Full Solution"
    **Correct Answer: Option A**

    **1. Step-by-Step Architectural & Mathematical Derivation:**
    In a planar 2D router, there are P = 5 bidirectional ports: {North, South, East, West, Local}. A full crossbar matrix requires P^2 = 5^2 = 25 crosspoint multiplexers. In a symmetric 3D router, two vertical ports {Up, Down} are added to connect adjacent tiers, bringing total radix to P = 7. The required crosspoints surge to P^2 = 7^2 = 49 crosspoints—a 96% increase in crossbar area and wire congestion! Furthermore, the switch allocator complexity scales as O(P^2), inflating arbitration delay and power. More et al. [[More2018](#ref-more2018)] and related 3D NoC architects showed that vertical traffic accounts for a fraction of total hops. By implementing Vertical Arbitration-Free (VAF) fast-paths: (1) Vertical flits skip complex two-stage switch allocation, utilizing dedicated vertical FIFO bypass muxes. (2) The crossbar is decomposed into an asymmetric 5x5 planar matrix plus dedicated vertical injection paths. This eliminates 40% of the crossbar silicon area while cutting vertical transit latency to 1 cycle.

    **2. Option-by-Option Breakdown & Distractor Analysis:**
    - **Option A (Correct):** 7-port crossbars require 49 crosspoints vs 25 (+96%); dedicated vertical fast-paths eliminate complex vertical arbiters and reduce crossbar area.
    - **Option B (Incorrect Distractor):** Crossbar area scales as O(P^2), strictly quadratic, never logarithmic.
    - **Option C (Incorrect Distractor):** 3D-ICs are manufactured on standard bulk silicon wafers with oxide bonding, not synthetic diamond.
    - **Option D (Incorrect Distractor):** Clock frequency is not doubled; dedicated bypass circuits eliminate arbitration delays.

    **3. Silicon Architect's Takeaway:**
    7-port 3D crossbars suffer from 2x crosspoint area; vertical bypass fast-paths prevent area inflation and reduce vertical traversal latency.

    *(Reference: [[AlAlousi2026](#ref-alalousi2026)] A. Al-Alousi, M. Li, and H. Meng, "Design Space Exploration for 3-D NoCs," IEEE TCAD, Vol. 45, No. 5, pp. 2236–2248, May 2026. DOI: 10.1109/TCAD.2025.3616073.)*

#### Question 8.3 (Tier 3: Silicon Mastery)
*Which of the following physical mechanisms cause severe 'Thermal Trapping' in vertically stacked 3D-ICs? (Select all that apply)*

- **A)** Heat generated in upper silicon tiers must conduct downward through multiple thinned silicon substrates and low-conductivity dielectric bonding interfaces (SiO2 / polymer adhesives, k ~ 0.2–1.4 W/m*K) before reaching the bottom heat sink.
- **B)** The vertical accumulation of inter-tier thermal resistances elevates top-tier temperatures by 25°C to 45°C over bottom tiers under identical power dissipation.
- **C)** Power densities of stacked active tiers additively multiply across a single package footprint (e.g. 4 tiers of 100 W/cm^2 = 400 W/cm^2 total thermal flux).
- **D)** Heat in silicon is physically incapable of conducting through copper TSVs.

??? success "Reveal Answer & Full Solution"
    **Correct Answer: Option A, B, C**

    **1. Step-by-Step Architectural & Mathematical Derivation:**
    In standard 2D packaging, the single active silicon die sits directly against the thermal interface material (TIM) and copper heat sink. In 3D-stacked ICs (e.g. 4–8 stacked dies): (1) Multiplied Thermal Flux: Stacking 4 dies each dissipating 80 W/cm^2 results in an aggregate package thermal flux of 320 W/cm^2, far exceeding the heat extraction capability of conventional air heat sinks (~100 W/cm^2). (2) Thermal Resistance Ladder: Heat generated in Tier 3 (the furthest die from the heat sink) must conduct through Tier 2, Tier 1, and Tier 0. Between each die lies a dielectric bonding layer (BCB polymer with k ~ 0.2 W/m*K or SiO2 with k ~ 1.4 W/m*K), whose thermal conductivity is 100x–700x worse than bulk silicon (k_Si ~ 140 W/m*K). (3) Thermal Trapping: The series sum of these inter-tier thermal resistances (R_total = R_sink + sum R_interlayer + sum R_Si) traps heat in the top layers, elevating junction temperatures by 25°C to 45°C. Copper TSVs (k_Cu ~ 390 W/m*K) actually act as thermal conduits, helping conduct heat vertically, but their volume fraction (1–3%) is insufficient to fully overcome the dielectric barrier without dedicated thermal TSV arrays.

    **2. Option-by-Option Breakdown & Distractor Analysis:**
    - **Option A (Correct):** True. Low-conductivity dielectric bonding layers (k ~ 0.2–1.4 W/m*K) act as thermal insulators between stacked tiers.
    - **Option B (Correct):** True. Series thermal resistance accumulation elevates top-tier temperatures substantially above the base die.
    - **Option C (Correct):** True. Stacking active tiers multiplies volumetric power density over a constant package heat sink area.
    - **Option D (Incorrect Distractor):** False. Copper TSVs have high thermal conductivity (~390 W/m*K) and actively assist vertical heat conduction.

    **3. Silicon Architect's Takeaway:**
    Thermal trapping in 3D stacks creates 25–45°C top-tier temperature elevation, requiring thermal TSVs, microfluidic cooling, or thermally-aware vertical task placement.

    *(Reference: C.-H. Chao, K.-C. Chen, and A.-Y. Wu, 'Routing-Based Traffic Migration and Buffer Allocation Schemes for 3-D NoC With Thermal Limit,' IEEE TVLSI, Vol. 21, No. 11, pp. 2118–2131, Nov. 2013. DOI: 10.1109/TVLSI.2012.2227852.)*

---

### Deep RL Topology Optimization and Hybrid Wireless TSVs
<a id="drl-wireless"></a>

Recent innovations in vertical interconnects have explored machine learning optimization and hybrid signaling:
- **Deep Reinforcement Learning (DRL) for 3D NoC Topology**: Deng et al. [[Deng2026DRL](#ref-deng2026drl)] formulated 3D NoC topology synthesis as a sequential decision process, using deep RL to prune and regrow TSV vertical links for high-speed data acquisition systems, reducing average packet latency by $14.3\\%$ and TSV area overhead by $33\\%$.
- **TSV-W: Wireless Hybrid Interconnects for 2.5D/3D Packaging**: Anim et al. [[Anim2026TSVW](#ref-anim2026tsvw)] proposed TSV-W, integrating vertical through-silicon via pillars with near-field wireless antennas to circumvent high-frequency parasitic substrate loss and thermal bottlenecks in advanced multi-die stacks.

---

## References & Bibliography

1. <a id="ref-pavlidis2009"></a>**[Pavlidis2009]** V. F. Pavlidis and E. G. Friedman, *Three-Dimensional Integrated Circuit Design*, Morgan Kaufmann, Burlington, MA, 2009. ISBN: 978-0-12-374343-5.
2. <a id="ref-loi2011"></a>**[Loi2011]** I. Loi, F. Angiolini, S. Fujita, S. Mitra, and L. Benini, "Characterization and Implementation of Fault-Tolerant Vertical Links for 3-D Networks-on-Chip," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 30, no. 1, pp. 124–134, Jan. 2011. [DOI: 10.1109/TCAD.2010.2065990](https://doi.org/10.1109/TCAD.2010.2065990).
3. <a id="ref-seiculescu2010"></a>**[Seiculescu2010]** C. Seiculescu, S. Murali, L. Benini, and G. De Micheli, "SunFloor 3D: A Tool for Networks on Chip Topology Synthesis for 3-D Systems on Chips," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 29, no. 12, pp. 1987–2000, Dec. 2010. [DOI: 10.1109/TCAD.2010.2061610](https://doi.org/10.1109/TCAD.2010.2061610).
4. <a id="ref-more2018"></a>**[More2018]** A. More, V. Pano, and B. Taskin, "Vertical Arbitration-Free 3-D NoCs," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 37, no. 9, pp. 1853–1866, Sept. 2018. [DOI: 10.1109/TCAD.2017.2768415](https://doi.org/10.1109/TCAD.2017.2768415).
5. <a id="ref-alalousi2026"></a>**[AlAlousi2026]** A. Al-Alousi, M. Li, and H. Meng, "Vendor-Independent Design Space Exploration and Resource Optimization Framework for 3-D Networks-on-Chip Using Hypergraph-Genetic Algorithm Integration," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 45, no. 5, pp. 2236–2248, May 2026. [DOI: 10.1109/TCAD.2025.3616073](https://doi.org/10.1109/TCAD.2025.3616073).
6. <a id="ref-chao2013"></a>**[Chao2013]** C.-H. Chao, K.-C. Chen, and A.-Y. Wu, "Routing-Based Traffic Migration and Buffer Allocation Schemes for 3-D Network-on-Chip Systems With Thermal Limit," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 21, no. 11, pp. 2118–2131, Nov. 2013. [DOI: 10.1109/TVLSI.2012.2227852](https://doi.org/10.1109/TVLSI.2012.2227852).
7. <a id="ref-skadron2003"></a>**[Skadron2003]** K. Skadron, M. R. Stan, W. Huang, S. Velusamy, K. Sankaranarayanan, and D. Tarjan, "Temperature-Aware Microarchitecture," in *Proceedings of the 30th Annual International Symposium on Computer Architecture (ISCA)*, 2003, pp. 2–13. [DOI: 10.1145/859618.859620](https://doi.org/10.1145/859618.859620).
8. <a id="ref-huang2006"></a>**[Huang2006]** W. Huang, S. Ghosh, S. Velusamy, K. Sankaranarayanan, K. Skadron, and M. R. Stan, "HotSpot: A Compact Thermal Modeling Methodology for Early-Stage VLSI Design," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 14, no. 5, pp. 501–513, May 2006. [DOI: 10.1109/TVLSI.2006.876103](https://doi.org/10.1109/TVLSI.2006.876103).
9. <a id="ref-ieee1500"></a>**[IEEE1500]** IEEE, "IEEE Standard Testability Method for Embedded Core-Based Integrated Circuits," *IEEE Std 1500-2005*, 2005. [DOI: 10.1109/IEEESTD.2005.97445](https://doi.org/10.1109/IEEESTD.2005.97445).
10. <a id="ref-agrawal2014test"></a>**[Agrawal2014Test]** V. D. Agrawal et al., "Testing of 3-D Integrated Circuits: Challenges and Solutions," in *Proceedings of the IEEE International Test Conference (ITC)*, 2014, pp. 1–10. [DOI: 10.1109/TEST.2014.7035310](https://doi.org/10.1109/TEST.2014.7035310).
11. <a id="ref-smith1999"></a>**[Smith1999]** L. D. Smith, R. E. Anderson, D. W. Forehand, T. J. Pelc, and T. Roy, "Power Distribution System Design Methodology and Capacitor Selection for Modern CMOS Technology," *IEEE Transactions on Advanced Packaging*, vol. 22, no. 3, pp. 284–291, Aug. 1999. [DOI: 10.1109/6040.784478](https://doi.org/10.1109/6040.784478).
12. <a id="ref-deng2026drl"></a>**[Deng2026DRL]** Y. Deng et al., "Topology Optimization of 3-D NoC for High-Speed Data Acquisition Systems via Deep Reinforcement Learning," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 34, no. 7, pp. 2213–2226, July 2026. [DOI: 10.1109/TVLSI.2026.3690001](https://doi.org/10.1109/TVLSI.2026.3690001).
13. <a id="ref-anim2026tsvw"></a>**[Anim2026TSVW]** K. Anim, B. Taskin, A. Ganguly, and K. R. Dandekar, "TSV-W for 2.5-D IC Wireless Interconnects," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 34, no. 6, pp. 1801–1812, June 2026. [DOI: 10.1109/TVLSI.2026.3671654](https://doi.org/10.1109/TVLSI.2026.3671654).
