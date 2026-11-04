# 🏓 Deflection Duel: Bufferless NoC Blitz

Eliminate input buffers entirely and master zero-buffer silicon routing! In bufferless Networks-on-Chip (such as **BLESS**, **CHIPPER**, and **MinBD**), routers discard all input FIFO queues—cutting silicon router area and static leakage power by up to 60%. However, because flits cannot be buffered, when two flits contend for the same productive output wire, one wins and the other is **deflected** onto an alternative free port!

Prevent livelock, manage Hop-to-Live (HTL) budgets, deploy **Golden Flit** arbitration guarantees, and sustain maximum throughput without packet drops. Your high scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="deflectionStartBtn" class="noc-sim-btn" onclick="startDeflectionGame()">▶ Start Duel</button>
    <button id="goldenTicketBtn" class="noc-sim-btn" onclick="triggerGoldenTicket()" style="background:#eab308; color:#0f172a !important; font-weight:800; border:none; box-shadow:0 0 14px rgba(234,179,8,0.5);">⭐ Golden Flit Surge (Space / G)</button>

    <label><b>Arbitration Policy:</b>
      <select id="deflectionPolicySelect" class="noc-sim-select" onchange="setDeflectionPolicy(this.value)">
        <option value="age_priority">Oldest-First (BLESS Priority)</option>
        <option value="golden_flit">Golden Flit Protocol (Livelock-Free)</option>
        <option value="random_deflect">Random Arbitration (Pure Chaos)</option>
      </select>
    </label>

    <button id="deflectionSoundBtn" class="noc-sim-btn secondary" onclick="toggleDeflectionSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleDeflectionPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="deflectionScore">0</span></span>
      <span style="color:#22c55e;">Delivered: <span id="deflectionDelivered">0</span></span>
      <span style="color:#f59e0b;">Deflections: <span id="deflectionCount">0</span></span>
      <span style="color:#ef4444;" id="deflectionWave">Wave 1</span>
    </div>
  </div>

  <!-- Bufferless Invariants HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#eab308;">⭐ Golden Flit Quantum Energy:</span>
        <span id="goldenEnergyText" style="font-weight:700; color:#eab308;">100% READY</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(234,179,8,0.15); border-radius:4px; overflow:hidden;">
        <div id="goldenEnergyBar" style="width:100%; height:100%; background:linear-gradient(90deg, #ca8a04, #eab308); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">🔄 Mesh Livelock Health (HTL &lt; 28):</span>
        <span id="livelockHealthText" style="font-weight:700; color:#38bdf8;">100% (Zero Drops)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="livelockHealthBar" style="width:100%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="deflectionCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="deflectionOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="deflectionModalIcon">💥</div>
      <h2 id="deflectionModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">LIVELOCK BUFFER COLLAPSE!</h2>
      <p id="deflectionModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Flits exceeded 28 hops in circular deflection orbits without reaching destinations!
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Bufferless Pilot Callsign:</label>
        <input type="text" id="deflectionCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. BLESS Architect" value="Deflection Ace">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="deflectionOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. CMU SAFARI / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveDeflectionRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitDeflectionToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartDeflectionGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="deflectionSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in local Hall of Fame!
      </div>
    </div>
  </div>

  <div id="deflectionInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">🏓 Bufferless NoC Microarchitecture &amp; Deflection Rules:</strong>
    <ul style="margin:0.4rem 0 0 1.2rem; padding:0;">
      <li><strong>Zero Buffering ("Hot Potato"):</strong> Routers have zero input FIFOs. Every flit arriving at an input port must leave in the exact same cycle on one of the four output ports ($N, S, E, W$).</li>
      <li><strong>Contention &amp; Deflection:</strong> When multiple flits request the same shortest-path output port, arbitration selects 1 winner. Losing flits are <em>deflected</em> to unrequested free links.</li>
      <li><strong>Livelock Freedom (Golden Flits):</strong> Pure random deflection can cause infinite circulating loops (livelock). To prove livelock-freedom, architectures like BLESS/CHIPPER assign strict age priority or designate periodic <em>Golden Flits</em> that can never be deflected.</li>
      <li><strong>Hop-to-Live (HTL):</strong> Every deflection increments a flit's hop count. If $HTL \ge 28$, the packet is dropped due to excessive delay, damaging mesh integrity.</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Deflection Duel
