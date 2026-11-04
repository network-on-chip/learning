# 💳 Credit Commander: Flow Control Defense

Master high-speed link-level flow control on silicon! Manage credit-based buffer allocations, tune credit batching, and prevent downstream buffer overrun under heavy traffic bursts with non-zero round-trip flight delays ($RTT = 2 \cdot t_{wire} + t_{proc}$). Keep the silicon pipeline running at 100% throughput without dropping a single flit! High scores can be inscribed directly onto the **Community Leaderboard**.

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="creditStartBtn" class="noc-sim-btn" onclick="startCreditGame()">▶ Start Command</button>
    <button id="stepCreditClockBtn" class="noc-sim-btn" onclick="fireCreditClock()" style="background:#ea580c; border:none; box-shadow:0 0 12px rgba(234,88,12,0.4);">⚡ Step Cycle (Space)</button>
    <button id="drainBoostBtn" class="noc-sim-btn" onclick="activateDrainBoost()" style="background:#10b981; border:none;">🚀 Drain Boost (D)</button>

    <label><b>Flow Control Protocol:</b>
      <select id="creditProtocolSelect" class="noc-sim-select" onchange="setCreditProtocol(this.value)">
        <option value="credit_instant">Credit-Based (Instant Return / Zero Drops)</option>
        <option value="credit_batched">Credit-Based (Batched x3 / Saves Wire Power)</option>
        <option value="on_off">On/Off Flow Control (High/Low Watermarks)</option>
      </select>
    </label>

    <label><b>Clock Speed:</b>
      <select id="creditClockSpeed" class="noc-sim-select" onchange="setCreditClockSpeed(this.value)">
        <option value="auto_1">Auto Clock (1.0 Hz)</option>
        <option value="auto_2">Auto Clock (2.0 Hz Fast)</option>
        <option value="manual">Manual Spacebar Only</option>
      </select>
    </label>

    <button id="creditSoundBtn" class="noc-sim-btn secondary" onclick="toggleCreditSound()">🔊 Sound: ON</button>
    <button class="noc-sim-btn secondary" onclick="toggleCreditPause()">⏸ Pause</button>

    <div style="margin-left:auto; display:flex; gap:1.2rem; align-items:center; font-weight:700; font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="creditScore">0</span></span>
      <span style="color:#22c55e;">Efficiency: <span id="creditEfficiency">100%</span></span>
      <span style="color:#ef4444;">Stalls: <span id="creditStalls">0</span></span>
      <span style="color:#f59e0b;" id="creditWave">Wave 1</span>
    </div>
  </div>

  <!-- Flow Control HUD: Credits & Buffer Fill Levels -->
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#38bdf8;">💳 Upstream Credits Available (TX):</span>
        <span id="txCreditsText" style="font-weight:700; color:#38bdf8;">8 / 8</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(56,189,248,0.15); border-radius:4px; overflow:hidden;">
        <div id="txCreditsBar" style="width:100%; height:100%; background:linear-gradient(90deg, #0284c7, #38bdf8); transition:width 0.15s ease;"></div>
      </div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.5rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; color:#f87171;">📦 Downstream Ingress FIFO Occupancy (RX):</span>
        <span id="rxBufferText" style="font-weight:700; color:#4ade80;">0 / 8 Flits</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(239,68,68,0.15); border-radius:4px; overflow:hidden;">
        <div id="rxBufferBar" style="width:0%; height:100%; background:#22c55e; transition:width 0.2s ease, background 0.2s ease;"></div>
      </div>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="creditCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block;"></canvas>

    <!-- Game Over / Victory Modal -->
    <div id="creditOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.94); border-radius:12px; z-index:20; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.35rem;" id="creditModalIcon">💥</div>
      <h2 id="creditModalTitle" style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">DOWNSTREAM BUFFER OVERFLOW!</h2>
      <p id="creditModalSummary" style="color:#cbd5e1; font-size:0.95rem; max-width:480px; margin-bottom:1.25rem; line-height:1.6;">
        Downstream ingress FIFO queue exceeded 8 flits! Packets were irreversibly dropped, violating credit flow control invariants.
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.25rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Flow Commander Callsign:</label>
        <input type="text" id="creditCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Credit Master" value="Flow Commander">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="creditOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box; background:#0f172a; color:#f8fafc; border-color:#475569;" placeholder="e.g. Intel Fabric / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveCreditRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitCreditToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartCreditGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="creditSaveConfirm" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in your browser Leaderboard!
      </div>
    </div>
  </div>

  <div id="creditInstructions" style="margin-top:1rem; padding:1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.65;">
    <strong style="color:var(--tcl-heading);">💳 Link Flow Control &amp; Credit Loop Architecture:</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Credit Invariant:</strong> The transmitter holds a Credit Counter $C$. Transmitting a flit decrements $C \leftarrow C - 1$. When $C = 0$, transmission stalls to prevent buffer overflow. When the receiver consumes a flit, it returns a credit along the reverse link ($C \leftarrow C + 1$).</li>
      <li><strong>Round-Trip Flight Delay ($RTT$):</strong> Because signals take cycles to propagate across wires and router pipelines ($RTT = 2 \cdot t_{flight} + t_{proc}$), the minimum buffer capacity to sustain 100% throughput is $B_{min} = RTT \cdot \text{Throughput}$. If $B &lt; RTT$, the link suffers credit starvation!</li>
      <li><strong>Credit Batching:</strong> Sending credits individually wastes wire switching energy. Batching credits in groups of 3 cuts link transitions, but increases upstream stall vulnerability during burst waves.</li>
      <li><strong>On/Off Signaling:</strong> An alternative to credit counting: the receiver asserts a single `STOP` signal when its buffer exceeds the high watermark ($6/8$), and resumes with `GO` when draining below the low watermark ($3/8$).</li>
    </ul>
  </div>
