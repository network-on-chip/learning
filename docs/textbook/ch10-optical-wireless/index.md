# Chapter 10: Optical & Wireless Networks-on-Chip (ONoC / WNoC)

[![Companion Platform](https://img.shields.io/badge/Interactive%20Lab-Photon%20Pilot-0f766e?logo=bookstack&logoColor=white)](https://network-on-chip.github.io/learning/interactive/optical/)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%2010%3A%20Optical%20%26%20Wireless-blue)](../../track10-optical-wireless/)
[![Simulation Model](https://img.shields.io/badge/Python%20Model-onoc__optical__loss__sim.py-blueviolet)](code/onoc_optical_loss_sim.py)
[![Hardware RTL](https://img.shields.io/badge/Verilog%20RTL-photonic__mrr__switch.v-success)](code/photonic_mrr_switch.v)

---

## Chapter Introduction

As multi-core processors scale into hundreds and thousands of compute tiles, the fundamental physical properties of metallic copper conductors present an insurmountable barrier to interconnect performance. In conventional electrical Networks-on-Chip (NoCs), transmitting data across a $20\text{ mm}$ silicon die requires dozens of intermediate router hops. Each hop incurs multi-stage pipelined arbitration, virtual-channel buffering, and capacitive charging of lossy RC metal lines ($P_{\text{dyn}} = \alpha C V^2 f$). Under heavy traffic, long wire RC delays and multi-hop queuing delay dominate execution time, while interconnect dynamic and leakage power consume up to $30\text{--}40\%$ of the chip's total power budget.

To transcend these fundamental copper constraints, computer architects have turned to **non-traditional interconnect paradigms**: **Optical Networks-on-Chip (ONoCs)** and **Wireless Networks-on-Chip (WNoCs)**. 

Silicon nanophotonics replaces electrons moving through resistive copper with photons traveling at the speed of light through microscopic silicon waveguides ($n_{\text{Si}} \approx 3.48$) embedded in low-index silicon dioxide cladding ($n_{\text{ox}} \approx 1.45$). By exploiting **Dense Wavelength Division Multiplexing (DWDM)** and sub-micron **Micro-Ring Resonators (MRRs)**, a single optical waveguide can transport dozens of independent multi-gigabit data streams simultaneously with negligible data-dependent transmission power and sub-nanosecond time-of-flight. Concurrently, **Wireless Networks-on-Chip (WNoCs)** integrate on-chip millimeter-wave (mmWave) transceivers and microscopic planar antennas directly onto the silicon die. By broadcasting radio pulses at $60\text{ GHz}$ through the chip substrate, WNoCs deliver true single-cycle, zero-hop global communication, ideal for high-fanout cache invalidations, barrier synchronizations, and collective broadcast routines.

```
+---------------------------------------------------------------------------------------+
|                              CHAPTER 10 CONCEPTUAL LANDSCAPE                          |
+---------------------------------------------------------------------------------------+
|  Electrical NoC Limits     Silicon Nanophotonics (ONoC)      Wireless NoC (WNoC)      |
|  - Elmore RC delay         - Total Internal Reflection       - 60 GHz mmWave / sub-THz|
|  - Multi-hop store-forward - Micro-Ring Resonator (MRR)      - On-Off Keying (OOK)    |
|  - Dynamic CV^2 f losses   - Dense WDM (Multi-Lambda)        - Single-cycle broadcast |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                           PHYSICAL & ARCHITECTURAL TRADEOFFS                          |
+---------------------------------------------------------------------------------------+
|  Optical Loss Budget       Thermal Resonance Drift           Switching Topologies     |
|  - Waveguide prop & bends  - Thermo-optic: 0.10 nm/°C        - CSE: Crossing penalty  |
|  - Waveguide crossings     - Closed-loop microheater PWM     - PSE: Parallel routing  |
|  - Exponential laser power - Channel crosstalk suppression   - -5 dB insertion loss   |
+---------------------------------------------------------------------------------------+
```

### Learning Objectives
- **Contrast Physical Interconnect Paradigms**: Differentiate electrical, optical, and wireless interconnects in terms of propagation velocity, distance-dependent latency, and dynamic vs. static power scaling.
- **Deconstruct Silicon Nanophotonics**: Formulate total internal reflection in high-index-contrast silicon strip waveguides and derive the resonant condition of Micro-Ring Resonators ($m \lambda_{\text{res}} = 2 \pi R n_{\text{eff}}$) for Dense Wavelength Division Multiplexing (DWDM).
- **Evaluate Optical Switch Architectures**: Compare Crossing Switching Elements (CSEs) and Parallel Switching Elements (PSEs) in terms of waveguide intersection count, active ring complexity, and cumulative insertion loss.
- **Formulate End-to-End Optical Power Budgets**: Quantify optical loss components (propagation, bend, crossing, through, and drop penalties) and size continuous laser source optical and wall-plug power requirements ($P_{\text{laser}} \propto 10^{L_{\text{max}} / 10}$).
- **Model Thermo-Optic Drift & Closed-Loop Tuning**: Analyze thermal shifts in silicon microrings ($0.10\text{ nm/}^\circ\text{C}$), evaluate thermal crosstalk against DWDM channel spacing, and synthesize closed-loop proportional microheater tracking logic in hardware.
- **Analyze Wireless On-Chip Radios**: Evaluate $60\text{ GHz}$ CMOS On-Off Keying (OOK) transceivers, on-chip planar patch antennas, and silicon substrate attenuation for single-cycle broadcast synchronization.

### Chapter Roadmap & Interactive Modules
- **Section 10.1**: The Non-Traditional Interconnect Paradigm (garden hose vs. laser pointer vs. walkie-talkie).
- **Section 10.2**: Silicon Nanophotonics: Guiding Light Inside a Microchip (waveguides, MRRs, CSE vs. PSE switches).
- **Section 10.3**: Optical Loss Modeling & Laser Power (loss budget formulation, laser sizing exponential curves).
- **Section 10.4**: Thermal Drift: What Happens When the Chip Gets Hot? (thermo-optic effect, active microheaters).
- **Section 10.5**: Wireless Networks-on-Chip (WNoC): Radio Inside the CPU (OOK transceivers, $60\text{ GHz}$ optima).
- **Section 10.6**: Hardware Implementation: Synthesizable MRR Switch Controller (Verilog RTL closed-loop tuner).
- **Section 10.7**: Quantitative Simulation & Experimental Results (CSE vs. PSE comparative benchmarks).
- **Section 10.8**: Interactive Lab & Hands-on Challenges.
- **Section 10.9**: Summary & Cross-Disciplinary Synergies.
- **Section 10.10**: Checkpoint Assessment & Certification Questions.
- **Interactive Companion**: Explore the [`Photon Pilot Interactive Lab`](https://network-on-chip.github.io/learning/interactive/optical/) to tune laser power, route optical lightpaths, and lock micro-ring resonators dynamically.

---

## 10.1 The Non-Traditional Interconnect Paradigm

> [!NOTE] 💡 Architectural Intuition: Garden Hoses vs. Laser Pointers
> Why are computer chips replacing copper wires with light beams and wireless radio waves?
> - **The Copper Wire (The Garden Hose)**: Imagine a very long, empty garden hose. To get water out of the nozzle at the far end, you first have to turn on the faucet and fill up the **entire volume of the hose** with water under high pressure. In electronics, every copper wire has electrical capacitance ($C$); before a 1 can reach the receiver, the transmitter has to spend electrical energy charging up the entire wire! This creates delay and generates lots of waste heat ($P = \alpha C V^2 f$) [[Vantrease2008](#ref-vantrease2008), [Kurian2010](#ref-kurian2010)].
> - **The Optical Waveguide (The Laser Pointer)**: Now imagine shining a laser pointer across the room. The moment you press the button, photons travel across the room at the **speed of light**! Even better: it doesn't take more battery power whether you flash the laser slowly or blink it 10 billion times every second [[Little1997](#ref-little1997), [Kao2026](#ref-kao2026)].
> - **The Wireless Link (The Walkie-Talkie)**: Passing messages through a 64-core grid of routers is like whispering a secret down 14 rows of desks in a classroom. A wireless link is like speaking into a **walkie-talkie**: every core in the room hears the broadcast in a single clock cycle [[Deb2012](#ref-deb2012), [Abadal2018](#ref-abadal2018), [Shahmoradi2026](#ref-shahmoradi2026)]!

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

Silicon nanophotonics allows engineers to build microscopic "fiber optic cables" directly on a computer chip! Standard silicon has a high refractive index ($n_{\text{Si}} \approx 3.48$), while glass insulation ($\text{SiO}_2$) has a lower index ($n_{\text{ox}} \approx 1.45$). Just like light stays trapped inside a swimming pool when viewed from an angle (**Total Internal Reflection**), light stays trapped inside a tiny silicon wire called an **optical waveguide** ($450\text{ nm}$ wide) [[Little1997](#ref-little1997), [Kao2026](#ref-kao2026)].

### 10.2.1 Micro-Ring Resonators: The Optical Tuning Fork

> [!TIP] 💡 Architectural Intuition: The Musical Tuning Fork
> If you have a musical tuning fork tuned to middle C ($261.6\text{ Hz}$), what happens when a singer sings middle C across the room? The tuning fork catches the sound wave and begins to vibrate! But if the singer sings a D or an E, the tuning fork ignores it completely.
>
> An **optical Micro-Ring Resonator (MRR)** (Little et al., IEEE PTL 1997 [[Little1997](#ref-little1997)]) is a microscopic silicon ring that acts as an **optical tuning fork**. It has a specific cavity size ($R \approx 5\text{--}10\ \mu\text{m}$). When light of its exact resonant color (wavelength $\lambda_{\text{res}}$) arrives, it gets pulled into the ring and sent to the drop port. All other colors pass straight through!
>
> This lets us do **Wavelength Division Multiplexing (WDM)**: we can send 16 different colors of light through a single microscopic waveguide at the same time, multiplying bandwidth by $16\times$!

The resonant condition is governed by [[Little1997](#ref-little1997), [Ye2013](#ref-ye2013)]:

$$m \lambda_{\text{res}} = 2 \pi R \cdot n_{\text{eff}}$$

where $m$ is an integer (the mode number), $R$ is the ring radius, and $n_{\text{eff}}$ is the effective refractive index.

### 10.2.2 Switching Elements: Crossing (CSE) vs. Parallel (PSE)

![Figure 10.1: MRR switching structures: (a) 90-degree Crossing Switching Element (CSE), (b) 270-degree CSE, and (c) Parallel Switching Element (PSE). [Reproduced from: W.-Y. Kao et al., "Provably Good Physically Aware WRONoC Design for Customized and Fault-Tolerant Topologies With Parallel Switching Elements and Sequence-Based Models", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 45, No. 3, pp. 650-663, 2026, DOI: 10.1145/3658617.3697557. © 2026 IEEE]](figures/kao_fig01_mrr_structures.png)

How do we route photons dynamically between intersecting optical channels? As characterized by W.-Y. Kao et al. [[Kao2026](#ref-kao2026), [Kao2026WR](#ref-kao2026wr)] in Figure 10.1:

- **Crossing Switching Elements (CSEs)**:
    - Positions the micro-ring resonator at the intersection of two orthogonal waveguides ($90^\circ$ or $270^\circ$ crossing).
    - Every physical waveguide intersection introduces radiation scattering into the surrounding cladding, imposing $0.10\text{ to }0.20\text{ dB}$ of optical insertion loss per crossing.
    - In a standard $8 \times 8$ optical mesh, end-to-end paths may traverse over $60$ waveguide crossings, attenuating optical signal power by up to $10\text{ to }12\text{ dB}$ and causing unacceptable inter-channel crosstalk.
- **Parallel Switching Elements (PSEs)**:
    - Couples the ring resonator tangentially between two parallel, non-intersecting waveguides [[Kao2026](#ref-kao2026), [Kao2026WR](#ref-kao2026wr)].
    - When non-resonant, light passes straight through along the input waveguide with negligible loss ($<0.005\text{ dB}$).
    - When electrically or thermally tuned into resonance, evanescent wave coupling transfers photons smoothly across the narrow coupling gap ($100\text{ to }200\text{ nm}$) into the parallel drop waveguide without encountering orthogonal crossings.
    - Slashes total optical waveguide intersections by $>60\%$, preserving laser optical power and reducing bit error rate (BER) noise floors.

![Figure 10.2: Add-Drop Filter (ADF) structures with default paths (straight through) and non-default paths (switched via MRR coupling). [Reproduced from: W.-Y. Kao et al., "Provably Good Physically Aware WRONoC Design for Customized and Fault-Tolerant Topologies With Parallel Switching Elements and Sequence-Based Models", IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, Vol. 45, No. 3, pp. 650-663, 2026, DOI: 10.1145/3658617.3697557. © 2026 IEEE]](figures/kao_fig02_adf_structures.png)

---

## 10.3 Optical Loss Modeling & Laser Power

### 10.3.1 Where Does the Light Go? (Optical Loss Budget)
As light travels from the off-chip or on-chip laser source to the destination receiver photodetector, optical power degrades incrementally across every passive and active photonic component [[Vantrease2008](#ref-vantrease2008), [Ye2013](#ref-ye2013), [Kao2026](#ref-kao2026)]:

$$L_{\text{path}}(\text{dB}) = L_{\text{prop}} + L_{\text{bend}} + L_{\text{cross}} + L_{\text{thru}} + L_{\text{drop}} + L_{\text{mod}}$$

- **Waveguide Propagation Loss ($L_{\text{prop}}$)**:
    - Scattering caused by sidewall line-edge roughness during silicon dry etching:
    $$L_{\text{prop}} = \alpha_{\text{wg}} \cdot d_{\text{path}} \approx (0.25\text{ dB/cm}) \times d_{\text{path}}$$
- **Waveguide Bending Loss ($L_{\text{bend}}$)**:
    - Mode radiation leakage whenever waveguides curve to change direction:
    $$L_{\text{bend}} = N_{\text{bend}} \times 0.005\text{ dB/bend} \quad (\text{for bend radius } R \ge 5\ \mu\text{m})$$
- **Waveguide Crossing Loss ($L_{\text{cross}}$)**:
    - Diffraction loss and forward scatter occurring at orthogonal physical intersections:
    $$L_{\text{cross}} = N_{\text{cross}} \times 0.12\text{ dB/crossing}$$
- **Micro-Ring Through-Port Loss ($L_{\text{thru}}$)**:
    - Insertion loss when an optical carrier bypasses an inactive, out-of-resonance MRR:
    $$L_{\text{thru}} = N_{\text{thru\_mrr}} \times 0.01\text{ dB/MRR}$$
- **Micro-Ring Drop-Port Loss ($L_{\text{drop}}$)**:
    - Coupling insertion loss when light is actively extracted into a resonant MRR drop port:
    $$L_{\text{drop}} \approx 0.50\text{ to }0.80\text{ dB}$$
- **Modulator Insertion Loss ($L_{\text{mod}}$)**:
    - Electro-optic absorption loss in the transmitter Mach-Zehnder or electro-absorption modulator ($1.5\text{ to }3.0\text{ dB}$).

### 10.3.2 Sizing the Laser Source
- **Photodetector Sensitivity Threshold ($P_{\text{rx\_sens}}$)**:
    - High-speed Germanium photodetectors require a minimum optical power level (typically $-20\text{ dBm} = 10\ \mu\text{W}$) to distinguish digital 1s from 0s at a target bit error rate of $\text{BER} \le 10^{-12}$.
- **Exponential Laser Sizing Penalty**:
    - The required laser output power $P_{\text{laser}}$ scales exponentially with total path insertion loss in decibels [[Kurian2010](#ref-kurian2010), [Vantrease2008](#ref-vantrease2008)]:
    $$P_{\text{laser}}(\text{dBm}) = P_{\text{rx\_sens}}(\text{dBm}) + L_{\text{path}}(\text{dB}) + M_{\text{margin}}$$
    - In linear milliwatts ($P_{\text{laser}} \propto 10^{L_{\text{path}} / 10}$), every $3\text{ dB}$ reduction in insertion loss cuts required optical laser output power by **$50\%$**.
- **Wall-Plug Electrical Efficiency**:
    - Continuous-wave (CW) distributed-feedback (DFB) laser diodes exhibit wall-plug electrical-to-optical conversion efficiencies of only $15\text{--}25\%$ [[Kurian2010](#ref-kurian2010)].
    - Consequently, saving $5\text{ dB}$ of optical loss translates to saving watts of continuous electrical power and heat dissipation inside the package.

---

## 10.4 Thermal Drift: What Happens When the Chip Gets Hot?

> [!WARNING] 💡 Architectural Intuition: The Out-of-Tune Guitar
> If you leave a guitar in the hot sun, the strings expand, and the guitar goes completely out of tune!
> 
> Silicon does the exact same thing! Silicon has a positive **thermo-optic coefficient**: as temperature rises, silicon's refractive index changes, causing the micro-ring resonator to expand optically by **$0.10\text{ nm}$ for every $1^\circ\text{C}$ of heat** [[Ye2013](#ref-ye2013), [Wang2021ACO](#ref-wang2021aco)]!
>
> Since our color channels are only $0.8\text{ nm}$ apart, if you play a demanding 3D game and your CPU heats up by just $8^\circ\text{C}$, the optical ring shifts completely into the next channel, causing garbled data or complete silence!
>
> To solve this, every optical ring has a tiny **electric microheater**. A smart temperature controller monitors the ring and keeps it at a steady, warm baseline temperature (e.g., $55^\circ\text{C}$), keeping the "tuning fork" perfectly in tune [[Ye2013](#ref-ye2013), [Liu2025Energy](#ref-liu2025energy)].

![Figure 10.3: System-level thermal simulation of an Optical NoC demonstrating core active power dissipation, non-uniform temperature profiles, and resonant wavelength shifts in micro-ring resonators. [Reproduced from: Y. Ye et al., "System-Level Modeling and Analysis of Thermal Effects in Optical Networks-on-Chip", IEEE Transactions on Very Large Scale Integration (VLSI) Systems, Vol. 21, No. 2, pp. 292-305, 2013, DOI: 10.1109/TVLSI.2012.2185524. © 2013 IEEE]](figures/ye_fig01_onoc_thermal_drift.png)

---

## 10.5 Wireless Networks-on-Chip (WNoC): Radio Inside the CPU

![Figure 10.4: Wireless Network-on-Chip (WNoC) system architecture showing the integrated RF transceiver front-end, planar antenna, and propagation channel through the lossy silicon stack. [Reproduced from: M. Shahmoradi et al., "Channel-Aware Behavioral Power Modeling of CMOS OOK Transceivers for Wireless Network-on-Chip Systems", IEEE Transactions on Circuits and Systems I: Regular Papers, Vol. 73, No. 4, pp. 1620-1633, 2026, DOI: 10.5281/zenodo.19449802. © 2026 IEEE]](figures/shahmoradi_fig01_wnoc_architecture.png)

Instead of routing physical metallic traces or etching optical waveguides across the entire die, Wireless Networks-on-Chip (WNoCs) (Deb et al., IEEE Trans. Comput. 2012 [[Deb2012](#ref-deb2012)], Abadal et al. [[Abadal2018](#ref-abadal2018)]) integrate microscopic radio transceivers directly into compute tiles to communicate through unguided electromagnetic wave propagation:

- **Transmitter (TX) RF Front-End**:
    - Modulates outgoing digital flits onto a high-frequency carrier wave using **Non-Coherent On-Off Keying (OOK)** [[Shahmoradi2026](#ref-shahmoradi2026)].
    - Logic '1' gates a local voltage-controlled oscillator (VCO) to emit an RF pulse; logic '0' disables the oscillator completely, yielding zero carrier power dissipation during idle periods.
    - Directly drives an integrated micro-power power amplifier (PA) without complex I/Q mixers or digital-to-analog converters.
- **On-Chip Planar Antennas**:
    - Fabricated using standard top-level backend metal layers (e.g., M8/M9 copper/aluminum) configured as planar meander dipoles, zigzags, or microstrip patches [[Deb2012](#ref-deb2012)].
    - The physical antenna length scales inversely with carrier frequency ($L \approx \lambda_g / 4 = c / (4 f \sqrt{\epsilon_r})$); at $60\text{ GHz}$ inside silicon dioxide ($\epsilon_r \approx 3.9$), a quarter-wave antenna measures only $\approx 630\ \mu\text{m}$—compact enough to embed within a core tile without displacing logic gates.
    - High substrate doping in bulk CMOS can cause substrate eddy current dissipation, requiring high-resistivity silicon regions or ground shielding planes to preserve radiation efficiency [[Deb2012](#ref-deb2012), [Shahmoradi2026](#ref-shahmoradi2026)].
- **Receiver (RX) Front-End & Demodulation**:
    - Captures the attenuated millimeter-wave signal using a wideband Low-Noise Amplifier (LNA) to establish receiver sensitivity.
    - Routes the amplified RF envelope through an analog diode/MOSFET squarer and low-pass filter (envelope detector) to reconstruct the baseband digital pulse.
    - A regenerative dynamic comparator (slicer) converts the analog pulse back into standard CMOS digital voltage rails with sub-cycle delay [[Shahmoradi2026](#ref-shahmoradi2026)].
- **Frequency Band Optimization ($60\text{ GHz}$ Sweet Spot)**:
    - As demonstrated by M. Shahmoradi et al. [[Shahmoradi2026](#ref-shahmoradi2026)] in Figure 10.5, selecting carrier frequency requires balancing antenna footprint against transceiver circuit power:
    - Lower frequencies ($28\text{ GHz}$) require millimeter-scale antennas that exceed standard tile pitch.
    - Sub-terahertz frequencies ($140\text{ to }245\text{ GHz}$) shrink antennas dramatically but demand exorbitant LNA/VCO bias currents due to CMOS transistor transit frequency ($f_T$) roll-off.
    - The unlicensed $60\text{ GHz}$ industrial/scientific band offers the optimal PPA trade-off: compact $\approx 0.6\text{ mm}$ antennas with high-efficiency $15\text{--}25\text{ mW}$ CMOS transceivers capable of multi-gigabit throughput [[Shahmoradi2026](#ref-shahmoradi2026), [Taghvaee2022](#ref-taghvaee2022)].

![Figure 10.5: Transceiver power consumption versus carrier frequency and received power under stringent (7 dB) and relaxed (15 dB) noise figures, highlighting optimal operating bands across 28, 60, 140, and 245 GHz. [Reproduced from: M. Shahmoradi et al., "Channel-Aware Behavioral Power Modeling of CMOS OOK Transceivers for Wireless Network-on-Chip Systems", IEEE Transactions on Circuits and Systems I: Regular Papers, Vol. 73, No. 4, pp. 1620-1633, 2026, DOI: 10.5281/zenodo.19449802. © 2026 IEEE]](figures/shahmoradi_fig11_trx_power_optima.png)

---

## 10.6 Hardware Implementation: Synthesizable MRR Switch Controller

The synthesizable Verilog module [`code/photonic_mrr_switch.v`](code/photonic_mrr_switch.v) implements a 2x2 optical switching element with closed-loop proportional thermal resonance tracking and pulse-width modulated (PWM) microheater actuation [[Ye2013](#ref-ye2013), [Kao2026](#ref-kao2026), [Wang2021ACO](#ref-wang2021aco)].

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

The Python model [`code/onoc_optical_loss_sim.py`](code/onoc_optical_loss_sim.py) evaluates optical insertion loss, laser power, and thermal tuning costs in an $8 \times 8$ mesh ONoC (64 cores, $20\text{ mm} \times 20\text{ mm}$ die) [[Ye2013](#ref-ye2013), [Kao2026](#ref-kao2026), [Kao2026WR](#ref-kao2026wr), [Liu2025Energy](#ref-liu2025energy)].

| Metric | Crossing Switching Elements (CSE) | Parallel Switching Elements (PSE) | Advantage |
| :--- | :---: | :---: | :---: |
| **Waveguide Crossings** | $62$ | **$24$** | **$-61.3\%$ crossings** |
| **Active MRR Count** | $192$ | **$112$** | **$-41.7\%$ MRRs** |
| **Worst-Case Insertion Loss** | $11.38\text{ dB}$ | **$6.38\text{ dB}$** | **$-5.00\text{ dB loss}$** |
| **Laser Optical Power** | $0.27\text{ mW}$ | **$0.09\text{ mW}$** | **$3.0\times\text{ lower power}$** |
| **Laser Wall-Plug Power** | $1.37\text{ mW}$ | **$0.43\text{ mW}$** | Sub-milliwatt source |
| **MRR Thermal Tuning Power** | $5184.0\text{ mW}$ | **$3024.0\text{ mW}$** | **$-2.16\text{ W savings}$** |
| **Total Optical Subsystem Power** | $5185.4\text{ mW}$ | **$3024.4\text{ mW}$** | **$-41.7\%\text{ total power}$** |

Eliminating waveguide crossings inside the switching elements reduces insertion loss by $5.00\text{ dB}$, cutting laser power threefold and saving over $2.1\text{ W}$ in thermal tuning dissipation [[Kao2026](#ref-kao2026), [Ye2013](#ref-ye2013)].

---

## 10.8 Interactive Lab & Hands-on Challenges

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.35), rgba(15, 23, 42, 0.65)); border: 1px solid rgba(59, 130, 246, 0.5); border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #93c5fd; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;">
      <span>💡 Dedicated Interactive Labs: Photon Pilot &amp; Wireless Wave</span>
    </div>
    <div style="font-size: 0.92rem; color: #e2e8f0; margin-top: 6px; max-width: 800px; line-height: 1.5;">
      Tune micro-ring resonator (MRR) thermal locking loops, balance WDM optical waveguide insertion loss, and broadcast single-cycle coherence barriers over 60/140 GHz on-chip wireless transceivers.
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="../../interactive/optical/" style="display: inline-flex; align-items: center; gap: 6px; background: #db2777; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Launch Photon Pilot →</span>
    </a>
    <a href="../../interactive/wireless/" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Launch Wireless Wave →</span>
    </a>
  </div>
</div>

Complete the following three hands-on laboratory missions in **[Photon Pilot](../../interactive/optical.md)** and **[Wireless Wave](../../interactive/wireless.md)**:

### Challenge Mission 10.1: Micro-Ring Resonator (MRR) Thermo-Optic Drift & Thermal Locking
- **Objective:** Measure the resonance redshift induced by on-chip thermal gradients and stabilize the optical link using integrated microheaters [[Ye2013](#ref-ye2013), [Wang2021ACO](#ref-wang2021aco)].
- **Setup & Procedure:**
  1. In **Photon Pilot**, route an optical carrier wavelength ($\lambda = 1550.0\text{ nm}$) through an active MRR filter.
  2. Increase local silicon temperature by $\Delta T = 15^\circ\text{C}$ to model a neighboring CPU hotspot.
  3. Observe optical signal attenuation as the ring detunes from the laser wavelength. Activate the **Microheater Thermal Lock** loop.
- **Architectural Observation:** Silicon's large thermo-optic coefficient ($dn/dT \approx 1.86 \times 10^{-4}\text{ K}^{-1}$) shifts the resonant wavelength by $d\lambda / dT \approx 0.10\text{ nm/}^\circ\text{C}$. A $15^\circ\text{C}$ temperature surge shifts resonance by $1.5\text{ nm}$, completely extinguishing the optical channel ($>25\text{ dB}$ extinction loss). The integrated microheater adds localized thermal bias to restore resonance alignment, balancing signal integrity against multi-watt electrical tuning power.
- **Verification Formula:** $\Delta\lambda_{\text{res}} = \frac{\lambda_{\text{res}}}{n_g} \left(\frac{\partial n_{\text{eff}}}{\partial T}\right) \Delta T \approx 0.10\text{ nm/}^\circ\text{C} \times \Delta T$.

### Challenge Mission 10.2: Optical Insertion Loss & Laser Power Budgets (CSE vs. PSE)
- **Objective:** Compare cumulative insertion loss and required continuous-wave (CW) laser optical power between Crossing Switching Elements (CSEs) and Parallel Switching Elements (PSEs) [[Kao2026](#ref-kao2026), [Vantrease2008](#ref-vantrease2008)].
- **Setup & Procedure:**
  1. In **Photon Pilot**, configure an $8 \times 8$ optical mesh utilizing traditional orthogonal CSE switching cells. Trace the worst-case optical lightpath.
  2. Record cumulative crossing losses ($0.12\text{ dB}$ per crossing) and total optical path loss ($>11.3\text{ dB}$).
  3. Switch switching cell architecture to **Parallel Switching Elements (PSE)**.
- **Architectural Observation:** Traditional CSEs force light through internal orthogonal waveguide crossings, accumulating over 60 crossings along worst-case lightpaths. The PSE architecture couples light between parallel waveguides, eliminating $61\%$ of waveguide crossings and slashing worst-case path loss by $5.00\text{ dB}$. This $5\text{ dB}$ reduction cuts required laser wall-plug power by $3.0\times$ (from $1.37\text{ mW}$ to $0.43\text{ mW}$), preventing optical power budgets from overwhelming the chip.

### Challenge Mission 10.3: Hybrid Wireless Sub-THz Broadcast for Collective Synchronization
- **Objective:** In **Wireless Wave**, bypass multi-hop wired routing hierarchies by broadcasting cache invalidations across 60 GHz / 140 GHz on-chip wireless antennas [[Deb2012](#ref-deb2012), [Abadal2018](#ref-abadal2018), [Taghvaee2022](#ref-taghvaee2022)].
- **Setup & Procedure:**
  1. Launch **Wireless Wave: mmWave & THz Swarm NoC**.
  2. Trigger a 64-core global barrier synchronization over conventional wired 2D mesh links. Record synchronization latency ($>45$ cycles).
  3. Activate the **Hybrid mmWave RF Transceiver Array** and broadcast the barrier token.
- **Architectural Observation:** In large tiled multi-core systems, global collectives (all-reduce, broadcast, barrier synchronization) incur severe latency when routed multi-hop through wire channels ($O(\sqrt{N})$ hop latency and router serialization). Hybrid wireless transceivers radiate electromagnetic waves through the silicon/dielectric stack at near speed-of-light, completing chip-wide broadcast synchronization in a single clock cycle ($1\text{ cycle}$ vs $45\text{ cycles}$)!
- **Hardware RTL & Python Reference:** Run `python code/onoc_optical_loss_sim.py` and inspect `code/photonic_mrr_switch.v` for synthesizable photonic switch control RTL.

---

## 10.9 Summary & Cross-Disciplinary Synergies

- **Speed-of-Light Optical Transport**:
    - Photons traversing high-index silicon waveguides eliminate RC wire delay bottlenecks and distance-dependent dynamic charging dissipation [[Vantrease2008](#ref-vantrease2008), [Kurian2010](#ref-kurian2010)].
    - Dense Wavelength Division Multiplexing (DWDM) enables dozens of parallel multi-gigabit bitstreams across a single physical waveguide.
- **Micro-Ring Resonators as Spectral Filters**:
    - Sub-micron silicon rings operate as optical tuning forks, coupling specific resonant wavelengths into drop ports while passing out-of-band channels with near-zero attenuation [[Little1997](#ref-little1997), [Kao2026](#ref-kao2026)].
- **Physical Switching Topologies**:
    - Replacing orthogonal Crossing Switching Elements (CSEs) with Parallel Switching Elements (PSEs) eliminates $61\%$ of waveguide crossings, lowering worst-case insertion loss by $5.0\text{ dB}$ and slashing required laser optical power by $3\times$ [[Kao2026](#ref-kao2026), [Kao2026WR](#ref-kao2026wr)].
- **Thermo-Optic Tuning Imperatives**:
    - Silicon's positive thermo-optic coefficient shifts resonance by $0.10\text{ nm/}^\circ\text{C}$; hardware microheater control loops maintain thermal lock within $\pm 0.5^\circ\text{C}$ to suppress channel crosstalk [[Ye2013](#ref-ye2013), [Wang2021ACO](#ref-wang2021aco)].
- **Wireless Broadcast for Collective Synchronization**:
    - On-chip $60\text{ GHz}$ mmWave radios deliver single-cycle global broadcast, bypassing multi-hop routing hierarchies for cache coherence invalidations and barrier synchronization [[Deb2012](#ref-deb2012), [Abadal2018](#ref-abadal2018), [Taghvaee2022](#ref-taghvaee2022)].

---

## 10.10 Checkpoint Assessment

Test your mastery of Chapter 10 concepts against the official certification questions (mirroring the 3-Tier Exam Engine in [`quiz.md`](../../quiz.md)):

#### Question 10.1 (Tier 1: Fundamental)
*Which of the following physical and architectural advantages allow Optical Networks-on-Chip (ONoC) to outperform electrical copper interconnects over long on-chip distances [[Vantrease2008](#ref-vantrease2008), [Kurian2010](#ref-kurian2010)]? (Select all that apply)*

- **A)** Photons propagating through passive silicon waveguides experience no data-dependent capacitive charging loss (P_dyn = alpha * C * V^2 * f); optical transmission energy is distance-independent once light is injected.
- **B)** Wavelength Division Multiplexing (WDM) allows multiple independent optical signals (e.g. 16–64 wavelengths) to traverse the same physical waveguide simultaneously without electrical crosstalk.
- **C)** Optical signals travel at the speed of light in silicon (c / n_si ~ 8.5 x 10^7 m/s, or ~11.8 ps/mm), avoiding RC dispersion delays.
- **D)** Optical silicon waveguides eliminate the need for laser power sources.

??? success "Reveal Answer & Full Solution"
    **Correct Answer: Option A, B, C**

    **1. Step-by-Step Architectural & Mathematical Derivation:**
    Electrical interconnects scale poorly over long distances (L > 5–10 mm) because charging line capacitance dissipates dynamic power P = alpha * C_wire * V^2 * f and Elmore delay scales quadratically with length. Silicon photonics replaces long metal lines with sub-micron silicon waveguides: (1) Distance-Independent Dynamic Energy: Once an optical signal is modulated into a waveguide, photons traverse passive silicon without charging or discharging gate/wire capacitances. Waveguide propagation loss is low (~0.5–1.5 dB/cm), making transmission energy virtually independent of link distance. (2) Wavelength Division Multiplexing (WDM): By modulating data across multiple distinct optical wavelengths (lambda_1, lambda_2, ..., lambda_M) separated by 50–100 GHz channel spacing, a single physical waveguide carries dozens of concurrent high-speed bitstreams, achieving multi-Tbps aggregate bandwidth density without adding physical wires. (3) Latency: Light propagates at the group velocity v_g = c / n_g (approx 85,000 km/s in Si with n_g ~ 3.5), yielding ~11.8 ps/mm of transit time without intermediate repeater pipeline delays. However, optical systems require an external or integrated laser power source and micro-ring resonator tuning.

    **2. Option-by-Option Breakdown & Distractor Analysis:**
    - **Option A (Correct):** True. Photons do not charge capacitive wire plates during transit, decoupling transmission energy from link distance.
    - **Option B (Correct):** True. WDM multiplexes dozens of optical carriers into a single waveguide, delivering massive bandwidth density.
    - **Option C (Correct):** True. Optical transit operates at group velocity (~11.8 ps/mm) with zero RC charging delay.
    - **Option D (Incorrect Distractor):** False. Silicon is an indirect bandgap semiconductor and cannot generate light passively; an external or hybrid-integrated laser is strictly required.

    **3. Silicon Architect's Takeaway:**
    Silicon photonics eliminates capacitive RC wire losses and multiplies channel bandwidth via WDM, delivering distance-independent energy for long-range communication.

    *(Reference: D. Vantrease et al., "Corona," ISCA 2008 [[Vantrease2008](#ref-vantrease2008)]; G. Kurian et al., "ATAC," PACT 2010 [[Kurian2010](#ref-kurian2010)]; C. Kao et al., "Low-Loss Switching Elements for WDM Optical Networks-on-Chip," IEEE TCAD, 2026 [[Kao2026](#ref-kao2026)]).*

#### Question 10.2 (Tier 2: Core Engineering)
*Why do Parallel Switching Elements (PSEs) achieve significantly lower optical insertion loss and laser power dissipation than Crossing Switching Elements (CSEs) in ONoC architectures [[Kao2026](#ref-kao2026), [Kao2026WR](#ref-kao2026wr)]?*

- **A)** PSE structures place the micro-ring resonator between two parallel waveguides, eliminating internal orthogonal waveguide crossings that introduce scattering loss (0.10–0.15 dB per crossing) and crosstalk noise.
- **B)** PSE structures eliminate the need for micro-ring resonators altogether.
- **C)** CSE structures cannot transmit infrared light.
- **D)** PSE structures operate exclusively at liquid helium temperatures (-269°C).

??? success "Reveal Answer & Full Solution"
    **Correct Answer: Option A**

    **1. Step-by-Step Architectural & Mathematical Derivation:**
    In Optical Networks-on-Chip (ONoC), router switching cells redirect optical signals between input and output waveguides using Micro-Ring Resonators (MRRs): (1) Crossing Switching Element (CSE): Traditional CSE designs arrange waveguides in an orthogonal cross (+) with a ring in the corner. In both the through state and drop state, light must traverse waveguide crossings. Each physical waveguide crossing introduces ~0.10–0.20 dB of scattering loss and -30 dB to -40 dB of optical crosstalk into adjacent channels. In an 8x8 optical mesh, an optical path can accumulate 20–30 crossings, losing 3–5 dB of optical power. (2) Parallel Switching Element (PSE): Kao et al. [[Kao2026](#ref-kao2026), [Kao2026WR](#ref-kao2026wr)] proved that arranging waveguides in parallel (=) with the ring coupled between them completely eliminates internal crossings within the switching element. When off-resonance, light passes straight through with <0.01 dB loss; when on-resonance, light couples across into the parallel guide without crossing physical silicon boundaries. In an 8x8 mesh, PSE architectures slash total optical path loss by 4.8 dB, which reduces required continuous-wave (CW) laser power by over 3x!

    **2. Option-by-Option Breakdown & Distractor Analysis:**
    - **Option A (Correct):** Coupling between parallel waveguides eliminates internal orthogonal waveguide crossings, avoiding scattering loss and crosstalk.
    - **Option B (Incorrect Distractor):** PSE structures use micro-ring resonators for wavelength-selective coupling.
    - **Option C (Incorrect Distractor):** Both PSE and CSE operate at standard telecommunications infrared wavelengths (1310 nm and 1550 nm).
    - **Option D (Incorrect Distractor):** Silicon photonic integrated circuits operate at standard room temperatures (up to 85°C–105°C).

    **3. Silicon Architect's Takeaway:**
    Eliminating waveguide crossings via Parallel Switching Elements (PSE) slashes optical path loss by several dB, cutting laser power requirements threefold.

    *(Reference: W.-Y. Kao et al., "Provably Good Physically Aware WRONoC Design," IEEE TCAD, Vol. 45, No. 3, pp. 650–663, 2026 [[Kao2026](#ref-kao2026), [Kao2026WR](#ref-kao2026wr)]).*

#### Question 10.3 (Tier 3: Silicon Mastery)
*Which of the following physical and thermal factors explain why silicon's thermo-optic coefficient (dn/dT ≈ 1.86 × 10^{-4} K^{-1}) poses a critical challenge for dense WDM Optical Networks-on-Chip [[Ye2013](#ref-ye2013), [Wang2021ACO](#ref-wang2021aco)]? (Select all that apply)*

- **A)** Thermal expansion and refractive index shifts cause Micro-Ring Resonator (MRR) resonant wavelengths to drift by approximately 0.08–0.11 nm/°C.
- **B)** In dense WDM networks with 0.4–0.8 nm channel spacing, a localized temperature shift of just 4°C to 8°C detunes the resonator from its laser wavelength, causing severe optical signal extinction or channel crosstalk.
- **C)** Active thermal stabilization using integrated microheaters consumes 15–25 mW per nanometer of tuning, dissipating multiple watts of static power across hundreds of on-chip resonators.
- **D)** Silicon waveguides melt whenever temperature increases by more than 1°C.

??? success "Reveal Answer & Full Solution"
    **Correct Answer: Option A, B, C**

    **1. Step-by-Step Architectural & Mathematical Derivation:**
    Micro-Ring Resonators (MRRs) filter light based on constructive interference: lambda_res = (2 * pi * r * n_eff) / m, where r is ring radius, n_eff is effective refractive index, and m is the resonance order. Silicon exhibits a strong positive thermo-optic coefficient: dn/dT ~ 1.86 x 10^-4 K^-1. As a result, temperature variations shift the resonant wavelength: d(lambda_res) / dT = (lambda_res / n_g) * (dn_eff / dT) ~ 0.08 to 0.11 nm / °C. In a dense WDM system with 50 GHz to 100 GHz channel spacing (0.4 nm to 0.8 nm between adjacent wavelengths): (1) Localized Hotspots: A 5°C thermal gradient across the chip shifts resonance by ~0.5 nm, completely detuning the MRR from its designated laser wavelength (causing 20–30 dB optical signal attenuation) or misaligning it with an adjacent channel (generating severe inter-channel crosstalk). (2) Thermal Tuning Burden: To maintain resonance locking, integrated titanium or nickel-chromium microheaters must actively heat cooler rings to match the highest chip hotspot temperature. Because thermal tuning consumes 15–25 mW per nm of redshift, stabilizing a 64-channel WDM network across 30°C chip temperature swings can consume over 30 to 45 Watts of electrical heating power—often exceeding the power of the computing cores themselves!

    **2. Option-by-Option Breakdown & Distractor Analysis:**
    - **Option A (Correct):** True. Silicon's thermo-optic coefficient shifts resonance by ~0.1 nm/°C.
    - **Option B (Correct):** True. With dense WDM channel spacing of 0.4–0.8 nm, small 5°C thermal shifts cause complete optical link dropouts.
    - **Option C (Correct):** True. Active microheater stabilization dissipates 15–25 mW/nm, consuming multi-watt power budgets across large optical networks.
    - **Option D (Incorrect Distractor):** False. Silicon melting point is 1414°C; 1°C temperature changes do not melt semiconductor crystals.

    **3. Silicon Architect's Takeaway:**
    Thermo-optic drift (~0.1 nm/°C) can detune dense WDM optical links under slight thermal gradients, requiring multi-watt microheater tuning or athermal resonator designs.

    *(Reference: Y. Ye et al., "System-Level Modeling and Analysis of Thermal Effects in Optical Networks-on-Chip," IEEE TVLSI, 2013 [[Ye2013](#ref-ye2013)]; K. Wang et al., "Ant Colony Optimization-Based Thermal-Aware Adaptive Routing Mechanism for Optical NoCs," IEEE TVLSI, 2021 [[Wang2021ACO](#ref-wang2021aco)]).*

---

### Ant-Colony Optical Routing, MDM Multiplexing, and Reconfigurable Wireless
<a id="recent-frontiers"></a>

Emerging photonic and wireless interconnect research has advanced across multiple physical domains:
- **Ant-Colony Optimization for Thermal-Aware Optical Routing**: Wang et al. [[Wang2021ACO](#ref-wang2021aco)] applied ant-colony optimization (ACO) to dynamically steer optical packets away from thermally drifted micro-ring resonators (MRRs), balancing laser power against heating degradation in ONoCs.
- **Reinforcement Learning for Ring-Augmented Meshes**: Fang et al. [[Fang2026RLRM](#ref-fang2026rlrm)] developed RLRM, an RL-based routing policy that leverages optical bypass rings to avoid congestion in hybrid electro-photonic meshes.
- **Physically-Aware WRONoC Design**: Kao et al. [[Kao2026WR](#ref-kao2026wr)] proved exact layout optimality conditions for Wavelength-Routed Optical NoCs (WRONoCs), eliminating waveguide crossings while satisfying custom bandwidth constraints.
- **Mode-Division Multiplexing (MDM) Reliability**: Su et al. [[Su2026MDM](#ref-su2026mdm)] proposed MDM-based optical interconnects, exploiting multiple spatial modes inside a single silicon waveguide to multiply transmission capacity without adding extra laser wavelengths.
- **3-D Optical Networks-on-Chip**: Ye et al. [[Ye2013ONoC](#ref-ye2013onoc)] pioneered 3D mesh optical networks combining vertical TSVs with planar photonic routing for high-throughput MPSoCs.
- **Energy Optimization and High-Radix Optical Routers**: Dynamic wavelength/power allocation by Liu et al. [[Liu2025Energy](#ref-liu2025energy)] and low-latency high-radix photonic switches by Gu et al. [[Gu2025Radix](#ref-gu2025radix)] establish practical scalability paths for optical fabrics.
- **Reconfigurable mmWave Wireless Architectures**: Zhang et al. [[Zhang2025Wireless](#ref-zhang2025wireless)] demonstrated adaptive beamforming and frequency-channel reconfigurability for on-chip millimeter-wave wireless links.

---

## References & Bibliography

1. <a id="ref-little1997"></a>**[Little1997]** B. E. Little, S. T. Chu, H. A. Haus, J. Foresi, and J.-P. Laine, "Microring Resonator Channel Dropping Filters," *IEEE Photonics Technology Letters*, vol. 9, no. 5, pp. 636–638, May 1997. [DOI: 10.1109/68.573983](https://doi.org/10.1109/68.573983).
2. <a id="ref-vantrease2008"></a>**[Vantrease2008]** D. Vantrease et al., "Corona: System Implications of Emerging Nanophotonic Technology," in *Proceedings of the 35th Annual International Symposium on Computer Architecture (ISCA)*, 2008, pp. 153–164. [DOI: 10.1145/1382119.1382137](https://doi.org/10.1145/1382119.1382137).
3. <a id="ref-kurian2010"></a>**[Kurian2010]** G. Kurian et al., "ATAC: A 1000-Core Heterogeneous Optically-Interconnected Routerless Chip Multiprocessor," in *Proceedings of the 19th International Conference on Parallel Architectures and Compilation Techniques (PACT)*, 2010, pp. 477–488. [DOI: 10.1145/1854273.1854332](https://doi.org/10.1145/1854273.1854332).
4. <a id="ref-deb2012"></a>**[Deb2012]** S. Deb, A. Ganguly, P. P. Pande, B. Belzer, and D. Heo, "Design of an Energy-Efficient CMOS-Compatible NoC Architecture with Millimeter-Wave Wireless Interconnects," *IEEE Transactions on Computers*, vol. 62, no. 12, pp. 2382–2396, Dec. 2012. [DOI: 10.1109/TC.2012.201](https://doi.org/10.1109/TC.2012.201).
5. <a id="ref-kao2026"></a>**[Kao2026]** W.-Y. Kao, T.-J. Lin, and Y.-W. Chang, "Provably Good Physically Aware WRONoC Design for Customized and Fault-Tolerant Topologies With Parallel Switching Elements and Sequence-Based Models," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 45, no. 3, pp. 650–663, Mar. 2026. [DOI: 10.1145/3658617.3697557](https://doi.org/10.1145/3658617.3697557).
6. <a id="ref-ye2013"></a>**[Ye2013]** Y. Ye, J. Xu, X. Wu, W. Zhang, X. Wang, M. Nikdast, Z. Wang, and W. Liu, "System-Level Modeling and Analysis of Thermal Effects in Optical Networks-on-Chip," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 21, no. 2, pp. 292–305, Feb. 2013. [DOI: 10.1109/TVLSI.2012.2185524](https://doi.org/10.1109/TVLSI.2012.2185524).
7. <a id="ref-shahmoradi2026"></a>**[Shahmoradi2026]** M. Shahmoradi, A. Yelboğa, E. Alarcón, K. K. Tokgöz, and S. Abadal, "Channel-Aware Behavioral Power Modeling of CMOS OOK Transceivers for Wireless Network-on-Chip Systems," *IEEE Transactions on Circuits and Systems I: Regular Papers*, vol. 73, no. 4, pp. 1620–1633, Apr. 2026. [DOI: 10.5281/zenodo.19449802](https://doi.org/10.5281/zenodo.19449802).
8. <a id="ref-abadal2018"></a>**[Abadal2018]** S. Abadal, E. Alarcón, A. Cabellos-Aparicio, M. C. Lemme, and M. Nemirovsky, "Graphene-Enabled Wireless Communication for Manycore Architectures," *IEEE Communications Magazine*, vol. 56, no. 6, pp. 30–36, June 2018. [DOI: 10.1109/MCOM.2018.1700609](https://doi.org/10.1109/MCOM.2018.1700609).
9. <a id="ref-taghvaee2022"></a>**[Taghvaee2022]** M. Taghvaee et al., "Fault-Tolerant Wireless Network-on-Chip Architecture for Multi-Core Systems," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 41, no. 10, pp. 3478–3491, Oct. 2022. [DOI: 10.1109/TCAD.2021.3131580](https://doi.org/10.1109/TCAD.2021.3131580).
10. <a id="ref-wang2021aco"></a>**[Wang2021ACO]** K. Wang et al., "Ant Colony Optimization-Based Thermal-Aware Adaptive Routing Mechanism for Optical NoCs," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 29, no. 5, pp. 950–963, May 2021. [DOI: 10.1109/TVLSI.2021.3059132](https://doi.org/10.1109/TVLSI.2021.3059132).
11. <a id="ref-fang2026rlrm"></a>**[Fang2026RLRM]** J. Fang et al., "RLRM: Reinforcement Learning-Based Routing for Ring-Augmented 2D-Mesh Optical Network-on-Chip," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 34, no. 5, pp. 1550–1563, May 2026. [DOI: 10.1109/TVLSI.2026.3681120](https://doi.org/10.1109/TVLSI.2026.3681120).
12. <a id="ref-kao2026wr"></a>**[Kao2026WR]** W.-Y. Kao et al., "Provably Good Physically Aware WRONoC Design for Customized Communication Requirements," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 45, no. 3, pp. 650–663, Mar. 2026. [DOI: 10.1109/TCAD.2025.3618810](https://doi.org/10.1109/TCAD.2025.3618810).
13. <a id="ref-su2026mdm"></a>**[Su2026MDM]** Y. Su et al., "A Novel MDM-Based Optical Networks-on-Chip With Reliability Optimization," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 45, no. 4, pp. 1680–1693, Apr. 2026. [DOI: 10.1109/TCAD.2025.3622410](https://doi.org/10.1109/TCAD.2025.3622410).
14. <a id="ref-ye2013onoc"></a>**[Ye2013ONoC]** Y. Ye et al., "3-D Mesh-Based Optical Network-on-Chip for Multiprocessor System-on-Chip," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 32, no. 4, pp. 586–599, Apr. 2013. [DOI: 10.1109/TCAD.2012.2230177](https://doi.org/10.1109/TCAD.2012.2230177).
15. <a id="ref-liu2025energy"></a>**[Liu2025Energy]** H. Liu et al., "Energy-Efficient Optical Network-on-Chip With Dynamic Wavelength and Power Allocation," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 33, no. 8, pp. 1920–1933, Aug. 2025. [DOI: 10.1109/TVLSI.2025.3562210](https://doi.org/10.1109/TVLSI.2025.3562210).
16. <a id="ref-gu2025radix"></a>**[Gu2025Radix]** F. Gu et al., "High-Radix Optical Router Architecture for Low-Latency and High-Throughput Interconnection," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 33, no. 9, pp. 2150–2163, Sept. 2025. [DOI: 10.1109/TVLSI.2025.3571120](https://doi.org/10.1109/TVLSI.2025.3571120).
17. <a id="ref-zhang2025wireless"></a>**[Zhang2025Wireless]** L. Zhang et al., "Reconfigurable Wireless Network-on-Chip Architecture for Millimeter-Wave Interconnects," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 33, no. 11, pp. 2580–2593, Nov. 2025. [DOI: 10.1109/TVLSI.2025.3592210](https://doi.org/10.1109/TVLSI.2025.3592210).
