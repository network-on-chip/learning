# 🎮 Deadlock Buster: The NoC Buffer Defense Game

Welcome to **Deadlock Buster**, an interactive computer architecture arcade game where you serve as the chip's Router Arbiter. Keep the silicon alive by preventing circular buffer deadlocks and thermal queue meltdowns as traffic waves intensify! High scores can be directly inscribed on the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="gameStartBtn" class="noc-sim-btn" onclick="startDeadlockGame()">▶ Start Game</button>
    <button id="escapeFlushBtn" class="noc-sim-btn" onclick="activateEscapeChannel()" style="background:#ea580c; border:none; box-shadow:0 0 12px rgba(234,88,12,0.4);">⚡ Flush Escape Channel (Space)</button>
    
    <label><b>Routing Policy:</b>
      <select id="gamePolicy" class="noc-sim-select" onchange="setGamePolicy(this.value)">
        <option value="adaptive">Unrestricted Adaptive (High Bandwidth / Deadlock Risk!)</option>
        <option value="west-first">West-First Turn Model (Deadlock-Free / Asymmetric Congestion)</option>
        <option value="xy">Strict XY Routing (Acyclic CDG / Queue Overflow Risk)</option>
      </select>
    </label>

    <button id="soundToggleBtn" class="noc-sim-btn secondary" onclick="toggleGameSound()" title="Toggle Web Audio Sound">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="togglePauseGame()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="gameScore">0</span></span>
      <span style="color:#ef4444;">Deadlocks: <span id="gameDeadlocks">0</span></span>
      <span style="color:#22c55e;">Wave: <span id="gameWave">1</span></span>
      <span style="color:#f59e0b;" id="comboBadge">Combo: 1x</span>
    </div>
  </div>

  <!-- Escape Energy & Thermal Status HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">⚡ Escape VC Energy (Space):</span>
        <span id="escapeEnergyText" style="font-weight:700; color:#38bdf8;">100%</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="escapeEnergyBar" style="width:100%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#f87171;">🔥 Chip Buffer Thermal Load:</span>
        <span id="chipTempText" style="font-weight:700; color:#4ade80;">45°C (Nominal)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(239,68,68,0.15); border-radius:4px; overflow:hidden;">
        <div id="chipTempBar" style="width:25%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="gameCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>
    
    <!-- Game Over / Victory Modal -->
    <div id="gameOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:2.8rem; margin-bottom:0.35rem;">💥</div>
      <h2 id="gameOverTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">CHIP NETWORK DEADLOCKED!</h2>
      <p id="gameOverSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Circular channel dependencies froze multiple routers simultaneously.
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Enter Your Callsign / Name:</label>
        <input type="text" id="playerCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Master Arbiter" value="NoC Defender">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="playerOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Stanford / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveGameRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitGameToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="saveConfirmMsg" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in your browser Leaderboard!
      </div>
    </div>
  </div>

  <div id="gameInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">🎮 How to Play &amp; Architectural Theory:</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Circular Wait Deadlocks (Adaptive Policy):</strong> Flits navigate dynamically. Heavy traffic creates circular channel dependencies ($R_A \to R_B \to R_C \to R_D \to R_A$) that freeze routers in <span style="color:#ef4444; font-weight:700;">pulsing RED rings</span>!</li>
      <li><strong>Duato's Escape Virtual Channel:</strong> Press <strong>SPACEBAR</strong> or tap <strong>⚡ Flush Escape Channel</strong> to deploy Duato's theorem. Escape VCs follow an acyclic XY path to drain the cycle! Flushing consumes <strong>Escape Energy</strong>, which recharges as flits deliver.</li>
      <li><strong>Queue Overflow (XY &amp; Turn Models):</strong> XY routing eliminates circular turns, but under bursty traffic, buffers saturate ($> 4$ flits) and chip temperature surges towards $110^\circ\text{C}$!</li>
      <li><strong>Controls:</strong> <code>Space</code> = Flush Escape Channel | <code>P</code> = Pause | <code>R</code> = Restart | <code>1</code>/<code>2</code>/<code>3</code> = Change Routing Policy.</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer (No external assets required)
