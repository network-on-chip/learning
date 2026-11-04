# 🎯 QoS Gladiator: Mixed-Criticality Traffic Arbiter

Balance life-critical real-time safety packets against massive neural network memory streams! In modern autonomous automotive SoCs (ISO 26262 ASIL-D) and heterogeneous edge AI processors, the on-chip network is concurrently shared by three conflicting traffic classes:

1. 🔴 **Hard Real-Time (HRT / Safety):** LiDAR, camera radar, and emergency brake signals with strict microsecond countdown deadlines ($\tau \le 15\mu\text{s}$) and zero acceptable drops.
2. 🟡 **Latency-Sensitive (LS / Cache):** CPU L2/L3 cache misses and spinlock synchronization where stalls degrade IPC.
3. 🟢 **Best-Effort (BE / Bulk DMA):** High-bandwidth neural network weights and GPU video frames that saturate link bandwidth.

Prevent deadline violations, deploy **Weighted Fair Queuing (WFQ)**, manage **Priority Virtual Channels (PVC)**, and fire **Emergency Flit Preemptions** to cut through congested crossbars before deadlines expire! High scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="qosStartBtn" class="noc-sim-btn" onclick="startQosGame()">▶ Start QoS Defense</button>
    <button id="qosPreemptBtn" class="noc-sim-btn" onclick="triggerQosPreemption()" style="background:#ef4444; border:none; box-shadow:0 0 14px rgba(239,68,68,0.5);">⚡ Emergency Preemption Pulse (Space / P)</button>

    <label><b>Scheduling Arbiter:</b>
      <select id="qosPolicySelect" class="noc-sim-select" onchange="setQosPolicy(this.value)">
        <option value="wfq_balanced">Weighted Fair Queuing (WFQ: 60/30/10)</option>
        <option value="strict_priority">Strict Priority (HRT &gt; LS &gt; BE)</option>
        <option value="round_robin">Naive Round-Robin (Unprotected)</option>
      </select>
    </label>

    <button id="qosSoundBtn" class="noc-sim-btn secondary" onclick="toggleQosSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleQosPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="qosScore">0</span></span>
      <span style="color:#22c55e;">SLA: <span id="qosSla">100%</span></span>
      <span style="color:#ef4444;">Misses: <span id="qosMisses">0</span>/4</span>
      <span style="color:#f59e0b;" id="qosWave">Wave 1</span>
    </div>
  </div>

  <!-- QoS Deadline Compliance & Preemption HUD -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#ef4444;">⚡ Flit Preemption Interrupt Reservoir:</span>
        <span id="preemptChargeText" style="font-weight:700; color:#ef4444;">100% READY</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(239,68,68,0.15); border-radius:4px; overflow:hidden;">
        <div id="preemptChargeBar" style="width:100%; height:100%; background:linear-gradient(90deg, #b91c1c, #ef4444); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#22c55e;">🛡️ ASIL-D Real-Time Safety Compliance:</span>
        <span id="safetyHealthText" style="font-weight:700; color:#22c55e;">100% (Zero Deadline Violations)</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(34,197,94,0.15); border-radius:4px; overflow:hidden;">
        <div id="safetyHealthBar" style="width:100%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="qosCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="qosOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="qosModalIcon">💥</div>
      <h2 id="qosModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">SAFETY DEADLINE VIOLATION!</h2>
      <p id="qosModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        4 hard real-time safety packets missed their microsecond deadlines due to crossbar starvation!
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">QoS Arbiter Callsign:</label>
        <input type="text" id="qosCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. ASIL-D Master" value="QoS Commander">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="qosOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. NVIDIA Drive / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveQosRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitQosToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartQosGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="qosSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in local Hall of Fame!
      </div>
    </div>
  </div>

  <div id="qosInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">🎯 Mixed-Criticality NoC Microarchitecture &amp; Scheduling:</strong>
    <ul style="margin:0.4rem 0 0 1.2rem; padding:0;">
      <li><strong>Hard Real-Time (HRT 🔴):</strong> Has a visible countdown ring. Must reach its destination router before the timer depletes. Each missed deadline chips away at your ASIL-D safety compliance.</li>
      <li><strong>Latency-Sensitive (LS 🟡):</strong> Cache misses. Moderate priority. Fast delivery awards high-accuracy bonus multipliers.</li>
      <li><strong>Best-Effort (BE 🟢):</strong> High-volume bulk transfers. Fills all available link capacity. In unmanaged round-robin, bulk streams create severe Head-of-Line delays for HRT packets.</li>
      <li><strong>Emergency Flit Preemption (Space / P):</strong> Interrupts in-flight best-effort flits mid-wormhole, granting immediate right-of-way to all pending HRT packets!</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for QoS Gladiator
