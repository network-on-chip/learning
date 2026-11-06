# ⚡ Wire Wizard: Interconnect Physics & Wire Scaling Lab

Master the physical foundations of on-chip communication! Experience the Interconnect Crisis firsthand by simulating distributed RC wire parasitics, Elmore delay scaling across technology nodes (180nm down to 3nm GAA), Bakoglu optimal repeater insertion, and the catastrophic throughput collapse of shared multi-drop buses versus scalable 2D Mesh Networks-on-Chip. High scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="wireStartBtn" class="noc-sim-btn" onclick="startWireSimulation()">▶ Start Simulation</button>
    <button id="wireModeBtn" class="noc-sim-btn" onclick="toggleWireMode()" style="background:#ea580c; border:none; box-shadow:0 0 12px rgba(234,88,12,0.4);">🔄 Mode: RC Wire &amp; Repeaters</button>
    <button id="wirePulseBtn" class="noc-sim-btn" onclick="fireWirePulse()" style="background:#0284c7; border:none;">⚡ Inject Pulse (Space)</button>

    <label><b>Technology Node:</b>
      <select id="wireNodeSelect" class="noc-sim-select" onchange="updateWireParams()">
        <option value="180">180nm Bulk (Aluminum / SiO2)</option>
        <option value="90">90nm CMOS (Copper / Low-k)</option>
        <option value="45">45nm HKMG (Copper Dual-Damascene)</option>
        <option value="14">14nm FinFET (Air Gaps / Co-liner)</option>
        <option value="7">7nm EUV (Ruthenium / Sub-25nm Pitch)</option>
        <option value="3" selected>3nm GAA MBCFET (Extreme Scattering)</option>
      </select>
    </label>

    <label><b>Metal Layer:</b>
      <select id="wireMetalSelect" class="noc-sim-select" onchange="updateWireParams()">
        <option value="local">Local (M1-M2, Dense, High R)</option>
        <option value="intermediate" selected>Intermediate (M3-M5, Balanced)</option>
        <option value="global">Global (Top Metal, Thick, Low R)</option>
      </select>
    </label>

    <button id="wireSoundBtn" class="noc-sim-btn secondary" onclick="toggleWireSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleWirePause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="wireScore">0</span></span>
      <span style="color:#22c55e;">Delay: <span id="wireDelayDisp">0.42 ns</span></span>
      <span style="color:#ef4444;">Fmax: <span id="wireFmaxDisp">2.38 GHz</span></span>
      <span style="color:#f59e0b;" id="wireWave">Wave 1</span>
    </div>
  </div>

  <!-- Live Interconnect Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">📏 Wire Length &amp; Repeaters:</span>
        <span id="wireLengthText" style="font-weight:700; color:#38bdf8;">5.0 mm (k=4)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="wireLengthBar" style="width:50%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#f87171;">🧪 Copper Resistivity (Scattering):</span>
        <span id="wireResistText" style="font-weight:700; color:#f87171;">5.40 µΩ·cm (3.2x bulk)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(239,68,68,0.15); border-radius:4px; overflow:hidden;">
        <div id="wireResistBar" style="width:65%; height:100%; background:#ef4444; transition:width 0.2s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#22c55e;">⚡ Repeater Power Overhead:</span>
        <span id="wirePowerText" style="font-weight:700; color:#22c55e;">8.4 mW (Area: 1.2%)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(34,197,94,0.15); border-radius:4px; overflow:hidden;">
        <div id="wirePowerBar" style="width:30%; height:100%; background:#22c55e; transition:width 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="wireCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Modal for Challenges / Results -->
    <div id="wireModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="wireModalIcon">💥</div>
      <h2 id="wireModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">BUS CONTENTION BREAKDOWN!</h2>
      <p id="wireModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Shared multi-drop bus wire RC delay and capacitive tap loading exceeded maximum cycle budget! Transaction latency spiked quadratically (O(N^2)).
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Silicon Architect Callsign:</label>
        <input type="text" id="wireCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Wire Wizard" value="Interconnect Architect">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="wireOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Stanford / TSMC / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveWireRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitWireToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartWireGame()" style="color:#ffffff !important;">🔄 Run Again</button>
      </div>
      <div id="wireSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in your browser Leaderboard!
      </div>
    </div>
  </div>

  <div id="wireInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">⚡ Wire Physics &amp; Scaling Principles (Chapter 1 Foundations):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Elmore Distributed RC Delay:</strong> An unbuffered wire of length $L$ incurs quadratic delay: $\tau = \frac{1}{2} r_w c_w L^2 + R_d(c_w L + C_L)$. At $L = 10\text{ mm}$, unbuffered delay exceeds $4\text{ ns}$—paralyzing gigahertz clock domains!</li>
      <li><strong>Bakoglu Optimal Repeater Insertion:</strong> Dividing long interconnects into $k_{opt} = \sqrt{\frac{r_w c_w L^2}{2 R_0 C_0}}$ segments with repeaters of size $h_{opt} = \sqrt{\frac{R_0 c_w}{r_w C_0}}$ converts quadratic delay $O(L^2)$ into linear delay $O(L)$, reducing total transit time by over 70%.</li>
      <li><strong>Nanoscale Resistivity Scaling:</strong> As wire widths scale below 30nm in advanced nodes, Fuchs-Sondheimer surface scattering and Mayadas-Shatzkes grain-boundary electron scattering cause copper resistivity $\rho(w)$ to surge from $1.7\,\mu\Omega\cdot\text{cm}$ to over $6.0\,\mu\Omega\cdot\text{cm}$.</li>
      <li><strong>Shared Bus Contention Collapse:</strong> In Mode B (Bus vs NoC), adding cores $N$ introduces capacitive tap loads $C_{tap} \cdot N$ and arbitration serialization bubbles. Total latency scales as $O(N^{3/2})$ to $O(N^2)$, causing throughput to saturate at 1x while 2D Mesh NoCs scale linearly!</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Wire Wizard