class GameAudio {
  constructor() {
    this.ctx = null;
    this.enabled = true;
  }

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.ctx = new AudioContext();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  playDelivery() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(587.33, now); // D5
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.08); // A5
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.15);
    } catch(e) {}
  }

  playDeadlockWarning() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.linearRampToValueAtTime(160, now + 0.18);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.2);
    } catch(e) {}
  }

  playEscapeFlush() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.exponentialRampToValueAtTime(1280, now + 0.25);
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.3);
    } catch(e) {}
  }

  playGameOver() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(180, now);
      osc.frequency.exponentialRampToValueAtTime(45, now + 0.55);
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.6);
    } catch(e) {}
  }
}

const gameAudio = new GameAudio();

function toggleGameSound() {
  gameAudio.enabled = !gameAudio.enabled;
  if (gameAudio.enabled) gameAudio.init();
  const btn = document.getElementById("soundToggleBtn");
  if (btn) {
    btn.textContent = gameAudio.enabled ? "🔊 Sound: ON" : "🔇 Sound: OFF";
  }
}

class DeadlockGame {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.rows = 4;
    this.cols = 4;
    this.policy = 'adaptive';

    this.score = 0;
    this.deadlockFlushed = 0;
    this.wave = 1;
    this.combo = 1;
    this.comboTimer = 0;
    this.isPlaying = false;
    this.isPaused = false;
    this.isOver = false;
    this.spawnTimer = 0;

    this.escapeEnergy = 100; // 0 - 100%
    this.chipTemp = 45; // in Celsius

    this.flits = [];
    this.deadlockedNodes = new Set();
    this.deadlockedCycles = []; // Array of cycles [[r1, r2, r3, r4], ...]
    this.deadlockTimer = 0;
    this.nodeBuffers = Array.from({ length: 16 }, () => 0);
    this.nodeWaitTarget = Array.from({ length: 16 }, () => null); // Which node each router is blocked waiting on
    this.particles = []; // Visual particle bursts

    this.nodeRadius = 22;
    this.padding = 60;
    this.initCanvas();
    this.bindEvents();

