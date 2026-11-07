#!/usr/bin/env python3
"""Builds remaining lessons for Tracks 8, 9, 10, 11, 12, 13.
"""

from pathlib import Path

LEARNING_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = LEARNING_DIR / "docs"

def write(rel, text):
    p = DOCS_DIR / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"Generated: {rel}")

def build_track8():
    write("track8-3d-noc-tsvs/02-tsv-parasitics-koz.md", """# Lesson 8.2: TSV Parasitics & Keep-Out Zones (KOZ)

<div class="noc-hero">
  <div class="noc-track-badge">Track 08 • Lesson 02</div>
  <h1>Through-Silicon Via (TSV) Parasitic Modeling &amp; Thermal Stress</h1>
  <p class="subtitle">
    Model copper-to-silicon thermal expansion mismatch, extract high-frequency TSV parasitic resistance and capacitance, and design keep-out zones to protect CMOS channel mobility.
  </p>
</div>

---

## 1. Electrical Modeling of TSVs

Through-Silicon Vias (TSVs) provide vertical interconnects across thinned silicon dies ($30\\text{--}50\\ \\mu\\text{m}$ thickness). A cylindrical TSV of diameter $D$ and height $H$ with dielectric liner thickness $t_{\\text{ox}}$ is modeled as a lumped $RLC$ circuit:

$$
R_{\\text{tsv}} = \\frac{4 \\rho_{\\text{Cu}} H}{\\pi D^2}
$$

$$
C_{\\text{tsv}} = \\frac{2 \\pi \\epsilon_{\\text{ox}} H}{\\ln\\left(1 + \\frac{2 t_{\\text{ox}}}{D}\\right)}
$$

For typical dimensions ($D = 5\\ \\mu\\text{m}, H = 40\\ \\mu\\text{m}, t_{\\text{ox}} = 200\\text{ nm}$), a TSV exhibits $R_{\\text{tsv}} \\approx 35\\text{ m}\\Omega$ and $C_{\\text{tsv}} \\approx 45\\text{ fF}$.

---

## 2. Thermo-Mechanical Stress & Keep-Out Zones (KOZ)

Copper has a coefficient of thermal expansion ($\text{CTE} \\approx 17\\text{ ppm/K}$) significantly higher than silicon ($\text{CTE} \\approx 2.6\\text{ ppm/K}$). Thermal cycling during manufacturing induces severe residual shear stress in the surrounding silicon lattice:

* **Piezoresistive Effect:** Compressive and tensile stresses alter silicon band structure, shifting PMOS and NMOS threshold voltages by up to $15\\%$ and degrading mobility.
* **Keep-Out Zone (KOZ):** Active transistors must be excluded from a circular region around the TSV (typically $R_{\\text{KOZ}} = 3\\text{--}5\\times D$) to prevent timing skew and circuit variability.

---

👉 **Next: [Lesson 8.3: 7-Port 3D Router Microarchitectures](03-3d-router-microarchitecture.md)**
""")

    write("track8-3d-noc-tsvs/03-3d-router-microarchitecture.md", """# Lesson 8.3: 7-Port 3D Router Microarchitectures

<div class="noc-hero">
  <div class="noc-track-badge">Track 08 • Lesson 03</div>
  <h1>7-Port Crossbars, Vertical Serialization &amp; Asymmetric Buffering</h1>
  <p class="subtitle">
    Expand planar 5-port routers to 7 ports (N, S, E, W, Up, Down, Local) while containing crossbar area explosion $O(P^2)$ and managing vertical TSV pitch constraints.
  </p>
</div>

---

## 1. The 7-Port Crossbar Challenge

Adding vertical dimensions increases the router radix from 5 to 7. A conventional monolithic crossbar matrix scales as $O(P^2)$: a $7 \\times 7$ switch requires $49$ crosspoints compared to $25$ in a 2D router ($+96\\%$ area increase).

To mitigate crossbar silicon overhead:
1. **Dimension-Decoupled Crossbars:** Separate planar traffic (N, S, E, W) from vertical traffic (Up, Down).
2. **Asymmetric Buffer Allocation:** Vertical links have near-zero wire flight latency compared to horizontal RC lines, permitting shallower vertical virtual channel buffers ($B_{\\text{vertical}} < B_{\\text{horizontal}}$).

---

👉 **Next: [Lesson 8.4: 3D Topologies, Thermal Stacking & Vertical Deadlock](04-3d-topologies-thermal-deadlock.md)**
""")

