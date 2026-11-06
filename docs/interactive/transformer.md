# ⚡ Transformer Titan: LLM & AI Collective Accelerator

Welcome to **Transformer Titan**, an interactive computer architecture arcade game where you command the on-chip and multi-die communication fabric accelerating a **100-Billion Parameter Large Language Model (LLM)**. Eliminate pipeline bubbles, orchestrate massive Tensor-Parallel All-Reduce collectives, break memory silos using 3D hybrid bonding, and prevent catastrophic buffer stalls! High scores can be inscribed directly on the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="ttStartBtn" class="noc-sim-btn" onclick="startTransformerGame()">▶ Start AI Training Engine</button>
    <button id="reductionBurstBtn" class="noc-sim-btn" onclick="activateReductionBurst()" style="background:#8b5cf6; border:none; box-shadow:0 0 14px rgba(139,92,246,0.5);">⚡ In-Network Reduction Burst (Space)</button>
    
    <label><b>Collective Interconnect Mode:</b>
      <select id="ttTopologySelect" class="noc-sim-select" onchange="setInterconnectMode(this.value)">
        <option value="pac_tree">Hierarchical In-Network Reduction Tree (PAC-NoC)</option>
        <option value="ruche">Ruche Wire-Maximal Express Links (HammerBlade)</option>
        <option value="ring">Conventional 2D Torus Ring-AllReduce</option>
      </select>
    </label>

    <button id="ttSoundBtn" class="noc-sim-btn secondary" onclick="toggleTtSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleTtPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="ttScore">0</span></span>
      <span style="color:#22c55e;">Tokens/s: <span id="ttTps">0</span></span>
      <span style="color:#f59e0b;" id="ttWaveBadge">Iteration: 1</span>
      <span style="color:#a855f7;" id="ttComboBadge">Combo: 1x</span>
    </div>
  </div>

  <!-- Memory Silo & Pipeline Bubble HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#a855f7;">⚡ In-Network ALU Reservoir (Space):</span>
        <span id="reductionEnergyText" style="font-weight:700; color:#a855f7;">100% READY</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(168,85,247,0.15); border-radius:4px; overflow:hidden;">
        <div id="reductionEnergyBar" style="width:100%; height:100%; background:linear-gradient(90deg, #7c3aed, #a855f7); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">🧠 DRAM Silo Bandwidth (Hybrid Bonding):</span>
        <span id="dramBwText" style="font-weight:700; color:#38bdf8;">16.4 TB/s (Optimal)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="dramBwBar" style="width:85%; height:100%; background:#38bdf8; transition:width 0.2s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#ef4444;">⏳ Pipeline Bubble Starvation:</span>
        <span id="bubbleRiskText" style="font-weight:700; color:#22c55e;">0% (Zero Idle)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(239,68,68,0.15); border-radius:4px; overflow:hidden;">
        <div id="bubbleRiskBar" style="width:0%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="ttCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>
    
    <!-- Game Over / Victory Modal -->
    <div id="ttOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:2.8rem; margin-bottom:0.35rem;" id="ttOverIcon">💥</div>
      <h2 id="ttOverTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">PIPELINE BUBBLE COLLAPSE!</h2>
      <p id="ttOverSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Communication delay exceeded compute deadlines, stalling the AI accelerator array.
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Enter Your Call Sign:</label>
        <input type="text" id="ttPlayerCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. LLM Architect" value="AI Cluster Architect">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Lab / Cluster Affiliation:</label>
        <input type="text" id="ttPlayerOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Cerebras / NVIDIA" value="Silicon AI Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveTtRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitTtToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartTransformerGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="ttSaveConfirmMsg" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Training record successfully recorded on Leaderboard!
      </div>
    </div>
  </div>
</div>

---

## 🔬 AI Interconnect Theory & Hardware Mapping

Transformer Titan models modern distributed deep learning interconnect research from IEEE TVLSI, TCAD, and JSSC:

### 1. In-Network Reduction Trees (PAC-NoC)
In **PAC-NoC** (TVLSI 2026), Transformer multi-head attention backward passes require massive gradient exchanges. Rather than streaming all weights back to memory, router crossbars embed addition ALU trees that perform **in-network reduction** on flits in flight. Pressing **Space** triggers an instantaneous reduction surge that halves network latency.