class QosAudio {
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

  playHrtDeliver() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      [659.25, 880, 1046.5].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, t + idx * 0.04);
        gain.gain.setValueAtTime(0.12, t + idx * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, t + idx * 0.04 + 0.16);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t + idx * 0.04);
        osc.stop(t + idx * 0.04 + 0.16);
      });
    } catch (e) {}
  }

  playPreempt() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(220, t);
      osc.frequency.exponentialRampToValueAtTime(880, t + 0.18);
      gain.gain.setValueAtTime(0.2, t);
      gain.gain.linearRampToValueAtTime(0.01, t + 0.18);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.18);
    } catch (e) {}
  }

  playWarning() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, t);
      gain.gain.setValueAtTime(0.08, t);
      gain.gain.linearRampToValueAtTime(0.001, t + 0.08);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.08);
    } catch (e) {}
  }

  playMiss() {
    if (!this.enabled || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(140, t);
      osc.frequency.linearRampToValueAtTime(45, t + 0.28);
      gain.gain.setValueAtTime(0.25, t);
      gain.gain.linearRampToValueAtTime(0.01, t + 0.28);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(t);
      osc.stop(t + 0.28);
    } catch (e) {}
  }
}

// 4x4 Mixed-Criticality NoC Engine
class QosGame {
  constructor() {
    this.canvas = document.getElementById('qosCanvas');
    this.ctx = this.canvas.getContext('2d');
    this.audio = new QosAudio();

    this.gridW = 4;
    this.gridH = 4;
    this.nodeSpacingX = 125;
    this.nodeSpacingY = 95;
    this.offsetX = 120;
    this.offsetY = 85;

    this.packets = [];
    this.particles = [];
    this.score = 0;
    this.hrtDelivered = 0;
    this.hrtMissed = 0;
    this.totalDelivered = 0;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.preemptCharge = 100.0;
    this.preemptActive = false;
    this.preemptTimer = 0.0;
    this.policy = 'wfq_balanced';

    this.isRunning = false;
    this.isPaused = false;
    this.lastTime = performance.now();
    this.injectTimer = 0;
    this.nextPktId = 1;
  }

  start() {
    this.audio.init();
    this.packets = [];
    this.particles = [];
    this.score = 0;
    this.hrtDelivered = 0;
    this.hrtMissed = 0;
    this.totalDelivered = 0;
    this.wave = 1;
    this.waveTimer = 22.0;
    this.preemptCharge = 100.0;
    this.preemptActive = false;
    this.preemptTimer = 0.0;
    this.isRunning = true;
    this.isPaused = false;

    document.getElementById('qosOverModal').style.display = 'none';
    document.getElementById('qosStartBtn').textContent = '🔄 Restart';
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

    // Traffic Class Distribution: 25% HRT (Red), 35% LS (Gold), 40% BE (Green)
    const roll = Math.random();
    let qosClass = 'BE';
    let color = '#22c55e';
    let deadline = 999.0;

    if (roll < 0.28) {
      qosClass = 'HRT';
      color = '#ef4444';
      deadline = Math.max(4.5, 7.5 - this.wave * 0.35); // Seconds to reach destination
    } else if (roll < 0.62) {
      qosClass = 'LS';
      color = '#eab308';
      deadline = 12.0;
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
      qosClass: qosClass,
      deadline: deadline,
      maxDeadline: deadline,
      color: color
    };
    this.packets.push(pkt);
  }

  triggerPreemption() {
    if (this.preemptCharge >= 100 && !this.preemptActive) {
      this.preemptActive = true;
      this.preemptTimer = 4.0;
      this.audio.playPreempt();
      this.addTextParticle(this.canvas.width / 2, 70, '⚡ EMERGENCY PREEMPTION ENGAGED!', '#ef4444');
    }
  }

