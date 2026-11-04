# 🛡️ Fault Defender: Silicon Resilience & BIST

Protect multi-core silicon from aging, physical interconnect failure, and radiation upsets! In advanced FinFET and GAA nodes (sub-3nm), deep-submicron interconnects suffer from **Electromigration (EM)**, **Time-Dependent Dielectric Breakdown (TDDB)**, and **Single-Event Upsets (SEU)** from cosmic ray strikes. 

When interconnect links or router ports permanently fail, standard deterministic routing (such as XY) drives packets into dead-ends, causing massive data corruption or fatal system deadlock. Master **Built-In Self-Test (BIST)** diagnostics, deploy **Fault-Ring detour routing**, activate **Reconfigurable Hot-Spare links**, and safeguard mission-critical packet streams. High scores can be directly inscribed onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="faultStartBtn" class="noc-sim-btn" onclick="startFaultGame()">▶ Start Resilience Defense</button>
    <button id="bistScanBtn" class="noc-sim-btn" onclick="fireBistScan()" style="background:#0284c7; border:none; box-shadow:0 0 14px rgba(2,132,199,0.5);">📡 BIST Diagnostic Pulse (Space / B)</button>

    <label><b>Resilience Protocol:</b>
      <select id="faultModeSelect" class="noc-sim-select" onchange="setFaultProtocol(this.value)">
        <option value="fault_ring">Fault-Ring Detour (Perimeter Routing)</option>
        <option value="spare_links">Hot-Spare Redundant Links (Hardware Bypass)</option>
        <option value="naive_xy">Naive XY (Unprotected · High Failure Risk)</option>
      </select>
    </label>

    <button id="faultSoundBtn" class="noc-sim-btn secondary" onclick="toggleFaultSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleFaultPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="faultScore">0</span></span>
      <span style="color:#22c55e;">Rescued: <span id="faultRescued">0</span></span>
      <span style="color:#ef4444;">Lost: <span id="faultLost">0</span></span>
      <span style="color:#f59e0b;" id="faultWave">Wave 1</span>
    </div>
  </div>

  <!-- Silicon Integrity & BIST Diagnostic HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">📡 BIST Diagnostic Radar Reservoir:</span>
        <span id="bistChargeText" style="font-weight:700; color:#38bdf8;">100% READY</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="bistChargeBar" style="width:100%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#22c55e;">🛡️ Silicon Substrate Reliability SLA:</span>
        <span id="siliconHealthText" style="font-weight:700; color:#22c55e;">100% HEALTHY</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(34,197,94,0.15); border-radius:4px; overflow:hidden;">
        <div id="siliconHealthBar" style="width:100%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="faultCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="faultOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="faultModalIcon">💥</div>
      <h2 id="faultModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">SILICON SUBSTRATE BREAKDOWN!</h2>
      <p id="faultModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Cascading link ruptures caused catastrophic packet loss exceeding SLA reliability limits!
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Resilience Architect Callsign:</label>
        <input type="text" id="faultCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Reliability Guru" value="Silicon Defender">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="faultOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. NASA JPL / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveFaultRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitFaultToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartFaultGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="faultSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in local Hall of Fame!
      </div>
    </div>
  </div>

  <div id="faultInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">🛡️ Fault-Tolerant Routing Architecture &amp; BIST Mechanics:</strong>
    <ul style="margin:0.4rem 0 0 1.2rem; padding:0;">
      <li><strong>Electromigration &amp; Link Fractures:</strong> Thermal cycling and continuous current density cause link voids. Broken links appear with red spark indicators. Packets attempting to cross broken wires are destroyed!</li>
      <li><strong>Built-In Self-Test (BIST Pulse):</strong> Press <code>Space</code> or <code>B</code> to launch an active diagnostic scan. BIST probes every wire and router port, immediately flagging damaged channels in routing tables to prevent premature packet dispatch.</li>
      <li><strong>Fault-Ring Routing:</strong> Routers adjacent to a damaged wire form a perimeter ring. Packets encountering the fault zone are diverted clockwise around the barrier until reconnecting with the original dimension path.</li>
      <li><strong>Hot-Spare Interconnects:</strong> Redundant silicon metal layers can be engaged to route around severed primary wires with zero packet latency penalty.</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Fault Defender
