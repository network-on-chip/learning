# 3.3 Interconnect Metrics & Benchmark Traffic Patterns

How do computer architects rigorously evaluate and compare network topologies? A topology that appears superior in theory may collapse under real-world cache coherence or matrix multiplication workloads.

To quantitatively evaluate on-chip networks, architects model two fundamental metrics—**Zero-Load Latency ($T_0$)** and **Saturation Throughput ($\Theta_{sat}$)**—and stress-test architectures against standard **Synthetic Traffic Patterns**.

In this lesson, we derive the mathematical laws of network throughput, analyze traffic distributions, and prove why certain communication patterns trigger premature network saturation.

<div class="noc-callout" style="background: rgba(15, 118, 110, 0.08); border-left: 4px solid #0f766e; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 8px 8px 0;">
  <div style="font-weight: 700; color: #0f766e; margin-bottom: 0.25rem;">📖 Textbook Reference</div>
  <div style="color: #334155; font-size: 0.95rem;">
    Access the complete traffic sensitivity matrix and maximum channel load bounds ($\gamma_{max}$) in <strong><a href="https://github.com/network-on-chip/book/blob/main/chapters/ch04-topologies-and-metrics/index.md#41-fundamentals-of-interconnect-graph-theory--quantitative-metrics" target="_blank" rel="noopener">Chapter 4.1: Fundamentals of Interconnect Graph Theory</a></strong>.
  </div>
</div>

---

## 1. Mathematical Modeling of Network Performance

When evaluating an interconnect, architects plot the classic **Latency vs. Offered Load Curve**:

```
Packet Latency (Cycles)
  ^
  |                                        | (Asymptotic Saturation: Latency ➔ ∞)
  |                                       /
  |                                      /
  |                                     /
  |                                    /
  |                                  /
  |________________________________/
  |-------- Zero-Load Latency (T_0) -------->
  +---------------------------------------------> Offered Load / Injection Rate (λ)
                                   ^
                              Saturation Throughput (Θ_sat)
```

### A. Zero-Load Latency ($T_0$)
Zero-Load Latency is the average time required for a packet to traverse the network when there is **zero contention** (no queuing stalls behind other packets):

$$T_0 = H_{avg} \cdot t_r + \frac{L}{w} + H_{avg} \cdot t_{link}$$

Where:
- $H_{avg}$ is the average shortest-path hop count.
- $t_r$ is the per-hop router pipeline delay (e.g., $1\text{–}3$ clock cycles).
- $L/w$ is the packet serialization delay ($L$ bits in packet, $w$ bits channel width).
- $t_{link}$ is the inter-router link wire propagation delay (typically $1$ clock cycle).

---

### B. Maximum Channel Load ($\gamma_{max}$) & Saturation Throughput ($\Theta_{sat}$)
Let $\gamma_c$ represent the traffic load on a physical channel $c$ (the expected number of flits traversing channel $c$ per injected packet).

The **Maximum Channel Load ($\gamma_{max}$)** is the load on the most heavily congested bottleneck channel in the entire network:

$$\gamma_{max} = \max_{c \in E} \gamma_c$$

Because a physical channel can carry at most **$1\text{ flit per clock cycle}$**, the network **saturates** when the bottleneck channel reaches 100% capacity:

$$\text{Saturation Injection Rate: } \mathbf{\Theta_{sat} = \frac{1}{\gamma_{max}} \quad \text{(flits / node / cycle)}}$$

Any attempt by nodes to inject traffic at a rate $\lambda > \Theta_{sat}$ will cause router FIFO queues to overflow and packet latency to diverge toward infinity!

---

### C. The Bisection Throughput Bound
A fundamental physical limit on saturation throughput is dictated by the **Bisection Bandwidth ($B_b$)**. If a fraction $\beta$ of all injected packets must cross the bisection:

$$\text{Total Bisection Demand} = N \cdot \lambda \cdot \beta$$

$$\text{Total Bisection Capacity} = 2 B_b$$

$$\mathbf{\Theta_{sat} \le \frac{2 B_b}{\beta \cdot N \cdot L}}$$

---

## 2. Standard Synthetic Traffic Patterns

To benchmark on-chip networks under reproducible, worst-case stress conditions, architects utilize standardized permutation patterns:

```
Source Node Coordinates: (x_s, y_s) in a k × k Mesh
```

### 1. Uniform Random (UR)
- Each node injects packets to any destination with equal probability:

    $$P(\text{dest} = j) = \frac{1}{N - 1} \quad (j \ne i)$$

- **Characteristics:** Perfectly distributed, benign baseline. Exercises all links evenly. Under UR, exactly **50% of traffic crosses the bisection** ($\beta = 0.5$).

