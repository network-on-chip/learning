# 🏗️ Chiplet Tycoon: 2.5D/3D Multi-Die Architect

Step into the shoes of a Principal Silicon Packaging Architect. Construct heterogeneous multi-die Superchips by placing and interconnecting specialized silicon chiplets on silicon interposers and 3D TSV vertical stacks with UCIe Die-to-Die interfaces. Balance compute throughput, memory bandwidth walls, thermal coupling, and packaging yield economics to master 5 engineering campaigns or experiment freely in Sandbox Mode! High scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Mission / Campaign:</b>
      <select id="chipletMissionSelect" class="noc-sim-select" onchange="loadChipletMission(this.value)">
        <option value="1">Mission 1: The First UCIe Link (Warm-Up)</option>
        <option value="2">Mission 2: Breaking the Memory Wall (HBM Balance)</option>
        <option value="3">Mission 3: Edge Automotive AI (Strict Cost Budget)</option>
        <option value="4">Mission 4: 3D Stack Thermal Coupling Trap</option>
        <option value="5">Mission 5: Hyperscale AI Superchip (&gt; 3.0 TB/s)</option>
        <option value="sandbox">🛠️ Free Sandbox Mode (Unconstrained)</option>
      </select>
    </label>

    <label><b>Packaging Substrate:</b>
      <select id="chipletPackageType" class="noc-sim-select" onchange="setPackageType(this.value)">
        <option value="ucie_adv">UCIe-Advanced (Silicon Interposer / 0.25 pJ/bit / $18)</option>
        <option value="ucie_std">UCIe-Standard (Organic Substrate / 0.50 pJ/bit / $6)</option>
        <option value="tsv_3d">3D TSV Stack (Vertical / 0.10 pJ/bit / +12°C Heat)</option>
      </select>
    </label>

    <label><b>Select Chiplet to Place:</b>
      <select id="chipletPalette" class="noc-sim-select" onchange="setSelectedPalette(this.value)">
        <option value="npu">🧠 Tensor NPU Corelet ($12 · 120W · High GEMM)</option>
        <option value="cpu">⚡ High-Radix CPU Cluster ($15 · 80W · Low Latency)</option>
        <option value="hbm">💾 HBM3 Memory Stack ($25 · 30W · 1.2 TB/s Sink)</option>
        <option value="io">🌐 UCIe PCIe/CXL I/O Die ($8 · 20W · Host Bridge)</option>
        <option value="l3">📦 Shared L3 Cache Tile ($10 · 25W · Buffers Flits)</option>
        <option value="clear">🧹 Clear Socket (Remove Tile)</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button id="runBenchmarkBtn" class="noc-sim-btn" onclick="runChipletBenchmark()">▶ Execute Benchmark</button>
      <button class="noc-sim-btn secondary" onclick="autoWireTopology('mesh')">🔗 Auto-Wire Mesh</button>
      <button class="noc-sim-btn secondary" onclick="autoWireTopology('ring')">⭕ Auto-Wire Ring</button>
      <button class="noc-sim-btn secondary" onclick="clearAllWires()">✂️ Clear Wires</button>
      <button class="noc-sim-btn secondary" onclick="resetChipletFloorplan()">🔄 Reset Floorplan</button>
      <button id="chipletSoundBtn" class="noc-sim-btn secondary" onclick="toggleChipletSound()">🔊 Sound: ON</button>
    </div>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem; width:100%; margin-top:0.35rem;">
      <span style="color:var(--tcl-blue-600);">Throughput: <span id="chipletThroughput">0.00</span> TB/s</span>
      <span style="color:#22c55e;">D2D Latency: <span id="chipletLatency">0.0</span> ns</span>
      <span style="color:#f59e0b;">Total Cost: $<span id="chipletCost">0</span></span>
      <span style="color:#ef4444;">Peak Temp: <span id="chipletPeakTemp">45°C</span></span>
      <span style="color:#eab308; margin-left:auto;" id="chipletStarsDisplay">⭐⭐⭐</span>
    </div>
  </div>

  <div id="chipletMissionBrief" style="margin-bottom:0.75rem; padding:0.65rem 0.95rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; font-size:0.85rem; line-height:1.6;">
    <strong>Mission Objective:</strong> <span id="chipletTargetText">Assemble an AI inference sub-module with at least 1 Tensor NPU and 1 HBM3 stack interconnected with UCIe under $55 packaging cost.</span>
    <div style="font-size:0.8rem; color:#94a3b8; margin-top:2px;">💡 Click on an empty socket to place the chosen chiplet. Click between two placed chiplets to manually route an interposer wire!</div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="chipletCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Benchmark Success Modal -->
    <div id="chipletSuccessModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;">🏆</div>
      <h2 style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#4ade80;">SUPERCHIP VALIDATED!</h2>
      <p id="chipletSuccessSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:460px; margin-bottom:1.25rem; line-height:1.6;">
        All mission benchmarks met with outstanding bandwidth and packaging yield efficiency!
      </p>

      <div id="chipletStarsAwarded" style="font-size:1.8rem; margin-bottom:1rem;">⭐⭐⭐</div>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:0.85rem 1.25rem; margin-bottom:1.25rem; width:100%; max-width:400px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Architect Callsign:</label>
        <input type="text" id="chipletCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.5rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Package Architect" value="Packaging Guru">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Team:</label>
        <input type="text" id="chipletOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. AMD / Intel / TSMC" value="Multi-Die Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveChipletRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitChipletToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <button class="noc-sim-btn secondary" onclick="nextChipletMission()" style="color:#ffffff !important;">▶ Next Mission</button>
        <button class="noc-sim-btn secondary" onclick="closeChipletModal()" style="color:#ffffff !important;">Close</button>
      </div>
      <div id="chipletSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Design score successfully saved to your browser Leaderboard!
      </div>
    </div>

    <!-- Benchmark Failure Modal -->
    <div id="chipletFailureModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;">⚠️</div>
      <h2 style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">PACKAGING BENCHMARK FAILED</h2>
      <p id="chipletFailureSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:440px; margin-bottom:1.25rem; line-height:1.6;">
        Throughput target not met or budget exceeded.
      </p>
      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="closeChipletModal()" style="background:#0284c7;">🔄 Adjust Placement &amp; Retry</button>
      </div>
    </div>
  </div>

  <div id="chipletInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">🏗️ Multi-Die Packaging Theory &amp; UCIe Trade-Offs:</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Why Chiplets? (Murphy Yield Model):</strong> Manufacturing large monolithic dies ($> 600\text{ mm}^2$) suffers poor wafer yields due to random defect density ($D_0$). Partitioning into modular chiplets drastically cuts silicon scrap: $Y = (1 + A \cdot D_0 / \alpha)^{-\alpha}$.</li>
      <li><strong>UCIe-Advanced vs Standard:</strong> UCIe-Advanced utilizes high-density silicon interposers (or Intel EMIB / TSMC CoWoS) with fine 25-55µm bump pitch, achieving 32 Gbps/wire and 0.25 pJ/bit, but adds $18 base packaging cost. UCIe-Standard runs on low-cost organic substrate at 16 Gbps and 0.50 pJ/bit.</li>
      <li><strong>3D TSV Stacking:</strong> Stacking HBM or SRAM vertically gives ultra-wide 1024-bit interfaces with 0.10 pJ/bit and sub-nanosecond latency, but creates a <strong>thermal sandwich penalty (+12°C to +18°C)</strong> because heat must dissipate through micro-bumps.</li>
      <li><strong>HBM Bandwidth Sink:</strong> Memory-bound workloads (Transformer LLM GEMMs) stall without adjacent HBM3 stacks. Placing Shared L3 Cache tiles reduces memory trips by caching frequently accessed weights.</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Chiplet Tycoon
