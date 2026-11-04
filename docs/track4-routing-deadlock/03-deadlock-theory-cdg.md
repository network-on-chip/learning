# 4.3 Formal Deadlock Theory & Duato's Escape Channels

In packet-switched and wormhole-switched interconnects, an unverified routing algorithm can lead to catastrophic failure: **Routing Deadlock**. 

Deadlock occurs when a set of packets hold network buffer resources while indefinitely waiting for other buffers held by each other in a closed dependency cycle. Once deadlock occurs, no packet in the cycle can ever advance. Buffer queues back up across the chip, freezing the entire processor and requiring a hard system reset.

To mathematically prove that an interconnect will never lock up under any conceivable traffic workload, computer architects rely on **Channel Dependency Graphs (CDGs)** and formal theorems developed by **William Dally, Charles Seitz, and José Duato**.

In this lesson, we examine the mathematical foundations of network deadlock, contrast the **Dally-Seitz Theorem** against **Duato's Escape Channel Theorem**, explore real-world silicon implementations, and simulate deadlock formation and escape in real time.

---

## 1. Formal Graph-Theoretic Foundations

Let an interconnection network be represented as a directed graph $I = G(N, C)$, where:
- $N$ is the set of router nodes (processing elements and switches).
- $C$ is the set of unidirectional communication channels (physical links or virtual channels).

A **Routing Function** $R: C \times N \rightarrow \mathcal{P}(C)$ maps the currently held channel $c_{curr}$ and destination node $d$ to a set of candidate next channels:
$$\{c_{next}\} = R(c_{curr}, d)$$

### The Waiting State and Deadlock Configuration
In a wormhole-routed network, a packet can span multiple routers simultaneously, holding buffer space in channel $c_i$ while its header flit requests channel $c_j$.

```
Deadlock Definition:
A non-empty set of packets P_deadlock = {p_1, p_2, ..., p_k} is deadlocked if and only if:
  - Packet p_1 holds Channel c_1 and waits for Channel c_2 (held by p_2)
  - Packet p_2 holds Channel c_2 and waits for Channel c_3 (held by p_3)
  ...
  - Packet p_k holds Channel c_k and waits for Channel c_1 (held by p_1)
```

Because every packet in $P_{deadlock}$ is waiting for a buffer that cannot be freed until another packet advances, **all $k$ packets are permanently frozen!**

---

## 2. The Channel Dependency Graph (CDG)

To analyze buffer dependencies independently of traffic, we construct the **Channel Dependency Graph (CDG)**, denoted $D = (C, E)$:
- **Vertices ($V = C$):** Every communication channel $c_i \in C$ in the network is a vertex in $D$.
- **Directed Edges ($(c_i, c_j) \in E$):** A directed edge from vertex $c_i$ to vertex $c_j$ exists if and only if a packet can transition directly from channel $c_i$ to channel $c_j$ under routing function $R$:
  $$(c_i, c_j) \in E \iff \exists d \in N \text{ such that } c_j \in R(c_i, d)$$

```mermaid
graph LR
  subgraph CDG_Cycle ["Directed Cycle in Channel Dependency Graph"]
    C0["Channel 0<br/>(Held by Pkt A)"] -->|Requests| C1["Channel 1<br/>(Held by Pkt B)"]
    C1 -->|Requests| C2["Channel 2<br/>(Held by Pkt C)"]
    C2 -->|Requests| C3["Channel 3<br/>(Held by Pkt D)"]
    C3 -->|Requests| C0
  end

  classDef cycleStyle fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b;
  class C0,C1,C2,C3 cycleStyle;
```

---

## 3. The Dally-Seitz Theorem (1987)

In their seminal 1987 paper, William J. Dally and Charles L. Seitz formulated the foundational theorem for deterministic routing:

> **Theorem (Dally & Seitz, 1987):**  
> A deterministic routing algorithm $R$ for an interconnection network is **deadlock-free if and only if** its Channel Dependency Graph $D$ contains **no directed cycles**.

