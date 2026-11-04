# 🧩 Packet Master: The NoC Routing Puzzle

Step into the shoes of a Silicon Interconnect Architect. Program router turning rules, bypass faulty links, and resolve crossbar port contention to guide colored data flits to their target destination cores without collisions or deadlocks!

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Mission / Level:</b>
      <select id="levelSelect" class="noc-sim-select" onchange="loadPuzzleLevel(parseInt(this.value))">
        <option value="1">Level 1: Dimension-Order Highway (Warm-up)</option>
        <option value="2">Level 2: Dielectric Fault Detour (Broken Router)</option>
        <option value="3">Level 3: The Turn Model Maze (West-First Rule)</option>
        <option value="4">Level 4: Crossbar Contention Duel (Timing)</option>
        <option value="5">Level 5: Breaking the 4-Node Deadlock Trap</option>
      </select>
    </label>

    <button id="runPuzzleBtn" class="noc-sim-btn" onclick="runPuzzleSim()">▶ Execute Clock</button>
    <button id="resetPuzzleBtn" class="noc-sim-btn secondary" onclick="resetPuzzleSim()">🔄 Reset</button>
    <button id="stepPuzzleBtn" class="noc-sim-btn secondary" onclick="stepPuzzleCycle()">⏭ Single Step</button>
    <button id="puzzleSoundBtn" class="noc-sim-btn secondary" onclick="togglePuzzleSound()">🔊 Sound: ON</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-family:'JetBrains Mono', monospace; font-size:0.9rem; font-weight:700;">
      <span style="color:var(--tcl-blue-600);">Cycle: <span id="puzzleCycle">0</span> / <span id="targetCycles">15</span></span>
      <span style="color:#22c55e;">Delivered: <span id="puzzleDelivered">0</span> / <span id="puzzleTotalPackets">2</span></span>
      <span style="color:#f59e0b;" id="puzzleStars">⭐⭐⭐</span>
    </div>
  </div>

  <div id="levelBriefing" style="margin-bottom:0.75rem; padding:0.6rem 0.95rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; font-size:0.85rem; line-height:1.6;">
    <strong>Mission Objective:</strong> <span id="objectiveText">Deliver Packet 1 (Blue) to Core (3,0) and Packet 2 (Green) to Core (0,3).</span>
    <div style="font-size:0.8rem; color:#94a3b8; margin-top:2px;" id="ruleHint">💡 Click on intermediate routers to toggle turning preference (Default: XY DOR).</div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="puzzleCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Mission Success Modal -->
    <div id="puzzleSuccessModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.92); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;">🏆</div>
      <h2 style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#4ade80;">MISSION ACCOMPLISHED!</h2>
      <p id="puzzleSuccessSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:440px; margin-bottom:1.25rem;">
        All packets successfully routed with zero collisions and verified deadlock freedom!
      </p>
      <div id="starsAwarded" style="font-size:1.6rem; margin-bottom:1.25rem;">⭐⭐⭐</div>
      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="nextPuzzleLevel()" style="background:#22c55e;">▶ Next Mission</button>
        <button class="noc-sim-btn secondary" onclick="resetPuzzleSim()" style="color:#ffffff !important;">🔄 Replay Mission</button>
        <a href="../game/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">👾 Play Deadlock Buster</a>
      </div>
    </div>

    <!-- Mission Failure Modal -->
    <div id="puzzleFailureModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="failureModalIcon">💥</div>
      <h2 style="margin:0 0 0.5rem 0; font-size:1.6rem; color:#f87171;" id="failureModalTitle">ROUTING CONFLICT DETECTED</h2>
      <p id="puzzleFailureSummary" style="color:#cbd5e1; font-size:0.92rem; max-width:440px; margin-bottom:1.25rem; line-height:1.5;">
        Contention detected at router port.
      </p>
      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="retryPuzzleLevel()" style="background:#0284c7;">🔄 Adjust Routers &amp; Retry</button>
        <button class="noc-sim-btn secondary" onclick="resetPuzzleSim()" style="color:#ffffff !important;">♻️ Reset All</button>
      </div>
    </div>
  </div>

  <div style="margin-top:1rem; padding:0.85rem 1.15rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; font-size:0.85rem; color:var(--md-default-fg-color--lighter); line-height:1.6;">
    <strong>Interactive Architect Instructions:</strong>
    Click on any active router node to toggle its routing direction preference:
    <span style="display:inline-flex; gap:0.75rem; margin-left:0.5rem;">
      <code style="color:#38bdf8;">XY (Horizontal first)</code> ➔ 
      <code style="color:#fb923c;">YX (Vertical first)</code> ➔ 
      <code style="color:#a855f7;">TURN (Adaptive detour)</code>
    </span>.
    Avoid colliding two flits onto the same router port in the exact same cycle, and route around faulty red-hatched routers!
  </div>
