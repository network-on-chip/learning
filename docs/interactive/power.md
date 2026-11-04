# ⚡ Volt Vortex: Dark Silicon & Power Gating

Conquer the dark silicon dilemma and design ultra-low-power Networks-on-Chip! In sub-3nm finFET and nanosheet technology, Dennard scaling has ended: we can fabricate more transistors on a die than we can thermally power simultaneously (**Dark Silicon**). 

Even when idle, static leakage current ($P_{leak} = I_{leak} \cdot V_{dd}$) burns up to 45% of total router energy. Deploying **Sleep Transistors** cuts leakage by over 90%, but waking up a sleeping router incurs an inrush wake-up penalty ($T_{wake} \approx 8\text{--}12$ cycles). If packets crash into dark routers, they stall or suffer detour latencies!

Master **Adaptive Run-Time Power Gating**, balance energy-delay product (EDP), deploy **Wake-up Surges**, and keep thermal dissipation within strict TDP power caps! Your high scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="powerStartBtn" class="noc-sim-btn" onclick="startPowerGame()">▶ Start Energy Maestro</button>
    <button id="powerSurgeBtn" class="noc-sim-btn" onclick="triggerPowerSurge()" style="background:#0284c7; border:none; box-shadow:0 0 14px rgba(2,132,199,0.5);">⚡ Rail Power Surge (Space / W)</button>

    <label><b>Power Gating Policy:</b>
      <select id="powerGatingSelect" class="noc-sim-select" onchange="setPowerPolicy(this.value)">
        <option value="adaptive_gating">Adaptive Dynamic Gating (3s Idle Timeout)</option>
        <option value="aggressive_sleep">Aggressive Dark Silicon (Instant Sleep)</option>
        <option value="always_on">Always-On Baseline (Zero Sleep · High Leakage)</option>
      </select>
    </label>

    <button id="powerSoundBtn" class="noc-sim-btn secondary" onclick="togglePowerSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="togglePowerPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="powerScore">0</span></span>
      <span style="color:#22c55e;">Saved: <span id="powerSaved">0.0</span> J</span>
      <span style="color:#ef4444;">Power: <span id="powerCurrent">0.0</span> W</span>
      <span style="color:#f59e0b;" id="powerWave">Wave 1</span>
    </div>
  </div>

  <!-- TDP Power Budget & Surge HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">⚡ Rail Power Surge Reservoir (Space / W):</span>
        <span id="surgeEnergyText" style="font-weight:700; color:#38bdf8;">100% READY</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="surgeEnergyBar" style="width:100%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#22c55e;">🌡️ Silicon TDP Thermal Budget (&lt; 14.0 W):</span>
        <span id="tdpStatusText" style="font-weight:700; color:#22c55e;">SAFE (4.2 W)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(34,197,94,0.15); border-radius:4px; overflow:hidden;">
        <div id="tdpBar" style="width:30%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="powerCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="powerOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="powerModalIcon">💥</div>
      <h2 id="powerModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">TDP THERMAL RUNAWAY!</h2>
      <p id="powerModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Static leakage and dynamic switching power exceeded the 15.0W silicon TDP envelope!
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Low-Power Architect Callsign:</label>
        <input type="text" id="powerCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Energy Maestro" value="Volt Maestro">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="powerOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Qualcomm Hexagon / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="savePowerRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitPowerToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartPowerGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="powerSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in local Hall of Fame!
      </div>
    </div>
  </div>

  <div id="powerInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">⚡ Power Gating Microarchitecture &amp; Dark Silicon Rules:</strong>
    <ul style="margin:0.4rem 0 0 1.2rem; padding:0;">
      <li><strong>Active vs. Dark Silicon:</strong> Active routers (blue) dissipate $1.2\text{ W}$ static leakage + dynamic flit power. Sleeping routers (dim gray) decouple power rails, slashing leakage to only $0.05\text{ W}$.</li>
      <li><strong>Wake-Up Penalty ($T_{wake}$):</strong> Flits heading toward a dark router must wait for header decoders to energize the sleep transistor ($1.0\text{s}$ delay).</li>
      <li><strong>Rail Power Surge (Space / W):</strong> Instantly powers up all 16 routers simultaneously for 4 seconds to flush backlog traffic during heavy bursts!</li>
      <li><strong>TDP Thermal Cap:</strong> Keep total chip power below $14.0\text{ W}$. If too many routers are left awake concurrently during heavy traffic, TDP breach triggers thermal shutdown.</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Volt Vortex
