# 📡 Wireless Wave: mmWave & THz Swarm NoC

Break through wire-delay bottlenecks with speed-of-light wireless interconnects on silicon! In large-scale multi-core processors (64+ cores), traditional multi-hop copper wires suffer from quadratic RC delay ($t_{wire} \propto L^2$), forcing long-distance cross-chip transfers to spend 20–40 clock cycles traversing intermediate router hops.

**Wireless Networks-on-Chip (WNoC / WiNoC)** solve this by integrating on-chip millimeter-wave (60 GHz mmWave) and sub-THz graphene antennas with integrated RF transceivers into designated **Wireless Hubs**. Hubs beam packets across the entire die in a **single clock cycle**!

Master on-chip **Frequency-Division Multiple Access (FDMA)**, resolve multi-access RF packet collisions, balance transceiver power, and trigger **Multi-Carrier Broadcast Bursts** to blast barrier synchronizations across the chip. Your high scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="wirelessStartBtn" class="noc-sim-btn" onclick="startWirelessGame()">▶ Start RF Transmission</button>
    <button id="rfBroadcastBtn" class="noc-sim-btn" onclick="triggerRfSurge()" style="background:#0284c7; border:none; box-shadow:0 0 14px rgba(2,132,199,0.5);">⚡ Multi-Carrier RF Surge (Space / R)</button>

    <label><b>MAC Channel Protocol:</b>
      <select id="rfMacSelect" class="noc-sim-select" onchange="setRfProtocol(this.value)">
        <option value="fdma_tri">FDMA Multi-Band (3 Orthogonal Channels)</option>
        <option value="csma_ca">CSMA/CA (Carrier Sense with Backoff)</option>
        <option value="aloha_raw">Pure Aloha (Zero Sensing · High Collision)</option>
      </select>
    </label>

    <button id="wirelessSoundBtn" class="noc-sim-btn secondary" onclick="toggleWirelessSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleWirelessPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="wirelessScore">0</span></span>
      <span style="color:#22c55e;">Speedup: <span id="wirelessSpeedup">1.0</span>x</span>
      <span style="color:#ef4444;">Collisions: <span id="wirelessCollisions">0</span>/5</span>
      <span style="color:#f59e0b;" id="wirelessWave">Wave 1</span>
    </div>
  </div>

  <!-- RF Channel Power & Spectrum Availability HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">📡 Multi-Carrier RF Power Reservoir (Space / R):</span>
        <span id="rfSurgeText" style="font-weight:700; color:#38bdf8;">100% READY</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="rfSurgeBar" style="width:100%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#22c55e;">📶 RF Channel Signal-to-Interference Ratio:</span>
        <span id="sinrStatusText" style="font-weight:700; color:#22c55e;">24.5 dB (Clean Airwave)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(34,197,94,0.15); border-radius:4px; overflow:hidden;">
        <div id="sinrBar" style="width:85%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="wirelessCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="wirelessOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="wirelessModalIcon">💥</div>
      <h2 id="wirelessModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">RF INTERFERENCE SATURATION!</h2>
      <p id="wirelessModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        5 RF transmission collisions caused complete airwave interference and dropped wireless packets!
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">RF Architect Callsign:</label>
        <input type="text" id="wirelessCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. THz Maestro" value="RF Navigator">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="wirelessOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Georgia Tech / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveWirelessRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitWirelessToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartWirelessGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="wirelessSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in local Hall of Fame!
      </div>
    </div>
  </div>

  <div id="wirelessInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">📡 Wireless NoC Microarchitecture &amp; RF Medium Rules:</strong>
    <ul style="margin:0.4rem 0 0 1.2rem; padding:0;">
      <li><strong>Hybrid Wired-Wireless Architecture:</strong> The chip is a 4×4 mesh with 4 strategic <strong>Wireless Hubs</strong> ($R_{00}, R_{30}, R_{03}, R_{33}$). Local traffic travels over short wired links; long-distance traffic routes to a hub for 1-cycle wireless teleportation!</li>
      <li><strong>RF Collision &amp; SINR:</strong> The on-chip wireless channel is a shared broadcast medium. If two hubs transmit on the same frequency band simultaneously, an RF collision destroys both packets!</li>
      <li><strong>FDMA vs. CSMA:</strong> FDMA splits spectrum into three isolated bands ($\lambda_1$ Cyan, $\lambda_2$ Gold, $\lambda_3$ Magenta) to prevent interference. CSMA senses the carrier and backs off if busy.</li>
      <li><strong>Multi-Carrier RF Surge (Space / R):</strong> Activates full-band beamforming, enabling all 4 wireless hubs to transmit concurrently with zero collision risk for 4 seconds!</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Wireless Wave