  update(dt) {
    if (!this.isRunning || this.isPaused) return;

    this.waveTimer -= dt;
    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 22.0;
      this.score += 350 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 60, `WAVE ${this.wave} TRAFFIC ACCELERATION!`, '#f59e0b');
    }

    // Preemption charge
    if (this.preemptActive) {
      this.preemptTimer -= dt;
      this.preemptCharge = Math.max(0, (this.preemptTimer / 4.0) * 100);
      if (this.preemptTimer <= 0) {
        this.preemptActive = false;
        this.preemptCharge = 0;
      }
    } else {
      this.preemptCharge = Math.min(100, this.preemptCharge + dt * 14.0);
    }

    // Dynamic Traffic Injections
    this.injectTimer += dt;
    const injectInterval = Math.max(0.4, 1.25 - this.wave * 0.1);
    if (this.injectTimer >= injectInterval && this.packets.length < 18 + this.wave * 2) {
      this.injectTimer = 0;
      this.injectTraffic();
    }

    // Advance packets & track deadlines
    const baseSpeed = 1.35;
    for (let i = this.packets.length - 1; i >= 0; i--) {
      const p = this.packets[i];

      // Update HRT countdown
      if (p.qosClass === 'HRT') {
        p.deadline -= dt;
        if (p.deadline < 1.5 && p.deadline > 1.4) {
          this.audio.playWarning();
        }
        if (p.deadline <= 0) {
          // Missed deadline!
          this.packets.splice(i, 1);
          this.hrtMissed++;
          this.audio.playMiss();
          this.addTextParticle(this.getNodeX(p.gx), this.getNodeY(p.gy), 'DEADLINE MISS!', '#ef4444');
          if (this.hrtMissed >= 4) {
            this.triggerGameOver();
            return;
          }
          continue;
        }
      }

      // Movement
      if (p.state === 'in_flight') {
        const speed = (this.preemptActive && p.qosClass === 'HRT') ? baseSpeed * 2.2 : baseSpeed;
        p.progress += dt * speed;

        if (p.progress >= 1.0) {
          p.progress = 1.0;
          p.gx = p.toGx;
          p.gy = p.toGy;
          p.state = 'at_node';

          // Delivered!
          if (p.gx === p.dstX && p.gy === p.dstY) {
            this.packets.splice(i, 1);
            this.totalDelivered++;
            let pts = 40;
            if (p.qosClass === 'HRT') {
              this.hrtDelivered++;
              pts = 120 + Math.floor(p.deadline * 25);
              this.audio.playHrtDeliver();
            } else if (p.qosClass === 'LS') {
              pts = 70;
            }
            this.score += pts;
            this.addTextParticle(this.getNodeX(p.gx), this.getNodeY(p.gy), `+${pts}`, p.color);
            continue;
          }
        }
      }
    }

    // Router Switch Allocation by QoS Priority
    const nodeGroups = {};
    for (let p of this.packets) {
      if (p.state === 'at_node') {
        const key = `${p.gx},${p.gy}`;
        if (!nodeGroups[key]) nodeGroups[key] = [];
        nodeGroups[key].push(p);
      }
    }

    for (let key in nodeGroups) {
      this.arbitrateQosNode(nodeGroups[key]);
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

  arbitrateQosNode(pktsAtNode) {
    if (pktsAtNode.length === 0) return;
    const gx = pktsAtNode[0].gx;
    const gy = pktsAtNode[0].gy;

    // Sort packets by QoS policy
    if (this.preemptActive) {
      // Preemption active: HRT always gets instant 100% priority
      pktsAtNode.sort((a, b) => (b.qosClass === 'HRT' ? 1 : 0) - (a.qosClass === 'HRT' ? 1 : 0) || a.deadline - b.deadline);
    } else if (this.policy === 'strict_priority') {
      const prio = { HRT: 3, LS: 2, BE: 1 };
      pktsAtNode.sort((a, b) => prio[b.qosClass] - prio[a.qosClass] || a.deadline - b.deadline);
    } else if (this.policy === 'wfq_balanced') {
      // WFQ: Weights HRT=6, LS=3, BE=1
      pktsAtNode.sort((a, b) => {
        if (a.qosClass === 'HRT' && a.deadline < 2.5) return -1;
        if (b.qosClass === 'HRT' && b.deadline < 2.5) return 1;
        const prio = { HRT: 3, LS: 2, BE: 1 };
        return prio[b.qosClass] - prio[a.qosClass];
      });
    } else {
      // round_robin (unordered)
      pktsAtNode.sort(() => Math.random() - 0.5);
    }

    // Dispatch along shortest path
    for (let p of pktsAtNode) {
      let nextX = p.gx;
      let nextY = p.gy;
      if (p.dstX > p.gx) nextX = p.gx + 1;
      else if (p.dstX < p.gx) nextX = p.gx - 1;
      else if (p.dstY > p.gy) nextY = p.gy + 1;
      else if (p.dstY < p.gy) nextY = p.gy - 1;

      p.toGx = nextX;
      p.toGy = nextY;
      p.fromGx = p.gx;
      p.fromGy = p.gy;
      p.progress = 0;
      p.state = 'in_flight';
    }
  }

  getNodeX(gx) { return this.offsetX + gx * this.nodeSpacingX; }
  getNodeY(gy) { return this.offsetY + gy * this.nodeSpacingY; }

  render() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw mesh interconnect links
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
      this.ctx.shadowBlur = p.qosClass === 'HRT' ? 14 : 7;
      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(px, py, p.qosClass === 'HRT' ? 7.5 : 6, 0, Math.PI * 2);
      this.ctx.fill();

      // Countdown deadline ring for Hard Real-Time packets
      if (p.qosClass === 'HRT') {
        const frac = Math.max(0, p.deadline / p.maxDeadline);
        this.ctx.strokeStyle = frac > 0.4 ? '#ef4444' : '#f87171';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(px, py, 11, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * frac);
        this.ctx.stroke();
      }
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
    document.getElementById('qosScore').textContent = this.score;
    document.getElementById('qosMisses').textContent = `${this.hrtMissed}`;
    document.getElementById('qosWave').textContent = `Wave ${this.wave}`;

    // Calculate SLA
    const totalHrt = this.hrtDelivered + this.hrtMissed;
    const sla = totalHrt > 0 ? ((this.hrtDelivered / totalHrt) * 100).toFixed(1) : '100.0';
    document.getElementById('qosSla').textContent = `${sla}%`;

    // Preemption charge bar
    const bar = document.getElementById('preemptChargeBar');
    const text = document.getElementById('preemptChargeText');
    bar.style.width = `${this.preemptCharge}%`;
    if (this.preemptActive) {
      text.textContent = `⚡ ACTIVE (${this.preemptTimer.toFixed(1)}s)`;
      bar.style.background = '#f59e0b';
    } else {
      text.textContent = this.preemptCharge >= 100 ? '100% READY' : `${Math.floor(this.preemptCharge)}% CHARGING`;
      bar.style.background = 'linear-gradient(90deg, #b91c1c, #ef4444)';
    }

    // Safety health bar
    const sHealth = Math.max(0, 100 - this.hrtMissed * 25);
    const sBar = document.getElementById('safetyHealthBar');
    const sText = document.getElementById('safetyHealthText');
    sBar.style.width = `${sHealth}%`;
    sBar.style.background = sHealth > 50 ? '#22c55e' : (sHealth > 25 ? '#f59e0b' : '#ef4444');
    sText.textContent = `${sHealth}% (${this.hrtMissed} misses / max 4)`;
  }

  triggerGameOver() {
    this.isRunning = false;
    document.getElementById('qosModalTitle').textContent = 'SAFETY DEADLINE VIOLATION!';
    document.getElementById('qosModalSummary').innerHTML = `
      4 Hard Real-Time packets missed their critical deadlines!<br><br>
      <b>Final Wave:</b> Wave ${this.wave} | <b>HRT Delivered:</b> ${this.hrtDelivered} | <b>Score:</b> ${this.score} pts
    `;
    document.getElementById('qosOverModal').style.display = 'flex';
  }
}

