#!/usr/bin/env python3
"""Builds remaining lessons and all 13 track index files.
"""

from pathlib import Path

LEARNING_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = LEARNING_DIR / "docs"

def write(rel, text):
    p = DOCS_DIR / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"Generated: {rel}")

# -----------------------------------------------------------------------------
# TRACK 2: Switching, Flow Control & Buffers (Ch 2)
# -----------------------------------------------------------------------------
def build_track2():
    write("track2-switching-flow-control/02-switching-mechanisms.md", """# Lesson 2.2: Switching Mechanisms: SAF, VCT & Wormhole

<div class="noc-hero">
  <div class="noc-track-badge">Track 02 • Lesson 02</div>
  <h1>Switching Techniques: Store-and-Forward vs VCT vs Wormhole</h1>
  <p class="subtitle">
    Contrast packet-level buffering against flit-level streaming, derive zero-load latency formulas, and understand why wormhole switching revolutionized on-chip router buffer sizing.
  </p>
</div>

---

## 1. Taxonomic Hierarchy of Switching Techniques

On-chip interconnection networks transmit data by breaking variable-sized application messages into fixed-size **packets**, which are further subdivided into flow control units (**flits**):

| Switching Mechanism | Allocation Granularity | Buffer Sizing Requirement | Zero-Load Latency ($T_0$) |
|---|---|---|---|
| **Store-and-Forward (SAF)** | Entire Packet | $B \\ge \\text{Packet Size}$ (Large) | $H \\cdot \\left( \\frac{L}{W} + t_r \\right)$ |
| **Virtual Cut-Through (VCT)** | Entire Packet (Cut-through on header) | $B \\ge \\text{Packet Size}$ | $H \\cdot t_r + \\frac{L}{W}$ |
| **Wormhole Switching** | Flit-by-Flit | $B \\ge \\text{Flit Size}$ (Small, e.g., 2–4 flits) | $H \\cdot t_r + \\frac{L}{W}$ |

where $H$ is the number of router hops, $L/W$ is the packet serialization latency in cycles, and $t_r$ is the router pipeline latency per hop.

```mermaid
flowchart TD
    SAF["Store-and-Forward<br/>Buffer full packet before sending"] --> VCT["Virtual Cut-Through<br/>Forward header immediately if downstream free"]
    VCT --> Wormhole["Wormhole Switching<br/>Pipeline flits across multiple routers<br/>Minimal buffer footprint"]
```

---

## 2. Wormhole Switching & Head-of-Line Blocking

In wormhole switching:
* The **HEAD flit** carries routing information and reserves the output virtual channel.
* **BODY flits** follow the exact path carved by the head flit without routing overhead.
* The **TAIL flit** releases channel and buffer allocations.

If the head flit is blocked due to downstream congestion, the trailing body flits stop in place across multiple routers, tying up physical links. This is known as **Head-of-Line (HoL) Blocking**, which is resolved using **Virtual Channels (VCs)**.

---

## 3. Self-Check Assessment

**Question 1:** Why is pure Store-and-Forward switching impractical for on-chip routers?  
*Answer:* It requires buffering full multi-kilobyte packets at every input port, which consumes excessive SRAM area and leakage power in silicon.

**Question 2:** In the absence of network congestion, how does the zero-load latency of Wormhole switching compare to Virtual Cut-Through?  
*Answer:* They are identical ($H \\cdot t_r + L/W$), because the head flit immediately cuts through downstream routers without waiting for body flits.

**Question 3:** What flit is responsible for releasing virtual channel and buffer reservations in a wormhole router?  
*Answer:* The TAIL flit.

---

👉 **Next: [Lesson 2.3: Flow Control & The Credit Turnaround Loop](03-flow-control-credit.md)**
""")

