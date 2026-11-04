# 🌐 Topology Titans: Interconnect Graph Architect

Design next-generation supercomputing and exascale chip interconnects! Wire network topologies across multicore processors, evaluate graph-theoretical metrics in real time (Network Diameter, Bisection Bandwidth, Average Hop Count), and stress-test communication patterns under router pin radix and wire cost constraints. High scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Mission / Campaign:</b>
      <select id="topoMissionSelect" class="noc-sim-select" onchange="loadTopoMission(this.value)">
        <option value="1">Mission 1: Ring to Torus Evolution (Cut Diameter &le; 4)</option>
        <option value="2">Mission 2: 16-Node 4D Hypercube (Bisection &ge; 8)</option>
        <option value="3">Mission 3: High-Radix Dragonfly (Grouped Interconnect)</option>
        <option value="4">Mission 4: 2-Tier Fat-Tree Clos Network</option>
        <option value="5">Mission 5: Small-World Shortcut Optimizer</option>
        <option value="sandbox">🛠️ Free Exascale Sandbox Mode</option>
      </select>
    </label>

    <label><b>Topology Preset:</b>
      <select id="topoPresetSelect" class="noc-sim-select" onchange="applyTopoPreset(this.value)">
        <option value="custom">Custom Wiring</option>
        <option value="ring">1D Ring (16 Nodes)</option>
        <option value="mesh">2D Mesh (4x4)</option>
        <option value="torus">2D Torus (4x4 Wrap-Around)</option>
        <option value="hypercube">4D Hypercube (16 Nodes)</option>
        <option value="dragonfly">Dragonfly (4 Groups of 4)</option>
      </select>
    </label>

    <label><b>Traffic Pattern:</b>
      <select id="topoTrafficPattern" class="noc-sim-select">
        <option value="uniform">Uniform Random Traffic</option>
        <option value="bit_complement">Bit-Complement Traffic</option>
        <option value="all_to_all">All-to-All Personalized Burst</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button id="runStressBtn" class="noc-sim-btn" onclick="runTopologyStressTest()">▶ Run Traffic Stress Test</button>
      <button class="noc-sim-btn secondary" onclick="clearTopologyWires()">✂️ Clear Links</button>
      <button class="noc-sim-btn secondary" onclick="resetTopologyLayout()">🔄 Reset Nodes</button>
      <button id="topoSoundBtn" class="noc-sim-btn secondary" onclick="toggleTopoSound()">🔊 Sound: ON</button>
    </div>

    <!-- Live Graph Metrics HUD -->
    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem; width:100%; margin-top:0.35rem;">
      <span style="color:var(--tcl-blue-600);">Diameter: <span id="topoDiameter">0</span> hops</span>
      <span style="color:#22c55e;">Avg Hops: <span id="topoAvgHops">0.00</span></span>
      <span style="color:#f59e0b;">Bisection: <span id="topoBisection">0</span> links</span>
      <span style="color:#ec4899;">Max Radix: <span id="topoMaxRadix">0</span></span>
      <span style="color:#38bdf8;">Wire Cost: $<span id="topoWireCost">0</span></span>
      <span style="color:#eab308; margin-left:auto;" id="topoStarsDisplay">⭐⭐⭐</span>
    </div>
  </div>

  <div id="topoMissionBrief" style="margin-bottom:0.75rem; padding:0.65rem 0.95rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; font-size:0.85rem; line-height:1.6;">
    <strong>Mission Objective:</strong> <span id="topoTargetText">Cut the 16-node ring diameter from 8 down to &le; 4 hops by adding wrap-around and cross-links while keeping node degree (radix) &le; 4.</span>
    <div style="font-size:0.8rem; color:#94a3b8; margin-top:2px;">💡 Click Router A, then click Router B to add a bidirectional link. Click an existing link to remove it!</div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="topoCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Mission Success Modal -->
    <div id="topoSuccessModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;">🏆</div>
      <h2 style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#4ade80;">TOPOLOGY VALIDATED!</h2>
      <p id="topoSuccessSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:460px; margin-bottom:1.25rem; line-height:1.6;">
        Interconnect graph satisfied all diameter, radix, and bisection bandwidth criteria!
      </p>

      <div id="topoStarsAwarded" style="font-size:1.8rem; margin-bottom:1rem;">⭐⭐⭐</div>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:0.85rem 1.25rem; margin-bottom:1.25rem; width:100%; max-width:400px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Architect Callsign:</label>
        <input type="text" id="topoCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.5rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Graph Master" value="Topology Titan">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="topoOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Berkeley / MIT / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveTopologyRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitTopologyToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <button class="noc-sim-btn secondary" onclick="nextTopoMission()" style="color:#ffffff !important;">▶ Next Mission</button>
        <button class="noc-sim-btn secondary" onclick="closeTopoModal()" style="color:#ffffff !important;">Close</button>
      </div>
      <div id="topoSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Topology score successfully recorded in your browser Leaderboard!
      </div>
    </div>

    <!-- Mission Failure Modal -->
    <div id="topoFailureModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;">⚠️</div>
      <h2 style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">TOPOLOGY CRITERIA UNMET</h2>
      <p id="topoFailureSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:440px; margin-bottom:1.25rem; line-height:1.6;">
        Diameter too high, radix exceeded, or graph disconnected.
      </p>
      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="closeTopoModal()" style="background:#0284c7;">🔄 Adjust Links &amp; Retry</button>
      </div>
    </div>
  </div>

  <div id="topoInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">🌐 Interconnect Topologies &amp; Graph Metrics:</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Network Diameter ($D$):</strong> The maximum shortest path between any pair of nodes ($\max_{u,v} d(u,v)$). Lower diameter translates directly to lower zero-load latency for remote memory and cache-coherence traffic.</li>
      <li><strong>Bisection Bandwidth ($B$):</strong> The minimum link cuts required to bisect the network into two equal partitions ($\lfloor N/2 \rfloor$). In adversarial traffic (such as Bit-Complement), throughput is strictly bound by bisection bandwidth: $\Theta_{max} \le \frac{2B}{N}$.</li>
      <li><strong>Node Degree / Radix ($k$):</strong> The number of physical ports on each router. Higher radix decreases diameter, but exponentially inflates the internal crossbar area ($O(k^2)$) and router pin count!</li>
      <li><strong>High-Radix Topologies (Dragonfly &amp; Flattened Butterfly):</strong> Modern supercomputers group high-density local nodes into intra-group cliques, reducing long global optical cables to achieve exascale scalability at affordable packaging cost.</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Synthesizer for Topology Titans