def build_track9():
    write("track9-chiplets-ucie/01-25d-packaging-economics.md", """# Lesson 9.1: 2.5D Packaging Economics & Reticle Limits

<div class="noc-hero">
  <div class="noc-track-badge">Track 09 • Lesson 01</div>
  <h1>Die Disaggregation, Negative Binomial Yield &amp; Packaging Technologies</h1>
  <p class="subtitle">
    Understand the economic forces driving monolithic SoCs into multi-die chiplets, calculate silicon yield curves, and compare silicon interposers (CoWoS) with embedded organic bridges (EMIB).
  </p>
</div>

---

## 1. The Reticle Limit & Yield Economics

Monolithic silicon dies are physically constrained by photolithography reticle limits ($\approx 858\\text{ mm}^2$). Furthermore, random defect densities make large monolithic dies economically ruinous under the **Negative Binomial Yield Model**:

$$
Y = \\left( 1 + \\frac{D_0 A}{\\alpha} \\right)^{-\\alpha}
$$

where $D_0$ is defect density, $A$ is die area, and $\\alpha$ is the defect clustering parameter ($\alpha \\approx 1.5\\text{--}2.0$). 

Disaggregating an $800\\text{ mm}^2$ monolithic GPU into four $200\\text{ mm}^2$ chiplets increases silicon die yield from $<30\\%$ to $>85\\%$, yielding substantial net manufacturing cost savings even after accounting for 2.5D packaging overhead.

---

## 2. Advanced Packaging Taxonomy

```mermaid
flowchart TD
    Monolithic["Monolithic Reticle Wall (~858 mm²)"] --> Disaggregation["Multi-Chiplet Disaggregation"]
    Disaggregation --> CoWoS["TSMC CoWoS<br/>Passive Silicon Interposer (High Density, High Cost)"]
    Disaggregation --> EMIB["Intel EMIB<br/>Embedded Multi-die Interconnect Bridge (Localized)"]
    Disaggregation --> HybridBonding["F2F Cu-Cu Hybrid Bonding<br/>Sub-micron pitch, >16 TB/s Bandwidth"]
```

---

👉 **Next: [Lesson 9.2: UCIe Protocol Stack & D2D Physical Layer](02-chiplets-ucie-interconnects.md)**
""")

    write("track9-chiplets-ucie/03-cross-die-deadlock-recovery.md", """# Lesson 9.3: Cross-Die Boundary Deadlock Recovery

<div class="noc-hero">
  <div class="noc-track-badge">Track 09 • Lesson 03</div>
  <h1>Boundary Interfaces, Cyclic Subpaths &amp; In/Outbound Swap</h1>
  <p class="subtitle">
    Analyze why connecting individually deadlock-free chiplets frequently induces catastrophic cross-die deadlocks, and implement backtracking swap mechanisms grounded in IEEE TCAD 2026.
  </p>
</div>

---

## 1. The Multi-Chiplet Deadlock Paradox

Even when every individual chiplet implements a provably deadlock-free routing algorithm (such as Dimension-Order Routing), interconnecting them across passive/active interposers creates **Cyclic Channel Dependencies across die boundary interfaces**.

Boundary bridge buffers frequently stall because outbound flits wait for downstream chiplet buffer credits while holding local inbound buffer resources, forming a global cyclic resource wait.

---

## 2. In/Outbound Backtracking Swap (TCAD '26)

Grounded in IEEE TCAD 2026 (*In/Outbound Swap: A Backtracking-based Deadlock Recovery Mechanism for Multi-Chiplet Networks*), deadlocks are resolved without wasting dedicated virtual channel buffers:
* **Detection:** Routers detect when boundary buffers remain stalled beyond an adaptive timeout window $T_{\\text{deadlock}}$.
* **Backtracking Swap:** Flit dependencies are dynamically swapped at the boundary router port, routing stalled packets onto localized escape paths and dissolving the cyclic dependency graph.

---

👉 **Next: [Lesson 9.4: Multi-Chiplet Router Bypassing (BuffeRS)](04-multichiplet-router-bypassing.md)**
""")

    write("track9-chiplets-ucie/04-multichiplet-router-bypassing.md", """# Lesson 9.4: Multi-Chiplet Router Bypassing & BuffeRS

<div class="noc-hero">
  <div class="noc-track-badge">Track 09 • Lesson 04</div>
  <h1>Near Wire-Speed Inter-Die Transit &amp; Buffer Reservation Scheduling</h1>
  <p class="subtitle">
    Eliminate multi-cycle store-and-forward penalties across chiplet boundaries using buffer-reserved router bypassing, achieving single-cycle transit across intermediate dies.
  </p>
</div>

---

## 1. The Inter-Die Latency Penalty

Traversing across a multi-chiplet package typically requires:
$$
T_{\\text{transit}} = N_{\\text{local}} \\cdot t_{\\text{router}} + T_{\\text{D2D}} + N_{\\text{remote}} \\cdot t_{\\text{router}}
$$
Where each intermediate router adds 3–4 pipeline cycles. For a 4-hop packet traversing two chiplets, latency exceeds $14\\text{ clock cycles}$.

---

## 2. The BuffeRS Architecture (IEEE TCAD '26)

Grounded in IEEE TCAD 2026 (*BuffeRS: A Buffer Reservation Scheduling Strategy for Router Bypassing in NoCs and Multichiplet Systems*):
* Upstream chiplet routers pre-reserve switch allocation slots at the downstream die bridge.
* Flits bypass intermediate router input buffers and crossbar arbitration in a **single clock cycle**, achieving near wire-speed transit across package boundaries.

Test this directly in our Web EDA Terminal:
```bash
guest@noc:~$ buffers-eval --hops 4 --bypass-slots 2
```

---

👉 **Advance to [Track 10: Optical & Wireless Networks-on-Chip](../track10-optical-wireless/)**
""")

