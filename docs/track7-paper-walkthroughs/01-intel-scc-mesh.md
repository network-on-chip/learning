# 7.1 The Manycore Milestone: Intel 48-Core Single-Chip Cloud Computer (SCC)

| Paper Details | Primary Reference |
| :--- | :--- |
| **Title** | *A 2-TB/s 6×4 Mesh Network for a Single-Chip Cloud Computer with DVFS in 45-nm CMOS* |
| **Authors** | P. Salihundam, S. Jain, T. Jacob, S. Kumar, V. Erraguntla, Y. Hoskote, S. Vangal, G. Ruhl, N. Borkar |
| **Venue** | **IEEE Journal of Solid-State Circuits (JSSC)**, Vol. 46, No. 4, April 2011 |
| **Repository Paper** | 📂 [`papers/a-2-tb-s-6-times-4-mesh-network-for-a-single-chip-cloud-computer-with-dvfs-in-45-nm-cmos/`](https://github.com/network-on-chip/noc-lab/tree/main/papers/a-2-tb-s-6-times-4-mesh-network-for-a-single-chip-cloud-computer-with-dvfs-in-45-nm-cmos) |

---

## 1. The Historical Challenge: Breaking the Cache Coherence Wall

In 2009, multi-core processors were hitting a scalability brick wall. Desktop and server CPUs scaled from 2 to 4 to 8 cores using snooping buses and centralized crossbars. However, attempting to scale hardware cache coherence (MESI/MOESI directories) to **48 or 100 cores** resulted in exponential coherence traffic, directory area explosions, and catastrophic power consumption.

Intel Labs embarked on a landmark experimental project: the **Single-Chip Cloud Computer (SCC)**.
Instead of treating on-chip cores as a tightly-coupled shared-memory multiprocessor with hardware cache coherence, Intel treated the chip as an **on-die datacenter cluster** (a "Cloud on a Chip"). 48 independent Pentium-class IA-32 cores communicate strictly via a high-speed **packet-switched 2D Mesh Network-on-Chip**.

```mermaid
graph TD
  subgraph SCC_Die ["Intel SCC Die (567 mm², 45nm CMOS, 1.3 Billion Transistors)"]
    direction TB
    subgraph Grid ["6x4 2D Mesh Topology (24 Tiles)"]
      T00["Tile (0,0)"] --- T10["Tile (1,0)"] --- T20["Tile (2,0)"] --- T30["Tile (3,0)"] --- T40["Tile (4,0)"] --- T50["Tile (5,0)"]
      T01["Tile (0,1)"] --- T11["Tile (1,1)"] --- T21["Tile (2,1)"] --- T31["Tile (3,1)"] --- T41["Tile (4,1)"] --- T51["Tile (5,1)"]
      T02["Tile (0,2)"] --- T12["Tile (1,2)"] --- T22["Tile (2,2)"] --- T32["Tile (3,2)"] --- T42["Tile (4,2)"] --- T52["Tile (5,2)"]
      T03["Tile (0,3)"] --- T13["Tile (1,3)"] --- T23["Tile (2,3)"] --- T33["Tile (3,3)"] --- T43["Tile (4,3)"] --- T53["Tile (5,3)"]
      
      T00 --- T01 --- T02 --- T03
      T10 --- T11 --- T12 --- T13
      T20 --- T21 --- T22 --- T23
      T30 --- T31 --- T32 --- T33
      T40 --- T41 --- T42 --- T43
      T50 --- T51 --- T52 --- T53
    end
  end
```

---

## 2. Microarchitecture of the SCC Tile & Router

The SCC floorplan integrates **24 dual-core tiles** in a $6 \times 4$ 2D mesh:

```mermaid
graph LR
  subgraph Tile ["SCC Dual-Core Tile Architecture"]
    Core0["IA-32 Core 0<br/>+ 256 KB L2"]
    Core1["IA-32 Core 1<br/>+ 256 KB L2"]
    MPB["16 KB Message Passing Buffer (MPB)<br/>Fast Local SRAM"]
    NI["Network Interface (NI)"]
    Router["5-Port 2D Mesh Router<br/>(N, S, E, W, Local)"]

    Core0 & Core1 <--> MPB
    Core0 & Core1 <--> NI
    MPB <--> NI
    NI <--> Router
  end
```

### Key Silicon Specifications:
- **Process Technology:** $45 \ \text{nm}$ Hi-K Metal Gate CMOS.
- **Die Size:** $567 \ \text{mm}^2$ containing $1.3 \ \text{Billion}$ transistors.
- **Fabric Bandwidth:** **$2.0 \ \text{Terabits/sec}$ ($256 \ \text{GB/s}$)** bisection bandwidth at $2.0 \ \text{GHz}$ ($1.1 \ \text{V}$).
- **Link Width:** $16 \ \text{Bytes}$ ($128 \ \text{bits}$) data $+ 16 \ \text{bits}$ sideband/credit per direction.
- **Physical Wire Length:** $5.4 \ \text{mm}$ inter-router links spanning between adjacent tiles.

---

### The 4-Cycle Low-Latency Router Pipeline

To minimize packet transit delay across the large $567 \ \text{mm}^2$ die, the SCC router employs an aggressive **4-stage pipeline** with **route pre-computation** and **speculative early buffer writing**:

```
 Cycle 1            Cycle 2            Cycle 3            Cycle 4
[ Link Traversal & ]  [ Route Compute &  ]  [ Switch Allocation ]  [ Crossbar Traversal ]
[ Speculative Write]  [ VC Allocation   ]  [ (Wrapped WFA)     ]  [ to Output Channel  ]
```

```mermaid
graph LR
  C1["Cycle 1: Link Traversal & Speculative Buffer Write"] --> C2["Cycle 2: Lookahead Routing & VC Allocation"]
  C2 --> C3["Cycle 3: Wrapped Wave-Front Allocation (WWFA)"]
  C3 --> C4["Cycle 4: 5x5 Crossbar Switch Traversal"]
```

1. **Cycle 1 (Link Traversal + Speculative Write):** Flits traverse the $5.4 \ \text{mm}$ inter-tile link and write directly into the input FIFO based on speculative write pointers, eliminating arrival dependency checks.
2. **Cycle 2 (Route Pre-Computation):** Using Lookahead Routing ([Lesson 2.1](../track2-router-architecture/01-pipeline-stages.md)), the output port for hop $N+1$ is computed during hop $N$.
3. **Cycle 3 (Wrapped Wave-Front Allocation - WWFA):** A specialized single-cycle 2D wave-front arbiter matches 5 input ports to 5 output ports concurrently, sustaining over **$90\%$ crossbar utilization**.
4. **Cycle 4 (Crossbar Switch Traversal):** The 128-bit flit traverses the crossbar matrix directly into the output link driver.

---

## 3. The Message Passing Buffer (MPB) Innovation

How did Intel bypass the cache coherence directory bottleneck?

Instead of maintaining cache lines coherent in hardware across 48 cores, each tile embeds a dedicated **$16 \ \text{KB}$ Message Passing Buffer (MPB)**:
- The MPB is a high-speed local SRAM visible to all cores via a global physical address window.
- When Core 0 on Tile $(0, 0)$ wants to send data to Core 15 on Tile $(3, 2)$, it writes payload cache lines directly into its local MPB and sends an ultra-short interrupt packet across the NoC.
- Core 15 reads the message directly across the mesh or copies it to its local cache.
- **Result:** Zero directory state overhead, zero false-sharing cache invalidation storms, and deterministic microsecond message passing!

---

## 4. Fine-Grained DVFS & Voltage Islands

The SCC paper was one of the earliest silicon demonstrations of **per-tile Dynamic Voltage and Frequency Scaling (DVFS)**:

```mermaid
graph TD
  subgraph Power_Domains ["Intel SCC Voltage & Frequency Domains"]
    V_Mesh["Router Mesh Power Domain (V_mesh = 1.1 V, f_mesh = 2.0 GHz)"]
    V_Tile0["Tile 0 Domain (V_0 = 0.7 V, f_0 = 400 MHz)"]
    V_Tile1["Tile 1 Domain (V_1 = 1.14 V, f_1 = 1.6 GHz - Turbo)"]
    V_Tile2["Tile 2 Domain (V_2 = 0.9 V, f_2 = 800 MHz)"]
  end
```

- **Independent Mesh Domain:** The router network operates on a dedicated voltage domain ($1.1 \ \text{V}$) and clock grid ($2.0 \ \text{GHz}$) to guarantee that communication channels never throttle, even if individual CPU cores sleep.
- **6 Separate Voltage Domains:** Dual-core tiles are grouped into 6 voltage regulators ($0.7 \ \text{V}$ to $1.14 \ \text{V}$).
- **24 Separate Frequency Domains:** Each individual tile controls its own clock frequency ($100 \ \text{MHz}$ to $1.6 \ \text{GHz}$) via on-die phase-locked loops (PLLs).
- **Clock Domain Crossing (CDC):** The Network Interface (NI) incorporates asynchronous dual-clock FIFOs to smoothly bridge the variable tile core clock ($f_{core}$) and the fixed $2.0 \ \text{GHz}$ mesh clock ($f_{mesh}$).

---

## 5. Interactive Intel SCC 48-Core Mesh Simulator

Explore Intel's $6 \times 4$ SCC processor below. Click on individual tiles to inspect core frequencies and voltage levels, adjust the global mesh frequency and core workloads, and observe total power dissipation and bisection bandwidth in real time!

<div style="background:var(--md-code-bg-color); border:1px solid var(--md-default-fg-color--lightest); border-radius:8px; padding:20px; margin:24px 0;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
    <h3 style="margin:0; font-size:1.15rem; color:var(--md-typeset-color);">⚡ Intel 48-Core SCC Mesh & DVFS Power Simulator</h3>
    <div style="display:flex; gap:8px;">
      <button onclick="setWorkload('idle')" style="padding:4px 10px; border-radius:4px; background:#1e293b; color:#cbd5e1; border:1px solid #475569; cursor:pointer;">Idle (25W)</button>
      <button onclick="setWorkload('balanced')" style="padding:4px 10px; border-radius:4px; background:#0284c7; color:#fff; border:1px solid #0284c7; cursor:pointer;">Balanced (65W)</button>
      <button onclick="setWorkload('turbo')" style="padding:4px 10px; border-radius:4px; background:#ef4444; color:#fff; border:1px solid #ef4444; cursor:pointer;">Turbo Peak (125W)</button>
    </div>
  </div>

  <div style="display:grid; grid-template-columns:1fr 280px; gap:20px; align-items:start;">
    <div>
      <canvas id="canvasSCC" width="600" height="380" style="width:100%; height:auto; background:#0f172a; border-radius:6px; display:block; cursor:pointer;"></canvas>
      <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:0.85rem; color:var(--md-default-fg-color--light);">
        <span>💡 Click on any tile to toggle its DVFS power state</span>
        <span id="txt-bisection" style="font-weight:700; color:#38bdf8;">Bisection BW: 256 GB/s</span>
      </div>
    </div>

    <div style="background:rgba(15,23,42,0.6); padding:16px; border-radius:6px; border:1px solid rgba(255,255,255,0.08); font-size:0.85rem;">
      <div style="font-weight:700; color:#38bdf8; margin-bottom:12px; font-size:0.95rem;">📊 Silicon Metrics & Telemetry</div>

      <div style="margin-bottom:12px;">
        <div style="font-size:0.8rem; color:#94a3b8;">Total Chip Power Dissipation:</div>
        <div id="txt-total-pwr" style="font-size:1.4rem; font-weight:800; color:#10b981;">62.4 Watts</div>
      </div>

      <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:10px; margin-bottom:12px;">
        <div style="font-size:0.8rem; color:#94a3b8;">Selected Tile Telemetry:</div>
        <div id="txt-tile-info" style="font-family:monospace; font-size:0.8rem; color:#e2e8f0; line-height:1.5; margin-top:4px;">
          Tile: (2, 1)<br/>
          Cores: Core 10 & 11<br/>
          Voltage: 1.00 V<br/>
          Frequency: 1.0 GHz<br/>
          Tile Power: 2.4 W
        </div>
      </div>

      <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">
        <label style="display:block; font-size:0.8rem; margin-bottom:4px; color:#94a3b8;">Router Mesh Frequency ($f_{mesh}$):</label>
        <select id="sel-mesh-clk" onchange="updateSCCSim()" style="width:100%; padding:4px 8px; border-radius:4px; background:#1e293b; color:#fff; border:1px solid #475569;">
          <option value="1.0">1.0 GHz (128 GB/s Bisection, 0.9V)</option>
          <option value="1.6">1.6 GHz (204 GB/s Bisection, 1.0V)</option>
          <option value="2.0" selected>2.0 GHz (256 GB/s Bisection, 1.1V - Max)</option>
        </select>
      </div>
    </div>
  </div>
</div>

<script>
(function() {
  const canvas = document.getElementById('canvasSCC');
  const ctx = canvas.getContext('2d');

  // 6 columns x 4 rows
  const COLS = 6;
  const ROWS = 4;
  const tiles = [];
  let selectedTile = { x: 2, y: 1 };

  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      tiles.push({
        x: x,
        y: y,
        state: 'balanced', // 'idle', 'balanced', 'turbo'
        v: 1.0,
        f: 1.0
      });
    }
  }

  canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const mx = (e.clientX - rect.left) * scaleX;
    const my = (e.clientY - rect.top) * scaleY;

    // Tile bounding boxes
    const padX = 40, padY = 40;
    const tileW = 75, tileH = 65;
    const gapX = 14, gapY = 16;

    for (let t of tiles) {
      const tx = padX + t.x * (tileW + gapX);
      const ty = padY + t.y * (tileH + gapY);
      if (mx >= tx && mx <= tx + tileW && my >= ty && my <= ty + tileH) {
        selectedTile = { x: t.x, y: t.y };
        // Cycle state
        if (t.state === 'idle') t.state = 'balanced';
        else if (t.state === 'balanced') t.state = 'turbo';
        else t.state = 'idle';
        updateTileParams(t);
        updateSCCSim();
        return;
      }
    }
  });

  function updateTileParams(t) {
    if (t.state === 'idle') { t.v = 0.7; t.f = 0.4; }
    else if (t.state === 'balanced') { t.v = 1.0; t.f = 1.0; }
    else if (t.state === 'turbo') { t.v = 1.14; t.f = 1.6; }
  }

  window.setWorkload = function(mode) {
    for (let t of tiles) {
      t.state = mode;
      updateTileParams(t);
    }
    updateSCCSim();
  };

  window.updateSCCSim = function() {
    const meshClk = parseFloat(document.getElementById('sel-mesh-clk').value);
    // Bisection BW: 4 links across the 6x4 cut * 2 directions * 16 bytes * f_mesh
    // 4 links * 32 B/cycle = 128 B/cycle * 2 GHz = 256 GB/s
    const bisectionGBs = 4 * 32 * meshClk;
    document.getElementById('txt-bisection').textContent = 'Bisection BW: ' + Math.round(bisectionGBs) + ' GB/s (' + (bisectionGBs * 8 / 1000).toFixed(1) + ' Tb/s)';

    // Compute total power: Mesh router baseline + sum of 24 tiles
    // Mesh baseline: 12W at 2.0 GHz
    const pMesh = 12.0 * (meshClk / 2.0);
    let pTiles = 0;

    for (let t of tiles) {
      // Dynamic power: P = C * V^2 * f
      // Tile power: 0.8W (idle), 2.2W (balanced), 4.8W (turbo)
      let pt = 0;
      if (t.state === 'idle') pt = 0.75;
      else if (t.state === 'balanced') pt = 2.2;
      else if (t.state === 'turbo') pt = 4.8;
      pTiles += pt;
    }

    const totalPwr = pMesh + pTiles;
    const pwrEl = document.getElementById('txt-total-pwr');
    pwrEl.textContent = totalPwr.toFixed(1) + ' Watts';
    pwrEl.style.color = totalPwr > 100 ? '#ef4444' : (totalPwr > 60 ? '#f59e0b' : '#10b981');

    // Update selected tile display
    const sel = tiles.find(t => t.x === selectedTile.x && t.y === selectedTile.y);
    if (sel) {
      const core0 = (sel.y * 6 + sel.x) * 2;
      const core1 = core0 + 1;
      let pt = sel.state === 'idle' ? 0.75 : (sel.state === 'balanced' ? 2.2 : 4.8);
      document.getElementById('txt-tile-info').innerHTML = `
        Tile: (${sel.x}, ${sel.y}) [${sel.state.toUpperCase()}]<br/>
        Cores: Core ${core0} & ${core1}<br/>
        Voltage: ${sel.v.toFixed(2)} V<br/>
        Frequency: ${sel.f.toFixed(1)} GHz<br/>
        Tile Power: ${pt.toFixed(2)} W
      `;
    }

    renderSCC();
  };

  function renderSCC() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const padX = 40, padY = 40;
    const tileW = 75, tileH = 65;
    const gapX = 14, gapY = 16;

    // Draw mesh interconnect links
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.45)';
    ctx.lineWidth = 3;

    // Horizontal links
    for (let y = 0; y < ROWS; y++) {
      for (let x = 0; x < COLS - 1; x++) {
        const x1 = padX + x * (tileW + gapX) + tileW;
        const y1 = padY + y * (tileH + gapY) + tileH / 2;
        const x2 = padX + (x + 1) * (tileW + gapX);
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y1);
        ctx.stroke();
      }
    }

    // Vertical links
    for (let x = 0; x < COLS; x++) {
      for (let y = 0; y < ROWS - 1; y++) {
        const x1 = padX + x * (tileW + gapX) + tileW / 2;
        const y1 = padY + y * (tileH + gapY) + tileH;
        const y2 = padY + (y + 1) * (tileH + gapY);
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x1, y2);
        ctx.stroke();
      }
    }

    // Draw tiles
    for (let t of tiles) {
      const tx = padX + t.x * (tileW + gapX);
      const ty = padY + t.y * (tileH + gapY);

      const isSelected = (t.x === selectedTile.x && t.y === selectedTile.y);

      // Color coding based on state
      let fill = '#1e293b';
      let border = '#475569';
      if (t.state === 'idle') { fill = 'rgba(2, 132, 199, 0.15)'; border = '#0284c7'; }
      else if (t.state === 'balanced') { fill = 'rgba(16, 185, 129, 0.2)'; border = '#10b981'; }
      else if (t.state === 'turbo') { fill = 'rgba(239, 68, 68, 0.25)'; border = '#ef4444'; }

      ctx.fillStyle = fill;
      ctx.fillRect(tx, ty, tileW, tileH);

      ctx.strokeStyle = isSelected ? '#ffffff' : border;
      ctx.lineWidth = isSelected ? 2.5 : 1.5;
      ctx.strokeRect(tx, ty, tileW, tileH);

      // Text inside tile
      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 10px Inter, sans-serif';
      ctx.fillText(`Tile (${t.x},${t.y})`, tx + 6, ty + 15);

      ctx.fillStyle = '#94a3b8';
      ctx.font = '9px Inter, sans-serif';
      ctx.fillText(`${t.f.toFixed(1)} GHz`, tx + 6, ty + 30);
      ctx.fillText(`${t.v.toFixed(2)} V`, tx + 6, ty + 44);

      // Central router dot
      ctx.beginPath();
      ctx.arc(tx + tileW - 12, ty + 14, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#38bdf8';
      ctx.fill();
    }
  }

  updateSCCSim();
})();
</script>

