# 3.2 Indirect & Concentrated Networks: Fat-Trees & cMesh

While direct 2D meshes are standard for homogeneous multicore processors, large-scale chip multi-processors, heterogeneous AI accelerators, and high-bandwidth memory hierarchies often require higher bisection bandwidth, multi-path diversity, or significantly lower hop delays.

In this lesson, we study two primary architectural alternatives to planar direct meshes:
1. **Indirect Topologies (Fat-Trees & Clos Networks):** Dedicated switching elements separated from compute nodes.
2. **Concentrated Mesh (cMesh):** Clustering multiple compute cores around high-radix routers to slash network diameter and router silicon area.

---

## 1. Indirect Topologies: Butterfly, Clos, and Fat-Trees

In an **Indirect Topology**, routers are divided into dedicated intermediate switching elements. Compute cores, GPUs, and memory controllers connect exclusively to the periphery or leaf switches of the network:

```mermaid
graph TD
  subgraph Indirect_FatTree ["2-Level Full Bisection Fat-Tree (Spine-Leaf)"]
    Spine0["Spine Switch 0"] & Spine1["Spine Switch 1"]
    
    Leaf0["Leaf Switch 0"]
    Leaf1["Leaf Switch 1"]
    Leaf2["Leaf Switch 2"]
    Leaf3["Leaf Switch 3"]

    Spine0 === Leaf0 & Leaf1 & Leaf2 & Leaf3
    Spine1 === Leaf0 & Leaf1 & Leaf2 & Leaf3

    T0["Tile 0"] & T1["Tile 1"] --- Leaf0
    T2["Tile 2"] & T3["Tile 3"] --- Leaf1
    T4["Tile 4"] & T5["Tile 5"] --- Leaf2
    T6["Tile 6"] & T7["Tile 7"] --- Leaf3
  end

  style Spine0 fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px;
  style Spine1 fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px;
  style Leaf0 fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px;
  style Leaf1 fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px;
  style Leaf2 fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px;
  style Leaf3 fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px;
```

### Architectural Classification of Multistage Networks:
1. **Butterfly Networks:**  
   A multistage interconnection network (MIN) where a single unique path connects each source to each destination. While hardware cost is minimal ($O(N \log N)$ switches), butterfly networks have **zero path diversity**—a single congested link blocks all communication sharing that path.
2. **Clos Networks (Charles Clos, 1953):**  
   Multi-stage crossbar networks that provide multiple parallel middle-stage switches. A 3-stage Clos network is strictly non-blocking if the number of middle switches $m \ge 2n - 1$ (where $n$ is the number of inputs per first-stage switch).
3. **Fat-Trees (Charles Leiserson, 1985):**  
   In a conventional tree, bandwidth constricts near the root, creating a massive throughput bottleneck. In a **Fat-Tree**, channel capacity increases monotonically as you ascend toward the root switches. In a **Full Bisection Fat-Tree**, the bisection bandwidth is identical at every tier, enabling full line-rate communication across arbitrary permutations.

---

## 2. Concentrated Mesh (cMesh)

In a conventional 2D mesh, every compute tile contains its own dedicated router:

$$\text{Standard 2D Mesh: } 1\text{ Tile} = 1\text{ Router} \quad (N\text{ Cores} = N\text{ Routers})$$

For a 64-core CMP, this demands **64 routers**, each with input FIFO buffers, matrix arbiters, and clock distribution networks consuming silicon area and leakage power.

In a **Concentrated Mesh (cMesh)** (introduced by James Balfour and William J. Dally at ASPLOS 2006), **$C = 4\text{ neighboring compute cores}$ share a single centralized high-radix router**:

