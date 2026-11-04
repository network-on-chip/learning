# 💡 Photon Pilot: Optical NoC Waveguide Grid

Harness the speed of light on silicon! Steer multi-wavelength laser beams through integrated silicon optical waveguides using thermally-tuned **Micro-Ring Resonators (MRRs)**. Master Wavelength-Division Multiplexing (WDM), balance optical insertion loss budgets ($&lt; 12\text{ dB}$), and counteract localized thermal drift before bit-error rates surge! High scores can be directly inscribed on the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="opticalStartBtn" class="noc-sim-btn" onclick="startOpticalGame()">▶ Start Photon Pilot</button>
    <button id="laserBoostBtn" class="noc-sim-btn" onclick="activateLaserBoost()" style="background:#0284c7; border:none; box-shadow:0 0 12px rgba(2,132,199,0.4);">⚡ Laser Power Surge (Space)</button>

    <label><b>Tuning Mode:</b>
      <select id="mrrTuneSelect" class="noc-sim-select" onchange="setMrrTuning(this.value)">
        <option value="lambda1">λ1 (Cyan · 1530nm)</option>
        <option value="lambda2">λ2 (Green · 1540nm)</option>
        <option value="lambda3">λ3 (Amber · 1550nm)</option>
        <option value="lambda4">λ4 (Magenta · 1560nm)</option>
        <option value="bypass">OFF (Bypass / Pass-Through)</option>
      </select>
    </label>

    <button id="opticalSoundBtn" class="noc-sim-btn secondary" onclick="toggleOpticalSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleOpticalPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="opticalScore">0</span></span>
      <span style="color:#22c55e;">Bandwidth: <span id="opticalBandwidth">0.0</span> Tbps</span>
      <span style="color:#ef4444;">Loss: <span id="opticalLoss">0.0</span> dB</span>
      <span style="color:#f59e0b;" id="opticalWave">Wave 1</span>
    </div>
  </div>

  <!-- Optical Power & Thermal Stability HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">⚡ Laser Transmitter Surge Reservoir (Space):</span>
        <span id="laserSurgeText" style="font-weight:700; color:#38bdf8;">100%</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="laserSurgeBar" style="width:100%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#4ade80;">🌡️ Photonic Thermal Drift Stability:</span>
        <span id="opticalThermalText" style="font-weight:700; color:#4ade80;">100% (On-Resonance)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(34,197,94,0.15); border-radius:4px; overflow:hidden;">
        <div id="opticalThermalBar" style="width:100%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="opticalCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="opticalOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="opticalModalIcon">💥</div>
      <h2 id="opticalModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">OPTICAL LINK DROPOUT!</h2>
      <p id="opticalModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Optical insertion loss exceeded 14.0 dB and thermal drift shifted micro-ring resonance completely off-pitch!
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Photonic Pilot Callsign:</label>
        <input type="text" id="opticalCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Laser Architect" value="Photon Pilot">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="opticalOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Columbia Lightwave / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveOpticalRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitOpticalToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartOpticalGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="opticalSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in your browser Leaderboard!
      </div>
    </div>
  </div>

  <div id="opticalInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">💡 Silicon Photonics &amp; Optical NoC (ONoC) Theory:</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Wavelength-Division Multiplexing (WDM):</strong> Multiple distinct optical signals ($\lambda_1=1530\text{nm}, \lambda_2=1540\text{nm}, \lambda_3=1550\text{nm}, \lambda_4=1560\text{nm}$) share the same silicon waveguide simultaneously without interference, achieving multi-terabit bandwidth with flight-time latency ($\sim 10\text{ ps/mm}$).</li>
      <li><strong>Micro-Ring Resonators (MRRs):</strong> Integrated sub-micron silicon rings act as electro-optic switches. When the optical wavelength matches the round-trip phase condition ($m \lambda_{res} = 2\pi R \cdot n_{eff}$), light couples into the ring and drops onto the cross waveguide. Click any MRR to change its tuned wavelength!</li>
      <li><strong>Thermal Sensitivity ($dn/dT$):</strong> Silicon's high thermo-optic coefficient ($dn/dT \approx 1.86 \times 10^{-4}\text{ K}^{-1}$) shifts resonant wavelengths by $\sim 0.1\text{ nm/K}$. Thermal drift degrades link SNR unless compensated.</li>
      <li><strong>Insertion Loss Budget:</strong> Optical power degrades through waveguide propagation ($0.2\text{ dB/cm}$), waveguide bending, and ring drop crossings ($0.5\text{ dB/drop}$). Keep total path loss below $12.0\text{ dB}$ to avoid photodetector bit errors!</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Photon Pilot