### Mathematical Proof via Topological Ordering:
1. **Sufficiency ($\Leftarrow$):**  
   Suppose the CDG $D$ contains no directed cycles (it is a Directed Acyclic Graph, or DAG).  
   Every finite DAG possesses a **topological ordering**. We can assign a strictly increasing integer rank to each channel:
   $$\text{rank}: C \rightarrow \mathbb{N} \quad \text{such that } (c_i, c_j) \in E \implies \text{rank}(c_i) < \text{rank}(c_j)$$
   Suppose a circular deadlock exists among channels $c_1 \rightarrow c_2 \dots \rightarrow c_k \rightarrow c_1$.  
   Then by definition:
   $$\text{rank}(c_1) < \text{rank}(c_2) < \dots < \text{rank}(c_k) < \text{rank}(c_1) \implies \text{rank}(c_1) < \text{rank}(c_1)$$
   This is a mathematical contradiction! Therefore, no circular waiting chain can form.
2. **Necessity ($\Rightarrow$):**  
   If $D$ contains a directed cycle, one can construct a valid traffic sequence where $k$ packets simultaneously occupy the channels in the cycle, producing an active deadlock.

### Limitations of Dally-Seitz for Adaptive Routing:
The Dally-Seitz theorem is **necessary and sufficient ONLY for deterministic routing**.

For **adaptive routing**, the condition is overly conservative! An adaptive packet can wait for channel $c_1$, but if an alternative channel $c_2$ becomes available, it can take $c_2$. Therefore, **a cycle in the CDG does NOT necessarily cause deadlock in an adaptive network!**

Applying Dally-Seitz to adaptive networks creates "false negatives"—forbidding highly efficient, deadlock-free adaptive routes.

---

## 4. Duato's Theorem: Escape Channels (1993, 1997)

In 1993, Spanish computer scientist **José Duato** published a breakthrough theorem that revolutionized high-performance network design by introducing **Escape Virtual Channels**:

> **Duato's Theorem (1993, 1997):**  
> An adaptive routing function $R$ is **deadlock-free** if the set of virtual channels $C$ can be partitioned into two subsets:
> $$C = C_1 \cup C_0$$
> 1. An **Adaptive Channel Subnetwork ($C_1$):** Packets in $C_1$ can route fully adaptively across any legal path. Directed cycles **ARE PERMITTED** in $C_1$'s dependency graph!
> 2. An **Escape Channel Subnetwork ($C_0$):** Guaranteed to have an **acyclic** Channel Dependency Graph (e.g., using deterministic XY DOR).
> 
> Provided that:
> - $C_0$ provides a connected path between every source and destination.
> - Any packet traveling in $C_1$ can **always transition into $C_0$** whenever it encounters blocked buffers.
> - Once a packet enters $C_0$, it must strictly obey $C_0$'s acyclic routing function.

```mermaid
graph TD
  subgraph Duato_Architecture ["Duato's Escape Virtual Channel Architecture"]
    Flit["Arriving Packet Flit"] --> Arbiter{"Adaptive VC Available?"}
    
    subgraph Adaptive_Plane ["Adaptive Subnetwork (C1: VC 1, VC 2)"]
      Arbiter -->|Yes (Normal Path)| C1_Route["Fully Adaptive Routing<br/>(Allows Cycles & Congestion Bypass)"]
    end

    subgraph Escape_Plane ["Escape Subnetwork (C0: VC 0)"]
      Arbiter -->|Blocked / Congested| C0_Route["Deterministic XY Routing<br/>(Strictly Acyclic CDG)"]
      C1_Route -. Hotspot Stalls .-> C0_Route
    end
  end

  classDef adaptStyle fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#166534;
  classDef escapeStyle fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px,color:#1e3a8a;

  class C1_Route adaptStyle;
  class C0_Route escapeStyle;
```

### Why Duato's Architecture is Impervious to Deadlock:
1. **Under Normal Load:** Over $95\%$ of packets traverse the high-speed adaptive channels in $C_1$, dynamically weaving around memory hotspots and heavy cache lines.
2. **When Deadlock Threatens in $C_1$:** If packets in $C_1$ ever form a circular waiting cycle, they do not freeze! As their buffer queues fill up, the blocked packets simply request the **Escape Virtual Channel ($C_0$)**.
3. **Guaranteed Drain:** Because $C_0$'s Channel Dependency Graph is strictly acyclic, the packet with the highest topological rank in $C_0$ is **guaranteed to reach its destination and exit the network**. Once it leaves, the next packet advances. By induction, **$C_0$ continuously drains flits out of the network**, breaking any potential deadlock!

---

## 5. Silicon Case Studies: Escape Channels in Commercial Routers

Where is Duato's escape channel architecture implemented in real hardware?