class ChipletAudio {
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

  playPlace() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.08);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.1);
    } catch(e) {}
  }

  playWire() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(587, now);
      osc.frequency.linearRampToValueAtTime(784, now + 0.09);
      gain.gain.setValueAtTime(0.1, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.11);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.11);
    } catch(e) {}
  }

  playBenchmark() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(150, now);
      osc.frequency.linearRampToValueAtTime(300, now + 0.4);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.45);
    } catch(e) {}
  }

  playFanfare() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const chord = [523.25, 659.25, 783.99, 1046.5]; // C major
      chord.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + idx * 0.07);
        gain.gain.setValueAtTime(0.12, now + idx * 0.07);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.07 + 0.25);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now + idx * 0.07);
        osc.stop(now + idx * 0.07 + 0.25);
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
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.linearRampToValueAtTime(110, now + 0.3);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } catch(e) {}
  }
}

const CHIPLET_DEFS = {
  npu: { name: 'Tensor NPU', icon: '🧠', cost: 12, power: 120, bwGen: 1.5, type: 'compute', color: '#8b5cf6' },
  cpu: { name: 'Radix CPU', icon: '⚡', cost: 15, power: 80, bwGen: 0.8, type: 'compute', color: '#0284c7' },
  hbm: { name: 'HBM3 Stack', icon: '💾', cost: 25, power: 30, bwGen: 1.2, type: 'memory', color: '#10b981' },
  io:  { name: 'UCIe I/O', icon: '🌐', cost: 8, power: 20, bwGen: 0.5, type: 'io', color: '#f59e0b' },
  l3:  { name: 'L3 Cache', icon: '📦', cost: 10, power: 25, bwGen: 0.6, type: 'cache', color: '#ec4899' }
};