class OpticalAudio {
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

  playTune() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, now);
      osc.frequency.exponentialRampToValueAtTime(1760, now + 0.08);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.1);
    } catch(e) {}
  }

  playLaserSurge() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(260, now);
      osc.frequency.exponentialRampToValueAtTime(1200, now + 0.25);
      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.3);
    } catch(e) {}
  }

  playReceive() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(659.25, now);
      osc.frequency.linearRampToValueAtTime(987.77, now + 0.09);
      gain.gain.setValueAtTime(0.1, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.11);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.11);
    } catch(e) {}
  }

  playAlarm() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.linearRampToValueAtTime(480, now + 0.15);
      gain.gain.setValueAtTime(0.12, now);
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
      osc.frequency.setValueAtTime(140, now);
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

const WAVELENGTHS = {
  lambda1: { name: 'λ1 (1530nm)', color: '#38bdf8', glow: 'rgba(56,189,248,0.6)' },
  lambda2: { name: 'λ2 (1540nm)', color: '#4ade80', glow: 'rgba(74,222,128,0.6)' },
  lambda3: { name: 'λ3 (1550nm)', color: '#fbbf24', glow: 'rgba(251,191,36,0.6)' },
  lambda4: { name: 'λ4 (1560nm)', color: '#f472b6', glow: 'rgba(244,114,182,0.6)' },
  bypass:  { name: 'OFF', color: '#64748b', glow: 'rgba(100,116,139,0.2)' }
};

class OpticalGame {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.audio = new OpticalAudio();

    this.grid = 4; // 4x4 Optical Crossbar
    this.mrrs = []; // 16 Micro-Ring Resonators
    this.photons = []; // In-flight optical pulses
    this.particles = [];

    this.selectedTune = 'lambda1';
    this.state = 'idle'; // 'idle', 'running', 'paused', 'over'
    this.score = 0;
    this.wave = 1;
    this.waveTimer = 25.0;
    this.laserSurge = 100.0;
    this.thermalDrift = 0.0; // Thermal drift in Kelvin
    this.thermalStability = 100.0;

    this.deliveredCount = 0;
    this.avgLoss = 2.4;
    this.lastTime = performance.now();