### 1. Cray T3E & Alpha 21364 (EV7)
The iconic DEC Alpha 21364 processor integrated an on-chip network router connecting 128 Alpha CPUs into a 2D Torus:
- **Virtual Channels:** 3 VCs per physical link.
- **Allocation:** $VC_1$ and $VC_2$ were configured as adaptive channels (allowing arbitrary non-minimal turns to evade failed chips).
- **Escape Channel:** $VC_0$ enforced strict dimension-order routing (DOR) with dateline virtual channel switching, serving as the Duato escape path.

### 2. Modern Server & AI Fabrics (Cray Slingshot / Intel Xeon)
In modern exascale clusters, switches like HPE/Cray Slingshot and Intel Ultra Path Interconnect (UPI) utilize dedicated escape virtual lanes ($VL_0$) to guarantee forward progress during heavy all-to-all collective communications.

---

## 6. 🔬 Interactive CDG Deadlock Simulator & Escape Channel Flusher

Experience how circular dependencies form and how Duato's escape virtual channels instantly drain deadlocked packets:

<div class="noc-sim-container" id="cdg-sim">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:1rem;">
    <div style="font-weight:700; font-size:1.05rem; color:var(--tcl-heading);">
      ⚡ CDG Cycle Simulator &amp; Duato Escape Channel Flusher
    </div>
    <span class="noc-track-badge" style="background:rgba(239,68,68,0.1); color:#ef4444;" id="cdg_status_badge">
      Normal Operation
    </span>
  </div>

  <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:1rem;">
    <button class="noc-sim-btn" style="background:#ef4444;" onclick="triggerDeadlock()">
      ⚠️ Inject Circular Contention (Cause Deadlock)
    </button>
    <button class="noc-sim-btn" style="background:#22c55e;" onclick="activateEscapeChannel()">
      🛡️ Activate Duato Escape Channel (C0)
    </button>
    <button class="noc-sim-btn" style="background:var(--md-default-fg-color--lightest); color:var(--md-default-fg-color); border:1px solid var(--tcl-border);" onclick="resetCDGSim()">
      🔄 Reset
    </button>
  </div>

  <div style="display:flex; gap:1.25rem; flex-wrap:wrap; align-items:flex-start;">
    <div style="flex:1; min-width:280px; text-align:center;">
      <canvas id="cdgCanvas" width="340" height="340" style="background:#0f172a; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.25); max-width:100%; height:auto;"></canvas>
    </div>

    <div style="flex:1.2; min-width:280px;">
      <div style="background:var(--md-default-fg-color--lightest); border:1px solid var(--tcl-border); border-radius:8px; padding:0.85rem; font-size:0.85rem; margin-bottom:0.75rem;">
        <div style="font-weight:700; color:var(--tcl-heading); margin-bottom:0.4rem;">📊 Channel Dependency State:</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.4rem;">
          <div>Active Channels: <strong id="cdg_chans">4 Channels</strong></div>
          <div>Cycle Status: <strong id="cdg_cycle" style="color:#22c55e;">Acyclic (Free)</strong></div>
          <div>Adaptive VCs (C1): <strong id="cdg_c1_state">Idle</strong></div>
          <div>Escape VC (C0): <strong id="cdg_c0_state" style="color:#38bdf8;">Standby</strong></div>
        </div>
      </div>

      <div style="background:var(--md-default-fg-color--lightest); border:1px solid var(--tcl-border); border-radius:8px; padding:0.85rem; font-size:0.82rem;">
        <div style="font-weight:700; color:var(--tcl-heading); margin-bottom:0.4rem;">🔍 Dependency Monitor:</div>
        <div id="cdg_log" style="font-family:monospace; height:130px; overflow-y:auto; line-height:1.5; color:var(--md-default-fg-color--lighter);">
          <span style="color:#22c55e;">[READY] Interconnect operating normally. Buffers have capacity.</span>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
const cdgState = {
  isDeadlocked: false,
  isEscaping: false,
  stepCount: 0,
  flits: [
    { id: "A", curr: 0, next: 1, color: "#ef4444", state: "normal" },
    { id: "B", curr: 1, next: 2, color: "#f97316", state: "normal" },
    { id: "C", curr: 2, next: 3, color: "#eab308", state: "normal" },
    { id: "D", curr: 3, next: 0, color: "#a855f7", state: "normal" }
  ]
};

