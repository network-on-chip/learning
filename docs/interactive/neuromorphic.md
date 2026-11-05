# 🧠 Neuromorphic Nexus: Spiking Neural NoC

Orchestrate brain-inspired asynchronous spike communication on silicon! In neuromorphic computing architectures (such as **Intel Loihi**, **IBM TrueNorth**, and **SpiNNaker**), computation and communication operate on sparse, event-driven action potentials (spikes) using **Address-Event Representation (AER)**.

Unlike traditional request-response memory traffic, spiking neural networks (SNNs) demand massive **1-to-$N$ multicast fan-out**: a single biological axon spike must be replicated across dozens of target post-synaptic neurons on distant cores. Routers must deploy **Hardware Multicast Trees** to branch flits in a single cycle without creating explosive buffer congestion!

Balance Leaky-Integrate-and-Fire (LIF) membrane potentials ($V_m$), manage AER ingress FIFOs, trigger **Spike-Timing-Dependent Plasticity (STDP) Learning Surges**, and prevent catastrophic neural queue overflow. Your high scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="snnStartBtn" class="noc-sim-btn" onclick="startSnnGame()">▶ Start Synaptic Engine</button>
    <button id="stdpSurgeBtn" class="noc-sim-btn" onclick="triggerStdpSurge()" style="background:#8b5cf6; border:none; box-shadow:0 0 14px rgba(139,92,246,0.5);">⚡ STDP Plasticity Surge (Space / S)</button>

    <label><b>Multicast Architecture:</b>
      <select id="snnMulticastSelect" class="noc-sim-select" onchange="setSnnProtocol(this.value)">
        <option value="hardware_tree">Hardware Multicast Trees (Bitmask Branching)</option>
        <option value="spatial_cluster">Spatial Axon Clustering (Localized Fan-Out)</option>
        <option value="unicast_replicate">Software Unicast Replicate (High Congestion)</option>
      </select>
    </label>

    <button id="snnSoundBtn" class="noc-sim-btn secondary" onclick="toggleSnnSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleSnnPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="snnScore">0</span></span>
      <span style="color:#22c55e;">Firings: <span id="snnFirings">0</span></span>
      <span style="color:#ef4444;">AER Load: <span id="snnAerLoad">0%</span></span>
      <span style="color:#f59e0b;" id="snnWave">Wave 1</span>
    </div>
  </div>

  <!-- Synaptic Plasticity & AER Buffer Headroom HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#a855f7;">⚡ STDP Synaptic Potentiation Reservoir:</span>
        <span id="stdpEnergyText" style="font-weight:700; color:#a855f7;">100% READY</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(168,85,247,0.15); border-radius:4px; overflow:hidden;">
        <div id="stdpEnergyBar" style="width:100%; height:100%; background:linear-gradient(90deg, #7c3aed, #a855f7); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#22c55e;">🧠 Ingress AER Queue Buffer Headroom:</span>
        <span id="aerStatusText" style="font-weight:700; color:#22c55e;">HEALTHY (Zero Drops)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(34,197,94,0.15); border-radius:4px; overflow:hidden;">
        <div id="aerBar" style="width:15%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="snnCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="snnOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="snnModalIcon">💥</div>
      <h2 id="snnModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">AER BUFFER OVERFLOW!</h2>
      <p id="snnModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Synchronous action-potential spike bursts saturated the AER ingress FIFOs, losing critical synaptic events!
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Neuromorphic Architect Callsign:</label>
        <input type="text" id="snnCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Synapse Master" value="Neuromorphic Pioneer">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="snnOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Intel Labs / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveSnnRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitSnnToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartSnnGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="snnSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in local Hall of Fame!
      </div>
    </div>
  </div>

  <div id="snnInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">🧠 Neuromorphic NoC Microarchitecture &amp; SNN Rules:</strong>
    <ul style="margin:0.4rem 0 0 1.2rem; padding:0;">
      <li><strong>Event-Driven Spikes (AER):</strong> Packets represent individual biological action potentials. Inactive cores transmit zero idle traffic, maintaining near-zero dynamic power.</li>
      <li><strong>1-to-$N$ Multicast Trees:</strong> A firing axon broadcasts to multiple target synapses across distant cores. Hardware multicast routers duplicate flits simultaneously across output ports ($N, S, E, W$).</li>
      <li><strong>Leaky-Integrate-and-Fire (LIF):</strong> Each core accumulates incoming spike voltages into its membrane potential ($V_m$). Reaching threshold ($V_{thresh}$) triggers a post-synaptic action potential, awarding bonus points!</li>
      <li><strong>STDP Plasticity Surge (Space / S):</strong> Engages Hebbian synaptic learning, doubling flit multicast throughput and clearing AER queue backlogs for 4 seconds!</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Neuromorphic Nexus