</div>

<script>
// Web Audio Helper for Puzzle
const puzzleAudio = {
  ctx: null,
  enabled: true,
  init() {
    if (!this.ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (AC) this.ctx = new AC();
    }
  },
  playStep() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(440, now);
      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.05);
    } catch(e) {}
  },
  playWin() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, now + i * 0.1);
        gain.gain.setValueAtTime(0.12, now + i * 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.1 + 0.25);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now + i * 0.1);
        osc.stop(now + i * 0.1 + 0.25);
      });
    } catch(e) {}
  },
  playCollision() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(150, now);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.2);
    } catch(e) {}
  }
};

function togglePuzzleSound() {
  puzzleAudio.enabled = !puzzleAudio.enabled;
  if (puzzleAudio.enabled) puzzleAudio.init();
  const btn = document.getElementById("puzzleSoundBtn");
  if (btn) btn.textContent = puzzleAudio.enabled ? "🔊 Sound: ON" : "🔇 Sound: OFF";
}

const PUZZLE_LEVELS = [
  {
    id: 1,
    name: "Dimension-Order Highway",
    objective: "Route Blue flit to (3,0) and Green flit to (0,3). All routers operational.",
    hint: "Default XY routing naturally prevents collision as their paths are orthogonal.",
    maxCycles: 12,
    faults: [],
    packets: [
      { id: 1, src: { x: 0, y: 0 }, dst: { x: 3, y: 0 }, color: '#38bdf8', label: 'P1' },
      { id: 2, src: { x: 0, y: 0 }, dst: { x: 0, y: 3 }, color: '#4ade80', label: 'P2' }
    ]
  },
  {
    id: 2,
    name: "Dielectric Fault Detour",
    objective: "Core (1,1) suffered dielectric breakdown and is OFFLINE. Detour Packets around the dead node.",
    hint: "Click Router (0,1) to switch from XY to YX so Packet 1 bypasses the dead router (1,1) via column 0.",
    maxCycles: 15,
    faults: [{ x: 1, y: 1 }],
    packets: [
      { id: 1, src: { x: 0, y: 0 }, dst: { x: 2, y: 2 }, color: '#38bdf8', label: 'P1' },
      { id: 2, src: { x: 2, y: 0 }, dst: { x: 0, y: 2 }, color: '#fb923c', label: 'P2' }
    ]
  },
  {
    id: 3,
    name: "The Turn Model Maze",
    objective: "West-bound turns are restricted. Route Orange flit from (2,2) to (0,1) using valid West-First turns.",
    hint: "In West-First, packets MUST traverse West before any vertical turns to avoid deadlock cycles.",
    maxCycles: 16,
    faults: [{ x: 1, y: 2 }],
    packets: [
      { id: 1, src: { x: 2, y: 2 }, dst: { x: 0, y: 1 }, color: '#fb923c', label: 'P1' },
      { id: 2, src: { x: 1, y: 0 }, dst: { x: 3, y: 2 }, color: '#38bdf8', label: 'P2' }
    ]
  },
  {
    id: 4,
    name: "Crossbar Contention Duel",
    objective: "Both flits seek Core (2,2) and will collide at Router (1,2) at cycle 3! Divert one path.",
    hint: "Click Router (0,2) to configure a detour, staggering their arrival cycles.",
    maxCycles: 14,
    faults: [],
    packets: [
      { id: 1, src: { x: 1, y: 0 }, dst: { x: 2, y: 2 }, color: '#38bdf8', label: 'P1' },
      { id: 2, src: { x: 0, y: 2 }, dst: { x: 2, y: 2 }, color: '#ec4899', label: 'P2' }
    ]
  },
  {
    id: 5,
    name: "Breaking the 4-Node Deadlock Trap",
    objective: "4 packets are trapped in a potential circular dependency cycle (R5-R6-R10-R9). Deploy turn overrides to break the loop!",
    hint: "Change the routing rule on R6 or R9 to force an exit from the cycle before buffers saturate.",
    maxCycles: 18,
    faults: [{ x: 3, y: 1 }, { x: 0, y: 2 }],
    packets: [
      { id: 1, src: { x: 1, y: 1 }, dst: { x: 2, y: 2 }, color: '#38bdf8', label: 'P1' },
      { id: 2, src: { x: 2, y: 1 }, dst: { x: 1, y: 2 }, color: '#fb923c', label: 'P2' },
      { id: 3, src: { x: 2, y: 2 }, dst: { x: 1, y: 1 }, color: '#4ade80', label: 'P3' },
      { id: 4, src: { x: 1, y: 2 }, dst: { x: 2, y: 1 }, color: '#a855f7', label: 'P4' }
    ]
  }
];

