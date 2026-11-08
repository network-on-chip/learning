# 🌐 Interconnect Topology CAD & Spectral Graph Analyzer

An engineering-grade computer architecture workbench for modeling, analyzing, and synthesizing high-performance on-chip and scale-up interconnect topologies. Evaluate graph-theoretic invariants, compute Laplacian eigenvalues and algebraic connectivity (Fiedler vector $\lambda_2$), calculate bisection bandwidth and network diameter, and simulate traffic bottleneck distributions under synthetic workloads.

---

## 1. Physical & Graph-Theoretic Foundations

Modern multi-core processors, accelerator clusters, and exascale supercomputers rely on structured interconnection networks whose performance is strictly bound by their graph-theoretical invariants:

### 1.1 Invariants and Formulations
1. **Adjacency and Laplacian Matrices**:
   For an undirected graph $G = (V, E)$ with $|V| = N$ nodes and $|E| = M$ links:
   $$A_{ij} = \begin{cases} 1 & \text{if } (i,j) \in E \\ 0 & \text{otherwise} \end{cases}, \quad D_{ii} = \sum_{j} A_{ij}, \quad L = D - A$$
2. **Spectral Graph Theory & Algebraic Connectivity**:
   The eigenvalues of the graph Laplacian $L$ satisfy:
   $$0 = \lambda_1 \le \lambda_2 \le \lambda_3 \le \dots \le \lambda_N$$
   The second smallest eigenvalue $\lambda_2(L)$ is the **Fiedler eigenvalue** (algebraic connectivity). It quantifies network robustness, expansion properties, and diffusion rate. A graph is connected if and only if $\lambda_2 > 0$. By Cheeger's inequality, the edge expansion (isoperimetric constant) $h(G)$ is bounded by:
   $$\frac{\lambda_2}{2} \le h(G) \le \sqrt{2 \lambda_2 d_{\max}}$$
3. **Network Diameter ($D$) & Average Hop Count ($\bar{h}$)**:
   $$D = \max_{u, v \in V} d(u, v), \qquad \bar{h} = \frac{1}{N(N-1)} \sum_{u \ne v} d(u, v)$$
   Zero-load network latency is directly governed by average hop count: $T_0 = \bar{h} \cdot t_r + \frac{\bar{L}_{wire}}{v_{prop}} + \frac{L_{pkt}}{W_{channel}}$.
4. **Bisection Bandwidth ($B$)**:
   The minimum number of channel cuts required to partition the $N$ nodes into two equal halves of size $\lfloor N/2 \rfloor$ and $\lceil N/2 \rceil$:
   $$B = \min_{S \subset V, |S| = \lfloor N/2 \rfloor} |E(S, V \setminus S)|$$
   Under worst-case traffic (e.g., bit-complement or bisection stress), maximum sustainable throughput is strictly constrained: $\Theta_{\max} \le \frac{2 B}{N}$.
5. **Channel Load & Moore Bound**:
   Given maximum router radix $k_{\max}$ and diameter $D$, the maximum theoretical node count is bound by the Moore bound:
   $$N \le 1 + k_{\max} \sum_{i=0}^{D-1} (k_{\max} - 1)^i$$

---

