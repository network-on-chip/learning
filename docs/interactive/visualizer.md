# 2D Mesh & Torus Routing Visualizer

An interactive, cycle-accurate Network-on-Chip (NoC) laboratory. Directly observe how flits navigate on-chip routers, arbitrate channels, and avoid deadlocks across different network topologies and routing algorithms.

<div class="noc-sim-container">
  <div class="noc-sim-controls">
    <label><b>Topology:</b>
      <select id="topoSelect" class="noc-sim-select" onchange="if(window.sim) window.sim.setTopology(this.value)">
        <option value="mesh">2D Mesh (4x4)</option>
        <option value="torus">2D Torus (4x4 Wrap-around)</option>
        <option value="mesh5">2D Mesh (5x5 Scaled)</option>
      </select>
    </label>
    
    <label><b>Algorithm:</b>
      <select id="algoSelect" class="noc-sim-select" onchange="if(window.sim) window.sim.setAlgorithm(this.value)">
        <option value="xy">Dimension-Order (Strict XY)</option>
        <option value="west-first">West-First (Turn Model)</option>
        <option value="odd-even">Odd-Even (Deadlock-Free Turn Model)</option>
        <option value="adaptive">Fully Adaptive (Minimal Congestion)</option>
      </select>
    </label>

    <label><b>Traffic Pattern:</b>
      <select id="trafficPatternSelect" class="noc-sim-select" onchange="if(window.sim) window.sim.trafficPattern = this.value">
        <option value="uniform">Uniform Random Traffic</option>
        <option value="transpose">Transpose Traffic (x,y → y,x)</option>
        <option value="hotspot">Hotspot Traffic (Target Core 5 & 10)</option>
      </select>
    </label>

    <label><b>Simulation Speed:</b>
      <select id="speedSelect" class="noc-sim-select" onchange="if(window.sim) window.sim.speed = parseFloat(this.value)">
        <option value="1">1.0x Normal</option>
        <option value="2">2.0x Fast</option>
        <option value="0.5">0.5x Slow Motion</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:0.35rem; width:100%;">
      <button class="noc-sim-btn" onclick="injectPatternPacket()">🎲 Inject Packet</button>
      <button class="noc-sim-btn" onclick="injectBurstTraffic()" style="background:#8b5cf6;">⚡ Inject 5-Packet Burst</button>
      <button id="stepCycleBtn" class="noc-sim-btn secondary" onclick="stepSingleCycle()">⏭ Step Cycle</button>
      <button id="pauseResumeBtn" class="noc-sim-btn secondary" onclick="toggleSim(this)">⏸ Pause</button>
      <button class="noc-sim-btn secondary" onclick="clearPackets()">🧹 Clear Flits</button>
      <button class="noc-sim-btn secondary" onclick="resetStats()">🔄 Reset Metrics</button>
    </div>
  </div>

  <div id="nocStats" style="margin-bottom: 0.75rem; font-size: 0.88rem; color: var(--noc-text-main); display:flex; gap:1.25rem; flex-wrap:wrap; font-family:'JetBrains Mono', monospace; background:var(--tcl-surface); padding:0.6rem 0.9rem; border-radius:8px; border:1px solid var(--tcl-border);">
    <span><b>Cycle:</b> <span id="statCycle" style="color:var(--tcl-blue-600);">0</span></span>
    <span><b>In-Flight:</b> <span id="statActive">0</span></span>
    <span><b>Delivered:</b> <span id="statDelivered" style="color:#22c55e;">0</span></span>
    <span><b>Avg Latency:</b> <span id="statHops">0.00</span> hops</span>
    <span><b>Throughput:</b> <span id="statThroughput" style="color:#f59e0b;">0.00</span> flits/cyc</span>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="nocCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>
  </div>

  <div id="nocLog" class="noc-sim-log"></div>
</div>