class PuzzleGame {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.cols = 4;
    this.rows = 4;

    this.currentLevelIdx = 0;
    this.cycle = 0;
    this.isRunning = false;
    this.isCompleted = false;

    this.routerPreferences = {}; // "x,y" -> 'xy', 'yx', 'alt'
    this.activePackets = [];
    this.deliveredCount = 0;

    this.nodeRadius = 22;
    this.padding = 60;
    this.initCanvas();
    this.bindEvents();
    this.loadLevel(0);

    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
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

  bindEvents() {
    this.canvas.addEventListener('click', (e) => {
      if (this.isRunning) return;
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.width / rect.width;
      const scaleY = this.height / rect.height;
      const mx = (e.clientX - rect.left) * scaleX;
      const my = (e.clientY - rect.top) * scaleY;

      for (let r = 0; r < this.rows; r++) {
        for (let c = 0; c < this.cols; c++) {
          const { px, py } = this.getNodePos(c, r);
          if (Math.hypot(mx - px, my - py) <= this.nodeRadius + 6) {
            this.toggleRouterPreference(c, r);
            return;
          }
        }
      }
    });
  }

  toggleRouterPreference(x, y) {
    const level = PUZZLE_LEVELS[this.currentLevelIdx];
    const isFault = level.faults.some(f => f.x === x && f.y === y);
    if (isFault) return;

    const key = `${x},${y}`;
    const curr = this.routerPreferences[key] || 'xy';
    if (curr === 'xy') this.routerPreferences[key] = 'yx';
    else if (curr === 'yx') this.routerPreferences[key] = 'alt';
    else this.routerPreferences[key] = 'xy';
    puzzleAudio.playStep();
    this.draw();
  }

  loadLevel(idx) {
    this.currentLevelIdx = idx;
    const lvl = PUZZLE_LEVELS[idx];
    this.cycle = 0;
    this.isRunning = false;
    this.isCompleted = false;
    this.deliveredCount = 0;
    this.routerPreferences = {};

    document.getElementById("levelSelect").value = lvl.id;
    document.getElementById("objectiveText").textContent = lvl.objective;
    document.getElementById("ruleHint").textContent = `💡 ${lvl.hint}`;
    document.getElementById("targetCycles").textContent = lvl.maxCycles;
    document.getElementById("puzzleCycle").textContent = "0";
    document.getElementById("puzzleDelivered").textContent = `0 / ${lvl.packets.length}`;
    document.getElementById("puzzleTotalPackets").textContent = lvl.packets.length;
    document.getElementById("puzzleStars").textContent = "⭐⭐⭐";
    document.getElementById("puzzleSuccessModal").style.display = "none";
    document.getElementById("runPuzzleBtn").textContent = "▶ Execute Clock";

    this.activePackets = lvl.packets.map(p => ({
      ...p,
      curr: { ...p.src },
      next: null,
      progress: 0,
      done: false
    }));

    this.draw();
  }

  getNodePos(x, y) {
    return {
      px: this.padding + x * this.stepX,
      py: this.padding + y * this.stepY
    };
  }