const MISSIONS = {
  "1": {
    name: "Mission 1: The First UCIe Link",
    desc: "Assemble an AI inference sub-module with at least 1 Tensor NPU and 1 HBM3 stack interconnected with UCIe under $55 packaging cost.",
    reqMinNpu: 1,
    reqMinHbm: 1,
    reqMinBw: 0.8,
    reqMaxCost: 55,
    reqMaxTemp: 85
  },
  "2": {
    name: "Mission 2: Breaking the Memory Wall",
    desc: "Balance a high-throughput engine with at least 2 Tensor NPUs, 2 HBM3 stacks, and achieve > 1.8 TB/s sustained bandwidth with < 4.5 ns latency.",
    reqMinNpu: 2,
    reqMinHbm: 2,
    reqMinBw: 1.8,
    reqMaxCost: 95,
    reqMaxTemp: 85
  },
  "3": {
    name: "Mission 3: Edge Automotive AI",
    desc: "Construct an automotive ADAS cluster under a strict $45 total packaging budget. Utilize low-cost UCIe-Standard packaging with 1 CPU, 1 NPU, and 1 L3 Cache.",
    reqMinCpu: 1,
    reqMinNpu: 1,
    reqMinL3: 1,
    reqMinBw: 0.6,
    reqMaxCost: 45,
    reqMaxTemp: 80
  },
  "4": {
    name: "Mission 4: 3D Stack Thermal Coupling Trap",
    desc: "Deploy a 3D TSV vertical configuration with 2 NPUs and 2 HBM stacks achieving > 2.2 TB/s while keeping peak temperature under 90°C.",
    reqPackage: "tsv_3d",
    reqMinNpu: 2,
    reqMinHbm: 2,
    reqMinBw: 2.2,
    reqMaxCost: 110,
    reqMaxTemp: 90
  },
  "5": {
    name: "Mission 5: Hyperscale AI Superchip",
    desc: "Build an ultra-dense powerhouse with at least 3 NPUs, 2 HBMs, 1 L3 Cache, and 1 I/O die. Achieve > 3.0 TB/s cross-die bisection bandwidth!",
    reqMinNpu: 3,
    reqMinHbm: 2,
    reqMinBw: 3.0,
    reqMaxCost: 150,
    reqMaxTemp: 95
  },
  "sandbox": {
    name: "Free Sandbox Mode",
    desc: "No mission constraints! Place any chiplets, customize interconnect topologies, and benchmark experimental multi-die packages.",
    reqMinBw: 0.1,
    reqMaxCost: 9999,
    reqMaxTemp: 9999
  }
};

class ChipletArchitect {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.audio = new ChipletAudio();

    this.cols = 4;
    this.rows = 3;
    this.sockets = []; // array of 12 sockets
    this.wires = []; // list of {fromIdx, toIdx}
    this.selectedPalette = 'npu';
    this.packageType = 'ucie_adv'; // 'ucie_adv', 'ucie_std', 'tsv_3d'
    this.currentMissionId = '1';
    this.wireSourceIdx = null;

    this.benchmarkActive = false;
    this.benchmarkTimer = 0.0;
    this.flits = []; // animated flits during benchmark
    this.metrics = {
      throughput: 0.0,
      latency: 0.0,
      cost: 0,
      peakTemp: 45.0,
      stars: 3
    };