---

## 6. Worked Numerical Problem: SCC Bisection Bandwidth

### Problem Statement
From the published silicon measurements in Intel's 2011 JSSC paper:
The SCC on-chip fabric is a $6 \times 4$ 2D mesh router network. Each inter-router physical link operates at clock frequency $f_{mesh} = 2.0 \ \text{GHz}$ and carries a **$16\text{-Byte}$ ($128\text{-bit}$)** flit payload per cycle in each direction.

1. **Calculate the bisection bandwidth of the $6 \times 4$ mesh across the vertical network bisection cut.**
2. **If an IA-32 core executes a cache miss requiring a 32-Byte cache line transfer across 3 hops, calculate the minimum packet serialization latency.**
3. **If the router network consumes $12.0 \ \text{W}$ at $2.0 \ \text{GHz}$ ($1.1 \ \text{V}$), calculate the energy efficiency per flit hop in picojoules ($\text{pJ/bit}$).**

---

### Step-by-Step Solution

#### Step 1: Bisection Bandwidth Across the Cut
In a $6 \times 4$ 2D mesh, cutting the network in half vertically divides the 6 columns into two $3 \times 4$ sub-meshes.
The number of parallel bidirectional physical links crossing this bisection cut is equal to the number of rows:

$$N_{cut\_links} = 4 \ \text{links}$$

