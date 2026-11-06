# 🛡️ Silicon Sentinel: NoC Security & Threat Defense

Welcome to **Silicon Sentinel**, an interactive computer architecture arcade game where you command the hardware security monitors of a multi-tenant System-on-Chip (SoC). Prevent malicious Hardware Trojans from melting silicon tiles, block timing covert-channel sniffing from leaking cryptographic keys, and purge Denial-of-Service (DoS) buffer-flooding attacks! High scores can be inscribed directly on the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="secStartBtn" class="noc-sim-btn" onclick="startSecurityGame()">▶ Start Security Engine</button>
    <button id="pufShieldBtn" class="noc-sim-btn" onclick="activatePufShield()" style="background:#0284c7; border:none; box-shadow:0 0 14px rgba(2,132,199,0.5);">⚡ Deploy PUF Shield (Space)</button>
    
    <label><b>Active Defense Protocol:</b>
      <select id="secDefenseSelect" class="noc-sim-select" onchange="setDefensePolicy(this.value)">
        <option value="wma">WMA Thermal Anomaly Filter (Detects Thermal Trojans)</option>
        <option value="jitter">Traffic Jitter Masking (Scrambles Timing Covert Channels)</option>
        <option value="quarantine">Zero-Trust Quarantine (Aggressive Rogue IP Isolation)</option>
      </select>
    </label>

    <button id="secSoundBtn" class="noc-sim-btn secondary" onclick="toggleSecSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleSecPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="secScore">0</span></span>
      <span style="color:#ef4444;">Threats Blocked: <span id="secBlocked">0</span></span>
      <span style="color:#22c55e;">Wave: <span id="secWave">1</span></span>
      <span style="color:#f59e0b;" id="secComboBadge">Combo: 1x</span>
    </div>
  </div>

  <!-- Silicon Integrity & Exfiltration Risk HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">⚡ PUF Shield Reservoir (Space):</span>
        <span id="pufEnergyText" style="font-weight:700; color:#38bdf8;">100% READY</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="pufEnergyBar" style="width:100%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#22c55e;">🛡️ Silicon Physical Integrity:</span>
        <span id="siliconHealthText" style="font-weight:700; color:#22c55e;">100% (Nominal)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(34,197,94,0.15); border-radius:4px; overflow:hidden;">
        <div id="siliconHealthBar" style="width:100%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#ef4444;">🕵️ AES Key Exfiltration Risk:</span>
        <span id="leakRiskText" style="font-weight:700; color:#4ade80;">0% SAFE</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(239,68,68,0.15); border-radius:4px; overflow:hidden;">
        <div id="leakRiskBar" style="width:0%; height:100%; background:#4ade80; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="secCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>
    
    <!-- Game Over / Victory Modal -->
    <div id="secOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:2.8rem; margin-bottom:0.35rem;" id="secOverIcon">💥</div>
      <h2 id="secOverTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">SECURITY BREACH DETECTED!</h2>
      <p id="secOverSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Malicious Hardware Trojans compromised the on-chip network.
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Enter Your Defender Handle:</label>
        <input type="text" id="secPlayerCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Silicon Sentinel" value="Silicon Sentinel">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Organization:</label>
        <input type="text" id="secPlayerOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Hardware Security Lab" value="Zero-Trust SoC Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveSecRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitSecToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartSecurityGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="secSaveConfirmMsg" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Security record successfully saved to browser Leaderboard!
      </div>
    </div>
  </div>
</div>

---

## 🔬 Hardware Defense Theory & Architectural Mapping

Silicon Sentinel directly reflects peer-reviewed research in hardware security from IEEE TCAD, TVLSI, and TCAS:

### 1. Weighted Moving Average (WMA) Thermal Anomaly Detection
In **HeatSense** (TCAD 2026), malicious hardware Trojans trigger localized overheating by manipulating Dynamic Thermal Management (DTM) loops. Each router node evaluates a lightweight threshold using hardware-friendly bit-shifts:
$$\mu_{t} = \alpha \cdot T_{t} + (1 - \alpha) \cdot \mu_{t-1}, \quad \text{Anomaly} \iff |T_t - \mu_t| > K \cdot \sigma_t$$
Selecting **WMA Thermal Anomaly Filter** (`1`) automatically quarantines routers exceeding the safe gradient threshold.