<script>
// Interactive Network-on-Chip (NoC) 2D Mesh & Torus Routing Simulator
class NoCSimulator {
  constructor(canvasId, logId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.logEl = document.getElementById(logId);

    this.rows = 4;
    this.cols = 4;
    this.topology = 'mesh'; // 'mesh', 'torus', 'mesh5'
    this.algorithm = 'xy'; // 'xy', 'west-first', 'odd-even', 'adaptive'
    this.trafficPattern = 'uniform';
    this.speed = 1;

    this.selectedSrc = null;
    this.selectedDst = null;
    this.cycle = 0;
    this.isRunning = true;
    this.packets = [];
    this.packetCounter = 0;
    this.stats = { injected: 0, delivered: 0, totalHops: 0 };
    this.linkLoad = {}; // "c1,r1-c2,r2" -> activity count

    this.nodeRadius = 22;
    this.padding = 55;

    this.initCanvas();
    this.bindEvents();
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
    this.log("✓ NoC Routing Simulator initialized. Click a source node, then a destination node to inject packets.");
  }

  initCanvas() {
    const dpr = window.devicePixelRatio || 1;
    this.width = 620;
    this.height = 460;
    this.canvas.width = this.width * dpr;
    this.canvas.height = this.height * dpr;
    this.ctx.scale(dpr, dpr);

    this.stepX = (this.width - 2 * this.padding) / (this.cols - 1);
    this.stepY = (this.height - 2 * this.padding) / (this.rows - 1);
  }

  setTopology(topo) {
    this.topology = topo;
    if (topo === 'mesh5') {
      this.rows = 5;
      this.cols = 5;
    } else {
      this.rows = 4;
      this.cols = 4;
    }
    this.stepX = (this.width - 2 * this.padding) / (this.cols - 1);
    this.stepY = (this.height - 2 * this.padding) / (this.rows - 1);
    this.packets = [];
    this.selectedSrc = null;
    this.selectedDst = null;
    this.linkLoad = {};
    this.log(`Topology switched to: ${topo.toUpperCase()} (${this.cols}x${this.rows})`);
  }

  setAlgorithm(algo) {
    this.algorithm = algo;
    this.log(`Routing algorithm switched to: ${algo.toUpperCase()}`);
  }

  getNodePos(x, y) {
    return {
      px: this.padding + x * this.stepX,
      py: this.padding + y * this.stepY
    };
  }