Each link transmits in both directions ($2 \times 16 \ \text{Bytes/cycle} = 32 \ \text{Bytes/cycle}$).
At $f_{mesh} = 2.0 \ \text{GHz}$ ($2.0 \times 10^9 \ \text{cycles/sec}$):

$$\text{Bisection Bandwidth} = 4 \times (32 \ \text{Bytes/cycle}) \times (2.0 \times 10^9 \ \text{cycles/sec})$$

$$\text{Bisection Bandwidth} = 256 \times 10^9 \ \text{Bytes/sec} = \mathbf{256 \ \text{GB/s}} = \mathbf{2.048 \ \text{Terabits/sec}}$$

This confirms Intel’s headline claim of **$2.0 \ \text{Tb/s}$ bisection bandwidth**!

#### Step 2: 32-Byte Cache Line Serialization
A 32-Byte packet payload plus an 8-Byte routing header yields a total packet size:

$$S_{packet} = 32 \ \text{Bytes} + 8 \ \text{Bytes} = 40 \ \text{Bytes}$$

Because each flit carries $16 \ \text{Bytes}$:

$$N_{flits} = \left\lceil \frac{40 \ \text{Bytes}}{16 \ \text{Bytes/flit}} \right\rceil = 3 \ \text{flits}$$

At $2.0 \ \text{GHz}$ ($0.5 \ \text{ns/cycle}$), serializing 3 flits into the network interface consumes:

