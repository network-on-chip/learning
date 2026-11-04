# 🔥 Hotspot Hero: Silicon Thermal Defender

Welcome to **Hotspot Hero**, an interactive microarchitecture and thermal physics arcade game! Serve as the Autonomous Thermal Management Engine on an ultra-dense multicore processor. Mitigate localized thermal hotspots using Dynamic Voltage & Frequency Scaling (DVFS), task migration, and microfluidic cryo pulses before thermal runaway triggers irreversible silicon breakdown! High scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="hotspotStartBtn" class="noc-sim-btn" onclick="startHotspotGame()">▶ Start Defense</button>
    <button id="cryoPulseBtn" class="noc-sim-btn" onclick="activateCryoPulse()" style="background:#0284c7; border:none; box-shadow:0 0 12px rgba(2,132,199,0.4);">❄️ Deploy Cryo Cool (Space)</button>

    <label><b>Routing Policy:</b>
      <select id="hotspotRoutingPolicy" class="noc-sim-select" onchange="setHotspotRouting(this.value)">
        <option value="deflection">Thermal-Aware Deflection (Steer Around Hotspots)</option>
        <option value="shortest">Shortest Path (High Bandwidth / Aggravates Heat)</option>
      </select>
    </label>

    <label><b>Click Tool:</b>
      <select id="hotspotToolSelect" class="noc-sim-select" onchange="setHotspotTool(this.value)">
        <option value="dvfs">⚡ Toggle DVFS (Throttle / Normal)</option>
        <option value="migrate">🔄 Task Migration (Select Source &amp; Dest)</option>
        <option value="cryo">❄️ Target Cryo Spot</option>
      </select>
    </label>

    <button id="hotspotSoundBtn" class="noc-sim-btn secondary" onclick="toggleHotspotSound()" title="Toggle Web Audio Sound">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleHotspotPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="hotspotScore">0</span></span>
      <span style="color:#ef4444;">Peak: <span id="hotspotPeakTemp">45.0°C</span></span>
      <span style="color:#22c55e;">Wave: <span id="hotspotWave">1</span></span>
      <span style="color:#f59e0b;" id="hotspotCombo">Combo: 1x</span>
    </div>
  </div>

  <!-- Thermal HUD & Coolant Battery -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">❄️ Microfluidic Coolant Reservoir (Space):</span>
        <span id="cryoEnergyText" style="font-weight:700; color:#38bdf8;">100%</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="cryoEnergyBar" style="width:100%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#f87171;">🔥 Silicon Die Thermal Safety Margin:</span>
        <span id="dieHealthText" style="font-weight:700; color:#4ade80;">100% (Safe &lt; 85°C)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(239,68,68,0.15); border-radius:4px; overflow:hidden;">
        <div id="dieHealthBar" style="width:100%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="hotspotCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="hotspotOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div id="hotspotModalIcon" style="font-size:3rem; margin-bottom:0.35rem;">💥</div>
      <h2 id="hotspotModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">THERMAL RUNAWAY MELTDOWN!</h2>
      <p id="hotspotModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Die junction temperature exceeded 105.0°C! Subthreshold leakage current surged exponentially, causing permanent dielectric gate oxide breakdown.
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Enter Your Callsign / Name:</label>
        <input type="text" id="hotspotCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Thermal Maestro" value="Thermal Defender">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="hotspotOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Stanford / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveHotspotRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitHotspotToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartHotspotGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="hotspotSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in your browser Leaderboard!
      </div>
    </div>
  </div>

  <div id="hotspotInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">🔥 Thermal Physics &amp; Gameplay Architecture:</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>2D RC Thermal Conduction:</strong> Heat diffuses between adjacent silicon tiles according to Fourier's law: $C_{th} \frac{dT_i}{dt} = P_i - \frac{T_i - T_{amb}}{R_{conv}} + \sum \frac{T_j - T_i}{R_{inter}}$. High compute bursts generate intense dynamic power ($P_{dyn} \propto V^2 f$).</li>
      <li><strong>Thermal Runaway ($T &gt; 100^\circ\text{C}$):</strong> Subthreshold leakage increases exponentially with temperature ($P_{leak} \propto T^2 e^{\frac{-qV_{th}}{k_B T}}$). If a core sustains $\ge 105^\circ\text{C}$ for over 3.0s, permanent gate breakdown occurs!</li>
      <li><strong>DVFS Throttling (Click Core):</strong> Click any core to toggle between <strong>Standard (0.9V/2.2GHz)</strong>, <strong>Throttled (0.65V/1.2GHz - cools down fast!)</strong>, and <strong>Boost (1.2V/3.2GHz - extreme speed &amp; heat)</strong>.</li>
      <li><strong>Task Migration:</strong> Set Click Tool to "Task Migration". Click an overheating core, then click an idle neighbor to migrate heavy workloads away from hotspots!</li>
      <li><strong>Cryo Cool Burst (Spacebar):</strong> Deploys a microfluidic thermoelectric cooling blast, quenching temperature by $25^\circ\text{C}$ across the hottest cluster. Recharges as packets successfully route.</li>
      <li><strong>Thermal Deflection Routing:</strong> Steers flits around cores exceeding $80^\circ\text{C}$, preventing dynamic switching power from worsening localized hot zones.</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Hotspot Hero