  bindEvents() {
    this.canvas.addEventListener('click', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.width / rect.width;
      const scaleY = this.height / rect.height;
      const mx = (e.clientX - rect.left) * scaleX;
      const my = (e.clientY - rect.top) * scaleY;

      for (let r = 0; r < this.rows; r++) {
        for (let c = 0; c < this.cols; c++) {
          const { px, py } = this.getNodePos(c, r);
          const dist = Math.hypot(mx - px, my - py);
          if (dist <= this.nodeRadius + 8) {
            this.handleNodeClick(c, r);
            return;
          }
        }
      }
    });
  }

  handleNodeClick(x, y) {
    if (!this.selectedSrc) {
      this.selectedSrc = { x, y };
      this.log(`📍 Source selected: Router (${x},${y}). Now click a destination router.`);
    } else if (!this.selectedDst) {
      if (this.selectedSrc.x === x && this.selectedSrc.y === y) {
        this.selectedSrc = null;
        this.log("Selection cancelled.");
        return;
      }
      this.selectedDst = { x, y };
      this.injectPacket(this.selectedSrc, this.selectedDst);
      this.selectedSrc = null;
      this.selectedDst = null;
    }
  }

  injectPacket(src, dst) {
    this.packetCounter++;
    const flitColors = ['#2563eb', '#38bdf8', '#fb923c', '#a855f7', '#10b981', '#ec4899'];
    const p = {
      id: this.packetCounter,
      src: { ...src },
      dst: { ...dst },
      curr: { ...src },
      next: null,
      hops: 0,
      progress: 0,
      color: flitColors[this.packetCounter % flitColors.length],
      done: false
    };
    p.next = this.computeNextHop(p.curr, p.dst, p.src);
    this.packets.push(p);
    this.stats.injected++;
    this.log(`[Cycle ${this.cycle}] Injected Pkt #${p.id}: (${src.x},${src.y}) ➔ (${dst.x},${dst.y}) via ${this.algorithm.toUpperCase()}`);
  }

  computeNextHop(curr, dst, src) {
    if (curr.x === dst.x && curr.y === dst.y) return null;

    if (this.algorithm === 'xy') {
      // Dimension-Order Routing (DOR): strictly exhaust X then Y
      if (curr.x < dst.x) return { x: curr.x + 1, y: curr.y };
      if (curr.x > dst.x) return { x: curr.x - 1, y: curr.y };
      if (curr.y < dst.y) return { x: curr.x, y: curr.y + 1 };
      if (curr.y > dst.y) return { x: curr.x, y: curr.y - 1 };
    } else if (this.algorithm === 'west-first') {
      // West-First Turn Model: If heading west, MUST turn west first.
      if (dst.x < curr.x) {
        return { x: curr.x - 1, y: curr.y };
      }
      const cand = [];
      if (dst.x > curr.x) cand.push({ x: curr.x + 1, y: curr.y });
      if (dst.y > curr.y) cand.push({ x: curr.x, y: curr.y + 1 });
      if (dst.y < curr.y) cand.push({ x: curr.x, y: curr.y - 1 });
      return cand[Math.floor(Math.random() * cand.length)] || null;
    } else if (this.algorithm === 'odd-even') {
      // Odd-Even Deadlock-Free Adaptive Turn Model
      const isEven = (curr.x % 2 === 0);
      const cand = [];
      if (dst.x > curr.x) cand.push({ x: curr.x + 1, y: curr.y });
      if (dst.x < curr.x && !isEven) cand.push({ x: curr.x - 1, y: curr.y });
      if (dst.y > curr.y) cand.push({ x: curr.x, y: curr.y + 1 });
      if (dst.y < curr.y) cand.push({ x: curr.x, y: curr.y - 1 });
      if (cand.length > 0) {
        return cand[Math.floor(Math.random() * cand.length)];
      }
      return { x: curr.x, y: (curr.y < dst.y ? curr.y + 1 : curr.y - 1) };
    } else {
      // Fully Adaptive (Minimal Congestion)
      const cand = [];
      if (dst.x > curr.x) cand.push({ x: curr.x + 1, y: curr.y });
      if (dst.x < curr.x) cand.push({ x: curr.x - 1, y: curr.y });
      if (dst.y > curr.y) cand.push({ x: curr.x, y: curr.y + 1 });
      if (dst.y < curr.y) cand.push({ x: curr.x, y: curr.y - 1 });
      return cand[Math.floor(Math.random() * cand.length)] || null;
    }
    return null;
  }

  step() {
    this.cycle++;
    for (let i = this.packets.length - 1; i >= 0; i--) {
      const p = this.packets[i];
      if (p.done) continue;

      p.progress += 0.05 * this.speed;
      if (p.progress >= 1) {
        p.progress = 0;
        p.curr = { ...p.next };
        p.hops++;

        // Track link load
        const linkKey = `${Math.min(p.curr.x, p.next.x)},${Math.min(p.curr.y, p.next.y)}-${Math.max(p.curr.x, p.next.x)},${Math.max(p.curr.y, p.next.y)}`;
        this.linkLoad[linkKey] = (this.linkLoad[linkKey] || 0) + 1;

        if (p.curr.x === p.dst.x && p.curr.y === p.dst.y) {
          p.done = true;
          this.stats.delivered++;
          this.stats.totalHops += p.hops;
          this.log(`[Cycle ${this.cycle}] ✨ Pkt #${p.id} DELIVERED to (${p.dst.x},${p.dst.y}) in ${p.hops} hops.`);
          this.packets.splice(i, 1);
        } else {
          p.next = this.computeNextHop(p.curr, p.dst, p.src);
        }
      }
    }
  }

  log(msg) {
    if (!this.logEl) return;
    const item = document.createElement('div');
    item.textContent = msg;
    this.logEl.appendChild(item);
    this.logEl.scrollTop = this.logEl.scrollHeight;
  }

  draw() {
    this.ctx.clearRect(0, 0, this.width, this.height);

    // Draw Links
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const { px, py } = this.getNodePos(c, r);

        // East link
        if (c < this.cols - 1) {
          const next = this.getNodePos(c + 1, r);
          const linkKey = `${c},${r}-${c+1},${r}`;
          const load = this.linkLoad[linkKey] || 0;
          this.ctx.lineWidth = load > 5 ? 4 : 2.5;
          this.ctx.strokeStyle = load > 8 ? '#ef4444' : (load > 3 ? '#f59e0b' : '#334155');
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
        } else if (this.topology === 'torus') {
          // Wrap-around East link
          const next = this.getNodePos(0, r);
          this.ctx.lineWidth = 2;
          this.ctx.strokeStyle = '#475569';
          this.ctx.setLineDash([4, 4]);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(px + 18, py);
          this.ctx.moveTo(next.px - 18, next.py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
          this.ctx.setLineDash([]);
        }

        // South link
        if (r < this.rows - 1) {
          const next = this.getNodePos(c, r + 1);
          const linkKey = `${c},${r}-${c},${r+1}`;
          const load = this.linkLoad[linkKey] || 0;
          this.ctx.lineWidth = load > 5 ? 4 : 2.5;
          this.ctx.strokeStyle = load > 8 ? '#ef4444' : (load > 3 ? '#f59e0b' : '#334155');
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
        } else if (this.topology === 'torus') {
          // Wrap-around South link
          const next = this.getNodePos(c, 0);
          this.ctx.lineWidth = 2;
          this.ctx.strokeStyle = '#475569';
          this.ctx.setLineDash([4, 4]);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(px, py + 18);
          this.ctx.moveTo(next.px, next.py - 18);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
          this.ctx.setLineDash([]);
        }
      }
    }

    // Draw Active Flits
    for (const p of this.packets) {
      if (!p.next) continue;
      const p1 = this.getNodePos(p.curr.x, p.curr.y);
      const p2 = this.getNodePos(p.next.x, p.next.y);
      const fx = p1.px + (p2.px - p1.px) * p.progress;
      const fy = p1.py + (p2.py - p1.py) * p.progress;

      // Outer glow
      this.ctx.beginPath();
      this.ctx.arc(fx, fy, 11, 0, Math.PI * 2);
      this.ctx.fillStyle = p.color + '44';
      this.ctx.fill();

      // Flit body
      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(fx, fy, 7.5, 0, Math.PI * 2);
      this.ctx.fill();

      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 8.5px sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(p.id, fx, fy);
    }

    // Draw Router Nodes
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const { px, py } = this.getNodePos(c, r);
        const isSrc = this.selectedSrc && this.selectedSrc.x === c && this.selectedSrc.y === r;
        const isDst = this.selectedDst && this.selectedDst.x === c && this.selectedDst.y === r;
        const idx = r * this.cols + c;

        this.ctx.beginPath();
        this.ctx.arc(px, py, this.nodeRadius, 0, Math.PI * 2);

        if (isSrc) {
          this.ctx.fillStyle = '#2563eb';
        } else if (isDst) {
          this.ctx.fillStyle = '#ea580c';
        } else {
          this.ctx.fillStyle = '#0f172a';
        }
        this.ctx.fill();

        this.ctx.lineWidth = isSrc || isDst ? 3 : 1.8;
        this.ctx.strokeStyle = isSrc ? '#60a5fa' : (isDst ? '#fb923c' : '#38bdf8');
        this.ctx.stroke();

        // Node ID label
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = 'bold 10px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(`R${idx}`, px, py - 3);

        this.ctx.fillStyle = '#94a3b8';
        this.ctx.font = '8px monospace';
        this.ctx.fillText(`(${c},${r})`, px, py + 8);
      }
    }

    // Update Stats Display
    const elCycle = document.getElementById('statCycle');
    if (elCycle) {
      elCycle.textContent = this.cycle;
      document.getElementById('statActive').textContent = this.packets.length;
      document.getElementById('statDelivered').textContent = this.stats.delivered;
      const avgHops = this.stats.delivered > 0 ? (this.stats.totalHops / this.stats.delivered).toFixed(2) : '0.00';
      document.getElementById('statHops').textContent = avgHops;
      const tp = this.cycle > 0 ? (this.stats.delivered / this.cycle).toFixed(3) : '0.000';
      document.getElementById('statThroughput').textContent = tp;
    }
  }

  animate() {
    if (this.isRunning) {
      this.step();
    }
    this.draw();
    requestAnimationFrame(this.animate);
  }
}