class WirelessAudio {
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

  playRfBeam() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(420, t);
      osc.frequency.exponentialRampToValueAtTime(1450, t + 0.16);
      gain.gain.setValueAtTime(0.12, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.16);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.16);
    } catch (e) {}
  }

  playCollision() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(280, t);
      osc.frequency.linearRampToValueAtTime(50, t + 0.22);
      gain.gain.setValueAtTime(0.2, t);
      gain.gain.linearRampToValueAtTime(0.01, t + 0.22);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.22);
    } catch (e) {}
  }

  playBroadcastSurge() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      [523.25, 659.25, 783.99, 1046.5].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, t + idx * 0.04);
        gain.gain.setValueAtTime(0.12, t + idx * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, t + idx * 0.04 + 0.2);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t + idx * 0.04);
        osc.stop(t + idx * 0.04 + 0.2);
      });
    } catch (e) {}
  }

  playDeliver() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(523.25, t);
      osc.frequency.exponentialRampToValueAtTime(783.99, t + 0.12);
      gain.gain.setValueAtTime(0.1, t);
      gain.gain.linearRampToValueAtTime(0.001, t + 0.12);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.12);
    } catch (e) {}
  }
}

// 4x4 Hybrid Wired-Wireless NoC Engine
class WirelessGame {
  constructor() {
    this.canvas = document.getElementById('wirelessCanvas');
    this.ctx = this.canvas.getContext('2d');
    this.audio = new WirelessAudio();

    this.gridW = 4;
    this.gridH = 4;
    this.nodeSpacingX = 125;
    this.nodeSpacingY = 95;
    this.offsetX = 120;
    this.offsetY = 85;

    // 4 designated Wireless Hub routers: R00, R30, R03, R33
    this.hubCoords = [
      { x: 0, y: 0 },
      { x: 3, y: 0 },
      { x: 0, y: 3 },
      { x: 3, y: 3 }
    ];

    this.packets = [];
    this.rfWaves = []; // Radio ripples
    this.particles = [];
    this.score = 0;
    this.deliveredCount = 0;
    this.wirelessDeliveries = 0;
    this.collisions = 0;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.surgeEnergy = 100.0;
    this.surgeActive = false;
    this.surgeTimer = 0.0;
    this.protocol = 'fdma_tri';

    this.activeRfTransmitters = []; // Hubs currently transmitting
    this.isRunning = false;
    this.isPaused = false;
    this.lastTime = performance.now();
    this.injectTimer = 0;
    this.nextPktId = 1;
  }

  isHub(x, y) {
    return this.hubCoords.some(h => h.x === x && h.y === y);
  }

  getNearestHub(x, y) {
    let nearest = this.hubCoords[0];
    let minDist = 999;
    for (let h of this.hubCoords) {
      const d = Math.abs(h.x - x) + Math.abs(h.y - y);
      if (d < minDist) {
        minDist = d;
        nearest = h;
      }
    }
    return nearest;
  }