class FaultAudio {
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

  playSpark() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(650, t);
      osc.frequency.exponentialRampToValueAtTime(80, t + 0.15);
      gain.gain.setValueAtTime(0.18, t);
      gain.gain.linearRampToValueAtTime(0.01, t + 0.15);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.15);
    } catch (e) {}
  }

  playBist() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(320, t);
      osc.frequency.exponentialRampToValueAtTime(960, t + 0.22);
      gain.gain.setValueAtTime(0.14, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.22);
    } catch (e) {}
  }

  playDetour() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      [440, 659.25].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, t + idx * 0.05);
        gain.gain.setValueAtTime(0.1, t + idx * 0.05);
        gain.gain.linearRampToValueAtTime(0.001, t + idx * 0.05 + 0.14);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t + idx * 0.05);
        osc.stop(t + idx * 0.05 + 0.14);
      });
    } catch (e) {}
  }

  playDeliver() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      [523.25, 783.99].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, t + idx * 0.04);
        gain.gain.setValueAtTime(0.1, t + idx * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, t + idx * 0.04 + 0.18);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t + idx * 0.04);
        osc.stop(t + idx * 0.04 + 0.18);
      });
    } catch (e) {}
  }

  playDestroy() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(160, t);
      osc.frequency.linearRampToValueAtTime(40, t + 0.25);
      gain.gain.setValueAtTime(0.25, t);
      gain.gain.linearRampToValueAtTime(0.01, t + 0.25);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.25);
    } catch (e) {}
  }
}

// 4x4 Fault-Tolerant Silicon Mesh Engine
class FaultGame {
  constructor() {
    this.canvas = document.getElementById('faultCanvas');
    this.ctx = this.canvas.getContext('2d');
    this.audio = new FaultAudio();

    this.gridW = 4;
    this.gridH = 4;
    this.nodeSpacingX = 125;
    this.nodeSpacingY = 95;
    this.offsetX = 120;
    this.offsetY = 85;

    this.packets = [];
    this.brokenLinks = new Set(); // Key: 'x1,y1-x2,y2'
    this.sparesActive = new Set();
    this.particles = [];
    this.bistWaves = [];

    this.score = 0;
    this.rescuedCount = 0;
    this.lostCount = 0;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.bistCharge = 100.0;
    this.health = 100.0;
    this.protocol = 'fault_ring';

    this.isRunning = false;
    this.isPaused = false;
    this.lastTime = performance.now();
    this.injectTimer = 0;
    this.faultInjectTimer = 0;
    this.nextPacketId = 1;
  }

  start() {
    this.audio.init();
    this.packets = [];
    this.brokenLinks.clear();
    this.sparesActive.clear();
    this.particles = [];
    this.bistWaves = [];

    this.score = 0;
    this.rescuedCount = 0;
    this.lostCount = 0;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.bistCharge = 100.0;
    this.health = 100.0;
    this.isRunning = true;
    this.isPaused = false;

    document.getElementById('faultOverModal').style.display = 'none';
    document.getElementById('faultStartBtn').textContent = '🔄 Restart';
    this.lastTime = performance.now();

    // Inject initial link fault
    this.injectRandomFault();

    // Initial packet dispatch
    for (let i = 0; i < 3; i++) {
      this.injectPacket();
    }
  }

  getLinkKey(x1, y1, x2, y2) {
    if (x1 > x2 || (x1 === x2 && y1 > y2)) {
      return `${x2},${y2}-${x1},${y1}`;
    }
    return `${x1},${y1}-${x2},${y2}`;
  }