### 2. Bit-Complement (BC)
- Each bit of the node coordinate is inverted:

    $$(x_d, y_d) = (k - 1 - x_s, \ k - 1 - y_s)$$

- *Example in $4 \times 4$ Mesh:* Node $(0,0) \rightarrow (3,3)$; Node $(0,1) \rightarrow (3,2)$.
- **Characteristics:** **100% of packets must cross both the horizontal and vertical bisections ($\beta = 1.0$)!** Creates extreme bisection congestion.

### 3. Transpose (TP)
- Inverts the coordinates across the main diagonal:

    $$(x_d, y_d) = (y_s, x_s)$$

- *Example in $4 \times 4$ Mesh:* Node $(1,3) \rightarrow (3,1)$.
- **Characteristics:** Common in matrix transposition and FFT operations. Stresses crossbar dimension switching while leaving diagonal nodes idle.

### 4. Tornado (TOR)
- Shifts packets halfway across the dimension:

    $$x_d = \left( x_s + \left\lfloor \frac{k}{2} \right\rfloor - 1 \right) \bmod k, \quad y_d = y_s$$

- **Characteristics:** Designed specifically to stress 2D Torus topologies by forcing packets to travel maximum distance along one direction without exploiting wrap-arounds.

### 5. Rent's Rule & Real-World Traffic Locality
Real application software (e.g., parallel graph traversal, deep learning forward/backward passes) is **NOT uniform random**. Communication exhibits strong spatial locality governed by **Rent's Rule**:

$$T = c \cdot G^p$$

Where $p$ is the **Rentian exponent** ($p \approx 0.5\text{–}0.7$). In cache-coherent CMPs, **over 70% of memory messages travel to immediate spatial neighbors ($H \le 2\text{ hops}$)**, drastically reducing bisection congestion compared to synthetic benchmarks!

---

## 3. Mathematical Proof: Why Bit-Complement Saturates at Half the Throughput of Uniform Random

> [!IMPORTANT]
> **Theorem:** In any symmetric $k \times k$ 2D Mesh, the saturation throughput under Bit-Complement traffic is **strictly 50% of the saturation throughput under Uniform Random traffic**:
>
> $$\Theta_{sat, BC} = \frac{1}{2} \Theta_{sat, UR}$$

### Proof:

1. **Under Uniform Random (UR) Traffic:**  
   The bisection cut divides the network into Left and Right halves ($N/2$ nodes each). The probability that a packet injected in the Left half has its destination in the Right half is $\beta_{UR} = \frac{N/2}{N} = \frac{1}{2} = 50\%$. The total number of packets crossing the bisection per cycle is:

$$\text{Load}_{bisection, UR} = \left(\frac{N}{2} \cdot \lambda \right) \times \frac{1}{2} \times 2\text{ (both ways)} = \frac{N \lambda}{2}$$

   Because the bisection has $B_b = 2k$ channels:

$$\gamma_{max, UR} = \frac{N/2}{2k} = \frac{k^2}{4k} = \frac{k}{4}$$

$$\Theta_{sat, UR} = \frac{1}{\gamma_{max, UR}} = \mathbf{\frac{4}{k}}$$

2. **Under Bit-Complement (BC) Traffic:**  
   Every node in the Left half has its complement in the Right half ($x_d = k - 1 - x_s$). Therefore, **100% of injected packets must cross the bisection** ($\beta_{BC} = 1.0$):

$$\text{Load}_{bisection, BC} = N \cdot \lambda$$

$$\gamma_{max, BC} = \frac{N}{2k} = \frac{k^2}{2k} = \frac{k}{2}$$

$$\Theta_{sat, BC} = \frac{1}{\gamma_{max, BC}} = \mathbf{\frac{2}{k}}$$

3. **Comparison:**

$$\frac{\Theta_{sat, BC}}{\Theta_{sat, UR}} = \frac{2/k}{4/k} = \mathbf{\frac{1}{2} = 50\%} \quad \blacksquare$$

Under Bit-Complement traffic, the bisection channels saturate at **exactly half the injection rate** of Uniform Random traffic!

---

## 4. 🎛️ Interactive Synthetic Traffic & Bisection Stress Visualizer

Select a traffic benchmark pattern on a $4 \times 4$ 2D Mesh and observe the resulting channel load distribution ($\gamma_c$) and bisection stress in real time!