let qosGame = null;

function startQosGame() {
  if (!qosGame) qosGame = new QosGame();
  qosGame.start();
}

function restartQosGame() {
  if (qosGame) qosGame.start();
}

function triggerQosPreemption() {
  if (qosGame && qosGame.isRunning) {
    qosGame.triggerPreemption();
  }
}

function setQosPolicy(pol) {
  if (qosGame) qosGame.policy = pol;
}

function toggleQosSound() {
  if (qosGame) {
    qosGame.audio.enabled = !qosGame.audio.enabled;
    document.getElementById('qosSoundBtn').textContent = qosGame.audio.enabled ? '🔊 Sound: ON' : '🔇 Sound: OFF';
  }
}

function toggleQosPause() {
  if (qosGame) qosGame.isPaused = !qosGame.isPaused;
}

// Global Animation Loop
function qosLoop(now) {
  if (qosGame && qosGame.isRunning) {
    const dt = Math.min(0.05, (now - qosGame.lastTime) / 1000);
    qosGame.lastTime = now;
    qosGame.update(dt);
    qosGame.render();
  }
  requestAnimationFrame(qosLoop);
}
requestAnimationFrame(qosLoop);

// Keyboard controls
window.addEventListener('keydown', (e) => {
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
  if (e.code === 'Space' || e.code === 'KeyP') {
    if (qosGame && qosGame.isRunning) {
      triggerQosPreemption();
      e.preventDefault();
    }
  }
});