class WireAudio {
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

  playPulse() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(440, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, this.ctx.currentTime + 0.12);
    gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.12);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.12);
  }

  playRepeater() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(720, this.ctx.currentTime);
    osc.frequency.setValueAtTime(1080, this.ctx.currentTime + 0.05);
    gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.09);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.09);
  }

  playError() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(150, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(60, this.ctx.currentTime + 0.3);
    gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.3);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.3);
  }

  playVictory() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    [523.25, 659.25, 783.99, 1046.50].forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime + idx * 0.08);
      gain.gain.setValueAtTime(0.2, this.ctx.currentTime + idx * 0.08);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + idx * 0.08 + 0.2);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(this.ctx.currentTime + idx * 0.08);
      osc.stop(this.ctx.currentTime + idx * 0.08 + 0.25);
    });
  }
}

// Main Simulation Engine
class WireSimulator {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.audio = new WireAudio();

    this.mode = 'rc_wire'; // 'rc_wire' or 'bus_vs_noc'
    this.node = '3';
    this.metal = 'intermediate';
    this.lengthMm = 5.0; // mm
    this.repeaterCount = 4;
    this.repeaterOpt = 4;
    this.repeaterSize = 25; // x min inv

    // Physics parameters
    this.rw = 0; // ohm/um
    this.cw = 0; // fF/um
    this.rho = 1.7; // uohm-cm
    this.tauUnbuf = 0; // ns
    this.tauBuf = 0; // ns
    this.fmax = 0; // GHz
    this.powerMw = 0; // mW

    // Bus vs NoC mode
    this.busCores = 16;
    this.busLoad = 0.6;
    this.busPackets = [];
    this.nocPackets = [];
    this.busLatency = 0;
    this.nocLatency = 0;