</div>

<script>
// Procedural Web Audio Sound Synthesizer for Credit Commander
class CreditAudio {
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

  playTx() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(520, now);
      osc.linearRampToValueAtTime(780, now + 0.05);
      gain.gain.setValueAtTime(0.09, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.06);
    } catch(e) {}
  }

  playCreditReturn() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(1046.5, now); // C6
      osc.exponentialRampToValueAtTime(1318.5, now + 0.06); // E6
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.08);
    } catch(e) {}
  }

  playStall() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(160, now);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.1);
    } catch(e) {}
  }

  playGameOver() {
    if (!this.enabled || !this.ctx) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(180, now);
      osc.exponentialRampToValueAtTime(35, now + 0.6);
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.65);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.65);
    } catch(e) {}
  }
}

class CreditGame {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.audio = new CreditAudio();

    this.maxBuffer = 8;
    this.txCredits = 8; // Available upstream credits
    this.rxBuffer = []; // Ingress FIFO
    this.forwardPipe = [null, null, null]; // 3-stage forward wire pipeline
    this.creditWire = [null, null]; // 2-stage reverse credit wire

    this.protocol = 'credit_instant'; // 'credit_instant', 'credit_batched', 'on_off'
    this.batchedCreditCount = 0;
    this.onOffState = 'GO'; // 'GO' or 'STOP'
    this.clockSpeedMode = 'auto_1';
    this.clockPeriod = 1.0;
    this.clockAccumulator = 0.0;

    this.state = 'idle';
    this.score = 0;
    this.cycles = 0;
    this.deliveredCount = 0;
    this.stalledCycles = 0;
    this.wave = 1;
    this.waveTimer = 25.0;
    this.drainRate = 1; // Flits drained per cycle