class PowerAudio {
  constructor() {
    this.ctx = null;
    this.enabled = true;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  playSleep() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(440, t);
      osc.frequency.exponentialRampToValueAtTime(110, t + 0.18);
      gain.gain.setValueAtTime(0.1, t);
      gain.gain.linearRampToValueAtTime(0.001, t + 0.18);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.18);
    } catch (e) {}
  }

  playWake() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(160, t);
      osc.frequency.exponentialRampToValueAtTime(540, t + 0.16);
      gain.gain.setValueAtTime(0.12, t);
      gain.gain.linearRampToValueAtTime(0.001, t + 0.16);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.16);
    } catch (e) {}
  }

  playSurge() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      [330, 440, 660].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(freq, t + idx * 0.05);
        gain.gain.setValueAtTime(0.14, t + idx * 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, t + idx * 0.05 + 0.22);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t + idx * 0.05);
        osc.stop(t + idx * 0.05 + 0.22);
      });
    } catch (e) {}
  }

  playDeliver() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(587.33, t);
      osc.frequency.exponentialRampToValueAtTime(880, t + 0.12);
      gain.gain.setValueAtTime(0.1, t);
      gain.gain.linearRampToValueAtTime(0.001, t + 0.12);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.12);
    } catch (e) {}
  }

  playOverheat() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(130, t);
      osc.frequency.linearRampToValueAtTime(40, t + 0.3);
      gain.gain.setValueAtTime(0.25, t);
      gain.gain.linearRampToValueAtTime(0.01, t + 0.3);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.3);
    } catch (e) {}
  }
}

// 4x4 Dark Silicon Simulation Engine
class PowerGame {
  constructor() {
    this.canvas = document.getElementById('powerCanvas');
    this.ctx = this.canvas.getContext('2d');
    this.audio = new PowerAudio();

    this.gridW = 4;
    this.gridH = 4;
    this.nodeSpacingX = 125;
    this.nodeSpacingY = 95;
    this.offsetX = 120;
    this.offsetY = 85;

    this.routers = []; // 16 routers: { state: 'awake'|'sleeping'|'waking', idleTimer: 0, wakeTimer: 0 }
    this.packets = [];
    this.particles = [];
    this.score = 0;
    this.deliveredCount = 0;
    this.energySavedJ = 0.0;
    this.currentPowerW = 4.2;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.surgeEnergy = 100.0;
    this.surgeActive = false;
    this.surgeTimer = 0.0;
    this.policy = 'adaptive_gating';

    this.isRunning = false;
    this.isPaused = false;
    this.lastTime = performance.now();
    this.injectTimer = 0;
    this.nextPktId = 1;
  }

  start() {
    this.audio.init();
    this.routers = [];
    for (let y = 0; y < this.gridH; y++) {
      for (let x = 0; x < this.gridW; x++) {
        this.routers.push({
          x: x,
          y: y,
          state: 'awake',
          idleTimer: 0,
          wakeTimer: 0
        });
      }
    }

    this.packets = [];
    this.particles = [];
    this.score = 0;
    this.deliveredCount = 0;
    this.energySavedJ = 0.0;
    this.currentPowerW = 4.2;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.surgeEnergy = 100.0;
    this.surgeActive = false;
    this.surgeTimer = 0.0;
    this.isRunning = true;
    this.isPaused = false;

    document.getElementById('powerOverModal').style.display = 'none';
    document.getElementById('powerStartBtn').textContent = '🔄 Restart';
    this.lastTime = performance.now();

    for (let i = 0; i < 4; i++) {
      this.injectTraffic();
    }
  }

  getRouter(x, y) {
    return this.routers[y * this.gridW + x];
  }