class TopoAudio {
  constructor() {
    this.ctx = null;
    this.enabled = true;
  }

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) this.ctx = new AudioContext();
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  playLink() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440, now);
      osc.exponentialRampToValueAtTime(880, now + 0.08);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.1);
    } catch(e) {}
  }

  playStress() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(180, now);
      osc.frequency.linearRampToValueAtTime(360, now + 0.35);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.4);
    } catch(e) {}
  }

  playSuccess() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const notes = [523.25, 659.25, 783.99, 1046.5]; // C major
      notes.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + idx * 0.07);
        gain.gain.setValueAtTime(0.12, now + idx * 0.07);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.07 + 0.2);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now + idx * 0.07);
        osc.stop(now + idx * 0.07 + 0.2);
      });
    } catch(e) {}
  }

  playFailure() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(200, now);
      osc.frequency.linearRampToValueAtTime(100, now + 0.3);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } catch(e) {}
  }
}

const TOPO_MISSIONS = {
  "1": {
    name: "Mission 1: Ring to Torus Evolution",
    desc: "Cut the 16-node ring diameter from 8 down to &le; 4 hops by adding wrap-around and cross-links while keeping node degree (radix) &le; 4.",
    numNodes: 16,
    reqMaxDiameter: 4,
    reqMaxRadix: 4,
    reqMinBisection: 4,
    preset: "ring"
  },
  "2": {
    name: "Mission 2: 16-Node 4D Hypercube",
    desc: "Construct a 4-dimensional binary hypercube ($D=4$, radix $k=4$, bisection $\\ge 8$). Every node has 4 links flipping binary bit coordinates.",
    numNodes: 16,
    reqMaxDiameter: 4,
    reqMaxRadix: 4,
    reqMinBisection: 8,
    preset: "custom"
  },
  "3": {
    name: "Mission 3: High-Radix Dragonfly",
    desc: "Partition 16 nodes into 4 dense local cliques (groups of 4) with sparse inter-group global channels, keeping total wire packaging cost under $130.",
    numNodes: 16,
    reqMaxDiameter: 3,
    reqMaxRadix: 5,
    reqMaxCost: 130,
    preset: "custom"
  },
  "4": {
    name: "Mission 4: 2-Tier Fat-Tree Clos Network",
    desc: "Wire a 2-stage hierarchical Fat-Tree connecting 8 compute nodes to 4 spine routers with non-blocking full bisection bandwidth ($B \\ge 4$).",
    numNodes: 12,
    reqMaxDiameter: 3,
    reqMaxRadix: 4,
    reqMinBisection: 4,
    preset: "custom"
  },
  "5": {
    name: "Mission 5: Small-World Shortcut Optimizer",
    desc: "Given an irregular cluster of 16 nodes, achieve an average path length $\\le 2.20$ hops by strategic shortcut insertion with max radix $\\le 4$.",
    numNodes: 16,
    reqMaxAvgHops: 2.20,
    reqMaxRadix: 4,
    preset: "mesh"
  },
  "sandbox": {
    name: "Free Exascale Sandbox Mode",
    desc: "Experiment freely! Connect custom graph topologies, measure graph properties, and stress-test synthetic traffic patterns.",
    numNodes: 16,
    preset: "mesh"
  }
};