<div class="noc-sim-container" id="trafficSim">
  <div style="font-size:1.1rem; font-weight:700; color:var(--tcl-heading); margin-bottom:1rem; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;">
    <span>🔬 Benchmark Traffic Pattern &amp; Channel Load Visualizer</span>
    <span id="trafficBadge" style="font-family:'JetBrains Mono', monospace; font-size:0.9rem; font-weight:700; color:var(--tcl-blue-600); background:rgba(37,99,235,0.1); padding:3px 10px; border-radius:6px;">
      Uniform Random
    </span>
  </div>

  <div class="noc-sim-controls">
    <label><b>Traffic Pattern:</b>
      <select id="selTrafficPattern" class="noc-sim-select" onchange="updateTrafficSim()">
        <option value="ur" selected>Uniform Random (Balanced Baseline)</option>
        <option value="bc">Bit-Complement (Maximum Bisection Stress)</option>
        <option value="tp">Transpose (Diagonal Cross-Traffic)</option>
        <option value="tor">Tornado (Directional Stress)</option>
      </select>
    </label>

    <label><b>Offered Injection Rate ($\lambda$):</b>
      <input type="range" id="sliderInjection" min="0.05" max="0.60" step="0.05" value="0.20" style="width:140px;" oninput="updateTrafficSim()">
      <span id="dispInjectionVal" style="font-family:'JetBrains Mono', monospace; font-weight:700; color:var(--tcl-blue-600);">0.20</span> flits/node/cyc
    </label>

    <div style="margin-left:auto; display:flex; gap:0.5rem; align-items:center; font-size:0.82rem;">
      <span style="display:inline-block; width:12px; height:12px; background:#22c55e; border-radius:2px;"></span> Low Load
      <span style="display:inline-block; width:12px; height:12px; background:#f59e0b; border-radius:2px;"></span> Moderate
      <span style="display:inline-block; width:12px; height:12px; background:#ef4444; border-radius:2px;"></span> Saturation (&gt;1.0)
    </div>
  </div>

  <!-- Interactive Traffic Heatmap Canvas -->
  <div style="display:grid; grid-template-columns: 1fr 280px; gap:1.25rem; align-items:start;">
    <div style="background:var(--noc-surface-subtle); border:1px solid var(--noc-border); border-radius:10px; padding:1.25rem; text-align:center; overflow-x:auto;">
      <canvas id="trafficCanvas" width="460" height="400" style="max-width:100%; border-radius:8px;"></canvas>
    </div>

    <!-- Real-Time Traffic Metrics -->
    <div style="display:flex; flex-direction:column; gap:0.75rem;">
      <div style="background:var(--noc-surface); border:1.5px solid var(--tcl-border); border-radius:8px; padding:1rem;">
        <div style="font-size:0.75rem; color:var(--noc-text-muted); text-transform:uppercase; font-weight:700;">Max Channel Load ($\gamma_{max}$)</div>
        <div id="dispMaxLoad" style="font-size:1.8rem; font-weight:900; color:var(--tcl-blue-600); margin:4px 0;">-- flits/cyc</div>
        <div id="dispSatStatus" style="font-size:0.78rem; font-weight:700; padding:2px 8px; border-radius:4px; display:inline-block;">BELOW SATURATION</div>
      </div>

      <div style="background:var(--noc-surface); border:1px solid var(--noc-border); border-radius:8px; padding:1rem; font-size:0.85rem; line-height:1.6;">
        <div style="font-weight:700; color:var(--tcl-heading); margin-bottom:4px;">Theoretical Limits ($4 \times 4$ Mesh):</div>
        • <b>Theoretical $\Theta_{sat}$:</b> <span id="dispTheoSat" style="font-weight:700; color:var(--tcl-blue-600);">1.00 flits/node/cyc</span><br>
        • <b>Bisection Fraction ($\beta$):</b> <span id="dispBeta" style="font-weight:700;">50%</span><br>
        • <b>Bottleneck Channels:</b> <span id="dispBottleneckCh" style="font-weight:700; color:#ef4444;">Central Horizontal Links</span>
      </div>

      <div id="trafficAnalysisCallout" style="background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.25); border-radius:8px; padding:0.75rem 1rem; font-size:0.82rem; color:var(--tcl-heading); line-height:1.5;"></div>
    </div>
  </div>
</div>

<script>
let tSim = {
  k: 4,
  pattern: "ur",
  injection: 0.20
};

function updateTrafficSim() {
  tSim.pattern = document.getElementById("selTrafficPattern").value;
  tSim.injection = parseFloat(document.getElementById("sliderInjection").value);
  document.getElementById("dispInjectionVal").textContent = tSim.injection.toFixed(2);

  const pNames = {
    ur: "Uniform Random",
    bc: "Bit-Complement",
    tp: "Transpose",
    tor: "Tornado"
  };
  document.getElementById("trafficBadge").textContent = pNames[tSim.pattern];

  drawTrafficHeatmap();
}