    this.loop = this.loop.bind(this);
    requestAnimationFrame(this.loop);
  }

  bindEvents() {
    const handleTap = (e) => {
      gameAudio.init();
      if (!this.isPlaying || this.isOver || this.isPaused) return;
      this.flushEscape();
    };

    this.canvas.addEventListener('click', handleTap);
    this.canvas.addEventListener('touchstart', (e) => {
      e.preventDefault();
      handleTap(e);
    }, { passive: false });
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

  start() {
    gameAudio.init();
    this.score = 0;
    this.deadlockFlushed = 0;
    this.wave = 1;
    this.combo = 1;
    this.comboTimer = 0;
    this.escapeEnergy = 100;
    this.chipTemp = 45;
    this.flits = [];
    this.particles = [];
    this.deadlockedNodes.clear();
    this.deadlockedCycles = [];
    this.deadlockTimer = 0;
    this.nodeBuffers.fill(0);
    this.nodeWaitTarget.fill(null);
    this.isPlaying = true;
    this.isPaused = false;
    this.isOver = false;

    const modal = document.getElementById("gameOverModal");
    if (modal) modal.style.display = "none";
    const msg = document.getElementById("saveConfirmMsg");
    if (msg) msg.style.display = "none";

    document.getElementById("gameScore").textContent = "0";
    document.getElementById("gameDeadlocks").textContent = "0";
    document.getElementById("gameWave").textContent = "1";
    document.getElementById("gameStartBtn").textContent = "🔄 Restart";
    this.updateHUD();
  }

  getNodePos(x, y) {
    return {
      px: this.padding + x * this.stepX,
      py: this.padding + y * this.stepY
    };
  }

  spawnFlit() {
    const sx = Math.floor(Math.random() * this.cols);
    const sy = Math.floor(Math.random() * this.rows);
    let dx = Math.floor(Math.random() * this.cols);
    let dy = Math.floor(Math.random() * this.rows);

    // Wave pattern variations:
    if (this.wave >= 3 && Math.random() < 0.45) {
      // Transpose traffic: (x,y) -> (y,x)
      dx = sy; dy = sx;
    } else if (this.wave >= 5 && Math.random() < 0.4) {
      // Hotspot traffic: Target cores (1,1) or (2,2)
      dx = Math.random() < 0.5 ? 1 : 2;
      dy = Math.random() < 0.5 ? 1 : 2;
    }

    while (dx === sx && dy === sy) {
      dx = Math.floor(Math.random() * this.cols);
      dy = Math.floor(Math.random() * this.rows);
    }

    const colors = ['#2563eb', '#38bdf8', '#fb923c', '#a855f7', '#10b981'];
    this.flits.push({
      id: Math.floor(Math.random() * 900) + 100,
      curr: { x: sx, y: sy },
      dst: { x: dx, y: dy },
      next: null,
      progress: 0,
      color: colors[Math.floor(Math.random() * colors.length)],
      isBlocked: false,
      isEscapeVC: false, // If true, routed via Duato's acyclic escape subchannel
      stallCycles: 0
    });
  }

  computeNext(curr, dst, isEscape) {
    if (curr.x === dst.x && curr.y === dst.y) return null;

    // Duato's Escape VC always uses strict XY Dimension-Order Routing (guaranteed acyclic CDG)
    if (isEscape || this.policy === 'xy') {
      if (curr.x < dst.x) return { x: curr.x + 1, y: curr.y };
      if (curr.x > dst.x) return { x: curr.x - 1, y: curr.y };
      if (curr.y < dst.y) return { x: curr.x, y: curr.y + 1 };
      if (curr.y > dst.y) return { x: curr.x, y: curr.y - 1 };
    } else if (this.policy === 'west-first') {
      // West-First Turn Model: Must route West first before any North/South turns
      if (dst.x < curr.x) return { x: curr.x - 1, y: curr.y };
      const cand = [];
      if (dst.x > curr.x) cand.push({ x: curr.x + 1, y: curr.y });
      if (dst.y > curr.y) cand.push({ x: curr.x, y: curr.y + 1 });
      if (dst.y < curr.y) cand.push({ x: curr.x, y: curr.y - 1 });
      return cand[Math.floor(Math.random() * cand.length)] || null;
    } else {
      // Unrestricted Adaptive: Chooses least-congested viable neighbor towards destination
      const cand = [];
      if (dst.x > curr.x) cand.push({ x: curr.x + 1, y: curr.y });
      if (dst.x < curr.x) cand.push({ x: curr.x - 1, y: curr.y });
      if (dst.y > curr.y) cand.push({ x: curr.x, y: curr.y + 1 });
      if (dst.y < curr.y) cand.push({ x: curr.x, y: curr.y - 1 });

      if (cand.length === 0) return null;
      // Sort candidates by lowest buffer occupancy
      cand.sort((a, b) => {
        const idxA = a.y * this.cols + a.x;
        const idxB = b.y * this.cols + b.x;
        return this.nodeBuffers[idxA] - this.nodeBuffers[idxB];
      });
      return cand[0];
    }
    return null;
  }

  detectCycles() {
    this.deadlockedNodes.clear();
    this.deadlockedCycles = [];

    if (this.policy !== 'adaptive') {
      return; // XY and West-first eliminate cycles mathematically
    }

    // Build wait-for graph: node -> waiting target node
    for (let i = 0; i < 16; i++) {
      this.nodeWaitTarget[i] = null;
    }

    for (const f of this.flits) {
      if (f.isBlocked && f.next && !f.isEscapeVC) {
        const currIdx = f.curr.y * this.cols + f.curr.x;
        const targetIdx = f.next.y * this.cols + f.next.x;
        this.nodeWaitTarget[currIdx] = targetIdx;
      }
    }

    // Detect directed cycles in the wait-for graph
    const visited = new Array(16).fill(0); // 0=unvisited, 1=visiting, 2=visited
    const stack = [];

    const dfs = (u) => {
      visited[u] = 1;
      stack.push(u);
      const v = this.nodeWaitTarget[u];
      if (v !== null && v !== undefined) {
        if (visited[v] === 1) {
          // Cycle found!
          const cycleStart = stack.indexOf(v);
          if (cycleStart !== -1) {
            const cycle = stack.slice(cycleStart);
            this.deadlockedCycles.push(cycle);
            for (const node of cycle) {
              this.deadlockedNodes.add(node);
            }
          }
        } else if (visited[v] === 0) {
          dfs(v);
        }
      }
      stack.pop();
      visited[u] = 2;
    };

    for (let i = 0; i < 16; i++) {
      if (visited[i] === 0 && this.nodeWaitTarget[i] !== null) {
        dfs(i);
      }
    }
  }

  flushEscape() {
    if (!this.isPlaying || this.isOver || this.isPaused) return;

    if (this.escapeEnergy < 25) {
      // Energy too low!
      return;
    }

    this.escapeEnergy = Math.max(0, this.escapeEnergy - 35);
    gameAudio.playEscapeFlush();

    let clearedCount = 0;
    // Release blocked flits in deadlocked nodes by promoting them to Escape VC (XY routing)
    for (const f of this.flits) {
      const currIdx = f.curr.y * this.cols + f.curr.x;
      if (this.deadlockedNodes.has(currIdx) || f.isBlocked) {
        f.isBlocked = false;
        f.isEscapeVC = true; // Promoted to Escape VC
        f.next = this.computeNext(f.curr, f.dst, true);
        f.progress = 0;
        clearedCount++;

        // Add visual particle effect
        const pos = this.getNodePos(f.curr.x, f.curr.y);
        for (let k = 0; k < 6; k++) {
          this.particles.push({
            x: pos.px,
            y: pos.py,
            vx: (Math.random() - 0.5) * 4,
            vy: (Math.random() - 0.5) * 4,
            life: 1.0,
            color: '#38bdf8'
          });
        }
      }
    }

    if (clearedCount > 0) {
      const bonus = clearedCount * 60 * this.combo;
      this.score += bonus;
      this.deadlockFlushed += clearedCount;
      this.combo = Math.min(5, this.combo + 1);
      this.comboTimer = 220; // Maintain combo window
      document.getElementById("gameScore").textContent = this.score;
      document.getElementById("comboBadge").textContent = `Combo: ${this.combo}x`;
    }

    this.deadlockTimer = 0;
    this.deadlockedNodes.clear();
    this.deadlockedCycles = [];
    document.getElementById("gameDeadlocks").textContent = "0";
    this.updateHUD();
  }

  gameOver(reason) {
    this.isPlaying = false;
    this.isOver = true;
    gameAudio.playGameOver();

    const modal = document.getElementById("gameOverModal");
    if (modal) modal.style.display = "flex";

    const titleEl = document.getElementById("gameOverTitle");
    if (titleEl) {
      titleEl.textContent = reason === 'thermal' ? "🔥 CHIP THERMAL MELTDOWN!" : "💥 CHIP NETWORK DEADLOCKED!";
    }

    const summaryEl = document.getElementById("gameOverSummary");
    if (summaryEl) {
      const reasonText = reason === 'thermal' 
        ? "Buffer queues in dimension-order routing saturated without escape channels, triggering thermal shutdown." 
        : "Circular channel dependencies froze 4+ routers simultaneously, halting the clock.";
      summaryEl.innerHTML = `<strong>${reasonText}</strong><br><br>Final Score: <strong>${this.score} pts</strong> | Wave Reached: <strong>Wave ${this.wave}</strong> | Deadlocks Cleared: <strong>${this.deadlockFlushed}</strong>`;
    }
  }

  updateHUD() {
    const energyBar = document.getElementById("escapeEnergyBar");
    const energyText = document.getElementById("escapeEnergyText");
    if (energyBar && energyText) {
      energyBar.style.width = `${Math.floor(this.escapeEnergy)}%`;
      energyText.textContent = `${Math.floor(this.escapeEnergy)}%`;
      if (this.escapeEnergy < 25) {
        energyBar.style.background = '#ef4444';
      } else {
        energyBar.style.background = 'linear-gradient(90deg, #0284c7, #38bdf8)';
      }
    }

    const tempBar = document.getElementById("chipTempBar");
    const tempText = document.getElementById("chipTempText");
    if (tempBar && tempText) {
      const pct = Math.min(100, Math.max(10, ((this.chipTemp - 35) / 75) * 100));
      tempBar.style.width = `${pct}%`;
      tempText.textContent = `${Math.floor(this.chipTemp)}°C ${this.chipTemp > 85 ? '(CRITICAL!)' : (this.chipTemp > 65 ? '(Elevated)' : '(Nominal)')}`;
      if (this.chipTemp > 85) {
        tempBar.style.background = '#ef4444';
        tempText.style.color = '#ef4444';
      } else if (this.chipTemp > 65) {
        tempBar.style.background = '#f59e0b';
        tempText.style.color = '#f59e0b';
      } else {
        tempBar.style.background = '#22c55e';
        tempText.style.color = '#22c55e';
      }
    }
  }

  update() {
    if (!this.isPlaying || this.isOver || this.isPaused) return;

    this.spawnTimer++;

    // Recharge Escape Energy over time
    this.escapeEnergy = Math.min(100, this.escapeEnergy + 0.08);

    // Combo timer decrement
    if (this.comboTimer > 0) {
      this.comboTimer--;
      if (this.comboTimer === 0) {
        this.combo = 1;
        document.getElementById("comboBadge").textContent = "Combo: 1x";
      }
    }

    // Spawn packets according to wave
    const spawnRate = Math.max(14, 52 - this.wave * 4);
    const maxActiveFlits = Math.min(32, 16 + this.wave * 2);
    if (this.spawnTimer % spawnRate === 0 && this.flits.length < maxActiveFlits) {
      this.spawnFlit();
    }

    // Wave advancement
    if (this.spawnTimer % 450 === 0) {
      this.wave++;
      document.getElementById("gameWave").textContent = this.wave;
      this.score += 100 * this.wave;
      document.getElementById("gameScore").textContent = this.score;
    }

    // Recalculate buffer counts
    this.nodeBuffers.fill(0);
    for (const f of this.flits) {
      const idx = f.curr.y * this.cols + f.curr.x;
      this.nodeBuffers[idx]++;
    }

    // Thermal load calculation: average buffers and hotspots
    const maxBuffer = Math.max(...this.nodeBuffers);
    const avgBuffer = this.nodeBuffers.reduce((a, b) => a + b, 0) / 16;
    this.chipTemp = 42 + avgBuffer * 7 + maxBuffer * 4;

    // In XY / West-First routing: test for Buffer Overflow Thermal Meltdown
    if (this.policy !== 'adaptive' && maxBuffer >= 5) {
      if (this.chipTemp >= 105) {
        this.gameOver('thermal');
        return;
      }
    }

    // Step flits
    for (let i = this.flits.length - 1; i >= 0; i--) {
      const f = this.flits[i];

      if (!f.next) {
        f.next = this.computeNext(f.curr, f.dst, f.isEscapeVC);
        if (!f.next) {
          // Delivered to destination!
          this.score += 25 * this.combo;
          this.escapeEnergy = Math.min(100, this.escapeEnergy + 2.5); // Reward delivery
          gameAudio.playDelivery();

          const pPos = this.getNodePos(f.curr.x, f.curr.y);
          for (let k = 0; k < 5; k++) {
            this.particles.push({
              x: pPos.px,
              y: pPos.py,
              vx: (Math.random() - 0.5) * 3,
              vy: (Math.random() - 0.5) * 3,
              life: 0.8,
              color: '#22c55e'
            });
          }

          document.getElementById("gameScore").textContent = this.score;
          this.flits.splice(i, 1);
          continue;
        }
      }

      // Check downstream buffer capacity (Max 4 flits per router)
      const targetIdx = f.next.y * this.cols + f.next.x;
      const targetIsFull = this.nodeBuffers[targetIdx] >= 3;

      if (targetIsFull && !f.isEscapeVC) {
        f.stallCycles++;
        if (f.stallCycles >= 15) {
          f.isBlocked = true;
        }
      } else {
        f.stallCycles = 0;
        f.isBlocked = false;
      }

      // Move flit if not blocked
      if (!f.isBlocked) {
        f.progress += 0.045;
        if (f.progress >= 1) {
          f.progress = 0;
          f.curr = { ...f.next };
          f.next = null;
        }
      }
    }

    // Run Cycle Detection
    this.detectCycles();
    document.getElementById("gameDeadlocks").textContent = this.deadlockedNodes.size;

    if (this.deadlockedNodes.size >= 4) {
      this.deadlockTimer = (this.deadlockTimer || 0) + 1;
      if (this.deadlockTimer % 20 === 0) {
        gameAudio.playDeadlockWarning();
      }
      if (this.deadlockTimer >= 150) { // ~2.5 seconds grace period
        this.gameOver('deadlock');
        return;
      }
    } else {
      this.deadlockTimer = 0;
      if (this.deadlockedNodes.size > 0 && this.spawnTimer % 40 === 0) {
        gameAudio.playDeadlockWarning();
      }
    }

    // Update Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.life -= 0.035;
      if (p.life <= 0) {
        this.particles.splice(i, 1);
      }
    }

    if (this.spawnTimer % 6 === 0) {
      this.updateHUD();
    }
  }

  draw() {
    this.ctx.clearRect(0, 0, this.width, this.height);

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

    // Draw Deadlock Dependency Cycle Rays
    if (this.deadlockedCycles.length > 0) {
      this.ctx.save();
      this.ctx.lineWidth = 3.5;
      this.ctx.strokeStyle = '#ef4444';
      this.ctx.setLineDash([6, 4]);
      this.ctx.lineDashOffset = -Date.now() / 30;

      for (const cycle of this.deadlockedCycles) {
        for (let k = 0; k < cycle.length; k++) {
          const u = cycle[k];
          const v = cycle[(k + 1) % cycle.length];
          const ux = u % this.cols, uy = Math.floor(u / this.cols);
          const vx = v % this.cols, vy = Math.floor(v / this.cols);
          const p1 = this.getNodePos(ux, uy);
          const p2 = this.getNodePos(vx, vy);

          this.ctx.beginPath();
          this.ctx.moveTo(p1.px, p1.py);
          this.ctx.lineTo(p2.px, p2.py);
          this.ctx.stroke();
        }
      }
      this.ctx.restore();
    }

    // Draw Particles
    for (const p of this.particles) {
      this.ctx.fillStyle = p.color;
      this.ctx.globalAlpha = Math.max(0, p.life);
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
      this.ctx.fill();
    }
    this.ctx.globalAlpha = 1.0;

    // Draw Flits
    for (const f of this.flits) {
      const p1 = this.getNodePos(f.curr.x, f.curr.y);
      let fx = p1.px;
      let fy = p1.py;
      if (f.next && !f.isBlocked) {
        const p2 = this.getNodePos(f.next.x, f.next.y);
        fx += (p2.px - p1.px) * f.progress;
        fy += (p2.py - p1.py) * f.progress;
      }

      this.ctx.fillStyle = f.isEscapeVC ? '#38bdf8' : (f.isBlocked ? '#ef4444' : f.color);
      this.ctx.beginPath();
      this.ctx.arc(fx, fy, 8, 0, Math.PI * 2);
      this.ctx.fill();

      // Escape VC aura
      if (f.isEscapeVC) {
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = '#38bdf8';
        this.ctx.stroke();
      }
    }

    // Draw Routers
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const { px, py } = this.getNodePos(c, r);
        const idx = r * this.cols + c;
        const isDeadlocked = this.deadlockedNodes.has(idx);
        const buf = this.nodeBuffers[idx];

        this.ctx.beginPath();
        this.ctx.arc(px, py, this.nodeRadius, 0, Math.PI * 2);

        if (isDeadlocked) {
          const pulse = (Math.sin(Date.now() / 140) + 1) / 2;
          this.ctx.fillStyle = pulse > 0.5 ? '#ef4444' : '#7f1d1d';
        } else if (buf >= 4) {
          this.ctx.fillStyle = '#b45309'; // Queue Warning
        } else {
          this.ctx.fillStyle = '#0f172a';
        }
        this.ctx.fill();

        this.ctx.lineWidth = isDeadlocked ? 3.5 : (buf >= 4 ? 2.5 : 1.5);
        this.ctx.strokeStyle = isDeadlocked ? '#fca5a5' : (buf >= 4 ? '#f59e0b' : '#38bdf8');
        this.ctx.stroke();

        // Router ID
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = 'bold 10px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(`R${idx}`, px, py - 3);

        // Buffer badge
        this.ctx.font = '9px monospace';
        this.ctx.fillStyle = buf >= 4 ? '#f87171' : (buf >= 2 ? '#fb923c' : '#94a3b8');
        this.ctx.fillText(`buf:${buf}`, px, py + 8);
      }
    }

    // Deadlock Countdown Warning Banner
    if (this.deadlockTimer > 0 && this.isPlaying && !this.isOver) {
      const remainingSec = Math.max(0, ((150 - this.deadlockTimer) / 60)).toFixed(1);
      const isFlash = Math.floor(this.deadlockTimer / 8) % 2 === 0;
      this.ctx.fillStyle = isFlash ? 'rgba(239, 68, 68, 0.92)' : 'rgba(185, 28, 28, 0.92)';
      this.ctx.fillRect(20, 15, this.width - 40, 36);
      this.ctx.strokeStyle = '#fef08a';
      this.ctx.lineWidth = 2;
      this.ctx.strokeRect(20, 15, this.width - 40, 36);

      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 13px sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(`🚨 DEADLOCK DETECTED! HIT SPACE / TAP CANVAS TO FLUSH ESCAPE VC (${remainingSec}s)`, this.width / 2, 33);
    }

    // Start Screen Overlay
    if (!this.isPlaying && !this.isOver) {
      this.ctx.fillStyle = 'rgba(15, 23, 42, 0.82)';
      this.ctx.fillRect(0, 0, this.width, this.height);
      this.ctx.fillStyle = '#38bdf8';
      this.ctx.font = 'bold 22px sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.fillText('👾 DEADLOCK BUSTER ARCADE', this.width / 2, this.height / 2 - 20);

      this.ctx.fillStyle = '#cbd5e1';
      this.ctx.font = '14px sans-serif';
      this.ctx.fillText('Press "▶ Start Game" to Defend the Silicon Network', this.width / 2, this.height / 2 + 15);
    }
  }

  loop() {
    this.update();
    this.draw();
    requestAnimationFrame(this.loop);
  }
}

