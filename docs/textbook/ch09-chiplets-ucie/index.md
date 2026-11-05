# Chapter 9: Multi-Chiplet Interconnects, 2.5D Systems & UCIe

[![Companion Platform](https://img.shields.io/badge/Interactive%20Lab-Chiplet%20Tycoon-0f766e?logo=bookstack&logoColor=white)](https://network-on-chip.github.io/learning/interactive/chiplet/)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%206%3A%20Chiplets%20%26%203D-blue)](https://network-on-chip.github.io/learning/track6-chiplets-and-3d/)
[![Simulation Model](https://img.shields.io/badge/Python%20Model-ucie__d2d__latency__model.py-blueviolet)](code/ucie_d2d_latency_model.py)
[![Hardware RTL](https://img.shields.io/badge/Verilog%20RTL-chiplet__bridge__protocol.v-success)](code/chiplet_bridge_protocol.v)

---

## 9.1 The Chiplet Revolution: Breaking the Monolithic Barrier

> [!NOTE] 💡 High-School Intuition: The Giant Pizza Problem (Why the World Switched to Chiplets)
> Imagine you are a baker running a pizza kitchen. If you try to bake one **gigantic pizza the size of a dining table** ($800\text{ mm}^2$), what happens if a single fly or dust speck lands anywhere on it during baking? The health inspector forces you to throw the **entire giant pizza** into the dumpster! Because tiny dust particles randomly land on silicon wafers during manufacturing, attempting to print one massive monolithic chip means up to **$75\%$ of the wafer is ruined and discarded**.
>
> Now imagine instead baking **four separate personal-sized pizzas** ($200\text{ mm}^2$ each) and placing them side by side on a serving board. If a dust speck lands on one pizza, you throw away only that single small pizza and serve the other three! Your success rate skyrockets from $25\%$ to **over $80\%$**.
>
> This is the secret behind the modern **chiplet revolution**: instead of carving one huge, fragile, ultra-expensive chip out of silicon, engineers build smaller modular silicon "tiles" (chiplets) and connect them together with microscopic high-speed wires!

For over four decades, Moore's Law advanced by packing ever-more transistors onto a single continuous slice of silicon called a **monolithic die**. In modern sub-3nm nodes, this approach has hit two hard physical and economic walls:

1. **The Optical Reticle Limit (The Camera Viewfinder)**:
   - Semiconductor chips are printed using photolithography machines (scanners) that shine extreme ultraviolet (EUV) light through a quartz mask onto a silicon wafer.
   - Just like a smartphone camera has a fixed rectangular viewfinder, the photolithography machine has a physical lens window called the **optical reticle limit** (typically $26\text{ mm} \times 33\text{ mm} \approx 858\text{ mm}^2$).
   - Modern artificial intelligence processors (like NVIDIA Blackwell or AMD Instinct) require over $1000\text{--}1500\text{ mm}^2$ of silicon—larger than the machine's lens can print in a single shot!
2. **Defect Density & Exponential Yield Collapse**:
   - Manufacturing yield $Y$ (the percentage of functional chips on a wafer) decays exponentially with chip area $A$ under the Murphy and Seeds models:
     $$Y = \left( \frac{1 - e^{-A \cdot D_0}}{A \cdot D_0} \right)^2 \quad \text{or} \quad Y = e^{-\sqrt{A \cdot D_0}}$$
   - Here, $A$ is the chip area ($\text{cm}^2$) and $D_0$ is the defect density (random dust specks per $\text{cm}^2$).
   - A massive $800\text{ mm}^2$ die ($A = 8.0\text{ cm}^2$) has a yield below $25\%$. Cutting it into four $200\text{ mm}^2$ chiplets ($A = 2.0\text{ cm}^2$) lifts individual yield above $82\%$, cutting total manufacturing costs by more than half!
3. **The LEGO Principle (Process Node Specialization)**:
   - You wouldn't make the bumper of a car out of pure titanium if steel works just as well.
   - Advanced 3nm silicon is astronomical in price. High-speed compute cores (AI tensor units and CPUs) thrive on 3nm scaling. However, analog circuits, clock generators (PLLs), and USB/PCIe memory controllers do not shrink well at 3nm.
   - Chiplets allow architects to build compute cores in cutting-edge 3nm, while building memory controllers and I/O hubs in mature, inexpensive 14nm or 7nm silicon, snapping them together like LEGO bricks.

```
       Monolithic SoC vs. Multi-Chiplet Modular Disaggregation
       
       [ Monolithic Die (800 mm2) ]            [ Disaggregated Multi-Chiplet System ]
       +--------------------------+            +------------------------------------+
       | Compute Cores (3nm)      |            |  [Compute 1]     [Compute 2]       |
       | + Analog PLLs            |   ====>    |    (3nm)            (3nm)          |
       | + High-V I/O Transceivers|            |       \              /             |
       | + Memory Controllers     |            |    ==== [Active Interposer] ====   |
       | Yield: ~25% (High Cost)  |            |       /              \             |
       +--------------------------+            |  [Compute 3]     [I/O & Memory]    |
         Optical Reticle Bounded               |    (3nm)           (14nm / 7nm)    |
                                               +------------------------------------+
                                                 Yield: >82% per die (Lower Cost)
```

---

## 9.2 2.5D Packaging Taxonomies: How Chiplets Talk to Each Other

> [!TIP] 💡 High-School Intuition: Dirt Roads vs. 16-Lane Glass Bridges
> If you have two houses on opposite sides of a river, how do you travel between them?
> - **Standard Organic Packaging**: Like driving across a bumpy dirt road. The wires are thick, far apart ($110\ \mu\text{m}$ pitch), and slow. It takes lots of energy ($1.2\text{ pJ/bit}$) to push electrical signals across centimeters of circuit board.
> - **Advanced Silicon Interposer (2.5D)**: Like building a **16-lane high-speed glass bridge** directly between the two houses! The bridge is made of pure polished silicon. The wires are microscopic ($45\ \mu\text{m}$ micro-bumps, thousands of lines), ultra-short ($1.8\text{ mm}$), and lightning-fast. It takes less than **one-third the energy** ($0.33\text{ pJ/bit}$) and carries **four times more data**!

As classified by **Z. Chen et al. (IEEE TVLSI 2026)** and illustrated in Figure 9.1, multi-chiplet packaging spans four distinct integration categories:

![Figure 9.1: Multi-chiplet packaging taxonomy: (a) Standard organic substrate, (b) 2.5D silicon interposer, (c) Embedded silicon bridge (e.g., Intel EMIB), and (d) 3D hybrid bonding. [Reproduced from: Z. Chen et al., "HiRe: A Hierarchical Reconfigurable Architecture for Large-Scale Multichiplet DNN Accelerators", IEEE Transactions on Very Large Scale Integration (VLSI) Systems, Vol. 34, No. 4, pp. 880-893, 2026, DOI: 10.1109/TVLSI.2026.3676552. © 2026 IEEE]](figures/chen_fig02_chiplet_packaging_taxonomy.png)

### 9.2.1 Packaging Substrate Comparison

| Packaging Technology | Bump Pitch ($\mu\text{m}$) | Channel Length | Shoreline Bandwidth Density | Energy Efficiency | Cost & Complexity |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Standard Organic Substrate** | $100\text{--}130$ | $10\text{--}25\text{ mm}$ | $100\text{--}150\text{ Gbps/mm}$ | $1.0\text{--}1.5\text{ pJ/bit}$ | Low cost, standard PCB/laminate manufacturing |
| **Passive Silicon Interposer (2.5D)** | $25\text{--}55$ | $1\text{--}3\text{ mm}$ | $700\text{--}1300\text{ Gbps/mm}$ | $0.2\text{--}0.4\text{ pJ/bit}$ | Moderate-high cost; subject to interposer reticle limit |
| **Embedded Bridge (EMIB)** | $25\text{--}45$ | $1\text{--}2\text{ mm}$ | $600\text{--}1000\text{ Gbps/mm}$ | $0.3\text{--}0.5\text{ pJ/bit}$ | Localized silicon cavities inside organic carrier |
| **Active Silicon Interposer** | $20\text{--}40$ | Distributed | $>1000\text{ Gbps/mm}$ | $0.3\text{--}0.6\text{ pJ/bit}$ | Active CMOS logic, routers, DC-DC converters in base die |

### 9.2.2 Active Silicon Interposers: The IntAct Architecture

![Figure 9.2: IntAct active interposer system architecture integrating six 16-core chiplets (96 cores total) over an active interposer 2D mesh NoC. [Reproduced from: P. Vivet et al., "IntAct: A 96-Core Processor With Six Chiplets 3D-Stacked on an Active Interposer With Distributed Interconnects and Integrated Power Management", IEEE Journal of Solid-State Circuits, Vol. 56, No. 1, pp. 79-97, Jan. 2021, DOI: 10.1109/JSSC.2020.3036341. © 2021 IEEE]](figures/vivet_fig03_active_interposer.png)

In passive interposers, the carrier wafer contains only copper wiring traces. In contrast, the **IntAct system (P. Vivet et al., IEEE JSSC 2021)**, shown in Figure 9.2, introduces an **Active Silicon Interposer**:
- Six 16-core compute chiplets (96 cores total) are 3D-stacked onto an active 28nm base die.
- The active interposer is not just a passive floor: it hosts active transistors, a distributed $6 \times 4$ network-on-chip router fabric, and on-chip voltage converters.
- Compute chiplets communicate via asynchronous micro-bump links, achieving $3.0\text{ Tbps}$ of total die-to-die bandwidth.

---

## 9.3 The Universal Chiplet Interconnect Express (UCIe) Standard

> [!NOTE] 💡 High-School Intuition: A Universal USB Cable for Chiplets
> If AMD makes a compute chiplet, can you plug it into an Intel memory chiplet or an Apple graphics chiplet?
> In the past, no—every company used secret, proprietary wiring formats.
> **UCIe (Universal Chiplet Interconnect Express)** is like creating the **USB-C standard for chiplets**! It establishes a single open rulebook so that any chiplet built anywhere in the world can plug into any other chiplet and exchange data immediately.

```
       UCIe Architectural Protocol Stack
       +-------------------------------------------------------+
       | Protocol Layer: PCIe 6/7 | CXL.io/cache/mem | Raw NoC |
       +-------------------------------------------------------+
                                  | Flits (68B / 256B)
       +-------------------------------------------------------+
       | Die-to-Die (D2D) Adapter Layer:                       |
       |  - Link State Management & Arbitration                |
       |  - CRC Generation & Checking (CRC-16 / CRC-32)        |
       |  - Retransmission Retry Buffer (Go-Back-N / Selective)|
       |  - Credit-Based Flow Control Turnaround               |
       +-------------------------------------------------------+
                                  | Raw Flit Stream + Credits
       +-------------------------------------------------------+
       | Physical Layer (PHY):                                 |
       |  - Mainband Data (x16/x32/x64 Single-Ended Lanes)     |
       |  - Forwarded Differential Clocks & Track Signals      |
       |  - Sideband Management Channel (800 MHz Manchester)   |
       |  - Lane Deskew, Training & Equalization               |
       +-------------------------------------------------------+
```

### 9.3.1 The Three Layers of UCIe
1. **Protocol Layer (The Message)**: Speaks standard software languages: PCIe for peripherals, CXL for shared memory, and Raw Streaming for direct NoC flit tunneling.
2. **Die-to-Die Adapter Layer (The Postal Inspector)**: Packages messages into envelopes, adds error-checking stamps (CRC checksums), manages re-sending lost letters, and tracks mailbox space (credit flow control).
3. **Physical Layer (The Electrical Copper Lanes)**: The actual physical metal pins, analog drivers, and receivers that blast 0s and 1s across micro-bumps at up to $32\text{ Gbps}$ per wire.

---

## 9.4 Inter-Chiplet Latency, Bandwidth Density & Credit Turnaround

### 9.4.1 How Long Does It Take to Cross the Chiplet Boundary?
When a packet leaves Chiplet A and enters Chiplet B, it experiences multiple delays:
$$t_{\text{D2D}} = t_{\text{CDC}} + t_{\text{adapter}} + t_{\text{PHY\_tx}} + t_{\text{flight}} + t_{\text{PHY\_rx}} + t_{\text{deskew}} + t_{\text{CDC}}$$

In simple terms:
- **$t_{\text{flight}}$ (Flight Time)**: How long it takes electricity to speed down the wire. Since light moves through silicon dioxide at $\approx 150\text{ mm/ns}$ ($15\text{ cm per nanosecond}$), traveling across a short $1.5\text{ mm}$ bridge takes only $10\text{ picoseconds}$ ($0.01\text{ ns}$)!
- **$t_{\text{CDC}}$ (Clock Domain Crossing)**: Chiplet A and Chiplet B might run on different clock speeds (e.g., $2.5\text{ GHz}$ vs. $2.0\text{ GHz}$). Crossing clocks safely without corrupting data takes 2 to 3 clock cycles of waiting.

### 9.4.2 Little's Law: Why Transmitters Need Buffer Queues
Imagine you are playing catch with a friend across a field. If you throw a baseball, you must wait for your friend to throw a ball back before you can throw again. If you only own 1 baseball, you spend most of your time standing around waiting!

To keep throwing continuously at full speed, you need a basket of balls. How many balls do you need? Exactly enough to fill the round-trip flight time! This is **Little's Law** applied to flow control:
$$B_{\text{min}} \ge \lceil \text{RTT}_{\text{credit}} \cdot f_{\text{clk}} \rceil$$

If a round-trip credit token takes $8.5\text{ ns}$ to return at a $2.0\text{ GHz}$ clock ($0.5\text{ ns per cycle}$), the transmitter must have at least $\lceil 8.5 / 0.5 \rceil = 17\text{ flits}$ of buffer space. If the buffer is smaller than 17 flits, the transmitter runs out of tokens and sits completely idle, wasting valuable wire bandwidth.

---

## 9.5 Deadlock in Multi-Chiplet Networks & In/Outbound Swap Recovery

> [!IMPORTANT] 💡 High-School Intuition: The 4-Way Traffic Jam at an Intersection
> Imagine four cars approach a narrow 4-way intersection simultaneously.
> - Car 1 is waiting for Car 2 to move forward.
> - Car 2 is waiting for Car 3 to move forward.
> - Car 3 is waiting for Car 4 to move forward.
> - Car 4 is waiting for Car 1 to move forward!
> 
> **Nobody can move forward because each car holds the lane that someone else needs.** That is a **routing deadlock**!
>
> In multi-chiplet networks, even if each individual chiplet is perfectly organized inside, sending packets back and forth across chiplet bridges can accidentally form this exact circular traffic jam!
>
> **The In/Outbound Swap Solution**: Imagine a smart traffic cop watching the intersection. If the cars stay stuck for more than 10 seconds, the cop steps in and directs Car 1 to pull into a temporary driveway on the side of the road (a 2-flit swap escape register). The moment Car 1 pulls aside, Car 4 drives through! Then Car 3 drives through, then Car 2 drives through. Finally, Car 1 pulls out of the driveway and continues on its journey. **The gridlock is broken, and not a single car is lost!**

![Figure 9.3: Multi-chiplet routing deadlock scenario where local subpath dependencies cross die-to-die bridge boundaries, forming a closed resource dependency cycle across four chiplets. [Reproduced from: P. Wang et al., "In/Outbound Swap: A Backtracking-based Deadlock Recovery Mechanism for Multi-Chiplet Networks", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 45, No. 5, pp. 2100-2114, 2026, DOI: 10.1109/TCAD.2026.3688573. © 2026 IEEE]](figures/wang_fig01_chiplet_deadlock_subpath.png)

As demonstrated by **P. Wang et al. (IEEE TCAD 2026)** in Figure 9.3, combining deadlock-free local networks creates dangerous global dependency loops across bridge routers.

![Figure 9.4: Operational flow of the In/Outbound Swap deadlock recovery mechanism: stall timeout detection, swap request assertion, queue handshake, and circular dependency breaking. [Reproduced from: P. Wang et al., "In/Outbound Swap: A Backtracking-based Deadlock Recovery Mechanism for Multi-Chiplet Networks", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 45, No. 5, pp. 2100-2114, 2026, DOI: 10.1109/TCAD.2026.3688573. © 2026 IEEE]](figures/wang_fig02_swap_recovery_flow.png)

Instead of doubling or tripling hardware buffers across the entire chip, Wang et al.'s **In/Outbound Swap** mechanism (Figure 9.4):
1. **Counts stall cycles**: If a flit is stuck at a bridge boundary for longer than a threshold $\tau_{\text{stall}}$, deadlock is detected.
2. **Backtracks into an escape buffer**: The blocked head flit is shifted into a tiny 2-flit swap register.
3. **Breaks the cycle**: Trailing packets move forward, downstream credits free up, and normal routing resumes without dropping any packets.

---

## 9.6 Hardware Implementation: Synthesizable Chiplet D2D Bridge

The accompanying synthesizable Verilog module [`code/chiplet_bridge_protocol.v`](code/chiplet_bridge_protocol.v) shows how this logic is written in real hardware registers and clocks.

```verilog
// Snippet from code/chiplet_bridge_protocol.v: In/Outbound Swap Recovery Logic
always @(posedge local_clk or negedge local_rst_n) begin
    if (!local_rst_n) begin
        d2d_tx_data       <= {DATA_WIDTH{1'b0}};
        d2d_tx_valid      <= 1'b0;
        stall_counter     <= 16'd0;
        swap_active       <= 1'b0;
        deadlock_detected <= 1'b0;
    end else begin
        // Monitor buffer stalls at D2D boundary: are we stuck with zero credits?
        if (tx_flit_valid && !has_tx_credit) begin
            stall_counter <= stall_counter + 1'b1;
            if (stall_counter >= STALL_TIMEOUT) begin
                // Traffic jam detected! Trigger the swap cop:
                deadlock_detected <= 1'b1;
                swap_active       <= 1'b1;
                // Divert blocked head flit into swap escape register
                swap_buffer       <= tx_flit_data;
                swap_buffer_valid <= 1'b1;
            end
        end else begin
            stall_counter     <= 16'd0;
            deadlock_detected <= 1'b0;
        end
    end
end
```

---

## 9.7 Quantitative Evaluation & Simulation Results

The Python model [`code/ucie_d2d_latency_model.py`](code/ucie_d2d_latency_model.py) evaluates Standard Organic vs. Advanced Silicon Interposer packaging across latency, bandwidth, power, and buffer depths.

| Metric | Standard Organic Packaging | Advanced Silicon Interposer (UCIe-A) | Why It Matters |
| :--- | :---: | :---: | :--- |
| **Bump / Pad Pitch** | $110\ \mu\text{m}$ | **$45\ \mu\text{m}$** | $2.44\times\text{ tighter pin spacing}$ |
| **Trace Channel Length** | $15.0\text{ mm}$ | **$1.8\text{ mm}$** | $8.3\times\text{ shorter wire distance}$ |
| **One-Way Flight Delay** | $100.0\text{ ps}$ | **$12.0\text{ ps}$** | Electricity arrives $88\text{ ps faster}$ |
| **One-Way Total Latency** | $4.25\text{ ns}$ ($8.5\text{ cycles}$) | **$4.06\text{ ns}$** ($8.1\text{ cycles}$) | Fast real-time response |
| **Credit RTT ($\text{RTT}_{\text{credit}}$)** | $8.50\text{ ns}$ ($17.0\text{ cycles}$) | **$8.11\text{ ns}$** ($16.2\text{ cycles}$) | Token turnaround speed |
| **Minimum Buffer Depth ($B_{\text{min}}$)** | $17\text{ flits}$ | **$17\text{ flits}$** | Memory needed to prevent stalling |
| **Total Raw Bandwidth** | $0.51\text{ Tbps}$ ($64\text{ GB/s}$) | **$2.05\text{ Tbps}$** ($256\text{ GB/s}$) | **$4\times\text{ more data per second}$** |
| **Shoreline Bandwidth Density** | $145.5\text{ Gbps/mm}$ | **$711.1\text{ Gbps/mm}$** | **$4.88\times\text{ more data per mm of chip edge}$** |
| **Energy Efficiency** | $1.200\text{ pJ/bit}$ | **$0.330\text{ pJ/bit}$** | **$3.64\times\text{ less battery / heat wasted}$** |
| **Interface Total Power** | $614.4\text{ mW}$ | **$675.8\text{ mW}$** | $4\times$ data at virtually identical power |

Advanced silicon interposers achieve a staggering **$4.88\times$** higher shoreline bandwidth density and **$3.64\times$** higher energy efficiency compared to standard organic laminate packaging, proving essential for modern AI accelerator chiplet complexes.

---

## 9.8 Summary: What You Learned

- **The Big Picture**: Making one giant chip is like baking a giant table-sized pizza: one fly ruins the whole thing. Chiplets let us make smaller personal pizzas, lifting yields from $25\%$ to $>80\%$.
- **Packaging Matters**: Standard circuit boards are slow dirt roads ($1.2\text{ pJ/bit}$). Silicon interposers are 16-lane glass superhighways ($0.33\text{ pJ/bit}$).
- **UCIe is the USB-C of Chiplets**: It provides an open standard so different companies can connect their chiplets together seamlessly.
- **Deadlock Can Be Solved Intelligently**: When cross-die traffic jams occur, the In/Outbound Swap acts as a traffic cop, pulling one packet aside into a temporary driveway to clear the jam without dropping data.

---

## 9.9 Exercises and Review Questions

1. **The Giant Pizza Yield Problem**: A processor needs $800\text{ mm}^2$ of silicon. Under Murphy's yield model $Y = \left(\frac{1 - e^{-A \cdot D_0}}{A \cdot D_0}\right)^2$ with defect density $D_0 = 0.08\text{ defects/cm}^2$:
   - Calculate the yield if you make it as 1 giant $800\text{ mm}^2$ chip.
   - Calculate the yield if you split it into 4 small $200\text{ mm}^2$ chiplets.
   - Which approach wastes less silicon?
2. **Playing Catch (Buffer Sizing)**: If a die-to-die bridge operates at $2.5\text{ GHz}$ ($0.4\text{ ns per cycle}$) and a round-trip credit token takes $6.4\text{ ns}$ to return, how many flit buffers must the sender have to keep transmitting without stopping?
3. **The 4-Way Traffic Jam**: Draw an intersection where four cars are stuck in a circular wait. Explain how moving just one car into a side parking bay allows all other cars to drive away.
4. **Energy Comparison**: How much total energy (in Joules) is required to transmit $1\text{ Terabyte}$ ($8\text{ Terabits}$) across standard organic packaging ($1.2\text{ pJ/bit}$) versus an advanced silicon interposer ($0.33\text{ pJ/bit}$)?