  injectTraffic() {
    const sx = Math.floor(Math.random() * this.gridW);
    const sy = Math.floor(Math.random() * this.gridH);
    let dx = Math.floor(Math.random() * this.gridW);
    let dy = Math.floor(Math.random() * this.gridH);
    while (dx === sx && dy === sy) {
      dx = Math.floor(Math.random() * this.gridW);
      dy = Math.floor(Math.random() * this.gridH);
    }

    const pkt = {
      id: this.nextPktId++,
      gx: sx,
      gy: sy,
      fromGx: sx,
      fromGy: sy,
      toGx: sx,
      toGy: sy,
      dstX: dx,
      dstY: dy,
      progress: 1.0,
      state: 'at_node',
      color: '#38bdf8'
    };
    this.packets.push(pkt);
  }

  triggerSurge() {
    if (this.surgeEnergy >= 100 && !this.surgeActive) {
      this.surgeActive = true;
      this.surgeTimer = 4.0;
      this.audio.playSurge();
      for (let r of this.routers) {
        r.state = 'awake';
        r.idleTimer = 0;
      }
      this.addTextParticle(this.canvas.width / 2, 70, '⚡ RAIL POWER SURGE: ALL NODES AWAKE!', '#38bdf8');
    }
  }

  update(dt) {
    if (!this.isRunning || this.isPaused) return;

    this.waveTimer -= dt;
    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 22.0;
      this.score += 300 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 60, `WAVE ${this.wave} WORKLOAD SCALING!`, '#f59e0b');
    }

    // Surge energy charge
    if (this.surgeActive) {
      this.surgeTimer -= dt;
      this.surgeEnergy = Math.max(0, (this.surgeTimer / 4.0) * 100);
      if (this.surgeTimer <= 0) {
        this.surgeActive = false;
        this.surgeEnergy = 0;
      }
    } else {
      this.surgeEnergy = Math.min(100, this.surgeEnergy + dt * 14.0);
    }

    // Step 1: Manage Router Power Gating States
    let awakeCount = 0;
    let sleepCount = 0;

    for (let r of this.routers) {
      if (this.surgeActive || this.policy === 'always_on') {
        r.state = 'awake';
      } else if (r.state === 'awake') {
        r.idleTimer += dt;
        const timeout = this.policy === 'aggressive_sleep' ? 0.6 : 2.5;
        if (r.idleTimer >= timeout) {
          r.state = 'sleeping';
          this.audio.playSleep();
        }
      } else if (r.state === 'waking') {
        r.wakeTimer -= dt;
        if (r.wakeTimer <= 0) {
          r.state = 'awake';
          r.idleTimer = 0;
          this.audio.playWake();
        }
      }

      if (r.state === 'awake') awakeCount++;
      else sleepCount++;
    }

    // Calculate Real-Time Power & Energy Saved
    const awakeLeakage = awakeCount * 0.75; // 0.75W per awake router
    const sleepLeakage = sleepCount * 0.04; // 0.04W per sleeping router
    const dynamicPower = this.packets.length * 0.18; // Switching power
    this.currentPowerW = awakeLeakage + sleepLeakage + dynamicPower;

    // Baseline if all were awake: 16 * 0.75 = 12.0W
    const savedWatts = Math.max(0, (12.0 + dynamicPower) - this.currentPowerW);
    this.energySavedJ += savedWatts * dt;

    // Check TDP Violation (>14.5W)
    if (this.currentPowerW > 14.5) {
      this.audio.playOverheat();
      this.triggerGameOver();
      return;
    }

    // Inject traffic
    this.injectTimer += dt;
    const injectInterval = Math.max(0.4, 1.3 - this.wave * 0.1);
    if (this.injectTimer >= injectInterval && this.packets.length < 18 + this.wave * 2) {
      this.injectTimer = 0;
      this.injectTraffic();
    }

    // Step 2: Advance Packets
    const speed = 1.35;
    for (let i = this.packets.length - 1; i >= 0; i--) {
      const p = this.packets[i];

      if (p.state === 'in_flight') {
        p.progress += dt * speed;
        if (p.progress >= 1.0) {
          p.progress = 1.0;
          p.gx = p.toGx;
          p.gy = p.toGy;
          p.state = 'at_node';

          // Mark current router as active
          const currR = this.getRouter(p.gx, p.gy);
          currR.idleTimer = 0;

          // Check Delivery
          if (p.gx === p.dstX && p.gy === p.dstY) {
            this.packets.splice(i, 1);
            this.deliveredCount++;
            this.score += 60;
            this.audio.playDeliver();
            this.addTextParticle(this.getNodeX(p.gx), this.getNodeY(p.gy), '+60', '#22c55e');
            continue;
          }
        }
      }
    }

    // Step 3: Route packets at nodes (handling sleeping next hops)
    for (let p of this.packets) {
      if (p.state === 'at_node') {
        let nextX = p.gx;
        let nextY = p.gy;
        if (p.dstX > p.gx) nextX = p.gx + 1;
        else if (p.dstX < p.gx) nextX = p.gx - 1;
        else if (p.dstY > p.gy) nextY = p.gy + 1;
        else if (p.dstY < p.gy) nextY = p.gy - 1;

        const nextR = this.getRouter(nextX, nextY);
        if (nextR.state === 'sleeping') {
          // Trigger wake-up sequence
          nextR.state = 'waking';
          nextR.wakeTimer = 0.8; // 0.8s wake-up delay
          this.addTextParticle(this.getNodeX(nextX), this.getNodeY(nextY), '⚡ WAKE UP', '#f59e0b');
        } else if (nextR.state === 'awake') {
          // Router is ready! Forward packet
          nextR.idleTimer = 0;
          p.toGx = nextX;
          p.toGy = nextY;
          p.fromGx = p.gx;
          p.fromGy = p.gy;
          p.progress = 0;
          p.state = 'in_flight';
        }
      }
    }

    // Update particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const pt = this.particles[i];
      pt.y -= dt * 30;
      pt.life -= dt;
      if (pt.life <= 0) this.particles.splice(i, 1);
    }

    this.updateHUD();
  }

  getNodeX(gx) { return this.offsetX + gx * this.nodeSpacingX; }
  getNodeY(gy) { return this.offsetY + gy * this.nodeSpacingY; }

  render() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw interconnect links
    this.ctx.lineWidth = 3;
    for (let y = 0; y < this.gridH; y++) {
      for (let x = 0; x < this.gridW; x++) {
        const nx = this.getNodeX(x);
        const ny = this.getNodeY(y);

        if (x < this.gridW - 1) {
          const r1 = this.getRouter(x, y);
          const r2 = this.getRouter(x + 1, y);
          const isDark = r1.state === 'sleeping' && r2.state === 'sleeping';
          this.ctx.strokeStyle = isDark ? '#1e293b' : '#334155';
          this.ctx.beginPath();
          this.ctx.moveTo(nx, ny);
          this.ctx.lineTo(this.getNodeX(x + 1), ny);
          this.ctx.stroke();
        }
        if (y < this.gridH - 1) {
          const r1 = this.getRouter(x, y);
          const r2 = this.getRouter(x, y + 1);
          const isDark = r1.state === 'sleeping' && r2.state === 'sleeping';
          this.ctx.strokeStyle = isDark ? '#1e293b' : '#334155';
          this.ctx.beginPath();
          this.ctx.moveTo(nx, ny);
          this.ctx.lineTo(nx, this.getNodeY(y + 1));
          this.ctx.stroke();
        }
      }
    }

    // Draw packets
    for (let p of this.packets) {
      let px, py;
      if (p.state === 'in_flight') {
        const x1 = this.getNodeX(p.fromGx);
        const y1 = this.getNodeY(p.fromGy);
        const x2 = this.getNodeX(p.toGx);
        const y2 = this.getNodeY(p.toGy);
        px = x1 + (x2 - x1) * p.progress;
        py = y1 + (y2 - y1) * p.progress;
      } else {
        px = this.getNodeX(p.gx);
        py = this.getNodeY(p.gy);
      }

      this.ctx.save();
      this.ctx.shadowColor = '#38bdf8';
      this.ctx.shadowBlur = 10;
      this.ctx.fillStyle = '#38bdf8';
      this.ctx.beginPath();
      this.ctx.arc(px, py, 6, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();
    }

    // Draw 4x4 routers with power state styling
    for (let r of this.routers) {
      const nx = this.getNodeX(r.x);
      const ny = this.getNodeY(r.y);

      this.ctx.save();
      if (r.state === 'awake') {
        this.ctx.fillStyle = '#1e293b';
        this.ctx.strokeStyle = '#38bdf8';
        this.ctx.lineWidth = 2;
        this.ctx.shadowColor = '#38bdf8';
        this.ctx.shadowBlur = 8;
      } else if (r.state === 'waking') {
        this.ctx.fillStyle = '#1e293b';
        this.ctx.strokeStyle = '#f59e0b';
        this.ctx.lineWidth = 3;
        this.ctx.shadowColor = '#f59e0b';
        this.ctx.shadowBlur = 12;
      } else {
        // sleeping (Dark Silicon)
        this.ctx.fillStyle = '#0f172a';
        this.ctx.strokeStyle = '#334155';
        this.ctx.lineWidth = 1;
      }

      this.ctx.beginPath();
      this.ctx.roundRect(nx - 18, ny - 18, 36, 36, 6);
      this.ctx.fill();
      this.ctx.stroke();
      this.ctx.restore();

      // State Text
      this.ctx.font = '10px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      if (r.state === 'sleeping') {
        this.ctx.fillStyle = '#475569';
        this.ctx.fillText('Zzz', nx, ny);
      } else if (r.state === 'waking') {
        this.ctx.fillStyle = '#f59e0b';
        this.ctx.fillText('⚡', nx, ny);
      } else {
        this.ctx.fillStyle = '#38bdf8';
        this.ctx.fillText(`R${r.x}${r.y}`, nx, ny);
      }
    }

    // Draw floating particles
    for (let pt of this.particles) {
      this.ctx.save();
      this.ctx.fillStyle = pt.color;
      this.ctx.font = 'bold 11px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.shadowColor = pt.color;
      this.ctx.shadowBlur = 6;
      this.ctx.fillText(pt.text, pt.x, pt.y);
      this.ctx.restore();
    }
  }

  addTextParticle(x, y, text, color) {
    this.particles.push({ x, y, text, color, life: 1.2 });
  }

  updateHUD() {
    document.getElementById('powerScore').textContent = this.score;
    document.getElementById('powerSaved').textContent = this.energySavedJ.toFixed(1);
    document.getElementById('powerCurrent').textContent = this.currentPowerW.toFixed(1);
    document.getElementById('powerWave').textContent = `Wave ${this.wave}`;

    // Surge energy bar
    const bar = document.getElementById('surgeEnergyBar');
    const text = document.getElementById('surgeEnergyText');
    bar.style.width = `${this.surgeEnergy}%`;
    if (this.surgeActive) {
      text.textContent = `⚡ SURGE ACTIVE (${this.surgeTimer.toFixed(1)}s)`;
      bar.style.background = '#f59e0b';
    } else {
      text.textContent = this.surgeEnergy >= 100 ? '100% READY' : `${Math.floor(this.surgeEnergy)}% CHARGING`;
      bar.style.background = 'linear-gradient(90deg, #0284c7, #38bdf8)';
    }

    // TDP thermal budget bar
    const tdpPct = Math.min(100, (this.currentPowerW / 14.5) * 100);
    const tdpBar = document.getElementById('tdpBar');
    const tdpText = document.getElementById('tdpStatusText');
    tdpBar.style.width = `${tdpPct}%`;
    tdpBar.style.background = tdpPct > 80 ? '#ef4444' : (tdpPct > 55 ? '#f59e0b' : '#22c55e');
    tdpText.textContent = `${this.currentPowerW.toFixed(1)} W (${tdpPct > 80 ? 'CRITICAL' : 'SAFE'})`;
  }

  triggerGameOver() {
    this.isRunning = false;
    document.getElementById('powerModalTitle').textContent = 'TDP THERMAL RUNAWAY!';
    document.getElementById('powerModalSummary').innerHTML = `
      Silicon total power exceeded the 14.5W TDP envelope!<br><br>
      <b>Final Wave:</b> Wave ${this.wave} | <b>Energy Saved:</b> ${this.energySavedJ.toFixed(1)} J | <b>Score:</b> ${this.score} pts
    `;
    document.getElementById('powerOverModal').style.display = 'flex';
  }
}