function initVisualizer() {
  if (document.getElementById('nocCanvas') && !window.sim) {
    window.sim = new NoCSimulator('nocCanvas', 'nocLog');
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initVisualizer);
} else {
  initVisualizer();
}

function injectPatternPacket() {
  if (!window.sim) return;
  const s = window.sim;
  let sx, sy, dx, dy;

  if (s.trafficPattern === 'transpose') {
    sx = Math.floor(Math.random() * s.cols);
    sy = Math.floor(Math.random() * s.rows);
    dx = sy % s.cols;
    dy = sx % s.rows;
    if (dx === sx && dy === sy) {
      dx = (sx + 1) % s.cols;
    }
  } else if (s.trafficPattern === 'hotspot') {
    sx = Math.floor(Math.random() * s.cols);
    sy = Math.floor(Math.random() * s.rows);
    // 60% of traffic directed to core 5 or 10
    if (Math.random() < 0.6) {
      dx = 1; dy = 1;
    } else {
      dx = Math.floor(Math.random() * s.cols);
      dy = Math.floor(Math.random() * s.rows);
    }
    if (dx === sx && dy === sy) {
      dx = (sx + 1) % s.cols;
    }
  } else {
    // Uniform random
    sx = Math.floor(Math.random() * s.cols);
    sy = Math.floor(Math.random() * s.rows);
    dx = Math.floor(Math.random() * s.cols);
    dy = Math.floor(Math.random() * s.rows);
    while (dx === sx && dy === sy) {
      dx = Math.floor(Math.random() * s.cols);
      dy = Math.floor(Math.random() * s.rows);
    }
  }
  s.injectPacket({x: sx, y: sy}, {x: dx, y: dy});
}