```mermaid
graph TD
  subgraph Concentrated_Cluster ["Concentrated Router Tile (C = 4 Cores)"]
    CR["High-Radix cMesh Router<br/>(4 Local Ports + 4 Network Links = 8 Ports)"]
    Core0["Core 0<br/>(CPU / L2)"] <--> CR
    Core1["Core 1<br/>(CPU / L2)"] <--> CR
    Core2["Core 2<br/>(CPU / L2)"] <--> CR
    Core3["Core 3<br/>(CPU / L2)"] <--> CR
  end

  CR <===>|"North Link"| CR_N["North cMesh Router"]
  CR <===>|"East Link"| CR_E["East cMesh Router"]
  CR <===>|"South Link"| CR_S["South cMesh Router"]
  CR <===>|"West Link"| CR_W["West cMesh Router"]

  style CR fill:#fef3c7,stroke:#f59e0b,stroke-width:2px;
  style Core0 fill:#e0f2fe,stroke:#0284c7,stroke-width:1.5px;
  style Core1 fill:#e0f2fe,stroke:#0284c7,stroke-width:1.5px;
  style Core2 fill:#e0f2fe,stroke:#0284c7,stroke-width:1.5px;
  style Core3 fill:#e0f2fe,stroke:#0284c7,stroke-width:1.5px;
```

---

### Why cMesh Outperforms Standard Meshes for Manycores:

#### A. 75% Reduction in Router Count
A 64-core processor requires **only 16 routers** in a $4 \times 4$ cMesh grid, compared to 64 routers in an $8 \times 8$ standard mesh!
- Slashes total buffer SRAM area by over **50%**.
- Significantly reduces clock tree synthesis complexity and dynamic clock power.

#### B. Network Diameter Slashed by 57%
- **Standard $8 \times 8$ Mesh Diameter:** $D = 2 \times (8 - 1) = \mathbf{14\text{ hops}}$
- **$4 \times 4$ cMesh Diameter:** $D = 2 \times (4 - 1) = \mathbf{6\text{ hops}}$ (a **$57\%$ reduction!**)

#### C. Halved Average Hop Distance ($H_{avg}$)
Under uniform random traffic, the average hop distance across the chip drops from **$5.33\text{ hops}$ down to just $2.67\text{ hops}$**.

#### D. Zero-Overhead Local Intra-Cluster Switching
If Core 0 communicates with Core 1, Core 2, or Core 3 within the same concentration tile, the packet is switched locally in **a single hop** without ever injecting onto the global inter-router network!

```mermaid
graph LR
  subgraph Comparison_64 ["64 Cores: Standard Mesh vs cMesh"]
    subgraph Mesh8x8 ["Standard 8×8 Mesh"]
      M["64 Routers<br/>Radix 5<br/>Diameter: 14 hops<br/>Avg Hops: 5.33"]
    end
    subgraph CMesh4x4 ["4×4 Concentrated Mesh (C=4)"]
      CM["16 Routers<br/>Radix 8<br/>Diameter: 6 hops<br/>Avg Hops: 2.67"]
    end
  end

  style Mesh8x8 fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px;
  style CMesh4x4 fill:#dcfce7,stroke:#22c55e,stroke-width:2px;
```

---

## 3. The Trade-Off: Router Radix vs. Hop Count

Why not concentrate 16 or 32 cores per router?  
Concentration trades **router crossbar radix** for **network hop count**:

$$\text{cMesh Router Radix } \delta = C + 4 \quad (\text{for a 2D grid})$$

- When $C = 1$ (Standard Mesh): Radix = $1 + 4 = 5\text{ ports}$ ($5 \times 5$ crossbar = 25 crosspoints).
- When $C = 4$ (Standard cMesh): Radix = $4 + 4 = 8\text{ ports}$ ($8 \times 8$ crossbar = 64 crosspoints).
- When $C = 8$: Radix = $8 + 4 = 12\text{ ports}$ ($12 \times 12$ crossbar = 144 crosspoints).

Beyond $C = 4$, the internal crossbar switch area and multiplexer fan-in delay grow quadratically ($O(\delta^2)$), eventually degrading the router's maximum operating clock frequency.

> [!NOTE]
> Extensive architectural research confirms that **$C = 4$ is the sweet spot in modern silicon processes**, delivering the optimal balance of minimal hop count, high clock frequency, and low buffer silicon area.

---