  computeNext(curr, dst, pref) {
    if (curr.x === dst.x && curr.y === dst.y) return null;
    const lvl = PUZZLE_LEVELS[this.currentLevelIdx];
    const isFault = (x, y) => lvl.faults.some(f => f.x === x && f.y === y);

    const tryStep = (dir) => {
      let nx = curr.x, ny = curr.y;
      if (dir === 'E') nx++;
      if (dir === 'W') nx--;
      if (dir === 'S') ny++;
      if (dir === 'N') ny--;
      if (nx >= 0 && nx < this.cols && ny >= 0 && ny < this.rows && !isFault(nx, ny)) {
        return { x: nx, y: ny };
      }
      return null;
    };

    if (pref === 'yx') {
      // Vertical first
      if (curr.y < dst.y && tryStep('S')) return tryStep('S');
      if (curr.y > dst.y && tryStep('N')) return tryStep('N');
      if (curr.x < dst.x && tryStep('E')) return tryStep('E');
      if (curr.x > dst.x && tryStep('W')) return tryStep('W');
    } else if (pref === 'alt') {
      // Adaptive alternate
      const cand = [];
      if (curr.x < dst.x && tryStep('E')) cand.push(tryStep('E'));
      if (curr.x > dst.x && tryStep('W')) cand.push(tryStep('W'));
      if (curr.y < dst.y && tryStep('S')) cand.push(tryStep('S'));
      if (curr.y > dst.y && tryStep('N')) cand.push(tryStep('N'));
      if (cand.length > 0) return cand[cand.length - 1];
    } else {
      // Strict XY (Horizontal first)
      if (curr.x < dst.x && tryStep('E')) return tryStep('E');
      if (curr.x > dst.x && tryStep('W')) return tryStep('W');
      if (curr.y < dst.y && tryStep('S')) return tryStep('S');
      if (curr.y > dst.y && tryStep('N')) return tryStep('N');
    }

    // Fallback obstacle detours
    const allDirs = ['E', 'S', 'W', 'N'];
    for (const d of allDirs) {
      const step = tryStep(d);
      if (step) return step;
    }
    return null;
  }

  step() {
    this.cycle++;
    document.getElementById("puzzleCycle").textContent = this.cycle;
    puzzleAudio.playStep();

    // Check collision on destination router
    const occupied = {};

    for (let i = 0; i < this.activePackets.length; i++) {
      const p = this.activePackets[i];
      if (p.done) continue;

      const pref = this.routerPreferences[`${p.curr.x},${p.curr.y}`] || 'xy';
      p.next = this.computeNext(p.curr, p.dst, pref);

      if (p.next) {
        const key = `${p.next.x},${p.next.y}`;
        if (occupied[key]) {
          // Crossbar Collision!
          puzzleAudio.playCollision();
          this.isRunning = false;
          alert(`💥 Collision detected at Router (${p.next.x},${p.next.y}) in Cycle ${this.cycle}! Reconfigure router preferences to stagger their arrival.`);
          this.reset();
          return;
        }
        occupied[key] = p.id;
      }
    }

    // Advance packets
    for (const p of this.activePackets) {
      if (p.done || !p.next) continue;
      p.curr = { ...p.next };
      p.next = null;

      if (p.curr.x === p.dst.x && p.curr.y === p.dst.y) {
        p.done = true;
        this.deliveredCount++;
        document.getElementById("puzzleDelivered").textContent = `${this.deliveredCount} / ${this.activePackets.length}`;
      }
    }

    // Victory condition check
    if (this.deliveredCount === this.activePackets.length) {
      this.isRunning = false;
      this.isCompleted = true;
      puzzleAudio.playWin();

      const lvl = PUZZLE_LEVELS[this.currentLevelIdx];
      let stars = "⭐⭐⭐";
      if (this.cycle > lvl.maxCycles) stars = "⭐";
      else if (this.cycle > lvl.maxCycles - 3) stars = "⭐⭐";

      document.getElementById("puzzleStars").textContent = stars;
      document.getElementById("starsAwarded").textContent = stars;
      document.getElementById("puzzleSuccessSummary").innerHTML = 
        `All packets delivered in <strong>${this.cycle} cycles</strong> (Par: ${lvl.maxCycles} cyc). Rating: <strong>${stars}</strong>!`;
      document.getElementById("puzzleSuccessModal").style.display = "flex";
    }
  }

  reset() {
    this.loadLevel(this.currentLevelIdx);
  }