  injectRandomFault() {
    const isHorizontal = Math.random() < 0.5;
    let x1, y1, x2, y2;
    if (isHorizontal) {
      x1 = Math.floor(Math.random() * (this.gridW - 1));
      y1 = Math.floor(Math.random() * this.gridH);
      x2 = x1 + 1;
      y2 = y1;
    } else {
      x1 = Math.floor(Math.random() * this.gridW);
      y1 = Math.floor(Math.random() * (this.gridH - 1));
      x2 = x1;
      y2 = y1 + 1;
    }
    const key = this.getLinkKey(x1, y1, x2, y2);
    if (!this.brokenLinks.has(key)) {
      this.brokenLinks.add(key);
      this.audio.playSpark();
      const midX = (this.getNodeX(x1) + this.getNodeX(x2)) / 2;
      const midY = (this.getNodeY(y1) + this.getNodeY(y2)) / 2;
      this.addTextParticle(midX, midY, '⚡ LINK FRACTURE', '#ef4444');
    }
  }

  injectPacket() {
    const sx = Math.floor(Math.random() * this.gridW);
    const sy = Math.floor(Math.random() * this.gridH);
    let dx = Math.floor(Math.random() * this.gridW);
    let dy = Math.floor(Math.random() * this.gridH);
    while (dx === sx && dy === sy) {
      dx = Math.floor(Math.random() * this.gridW);
      dy = Math.floor(Math.random() * this.gridH);
    }

    const pkt = {
      id: this.nextPacketId++,
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
      hops: 0,
      detoured: false,
      color: '#38bdf8'
    };
    this.packets.push(pkt);
  }