let game = null;

function initDeadlockGame() {
  if (document.getElementById('gameCanvas') && !game) {
    game = new DeadlockGame('gameCanvas');
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDeadlockGame);
} else {
  initDeadlockGame();
}

function startDeadlockGame() {
  if (game) game.start();
}

function restartGame() {
  if (game) game.start();
}

function activateEscapeChannel() {
  if (game) game.flushEscape();
}

function setGamePolicy(pol) {
  if (game) game.policy = pol;
}

function togglePauseGame() {
  if (!game) return;
  game.isPaused = !game.isPaused;
}

function saveGameRecord() {
  if (!game) return;
  const name = document.getElementById("playerCallsign").value.trim() || "NoC Defender";
  const org = document.getElementById("playerOrg").value.trim() || "Silicon Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const record = {
    name: name,
    org: org,
    track: `Deadlock Buster (Wave ${game.wave})`,
    score: game.score,
    accuracy: game.deadlockFlushed,
    certId: `GAME-WAVE-${game.wave}`,
    date: dateStr,
    type: "game"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    const existingIdx = list.findIndex(r => r.certId === record.certId && r.score === record.score);
    if (existingIdx !== -1) {
      list[existingIdx] = record;
    } else {
      list.unshift(record);
    }
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    const msg = document.getElementById("saveConfirmMsg");
    if (msg) msg.style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitGameToGithub() {
  if (!game) return;
  const name = document.getElementById("playerCallsign").value.trim() || "NoC Defender";
  const org = document.getElementById("playerOrg").value.trim() || "Silicon Lab";
  const title = `[game-highscore] ${name} — ${game.score} pts (Wave ${game.wave})`;
  const body = [
    "### Deadlock Buster Arcade High Score Submission",
    `- **Player**: ${name}`,
    `- **Institution/Handle**: ${org}`,
    `- **High Score**: ${game.score} pts`,
    `- **Wave Reached**: Wave ${game.wave}`,
    `- **Deadlocks Cleared**: ${game.deadlockFlushed}`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: game.score,
      wave: game.wave,
      cleared: game.deadlockFlushed,
      type: "game"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}

window.addEventListener('keydown', (e) => {
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) {
    return;
  }
  if (e.code === 'Space') {
    e.preventDefault();
    activateEscapeChannel();
  } else if (e.code === 'KeyP') {
    togglePauseGame();
  } else if (e.code === 'KeyR') {
    restartGame();
  } else if (e.code === 'Digit1') {
    const sel = document.getElementById("gamePolicy");
    if (sel) { sel.value = "adaptive"; setGamePolicy("adaptive"); }
  } else if (e.code === 'Digit2') {
    const sel = document.getElementById("gamePolicy");
    if (sel) { sel.value = "west-first"; setGamePolicy("west-first"); }
  } else if (e.code === 'Digit3') {
    const sel = document.getElementById("gamePolicy");
    if (sel) { sel.value = "xy"; setGamePolicy("xy"); }
  }
});
</script>