class NeuromorphicAudio {
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

  playSpike() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(820, t);
      osc.frequency.exponentialRampToValueAtTime(200, t + 0.05);
      gain.gain.setValueAtTime(0.08, t);
      gain.gain.linearRampToValueAtTime(0.001, t + 0.05);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.05);
    } catch (e) {}
  }

  playNeuronFire() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      [587.33, 880, 1174.66].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, t + idx * 0.03);
        gain.gain.setValueAtTime(0.12, t + idx * 0.03);
        gain.gain.exponentialRampToValueAtTime(0.001, t + idx * 0.03 + 0.18);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t + idx * 0.03);
        osc.stop(t + idx * 0.03 + 0.18);
      });
    } catch (e) {}
  }

  playStdp() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      [440, 554.37, 659.25, 880].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, t + idx * 0.04);
        gain.gain.setValueAtTime(0.14, t + idx * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, t + idx * 0.04 + 0.22);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t + idx * 0.04);
        osc.stop(t + idx * 0.04 + 0.22);
      });
    } catch (e) {}
  }

  playOverflow() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(150, t);
      osc.frequency.linearRampToValueAtTime(50, t + 0.25);
      gain.gain.setValueAtTime(0.25, t);
      gain.gain.linearRampToValueAtTime(0.01, t + 0.25);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.25);
    } catch (e) {}
  }
}

// 4x4 Spiking Neuromorphic NoC Engine
class NeuromorphicGame {
  constructor() {
    this.canvas = document.getElementById('snnCanvas');
    this.ctx = this.canvas.getContext('2d');
    this.audio = new NeuromorphicAudio();

    this.gridW = 4;
    this.gridH = 4;
    this.nodeSpacingX = 125;
    this.nodeSpacingY = 95;
    this.offsetX = 120;
    this.offsetY = 85;

    // 16 LIF Neurons: { x, y, vm, thresh: 100, firings: 0 }
    this.neurons = [];
    this.spikes = [];
    this.particles = [];
    this.score = 0;
    this.neuronFirings = 0;
    this.totalSpikesDelivered = 0;
    this.aerBufferCount = 0;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.stdpEnergy = 100.0;
    this.stdpActive = false;
    this.stdpTimer = 0.0;
    this.protocol = 'hardware_tree';

    this.isRunning = false;
    this.isPaused = false;
    this.lastTime = performance.now();
    this.injectTimer = 0;
    this.nextSpikeId = 1;
  }

  start() {
    this.audio.init();
    this.neurons = [];
    for (let y = 0; y < this.gridH; y++) {
      for (let x = 0; x < this.gridW; x++) {
        this.neurons.push({
          x: x,
          y: y,
          vm: 15.0, // Initial resting potential
          thresh: 100.0,
          firings: 0
        });
      }
    }

    this.spikes = [];
    this.particles = [];
    this.score = 0;
    this.neuronFirings = 0;
    this.totalSpikesDelivered = 0;
    this.aerBufferCount = 0;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.stdpEnergy = 100.0;
    this.stdpActive = false;
    this.stdpTimer = 0.0;
    this.isRunning = true;
    this.isPaused = false;

    document.getElementById('snnOverModal').style.display = 'none';
    document.getElementById('snnStartBtn').textContent = '🔄 Restart';
    this.lastTime = performance.now();

    for (let i = 0; i < 3; i++) {
      this.fireAxonSpikeTrain();
    }
  }

  getNeuron(x, y) {
    return this.neurons[y * this.gridW + x];
  }

  fireAxonSpikeTrain() {
    const sx = Math.floor(Math.random() * this.gridW);
    const sy = Math.floor(Math.random() * this.gridH);

    // Multicast fan-out: select 2-4 target synapses across the chip
    const numTargets = this.protocol === 'spatial_cluster' ? 2 : 3;
    const targets = [];
    for (let i = 0; i < numTargets; i++) {
      let dx = Math.floor(Math.random() * this.gridW);
      let dy = Math.floor(Math.random() * this.gridH);
      if (this.protocol === 'spatial_cluster') {
        // Local cluster targets
        dx = Math.min(this.gridW - 1, Math.max(0, sx + (Math.random() < 0.5 ? 1 : -1)));
        dy = Math.min(this.gridH - 1, Math.max(0, sy + (Math.random() < 0.5 ? 1 : -1)));
      }
      targets.push({ x: dx, y: dy });
    }

    for (let t of targets) {
      this.spikes.push({
        id: this.nextSpikeId++,
        gx: sx,
        gy: sy,
        fromGx: sx,
        fromGy: sy,
        toGx: sx,
        toGy: sy,
        dstX: t.x,
        dstY: t.y,
        progress: 1.0,
        state: 'at_node',
        color: '#c084fc'
      });
    }
    this.audio.playSpike();
  }