// Hall of Fame Leaderboard & GitHub Submission Integration
function saveQosRecord() {
  if (!qosGame) return;
  const nameInput = document.getElementById('qosCallsign').value.trim() || 'QoS Commander';
  const orgInput = document.getElementById('qosOrg').value.trim() || 'Silicon Lab';

  const record = {
    name: nameInput,
    org: orgInput,
    track: `QoS Gladiator (Wave ${qosGame.wave})`,
    score: qosGame.score,
    accuracy: qosGame.hrtDelivered,
    date: new Date().toISOString().slice(0, 10),
    certId: `QOS-WAVE-${qosGame.wave}-${Math.floor(Math.random() * 900 + 100)}`,
    type: 'qos'
  };

  try {
    const key = 'noc_leaderboard_records';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push(record);
    localStorage.setItem(key, JSON.stringify(existing));
    const confirmEl = document.getElementById('qosSaveConfirm');
    if (confirmEl) confirmEl.style.display = 'block';
  } catch (err) {
    console.error('Failed to save to localStorage', err);
  }
}

function submitQosToGithub() {
  if (!qosGame) return;
  const nameInput = document.getElementById('qosCallsign').value.trim() || 'QoS Commander';
  const orgInput = document.getElementById('qosOrg').value.trim() || 'Silicon Lab';

  const title = encodeURIComponent(`[Leaderboard Submission] QoS Gladiator - ${nameInput} (${qosGame.score} pts)`);
  const body = encodeURIComponent([
    `### 🎯 QoS Gladiator: Mixed-Criticality Traffic Score Submission`,
    `- **Architect / Callsign**: ${nameInput}`,
    `- **Institution / Org**: ${orgInput}`,
    `- **Wave Reached**: Wave ${qosGame.wave}`,
    `- **HRT Safety Packets Delivered**: ${qosGame.hrtDelivered}`,
    `- **Total Packets Delivered**: ${qosGame.totalDelivered}`,
    `- **Total Score**: ${qosGame.score} pts`,
    `- **Submission Timestamp**: ${new Date().toISOString()}`,
    ``,
    `\`\`\`json`,
    JSON.stringify({
      type: "qos",
      player: nameInput,
      org: orgInput,
      score: qosGame.score,
      wave: qosGame.wave,
      delivered: qosGame.hrtDelivered,
      total: qosGame.totalDelivered,
      date: new Date().toISOString().slice(0, 10),
      certId: `QOS-WAVE-${qosGame.wave}-${Math.floor(Math.random() * 900 + 100)}`
    }, null, 2),
    `\`\`\``
  ].join('\n'));

  window.open(`https://github.com/network-on-chip/learning/issues/new?title=${title}&body=${body}`, '_blank');
}
</script>
