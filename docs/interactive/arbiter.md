# ⚡ Arbiter Arena: The 5-Port Crossbar Clash

Step inside the router microarchitecture as the **Switch Allocator & Crossbar Arbiter**! Packets and flits flood into the router's 5 physical input ports: **North (N)**, **South (S)**, **East (E)**, **West (W)**, and **Local (L)**. As flits queue up in Virtual Channels, configure conflict-free crossbar matchings in real-time, bypass Head-of-Line (HOL) blocking flits, and prevent buffer FIFO overflow before time expires! High scores can be directly inscribed on the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="arbiterStartBtn" class="noc-sim-btn" onclick="startArbiterGame()">▶ Start Clash</button>
    <button id="stepClockBtn" class="noc-sim-btn" onclick="fireArbiterClock()" style="background:#ea580c; border:none; box-shadow:0 0 12px rgba(234,88,12,0.4);">⚡ Clock Cycle (Space)</button>

    <label><b>Arbiter Policy:</b>
      <select id="arbiterPolicySelect" class="noc-sim-select" onchange="setArbiterPolicy(this.value)">
        <option value="islip">iSLIP (Iterative Round-Robin / High Throughput)</option>
        <option value="round-robin">Strict Round-Robin (Fixed Priority Rotation)</option>
        <option value="longest-queue">Longest Queue First (Anti-Overflow Priority)</option>
        <option value="manual">Manual Crosspoint Matcher (Arcade Puzzle)</option>
      </select>
    </label>

    <label><b>Clock Speed:</b>
      <select id="clockSpeedSelect" class="noc-sim-select" onchange="setArbiterClockSpeed(this.value)">
        <option value="auto_1">Auto Clock (1.0 Hz)</option>
        <option value="auto_2">Auto Clock (2.0 Hz Fast)</option>
        <option value="manual_only">Manual Spacebar Only</option>
      </select>
    </label>

    <button id="arbiterSoundBtn" class="noc-sim-btn secondary" onclick="toggleArbiterSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleArbiterPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="arbiterScore">0</span></span>
      <span style="color:#22c55e;">Delivered: <span id="arbiterDelivered">0</span></span>
      <span style="color:#ef4444;">Queued: <span id="arbiterTotalQueued">0</span>/40</span>
      <span style="color:#f59e0b;" id="arbiterWaveBadge">Wave 1</span>
    </div>
  </div>

  <!-- Arbiter Metrics HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">⚡ Crossbar Utilization Efficiency:</span>
        <span id="xbarUtilText" style="font-weight:700; color:#38bdf8;">0%</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="xbarUtilBar" style="width:0%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#f87171;">⚠️ Input Buffer Safety Margin:</span>
        <span id="bufferSafetyText" style="font-weight:700; color:#4ade80;">100% (No Stalls)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(239,68,68,0.15); border-radius:4px; overflow:hidden;">
        <div id="bufferSafetyBar" style="width:100%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="arbiterCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="arbiterOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="arbiterModalIcon">💥</div>
      <h2 id="arbiterModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">INPUT BUFFER OVERFLOW!</h2>
      <p id="arbiterModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Input Virtual Channel queues saturated past maximum capacity. Backpressure credit starvation halted upstream routers!
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Arbiter Callsign / Name:</label>
        <input type="text" id="arbiterCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Matrix Master" value="Arbiter Prime">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="arbiterOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Stanford VLSI / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveArbiterRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitArbiterToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartArbiterGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="arbiterSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in your browser Leaderboard!
      </div>
    </div>
  </div>

  <div id="arbiterInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">⚡ Router Switch Microarchitecture &amp; Crossbar Theory:</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>5×5 Crossbar Allocation:</strong> In canonical wormhole routers, flits arriving at 5 input ports (North, South, East, West, Local) compete for 5 output directions. A valid crossbar schedule requires a <em>bipartite maximal matching</em> (no two inputs drive the same output; no input drives two outputs in the same cycle).</li>
      <li><strong>Head-of-Line (HOL) Blocking:</strong> When a flit at the head of a queue requests an output that is contested or busy, all subsequent flits behind it are blocked, even if their own destinations are completely idle!</li>
      <li><strong>Virtual Channel Bypass (Click Queue):</strong> Click on any input port to toggle between <strong>VC0</strong> and <strong>VC1</strong>. Switching VCs bypasses a blocked head flit and unlocks idle crossbar ports!</li>
      <li><strong>Arbitration Algorithms:</strong>
        <ul>
          <li><strong>iSLIP:</strong> Iterative Round-Robin with decoupled request, grant, and accept phases. Prevents starvation and desynchronizes arbiter pointers.</li>
          <li><strong>Longest Queue First (LQF):</strong> Prioritizes buffers nearing saturation ($> 3$ flits) to prevent buffer overflows.</li>
          <li><strong>Manual Matching:</strong> Click on crossbar crosspoint matrix cells to manually route connections.</li>
        </ul>
      </li>
      <li><strong>Controls:</strong> <code>Space</code> = Fire Clock Cycle | <code>1</code>–<code>5</code> = Select Input Port | <code>Tab</code> = Toggle VC | <code>P</code> = Pause.</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Arbiter Arena
