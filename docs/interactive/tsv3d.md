# 🏢 TSV Titan: 3D-NoC & Thermal Stacking Architect

Design, route, and cool high-density Three-Dimensional Networks-on-Chip (3D-NoCs)! Step into the role of a 3D Silicon Architect: place Through-Silicon Vias (TSVs) across multi-tier vertical silicon stacks (Compute, Cache, HBM DRAM, Photonic), balance thermo-mechanical Keep-Out Zone (KOZ) transistor exclusion areas, route vertical flits without circular credit deadlock, and defeat the vertical thermal stacking crisis by inserting thermal dummy TSVs to sink heat from trapped lower tiers! High scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="tsvStartBtn" class="noc-sim-btn" onclick="startTSVSimulation()">▶ Start 3D Architect</button>
    <button id="tsvModeBtn" class="noc-sim-btn" onclick="toggleTSVMode()" style="background:#ea580c; border:none; box-shadow:0 0 12px rgba(234,88,12,0.4);">🔄 Mode: 3D Routing &amp; Tiers</button>
    <button id="tsvThermalBoostBtn" class="noc-sim-btn" onclick="deployThermalTSVs()" style="background:#0284c7; border:none;">❄️ Add Thermal TSVs (Space)</button>

    <label><b>3D Tier Count:</b>
      <select id="tsvTierSelect" class="noc-sim-select" onchange="updateTSVConfig()">
        <option value="2">2 Tiers (Logic + SRAM)</option>
        <option value="3" selected>3 Tiers (Logic + SRAM + HBM)</option>
        <option value="4">4 Tiers (Logic + 3D Cache + 2x DRAM)</option>
        <option value="5">5 Tiers (Hetero Compute + RF + 3D Memory)</option>
      </select>
    </label>

    <label><b>3D Routing Algorithm:</b>
      <select id="tsvRoutingSelect" class="noc-sim-select" onchange="updateTSVRouting(this.value)">
        <option value="zxy">Dimension-Order Z-X-Y (Vertical-First / Deadlock-Free)</option>
        <option value="xyz">Dimension-Order X-Y-Z (Horizontal-First / Deadlock-Free)</option>
        <option value="elevator">Elevator Routing (Sparse TSV Pillars with Deflection)</option>
      </select>
    </label>

    <button id="tsvSoundBtn" class="noc-sim-btn secondary" onclick="toggleTSVSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleTSVPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="tsvScore">0</span></span>
      <span style="color:#ef4444;">Peak Temp: <span id="tsvPeakTemp">72.4°C</span></span>
      <span style="color:#22c55e;">KOZ Area: <span id="tsvKozDisp">4.8%</span></span>
      <span style="color:#f59e0b;" id="tsvWave">Wave 1</span>
    </div>
  </div>

  <!-- Live 3D Silicon & TSV Physical HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">🏢 Vertical TSV Latency &amp; RC:</span>
        <span id="tsvRcText" style="font-weight:700; color:#38bdf8;">15 ps (25 fF, 28 mΩ)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="tsvRcBar" style="width:25%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#f87171;">🔥 Thermal Stacking Trap (Middle Tier):</span>
        <span id="tsvThermalText" style="font-weight:700; color:#f87171;">Tier 1: 82.1°C (ILD Trap)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(239,68,68,0.15); border-radius:4px; overflow:hidden;">
        <div id="tsvThermalBar" style="width:78%; height:100%; background:#ef4444; transition:width 0.2s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#22c55e;">❄️ Thermal TSV Conduits:</span>
        <span id="tsvDummyText" style="font-weight:700; color:#22c55e;">16 Conduits (-14.2°C)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(34,197,94,0.15); border-radius:4px; overflow:hidden;">
        <div id="tsvDummyBar" style="width:50%; height:100%; background:#22c55e; transition:width 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="tsvCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Modal for 3D Challenges / Results -->
    <div id="tsvModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="tsvModalIcon">🏢</div>
      <h2 id="tsvModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#4ade80;">3D ARCHITECTURE VERIFIED!</h2>
      <p id="tsvModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Successfully routed 3D vertical traffic across 3 silicon tiers while suppressing thermal stacking hotspots below 85.0°C!
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">3D Silicon Architect Callsign:</label>
        <input type="text" id="tsvCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. 3D Titan" value="TSV Architect">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="tsvOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Intel 3DFab / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveTSVRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitTSVToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartTSVGame()" style="color:#ffffff !important;">🔄 Run Again</button>
      </div>
      <div id="tsvSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in your browser Leaderboard!
      </div>
    </div>
  </div>

  <div id="tsvInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">🏢 3D-NoC &amp; TSV Physics Principles (Chapter 8 Foundations):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Vertical Link Asymmetry:</strong> A vertical TSV link has tiny electrical transit delay ($\approx 15\text{–}30\text{ ps}$, $C_{tsv} \approx 25\text{ fF}$) compared to long horizontal wires ($\approx 150\text{ ps}$). A 3D mesh router adds a 7th port (Up/Down), drastically cutting average hop diameter from $O(\sqrt{N})$ to $O(\sqrt[3]{N})$.</li>
      <li><strong>Keep-Out Zone (KOZ) Silicon Overhead:</strong> Copper TSVs ($\text{CTE} \approx 17\times 10^{-6}/\text{K}$) expand $6\times$ more than silicon ($\text{CTE} \approx 2.6\times 10^{-6}/\text{K}$), creating thermo-mechanical radial stress fields ($\sigma_r \propto 1/r^2$). To prevent piezoresistive carrier mobility shifts, transistors must be excluded within a Keep-Out Zone ($r_{koz} \approx 3\text{–}5\,\mu\text{m}$), consuming valuable active silicon area!</li>
      <li><strong>The 3D Thermal Stacking Trap:</strong> In 3D-stacked silicon, heat generated in bottom and middle active tiers must travel through low-conductivity dielectric bonding layers ($k_{ILD} \approx 1.2\text{ W/m}\cdot\text{K}$ vs $k_{Si} \approx 140\text{ W/m}\cdot\text{K}$). Without thermal conduits, middle tiers reach critical runaway ($&gt; 95^\circ\text{C}$)!</li>
      <li><strong>Thermal Dummy TSVs:</strong> Strategic insertion of dummy copper TSVs ($k_{Cu} \approx 400\text{ W/m}\cdot\text{K}$) acts as vertical thermal superhighways, conducting heat directly away from hotspot clusters down to the heat sink.</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for TSV Titan