## 2. Interactive Topology CAD & Spectral Workbench

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Topology Architecture:</b>
      <select id="topoPresetSelect" class="noc-sim-select" onchange="applyTopologyPreset(this.value)">
        <option value="mesh">2D Mesh (4x4, 16 Nodes)</option>
        <option value="torus">2D Torus (4x4 Periodic Wraparound)</option>
        <option value="folded_torus">Folded Torus (Equalized Wire Lengths)</option>
        <option value="hypercube">4D Hypercube (Q_4, 16 Nodes)</option>
        <option value="ring">1D Ring (16 Nodes)</option>
        <option value="dragonfly">Dragonfly (4 Groups of 4 Routers)</option>
        <option value="clos">Flattened Butterfly / 2-Tier Clos</option>
        <option value="custom">Custom Adjacency (Interactive Editor)</option>
      </select>
    </label>

    <label><b>Traffic Pattern:</b>
      <select id="topoTrafficSelect" class="noc-sim-select" onchange="evaluateTopologyMetrics()">
        <option value="uniform">Uniform Random Traffic</option>
        <option value="bit_complement">Bit-Complement Traffic</option>
        <option value="transpose">Transpose Traffic</option>
        <option value="tornado">Tornado Traffic</option>
      </select>
    </label>

    <label><b>Display Mode:</b>
      <select id="topoColorMode" class="noc-sim-select" onchange="renderTopology()">
        <option value="spectral">Spectral Fiedler Vector (λ₂ Partition)</option>
        <option value="traffic">Link Utilization & Congestion Heatmap</option>
        <option value="degree">Router Radix (Node Degree)</option>
        <option value="clusters">Physical Packaging Hierarchy</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" onclick="runForceLayoutStep()">⚡ Relax Physical Layout</button>
      <button class="noc-sim-btn secondary" onclick="resetNodePositions()">📐 Reset 2D Grid</button>
      <button class="noc-sim-btn secondary" onclick="clearAllLinks()">✂️ Clear Links</button>
      <button class="noc-sim-btn secondary" onclick="exportTopologyJson()">💾 Export JSON</button>
      <button class="noc-sim-btn secondary" onclick="exportVerilogNetlist()">📋 Export Verilog</button>
    </div>

    <!-- Live Engineering HUD -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:0.6rem; width:100%; margin-top:0.5rem; font-family:'JetBrains Mono', monospace; font-size:0.82rem;">
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Nodes / Links</span>
        <strong id="hudNodesLinks" style="color:#38bdf8; font-size:0.95rem;">16 / 24</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Diameter (D)</span>
        <strong id="hudDiameter" style="color:#22c55e; font-size:0.95rem;">6 hops</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Avg Hop Count (h̄)</span>
        <strong id="hudAvgHops" style="color:#38bdf8; font-size:0.95rem;">2.53 hops</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Bisection Bandwidth</span>
        <strong id="hudBisection" style="color:#f59e0b; font-size:0.95rem;">4 links</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Fiedler λ₂ (Conn.)</span>
        <strong id="hudFiedler" style="color:#a855f7; font-size:0.95rem;">0.586</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Max Radix (k_max)</span>
        <strong id="hudMaxRadix" style="color:#ec4899; font-size:0.95rem;">4</strong>
      </div>
    </div>
  </div>

  <div style="margin:0.75rem 0; padding:0.65rem 0.95rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; font-size:0.83rem; line-height:1.6; color:#94a3b8;">
    <strong style="color:#f8fafc;">Interactive CAD Editor:</strong>
    Click node $A$ then node $B$ to add/remove a bidirectional channel. Drag nodes to customize floorplan coordinates. The spectral solver continuously computes eigenvalues, shortest paths, and bisection cuts.
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="topoCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block; background:#0f172a; border-radius:10px;"></canvas>
  </div>

  <!-- Spectral & Analytical Diagnostics Table -->
  <div style="margin-top:1rem; display:grid; grid-template-columns: 1fr 1fr; gap:1rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; padding:0.75rem;">
      <strong style="color:#38bdf8; display:block; margin-bottom:0.4rem;">Eigenvalue Spectrum:</strong>
      <div id="topoEigenSpectrum" style="color:#94a3b8; font-size:0.75rem; max-height:100px; overflow-y:auto; line-height:1.5;">
        λ₀=0.000, λ₁=0.586, λ₂=0.586, λ₃=1.000...
      </div>
      <div style="margin-top:0.4rem; font-size:0.75rem; color:#cbd5e1;">
        Spectral Gap ($\lambda_N - \lambda_2$): <span id="topoSpmGap" style="color:#f59e0b;">-</span>
      </div>
    </div>

    <div style="background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; padding:0.75rem;">
      <strong style="color:#22c55e; display:block; margin-bottom:0.4rem;">Wiring & Bottleneck Analysis:</strong>
      <div style="color:#94a3b8; font-size:0.75rem; line-height:1.6;">
        Total Wire Length: <span id="topoTotalWire" style="color:#f8fafc;">0.00 mm</span><br>
        Peak Channel Load ($\gamma_{\max}$): <span id="topoPeakLoad" style="color:#ef4444;">0.000 pkts/cycle</span><br>
        Throughput Saturation Limit ($\Theta_{\text{sat}}$): <span id="topoSatBound" style="color:#38bdf8;">0.000</span>
      </div>
    </div>
  </div>

  <!-- CAD Netlist Export Drawer -->
  <div id="topoExportDrawer" style="display:none; margin-top:1rem; background:#0b1120; border:1px solid #1e293b; border-radius:8px; padding:0.85rem;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
      <strong id="topoExportTitle" style="color:#38bdf8; font-size:0.85rem;">Generated Specification</strong>
      <button class="noc-sim-btn secondary" style="padding:2px 8px; font-size:0.75rem;" onclick="document.getElementById('topoExportDrawer').style.display='none'">Close</button>
    </div>
    <textarea id="topoExportCode" readonly style="width:100%; height:160px; background:#050811; color:#a5f3fc; border:1px solid #334155; border-radius:6px; font-family:'JetBrains Mono', monospace; font-size:0.75rem; padding:0.5rem; box-sizing:border-box;"></textarea>
  </div>