class DeflectionAudio {
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

  playDeflect() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(380, t);
      osc.frequency.exponentialRampToValueAtTime(180, t + 0.08);
      gain.gain.setValueAtTime(0.12, t);
      gain.gain.linearRampToValueAtTime(0.01, t + 0.08);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.08);
    } catch (e) {}
  }

  playDeliver() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      [523.25, 659.25, 783.99].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, t + idx * 0.04);
        gain.gain.setValueAtTime(0.1, t + idx * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, t + idx * 0.04 + 0.15);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t + idx * 0.04);
        osc.stop(t + idx * 0.04 + 0.15);
      });
    } catch (e) {}
  }

  playGoldenSurge() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      [440, 554.37, 659.25, 880].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, t + idx * 0.05);
        gain.gain.setValueAtTime(0.15, t + idx * 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, t + idx * 0.05 + 0.28);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t + idx * 0.05);
        osc.stop(t + idx * 0.05 + 0.28);
      });
    } catch (e) {}
  }

  playDrop() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(140, t);
      osc.frequency.linearRampToValueAtTime(60, t + 0.2);
      gain.gain.setValueAtTime(0.2, t);
      gain.gain.linearRampToValueAtTime(0.01, t + 0.2);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.2);
    } catch (e) {}
  }
}

// 4x4 Bufferless Mesh Simulation Engine
class DeflectionGame {
  constructor() {
    this.canvas = document.getElementById('deflectionCanvas');
    this.ctx = this.canvas.getContext('2d');
    this.audio = new DeflectionAudio();

    this.gridW = 4;
    this.gridH = 4;
    this.nodeSpacingX = 125;
    this.nodeSpacingY = 95;
    this.offsetX = 120;
    this.offsetY = 85;

    this.flits = [];
    this.particles = [];
    this.score = 0;
    this.deliveredCount = 0;
    this.deflectionCount = 0;
    this.droppedCount = 0;
    this.wave = 1;
    this.waveTimer = 20.0;
    this.goldenEnergy = 100.0;
    this.goldenActive = false;
    this.goldenTimer = 0.0;
    this.policy = 'age_priority';

    this.isRunning = false;
    this.isPaused = false;
    this.lastTime = performance.now();
    this.injectTimer = 0;
    this.nextFlitId = 1;
  }

  start() {
    this.audio.init();
    this.flits = [];
    this.particles = [];
    this.score = 0;
    this.deliveredCount = 0;
    this.deflectionCount = 0;
    this.droppedCount = 0;
    this.wave = 1;
    this.waveTimer = 20.0;
    this.goldenEnergy = 100.0;
    this.goldenActive = false;
    this.goldenTimer = 0.0;
    this.isRunning = true;
    this.isPaused = false;

    document.getElementById('deflectionOverModal').style.display = 'none';
    document.getElementById('deflectionStartBtn').textContent = '🔄 Restart';
    this.lastTime = performance.now();

    // Initial flit injections
    for (let i = 0; i < 4; i++) {
      this.injectFlit();
    }
  }

  injectFlit() {
    const sx = Math.floor(Math.random() * this.gridW);
    const sy = Math.floor(Math.random() * this.gridH);
    let dx = Math.floor(Math.random() * this.gridW);
    let dy = Math.floor(Math.random() * this.gridH);
    while (dx === sx && dy === sy) {
      dx = Math.floor(Math.random() * this.gridW);
      dy = Math.floor(Math.random() * this.gridH);
    }

    const flit = {
      id: this.nextFlitId++,
      gx: sx,
      gy: sy,
      fromGx: sx,
      fromGy: sy,
      toGx: sx,
      toGy: sy,
      dstX: dx,
      dstY: dy,
      progress: 1.0, // 1.0 = at node, needs route
      state: 'at_node', // 'at_node' or 'in_flight'
      hops: 0,
      age: 0,
      isGolden: this.goldenActive,
      color: this.goldenActive ? '#eab308' : (Math.random() < 0.5 ? '#38bdf8' : '#a855f7')
    };
    this.flits.push(flit);
  }