    this.initMrrs();
    this.bindEvents();
    this.loop = this.loop.bind(this);
    requestAnimationFrame(this.loop);
  }

  initMrrs() {
    this.mrrs = [];
    for (let r = 0; r < this.grid; r++) {
      for (let c = 0; c < this.grid; c++) {
        // Set diagonal to default match
        let defaultTune = 'bypass';
        if (r === c) {
          const keys = ['lambda1', 'lambda2', 'lambda3', 'lambda4'];
          defaultTune = keys[r % keys.length];
        }
        this.mrrs.push({
          r: r,
          c: c,
          tune: defaultTune,
          tempOffset: 0.0
        });
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

      if (this.state !== 'running') return;

      const mrr = this.getMrrAtPixel(mx, my);
      if (mrr) {
        // Cycle tuning: lambda1 -> lambda2 -> lambda3 -> lambda4 -> bypass
        const order = ['lambda1', 'lambda2', 'lambda3', 'lambda4', 'bypass'];
        const nextIdx = (order.indexOf(mrr.tune) + 1) % order.length;
        mrr.tune = order[nextIdx];
        this.audio.playTune();
        const pos = this.getIntersectionPixel(mrr.r, mrr.c);
        this.addTextParticle(pos.x, pos.y, WAVELENGTHS[mrr.tune].name.split(' ')[0], WAVELENGTHS[mrr.tune].color);
      }
    });

    window.addEventListener('keydown', (e) => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
      if (e.code === 'Space') {
        e.preventDefault();
        this.audio.init();
        this.activateLaserBoost();
      } else if (e.key === 'p' || e.key === 'P') {
        this.togglePause();
      }
    });
  }

  getIntersectionPixel(r, c) {
    const startX = 140;
    const startY = 90;
    const stepX = 100;
    const stepY = 85;
    return {
      x: startX + c * stepX,
      y: startY + r * stepY
    };
  }

  getMrrAtPixel(px, py) {
    for (let i = 0; i < this.mrrs.length; i++) {
      const m = this.mrrs[i];
      const pos = this.getIntersectionPixel(m.r, m.c);
      if (Math.hypot(px - pos.x, py - pos.y) <= 18) {
        return m;
      }
    }
    return null;
  }

  start() {
    this.audio.init();
    this.initMrrs();
    this.photons = [];
    this.particles = [];
    this.state = 'running';
    this.score = 0;
    this.wave = 1;
    this.waveTimer = 25.0;
    this.laserSurge = 100.0;
    this.thermalDrift = 0.0;
    this.deliveredCount = 0;

    document.getElementById('opticalOverModal').style.display = 'none';
    document.getElementById('opticalStartBtn').textContent = '🔄 Restart';
    this.updateHUD();
  }

  togglePause() {
    if (this.state === 'running') this.state = 'paused';
    else if (this.state === 'paused') this.state = 'running';
  }

  activateLaserBoost() {
    if (this.state !== 'running' || this.laserSurge < 25) return;
    this.laserSurge = Math.max(0, this.laserSurge - 30);
    this.thermalDrift = Math.max(0, this.thermalDrift - 4.5);
    this.audio.playLaserSurge();
    this.score += 50;
    this.addTextParticle(this.canvas.width / 2, 60, '⚡ LASER SURGE / DRIFT COOLED!', '#38bdf8');
    this.updateHUD();
  }

  addTextParticle(x, y, text, color) {
    this.particles.push({
      x, y, vx: 0, vy: -0.8, life: 1.0, text, color, isText: true
    });
  }

  update(dt) {
    if (this.state !== 'running') return;

    // Progress Wave & Surge recharge
    this.waveTimer -= dt;
    this.laserSurge = Math.min(100.0, this.laserSurge + dt * 8.0);
    this.thermalDrift += dt * (0.35 + this.wave * 0.1); // Gradual thermal drift
    this.thermalStability = Math.max(0, Math.min(100, 100 - (this.thermalDrift / 15.0) * 100));

    if (this.thermalStability <= 5) {
      this.triggerDropout("Thermal drift shifted micro-ring resonance beyond receiver photodetector locking range!");
      return;
    }

    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 25.0;
      this.score += 300 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 50, `WAVE ${this.wave} OPTICAL BURST!`, '#22c55e');
    }

    // Spawn optical pulses from Laser Ingress (Left side)
    const spawnRate = 0.8 + this.wave * 0.25;
    if (Math.random() < spawnRate * dt) {
      const ingressRow = Math.floor(Math.random() * this.grid);
      const targetCol = Math.floor(Math.random() * this.grid);
      const wkeys = ['lambda1', 'lambda2', 'lambda3', 'lambda4'];
      const wavelength = wkeys[targetCol % wkeys.length];

      this.photons.push({
        r: ingressRow,
        c: 0,
        x: 40,
        y: this.getIntersectionPixel(ingressRow, 0).y,
        dir: 'horizontal', // 'horizontal' or 'vertical'
        targetCol: targetCol,
        wavelength: wavelength,
        speed: 380, // pixels per second
        loss: 0.5
      });
    }

    // Move optical pulses along waveguides
    for (let i = this.photons.length - 1; i >= 0; i--) {
      const p = this.photons[i];
      if (p.dir === 'horizontal') {
        p.x += p.speed * dt;
        p.loss += dt * 1.2;

        // Check intersection with vertical waveguide
        const nextCol = Math.floor((p.x - 90) / 100);
        if (nextCol >= 0 && nextCol < this.grid) {
          const mrr = this.mrrs[p.r * this.grid + nextCol];
          const pos = this.getIntersectionPixel(p.r, nextCol);

          // If close to MRR center and wavelength matches, drop to vertical!
          if (Math.abs(p.x - pos.x) < 8 && mrr.tune === p.wavelength) {
            p.dir = 'vertical';
            p.c = nextCol;
            p.x = pos.x;
            p.y = pos.y;
            p.loss += 0.8; // Drop loss
          }
        }

        // Exited right edge uncoupled
        if (p.x > 580) {
          this.photons.splice(i, 1);
        }
      } else if (p.dir === 'vertical') {
        p.y += p.speed * dt;
        p.loss += dt * 1.2;

        // Reached bottom photodetector
        if (p.y > 410) {
          this.deliveredCount++;
          this.score += 35 * this.wave;
          this.audio.playReceive();
          const targetPos = this.getIntersectionPixel(3, p.c);
          this.addTextParticle(targetPos.x, 430, '+1 Tbps', '#4ade80');
          this.photons.splice(i, 1);
        }
      }
    }

    // Update Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const pt = this.particles[i];
      pt.y += pt.vy;
      pt.life -= dt * 1.5;
      if (pt.life <= 0) this.particles.splice(i, 1);
    }

    this.updateHUD();
  }

  triggerDropout(reason) {
    this.state = 'over';
    this.audio.playGameOver();
    document.getElementById('opticalModalTitle').textContent = 'OPTICAL LINK DROPOUT!';
    document.getElementById('opticalModalSummary').innerHTML = `
      ${reason}<br>
      High bit-error rates caused irreversible loss of packet sync across optical waveguides.
      <br><br><b>Final Wave:</b> Wave ${this.wave} | <b>Photons Received:</b> ${this.deliveredCount} | <b>Score:</b> ${this.score} pts
    `;
    document.getElementById('opticalOverModal').style.display = 'flex';
  }

  updateHUD() {
    document.getElementById('opticalScore').textContent = this.score;
    document.getElementById('opticalWave').textContent = `Wave ${this.wave}`;
    document.getElementById('opticalBandwidth').textContent = (this.deliveredCount * 0.4).toFixed(1);
    document.getElementById('opticalLoss').textContent = (2.4 + this.thermalDrift * 0.45).toFixed(1);

    // Laser surge bar
    document.getElementById('laserSurgeBar').style.width = `${Math.round(this.laserSurge)}%`;
    document.getElementById('laserSurgeText').textContent = `${Math.round(this.laserSurge)}%`;

    // Thermal Stability bar
    const tBar = document.getElementById('opticalThermalBar');
    tBar.style.width = `${Math.round(this.thermalStability)}%`;
    if (this.thermalStability < 30) {
      tBar.style.background = '#ef4444';
      document.getElementById('opticalThermalText').style.color = '#ef4444';
      document.getElementById('opticalThermalText').textContent = `${Math.round(this.thermalStability)}% (SEVERE DRIFT!)`;
    } else if (this.thermalStability < 60) {
      tBar.style.background = '#f59e0b';
      document.getElementById('opticalThermalText').style.color = '#f59e0b';
      document.getElementById('opticalThermalText').textContent = `${Math.round(this.thermalStability)}% (DRIFT DETECTED)`;
    } else {
      tBar.style.background = '#22c55e';
      document.getElementById('opticalThermalText').style.color = '#4ade80';
      document.getElementById('opticalThermalText').textContent = `${Math.round(this.thermalStability)}% (STABLE)`;
    }
  }

  draw() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 1. Draw Waveguides (4 Horizontal and 4 Vertical)
    this.ctx.lineWidth = 6;
    for (let r = 0; r < this.grid; r++) {
      const pos = this.getIntersectionPixel(r, 0);
      this.ctx.strokeStyle = '#1e293b';
      this.ctx.beginPath();
      this.ctx.moveTo(35, pos.y);
      this.ctx.lineTo(580, pos.y);
      this.ctx.stroke();

      // Core inner stripe
      this.ctx.strokeStyle = '#334155';
      this.ctx.lineWidth = 2;
      this.ctx.beginPath();
      this.ctx.moveTo(35, pos.y);
      this.ctx.lineTo(580, pos.y);
      this.ctx.stroke();
      this.ctx.lineWidth = 6;
    }

    for (let c = 0; c < this.grid; c++) {
      const pos = this.getIntersectionPixel(0, c);
      this.ctx.strokeStyle = '#1e293b';
      this.ctx.beginPath();
      this.ctx.moveTo(pos.x, 50);
      this.ctx.lineTo(pos.x, 420);
      this.ctx.stroke();

      this.ctx.strokeStyle = '#334155';
      this.ctx.lineWidth = 2;
      this.ctx.beginPath();
      this.ctx.moveTo(pos.x, 50);
      this.ctx.lineTo(pos.x, 420);
      this.ctx.stroke();
      this.ctx.lineWidth = 6;
    }

    // 2. Draw Micro-Ring Resonators at Intersections
    this.mrrs.forEach(m => {
      const pos = this.getIntersectionPixel(m.r, m.c);
      const wdef = WAVELENGTHS[m.tune];

      // Outer ring
      this.ctx.strokeStyle = wdef.color;
      this.ctx.lineWidth = m.tune !== 'bypass' ? 3.5 : 1.5;
      this.ctx.shadowColor = wdef.color;
      this.ctx.shadowBlur = m.tune !== 'bypass' ? 10 : 0;

      this.ctx.beginPath();
      this.ctx.arc(pos.x, pos.y, 14, 0, Math.PI * 2);
      this.ctx.stroke();
      this.ctx.shadowBlur = 0;

      // Center disc
      this.ctx.fillStyle = m.tune !== 'bypass' ? wdef.glow : 'rgba(30, 41, 59, 0.6)';
      this.ctx.beginPath();
      this.ctx.arc(pos.x, pos.y, 8, 0, Math.PI * 2);
      this.ctx.fill();

      // Text label
      if (m.tune !== 'bypass') {
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = 'bold 9px "JetBrains Mono", monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(m.tune.replace('lambda', 'λ'), pos.x, pos.y + 3);
      }
    });

    // 3. Draw Laser Ingress Modulators (Left) & Photodetectors (Bottom)
    for (let r = 0; r < this.grid; r++) {
      const pos = this.getIntersectionPixel(r, 0);
      this.ctx.fillStyle = '#38bdf8';
      this.ctx.fillRect(20, pos.y - 10, 18, 20);
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 9px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.fillText(`TX${r}`, 29, pos.y + 3);
    }

    for (let c = 0; c < this.grid; c++) {
      const pos = this.getIntersectionPixel(3, c);
      this.ctx.fillStyle = '#10b981';
      this.ctx.fillRect(pos.x - 10, 420, 20, 18);
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 9px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.fillText(`RX${c}`, pos.x, 433);
    }

    // 4. Draw Moving Photons
    this.photons.forEach(p => {
      const wdef = WAVELENGTHS[p.wavelength];
      this.ctx.fillStyle = wdef.color;
      this.ctx.shadowColor = wdef.color;
      this.ctx.shadowBlur = 12;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.shadowBlur = 0;
    });

    // 5. Draw Flying Particles
    this.particles.forEach(pt => {
      this.ctx.globalAlpha = Math.max(0, pt.life);
      this.ctx.fillStyle = pt.color;
      this.ctx.font = 'bold 12px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.fillText(pt.text, pt.x, pt.y);
      this.ctx.globalAlpha = 1.0;
    });

    // Idle Watermark
    if (this.state === 'idle') {
      this.ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 20px "Inter", sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.fillText('Press "Start Photon Pilot" to Play!', this.canvas.width / 2, this.canvas.height / 2 - 10);
      this.ctx.font = '13px "Inter", sans-serif';
      this.ctx.fillStyle = '#94a3b8';
      this.ctx.fillText('Tune micro-ring resonators to route laser wavelengths at the speed of light', this.canvas.width / 2, this.canvas.height / 2 + 18);
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

let opticalGame = null;
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('opticalCanvas')) {
    opticalGame = new OpticalGame('opticalCanvas');
  }
});