  triggerStdp() {
    if (this.stdpEnergy >= 100 && !this.stdpActive) {
      this.stdpActive = true;
      this.stdpTimer = 4.0;
      this.audio.playStdp();
      this.addTextParticle(this.canvas.width / 2, 70, '⚡ STDP SYNAPTIC SURGE ENGAGED!', '#a855f7');
    }
  }

  update(dt) {
    if (!this.isRunning || this.isPaused) return;

    this.waveTimer -= dt;
    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 22.0;
      this.score += 350 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 60, `WAVE ${this.wave} SYNAPTIC BURST!`, '#f59e0b');
    }

    // STDP energy charge
    if (this.stdpActive) {
      this.stdpTimer -= dt;
      this.stdpEnergy = Math.max(0, (this.stdpTimer / 4.0) * 100);
      if (this.stdpTimer <= 0) {
        this.stdpActive = false;
        this.stdpEnergy = 0;
      }
    } else {
      this.stdpEnergy = Math.min(100, this.stdpEnergy + dt * 14.0);
    }

    // Leaky membrane potential decay (biological leak)
    for (let n of this.neurons) {
      n.vm = Math.max(10.0, n.vm - dt * 6.5);
    }

    // Generate axon spike bursts
    this.injectTimer += dt;
    const injectInterval = Math.max(0.4, 1.3 - this.wave * 0.12);
    if (this.injectTimer >= injectInterval && this.spikes.length < 24 + this.wave * 3) {
      this.injectTimer = 0;
      this.fireAxonSpikeTrain();
    }

    // Step 1: Advance in-flight spikes
    const speed = this.stdpActive ? 2.4 : 1.4;
    for (let i = this.spikes.length - 1; i >= 0; i--) {
      const sp = this.spikes[i];

      if (sp.state === 'in_flight') {
        sp.progress += dt * speed;
        if (sp.progress >= 1.0) {
          sp.progress = 1.0;
          sp.gx = sp.toGx;
          sp.gy = sp.toGy;
          sp.state = 'at_node';

          // Delivered to destination synapse!
          if (sp.gx === sp.dstX && sp.gy === sp.dstY) {
            this.spikes.splice(i, 1);
            this.totalSpikesDelivered++;
            this.score += 25;

            // Deposit membrane potential Vm
            const n = this.getNeuron(sp.gx, sp.gy);
            n.vm += 28.0;

            // Check if Neuron reaches threshold and fires an Action Potential!
            if (n.vm >= n.thresh) {
              n.vm = 10.0; // Reset potential
              n.firings++;
              this.neuronFirings++;
              this.score += 120;
              this.audio.playNeuronFire();
              this.addTextParticle(this.getNodeX(sp.gx), this.getNodeY(sp.gy), '⚡ ACTION POTENTIAL!', '#22c55e');
            }
            continue;
          }
        }
      }
    }

    // Step 2: Route spikes at routers (Handling Multicast Fan-out)
    for (let sp of this.spikes) {
      if (sp.state === 'at_node') {
        let nextX = sp.gx;
        let nextY = sp.gy;
        if (sp.dstX > sp.gx) nextX = sp.gx + 1;
        else if (sp.dstX < sp.gx) nextX = sp.gx - 1;
        else if (sp.dstY > sp.gy) nextY = sp.gy + 1;
        else if (sp.dstY < sp.gy) nextY = sp.gy - 1;

        sp.toGx = nextX;
        sp.toGy = nextY;
        sp.fromGx = sp.gx;
        sp.fromGy = sp.gy;
        sp.progress = 0;
        sp.state = 'in_flight';
      }
    }

    // Track AER buffer occupancy
    this.aerBufferCount = this.spikes.length;
    if (this.aerBufferCount >= 34) {
      this.audio.playOverflow();
      this.triggerGameOver();
      return;
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

    // Draw synaptic interconnect links
    this.ctx.lineWidth = 3;
    this.ctx.strokeStyle = '#1e293b';
    for (let y = 0; y < this.gridH; y++) {
      for (let x = 0; x < this.gridW; x++) {
        const nx = this.getNodeX(x);
        const ny = this.getNodeY(y);

        if (x < this.gridW - 1) {
          this.ctx.beginPath();
          this.ctx.moveTo(nx, ny);
          this.ctx.lineTo(this.getNodeX(x + 1), ny);
          this.ctx.stroke();
        }
        if (y < this.gridH - 1) {
          this.ctx.beginPath();
          this.ctx.moveTo(nx, ny);
          this.ctx.lineTo(nx, this.getNodeY(y + 1));
          this.ctx.stroke();
        }
      }
    }

    // Draw action-potential spikes
    for (let sp of this.spikes) {
      let sx, sy;
      if (sp.state === 'in_flight') {
        const x1 = this.getNodeX(sp.fromGx);
        const y1 = this.getNodeY(sp.fromGy);
        const x2 = this.getNodeX(sp.toGx);
        const y2 = this.getNodeY(sp.toGy);
        sx = x1 + (x2 - x1) * sp.progress;
        sy = y1 + (y2 - y1) * sp.progress;
      } else {
        sx = this.getNodeX(sp.gx);
        sy = this.getNodeY(sp.gy);
      }

      this.ctx.save();
      this.ctx.shadowColor = '#c084fc';
      this.ctx.shadowBlur = 10;
      this.ctx.fillStyle = '#c084fc';
      this.ctx.beginPath();
      this.ctx.arc(sx, sy, 5.5, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();
    }

    // Draw 4x4 Neuromorphic cores with LIF membrane potential rings
    for (let n of this.neurons) {
      const nx = this.getNodeX(n.x);
      const ny = this.getNodeY(n.y);

      this.ctx.save();
      this.ctx.fillStyle = '#1e293b';
      this.ctx.strokeStyle = '#a855f7';
      this.ctx.lineWidth = 2;
      this.ctx.beginPath();
      this.ctx.roundRect(nx - 18, ny - 18, 36, 36, 6);
      this.ctx.fill();
      this.ctx.stroke();

      // Membrane potential arc ring around neuron core
      const frac = Math.min(1.0, n.vm / n.thresh);
      this.ctx.strokeStyle = frac > 0.75 ? '#22c55e' : '#a855f7';
      this.ctx.lineWidth = 3;
      this.ctx.beginPath();
      this.ctx.arc(nx, ny, 23, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * frac);
      this.ctx.stroke();
      this.ctx.restore();

      this.ctx.fillStyle = '#e2e8f0';
      this.ctx.font = 'bold 9px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(`${Math.floor(n.vm)}mV`, nx, ny);
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
    document.getElementById('snnScore').textContent = this.score;
    document.getElementById('snnFirings').textContent = `${this.neuronFirings}`;
    document.getElementById('snnWave').textContent = `Wave ${this.wave}`;

    // AER Load
    const loadPct = Math.min(100, Math.floor((this.aerBufferCount / 34) * 100));
    document.getElementById('snnAerLoad').textContent = `${loadPct}%`;

    // STDP energy bar
    const bar = document.getElementById('stdpEnergyBar');
    const text = document.getElementById('stdpEnergyText');
    bar.style.width = `${this.stdpEnergy}%`;
    if (this.stdpActive) {
      text.textContent = `⚡ SURGE ACTIVE (${this.stdpTimer.toFixed(1)}s)`;
      bar.style.background = '#f59e0b';
    } else {
      text.textContent = this.stdpEnergy >= 100 ? '100% READY' : `${Math.floor(this.stdpEnergy)}% CHARGING`;
      bar.style.background = 'linear-gradient(90deg, #7c3aed, #a855f7)';
    }

    // AER Headroom bar
    const aerBar = document.getElementById('aerBar');
    const aerText = document.getElementById('aerStatusText');
    aerBar.style.width = `${loadPct}%`;
    aerBar.style.background = loadPct > 75 ? '#ef4444' : (loadPct > 45 ? '#f59e0b' : '#22c55e');
    aerText.textContent = `${loadPct}% (${loadPct > 75 ? 'CONGESTION' : 'HEALTHY'})`;
  }

  triggerGameOver() {
    this.isRunning = false;
    document.getElementById('snnModalTitle').textContent = 'AER BUFFER OVERFLOW!';
    document.getElementById('snnModalSummary').innerHTML = `
      Synchronous action-potential spike bursts exceeded AER ingress FIFO limits!<br><br>
      <b>Final Wave:</b> Wave ${this.wave} | <b>Neuron Firings:</b> ${this.neuronFirings} | <b>Score:</b> ${this.score} pts
    `;
    document.getElementById('snnOverModal').style.display = 'flex';
  }
}

let snnGame = null;

function startSnnGame() {
  if (!snnGame) snnGame = new NeuromorphicGame();
  snnGame.start();
}

function restartSnnGame() {
  if (snnGame) snnGame.start();
}

function triggerStdpSurge() {
  if (snnGame && snnGame.isRunning) {
    snnGame.triggerStdp();
  }
}

function setSnnProtocol(proto) {
  if (snnGame) snnGame.protocol = proto;
}

function toggleSnnSound() {
  if (snnGame) {
    snnGame.audio.enabled = !snnGame.audio.enabled;
    document.getElementById('snnSoundBtn').textContent = snnGame.audio.enabled ? '🔊 Sound: ON' : '🔇 Sound: OFF';
  }
}

function toggleSnnPause() {
  if (snnGame) snnGame.isPaused = !snnGame.isPaused;
}

// Global Animation Loop
function snnLoop(now) {
  if (snnGame && snnGame.isRunning) {
    const dt = Math.min(0.05, (now - snnGame.lastTime) / 1000);
    snnGame.lastTime = now;
    snnGame.update(dt);
    snnGame.render();
  }
  requestAnimationFrame(snnLoop);
}
requestAnimationFrame(snnLoop);

// Keyboard controls
window.addEventListener('keydown', (e) => {
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
  if (e.code === 'Space' || e.code === 'KeyS') {
    if (snnGame && snnGame.isRunning) {
      triggerStdpSurge();
      e.preventDefault();
    }
  }
});

// Hall of Fame Leaderboard & GitHub Submission Integration
function saveSnnRecord() {
  if (!snnGame) return;
  const nameInput = document.getElementById('snnCallsign').value.trim() || 'Neuromorphic Pioneer';
  const orgInput = document.getElementById('snnOrg').value.trim() || 'Silicon Lab';

  const record = {
    name: nameInput,
    org: orgInput,
    track: `Neuromorphic Nexus (Wave ${snnGame.wave})`,
    score: snnGame.score,
    accuracy: snnGame.neuronFirings,
    date: new Date().toISOString().slice(0, 10),
    certId: `SNN-WAVE-${snnGame.wave}-${Math.floor(Math.random() * 900 + 100)}`,
    type: 'neuromorphic'
  };

  try {
    const key = 'noc_leaderboard_records';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push(record);
    localStorage.setItem(key, JSON.stringify(existing));
    const confirmEl = document.getElementById('snnSaveConfirm');
    if (confirmEl) confirmEl.style.display = 'block';
  } catch (err) {
    console.error('Failed to save to localStorage', err);
  }
}

function submitSnnToGithub() {
  if (!snnGame) return;
  const nameInput = document.getElementById('snnCallsign').value.trim() || 'Neuromorphic Pioneer';
  const orgInput = document.getElementById('snnOrg').value.trim() || 'Silicon Lab';

  const title = encodeURIComponent(`[Leaderboard Submission] Neuromorphic Nexus - ${nameInput} (${snnGame.score} pts)`);
  const body = encodeURIComponent([
    `### 🧠 Neuromorphic Nexus: Spiking Neural NoC Score Submission`,
    `- **Architect / Callsign**: ${nameInput}`,
    `- **Institution / Org**: ${orgInput}`,
    `- **Wave Reached**: Wave ${snnGame.wave}`,
    `- **Neuron Action Potentials**: ${snnGame.neuronFirings}`,
    `- **Synaptic Spikes Delivered**: ${snnGame.totalSpikesDelivered}`,
    `- **Total Score**: ${snnGame.score} pts`,
    `- **Submission Timestamp**: ${new Date().toISOString()}`,
    ``,
    `\`\`\`json`,
    JSON.stringify({
      type: "neuromorphic",
      player: nameInput,
      org: orgInput,
      score: snnGame.score,
      wave: snnGame.wave,
      firings: snnGame.neuronFirings,
      delivered: snnGame.totalSpikesDelivered,
      date: new Date().toISOString().slice(0, 10),
      certId: `SNN-WAVE-${snnGame.wave}-${Math.floor(Math.random() * 900 + 100)}`
    }, null, 2),
    `\`\`\``
  ].join('\n'));

  window.open(`https://github.com/network-on-chip/learning/issues/new?title=${title}&body=${body}`, '_blank');
}
</script>