  update(dt) {
    if (!this.isRunning || this.isPaused) return;

    this.waveTimer -= dt;
    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 22.0;
      this.score += 250 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 60, `WAVE ${this.wave} INJECTION BOOST!`, '#22c55e');
    }

    // Golden ticket regeneration & countdown
    if (this.goldenActive) {
      this.goldenTimer -= dt;
      this.goldenEnergy = Math.max(0, (this.goldenTimer / 5.0) * 100);
      if (this.goldenTimer <= 0) {
        this.goldenActive = false;
        this.goldenEnergy = 0;
      }
    } else {
      this.goldenEnergy = Math.min(100, this.goldenEnergy + dt * 12.0);
    }

    // Packet injection rate scales with wave
    this.injectTimer += dt;
    const injectInterval = Math.max(0.45, 1.4 - this.wave * 0.12);
    if (this.injectTimer >= injectInterval && this.flits.length < 18 + this.wave * 3) {
      this.injectTimer = 0;
      this.injectFlit();
    }

    // Step 1: Advance in-flight flits
    const speed = 1.35 + this.wave * 0.08;
    for (let i = this.flits.length - 1; i >= 0; i--) {
      const f = this.flits[i];
      f.age += dt;

      if (f.state === 'in_flight') {
        f.progress += dt * speed;
        if (f.progress >= 1.0) {
          f.progress = 1.0;
          f.gx = f.toGx;
          f.gy = f.toGy;
          f.state = 'at_node';

          // Check if arrived at destination
          if (f.gx === f.dstX && f.gy === f.dstY) {
            this.flits.splice(i, 1);
            this.deliveredCount++;
            const hopBonus = Math.max(10, 80 - f.hops * 4);
            this.score += 50 + hopBonus;
            this.audio.playDeliver();
            this.addTextParticle(this.getNodeX(f.gx), this.getNodeY(f.gy), `+${50 + hopBonus}`, '#4ade80');
            continue;
          }

          // Check hop limit (livelock detection)
          f.hops++;
          if (f.hops >= 28) {
            this.flits.splice(i, 1);
            this.droppedCount++;
            this.audio.playDrop();
            this.addTextParticle(this.getNodeX(f.gx), this.getNodeY(f.gy), 'LIVELOCK DROP!', '#ef4444');
            if (this.droppedCount >= 5) {
              this.triggerGameOver();
              return;
            }
          }
        }
      }
    }

    // Step 2: Bufferless Router Arbitration for flits at nodes
    const nodeGroups = {};
    for (let f of this.flits) {
      if (f.state === 'at_node') {
        const key = `${f.gx},${f.gy}`;
        if (!nodeGroups[key]) nodeGroups[key] = [];
        nodeGroups[key].push(f);
      }
    }

    for (let key in nodeGroups) {
      const flitsAtNode = nodeGroups[key];
      this.arbitrateNode(flitsAtNode);
    }

    // Update floating text particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.y -= dt * 30;
      p.life -= dt;
      if (p.life <= 0) this.particles.splice(i, 1);
    }

    this.updateHUD();
  }

  arbitrateNode(flitsAtNode) {
    if (flitsAtNode.length === 0) return;
    const gx = flitsAtNode[0].gx;
    const gy = flitsAtNode[0].gy;

    // Available output directions: N, S, E, W (omitting boundary links)
    const validDirs = [];
    if (gy > 0) validDirs.push({ dir: 'N', toX: gx, toY: gy - 1 });
    if (gy < this.gridH - 1) validDirs.push({ dir: 'S', toX: gx, toY: gy + 1 });
    if (gx < this.gridW - 1) validDirs.push({ dir: 'E', toX: gx + 1, toY: gy });
    if (gx > 0) validDirs.push({ dir: 'W', toX: gx - 1, toY: gy });

    // Determine ideal productive direction for each flit (Dimension-Order Routing preference)
    for (let f of flitsAtNode) {
      let ideal = null;
      if (f.dstX > f.gx && gx < this.gridW - 1) ideal = 'E';
      else if (f.dstX < f.gx && gx > 0) ideal = 'W';
      else if (f.dstY > f.gy && gy < this.gridH - 1) ideal = 'S';
      else if (f.dstY < f.gy && gy > 0) ideal = 'N';

      f.idealDir = ideal || (validDirs.length > 0 ? validDirs[0].dir : 'E');
    }

    // Sort flits by priority based on chosen arbitration policy
    if (this.policy === 'golden_flit') {
      flitsAtNode.sort((a, b) => (b.isGolden ? 1 : 0) - (a.isGolden ? 1 : 0) || b.age - a.age);
    } else if (this.policy === 'age_priority') {
      flitsAtNode.sort((a, b) => b.age - a.age);
    } else {
      // random_deflect
      flitsAtNode.sort(() => Math.random() - 0.5);
    }

    // Allocate output ports without buffering
    const assignedPorts = new Set();
    const freePorts = [...validDirs];

    for (let f of flitsAtNode) {
      // Check if ideal port is available
      const idealIdx = freePorts.findIndex(p => p.dir === f.idealDir);
      if (idealIdx !== -1) {
        const port = freePorts.splice(idealIdx, 1)[0];
        f.toGx = port.toX;
        f.toGy = port.toY;
        f.fromGx = f.gx;
        f.fromGy = f.gy;
        f.progress = 0;
        f.state = 'in_flight';
      } else if (freePorts.length > 0) {
        // DEFLECT! Assign any remaining free port
        const deflectedPort = freePorts.pop();
        f.toGx = deflectedPort.toX;
        f.toGy = deflectedPort.toY;
        f.fromGx = f.gx;
        f.fromGy = f.gy;
        f.progress = 0;
        f.state = 'in_flight';
        this.deflectionCount++;
        this.audio.playDeflect();
        this.addTextParticle(this.getNodeX(f.gx), this.getNodeY(f.gy), 'DEFLECT', '#f59e0b');
      } else {
        // All router links saturated; flit stalls on local cycle
        f.age += 1.0;
      }
    }
  }

  getNodeX(gx) { return this.offsetX + gx * this.nodeSpacingX; }
  getNodeY(gy) { return this.offsetY + gy * this.nodeSpacingY; }

  render() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw mesh interconnect links
    this.ctx.lineWidth = 3;
    for (let y = 0; y < this.gridH; y++) {
      for (let x = 0; x < this.gridW; x++) {
        const nx = this.getNodeX(x);
        const ny = this.getNodeY(y);

        if (x < this.gridW - 1) {
          const nextX = this.getNodeX(x + 1);
          this.ctx.strokeStyle = '#1e293b';
          this.ctx.beginPath();
          this.ctx.moveTo(nx, ny);
          this.ctx.lineTo(nextX, ny);
          this.ctx.stroke();
        }
        if (y < this.gridH - 1) {
          const nextY = this.getNodeY(y + 1);
          this.ctx.strokeStyle = '#1e293b';
          this.ctx.beginPath();
          this.ctx.moveTo(nx, ny);
          this.ctx.lineTo(nx, nextY);
          this.ctx.stroke();
        }
      }
    }

    // Draw active flits traveling along wires
    for (let f of this.flits) {
      let fx, fy;
      if (f.state === 'in_flight') {
        const x1 = this.getNodeX(f.fromGx);
        const y1 = this.getNodeY(f.fromGy);
        const x2 = this.getNodeX(f.toGx);
        const y2 = this.getNodeY(f.toGy);
        fx = x1 + (x2 - x1) * f.progress;
        fy = y1 + (y2 - y1) * f.progress;
      } else {
        fx = this.getNodeX(f.gx);
        fy = this.getNodeY(f.gy);
      }

      // Flit glow
      this.ctx.save();
      const radius = f.isGolden ? 8 : (f.hops > 14 ? 7 : 6);
      const color = f.isGolden ? '#eab308' : (f.hops > 16 ? '#ef4444' : f.color);

      this.ctx.shadowColor = color;
      this.ctx.shadowBlur = f.isGolden ? 16 : 8;
      this.ctx.fillStyle = color;
      this.ctx.beginPath();
      this.ctx.arc(fx, fy, radius, 0, Math.PI * 2);
      this.ctx.fill();

      // Destination indicator line for selected flits
      if (f.isGolden || f.hops > 18) {
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 1;
        this.ctx.setLineDash([2, 4]);
        this.ctx.beginPath();
        this.ctx.moveTo(fx, fy);
        this.ctx.lineTo(this.getNodeX(f.dstX), this.getNodeY(f.dstY));
        this.ctx.stroke();
        this.ctx.setLineDash([]);
      }
      this.ctx.restore();
    }

    // Draw 4x4 router nodes
    for (let y = 0; y < this.gridH; y++) {
      for (let x = 0; x < this.gridW; x++) {
        const nx = this.getNodeX(x);
        const ny = this.getNodeY(y);

        this.ctx.fillStyle = '#1e293b';
        this.ctx.strokeStyle = '#38bdf8';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.roundRect(nx - 18, ny - 18, 36, 36, 6);
        this.ctx.fill();
        this.ctx.stroke();

        this.ctx.fillStyle = '#94a3b8';
        this.ctx.font = '10px "JetBrains Mono", monospace';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(`R${x}${y}`, nx, ny);
      }
    }

    // Draw floating particles
    for (let p of this.particles) {
      this.ctx.save();
      this.ctx.fillStyle = p.color;
      this.ctx.font = 'bold 11px "JetBrains Mono", monospace';
      this.ctx.textAlign = 'center';
      this.ctx.shadowColor = p.color;
      this.ctx.shadowBlur = 6;
      this.ctx.fillText(p.text, p.x, p.y);
      this.ctx.restore();
    }
  }

  addTextParticle(x, y, text, color) {
    this.particles.push({ x, y, text, color, life: 1.2 });
  }

  updateHUD() {
    document.getElementById('deflectionScore').textContent = this.score;
    document.getElementById('deflectionDelivered').textContent = this.deliveredCount;
    document.getElementById('deflectionCount').textContent = this.deflectionCount;
    document.getElementById('deflectionWave').textContent = `Wave ${this.wave}`;

    // Golden ticket energy
    const energyBar = document.getElementById('goldenEnergyBar');
    const energyText = document.getElementById('goldenEnergyText');
    energyBar.style.width = `${this.goldenEnergy}%`;
    if (this.goldenActive) {
      energyText.textContent = `⭐ ACTIVE (${this.goldenTimer.toFixed(1)}s)`;
      energyBar.style.background = '#f59e0b';
    } else {
      energyText.textContent = `${Math.floor(this.goldenEnergy)}% READY`;
      energyBar.style.background = 'linear-gradient(90deg, #ca8a04, #eab308)';
    }

    // Livelock drop health
    const health = Math.max(0, 100 - this.droppedCount * 20);
    const healthBar = document.getElementById('livelockHealthBar');
    const healthText = document.getElementById('livelockHealthText');
    healthBar.style.width = `${health}%`;
    healthBar.style.background = health > 60 ? '#22c55e' : (health > 30 ? '#f59e0b' : '#ef4444');
    healthText.textContent = `${health}% (${this.droppedCount} drops / max 5)`;
  }

  triggerGameOver() {
    this.isRunning = false;
    document.getElementById('deflectionModalTitle').textContent = 'LIVELOCK BUFFER COLLAPSE!';
    document.getElementById('deflectionModalSummary').innerHTML = `
      5 packets exceeded the 28-hop livelock threshold!<br><br>
      <b>Final Wave:</b> Wave ${this.wave} | <b>Packets Delivered:</b> ${this.deliveredCount} | <b>Score:</b> ${this.score} pts
    `;
    document.getElementById('deflectionOverModal').style.display = 'flex';
  }
}