### 2. Intrinsic Physical Unclonable Functions (PUFs)
In **NoCiPUF** (TCAS-I 2025), sub-nanosecond wire propagation delay variations between router crossbars serve as an unclonable silicon fingerprint. Pressing **Space** verifies cryptographic tokens across all in-flight flits and flushes forged packets injected by untrusted chiplets.

### 3. Timing Covert Channel Mitigation
Malicious IP blocks exfiltrate secret keys by modulating the inter-packet departure delay $\Delta t$. Activating **Traffic Jitter Masking** (`2`) injects pseudo-random micro-delays into virtual channels, reducing mutual information to near zero without causing throughput collapse.

---

<script>
// --- Silicon Sentinel Audio Engine ---
class SecurityAudioEngine {
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
  beep(freq = 440, duration = 0.08, type = 'sine', gainVal = 0.12) {
    if (!this.enabled || !this.ctx) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch(e) {}
  }
  shield() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.25);
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.linearRampToValueAtTime(0.001, now + 0.35);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } catch(e) {}
  }
  alert() {
    if (!this.enabled || !this.ctx) return;
    this.beep(880, 0.15, 'triangle', 0.2);
    setTimeout(() => this.beep(440, 0.18, 'triangle', 0.25), 120);
  }
  blocked() {
    this.beep(660, 0.06, 'sine', 0.15);
    setTimeout(() => this.beep(990, 0.08, 'sine', 0.18), 50);
  }
}

const secAudio = new SecurityAudioEngine();

// --- Game Engine Implementation ---
let secGame = null;

class SecurityGame {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.gridSize = 6;
    this.cellW = canvas.width / this.gridSize;
    this.cellH = canvas.height / this.gridSize;
    
    this.isPlaying = false;
    this.isPaused = false;
    this.isOver = false;
    
    this.score = 0;
    this.threatsBlocked = 0;
    this.wave = 1;
    this.combo = 1;
    this.comboTimer = 0;
    
    this.health = 100; // Silicon physical integrity
    this.leakRisk = 0; // Exfiltration risk percentage
    this.pufEnergy = 100;
    this.pufShieldActive = false;
    this.pufShieldTimer = 0;
    
    this.defensePolicy = 'wma'; // wma, jitter, quarantine
    
    this.routers = [];
    this.packets = [];
    this.particles = [];
    