def build_track10():
    write("track10-optical-wireless/01-silicon-nanophotonics-mrrs.md", """# Lesson 10.1: Silicon Nanophotonics & Microring Resonators

<div class="noc-hero">
  <div class="noc-track-badge">Track 10 • Lesson 01</div>
  <h1>Optical Waveguides, Microring Resonators &amp; Light Modulation</h1>
  <p class="subtitle">
    Transport data at the speed of light in silicon using single-mode optical waveguides, resonance condition tuning, and electro-optic microring modulators.
  </p>
</div>

---

## 1. Photonic Waveguides & The Speed of Light

Silicon optical waveguides ($450\\text{ nm} \\times 220\\text{ nm}$) exploit the high refractive index contrast between silicon ($n_{\\text{Si}} \\approx 3.45$) and silicon dioxide cladding ($n_{\\text{SiO2}} \\approx 1.45$) to achieve Total Internal Reflection (TIR). Optical propagation speed is:

$$
v_{\\text{opt}} = \\frac{c}{n_g} \\approx \\frac{3 \\times 10^8\\text{ m/s}}{4.0} = 7.5 \\times 10^7\\text{ m/s} = 75\\ \\mu\\text{m/ps}
$$

Light traverses a $10\\text{ mm}$ silicon interposer in just $133\\text{ ps}$ (less than half an electrical clock cycle at $3\\text{ GHz}$), with zero dynamic $CV^2f$ capacitive charging dissipation along the waveguide length!

---

## 2. Microring Resonators (MRRs)

A microring resonator consists of a circular waveguide looped adjacent to a straight bus waveguide. Constructive interference occurs at resonant wavelengths $\\lambda_m$:

$$
m \\cdot \\lambda_m = 2 \\pi R \\cdot n_{\\text{eff}}
$$

Applying a voltage across an embedded PN junction injects free carriers, shifting $n_{\\text{eff}}$ and modulating the optical carrier to encode data bits.

---

👉 **Next: [Lesson 10.2: Wavelength-Routed Optical NoC (WRONoC) Crossbars](02-wronoc-optical-crossbars.md)**
""")

    write("track10-optical-wireless/02-wronoc-optical-crossbars.md", """# Lesson 10.2: Wavelength-Routed Optical NoC (WRONoC)

<div class="noc-hero">
  <div class="noc-track-badge">Track 10 • Lesson 02</div>
  <h1>Wavelength-Division Multiplexing (WDM) &amp; Non-Blocking Optical Crossbars</h1>
  <p class="subtitle">
    Multiply interconnect bandwidth using dense WDM optical carriers, design non-blocking MRR crossbar matrices, and minimize optical insertion loss.
  </p>
</div>

---

## 1. Wavelength-Division Multiplexing (WDM)

By coupling $K$ laser wavelengths (e.g., $\\lambda_1 = 1550\\text{ nm}, \\lambda_2 = 1550.8\\text{ nm}, \\dots$) onto a single shared optical waveguide, total link bandwidth scales linearly without increasing physical metal wire count:

$$
\\text{Bandwidth} = K \\cdot f_{\\text{mod}}
$$

With $K = 64$ wavelengths modulating at $25\\text{ Gb/s}$, a single waveguide carries **$1.6\\text{ TB/s}$ of bi-directional data**.

---

👉 **Next: [Lesson 10.3: Laser Power-Gating & Automated Phase Control](03-laser-power-gating-apc.md)**
""")

    write("track10-optical-wireless/03-laser-power-gating-apc.md", """# Lesson 10.3: Laser Power-Gating & Thermal Drift Compensation

<div class="noc-hero">
  <div class="noc-track-badge">Track 10 • Lesson 03</div>
  <h1>Off-Chip Laser Efficiency, Thermal Ring Drift &amp; Automated Phase Control</h1>
  <p class="subtitle">
    Overcome the thermal sensitivity of microring resonators ($\sim 0.1\text{ nm/K}$), and evaluate laser power-gating techniques to maintain high wall-plug efficiency.
  </p>
</div>

---

## 1. Thermal Drift in Silicon Microrings

Silicon exhibits a high thermo-optic coefficient ($dn/dT \\approx 1.86 \\times 10^{-4}\\text{ K}^{-1}$). As neighboring processor cores heat up and cool down ($40^\circ\\text{C} \\to 90^\circ\\text{C}$), the resonant wavelength of MRRs drifts:

$$
\\frac{d\\lambda}{dT} = \\frac{\\lambda}{n_g} \\frac{dn_{\\text{eff}}}{dT} \\approx 0.10\\text{ nm/K}
$$

A temperature rise of just $8^\circ\\text{C}$ shifts the resonance completely off the laser carrier wavelength, causing optical signal blackout. Mitigation requires integrated micro-heaters driven by **Automated Phase Control (APC)** closed-loop feedback circuits.

---

👉 **Next: [Lesson 10.4: On-Chip Wireless NoC (WiNoC) Frontiers](04-wireless-noc-frontiers.md)**
""")