class HotspotAudio {
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

  playCryo() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      // White noise buffer for ice / cryo spray whoosh
      const bufferSize = this.ctx.sampleRate * 0.3;
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.4));
      }
      const noise = this.ctx.createBufferSource();
      noise.buffer = buffer;
      const filter = this.ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(1400, now);
      filter.frequency.exponentialRampToValueAtTime(400, now + 0.3);
      const gain = this.ctx.createGain();
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
      noise.connect(filter);
      filter.connect(gain);
      gain.connect(this.ctx.destination);
      noise.start(now);
    } catch(e) {}
  }

  playThrottle() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440, now);
      osc.frequency.linearRampToValueAtTime(330, now + 0.08);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.09);
    } catch(e) {}
  }

  playMigrate() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(350, now);
      osc.frequency.exponentialRampToValueAtTime(700, now + 0.12);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.14);
    } catch(e) {}
  }

  playAlarm() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(650, now);
      osc.frequency.linearRampToValueAtTime(850, now + 0.12);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.15);
    } catch(e) {}
  }

  playMeltdown() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(140, now);
      osc.frequency.exponentialRampToValueAtTime(35, now + 0.7);
      gain.gain.setValueAtTime(0.3, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.75);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.75);
    } catch(e) {}
  }

  playVictory() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const notes = [523.25, 659.25, 783.99, 1046.5]; // C5, E5, G5, C6
      notes.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + idx * 0.08);
        gain.gain.setValueAtTime(0.12, now + idx * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.16);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now + idx * 0.08);
        osc.stop(now + idx * 0.08 + 0.16);
      });
    } catch(e) {}
  }
}

class HotspotGame {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.audio = new HotspotAudio();
    
    this.gridSize = 4; // 4x4 Tiles
    this.tiles = [];
    this.packets = [];
    this.particles = [];
    
    this.state = 'idle'; // 'idle', 'running', 'paused', 'over', 'victory'
    this.score = 0;
    this.wave = 1;
    this.waveTimer = 25.0; // seconds per wave
    this.cryoEnergy = 100.0;
    this.maxCryo = 100.0;
    this.routingPolicy = 'deflection';
    this.selectedTool = 'dvfs';
    this.migrationSource = null;
    
    this.peakTemp = 45.0;
    this.lastAlarmTime = 0;
    this.lastTime = performance.now();
    