class TopologyArchitect {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.audio = new TopoAudio();

    this.numNodes = 16;
    this.nodes = []; // {id, x, y, vx, vy}
    this.edges = []; // array of {u, v}
    this.currentMissionId = "1";
    this.selectedNode = null;

    this.stressActive = false;
    this.stressTimer = 0.0;
    this.stressPackets = [];

    this.metrics = {
      diameter: 0,
      avgHops: 0.0,
      bisection: 0,
      maxRadix: 0,
      wireCost: 0,
      isConnected: false
    };

    this.initLayout('circle');
    this.bindEvents();
    this.loop = this.loop.bind(this);
    requestAnimationFrame(this.loop);
  }

  initLayout(type = 'circle') {
    this.nodes = [];
    this.edges = [];
    this.selectedNode = null;
    const cx = this.canvas.width / 2;
    const cy = this.canvas.height / 2;

    if (type === 'circle') {
      const radius = 175;
      for (let i = 0; i < this.numNodes; i++) {
        const ang = (i / this.numNodes) * Math.PI * 2 - Math.PI / 2;
        this.nodes.push({
          id: i,
          x: cx + Math.cos(ang) * radius,
          y: cy + Math.sin(ang) * radius,
          rad: 14
        });
      }
    } else if (type === 'grid') {
      const cols = 4;
      const rows = 4;
      const startX = 140;
      const startY = 80;
      const stepX = 110;
      const stepY = 95;
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          this.nodes.push({
            id: r * cols + c,
            x: startX + c * stepX,
            y: startY + r * stepY,
            rad: 14
          });
        }
      }
    }
  }

  bindEvents() {
    this.canvas.addEventListener('click', (e) => {
      this.audio.init();
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.canvas.width / rect.width;
      const scaleY = this.canvas.height / rect.height;
      const mx = (e.clientX - rect.left) * scaleX;
      const my = (e.clientY - rect.top) * scaleY;

      const clickedNode = this.getNodeAtPixel(mx, my);
      if (clickedNode === null) {
        this.selectedNode = null;
        return;
      }

      if (this.selectedNode === null) {
        this.selectedNode = clickedNode;
      } else if (this.selectedNode === clickedNode) {
        this.selectedNode = null; // Deselect
      } else {
        // Toggle link between selectedNode and clickedNode
        this.toggleEdge(this.selectedNode, clickedNode);
        this.selectedNode = null;
        this.calculateMetrics();
      }
    });
  }

  getNodeAtPixel(px, py) {
    for (let i = 0; i < this.nodes.length; i++) {
      const n = this.nodes[i];
      const dist = Math.hypot(px - n.x, py - n.y);
      if (dist <= n.rad + 6) return i;
    }
    return null;
  }

  toggleEdge(u, v) {
    const minId = Math.min(u, v);
    const maxId = Math.max(u, v);
    const existing = this.edges.findIndex(e => e.u === minId && e.v === maxId);
    if (existing >= 0) {
      this.edges.splice(existing, 1);
    } else {
      this.edges.push({ u: minId, v: maxId });
      this.audio.playLink();
    }
  }

  applyPreset(preset) {
    this.edges = [];
    if (preset === 'ring') {
      this.initLayout('circle');
      for (let i = 0; i < this.numNodes; i++) {
        this.toggleEdge(i, (i + 1) % this.numNodes);
      }
    } else if (preset === 'mesh') {
      this.initLayout('grid');
      const cols = 4;
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          const idx = r * cols + c;
          if (c < 3) this.toggleEdge(idx, idx + 1);
          if (r < 3) this.toggleEdge(idx, idx + cols);
        }
      }
    } else if (preset === 'torus') {
      this.initLayout('grid');
      const cols = 4;
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          const idx = r * cols + c;
          this.toggleEdge(idx, r * cols + ((c + 1) % 4));
          this.toggleEdge(idx, ((r + 1) % 4) * cols + c);
        }
      }
    } else if (preset === 'hypercube') {
      this.initLayout('circle');
      for (let i = 0; i < 16; i++) {
        for (let bit = 0; bit < 4; bit++) {
          const neighbor = i ^ (1 << bit);
          if (neighbor > i) this.toggleEdge(i, neighbor);
        }
      }
    } else if (preset === 'dragonfly') {
      this.initLayout('circle');
      // 4 groups of 4: All-to-all inside each group
      for (let g = 0; g < 4; g++) {
        const base = g * 4;
        for (let a = 0; a < 4; a++) {
          for (let b = a + 1; b < 4; b++) {
            this.toggleEdge(base + a, base + b);
          }
        }
      }
      // Sparse global channels connecting groups
      this.toggleEdge(0, 4);
      this.toggleEdge(5, 8);
      this.toggleEdge(9, 12);
      this.toggleEdge(13, 1);
    }
    this.audio.playLink();
    this.calculateMetrics();
  }

  calculateMetrics() {
    const N = this.nodes.length;
    const adj = Array.from({ length: N }, () => []);
    const degrees = Array(N).fill(0);
    let totalLength = 0;

    this.edges.forEach(e => {
      adj[e.u].push(e.v);
      adj[e.v].push(e.u);
      degrees[e.u]++;
      degrees[e.v]++;
      const n1 = this.nodes[e.u];
      const n2 = this.nodes[e.v];
      totalLength += Math.hypot(n1.x - n2.x, n1.y - n2.y);
    });

    const maxRadix = degrees.length > 0 ? Math.max(...degrees) : 0;

    // Floyd-Warshall for All-Pairs Shortest Paths
    const dist = Array.from({ length: N }, () => Array(N).fill(Infinity));
    for (let i = 0; i < N; i++) dist[i][i] = 0;
    this.edges.forEach(e => {
      dist[e.u][e.v] = 1;
      dist[e.v][e.u] = 1;
    });

    for (let k = 0; k < N; k++) {
      for (let i = 0; i < N; i++) {
        for (let j = 0; j < N; j++) {
          if (dist[i][k] + dist[k][j] < dist[i][j]) {
            dist[i][j] = dist[i][k] + dist[k][j];
          }
        }
      }
    }

    let diameter = 0;
    let sumDist = 0;
    let pairs = 0;
    let isConnected = true;

    for (let i = 0; i < N; i++) {
      for (let j = i + 1; j < N; j++) {
        if (dist[i][j] === Infinity) {
          isConnected = false;
        } else {
          if (dist[i][j] > diameter) diameter = dist[i][j];
          sumDist += dist[i][j];
          pairs++;
        }
      }
    }

    const avgHops = pairs > 0 ? (sumDist / pairs).toFixed(2) : '0.00';

    // Bisection Bandwidth (Cut dividing nodes 0..N/2-1 vs N/2..N-1)
    let bisectionCut = 0;
    const half = Math.floor(N / 2);
    this.edges.forEach(e => {
      const inFirst = e.u < half;
      const inSecond = e.v < half;
      if (inFirst !== inSecond) bisectionCut++;
    });

    const wireCost = Math.round(totalLength * 0.05 + this.edges.length * 2.5);

    this.metrics = {
      diameter: isConnected ? diameter : 999,
      avgHops: isConnected ? parseFloat(avgHops) : 999,
      bisection: bisectionCut,
      maxRadix: maxRadix,
      wireCost: wireCost,
      isConnected: isConnected
    };

    // Update HUD
    document.getElementById('topoDiameter').textContent = isConnected ? diameter : '∞ (Broken)';
    document.getElementById('topoAvgHops').textContent = isConnected ? avgHops : '∞';
    document.getElementById('topoBisection').textContent = bisectionCut;
    document.getElementById('topoMaxRadix').textContent = maxRadix;
    document.getElementById('topoWireCost').textContent = wireCost;

    return this.metrics;
  }

  runStressTest() {
    this.audio.init();
    this.audio.playStress();
    this.calculateMetrics();
    this.stressActive = true;
    this.stressTimer = 2.5;
    this.stressPackets = [];

    // Spawn packets moving between nodes along edges
    this.edges.forEach(e => {
      for (let k = 0; k < 3; k++) {
        this.stressPackets.push({
          u: e.u,
          v: e.v,
          progress: Math.random(),
          speed: 0.5 + Math.random() * 0.5,
          color: '#38bdf8'
        });
      }
    });
  }

  evaluateMission() {
    const m = TOPO_MISSIONS[this.currentMissionId];
    if (!m) return;

    if (this.currentMissionId === 'sandbox') {
      this.showSuccessModal("Exascale sandbox topology validated! Graph metrics successfully calculated.", 3);
      return;
    }

    let pass = true;
    let failReason = [];

    if (!this.metrics.isConnected) {
      pass = false;
      failReason.push("Graph is disconnected! Ensure all nodes have valid routing paths.");
    }
    if (m.reqMaxDiameter && this.metrics.diameter > m.reqMaxDiameter) {
      pass = false;
      failReason.push(`Diameter ${this.metrics.diameter} hops exceeds maximum limit (${m.reqMaxDiameter} hops).`);
    }
    if (m.reqMaxAvgHops && this.metrics.avgHops > m.reqMaxAvgHops) {
      pass = false;
      failReason.push(`Average hop count ${this.metrics.avgHops} exceeds target (${m.reqMaxAvgHops} hops).`);
    }
    if (m.reqMinBisection && this.metrics.bisection < m.reqMinBisection) {
      pass = false;
      failReason.push(`Bisection bandwidth ${this.metrics.bisection} links is below target (${m.reqMinBisection}).`);
    }
    if (m.reqMaxRadix && this.metrics.maxRadix > m.reqMaxRadix) {
      pass = false;
      failReason.push(`Maximum router radix ${this.metrics.maxRadix} exceeds router pin limit (${m.reqMaxRadix}).`);
    }
    if (m.reqMaxCost && this.metrics.wireCost > m.reqMaxCost) {
      pass = false;
      failReason.push(`Wire packaging cost $${this.metrics.wireCost} exceeds budget ($${m.reqMaxCost}).`);
    }

    if (pass) {
      this.audio.playSuccess();
      let stars = 3;
      if (m.reqMaxCost && this.metrics.wireCost > m.reqMaxCost * 0.9) stars = 2;
      this.showSuccessModal(`Interconnect Graph successfully passed all ${m.name} specifications! Achieved Diameter ${this.metrics.diameter} and Bisection ${this.metrics.bisection}.`, stars);
    } else {
      this.audio.playFailure();
      this.showFailureModal(failReason.join("<br>"));
    }
  }

  showSuccessModal(summary, stars) {
    const modal = document.getElementById('topoSuccessModal');
    document.getElementById('topoSuccessSummary').innerHTML = summary;
    document.getElementById('topoStarsAwarded').textContent = '⭐'.repeat(stars);
    document.getElementById('topoStarsDisplay').textContent = '⭐'.repeat(stars);
    modal.style.display = 'flex';
  }

  showFailureModal(summary) {
    const modal = document.getElementById('topoFailureModal');
    document.getElementById('topoFailureSummary').innerHTML = summary;
    modal.style.display = 'flex';
  }

  update(dt) {
    if (this.stressActive) {
      this.stressTimer -= dt;
      this.stressPackets.forEach(p => {
        p.progress += p.speed * dt;
        if (p.progress >= 1.0) p.progress = 0.0;
      });

      if (this.stressTimer <= 0) {
        this.stressActive = false;
        this.evaluateMission();
      }
    }
  }

  draw() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 1. Draw Edges
    this.edges.forEach(e => {
      const n1 = this.nodes[e.u];
      const n2 = this.nodes[e.v];
      this.ctx.strokeStyle = '#334155';
      this.ctx.lineWidth = 2.5;
      this.ctx.beginPath();
      this.ctx.moveTo(n1.x, n1.y);
      this.ctx.lineTo(n2.x, n2.y);
      this.ctx.stroke();
    });

    // 2. Draw In-Flight Stress Packets
    if (this.stressActive) {
      this.stressPackets.forEach(p => {
        const n1 = this.nodes[p.u];
        const n2 = this.nodes[p.v];
        const curX = n1.x + (n2.x - n1.x) * p.progress;
        const curY = n1.y + (n2.y - n1.y) * p.progress;

        this.ctx.fillStyle = p.color;
        this.ctx.shadowColor = p.color;
        this.ctx.shadowBlur = 8;
        this.ctx.beginPath();
        this.ctx.arc(curX, curY, 4.5, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.shadowBlur = 0;
      });
    }

    // 3. Draw Nodes (Routers)
    this.nodes.forEach((n, idx) => {
      const isSelected = this.selectedNode === idx;

      // Outer Glow if Selected
      if (isSelected) {
        this.ctx.shadowColor = '#38bdf8';
        this.ctx.shadowBlur = 14;
      }

      this.ctx.fillStyle = isSelected ? '#38bdf8' : '#1e293b';
      this.ctx.beginPath();
      this.ctx.arc(n.x, n.y, n.rad, 0, Math.PI * 2);
      this.ctx.fill();

      this.ctx.strokeStyle = isSelected ? '#ffffff' : '#475569';
      this.ctx.lineWidth = isSelected ? 3 : 2;
      this.ctx.stroke();
      this.ctx.shadowBlur = 0;

      // Label
      this.ctx.fillStyle = isSelected ? '#0f172a' : '#f8fafc';
      this.ctx.font = 'bold 11px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.fillText(n.id, n.x, n.y + 4);
    });

    // 4. Draw Header Overlay
    this.ctx.fillStyle = '#64748b';
    this.ctx.font = 'bold 11px "JetBrains Mono", monospace';
    this.ctx.textAlign = 'left';
    this.ctx.fillText(`TOPOLOGY GRAPH [${this.nodes.length} NODES · ${this.edges.length} LINKS]`, 25, 30);
  }

  loop(timestamp) {
    this.update(0.016);
    this.draw();
    requestAnimationFrame(this.loop);
  }
}