  update(dt) {
    if (!this.isRunning || this.isPaused) return;

    this.waveTimer -= dt;
    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 22.0;
      this.score += 300 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 60, `WAVE ${this.wave} RELIABILITY CHALLENGE!`, '#f59e0b');
      this.injectRandomFault();
    }

    // BIST charge recharge
    this.bistCharge = Math.min(100, this.bistCharge + dt * 14.0);

    // Dynamic fault generation over time
    this.faultInjectTimer += dt;
    const faultInterval = Math.max(5.0, 14.0 - this.wave * 1.5);
    if (this.faultInjectTimer >= faultInterval && this.brokenLinks.size < 6) {
      this.faultInjectTimer = 0;
      this.injectRandomFault();
    }

    // Regular packet traffic injection
    this.injectTimer += dt;
    const injectInterval = Math.max(0.5, 1.5 - this.wave * 0.12);
    if (this.injectTimer >= injectInterval && this.packets.length < 16) {
      this.injectTimer = 0;
      this.injectPacket();
    }

    // Step 1: Advance in-flight packets
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

          // Destination reached
          if (p.gx === p.dstX && p.gy === p.dstY) {
            this.packets.splice(i, 1);
            this.rescuedCount++;
            const bonus = p.detoured ? 80 : 50;
            this.score += bonus;
            this.audio.playDeliver();
            this.addTextParticle(this.getNodeX(p.gx), this.getNodeY(p.gy), `+${bonus}`, '#22c55e');
            continue;
          }
        }
      }
    }

    // Step 2: Route packets currently resting at nodes
    for (let i = this.packets.length - 1; i >= 0; i--) {
      const p = this.packets[i];
      if (p.state === 'at_node') {
        this.routePacket(p, i);
      }
    }

    // Update BIST radar waves
    for (let i = this.bistWaves.length - 1; i >= 0; i--) {
      const w = this.bistWaves[i];
      w.radius += dt * 320;
      w.alpha -= dt * 1.2;
      if (w.alpha <= 0) this.bistWaves.splice(i, 1);
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

  routePacket(p, pktIdx) {
    let nextX = p.gx;
    let nextY = p.gy;

    // Ideal XY routing target
    if (p.dstX > p.gx) nextX = p.gx + 1;
    else if (p.dstX < p.gx) nextX = p.gx - 1;
    else if (p.dstY > p.gy) nextY = p.gy + 1;
    else if (p.dstY < p.gy) nextY = p.gy - 1;

    const linkKey = this.getLinkKey(p.gx, p.gy, nextX, nextY);
    const isBroken = this.brokenLinks.has(linkKey);

    if (!isBroken) {
      // Healthy primary wire
      p.toGx = nextX;
      p.toGy = nextY;
      p.fromGx = p.gx;
      p.fromGy = p.gy;
      p.progress = 0;
      p.state = 'in_flight';
    } else {
      // Link is fractured!
      if (this.protocol === 'naive_xy') {
        // Destroy packet!
        this.packets.splice(pktIdx, 1);
        this.lostCount++;
        this.health = Math.max(0, this.health - 18.0);
        this.audio.playDestroy();
        this.addTextParticle(this.getNodeX(p.gx), this.getNodeY(p.gy), '💥 PACKET LOST', '#ef4444');
        if (this.health <= 0) {
          this.triggerGameOver();
        }
      } else if (this.protocol === 'spare_links') {
        // Activate hot-spare bypass wire
        this.sparesActive.add(linkKey);
        p.toGx = nextX;
        p.toGy = nextY;
        p.fromGx = p.gx;
        p.fromGy = p.gy;
        p.progress = 0;
        p.state = 'in_flight';
        p.detoured = true;
        p.color = '#4ade80';
        this.audio.playDetour();
        this.addTextParticle(this.getNodeX(p.gx), this.getNodeY(p.gy), 'SPARE BYPASS', '#22c55e');
      } else {
        // fault_ring perimeter detour
        // Find alternative orthogonal healthy link
        const neighbors = [
          { x: p.gx, y: p.gy - 1 },
          { x: p.gx + 1, y: p.gy },
          { x: p.gx, y: p.gy + 1 },
          { x: p.gx - 1, y: p.gy }
        ];

        let chosen = null;
        for (let n of neighbors) {
          if (n.x >= 0 && n.x < this.gridW && n.y >= 0 && n.y < this.gridH) {
            const key = this.getLinkKey(p.gx, p.gy, n.x, n.y);
            if (!this.brokenLinks.has(key)) {
              chosen = n;
              break;
            }
          }
        }

        if (chosen) {
          p.toGx = chosen.x;
          p.toGy = chosen.y;
          p.fromGx = p.gx;
          p.fromGy = p.gy;
          p.progress = 0;
          p.state = 'in_flight';
          p.detoured = true;
          p.color = '#f59e0b';
          this.audio.playDetour();
          this.addTextParticle(this.getNodeX(p.gx), this.getNodeY(p.gy), 'FAULT-RING DETOUR', '#f59e0b');
        } else {
          // Complete isolation
          this.packets.splice(pktIdx, 1);
          this.lostCount++;
          this.health = Math.max(0, this.health - 20.0);
          this.audio.playDestroy();
          if (this.health <= 0) this.triggerGameOver();
        }
      }
    }
  }

  fireBist() {
    if (this.bistCharge >= 100) {
      this.bistCharge = 0;
      this.audio.playBist();
      this.bistWaves.push({
        x: this.canvas.width / 2,
        y: this.canvas.height / 2,
        radius: 10,
        alpha: 1.0
      });
      // BIST bonus points
      this.score += 150;
      this.health = Math.min(100, this.health + 10);
      this.addTextParticle(this.canvas.width / 2, 70, '📡 BIST RADAR SCAN COMPLETE: FAULTS ISOLATED!', '#38bdf8');
    }
  }

  getNodeX(gx) { return this.offsetX + gx * this.nodeSpacingX; }
  getNodeY(gy) { return this.offsetY + gy * this.nodeSpacingY; }

  render() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw interconnect links
    for (let y = 0; y < this.gridH; y++) {
      for (let x = 0; x < this.gridW; x++) {
        const nx = this.getNodeX(x);
        const ny = this.getNodeY(y);

        // Horizontal Link
        if (x < this.gridW - 1) {
          const nextX = this.getNodeX(x + 1);
          const key = this.getLinkKey(x, y, x + 1, y);
          const isBroken = this.brokenLinks.has(key);
          const hasSpare = this.sparesActive.has(key);

          this.ctx.lineWidth = isBroken ? 4 : 3;
          this.ctx.strokeStyle = isBroken ? '#ef4444' : (hasSpare ? '#22c55e' : '#1e293b');
          if (isBroken) this.ctx.setLineDash([4, 4]);
          this.ctx.beginPath();
          this.ctx.moveTo(nx, ny);
          this.ctx.lineTo(nextX, ny);
          this.ctx.stroke();
          this.ctx.setLineDash([]);

          if (isBroken) {
            // Draw fracture cross
            const mx = (nx + nextX) / 2;
            this.ctx.fillStyle = '#ef4444';
            this.ctx.font = 'bold 13px sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('⚡', mx, ny + 4);
          }
        }

        // Vertical Link
        if (y < this.gridH - 1) {
          const nextY = this.getNodeY(y + 1);
          const key = this.getLinkKey(x, y, x, y + 1);
          const isBroken = this.brokenLinks.has(key);
          const hasSpare = this.sparesActive.has(key);

          this.ctx.lineWidth = isBroken ? 4 : 3;
          this.ctx.strokeStyle = isBroken ? '#ef4444' : (hasSpare ? '#22c55e' : '#1e293b');
          if (isBroken) this.ctx.setLineDash([4, 4]);
          this.ctx.beginPath();
          this.ctx.moveTo(nx, ny);
          this.ctx.lineTo(nx, nextY);
          this.ctx.stroke();
          this.ctx.setLineDash([]);

          if (isBroken) {
            const my = (ny + nextY) / 2;
            this.ctx.fillStyle = '#ef4444';
            this.ctx.font = 'bold 13px sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('⚡', nx, my + 4);
          }
        }
      }
    }

    // Draw BIST radar waves
    for (let w of this.bistWaves) {
      this.ctx.save();
      this.ctx.strokeStyle = `rgba(56, 189, 248, ${w.alpha})`;
      this.ctx.lineWidth = 3;
      this.ctx.beginPath();
      this.ctx.arc(w.x, w.y, w.radius, 0, Math.PI * 2);
      this.ctx.stroke();
      this.ctx.restore();
    }

    // Draw active packets
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
      this.ctx.shadowColor = p.color;
      this.ctx.shadowBlur = 10;
      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(px, py, 6, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();
    }

    // Draw router nodes
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
    document.getElementById('faultScore').textContent = this.score;
    document.getElementById('faultRescued').textContent = this.rescuedCount;
    document.getElementById('faultLost').textContent = this.lostCount;
    document.getElementById('faultWave').textContent = `Wave ${this.wave}`;

    // BIST charge bar
    const bistBar = document.getElementById('bistChargeBar');
    const bistText = document.getElementById('bistChargeText');
    bistBar.style.width = `${this.bistCharge}%`;
    bistText.textContent = this.bistCharge >= 100 ? '100% READY' : `${Math.floor(this.bistCharge)}% CHARGING`;

    // Silicon health bar
    const healthBar = document.getElementById('siliconHealthBar');
    const healthText = document.getElementById('siliconHealthText');
    healthBar.style.width = `${this.health}%`;
    healthBar.style.background = this.health > 60 ? '#22c55e' : (this.health > 30 ? '#f59e0b' : '#ef4444');
    healthText.textContent = `${Math.floor(this.health)}% ${this.health > 60 ? 'HEALTHY' : (this.health > 30 ? 'DEGRADED' : 'CRITICAL')}`;
  }

  triggerGameOver() {
    this.isRunning = false;
    document.getElementById('faultModalTitle').textContent = 'SILICON SUBSTRATE BREAKDOWN!';
    document.getElementById('faultModalSummary').innerHTML = `
      Silicon SLA reliability threshold depleted!<br><br>
      <b>Final Wave:</b> Wave ${this.wave} | <b>Packets Rescued:</b> ${this.rescuedCount} | <b>Final Score:</b> ${this.score} pts
    `;
    document.getElementById('faultOverModal').style.display = 'flex';
  }
}

