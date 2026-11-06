# Chapter 11: Hardware Security & Trust in On-Chip Networks

[![Companion Platform](https://img.shields.io/badge/Interactive%20Arcade-Silicon%20Sentinel-0284c7?logo=gamepad&logoColor=white)](https://network-on-chip.github.io/learning/interactive/security/)
[![Curriculum Track](https://img.shields.io/badge/Learning%20Track-Track%208%3A%20Hardware%20Security-red)](https://network-on-chip.github.io/learning/track8-security/)
[![Hardware RTL](https://img.shields.io/badge/SystemVerilog%20RTL-wma__thermal__detector.sv-success)](code/wma_thermal_detector.sv)
[![Reference Papers](https://img.shields.io/badge/IEEE%20TCAD%202026-HeatSense%20%7C%20NoCiPUF-purple)](https://doi.org/10.1145/3639821)

---

## Chapter Introduction

As multi-core processors expand into multi-tenant cloud servers and heterogeneously packaged 2.5D/3D chiplet ecosystems, the Network-on-Chip (NoC) is no longer an isolated internal bus—it is a **shared multi-user communication highway**. In modern heterogeneous SoCs, third-party intellectual property (3P-IP) blocks, untrusted accelerator chiplets, and untrusted virtualized guest operating systems share identical router crossbars, virtual channel buffers, and physical link wires.

This multi-tenant physical convergence creates severe **zero-trust hardware security vulnerabilities**:
1. **Thermal Hardware Trojans (HTs):** Malicious IP cores silently manipulate traffic patterns to induce localized thermal hotspots, tripping Dynamic Thermal Management (DTM) throttling and degrading system performance or accelerating physical wearout.
2. **Timing Covert Channels:** Co-located malicious applications extract cryptographic secrets (such as AES private keys) by measuring packet traversal jitter ($\Delta t$) and buffer contention across shared router queues.
3. **Denial-of-Service (DoS) Buffer Exhaustion:** Rogue or defective nodes flood router input ports with circular packet streams, inducing global buffer starvation and network-wide livelocks.

Traditional software cryptography and payload encryption fail to address these interconnect-level attacks: encrypting 64-bit or 128-bit on-chip flits introduces multi-cycle latency, massive silicon area overhead, and leaves routing headers, packet arrival times, and thermal dissipation completely unshielded.

Modern on-chip security requires **architectural and physical-layer defenses**: lightweight in-situ anomaly detection at router crossbars, intrinsic Physical Unclonable Functions (PUFs) derived from sub-nanosecond wire delay variation, and traffic jitter shaping.

```
+---------------------------------------------------------------------------------------+
|                              CHAPTER 11 CONCEPTUAL LANDSCAPE                          |
+---------------------------------------------------------------------------------------+
|  Interconnect Threat Models    Physical-Layer Defenses         Architectural Security |
|  - Thermal Hardware Trojans    - WMA Thermal Anomaly Filters   - Oblivious Routing    |
|  - Timing Covert Channels      - Intrinsic Interconnect PUFs   - Dynamic Quarantine   |
|  - DoS Buffer Starvation       - Delay Fingerprint Auth        - Jitter Watermarking  |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                           HARDWARE METRICS & TRADEOFFS                                |
+---------------------------------------------------------------------------------------+
|  Anomaly Detection Latency    Silicon Area Overhead (<2%)      Packet Delay Penalty   |
|  - Exponential WMA (α = 1/8)  - Zero multipliers (bit-shifts)  - Jitter vs. Bandwidth |
|  - 3-sigma dynamic threshold  - Standard-cell synthesis        - Line-rate filtering  |
+---------------------------------------------------------------------------------------+
```

### Learning Objectives
- **Deconstruct On-Chip Threat Vectors**: Formulate attack mechanics for thermal Hardware Trojans, timing covert channels, and packet corruption in multi-tenant NoCs.
- **Formulate Weighted Moving Average (WMA) Anomaly Filtering**: Mathematically derive exponential moving average baseline estimation ($\mu_t$) and absolute deviation ($\sigma_t$) with zero-multiplier bit-shift hardware implementations (**HeatSense**, TCAD 2026).
- **Evaluate Intrinsic Physical Unclonable Functions (PUFs)**: Formulate path delay variations across router crossbar arbiters to construct challenge-response pairs for zero-overhead chiplet authentication (**NoCiPUF**, TCAS-I 2025).
- **Mitigate Timing Covert Channels**: Quantify Shannon mutual information in packet departure intervals and design pseudo-random jitter injection mechanisms.
- **Implement Synthesizable Hardware Monitors**: Deploy standard-cell SystemVerilog RTL for real-time router anomaly detection and hardware port quarantine.
- **Interactive Arcade Simulation**: Defend a multi-tenant SoC against escalating Trojan and exfiltration attacks in the [`Silicon Sentinel Arcade`](https://network-on-chip.github.io/learning/interactive/security/).

---

## 11.1 The Zero-Trust Silicon Frontier

In traditional systems, security was assumed to be an operating system or software concern. In modern silicon reality, hardware is vulnerable:

```
Multi-Tenant Shared Silicon Substrate:
+-------------------+      +-------------------+
| Tenant A (Secure) |      | Tenant B (Rogue)  |
| AES Engine / Encl |      | Untrusted 3P-IP   |
+---------+---------+      +---------+---------+
          | (Flits)                  | (Trojan Jitter)
          v                          v
   +--------------+           +--------------+
   |   Router 0   |<=========>|   Router 1   |  <--- Shared Buffer Contention
   +--------------+           +--------------+
```

When Tenant B floods packets through Router 1, Tenant A experiences queue head-of-line blocking. By measuring the variance in round-trip ACK delays, Tenant B can deduce whether Tenant A is computing a cryptographic modular exponentiation, successfully reconstructing private keys without ever reading Tenant A's memory!

---

## 11.2 Threat Models & Attack Vectors

### 1. Thermal Hardware Trojans (HTs)
A thermal Trojan does not corrupt data payloads; instead, it repeatedly routes dummy flits through a targeted victim router. The dynamic switching energy ($P_{\text{dyn}} = \alpha C V^2 f$) heats the victim tile above its safe junction threshold ($T_j > 105^\circ\text{C}$). This triggers hardware DTM throttling, causing severe Quality-of-Service (QoS) degradation for critical applications.

### 2. Timing Covert Channels
Two colluding processes—a Trojan transmitter in a high-security domain and an external receiver in an untrusted domain—communicate across security boundaries without violating memory access controls. The transmitter modulates packet arrival intervals $\Delta t \in \{t_0, t_1\}$ representing binary 0 and 1. The receiver measures packet delay variances across the shared router crossbar to decode the stream.

### 3. Denial-of-Service (DoS) and Protocol Deadlocks
By injecting packets that deliberately violate dimension-order routing rules or by asserting false credit tokens, an attacker can create cyclic buffer dependency knots in the Channel Dependency Graph (CDG), freezing the entire on-chip network.

---

## 11.3 Weighted Moving Average (WMA) Thermal Anomaly Detection

To detect thermal Trojans without heavy floating-point digital signal processors, **HeatSense** (TCAD 2026) develops an Exponentially Weighted Moving Average (EWMA) detector optimized for single-cycle standard-cell logic.

### Mathematical Formulation
Let $T_t$ be the raw digital temperature sensor reading at sample epoch $t$. The estimated baseline temperature $\mu_t$ and mean absolute deviation $D_t$ evolve according to:

$$\mu_t = \alpha T_t + (1 - \alpha) \mu_{t-1} = \mu_{t-1} + \alpha (T_t - \mu_{t-1})$$

$$D_t = \alpha |T_t - \mu_{t-1}| + (1 - \alpha) D_{t-1} = D_{t-1} + \alpha (|T_t - \mu_{t-1}| - D_{t-1})$$

To eliminate silicon multipliers, $\alpha$ is chosen as an inverse power of two ($\alpha = 2^{-S}$, where $S = 3 \implies \alpha = 1/8$). Multiplication by $\alpha$ reduces to a 3-bit arithmetic right shift (`>>> 3`).

An anomaly is flagged whenever the current thermal excursion exceeds a dynamic statistical boundary:

$$\text{Anomaly Alert} \iff |T_t - \mu_{t-1}| > K \cdot D_{t-1}$$

Choosing $K = 3$ corresponds to a $3\sigma$ confidence interval. In hardware, $3 \cdot D = (D \ll 1) + D$, requiring only a 1-bit left shift and a single adder!

```
      WMA Thermal Anomaly Detection Pipeline (Zero Multipliers)
      
      T_t ------> (+) -----------> [ >>> 3 ] ------> (+) ---------> μ_t (Mean)
                   ^                                  ^
                   |                                  |
                   +-- [-1] -- ( μ_{t-1} ) -----------+
                   
      |T_t - μ| -> (+) -----------> [ >>> 3 ] ------> (+) ---------> D_t (Dev)
                   ^                                  ^
                   |                                  |
                   +-- [-1] -- ( D_{t-1} ) -----------+
```

---

## 11.4 Intrinsic Physical Unclonable Functions (PUF) from Wire Delay Variations

Rather than storing cryptographic keys in vulnerable on-chip non-volatile memory (which can be probed using electron microscopy), **NoCiPUF** (TCAS-I 2025) leverages intrinsic manufacturing process variations in router crossbars:

1. **Sub-Nanosecond Path Mismatch:** No two silicon routers have identical wire parasitics ($RC$) and gate threshold voltages ($V_{th}$). A challenge pulse sent across symmetrical router paths results in race conditions at an SR latch arbiter.
2. **Challenge-Response Pair (CRP):** A 32-bit challenge word selects specific input-output port combinations. The winner of the arbiter race generates an unclonable output bit $R_i \in \{0, 1\}$.
3. **Zero-Overhead Authentication:** Before a chiplet accepts packets from an adjacent die, it exchanges a PUF-verified challenge token, immediately dropping forged packets injected by untrusted silicon.

---

## 11.5 Traffic Watermarking & Jitter Masking

To neutralize timing covert channels, routers implement **stochastic traffic jitter injection**:

```
Packet Arrival (T_in):      |||   ||   ||||  |   (Leaking AES Key via Delay Jitter)
                                   |
                                   v
Delay Jitter Mask (PRNG):    [ Fixed + Pseudo-Random Noise ]
                                   |
                                   v
Packet Departure (T_out):   |   |   |   |   |   (Constant Rate / Flattened Mutual Info)
```

By enforcing minimum flit departure intervals and injecting pseudo-random delays into virtual channel allocation, the mutual information $I(X; Y)$ between transmitter packet timing and receiver observations drops to near zero, eliminating cryptographic leakage without halting network traffic.

---

## 11.6 Synthesizable SystemVerilog Implementation

Below is the synthesizable SystemVerilog RTL for the lightweight WMA thermal anomaly detector ([`wma_thermal_detector.sv`](code/wma_thermal_detector.sv)):

```systemverilog
module wma_thermal_detector #(
    parameter DATA_WIDTH   = 16, // 8-bit integer, 8-bit fraction
    parameter ALPHA_SHIFT  = 3,  // alpha = 1/8
    parameter SIGMA_FACTOR = 3   // 3 * deviation threshold
)(
    input  wire                   clk,
    input  wire                   rst_n,
    input  wire                   sample_valid,
    input  wire [DATA_WIDTH-1:0]  raw_temp_sensor,
    
    output reg                    anomaly_alert,
    output reg                    quarantine_req,
    output reg  [DATA_WIDTH-1:0]  wma_mean,
    output reg  [DATA_WIDTH-1:0]  wma_deviation
);
    // Fixed-point shift-and-add logic (zero multipliers)
    // Full synthesizable RTL in code/wma_thermal_detector.sv
endmodule
```

Synthesizing this module on an open standard-cell library (e.g. Nangate45) consumes **under 180 NAND2-equivalent gates** and closes timing at **>2.5 GHz**, adding negligible area overhead (<0.5%) to a standard 5-port virtual-channel router.

---

## 11.7 Interactive Lab Challenge

Test your defensive reflexes against real-time Hardware Trojans and timing sniffers in our interactive client-side arcade:

👉 [**Launch Silicon Sentinel Arcade Game**](../../interactive/security.md)

- Monitor a $6\times 6$ router fabric in real time.
- Deploy WMA Anomaly Detection (`1`) to isolate overheating Trojan routers.
- Activate Jitter Masking (`2`) to disrupt cryptographic AES key exfiltration.
- Fire the PUF Authentication Shield (`Space`) to purge malicious packets and inscribe your high score on the Community Leaderboard!

---

## 11.8 Checkpoint Assessment

1. **Why is software payload encryption insufficient for securing Networks-on-Chip?**
   - *Answer:* Payload encryption leaves packet headers, routing tags, packet injection intervals, and thermal dissipation unencrypted, allowing attackers to mount timing covert channels, thermal Hardware Trojan attacks, and denial-of-service flooding. Furthermore, cryptographic encryption engines introduce prohibitive multi-cycle latency into sub-nanosecond router pipelines.
2. **How does the WMA thermal detector eliminate multipliers in hardware?**
   - *Answer:* By choosing the EWMA weighting coefficient $\alpha$ as a negative power of two ($\alpha = 2^{-S}$, e.g. $\alpha = 1/8$ with $S=3$), multiplication reduces to an arithmetic right shift (`>>> 3`). Similarly, multiplying the deviation by $K=3$ is computed via $(D \ll 1) + D$.
3. **What physical property is exploited by NoC-based PUFs?**
   - *Answer:* Sub-nanosecond propagation delay differences and threshold voltage variations across identically laid out crossbar wires and arbiter gates caused by deep-submicron manufacturing process variations.