let deflectionGame = null;

function startDeflectionGame() {
  if (!deflectionGame) deflectionGame = new DeflectionGame();
  deflectionGame.start();
}

function restartDeflectionGame() {
  if (deflectionGame) deflectionGame.start();
}

function triggerGoldenTicket() {
  if (!deflectionGame || !deflectionGame.isRunning) return;
  if (deflectionGame.goldenEnergy >= 100 && !deflectionGame.goldenActive) {
    deflectionGame.goldenActive = true;
    deflectionGame.goldenTimer = 5.0;
    deflectionGame.audio.playGoldenSurge();
    for (let f of deflectionGame.flits) {
      f.isGolden = true;
    }
    deflectionGame.addTextParticle(deflectionGame.canvas.width / 2, 70, '⭐ GOLDEN FLIT SURGE ENGAGED!', '#eab308');
  }
}

function setDeflectionPolicy(pol) {
  if (deflectionGame) deflectionGame.policy = pol;
}

function toggleDeflectionSound() {
  if (deflectionGame) {
    deflectionGame.audio.enabled = !deflectionGame.audio.enabled;
    document.getElementById('deflectionSoundBtn').textContent = deflectionGame.audio.enabled ? '🔊 Sound: ON' : '🔇 Sound: OFF';
  }
}