function startOpticalGame() {
  if (opticalGame) opticalGame.start();
}

function restartOpticalGame() {
  if (opticalGame) opticalGame.start();
}

function activateLaserBoost() {
  if (opticalGame) opticalGame.activateLaserBoost();
}

function setMrrTuning(val) {
  if (opticalGame) opticalGame.selectedTune = val;
}

function toggleOpticalSound() {
  if (!opticalGame) return;
  opticalGame.audio.enabled = !opticalGame.audio.enabled;
  document.getElementById('opticalSoundBtn').textContent = opticalGame.audio.enabled ? '🔊 Sound: ON' : '🔈 Sound: OFF';
}

function toggleOpticalPause() {
  if (opticalGame) opticalGame.togglePause();
}

function saveOpticalRecord() {
  if (!opticalGame) return;
  const name = document.getElementById("opticalCallsign").value.trim() || "Photon Pilot";
  const org = document.getElementById("opticalOrg").value.trim() || "Silicon Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const record = {
    name: name,
    org: org,
    track: `Photon Pilot (Wave ${opticalGame.wave})`,
    score: opticalGame.score,
    accuracy: Math.round(opticalGame.deliveredCount * 0.4 * 10) / 10, // Tbps achieved
    certId: `OPTICAL-WAVE-${opticalGame.wave}`,
    date: dateStr,
    type: "optical"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("opticalSaveConfirm").style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitOpticalToGithub() {
  if (!opticalGame) return;
  const name = document.getElementById("opticalCallsign").value.trim() || "Photon Pilot";
  const org = document.getElementById("opticalOrg").value.trim() || "Silicon Lab";
  const title = `[optical-highscore] ${name} — ${opticalGame.score} pts (${(opticalGame.deliveredCount * 0.4).toFixed(1)} Tbps)`;
  const body = [
    "### Photon Pilot Optical NoC High Score",
    `- **Pilot**: ${name}`,
    `- **Institution/Handle**: ${org}`,
    `- **High Score**: ${opticalGame.score} pts`,
    `- **Optical Bandwidth**: ${(opticalGame.deliveredCount * 0.4).toFixed(1)} Tbps`,
    `- **Wave Reached**: Wave ${opticalGame.wave}`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: opticalGame.score,
      bandwidth_tbps: (opticalGame.deliveredCount * 0.4).toFixed(1),
      wave: opticalGame.wave,
      type: "optical"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}
</script>
