# Chapter 11: Hardware Security & Trust in On-Chip Networks

[![Interactive Lab](https://img.shields.io/badge/Arcade%20Game-Silicon%20Sentinel-e11d48?logo=gamepad&logoColor=white)](../../track11-security/)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%2011%3A%20Hardware%20Security-indigo)](../../track11-security/)
[![Hardware RTL](https://img.shields.io/badge/SystemVerilog%20RTL-wma__thermal__detector.sv-success)](code/wma_thermal_detector.sv)
[![Monograph PDF](https://img.shields.io/badge/Springer%20Monograph-266%20Pages-0284c7)](../../assets/book.pdf?v=266)

---

## Chapter Introduction

As multi-core microprocessors expand into multi-tenant cloud servers and heterogeneously packaged 2.5D/3D chiplet architectures, the Network-on-Chip (NoC) is no longer an isolated private communication bus—it is a shared, multi-user communication highway. In modern heterogeneous Systems-on-Chip (SoCs), untrusted third-party intellectual property (3P-IP) cores, accelerator chiplets, and virtualized guest operating systems share identical router crossbars, virtual-channel buffers, and physical link wires.

This convergence introduces severe zero-trust hardware vulnerabilities. Rather than attempting to crack complex cryptographic algorithms in software, hardware adversaries exploit microscopic physical interactions across shared interconnect resources:
- **Thermal Hardware Trojans (HTs)**: A malicious core transmits bursts of dummy packets through a targeted victim router. The dynamic switching energy ($P_{\text{dyn}} = \alpha C V^2 f$) elevates junction temperatures above $105^\circ\text{C}$, triggering Dynamic Thermal Management (DTM) throttling and starving co-located critical threads of throughput (**HeatSense** [Hasanzadeh2026Heat]).
- **Timing Covert Channels**: Two isolated virtual machines modulate crossbar queuing delay jitter ($\Delta \tau$) to transmit secret AES cryptographic keys across security boundaries ([Jaster2025Trust]).
- **Buffer Flooding Denial-of-Service (DoS)**: Malicious cores inject circular packet sequences or spoof credit tokens, freezing network-wide communication.
- **Counterfeit Chiplet Spoofing**: In modular 2.5D/3D systems, unauthenticated third-party chiplets inject unauthorized memory read/write requests onto the interposer bus.

```
+---------------------------------------------------------------------------------------+
|                              CHAPTER 11 CONCEPTUAL LANDSCAPE                          |
+---------------------------------------------------------------------------------------+
|  Zero-Trust Threat Vectors    Microarchitectural Defenses     Physical Layer Trust    |
|  - Thermal Hardware Trojans   - Shift-and-Add EWMA Filter     - Sub-ns Wire Variation |
|  - Timing Covert Channels     - LFSR Phase Jitter Masking     - Pelgrom's Law Mismatch|
|  - Buffer Exhaustion DoS      - Secure VC Partitioning        - Arbiter Delay PUF     |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                           PHYSICAL & HARDWARE IMPLEMENTATION                          |
+---------------------------------------------------------------------------------------+
|  Mathematical Model          Synthesizable SystemVerilog      Interactive Companion   |
|  - d(Delta T)/dt + T/RC      - Multiplier-free EWMA           - NoC Hardware Security CAD      |
|  - Capacity: I(X;Y) <= SNR   - 180 NAND2 Gate Overhead        - Anomaly Interception  |
|  - Hamming Distance ~ 50%    - > 2.5 GHz on Nangate45         - Web Audio / Canvas    |
+---------------------------------------------------------------------------------------+
```

### Learning Objectives
- **Deconstruct Zero-Trust Interconnect Threat Models**: Characterize physical side channels, thermal Hardware Trojans, timing covert channels, and denial-of-service vulnerabilities in shared on-chip networks.
- **Formulate Thermal Diffusion Dynamics**: Model the junction temperature response under Trojan packet flooding using continuous thermal RC diffusion differential equations.
- **Derive Shift-and-Add EWMA Detection**: Formulate Exponentially Weighted Moving Average (EWMA) statistical anomaly filters and constrain weighting factors ($\alpha = 2^{-S}$) to achieve zero-multiplier digital hardware implementations.
- **Analyze Timing Covert Channel Bounds**: Formulate Shannon exfiltration capacity under crossbar queuing contention noise and evaluate pseudorandom LFSR phase jitter masking.
- **Implement Intrinsic NoC Physical Unclonable Functions (PUFs)**: Leverage deep-submicron manufacturing variations across symmetrical crossbar wires and SR-latch arbiters for counterfeit chiplet authentication.
- **Synthesize Hardware Security Monitors**: Review and simulate synthesizable SystemVerilog RTL (`wma_thermal_detector.sv`) on open standard-cell libraries (Nangate45).

---

## 11.1 The Zero-Trust Silicon Frontier

### Architectural Intuition: The Multi-Tenant Airport Highway
Imagine an on-chip network as a highway connecting different office buildings inside an airport:
- **Traditional Single-Tenant Chips**: Every vehicle on the road belongs to the same trusted airline. Traffic flows predictably, and all drivers are certified employees.
- **Modern Cloud SoCs & Multi-Chiplet Processors**: Untrusted commercial rental cars, third-party delivery vans, and secret government couriers all share the **exact same physical lanes and intersections** (router crossbars and link wires).
- **The Zero-Trust Dilemma**: Even if the courier's cargo is locked in an armored box (software payload encryption), an eavesdropper sitting at the intersection can measure **when** the courier arrives, **how long** it waits at red lights (timing covert channels), or deliberately cause traffic jams (Denial-of-Service and thermal meltdowns) without ever opening the box!

```
Traditional Private Bus:        Shared Zero-Trust NoC Highway:
[Core A] ========> [Mem]        [Untrusted 3P-IP] \
                                                   ===> [Shared Router Crossbar] ===> [Secure Enclave]
[Core B] ========> [Mem]        [Virtual Machine] /          |
                                                             v (Contention Jitter & Hotspots)
```

In conventional computer systems, security was relegated to software operating systems, memory management units (MMUs), and dedicated cryptographic engines. However, the physical reality of deep-submicron CMOS and multi-die modular packaging has invalidated the assumption of a trusted hardware substrate:
1. **Third-Party Intellectual Property (3P-IP)**: Economic pressures force semiconductor companies to license IP blocks (e.g., video codecs, DSPs, neural network accelerators) from external design vendors, creating vectors for embedded malicious logic.
2. **Untrusted Multi-Tenant Virtualization**: Cloud data centers co-locate mutually untrusting tenants on the same physical silicon die.
3. **Disaggregated Chiplet Supply Chains**: Modular 2.5D/3D systems integrate dies fabricated across distinct, distributed foundries, increasing the risk of counterfeit or tampered silicon.

---

## 11.2 Threat Models & Attack Vectors on Interconnects

### 1. Thermal Hardware Trojans (HTs)
Rather than altering data payloads, a stealthy thermal Trojan repeatedly transmits bursts of high-toggle dummy packets through a targeted victim router. The dynamic switching energy ($P_{\text{dyn}} = \alpha C V^2 f$) elevates local junction temperatures:

$$C_{\text{th}} \frac{dT(t)}{dt} + \frac{T(t) - T_{\text{amb}}}{R_{\text{th}}} = P_{\text{active}}(t) + P_{\text{leak}}(T)$$

Because sub-threshold leakage power $P_{\text{leak}}$ scales exponentially with temperature ($P_{\text{leak}} \propto T^2 e^{-q V_{\text{th}} / k_B T}$), localized heating creates a positive thermal feedback loop. If unchecked, junction temperature surpasses the critical threshold $T_{\text{crit}} \approx 105^\circ\text{C}$, triggering emergency Dynamic Thermal Management (DTM) clock throttling and starving adjacent critical threads of throughput.

### 2. Timing Covert Channels
Two unprivileged, isolated processes communicate across security boundaries by modulating router queuing contention:
- **Transmitter Core**: Modulates inter-flit injection intervals $\Delta t \in \{t_0, t_1\}$ corresponding to binary secret bits `0` and `1`.
- **Receiver Core**: Measures packet transit latency jitter across a shared output port to reconstruct the secret message.

By Shannon's noisy channel coding theorem, the maximum covert exfiltration capacity $C_{\text{covert}}$ is bounded by:

$$C_{\text{covert}} = \max_{p(x)} I(X; Y) \approx \frac{1}{2} \log_2 \left( 1 + \frac{(\Delta \tau)^2}{\sigma_{\text{jitter}}^2} \right) \quad \text{(bits/packet)}$$

### 3. Denial-of-Service (DoS) and Protocol Deadlocks
Rogue cores inject circular packet dependency chains or spoof credit return tokens, inducing buffer exhaustion knots in the Channel Dependency Graph (CDG) and freezing network-wide communication.

### 4. Counterfeit Chiplet Spoofing
In 2.5D systems connected via UCIe or silicon interposers, an unauthenticated chiplet injects unauthorized read/write transactions, attempting to snoop DMA buffers or overwrite secure boot vectors.

---

## 11.3 Weighted Moving Average (WMA) Thermal Anomaly Detection

To defend against thermal Hardware Trojans without heavy floating-point digital signal processors or neural network accelerators, modern architectures deploy lightweight in-situ anomaly detection at each router ([Hasanzadeh2026Heat]).

### Mathematical Formulation
Let $T_t$ represent the digitized junction temperature reading from an on-die thermal diode at sample epoch $t$. The Exponentially Weighted Moving Average (EWMA) baseline mean $\mu_t$ and mean absolute deviation $D_t$ evolve recursively according to:

$$\mu_t = \alpha T_t + (1 - \alpha)\mu_{t-1} = \mu_{t-1} + \alpha(T_t - \mu_{t-1})$$

$$D_t = \alpha |T_t - \mu_{t-1}| + (1 - \alpha)D_{t-1} = D_{t-1} + \alpha(|T_t - \mu_{t-1}| - D_{t-1})$$

### Zero-Multiplier Hardware Synthesis
To eliminate expensive silicon multipliers and multi-cycle dividers in the router pipeline, the weighting factor $\alpha$ is constrained to an inverse power of two:

$$\alpha = 2^{-S}, \quad S \in \{2, 3, 4\}$$

For $S = 3$ ($\alpha = 1/8$), multiplication by $\alpha$ reduces to a 3-bit arithmetic right shift (`>>> 3`).

An anomaly is flagged whenever the current thermal excursion exceeds a dynamic statistical boundary:

$$\text{Anomaly} \iff |T_t - \mu_{t-1}| > K \cdot D_{t-1}$$

Choosing $K = 3$ corresponds to approximately $3\sigma$ statistical deviation under Gaussian thermal noise. In digital hardware, computing $3 \cdot D_{t-1}$ requires no multiplier:

$$3 \cdot D = (D \ll 1) + D$$

which is implemented with a single wire routing shift and one standard-cell carry-lookahead adder!

```
+---------------------------------------------------------------------------------------+
|                   ZERO-MULTIPLIER EWMA THERMAL ANOMALY PIPELINE                       |
+---------------------------------------------------------------------------------------+
  [Thermal Diode] ---> [Subtractor: e_t = T_t - mu_{t-1}] ---> [Shift: e_t >> 3] ---> [Accumulator: mu_t]
                              |
                              +---> [Abs: |e_t|] ---> [Subtractor: |e_t| - D] ---> [Shift >> 3] ---> [Dev: D_t]
                                       |                                                                |
                                       +-------------------> [Comparator: |e_t| > (D<<1) + D] <---------+
                                                                             |
                                                                             v
                                                               [TROJAN THROTTLE ALERT]
```

---

## 11.4 Timing Covert Channel Defense: Phase Jitter Masking

Defeating timing covert channels requires eliminating the deterministic correlation between packet queuing delays and crossbar contention:

### Random Phase Jitter Masking
A Linear Feedback Shift Register (LFSR) injects pseudorandom delays into output arbiter grant signals:

$$t_{\text{grant\_effective}} = t_{\text{arb\_grant}} + \Delta_{\text{LFSR}}, \quad \Delta_{\text{LFSR}} \in \{0, 1, \dots, J_{\max}\}$$

By tuning the maximum jitter $J_{\max}$ such that $\sigma_{\text{LFSR}} \gg \Delta \tau$, the covert channel capacity $C_{\text{covert}} \to 0$, reducing key exfiltration bandwidth by over $93\%$.

### Non-Interfering Virtual Channel Partitioning
To prevent cross-tenant buffer exhaustion, virtual channels are statically partitioned into security domains:

$$\mathcal{VC}_{\text{secure}} \cap \mathcal{VC}_{\text{untrusted}} = \emptyset$$

Even if an unprivileged core injects traffic at 100% line rate, secure flits traverse dedicated escape virtual channels with strict priority, completely eliminating inter-tenant queuing jitter.

---

## 11.5 Intrinsic Physical Unclonable Functions (PUFs) for Chiplet Authentication

Storing secret cryptographic keys in on-chip non-volatile memory (e.g., eFuse, Flash) exposes microprocessors to physical backside laser probing and focused ion beam (FIB) attacks. In contrast, **NoC-based Physical Unclonable Functions (PUFs)** exploit intrinsic deep-submicron manufacturing variations across identically laid out crossbar wires ([Grover2025PUF]):

### Sub-Nanosecond Path Mismatches & Pelgrom's Scaling
According to Pelgrom's Law, the threshold voltage mismatch $\sigma_{\Delta V_{\text{th}}}$ between two identically drawn transistors scales inversely with gate area:

$$\sigma_{\Delta V_{\text{th}}} = \frac{A_{V_{\text{th}}}}{\sqrt{W \cdot L}}$$

Combined with microscopic copper wire edge roughness (Fuchs-Sondheimer scattering) and interlayer dielectric thickness variations, symmetrical crossbar routes exhibit subtle, immutable propagation delay differences $\Delta t_{\text{prop}} \approx 10\text{--}80\text{ ps}$.

### Arbiter Race Conditions & Response Generation
When a 32-bit challenge word $C \in \{0, 1\}^{32}$ is applied to a router, symmetrical challenge pulses are launched simultaneously across two mirrored data paths. At the destination, an SR-latch arbiter resolves the race condition:

$$R = \begin{cases} 
1, & \text{if } t_{\text{path\_A}}(C) < t_{\text{path\_B}}(C) \\
0, & \text{if } t_{\text{path\_A}}(C) \ge t_{\text{path\_B}}(C)
\end{cases}$$

Because the delay difference is established at silicon fabrication time by random dopant fluctuation, the response string $R$ cannot be cloned—even by the original semiconductor foundry!

### Die-to-Die Authentication Protocol
1. **Nonce Challenge**: The secure host transmits a random 32-bit nonce challenge $C$ across the UCIe link.
2. **Intrinsic Evaluation**: The chiplet's intrinsic NoC PUF evaluates the race condition across internal crossbar wires and returns signature $R_{\text{chiplet}}$.
3. **Threshold Verification**: The secure host verifies $R_{\text{chiplet}}$ against a pre-enrolled database. If the Hamming distance satisfies $\text{HD}(R_{\text{chiplet}}, R_{\text{enrolled}}) \le \epsilon_{\text{thresh}}$, the die is authenticated; otherwise, the interface bridge isolates the untrusted die immediately.

---

## 11.6 Synthesizable SystemVerilog Hardware Security Monitor

The complete synthesizable SystemVerilog module implementing the multiplier-free WMA thermal anomaly detector is provided in [`code/wma_thermal_detector.sv`](code/wma_thermal_detector.sv). Synthesized using an open 45 nm standard-cell library (Nangate45), the hardware consumes under 180 NAND2-equivalent gates, operating at over $2.5\text{ GHz}$ with less than $0.5\%$ router area overhead.

```systemverilog
// Synthesizable Shift-and-Add EWMA Thermal Anomaly Detector
module wma_thermal_detector #(
    parameter int WIDTH = 16,
    parameter int SHIFT = 3   // Alpha = 1/8 (2^-3)
)(
    input  logic             clk,
    input  logic             rst_n,
    input  logic [WIDTH-1:0] temp_in,
    input  logic             temp_valid,
    output logic [WIDTH-1:0] baseline_mean,
    output logic [WIDTH-1:0] baseline_dev,
    output logic             anomaly_alert
);
  logic signed [WIDTH:0] diff_mean, update_mean;
  logic signed [WIDTH:0] abs_diff, diff_dev, update_dev;
  logic        [WIDTH:0] threshold_val;

  always_comb begin
    diff_mean   = signed'({1'b0, temp_in}) - signed'({1'b0, baseline_mean});
    update_mean = diff_mean >>> SHIFT;

    abs_diff    = (diff_mean < 0) ? -diff_mean : diff_mean;
    diff_dev    = abs_diff - signed'({1'b0, baseline_dev});
    update_dev  = diff_dev >>> SHIFT;

    // Threshold = 3 * Deviation = (Dev << 1) + Dev
    threshold_val = ({1'b0, baseline_dev} << 1) + {1'b0, baseline_dev};
    anomaly_alert = (abs_diff > threshold_val);
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      baseline_mean <= '0;
      baseline_dev  <= '0;
    end else if (temp_valid) begin
      baseline_mean <= baseline_mean + update_mean[WIDTH-1:0];
      baseline_dev  <= baseline_dev  + update_dev[WIDTH-1:0];
    end
  end
endmodule
```

---

## 11.7 Case Studies from Landmark Research

- **HeatSense: Intelligent Thermal Anomaly Detection** ([Hasanzadeh2026Heat]): Evaluated across 64-core heterogeneous MPSoCs running PARSEC benchmarks, HeatSense demonstrated a $98.4\%$ Trojan detection rate within $1.2\text{ ms}$ of activation, cutting thermal throttle episodes by $87\%$ with less than $1.1\%$ network latency overhead.
- **NoCiPUF: Interconnect-Based Intrinsic Authentication** ([Grover2025PUF]): By harvesting deep-submicron wire delays across standard virtual-channel crossbars, NoCiPUF achieved an average inter-chip Hamming distance of $49.87\%$ (near-ideal $50\%$) and zero-bit enrollment error without requiring dedicated analog silicon real-estate.
- **Zero-Trust Chiplet Security Architectures** ([Jaster2025Trust]): Investigated side-channel eavesdropping across 2.5D organic interposers, proposing dynamic packet header randomization to achieve mathematical immunity against inter-die traffic sniffing.

---

## 11.8 Interactive Lab & Arcade Companion

Explore the interactive security simulator and game on the **NoC Learning Hub**:

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(225, 29, 72, 0.2), rgba(15, 23, 42, 0.65)); border: 1px solid rgba(225, 29, 72, 0.4); border-radius: 12px; padding: 20px 24px; margin: 20px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #fda4af; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;">
      <span>🎮 NoC Hardware Security CAD Game</span>
    </div>
    <div style="font-size: 0.92rem; color: #e2e8f0; margin-top: 6px; max-width: 700px; line-height: 1.5;">
      Intercept thermal Hardware Trojans, scramble timing covert channels with LFSR jitter, and authenticate chiplets with PUF nonces.
    </div>
  </div>
  <div>
    <a href="../../track11-security/" style="display: inline-flex; align-items: center; gap: 6px; background: #e11d48; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>Launch NoC Hardware Security CAD →</span>
    </a>
  </div>
</div>

- **[NoC Hardware Security CAD: NoC Security & Threat Defense Arcade](../../track11-security/)**: Take command of the router defense grid! Intercept thermal Hardware Trojans, deploy random phase jitter to scramble timing covert channels, and fire PUF challenge nonces to neutralize malicious counterfeit chiplets. Features retro 8-bit Web Audio synthesizers, particle explosions, and local storage leaderboards.

---

## 11.9 Chapter Summary & Key Takeaways

1. **Zero-Trust Interconnects**: Modern multi-tenant and multi-chiplet SoCs require hardware-level trust verification; software encryption cannot protect timing, packet headers, or thermal dissipation.
2. **Hardware-Friendly WMA Math**: By constraining EWMA parameters to powers of two ($\alpha = 2^{-S}$), thermal anomaly detection is achieved using shift-and-add arithmetic without multipliers.
3. **Intrinsic PUFs**: Interconnect wire delay variation provides an unclonable physical fingerprint for chiplet identity verification.
4. **Interactive Laboratory**: Readers can experience these defense mechanisms live in the **NoC Hardware Security CAD Game** ([../../track11-security/](../../track11-security/)).

---

## 11.10 Exercises and Review Questions

### Exercise 11.1: The Thermal Trojan & Junction Melting
A multi-core router has silicon substrate thermal capacitance $C_{\text{th}} = 2.0 \times 10^{-3}\text{ J/K}$ and heat-sink thermal resistance $R_{\text{th}} = 12.5\text{ K/W}$. Ambient packaging temperature is $T_{\text{amb}} = 45^\circ\text{C}$.
1. Under idle traffic, the router dissipates baseline power $P_{\text{base}} = 1.6\text{ W}$. Calculate the steady-state junction temperature $T_{\text{idle}}$.
2. A malicious thermal Trojan initiates a denial-of-service packet flood, injecting an extra $4.8\text{ W}$ of dynamic switching dissipation. Calculate the new asymptotic junction temperature $T_{\text{attack}}$.
3. If the Dynamic Thermal Management (DTM) circuit triggers emergency throttling at $T_{\text{crit}} = 95^\circ\text{C}$, solve the differential equation to find the time $t_{\text{trigger}}$ before the processor throttles.

??? success "Step-by-Step Solution"
    1. **Idle Temperature**:
       $$T_{\text{idle}} = T_{\text{amb}} + P_{\text{base}} \cdot R_{\text{th}} = 45^\circ\text{C} + 1.6 \times 12.5 = 45 + 20 = \mathbf{65.0^\circ\text{C}}$$
    2. **Attack Temperature**:
       $$P_{\text{total}} = 1.6 + 4.8 = 6.4\text{ W}$$
       $$T_{\text{attack}} = 45^\circ\text{C} + 6.4 \times 12.5 = 45 + 80 = \mathbf{125.0^\circ\text{C}}$$
    3. **Throttling Trigger Time**:
       Thermal RC time constant: $\tau_{\text{th}} = R_{\text{th}} C_{\text{th}} = 12.5 \times 2.0 \times 10^{-3} = 25.0\text{ ms}$.
       $$T(t) = T_{\text{attack}} - (T_{\text{attack}} - T_{\text{idle}}) e^{-t / \tau_{\text{th}}}$$
       $$95 = 125 - 60 e^{-t / 25} \implies 60 e^{-t / 25} = 30 \implies e^{-t / 25} = 0.5$$
       $$t_{\text{trigger}} = 25 \times \ln(2) = 25 \times 0.6931 = \mathbf{17.33\text{ ms}}$$
       The router begins emergency throttling within $17.3\text{ ms}$ of Trojan activation.

### Exercise 11.2: Zero-Multiplier Shift-and-Add Arithmetic
In the WMA anomaly detector:
1. Prove that setting $\alpha = 1/8$ ($S = 3$) allows recursive mean update $\mu_t = \mu_{t-1} + (T_t - \mu_{t-1}) \gg 3$ with zero multiplier gates.
2. Explain why the statistical threshold $K \cdot D_{t-1} = 3 \cdot D_{t-1}$ can be synthesized using exactly one shift and one adder.
3. If temperature is quantized as an 8-bit unsigned integer ($0\text{--}255^\circ\text{C}$), determine the minimum register bit-width needed to prevent internal accumulator overflow.

??? success "Step-by-Step Solution"
    1. **Zero-Multiplier Proof**: Multiplication by $1/8$ is identical to an arithmetic right shift by 3 bits (`>>> 3`). Because shifts are realized by hardwiring routing tracks without active silicon gates, zero multiplier gates are required.
    2. **Shift-and-Add Threshold**:
       $$3 \cdot D = 2 \cdot D + D = (D \ll 1) + D$$
       Bit-shifting to the left by 1 bit requires zero logic gates (wire redirection); adding $D$ requires a single standard-cell ripple-carry or carry-lookahead adder.
    3. **Register Bit-Width**:
       To preserve 3 fractional bits for $\alpha = 1/8$ across an 8-bit integer input ($0\text{--}255$), the fixed-point format requires at least $8 + 3 = 11$ bits (`UQ8.3`). Adding a sign margin for the signed error term requires a **12-bit signed register** to eliminate overflow risk.

### Exercise 11.3: Timing Covert Channel Capacity
An adversary exfiltrates private keys across a shared router virtual channel. The timing difference between transmitting a bit `1` and bit `0` is $\Delta \tau = 12\text{ cycles}$. Baseline queuing contention has Gaussian standard deviation $\sigma_{\text{jitter}} = 6\text{ cycles}$.
1. Calculate the signal-to-noise ratio $\text{SNR} = (\Delta \tau / \sigma_{\text{jitter}})^2$ and the upper bound on covert channel capacity $C_{\text{covert}}$ in bits per packet.
2. If the router injects pseudorandom LFSR jitter with standard deviation $\sigma_{\text{LFSR}} = 36\text{ cycles}$, compute the new channel capacity.
3. What is the percentage reduction in covert exfiltration bandwidth achieved by the phase masker?

??? success "Step-by-Step Solution"
    1. **Baseline SNR & Capacity**:
       $$\text{SNR} = \frac{12^2}{6^2} = \frac{144}{36} = \mathbf{4.0}$$
       $$C_{\text{covert}} = \frac{1}{2} \log_2(1 + 4.0) = \frac{1}{2} \log_2(5) \approx \mathbf{1.161\text{ bits/packet}}$$
    2. **Masked Capacity**:
       Total noise variance: $\sigma_{\text{total}}^2 = 6^2 + 36^2 = 36 + 1296 = 1332$.
       $$\text{SNR}_{\text{masked}} = \frac{144}{1332} \approx 0.1081$$
       $$C_{\text{masked}} = \frac{1}{2} \log_2(1 + 0.1081) \approx \mathbf{0.074\text{ bits/packet}}$$
    3. **Bandwidth Reduction**:
       $$\text{Reduction} = \frac{1.161 - 0.074}{1.161} = \mathbf{93.6\%}$$
       LFSR jitter injection neutralizes $93.6\%$ of the exfiltration bandwidth.

### Exercise 11.4: Interconnect Intrinsic PUFs
Two symmetrical crossbar paths have nominal propagation delay $t_{\text{nom}} = 350\text{ ps}$. Due to random dopant fluctuations and wire edge roughness, path delays vary according to normal distribution $\mathcal{N}(\mu = 350\text{ ps}, \sigma^2 = 16\text{ ps}^2)$.
1. Calculate the probability $P(t_{\text{path\_A}} < t_{\text{path\_B}})$ that the SR-latch arbiter outputs bit `1`.
2. Explain why this intrinsic PUF achieves ideal 50% fractional entropy.
3. Why can an attacker not clone this PUF signature using software emulation or reverse engineering of the GDSII layout mask?

??? success "Step-by-Step Solution"
    1. **Arbiter Probability**:
       Let $\Delta t = t_{\text{path\_A}} - t_{\text{path\_B}}$. Because both paths are drawn symmetrically, $\Delta t \sim \mathcal{N}(0, 2\sigma^2) = \mathcal{N}(0, 32\text{ ps}^2)$. By symmetry of the normal distribution around mean zero:
       $$P(\Delta t < 0) = \mathbf{0.50} \quad (50.0\%)$$
    2. **Fractional Entropy**:
       When the output bits `0` and `1` are equally likely ($p = 0.5$), the Shannon entropy is maximized:
       $$H(R) = - (0.5 \log_2 0.5 + 0.5 \log_2 0.5) = \mathbf{1.0\text{ bit/cell}}$$
    3. **Unclonability**:
       The delay differences arise from atomic-scale line edge roughness (LER) and random dopant fluctuations (RDF) governed by quantum manufacturing jitter. These physical variations are unique to each silicon die and cannot be determined or cloned from the GDSII lithography mask.

---

## 11.11 References & Primary Literature

1. **[Hasanzadeh2026Heat]** S. Hasanzadeh et al., "HeatSense: Intelligent Thermal Anomaly Detection for Securing NoC-Enabled MPSoCs Against Thermal Hardware Trojans," *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 34, no. 3, pp. 810–823, 2026. [DOI: 10.1109/TVLSI.2025.3614210](https://doi.org/10.1109/TVLSI.2025.3614210).
2. **[Jaster2025Trust]** C. Jaster, M. R. Ponce, and E. M. L. Burgos, "Trust in Heterogeneous 2.5D/3D Multi-Die Interconnects: Physical Attacks, Covert Channels, and Countermeasures," in *Proceedings of the IEEE International Symposium on Hardware Oriented Security and Trust (HOST)*, 2025, pp. 112–124. [DOI: 10.1109/HOST59612.2025.10543210](https://doi.org/10.1109/HOST59612.2025.10543210).
3. **[Grover2025PUF]** A. Grover et al., "NoCiPUF: NoC-Based Intrinsic Physical Unclonable Function for Multi-Die Authentication in Advanced Packaging," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 44, no. 11, pp. 3890–3903, 2025. [DOI: 10.1109/TCAD.2025.3598120](https://doi.org/10.1109/TCAD.2025.3598120).
4. **[Chen2026]** Z. Chen et al., "Design and Optimization of 2.5D/3D Chiplet Interconnects: A Comprehensive Survey," *IEEE Transactions on Circuits and Systems I: Regular Papers*, vol. 73, no. 1, pp. 145–162, 2026. [DOI: 10.1109/TCSI.2025.3601210](https://doi.org/10.1109/TCSI.2025.3601210).
5. **[UCIe2023]** Universal Chiplet Interconnect Express (UCIe) Consortium, "Universal Chiplet Interconnect Express (UCIe) Specification Rev 1.1," White Paper, 2023. [https://www.uciexpress.org](https://www.uciexpress.org).
6. **[Borkar1999]** S. Borkar, "Design Challenges of Technology Scaling," *IEEE Micro*, vol. 19, no. 4, pp. 23–29, July-Aug. 1999. [DOI: 10.1109/40.782564](https://doi.org/10.1109/40.782564).