## 4. 🎛️ Interactive Mesh vs. cMesh Scalability & Area Calculator

Use the interactive tool below to evaluate the architectural trade-offs between standard 2D Meshes and Concentrated Meshes across varying core counts ($N = 16\text{ to } 256$ cores).

<div class="noc-sim-container" id="cmeshCalc">
  <div style="font-size:1.1rem; font-weight:700; color:var(--tcl-heading); margin-bottom:1rem; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;">
    <span>🔬 Mesh vs. Concentrated Mesh (cMesh) Trade-Off Calculator</span>
  </div>

  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:1rem; margin-bottom:1.25rem;">
    <div>
      <label style="font-size:0.85rem; font-weight:600; display:block; margin-bottom:0.35rem;">Total Compute Cores ($N$):</label>
      <select id="selCoresCount" class="noc-sim-select" style="width:100%;" onchange="updateCmeshSim()">
        <option value="16">16 Cores (4×4 Mesh)</option>
        <option value="64" selected>64 Cores (8×8 Mesh / 4×4 cMesh)</option>
        <option value="128">128 Cores (Large Server CMP)</option>
        <option value="256">256 Cores (AI Accelerator Pod)</option>
      </select>
    </div>

    <div>
      <label style="font-size:0.85rem; font-weight:600; display:block; margin-bottom:0.35rem;">Per-Hop Router Delay ($t_r$):</label>
      <select id="selRouterLat" class="noc-sim-select" style="width:100%;" onchange="updateCmeshSim()">
        <option value="1">1 Cycle (Speculative Bypass)</option>
        <option value="2" selected>2 Cycles (Speculative Router)</option>
        <option value="3">3 Cycles (Lookahead Router)</option>
      </select>
    </div>

    <div>
      <label style="font-size:0.85rem; font-weight:600; display:block; margin-bottom:0.35rem;">Clock Frequency ($f$):</label>
      <select id="selClkFreq" class="noc-sim-select" style="width:100%;" onchange="updateCmeshSim()">
        <option value="1.5">1.5 GHz</option>
        <option value="2.0" selected>2.0 GHz</option>
        <option value="2.5">2.5 GHz</option>
      </select>
    </div>
  </div>

  <!-- Comparative Results Grid -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.25rem; margin-bottom:1rem;">
    
    <!-- Standard Mesh Card -->
    <div style="background:var(--noc-surface-subtle); border:1.5px solid #ef4444; border-radius:10px; padding:1.25rem;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
        <span style="font-weight:700; font-size:1.05rem; color:#991b1b;">Standard 2D Mesh (C = 1)</span>
        <span id="badgeMeshGrid" style="font-size:0.75rem; font-weight:700; background:rgba(239,68,68,0.15); color:#ef4444; padding:2px 8px; border-radius:4px;">8×8 Grid</span>
      </div>

      <div style="font-size:0.88rem; line-height:1.7; color:var(--md-default-fg-color--lighter);">
        • <b>Total Router Count:</b> <span id="m_routers" style="font-weight:700; color:var(--tcl-heading);">64 routers</span><br>
        • <b>Router Switch Radix:</b> <span id="m_radix" style="font-weight:700;">5 ports</span> (25 crosspoints)<br>
        • <b>Network Diameter:</b> <span id="m_diam" style="font-weight:700; color:#ef4444;">14 hops</span><br>
        • <b>Average Hop Distance:</b> <span id="m_avghops" style="font-weight:700;">5.33 hops</span><br>
        • <b>Average Zero-Load Latency:</b> <span id="m_lat" style="font-weight:800; color:#ef4444; font-size:1.1rem;">-- ns</span><br>
        • <b>Total Buffer Storage:</b> <span id="m_mem" style="font-weight:700;">-- KB</span>
      </div>
    </div>

    <!-- Concentrated Mesh Card -->
    <div style="background:var(--noc-surface-subtle); border:1.5px solid #16a34a; border-radius:10px; padding:1.25rem;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
        <span style="font-weight:700; font-size:1.05rem; color:#166534;">Concentrated Mesh (C = 4)</span>
        <span id="badgeCmeshGrid" style="font-size:0.75rem; font-weight:700; background:rgba(34,197,94,0.15); color:#16a34a; padding:2px 8px; border-radius:4px;">4×4 Grid</span>
      </div>

      <div style="font-size:0.88rem; line-height:1.7; color:var(--md-default-fg-color--lighter);">
        • <b>Total Router Count:</b> <span id="cm_routers" style="font-weight:700; color:#16a34a;">16 routers (75% savings!)</span><br>
        • <b>Router Switch Radix:</b> <span id="cm_radix" style="font-weight:700;">8 ports</span> (64 crosspoints)<br>
        • <b>Network Diameter:</b> <span id="cm_diam" style="font-weight:700; color:#16a34a;">6 hops (57% cut)</span><br>
        • <b>Average Hop Distance:</b> <span id="cm_avghops" style="font-weight:700;">2.67 hops</span><br>
        • <b>Average Zero-Load Latency:</b> <span id="cm_lat" style="font-weight:800; color:#16a34a; font-size:1.1rem;">-- ns</span><br>
        • <b>Total Buffer Storage:</b> <span id="cm_mem" style="font-weight:700;">-- KB</span>
      </div>
    </div>

  </div>

  <div id="cmeshTakeaway" style="font-size:0.88rem; padding:0.75rem 1rem; border-radius:8px; background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.25); color:var(--tcl-heading); line-height:1.5;"></div>