function drawTrafficHeatmap() {
  const canvas = document.getElementById("trafficCanvas");
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;
  const k = tSim.k;

  ctx.clearRect(0, 0, width, height);

  const margin = 50;
  const stepX = (width - 2 * margin) / (k - 1);
  const stepY = (height - 2 * margin) / (k - 1);

  // Compute Link Loads
  // Under XY routing on 4x4 mesh:
  let h_load = Array(k).fill(0).map(() => Array(k-1).fill(0));
  let v_load = Array(k-1).fill(0).map(() => Array(k).fill(0));

  let totalCrossBisection = 0;
  let totalPkts = 0;

  for (let sy = 0; sy < k; sy++) {
    for (let sx = 0; sx < k; sx++) {
      let dests = [];
      if (tSim.pattern === "ur") {
        for (let dy = 0; dy < k; dy++) {
          for (let dx = 0; dx < k; dx++) {
            if (sx !== dx || sy !== dy) dests.push({ dx, dy, prob: 1.0 / (k*k - 1) });
          }
        }
      } else if (tSim.pattern === "bc") {
        dests.push({ dx: k - 1 - sx, dy: k - 1 - sy, prob: 1.0 });
      } else if (tSim.pattern === "tp") {
        dests.push({ dx: sy, dy: sx, prob: 1.0 });
      } else if (tSim.pattern === "tor") {
        dests.push({ dx: (sx + Math.floor(k/2) - 1 + k) % k, dy: sy, prob: 1.0 });
      }

      dests.forEach(d => {
        totalPkts += d.prob;
        // Check bisection
        if ((sx < 2 && d.dx >= 2) || (sx >= 2 && d.dx < 2)) {
          totalCrossBisection += d.prob;
        }

        // Trace XY path
        let cx = sx;
        while (cx !== d.dx) {
          const step = (d.dx > cx) ? 1 : -1;
          const linkIdx = Math.min(cx, cx + step);
          h_load[sy][linkIdx] += d.prob * tSim.injection;
          cx += step;
        }
        let cy = sy;
        while (cy !== d.dy) {
          const step = (d.dy > cy) ? 1 : -1;
          const linkIdx = Math.min(cy, cy + step);
          v_load[linkIdx][d.dx] += d.prob * tSim.injection;
          cy += step;
        }
      });
    }
  }

  // Find max load
  let maxLoad = 0;
  for (let r = 0; r < k; r++) {
    for (let c = 0; c < k - 1; c++) {
      if (h_load[r][c] > maxLoad) maxLoad = h_load[r][c];
    }
  }
  for (let r = 0; r < k - 1; r++) {
    for (let c = 0; c < k; c++) {
      if (v_load[r][c] > maxLoad) maxLoad = v_load[r][c];
    }
  }

  // Draw Horizontal Links with Heatmap Color
  for (let y = 0; y < k; y++) {
    for (let x = 0; x < k - 1; x++) {
      const load = h_load[y][x];
      const px = margin + x * stepX;
      const py = margin + y * stepY;

      ctx.lineWidth = 3.5 + Math.min(5, load * 4);
      ctx.strokeStyle = getHeatColor(load);
      ctx.beginPath();
      ctx.moveTo(px, py);
      ctx.lineTo(px + stepX, py);
      ctx.stroke();
    }
  }

  // Draw Vertical Links with Heatmap Color
  for (let y = 0; y < k - 1; y++) {
    for (let x = 0; x < k; x++) {
      const load = v_load[y][x];
      const px = margin + x * stepX;
      const py = margin + y * stepY;

      ctx.lineWidth = 3.5 + Math.min(5, load * 4);
      ctx.strokeStyle = getHeatColor(load);
      ctx.beginPath();
      ctx.moveTo(px, py);
      ctx.lineTo(px, py + stepY);
      ctx.stroke();
    }
  }

  // Draw Nodes
  for (let y = 0; y < k; y++) {
    for (let x = 0; x < k; x++) {
      const px = margin + x * stepX;
      const py = margin + y * stepY;

      ctx.beginPath();
      ctx.arc(px, py, 9, 0, Math.PI * 2);
      ctx.fillStyle = "#0f172a";
      ctx.fill();
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.fillStyle = "#64748b";
      ctx.font = "9px 'JetBrains Mono', monospace";
      ctx.fillText(`${x},${y}`, px - 9, py + 18);
    }
  }

  // Update UI stats
  document.getElementById("dispMaxLoad").textContent = `${maxLoad.toFixed(2)} flits/cyc`;
  const statBadge = document.getElementById("dispSatStatus");
  if (maxLoad >= 1.0) {
    statBadge.textContent = "🔥 NETWORK SATURATED!";
    statBadge.style.background = "rgba(239,68,68,0.15)";
    statBadge.style.color = "#ef4444";
  } else if (maxLoad >= 0.75) {
    statBadge.textContent = "⚠️ HEAVY CONGESTION";
    statBadge.style.background = "rgba(234,88,12,0.15)";
    statBadge.style.color = "#ea580c";
  } else {
    statBadge.textContent = "🟢 BELOW SATURATION";
    statBadge.style.background = "rgba(34,197,94,0.15)";
    statBadge.style.color = "#16a34a";
  }

  const theoSat = (tSim.pattern === "ur") ? 1.00 : (tSim.pattern === "bc" ? 0.50 : 0.67);
  const betaPct = Math.round((totalCrossBisection / totalPkts) * 100);
  document.getElementById("dispTheoSat").textContent = `${theoSat.toFixed(2)} flits/node/cyc`;
  document.getElementById("dispBeta").textContent = `${betaPct}%`;

  const callout = document.getElementById("trafficAnalysisCallout");
  if (tSim.pattern === "bc") {
    callout.innerHTML = `
      <strong>Bit-Complement Stress Profile:</strong><br>
      • <strong>${betaPct}% of traffic</strong> must traverse the central bisection cut.<br>
      • Bisection channels saturate at <strong>λ = 0.50</strong>, causing premature throughput collapse at half the capacity of uniform traffic.
    `;
  } else if (tSim.pattern === "tp") {
    callout.innerHTML = `
      <strong>Transpose Pattern Profile:</strong><br>
      • Stresses asymmetric dimension switching (X ➔ Y turns on diagonal).<br>
      • Corner and diagonal nodes experience stark load disparities.
    `;
  } else {
    callout.innerHTML = `
      <strong>Uniform Random Profile:</strong><br>
      • Exactly 50% of traffic crosses bisection.<br>
      • Maximum channel load is distributed uniformly across interior links.
    `;
  }
}