$$t_{serial} = 3 \ \text{cycles} \times 0.5 \ \text{ns} = \mathbf{1.5 \ \text{ns}}$$

#### Step 3: Router Energy Efficiency
The 24 routers together dissipate $12.0 \ \text{W}$. The power per router is:

$$P_{router} = \frac{12.0 \ \text{W}}{24} = 0.50 \ \text{W/router} \ (500 \ \text{mW})$$

At full saturation, each 5-port router can switch up to 5 incoming flits of 128 bits every cycle ($5 \times 128 = 640 \ \text{bits/cycle}$):

$$\text{Throughput} = 640 \ \text{bits/cycle} \times (2.0 \times 10^9 \ \text{cycles/s}) = 1.28 \ \text{Tbps/router}$$

$$\text{Energy per bit} = \frac{0.50 \ \text{Joules/sec}}{1.28 \times 10^{12} \ \text{bits/sec}} \approx 0.39 \times 10^{-12} \ \text{J/bit} = \mathbf{0.39 \ \text{pJ/bit/hop}}$$

---

## 7. Self-Assessment Concept Check

<div style="background:var(--md-code-bg-color); border:1px solid var(--md-default-fg-color--lightest); border-radius:8px; padding:20px; margin:24px 0;">
  <div style="font-weight:700; font-size:1.05rem; margin-bottom:12px; color:var(--md-typeset-color);">
    Question 1: Why did Intel's SCC architecture employ on-die Message Passing Buffers (MPBs) instead of a monolithic hardware MESI/MOESI cache coherence directory across its 48 cores?
  </div>
  <div style="display:flex; flex-direction:column; gap:8px;">
    <label style="cursor:pointer;"><input type="radio" name="q1" value="a"> A) The IA-32 instruction set does not support load and store operations.</label>
    <label style="cursor:pointer;"><input type="radio" name="q1" value="b"> B) Directory-based hardware cache coherence introduces exponential messaging traffic, directory area explosions, and high power dissipation when scaling past 16–32 cores.</label>
    <label style="cursor:pointer;"><input type="radio" name="q1" value="c"> C) 45nm silicon cannot fabricate SRAM cells.</label>
  </div>
  <button onclick="checkQ1()" style="margin-top:12px; padding:6px 14px; border-radius:4px; background:#0284c7; color:#fff; border:none; cursor:pointer; font-weight:600;">Check Answer</button>
  <div id="q1-feedback" style="margin-top:10px; font-size:0.9rem; font-weight:600;"></div>