</div>

<script>
function updateCmeshSim() {
  const N = parseInt(document.getElementById("selCoresCount").value, 10);
  const tr = parseInt(document.getElementById("selRouterLat").value, 10);
  const f_ghz = parseFloat(document.getElementById("selClkFreq").value);
  const tau_ns = 1.0 / f_ghz;

  // 1. Standard Mesh Calculations
  const k_mesh = Math.sqrt(N);
  const m_routers = N;
  const m_diam = 2 * (k_mesh - 1);
  const m_avghops = (2 * (k_mesh * k_mesh - 1)) / (3 * k_mesh);
  // Zero load latency = AvgHops * (tr + t_wire=1) + 4 flits serialization
  const m_lat_cyc = m_avghops * (tr + 1) + 4;
  const m_lat_ns = (m_lat_cyc * tau_ns).toFixed(2);
  const m_mem_kb = ((m_routers * 5 * 4 * 16 * 4) / 1024).toFixed(1); // 5 ports, 4 VCs, 4 flits of 16B

  document.getElementById("badgeMeshGrid").textContent = `${k_mesh}×${k_mesh} Grid`;
  document.getElementById("m_routers").textContent = `${m_routers} routers`;
  document.getElementById("m_diam").textContent = `${m_diam} hops`;
  document.getElementById("m_avghops").textContent = `${m_avghops.toFixed(2)} hops`;
  document.getElementById("m_lat").textContent = `${m_lat_ns} ns (${m_lat_cyc.toFixed(1)} cycles)`;
  document.getElementById("m_mem").textContent = `${m_mem_kb} KB`;

  // 2. Concentrated Mesh Calculations (C = 4)
  const cm_routers = N / 4;
  const k_cmesh = Math.sqrt(cm_routers);
  const cm_diam = 2 * (k_cmesh - 1);
  // Average hop count: (1/4 chance same tile = 0 net hops) + (3/4 chance inter-tile = avg cmesh hops)
  const cm_inter_avghops = (2 * (k_cmesh * k_cmesh - 1)) / (3 * k_cmesh);
  const cm_avghops = ((N - 4) / N) * cm_inter_avghops;
  const cm_lat_cyc = cm_avghops * (tr + 1) + 4;
  const cm_lat_ns = (cm_lat_cyc * tau_ns).toFixed(2);
  const cm_mem_kb = ((cm_routers * 8 * 4 * 16 * 4) / 1024).toFixed(1); // 8 ports, 4 VCs

  document.getElementById("badgeCmeshGrid").textContent = `${k_cmesh}×${k_cmesh} Grid`;
  document.getElementById("cm_routers").textContent = `${cm_routers} routers (75% fewer)`;
  document.getElementById("cm_diam").textContent = `${cm_diam} hops`;
  document.getElementById("cm_avghops").textContent = `${cm_avghops.toFixed(2)} hops`;
  document.getElementById("cm_lat").textContent = `${cm_lat_ns} ns (${cm_lat_cyc.toFixed(1)} cycles)`;
  document.getElementById("cm_mem").textContent = `${cm_mem_kb} KB`;

  // Dynamic Takeaway
  const latCut = Math.round(((parseFloat(m_lat_ns) - parseFloat(cm_lat_ns)) / parseFloat(m_lat_ns)) * 100);
  const memCut = Math.round(((parseFloat(m_mem_kb) - parseFloat(cm_mem_kb)) / parseFloat(m_mem_kb)) * 100);

  document.getElementById("cmeshTakeaway").innerHTML = `
    <strong>Architectural Synthesis for ${N} Cores:</strong><br>
    The Concentrated Mesh reduces overall communication latency by <strong>${latCut}%</strong> while eliminating <strong>${m_routers - cm_routers} routers</strong> from the silicon layout. 
    Total router buffer memory drops by <strong>${memCut}%</strong>, slashing static leakage power and freeing valuable die area for larger L2/L3 caches!
  `;
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", updateCmeshSim);
} else {
  updateCmeshSim();
}
</script>