function getHeatColor(val) {
  if (val >= 1.0) return "#ef4444"; // Red
  if (val >= 0.7) return "#ea580c"; // Orange
  if (val >= 0.4) return "#f59e0b"; // Amber
  return "#22c55e"; // Green
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", updateTrafficSim);
} else {
  updateTrafficSim();
}
</script>

---

## 5. Worked Numerical Example: Saturation Throughput Calculation

> [!TIP]
> **Problem Statement:**  
> An $8 \times 8$ 2D Mesh NoC operates with a 2.0 GHz clock frequency ($\tau = 0.5\text{ ns}$).  
> Channel width is $w = 128\text{ bits}$ ($16\text{ Bytes}$).  
> 
> Calculate:
> 1. The Maximum Theoretical Saturation Injection Rate ($\Theta_{sat}$) under **Uniform Random (UR)** traffic.
> 2. The Maximum Theoretical Saturation Injection Rate ($\Theta_{sat}$) under **Bit-Complement (BC)** traffic.
> 3. The aggregate sustained network bandwidth (in TB/s) at the saturation threshold for both patterns.

### Step 1: Compute Saturation Injection Rates

For a $k \times k$ mesh with $k = 8$:

- **Uniform Random:** $\Theta_{sat, UR} = \frac{4}{k} = \frac{4}{8} = \mathbf{0.50\text{ flits/node/cycle}}$
- **Bit-Complement:** $\Theta_{sat, BC} = \frac{2}{k} = \frac{2}{8} = \mathbf{0.25\text{ flits/node/cycle}}$

### Step 2: Compute Aggregate Bandwidth at Saturation
Total nodes $N = 64$. Total flits injected per cycle across the entire chip:

$$\text{Flits/cycle (UR)} = N \times \Theta_{sat, UR} = 64 \times 0.50 = 32\text{ flits/cycle}$$

$$\text{Aggregate Bandwidth (UR)} = 32\text{ flits/cycle} \times 16\text{ Bytes/flit} \times 2.0\text{ GHz} = \mathbf{1,024\text{ GB/s} = 1.024\text{ TB/s}}$$

$$\text{Flits/cycle (BC)} = N \times \Theta_{sat, BC} = 64 \times 0.25 = 16\text{ flits/cycle}$$

$$\text{Aggregate Bandwidth (BC)} = 16\text{ flits/cycle} \times 16\text{ Bytes/flit} \times 2.0\text{ GHz} = \mathbf{512\text{ GB/s} = 0.512\text{ TB/s}}$$

### Takeaway:
Under Bit-Complement traffic, bisection bottleneck links choke the entire network, halving usable throughput!

---

## 6. 💻 Synthesizable Hardware: Synthetic Traffic Pattern Generator

To benchmark on-chip networks in hardware emulation and FPGA rapid prototyping, designers implement **On-Chip Traffic Generators & Latency Profilers**.