</div>

<div style="background:var(--md-code-bg-color); border:1px solid var(--md-default-fg-color--lightest); border-radius:8px; padding:20px; margin:24px 0;">
  <div style="font-weight:700; font-size:1.05rem; margin-bottom:12px; color:var(--md-typeset-color);">
    Question 2: In the SCC 4-stage router pipeline, what architectural technique allows the router to achieve a 2.0 ns per-hop latency while sustaining >90% switch utilization?
  </div>
  <div style="display:flex; flex-direction:column; gap:8px;">
    <label style="cursor:pointer;"><input type="radio" name="q2" value="a"> A) Lookahead routing and speculative early buffer writing coupled with a single-cycle Wrapped Wave-Front Allocator (WWFA).</label>
    <label style="cursor:pointer;"><input type="radio" name="q2" value="b"> B) Dropping packets whenever an output port experiences contention.</label>
    <label style="cursor:pointer;"><input type="radio" name="q2" value="c"> C) Operating the crossbar on analog optical signals.</label>
  </div>
  <button onclick="checkQ2()" style="margin-top:12px; padding:6px 14px; border-radius:4px; background:#0284c7; color:#fff; border:none; cursor:pointer; font-weight:600;">Check Answer</button>
  <div id="q2-feedback" style="margin-top:10px; font-size:0.9rem; font-weight:600;"></div>