let topoArchitect = null;
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('topoCanvas')) {
    topoArchitect = new TopologyArchitect('topoCanvas');
    loadTopoMission('1');
  }
});

function loadTopoMission(id) {
  if (!topoArchitect) return;
  topoArchitect.currentMissionId = id;
  const m = TOPO_MISSIONS[id];
  if (!m) return;

  document.getElementById('topoTargetText').innerHTML = m.desc;
  document.getElementById('topoPresetSelect').value = m.preset;
  topoArchitect.applyPreset(m.preset);
}

function applyTopoPreset(preset) {
  if (topoArchitect) topoArchitect.applyPreset(preset);
}

function clearTopologyWires() {
  if (topoArchitect) {
    topoArchitect.edges = [];
    topoArchitect.calculateMetrics();
  }
}

function resetTopologyLayout() {
  if (topoArchitect) {
    topoArchitect.initLayout('circle');
    topoArchitect.calculateMetrics();
  }
}

function runTopologyStressTest() {
  if (topoArchitect) topoArchitect.runStressTest();
}

function toggleTopoSound() {
  if (!topoArchitect) return;
  topoArchitect.audio.enabled = !topoArchitect.audio.enabled;
  document.getElementById('topoSoundBtn').textContent = topoArchitect.audio.enabled ? '🔊 Sound: ON' : '🔈 Sound: OFF';
}