class ArbiterAudio {
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

  playClock() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'square';
      osc.frequency.setValueAtTime(800, now);
      osc.frequency.exponentialRampToValueAtTime(200, now + 0.04);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.05);
    } catch(e) {}
  }

  playMatch() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(523.25, now); // C5
      osc.frequency.exponentialRampToValueAtTime(1046.5, now + 0.09); // C6
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.12);
    } catch(e) {}
  }

  playBypass() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.linearRampToValueAtTime(640, now + 0.08);
      gain.gain.setValueAtTime(0.1, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.1);
    } catch(e) {}
  }

  playWarning() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(240, now);
      osc.frequency.linearRampToValueAtTime(180, now + 0.15);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.18);
    } catch(e) {}
  }

  playGameOver() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(150, now);
      osc.frequency.exponentialRampToValueAtTime(35, now + 0.6);
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.65);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.65);
    } catch(e) {}
  }
}

const PORTS = ['North', 'South', 'East', 'West', 'Local'];
const PORT_COLORS = {
  North: '#38bdf8',
  South: '#22c55e',
  East: '#f59e0b',
  West: '#c084fc',
  Local: '#f43f5e'
};

class ArbiterGame {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.audio = new ArbiterAudio();

    // 5 Input Ports, each with 2 VCs (VC0, VC1). Queue capacity = 4 flits per VC.
    this.inputs = [];
    this.activeVc = [0, 0, 0, 0, 0]; // Selected active VC per input port (0 or 1)
    this.currentMatches = []; // array of {inIdx, outIdx}
    this.particles = [];

    this.policy = 'islip';
    this.clockSpeedMode = 'auto_1';
    this.clockAccumulator = 0.0;
    this.clockPeriod = 1.0; // 1 second per cycle in auto_1

    this.state = 'idle'; // 'idle', 'running', 'paused', 'over'
    this.score = 0;
    this.cycle = 0;
    this.deliveredCount = 0;
    this.wave = 1;
    this.waveTimer = 25.0;
    this.utilizationHistory = [];