def build_track11():
    write("track11-security/01-security-threat-models.md", """# Lesson 11.1: Security Threat Models in On-Chip Networks

<div class="noc-hero">
  <div class="noc-track-badge">Track 11 • Lesson 01</div>
  <h1>Multi-Tenant SoCs, Untrusted Third-Party IPs &amp; Attack Taxonomy</h1>
  <p class="subtitle">
    Classify hardware security vulnerabilities in modern shared networks-on-chip: from malicious third-party IP cores to buffer-flooding Denial-of-Service and side-channel leakage.
  </p>
</div>

---

## 1. The Zero-Trust Silicon Paradigm

In cloud data centers and multi-tenant SoCs (e.g., AWS Graviton, Apple Silicon, heterogeneous automotive SoCs), multiple mutually distrusting applications share the same physical router fabric. Furthermore, modern chips integrate dozens of third-party IP blocks (3PIPs) whose transistor layouts cannot be fully verified:

```mermaid
flowchart TD
    SharedNoC["Shared On-Chip Interconnect"] --> Threat1["Denial of Service (DoS)<br/>Buffer Flooding & Bandwidth Starvation"]
    SharedNoC --> Threat2["Covert Timing Channels<br/>Packet Inter-Arrival Modulation"]
    SharedNoC --> Threat3["Thermal Covert Channels<br/>High-Frequency Power Throttle Attacks"]
    SharedNoC --> Threat4["Eavesdropping & Spoofing<br/>Unencrypted Packet Header Sniffing"]
```

---

## 2. Interactive Arcade Challenge

Defend against live hardware threats in our web arcade:

👉 **[Launch Silicon Sentinel: NoC Security &amp; Threat Defense Arcade](../../interactive/security/)**

---

👉 **Next: [Lesson 11.2: Thermal & Timing Covert Channels](02-thermal-timing-covert-channels.md)**
""")

    write("track11-security/02-thermal-timing-covert-channels.md", """# Lesson 11.2: Thermal & Timing Covert Channels

<div class="noc-hero">
  <div class="noc-track-badge">Track 11 • Lesson 02</div>
  <h1>Covert Timing Leakage, Substrate Thermal Coupling &amp; Key Exfiltration</h1>
  <p class="subtitle">
    Model how malicious hardware trojans exfiltrate 256-bit AES encryption keys across physically isolated virtual networks using packet delay variations and substrate thermal conduction.
  </p>
</div>

---

## 1. Timing Covert Channels

Even when an SoC enforces strict software process isolation, tenants share physical crossbars and virtual channels. An attacker core modulates the inter-arrival latency of benign packets:
* Bit `1`: Inject a burst of high-priority packets, congesting shared router buffers and delaying victim traffic.
* Bit `0`: Remain idle, allowing victim traffic to pass with minimal zero-load latency.

A receiver core measuring packet round-trip times can decode the transmitted bits at rates up to **$50\\text{ kb/s}$**, bypassing all software firewalls!

---

👉 **Next: [Lesson 11.3: Online WMA Anomaly Detection (HeatSense)](03-heatsense-wma-anomaly-detection.md)**
""")

    write("track11-security/03-heatsense-wma-anomaly-detection.md", """# Lesson 11.3: Online WMA Anomaly Detection (HeatSense)

<div class="noc-hero">
  <div class="noc-track-badge">Track 11 • Lesson 03</div>
  <h1>Hardware-Friendly Fixed-Point EWMA &amp; Shift-and-Add Arithmetic</h1>
  <p class="subtitle">
    Reproduce the landmark IEEE TCAD 2026 HeatSense architecture, implementing real-time thermal anomaly detection in synthesizable SystemVerilog with zero multiplier overhead.
  </p>
</div>

---

## 1. The HeatSense Architecture (IEEE TCAD '26)

Grounded in IEEE TCAD 2026 (*HeatSense: Intelligent Thermal Anomaly Detection for Securing NoC-Enabled MPSoCs*):
To detect thermal Trojans without burning power on 32-bit floating-point ALUs, HeatSense tracks baseline substrate temperature using a hardware-friendly **Exponentially Weighted Moving Average (EWMA)** where $\\alpha$ is constrained to powers of two:

$$
\\alpha = 2^{-S}
$$

$$
\\mu[n] = \\mu[n-1] + (T_{\\text{sensor}}[n] - \\mu[n-1]) \\gg S
$$

$$
\\sigma[n] = \\sigma[n-1] + (|T_{\\text{sensor}}[n] - \\mu[n-1]| - \\sigma[n-1]) \\gg S
$$

Threshold violation condition:
$$
|T_{\\text{sensor}}[n] - \\mu[n]| > K \\cdot \\sigma[n]
$$
Setting $K = 3$ (approx $3\\text{-sigma}$) is computed via $( \\sigma \\ll 1 ) + \\sigma$, requiring **zero hardware multipliers**!

---

## 2. Synthesizable Verilog: WMA Detector

```systemverilog
--8<-- "docs/textbook/ch11-security/code/wma_thermal_detector.sv"
```

---

👉 **Next: [Lesson 11.4: Hardware Trojan Mitigation & Zero-Trust Quarantine](04-trojan-defense-quarantine.md)**
""")

    write("track11-security/04-trojan-defense-quarantine.md", """# Lesson 11.4: Hardware Trojan Defense & Zero-Trust Quarantine

<div class="noc-hero">
  <div class="noc-track-badge">Track 11 • Lesson 04</div>
  <h1>Autonomous Isolation Protocols &amp; Physical Unclonable Functions (PUFs)</h1>
  <p class="subtitle">
    Quarantine rogue silicon cores in real time, scramble timing covert channels using LFSR phase jitter, and authenticate multi-die chiplets using intrinsic wire-delay PUFs.
  </p>
</div>

---

## 1. Autonomous Quarantine Protocol

When the WMA detector triggers an anomaly pulse, the router's Network Interface (NI) executes an autonomous containment sequence:
1. **Clock Gating:** Immediately gate the clock to the compromised tile to halt further thermal escalation.
2. **Packet Deflection:** Reconfigure routing arbitration masks to drop or reroute egress packets from the malicious port.
3. **Security Interrup:** Raise a trusted cryptographic interrupt to the secure root-of-trust core.

---

👉 **Advance to [Track 12: Domain-Specific NoCs for LLMs, Transformers & SNNs](../track12-ai-llm-snn/)**
""")