class TSVAudio {
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

  playElevator() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(320, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(960, this.ctx.currentTime + 0.18);
    gain.gain.setValueAtTime(0.18, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.18);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.18);
  }

  playCool() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(800, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(400, this.ctx.currentTime + 0.25);
    gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.25);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.25);
  }

  playWarning() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(220, this.ctx.currentTime);
    osc.frequency.setValueAtTime(180, this.ctx.currentTime + 0.1);
    gain.gain.setValueAtTime(0.25, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.25);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.25);
  }
}

// Main 3D-NoC Simulation Engine
class TSVSimulator {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.audio = new TSVAudio();

    this.mode = 'isometric_3d'; // 'isometric_3d' or 'thermal_stack'
    this.numTiers = 3;
    this.routingAlgo = 'zxy'; // 'zxy', 'xyz', 'elevator'
    this.tsvPitchUm = 10; // um
    this.tsvDiamUm = 4; // um
    this.tsvHeightUm = 40; // um
    this.dummyTsvCount = 16;

    // Physical metrics
    this.rTsv = 0.028; // ohm
    this.cTsv = 25.0; // fF
    this.kozPercent = 4.8;
    this.peakTemp = 74.2;
    this.tierTemps = [52.0, 78.4, 64.0, 58.0, 55.0];

    // Packets traveling through 3D stack
    this.packets3d = [];
    this.particles = [];
    this.score = 0;
    this.wave = 1;
    this.isPaused = false;
    this.running = false;
    this.animId = null;