let faultGame = null;

function startFaultGame() {
  if (!faultGame) faultGame = new FaultGame();
  faultGame.start();
}

function restartFaultGame() {
  if (faultGame) faultGame.start();
}

function fireBistScan() {
  if (faultGame && faultGame.isRunning) {
    faultGame.fireBist();
  }
}

function setFaultProtocol(proto) {
  if (faultGame) faultGame.protocol = proto;
}

function toggleFaultSound() {
  if (faultGame) {
    faultGame.audio.enabled = !faultGame.audio.enabled;
    document.getElementById('faultSoundBtn').textContent = faultGame.audio.enabled ? '🔊 Sound: ON' : '🔇 Sound: OFF';
  }
}

function toggleFaultPause() {
  if (faultGame) faultGame.isPaused = !faultGame.isPaused;
}

// Global Animation Loop
function faultLoop(now) {
  if (faultGame && faultGame.isRunning) {
    const dt = Math.min(0.05, (now - faultGame.lastTime) / 1000);
    faultGame.lastTime = now;
    faultGame.update(dt);
    faultGame.render();
  }
  requestAnimationFrame(faultLoop);
}
requestAnimationFrame(faultLoop);

// Keyboard listener
window.addEventListener('keydown', (e) => {
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
  if (e.code === 'Space' || e.code === 'KeyB') {
    if (faultGame && faultGame.isRunning) {
      fireBistScan();
      e.preventDefault();
    }
  }
});