function toggleDeflectionPause() {
  if (deflectionGame) deflectionGame.isPaused = !deflectionGame.isPaused;
}

// Global Animation Loop
function deflectionLoop(now) {
  if (deflectionGame && deflectionGame.isRunning) {
    const dt = Math.min(0.05, (now - deflectionGame.lastTime) / 1000);
    deflectionGame.lastTime = now;
    deflectionGame.update(dt);
    deflectionGame.render();
  }
  requestAnimationFrame(deflectionLoop);
}
requestAnimationFrame(deflectionLoop);

// Keyboard controls
window.addEventListener('keydown', (e) => {
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
  if (e.code === 'Space' || e.code === 'KeyG') {
    if (deflectionGame && deflectionGame.isRunning) {
      triggerGoldenTicket();
      e.preventDefault();
    }
  }
});

// Hall of Fame Leaderboard & GitHub Submission Integration
function saveDeflectionRecord() {
  if (!deflectionGame) return;
  const nameInput = document.getElementById('deflectionCallsign').value.trim() || 'Deflection Ace';
  const orgInput = document.getElementById('deflectionOrg').value.trim() || 'Silicon Lab';

  const record = {
    name: nameInput,
    org: orgInput,
    track: `Deflection Duel (Wave ${deflectionGame.wave})`,
    score: deflectionGame.score,
    accuracy: deflectionGame.deliveredCount,
    date: new Date().toISOString().slice(0, 10),
    certId: `DEFLECT-WAVE-${deflectionGame.wave}-${Math.floor(Math.random() * 900 + 100)}`,
    type: 'deflection'
  };

  try {
    const key = 'noc_leaderboard_records';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push(record);
    localStorage.setItem(key, JSON.stringify(existing));
    const confirmEl = document.getElementById('deflectionSaveConfirm');
    if (confirmEl) confirmEl.style.display = 'block';
  } catch (err) {
    console.error('Failed to save to localStorage', err);
  }
}