    this.initSockets();
    this.bindEvents();
    this.calculateStaticMetrics();
    this.loop = this.loop.bind(this);
    requestAnimationFrame(this.loop);
  }

  initSockets() {
    this.sockets = [];
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        this.sockets.push({
          c: c,
          r: r,
          chiplet: null // null or key in CHIPLET_DEFS
        });
      }
    }
    this.wires = [];
  }

  bindEvents() {
    this.canvas.addEventListener('click', (e) => {
      this.audio.init();
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.canvas.width / rect.width;
      const scaleY = this.canvas.height / rect.height;
      const mx = (e.clientX - rect.left) * scaleX;
      const my = (e.clientY - rect.top) * scaleY;

      const idx = this.getSocketIndexAtPixel(mx, my);
      if (idx === -1) {
        this.wireSourceIdx = null;
        return;
      }

      const sock = this.sockets[idx];

      // If palette is 'clear', remove chiplet
      if (this.selectedPalette === 'clear') {
        sock.chiplet = null;
        this.removeWiresAttachedTo(idx);
        this.wireSourceIdx = null;
        this.calculateStaticMetrics();
        return;
      }

      // If socket is empty, place selected chiplet
      if (!sock.chiplet) {
        sock.chiplet = this.selectedPalette;
        this.audio.playPlace();
        this.wireSourceIdx = null;
        this.calculateStaticMetrics();
        return;
      }

      // If socket has a chiplet, handle wire routing between two chiplets!
      if (this.wireSourceIdx === null) {
        this.wireSourceIdx = idx;
      } else if (this.wireSourceIdx === idx) {
        // Clicking same socket toggles palette replacement
        sock.chiplet = this.selectedPalette;
        this.audio.playPlace();
        this.wireSourceIdx = null;
        this.calculateStaticMetrics();
      } else {
        // Toggle wire between source and target
        this.toggleWire(this.wireSourceIdx, idx);
        this.wireSourceIdx = null;
        this.calculateStaticMetrics();
      }
    });
  }

  getSocketPixelBox(idx) {
    const padX = 45;
    const padY = 40;
    const cw = (this.canvas.width - padX * 2) / this.cols;
    const ch = (this.canvas.height - padY * 2) / this.rows;
    const c = idx % this.cols;
    const r = Math.floor(idx / this.cols);
    return {
      x: padX + c * cw + cw * 0.1,
      y: padY + r * ch + ch * 0.1,
      w: cw * 0.8,
      h: ch * 0.8,
      cx: padX + c * cw + cw * 0.5,
      cy: padY + r * ch + ch * 0.5
    };
  }

  getSocketIndexAtPixel(px, py) {
    for (let i = 0; i < this.sockets.length; i++) {
      const b = this.getSocketPixelBox(i);
      if (px >= b.x && px <= b.x + b.w && py >= b.y && py <= b.y + b.h) {
        return i;
      }
    }
    return -1;
  }

  toggleWire(fromIdx, toIdx) {
    const minI = Math.min(fromIdx, toIdx);
    const maxI = Math.max(fromIdx, toIdx);
    const existing = this.wires.findIndex(w => w.from === minI && w.to === maxI);
    if (existing >= 0) {
      this.wires.splice(existing, 1);
    } else {
      this.wires.push({ from: minI, to: maxI });
      this.audio.playWire();
    }
  }

  removeWiresAttachedTo(idx) {
    this.wires = this.wires.filter(w => w.from !== idx && w.to !== idx);
  }

  autoWireTopology(topo) {
    this.wires = [];
    const occupied = [];
    this.sockets.forEach((s, idx) => {
      if (s.chiplet) occupied.push(idx);
    });

    if (occupied.length < 2) return;

    if (topo === 'ring') {
      for (let i = 0; i < occupied.length; i++) {
        const next = (i + 1) % occupied.length;
        this.toggleWire(occupied[i], occupied[next]);
      }
    } else if (topo === 'mesh') {
      // Connect adjacent grid neighbors
      for (let i = 0; i < occupied.length; i++) {
        for (let j = i + 1; j < occupied.length; j++) {
          const idxA = occupied[i];
          const idxB = occupied[j];
          const cA = idxA % this.cols, rA = Math.floor(idxA / this.cols);
          const cB = idxB % this.cols, rB = Math.floor(idxB / this.cols);
          const dist = Math.abs(cA - cB) + Math.abs(rA - rB);
          if (dist === 1) {
            this.toggleWire(idxA, idxB);
          }
        }
      }
    }
    this.audio.playWire();
    this.calculateStaticMetrics();
  }

  clearWires() {
    this.wires = [];
    this.calculateStaticMetrics();
  }

  resetFloorplan() {
    this.initSockets();
    this.wireSourceIdx = null;
    this.calculateStaticMetrics();
  }

  calculateStaticMetrics() {
    let chipletCost = 0;
    let totalPower = 0;
    let numNpu = 0;
    let numCpu = 0;
    let numHbm = 0;
    let numL3 = 0;
    let numIo = 0;

    this.sockets.forEach(s => {
      if (s.chiplet && CHIPLET_DEFS[s.chiplet]) {
        const def = CHIPLET_DEFS[s.chiplet];
        chipletCost += def.cost;
        totalPower += def.power;
        if (s.chiplet === 'npu') numNpu++;
        if (s.chiplet === 'cpu') numCpu++;
        if (s.chiplet === 'hbm') numHbm++;
        if (s.chiplet === 'l3') numL3++;
        if (s.chiplet === 'io') numIo++;
      }
    });

    // Base packaging cost based on technology
    let basePkgCost = 6;
    let linkMultiplier = 1.0;
    let wireCost = this.wires.length * 1.5;
    let latencyBase = 2.0;
    let thermalPenalty = 0;

    if (this.packageType === 'ucie_adv') {
      basePkgCost = 18;
      linkMultiplier = 1.6;
      latencyBase = 0.8;
      thermalPenalty = 4;
    } else if (this.packageType === 'tsv_3d') {
      basePkgCost = 28;
      linkMultiplier = 2.2;
      latencyBase = 0.3;
      thermalPenalty = 14;
    }

    const totalCost = chipletCost + (chipletCost > 0 ? basePkgCost : 0) + Math.round(wireCost);

    // Bandwidth calculation based on wires and placed chiplet capacity
    let rawBw = 0.0;
    this.wires.forEach(w => {
      const sockA = this.sockets[w.from];
      const sockB = this.sockets[w.to];
      if (sockA.chiplet && sockB.chiplet) {
        const defA = CHIPLET_DEFS[sockA.chiplet];
        const defB = CHIPLET_DEFS[sockB.chiplet];
        const linkCap = Math.min(defA.bwGen, defB.bwGen) * linkMultiplier;
        rawBw += linkCap;
      }
    });

    // HBM and Cache synergy
    let synergyMultiplier = 1.0;
    if (numHbm > 0 && numNpu > 0) synergyMultiplier += Math.min(1.0, (numHbm / numNpu) * 0.4);
    if (numL3 > 0) synergyMultiplier += 0.2;

    const finalBw = Math.min(6.0, rawBw * synergyMultiplier * 0.45);
    const finalLatency = finalBw > 0 ? (latencyBase + 6.0 / (finalBw + 0.5)).toFixed(1) : '0.0';
    const peakTemp = (45.0 + totalPower * 0.12 + thermalPenalty).toFixed(1);

    this.metrics.throughput = finalBw;
    this.metrics.latency = parseFloat(finalLatency);
    this.metrics.cost = totalCost;
    this.metrics.peakTemp = parseFloat(peakTemp);
    this.metrics.numNpu = numNpu;
    this.metrics.numCpu = numCpu;
    this.metrics.numHbm = numHbm;
    this.metrics.numL3 = numL3;

    // Update HUD
    document.getElementById('chipletThroughput').textContent = finalBw.toFixed(2);
    document.getElementById('chipletLatency').textContent = finalLatency;
    document.getElementById('chipletCost').textContent = totalCost;
    document.getElementById('chipletPeakTemp').textContent = `${peakTemp}°C`;

    return this.metrics;
  }

  runBenchmark() {
    this.audio.init();
    this.audio.playBenchmark();
    this.calculateStaticMetrics();
    this.benchmarkActive = true;
    this.benchmarkTimer = 2.5; // 2.5 seconds of live animated flits
    this.flits = [];

    // Spawn test flits along wires
    this.wires.forEach(w => {
      for (let k = 0; k < 4; k++) {
        this.flits.push({
          from: w.from,
          to: w.to,
          progress: Math.random(),
          speed: 0.6 + Math.random() * 0.5,
          color: '#38bdf8'
        });
      }
    });
  }

  evaluateMission() {
    const m = MISSIONS[this.currentMissionId];
    if (!m) return;

    if (this.currentMissionId === 'sandbox') {
      this.showSuccessModal("Sandbox benchmark completed! Superchip configuration analyzed successfully.", 3);
      return;
    }

    let pass = true;
    let failReason = [];

    if (m.reqMinNpu && (this.metrics.numNpu || 0) < m.reqMinNpu) {
      pass = false;
      failReason.push(`Requires at least ${m.reqMinNpu} Tensor NPU chiplet(s).`);
    }
    if (m.reqMinHbm && (this.metrics.numHbm || 0) < m.reqMinHbm) {
      pass = false;
      failReason.push(`Requires at least ${m.reqMinHbm} HBM3 Memory stack(s).`);
    }
    if (m.reqMinCpu && (this.metrics.numCpu || 0) < m.reqMinCpu) {
      pass = false;
      failReason.push(`Requires at least ${m.reqMinCpu} CPU cluster(s).`);
    }
    if (m.reqMinL3 && (this.metrics.numL3 || 0) < m.reqMinL3) {
      pass = false;
      failReason.push(`Requires at least ${m.reqMinL3} Shared L3 Cache tile(s).`);
    }
    if (m.reqPackage && this.packageType !== m.reqPackage) {
      pass = false;
      failReason.push(`Requires '${m.reqPackage.toUpperCase()}' packaging standard.`);
    }
    if (this.metrics.throughput < m.reqMinBw) {
      pass = false;
      failReason.push(`Throughput ${this.metrics.throughput.toFixed(2)} TB/s is below target (${m.reqMinBw} TB/s). Add interposer wires or HBM.`);
    }
    if (this.metrics.cost > m.reqMaxCost) {
      pass = false;
      failReason.push(`Total cost $${this.metrics.cost} exceeds budget ceiling ($${m.reqMaxCost}).`);
    }
    if (this.metrics.peakTemp > m.reqMaxTemp) {
      pass = false;
      failReason.push(`Peak temperature ${this.metrics.peakTemp}°C exceeds thermal ceiling (${m.reqMaxTemp}°C).`);
    }

    if (pass) {
      let stars = 1;
      if (this.metrics.throughput >= m.reqMinBw * 1.25 && this.metrics.cost <= m.reqMaxCost * 0.9) stars = 3;
      else if (this.metrics.throughput >= m.reqMinBw * 1.1) stars = 2;
      
      this.audio.playFanfare();
      this.showSuccessModal(`Superchip successfully passed all ${m.name} specifications! Sustained ${this.metrics.throughput.toFixed(2)} TB/s bandwidth at $${this.metrics.cost} packaging cost.`, stars);
    } else {
      this.audio.playFailure();
      this.showFailureModal(failReason.join("<br>"));
    }
  }

  showSuccessModal(summary, stars) {
    const modal = document.getElementById('chipletSuccessModal');
    document.getElementById('chipletSuccessSummary').innerHTML = summary;
    document.getElementById('chipletStarsAwarded').textContent = '⭐'.repeat(stars);
    document.getElementById('chipletStarsDisplay').textContent = '⭐'.repeat(stars);
    modal.style.display = 'flex';
  }

  showFailureModal(summary) {
    const modal = document.getElementById('chipletFailureModal');
    document.getElementById('chipletFailureSummary').innerHTML = summary;
    modal.style.display = 'flex';
  }

  update(dt) {
    if (this.benchmarkActive) {
      this.benchmarkTimer -= dt;
      this.flits.forEach(f => {
        f.progress += f.speed * dt;
        if (f.progress >= 1.0) f.progress = 0.0;
      });

      if (this.benchmarkTimer <= 0) {
        this.benchmarkActive = false;
        this.evaluateMission();
      }
    }
  }

  draw() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 1. Draw Silicon Interposer Base Substrate
    this.ctx.strokeStyle = this.packageType === 'tsv_3d' ? '#ec4899' : (this.packageType === 'ucie_adv' ? '#38bdf8' : '#10b981');
    this.ctx.lineWidth = 2;
    this.ctx.strokeRect(25, 20, this.canvas.width - 50, this.canvas.height - 40);

    this.ctx.fillStyle = 'rgba(255, 255, 255, 0.03)';
    this.ctx.fillRect(25, 20, this.canvas.width - 50, this.canvas.height - 40);

    // Substrate Label Header
    this.ctx.fillStyle = '#64748b';
    this.ctx.font = 'bold 11px "JetBrains Mono", monospace';
    this.ctx.textAlign = 'left';
    let pkgLabel = "SUBSTRATE: ORGANIC STANDARD (UCIe-S 16G)";
    if (this.packageType === 'ucie_adv') pkgLabel = "SUBSTRATE: SILICON INTERPOSER (UCIe-A 32G / EMIB)";
    if (this.packageType === 'tsv_3d') pkgLabel = "SUBSTRATE: 3D TSV VERTICAL STACK (64G D2D)";
    this.ctx.fillText(pkgLabel, 35, 36);

    // 2. Draw Interposer Wires
    this.wires.forEach(w => {
      const boxA = this.getSocketPixelBox(w.from);
      const boxB = this.getSocketPixelBox(w.to);

      this.ctx.strokeStyle = '#38bdf8';
      this.ctx.lineWidth = 3.5;
      this.ctx.beginPath();
      this.ctx.moveTo(boxA.cx, boxA.cy);
      this.ctx.lineTo(boxB.cx, boxB.cy);
      this.ctx.stroke();

      // D2D PHY bump pads at both ends
      this.ctx.fillStyle = '#0284c7';
      this.ctx.beginPath();
      this.ctx.arc(boxA.cx, boxA.cy, 6, 0, Math.PI * 2);
      this.ctx.arc(boxB.cx, boxB.cy, 6, 0, Math.PI * 2);
      this.ctx.fill();
    });

    // 3. Draw Sockets & Chiplets
    this.sockets.forEach((s, idx) => {
      const b = this.getSocketPixelBox(idx);
      const isSelected = this.wireSourceIdx === idx;

      if (!s.chiplet) {
        // Empty Socket
        this.ctx.strokeStyle = '#334155';
        this.ctx.lineWidth = 1.5;
        this.ctx.setLineDash([4, 4]);
        this.ctx.strokeRect(b.x, b.y, b.w, b.h);
        this.ctx.setLineDash([]);

        this.ctx.fillStyle = '#475569';
        this.ctx.font = '11px "Inter", sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(`Socket [${s.c},${s.r}]`, b.cx, b.cy - 6);
        this.ctx.fillText('+ Click to Place', b.cx, b.cy + 12);
      } else {
        // Occupied Chiplet
        const def = CHIPLET_DEFS[s.chiplet];
        this.ctx.fillStyle = def.color;
        this.ctx.beginPath();
        this.ctx.roundRect(b.x, b.y, b.w, b.h, 8);
        this.ctx.fill();

        this.ctx.strokeStyle = isSelected ? '#f59e0b' : '#f8fafc';
        this.ctx.lineWidth = isSelected ? 3.5 : 1.5;
        this.ctx.stroke();

        // Icon & Name
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '20px "Segoe UI Emoji", sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(def.icon, b.cx, b.cy - 10);

        this.ctx.font = 'bold 12px "JetBrains Mono", monospace';
        this.ctx.fillText(def.name, b.cx, b.cy + 10);

        this.ctx.font = '10px "Inter", sans-serif';
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
        this.ctx.fillText(`$${def.cost} · ${def.power}W`, b.cx, b.cy + 24);
      }
    });

    // 4. Draw Animated Flits during Benchmark
    if (this.benchmarkActive) {
      this.flits.forEach(f => {
        const boxA = this.getSocketPixelBox(f.from);
        const boxB = this.getSocketPixelBox(f.to);
        const curX = boxA.cx + (boxB.cx - boxA.cx) * f.progress;
        const curY = boxA.cy + (boxB.cy - boxA.cy) * f.progress;

        this.ctx.fillStyle = f.color;
        this.ctx.shadowColor = f.color;
        this.ctx.shadowBlur = 8;
        this.ctx.beginPath();
        this.ctx.arc(curX, curY, 5, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.shadowBlur = 0;
      });

      // Benchmark Watermark Banner
      this.ctx.fillStyle = 'rgba(2, 132, 199, 0.2)';
      this.ctx.fillRect(0, this.canvas.height - 35, this.canvas.width, 35);
      this.ctx.fillStyle = '#38bdf8';
      this.ctx.font = 'bold 13px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.fillText(`⚡ EXECUTING MULTI-DIE TRAFFIC BENCHMARK... (${this.benchmarkTimer.toFixed(1)}s)`, this.canvas.width / 2, this.canvas.height - 12);
    }
  }

  loop(timestamp) {
    this.update(0.016);
    this.draw();
    requestAnimationFrame(this.loop);
  }
}