The module below, `traffic_pattern_generator.v`, provides:
1. **Four runtime-selectable traffic modes**: Uniform Random (via 16-bit Galois LFSR), Bit-Complement, Transpose, and Tornado.
2. **Fractional injection rate throttling**: Allows sweeping injection loads from $\lambda = 0.01$ to $1.0\text{ flits/cycle}$.
3. **Cycle timestamp insertion & bisection link crossing counters**: Enables real-time verification of the Bit-Complement 100% bisection stress phenomenon!

```verilog
//=============================================================================
// Module: traffic_pattern_generator
// Description: Synthesizable On-Chip Benchmark Traffic Pattern Generator &
//              Latency Profiling Engine for NoC Routers.
//              Supports 4 selectable traffic patterns:
//                2'b00: Uniform Random (via 16-bit Galois LFSR)
//                2'b01: Bit-Complement (x_d = K-1-x_s, y_d = K-1-y_s)
//                2'b10: Transpose      (x_d = y_s,     y_d = x_s)
//                2'b11: Tornado        (x_d = (x_s + K/2 - 1)%K, y_d = y_s)
//              Includes injection rate regulation (rate_limiter), cycle timestamp
//              tagging, and bisection link crossing counters.
//=============================================================================

module traffic_pattern_generator #(
    parameter integer K          = 8,   // Mesh dimension size (8x8 = 64 nodes)
    parameter integer COORD_W    = 3,   // log2(K)
    parameter integer FLIT_WIDTH = 64,
    parameter integer TIME_W     = 16   // Cycle timestamp bitwidth
)(
    input  wire                   clk,
    input  wire                   rst_n,

    // Node Configuration & Traffic Control
    input  wire [COORD_W-1:0]     src_x,
    input  wire [COORD_W-1:0]     src_y,
    input  wire [1:0]             pattern_sel,     // 00=UR, 01=BC, 10=TP, 11=TOR
    input  wire [9:0]             rate_fraction,   // 0..1023 (1024 = 100% injection load)
    input  wire                   enable_gen,

    // Outgoing Injected Flit Interface
    output reg                    inj_valid,
    output reg  [FLIT_WIDTH-1:0]  inj_flit,
    input  wire                   inj_ready,

    // Performance Monitoring Outputs
    output reg  [31:0]            total_injected_pkts,
    output reg  [31:0]            bisection_crossings,
    output wire                   crosses_bisection
);

    // 16-bit Galois LFSR for Pseudorandom Destination Generation (Uniform Random)
    reg [15:0] lfsr_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // Seed based on node coordinate to ensure independent random sequences per node
            lfsr_reg <= {src_y, src_x, 10'b1010011001};
        end else if (enable_gen) begin
            lfsr_reg <= {lfsr_reg[0], lfsr_reg[15] ^ lfsr_reg[0], lfsr_reg[14],
                         lfsr_reg[13] ^ lfsr_reg[0], lfsr_reg[12] ^ lfsr_reg[0],
                         lfsr_reg[11:1]};
        end
    end

    // Traffic Pattern Destination Mapping Combinational Logic
    reg [COORD_W-1:0] target_x;
    reg [COORD_W-1:0] target_y;

    always @(*) begin
        case (pattern_sel)
            2'b00: begin // Uniform Random
                target_x = lfsr_reg[COORD_W-1:0];
                target_y = lfsr_reg[2*COORD_W-1:COORD_W];
            end
            2'b01: begin // Bit-Complement
                target_x = (K - 1) - src_x;
                target_y = (K - 1) - src_y;
            end
            2'b10: begin // Transpose
                target_x = src_y;
                target_y = src_x;
            end
            2'b11: begin // Tornado
                target_x = (src_x + (K / 2) - 1'b1) % K;
                target_y = src_y;
            end
        endcase
    end

    // Fractional Rate Accumulator (Leaky-Bucket Injection Throttle)
    reg [10:0] rate_accum;
    wire inject_trigger = rate_accum[10];

    // Hardware Cycle Counter for Timestamp Tagging
    reg [TIME_W-1:0] cycle_counter;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) cycle_counter <= {TIME_W{1'b0}};
        else        cycle_counter <= cycle_counter + 1'b1;
    end

    // Bisection Crossing Detector: High if traffic crosses central cut line (x = K/2)
    assign crosses_bisection = (src_x < (K / 2)) ^ (target_x < (K / 2));

    // Injection Engine State Machine & Accounting
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rate_accum          <= 11'd0;
            inj_valid           <= 1'b0;
            inj_flit            <= {FLIT_WIDTH{1'b0}};
            total_injected_pkts <= 32'd0;
            bisection_crossings <= 32'd0;
        end else if (enable_gen) begin
            rate_accum <= rate_accum[9:0] + {1'b0, rate_fraction};

            if (inject_trigger && inj_ready) begin
                inj_valid <= 1'b1;
                // Header format: [63:58]=Type, [57:52]=DestX/Y, [51:46]=SrcX/Y, [31:16]=Timestamp, [15:0]=Seq
                inj_flit  <= {2'b11, 4'b0000, target_x, target_y, src_x, src_y, cycle_counter, total_injected_pkts[15:0]};
                total_injected_pkts <= total_injected_pkts + 1'b1;
                if (crosses_bisection) begin
                    bisection_crossings <= bisection_crossings + 1'b1;
                end
            end else if (!inj_ready) begin
                inj_valid <= inj_valid; // Hold until downstream absorbs
            end else begin
                inj_valid <= 1'b0;
            end
        end else begin
            inj_valid <= 1'b0;
        end
    end

endmodule
```

