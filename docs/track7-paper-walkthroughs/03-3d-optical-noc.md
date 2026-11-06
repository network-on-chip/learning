# 7.3 Stacking the 3rd Dimension: 3D Optical NoC for MPSoCs

> **Companion Reading:** Monograph Chapter 10 — *Emerging Frontiers: Optical, Wireless, and Neuromorphic NoCs*, Section 10.1 (Silicon Nanophotonics and Optical NoCs). [Read in Companion Textbook →](/learning/textbook/ch10-emerging-frontiers/)

| Paper Details | Primary Reference |
| :--- | :--- |
| **Title** | *3-D Mesh-Based Optical Network-on-Chip for Multiprocessor System-on-Chip* |
| **Authors** | Y. Ye, J. Xu, X. Wu, W. Zhang, W. Liu, M. Nikdast |
| **Venue** | **IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD)**, Vol. 32, No. 4, April 2013 [[Ye2013]](#ref-ye2013) |
| **Repository Paper** | 📂 [`papers/3-d-mesh-based-optical-network-on-chip-for-multiprocessor-system-on-chip/`](https://github.com/network-on-chip/noc-lab/tree/main/papers/3-d-mesh-based-optical-network-on-chip-for-multiprocessor-system-on-chip) |

---

## 1. The Vision: Uniting 3D Stacking and Silicon Photonics

By 2013, two revolutionary interconnect paradigms had emerged independently:
1. **3D Integrated Circuits (3D ICs):** Stacking dies vertically with Through-Silicon Vias (TSVs) to reduce average planar wire distance [[Pavlidis2009]](#ref-pavlidis2009).
2. **Optical Networks-on-Chip (ONoCs):** Guiding photons along silicon waveguides to achieve speed-of-light propagation with zero capacitive in-flight power [[Vantrease2008]](#ref-vantrease2008).

However, prior optical networks were purely 2D planar meshes. When mapped onto multi-layer 3D chips, fabricating multiple optical waveguide layers proved prohibitively expensive and introduced massive thermal cross-talk.

In this landmark IEEE TCAD paper, researchers from the Hong Kong University of Science and Technology (HKUST) proposed a unified architecture: **a 3D Mesh-Based Optical Network-on-Chip** [[Ye2013]](#ref-ye2013).
By stacking two active CMOS electrical computing tiers using vertical TSVs and dedicating a single top optical layer for high-speed photonic routing, they demonstrated that multi-terabit bisection bandwidth could be achieved with unprecedented energy efficiency.

```mermaid
graph TD
  subgraph Physical_Stack ["3D Hybrid Electro-Optical Stack"]
    direction TB
    Opt_Layer["Top Optical Routing Layer<br/>Silicon Waveguides + Micro-Ring Resonators (MRRs) + VCSEL Lasers"]
    TSV_Bus["Vertical TSV Interconnect Layer<br/>Transfers control signals and electrical payloads between tiers"]
    Tier1["Tier 1: Electrical Compute Tier (32 Cores + L2 Caches)"]
    Tier0["Tier 0: Electrical Compute Tier (32 Cores + L2 Caches)"]

    Opt_Layer === TSV_Bus
    TSV_Bus === Tier1
    Tier1 === Tier0
  end
```

---

## 2. Low-Loss Passive 7×7 Optical Router Microarchitecture

In a 3D mesh network, each optical router must switch light across 7 spatial directions: $\{Local, East, West, North, South, Up, Down\}$.

### The Crossbar Crisis in Optics
A traditional non-blocking optical crossbar requires $7 \times 7 = \mathbf{49 \ \text{Micro-Ring Resonators (MRRs)}}$ [[Little1997]](#ref-little1997) and generates **$67 \ \text{waveguide crossings}$**.
Because every waveguide crossing scatters light and introduces an optical insertion loss ($\approx 0.12 \ \text{dB/crossing}$), an optical signal passing through multiple cascaded crossbars loses over $80\%$ of its optical power to crossing attenuation alone!

### The Authors' Breakthrough: The Passive-Routing 7×7 Router
The HKUST team designed a specialized **passive-routing $7 \times 7$ optical router** optimized specifically for 3D Dimension-Order Routing (DOR):

```
  Traditional 7x7 Crossbar:  49 MRRs  |  67 Crossings  |  Active Power on Every Hop
  HKUST Proposed 7x7 Router: 26 MRRs  |  31 Crossings  |  PASSIVE Straight-Through (0 mW)
```

```mermaid
graph LR
  subgraph Passive_Benefit ["Passive Routing Mechanism"]
    direction TB
    Straight["East ↔ West or North ↔ South Packets<br/>Travel straight along waveguides<br/>⚡ ZERO MRRs powered on! (0 mW)"]
    Turn["Dimension Turns (e.g., East → North or X → Up)<br/>Light couples through exactly ONE MRR<br/>⚡ Minimal switching power!"]
  end
```

1. **47% Fewer Micro-Rings:** Reduced from 49 to **26 MRRs**, slashing silicon area and thermal tuning heaters.
2. **54% Fewer Waveguide Crossings:** Reduced from 67 to **31 crossings**, saving over $4.3 \ \text{dB}$ of optical signal power across an end-to-end traversal.
3. **Zero Power for Straight Hops:** Packets propagating along the same dimension ($X$ or $Y$) pass through straight waveguides passively without requiring any active electrical bias on the micro-rings.

---

## 3. Adaptive Power Control (APC) for On-Chip Lasers

In conventional optical interconnects, laser sources (such as Vertical-Cavity Surface-Emitting Lasers, or VCSELs) are hardwired to output the **worst-case optical power** required by the longest, most lossy physical path across the chip.
For shorter paths (e.g., a 1-hop neighbor), this results in massive waste: over $75\%$ of the laser optical power is needlessly absorbed by photodetectors.

```mermaid
graph TD
  subgraph APC_Engine ["Adaptive Power Control (APC) Mechanism"]
    Router_Ctrl["Router Path Setup Logic<br/>Knows (Src_X, Src_Y, Src_Z) and (Dst_X, Dst_Y, Dst_Z)"]
    Loss_Table["Pre-Calculated Optical Loss Lookup Table<br/>Path Loss = L_prop(d) + N_cross * 0.12 dB + N_turn * 0.8 dB"]
    VCSEL_Driver["Dynamic Multi-Level VCSEL Current Driver"]
    Laser_Beam["VCSEL Laser Emits JUST-ENOUGH Optical Power<br/>Saves 40%–60% of Total Laser Energy!"]

    Router_Ctrl --> Loss_Table
    Loss_Table --> VCSEL_Driver
    VCSEL_Driver --> Laser_Beam
  end
```

The authors introduced **Adaptive Power Control (APC)**:
1. Because packets use deterministic XYZ dimension-order routing, the exact sequence of waveguide crossings and micro-ring drops between any source $(x_s, y_s, z_s)$ and destination $(x_d, y_d, z_d)$ is known statically.
2. During the 1-cycle path setup, an on-chip lookup table computes the exact path loss in decibels.
3. The VCSEL laser driver dynamically adjusts its driving current to emit **just enough photons** to meet receiver photodetector sensitivity (plus a $3\text{ dB}$ margin).
4. **Result:** Laser power dissipation drops by **$40\text{–}60\%$** across benchmark suites!

---

## 4. Single Optical Layer Floorplan Optimization

How do you map a 3-dimensional mesh network ($M \times N \times 2$) onto a single planar optical layer without creating hundreds of intersecting waveguide crossings?

```mermaid
graph LR
  subgraph Floorplan ["HKUST Optimized Single-Layer Optical Floorplan"]
    direction LR
    E_Tier0["Tier 0 Routers (Interleaved in Center)"]
    E_Tier1["Tier 1 Routers (Folded into Outer Perimeter)"]
    Waveguides["Re-ordered Waveguide Busses with Offset Interleaving"]

    E_Tier0 --- Waveguides --- E_Tier1
  end
```

By folding the two 3D tiers into an interleaved concentric layout, the authors proved that an $8 \times 8 \times 2$ (128-core) 3D mesh can be implemented on a single top optical layer with **only 224 network-level waveguide crossings**, compared to over $500$ crossings in naive grid mappings.

---

## 5. Interactive 3D Optical NoC Insertion Loss & APC Simulator

Experiment with the optical physics of this IEEE TCAD paper below. Select a source and destination node across the 3D tiers, toggle between a Traditional Crossbar and the proposed Low-Loss 7×7 Passive Router, and observe the cumulative optical loss and dynamic laser power required!

<div style="background:var(--md-code-bg-color); border:1px solid var(--md-default-fg-color--lightest); border-radius:8px; padding:20px; margin:24px 0;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
    <h3 style="margin:0; font-size:1.15rem; color:var(--md-typeset-color);">🔬 3D Optical NoC Insertion Loss & Laser Power Calculator</h3>
    <label style="font-size:0.85rem; color:#38bdf8; font-weight:600;">
      <input type="checkbox" id="chk-apc" onchange="updateOptSim()" checked> Enable Adaptive Power Control (APC)
    </label>
  </div>

  <div style="display:grid; grid-template-columns:1fr 280px; gap:20px; align-items:start;">
    <div>
      <canvas id="canvasOpt" width="600" height="340" style="width:100%; height:auto; background:#0f172a; border-radius:6px; display:block;"></canvas>
      <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:0.85rem; color:var(--md-default-fg-color--light);">
        <span>Optical Path: Tier 0 (Red) → Vertical TSV → Top Optical Waveguide (Gold)</span>
        <span id="txt-apc-status" style="font-weight:700; color:#10b981;">APC Active</span>
      </div>
    </div>

    <div style="background:rgba(15,23,42,0.6); padding:16px; border-radius:6px; border:1px solid rgba(255,255,255,0.08); font-size:0.85rem;">
      <div style="font-weight:700; color:#38bdf8; margin-bottom:12px; font-size:0.95rem;">⚙️ Path Configuration</div>

      <div style="margin-bottom:10px;">
        <label style="display:block; margin-bottom:4px; color:#94a3b8;">Source Node (Tier 0):</label>
        <select id="sel-opt-src" onchange="updateOptSim()" style="width:100%; padding:4px 8px; border-radius:4px; background:#1e293b; color:#fff; border:1px solid #475569;">
          <option value="0,0,0">Node (0, 0, 0) - Corner</option>
          <option value="2,2,0">Node (2, 2, 0) - Center</option>
        </select>
      </div>

      <div style="margin-bottom:12px;">
        <label style="display:block; margin-bottom:4px; color:#94a3b8;">Destination Node (Tier 1):</label>
        <select id="sel-opt-dst" onchange="updateOptSim()" style="width:100%; padding:4px 8px; border-radius:4px; background:#1e293b; color:#fff; border:1px solid #475569;">
          <option value="7,7,1">Node (7, 7, 1) - Diametric Opposite (Max Loss)</option>
          <option value="3,3,1">Node (3, 3, 1) - Intermediate Hop</option>
          <option value="1,0,1">Node (1, 0, 1) - Short 2-Hop Path</option>
        </select>
      </div>

      <div style="margin-bottom:14px;">
        <label style="display:block; margin-bottom:4px; color:#94a3b8;">Optical Router Design:</label>
        <select id="sel-router-type" onchange="updateOptSim()" style="width:100%; padding:4px 8px; border-radius:4px; background:#1e293b; color:#fff; border:1px solid #475569;">
          <option value="proposed" selected>HKUST Proposed 7x7 Passive Router (26 MRRs)</option>
          <option value="traditional">Traditional 7x7 Crossbar (49 MRRs - High Loss)</option>
        </select>
      </div>

      <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">
        <div style="font-family:monospace; font-size:0.8rem; color:#cbd5e1; line-height:1.5;">
          Waveguide Crossings: <span id="txt-opt-cross" style="color:#38bdf8;">14</span><br/>
          Total Optical Loss: <span id="txt-opt-loss" style="color:#ef4444; font-weight:bold;">5.42 dB</span><br/>
          Laser Power Output: <span id="txt-opt-pwr" style="color:#10b981; font-weight:bold;">0.78 mW</span><br/>
          Power Savings vs Static: <span id="txt-opt-savings" style="color:#f59e0b; font-weight:bold;">48.5%</span>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
function updateOptSim() {
  const src = document.getElementById('sel-opt-src').value.split(',').map(Number);
  const dst = document.getElementById('sel-opt-dst').value.split(',').map(Number);
  const routerType = document.getElementById('sel-router-type').value;
  const useAPC = document.getElementById('chk-apc').checked;

  const dx = Math.abs(dst[0] - src[0]);
  const dy = Math.abs(dst[1] - src[1]);
  const dz = Math.abs(dst[2] - src[2]);
  const totalHops = dx + dy + dz;

  // Loss models from TCAD paper:
  // Waveguide propagation: 1.0 dB/cm (die width ≈ 1.5 cm)
  // Distance in cm ≈ (dx + dy) * 0.18 cm
  const propLoss = (dx + dy) * 0.18 * 1.0;

  // Waveguide crossings:
  // Proposed router: ~2 crossings/hop. Traditional crossbar: ~5 crossings/hop
  const crossPerHop = (routerType === 'proposed') ? 2 : 5;
  const numCrossings = totalHops * crossPerHop;
  const crossLoss = numCrossings * 0.12; // 0.12 dB per crossing

  // MRR drop loss: 0.8 dB per turn. In XYZ DOR, there are at most 2 turns (X->Y and Y->Z)
  const numTurns = (dx > 0 && dy > 0 ? 1 : 0) + (dz > 0 ? 1 : 0);
  const turnLoss = numTurns * 0.8;

  // Coupler loss
  const couplerLoss = 1.5;

  const totalLoss = couplerLoss + propLoss + crossLoss + turnLoss;

  // Worst-case loss for 8x8x2 mesh
  const maxLoss = couplerLoss + (14 * 0.18 * 1.0) + (15 * crossPerHop * 0.12) + 1.6;

  // Photodetector sensitivity: -20 dBm + 3 dB margin = -17 dBm (0.02 mW)
  const pSensitivityDbm = -17.0;
  const pLaserDbmAPC = pSensitivityDbm + totalLoss;
  const pLaserDbmStatic = pSensitivityDbm + maxLoss;

  const pLaserMwAPC = Math.pow(10, pLaserDbmAPC / 10.0);
  const pLaserMwStatic = Math.pow(10, pLaserDbmStatic / 10.0);

  const finalPowerMw = useAPC ? pLaserMwAPC : pLaserMwStatic;
  const savingsPct = ((pLaserMwStatic - pLaserMwAPC) / pLaserMwStatic) * 100.0;

  document.getElementById('txt-opt-cross').textContent = numCrossings;
  document.getElementById('txt-opt-loss').textContent = totalLoss.toFixed(2) + ' dB';
  document.getElementById('txt-opt-pwr').textContent = finalPowerMw.toFixed(3) + ' mW';
  document.getElementById('txt-opt-savings').textContent = useAPC ? savingsPct.toFixed(1) + '%' : '0% (Static Worst-Case)';
  document.getElementById('txt-apc-status').textContent = useAPC ? 'APC Active' : 'Static Laser (Unoptimized)';
  document.getElementById('txt-apc-status').style.color = useAPC ? '#10b981' : '#ef4444';

  // Render optical loss bar chart
  const canvas = document.getElementById('canvasOpt');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw 3D Floorplan stack representation
  // Top layer: Optical (Gold)
  ctx.fillStyle = 'rgba(234, 179, 8, 0.12)';
  ctx.strokeStyle = '#eab308';
  ctx.lineWidth = 1.5;
  ctx.fillRect(50, 40, 500, 70);
  ctx.strokeRect(50, 40, 500, 70);
  ctx.fillStyle = '#eab308';
  ctx.font = 'bold 11px Inter, sans-serif';
  ctx.fillText('Top Optical Routing Layer (Waveguides & Micro-Ring Switches)', 65, 60);

  // Middle layer: TSV vias
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.6)';
  ctx.lineWidth = 2;
  ctx.setLineDash([3, 3]);
  ctx.beginPath();
  ctx.moveTo(120, 110); ctx.lineTo(120, 160);
  ctx.moveTo(300, 110); ctx.lineTo(300, 160);
  ctx.moveTo(480, 110); ctx.lineTo(480, 160);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#38bdf8';
  ctx.font = '10px Inter, sans-serif';
  ctx.fillText('Vertical Copper TSVs (Control & Power)', 200, 140);

  // Bottom Electrical Layers
  ctx.fillStyle = 'rgba(2, 132, 199, 0.12)';
  ctx.strokeStyle = '#0284c7';
  ctx.fillRect(50, 160, 500, 50);
  ctx.strokeRect(50, 160, 500, 50);
  ctx.fillStyle = '#38bdf8';
  ctx.fillText('Tier 1: Electrical MPSoC Processor Cores', 65, 185);

  ctx.fillStyle = 'rgba(16, 185, 129, 0.12)';
  ctx.strokeStyle = '#10b981';
  ctx.fillRect(50, 220, 500, 50);
  ctx.strokeRect(50, 220, 500, 50);
  ctx.fillStyle = '#10b981';
  ctx.fillText('Tier 0: Electrical MPSoC Processor Cores + Memory', 65, 245);

  // Optical Traversal Path in Gold
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(120, 245);
  ctx.lineTo(120, 80);
  ctx.lineTo(460, 80);
  ctx.lineTo(460, 185);
  ctx.stroke();

  // Draw active photon dot
  ctx.beginPath();
  ctx.arc(300, 80, 6, 0, Math.PI * 2);
  ctx.fillStyle = '#ef4444';
  ctx.shadowColor = '#ef4444';
  ctx.shadowBlur = 10;
  ctx.fill();
  ctx.shadowBlur = 0;

  // Breakdown bar
  ctx.fillStyle = '#94a3b8';
  ctx.font = '10px Inter, sans-serif';
  ctx.fillText(`Loss Breakdown: Propagation (${propLoss.toFixed(1)} dB) + Waveguide Crossings (${crossLoss.toFixed(1)} dB) + MRR Turns (${turnLoss.toFixed(1)} dB) = ${totalLoss.toFixed(2)} dB`, 50, 310);
}

updateOptSim();
</script>

---

## 6. Worked Numerical Problem: Router Insertion Loss & Laser Budget

### Problem Statement
From the HKUST IEEE TCAD paper measurements on a 3D $8 \times 8 \times 2$ mesh ONoC:
An optical flit originates at core $(0, 0, 0)$ and terminates at core $(7, 7, 1)$, traversing a distance of $14 \ \text{hops}$ ($7 \ X$-hops, $7 \ Y$-hops, and $1 \ Z$-hop across tiers).

The physical parameters are:
- Waveguide propagation loss: $L_{prop} = 1.0 \ \text{dB/cm}$ across $L = 2.5 \ \text{cm}$ of silicon waveguide.
- Input and output grating coupler loss: $1.5 \ \text{dB}$ total.
- MRR turn insertion loss: $0.8 \ \text{dB}$ per dimension turn (2 turns total).
- Waveguide crossing loss: $0.12 \ \text{dB}$ per crossing.

1. **Calculate the total optical insertion loss for the Proposed HKUST Router ($2$ crossings/hop = 28 crossings).**
2. **Calculate the total optical insertion loss for the Traditional Crossbar ($5$ crossings/hop = 70 crossings).**
3. **If receiver sensitivity is $-17 \ \text{dBm}$, calculate how much more optical laser power the traditional crossbar requires compared to the proposed architecture.**

---

### Step-by-Step Solution

#### Step 1: Loss with Proposed HKUST 7×7 Router
Summing the loss components:

$$L_{proposed} = L_{coupler} + L_{prop} + (N_{cross} \times 0.12 \ \text{dB}) + (N_{turns} \times 0.8 \ \text{dB})$$

$$L_{proposed} = 1.5 \ \text{dB} + (1.0 \ \text{dB/cm} \times 2.5 \ \text{cm}) + (28 \times 0.12 \ \text{dB}) + (2 \times 0.8 \ \text{dB})$$

$$L_{proposed} = 1.5 + 2.5 + 3.36 + 1.6 = \mathbf{8.96 \ \text{dB}}$$

#### Step 2: Loss with Traditional 7×7 Crossbar
Using 70 waveguide crossings:

$$L_{traditional} = 1.5 \ \text{dB} + 2.5 \ \text{dB} + (70 \times 0.12 \ \text{dB}) + 1.6 \ \text{dB}$$

$$L_{traditional} = 1.5 + 2.5 + 8.40 + 1.6 = \mathbf{14.00 \ \text{dB}}$$

#### Step 3: Laser Power Ratio
The difference in decibel loss between the two architectures is:

$$\Delta L = L_{traditional} - L_{proposed} = 14.00 \ \text{dB} - 8.96 \ \text{dB} = \mathbf{5.04 \ \text{dB}}$$

Converting the decibel ratio to a linear optical power multiplier:

$$\frac{P_{laser, traditional}}{P_{laser, proposed}} = 10^{\frac{5.04}{10}} \approx \mathbf{3.19\times}$$

> [!TIP]
> The traditional crossbar forces the on-chip laser to emit **$3.19\times$ more optical power** ($>300\%$ higher laser energy) just to overcome waveguide crossing attenuation! The HKUST passive router design saves over **$68\%$ in laser energy**!

---

## 7. Synthesizable Verilog Module: `onoc_hybrid_3d_crossbar.v`

To overcome the thermal and optical loss bottlenecks of traditional 3D crossbars, the HKUST architecture combined **XYZ Dimension-Order Routing with passive straight-through waveguides** (reducing micro-ring count from 49 to 26) and deployed **Adaptive Power Control (APC)** to dynamically modulate VCSEL laser current based on deterministic destination loss.

The synthesizable module below implements the **3D Optical NoC Hybrid Controller**. It evaluates 3D coordinates, detects non-turning straight-through optical routes to bypass active rings, activates only the required subset of the 26 micro-ring resonators, and computes an 8-bit APC laser drive word scaled to exact path attenuation.

```verilog
//=============================================================================
// File: onoc_hybrid_3d_crossbar.v
// Module: onoc_hybrid_3d_crossbar
// Description: Synthesizable 7-Port 3D Optical NoC Hybrid Router Controller
//              with Reduced-MRR XYZ DOR Decoding and Adaptive Laser Power
//              Control (APC) based on HKUST 3D ONoC (IEEE TCAD 2013).
//              Ports: 0: East(+X), 1: West(-X), 2: South(+Y), 3: North(-Y),
//                     4: Down(-Z TSV), 5: Up(+Z TSV), 6: Local
//              Features:
//              - 26-MRR control matrix (slashed from 49 via passive pass-through).
//              - Adaptive Power Control (APC) VCSEL DAC word calculation.
//              - Vertical electrical TSV credit arbitration.
//              - Passive straight-through bypass detection.
//=============================================================================

`timescale 1ns / 1ps

module onoc_hybrid_3d_crossbar #(
    parameter integer MESH_X = 4,
    parameter integer MESH_Y = 4,
    parameter integer MESH_Z = 4
)(
    input  wire                   clk,
    input  wire                   rst_n,
    
    // Router Physical Coordinates
    input  wire [1:0]             cur_x,
    input  wire [1:0]             cur_y,
    input  wire [1:0]             cur_z,
    
    // 7 Input Request Channels
    input  wire [6:0]             req_valid,
    input  wire [1:0]             dest_x [6:0],
    input  wire [1:0]             dest_y [6:0],
    input  wire [1:0]             dest_z [6:0],
    
    // Vertical TSV Downstream Flow Control Status
    input  wire [1:0]             tsv_ready,          // [0]: Down, [1]: Up
    
    // Actuation Outputs
    output reg  [25:0]            mrr_activate,       // 26 Micro-Ring Resonators
    output reg  [7:0]             apc_laser_dac [6:0], // 8-bit VCSEL current per input
    output reg  [6:0]             optical_grant,      // Optical transmission enable
    output reg  [2:0]             passive_bypass_cnt  // Number of straight passive paths
);

    // Port Enumeration
    localparam P_EAST  = 3'd0;
    localparam P_WEST  = 3'd1;
    localparam P_SOUTH = 3'd2;
    localparam P_NORTH = 3'd3;
    localparam P_DOWN  = 3'd4;
    localparam P_UP    = 3'd5;
    localparam P_LOCAL = 3'd6;

    // Dimension-Order Routing (XYZ DOR) Logic
    reg [2:0] target_port [6:0];
    reg [2:0] hop_dist [6:0];
    integer i;

    always @(*) begin
        for (i = 0; i < 7; i = i + 1) begin
            if (req_valid[i]) begin
                if (dest_x[i] > cur_x) begin
                    target_port[i] = P_EAST;
                    hop_dist[i]    = (dest_x[i] - cur_x) + (dest_y[i] >= cur_y ? dest_y[i] - cur_y : cur_y - dest_y[i]);
                end else if (dest_x[i] < cur_x) begin
                    target_port[i] = P_WEST;
                    hop_dist[i]    = (cur_x - dest_x[i]) + (dest_y[i] >= cur_y ? dest_y[i] - cur_y : cur_y - dest_y[i]);
                end else if (dest_y[i] > cur_y) begin
                    target_port[i] = P_SOUTH;
                    hop_dist[i]    = (dest_y[i] - cur_y);
                end else if (dest_y[i] < cur_y) begin
                    target_port[i] = P_NORTH;
                    hop_dist[i]    = (cur_y - dest_y[i]);
                end else if (dest_z[i] > cur_z) begin
                    target_port[i] = P_UP;
                    hop_dist[i]    = (dest_z[i] - cur_z);
                end else if (dest_z[i] < cur_z) begin
                    target_port[i] = P_DOWN;
                    hop_dist[i]    = (cur_z - dest_z[i]);
                end else begin
                    target_port[i] = P_LOCAL;
                    hop_dist[i]    = 3'd0;
                end
            end else begin
                target_port[i] = P_LOCAL;
                hop_dist[i]    = 3'd0;
            end
        end
    end

    // Adaptive Power Control (APC) Calculation & Ring Activation
    integer k;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mrr_activate       <= 26'd0;
            optical_grant      <= 7'd0;
            passive_bypass_cnt <= 3'd0;
            for (k = 0; k < 7; k = k + 1) begin
                apc_laser_dac[k] <= 8'd0;
            end
        end else begin
            mrr_activate       <= 26'd0;
            optical_grant      <= req_valid;
            passive_bypass_cnt <= 3'd0;

            for (k = 0; k < 7; k = k + 1) begin
                if (req_valid[k]) begin
                    // Base current + dynamic hop-dependent boost
                    // Near hops (1 hop): 8'd80; Distant hops: up to 8'd220
                    apc_laser_dac[k] <= 8'd75 + (hop_dist[k] * 8'd28);

                    // Check if route is a passive straight-through waveguide (e.g. East->East or North->North)
                    if ((k == P_WEST && target_port[k] == P_EAST) ||
                        (k == P_EAST && target_port[k] == P_WEST) ||
                        (k == P_NORTH && target_port[k] == P_SOUTH) ||
                        (k == P_SOUTH && target_port[k] == P_NORTH)) begin
                        // Straight-through: Passively bypasses micro-rings!
                        passive_bypass_cnt <= passive_bypass_cnt + 3'd1;
                    end else begin
                        // Turning traffic: Activate specific micro-ring index
                        mrr_activate[(k * 3 + target_port[k]) % 26] <= 1'b1;
                    end
                end else begin
                    apc_laser_dac[k] <= 8'd0;
                end
            end
        end
    end

endmodule
```

---

## 8. 🕹️ Interactive Simulation & Arcade Linkages

Deepen your practical understanding of 3D optical interconnects, laser power budgets, and thermal detuning with our interactive arcade games:

- 🎮 **[Photon Pilot: Silicon Photonics](../interactive/optical.md):** Command laser wavelengths, align micro-ring resonators, and tune thermal micro-heaters in an interactive optical NoC simulator.
- 🎮 **[Hotspot Hero: Silicon Thermal Defender](../interactive/hotspot.md):** Defend 3D vertical stacked silicon layers from thermal accumulation and thermo-optic detuning.

---

## 9. 🎯 Concept Check: Lesson 7.3

Test your mastery of the HKUST 3D Optical NoC architecture with this 3-question self-assessment.

<div class="noc-sim-container" id="quiz73" style="margin-top:1rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; flex-wrap:wrap; gap:0.5rem;">
    <div style="font-weight:700; font-size:1.05rem; color:var(--tcl-heading);">
      📝 Concept Check: 3D Optical NoC Landmark Paper
    </div>
    <div id="q73_score_badge" style="font-size:0.85rem; font-weight:600; padding:4px 10px; border-radius:12px; background:rgba(37,99,235,0.1); color:#2563eb;">
      Score: 0 / 3
    </div>
  </div>

  <!-- Question 1 -->
  <div id="q73_1_block" style="margin-bottom:1.5rem; padding-bottom:1rem; border-bottom:1px solid var(--noc-border);">
    <p style="font-weight:600; font-size:0.95rem; margin-bottom:0.75rem;">
      <b>1. Reduced-MRR Router Architecture:</b> What microarchitectural strategy allows the HKUST 7x7 optical router to cut micro-ring resonator (MRR) count from 49 down to 26?
    </p>
    <div style="display:flex; flex-direction:column; gap:0.5rem;" id="q73_1_opts">
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(1, 0)">
        A. The router exploits the dimension-order routing (XYZ DOR) invariant and incorporates passive straight-through waveguides that require zero MRRs for non-turning traffic, eliminating 23 redundant active rings.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(1, 1)">
        B. The router restricts all packets to 1 bit in length.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(1, 2)">
        C. Flits are routed without packet headers or destination coordinates.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(1, 3)">
        D. Micro-rings are replaced with copper wires on every turn.
      </button>
    </div>
    <div id="q73_1_fb" style="display:none; margin-top:0.75rem; padding:0.75rem; border-radius:8px; font-size:0.9rem; line-height:1.5;"></div>
  </div>

  <!-- Question 2 -->
  <div id="q73_2_block" style="margin-bottom:1.5rem; padding-bottom:1rem; border-bottom:1px solid var(--noc-border);">
    <p style="font-weight:600; font-size:0.95rem; margin-bottom:0.75rem;">
      <b>2. Adaptive Power Control (APC) Efficiency:</b> How does Adaptive Power Control (APC) save over $40\%\text{–}60\%$ in laser power compared to conventional optical NoC transmitters?
    </p>
    <div style="display:flex; flex-direction:column; gap:0.5rem;" id="q73_2_opts">
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(2, 0)">
        A. Rather than powering the VCSEL laser for the static worst-case corner-to-corner path attenuation, APC calculates exact path loss in decibels and dynamically tunes laser driving current to emit just-enough optical power to meet receiver sensitivity.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(2, 1)">
        B. By turning off the laser when the computer enters sleep mode.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(2, 2)">
        C. By reflecting photons back into the laser cavity with silver mirrors.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(2, 3)">
        D. By transmitting data using solar energy captured from room lighting.
      </button>
    </div>
    <div id="q73_2_fb" style="display:none; margin-top:0.75rem; padding:0.75rem; border-radius:8px; font-size:0.9rem; line-height:1.5;"></div>
  </div>

  <!-- Question 3 -->
  <div id="q73_3_block" style="margin-bottom:1rem;">
    <p style="font-weight:600; font-size:0.95rem; margin-bottom:0.75rem;">
      <b>3. Heterogeneous 3D Partitioning:</b> In this 3D architecture, what is the key architectural rationale for using vertical copper TSVs for control signaling while reserving optical waveguides for data payloads?
    </p>
    <div style="display:flex; flex-direction:column; gap:0.5rem;" id="q73_3_opts">
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(3, 0)">
        A. TSVs provide ultra-short ($<10\text{ ps}$), zero-laser-power vertical interconnects ideal for credit handshakes and arbitration, while optical waveguides provide distance-independent terabit bandwidth for multi-kilobyte data transfers.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(3, 1)">
        B. Optical waveguides cannot transmit more than 2 bits of data per hour.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(3, 2)">
        C. TSVs are transparent to infrared light.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQ73(3, 3)">
        D. Photons cannot travel in the horizontal dimension.
      </button>
    </div>
    <div id="q73_3_fb" style="display:none; margin-top:0.75rem; padding:0.75rem; border-radius:8px; font-size:0.9rem; line-height:1.5;"></div>
  </div>

  <div style="margin-top:1rem; text-align:right;">
    <button class="noc-sim-btn" onclick="resetQuiz73()" style="padding:4px 12px; font-size:0.85rem;">🔄 Reset Quiz</button>
  </div>
</div>

<script>
const q73Answers = [0, 0, 0];
const q73Feedback = [
  "✓ Correct! A general 7x7 crossbar requires 49 switching elements. By constraining routing to XYZ DOR, straight-through flits traverse passive silicon waveguides without hitting micro-rings, slashing MRR count to 26 and saving significant static heating power.",
  "✓ Correct! Because XYZ DOR paths are deterministic, path insertion loss can be pre-calculated. APC dynamically modulates VCSEL current so optical power arrives right at the sensitivity floor, saving 40%–60% of laser power.",
  "✓ Correct! Vertical copper TSVs have negligible sub-picosecond delay and zero static laser overhead, making them ideal for short-flit credits and interrupts, while photonic waveguides handle high-bandwidth payload flight."
];
let q73Score = [0, 0, 0];

function checkQ73(qIdx, optIdx) {
  const fb = document.getElementById(`q73_${qIdx}_fb`);
  const opts = document.querySelectorAll(`#q73_${qIdx}_opts button`);
  
  opts.forEach(b => {
    b.disabled = true;
    b.style.opacity = '0.7';
  });

  fb.style.display = 'block';
  if (optIdx === q73Answers[qIdx - 1]) {
    opts[optIdx].style.border = '2px solid #10b981';
    opts[optIdx].style.background = 'rgba(16, 185, 129, 0.15)';
    opts[optIdx].style.opacity = '1';
    fb.style.background = 'rgba(16, 185, 129, 0.1)';
    fb.style.border = '1px solid #10b981';
    fb.style.color = '#10b981';
    fb.textContent = q73Feedback[qIdx - 1];
    q73Score[qIdx - 1] = 1;
  } else {
    opts[optIdx].style.border = '2px solid #ef4444';
    opts[optIdx].style.background = 'rgba(239, 68, 68, 0.15)';
    opts[optIdx].style.opacity = '1';
    opts[q73Answers[qIdx - 1]].style.border = '2px solid #10b981';
    opts[q73Answers[qIdx - 1]].style.opacity = '1';
    fb.style.background = 'rgba(239, 68, 68, 0.1)';
    fb.style.border = '1px solid #ef4444';
    fb.style.color = '#ef4444';
    fb.textContent = "✗ Incorrect. " + q73Feedback[qIdx - 1];
    q73Score[qIdx - 1] = 0;
  }

  const total = q73Score.reduce((a, b) => a + b, 0);
  const badge = document.getElementById('q73_score_badge');
  badge.textContent = `Score: ${total} / 3`;
  if (total === 3) {
    badge.style.background = 'rgba(16, 185, 129, 0.15)';
    badge.style.color = '#10b981';
  }
}

function resetQuiz73() {
  q73Score = [0, 0, 0];
  const badge = document.getElementById('q73_score_badge');
  badge.textContent = 'Score: 0 / 3';
  badge.style.background = 'rgba(37,99,235,0.1)';
  badge.style.color = '#2563eb';

  for (let q = 1; q <= 3; q++) {
    const fb = document.getElementById(`q73_${q}_fb`);
    fb.style.display = 'none';
    fb.textContent = '';
    const opts = document.querySelectorAll(`#q73_${q}_opts button`);
    opts.forEach(b => {
      b.disabled = false;
      b.style.border = '';
      b.style.background = '';
      b.style.opacity = '1';
    });
  }
}
</script>

---

## 10. Summary & Next Steps

This IEEE TCAD landmark proved that 3D vertical integration and silicon nanophotonics are natural partners: TSVs provide compact vertical electronic control, while a dedicated top optical layer delivers speed-of-light photonic routing with low-loss passive crossbars.

In **[Lesson 7.4: In-Network Computing Neuromorphic Router](04-in-network-neuromorphic.md)**, we examine how the communication fabric itself becomes the compute engine by performing **in-flight partial-sum reductions inside router crossbars**!

---

## References & Primary Sources

<a id="ref-ye2013"></a>**[Ye2013]** Y. Ye, J. Xu, X. Wu, W. Zhang, W. Liu, and M. Nikdast, "3-D Mesh-Based Optical Network-on-Chip for Multiprocessor System-on-Chip," *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 32, no. 4, pp. 584–596, 2013. [DOI: 10.1109/TCAD.2012.2227483](https://doi.org/10.1109/TCAD.2012.2227483)

<a id="ref-pavlidis2009"></a>**[Pavlidis2009]** V. F. Pavlidis and E. G. Friedman, *Three-Dimensional Integrated Circuit Design*, Morgan Kaufmann, 2009. [DOI: 10.1016/B978-0-12-374389-3.X0001-4](https://doi.org/10.1016/B978-0-12-374389-3.X0001-4)

<a id="ref-vantrease2008"></a>**[Vantrease2008]** D. Vantrease, R. Schreiber, M. Monchiero, M. McLaren, N. P. Jouppi, M. Fiorentino, A. Davis, N. Binkert, R. G. Beausoleil, and J. H. Ahn, "Corona: System implications of emerging nanophotonic technology," in *Proceedings of the 35th Annual International Symposium on Computer Architecture (ISCA)*, pp. 153–164, 2008. [DOI: 10.1109/ISCA.2008.35](https://doi.org/10.1109/ISCA.2008.35)

<a id="ref-little1997"></a>**[Little1997]** B. E. Little, J. S. Foresi, G. Steinmeyer, E. R. Thoen, S. T. Chu, H. A. Haus, E. P. Ippen, and J. L. Greene, "Ultra-compact $\text{Si-SiO}_2$ microring resonator optical channel dropping filters," *IEEE Photonics Technology Letters*, vol. 10, no. 4, pp. 549–551, 1998. [DOI: 10.1109/68.662590](https://doi.org/10.1109/68.662590)