let chipletArchitect = null;
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('chipletCanvas')) {
    chipletArchitect = new ChipletArchitect('chipletCanvas');
    loadChipletMission('1');
  }
});

function loadChipletMission(id) {
  if (!chipletArchitect) return;
  chipletArchitect.currentMissionId = id;
  const m = MISSIONS[id];
  if (!m) return;

  document.getElementById('chipletTargetText').textContent = m.desc;
  chipletArchitect.resetFloorplan();
}

function setPackageType(type) {
  if (chipletArchitect) {
    chipletArchitect.packageType = type;
    chipletArchitect.calculateStaticMetrics();
  }
}

function setSelectedPalette(type) {
  if (chipletArchitect) {
    chipletArchitect.selectedPalette = type;
  }
}

function runChipletBenchmark() {
  if (chipletArchitect) chipletArchitect.runBenchmark();
}

function autoWireTopology(topo) {
  if (chipletArchitect) chipletArchitect.autoWireTopology(topo);
}

function clearAllWires() {
  if (chipletArchitect) chipletArchitect.clearWires();
}

function resetChipletFloorplan() {
  if (chipletArchitect) chipletArchitect.resetFloorplan();
}

function toggleChipletSound() {
  if (!chipletArchitect) return;
  chipletArchitect.audio.enabled = !chipletArchitect.audio.enabled;
  document.getElementById('chipletSoundBtn').textContent = chipletArchitect.audio.enabled ? '🔊 Sound: ON' : '🔈 Sound: OFF';
}