---

## 7. 🕹️ Interactive Lab & Arcade Arena

Benchmark traffic patterns and thermal dynamics in real-time arcade simulations:

<div class="noc-tracks-grid" style="margin-top:1rem;">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(239,68,68,0.15); color:#ef4444;">Arcade Defense</span>
      <div class="noc-track-title">🛡️ Hotspot Hero: Thermal Defender</div>
      <div class="noc-track-desc">
        Observe how localized traffic bursts and Bit-Complement congestion trigger severe silicon hot spots, requiring real-time DVFS and cryo cooling.
      </div>
    </div>
    <a href="../interactive/hotspot/" class="noc-track-link">Play Hotspot Hero →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(37,99,235,0.15); color:#2563eb;">Topology Lab</span>
      <div class="noc-track-title">🌐 Topology Titans: Traffic Stress</div>
      <div class="noc-track-desc">
        Toggle between Uniform Random, Bit-Complement, and All-to-All communication patterns and observe network link saturation live on graph topologies.
      </div>
    </div>
    <a href="../interactive/topology/" class="noc-track-link">Launch Stress Lab →</a>
  </div>
</div>

---

## 8. 🎯 Comprehensive Self-Assessment Quiz

Test your mastery of network performance bounds, channel loads, and traffic locality:

<div class="noc-sim-container" id="quiz33_container" style="margin-top:1rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; border-bottom:1px solid var(--tcl-border); padding-bottom:0.5rem;">
    <span style="font-weight:700; font-size:1.05rem; color:var(--tcl-heading);">📝 Lesson 3.3 Self-Check</span>
    <span id="quiz33_score" style="font-weight:700; font-size:0.9rem; color:#2563eb;">Score: 0 / 3</span>
  </div>

  <!-- Question 1 -->
  <div class="quiz-item" style="margin-bottom:1.5rem;">
    <p style="font-weight:600; font-size:0.95rem; margin-bottom:0.6rem;">
      <b>Q1:</b> Why does a 2D Mesh saturate at a significantly lower injection rate under <strong>Bit-Complement</strong> traffic compared to <strong>Uniform Random</strong> traffic?
    </p>
    <div style="display:flex; flex-direction:column; gap:0.45rem;" id="q33_1_options">
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(1, 0)">A. Because Bit-Complement traffic disables Virtual Channels.</button>
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(1, 1)">B. Because 100% of packets in Bit-Complement traffic must cross the network bisection cut ($\beta = 1.0$), doubling the channel load on central bisection links compared to Uniform Random (where only 50% cross).</button>
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(1, 2)">C. Because Bit-Complement packets are twice as large.</button>
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(1, 3)">D. Because Bit-Complement traffic forces all packets to route to Corner 0.</button>
    </div>
    <div id="q33_1_feedback" style="display:none; margin-top:0.6rem; padding:0.75rem; border-radius:6px; font-size:0.88rem; line-height:1.5;"></div>
  </div>

  <!-- Question 2 -->
  <div class="quiz-item" style="margin-bottom:1.5rem;">
    <p style="font-weight:600; font-size:0.95rem; margin-bottom:0.6rem;">
      <b>Q2:</b> Under the Zero-Load Latency formula $T_0 = H_{avg} \cdot (t_r + t_{link}) + \frac{L}{w}$, which term dominates in large-scale on-chip networks ($N \ge 256$ nodes)?
    </p>
    <div style="display:flex; flex-direction:column; gap:0.45rem;" id="q33_2_options">
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(2, 0)">A. The serialization latency $L/w$, because packets grow quadratically with core count.</button>
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(2, 1)">B. The accumulated hop traversal delay $H_{avg} \cdot (t_r + t_{link})$, because $H_{avg} = \frac{2}{3}\sqrt{N}$ scales with grid size while serialization delay remains constant.</button>
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(2, 2)">C. The arbiter setup time, which increases exponentially with chip area.</button>
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(2, 3)">D. The clock jitter buffer delay.</button>
    </div>
    <div id="q33_2_feedback" style="display:none; margin-top:0.6rem; padding:0.75rem; border-radius:6px; font-size:0.88rem; line-height:1.5;"></div>
  </div>

  <!-- Question 3 -->
  <div class="quiz-item" style="margin-bottom:1rem;">
    <p style="font-weight:600; font-size:0.95rem; margin-bottom:0.6rem;">
      <b>Q3:</b> According to <strong>Rent's Rule</strong> ($T = k \cdot C^p$), what does an empirical Rent exponent of $p < 0.6$ signify for multi-core SoC traffic?
    </p>
    <div style="display:flex; flex-direction:column; gap:0.45rem;" id="q33_3_options">
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(3, 0)">A. Strong communication locality, meaning compute cores predominantly access nearest-neighbor caches and cluster memory rather than distant global nodes.</button>
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(3, 1)">B. Perfect all-to-all broadcast traffic across the full chip.</button>
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(3, 2)">C. That the network routers must use circuit switching.</button>
      <button class="noc-sim-select" style="text-align:left; padding:0.6rem 0.85rem; cursor:pointer;" onclick="answerQ33(3, 3)">D. That the network has zero dynamic power dissipation.</button>
    </div>
    <div id="q33_3_feedback" style="display:none; margin-top:0.6rem; padding:0.75rem; border-radius:6px; font-size:0.88rem; line-height:1.5;"></div>
  </div>