### 2. Ruche Wire-Maximal Topologies
In **HammerBlade in Silicon** (TVLSI 2026), 2,048 RISC-V cores connect via Ruche networks—exploiting thick upper metal layers to jump across multiple tile routers without adding crossbar ports. Selecting **Ruche Mode** (`2`) enables long-distance token hops that bypass intermediate routing congestion.

### 3. Face-to-Face 3D Hybrid Bonding
In **SiloBreaker** (TCAD 2026), 3D hybrid bonding deploys 3 µm pitch copper pillars directly between logic dies and DRAM, delivering over **16 TB/s of vertical bandwidth**. Scheduling memory access appropriately eliminates pipeline stalls during auto-regressive token generation.

---

<script>
// --- Audio Engine for Transformer Titan ---
class TransformerAudioEngine {
  constructor() {
    this.ctx = null;
    this.enabled = true;
  }
  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
  }
  token() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(523 + Math.random() * 120, now);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.08);
    } catch(e) {}
  }
  reduction() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(300, now);
      osc.frequency.exponentialRampToValueAtTime(900, now + 0.28);
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.linearRampToValueAtTime(0.001, now + 0.3);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.3);
    } catch(e) {}
  }
  stall() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(140, now);
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } catch(e) {}
  }
}

const ttAudio = new TransformerAudioEngine();

// --- Game Engine Implementation ---
let ttGame = null;

class TransformerGame {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.gridCols = 6;
    this.gridRows = 5;
    this.cellW = canvas.width / this.gridCols;
    this.cellH = canvas.height / this.gridRows;

    this.isPlaying = false;
    this.isPaused = false;
    this.isOver = false;

    this.score = 0;
    this.tokensPerSec = 0;
    this.iteration = 1;
    this.combo = 1;
    this.comboTimer = 0;

    this.reductionEnergy = 100;
    this.dramBw = 16.4; // TB/s
    this.bubbleRisk = 0; // %
    this.interconnectMode = 'pac_tree'; // pac_tree, ruche, ring

    this.cores = [];
    this.flits = [];
    this.particles = [];