def build_track12():
    write("track12-ai-llm-snn/01-llm-collective-communication.md", """# Lesson 12.1: LLM Collective Communication Bottlenecks

<div class="noc-hero">
  <div class="noc-track-badge">Track 12 • Lesson 01</div>
  <h1>All-Reduce, All-to-All &amp; The Transformer Interconnect Wall</h1>
  <p class="subtitle">
    Quantify communication-to-computation ratios in 100B+ Large Language Models (LLMs), analyze tensor and pipeline parallelism, and evaluate the Ring All-Reduce bottleneck.
  </p>
</div>

---

## 1. Generative AI Interconnect Scaling

Large Language Models (LLMs) such as Llama-3 (70B/405B) and DeepSeek-V3 rely on massive distributed clusters. During multi-head attention and feed-forward training passes, tensor cores must synchronize gradients across all nodes:

$$
\\text{Volume}_{\\text{All-Reduce}} = 2 \\cdot \\frac{N-1}{N} \\cdot M
$$

where $N$ is the number of accelerator cores and $M$ is the tensor model parameter size in bytes. When computing 70B parameter models, memory and interconnect communication dominate over $70\\%$ of total cycle time.

---

## 2. Interactive Arcade Challenge

Accelerate generative AI models live in our web arcade:

👉 **[Launch Transformer Titan: LLM &amp; AI Collective Accelerator Arcade](../../interactive/transformer/)**

---

👉 **Next: [Lesson 12.2: In-Network Reduction Crossbars (PAC-NoC)](02-in-network-reduction-crossbars.md)**
""")

    write("track12-ai-llm-snn/02-in-network-reduction-crossbars.md", """# Lesson 12.2: In-Network Reduction Crossbars (PAC-NoC)

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
\\text{Flit}_{\\text{out}} = \\sum_{i \\in \\text{Active Ports}} \\text{Flit}_{\\text{in}}[i]
$$

Flits arriving from North, East, South, and West ports are summed dynamically inside the crossbar, emitting a single reduced flit up the hierarchical tree. This **reduces total network flit traffic by up to $75\\%$**!

---

## 2. Synthesizable Verilog: In-Network Reduction Router

```systemverilog
--8<-- "docs/textbook/ch12-ai-llm-snn/code/in_network_reduction_router.sv"
```

---

👉 **Next: [Lesson 12.3: Wafer-Scale Fabrics & Ruche Express Links](03-wafer-scale-ruche-fabrics.md)**
""")

    write("track12-ai-llm-snn/03-wafer-scale-ruche-fabrics.md", """# Lesson 12.3: Wafer-Scale Fabrics & Ruche Express Links

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

**Ruche networks** exploit upper metal layers ($M_{10}\\text{--}M_{12}$) to create direct express links spanning $K = 4\\text{--}8$ routers. Packets traverse across the die in single hops, bypassing intermediate input buffers while maintaining low router port count.

---

👉 **Next: [Lesson 12.4: Neuromorphic Event-Driven Spike Multicasting](04-neuromorphic-snn-multicast.md)**
""")

    write("track12-ai-llm-snn/04-neuromorphic-snn-multicast.md", """# Lesson 12.4: Neuromorphic Event-Driven Spike Multicasting

<div class="noc-hero">
  <div class="noc-track-badge">Track 12 • Lesson 04</div>
  <h1>Address-Event Representation (AER), Synaptic Fanout &amp; Hypergraph Cut</h1>
  <p class="subtitle">
    Route discrete axonal action potentials across millions of spiking neurons using Address-Event Representation (AER) and optimal hypergraph partitioning (SNNcut).
  </p>
</div>

---

## 1. Event-Driven Spiking Communication

Unlike synchronous clock-driven DNNs, Spiking Neural Networks (SNNs) communicate via discrete, sparse **action potential spikes**. Each spike is encoded using the **Address-Event Representation (AER)** protocol:

```text
┌────────────────────────┬────────────────────────┐
│  Source Neuron ID (16)  │  Timestamp Phase (16)  │
└────────────────────────┴────────────────────────┘
```

Because an axonal spike can have a synaptic fanout of $>10^3$ target dendrites, routers must support hardware **Multicast Replication Trees** without duplicating packet flits on shared physical links.

---

👉 **Advance to [Track 13: Capstone — Landmark Silicon Case Studies & System Synthesis](../track13-capstone/)**
""")