  draw() {
    this.ctx.clearRect(0, 0, this.width, this.height);
    const lvl = PUZZLE_LEVELS[this.currentLevelIdx];

    // Draw Links
    this.ctx.lineWidth = 2.5;
    this.ctx.strokeStyle = '#334155';
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const { px, py } = this.getNodePos(c, r);
        if (c < this.cols - 1) {
          const next = this.getNodePos(c + 1, r);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
        }
        if (r < this.rows - 1) {
          const next = this.getNodePos(c, r + 1);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
        }
      }
    }

    // Draw Routers
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const { px, py } = this.getNodePos(c, r);
        const isFault = lvl.faults.some(f => f.x === c && f.y === r);
        const pref = this.routerPreferences[`${c},${r}`] || 'xy';

        this.ctx.beginPath();
        this.ctx.arc(px, py, this.nodeRadius, 0, Math.PI * 2);

        if (isFault) {
          this.ctx.fillStyle = '#450a0a';
          this.ctx.fill();
          this.ctx.lineWidth = 2.5;
          this.ctx.strokeStyle = '#ef4444';
          this.ctx.stroke();

          // Hatching for broken core
          this.ctx.fillStyle = '#f87171';
          this.ctx.font = 'bold 12px sans-serif';
          this.ctx.textAlign = 'center';
          this.ctx.textBaseline = 'middle';
          this.ctx.fillText('⚡X', px, py);
          continue;
        }

        // Active router
        this.ctx.fillStyle = '#0f172a';
        this.ctx.fill();

        this.ctx.lineWidth = pref !== 'xy' ? 2.5 : 1.5;
        this.ctx.strokeStyle = pref === 'yx' ? '#fb923c' : (pref === 'alt' ? '#c084fc' : '#38bdf8');
        this.ctx.stroke();

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = 'bold 10px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(`R(${c},${r})`, px, py - 3);

        this.ctx.font = '8px monospace';
        this.ctx.fillStyle = pref === 'yx' ? '#fb923c' : (pref === 'alt' ? '#c084fc' : '#94a3b8');
        this.ctx.fillText(pref.toUpperCase(), px, py + 8);
      }
    }

    // Draw Packet Destinations & Start Bases
    for (const p of this.activePackets) {
      const dstPos = this.getNodePos(p.dst.x, p.dst.y);
      this.ctx.lineWidth = 2.5;
      this.ctx.strokeStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(dstPos.px, dstPos.py, this.nodeRadius + 4, 0, Math.PI * 2);
      this.ctx.stroke();

      // Destination Tag
      this.ctx.fillStyle = p.color;
      this.ctx.font = 'bold 9px sans-serif';
      this.ctx.fillText(`DST:${p.label}`, dstPos.px, dstPos.py - this.nodeRadius - 8);
    }

    // Draw In-Flight Flits
    for (const p of this.activePackets) {
      if (p.done) continue;
      const pos = this.getNodePos(p.curr.x, p.curr.y);

      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(pos.px, pos.py, 10, 0, Math.PI * 2);
      this.ctx.fill();

      this.ctx.lineWidth = 1.5;
      this.ctx.strokeStyle = '#ffffff';
      this.ctx.stroke();

      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 9px sans-serif';
      this.ctx.fillText(p.label, pos.px, pos.py);
    }
  }

  animate() {
    this.draw();
    requestAnimationFrame(this.animate);
  }
}

let puzzleGame = null;

function initPuzzleGame() {
  if (document.getElementById('puzzleCanvas') && !puzzleGame) {
    puzzleGame = new PuzzleGame('puzzleCanvas');
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPuzzleGame);
} else {
  initPuzzleGame();
}

function loadPuzzleLevel(lvlId) {
  if (puzzleGame) puzzleGame.loadLevel(lvlId - 1);
}

function runPuzzleSim() {
  if (!puzzleGame) return;
  puzzleAudio.init();
  if (puzzleGame.isCompleted) {
    puzzleGame.reset();
  }
  puzzleGame.isRunning = true;
  document.getElementById("runPuzzleBtn").textContent = "⏸ Running...";
  
  const stepInterval = setInterval(() => {
    if (!puzzleGame.isRunning || puzzleGame.isCompleted) {
      clearInterval(stepInterval);
      document.getElementById("runPuzzleBtn").textContent = "▶ Execute Clock";
      return;
    }
    puzzleGame.step();
  }, 450);
}

function stepPuzzleCycle() {
  if (!puzzleGame) return;
  puzzleAudio.init();
  puzzleGame.step();
}

function resetPuzzleSim() {
  if (puzzleGame) puzzleGame.reset();
}

function nextPuzzleLevel() {
  if (!puzzleGame) return;
  const nextIdx = (puzzleGame.currentLevelIdx + 1) % PUZZLE_LEVELS.length;
  puzzleGame.loadLevel(nextIdx);
}
</script>