    this.particles = [];
    this.lastTime = performance.now();
    this.bindEvents();
    this.loop = this.loop.bind(this);
    requestAnimationFrame(this.loop);
  }

  bindEvents() {
    window.addEventListener('keydown', (e) => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
      if (e.code === 'Space') {
        e.preventDefault();
        this.audio.init();
        this.stepCycle();
      } else if (e.key === 'd' || e.key === 'D') {
        this.activateDrainBoost();
      } else if (e.key === 'p' || e.key === 'P') {
        this.togglePause();
      }
    });
  }

  start() {
    this.audio.init();
    this.txCredits = 8;
    this.rxBuffer = [];
    this.forwardPipe = [null, null, null];
    this.creditWire = [null, null];
    this.batchedCreditCount = 0;
    this.onOffState = 'GO';

    this.state = 'running';
    this.score = 0;
    this.cycles = 0;
    this.deliveredCount = 0;
    this.stalledCycles = 0;
    this.wave = 1;
    this.waveTimer = 25.0;
    this.drainRate = 1;
    this.particles = [];

    document.getElementById('creditOverModal').style.display = 'none';
    document.getElementById('creditStartBtn').textContent = '🔄 Restart';
    this.updateHUD();
  }

  togglePause() {
    if (this.state === 'running') this.state = 'paused';
    else if (this.state === 'paused') this.state = 'running';
  }

  activateDrainBoost() {
    if (this.state !== 'running') return;
    this.drainRate = Math.min(3, this.drainRate + 1);
    this.addTextParticle(520, 200, `DRAIN x${this.drainRate}!`, '#10b981');
    setTimeout(() => { this.drainRate = 1; }, 4000);
  }

  addTextParticle(x, y, text, color) {
    this.particles.push({
      x, y, vx: 0, vy: -0.8, life: 1.0, text, color, isText: true
    });
  }

  stepCycle() {
    if (this.state !== 'running') return;
    this.cycles++;

    // 1. Advance Reverse Credit Wire (Returns to Upstream TX)
    const returnedCredit = this.creditWire.shift();
    this.creditWire.push(null);

    if (returnedCredit) {
      if (typeof returnedCredit === 'number') {
        this.txCredits = Math.min(this.maxBuffer, this.txCredits + returnedCredit);
        this.audio.playCreditReturn();
        this.addTextParticle(80, 290, `+${returnedCredit} CR`, '#38bdf8');
      } else if (returnedCredit === 'ON') {
        this.onOffState = 'GO';
        this.addTextParticle(80, 290, `LINK GO!`, '#4ade80');
      } else if (returnedCredit === 'OFF') {
        this.onOffState = 'STOP';
        this.addTextParticle(80, 290, `LINK STOP!`, '#ef4444');
      }
    }

    // 2. Downstream Receiver Drains Flits & Generates Credits
    for (let d = 0; d < this.drainRate; d++) {
      if (this.rxBuffer.length > 0) {
        this.rxBuffer.shift();
        this.deliveredCount++;
        this.score += 20 * this.wave;

        // Credit generation logic based on protocol
        if (this.protocol === 'credit_instant') {
          this.creditWire[1] = 1; // Inject credit into wire
        } else if (this.protocol === 'credit_batched') {
          this.batchedCreditCount++;
          if (this.batchedCreditCount >= 3) {
            this.creditWire[1] = this.batchedCreditCount;
            this.batchedCreditCount = 0;
          }
        }
      }
    }

    // On/Off Signaling Watermark Checks
    if (this.protocol === 'on_off') {
      if (this.rxBuffer.length >= 6 && this.onOffState !== 'STOP') {
        this.creditWire[1] = 'OFF';
      } else if (this.rxBuffer.length <= 3 && this.onOffState !== 'GO') {
        this.creditWire[1] = 'ON';
      }
    }

    // 3. Advance Forward Wire Pipeline into Receiver
    const arrivingFlit = this.forwardPipe.pop();
    this.forwardPipe.unshift(null);

    if (arrivingFlit) {
      this.rxBuffer.push(arrivingFlit);
      // Check for Buffer Overflow
      if (this.rxBuffer.length > this.maxBuffer) {
        this.triggerOverflow();
        return;
      }
    }

    // 4. Upstream Transmitter Decision: Transmit or Stall?
    let canTransmit = false;
    if (this.protocol === 'on_off') {
      canTransmit = (this.onOffState === 'GO');
    } else {
      canTransmit = (this.txCredits > 0);
    }

    const trafficInject = (Math.random() < (0.65 + this.wave * 0.08));
    if (trafficInject) {
      if (canTransmit) {
        if (this.protocol !== 'on_off') this.txCredits--;
        this.forwardPipe[0] = { id: Math.floor(Math.random() * 900 + 100), color: '#38bdf8' };
        this.audio.playTx();
      } else {
        // Transmitter Stalled!
        this.stalledCycles++;
        this.audio.playStall();
        this.addTextParticle(120, 140, 'STALL (NO CR)', '#ef4444');
      }
    }

    this.updateHUD();
  }

  triggerOverflow() {
    this.state = 'over';
    this.audio.playGameOver();
    document.getElementById('creditModalTitle').textContent = 'DOWNSTREAM BUFFER OVERFLOW!';
    document.getElementById('creditModalSummary').innerHTML = `
      Ingress buffer exceeded maximum capacity (${this.maxBuffer} flits)!<br>
      Round-trip flight delays broke credit invariants, causing irreversible data loss.
      <br><br><b>Final Wave:</b> Wave ${this.wave} | <b>Flits Delivered:</b> ${this.deliveredCount} | <b>Score:</b> ${this.score} pts
    `;
    document.getElementById('creditOverModal').style.display = 'flex';
  }

  update(dt) {
    if (this.state !== 'running') return;

    // Progress Wave
    this.waveTimer -= dt;
    if (this.waveTimer <= 0) {
      this.wave++;
      this.waveTimer = 25.0;
      this.score += 250 * this.wave;
      this.addTextParticle(this.canvas.width / 2, 50, `WAVE ${this.wave} SPEEDUP!`, '#22c55e');
    }

    // Auto clock
    if (this.clockSpeedMode !== 'manual') {
      this.clockAccumulator += dt;
      if (this.clockAccumulator >= this.clockPeriod) {
        this.clockAccumulator = 0.0;
        this.stepCycle();
      }
    }

    // Update Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const pt = this.particles[i];
      pt.y += pt.vy;
      pt.life -= dt * 1.4;
      if (pt.life <= 0) this.particles.splice(i, 1);
    }
  }

  updateHUD() {
    document.getElementById('creditScore').textContent = this.score;
    document.getElementById('creditWave').textContent = `Wave ${this.wave}`;
    document.getElementById('creditStalls').textContent = this.stalledCycles;

    const eff = this.cycles > 0 ? Math.round(((this.cycles - this.stalledCycles) / this.cycles) * 100) : 100;
    document.getElementById('creditEfficiency').textContent = `${eff}%`;

    // Credits Bar
    const crPct = Math.round((this.txCredits / this.maxBuffer) * 100);
    document.getElementById('txCreditsBar').style.width = `${crPct}%`;
    document.getElementById('txCreditsText').textContent = `${this.txCredits} / ${this.maxBuffer}`;

    // Buffer Bar
    const bufPct = Math.round((this.rxBuffer.length / this.maxBuffer) * 100);
    const bBar = document.getElementById('rxBufferBar');
    bBar.style.width = `${bufPct}%`;
    document.getElementById('rxBufferText').textContent = `${this.rxBuffer.length} / ${this.maxBuffer} Flits`;

    if (bufPct >= 75) {
      bBar.style.background = '#ef4444';
      document.getElementById('rxBufferText').style.color = '#ef4444';
    } else if (bufPct >= 50) {
      bBar.style.background = '#f59e0b';
      document.getElementById('rxBufferText').style.color = '#f59e0b';
    } else {
      bBar.style.background = '#22c55e';
      document.getElementById('rxBufferText').style.color = '#4ade80';
    }
  }

  draw() {
    this.ctx.fillStyle = '#0f172a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 1. Draw Transmitter Core (TX) Box (Left)
    this.ctx.fillStyle = '#1e293b';
    this.ctx.beginPath();
    this.ctx.roundRect(25, 100, 130, 230, 10);
    this.ctx.fill();
    this.ctx.strokeStyle = '#38bdf8';
    this.ctx.lineWidth = 2;
    this.ctx.stroke();

    this.ctx.fillStyle = '#f8fafc';
    this.ctx.font = 'bold 13px "JetBrains Mono", monospace';
    this.ctx.textAlign = 'center';
    this.ctx.fillText('UPSTREAM TX', 90, 126);

    // Credit Counter Display inside TX
    this.ctx.fillStyle = '#0f172a';
    this.ctx.beginPath();
    this.ctx.roundRect(40, 150, 100, 60, 6);
    this.ctx.fill();
    this.ctx.strokeStyle = '#334155';
    this.ctx.lineWidth = 1.5;
    this.ctx.stroke();

    this.ctx.fillStyle = '#94a3b8';
    this.ctx.font = '10px "Inter", sans-serif';
    this.ctx.fillText('CREDIT COUNTER', 90, 168);
    this.ctx.font = 'bold 22px "JetBrains Mono", monospace';
    this.ctx.fillStyle = this.txCredits > 2 ? '#38bdf8' : (this.txCredits > 0 ? '#f59e0b' : '#ef4444');
    this.ctx.fillText(this.txCredits, 90, 198);

    // TX Status Tag
    const isStalled = (this.txCredits === 0 && this.protocol !== 'on_off') || (this.protocol === 'on_off' && this.onOffState === 'STOP');
    this.ctx.fillStyle = isStalled ? '#ef4444' : '#22c55e';
    this.ctx.font = 'bold 11px "JetBrains Mono", monospace';
    this.ctx.fillText(isStalled ? '● STALLED' : '● READY', 90, 240);

    // 2. Draw Receiver Core (RX) Box (Right)
    this.ctx.fillStyle = '#1e293b';
    this.ctx.beginPath();
    this.ctx.roundRect(465, 100, 130, 230, 10);
    this.ctx.fill();
    this.ctx.strokeStyle = '#10b981';
    this.ctx.lineWidth = 2;
    this.ctx.stroke();

    this.ctx.fillStyle = '#f8fafc';
    this.ctx.font = 'bold 13px "JetBrains Mono", monospace';
    this.ctx.textAlign = 'center';
    this.ctx.fillText('DOWNSTREAM RX', 530, 126);

    // RX Ingress FIFO Stack
    this.ctx.fillStyle = '#0f172a';
    this.ctx.beginPath();
    this.ctx.roundRect(480, 150, 100, 150, 6);
    this.ctx.fill();
    this.ctx.strokeStyle = '#334155';
    this.ctx.lineWidth = 1.5;
    this.ctx.stroke();

    // Draw FIFO Slots from bottom up
    const slotH = 14;
    for (let s = 0; s < this.maxBuffer; s++) {
      const sy = 280 - s * (slotH + 2);
      if (s < this.rxBuffer.length) {
        this.ctx.fillStyle = '#38bdf8';
        this.ctx.beginPath();
        this.ctx.roundRect(486, sy, 88, slotH, 3);
        this.ctx.fill();
      } else {
        this.ctx.strokeStyle = '#334155';
        this.ctx.strokeRect(486, sy, 88, slotH);
      }
    }

    // 3. Draw Forward Data Pipeline Link (Top Wire)
    this.ctx.strokeStyle = '#475569';
    this.ctx.lineWidth = 3;
    this.ctx.beginPath();
    this.ctx.moveTo(155, 160);
    this.ctx.lineTo(465, 160);
    this.ctx.stroke();

    this.ctx.fillStyle = '#94a3b8';
    this.ctx.font = 'bold 10px "JetBrains Mono", monospace';
    this.ctx.textAlign = 'center';
    this.ctx.fillText('FORWARD DATA WIRE (3 STAGES)', 310, 145);

    // Draw 3 Pipeline Registers along Forward Wire
    const fStep = (465 - 155) / 4;
    for (let r = 0; r < 3; r++) {
      const rx = 155 + (r + 1) * fStep;
      this.ctx.fillStyle = '#1e293b';
      this.ctx.fillRect(rx - 16, 146, 32, 28);
      this.ctx.strokeStyle = '#64748b';
      this.ctx.lineWidth = 1.5;
      this.ctx.strokeRect(rx - 16, 146, 32, 28);

      if (this.forwardPipe[r]) {
        this.ctx.fillStyle = '#38bdf8';
        this.ctx.shadowColor = '#38bdf8';
        this.ctx.shadowBlur = 8;
        this.ctx.beginPath();
        this.ctx.roundRect(rx - 12, 150, 24, 20, 4);
        this.ctx.fill();
        this.ctx.shadowBlur = 0;
        this.ctx.fillStyle = '#0f172a';
        this.ctx.font = 'bold 9px "JetBrains Mono", monospace';
        this.ctx.fillText('FLIT', rx, 164);
      }
    }

    // 4. Draw Reverse Credit Return Wire (Bottom Wire)
    this.ctx.strokeStyle = '#10b981';
    this.ctx.lineWidth = 2.5;
    this.ctx.beginPath();
    this.ctx.moveTo(465, 270);
    this.ctx.lineTo(155, 270);
    this.ctx.stroke();

    this.ctx.fillStyle = '#10b981';
    this.ctx.font = 'bold 10px "JetBrains Mono", monospace';
    this.ctx.fillText('REVERSE CREDIT LINE (RTT = 5 CYCLES)', 310, 290);

    // Draw 2 Stages along Credit Wire
    const cStep = (465 - 155) / 3;
    for (let c = 0; c < 2; c++) {
      const cx = 465 - (c + 1) * cStep;
      this.ctx.fillStyle = '#1e293b';
      this.ctx.fillRect(cx - 14, 256, 28, 28);
      this.ctx.strokeStyle = '#10b981';
      this.ctx.strokeRect(cx - 14, 256, 28, 28);

      if (this.creditWire[c]) {
        this.ctx.fillStyle = '#4ade80';
        this.ctx.shadowColor = '#4ade80';
        this.ctx.shadowBlur = 8;
        this.ctx.beginPath();
        this.ctx.arc(cx, 270, 7, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.shadowBlur = 0;
      }
    }

    // 5. Draw Particles
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
      this.ctx.fillText('Press "Start Command" to Play!', this.canvas.width / 2, this.canvas.height / 2 - 10);
      this.ctx.font = '13px "Inter", sans-serif';
      this.ctx.fillStyle = '#94a3b8';
      this.ctx.fillText('Manage credit-based flow control with flight-time delay RTT = 5 cycles', this.canvas.width / 2, this.canvas.height / 2 + 18);
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

let creditGame = null;
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('creditCanvas')) {
    creditGame = new CreditGame('creditCanvas');
  }
});

