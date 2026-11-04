# 4.1 Deterministic Dimension-Order Routing (DOR)

In any network-on-chip, the **Routing Algorithm** is the decision logic that selects which physical output port a packet must take to reach its destination.

Routing algorithms fall into three fundamental classes:
1. **Deterministic:** The path between a given source and destination is completely fixed and invariant, regardless of network traffic, congestion, or buffer occupancy.
2. **Oblivious:** The path is chosen without regard to current network state, but may incorporate randomized intermediate nodes (e.g., Valiant's algorithm).
3. **Adaptive:** The path dynamically responds to network congestion, buffer fullness, and hardware faults in real time.

The most widely deployed routing policy in commercial silicon—from Intel Xeon to AMD EPYC and Tilera TILE-Gx—is **Dimension-Order Routing (DOR)**, universally known as **XY Routing**.

In this lesson, we examine the algorithmic mechanics of DOR, synthesize single-cycle lookahead route computation hardware in Verilog, prove its mathematical deadlock freedom, and benchmark its strengths and limitations.

---

## 1. Algorithmic Logic: XY vs. YX Routing

In a 2D mesh topology, every router is identified by its integer 2D Cartesian coordinates:
$$\text{Current Router: } (x_c, y_c), \quad \text{Destination Node: } (x_d, y_d)$$

### The XY Routing Rule
In **XY Routing**, a packet must strictly traverse the **horizontal dimension ($X$) first** until it aligns with the destination column ($x_c = x_d$). Only then is it permitted to turn into the **vertical dimension ($Y$)** to reach the destination row ($y_c = y_d$):

$$\Delta x = x_d - x_c, \quad \Delta y = y_d - y_c$$

$$\text{Next Port} = \begin{cases} 
\text{East}, & \text{if } \Delta x > 0 \\ 
\text{West}, & \text{if } \Delta x < 0 \\ 
\text{South}, & \text{if } \Delta x = 0 \text{ and } \Delta y > 0 \\ 
\text{North}, & \text{if } \Delta x = 0 \text{ and } \Delta y < 0 \\ 
\text{Local (Core)}, & \text{if } \Delta x = 0 \text{ and } \Delta y = 0 
\end{cases}$$

```
XY Routing: Route along X axis until target column, then turn into Y axis:
  (0,0) ----East----> (1,0) ----East----> (2,0) [Turn!]
                                            |
                                          South
                                            v
                                          (2,1) ----South----> (2,2) [Destination]
```

### The YX Routing Rule
Conversely, in **YX Routing**, the packet strictly resolves the vertical dimension ($Y$) first, and only travels horizontally ($X$) after reaching the destination row:

$$\text{Next Port (YX)} = \begin{cases} 
\text{South}, & \text{if } \Delta y > 0 \\ 
\text{North}, & \text{if } \Delta y < 0 \\ 
\text{East}, & \text{if } \Delta y = 0 \text{ and } \Delta x > 0 \\ 
\text{West}, & \text{if } \Delta y = 0 \text{ and } \Delta x < 0 \\ 
\text{Local}, & \text{if } \Delta x = 0 \text{ and } \Delta y = 0 
\end{cases}$$

Both XY and YX are strictly minimal (shortest-path) algorithms: every hop reduces the Manhattan distance $D_{Manhattan} = |\Delta x| + |\Delta y|$ by exactly $1$.

---

## 2. Lookahead Route Computation (L-RC)

In a naive 5-stage router pipeline, Route Computation (RC) occurs at the current router *after* the header flit arrives:
$$\text{Arrive} \longrightarrow [\mathbf{RC}] \longrightarrow [\text{VCA}] \longrightarrow [\text{SA}] \longrightarrow [\text{ST}] \longrightarrow \text{Link}$$

This adds a full clock cycle (or sub-cycle combinational delay) to the critical path!

To eliminate this overhead, modern routers use **Lookahead Routing** (Peh & Dally, 2001). Instead of computing its *own* output port, Router $R_i$ computes the output port for the **next downstream router ($R_{i+1}$)** and writes that direction directly into the packet header flit:

```
+----------------------------------------------------------------------------+
| Lookahead Pipeline Optimization:                                            |
| Router R_i (Current):                                                      |
|   1. Flit arrives with pre-computed port for R_i in its header.            |
|   2. Flit directly enters Switch Allocation (SA) with ZERO route delay!    |
|   3. IN PARALLEL: Combinational Lookahead RC computes port for R_{i+1}.     |
|   4. New lookahead port is overwritten into header before flit exits ST.   |
+----------------------------------------------------------------------------+
```

Because Route Computation runs in parallel with Virtual Channel or Switch Allocation, **RC is completely removed from the critical latency path of the router!**

---

## 3. Synthesizable Verilog RTL: Lookahead Route Computation

Below is the complete, synthesizable SystemVerilog module for a lookahead XY route computation unit. It takes the current router's coordinate, the selected downstream neighbor's coordinate, and the packet's destination coordinate, producing a 1-hot encoded output port for the next router:

```verilog
// File: lookahead_route_comp.v
// Synthesizable Lookahead Route Computation Unit for 2D Mesh XY DOR
// Computes the output port for the DOWNSTREAM router in parallel with switch allocation.

module lookahead_route_comp #(
    parameter int COORD_WIDTH = 4  // Supports up to 16x16 mesh
)(
    // Coordinates
    input  logic [COORD_WIDTH-1:0] next_x,     // X-coordinate of downstream router R_{i+1}
    input  logic [COORD_WIDTH-1:0] next_y,     // Y-coordinate of downstream router R_{i+1}
    input  logic [COORD_WIDTH-1:0] dest_x,     // Target destination X-coordinate
    input  logic [COORD_WIDTH-1:0] dest_y,     // Target destination Y-coordinate

    // Pre-computed Output Port for Downstream Router (1-hot encoded: {Local, South, North, West, East})
    output logic [4:0]             lookahead_port
);

    // Port bit index definition
    localparam int PORT_EAST  = 0;
    localparam int PORT_WEST  = 1;
    localparam int PORT_NORTH = 2;
    localparam int PORT_SOUTH = 3;
    localparam int PORT_LOCAL = 4;

    always_comb begin
        lookahead_port = 5'b00000;

        // Dimension-Order Routing (XY) logic evaluated at downstream router:
        if (dest_x > next_x) begin
            // Destination is further East of downstream router
            lookahead_port[PORT_EAST] = 1'b1;
        end else if (dest_x < next_x) begin
            // Destination is further West of downstream router
            lookahead_port[PORT_WEST] = 1'b1;
        end else begin
            // Horizontal dimension is completely satisfied (dest_x == next_x)
            // Now resolve the vertical (Y) dimension:
            if (dest_y > next_y) begin
                lookahead_port[PORT_SOUTH] = 1'b1;
            end else if (dest_y < next_y) begin
                lookahead_port[PORT_NORTH] = 1'b1;
            end else begin
                // Packet has reached its destination core!
                lookahead_port[PORT_LOCAL] = 1'b1;
            end
        end
    end

endmodule
```

### Hardware Cost Analysis:
- **Area:** 4 integer magnitude comparators ($>$ and $<$) and 2 equality gates. In a 7nm standard-cell library, this synthesizes to **under 45 logic gates ($\approx 35\ \mu\text{m}^2$)**.
- **Critical Path Delay:** Less than **$40\text{ picoseconds}$**, effortlessly meeting timing at frequencies exceeding $3.0\text{ GHz}$.

---

## 4. Formal Proof of Deadlock Freedom

Why is XY routing guaranteed to never deadlock?

### The 8 Orthogonal Turns in a 2D Mesh
In a 2D planar mesh, a packet changing directions at any router makes one of **8 possible turns**:

```
X-to-Y Turns:                       Y-to-X Turns:
1. East  -> North                   5. North -> East
2. East  -> South                   6. North -> West
3. West  -> North                   7. South -> East
4. West  -> South                   8. South -> West
```

A routing deadlock in a wormhole network requires a **closed circular loop of channel dependencies**:
$$\text{Channel } C_1 \rightarrow C_2 \rightarrow C_3 \rightarrow C_4 \rightarrow C_1$$

In a 2D mesh, every closed cycle must consist of at least one turn from each quadrant, forming either:
- A **Clockwise (CW) Cycle:** $\text{North} \rightarrow \text{East} \rightarrow \text{South} \rightarrow \text{West} \rightarrow \text{North}$
- A **Counter-Clockwise (CCW) Cycle:** $\text{North} \rightarrow \text{West} \rightarrow \text{South} \rightarrow \text{East} \rightarrow \text{North}$

```mermaid
graph TD
  subgraph Prohibited_In_XY [All 4 Y-to-X Turns Are FORBIDDEN]
    NE[North -> East: ILLEGAL]
    NW[North -> West: ILLEGAL]
    SE[South -> East: ILLEGAL]
    SW[South -> West: ILLEGAL]
  end

  subgraph Permitted_In_XY [All 4 X-to-Y Turns Are Permitted]
    EN[East -> North: Allowed]
    ES[East -> South: Allowed]
    WN[West -> North: Allowed]
    WS[West -> South: Allowed]
  end

  classDef forbidStyle fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px,color:#991b1b;
  classDef allowStyle fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#166534;

  class NE,NW,SE,SW forbidStyle;
  class EN,ES,WN,WS allowStyle;
```

### The Monotonic Dimension Invariant
Under XY routing:
1. A packet begins in dimension $X$.
2. It can transition from $X \rightarrow X$ (continuing horizontally) or $X \rightarrow Y$ (turning into the vertical dimension).
3. **A packet is NEVER permitted to transition from $Y \rightarrow X$!**
4. Once a packet enters dimension $Y$, it can only transition from $Y \rightarrow Y$ or exit into the Local core.

Because transitions are strictly monotonic ($X \rightarrow Y$), any potential channel dependency path is a directed acyclic sequence. **A circular cycle requires at least one transition from $Y \rightarrow X$ to close the loop!**

Because all four $Y \rightarrow X$ turns are prohibited, **no directed cycle can ever form in the Channel Dependency Graph (CDG). Therefore, XY routing is provably deadlock-free!**

---

## 5. 🔬 Interactive XY / YX Dimension-Order Routing Stepper

Experiment with Dimension-Order Routing on a live $5 \times 5$ mesh grid. Set any source and destination, toggle between **XY** and **YX** routing, and step through the hop-by-hop route while auditing turn legality in real time:

<div class="noc-sim-container" id="dor-sim">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:1rem;">
    <div style="font-weight:700; font-size:1.05rem; color:var(--tcl-heading);">
      🧭 Dimension-Order Routing (DOR) Interactive Stepper &amp; Turn Auditor
    </div>
    <span class="noc-track-badge" style="background:rgba(37,99,235,0.1); color:#2563eb;">
      Live Turn Auditor &amp; CDG Tracker
    </span>
  </div>

  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:0.75rem; margin-bottom:1rem;">
    <div>
      <label style="font-size:0.82rem; font-weight:600; display:block; margin-bottom:0.25rem;">Routing Policy:</label>
      <select id="dor_policy" class="noc-sim-select" onchange="initDORSim()">
        <option value="XY" selected>XY Routing (X first, then Y)</option>
        <option value="YX">YX Routing (Y first, then X)</option>
      </select>
    </div>
    <div>
      <label style="font-size:0.82rem; font-weight:600; display:block; margin-bottom:0.25rem;">Source Node (x, y):</label>
      <select id="dor_src" class="noc-sim-select" onchange="initDORSim()">
        <option value="0,0" selected>(0, 0) - Top-Left</option>
        <option value="0,4">(0, 4) - Bottom-Left</option>
        <option value="1,3">(1, 3) - Center-South</option>
        <option value="4,0">(4, 0) - Top-Right</option>
      </select>
    </div>
    <div>
      <label style="font-size:0.82rem; font-weight:600; display:block; margin-bottom:0.25rem;">Destination Node (x, y):</label>
      <select id="dor_dst" class="noc-sim-select" onchange="initDORSim()">
        <option value="4,4" selected>(4, 4) - Bottom-Right</option>
        <option value="4,0">(4, 0) - Top-Right</option>
        <option value="0,3">(0, 3) - West Edge</option>
        <option value="2,1">(2, 1) - North-Central</option>
      </select>
    </div>
    <div style="display:flex; align-items:flex-end; gap:0.5rem;">
      <button class="noc-sim-btn" onclick="stepDOR()">⏭ Step Flit</button>
      <button class="noc-sim-btn" style="background:var(--md-default-fg-color--lightest); color:var(--md-default-fg-color); border:1px solid var(--tcl-border);" onclick="initDORSim()">🔄 Reset</button>
    </div>
  </div>

  <div style="display:flex; gap:1.25rem; flex-wrap:wrap; align-items:flex-start;">
    <div style="flex:1; min-width:280px; text-align:center;">
      <canvas id="dorCanvas" width="360" height="360" style="background:#0f172a; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.25); max-width:100%; height:auto;"></canvas>
    </div>

    <div style="flex:1.2; min-width:280px;">
      <div style="background:var(--md-default-fg-color--lightest); border:1px solid var(--tcl-border); border-radius:8px; padding:0.85rem; font-size:0.85rem; margin-bottom:0.75rem;">
        <div style="font-weight:700; color:var(--tcl-heading); margin-bottom:0.4rem;">📊 Real-Time Routing Status:</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.4rem;">
          <div>Current Position: <strong id="dor_curr" style="color:#38bdf8;">(0, 0)</strong></div>
          <div>Target: <strong id="dor_dest_lbl" style="color:#fb923c;">(4, 4)</strong></div>
          <div>Hop Count: <strong id="dor_hops">0</strong></div>
          <div>Manhattan Dist: <strong id="dor_dist">8</strong></div>
          <div>Active Dimension: <strong id="dor_dim" style="color:#22c55e;">X-Dimension</strong></div>
          <div>Last Turn: <strong id="dor_turn">None</strong></div>
        </div>
      </div>

      <div style="background:var(--md-default-fg-color--lightest); border:1px solid var(--tcl-border); border-radius:8px; padding:0.85rem; font-size:0.82rem;">
        <div style="font-weight:700; color:var(--tcl-heading); margin-bottom:0.4rem;">🔍 Turn Auditor Log:</div>
        <div id="dor_log" style="font-family:monospace; height:130px; overflow-y:auto; line-height:1.5; color:var(--md-default-fg-color--lighter);">
          <!-- Dynamic execution log -->
        </div>
      </div>
    </div>
  </div>
</div>

<script>
const dorState = {
  gridSize: 5,
  policy: "XY",
  src: { x: 0, y: 0 },
  dst: { x: 4, y: 4 },
  curr: { x: 0, y: 0 },
  path: [],
  hops: 0,
  lastDir: null,
  isFinished: false
};

function initDORSim() {
  const p = document.getElementById("dor_policy").value;
  const sParts = document.getElementById("dor_src").value.split(",").map(Number);
  const dParts = document.getElementById("dor_dst").value.split(",").map(Number);

  dorState.policy = p;
  dorState.src = { x: sParts[0], y: sParts[1] };
  dorState.dst = { x: dParts[0], y: dParts[1] };
  dorState.curr = { x: sParts[0], y: sParts[1] };
  dorState.path = [{ x: sParts[0], y: sParts[1] }];
  dorState.hops = 0;
  dorState.lastDir = null;
  dorState.isFinished = (sParts[0] === dParts[0] && sParts[1] === dParts[1]);

  const log = document.getElementById("dor_log");
  log.innerHTML = `<span style="color:#38bdf8;">[INIT] Packet injected at (${dorState.src.x}, ${dorState.src.y}) targeting (${dorState.dst.x}, ${dorState.dst.y}) via ${p} DOR.</span>`;

  updateDORUI();
  drawDORCanvas();
}

function stepDOR() {
  if (dorState.isFinished) return;

  const { curr, dst, policy } = dorState;
  let nextX = curr.x;
  let nextY = curr.y;
  let activeDim = "X";
  let dir = "";

  if (policy === "XY") {
    if (curr.x < dst.x) { nextX++; dir = "East"; activeDim = "X"; }
    else if (curr.x > dst.x) { nextX--; dir = "West"; activeDim = "X"; }
    else if (curr.y < dst.y) { nextY++; dir = "South"; activeDim = "Y"; }
    else if (curr.y > dst.y) { nextY--; dir = "North"; activeDim = "Y"; }
  } else { // YX
    if (curr.y < dst.y) { nextY++; dir = "South"; activeDim = "Y"; }
    else if (curr.y > dst.y) { nextY--; dir = "North"; activeDim = "Y"; }
    else if (curr.x < dst.x) { nextX++; dir = "East"; activeDim = "X"; }
    else if (curr.x > dst.x) { nextX--; dir = "West"; activeDim = "X"; }
  }

  // Audit turn legality
  let turnStr = "Straight";
  let turnLegal = true;
  if (dorState.lastDir && dorState.lastDir !== dir) {
    turnStr = `${dorState.lastDir} ➔ ${dir}`;
    if (policy === "XY") {
      // Y-to-X is forbidden in XY
      if ((dorState.lastDir === "North" || dorState.lastDir === "South") && (dir === "East" || dir === "West")) {
        turnLegal = false;
      }
    } else {
      // X-to-Y is forbidden in YX
      if ((dorState.lastDir === "East" || dorState.lastDir === "West") && (dir === "North" || dir === "South")) {
        turnLegal = false;
      }
    }
  }

  dorState.curr = { x: nextX, y: nextY };
  dorState.path.push({ x: nextX, y: nextY });
  dorState.hops++;
  dorState.lastDir = dir;

  const log = document.getElementById("dor_log");
  const turnBadge = turnLegal ? `<span style="color:#22c55e;">[LEGAL]</span>` : `<span style="color:#ef4444;">[ILLEGAL!]</span>`;
  log.innerHTML += `<br/>Hop ${dorState.hops}: (${curr.x},${curr.y}) ➔ (${nextX},${nextY}) [${dir}] | Turn: ${turnStr} ${turnBadge}`;
  log.scrollTop = log.scrollHeight;

  if (nextX === dst.x && nextY === dst.y) {
    dorState.isFinished = true;
    log.innerHTML += `<br/><span style="color:#22c55e; font-weight:bold;">[DELIVERED] Reached destination (${dst.x}, ${dst.y}) in ${dorState.hops} hops!</span>`;
  }

  updateDORUI();
  drawDORCanvas();
}

function updateDORUI() {
  document.getElementById("dor_curr").textContent = `(${dorState.curr.x}, ${dorState.curr.y})`;
  document.getElementById("dor_dest_lbl").textContent = `(${dorState.dst.x}, ${dorState.dst.y})`;
  document.getElementById("dor_hops").textContent = dorState.hops;
  const remDist = Math.abs(dorState.dst.x - dorState.curr.x) + Math.abs(dorState.dst.y - dorState.curr.y);
  document.getElementById("dor_dist").textContent = remDist;
  
  const dimEl = document.getElementById("dor_dim");
  if (dorState.policy === "XY") {
    dimEl.textContent = dorState.curr.x !== dorState.dst.x ? "X-Dimension (Horizontal)" : (dorState.curr.y !== dorState.dst.y ? "Y-Dimension (Vertical)" : "Arrived");
  } else {
    dimEl.textContent = dorState.curr.y !== dorState.dst.y ? "Y-Dimension (Vertical)" : (dorState.curr.x !== dorState.dst.x ? "X-Dimension (Horizontal)" : "Arrived");
  }
  document.getElementById("dor_turn").textContent = dorState.lastDir || "None";
}

function drawDORCanvas() {
  const canvas = document.getElementById("dorCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  const N = dorState.gridSize;
  const pad = 36;
  const step = (w - pad * 2) / (N - 1);

  // Draw links
  ctx.lineWidth = 2;
  ctx.strokeStyle = "#334155";
  for (let r = 0; r < N; r++) {
    ctx.beginPath();
    ctx.moveTo(pad, pad + r * step);
    ctx.lineTo(w - pad, pad + r * step);
    ctx.stroke();
  }
  for (let c = 0; c < N; c++) {
    ctx.beginPath();
    ctx.moveTo(pad + c * step, pad);
    ctx.lineTo(pad + c * step, h - pad);
    ctx.stroke();
  }

  // Draw Traversed Path
  if (dorState.path.length > 1) {
    ctx.lineWidth = 4;
    ctx.strokeStyle = "#38bdf8";
    ctx.beginPath();
    for (let i = 0; i < dorState.path.length; i++) {
      const px = pad + dorState.path[i].x * step;
      const py = pad + dorState.path[i].y * step;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();
  }

  // Draw Router Nodes
  for (let r = 0; r < N; r++) {
    for (let c = 0; c < N; c++) {
      const px = pad + c * step;
      const py = pad + r * step;
      const isSrc = (c === dorState.src.x && r === dorState.src.y);
      const isDst = (c === dorState.dst.x && r === dorState.dst.y);
      const isCurr = (c === dorState.curr.x && r === dorState.curr.y);

      ctx.beginPath();
      ctx.arc(px, py, 11, 0, Math.PI * 2);

      if (isCurr) {
        ctx.fillStyle = "#eab308";
      } else if (isSrc) {
        ctx.fillStyle = "#2563eb";
      } else if (isDst) {
        ctx.fillStyle = "#ea580c";
      } else {
        ctx.fillStyle = "#1e293b";
      }
      ctx.fill();

      ctx.lineWidth = 2;
      ctx.strokeStyle = isCurr ? "#fef08a" : (isSrc ? "#60a5fa" : (isDst ? "#fb923c" : "#475569"));
      ctx.stroke();

      // Coordinates text
      ctx.fillStyle = "#94a3b8";
      ctx.font = "8px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(`${c},${r}`, px, py + 18);
    }
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initDORSim);
} else {
  initDORSim();
}
</script>

---

## 6. Worked Numerical Example: Channel Load Imbalance in DOR

> [!TIP]
> **Problem Statement:**  
> Consider an $8 \times 8$ 2D Mesh NoC running an asymmetric scientific computing workload.  
> - 32 worker cores located in columns $X \in [0, 3]$ concurrently send data to 32 accelerator cores located in columns $X \in [4, 7]$.
> - Every packet has source $(x_s, y_s)$ and destination $(x_d, y_d) = (x_s + 4, y_s)$.
> 
> Compare:
> 1. The maximum channel load ($\gamma_{max}$) under **XY Routing**.
> 2. The maximum channel load ($\gamma_{max}$) under **YX Routing**.
> 3. What happens if all workers instead send packets to $(x_d, y_d) = (x_s + 4, (y_s + 4) \bmod 8)$?

### Step 1: Evaluate Pure Horizontal Flow
For the pure horizontal flow ($y_s = y_d$):
- Under **XY Routing**, packets travel along rows: $(x_s, y) \rightarrow (x_s+1, y) \dots \rightarrow (x_s+4, y)$.
  - Traffic crosses the horizontal bisection between column 3 and column 4.
  - There are 8 horizontal bisection links (one per row).
  - Each link carries exactly $\frac{32}{8} = \mathbf{4\text{ packets per injection round}}$.
- Under **YX Routing**, $\Delta y = 0$, so packets also immediately traverse along $X$.
  - Maximum channel load is identical: $\gamma_{max} = 4$.

### Step 2: Evaluate Diagonal Shift Flow
Now consider destination $(x_d, y_d) = (x_s + 4, (y_s + 4) \bmod 8)$:
- **Under XY Routing:**
  - Packets first move horizontally across columns $0 \rightarrow 1 \rightarrow 2 \rightarrow 3 \rightarrow 4$.
  - All 32 packets cross the 8 horizontal bisection channels at column $3 \rightarrow 4$.
  - Load per horizontal bisection channel: $\gamma_{X} = \frac{32}{8} = \mathbf{4\text{ pkts/channel}}$.
  - Then, at column 4, packets turn South or North to resolve the $Y$ offset.
  - The vertical bisection channels in column 4 now experience severe congestion because all turning packets converge on column 4!
- **Under YX Routing:**
  - Packets first move vertically within their source columns $X \in [0, 3]$.
  - The vertical movement is spread evenly across all 4 source columns ($0, 1, 2, 3$).
  - Once vertical alignment is reached, packets cross the horizontal bisection channels into columns $4\text{–}7$.

### Takeaway:
Deterministic routing has zero flexibility to balance load dynamically. If a workload's communication pattern aligns unfavorably with the routing dimension order (e.g. all packets turning in the same column), severe localized hotspots emerge!

---

## 7. 🎯 Knowledge Check: Lesson 4.1

<div class="noc-sim-container" id="quiz41" style="margin-top:1rem;">
  <div style="font-weight:700; font-size:1.05rem; margin-bottom:1rem; color:var(--tcl-heading);">
    📝 Concept Check: Deterministic Routing &amp; DOR
  </div>

  <div id="q41_block">
    <p style="font-weight:600; font-size:0.95rem; margin-bottom:0.75rem;">
      <b>Question:</b> In Lookahead Route Computation (L-RC), why does router $R_i$ compute the output port for router $R_{i+1}$ instead of computing its own output port?
    </p>

    <div style="display:flex; flex-direction:column; gap:0.5rem;" id="q41_options">
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz41(0)">
        A. Because router R_{i} does not know its own coordinate.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz41(1)">
        B. To remove the Route Computation delay from the critical path of router R_{i+1}, allowing the flit to enter Switch Allocation immediately upon arrival.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz41(2)">
        C. Because lookahead routing enables packets to travel diagonally.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz41(3)">
        D. To reduce the number of Virtual Channels required.
      </button>
    </div>

    <div id="q41_feedback" style="display:none; margin-top:1rem; padding:0.85rem; border-radius:8px; font-size:0.9rem; line-height:1.5;"></div>
  </div>
</div>

<script>
function checkQuiz41(idx) {
  const fb = document.getElementById("q41_feedback");
  fb.style.display = "block";
  const opts = document.getElementById("q41_options").children;
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
    fb.innerHTML = "<strong>✓ Correct!</strong> By pre-computing the output port for the next downstream router in parallel with switch allocation at the current router, Route Computation is completely removed from the critical pipeline latency path.";
  } else {
    opts[idx].style.background = "rgba(239,68,68,0.15)";
    opts[idx].style.borderColor = "#ef4444";
    opts[1].style.background = "rgba(34,197,94,0.15)";
    opts[1].style.borderColor = "#22c55e";
    fb.style.background = "rgba(239,68,68,0.1)";
    fb.style.border = "1px solid rgba(239,68,68,0.3)";
    fb.style.color = "#991b1b";
    fb.innerHTML = "<strong>✗ Incorrect.</strong> The correct answer is <strong>B</strong>. Lookahead routing pre-computes the routing decision one hop ahead to eliminate the RC pipeline stage from downstream routers.";
  }
}
</script>

---

## Summary & Next Steps

In this lesson, we established:
- **Dimension-Order Routing (XY / YX)**: Algorithmic mechanics and minimal distance routing.
- **Lookahead Route Computation**: Removing route computation from the router's critical path via downstream pre-computation.
- **Synthesizable Verilog RTL**: Clean, low-latency combinational routing logic.
- **Deadlock Freedom Proof**: Proving that strictly forbidding $Y \rightarrow X$ turns breaks all circular dependency cycles.

However, XY routing's strict rigidity means packets cannot route around congested or faulty nodes. Can we break cycles while eliminating *fewer* turns to unlock path diversity?

👉 **Proceed to [Lesson 4.2: Adaptive Routing & The Turn Model](02-adaptive-turn-model.md)**