</div>

<script>
let q33Score = 0;
const answeredQ33 = {1: false, 2: false, 3: false};

function answerQ33(qNum, selected) {
  if (answeredQ33[qNum]) return;
  answeredQ33[qNum] = true;

  const correctAnswers = {1: 1, 2: 1, 3: 0};
  const isCorrect = (selected === correctAnswers[qNum]);
  const fb = document.getElementById("q33_" + qNum + "_feedback");
  const opts = document.getElementById("q33_" + qNum + "_options").children;

  for (let i = 0; i < opts.length; i++) {
    opts[i].style.cursor = "default";
    opts[i].onclick = null;
  }

  if (isCorrect) {
    q33Score++;
    opts[selected].style.background = "rgba(34, 197, 94, 0.15)";
    opts[selected].style.borderColor = "#22c55e";
    fb.style.display = "block";
    fb.style.background = "rgba(34, 197, 94, 0.1)";
    fb.style.border = "1px solid rgba(34, 197, 94, 0.3)";
    fb.style.color = "#166534";
    fb.innerHTML = "<strong>✓ Correct!</strong> " + getQ33Explanation(qNum, true);
  } else {
    opts[selected].style.background = "rgba(239, 68, 68, 0.15)";
    opts[selected].style.borderColor = "#ef4444";
    opts[correctAnswers[qNum]].style.background = "rgba(34, 197, 94, 0.15)";
    opts[correctAnswers[qNum]].style.borderColor = "#22c55e";
    fb.style.display = "block";
    fb.style.background = "rgba(239, 68, 68, 0.1)";
    fb.style.border = "1px solid rgba(239, 68, 68, 0.3)";
    fb.style.color = "#991b1b";
    fb.innerHTML = "<strong>✗ Incorrect.</strong> " + getQ33Explanation(qNum, false);
  }

  document.getElementById("quiz33_score").textContent = "Score: " + q33Score + " / 3";
}

function getQ33Explanation(qNum, wasCorrect) {
  if (qNum === 1) {
    return "Under Bit-Complement, each node targets the coordinate-inverted tile on the opposite side of the chip. Thus 100% of packets cross the bisection cut, doubling bottleneck link load and halving saturation throughput.";
  } else if (qNum === 2) {
    return "In large meshes, average hop count H_avg = (2/3)sqrt(N) multiplies the per-hop router and wire delay. As N grows to 256 or 1024, hop latency accounts for >80% of total zero-load packet transit time.";
  } else {
    return "Rent's exponent p characterizes boundary traffic scaling. A low exponent (p < 0.6) reflects high spatial locality: local clusters communicate internally, requiring much less global bisection bandwidth than random traffic.";
  }
}
</script>

---

## Summary & Next Steps

In this lesson, we established:
- Mathematical derivations of **Zero-Load Latency ($T_0$)** and **Saturation Throughput ($\Theta_{sat} = 1/\gamma_{max}$)**.
- Standard benchmark traffic patterns (**Uniform Random, Bit-Complement, Transpose, Tornado**).
- Mathematical proof showing that **Bit-Complement saturates at exactly half the throughput of Uniform Random traffic**.
- Synthesizable Verilog implementation of the `traffic_pattern_generator.v` module.

👉 **Proceed to [Lesson 3.4: High-Radix Topologies: Dragonfly & Flattened Butterfly](04-high-radix-topologies.md)**