</div>

<script>
function checkQ1() {
  const sel = document.querySelector('input[name="q1"]:checked');
  const fb = document.getElementById('q1-feedback');
  if (!sel) { fb.innerHTML = '<span style="color:#f59e0b;">Please select an option.</span>'; return; }
  if (sel.value === 'b') {
    fb.innerHTML = '<span style="color:#10b981;">✓ Correct! Maintaining full hardware cache coherence across 48 cores creates severe invalidation storms and massive directory overhead. Intel’s message-passing architecture treats the chip as a distributed cluster, scaling cleanly.</span>';
  } else {
    fb.innerHTML = '<span style="color:#ef4444;">✗ Incorrect. The SCC abandoned monolithic hardware cache coherence to eliminate directory scaling bottlenecks and invalidation overhead across 48 cores.</span>';
  }
}

function checkQ2() {
  const sel = document.querySelector('input[name="q2"]:checked');
  const fb = document.getElementById('q2-feedback');
  if (!sel) { fb.innerHTML = '<span style="color:#f59e0b;">Please select an option.</span>'; return; }
  if (sel.value === 'a') {
    fb.innerHTML = '<span style="color:#10b981;">✓ Correct! By computing the next hop in advance (lookahead) and writing flits speculatively into FIFOs, the router hides arbitration and queuing overhead, completing switch matching in a single-cycle WWFA.</span>';
  } else {
    fb.innerHTML = '<span style="color:#ef4444;">✗ Incorrect. The SCC router achieves 2 ns per-hop latency via lookahead routing, speculative early buffer write, and a single-cycle Wrapped Wave-Front Allocator.</span>';
  }
}
</script>

---

## 8. Summary & Next Steps

Intel’s 48-Core Single-Chip Cloud Computer demonstrated that a packet-switched 2D mesh combined with tile-level DVFS and message passing can scale manycore architectures to commercial reality.

In **[Lesson 7.2: The Multi-Chiplet Revolution: NVIDIA Simba](02-nvidia-simba-mcm.md)**, we examine how NVIDIA scaled deep learning acceleration across **36 chiplets** using Ground-Referenced Signaling (GRS) and hierarchical on-package networks!