// Leaderboard and GitHub issue integration
function saveFaultRecord() {
  if (!faultGame) return;
  const nameInput = document.getElementById('faultCallsign').value.trim() || 'Silicon Defender';
  const orgInput = document.getElementById('faultOrg').value.trim() || 'Silicon Lab';

  const record = {
    name: nameInput,
    org: orgInput,
    track: `Fault Defender (Wave ${faultGame.wave})`,
    score: faultGame.score,
    accuracy: faultGame.rescuedCount,
    date: new Date().toISOString().slice(0, 10),
    certId: `FAULT-WAVE-${faultGame.wave}-${Math.floor(Math.random() * 900 + 100)}`,
    type: 'fault'
  };

  try {
    const key = 'noc_leaderboard_records';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push(record);
    localStorage.setItem(key, JSON.stringify(existing));
    const confirmEl = document.getElementById('faultSaveConfirm');
    if (confirmEl) confirmEl.style.display = 'block';
  } catch (err) {
    console.error('Failed to save to localStorage', err);
  }
}

function submitFaultToGithub() {
  if (!faultGame) return;
  const nameInput = document.getElementById('faultCallsign').value.trim() || 'Silicon Defender';
  const orgInput = document.getElementById('faultOrg').value.trim() || 'Silicon Lab';

  const title = encodeURIComponent(`[Leaderboard Submission] Fault Defender - ${nameInput} (${faultGame.score} pts)`);
  const body = encodeURIComponent([
    `### 🛡️ Fault Defender: Silicon Resilience Score Submission`,
    `- **Resilience Architect**: ${nameInput}`,
    `- **Institution / Org**: ${orgInput}`,
    `- **Wave Reached**: Wave ${faultGame.wave}`,
    `- **Packets Rescued**: ${faultGame.rescuedCount}`,
    `- **Packets Lost**: ${faultGame.lostCount}`,
    `- **Total Score**: ${faultGame.score} pts`,
    `- **Submission Timestamp**: ${new Date().toISOString()}`,
    ``,
    `\`\`\`json`,
    JSON.stringify({
      type: "fault",
      player: nameInput,
      org: orgInput,
      score: faultGame.score,
      wave: faultGame.wave,
      rescued: faultGame.rescuedCount,
      lost: faultGame.lostCount,
      date: new Date().toISOString().slice(0, 10),
      certId: `FAULT-WAVE-${faultGame.wave}-${Math.floor(Math.random() * 900 + 100)}`
    }, null, 2),
    `\`\`\``
  ].join('\n'));

  window.open(`https://github.com/network-on-chip/learning/issues/new?title=${title}&body=${body}`, '_blank');
}
</script>