    // Pulse animation
    this.pulses = [];
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
        this.injectPulse();
      }
    });
  }

  computePhysics() {
    // Node scaling data (node in nm)
    const nodeData = {
      '180': { pitch: 500, w: 250, t: 500, k: 3.9, rho0: 2.7, r0: 1000, c0: 1.5, vdd: 1.8 },
      '90':  { pitch: 200, w: 100, t: 220, k: 3.0, rho0: 2.0, r0: 1800, c0: 1.2, vdd: 1.2 },
      '45':  { pitch: 100, w: 45,  t: 110, k: 2.6, rho0: 2.5, r0: 2500, c0: 1.0, vdd: 1.0 },
      '14':  { pitch: 40,  w: 20,  t: 50,  k: 2.4, rho0: 3.8, r0: 3800, c0: 0.8, vdd: 0.8 },
      '7':   { pitch: 24,  w: 12,  t: 36,  k: 2.3, rho0: 4.8, r0: 5000, c0: 0.7, vdd: 0.7 },
      '3':   { pitch: 18,  w: 9,   t: 28,  k: 2.2, rho0: 5.8, r0: 6500, c0: 0.6, vdd: 0.65 }
    };

    const d = nodeData[this.node] || nodeData['3'];
    let w = d.w * 1e-3; // um
    let t = d.t * 1e-3; // um

    if (this.metal === 'local') {
      w *= 0.8;
      t *= 0.8;
    } else if (this.metal === 'global') {
      w *= 3.5;
      t *= 3.0;
    }

    // Fuchs-Sondheimer surface scattering & Mayadas-Shatzkes grain boundary scattering
    const lambda_e = 0.039; // um electron mean free path in Cu
    const p = 0.2; // specularity parameter
    const R_refl = 0.4; // grain boundary reflection coefficient
    const d_grain = w; // grain size roughly equals wire width

    const alpha = (lambda_e / d_grain) * (R_refl / (1 - R_refl));
    const rho_bulk = 1.7; // uOhm-cm
    const fs_factor = 1 + (3 / 8) * (1 - p) * (lambda_e / w);
    const ms_factor = 1 + 1.33 * alpha;
    this.rho = rho_bulk * fs_factor * ms_factor;

    // Resistance per um (ohm/um)
    const area_um2 = w * t;
    this.rw = (this.rho * 1e-4) / area_um2; // ohm/um

    // Capacitance per um (fF/um)
    const eps0 = 8.854e-3; // fF/um
    const c_ground = (d.k * eps0 * w) / (t * 1.2);
    const c_coupling = 2 * (d.k * eps0 * t) / (w * 1.1);
    this.cw = c_ground + c_coupling; // fF/um

    const L_um = this.lengthMm * 1000;
    const R_wire = this.rw * L_um;
    const C_wire = this.cw * L_um * 1e-3; // pF

    // Bakoglu optimal repeaters
    const R0 = d.r0; // ohm of min inverter
    const C0 = d.c0 * 1e-3; // pF of min inverter
    const cw_pF_um = this.cw * 1e-3;

    this.repeaterOpt = Math.max(1, Math.round(L_um * Math.sqrt((this.rw * cw_pF_um) / (2 * R0 * C0))));
    this.repeaterSize = Math.max(5, Math.round(Math.sqrt((R0 * cw_pF_um) / (this.rw * C0))));

    // Unbuffered Elmore delay
    const R_driver = R0 / 20; // 20x driver
    const C_load = C0 * 20;
    this.tauUnbuf = (0.5 * R_wire * C_wire + R_driver * (C_wire + C_load) + R_wire * C_load) * 1e-3; // ns

    // Buffered delay with current repeaterCount
    const k = Math.max(1, this.repeaterCount);
    const l_seg = L_um / k;
    const r_seg = this.rw * l_seg;
    const c_seg = cw_pF_um * l_seg;
    const r_rep = R0 / this.repeaterSize;
    const c_rep = C0 * this.repeaterSize;

    const tau_seg = 0.5 * r_seg * c_seg + r_rep * (c_seg + c_rep) + r_seg * c_rep;
    this.tauBuf = (k * tau_seg) * 1e-3; // ns

    this.fmax = 1 / (2.5 * this.tauBuf); // GHz
    this.powerMw = k * (this.repeaterSize * d.c0 * 1e-15 * Math.pow(d.vdd, 2) * (this.fmax * 1e9) + 2e-6 * d.vdd) * 1000;

    this.updateHUD();
  }

  updateHUD() {
    document.getElementById('wireDelayDisp').textContent = `${this.tauBuf.toFixed(3)} ns`;
    document.getElementById('wireFmaxDisp').textContent = `${this.fmax.toFixed(2)} GHz`;
    document.getElementById('wireScore').textContent = this.score;

    document.getElementById('wireLengthText').textContent = `${this.lengthMm.toFixed(1)} mm (k=${this.repeaterCount}, opt=${this.repeaterOpt})`;
    document.getElementById('wireLengthBar').style.width = `${Math.min(100, (this.lengthMm / 15) * 100)}%`;

    document.getElementById('wireResistText').textContent = `${this.rho.toFixed(2)} µΩ·cm (${(this.rho / 1.7).toFixed(1)}x)`;
    document.getElementById('wireResistBar').style.width = `${Math.min(100, (this.rho / 10) * 100)}%`;

    document.getElementById('wirePowerText').textContent = `${this.powerMw.toFixed(1)} mW (h=${this.repeaterSize}x)`;
    document.getElementById('wirePowerBar').style.width = `${Math.min(100, (this.powerMw / 30) * 100)}%`;
  }

  injectPulse() {
    this.audio.playPulse();
    if (this.mode === 'rc_wire') {
      this.pulses.push({
        x: 60,
        progress: 0,
        speed: 1 / (this.tauBuf * 60 + 15),
        color: '#38bdf8',
        stage: 0
      });
      this.score += 25;
    } else {
      // Inject bus transaction
      const src = Math.floor(Math.random() * this.busCores);
      const dst = (src + 1 + Math.floor(Math.random() * (this.busCores - 1))) % this.busCores;
      this.busPackets.push({
        src, dst,
        age: 0,
        state: 'arbitrating',
        progress: 0
      });
      // Inject NoC concurrent transaction
      this.nocPackets.push({
        src, dst,
        age: 0,
        hops: Math.abs((dst % 4) - (src % 4)) + Math.abs(Math.floor(dst / 4) - Math.floor(src / 4)),
        currentHop: 0,
        progress: 0
      });
      this.score += 50;
    }
    this.updateHUD();
  }

  handleClick(x, y) {
    if (this.mode === 'rc_wire') {
      // Click along wire to add/remove repeaters
      if (y >= 140 && y <= 240) {
        if (x > 500) {
          this.repeaterCount = Math.min(16, this.repeaterCount + 1);
        } else if (x < 120) {
          this.repeaterCount = Math.max(1, this.repeaterCount - 1);
        } else {
          // Toggle optimal Bakoglu repeater config
          this.repeaterCount = this.repeaterOpt;
          this.addFloatingText(x, y, `OPT BAKOGLU: k=${this.repeaterOpt}!`, '#22c55e');
          this.audio.playVictory();
        }
        this.computePhysics();
      }
    } else {
      // Toggle bus cores
      if (y >= 380 && y <= 440) {
        if (x < 300) {
          this.busCores = this.busCores === 64 ? 4 : this.busCores * 2;
          this.addFloatingText(x, y, `CORES: ${this.busCores}`, '#f59e0b');
        }
      }
    }
  }

  addFloatingText(x, y, text, color) {
    this.particles.push({
      x, y, text, color,
      alpha: 1.0,
      vy: -1.2,
      life: 50
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
    // Pulse animation in rc_wire mode
    for (let i = this.pulses.length - 1; i >= 0; i--) {
      const p = this.pulses[i];
      p.progress += p.speed;
      const totalWidth = 500;
      p.x = 60 + p.progress * totalWidth;

      // Check repeater boundaries
      const segWidth = totalWidth / this.repeaterCount;
      const currentSeg = Math.floor((p.x - 60) / segWidth);
      if (currentSeg > p.stage) {
        p.stage = currentSeg;
        this.audio.playRepeater();
        this.particles.push({
          x: 60 + currentSeg * segWidth,
          y: 190,
          text: '⚡ BOOST',
          color: '#eab308',
          alpha: 1.0,
          vy: -1.5,
          life: 30
        });
      }

      if (p.progress >= 1.0) {
        this.pulses.splice(i, 1);
        this.score += 10;
        this.updateHUD();
      }
    }

    // Update Bus vs NoC packets
    if (this.mode === 'bus_vs_noc') {
      // Auto-inject periodic packets
      if (Math.random() < 0.15) {
        const src = Math.floor(Math.random() * this.busCores);
        const dst = (src + 1 + Math.floor(Math.random() * (this.busCores - 1))) % this.busCores;
        this.busPackets.push({ src, dst, age: 0, state: 'arbitrating', progress: 0 });
        this.nocPackets.push({ src, dst, age: 0, hops: 2 + Math.floor(Math.random() * 3), currentHop: 0, progress: 0 });
      }

      // Bus: Only 1 packet traverses at a time!
      let busBusy = false;
      for (let i = 0; i < this.busPackets.length; i++) {
        const bp = this.busPackets[i];
        bp.age++;
        if (!busBusy && bp.state === 'arbitrating') {
          bp.state = 'transmitting';
          busBusy = true;
        } else if (bp.state === 'transmitting') {
          busBusy = true;
          bp.progress += 0.08 / (1 + this.busCores * 0.05); // Bus slows down with core capacitance!
          if (bp.progress >= 1.0) {
            this.busPackets.splice(i, 1);
            i--;
            this.score += 15;
          }
        }
      }

      // NoC: All concurrent links transmit simultaneously!
      for (let i = 0; i < this.nocPackets.length; i++) {
        const np = this.nocPackets[i];
        np.age++;
        np.progress += 0.15; // Uncongested point-to-point links
        if (np.progress >= 1.0) {
          np.currentHop++;
          np.progress = 0;
          if (np.currentHop >= np.hops) {
            this.nocPackets.splice(i, 1);
            i--;
            this.score += 25;
          }
        }
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

    if (this.mode === 'rc_wire') {
      this.renderRCWireMode();
    } else {
      this.renderBusVsNocMode();
    }

    // Render floating particles
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

  renderRCWireMode() {
    const ctx = this.ctx;
    const w = this.canvas.width;

    // Header Title
    ctx.fillStyle = '#94a3b8';
    ctx.font = '600 12px "JetBrains Mono", monospace';
    ctx.fillText('DISTRIBUTED RC TRANSMISSION LINE & BAKOGLU REPEATER MODEL', 20, 30);

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 14px "JetBrains Mono", monospace';
    ctx.fillText(`Node: ${this.node}nm | Layer: ${this.metal.toUpperCase()} | Length: ${this.lengthMm}mm`, 20, 52);

    // Draw Silicon Substrate & Interconnect Wire
    const wireY = 190;
    const wireStartX = 60;
    const wireEndX = 560;
    const wireLen = wireEndX - wireStartX;

    // Substrate plane
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(wireStartX - 10, wireY + 45, wireLen + 20, 15);
    ctx.fillStyle = '#475569';
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.fillText('GROUND SUBSTRATE PLANE (VSS)', wireStartX, wireY + 75);

    // Unbuffered wire background glow
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 14;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(wireStartX, wireY);
    ctx.lineTo(wireEndX, wireY);
    ctx.stroke();

    // Segment divisions & Repeaters
    const k = this.repeaterCount;
    const segLen = wireLen / k;

    for (let i = 0; i <= k; i++) {
      const rx = wireStartX + i * segLen;

      if (i === 0) {
        // Transmitter Driver Inverter
        this.drawInverter(ctx, rx - 20, wireY, 28, '#0284c7', 'TX');
      } else if (i === k) {
        // Receiver Load Inverter
        this.drawInverter(ctx, rx, wireY, 28, '#10b981', 'RX');
      } else {
        // Intermediate Repeater Inverter
        this.drawInverter(ctx, rx - 14, wireY, 24, '#eab308', `R${i}`);
      }

      // Draw capacitive coupling to ground
      if (i < k) {
        const capX = rx + segLen * 0.5;
        ctx.strokeStyle = 'rgba(56,189,248,0.3)';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.moveTo(capX, wireY + 7);
        ctx.lineTo(capX, wireY + 45);
        ctx.stroke();
        ctx.setLineDash([]);

        // Small capacitor symbol
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(capX - 6, wireY + 24);
        ctx.lineTo(capX + 6, wireY + 24);
        ctx.moveTo(capX - 6, wireY + 28);
        ctx.lineTo(capX + 6, wireY + 28);
        ctx.stroke();
      }
    }

    // Draw active pulses
    for (const p of this.pulses) {
      const grad = ctx.createRadialGradient(p.x, wireY, 0, p.x, wireY, 18);
      grad.addColorStop(0, '#ffffff');
      grad.addColorStop(0.4, '#38bdf8');
      grad.addColorStop(1, 'rgba(56,189,248,0)');

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(p.x, wireY, 16, 0, Math.PI * 2);
      ctx.fill();
    }

    // Lower Comparison Dashboard: Unbuffered Quadratic vs Buffered Linear
    ctx.fillStyle = '#1e293b';
    ctx.roundRect(20, 275, 580, 165, 8);
    ctx.fill();
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 12px "JetBrains Mono", monospace';
    ctx.fillText('ELMORE DELAY FORMULATION & SCALING COMPARISON', 35, 300);

    // Left column: Unbuffered
    ctx.fillStyle = '#f87171';
    ctx.font = '11px "JetBrains Mono", monospace';
    ctx.fillText('🔴 UNBUFFERED RC SCALING (O(L²)):', 35, 325);
    ctx.fillStyle = '#cbd5e1';
    ctx.font = '11px "JetBrains Mono", monospace';
    ctx.fillText(`• τ_unbuffered = 0.5·rw·cw·L² + Rd·CL = ${this.tauUnbuf.toFixed(3)} ns`, 35, 345);
    ctx.fillText(`• Delay Penalty: ${(this.tauUnbuf / this.tauBuf).toFixed(1)}x SLOWER than buffered!`, 35, 365);
    ctx.fillText(`• Signal Slew Degradation: Severe Edge Droop`, 35, 385);

    // Right column: Bakoglu Buffered
    ctx.fillStyle = '#4ade80';
    ctx.font = '11px "JetBrains Mono", monospace';
    ctx.fillText('🟢 BAKOGLU REPEATER INSERTION (O(L)):', 320, 325);
    ctx.fillStyle = '#cbd5e1';
    ctx.fillText(`• Optimal Repeaters: k_opt = ${this.repeaterOpt} (Active: ${this.repeaterCount})`, 320, 345);
    ctx.fillText(`• Optimal Inverter Sizing: h_opt = ${this.repeaterSize}x min`, 320, 365);
    ctx.fillText(`• Sustained Clock Fmax: ${this.fmax.toFixed(2)} GHz`, 320, 385);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.fillText('💡 Click on wire to toggle optimal Bakoglu configuration! Spacebar to inject signal pulse.', 35, 422);
  }

  drawInverter(ctx, x, y, size, color, label) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x, y - size / 2);
    ctx.lineTo(x + size * 0.85, y);
    ctx.lineTo(x, y + size / 2);
    ctx.closePath();
    ctx.fill();

    // Inversion circle
    ctx.beginPath();
    ctx.arc(x + size * 0.95, y, size * 0.12, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 9px "JetBrains Mono", monospace';
    ctx.textAlign = 'center';
    ctx.fillText(label, x + size * 0.35, y + 3);
    ctx.textAlign = 'left';
  }

  renderBusVsNocMode() {
    const ctx = this.ctx;
    const w = this.canvas.width;

    ctx.fillStyle = '#94a3b8';
    ctx.font = '600 12px "JetBrains Mono", monospace';
    ctx.fillText('MULTI-DROP BUS CONTENTION CRISIS VS 2D MESH NOC SCALABILITY', 20, 30);

    ctx.fillStyle = '#f59e0b';
    ctx.font = 'bold 13px "JetBrains Mono", monospace';
    ctx.fillText(`Core Count N = ${this.busCores} | Tap Capacitance: ${(this.busCores * 15)} fF | Shared Arbiter`, 20, 52);

    // Top half: Shared Bus
    ctx.fillStyle = 'rgba(239, 68, 68, 0.08)';
    ctx.roundRect(20, 75, 580, 160, 8);
    ctx.fill();
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.fillStyle = '#f87171';
    ctx.font = 'bold 12px "JetBrains Mono", monospace';
    ctx.fillText('🛑 SHARED MULTI-DROP BUS (Single Shared Channel)', 35, 98);

    // Bus wire
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(40, 160);
    ctx.lineTo(580, 160);
    ctx.stroke();

    // Cores tapping into bus
    const coreSpacing = 520 / Math.min(16, this.busCores);
    for (let i = 0; i < Math.min(16, this.busCores); i++) {
      const cx = 50 + i * coreSpacing;
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(cx - 10, 115, 20, 20);
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 1;
      ctx.strokeRect(cx - 10, 115, 20, 20);

      ctx.fillStyle = '#94a3b8';
      ctx.font = '8px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`C${i}`, cx, 128);

      // Tap line
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(cx, 135);
      ctx.lineTo(cx, 160);
      ctx.stroke();
    }
    ctx.textAlign = 'left';

    // Bus packet queue indicator
    ctx.fillStyle = '#cbd5e1';
    ctx.font = '11px "JetBrains Mono", monospace';
    ctx.fillText(`Queued Transactions: ${this.busPackets.length} | Bus Status: ${this.busPackets.length > 0 ? 'CONGESTED / STALLED' : 'IDLE'}`, 35, 215);

    // Bottom half: 2D Mesh NoC
    ctx.fillStyle = 'rgba(34, 197, 94, 0.08)';
    ctx.roundRect(20, 255, 580, 180, 8);
    ctx.fill();
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.fillStyle = '#4ade80';
    ctx.font = 'bold 12px "JetBrains Mono", monospace';
    ctx.fillText('✅ 2D MESH NETWORK-ON-CHIP (Point-to-Point Concurrent Routing)', 35, 278);

    // Render mini 4x4 mesh nodes
    const meshX = 50;
    const meshY = 295;
    const nodeGap = 36;
    for (let r = 0; r < 3; r++) {
      for (let c = 0; c < 4; c++) {
        const nx = meshX + c * nodeGap;
        const ny = meshY + r * nodeGap;

        ctx.fillStyle = '#1e293b';
        ctx.fillRect(nx - 7, ny - 7, 14, 14);
        ctx.strokeStyle = '#22c55e';
        ctx.lineWidth = 1;
        ctx.strokeRect(nx - 7, ny - 7, 14, 14);

        // Links
        if (c < 3) {
          ctx.strokeStyle = '#334155';
          ctx.beginPath();
          ctx.moveTo(nx + 7, ny);
          ctx.lineTo(nx + nodeGap - 7, ny);
          ctx.stroke();
        }
        if (r < 2) {
          ctx.strokeStyle = '#334155';
          ctx.beginPath();
          ctx.moveTo(nx, ny + 7);
          ctx.lineTo(nx, ny + nodeGap - 7);
          ctx.stroke();
        }
      }
    }

    // Right-side explanation of scaling
    ctx.fillStyle = '#cbd5e1';
    ctx.font = '11px "JetBrains Mono", monospace';
    ctx.fillText('• Bisection Bandwidth: Scales O(√N)', 220, 315);
    ctx.fillText('• Concurrent Channels: 2·N links active in parallel', 220, 335);
    ctx.fillText('• Wire Delay: Confined to localized tile-to-tile hops', 220, 355);
    ctx.fillText(`• Active Concurrent NoC Flits: ${this.nocPackets.length}`, 220, 375);

    ctx.fillStyle = '#f59e0b';
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.fillText('💡 Click bottom banner to double core count N! Spacebar to inject concurrent traffic.', 35, 418);
  }
}

let wireSim = null;

function startWireSimulation() {
  if (!wireSim) {
    wireSim = new WireSimulator('wireCanvas');
  }
  wireSim.start();
  document.getElementById('wireStartBtn').textContent = '⚡ Running';
  document.getElementById('wireStartBtn').style.background = '#22c55e';
}

function toggleWireMode() {
  if (!wireSim) startWireSimulation();
  wireSim.mode = wireSim.mode === 'rc_wire' ? 'bus_vs_noc' : 'rc_wire';
  document.getElementById('wireModeBtn').textContent = wireSim.mode === 'rc_wire' ? '🔄 Mode: RC Wire & Repeaters' : '🔄 Mode: Bus vs NoC Arena';
  wireSim.audio.playRepeater();
}

function fireWirePulse() {
  if (!wireSim) startWireSimulation();
  wireSim.injectPulse();
}

function updateWireParams() {
  if (!wireSim) return;
  wireSim.node = document.getElementById('wireNodeSelect').value;
  wireSim.metal = document.getElementById('wireMetalSelect').value;
  wireSim.computePhysics();
}

function toggleWireSound() {
  if (!wireSim) return;
  wireSim.audio.enabled = !wireSim.audio.enabled;
  document.getElementById('wireSoundBtn').textContent = wireSim.audio.enabled ? '🔊 Sound: ON' : '🔈 Sound: OFF';
}

function toggleWirePause() {
  if (!wireSim) return;
  wireSim.isPaused = !wireSim.isPaused;
}

function saveWireRecord() {
  if (!wireSim) return;
  const name = document.getElementById("wireCallsign").value.trim() || "Wire Wizard";
  const org = document.getElementById("wireOrg").value.trim() || "Silicon Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const record = {
    name: name,
    org: org,
    track: `Wire Wizard (${wireSim.node}nm ${wireSim.metal})`,
    score: wireSim.score,
    accuracy: Math.round(wireSim.fmax * 100) / 100,
    certId: `WIRE-PHYSICS-${wireSim.node}NM`,
    date: dateStr,
    type: "wire"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("wireSaveConfirm").style.display = "block";
  } catch (e) {
    console.error("Failed to save to localStorage", e);
  }
}

function submitWireToGithub() {
  if (!wireSim) return;
  const name = document.getElementById("wireCallsign").value.trim() || "Wire Wizard";
  const org = document.getElementById("wireOrg").value.trim() || "Silicon Lab";
  const body = encodeURIComponent(
    `### Interconnect Physics Benchmark Submission\n\n- **Player:** ${name}\n- **Institution:** ${org}\n- **Technology Node:** ${wireSim.node}nm\n- **Fmax Achieved:** ${wireSim.fmax.toFixed(2)} GHz\n- **Score:** ${wireSim.score}`
  );
  window.open(`https://github.com/network-on-chip/learning/issues/new?title=ScoreSubmission:+${encodeURIComponent(name)}&body=${body}`, '_blank');
}

function restartWireGame() {
  document.getElementById("wireModal").style.display = "none";
  if (wireSim) {
    wireSim.score = 0;
    wireSim.pulses = [];
    wireSim.busPackets = [];
    wireSim.nocPackets = [];
    wireSim.updateHUD();
  }
}

// Auto-boot on page load
window.addEventListener('DOMContentLoaded', () => {
  startWireSimulation();
});
</script>