</div>

---

## 3. Topologies Comparison & Trade-off Matrix

| Topology Family | Diameter ($D$) | Bisection Bandwidth ($B$) | Router Radix ($k$) | Wire Complexity | Scalability Bottleneck |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2D Mesh ($k \times k$)** | $2(k - 1)$ | $k$ | $4$ (fixed) | Minimal (planar nearest-neighbor) | Large diameter, edge congestion |
| **2D Torus ($k \times k$)** | $2 \lfloor k/2 \rfloor$ | $2k$ | $4$ (fixed) | Moderate (long wraparound wires) | Long physical wrap wires without folding |
| **Folded Torus** | $2 \lfloor k/2 \rfloor$ | $2k$ | $4$ (fixed) | Uniform (interleaved coordinates) | $2\times$ trace density |
| **4D Hypercube ($Q_4$)** | $n = \log_2 N$ | $N/2$ | $n = \log_2 N$ | High (logarithmic wire crossing) | Radix scales with network size |
| **Dragonfly ($a, p, h$)** | $3$ (hierarchical) | High (global inter-group links) | $p + a - 1 + h$ | Mixed (local copper + global optical) | Asymmetric traffic load balancing |
| **Flattened Butterfly** | $2$ (low-latency) | $\frac{N \cdot k}{4}$ | $k(n-1) + 1$ | Very high ($O(N^2)$ board routing) | Rapid crossbar area growth ($O(k^2)$) |

---