def build_track13():
    write("track13-capstone/05-grand-synthesis-moe.md", """# Lesson 13.5: Capstone Challenge: Zero-Trust MoE Accelerator

<div class="noc-hero">
  <div class="noc-track-badge">Track 13 • Lesson 05 • Capstone Grand Challenge</div>
  <h1>The Grand Synthesis: 16-Chiplet Zero-Trust MoE Collective Accelerator</h1>
  <p class="subtitle">
    Synthesize all 12 textbook chapters into a single production-grade multi-die architecture: implement All-Reduce collective crossbars, defend against thermal Trojans, and achieve timing closure.
  </p>
</div>

---

## 1. The Capstone Engineering Challenge

You are tasked with closing the design and verification of a **16-Chiplet Active Interposer Fabric** designed to serve a **70-Billion Parameter Mixture-of-Experts (MoE)** Generative AI workload:

```mermaid
flowchart TD
    subgraph Die0 ["Chiplet 0 (Tenant A)"]
        Core0["Tensor Core"] --> R0["Secure MoE Router Top"]
    end
    subgraph Die1 ["Chiplet 1 (Tenant B)"]
        Core1["Tensor Core"] --> R1["Secure MoE Router Top"]
    end
    subgraph Interposer ["2.5D Active Silicon Interposer Fabric"]
        R0 <--> R1
        R0 <--> R2["Chiplet 2 (Expert)"]
        R1 <--> R3["Chiplet 3 (Expert)"]
    end
```

### 📋 Architectural Specifications:
1. **Collective Acceleration (Ch 12):** Embedded In-Network Computing All-Reduce tree delivering $>0.70\\text{ flits/cycle}$ throughput under all-to-all token dispatch.
2. **Zero-Trust Threat Defense (Ch 11):** Integrated online WMA thermal anomaly filter intercepting thermal covert channels with zero false alarms.
3. **Deadlock Freedom (Ch 5):** SMT-verified acyclic turn-model routing across multi-chiplet boundaries.
4. **Timing Closure (Ch 1, 3, 6):** Standard cell synthesis targeting Nangate45, achieving $f_{\\max} \\ge 1.20\\text{ GHz}$ with positive setup slack.

---

## 2. Interactive Verification in the Web EDA Terminal

You can verify and grade this complete design directly in the browser:

```bash
guest@noc:~$ grade-capstone
```

Expected Output:
```text
╔═══════════════════════════════════════════════════════════════════════╗
║  CAPSTONE VERIFICATION SUITE: Zero-Trust MoE Collective Accelerator   ║
╚═══════════════════════════════════════════════════════════════════════╝
  [PASS] Gate 1: 16-Chiplet MoE All-to-All Token Throughput (>0.70 flit/cyc)
  [PASS] Gate 2: SMT Channel Dependency Graph Deadlock Freedom
  [PASS] Gate 3: TCAD '26 WMA Thermal Trojan Interception (>95% accuracy)
  [PASS] Gate 4: Nangate45 Static Timing Closure (fmax >= 1.20 GHz)
  FINAL SCORE: 100 / 100 • STATUS: SILICON GRANDMASTER CERTIFIED
```

👉 **[Open Interactive Web EDA Unix Terminal &amp; Visualizer](../../interactive/terminal/)**
""")

if __name__ == "__main__":
    build_track8()
    build_track9()
    build_track10()
    build_track11()
    build_track12()
    build_track13()
    print("All expanded lessons built successfully.")