function submitDeflectionToGithub() {
  if (!deflectionGame) return;
  const nameInput = document.getElementById('deflectionCallsign').value.trim() || 'Deflection Ace';
  const orgInput = document.getElementById('deflectionOrg').value.trim() || 'Silicon Lab';

  const title = encodeURIComponent(`[Leaderboard Submission] Deflection Duel - ${nameInput} (${deflectionGame.score} pts)`);
  const body = encodeURIComponent([
    `### 🏓 Deflection Duel: Bufferless NoC Blitz Score Submission`,
    `- **Architect / Callsign**: ${nameInput}`,
    `- **Institution / Org**: ${orgInput}`,
    `- **Wave Reached**: Wave ${deflectionGame.wave}`,
    `- **Packets Delivered**: ${deflectionGame.deliveredCount}`,
    `- **Deflection Count**: ${deflectionGame.deflectionCount}`,
    `- **Total Score**: ${deflectionGame.score} pts`,
    `- **Submission Timestamp**: ${new Date().toISOString()}`,
    ``,
    `\`\`\`json`,
    JSON.stringify({
      type: "deflection",
      player: nameInput,
      org: orgInput,
      score: deflectionGame.score,
      wave: deflectionGame.wave,
      delivered: deflectionGame.deliveredCount,
      deflections: deflectionGame.deflectionCount,
      date: new Date().toISOString().slice(0, 10),
      certId: `DEFLECT-WAVE-${deflectionGame.wave}-${Math.floor(Math.random() * 900 + 100)}`
    }, null, 2),
    `\`\`\``
  ].join('\n'));

  window.open(`https://github.com/network-on-chip/learning/issues/new?title=${title}&body=${body}`, '_blank');
}
</script>