    this.computePhysics();
    this.setupListeners();
  }

  setupListeners() {
    this.canvas.addEventListener('click', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left) * (this.canvas.width / rect.width);
      const y = (e.clientY - rect.top) * (this.canvas.height / rect.height);
      this.handleClick(x, y);
    });

    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space' && !e.target.matches('input, select, textarea')) {
        e.preventDefault();
        this.addThermalConduits();
      }
    });
  }

  computePhysics() {
    // Electrical TSV models
    const rhoCu = 1.7e-8; // ohm-m
    const r_radius = (this.tsvDiamUm * 1e-6) / 2;
    const height_m = this.tsvHeightUm * 1e-6;
    const area_m2 = Math.PI * r_radius * r_radius;
    this.rTsv = (rhoCu * height_m) / area_m2; // Ohms (~20-40 mOhm)

    // Liner capacitance (SiO2 liner ~ 100nm)
    const tox_m = 100e-9;
    const epsOx = 3.9 * 8.854e-12;
    this.cTsv = ((2 * Math.PI * epsOx * height_m) / Math.log((r_radius + tox_m) / r_radius)) * 1e15; // fF

    // KOZ calculation
    const kozRadiusUm = this.tsvDiamUm * 2.2;
    const kozAreaUm2 = Math.PI * Math.pow(kozRadiusUm, 2);
    const tileAreaUm2 = 10000; // 100x100 um tile
    this.kozPercent = Math.min(25, (kozAreaUm2 / tileAreaUm2) * 100);

    // Thermal stack calculation
    // Heat sink is mounted at Tier 0 (bottom).
    // Higher active tiers have trapped heat via ILD layers.
    const baseTemp = 45.0;
    const kILD = 1.2; // W/mK
    const kSi = 140.0;
    const kCu = 400.0;

    const dummyCooling = this.dummyTsvCount * 0.9;
    this.tierTemps = [];
    for (let t = 0; t < this.numTiers; t++) {
      let t_temp = baseTemp + (t === 0 ? 10 : 25 + t * 14);
      // Middle tiers suffer worst ILD bottleneck
      if (t === 1 && this.numTiers >= 3) t_temp += 12;
      t_temp -= dummyCooling * (t / this.numTiers);
      this.tierTemps.push(Math.max(45, t_temp));
    }
    this.peakTemp = Math.max(...this.tierTemps);

    this.updateHUD();
  }

  updateHUD() {
    document.getElementById('tsvRcText').textContent = `${(this.rTsv * 1000).toFixed(0)} mΩ, ${this.cTsv.toFixed(1)} fF`;
    document.getElementById('tsvRcBar').style.width = `${Math.min(100, (this.cTsv / 60) * 100)}%`;

    document.getElementById('tsvPeakTemp').textContent = `${this.peakTemp.toFixed(1)}°C`;
    document.getElementById('tsvThermalText').textContent = `Peak: ${this.peakTemp.toFixed(1)}°C (Tier ${this.tierTemps.indexOf(this.peakTemp)})`;
    document.getElementById('tsvThermalBar').style.width = `${Math.min(100, ((this.peakTemp - 40) / 60) * 100)}%`;
    if (this.peakTemp > 85) {
      document.getElementById('tsvThermalBar').style.background = '#ef4444';
    } else {
      document.getElementById('tsvThermalBar').style.background = '#22c55e';
    }

    document.getElementById('tsvKozDisp').textContent = `${this.kozPercent.toFixed(1)}%`;
    document.getElementById('tsvDummyText').textContent = `${this.dummyTsvCount} Conduits (-${(this.dummyTsvCount * 0.9).toFixed(1)}°C)`;
    document.getElementById('tsvDummyBar').style.width = `${Math.min(100, (this.dummyTsvCount / 32) * 100)}%`;

    document.getElementById('tsvScore').textContent = this.score;
  }

  addThermalConduits() {
    this.dummyTsvCount = Math.min(32, this.dummyTsvCount + 4);
    this.audio.playCool();
    this.addFloatingText(310, 200, `❄️ +4 THERMAL TSVs (Cooling Activated!)`, '#38bdf8');
    this.score += 75;
    this.computePhysics();
  }

  handleClick(x, y) {
    // Click on canvas to inject vertical 3D flit or place TSVs
    const srcTier = Math.floor(Math.random() * this.numTiers);
    let dstTier = Math.floor(Math.random() * this.numTiers);
    while (dstTier === srcTier && this.numTiers > 1) {
      dstTier = Math.floor(Math.random() * this.numTiers);
    }

    this.inject3DPacket(srcTier, dstTier);
    this.audio.playElevator();
    this.addFloatingText(x, y, `VERTICAL HOP: T${srcTier} ➔ T${dstTier}`, '#4ade80');
  }

  inject3DPacket(srcTier, dstTier) {
    this.packets3d.push({
      srcTier,
      dstTier,
      currentTier: srcTier,
      x: 140 + Math.random() * 320,
      y: 0,
      progress: 0,
      verticalSpeed: 0.03,
      state: 'vertical'
    });
    this.score += 35;
    this.updateHUD();
  }

  addFloatingText(x, y, text, color) {
    this.particles.push({
      x, y, text, color,
      alpha: 1.0,
      vy: -1.2,
      life: 45
    });
  }

  start() {
    this.running = true;
    this.isPaused = false;
    this.loop();
  }

  loop() {
    if (!this.running) return;
    if (!this.isPaused) {
      this.update();
      this.render();
    }
    this.animId = requestAnimationFrame(() => this.loop());
  }

  update() {
    // Auto-inject occasional background 3D transactions
    if (Math.random() < 0.04) {
      const srcT = Math.floor(Math.random() * this.numTiers);
      const dstT = (srcT + 1) % this.numTiers;
      this.inject3DPacket(srcT, dstT);
    }

    // Update 3D packets
    for (let i = this.packets3d.length - 1; i >= 0; i--) {
      const p = this.packets3d[i];
      p.progress += p.verticalSpeed;
      if (p.progress >= 1.0) {
        this.packets3d.splice(i, 1);
        this.score += 20;
      }
    }

    // Update particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const pt = this.particles[i];
      pt.y += pt.vy;
      pt.alpha -= 1 / pt.life;
      if (pt.alpha <= 0) {
        this.particles.splice(i, 1);
      }
    }
  }

  render() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    if (this.mode === 'isometric_3d') {
      this.renderIsometricStack();
    } else {
      this.renderThermalStackView();
    }

    // Floating particles
    for (const pt of this.particles) {
      this.ctx.save();
      this.ctx.globalAlpha = pt.alpha;
      this.ctx.fillStyle = pt.color;
      this.ctx.font = 'bold 12px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.fillText(pt.text, pt.x, pt.y);
      this.ctx.restore();
    }
  }

  renderIsometricStack() {
    const ctx = this.ctx;
    const w = this.canvas.width;

    ctx.fillStyle = '#94a3b8';
    ctx.font = '600 12px "JetBrains Mono", monospace';
    ctx.fillText('3D SILICON TIERS & VERTICAL TSV PILLARS (ISOMETRIC STACK)', 20, 30);

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 13px "JetBrains Mono", monospace';
    ctx.fillText(`Algorithm: ${this.routingAlgo.toUpperCase()} | Pitch: ${this.tsvPitchUm}µm | TSVs: ${this.dummyTsvCount + 16} Links`, 20, 52);

    // Draw stacked silicon layers in isometric projection
    const tierSpacing = 280 / (this.numTiers + 0.5);
    const startY = 360;

    const tierLabels = [
      'Tier 0: Base Logic & Heat Sink Plane (Bottom)',
      'Tier 1: High-Performance Multi-Core CPU/GPU',
      'Tier 2: 3D Stacked SRAM Cache Matrix',
      'Tier 3: High-Bandwidth Memory (3D DRAM)',
      'Tier 4: Photonic Interconnect / RF Interface'
    ];

    const tierColors = ['#0284c7', '#38bdf8', '#8b5cf6', '#ec4899', '#f59e0b'];

    for (let t = 0; t < this.numTiers; t++) {
      const ty = startY - t * tierSpacing;
      const tColor = tierColors[t % tierColors.length];

      // Draw isometric silicon die plane
      this.drawIsoPlane(ctx, 310, ty, 200, 75, tColor, t === 0 ? 0.35 : 0.2);

      // Label
      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 11px "JetBrains Mono", monospace';
      ctx.fillText(tierLabels[t] || `Tier ${t}`, 50, ty + 5);

      ctx.fillStyle = this.tierTemps[t] > 80 ? '#f87171' : '#4ade80';
      ctx.font = '10px "JetBrains Mono", monospace';
      ctx.fillText(`${this.tierTemps[t].toFixed(1)}°C`, 470, ty + 5);

      // Draw vertical TSV pillars connecting tiers
      if (t < this.numTiers - 1) {
        const nextTy = ty - tierSpacing;
        for (let col = -2; col <= 2; col++) {
          const px = 310 + col * 45;
          const py1 = ty - 12;
          const py2 = nextTy + 12;

          // Copper TSV Pillar
          ctx.strokeStyle = '#eab308';
          ctx.lineWidth = 3.5;
          ctx.beginPath();
          ctx.moveTo(px, py1);
          ctx.lineTo(px, py2);
          ctx.stroke();

          // TSV Keep-Out Zone (KOZ) ring
          ctx.strokeStyle = 'rgba(234, 179, 8, 0.4)';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.ellipse(px, py1, 8, 4, 0, 0, Math.PI * 2);
          ctx.stroke();
        }
      }
    }

    // Render active vertical flits
    for (const p of this.packets3d) {
      const ySrc = startY - p.srcTier * tierSpacing - 12;
      const yDst = startY - p.dstTier * tierSpacing + 12;
      const currentY = ySrc + (yDst - ySrc) * p.progress;

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(p.x, currentY, 6, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(p.x, currentY, 10, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Substrate Heatsink Banner
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(150, 425, 320, 20);
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 1;
    ctx.strokeRect(150, 425, 320, 20);
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 10px "JetBrains Mono", monospace';
    ctx.textAlign = 'center';
    ctx.fillText('▼ INTEGRATED HEAT SINK & THERMAL INTERFACE MATERIAL ▼', 310, 439);
    ctx.textAlign = 'left';
  }

  drawIsoPlane(ctx, cx, cy, rx, ry, color, alpha) {
    ctx.save();
    ctx.fillStyle = color;
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    ctx.moveTo(cx, cy - ry);
    ctx.lineTo(cx + rx, cy);
    ctx.lineTo(cx, cy + ry);
    ctx.lineTo(cx - rx, cy);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = color;
    ctx.globalAlpha = 0.8;
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.restore();
  }

  renderThermalStackView() {
    const ctx = this.ctx;
    ctx.fillStyle = '#94a3b8';
    ctx.font = '600 12px "JetBrains Mono", monospace';
    ctx.fillText('3D THERMAL STACKING PROFILE & ILD HEAT DISSIPATION', 20, 30);

    ctx.fillStyle = '#ef4444';
    ctx.font = 'bold 13px "JetBrains Mono", monospace';
    ctx.fillText(`Peak Thermal Hotspot: ${this.peakTemp.toFixed(1)}°C (Thermal Runaway Threshold: 85.0°C)`, 20, 52);

    // Cross-section of stacked dies and thermal resistance ladder
    const barW = 380;
    const barH = 45;
    const startX = 60;
    let currY = 85;

    for (let t = this.numTiers - 1; t >= 0; t--) {
      const temp = this.tierTemps[t];
      const heatFrac = Math.min(1.0, Math.max(0, (temp - 40) / 60));
      const r = Math.floor(255 * heatFrac);
      const g = Math.floor(180 * (1 - heatFrac * 0.7));
      const b = Math.floor(240 * (1 - heatFrac));

      // Silicon Die
      ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
      ctx.fillRect(startX, currY, barW, barH);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      ctx.strokeRect(startX, currY, barW, barH);

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 11px "JetBrains Mono", monospace';
      ctx.fillText(`TIER ${t}: ${temp.toFixed(1)}°C (Silicon Layer, k_Si = 140 W/m·K)`, startX + 12, currY + 26);

      currY += barH;

      // ILD Layer between tiers
      if (t > 0) {
        ctx.fillStyle = '#334155';
        ctx.fillRect(startX, currY, barW, 14);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '9px "JetBrains Mono", monospace';
        ctx.fillText(`ILD Oxide Bond (k_ILD = 1.2 W/m·K - THERMAL BOTTLENECK)`, startX + 10, currY + 11);
        currY += 14;
      }
    }

    // Heat sink below
    ctx.fillStyle = '#0284c7';
    ctx.fillRect(startX, currY, barW, 25);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 11px "JetBrains Mono", monospace';
    ctx.fillText('HEAT SINK BASE (T_amb = 40.0°C)', startX + 75, currY + 17);

    // Right-side explanation
    ctx.fillStyle = '#cbd5e1';
    ctx.font = '11px "JetBrains Mono", monospace';
    ctx.fillText('• Copper TSV Conduits: k_Cu = 400 W/m·K', 460, 110);
    ctx.fillText('• Thermal Trap: Middle tiers climb', 460, 135);
    ctx.fillText('  fast without dummy TSV conduits.', 460, 155);
    ctx.fillText(`• Active Conduits: ${this.dummyTsvCount}`, 460, 185);
    ctx.fillText(`• Cooling Gain: -${(this.dummyTsvCount * 0.9).toFixed(1)}°C`, 460, 210);

    ctx.fillStyle = '#38bdf8';
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.fillText('💡 Press Space to deploy more thermal dummy TSVs and draw heat away from trapped tiers!', 20, 435);
  }
}

let tsvSim = null;

function startTSVSimulation() {
  if (!tsvSim) {
    tsvSim = new TSVSimulator('tsvCanvas');
  }
  tsvSim.start();
  document.getElementById('tsvStartBtn').textContent = '⚡ Architect Active';
  document.getElementById('tsvStartBtn').style.background = '#22c55e';
}

function toggleTSVMode() {
  if (!tsvSim) startTSVSimulation();
  tsvSim.mode = tsvSim.mode === 'isometric_3d' ? 'thermal_stack' : 'isometric_3d';
  document.getElementById('tsvModeBtn').textContent = tsvSim.mode === 'isometric_3d' ? '🔄 Mode: 3D Routing & Tiers' : '🔄 Mode: Thermal Stacking View';
}

function deployThermalTSVs() {
  if (!tsvSim) startTSVSimulation();
  tsvSim.addThermalConduits();
}

function updateTSVConfig() {
  if (!tsvSim) return;
  tsvSim.numTiers = parseInt(document.getElementById('tsvTierSelect').value, 10);
  tsvSim.computePhysics();
}

function updateTSVRouting(val) {
  if (!tsvSim) return;
  tsvSim.routingAlgo = val;
}

function toggleTSVSound() {
  if (!tsvSim) return;
  tsvSim.audio.enabled = !tsvSim.audio.enabled;
  document.getElementById('tsvSoundBtn').textContent = tsvSim.audio.enabled ? '🔊 Sound: ON' : '🔈 Sound: OFF';
}

function toggleTSVPause() {
  if (!tsvSim) return;
  tsvSim.isPaused = !tsvSim.isPaused;
}

function saveTSVRecord() {
  if (!tsvSim) return;
  const name = document.getElementById("tsvCallsign").value.trim() || "TSV Titan";
  const org = document.getElementById("tsvOrg").value.trim() || "Silicon Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const record = {
    name: name,
    org: org,
    track: `TSV Titan (3D ${tsvSim.numTiers}-Tier ${tsvSim.routingAlgo.toUpperCase()})`,
    score: tsvSim.score,
    accuracy: Math.round(tsvSim.peakTemp * 10) / 10,
    certId: `3D-NOC-TSV-${tsvSim.numTiers}TIER`,
    date: dateStr,
    type: "tsv3d"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("tsvSaveConfirm").style.display = "block";
  } catch (e) {
    console.error("Failed to save to localStorage", e);
  }
}

function submitTSVToGithub() {
  if (!tsvSim) return;
  const name = document.getElementById("tsvCallsign").value.trim() || "TSV Titan";
  const org = document.getElementById("tsvOrg").value.trim() || "Silicon Lab";
  const body = encodeURIComponent(
    `### 3D-NoC TSV Architect Benchmark Submission\n\n- **Player:** ${name}\n- **Institution:** ${org}\n- **3D Tiers:** ${tsvSim.numTiers}\n- **Peak Temp:** ${tsvSim.peakTemp.toFixed(1)}°C\n- **Score:** ${tsvSim.score}`
  );
  window.open(`https://github.com/network-on-chip/learning/issues/new?title=ScoreSubmission:+${encodeURIComponent(name)}&body=${body}`, '_blank');
}

function restartTSVGame() {
  document.getElementById("tsvModal").style.display = "none";
  if (tsvSim) {
    tsvSim.score = 0;
    tsvSim.packets3d = [];
    tsvSim.dummyTsvCount = 16;
    tsvSim.computePhysics();
  }
}

// Auto-boot on load
window.addEventListener('DOMContentLoaded', () => {
  startTSVSimulation();
});
</script>
