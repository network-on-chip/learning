# Chapter 10: Optical & Wireless Networks-on-Chip (ONoC / WNoC)

[![Companion Platform](https://img.shields.io/badge/Interactive%20Lab-Photon%20Pilot-0f766e?logo=bookstack&logoColor=white)](https://network-on-chip.github.io/learning/interactive/optical/)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%207%3A%20Emerging%20Frontiers-blue)](https://network-on-chip.github.io/learning/track7-emerging-frontiers/)
[![Simulation Model](https://img.shields.io/badge/Python%20Model-onoc__optical__loss__sim.py-blueviolet)](code/onoc_optical_loss_sim.py)
[![Hardware RTL](https://img.shields.io/badge/Verilog%20RTL-photonic__mrr__switch.v-success)](code/photonic_mrr_switch.v)

---

## 10.1 The Non-Traditional Interconnect Paradigm

> [!NOTE] 💡 Architectural Intuition: Garden Hoses vs. Laser Pointers
> Why are computer chips replacing copper wires with light beams and wireless radio waves?
> - **The Copper Wire (The Garden Hose)**: Imagine a very long, empty garden hose. To get water out of the nozzle at the far end, you first have to turn on the faucet and fill up the **entire volume of the hose** with water under high pressure. In electronics, every copper wire has electrical capacitance ($C$); before a 1 can reach the receiver, the transmitter has to spend electrical energy charging up the entire wire! This creates delay and generates lots of waste heat.
> - **The Optical Waveguide (The Laser Pointer)**: Now imagine shining a laser pointer across the room. The moment you press the button, photons travel across the room at the **speed of light**! Even better: it doesn't take more battery power whether you flash the laser slowly or blink it 10 billion times every second.
> - **The Wireless Link (The Walkie-Talkie)**: Passing messages through a 64-core grid of routers is like whispering a secret down 14 rows of desks in a classroom. A wireless link is like speaking into a **walkie-talkie**: every core in the room hears the broadcast in a single clock cycle!

```
       Non-Traditional Interconnects vs. Electrical Multi-Hop NoC
       
       Conventional Electrical NoC (Multi-Hop Routing):
       [ Core 00 ] ---> [ Router ] ---> [ Router ] ---> [ Router ] ---> [ Core 63 ]
       (High RC Wire Delay, 4-Stage Pipeline per Hop, Dynamic CV^2 Switching Loss)
       
       Optical Network-on-Chip (ONoC):
       [ Laser Source ] ==> [ Modulator ] ===(Lightwave Guided Waveguide)===> [ Photodetector ]
       (Speed-of-Light Transit, Wavelength Division Multiplexing, Fixed Laser Power)
       
       Wireless Network-on-Chip (WNoC):
       [ Core 00 / RF TX ] ~ ~ ~ (Free-Space / Dielectric mmWave Broadcast) ~ ~ ~> [ Cores 01..63 ]
       (Single-Cycle Global Broadcast, Zero Buffer Latency, High-Bandwidth Aggregation)
```

---

## 10.2 Silicon Nanophotonics: Guiding Light Inside a Microchip

Silicon nanophotonics allows engineers to build microscopic "fiber optic cables" directly on a computer chip! Standard silicon has a high refractive index ($n_{\text{Si}} \approx 3.48$), while glass insulation ($\text{SiO}_2$) has a lower index ($n_{\text{ox}} \approx 1.45$). Just like light stays trapped inside a swimming pool when viewed from an angle (**Total Internal Reflection**), light stays trapped inside a tiny silicon wire called an **optical waveguide** ($450\text{ nm}$ wide).

### 10.2.1 Micro-Ring Resonators: The Optical Tuning Fork

> [!TIP] 💡 Architectural Intuition: The Musical Tuning Fork
> If you have a musical tuning fork tuned to middle C ($261.6\text{ Hz}$), what happens when a singer sings middle C across the room? The tuning fork catches the sound wave and begins to vibrate! But if the singer sings a D or an E, the tuning fork ignores it completely.
>
> An **optical Micro-Ring Resonator (MRR)** is a microscopic silicon ring that acts as an **optical tuning fork**. It has a specific cavity size ($R \approx 5\text{--}10\ \mu\text{m}$). When light of its exact resonant color (wavelength $\lambda_{\text{res}}$) arrives, it gets pulled into the ring and sent to the drop port. All other colors pass straight through!
>
> This lets us do **Wavelength Division Multiplexing (WDM)**: we can send 16 different colors of light through a single microscopic waveguide at the same time, multiplying bandwidth by $16\times$!

The resonant condition is governed by:

$$m \lambda_{\text{res}} = 2 \pi R \cdot n_{\text{eff}}$$

where $m$ is an integer (the mode number), $R$ is the ring radius, and $n_{\text{eff}}$ is the effective refractive index.

### 10.2.2 Switching Elements: Crossing (CSE) vs. Parallel (PSE)

![Figure 10.1: MRR switching structures: (a) 90-degree Crossing Switching Element (CSE), (b) 270-degree CSE, and (c) Parallel Switching Element (PSE). [Reproduced from: W.-Y. Kao et al., "Provably Good Physically Aware WRONoC Design for Customized and Fault-Tolerant Topologies With Parallel Switching Elements and Sequence-Based Models", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 45, No. 3, pp. 650-663, 2026, DOI: 10.1145/3658617.3697557. © 2026 IEEE]](figures/kao_fig01_mrr_structures.png)

How do we switch light between waveguides? As shown by **W.-Y. Kao et al. (IEEE TCAD 2026)** in Figure 10.1:
1. **Crossing Switching Elements (CSEs)**: The ring is placed at a perpendicular 90-degree crossroad. Every time light crosses another waveguide, some light scatters away ($0.1\text{--}0.2\text{ dB}$ loss). In a large chip, passing through 60 crossings dims the light significantly!
2. **Parallel Switching Elements (PSEs)**: The ring is placed between two parallel waveguides. Light transfers smoothly without needing any perpendicular crossings, keeping the light beam bright and clear.

![Figure 10.2: Add-Drop Filter (ADF) structures with default paths (straight through) and non-default paths (switched via MRR coupling). [Reproduced from: W.-Y. Kao et al., "Provably Good Physically Aware WRONoC Design for Customized and Fault-Tolerant Topologies With Parallel Switching Elements and Sequence-Based Models", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 45, No. 3, pp. 650-663, 2026, DOI: 10.1145/3658617.3697557. © 2026 IEEE]](figures/kao_fig02_adf_structures.png)

---

## 10.3 Optical Loss Modeling & Laser Power

### 10.3.1 Where Does the Light Go? (Optical Loss Budget)
As light travels from the laser to the photodetector, it loses a fraction of its power at every step:

$$L_{\text{path}}(\text{dB}) = L_{\text{prop}} + L_{\text{bend}} + L_{\text{cross}} + L_{\text{thru}} + L_{\text{drop}} + L_{\text{mod}}$$

- **Waveguide Length**: Light dims as it travels ($0.25\text{ dB/cm}$).
- **Bends**: Bending light around sharp corners radiates a tiny bit of light into the silicon ($0.005\text{ dB/bend}$).
- **Crossings**: Intersecting other waveguides scatters light ($0.12\text{ dB/crossing}$).
- **Drop Rings**: Transferring into a ring costs $\approx 0.5\text{ dB}$.

### 10.3.2 Sizing the Laser Source
The photodetector needs at least $-20\text{ dBm}$ ($0.01\text{ mW}$) of light to distinguish a 0 from a 1 reliably. If the path loss is $10\text{ dB}$ (which means $90\%$ of the light is lost along the way), the laser must shine at least $10\times$ brighter ($0.1\text{ mW}$) to compensate!

Because electrical laser power scales exponentially with decibel loss ($P \propto 10^{L_{\text{max}} / 10}$), every $3\text{ dB}$ you save cuts laser power consumption in half.

---

## 10.4 Thermal Drift: What Happens When the Chip Gets Hot?

> [!WARNING] 💡 Architectural Intuition: The Out-of-Tune Guitar
> If you leave a guitar in the hot sun, the strings expand, and the guitar goes completely out of tune!
> 
> Silicon does the exact same thing! Silicon has a positive **thermo-optic coefficient**: as temperature rises, silicon's refractive index changes, causing the micro-ring resonator to expand optically by **$0.10\text{ nm}$ for every $1^\circ\text{C}$ of heat**!
>
> Since our color channels are only $0.8\text{ nm}$ apart, if you play a demanding 3D game and your CPU heats up by just $8^\circ\text{C}$, the optical ring shifts completely into the next channel, causing garbled data or complete silence!
>
> To solve this, every optical ring has a tiny **electric microheater**. A smart temperature controller monitors the ring and keeps it at a steady, warm baseline temperature (e.g., $55^\circ\text{C}$), keeping the "tuning fork" perfectly in tune.

![Figure 10.3: System-level thermal simulation of an Optical NoC demonstrating core active power dissipation, non-uniform temperature profiles, and resonant wavelength shifts in micro-ring resonators. [Reproduced from: Y. Ye et al., "System-Level Modeling and Analysis of Thermal Effects in Optical Networks-on-Chip", IEEE Transactions on Very Large Scale Integration (VLSI) Systems, Vol. 21, No. 2, pp. 292-305, 2013, DOI: 10.1109/TVLSI.2012.2185524. © 2013 IEEE]](figures/ye_fig01_onoc_thermal_drift.png)

---

## 10.5 Wireless Networks-on-Chip (WNoC): Radio Inside the CPU

![Figure 10.4: Wireless Network-on-Chip (WNoC) system architecture showing the integrated RF transceiver front-end, planar antenna, and propagation channel through the lossy silicon stack. [Reproduced from: M. Shahmoradi et al., "Channel-Aware Behavioral Power Modeling of CMOS OOK Transceivers for Wireless Network-on-Chip Systems", IEEE Transactions on Circuits and Systems I: Regular Papers, Vol. 73, No. 4, pp. 1620-1633, 2026, DOI: 10.5281/zenodo.19449802. © 2026 IEEE]](figures/shahmoradi_fig01_wnoc_architecture.png)

Instead of routing physical wires or optical tubes, why not just broadcast radio waves?
A **Wireless Network-on-Chip (WNoC)** puts tiny microscopic radio antennas right on the silicon:
- **Transmitter (TX)**: Turns digital 1s and 0s into radio pulses using **On-Off Keying (OOK)**—1 means radio pulse ON, 0 means radio pulse OFF. Simple, fast, and needs very little power!
- **On-Chip Antennas**: Tiny zigzag or patch metal strips (under $1\text{ mm}$ long) that broadcast high-frequency millimeter waves ($60\text{ GHz}$).
- **Receiver (RX)**: An amplifier and an envelope detector that sense the incoming radio wave and convert it back into digital bits.

![Figure 10.5: Transceiver power consumption versus carrier frequency and received power under stringent (7 dB) and relaxed (15 dB) noise figures, highlighting optimal operating bands across 28, 60, 140, and 245 GHz. [Reproduced from: M. Shahmoradi et al., "Channel-Aware Behavioral Power Modeling of CMOS OOK Transceivers for Wireless Network-on-Chip Systems", IEEE Transactions on Circuits and Systems I: Regular Papers, Vol. 73, No. 4, pp. 1620-1633, 2026, DOI: 10.5281/zenodo.19449802. © 2026 IEEE]](figures/shahmoradi_fig11_trx_power_optima.png)

As demonstrated by **M. Shahmoradi et al. (IEEE TCAS-I 2026)** in Figure 10.5, **60 GHz** represents the sweet spot for on-chip wireless: antennas are small enough to fit on a compute tile, yet the radio circuits consume only $15\text{--}25\text{ mW}$.

---

## 10.6 Hardware Implementation: Synthesizable MRR Switch Controller

The synthesizable Verilog module [`code/photonic_mrr_switch.v`](code/photonic_mrr_switch.v) implements a 2x2 optical switching element with closed-loop proportional thermal resonance tracking and pulse-width modulated (PWM) microheater actuation.

```verilog
// Snippet from code/photonic_mrr_switch.v: Closed-Loop Thermal Tuning Loop
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        heater_power_val <= 8'd128; // Default 50% duty cycle
        optical_state    <= 1'b0;
        switch_ready     <= 1'b0;
    end else begin
        if (temp_valid) begin
            // Proportional thermal actuation: keep the tuning fork on pitch!
            if (measured_temp < TARGET_TEMP) begin
                if (heater_power_val < 8'd250)
                    heater_power_val <= heater_power_val + 8'd2; // Too cold: heat up
            end else begin
                if (heater_power_val > 8'd5)
                    heater_power_val <= heater_power_val - 8'd2; // Too hot: cool down
            end

            // Verify thermal lock window (+/- 0.5 deg C)
            if ((measured_temp >= (TARGET_TEMP - LOCK_TOLERANCE)) &&
                (measured_temp <= (TARGET_TEMP + LOCK_TOLERANCE)))
                switch_ready <= 1'b1; // Locked and ready to route photons!
            else
                switch_ready <= 1'b0;
        end

        // Safely route light only when resonator is locked
        if (switch_ready) optical_state <= switch_cmd;
        else              optical_state <= 1'b0;
    end
end
```

---

## 10.7 Quantitative Simulation & Experimental Results

The Python model [`code/onoc_optical_loss_sim.py`](code/onoc_optical_loss_sim.py) evaluates optical insertion loss, laser power, and thermal tuning costs in an $8 \times 8$ mesh ONoC (64 cores, $20\text{ mm} \times 20\text{ mm}$ die).

| Metric | Crossing Switching Elements (CSE) | Parallel Switching Elements (PSE) | Advantage |
| :--- | :---: | :---: | :---: |
| **Waveguide Crossings** | $62$ | **$24$** | **$-61.3\%$ crossings** |
| **Active MRR Count** | $192$ | **$112$** | **$-41.7\%$ MRRs** |
| **Worst-Case Insertion Loss** | $11.38\text{ dB}$ | **$6.38\text{ dB}$** | **$-5.00\text{ dB loss}$** |
| **Laser Optical Power** | $0.27\text{ mW}$ | **$0.09\text{ mW}$** | **$3.0\times\text{ lower power}$** |
| **Laser Wall-Plug Power** | $1.37\text{ mW}$ | **$0.43\text{ mW}$** | Sub-milliwatt source |
| **MRR Thermal Tuning Power** | $5184.0\text{ mW}$ | **$3024.0\text{ mW}$** | **$-2.16\text{ W savings}$** |
| **Total Optical Subsystem Power** | $5185.4\text{ mW}$ | **$3024.4\text{ mW}$** | **$-41.7\%\text{ total power}$** |

Eliminating waveguide crossings inside the switching elements reduces insertion loss by $5.00\text{ dB}$, cutting laser power threefold and saving over $2.1\text{ W}$ in thermal tuning dissipation.

---

## 10.8 Summary: What You Learned

- **Light Moves at Light Speed**: Optical NoCs send photons through microscopic silicon waveguides with zero data-dependent wire charging loss.
- **Micro-Ring Resonators Are Tuning Forks**: They select specific wavelengths of light out of a multi-color beam.
- **Parallel Switching Saves Power**: Using parallel waveguides instead of crossing intersections saves $5\text{ dB}$ of optical loss, cutting laser power threefold.
- **Silicon Resonators Need Heating**: Heat shifts resonance by $0.1\text{ nm/}^\circ\text{C}$, so smart microheaters keep the resonators locked on pitch.
- **Wireless NoC is Walkie-Talkie for Chips**: 60 GHz on-chip radios broadcast messages to all 64 cores simultaneously in a single cycle.

---

## 10.9 Exercises and Review Questions

1. **The Optical Tuning Fork**: A ring resonator has radius $R = 6.0\ \mu\text{m}$ and effective index $n_{\text{eff}} = 2.45$. What resonant mode $m$ matches wavelength $\lambda_0 = 1550\text{ nm}$?
2. **The Laser Flashlight**: If a lightpath suffers $10\text{ dB}$ of loss, what fraction of the light arrives at the photodetector? If the receiver needs $0.01\text{ mW}$, how powerful must the laser be?
3. **The Hot CPU**: A processor heats up by $15^\circ\text{C}$. If the ring resonator drifts by $0.10\text{ nm/}^\circ\text{C}$, how many nanometers did the resonant wavelength move?
4. **Walkie-Talkie vs. Whisper**: Why is an on-chip wireless broadcast faster for cache invalidation than sending 63 separate point-to-point electrical packets through a mesh?