  start() {
    this.audio.init();
    this.packets = [];
    this.rfWaves = [];
    this.particles = [];
    this.score = 0;
    this.deliveredCount = 0;
    this.wirelessDeliveries = 0;
    this.collisions = 0;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.surgeEnergy = 100.0;
    this.surgeActive = false;
    this.surgeTimer = 0.0;
    this.isRunning = true;
    this.isPaused = false;

    document.getElementById('wirelessOverModal').style.display = 'none';
    document.getElementById('wirelessStartBtn').textContent = '🔄 Restart';
    this.lastTime = performance.now();

    for (let i = 0; i < 4; i++) {
      this.injectTraffic();
    }
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

    const dist = Math.abs(dx - sx) + Math.abs(dy - sy);
    const useWireless = dist >= 3; // Long-distance packets target wireless bypass

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
      useWireless: useWireless,
      wirelessHopDone: false,
      channelBand: Math.floor(Math.random() * 3), // 0, 1, 2 for FDMA
      color: useWireless ? '#38bdf8' : '#a855f7'
    };
    this.packets.push(pkt);
  }

  triggerSurge() {
    if (this.surgeEnergy >= 100 && !this.surgeActive) {
      this.surgeActive = true;
      this.surgeTimer = 4.0;
      this.audio.playBroadcastSurge();
      this.addTextParticle(this.canvas.width / 2, 70, '⚡ MULTI-CARRIER RF SURGE ACTIVE!', '#38bdf8');
    }
  }

  update(dt) {
    if (!this.isRunning || this.isPaused) return;

    this.waveTimer -= dt;
    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 22.0;
      this.score += 350 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 60, `WAVE ${this.wave} BANDWIDTH BOOST!`, '#f59e0b');
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

    // Inject traffic
    this.injectTimer += dt;
    const injectInterval = Math.max(0.4, 1.25 - this.wave * 0.1);
    if (this.injectTimer >= injectInterval && this.packets.length < 18 + this.wave * 2) {
      this.injectTimer = 0;
      this.injectTraffic();
    }

    // Step 1: Advance in-flight wired packets
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

          // Delivered?
          if (p.gx === p.dstX && p.gy === p.dstY) {
            this.packets.splice(i, 1);
            this.deliveredCount++;
            const pts = p.wirelessHopDone ? 110 : 50;
            if (p.wirelessHopDone) this.wirelessDeliveries++;
            this.score += pts;
            this.audio.playDeliver();
            this.addTextParticle(this.getNodeX(p.gx), this.getNodeY(p.gy), `+${pts}`, '#22c55e');
            continue;
          }
        }
      }
    }

    // Step 2: Route packets at nodes
    const hubTransmittersThisCycle = [];

    for (let i = this.packets.length - 1; i >= 0; i--) {
      const p = this.packets[i];
      if (p.state === 'at_node') {
        // If packet wants wireless bypass and is at a wireless hub
        if (p.useWireless && !p.wirelessHopDone && this.isHub(p.gx, p.gy)) {
          const targetHub = this.getNearestHub(p.dstX, p.dstY);
          if (targetHub.x !== p.gx || targetHub.y !== p.gy) {
            // Attempt RF wireless broadcast!
            const canTransmit = this.surgeActive || this.checkRfCollision(p.gx, p.gy, p.channelBand, hubTransmittersThisCycle);

            if (canTransmit) {
              hubTransmittersThisCycle.push({ x: p.gx, y: p.gy, band: p.channelBand });
              p.gx = targetHub.x;
              p.gy = targetHub.y;
              p.toGx = targetHub.x;
              p.toGy = targetHub.y;
              p.wirelessHopDone = true;
              p.state = 'at_node';
              this.audio.playRfBeam();
              this.addRfWave(this.getNodeX(p.gx), this.getNodeY(p.gy), p.channelBand);
              this.addTextParticle(this.getNodeX(targetHub.x), this.getNodeY(targetHub.y), '⚡ 1-CYCLE RF BEAM', '#38bdf8');
              continue;
            } else {
              // RF Collision or medium busy
              if (this.protocol === 'aloha_raw') {
                this.packets.splice(i, 1);
                this.collisions++;
                this.audio.playCollision();
                this.addTextParticle(this.getNodeX(p.gx), this.getNodeY(p.gy), '💥 RF COLLISION', '#ef4444');
                if (this.collisions >= 5) {
                  this.triggerGameOver();
                  return;
                }
                continue;
              }
              // CSMA backoff: stall at hub until clear
              continue;
            }
          }
        }

        // Standard wired routing
        let targetX = p.dstX;
        let targetY = p.dstY;
        if (p.useWireless && !p.wirelessHopDone) {
          const nearestHub = this.getNearestHub(p.gx, p.gy);
          targetX = nearestHub.x;
          targetY = nearestHub.y;
        }

        let nextX = p.gx;
        let nextY = p.gy;
        if (targetX > p.gx) nextX = p.gx + 1;
        else if (targetX < p.gx) nextX = p.gx - 1;
        else if (targetY > p.gy) nextY = p.gy + 1;
        else if (targetY < p.gy) nextY = p.gy - 1;

        p.toGx = nextX;
        p.toGy = nextY;
        p.fromGx = p.gx;
        p.fromGy = p.gy;
        p.progress = 0;
        p.state = 'in_flight';
      }
    }

    // Step 3: Update RF waves
    for (let i = this.rfWaves.length - 1; i >= 0; i--) {
      const w = this.rfWaves[i];
      w.radius += dt * 360;
      w.alpha -= dt * 1.5;
      if (w.alpha <= 0) this.rfWaves.splice(i, 1);
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

  checkRfCollision(x, y, band, activeThisCycle) {
    if (this.protocol === 'fdma_tri') {
      // Free if no other hub is using the same band
      return !activeThisCycle.some(h => h.band === band);
    } else if (this.protocol === 'csma_ca') {
      // Free if airwave is totally silent
      return activeThisCycle.length === 0;
    } else {
      // aloha_raw: high chance of collision if any other hub is active
      return activeThisCycle.length === 0 || Math.random() < 0.25;
    }
  }

  addRfWave(x, y, band) {
    const colors = ['#38bdf8', '#eab308', '#ec4899'];
    this.rfWaves.push({
      x: x,
      y: y,
      radius: 12,
      alpha: 1.0,
      color: colors[band % 3]
    });
  }

  getNodeX(gx) { return this.offsetX + gx * this.nodeSpacingX; }
  getNodeY(gy) { return this.offsetY + gy * this.nodeSpacingY; }

  render() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw interconnect links
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

    // Draw expanding RF radio ripples
    for (let w of this.rfWaves) {
      this.ctx.save();
      this.ctx.strokeStyle = w.color;
      this.ctx.globalAlpha = Math.max(0, w.alpha);
      this.ctx.lineWidth = 2.5;
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
      this.ctx.shadowBlur = 8;
      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(px, py, 6, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();
    }

    // Draw 4x4 routers & Wireless Hubs
    for (let y = 0; y < this.gridH; y++) {
      for (let x = 0; x < this.gridW; x++) {
        const nx = this.getNodeX(x);
        const ny = this.getNodeY(y);
        const isHubRouter = this.isHub(x, y);

        this.ctx.save();
        this.ctx.fillStyle = isHubRouter ? '#0369a1' : '#1e293b';
        this.ctx.strokeStyle = isHubRouter ? '#38bdf8' : '#475569';
        this.ctx.lineWidth = isHubRouter ? 3 : 2;
        if (isHubRouter) {
          this.ctx.shadowColor = '#38bdf8';
          this.ctx.shadowBlur = 12;
        }

        this.ctx.beginPath();
        this.ctx.roundRect(nx - 18, ny - 18, 36, 36, 6);
        this.ctx.fill();
        this.ctx.stroke();
        this.ctx.restore();

        // Router text or Antenna tower
        this.ctx.fillStyle = isHubRouter ? '#ffffff' : '#94a3b8';
        this.ctx.font = 'bold 10px "JetBrains Mono", monospace';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        if (isHubRouter) {
          this.ctx.fillText('📡', nx, ny - 1);
        } else {
          this.ctx.fillText(`R${x}${y}`, nx, ny);
        }
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
    document.getElementById('wirelessScore').textContent = this.score;
    document.getElementById('wirelessCollisions').textContent = `${this.collisions}`;
    document.getElementById('wirelessWave').textContent = `Wave ${this.wave}`;

    // Speedup metric: 1.0 + (wirelessDeliveries / max(1, total)) * 2.8
    const ratio = this.deliveredCount > 0 ? (this.wirelessDeliveries / this.deliveredCount) : 0;
    const speedup = (1.0 + ratio * 2.8).toFixed(1);
    document.getElementById('wirelessSpeedup').textContent = `${speedup}`;

    // Surge energy bar
    const bar = document.getElementById('rfSurgeBar');
    const text = document.getElementById('rfSurgeText');
    bar.style.width = `${this.surgeEnergy}%`;
    if (this.surgeActive) {
      text.textContent = `⚡ SURGE ACTIVE (${this.surgeTimer.toFixed(1)}s)`;
      bar.style.background = '#f59e0b';
    } else {
      text.textContent = this.surgeEnergy >= 100 ? '100% READY' : `${Math.floor(this.surgeEnergy)}% CHARGING`;
      bar.style.background = 'linear-gradient(90deg, #0284c7, #38bdf8)';
    }

    // SINR bar
    const sinrDb = Math.max(0, 24.5 - this.collisions * 4.8);
    const sinrPct = Math.min(100, (sinrDb / 25.0) * 100);
    const sinrBar = document.getElementById('sinrBar');
    const sinrText = document.getElementById('sinrStatusText');
    sinrBar.style.width = `${sinrPct}%`;
    sinrBar.style.background = sinrPct > 60 ? '#22c55e' : (sinrPct > 30 ? '#f59e0b' : '#ef4444');
    sinrText.textContent = `${sinrDb.toFixed(1)} dB (${sinrPct > 60 ? 'CLEAN' : 'INTERFERENCE'})`;
  }

  triggerGameOver() {
    this.isRunning = false;
    document.getElementById('wirelessModalTitle').textContent = 'RF INTERFERENCE SATURATION!';
    document.getElementById('wirelessModalSummary').innerHTML = `
      5 on-chip wireless collisions corrupted airwave packets!<br><br>
      <b>Final Wave:</b> Wave ${this.wave} | <b>Wireless Speedup:</b> ${document.getElementById('wirelessSpeedup').textContent}x | <b>Score:</b> ${this.score} pts
    `;
    document.getElementById('wirelessOverModal').style.display = 'flex';
  }
}

let wirelessGame = null;

function startWirelessGame() {
  if (!wirelessGame) wirelessGame = new WirelessGame();
  wirelessGame.start();
}

function restartWirelessGame() {
  if (wirelessGame) wirelessGame.start();
}

function triggerRfSurge() {
  if (wirelessGame && wirelessGame.isRunning) {
    wirelessGame.triggerSurge();
  }
}

function setRfProtocol(proto) {
  if (wirelessGame) wirelessGame.protocol = proto;
}

function toggleWirelessSound() {
  if (wirelessGame) {
    wirelessGame.audio.enabled = !wirelessGame.audio.enabled;
    document.getElementById('wirelessSoundBtn').textContent = wirelessGame.audio.enabled ? '🔊 Sound: ON' : '🔇 Sound: OFF';
  }
}

function toggleWirelessPause() {
  if (wirelessGame) wirelessGame.isPaused = !wirelessGame.isPaused;
}

// Global Animation Loop
function wirelessLoop(now) {
  if (wirelessGame && wirelessGame.isRunning) {
    const dt = Math.min(0.05, (now - wirelessGame.lastTime) / 1000);
    wirelessGame.lastTime = now;
    wirelessGame.update(dt);
    wirelessGame.render();
  }
  requestAnimationFrame(wirelessLoop);
}
requestAnimationFrame(wirelessLoop);

// Keyboard controls
window.addEventListener('keydown', (e) => {
  if (e.code === 'Space' || e.code === 'KeyR') {
    if (wirelessGame && wirelessGame.isRunning) {
      triggerRfSurge();
      e.preventDefault();
    }
  }
});

// Hall of Fame Leaderboard & GitHub Submission Integration
function saveWirelessRecord() {
  if (!wirelessGame) return;
  const nameInput = document.getElementById('wirelessCallsign').value.trim() || 'RF Navigator';
  const orgInput = document.getElementById('wirelessOrg').value.trim() || 'Silicon Lab';

  const record = {
    name: nameInput,
    org: orgInput,
    track: `Wireless Wave (Wave ${wirelessGame.wave})`,
    score: wirelessGame.score,
    accuracy: Number(document.getElementById('wirelessSpeedup').textContent),
    date: new Date().toISOString().slice(0, 10),
    certId: `WIRELESS-WAVE-${wirelessGame.wave}-${Math.floor(Math.random() * 900 + 100)}`,
    type: 'wireless'
  };

  try {
    const key = 'noc_leaderboard_records';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push(record);
    localStorage.setItem(key, JSON.stringify(existing));
    const confirmEl = document.getElementById('wirelessSaveConfirm');
    if (confirmEl) confirmEl.style.display = 'block';
  } catch (err) {
    console.error('Failed to save to localStorage', err);
  }
}

function submitWirelessToGithub() {
  if (!wirelessGame) return;
  const nameInput = document.getElementById('wirelessCallsign').value.trim() || 'RF Navigator';
  const orgInput = document.getElementById('wirelessOrg').value.trim() || 'Silicon Lab';

  const title = encodeURIComponent(`[Leaderboard Submission] Wireless Wave - ${nameInput} (${wirelessGame.score} pts)`);
  const body = encodeURIComponent([
    `### 📡 Wireless Wave: mmWave & THz WNoC Score Submission`,
    `- **Architect / Callsign**: ${nameInput}`,
    `- **Institution / Org**: ${orgInput}`,
    `- **Wave Reached**: Wave ${wirelessGame.wave}`,
    `- **Wireless Speedup**: ${document.getElementById('wirelessSpeedup').textContent}x`,
    `- **Packets Delivered**: ${wirelessGame.deliveredCount}`,
    `- **Total Score**: ${wirelessGame.score} pts`,
    `- **Submission Timestamp**: ${new Date().toISOString()}`,
    ``,
    `\`\`\`json`,
    JSON.stringify({
      type: "wireless",
      player: nameInput,
      org: orgInput,
      score: wirelessGame.score,
      wave: wirelessGame.wave,
      speedup: Number(document.getElementById('wirelessSpeedup').textContent),
      delivered: wirelessGame.deliveredCount,
      date: new Date().toISOString().slice(0, 10),
      certId: `WIRELESS-WAVE-${wirelessGame.wave}-${Math.floor(Math.random() * 900 + 100)}`
    }, null, 2),
    `\`\`\``
  ].join('\n'));

  window.open(`https://github.com/network-on-chip/learning/issues/new?title=${title}&body=${body}`, '_blank');
}
</script>