function triggerDeadlock() {
  cdgState.isDeadlocked = true;
  cdgState.isEscaping = false;

  const badge = document.getElementById("cdg_status_badge");
  badge.textContent = "CRITICAL: DEADLOCK DETECTED";
  badge.style.background = "rgba(239,68,68,0.2)";
  badge.style.color = "#ef4444";

  document.getElementById("cdg_cycle").innerHTML = "<span style='color:#ef4444;'>CLOSED DIRECTED CYCLE!</span>";
  document.getElementById("cdg_c1_state").innerHTML = "<span style='color:#ef4444;'>100% Full (Blocked)</span>";

  const log = document.getElementById("cdg_log");
  log.innerHTML = `
    <span style="color:#ef4444; font-weight:bold;">[DEADLOCK DETECTED]</span><br/>
    - Pkt A holds Chan 0 ➔ waiting for Chan 1 (held by Pkt B)<br/>
    - Pkt B holds Chan 1 ➔ waiting for Chan 2 (held by Pkt C)<br/>
    - Pkt C holds Chan 2 ➔ waiting for Chan 3 (held by Pkt D)<br/>
    - Pkt D holds Chan 3 ➔ waiting for Chan 0 (held by Pkt A)<br/>
    <span style="color:#ef4444;">All 4 packets are frozen indefinitely!</span>
  `;

  drawCDGCanvas();
}

function activateEscapeChannel() {
  if (!cdgState.isDeadlocked) return;
  cdgState.isEscaping = true;

  const badge = document.getElementById("cdg_status_badge");
  badge.textContent = "DRAINING VIA DUATO ESCAPE CHANNEL (C0)";
  badge.style.background = "rgba(34,197,94,0.2)";
  badge.style.color = "#22c55e";

  document.getElementById("cdg_cycle").innerHTML = "<span style='color:#22c55e;'>Cycle Broken via C0</span>";
  document.getElementById("cdg_c0_state").innerHTML = "<span style='color:#22c55e; font-weight:bold;'>Active Draining</span>";

  const log = document.getElementById("cdg_log");
  log.innerHTML += `
    <br/><span style="color:#22c55e; font-weight:bold;">[DUATO RECOVERY ACTIVE]</span><br/>
    - Packet D falls back into acyclic Escape Virtual Channel (C0).<br/>
    - C0 has no cycles: Packet D drains into local memory core!<br/>
    - Channel 3 buffer is freed ➔ Packet C advances!<br/>
    - Channel 2 buffer is freed ➔ Packet B advances!<br/>
    - Channel 1 buffer is freed ➔ Packet A advances!<br/>
    <span style="color:#22c55e;">Interconnect completely recovered. Forward progress restored!</span>
  `;
  log.scrollTop = log.scrollHeight;

  drawCDGCanvas();
}

function resetCDGSim() {
  cdgState.isDeadlocked = false;
  cdgState.isEscaping = false;

  const badge = document.getElementById("cdg_status_badge");
  badge.textContent = "Normal Operation";
  badge.style.background = "rgba(34,197,94,0.1)";
  badge.style.color = "#22c55e";

  document.getElementById("cdg_cycle").innerHTML = "<span style='color:#22c55e;'>Acyclic (Free)</span>";
  document.getElementById("cdg_c1_state").textContent = "Idle";
  document.getElementById("cdg_c0_state").textContent = "Standby";

  document.getElementById("cdg_log").innerHTML = `<span style="color:#22c55e;">[READY] Interconnect operating normally. Buffers have capacity.</span>`;

  drawCDGCanvas();
}