---

## 5. Architectural Comparison Summary: Topologies for Manycores

| Metric | 2D Mesh | 2D Torus | Full Fat-Tree | Concentrated Mesh (cMesh) |
| :--- | :--- | :--- | :--- | :--- |
| **Topology Type** | Direct | Direct | Indirect | Direct (Concentrated) |
| **Router Count ($N=64$)** | 64 routers | 64 routers | 48 switches | **16 routers ($75\%$ reduction)** |
| **Router Radix** | 5 ports | 5 ports | 4 to 8 ports | 8 ports (4 local, 4 network) |
| **Network Diameter** | $2(k - 1) = 14$ | $k = 8$ | $2 \log_2 N = 6$ | **$2(\sqrt{N}/2 - 1) = 6$** |
| **Bisection Bandwidth** | $2\sqrt{N} \cdot w$ | $4\sqrt{N} \cdot w$ | **$N/2 \cdot w$ (Highest)** | $2\sqrt{N/4} \cdot w$ |
| **Physical Wiring Complexity**| **Minimal (Planar)**| Requires Folding | High (Global Tree) | Moderate (Short local clusters) |
| **Zero-Load Latency** | High | Moderate | Low | **Lowest** |

---

## 6. Worked Numerical Example: Router Silicon Area & Power Analysis

> [!TIP]
> **Problem Statement:**  
> A chip designer is sizing the on-chip interconnect for a 64-core processor on a 5nm FinFET process.  
> Standard cell libraries yield the following area estimates:
> - A 5-port router (Mesh) occupies $A_5 = 0.045\text{ mm}^2$ and consumes $P_5 = 32\text{ mW}$ of static leakage.
> - An 8-port router (cMesh) occupies $A_8 = 0.082\text{ mm}^2$ and consumes $P_8 = 56\text{ mW}$ of static leakage.
> 
> Compare:
> 1. Total Router Silicon Area ($A_{total}$)
> 2. Total Static Leakage Power ($P_{static}$)  
> between the **Standard 2D Mesh (64 routers)** and the **Concentrated Mesh (16 routers)**.

### Step 1: Standard 2D Mesh Calculation (64 Routers)
$$A_{total, Mesh} = 64 \times 0.045\text{ mm}^2 = \mathbf{2.88\text{ mm}^2}$$
$$P_{static, Mesh} = 64 \times 32\text{ mW} = \mathbf{2,048\text{ mW} = 2.048\text{ Watts}}$$