function closeChipletModal() {
  document.getElementById('chipletSuccessModal').style.display = 'none';
  document.getElementById('chipletFailureModal').style.display = 'none';
}

function nextChipletMission() {
  closeChipletModal();
  if (!chipletArchitect) return;
  const nextId = String(parseInt(chipletArchitect.currentMissionId) + 1);
  if (MISSIONS[nextId]) {
    document.getElementById('chipletMissionSelect').value = nextId;
    loadChipletMission(nextId);
  } else {
    document.getElementById('chipletMissionSelect').value = 'sandbox';
    loadChipletMission('sandbox');
  }
}

function saveChipletRecord() {
  if (!chipletArchitect) return;
  const name = document.getElementById("chipletCallsign").value.trim() || "Packaging Guru";
  const org = document.getElementById("chipletOrg").value.trim() || "Multi-Die Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const scoreVal = Math.round(chipletArchitect.metrics.throughput * 1000 - chipletArchitect.metrics.cost * 5);
  const record = {
    name: name,
    org: org,
    track: `Chiplet Tycoon (Mission ${chipletArchitect.currentMissionId})`,
    score: Math.max(100, scoreVal),
    accuracy: Math.round(chipletArchitect.metrics.throughput * 100) / 100, // TB/s achieved
    certId: `CHIPLET-M${chipletArchitect.currentMissionId}-${Math.round(chipletArchitect.metrics.throughput * 10)}`,
    date: dateStr,
    type: "chiplet"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("chipletSaveConfirm").style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitChipletToGithub() {
  if (!chipletArchitect) return;
  const name = document.getElementById("chipletCallsign").value.trim() || "Packaging Guru";
  const org = document.getElementById("chipletOrg").value.trim() || "Multi-Die Lab";
  const scoreVal = Math.round(chipletArchitect.metrics.throughput * 1000 - chipletArchitect.metrics.cost * 5);
  const title = `[chiplet-highscore] ${name} — ${chipletArchitect.metrics.throughput.toFixed(2)} TB/s (Mission ${chipletArchitect.currentMissionId})`;
  const body = [
    "### Chiplet Tycoon Multi-Die Architect High Score",
    `- **Architect**: ${name}`,
    `- **Institution/Team**: ${org}`,
    `- **Mission**: Mission ${chipletArchitect.currentMissionId}`,
    `- **Sustained Bandwidth**: ${chipletArchitect.metrics.throughput.toFixed(2)} TB/s`,
    `- **Package Cost**: $${chipletArchitect.metrics.cost}`,
    `- **D2D Latency**: ${chipletArchitect.metrics.latency.toFixed(1)} ns`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: scoreVal,
      mission: chipletArchitect.currentMissionId,
      throughput_tbs: chipletArchitect.metrics.throughput.toFixed(2),
      cost: chipletArchitect.metrics.cost,
      type: "chiplet"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}
</script>