let powerGame = null;

function startPowerGame() {
  if (!powerGame) powerGame = new PowerGame();
  powerGame.start();
}

function restartPowerGame() {
  if (powerGame) powerGame.start();
}

function triggerPowerSurge() {
  if (powerGame && powerGame.isRunning) {
    powerGame.triggerSurge();
  }
}

function setPowerPolicy(pol) {
  if (powerGame) powerGame.policy = pol;
}

function togglePowerSound() {
  if (powerGame) {
    powerGame.audio.enabled = !powerGame.audio.enabled;
    document.getElementById('powerSoundBtn').textContent = powerGame.audio.enabled ? '🔊 Sound: ON' : '🔇 Sound: OFF';
  }
}

function togglePowerPause() {
  if (powerGame) powerGame.isPaused = !powerGame.isPaused;
}

// Global Animation Loop
function powerLoop(now) {
  if (powerGame && powerGame.isRunning) {
    const dt = Math.min(0.05, (now - powerGame.lastTime) / 1000);
    powerGame.lastTime = now;
    powerGame.update(dt);
    powerGame.render();
  }
  requestAnimationFrame(powerLoop);
}
requestAnimationFrame(powerLoop);

// Keyboard controls
window.addEventListener('keydown', (e) => {
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
  if (e.code === 'Space' || e.code === 'KeyW') {
    if (powerGame && powerGame.isRunning) {
      triggerPowerSurge();
      e.preventDefault();
    }
  }
});