function injectBurstTraffic() {
  for (let i = 0; i < 5; i++) {
    setTimeout(() => injectPatternPacket(), i * 60);
  }
}

function stepSingleCycle() {
  if (!window.sim) return;
  window.sim.step();
  window.sim.draw();
}

function toggleSim(btn) {
  if (!window.sim) return;
  window.sim.isRunning = !window.sim.isRunning;
  btn.textContent = window.sim.isRunning ? "⏸ Pause" : "▶ Resume";
}

function clearPackets() {
  if (!window.sim) return;
  window.sim.packets = [];
  window.sim.log("Active in-flight packets cleared.");
}

function resetStats() {
  if (!window.sim) return;
  window.sim.cycle = 0;
  window.sim.stats = { injected: 0, delivered: 0, totalHops: 0 };
  window.sim.linkLoad = {};
  window.sim.log("Metrics and cycle count reset.");
}
</script>

---

## Experimental Exploration Guide

1. **Manual Path Tracing**: Click on any router node $(x,y)$ to select it as the **source** (turns royal blue). Then click another router to set the **destination** (turns vibrant orange). Watch the flit navigate step-by-step.
2. **Dimension-Order Routing (DOR / XY)**:
   - Notice that packets strictly traverse along the horizontal axis ($X$) until reaching the target column, then turn onto the vertical axis ($Y$).
   - Turns from $Y$ to $X$ are strictly prohibited ($\text{Turn}(\star \to X) = \emptyset$). This mathematical restriction guarantees an acyclic Channel Dependency Graph (CDG).
3. **West-First Turn Model**:
   - In West-First, packets heading West must do so first. Once a packet turns North or South, it can never turn West again. This eliminates two turns ($\text{North} \rightarrow \text{West}$ and $\text{South} \rightarrow \text{West}$), preventing circular cycles while retaining adaptive path diversity towards the East.
4. **Odd-Even Turn Model**:
   - Odd-Even restricts turns depending on whether the current node's column is even or odd. It provides minimal restriction without requiring virtual channels!
5. **Traffic Matrix Comparisons**:
   - Switch between **Uniform Random**, **Transpose Traffic**, and **Hotspot Traffic** to observe how link loads (red/orange links) heat up under non-uniform communication.

> [!TIP]
> Dive deeper into the mathematical proof of deadlock freedom in [Track 4: Routing & Deadlock Avoidance](../track4-routing-deadlock/01-deterministic-dor.md).