    this.initGrid();
    this.lastTime = performance.now();
    this.spawnTimer = 0;
    this.waveTimer = 0;
  }

  initGrid() {
    this.routers = [];
    for (let r = 0; r < this.gridSize; r++) {
      for (let c = 0; c < this.gridSize; c++) {
        this.routers.push({
          row: r,
          col: c,
          x: c * this.cellW + this.cellW / 2,
          y: r * this.cellH + this.cellH / 2,
          temp: 45, // Celsius
          trojan: false,
          sniffing: false,
          quarantined: false,
          quarantineTimer: 0,
          wmaTemp: 45
        });
      }
    }
  }

  start() {
    this.isPlaying = true;
    this.isPaused = false;
    this.isOver = false;
    this.score = 0;
    this.threatsBlocked = 0;
    this.wave = 1;
    this.combo = 1;
    this.health = 100;
    this.leakRisk = 0;
    this.pufEnergy = 100;
    this.packets = [];
    this.particles = [];
    this.initGrid();
    this.lastTime = performance.now();
    secAudio.init();
    secAudio.beep(523, 0.15, 'sine');
    this.updateHUD();
    document.getElementById("secOverModal").style.display = "none";
  }

  update(dt) {
    if (!this.isPlaying || this.isPaused || this.isOver) return;

    this.spawnTimer += dt;
    this.waveTimer += dt;

    // Advance waves every 25 seconds
    if (this.waveTimer > 25) {
      this.waveTimer = 0;
      this.wave++;
      this.score += 500 * this.wave;
      secAudio.shield();
      this.createShockwave(this.canvas.width/2, this.canvas.height/2, '#38bdf8');
    }

    // Recharge PUF energy
    if (this.pufEnergy < 100) {
      this.pufEnergy = Math.min(100, this.pufEnergy + dt * 15);
    }
    if (this.pufShieldActive) {
      this.pufShieldTimer -= dt;
      if (this.pufShieldTimer <= 0) {
        this.pufShieldActive = false;
      }
    }

    // Combo countdown
    if (this.combo > 1) {
      this.comboTimer -= dt;
      if (this.comboTimer <= 0) {
        this.combo = 1;
      }
    }

    // Packet Spawning
    const spawnInterval = Math.max(0.18, 0.65 - (this.wave * 0.05));
    if (this.spawnTimer >= spawnInterval) {
      this.spawnTimer = 0;
      this.spawnPacket();
    }

    // Occasional Trojan / Sniffer Activation
    if (Math.random() < 0.02 * this.wave) {
      const eligible = this.routers.filter(rt => !rt.trojan && !rt.sniffing && !rt.quarantined);
      if (eligible.length > 0) {
        const target = eligible[Math.floor(Math.random() * eligible.length)];
        if (Math.random() < 0.5) {
          target.trojan = true; // Thermal Trojan
          secAudio.alert();
        } else {
          target.sniffing = true; // Timing Sniffer
          secAudio.beep(330, 0.12, 'sawtooth');
        }
      }
    }

    // Update Routers
    for (const rt of this.routers) {
      if (rt.quarantined) {
        rt.quarantineTimer -= dt;
        if (rt.quarantineTimer <= 0) {
          rt.quarantined = false;
        }
      }

      // Trojan heat buildup
      if (rt.trojan && !rt.quarantined) {
        rt.temp += dt * (12 + this.wave * 2);
        if (rt.temp > 105) {
          this.health -= dt * 8; // Silicon burn
        }
        // WMA Policy Auto-Quarantine
        if (this.defensePolicy === 'wma' && rt.temp > 75) {
          rt.quarantined = true;
          rt.trojan = false;
          rt.quarantineTimer = 4.0;
          this.threatsBlocked++;
          this.score += 250 * this.combo;
          this.addCombo();
          secAudio.blocked();
          this.createShockwave(rt.x, rt.y, '#22c55e');
        }
      } else {
        rt.temp = Math.max(45, rt.temp - dt * 8);
      }

      // Sniffer key leakage
      if (rt.sniffing && !rt.quarantined) {
        if (this.defensePolicy === 'jitter') {
          // Jitter scrambles the timing channel
          rt.sniffing = false;
          this.threatsBlocked++;
          this.score += 300 * this.combo;
          this.addCombo();
          secAudio.blocked();
          this.createShockwave(rt.x, rt.y, '#a855f7');
        } else {
          this.leakRisk += dt * (4.5 + this.wave * 0.8);
        }
      }
    }

    // Zero-Trust Quarantine Policy
    if (this.defensePolicy === 'quarantine') {
      for (const rt of this.routers) {
        if ((rt.trojan || rt.sniffing) && !rt.quarantined) {
          rt.quarantined = true;
          rt.trojan = false;
          rt.sniffing = false;
          rt.quarantineTimer = 5.0;
          this.threatsBlocked++;
          this.score += 200 * this.combo;
          this.addCombo();
          secAudio.blocked();
        }
      }
    }

    // Update Packets
    for (let i = this.packets.length - 1; i >= 0; i--) {
      const pkt = this.packets[i];
      pkt.progress += dt * pkt.speed;

      // PUF Shield absorbs malicious packets instantly
      if (this.pufShieldActive && pkt.isMalicious) {
        this.createSparks(pkt.x, pkt.y, '#38bdf8');
        this.packets.splice(i, 1);
        this.threatsBlocked++;
        this.score += 150 * this.combo;
        continue;
      }

      if (pkt.progress >= 1.0) {
        pkt.currR = pkt.targetR;
        pkt.currC = pkt.targetC;
        if (pkt.currR === pkt.destR && pkt.currC === pkt.destC) {
          // Reached destination
          if (pkt.isMalicious) {
            this.health -= 6;
            this.createSparks(pkt.x, pkt.y, '#ef4444');
            secAudio.alert();
          } else {
            this.score += 20;
          }
          this.packets.splice(i, 1);
        } else {
          // Next Hop via XY routing
          pkt.progress = 0;
          if (pkt.currC !== pkt.destC) {
            pkt.targetC = pkt.currC + (pkt.destC > pkt.currC ? 1 : -1);
            pkt.targetR = pkt.currR;
          } else if (pkt.currR !== pkt.destR) {
            pkt.targetR = pkt.currR + (pkt.destR > pkt.currR ? 1 : -1);
            pkt.targetC = pkt.currC;
          }
        }
      }

      const curRt = this.getRouter(pkt.currR, pkt.currC);
      const tarRt = this.getRouter(pkt.targetR, pkt.targetC);
      if (curRt && tarRt) {
        pkt.x = curRt.x + (tarRt.x - curRt.x) * pkt.progress;
        pkt.y = curRt.y + (tarRt.y - curRt.y) * pkt.progress;
      }
    }

    // Update Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt;
      if (p.life <= 0) this.particles.splice(i, 1);
    }

    // Check Loss Conditions
    if (this.health <= 0 || this.leakRisk >= 100) {
      this.gameOver();
    }

    this.updateHUD();
  }

  spawnPacket() {
    const srcR = Math.floor(Math.random() * this.gridSize);
    const srcC = Math.floor(Math.random() * this.gridSize);
    let destR = Math.floor(Math.random() * this.gridSize);
    let destC = Math.floor(Math.random() * this.gridSize);
    while (destR === srcR && destC === srcC) {
      destR = Math.floor(Math.random() * this.gridSize);
      destC = Math.floor(Math.random() * this.gridSize);
    }

    const srcRouter = this.getRouter(srcR, srcC);
    const isMalicious = srcRouter.trojan || (Math.random() < 0.15 + this.wave * 0.03);

    this.packets.push({
      srcR, srcC,
      currR: srcR, currC: srcC,
      targetR: srcC !== destC ? srcR : (srcR + (destR > srcR ? 1 : -1)),
      targetC: srcC !== destC ? (srcC + (destC > srcC ? 1 : -1)) : srcC,
      destR, destC,
      progress: 0,
      speed: isMalicious ? 2.4 : 1.8,
      isMalicious,
      x: srcRouter.x,
      y: srcRouter.y
    });
  }

  getRouter(r, c) {
    if (r < 0 || r >= this.gridSize || c < 0 || c >= this.gridSize) return null;
    return this.routers[r * this.gridSize + c];
  }

  addCombo() {
    this.combo = Math.min(10, this.combo + 1);
    this.comboTimer = 2.5;
  }

  activateShield() {
    if (this.pufEnergy < 35 || this.pufShieldActive) return;
    this.pufEnergy -= 35;
    this.pufShieldActive = true;
    this.pufShieldTimer = 3.5;
    secAudio.shield();
    this.createShockwave(this.canvas.width/2, this.canvas.height/2, '#0284c7');
  }

  createShockwave(x, y, color) {
    for (let i = 0; i < 24; i++) {
      const angle = (i / 24) * Math.PI * 2;
      const spd = 120 + Math.random() * 80;
      this.particles.push({
        x, y,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd,
        life: 0.45,
        maxLife: 0.45,
        color,
        size: 3.5
      });
    }
  }

  createSparks(x, y, color) {
    for (let i = 0; i < 8; i++) {
      const angle = Math.random() * Math.PI * 2;
      const spd = 40 + Math.random() * 60;
      this.particles.push({
        x, y,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd,
        life: 0.3,
        maxLife: 0.3,
        color,
        size: 2.5
      });
    }
  }

  draw() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Background Silicon Substrate
    ctx.fillStyle = '#0a0f1d';
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Grid Interconnect Links
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#1e293b';
    for (let r = 0; r < this.gridSize; r++) {
      for (let c = 0; c < this.gridSize; c++) {
        const rt = this.getRouter(r, c);
        const east = this.getRouter(r, c + 1);
        const south = this.getRouter(r + 1, c);
        if (east) {
          ctx.beginPath();
          ctx.moveTo(rt.x, rt.y);
          ctx.lineTo(east.x, east.y);
          ctx.stroke();
        }
        if (south) {
          ctx.beginPath();
          ctx.moveTo(rt.x, rt.y);
          ctx.lineTo(south.x, south.y);
          ctx.stroke();
        }
      }
    }

    // PUF Shield Field
    if (this.pufShieldActive) {
      ctx.save();
      ctx.fillStyle = 'rgba(2, 132, 199, 0.12)';
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.6)';
      ctx.lineWidth = 4;
      ctx.strokeRect(10, 10, this.canvas.width - 20, this.canvas.height - 20);
      ctx.fillRect(10, 10, this.canvas.width - 20, this.canvas.height - 20);
      ctx.restore();
    }

    // Routers
    for (const rt of this.routers) {
      ctx.save();
      ctx.translate(rt.x, rt.y);

      // Thermal Glow / Status
      if (rt.trojan) {
        ctx.fillStyle = 'rgba(239, 68, 68, 0.35)';
        ctx.beginPath();
        ctx.arc(0, 0, 24, 0, Math.PI * 2);
        ctx.fill();
      } else if (rt.sniffing) {
        ctx.fillStyle = 'rgba(168, 85, 247, 0.35)';
        ctx.beginPath();
        ctx.arc(0, 0, 24, 0, Math.PI * 2);
        ctx.fill();
      }

      // Router Tile Body
      ctx.fillStyle = rt.quarantined ? '#334155' : (rt.trojan ? '#dc2626' : (rt.sniffing ? '#9333ea' : '#1e293b'));
      ctx.strokeStyle = rt.quarantined ? '#64748b' : (rt.trojan ? '#f87171' : (rt.sniffing ? '#c084fc' : '#38bdf8'));
      ctx.lineWidth = 2;
      ctx.fillRect(-14, -14, 28, 28);
      ctx.strokeRect(-14, -14, 28, 28);

      // Temperature indicator
      ctx.fillStyle = '#94a3b8';
      ctx.font = '9px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`${Math.round(rt.temp)}°C`, 0, 24);

      if (rt.quarantined) {
        ctx.fillStyle = '#f87171';
        ctx.font = 'bold 12px sans-serif';
        ctx.fillText('🔒', 0, 4);
      }

      ctx.restore();
    }

    // Packets
    for (const pkt of this.packets) {
      ctx.save();
      ctx.fillStyle = pkt.isMalicious ? '#ef4444' : '#38bdf8';
      ctx.shadowColor = pkt.isMalicious ? '#f87171' : '#38bdf8';
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.arc(pkt.x, pkt.y, pkt.isMalicious ? 5.5 : 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // Particles
    for (const p of this.particles) {
      ctx.save();
      const alpha = p.life / p.maxLife;
      ctx.globalAlpha = alpha;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  updateHUD() {
    document.getElementById("secScore").textContent = this.score;
    document.getElementById("secBlocked").textContent = this.threatsBlocked;
    document.getElementById("secWave").textContent = this.wave;
    document.getElementById("secComboBadge").textContent = `Combo: ${this.combo}x`;

    // PUF Energy Bar
    document.getElementById("pufEnergyText").textContent = `${Math.round(this.pufEnergy)}% ${this.pufShieldActive ? '(SHIELD ACTIVE)' : ''}`;
    document.getElementById("pufEnergyBar").style.width = `${this.pufEnergy}%`;

    // Health Bar
    const healthEl = document.getElementById("siliconHealthBar");
    const healthTxt = document.getElementById("siliconHealthText");
    const h = Math.max(0, Math.round(this.health));
    healthTxt.textContent = `${h}% ${h < 30 ? '(CRITICAL)' : '(NOMINAL)'}`;
    healthEl.style.width = `${h}%`;
    healthEl.style.background = h > 60 ? '#22c55e' : (h > 30 ? '#f59e0b' : '#ef4444');

    // Leak Risk Bar
    const leakEl = document.getElementById("leakRiskBar");
    const leakTxt = document.getElementById("leakRiskText");
    const r = Math.min(100, Math.round(this.leakRisk));
    leakTxt.textContent = `${r}% ${r > 70 ? '(BREACH IMMINENT)' : (r > 30 ? '(EXFILTRATING)' : 'SAFE')}`;
    leakEl.style.width = `${r}%`;
    leakEl.style.background = r < 35 ? '#4ade80' : (r < 70 ? '#f59e0b' : '#ef4444');
  }

  gameOver() {
    this.isOver = true;
    this.isPlaying = false;
    secAudio.alert();
    const modal = document.getElementById("secOverModal");
    const title = document.getElementById("secOverTitle");
    const summary = document.getElementById("secOverSummary");

    if (this.health <= 0) {
      title.textContent = "SILICON THERMAL MELTDOWN!";
      summary.textContent = `Hardware Trojans overheated tile routers, exceeding maximum junction temperature (TDP breakdown). Wave reached: ${this.wave}. Final Score: ${this.score} pts.`;
    } else {
      title.textContent = "AES ENCRYPTION KEYS EXFILTRATED!";
      summary.textContent = `Timing covert channels successfully reconstructed the root cryptographic secret from packet delay jitter. Wave reached: ${this.wave}. Final Score: ${this.score} pts.`;
    }
    modal.style.display = "flex";
  }
}

// Global Hook Functions
function initSecurityGame() {
  const canvas = document.getElementById('secCanvas');
  if (!canvas) return;
  secGame = new SecurityGame(canvas);

  let last = performance.now();
  function loop(now) {
    const dt = (now - last) / 1000;
    last = now;
    if (secGame) {
      secGame.update(Math.min(dt, 0.1));
      secGame.draw();
    }
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
}

function startSecurityGame() {
  if (!secGame) initSecurityGame();
  secGame.start();
}

function restartSecurityGame() {
  if (secGame) secGame.start();
}

function activatePufShield() {
  if (secGame && secGame.isPlaying) {
    secGame.activateShield();
  }
}

function setDefensePolicy(pol) {
  if (secGame) {
    secGame.defensePolicy = pol;
    secAudio.beep(587, 0.08, 'triangle');
  }
}

function toggleSecSound() {
  secAudio.enabled = !secAudio.enabled;
  document.getElementById("secSoundBtn").textContent = `🔊 Sound: ${secAudio.enabled ? 'ON' : 'OFF'}`;
}

function toggleSecPause() {
  if (!secGame) return;
  secGame.isPaused = !secGame.isPaused;
}

function saveSecRecord() {
  if (!secGame) return;
  const name = document.getElementById("secPlayerCallsign").value.trim() || "Silicon Sentinel";
  const org = document.getElementById("secPlayerOrg").value.trim() || "Zero-Trust SoC Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const record = {
    score: secGame.score,
    accuracy: Math.round(secGame.health),
    passed: secGame.score >= 1000,
    module: `Silicon Sentinel: Wave ${secGame.wave} (${secGame.threatsBlocked} Threats Defended)`,
    student: `${name} (${org})`,
    certId: `SEC-WAVE-${secGame.wave}`,
    date: dateStr,
    type: "game"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("secSaveConfirmMsg").style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitSecToGithub() {
  if (!secGame) return;
  const name = document.getElementById("secPlayerCallsign").value.trim() || "Silicon Sentinel";
  const org = document.getElementById("secPlayerOrg").value.trim() || "Zero-Trust SoC Lab";
  const title = `[game-highscore] ${name} — ${secGame.score} pts in Silicon Sentinel (Wave ${secGame.wave})`;
  const body = [
    "### Silicon Sentinel Security Defense High Score",
    `- **Player**: ${name}`,
    `- **Institution/Handle**: ${org}`,
    `- **Score**: ${secGame.score} pts`,
    `- **Wave**: Wave ${secGame.wave}`,
    `- **Threats Blocked**: ${secGame.threatsBlocked}`,
    `- **Silicon Integrity**: ${Math.round(secGame.health)}%`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: secGame.score,
      wave: secGame.wave,
      blocked: secGame.threatsBlocked,
      health: Math.round(secGame.health),
      type: "game"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}

// Window Event Listeners
window.addEventListener('DOMContentLoaded', initSecurityGame);
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  setTimeout(initSecurityGame, 100);
}

window.addEventListener('keydown', (e) => {
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
  if (e.code === 'Space') {
    e.preventDefault();
    activatePufShield();
  } else if (e.code === 'Digit1') {
    const sel = document.getElementById("secDefenseSelect");
    if (sel) { sel.value = "wma"; setDefensePolicy("wma"); }
  } else if (e.code === 'Digit2') {
    const sel = document.getElementById("secDefenseSelect");
    if (sel) { sel.value = "jitter"; setDefensePolicy("jitter"); }
  } else if (e.code === 'Digit3') {
    const sel = document.getElementById("secDefenseSelect");
    if (sel) { sel.value = "quarantine"; setDefensePolicy("quarantine"); }
  } else if (e.code === 'KeyP') {
    toggleSecPause();
  } else if (e.code === 'KeyR') {
    restartSecurityGame();
  }
});
</script>