function startCreditGame() {
  if (creditGame) creditGame.start();
}

function restartCreditGame() {
  if (creditGame) creditGame.start();
}

function fireCreditClock() {
  if (creditGame) creditGame.stepCycle();
}

function activateDrainBoost() {
  if (creditGame) creditGame.activateDrainBoost();
}

function setCreditProtocol(proto) {
  if (creditGame) creditGame.protocol = proto;
}

function setCreditClockSpeed(spd) {
  if (creditGame) {
    creditGame.clockSpeedMode = spd;
    if (spd === 'auto_1') creditGame.clockPeriod = 1.0;
    else if (spd === 'auto_2') creditGame.clockPeriod = 0.5;
  }
}

function toggleCreditSound() {
  if (!creditGame) return;
  creditGame.audio.enabled = !creditGame.audio.enabled;
  document.getElementById('creditSoundBtn').textContent = creditGame.audio.enabled ? '🔊 Sound: ON' : '🔈 Sound: OFF';
}

function toggleCreditPause() {
  if (creditGame) creditGame.togglePause();
}

function saveCreditRecord() {
  if (!creditGame) return;
  const name = document.getElementById("creditCallsign").value.trim() || "Flow Commander";
  const org = document.getElementById("creditOrg").value.trim() || "Silicon Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const eff = creditGame.cycles > 0 ? Math.round(((creditGame.cycles - creditGame.stalledCycles) / creditGame.cycles) * 100) : 100;
  const record = {
    name: name,
    org: org,
    track: `Credit Commander (Wave ${creditGame.wave})`,
    score: creditGame.score,
    accuracy: eff, // Link efficiency %
    certId: `CREDIT-WAVE-${creditGame.wave}`,
    date: dateStr,
    type: "credit"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("creditSaveConfirm").style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitCreditToGithub() {
  if (!creditGame) return;
  const name = document.getElementById("creditCallsign").value.trim() || "Flow Commander";
  const org = document.getElementById("creditOrg").value.trim() || "Silicon Lab";
  const eff = creditGame.cycles > 0 ? Math.round(((creditGame.cycles - creditGame.stalledCycles) / creditGame.cycles) * 100) : 100;
  const title = `[credit-highscore] ${name} — ${creditGame.score} pts (${eff}% Efficiency)`;
  const body = [
    "### Credit Commander Flow Control High Score",
    `- **Commander**: ${name}`,
    `- **Institution/Handle**: ${org}`,
    `- **High Score**: ${creditGame.score} pts`,
    `- **Link Efficiency**: ${eff}%`,
    `- **Flits Delivered**: ${creditGame.deliveredCount}`,
    `- **Wave Reached**: Wave ${creditGame.wave}`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: creditGame.score,
      efficiency: eff,
      delivered: creditGame.deliveredCount,
      wave: creditGame.wave,
      type: "credit"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}
</script>