function drawCDGCanvas() {
  const canvas = document.getElementById("cdgCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  const cx = w / 2;
  const cy = h / 2;
  const r = 100;

  const nodes = [
    { x: cx, y: cy - r, label: "R0 (Chan 0)" },
    { x: cx + r, y: cy, label: "R1 (Chan 1)" },
    { x: cx, y: cy + r, label: "R2 (Chan 2)" },
    { x: cx - r, y: cy, label: "R3 (Chan 3)" }
  ];

  // Draw Channels
  for (let i = 0; i < 4; i++) {
    const nextIdx = (i + 1) % 4;
    const n1 = nodes[i];
    const n2 = nodes[nextIdx];

    ctx.beginPath();
    ctx.moveTo(n1.x, n1.y);
    ctx.lineTo(n2.x, n2.y);

    if (cdgState.isDeadlocked && !cdgState.isEscaping) {
      ctx.strokeStyle = "#ef4444";
      ctx.lineWidth = 4;
    } else if (cdgState.isEscaping) {
      ctx.strokeStyle = (i === 3) ? "#22c55e" : "#38bdf8";
      ctx.lineWidth = (i === 3) ? 5 : 3;
    } else {
      ctx.strokeStyle = "#334155";
      ctx.lineWidth = 2;
    }
    ctx.stroke();
  }

  // Draw Nodes
  for (let i = 0; i < 4; i++) {
    const n = nodes[i];

    ctx.beginPath();
    ctx.arc(n.x, n.y, 22, 0, Math.PI * 2);

    if (cdgState.isDeadlocked && !cdgState.isEscaping) {
      ctx.fillStyle = "#7f1d1d";
      ctx.strokeStyle = "#ef4444";
    } else if (cdgState.isEscaping && i === 3) {
      ctx.fillStyle = "#14532d";
      ctx.strokeStyle = "#22c55e";
    } else {
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = "#38bdf8";
    }
    ctx.lineWidth = 2.5;
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 9px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(`R${i}`, n.x, n.y - 4);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "7.5px monospace";
    ctx.fillText(`C${i}`, n.x, n.y + 7);
  }

  // Draw Center Deadlock / Escape Badge
  ctx.beginPath();
  ctx.arc(cx, cy, 32, 0, Math.PI * 2);
  if (cdgState.isDeadlocked && !cdgState.isEscaping) {
    ctx.fillStyle = "rgba(239, 68, 68, 0.2)";
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2;
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#ef4444";
    ctx.font = "bold 10px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("CYCLE!", cx, cy);
  } else if (cdgState.isEscaping) {
    ctx.fillStyle = "rgba(34, 197, 94, 0.2)";
    ctx.strokeStyle = "#22c55e";
    ctx.lineWidth = 2;
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#22c55e";
    ctx.font = "bold 9px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("C0 DRAIN", cx, cy);
  } else {
    ctx.fillStyle = "rgba(56, 189, 248, 0.1)";
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 1.5;
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 9px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("FREE", cx, cy);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", drawCDGCanvas);
} else {
  drawCDGCanvas();
}
</script>

---

## 7. Worked Numerical Example: Verifying Duato's Theorem

> [!TIP]
> **Problem Statement:**  
> A system architect is designing a 2D Torus interconnect ($4 \times 4$).  
> Because a Torus has physical wrap-around channels, even deterministic XY routing contains cycles in each ring dimension (e.g. $0 \rightarrow 1 \rightarrow 2 \rightarrow 3 \rightarrow 0$).  
> 
> The architect equips each physical link with **3 Virtual Channels**: $VC_0, VC_1, VC_2$.  
> - Packets can use $VC_1$ and $VC_2$ with fully adaptive, non-minimal routing.
> - $VC_0$ is restricted to deterministic dimension-order routing using **Dateline Virtual Channel Switching** (packets switch from $VC_0A$ to $VC_0B$ when crossing the wrap-around link).
> 
> Verify whether this interconnect satisfies Duato's Conditions for deadlock freedom.

### Verification of Duato's 3 Conditions:

1. **Subnetwork Partitioning:**
   $$C = C_1 \cup C_0, \quad \text{where } C_1 = \{VC_1, VC_2\} \text{ and } C_0 = \{VC_0\}$$
   - $C_1$ allows cycles (adaptive plane).
   - $C_0$ uses dateline splitting, which splits the circular ring into a monotonically ranked linear chain ($VC_0A < VC_0B$).
   - Therefore, the Channel Dependency Graph of $C_0$ is **strictly acyclic**! (Condition 1 Satisfied ✔)

2. **Full Connectivity of Escape Subnetwork ($C_0$):**
   - Does $C_0$ provide a legal path between every node pair $(s, d)$?
   - Yes: Dimension-Order Routing with dateline splitting connects every source to every destination in the $4 \times 4$ Torus. (Condition 2 Satisfied ✔)

3. **Guaranteed Transition to Escape Path:**
   - A packet in $C_1$ that finds all adaptive buffers blocked can always request $VC_0$.
   - Once a packet enters $VC_0$, it is forbidden from ever jumping back into $C_1$.
   - Because $C_0$ is acyclic, it continuously drains flits out of the network, preventing any permanent starvation. (Condition 3 Satisfied ✔)

### Conclusion:
The architecture strictly satisfies Duato's Theorem and is **provably deadlock-free**, despite allowing arbitrary non-minimal adaptive routing in $VC_1$ and $VC_2$!

---

## 8. 🎯 Knowledge Check: Lesson 4.3

<div class="noc-sim-container" id="quiz43" style="margin-top:1rem;">
  <div style="font-weight:700; font-size:1.05rem; margin-bottom:1rem; color:var(--tcl-heading);">
    📝 Concept Check: Deadlock Theory &amp; Duato's Theorem
  </div>

  <div id="q43_block">
    <p style="font-weight:600; font-size:0.95rem; margin-bottom:0.75rem;">
      <b>Question:</b> Why does the Dally-Seitz theorem fail to accurately classify deadlock freedom in adaptive routing algorithms?
    </p>

    <div style="display:flex; flex-direction:column; gap:0.5rem;" id="q43_options">
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz43(0)">
        A. Because the Dally-Seitz theorem only applies to circuit-switched networks.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz43(1)">
        B. Because Dally-Seitz requires an acyclic Channel Dependency Graph (CDG). In an adaptive network, a CDG may contain cycles, but packets can adaptively choose alternative non-blocked channels, meaning cycles do not necessarily cause deadlock.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz43(2)">
        C. Because Dally-Seitz does not account for packet serialization delay.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz43(3)">
        D. Because adaptive routers cannot implement Virtual Channels.
      </button>
    </div>

    <div id="q43_feedback" style="display:none; margin-top:1rem; padding:0.85rem; border-radius:8px; font-size:0.9rem; line-height:1.5;"></div>
  </div>
</div>

<script>
function checkQuiz43(idx) {
  const fb = document.getElementById("q43_feedback");
  fb.style.display = "block";
  const opts = document.getElementById("q43_options").children;
  for (let i = 0; i < opts.length; i++) {
    opts[i].onclick = null;
    opts[i].style.cursor = "default";
  }

  if (idx === 1) {
    opts[1].style.background = "rgba(34,197,94,0.15)";
    opts[1].style.borderColor = "#22c55e";
    fb.style.background = "rgba(34,197,94,0.1)";
    fb.style.border = "1px solid rgba(34,197,94,0.3)";
    fb.style.color = "#166534";
    fb.innerHTML = "<strong>✓ Correct!</strong> Dally-Seitz provides a necessary and sufficient condition only for deterministic routing. In adaptive networks, packets have path choices; thus, cyclic dependencies do not automatically imply that packets are permanently stuck.";
  } else {
    opts[idx].style.background = "rgba(239,68,68,0.15)";
    opts[idx].style.borderColor = "#ef4444";
    opts[1].style.background = "rgba(34,197,94,0.15)";
    opts[1].style.borderColor = "#22c55e";
    fb.style.background = "rgba(239,68,68,0.1)";
    fb.style.border = "1px solid rgba(239,68,68,0.3)";
    fb.style.color = "#991b1b";
    fb.innerHTML = "<strong>✗ Incorrect.</strong> The correct answer is <strong>B</strong>. Dally-Seitz produces false negatives on adaptive routing because alternative paths can drain flits even if a cycle exists.";
  }
}
</script>

---

## Summary & Next Steps

In this lesson, we established:
- **Channel Dependency Graphs (CDGs):** Modeling routing functions as directed graphs of channel resources.
- **The Dally-Seitz Theorem:** Necessary and sufficient proof of deadlock freedom for deterministic routing via topological ordering.
- **Duato's Theorem:** Decoupling adaptivity from deadlock freedom by partitioning channels into an adaptive plane ($C_1$) and an acyclic escape plane ($C_0$).
- **Silicon Microarchitecture:** How Alpha EV7, Cray T3E, and modern server fabrics implement escape virtual channels.

However, even if our physical routing algorithm is provably deadlock-free, a chip can STILL freeze due to **Cache Coherence Protocol Deadlock** or physical link failures! 

In our final lesson of Track 4, we explore **Fault-Tolerant Routing & Protocol Deadlock Avoidance**.

👉 **Proceed to [Lesson 4.4: Fault-Tolerant Routing & Protocol Deadlock](04-fault-tolerant-protocol-deadlock.md)**