    this.initGrid();
    this.bindEvents();
    this.loop = this.loop.bind(this);
    requestAnimationFrame(this.loop);
  }

  initGrid() {
    this.tiles = [];
    const coreTypes = ['NPU', 'CPU', 'GPU', 'MEM'];
    for (let y = 0; y < this.gridSize; y++) {
      for (let x = 0; x < this.gridSize; x++) {
        const typeIndex = (x + y * 2) % coreTypes.length;
        this.tiles.push({
          x: x,
          y: y,
          type: coreTypes[typeIndex],
          temp: 45.0, // Ambient base temperature
          power: 1.0, // Base power
          dvfs: 'normal', // 'normal', 'throttled', 'boost'
          freq: 2.2, // GHz
          voltage: 0.9, // V
          load: 0.15, // Workload fraction
          meltdownTimer: 0.0, // seconds at >= 105C
          hotspot: false
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

      const tile = this.getTileAtPixel(mx, my);
      if (!tile || this.state !== 'running') return;

      if (this.selectedTool === 'dvfs') {
        if (tile.dvfs === 'normal') {
          tile.dvfs = 'throttled';
          tile.freq = 1.2;
          tile.voltage = 0.65;
        } else if (tile.dvfs === 'throttled') {
          tile.dvfs = 'boost';
          tile.freq = 3.2;
          tile.voltage = 1.2;
        } else {
          tile.dvfs = 'normal';
          tile.freq = 2.2;
          tile.voltage = 0.9;
        }
        this.audio.playThrottle();
        this.addTextParticle(mx, my, tile.dvfs.toUpperCase(), '#38bdf8');
      } else if (this.selectedTool === 'migrate') {
        if (!this.migrationSource) {
          this.migrationSource = tile;
          this.addTextParticle(mx, my, 'SRC SELECTED', '#f59e0b');
        } else {
          if (this.migrationSource !== tile) {
            // Migrate load
            const transferred = this.migrationSource.load * 0.65;
            this.migrationSource.load -= transferred;
            tile.load += transferred;
            this.audio.playMigrate();
            this.addTextParticle(mx, my, 'LOAD MIGRATED!', '#22c55e');
            this.score += 75;
          }
          this.migrationSource = null;
        }
      } else if (this.selectedTool === 'cryo') {
        this.applyCryoToTile(tile);
      }
    });

    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space') {
        e.preventDefault();
        this.audio.init();
        this.activateCryoPulse();
      } else if (e.key === 'p' || e.key === 'P') {
        this.togglePause();
      } else if (e.key === 'r' || e.key === 'R') {
        this.start();
      }
    });
  }

  getTileAtPixel(px, py) {
    const pad = 40;
    const cw = (this.canvas.width - pad * 2) / this.gridSize;
    const ch = (this.canvas.height - pad * 2) / this.gridSize;
    const x = Math.floor((px - pad) / cw);
    const y = Math.floor((py - pad) / ch);
    if (x >= 0 && x < this.gridSize && y >= 0 && y < this.gridSize) {
      return this.tiles[y * this.gridSize + x];
    }
    return null;
  }

  getTilePixelCenter(x, y) {
    const pad = 40;
    const cw = (this.canvas.width - pad * 2) / this.gridSize;
    const ch = (this.canvas.height - pad * 2) / this.gridSize;
    return {
      x: pad + x * cw + cw / 2,
      y: pad + y * ch + ch / 2,
      w: cw,
      h: ch
    };
  }

  start() {
    this.audio.init();
    this.initGrid();
    this.packets = [];
    this.particles = [];
    this.state = 'running';
    this.score = 0;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.cryoEnergy = 100.0;
    this.peakTemp = 45.0;
    this.migrationSource = null;

    document.getElementById('hotspotOverModal').style.display = 'none';
    document.getElementById('hotspotStartBtn').textContent = '🔄 Restart';
    this.updateHUD();
  }

  togglePause() {
    if (this.state === 'running') this.state = 'paused';
    else if (this.state === 'paused') this.state = 'running';
  }

  activateCryoPulse() {
    if (this.state !== 'running' || this.cryoEnergy < 25) return;
    this.cryoEnergy = Math.max(0, this.cryoEnergy - 30);
    this.audio.playCryo();

    // Find hottest tile cluster
    let hottest = this.tiles[0];
    this.tiles.forEach(t => { if (t.temp > hottest.temp) hottest = t; });
    this.applyCryoToTile(hottest, true);
  }

  applyCryoToTile(tile, isBurst = false) {
    tile.temp = Math.max(42.0, tile.temp - (isBurst ? 28.0 : 18.0));
    tile.meltdownTimer = 0.0;
    const pos = this.getTilePixelCenter(tile.x, tile.y);

    // Spawn cryo frost particles
    for (let i = 0; i < 24; i++) {
      const ang = Math.random() * Math.PI * 2;
      const spd = Math.random() * 3 + 1;
      this.particles.push({
        x: pos.x,
        y: pos.y,
        vx: Math.cos(ang) * spd,
        vy: Math.sin(ang) * spd,
        life: 1.0,
        color: '#38bdf8',
        size: Math.random() * 4 + 2
      });
    }
    this.addTextParticle(pos.x, pos.y, '-28°C CRYO!', '#38bdf8');
    this.score += 50;
    this.updateHUD();
  }

  addTextParticle(x, y, text, color) {
    this.particles.push({
      x: x,
      y: y,
      vx: 0,
      vy: -0.8,
      life: 1.0,
      text: text,
      color: color,
      isText: true
    });
  }

  update(dt) {
    if (this.state !== 'running') return;

    // 1. Progress Wave & recharge cryo
    this.waveTimer -= dt;
    this.cryoEnergy = Math.min(this.maxCryo, this.cryoEnergy + dt * 6.5);

    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 22.0 + this.wave * 2.0;
      this.audio.playVictory();
      this.score += 200 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 70, `WAVE ${this.wave} ADVANCE!`, '#22c55e');
    }

    // 2. Spawn Traffic Flits
    const spawnChance = (0.2 + this.wave * 0.08) * dt;
    if (Math.random() < spawnChance) {
      const srcIdx = Math.floor(Math.random() * this.tiles.length);
      let dstIdx = Math.floor(Math.random() * this.tiles.length);
      while (dstIdx === srcIdx) dstIdx = Math.floor(Math.random() * this.tiles.length);
      
      const src = this.tiles[srcIdx];
      const dst = this.tiles[dstIdx];
      src.load = Math.min(1.0, src.load + 0.12);

      this.packets.push({
        cx: src.x,
        cy: src.y,
        dx: dst.x,
        dy: dst.y,
        progress: 0.0,
        color: '#f59e0b'
      });
    }

    // 3. Move Flits along Routers
    for (let i = this.packets.length - 1; i >= 0; i--) {
      const p = this.packets[i];
      p.progress += dt * 1.8;
      if (p.progress >= 1.0) {
        p.progress = 0.0;
        // Determine next hop based on policy
        let nextX = p.cx;
        let nextY = p.cy;

        if (this.routingPolicy === 'deflection') {
          // Check if candidate XY is hot
          let candX = p.cx + Math.sign(p.dx - p.cx);
          let candY = p.cy + Math.sign(p.dy - p.cy);
          let hotX = false;
          let hotY = false;

          if (candX !== p.cx) {
            const tX = this.tiles[p.cy * this.gridSize + candX];
            if (tX && tX.temp > 82.0) hotX = true;
          }
          if (candY !== p.cy) {
            const tY = this.tiles[candY * this.gridSize + p.cx];
            if (tY && tY.temp > 82.0) hotY = true;
          }

          if (candX !== p.cx && !hotX) {
            nextX = candX;
          } else if (candY !== p.cy && !hotY) {
            nextY = candY;
          } else if (candX !== p.cx) {
            nextX = candX;
          } else if (candY !== p.cy) {
            nextY = candY;
          }
        } else {
          // Strict Dimension-Order XY
          if (p.cx !== p.dx) nextX = p.cx + Math.sign(p.dx - p.cx);
          else if (p.cy !== p.dy) nextY = p.cy + Math.sign(p.dy - p.cy);
        }

        p.cx = nextX;
        p.cy = nextY;

        // Dynamic dissipation at intermediate router
        const curTile = this.tiles[p.cy * this.gridSize + p.cx];
        curTile.temp += 0.15;

        if (p.cx === p.dx && p.cy === p.dy) {
          this.packets.splice(i, 1);
          this.score += 15;
          this.cryoEnergy = Math.min(this.maxCryo, this.cryoEnergy + 1.2);
        }
      }
    }

    // 4. Heat Generation & 2D Thermal Diffusion
    const ambient = 45.0;
    const condRate = 0.22; // Conductance between neighboring silicon tiles
    const convRate = 0.18; // Convective dissipation to heat spreader
    const tempsCopy = this.tiles.map(t => t.temp);

    let maxT = 45.0;
    let criticalCount = 0;

    for (let idx = 0; idx < this.tiles.length; idx++) {
      const tile = this.tiles[idx];
      // Dynamic power: P = C * V^2 * f * load
      const v = tile.voltage;
      const f = tile.freq;
      const dynPower = (v * v) * f * (0.8 + tile.load * 1.5) * (1.0 + this.wave * 0.15);
      
      // Leakage power: exponential with temperature
      const leakPower = 0.08 * Math.exp(Math.max(0, (tempsCopy[idx] - 70) * 0.055));
      const totalGen = (dynPower + leakPower) * 1.8;

      // Conduction with 4 orthogonal neighbors
      let neighborDiff = 0;
      const x = tile.x;
      const y = tile.y;
      const neighbors = [
        y > 0 ? (y - 1) * this.gridSize + x : null,
        y < this.gridSize - 1 ? (y + 1) * this.gridSize + x : null,
        x > 0 ? y * this.gridSize + (x - 1) : null,
        x < this.gridSize - 1 ? y * this.gridSize + (x + 1) : null
      ];

      neighbors.forEach(nIdx => {
        if (nIdx !== null) {
          neighborDiff += (tempsCopy[nIdx] - tempsCopy[idx]) * condRate;
        }
      });

      // Ambient dissipation
      const ambLoss = (tempsCopy[idx] - ambient) * convRate;

      // Integrate temp
      tile.temp += (totalGen + neighborDiff - ambLoss) * dt * 3.5;
      if (tile.temp < ambient) tile.temp = ambient;

      // Natural load decay
      tile.load = Math.max(0.1, tile.load - dt * 0.12);

      if (tile.temp > maxT) maxT = tile.temp;

      // Alarm / Warning
      if (tile.temp >= 85.0) {
        criticalCount++;
        tile.hotspot = true;
      } else {
        tile.hotspot = false;
      }

      // Meltdown Countdown
      if (tile.temp >= 105.0) {
        tile.meltdownTimer += dt;
        if (tile.meltdownTimer >= 3.0) {
          this.triggerMeltdown(tile);
          return;
        }
      } else {
        tile.meltdownTimer = Math.max(0, tile.meltdownTimer - dt * 1.5);
      }
    }

    this.peakTemp = maxT;

    // Siren audio when hot
    const now = performance.now();
    if (criticalCount > 0 && now - this.lastAlarmTime > 750) {
      this.audio.playAlarm();
      this.lastAlarmTime = now;
    }

    // 5. Update Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const pt = this.particles[i];
      pt.x += pt.vx;
      pt.y += pt.vy;
      pt.life -= dt * (pt.isText ? 0.9 : 1.8);
      if (pt.life <= 0) this.particles.splice(i, 1);
    }

    this.score += Math.floor(dt * 10 * this.wave);
    this.updateHUD();
  }

  triggerMeltdown(tile) {
    this.state = 'over';
    this.audio.playMeltdown();
    document.getElementById('hotspotModalIcon').textContent = '💥';
    document.getElementById('hotspotModalTitle').textContent = 'THERMAL RUNAWAY MELTDOWN!';
    document.getElementById('hotspotModalTitle').style.color = '#f87171';
    document.getElementById('hotspotModalSummary').innerHTML = `
      Core <b>(${tile.x}, ${tile.y})</b> reached <b>${tile.temp.toFixed(1)}°C</b> for over 3 seconds!<br>
      Exponential subthreshold leakage provoked localized gate oxide perforation.
      <br><br><b>Final Wave:</b> Wave ${this.wave} | <b>Final Score:</b> ${this.score} pts
    `;
    document.getElementById('hotspotOverModal').style.display = 'flex';
  }

  updateHUD() {
    document.getElementById('hotspotScore').textContent = this.score;
    document.getElementById('hotspotWave').textContent = this.wave;
    
    const peakEl = document.getElementById('hotspotPeakTemp');
    peakEl.textContent = `${this.peakTemp.toFixed(1)}°C`;
    if (this.peakTemp >= 100.0) peakEl.style.color = '#ef4444';
    else if (this.peakTemp >= 85.0) peakEl.style.color = '#f59e0b';
    else peakEl.style.color = '#22c55e';

    // Battery Bar
    const energyPct = Math.max(0, Math.min(100, (this.cryoEnergy / this.maxCryo) * 100));
    document.getElementById('cryoEnergyBar').style.width = `${energyPct}%`;
    document.getElementById('cryoEnergyText').textContent = `${Math.round(energyPct)}%`;

    // Health Bar based on peak temp (45C -> 100%, 105C -> 0%)
    const healthPct = Math.max(0, Math.min(100, 100 - ((this.peakTemp - 45.0) / (105.0 - 45.0)) * 100));
    const hBar = document.getElementById('dieHealthBar');
    hBar.style.width = `${healthPct}%`;
    if (healthPct < 30) {
      hBar.style.background = '#ef4444';
      document.getElementById('dieHealthText').style.color = '#ef4444';
      document.getElementById('dieHealthText').textContent = `${Math.round(healthPct)}% (CRITICAL DANGER!)`;
    } else if (healthPct < 60) {
      hBar.style.background = '#f59e0b';
      document.getElementById('dieHealthText').style.color = '#f59e0b';
      document.getElementById('dieHealthText').textContent = `${Math.round(healthPct)}% (ELEVATED HEAT)`;
    } else {
      hBar.style.background = '#22c55e';
      document.getElementById('dieHealthText').style.color = '#4ade80';
      document.getElementById('dieHealthText').textContent = `${Math.round(healthPct)}% (NOMINAL)`;
    }
  }

  draw() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 1. Draw Silicon Substrate & Interconnect Mesh
    const pad = 40;
    const cw = (this.canvas.width - pad * 2) / this.gridSize;
    const ch = (this.canvas.height - pad * 2) / this.gridSize;

    // Draw mesh bus lines
    this.ctx.strokeStyle = '#334155';
    this.ctx.lineWidth = 3;
    for (let i = 0; i < this.gridSize; i++) {
      const yPos = pad + i * ch + ch / 2;
      this.ctx.beginPath();
      this.ctx.moveTo(pad + cw / 2, yPos);
      this.ctx.lineTo(this.canvas.width - pad - cw / 2, yPos);
      this.ctx.stroke();

      const xPos = pad + i * cw + cw / 2;
      this.ctx.beginPath();
      this.ctx.moveTo(xPos, pad + ch / 2);
      this.ctx.lineTo(xPos, this.canvas.height - pad - ch / 2);
      this.ctx.stroke();
    }

    // 2. Draw Tiles with Thermal Heat Radiance
    this.tiles.forEach(tile => {
      const pos = this.getTilePixelCenter(tile.x, tile.y);
      const w = pos.w - 14;
      const h = pos.h - 14;
      const left = pos.x - w / 2;
      const top = pos.y - h / 2;

      // Color mapping from temp
      // 45C: #1e293b (cool dark blue) -> 75C: #d97706 (amber) -> 95C: #dc2626 (crimson) -> 105C: #ffffff (white hot)
      let r = 30, g = 41, b = 59;
      if (tile.temp < 75.0) {
        const factor = (tile.temp - 45.0) / 30.0;
        r = Math.floor(30 + factor * (217 - 30));
        g = Math.floor(41 + factor * (119 - 41));
        b = Math.floor(59 + factor * (6 - 59));
      } else if (tile.temp < 100.0) {
        const factor = (tile.temp - 75.0) / 25.0;
        r = Math.floor(217 + factor * (239 - 217));
        g = Math.floor(119 + factor * (35 - 119));
        b = Math.floor(6 + factor * (35 - 6));
      } else {
        const factor = Math.min(1.0, (tile.temp - 100.0) / 5.0);
        r = Math.floor(239 + factor * (255 - 239));
        g = Math.floor(35 + factor * (255 - 35));
        b = Math.floor(35 + factor * (255 - 35));
      }

      // Outer Heat Radiation Glow
      if (tile.temp > 65.0) {
        const glow = this.ctx.createRadialGradient(pos.x, pos.y, 10, pos.x, pos.y, pos.w * 0.85);
        glow.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${Math.min(0.7, (tile.temp - 60) / 50)})`);
        glow.addColorStop(1, 'rgba(0, 0, 0, 0)');
        this.ctx.fillStyle = glow;
        this.ctx.fillRect(pos.x - pos.w, pos.y - pos.h, pos.w * 2, pos.h * 2);
      }

      // Tile Body Box
      this.ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
      this.ctx.beginPath();
      this.ctx.roundRect(left, top, w, h, 8);
      this.ctx.fill();

      // Border with DVFS indication
      if (tile === this.migrationSource) {
        this.ctx.strokeStyle = '#f59e0b';
        this.ctx.lineWidth = 3;
      } else if (tile.temp >= 105.0) {
        this.ctx.strokeStyle = '#ffffff';
        this.ctx.lineWidth = 3.5;
      } else if (tile.temp >= 85.0) {
        this.ctx.strokeStyle = '#ef4444';
        this.ctx.lineWidth = 2.5;
      } else if (tile.dvfs === 'throttled') {
        this.ctx.strokeStyle = '#38bdf8';
        this.ctx.lineWidth = 2;
      } else if (tile.dvfs === 'boost') {
        this.ctx.strokeStyle = '#ec4899';
        this.ctx.lineWidth = 2;
      } else {
        this.ctx.strokeStyle = '#475569';
        this.ctx.lineWidth = 1.5;
      }
      this.ctx.stroke();

      // Label & Microarchitecture Info
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 12px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.fillText(`${tile.type} [${tile.x},${tile.y}]`, pos.x, pos.y - 12);

      // Temperature display
      this.ctx.font = 'bold 13px "JetBrains Mono", monospace';
      this.ctx.fillStyle = tile.temp >= 85.0 ? '#fee2e2' : '#f8fafc';
      this.ctx.fillText(`${tile.temp.toFixed(1)}°C`, pos.x, pos.y + 6);

      // DVFS & Frequency indicator
      this.ctx.font = '10px "Inter", sans-serif';
      let dvfsText = `${tile.freq}GHz (${tile.dvfs.charAt(0).toUpperCase()})`;
      if (tile.meltdownTimer > 0) {
        dvfsText = `🔥 MELT: ${(3.0 - tile.meltdownTimer).toFixed(1)}s`;
        this.ctx.fillStyle = '#ffffff';
      } else {
        this.ctx.fillStyle = tile.dvfs === 'throttled' ? '#7dd3fc' : (tile.dvfs === 'boost' ? '#f472b6' : '#cbd5e1');
      }
      this.ctx.fillText(dvfsText, pos.x, pos.y + 22);
    });

    // 3. Draw In-Flight Flits
    this.packets.forEach(p => {
      const srcPos = this.getTilePixelCenter(p.cx, p.cy);
      let curX = srcPos.x;
      let curY = srcPos.y;

      this.ctx.fillStyle = p.color;
      this.ctx.shadowColor = p.color;
      this.ctx.shadowBlur = 8;
      this.ctx.beginPath();
      this.ctx.arc(curX, curY, 5, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.shadowBlur = 0;
    });

    // 4. Draw Particles & Flying Text
    this.particles.forEach(pt => {
      this.ctx.globalAlpha = Math.max(0, pt.life);
      if (pt.isText) {
        this.ctx.fillStyle = pt.color;
        this.ctx.font = 'bold 12px "JetBrains Mono", monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(pt.text, pt.x, pt.y);
      } else {
        this.ctx.fillStyle = pt.color;
        this.ctx.beginPath();
        this.ctx.arc(pt.x, pt.y, pt.size, 0, Math.PI * 2);
        this.ctx.fill();
      }
      this.ctx.globalAlpha = 1.0;
    });

    // Idle Watermark if not started
    if (this.state === 'idle') {
      this.ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 20px "Inter", sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.fillText('Press "Start Defense" to Play!', this.canvas.width / 2, this.canvas.height / 2 - 10);
      this.ctx.font = '13px "Inter", sans-serif';
      this.ctx.fillStyle = '#94a3b8';
      this.ctx.fillText('Prevent thermal runaway on a 4x4 multicore chip using DVFS & Cryo Cool', this.canvas.width / 2, this.canvas.height / 2 + 18);
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

let hotspotGame = null;
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('hotspotCanvas')) {
    hotspotGame = new HotspotGame('hotspotCanvas');
  }
});

function startHotspotGame() {
  if (hotspotGame) hotspotGame.start();
}

function restartHotspotGame() {
  if (hotspotGame) hotspotGame.start();
}

function activateCryoPulse() {
  if (hotspotGame) hotspotGame.activateCryoPulse();
}

function toggleHotspotSound() {
  if (!hotspotGame) return;
  hotspotGame.audio.enabled = !hotspotGame.audio.enabled;
  document.getElementById('hotspotSoundBtn').textContent = hotspotGame.audio.enabled ? '🔊 Sound: ON' : '🔈 Sound: OFF';
}

function toggleHotspotPause() {
  if (hotspotGame) hotspotGame.togglePause();
}

function setHotspotRouting(pol) {
  if (hotspotGame) hotspotGame.routingPolicy = pol;
}

function setHotspotTool(tool) {
  if (hotspotGame) {
    hotspotGame.selectedTool = tool;
    hotspotGame.migrationSource = null;
  }
}

function saveHotspotRecord() {
  if (!hotspotGame) return;
  const name = document.getElementById("hotspotCallsign").value.trim() || "Thermal Defender";
  const org = document.getElementById("hotspotOrg").value.trim() || "Silicon Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const record = {
    name: name,
    org: org,
    track: `Hotspot Hero (Wave ${hotspotGame.wave})`,
    score: hotspotGame.score,
    accuracy: Math.round(hotspotGame.peakTemp), // Peak temp reached
    certId: `HOTSPOT-WAVE-${hotspotGame.wave}`,
    date: dateStr,
    type: "hotspot"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("hotspotSaveConfirm").style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitHotspotToGithub() {
  if (!hotspotGame) return;
  const name = document.getElementById("hotspotCallsign").value.trim() || "Thermal Defender";
  const org = document.getElementById("hotspotOrg").value.trim() || "Silicon Lab";
  const title = `[hotspot-highscore] ${name} — ${hotspotGame.score} pts (Wave ${hotspotGame.wave})`;
  const body = [
    "### Hotspot Hero Silicon Thermal Defense High Score",
    `- **Player**: ${name}`,
    `- **Institution/Handle**: ${org}`,
    `- **High Score**: ${hotspotGame.score} pts`,
    `- **Wave Reached**: Wave ${hotspotGame.wave}`,
    `- **Peak Temp Managed**: ${hotspotGame.peakTemp.toFixed(1)}°C`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: hotspotGame.score,
      wave: hotspotGame.wave,
      peakTemp: hotspotGame.peakTemp.toFixed(1),
      type: "hotspot"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}
</script>