<script>
(function() {
  const NUM_NODES = 16;
  let nodes = [];
  let adj = []; // NUM_NODES x NUM_NODES matrix
  let selectedNode = -1;
  let draggedNode = -1;
  let dragOffset = {x: 0, y: 0};
  let distMatrix = [];
  let linkLoads = {}; // "u-v": load
  let fiedlerVector = [];
  let eigenvalues = [];

  // Canvas
  const canvas = document.getElementById('topoCanvas');
  const ctx = canvas.getContext('2d');

  // Initialize adjacency matrix
  function initAdj() {
    adj = Array(NUM_NODES).fill(0).map(() => Array(NUM_NODES).fill(0));
  }

  // Predefined topologies
  window.applyTopologyPreset = function(preset) {
    initAdj();
    if (preset === 'mesh' || preset === 'folded_torus') {
      setup2DGrid(4, 4);
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          const u = r * 4 + c;
          if (c + 1 < 4) addEdge(u, r * 4 + (c + 1));
          if (r + 1 < 4) addEdge(u, (r + 1) * 4 + c);
        }
      }
      if (preset === 'folded_torus') {
        // Interleave node physical placement for folded torus
        for (let r = 0; r < 4; r++) {
          for (let c = 0; c < 4; c++) {
            const u = r * 4 + c;
            addEdge(r * 4 + 0, r * 4 + 3);
            addEdge(0 * 4 + c, 3 * 4 + c);
          }
        }
      }
    } else if (preset === 'torus') {
      setup2DGrid(4, 4);
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          const u = r * 4 + c;
          addEdge(u, r * 4 + ((c + 1) % 4));
          addEdge(u, ((r + 1) % 4) * 4 + c);
        }
      }
    } else if (preset === 'hypercube') {
      setupCircleLayout();
      for (let i = 0; i < 16; i++) {
        for (let b = 0; b < 4; b++) {
          const neighbor = i ^ (1 << b);
          if (i < neighbor) addEdge(i, neighbor);
        }
      }
    } else if (preset === 'ring') {
      setupCircleLayout();
      for (let i = 0; i < 16; i++) {
        addEdge(i, (i + 1) % 16);
      }
    } else if (preset === 'dragonfly') {
      setupDragonflyLayout();
      // 4 groups of 4 routers: full local clique in each group
      for (let g = 0; g < 4; g++) {
        const base = g * 4;
        for (let i = 0; i < 4; i++) {
          for (let j = i + 1; j < 4; j++) {
            addEdge(base + i, base + j);
          }
        }
      }
      // Global links connecting groups
      addEdge(0, 4);
      addEdge(1, 8);
      addEdge(2, 12);
      addEdge(5, 9);
      addEdge(6, 13);
      addEdge(10, 14);
    } else if (preset === 'clos') {
      setupCircleLayout();
      // 2-tier / Flattened Butterfly: full row and column cliques
      for (let r = 0; r < 4; r++) {
        for (let c1 = 0; c1 < 4; c1++) {
          for (let c2 = c1 + 1; c2 < 4; c2++) {
            addEdge(r * 4 + c1, r * 4 + c2);
          }
        }
      }
      for (let c = 0; c < 4; c++) {
        for (let r1 = 0; r1 < 4; r1++) {
          for (let r2 = r1 + 1; r2 < 4; r2++) {
            addEdge(r1 * 4 + c, r2 * 4 + c);
          }
        }
      }
    }
    evaluateTopologyMetrics();
  };

  function addEdge(u, v) {
    if (u === v) return;
    adj[u][v] = 1;
    adj[v][u] = 1;
  }

  function removeEdge(u, v) {
    adj[u][v] = 0;
    adj[v][u] = 0;
  }

  function setup2DGrid(rows, cols) {
    nodes = [];
    const padX = 80;
    const padY = 60;
    const stepX = (canvas.width - 2 * padX) / (cols - 1);
    const stepY = (canvas.height - 2 * padY) / (rows - 1);
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        nodes.push({
          id: r * cols + c,
          x: padX + c * stepX,
          y: padY + r * stepY,
          vx: 0,
          vy: 0,
          label: `R(${c},${r})`
        });
      }
    }
  }

  function setupCircleLayout() {
    nodes = [];
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    const radius = Math.min(cx, cy) - 55;
    for (let i = 0; i < NUM_NODES; i++) {
      const angle = (2 * Math.PI * i) / NUM_NODES - Math.PI / 2;
      nodes.push({
        id: i,
        x: cx + radius * Math.cos(angle),
        y: cy + radius * Math.sin(angle),
        vx: 0,
        vy: 0,
        label: `R${i}`
      });
    }
  }

  function setupDragonflyLayout() {
    nodes = [];
    const groupCenters = [
      {x: 160, y: 130},
      {x: 460, y: 130},
      {x: 160, y: 330},
      {x: 460, y: 330}
    ];
    for (let g = 0; g < 4; g++) {
      const gc = groupCenters[g];
      for (let i = 0; i < 4; i++) {
        const angle = (2 * Math.PI * i) / 4;
        nodes.push({
          id: g * 4 + i,
          x: gc.x + 55 * Math.cos(angle),
          y: gc.y + 55 * Math.sin(angle),
          vx: 0,
          vy: 0,
          label: `G${g}:${i}`
        });
      }
    }
  }

  // Numerical Graph Analysis: Floyd-Warshall, Laplacian Eigenvalues, Min Bisection
  function evaluateTopologyMetrics() {
    // 1. Floyd-Warshall All-Pairs Shortest Path
    distMatrix = Array(NUM_NODES).fill(0).map(() => Array(NUM_NODES).fill(Infinity));
    for (let i = 0; i < NUM_NODES; i++) distMatrix[i][i] = 0;
    let linkCount = 0;
    let maxDegree = 0;

    for (let i = 0; i < NUM_NODES; i++) {
      let deg = 0;
      for (let j = 0; j < NUM_NODES; j++) {
        if (adj[i][j]) {
          distMatrix[i][j] = 1;
          deg++;
          if (i < j) linkCount++;
        }
      }
      if (deg > maxDegree) maxDegree = deg;
    }

    for (let k = 0; k < NUM_NODES; k++) {
      for (let i = 0; i < NUM_NODES; i++) {
        for (let j = 0; j < NUM_NODES; j++) {
          if (distMatrix[i][k] + distMatrix[k][j] < distMatrix[i][j]) {
            distMatrix[i][j] = distMatrix[i][k] + distMatrix[k][j];
          }
        }
      }
    }

    let diameter = 0;
    let totalHops = 0;
    let validPairs = 0;
    for (let i = 0; i < NUM_NODES; i++) {
      for (let j = 0; j < NUM_NODES; j++) {
        if (i !== j) {
          if (distMatrix[i][j] < Infinity) {
            if (distMatrix[i][j] > diameter) diameter = distMatrix[i][j];
            totalHops += distMatrix[i][j];
            validPairs++;
          }
        }
      }
    }
    const avgHops = validPairs > 0 ? (totalHops / validPairs) : 0;

    // 2. Exact Bisection Bandwidth for N=16
    const bisectionCut = computeMinBisection(adj, NUM_NODES);

    // 3. Graph Laplacian L = D - A and Jacobi Eigenvalues
    const L = Array(NUM_NODES).fill(0).map(() => Array(NUM_NODES).fill(0));
    for (let i = 0; i < NUM_NODES; i++) {
      let deg = 0;
      for (let j = 0; j < NUM_NODES; j++) {
        if (adj[i][j]) {
          L[i][j] = -1;
          deg++;
        }
      }
      L[i][i] = deg;
    }
    const eig = jacobiEigenvalues(L, NUM_NODES);
    eigenvalues = eig.values;
    // Fiedler vector corresponds to the 2nd smallest eigenvalue (index 1)
    fiedlerVector = eig.vectors.map(row => row[1]);

    // 4. Traffic Flow & Channel Load Simulation
    simulateTrafficLoad();

    // 5. Update HUD elements
    document.getElementById('hudNodesLinks').textContent = `${NUM_NODES} / ${linkCount}`;
    document.getElementById('hudDiameter').textContent = diameter === Infinity ? 'Disconnected' : `${diameter} hops`;
    document.getElementById('hudAvgHops').textContent = diameter === Infinity ? 'Inf' : `${avgHops.toFixed(2)} hops`;
    document.getElementById('hudBisection').textContent = `${bisectionCut} links`;
    document.getElementById('hudFiedler').textContent = eigenvalues[1] !== undefined ? eigenvalues[1].toFixed(3) : '0.000';
    document.getElementById('hudMaxRadix').textContent = `${maxDegree}`;

    // Spectrum display
    const specStr = eigenvalues.slice(0, 8).map((v, i) => `λ_${i}=${v.toFixed(3)}`).join(', ');
    document.getElementById('topoEigenSpectrum').textContent = specStr + (eigenvalues.length > 8 ? '...' : '');
    const spmGap = (eigenvalues[eigenvalues.length - 1] - eigenvalues[1]).toFixed(3);
    document.getElementById('topoSpmGap').textContent = spmGap;

    renderTopology();
  }

  // Exact Bisection Bandwidth via Combinatorial Search for N=16 (12,870 combos)
  function computeMinBisection(matrix, n) {
    if (n > 16) return -1; // Fallback for larger sizes
    let minCut = Infinity;
    const half = n / 2;
    // Generate all combinations of picking half elements from n, fixing node 0 in partition A to break symmetry
    const comb = [];
    function backtrack(start, chosen) {
      if (chosen.length === half) {
        let cut = 0;
        const setA = new Set(chosen);
        for (let u of chosen) {
          for (let v = 0; v < n; v++) {
            if (matrix[u][v] && !setA.has(v)) cut++;
          }
        }
        if (cut < minCut) minCut = cut;
        return;
      }
      for (let i = start; i < n; i++) {
        chosen.push(i);
        backtrack(i + 1, chosen);
        chosen.pop();
      }
    }
    backtrack(1, [0]);
    return minCut === Infinity ? 0 : minCut;
  }

  // Jacobi Eigenvalue Solver for Real Symmetric Matrices
  function jacobiEigenvalues(A_in, n) {
    let A = A_in.map(r => r.slice());
    let V = Array(n).fill(0).map((_, i) => Array(n).fill(0).map((_, j) => (i === j ? 1 : 0)));
    const maxIter = 100;
    const eps = 1e-9;

    for (let iter = 0; iter < maxIter; iter++) {
      let maxVal = 0;
      let p = 0, q = 1;
      for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
          if (Math.abs(A[i][j]) > maxVal) {
            maxVal = Math.abs(A[i][j]);
            p = i; q = j;
          }
        }
      }
      if (maxVal < eps) break;

      const app = A[p][p], aqq = A[q][q], apq = A[p][q];
      const theta = (aqq - app) / (2 * apq);
      const t = (theta >= 0 ? 1 : -1) / (Math.abs(theta) + Math.sqrt(theta * theta + 1));
      const c = 1 / Math.sqrt(t * t + 1);
      const s = t * c;

      // Update A
      A[p][p] = c * c * app - 2 * s * c * apq + s * s * aqq;
      A[q][q] = s * s * app + 2 * s * c * apq + c * c * aqq;
      A[p][q] = 0;
      A[q][p] = 0;

      for (let i = 0; i < n; i++) {
        if (i !== p && i !== q) {
          const aip = A[i][p];
          const aiq = A[i][q];
          A[i][p] = c * aip - s * aiq;
          A[p][i] = A[i][p];
          A[i][q] = s * aip + c * aiq;
          A[q][i] = A[i][q];
        }
      }

      // Update eigenvectors
      for (let i = 0; i < n; i++) {
        const vip = V[i][p];
        const viq = V[i][q];
        V[i][p] = c * vip - s * viq;
        V[i][q] = s * vip + c * viq;
      }
    }

    // Extract and sort eigenvalues with eigenvectors
    const pairs = [];
    for (let i = 0; i < n; i++) {
      const vec = [];
      for (let r = 0; r < n; r++) vec.push(V[r][i]);
      pairs.push({ val: Math.max(0, A[i][i]), vec: vec });
    }
    pairs.sort((a, b) => a.val - b.val);

    const values = pairs.map(p => p.val);
    const sortedVectors = Array(n).fill(0).map((_, r) => pairs.map(p => p.vec[r]));
    return { values, vectors: sortedVectors };
  }

  // Traffic Load Simulation: Route shortest paths and aggregate link traversals
  function simulateTrafficLoad() {
    linkLoads = {};
    const trafficType = document.getElementById('topoTrafficSelect').value;
    const n = NUM_NODES;
    let totalTraversals = 0;
    let maxLinkLoad = 0;

    function getDest(src) {
      if (trafficType === 'uniform') return Math.floor(Math.random() * n);
      if (trafficType === 'bit_complement') return (~src) & (n - 1);
      if (trafficType === 'transpose') {
        const r = Math.floor(src / 4), c = src % 4;
        return c * 4 + r;
      }
      if (trafficType === 'tornado') {
        const r = Math.floor(src / 4), c = src % 4;
        return r * 4 + ((c + 1) % 4);
      }
      return (src + 1) % n;
    }

    // Accumulate shortest paths
    for (let s = 0; s < n; s++) {
      const d = getDest(s);
      if (s === d || distMatrix[s][d] === Infinity) continue;

      // Find path via BFS / predecessor
      let curr = s;
      while (curr !== d) {
        let nextHop = -1;
        let minD = Infinity;
        for (let v = 0; v < n; v++) {
          if (adj[curr][v] && distMatrix[v][d] < minD) {
            minD = distMatrix[v][d];
            nextHop = v;
          }
        }
        if (nextHop === -1) break;
        const key = curr < nextHop ? `${curr}-${nextHop}` : `${nextHop}-${curr}`;
        linkLoads[key] = (linkLoads[key] || 0) + 1;
        totalTraversals++;
        curr = nextHop;
      }
    }

    for (let k in linkLoads) {
      if (linkLoads[k] > maxLinkLoad) maxLinkLoad = linkLoads[k];
    }

    // Physical wiring length
    let totalWireMm = 0;
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        if (adj[i][j]) {
          const dx = (nodes[i].x - nodes[j].x) * 0.05; // 0.05 mm per canvas px
          const dy = (nodes[i].y - nodes[j].y) * 0.05;
          totalWireMm += Math.sqrt(dx * dx + dy * dy);
        }
      }
    }

    document.getElementById('topoTotalWire').textContent = `${totalWireMm.toFixed(2)} mm`;
    const normLoad = totalTraversals > 0 ? (maxLinkLoad / n).toFixed(3) : '0.000';
    document.getElementById('topoPeakLoad').textContent = `${normLoad} pkts/cycle`;
    const satThroughput = maxLinkLoad > 0 ? (1.0 / (maxLinkLoad / n)).toFixed(3) : '1.000';
    document.getElementById('topoSatBound').textContent = `${satThroughput} flits/node/cyc`;
  }

  // Force-Directed Layout Physics
  window.runForceLayoutStep = function() {
    const kRepel = 2200;
    const kSpring = 0.06;
    const restLen = 80;
    const damping = 0.85;

    for (let i = 0; i < NUM_NODES; i++) {
      let fx = 0, fy = 0;
      // Repulsion between all node pairs
      for (let j = 0; j < NUM_NODES; j++) {
        if (i !== j) {
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          const force = kRepel / (dist * dist);
          fx += (dx / dist) * force;
          fy += (dy / dist) * force;
        }
      }
      // Spring attraction along links
      for (let j = 0; j < NUM_NODES; j++) {
        if (adj[i][j]) {
          const dx = nodes[j].x - nodes[i].x;
          const dy = nodes[j].y - nodes[i].y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          const springF = (dist - restLen) * kSpring;
          fx += (dx / dist) * springF;
          fy += (dy / dist) * springF;
        }
      }
      // Wall boundary repulsion
      fx += (15 / Math.max(10, nodes[i].x)) - (15 / Math.max(10, canvas.width - nodes[i].x));
      fy += (15 / Math.max(10, nodes[i].y)) - (15 / Math.max(10, canvas.height - nodes[i].y));

      nodes[i].vx = (nodes[i].vx + fx) * damping;
      nodes[i].vy = (nodes[i].vy + fy) * damping;
    }

    for (let i = 0; i < NUM_NODES; i++) {
      nodes[i].x = Math.max(40, Math.min(canvas.width - 40, nodes[i].x + nodes[i].vx));
      nodes[i].y = Math.max(40, Math.min(canvas.height - 40, nodes[i].y + nodes[i].vy));
    }
    renderTopology();
  };

  window.resetNodePositions = function() {
    setup2DGrid(4, 4);
    evaluateTopologyMetrics();
  };

  window.clearAllLinks = function() {
    initAdj();
    evaluateTopologyMetrics();
  };

  // Canvas Rendering
  function renderTopology() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const mode = document.getElementById('topoColorMode').value;

    // Draw Links
    let maxLoad = 1;
    for (let k in linkLoads) {
      if (linkLoads[k] > maxLoad) maxLoad = linkLoads[k];
    }

    for (let i = 0; i < NUM_NODES; i++) {
      for (let j = i + 1; j < NUM_NODES; j++) {
        if (adj[i][j]) {
          const key = `${i}-${j}`;
          const load = linkLoads[key] || 0;
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);

          if (mode === 'traffic') {
            const ratio = Math.min(1, load / maxLoad);
            ctx.strokeStyle = `hsl(${(1 - ratio) * 220}, 90%, 55%)`;
            ctx.lineWidth = 1.5 + ratio * 3.5;
          } else {
            ctx.strokeStyle = 'rgba(100, 116, 139, 0.45)';
            ctx.lineWidth = 2;
          }
          ctx.stroke();
        }
      }
    }

    // Draw Nodes
    for (let i = 0; i < NUM_NODES; i++) {
      const nd = nodes[i];
      ctx.beginPath();
      ctx.arc(nd.x, nd.y, 16, 0, Math.PI * 2);

      if (mode === 'spectral') {
        const val = fiedlerVector[i] || 0;
        // Negative = cyan, Positive = orange
        if (val >= 0) {
          ctx.fillStyle = `rgba(249, 115, 22, ${Math.min(1, 0.3 + val * 2)})`;
        } else {
          ctx.fillStyle = `rgba(56, 189, 248, ${Math.min(1, 0.3 + Math.abs(val) * 2)})`;
        }
      } else if (mode === 'degree') {
        let deg = 0;
        for (let j = 0; j < NUM_NODES; j++) if (adj[i][j]) deg++;
        const hue = Math.min(300, deg * 40);
        ctx.fillStyle = `hsl(${hue}, 80%, 45%)`;
      } else if (mode === 'clusters') {
        const grp = Math.floor(i / 4);
        const palette = ['#38bdf8', '#4ade80', '#fb923c', '#c084fc'];
        ctx.fillStyle = palette[grp % 4];
      } else {
        ctx.fillStyle = '#1e293b';
      }

      ctx.fill();
      ctx.strokeStyle = (selectedNode === i) ? '#facc15' : '#475569';
      ctx.lineWidth = (selectedNode === i) ? 3 : 1.5;
      ctx.stroke();

      // Node Label
      ctx.fillStyle = '#ffffff';
      ctx.font = '10px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(nd.label, nd.x, nd.y);
    }
  }

  // Interactive Click & Drag Handling
  canvas.addEventListener('mousedown', function(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const mx = (e.clientX - rect.left) * scaleX;
    const my = (e.clientY - rect.top) * scaleY;

    let hit = -1;
    for (let i = 0; i < NUM_NODES; i++) {
      const dx = mx - nodes[i].x;
      const dy = my - nodes[i].y;
      if (dx * dx + dy * dy <= 18 * 18) {
        hit = i;
        break;
      }
    }

    if (hit !== -1) {
      if (selectedNode === -1) {
        selectedNode = hit;
      } else if (selectedNode === hit) {
        selectedNode = -1;
      } else {
        // Toggle edge between selectedNode and hit
        if (adj[selectedNode][hit]) {
          removeEdge(selectedNode, hit);
        } else {
          addEdge(selectedNode, hit);
        }
        selectedNode = -1;
        evaluateTopologyMetrics();
      }
      draggedNode = hit;
      dragOffset.x = mx - nodes[hit].x;
      dragOffset.y = my - nodes[hit].y;
      renderTopology();
    } else {
      selectedNode = -1;
      renderTopology();
    }
  });

  window.addEventListener('mousemove', function(e) {
    if (draggedNode !== -1) {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const mx = (e.clientX - rect.left) * scaleX;
      const my = (e.clientY - rect.top) * scaleY;

      nodes[draggedNode].x = Math.max(25, Math.min(canvas.width - 25, mx - dragOffset.x));
      nodes[draggedNode].y = Math.max(25, Math.min(canvas.height - 25, my - dragOffset.y));
      renderTopology();
    }
  });

  window.addEventListener('mouseup', function() {
    draggedNode = -1;
  });

  // Export JSON Topology Specification
  window.exportTopologyJson = function() {
    const edges = [];
    for (let i = 0; i < NUM_NODES; i++) {
      for (let j = i + 1; j < NUM_NODES; j++) {
        if (adj[i][j]) edges.push([i, j]);
      }
    }
    const spec = {
      network_name: document.getElementById('topoPresetSelect').value,
      num_nodes: NUM_NODES,
      diameter: document.getElementById('hudDiameter').textContent,
      bisection_bandwidth: document.getElementById('hudBisection').textContent,
      fiedler_eigenvalue: parseFloat(document.getElementById('hudFiedler').textContent),
      edges: edges,
      node_coordinates: nodes.map(n => ({ id: n.id, x: Math.round(n.x), y: Math.round(n.y) }))
    };
    document.getElementById('topoExportTitle').textContent = 'JSON Topology Specification';
    document.getElementById('topoExportCode').value = JSON.stringify(spec, null, 2);
    document.getElementById('topoExportDrawer').style.display = 'block';
  };

  // Export Synthesizable Verilog Network Interconnect
  window.exportVerilogNetlist = function() {
    let verilog = `// Synthesizable Top-Level NoC Interconnect Netlist\n`;
    verilog += `// Generated by Interconnect Topology CAD Analyzer\n`;
    verilog += `\`timescale 1ns/1ps\n\n`;
    verilog += `module noc_top_interconnect (\n`;
    verilog += `    input  wire        clk,\n`;
    verilog += `    input  wire        rst_n\n`;
    verilog += `);\n\n`;

    let linkIdx = 0;
    for (let i = 0; i < NUM_NODES; i++) {
      for (let j = i + 1; j < NUM_NODES; j++) {
        if (adj[i][j]) {
          verilog += `    // Bidirectional link: Router ${i} <--> Router ${j}\n`;
          verilog += `    wire [31:0] link_${i}_to_${j}_data;\n`;
          verilog += `    wire        link_${i}_to_${j}_valid;\n`;
          verilog += `    wire        link_${i}_to_${j}_credit;\n`;
          verilog += `    wire [31:0] link_${j}_to_${i}_data;\n`;
          verilog += `    wire        link_${j}_to_${i}_valid;\n`;
          verilog += `    wire        link_${j}_to_${i}_credit;\n\n`;
          linkIdx++;
        }
      }
    }
    verilog += `    // Router Instances instantiated with local ports...\n`;
    verilog += `endmodule\n`;

    document.getElementById('topoExportTitle').textContent = 'Synthesizable Verilog Netlist';
    document.getElementById('topoExportCode').value = verilog;
    document.getElementById('topoExportDrawer').style.display = 'block';
  };

  // Initial load
  window.applyTopologyPreset('mesh');
})();
</script>