    this.lastTime = performance.now();
    this.initQueues();
    this.bindEvents();
    this.loop = this.loop.bind(this);
    requestAnimationFrame(this.loop);
  }

  initQueues() {
    this.inputs = [];
    for (let i = 0; i < 5; i++) {
      this.inputs.push({
        name: PORTS[i],
        vc0: [], // array of {dest: string, id: number}
        vc1: [],
        stalled: false
      });
    }
    this.activeVc = [0, 0, 0, 0, 0];
    this.currentMatches = [];
    this.particles = [];
  }

  bindEvents() {
    this.canvas.addEventListener('click', (e) => {
      this.audio.init();
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.canvas.width / rect.width;
      const scaleY = this.canvas.height / rect.height;
      const mx = (e.clientX - rect.left) * scaleX;
      const my = (e.clientY - rect.top) * scaleY;

      if (this.state !== 'running') return;

      // 1. Check click on Input Port / VC Toggle
      for (let i = 0; i < 5; i++) {
        const inBox = this.getInputBox(i);
        if (mx >= inBox.x && mx <= inBox.x + inBox.w && my >= inBox.y && my <= inBox.y + inBox.h) {
          // Toggle active VC
          this.activeVc[i] = 1 - this.activeVc[i];
          this.audio.playBypass();
          this.addTextParticle(inBox.x + inBox.w / 2, inBox.y + inBox.h / 2, `VC${this.activeVc[i]} ACTIVE`, '#38bdf8');
          this.solveMatching();
          return;
        }
      }

      // 2. Check click on Crosspoint Grid in Manual Mode
      if (this.policy === 'manual') {
        const grid = this.getGridDimensions();
        if (mx >= grid.x && mx <= grid.x + grid.w && my >= grid.y && my <= grid.y + grid.h) {
          const colW = grid.w / 5;
          const rowH = grid.h / 5;
          const outIdx = Math.floor((mx - grid.x) / colW);
          const inIdx = Math.floor((my - grid.y) / rowH);
          if (inIdx >= 0 && inIdx < 5 && outIdx >= 0 && outIdx < 5) {
            this.toggleManualMatch(inIdx, outIdx);
          }
        }
      }
    });

    window.addEventListener('keydown', (e) => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
      if (e.code === 'Space') {
        e.preventDefault();
        this.audio.init();
        this.stepCycle();
      } else if (e.key === 'p' || e.key === 'P') {
        this.togglePause();
      } else if (e.key >= '1' && e.key <= '5') {
        const inIdx = parseInt(e.key) - 1;
        this.activeVc[inIdx] = 1 - this.activeVc[inIdx];
        this.audio.playBypass();
        this.solveMatching();
      }
    });
  }

  getInputBox(i) {
    const padY = 55;
    const rowH = 68;
    return {
      x: 20,
      y: padY + i * rowH,
      w: 160,
      h: rowH - 8
    };
  }

  getOutputBox(i) {
    const padY = 55;
    const rowH = 68;
    return {
      x: 460,
      y: padY + i * rowH,
      w: 140,
      h: rowH - 8
    };
  }

  getGridDimensions() {
    return {
      x: 205,
      y: 75,
      w: 230,
      h: 290
    };
  }

  start() {
    this.audio.init();
    this.initQueues();
    this.state = 'running';
    this.score = 0;
    this.cycle = 0;
    this.deliveredCount = 0;
    this.wave = 1;
    this.waveTimer = 25.0;
    this.utilizationHistory = [];

    // Seed initial flits
    for (let i = 0; i < 5; i++) {
      this.injectFlit(i, 0);
      if (Math.random() > 0.4) this.injectFlit(i, 1);
    }
    this.solveMatching();

    document.getElementById('arbiterOverModal').style.display = 'none';
    document.getElementById('arbiterStartBtn').textContent = '🔄 Restart';
    this.updateHUD();
  }

  togglePause() {
    if (this.state === 'running') this.state = 'paused';
    else if (this.state === 'paused') this.state = 'running';
  }

  injectFlit(inIdx, vcIdx) {
    const inPort = this.inputs[inIdx];
    const q = vcIdx === 0 ? inPort.vc0 : inPort.vc1;
    if (q.length >= 4) return false;

    // Pick a destination different from origin or based on wave
    let validDests = PORTS.filter((_, idx) => idx !== inIdx);
    if (this.wave === 2) {
      // Hotspot on Local port
      validDests.push('Local', 'Local');
    }
    const dest = validDests[Math.floor(Math.random() * validDests.length)];
    q.push({
      dest: dest,
      id: Math.floor(Math.random() * 9000 + 1000)
    });
    return true;
  }

  toggleManualMatch(inIdx, outIdx) {
    const existingIdx = this.currentMatches.findIndex(m => m.inIdx === inIdx && m.outIdx === outIdx);
    if (existingIdx >= 0) {
      this.currentMatches.splice(existingIdx, 1);
    } else {
      // Remove any conflicting match on same inIdx or outIdx
      this.currentMatches = this.currentMatches.filter(m => m.inIdx !== inIdx && m.outIdx !== outIdx);
      this.currentMatches.push({ inIdx, outIdx });
      this.audio.playMatch();
    }
  }

  solveMatching() {
    if (this.policy === 'manual') return;

    this.currentMatches = [];
    const inRequests = [];

    for (let inIdx = 0; inIdx < 5; inIdx++) {
      const vcIdx = this.activeVc[inIdx];
      const q = vcIdx === 0 ? this.inputs[inIdx].vc0 : this.inputs[inIdx].vc1;
      if (q.length > 0) {
        const head = q[0];
        const outIdx = PORTS.indexOf(head.dest);
        inRequests.push({ inIdx, outIdx, qLen: q.length });
      }
    }

    if (this.policy === 'longest-queue') {
      // Sort requests by queue length descending
      inRequests.sort((a, b) => b.qLen - a.qLen);
    } else if (this.policy === 'round-robin') {
      // Rotate priority based on cycle
      const offset = this.cycle % 5;
      inRequests.sort((a, b) => ((a.inIdx - offset + 5) % 5) - ((b.inIdx - offset + 5) % 5));
    }

    // Allocate conflict-free matches
    const claimedOutputs = new Set();
    const claimedInputs = new Set();

    inRequests.forEach(req => {
      if (!claimedInputs.has(req.inIdx) && !claimedOutputs.has(req.outIdx)) {
        this.currentMatches.push({ inIdx: req.inIdx, outIdx: req.outIdx });
        claimedInputs.add(req.inIdx);
        claimedOutputs.add(req.outIdx);
      }
    });
  }

  stepCycle() {
    if (this.state !== 'running') return;
    this.cycle++;
    this.audio.playClock();

    // 1. Deliver matched flits through Crossbar
    let matchedCount = 0;
    this.currentMatches.forEach(m => {
      const inPort = this.inputs[m.inIdx];
      const vcIdx = this.activeVc[m.inIdx];
      const q = vcIdx === 0 ? inPort.vc0 : inPort.vc1;

      if (q.length > 0) {
        const flit = q.shift();
        matchedCount++;
        this.deliveredCount++;
        this.score += 25 * this.wave;

        // Visual beam / laser particle
        const inBox = this.getInputBox(m.inIdx);
        const outBox = this.getOutputBox(m.outIdx);
        this.addLaserParticle(inBox.x + inBox.w, inBox.y + inBox.h / 2, outBox.x, outBox.y + outBox.h / 2, PORT_COLORS[flit.dest]);
      }
    });

    if (matchedCount > 0) {
      this.audio.playMatch();
    }

    // Record crossbar utilization (matched / 5)
    const util = (matchedCount / 5.0) * 100.0;
    this.utilizationHistory.push(util);
    if (this.utilizationHistory.length > 20) this.utilizationHistory.shift();

    // 2. Inject incoming flits
    const burstChance = 0.55 + this.wave * 0.08;
    for (let i = 0; i < 5; i++) {
      if (Math.random() < burstChance) {
        const targetVc = Math.random() > 0.5 ? 0 : 1;
        this.injectFlit(i, targetVc);
      }
    }

    // 3. Check for Buffer Overflow & Meltdown
    let totalQueued = 0;
    let overflowOccurred = false;
    for (let i = 0; i < 5; i++) {
      const q0 = this.inputs[i].vc0.length;
      const q1 = this.inputs[i].vc1.length;
      totalQueued += (q0 + q1);
      if (q0 >= 4 && q1 >= 4) {
        overflowOccurred = true;
      }
    }

    if (overflowOccurred) {
      this.audio.playWarning();
      // If full capacity hit
      if (totalQueued >= 36) {
        this.triggerOverflow();
        return;
      }
    }

    // 4. Update Matching for next cycle
    this.solveMatching();
    this.updateHUD();
  }

  triggerOverflow() {
    this.state = 'over';
    this.audio.playGameOver();
    document.getElementById('arbiterModalTitle').textContent = 'INPUT BUFFER OVERFLOW!';
    document.getElementById('arbiterModalSummary').innerHTML = `
      Input Virtual Channel queues saturated to maximum capacity (40 flits)!<br>
      Severe Head-of-Line blocking created upstream credit starvation across neighboring tiles.
      <br><br><b>Final Wave:</b> Wave ${this.wave} | <b>Total Delivered:</b> ${this.deliveredCount} flits | <b>Score:</b> ${this.score} pts
    `;
    document.getElementById('arbiterOverModal').style.display = 'flex';
  }

  addTextParticle(x, y, text, color) {
    this.particles.push({
      x, y, vx: 0, vy: -0.8, life: 1.0, text, color, isText: true
    });
  }

  addLaserParticle(x1, y1, x2, y2, color) {
    this.particles.push({
      x1, y1, x2, y2, life: 1.0, color, isLaser: true
    });
  }

  update(dt) {
    if (this.state !== 'running') return;

    // Progress Wave
    this.waveTimer -= dt;
    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 25.0;
      this.score += 250 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 40, `WAVE ${this.wave} ESCALATION!`, '#22c55e');
    }

    // Auto clock timer
    if (this.clockSpeedMode !== 'manual_only') {
      this.clockAccumulator += dt;
      if (this.clockAccumulator >= this.clockPeriod) {
        this.clockAccumulator = 0.0;
        this.stepCycle();
      }
    }

    // Update Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const pt = this.particles[i];
      pt.life -= dt * (pt.isLaser ? 3.0 : 1.2);
      if (pt.isText) pt.y += pt.vy;
      if (pt.life <= 0) this.particles.splice(i, 1);
    }
  }

  updateHUD() {
    document.getElementById('arbiterScore').textContent = this.score;
    document.getElementById('arbiterDelivered').textContent = this.deliveredCount;
    document.getElementById('arbiterWaveBadge').textContent = `Wave ${this.wave}`;

    let totalQueued = 0;
    this.inputs.forEach(inp => totalQueued += (inp.vc0.length + inp.vc1.length));
    document.getElementById('arbiterTotalQueued').textContent = totalQueued;

    // Crossbar Util
    const avgUtil = this.utilizationHistory.length > 0 ? (this.utilizationHistory.reduce((a, b) => a + b, 0) / this.utilizationHistory.length) : 0;
    document.getElementById('xbarUtilBar').style.width = `${Math.round(avgUtil)}%`;
    document.getElementById('xbarUtilText').textContent = `${Math.round(avgUtil)}%`;

    // Buffer Safety
    const safety = Math.max(0, Math.min(100, 100 - (totalQueued / 40.0) * 100));
    const safetyBar = document.getElementById('bufferSafetyBar');
    safetyBar.style.width = `${Math.round(safety)}%`;
    if (safety < 30) {
      safetyBar.style.background = '#ef4444';
      document.getElementById('bufferSafetyText').style.color = '#ef4444';
      document.getElementById('bufferSafetyText').textContent = `${Math.round(safety)}% (NEAR OVERFLOW!)`;
    } else if (safety < 60) {
      safetyBar.style.background = '#f59e0b';
      document.getElementById('bufferSafetyText').style.color = '#f59e0b';
      document.getElementById('bufferSafetyText').textContent = `${Math.round(safety)}% (HIGH LOAD)`;
    } else {
      safetyBar.style.background = '#22c55e';
      document.getElementById('bufferSafetyText').style.color = '#4ade80';
      document.getElementById('bufferSafetyText').textContent = `${Math.round(safety)}% (HEALTHY)`;
    }
  }

  draw() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 1. Draw 5 Input Port FIFOs
    for (let i = 0; i < 5; i++) {
      const box = this.getInputBox(i);
      const inPort = this.inputs[i];
      const active = this.activeVc[i];

      this.ctx.fillStyle = '#1e293b';
      this.ctx.beginPath();
      this.ctx.roundRect(box.x, box.y, box.w, box.h, 6);
      this.ctx.fill();

      this.ctx.strokeStyle = '#334155';
      this.ctx.lineWidth = 1.5;
      this.ctx.stroke();

      // Port Name & Active VC Tag
      this.ctx.fillStyle = '#f8fafc';
      this.ctx.font = 'bold 11px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'left';
      this.ctx.fillText(`IN: ${inPort.name}`, box.x + 8, box.y + 16);

      this.ctx.fillStyle = active === 0 ? '#38bdf8' : '#c084fc';
      this.ctx.font = 'bold 10px "Inter", sans-serif';
      this.ctx.fillText(`VC${active} (Click to Swap)`, box.x + 8, box.y + 30);

      // Draw Flit Slots in Active VC
      const q = active === 0 ? inPort.vc0 : inPort.vc1;
      const slotW = 20;
      const slotH = 18;
      for (let s = 0; s < 4; s++) {
        const sx = box.x + 60 + s * (slotW + 3);
        const sy = box.y + 36;
        if (s < q.length) {
          const flit = q[s];
          this.ctx.fillStyle = PORT_COLORS[flit.dest];
          this.ctx.beginPath();
          this.ctx.roundRect(sx, sy, slotW, slotH, 4);
          this.ctx.fill();
          this.ctx.fillStyle = '#ffffff';
          this.ctx.font = 'bold 9px "JetBrains Mono", monospace';
          this.ctx.textAlign = 'center';
          this.ctx.fillText(flit.dest.charAt(0), sx + slotW / 2, sy + 13);
        } else {
          this.ctx.strokeStyle = '#334155';
          this.ctx.strokeRect(sx, sy, slotW, slotH);
        }
      }
    }

    // 2. Draw 5×5 Crossbar Grid in Center
    const grid = this.getGridDimensions();
    this.ctx.fillStyle = 'rgba(30, 41, 59, 0.7)';
    this.ctx.beginPath();
    this.ctx.roundRect(grid.x, grid.y, grid.w, grid.h, 8);
    this.ctx.fill();
    this.ctx.strokeStyle = '#475569';
    this.ctx.stroke();

    // Grid Column & Row Labels
    const colW = grid.w / 5;
    const rowH = grid.h / 5;
    this.ctx.fillStyle = '#94a3b8';
    this.ctx.font = '10px "JetBrains Mono", monospace';
    this.ctx.textAlign = 'center';
    for (let c = 0; c < 5; c++) {
      this.ctx.fillText(PORTS[c].charAt(0), grid.x + c * colW + colW / 2, grid.y - 6);
    }
    this.ctx.textAlign = 'right';
    for (let r = 0; r < 5; r++) {
      this.ctx.fillText(PORTS[r].charAt(0), grid.x - 6, grid.y + r * rowH + rowH / 2 + 3);
    }

    // Draw Crossbar Crosspoints
    for (let r = 0; r < 5; r++) {
      for (let c = 0; c < 5; c++) {
        const cx = grid.x + c * colW + colW / 2;
        const cy = grid.y + r * rowH + rowH / 2;
        const isMatched = this.currentMatches.some(m => m.inIdx === r && m.outIdx === c);

        // Crosspoint dot
        this.ctx.fillStyle = isMatched ? '#22c55e' : '#334155';
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, isMatched ? 6.5 : 3.5, 0, Math.PI * 2);
        this.ctx.fill();

        if (isMatched) {
          this.ctx.shadowColor = '#22c55e';
          this.ctx.shadowBlur = 10;
          this.ctx.strokeStyle = '#4ade80';
          this.ctx.stroke();
          this.ctx.shadowBlur = 0;
        }
      }
    }

    // 3. Draw 5 Output Ports
    for (let j = 0; j < 5; j++) {
      const box = this.getOutputBox(j);
      const isDriven = this.currentMatches.some(m => m.outIdx === j);

      this.ctx.fillStyle = isDriven ? 'rgba(34, 197, 94, 0.15)' : '#1e293b';
      this.ctx.beginPath();
      this.ctx.roundRect(box.x, box.y, box.w, box.h, 6);
      this.ctx.fill();

      this.ctx.strokeStyle = isDriven ? '#22c55e' : '#334155';
      this.ctx.lineWidth = isDriven ? 2 : 1.5;
      this.ctx.stroke();

      this.ctx.fillStyle = PORT_COLORS[PORTS[j]];
      this.ctx.font = 'bold 12px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'left';
      this.ctx.fillText(`OUT: ${PORTS[j]}`, box.x + 12, box.y + 26);

      this.ctx.fillStyle = isDriven ? '#4ade80' : '#64748b';
      this.ctx.font = '10px "Inter", sans-serif';
      this.ctx.fillText(isDriven ? '● TRANSMITTING' : '○ IDLE', box.x + 12, box.y + 44);
    }

    // 4. Draw Animated Laser Particles across Crossbar
    this.particles.forEach(pt => {
      this.ctx.globalAlpha = Math.max(0, pt.life);
      if (pt.isLaser) {
        this.ctx.strokeStyle = pt.color;
        this.ctx.lineWidth = 3;
        this.ctx.shadowColor = pt.color;
        this.ctx.shadowBlur = 12;
        this.ctx.beginPath();
        this.ctx.moveTo(pt.x1, pt.y1);
        this.ctx.lineTo(pt.x2, pt.y2);
        this.ctx.stroke();
        this.ctx.shadowBlur = 0;
      } else if (pt.isText) {
        this.ctx.fillStyle = pt.color;
        this.ctx.font = 'bold 12px "JetBrains Mono", monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(pt.text, pt.x, pt.y);
      }
      this.ctx.globalAlpha = 1.0;
    });

    // Idle Watermark
    if (this.state === 'idle') {
      this.ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 20px "Inter", sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.fillText('Press "Start Clash" to Play!', this.canvas.width / 2, this.canvas.height / 2 - 10);
      this.ctx.font = '13px "Inter", sans-serif';
      this.ctx.fillStyle = '#94a3b8';
      this.ctx.fillText('Arbitrate 5x5 crossbar matchings & prevent buffer overflow', this.canvas.width / 2, this.canvas.height / 2 + 18);
    }
  }

  loop(timestamp) {
    const dt = Math.min(0.08, (timestamp - this.lastTime) / 1000.0);
    this.lastTime = timestamp;

    this.update(dt);
    this.draw();
    requestAnimationFrame(this.loop);
  }
}