    this.initGrid();
    this.lastTime = performance.now();
    this.spawnTimer = 0;
    this.iterTimer = 0;
    this.tpsAccumulator = 0;
  }

  initGrid() {
    this.cores = [];
    for (let r = 0; r < this.gridRows; r++) {
      for (let c = 0; c < this.gridCols; c++) {
        const isMemTier = (r === 0 || r === this.gridRows - 1);
        this.cores.push({
          row: r,
          col: c,
          x: c * this.cellW + this.cellW / 2,
          y: r * this.cellH + this.cellH / 2,
          isMemory: isMemTier,
          load: 0.1,
          attentionLoad: 0,
          active: false
        });
      }
    }
  }

  start() {
    this.isPlaying = true;
    this.isPaused = false;
    this.isOver = false;
    this.score = 0;
    this.tokensPerSec = 1200;
    this.iteration = 1;
    this.combo = 1;
    this.reductionEnergy = 100;
    this.bubbleRisk = 0;
    this.flits = [];
    this.particles = [];
    this.initGrid();
    this.lastTime = performance.now();
    ttAudio.init();
    ttAudio.token();
    this.updateHUD();
    document.getElementById("ttOverModal").style.display = "none";
  }

  update(dt) {
    if (!this.isPlaying || this.isPaused || this.isOver) return;

    this.spawnTimer += dt;
    this.iterTimer += dt;

    // Advance iterations every 20s
    if (this.iterTimer > 20) {
      this.iterTimer = 0;
      this.iteration++;
      this.score += 1000 * this.iteration;
      ttAudio.reduction();
      this.createShockwave(this.canvas.width/2, this.canvas.height/2, '#a855f7');
    }

    // Recharge Reduction ALU
    if (this.reductionEnergy < 100) {
      this.reductionEnergy = Math.min(100, this.reductionEnergy + dt * 20);
    }

    // Combo countdown
    if (this.combo > 1) {
      this.comboTimer -= dt;
      if (this.comboTimer <= 0) this.combo = 1;
    }

    // Spawn AI Attention / All-Reduce Flits
    const spawnRate = Math.max(0.08, 0.35 - (this.iteration * 0.025));
    if (this.spawnTimer >= spawnRate) {
      this.spawnTimer = 0;
      this.spawnAiFlit();
    }

    // Update Flits
    for (let i = this.flits.length - 1; i >= 0; i--) {
      const f = this.flits[i];
      f.progress += dt * f.speed;

      if (f.progress >= 1.0) {
        f.currR = f.targetR;
        f.currC = f.targetC;

        if (f.currR === f.destR && f.currC === f.destC) {
          // Reached destination core
          this.score += 35 * this.combo;
          this.tpsAccumulator += 12;
          this.bubbleRisk = Math.max(0, this.bubbleRisk - 1.2);
          ttAudio.token();
          this.flits.splice(i, 1);
        } else {
          // Route towards destination
          f.progress = 0;
          if (this.interconnectMode === 'ruche' && Math.abs(f.destC - f.currC) >= 2) {
            // Ruche Express jump
            f.targetC = f.currC + (f.destC > f.currC ? 2 : -2);
            f.targetR = f.currR;
          } else if (f.currC !== f.destC) {
            f.targetC = f.currC + (f.destC > f.currC ? 1 : -1);
            f.targetR = f.currR;
          } else if (f.currR !== f.destR) {
            f.targetR = f.currR + (f.destR > f.currR ? 1 : -1);
            f.targetC = f.currC;
          }
        }
      }

      const cur = this.getCore(f.currR, f.currC);
      const tar = this.getCore(f.targetR, f.targetC);
      if (cur && tar) {
        f.x = cur.x + (tar.x - cur.x) * f.progress;
        f.y = cur.y + (tar.y - cur.y) * f.progress;
      }
    }

    // Compute Tokens/Sec dynamically
    this.tokensPerSec = Math.round(1800 + this.tpsAccumulator * 15 + (this.iteration * 450));
    this.tpsAccumulator = Math.max(0, this.tpsAccumulator - dt * 10);

    // Bubble Starvation accumulation if queue is too crowded
    const inFlightCount = this.flits.length;
    if (inFlightCount > 35) {
      this.bubbleRisk += dt * (inFlightCount - 35) * 1.5;
    } else {
      this.bubbleRisk = Math.max(0, this.bubbleRisk - dt * 4);
    }

    // Mode-specific perks
    if (this.interconnectMode === 'pac_tree') {
      this.dramBw = 18.2;
    } else if (this.interconnectMode === 'ruche') {
      this.dramBw = 16.0;
    } else {
      this.dramBw = 11.5;
    }

    // Update Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt;
      if (p.life <= 0) this.particles.splice(i, 1);
    }

    // Check Loss condition
    if (this.bubbleRisk >= 100) {
      this.gameOver();
    }

    this.updateHUD();
  }

  spawnAiFlit() {
    const srcR = Math.floor(Math.random() * this.gridRows);
    const srcC = Math.floor(Math.random() * this.gridCols);
    let destR = Math.floor(Math.random() * this.gridRows);
    let destC = Math.floor(Math.random() * this.gridCols);
    while (destR === srcR && destC === srcC) {
      destR = Math.floor(Math.random() * this.gridRows);
      destC = Math.floor(Math.random() * this.gridCols);
    }

    const srcCore = this.getCore(srcR, srcC);
    const isMemoryAccess = srcCore.isMemory;
    const speed = this.interconnectMode === 'ruche' ? 3.0 : (this.interconnectMode === 'pac_tree' ? 2.5 : 1.9);

    this.flits.push({
      srcR, srcC,
      currR: srcR, currC: srcC,
      targetR: srcC !== destC ? srcR : (srcR + (destR > srcR ? 1 : -1)),
      targetC: srcC !== destC ? (srcC + (destC > srcC ? 1 : -1)) : srcC,
      destR, destC,
      progress: 0,
      speed,
      isMemoryAccess,
      x: srcCore.x,
      y: srcCore.y
    });
  }

  getCore(r, c) {
    if (r < 0 || r >= this.gridRows || c < 0 || c >= this.gridCols) return null;
    return this.cores[r * this.gridCols + c];
  }

  activateReduction() {
    if (this.reductionEnergy < 30) return;
    this.reductionEnergy -= 30;
    ttAudio.reduction();

    // Instant in-network reduction clears 50% of in-transit flits
    const reduced = Math.floor(this.flits.length * 0.55);
    for (let i = 0; i < reduced; i++) {
      if (this.flits.length > 0) {
        const removed = this.flits.pop();
        this.createShockwave(removed.x, removed.y, '#a855f7');
        this.score += 80 * this.combo;
      }
    }
    this.bubbleRisk = Math.max(0, this.bubbleRisk - 25);
    this.combo = Math.min(10, this.combo + 1);
    this.comboTimer = 3.0;
  }

  createShockwave(x, y, color) {
    for (let i = 0; i < 16; i++) {
      const angle = (i / 16) * Math.PI * 2;
      const spd = 90 + Math.random() * 60;
      this.particles.push({
        x, y,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd,
        life: 0.35,
        maxLife: 0.35,
        color,
        size: 3.0
      });
    }
  }

  draw() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Silicon Substrate & Interposer
    ctx.fillStyle = '#080c18';
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw Interconnect Wiring
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = '#1e293b';
    for (let r = 0; r < this.gridRows; r++) {
      for (let c = 0; c < this.gridCols; c++) {
        const cur = this.getCore(r, c);
        const east = this.getCore(r, c + 1);
        const south = this.getCore(r + 1, c);
        if (east) {
          ctx.beginPath();
          ctx.moveTo(cur.x, cur.y);
          ctx.lineTo(east.x, east.y);
          ctx.stroke();
        }
        if (south) {
          ctx.beginPath();
          ctx.moveTo(cur.x, cur.y);
          ctx.lineTo(south.x, south.y);
          ctx.stroke();
        }

        // Ruche 2-hop express links
        if (this.interconnectMode === 'ruche') {
          const rucheEast = this.getCore(r, c + 2);
          if (rucheEast) {
            ctx.save();
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
            ctx.setLineDash([4, 4]);
            ctx.beginPath();
            ctx.moveTo(cur.x, cur.y - 6);
            ctx.lineTo(rucheEast.x, rucheEast.y - 6);
            ctx.stroke();
            ctx.restore();
          }
        }
      }
    }

    // Cores / Memory Tiles
    for (const core of this.cores) {
      ctx.save();
      ctx.translate(core.x, core.y);

      if (core.isMemory) {
        // 3D Hybrid Bonding DRAM Pillar
        ctx.fillStyle = '#0284c7';
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2;
        ctx.fillRect(-16, -12, 32, 24);
        ctx.strokeRect(-16, -12, 32, 24);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 9px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillText('DRAM', 0, 3);
      } else {
        // AI Tensor Core Tile
        ctx.fillStyle = this.interconnectMode === 'pac_tree' ? '#4c1d95' : '#1e1b4b';
        ctx.strokeStyle = this.interconnectMode === 'pac_tree' ? '#c084fc' : '#818cf8';
        ctx.lineWidth = 2;
        ctx.fillRect(-14, -14, 28, 28);
        ctx.strokeRect(-14, -14, 28, 28);
        ctx.fillStyle = '#a5b4fc';
        ctx.font = '9px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillText('NPU', 0, 4);
      }
      ctx.restore();
    }

    // Flits
    for (const f of this.flits) {
      ctx.save();
      ctx.fillStyle = f.isMemoryAccess ? '#38bdf8' : (this.interconnectMode === 'pac_tree' ? '#c084fc' : '#fbbf24');
      ctx.shadowColor = f.isMemoryAccess ? '#38bdf8' : '#c084fc';
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.arc(f.x, f.y, 4.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // Particles
    for (const p of this.particles) {
      ctx.save();
      ctx.globalAlpha = p.life / p.maxLife;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  updateHUD() {
    document.getElementById("ttScore").textContent = this.score;
    document.getElementById("ttTps").textContent = `${this.tokensPerSec}`;
    document.getElementById("ttWaveBadge").textContent = `Iteration: ${this.iteration}`;
    document.getElementById("ttComboBadge").textContent = `Combo: ${this.combo}x`;

    // Reduction Energy
    document.getElementById("reductionEnergyText").textContent = `${Math.round(this.reductionEnergy)}% READY`;
    document.getElementById("reductionEnergyBar").style.width = `${this.reductionEnergy}%`;

    // DRAM Bandwidth
    document.getElementById("dramBwText").textContent = `${this.dramBw.toFixed(1)} TB/s`;
    document.getElementById("dramBwBar").style.width = `${Math.min(100, (this.dramBw / 20.0) * 100)}%`;

    // Bubble Risk
    const r = Math.min(100, Math.round(this.bubbleRisk));
    const bubbleEl = document.getElementById("bubbleRiskBar");
    const bubbleTxt = document.getElementById("bubbleRiskText");
    bubbleTxt.textContent = `${r}% ${r > 70 ? '(STALL IMMINENT)' : (r > 35 ? '(CONGESTED)' : '(HEALTHY)')}`;
    bubbleEl.style.width = `${r}%`;
    bubbleEl.style.background = r < 40 ? '#22c55e' : (r < 75 ? '#f59e0b' : '#ef4444');
  }

  gameOver() {
    this.isOver = true;
    this.isPlaying = false;
    ttAudio.stall();
    const modal = document.getElementById("ttOverModal");
    modal.style.display = "flex";
  }
}

// Global Handlers
function initTransformerGame() {
  const canvas = document.getElementById('ttCanvas');
  if (!canvas) return;
  ttGame = new TransformerGame(canvas);

  let last = performance.now();
  function loop(now) {
    const dt = (now - last) / 1000;
    last = now;
    if (ttGame) {
      ttGame.update(Math.min(dt, 0.1));
      ttGame.draw();
    }
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
}

function startTransformerGame() {
  if (!ttGame) initTransformerGame();
  ttGame.start();
}

function restartTransformerGame() {
  if (ttGame) ttGame.start();
}

function activateReductionBurst() {
  if (ttGame && ttGame.isPlaying) {
    ttGame.activateReduction();
  }
}

function setInterconnectMode(mode) {
  if (ttGame) {
    ttGame.interconnectMode = mode;
    ttAudio.reduction();
  }
}

function toggleTtSound() {
  ttAudio.enabled = !ttAudio.enabled;
  document.getElementById("ttSoundBtn").textContent = `🔊 Sound: ${ttAudio.enabled ? 'ON' : 'OFF'}`;
}

function toggleTtPause() {
  if (!ttGame) return;
  ttGame.isPaused = !ttGame.isPaused;
}

function saveTtRecord() {
  if (!ttGame) return;
  const name = document.getElementById("ttPlayerCallsign").value.trim() || "AI Cluster Architect";
  const org = document.getElementById("ttPlayerOrg").value.trim() || "Silicon AI Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const record = {
    score: ttGame.score,
    accuracy: Math.round(100 - ttGame.bubbleRisk),
    passed: ttGame.score >= 1200,
    module: `Transformer Titan: Iteration ${ttGame.iteration} (${ttGame.tokensPerSec} tokens/s)`,
    student: `${name} (${org})`,
    certId: `TT-ITER-${ttGame.iteration}`,
    date: dateStr,
    type: "game"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("ttSaveConfirmMsg").style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitTtToGithub() {
  if (!ttGame) return;
  const name = document.getElementById("ttPlayerCallsign").value.trim() || "AI Cluster Architect";
  const org = document.getElementById("ttPlayerOrg").value.trim() || "Silicon AI Lab";
  const title = `[game-highscore] ${name} — ${ttGame.score} pts in Transformer Titan (Iter ${ttGame.iteration}, ${ttGame.tokensPerSec} tok/s)`;
  const body = [
    "### Transformer Titan AI Accelerator High Score",
    `- **Player**: ${name}`,
    `- **Institution/Handle**: ${org}`,
    `- **Score**: ${ttGame.score} pts`,
    `- **Iteration**: Iteration ${ttGame.iteration}`,
    `- **Tokens/sec**: ${ttGame.tokensPerSec} tokens/s`,
    `- **Interconnect Mode**: ${ttGame.interconnectMode}`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: ttGame.score,
      iteration: ttGame.iteration,
      tokensPerSec: ttGame.tokensPerSec,
      mode: ttGame.interconnectMode,
      type: "game"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}

// Window Event Listeners
window.addEventListener('DOMContentLoaded', initTransformerGame);
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  setTimeout(initTransformerGame, 100);
}

window.addEventListener('keydown', (e) => {
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
  if (e.code === 'Space') {
    e.preventDefault();
    activateReductionBurst();
  } else if (e.code === 'Digit1') {
    const sel = document.getElementById("ttTopologySelect");
    if (sel) { sel.value = "pac_tree"; setInterconnectMode("pac_tree"); }
  } else if (e.code === 'Digit2') {
    const sel = document.getElementById("ttTopologySelect");
    if (sel) { sel.value = "ruche"; setInterconnectMode("ruche"); }
  } else if (e.code === 'Digit3') {
    const sel = document.getElementById("ttTopologySelect");
    if (sel) { sel.value = "ring"; setInterconnectMode("ring"); }
  } else if (e.code === 'KeyP') {
    toggleTtPause();
  } else if (e.code === 'KeyR') {
    restartTransformerGame();
  }
});
</script>