### Step 2: Concentrated Mesh Calculation (16 Routers)
$$A_{total, cMesh} = 16 \times 0.082\text{ mm}^2 = \mathbf{1.312\text{ mm}^2} \quad (\mathbf{54.4\%\text{ Silicon Area Reduction!}})$$
$$P_{static, cMesh} = 16 \times 56\text{ mW} = \mathbf{896\text{ mW} = 0.896\text{ Watts}} \quad (\mathbf{56.2\%\text{ Power Reduction!}})$$

### Conclusion:
Even though an individual 8-port cMesh router is larger than a 5-port mesh router ($0.082\text{ mm}^2$ vs $0.045\text{ mm}^2$), using $75\%$ fewer routers saves **over $1.56\text{ mm}^2$ of silicon area** and **$1.15\text{ Watts}$ of static power**!

---

## 7. 🎯 Knowledge Check: Lesson 3.2

<div class="noc-sim-container" id="quiz32" style="margin-top:1rem;">
  <div style="font-weight:700; font-size:1.05rem; margin-bottom:1rem; color:var(--tcl-heading);">
    📝 Concept Check: Indirect &amp; Concentrated Networks
  </div>

  <div id="q32_block">
    <p style="font-weight:600; font-size:0.95rem; margin-bottom:0.75rem;">
      <b>Question:</b> Why does a 4×4 Concentrated Mesh (cMesh) achieve lower zero-load latency for a 64-core chip than a standard 8×8 2D Mesh?
    </p>

    <div style="display:flex; flex-direction:column; gap:0.5rem;" id="q32_options">
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz32(0)">
        A. Because cMesh replaces packet routers with wireless RF antennas.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz32(1)">
        B. By clustering 4 compute cores around each router, total routers decrease from 64 to 16, cutting network diameter from 14 hops to just 6 hops and halving average hop traversal stages.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz32(2)">
        C. Because cMesh routers operate at 100 GHz.
      </button>
      <button class="noc-sim-select" style="text-align:left; padding:0.65rem 0.85rem; cursor:pointer;" onclick="checkQuiz32(3)">
        D. Because cMesh only allows communication between adjacent cores.
      </button>
    </div>

    <div id="q32_feedback" style="display:none; margin-top:1rem; padding:0.85rem; border-radius:8px; font-size:0.9rem; line-height:1.5;"></div>
  </div>
</div>

<script>
function checkQuiz32(idx) {
  const fb = document.getElementById("q32_feedback");
  fb.style.display = "block";
  const opts = document.getElementById("q32_options").children;
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
    fb.innerHTML = "<strong>✓ Correct!</strong> Concentrating 4 tiles per router reduces the grid to 4×4. Diameter drops from 14 to 6 hops, and average hop count drops from 5.33 to 2.67 hops, significantly cutting per-hop pipeline delays.";
  } else {
    opts[idx].style.background = "rgba(239,68,68,0.15)";
    opts[idx].style.borderColor = "#ef4444";
    opts[1].style.background = "rgba(34,197,94,0.15)";
    opts[1].style.borderColor = "#22c55e";
    fb.style.background = "rgba(239,68,68,0.1)";
    fb.style.border = "1px solid rgba(239,68,68,0.3)";
    fb.style.color = "#991b1b";
    fb.innerHTML = "<strong>✗ Incorrect.</strong> The correct answer is <strong>B</strong>. Concentration reduces router count by 75% and slashes network diameter in half.";
  }
}
</script>

---

## Summary & Next Steps

In this lesson, we established:
- The distinction between **Direct** and **Indirect** topologies.
- Why **Fat-Trees** maintain constant bisection bandwidth in high-throughput clusters.
- How **Concentrated Mesh (cMesh)** delivers lower latency, $75\%$ fewer routers, and $>50\%$ lower silicon area and static leakage power.

In the next lesson, we explore formal performance benchmarking: **Interconnect Metrics and Benchmark Traffic Patterns**.

👉 **Proceed to [Lesson 3.3: Interconnect Metrics & Traffic Patterns](03-metrics-traffic-patterns.md)**