let arbiterGame = null;
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('arbiterCanvas')) {
    arbiterGame = new ArbiterGame('arbiterCanvas');
  }
});

function startArbiterGame() {
  if (arbiterGame) arbiterGame.start();
}

function restartArbiterGame() {
  if (arbiterGame) arbiterGame.start();
}

function fireArbiterClock() {
  if (arbiterGame) arbiterGame.stepCycle();
}

function setArbiterPolicy(pol) {
  if (arbiterGame) {
    arbiterGame.policy = pol;
    arbiterGame.solveMatching();
  }
}

function setArbiterClockSpeed(speed) {
  if (arbiterGame) {
    arbiterGame.clockSpeedMode = speed;
    if (speed === 'auto_1') arbiterGame.clockPeriod = 1.0;
    else if (speed === 'auto_2') arbiterGame.clockPeriod = 0.5;
  }
}

function toggleArbiterSound() {
  if (!arbiterGame) return;
  arbiterGame.audio.enabled = !arbiterGame.audio.enabled;
  document.getElementById('arbiterSoundBtn').textContent = arbiterGame.audio.enabled ? '🔊 Sound: ON' : '🔈 Sound: OFF';
}

function toggleArbiterPause() {
  if (arbiterGame) arbiterGame.togglePause();
}

function saveArbiterRecord() {
  if (!arbiterGame) return;
  const name = document.getElementById("arbiterCallsign").value.trim() || "Arbiter Prime";
  const org = document.getElementById("arbiterOrg").value.trim() || "Silicon Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const record = {
    name: name,
    org: org,
    track: `Arbiter Arena (Wave ${arbiterGame.wave})`,
    score: arbiterGame.score,
    accuracy: arbiterGame.deliveredCount, // flits delivered
    certId: `ARBITER-WAVE-${arbiterGame.wave}`,
    date: dateStr,
    type: "arbiter"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("arbiterSaveConfirm").style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitArbiterToGithub() {
  if (!arbiterGame) return;
  const name = document.getElementById("arbiterCallsign").value.trim() || "Arbiter Prime";
  const org = document.getElementById("arbiterOrg").value.trim() || "Silicon Lab";
  const title = `[arbiter-highscore] ${name} — ${arbiterGame.score} pts (${arbiterGame.deliveredCount} flits)`;
  const body = [
    "### Arbiter Arena Crossbar Clash High Score",
    `- **Arbiter**: ${name}`,
    `- **Institution/Handle**: ${org}`,
    `- **High Score**: ${arbiterGame.score} pts`,
    `- **Flits Delivered**: ${arbiterGame.deliveredCount}`,
    `- **Wave Reached**: Wave ${arbiterGame.wave}`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: arbiterGame.score,
      delivered: arbiterGame.deliveredCount,
      wave: arbiterGame.wave,
      type: "arbiter"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}
</script>