function closeTopoModal() {
  document.getElementById('topoSuccessModal').style.display = 'none';
  document.getElementById('topoFailureModal').style.display = 'none';
}

function nextTopoMission() {
  closeTopoModal();
  if (!topoArchitect) return;
  const nextId = String(parseInt(topoArchitect.currentMissionId) + 1);
  if (TOPO_MISSIONS[nextId]) {
    document.getElementById('topoMissionSelect').value = nextId;
    loadTopoMission(nextId);
  } else {
    document.getElementById('topoMissionSelect').value = 'sandbox';
    loadTopoMission('sandbox');
  }
}

function saveTopologyRecord() {
  if (!topoArchitect) return;
  const name = document.getElementById("topoCallsign").value.trim() || "Topology Titan";
  const org = document.getElementById("topoOrg").value.trim() || "Silicon Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const scoreVal = Math.round(1500 - topoArchitect.metrics.diameter * 80 - topoArchitect.metrics.wireCost * 2 + topoArchitect.metrics.bisection * 50);
  const record = {
    name: name,
    org: org,
    track: `Topology Titans (Mission ${topoArchitect.currentMissionId})`,
    score: Math.max(100, scoreVal),
    accuracy: topoArchitect.metrics.diameter, // Diameter achieved
    certId: `TOPO-M${topoArchitect.currentMissionId}-D${topoArchitect.metrics.diameter}`,
    date: dateStr,
    type: "topology"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("topoSaveConfirm").style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitTopologyToGithub() {
  if (!topoArchitect) return;
  const name = document.getElementById("topoCallsign").value.trim() || "Topology Titan";
  const org = document.getElementById("topoOrg").value.trim() || "Silicon Lab";
  const scoreVal = Math.round(1500 - topoArchitect.metrics.diameter * 80 - topoArchitect.metrics.wireCost * 2 + topoArchitect.metrics.bisection * 50);
  const title = `[topology-highscore] ${name} — Diam ${topoArchitect.metrics.diameter} hops (Mission ${topoArchitect.currentMissionId})`;
  const body = [
    "### Topology Titans Exascale Graph Architect High Score",
    `- **Architect**: ${name}`,
    `- **Institution/Handle**: ${org}`,
    `- **Mission**: Mission ${topoArchitect.currentMissionId}`,
    `- **Network Diameter**: ${topoArchitect.metrics.diameter} hops`,
    `- **Average Hops**: ${topoArchitect.metrics.avgHops}`,
    `- **Bisection Bandwidth**: ${topoArchitect.metrics.bisection} links`,
    `- **Wire Packaging Cost**: $${topoArchitect.metrics.wireCost}`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: scoreVal,
      mission: topoArchitect.currentMissionId,
      diameter: topoArchitect.metrics.diameter,
      bisection: topoArchitect.metrics.bisection,
      cost: topoArchitect.metrics.wireCost,
      type: "topology"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}
</script>
