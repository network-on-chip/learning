# Chapter 8: Three-Dimensional Networks-on-Chip (3D-NoC) & TSVs

[![Companion Platform](https://img.shields.io/badge/Interactive%20Lab-Chiplet%20Tycoon-0f766e?logo=bookstack&logoColor=white)](https://network-on-chip.github.io/learning/interactive/chiplet/)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%206%3A%20Chiplets%20%26%203D-blue)](https://network-on-chip.github.io/learning/track6-chiplets-and-3d/)
[![Simulation Model](https://img.shields.io/badge/Python%20Model-tsv__vertical__mesh__sim.py-blueviolet)](code/tsv_vertical_mesh_sim.py)
[![Hardware RTL](https://img.shields.io/badge/Verilog%20RTL-tsv__arbiter__3d.v-success)](code/tsv_arbiter_3d.v)

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
1. **Dramatically Shortened Interconnect Lengths**: A $4 \times 4 \times 4$ 3D mesh containing 64 cores has a maximum network diameter of $(3 + 3 + 3) = 9$ hops, compared to $(7 + 7) = 14$ hops in an $8 \times 8$ 2D mesh, reducing average packet hop distance by more than **$35\%$**.
2. **Heterogeneous Technology Stacking**: Different functional tiers can be fabricated in independently optimized process technologies—for example, stacking a 3nm logic compute tier directly on top of a 14nm embedded DRAM (eDRAM) tier or an analog RF transceiver tier.
3. **Massive Vertical Bandwidth Density**: Thousands of TSVs operating in parallel provide terabits-per-second inter-tier bandwidth with sub-100 picosecond propagation delays.

---

## 8.2 Through-Silicon Via (TSV) Physical Characteristics & Parasitics

A Through-Silicon Via is a microscopic copper plug etched vertically through the bulk silicon substrate of a thinned wafer (typically $20\ \mu\text{m}\text{ to }50\ \mu\text{m}$ thick) and insulated from the conductive silicon by a thin dielectric liner (such as $\text{SiO}_2$ or $\text{Si}_3\text{N}_4$).

![Figure 8.1: TSV bundle in bulk silicon technology showing Metal 1 landing pad routing. [Reproduced from: I. Loi et al., "Characterization and Implementation of Fault-Tolerant Vertical Links for 3-D Networks-on-Chip", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 30, No. 1, pp. 124-134, Jan. 2011, DOI: 10.1109/TCAD.2010.2065990. © 2011 IEEE]](figures/loi_fig02_tsv_bundle.png)

![Figure 8.2: Circuit-level lumped parasitic model of a multi-TSV bundle. [Reproduced from: I. Loi et al., "Characterization and Implementation of Fault-Tolerant Vertical Links for 3-D Networks-on-Chip", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 30, No. 1, pp. 124-134, Jan. 2011, DOI: 10.1109/TCAD.2010.2065990. © 2011 IEEE]](figures/loi_fig03_tsv_schematic.png)

### 8.2.1 Lumped Electrical Model
As characterized by **I. Loi et al. (IEEE TCAD 2011)** and depicted in Figures 8.1 and 8.2, each TSV is modeled as a lumped $\pi$-network containing:

1. **Ohmic Resistance ($R_{\text{tsv}}$)**: Due to the high electrical conductivity of electroplated copper:

    $$R_{\text{tsv}} = \rho_{\text{Cu}} \frac{h_{\text{tsv}}}{\pi (d_{\text{tsv}} / 2)^2}$$

    For a typical TSV with height $h_{\text{tsv}} = 30\ \mu\text{m}$ and diameter $d_{\text{tsv}} = 4\ \mu\text{m}$, $R_{\text{tsv}} \approx 30\text{ to }50\text{ m}\Omega$—orders of magnitude lower than millimeter-long planar metal traces.

2. **Insulator Oxide Capacitance ($C_{\text{ox}}$)**: Formed between the cylindrical copper core and the substrate across the thin $\text{SiO}_2$ liner ($t_{\text{ox}} \approx 100\text{ to }200\text{ nm}$):

    $$C_{\text{ox}} = \frac{2 \pi \epsilon_{\text{ox}} \epsilon_0 h_{\text{tsv}}}{\ln\left(\frac{r_{\text{tsv}} + t_{\text{ox}}}{r_{\text{tsv}}}\right)} \approx 20\text{ to }50\text{ fF}$$

3. **Substrate Conductance and Inter-TSV Coupling ($C_{\text{sub}}, G_{\text{sub}}$)**: High-frequency signals couple through the lossy silicon substrate to neighboring TSVs, requiring ground shielding vias or differential signaling to suppress inter-wire crosstalk.

### 8.2.2 The Keep-Out Zone (KOZ)
Copper has a coefficient of thermal expansion ($\alpha_{\text{Cu}} \approx 17.0\text{ ppm/K}$) nearly an order of magnitude higher than silicon ($\alpha_{\text{Si}} \approx 2.6\text{ ppm/K}$). During thermal cycling from annealing ($350^\circ\text{C}$) to room temperature, the expanding copper exerts hundreds of megapascals of thermo-mechanical compressive stress onto the surrounding silicon crystal.

Via the **piezoresistive effect**, this mechanical stress alters silicon band structure, shifting CMOS transistor mobility by up to **$\pm 30\%$** and inducing clock skew. Consequently, standard cells cannot be placed within a radial boundary of $3\ \mu\text{m}\text{ to }5\ \mu\text{m}$ surrounding each TSV—a silicon exclusion area known as the **Keep-Out Zone (KOZ)**.

---

## 8.3 3D Router Microarchitectures & Vertical Arbitration

In a planar 2D mesh, routers have 5 ports: North, South, East, West, and Local. Extending the network to 3D requires two additional ports: **Up** ($+Z$) and **Down** ($-Z$).

![Figure 8.3: 3D Network-on-Chip router microarchitecture structures: 7-port full crossbar vs. hybrid partitioned routers. [Reproduced from: A. More et al., "Vertical Arbitration-Free 3-D NoCs", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 37, No. 9, pp. 1853-1866, Sept. 2018, DOI: 10.1109/TCAD.2017.2768415. © 2018 IEEE]](figures/more_fig01_3d_router_structs.png)

![Figure 8.4: Comparison of (a) traditional arbitrated vertical links versus (b) vertical arbitration-free fast-path designs. [Reproduced from: A. More et al., "Vertical Arbitration-Free 3-D NoCs", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 37, No. 9, pp. 1853-1866, Sept. 2018, DOI: 10.1109/TCAD.2017.2768415. © 2018 IEEE]](figures/more_fig04_arbitration_free.png)

### 8.3.1 The Silicon Area Penalty of Full 7-Port Crossbars
As shown in Figure 8.3, expanding a router crossbar from 5 to 7 ports increases internal crossbar multiplexer complexity quadratically:

$$\text{Crosspoints} = P^2 = 7^2 = 49 \quad \text{vs.} \quad 5^2 = 25 \quad (+96\% \text{ area})$$

Moreover, 7 input buffers demand significant silicon real estate and static leakage.

### 8.3.2 Shared Vertical Links & Vertical Arbitration Contention
To economize TSV footprint and routing area, many architectures deploy **shared vertical pillars** where multiple adjacent planar nodes share a single vertical TSV channel. However, as proven by **A. More, V. Pano, and B. Taskin (IEEE TCAD 2018)**:
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

While 3D stacking slashes communication latency, it creates an acute physical challenge: **thermal trapping**.

```
   Tier 2 (Top Stack):     [ High-Power Compute Cores ]  <-- T_max = 136.5°C (Extreme Heat Trapping)
   ----------------------------------------------------      Thermal Resistance: R_inter (Dielectric)
   Tier 1 (Middle Tier):   [ High-Power Compute Cores ]  <-- T = 123.7°C
   ----------------------------------------------------      Thermal Resistance: R_inter (Dielectric)
   Tier 0 (Bottom Tier):   [ Lower-Power Memory / IO  ]  <-- T = 97.2°C
   ====================================================      Thermal Resistance: R_hs (TIM + Spreader)
   [ COPPER HEAT SPREADER & EXTERNAL FORCED-AIR HEATSINK ]  <-- Ambient Air = 45.0°C
```

In standard single-die packaging, silicon sits directly on the package heat sink. In 3D-ICs, only **Tier 0** is directly adjacent to the heat spreader. Heat generated in **Tier 1** and **Tier 2** must conduct through intervening bulk silicon substrates and low-conductivity dielectric bonding interfaces ($\text{SiO}_2$ or polymer adhesive, $k_{\text{th}} \approx 0.2\text{ to }1.4\text{ W/(m}\cdot\text{K)}$).

As demonstrated by our simulation model, under equivalent uniform workloads, top-tier silicon reaches **$136.5^\circ\text{C}$**—an alarming **$+39.3^\circ\text{C}$ thermal stacking penalty** over bottom-tier silicon ($97.2^\circ\text{C}$).

---

## 8.5 TSV Defect Tolerance & Redundancy

TSV fabrication involves deep reactive-ion etching (DRIE), liner chemical vapor deposition, copper electroplating, chemical-mechanical polishing (CMP), and high-precision wafer bonding. A single physical void, seam, or micro-crack breaks the vertical link, ruining the entire multi-die stack.

### 8.5.1 Redundancy Configurations
To achieve viable manufacturing yield, modern 3D-NoC designs deploy hardware redundancy:
- **Double-TSV Bundles**: Routing each critical signal bit through two parallel TSVs. If one suffers an open defect, the redundant path maintains continuity.
- **$N:1$ Spare TSV Multiplexing**: Grouping a 32-bit flit bus into 4 bundles of 8 bits, each protected by 1 spare TSV and a dynamic multiplexer steering network. As proved by Loi et al.~\cite{Loi2011}, this raises vertical link yield from **$66\%$ to $98\%$** with only a **$2.1\%$ router area overhead**.

---

## 8.6 Hardware Microarchitecture: 7-Port Vertical Link Arbiter

Below is the synthesizable Verilog implementation of the 3D router vertical link arbiter with runtime TSV defect bypass logic from [`code/tsv_arbiter_3d.v`](code/tsv_arbiter_3d.v).

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

The companion simulation script [`code/tsv_vertical_mesh_sim.py`](code/tsv_vertical_mesh_sim.py) evaluates a $4 \times 4 \times 3$ mesh (48 cores) under uniform random traffic comparing **3D XYZ Dimension-Order Routing** and **ZXY Dimension-Order Routing**.

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

1. **Interconnect Volume Folding**: 3D stacking replaces long, high-resistance planar lines with short Through-Silicon Vias, reducing average network hop count by $>35\%$.
2. **TSV Parasitics & KOZ**: While TSV electrical resistance is tiny ($<50\text{ m}\Omega$), substrate capacitive coupling ($30\text{--}50\text{ fF}$) and thermo-mechanical stress require careful keep-out zones.
3. **Crossbar Overhead**: 7-port full 3D crossbars double internal crosspoint complexity ($P^2 = 49$ vs. $25$); vertical arbitration-free fast-paths and shared vertical channels mitigate silicon area penalties.
4. **Thermal Trapping**: Heat generated in upper tiers must traverse multiple bonding interfaces to reach the heatsink, elevating top-tier temperatures by up to $+40^\circ\text{C}$ and demanding thermal-aware 3D routing.

### Companion Platform Interactive Labs
- **[Interactive Lab: Chiplet Tycoon](https://network-on-chip.github.io/learning/interactive/chiplet/)**: Architect multi-die 2.5D and 3D stacked topologies with live TSV latency and thermal throttling gauges.
- **[Curriculum Track 6: Chiplets & 3D Interconnects](https://network-on-chip.github.io/learning/track6-chiplets-and-3d/)**: Master die-to-die PHY protocols, TSV Keep-Out Zones, and vertical routing algorithms.

---

## 8.9 Comprehensive Problem Set & Solutions

### Problem 8.1: TSV Elmore Delay vs. Planar Intermediate Metal Wire
Compare the propagation delay of a vertical TSV link versus a planar intermediate metal layer (M5) wire in a 7nm technology node:
- **TSV Parameters**: Height $h_{\text{tsv}} = 40\ \mu\text{m}$, diameter $d_{\text{tsv}} = 4\ \mu\text{m}$, copper resistivity $\rho = 1.7 \times 10^{-8}\ \Omega\cdot\text{m}$, oxide liner thickness $t_{\text{ox}} = 150\text{ nm}$, $\epsilon_r = 3.9$, driver resistance $R_d = 400\ \Omega$.
- **Planar Wire Parameters**: Length $L_{\text{wire}} = 1.5\text{ mm}$ (spanning one router tile), resistance $r_{\text{wire}} = 80\ \Omega/\text{mm}$, capacitance $c_{\text{wire}} = 180\text{ fF/mm}$, driver resistance $R_d = 400\ \Omega$.
1. Calculate the resistance and capacitance of the TSV ($R_{\text{tsv}}, C_{\text{tsv}}$).
2. Calculate the Elmore delay of the TSV link: $\tau_{\text{tsv}} = R_d C_{\text{tsv}} + R_{\text{tsv}} C_{\text{tsv}} / 2$.
3. Calculate the Elmore delay of the planar wire: $\tau_{\text{planar}} = R_d C_{\text{wire}} + R_{\text{wire}} C_{\text{wire}} / 2$.
4. Determine the speedup of the vertical TSV link over the planar wire.

#### Solution:

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

### Problem 8.2: 3D-IC Stacking Thermal Gradient Calculation
A 3-tier 3D-IC stack dissipates power uniformly across each layer: $P_0 = P_1 = P_2 = 25.0\text{ W}$ ($P_{\text{total}} = 75.0\text{ W}$). The bottom tier (Tier 0) is attached to a forced-convection heat sink with thermal resistance $R_{\text{hs}} = 0.40\text{ K/W}$ to ambient air ($T_{\text{amb}} = 40.0^\circ\text{C}$). The inter-tier bonding interfaces each have an effective thermal resistance of $R_{\text{inter}} = 0.35\text{ K/W}$.
1. Derive the mathematical expressions for the steady-state temperature of each tier ($T_0, T_1, T_2$).
2. Compute the exact temperatures of Tier 0, Tier 1, and Tier 2.
3. What is the temperature differential between the top tier and bottom tier?

#### Solution:

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