// Hall of Fame Leaderboard & GitHub Submission Integration
function savePowerRecord() {
  if (!powerGame) return;
  const nameInput = document.getElementById('powerCallsign').value.trim() || 'Volt Maestro';
  const orgInput = document.getElementById('powerOrg').value.trim() || 'Silicon Lab';

  const record = {
    name: nameInput,
    org: orgInput,
    track: `Volt Vortex (Wave ${powerGame.wave})`,
    score: powerGame.score,
    accuracy: Number(powerGame.energySavedJ.toFixed(1)),
    date: new Date().toISOString().slice(0, 10),
    certId: `POWER-WAVE-${powerGame.wave}-${Math.floor(Math.random() * 900 + 100)}`,
    type: 'power'
  };

  try {
    const key = 'noc_leaderboard_records';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push(record);
    localStorage.setItem(key, JSON.stringify(existing));
    const confirmEl = document.getElementById('powerSaveConfirm');
    if (confirmEl) confirmEl.style.display = 'block';
  } catch (err) {
    console.error('Failed to save to localStorage', err);
  }
}

function submitPowerToGithub() {
  if (!powerGame) return;
  const nameInput = document.getElementById('powerCallsign').value.trim() || 'Volt Maestro';
  const orgInput = document.getElementById('powerOrg').value.trim() || 'Silicon Lab';

  const title = encodeURIComponent(`[Leaderboard Submission] Volt Vortex - ${nameInput} (${powerGame.score} pts)`);
  const body = encodeURIComponent([
    `### ⚡ Volt Vortex: Dark Silicon & Power Gating Score Submission`,
    `- **Low-Power Architect**: ${nameInput}`,
    `- **Institution / Org**: ${orgInput}`,
    `- **Wave Reached**: Wave ${powerGame.wave}`,
    `- **Energy Saved**: ${powerGame.energySavedJ.toFixed(1)} Joules`,
    `- **Packets Delivered**: ${powerGame.deliveredCount}`,
    `- **Total Score**: ${powerGame.score} pts`,
    `- **Submission Timestamp**: ${new Date().toISOString()}`,
    ``,
    `\`\`\`json`,
    JSON.stringify({
      type: "power",
      player: nameInput,
      org: orgInput,
      score: powerGame.score,
      wave: powerGame.wave,
      saved_joules: Number(powerGame.energySavedJ.toFixed(1)),
      delivered: powerGame.deliveredCount,
      date: new Date().toISOString().slice(0, 10),
      certId: `POWER-WAVE-${powerGame.wave}-${Math.floor(Math.random() * 900 + 100)}`
    }, null, 2),
    `\`\`\``
  ].join('\n'));

  window.open(`https://github.com/network-on-chip/learning/issues/new?title=${title}&body=${body}`, '_blank');
}
</script>