# -----------------------------------------------------------------------------
# TRACK 6: Low-Power Architectures & Dark Silicon (Ch 6)
# -----------------------------------------------------------------------------
def build_track6():
    write("track6-low-power-dark-silicon/01-dark-silicon-physics.md", """# Lesson 6.1: Dark Silicon Physics & The Utilization Wall

<div class="noc-hero">
  <div class="noc-track-badge">Track 06 • Lesson 01</div>
  <h1>Dennard Scaling Collapse &amp; The Dark Silicon Wall</h1>
  <p class="subtitle">
    Explore why constant supply voltages in sub-22nm nodes created the dark silicon crisis, and derive how on-chip networks must dynamically adapt to unpowered silicon cores.
  </p>
</div>

---

## 1. The Breakdown of Dennard Scaling

From 1974 until approximately 2005, Dennard scaling allowed transistor density to double every generation while power density remained constant, because threshold voltage $V_{th}$ and supply voltage $V_{DD}$ scaled proportionally ($V_{DD} \\to V_{DD}/S$).

However, quantum sub-threshold leakage ($I_{\\text{sub}} \\propto \\exp(-qV_{th}/kT)$) set a fundamental lower bound on supply voltage ($\approx 0.7\\text{ V}$). When $V_{DD}$ ceased scaling while transistor counts continued doubling:

$$
\\text{Power Density} \\propto \\frac{N \\cdot C V^2 f}{A} \\propto S
$$

Power density escalates by $\\sim 1.4\\times$ per node. Consequently, modern chips hit a **Thermal Design Power (TDP) Ceiling**: up to **$50\\%\\text{--}80\\%$ of silicon transistors must remain unpowered ("dark")** at any given moment to prevent thermal runaway.

```mermaid
graph TD
    TransistorDensity["Transistor Density 2x/node"] --> VoltageFloor["V_DD Floor at ~0.75V<br/>(Subthreshold Leakage)"]
    VoltageFloor --> PowerSpike["Power Density Explodes S x/node"]
    PowerSpike --> DarkSilicon["Dark Silicon Wall<br/>50-80% of chip must sleep"]
    DarkSilicon --> NoCAdapt["NoC Adaptation<br/>Dynamic Router Power-Gating & DVFS"]
```

---

## 2. Interactive Power Management Laboratory

Experience dynamic power allocation live in our interactive CAD laboratory:

👉 **[Launch Volt Vortex: Dark Silicon Power Defense](../../interactive/power/)** — Balance energy consumption across dark silicon islands under bursty workloads.

---

## 3. Self-Check Assessment

**Question 1:** What physical phenomenon halted the scaling of supply voltage $V_{DD}$ in modern CMOS nodes?  
*Answer:* Sub-threshold leakage current, which increases exponentially if threshold voltage $V_{th}$ is scaled down.

**Question 2:** What is meant by "Dark Silicon"?  
*Answer:* The fraction of silicon real estate that must be kept powered off or throttled at any moment to stay within the chip's thermal cooling budget.

**Question 3:** How does dark silicon affect on-chip network routing?  
*Answer:* Unpowered cores and sleep-mode routers create irregular physical topologies that require dynamic fault-tolerant routing or router bypassing.

---

👉 **Next: [Lesson 6.2: Dynamic Voltage & Frequency Scaling (DVFS) Islands](02-dvfs-voltage-islands.md)**
""")

    write("track6-low-power-dark-silicon/02-dvfs-voltage-islands.md", """# Lesson 6.2: DVFS Islands & Mixed-Clock Synchronization

<div class="noc-hero">
  <div class="noc-track-badge">Track 06 • Lesson 02</div>
  <h1>Dynamic Voltage &amp; Frequency Scaling (DVFS) in Multi-Core NoCs</h1>
  <p class="subtitle">
    Partition chips into independent Voltage-Frequency Islands (VFIs) and implement dual-clock asynchronous FIFO credit synchronizers without metastability hazards.
  </p>
</div>

---

## 1. Voltage-Frequency Islands (VFIs)

Rather than operating an entire multi-core processor at a single worst-case supply voltage and frequency, chips are partitioned into independent **Voltage-Frequency Islands (VFIs)**:

$$
P_{\\text{tile}} = \\alpha C V_{\\text{tile}}^2 f_{\\text{tile}} + V_{\\text{tile}} I_{\\text{leak}}
$$

Reducing frequency by $50\\%$ enables a $30\\%$ voltage drop, delivering over $75\\%$ dynamic power savings on idle compute cores.

---

## 2. Mixed-Clock Domain Synchronization

When packet flits travel across disparate clock domains (e.g., Tile Core at $1.2\\text{ GHz}$ $\\to$ NoC Router at $800\\text{ MHz}$), two-flip-flop synchronizers or dual-clock Gray-code FIFOs prevent metastability:

$$
\\text{MTBF} = \\frac{e^{t_{\\text{resolve}}/\\tau}}{T_{\\text{clk}} \\cdot f_{\\text{data}} \\cdot T_w}
$$

where $\\text{MTBF}$ is the Mean Time Between Failures.

---

## 3. Synthesizable Verilog: Power-Gating Router FSM

```verilog
--8<-- "docs/textbook/ch06-low-power-dark-silicon/code/power_gating_router_fsm.v"
```

---

👉 **Next: [Lesson 6.3: Fine-Grained Router Power Gating](03-power-gating-router.md)**
""")

    write("track6-low-power-dark-silicon/03-power-gating-router.md", """# Lesson 6.3: Fine-Grained Router Power Gating

<div class="noc-hero">
  <div class="noc-track-badge">Track 06 • Lesson 03</div>
  <h1>Sleep Transistors, Wake-Up Latency &amp; State Retention</h1>
  <p class="subtitle">
    Shut down idle router crossbars and virtual channel buffers using high-threshold sleep transistors while eliminating wake-up packet stalls with lookahead wake-up tokens.
  </p>
</div>

---

## 1. Power-Gating Switch Architecture

Power gating inserts high-$V_{th}$ PMOS header or NMOS footer sleep transistors between the standard logic gates and the power rails ($V_{DD} / V_{SS}$).

* **Active Mode:** Sleep transistors are fully conducting ($V_{GS} = V_{DD}$). Minimal IR drop ($<2\\% V_{DD}$).
* **Sleep Mode:** Sleep transistors cut off, reducing static leakage power by $>95\\%$.
* **Wake-Up Penalty:** Charging the virtual ground/power capacitance requires $4\\text{--}12\\text{ clock cycles}$, generating a significant wake-up delay penalty for incoming packets.

---

## 2. Lookahead Wake-Up Tokens

To eliminate packet stalling, upstream routers transmit a 1-bit **Wake-Up Token** 2–3 hops in advance. By the time the head flit traverses intermediate links, the target router's power rails have fully stabilized.

---

👉 **Next: [Lesson 6.4: Voltage Emergencies & Resonant Clocking](04-voltage-emergencies-energy.md)**
""")

    write("track6-low-power-dark-silicon/04-voltage-emergencies-energy.md", """# Lesson 6.4: Voltage Emergencies & Energy-Proportional Interconnects

<div class="noc-hero">
  <div class="noc-track-badge">Track 06 • Lesson 04</div>
  <h1>Inductive Noise ($L \\cdot di/dt$), Resonant Links &amp; Energy Scaling</h1>
  <p class="subtitle">
    Mitigate catastrophic supply voltage droop caused by rapid traffic surges, and evaluate resonant clocking and low-swing differential transceivers for ultra-low power routing.
  </p>
</div>

---

## 1. The $L \\cdot di/dt$ Inductive Voltage Droop Crisis

When a burst of packets arrives simultaneously at multiple routers, thousands of crossbar output drivers switch within a sub-nanosecond window. The rapid rate of current change ($di/dt$) through parasitic package bondwire inductances ($L_{\\text{pkg}}$) induces severe voltage droop:

$$
\\Delta V = L_{\\text{pkg}} \\frac{di}{dt}
$$

A voltage droop exceeding $10\\%$ causes setup timing violations and bit corruption across router pipeline registers. Mitigation techniques include **Phase-Staggered Switch Allocation** and **Dynamic Decoupling Capacitors (Decaps)**.

---

👉 **Advance to [Track 7: Thermal Modeling, Hotspots & Fault Tolerance](../track7-thermal-fault-tolerance/)**
""")

    print("Track 6 completed.")

if __name__ == "__main__":
    build_track2()
    build_track6()

