# 🎮 Deadlock Buster: The NoC Buffer Defense Game

Welcome to **Deadlock Buster**, an interactive arcade challenge where you serve as the router arbiter. Keep the chip alive by preventing circular buffer deadlocks as traffic waves intensify!

<div class="noc-sim-container">
  <div class="noc-sim-controls">
    <button id="gameStartBtn" class="noc-sim-btn" onclick="startDeadlockGame()">▶ Start Game</button>
    <button class="noc-sim-btn secondary" onclick="activateEscapeChannel()">⚡ Flush Escape Channel (Spacebar)</button>
    
    <label><b>Routing Policy:</b>
      <select id="gamePolicy" class="noc-sim-select" onchange="setGamePolicy(this.value)">
        <option value="adaptive">Unrestricted Adaptive (High Risk of Deadlock!)</option>
        <option value="west-first">West-First Turn Model (Protected)</option>
        <option value="xy">Strict XY Routing (Deadlock Immune)</option>
      </select>
    </label>

    <div style="margin-left:auto; display:flex; gap:1rem; align-items:center; font-weight:700;">
      <span style="color:var(--tcl-blue-600);">Score: <span id="gameScore">0</span></span>
      <span style="color:#ef4444;">Deadlocks: <span id="gameDeadlocks">0</span></span>
      <span style="color:#22c55e;">Wave: <span id="gameWave">1</span></span>
    </div>
  </div>

  <div class="noc-sim-canvas-wrap">
    <canvas id="gameCanvas" width="620" height="460"></canvas>
  </div>

  <div id="gameInstructions" style="margin-top:1rem; padding:0.85rem 1rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; font-size:0.85rem; color:var(--md-default-fg-color--lighter); line-height:1.6;">
    <strong>How to Play:</strong>
    Packets spawn and navigate between routers. Under <em>Unrestricted Adaptive</em> routing, high traffic creates circular channel dependencies (routers will glow <span style="color:#ef4444; font-weight:700;">pulsing RED</span>!).
    When a deadlock forms, press <strong>SPACEBAR</strong> or click <strong>Flush Escape Channel</strong> to deploy Duato's escape mechanism and drain the frozen flits before the buffer overflow timer expires!
  </div>
</div>

<script>
class DeadlockGame {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.rows = 4;
    this.cols = 4;
    this.policy = 'adaptive';

    this.score = 0;
    this.deadlockCount = 0;
    this.wave = 1;
    this.isPlaying = false;
    this.spawnTimer = 0;

    this.flits = [];
    this.deadlockedNodes = new Set();
    this.nodeBuffers = Array.from({ length: 16 }, () => 0);

    this.nodeRadius = 22;
    this.padding = 60;
    this.stepX = (this.canvas.width - 2 * this.padding) / (this.cols - 1);
    this.stepY = (this.canvas.height - 2 * this.padding) / (this.rows - 1);

    this.loop = this.loop.bind(this);
    requestAnimationFrame(this.loop);
  }

  start() {
    this.score = 0;
    this.deadlockCount = 0;
    this.wave = 1;
    this.flits = [];
    this.deadlockedNodes.clear();
    this.nodeBuffers.fill(0);
    this.isPlaying = true;
    document.getElementById("gameScore").textContent = "0";
    document.getElementById("gameDeadlocks").textContent = "0";
    document.getElementById("gameWave").textContent = "1";
    document.getElementById("gameStartBtn").textContent = "🔄 Restart";
  }

  getNodePos(x, y) {
    return {
      px: this.padding + x * this.stepX,
      py: this.padding + y * this.stepY
    };
  }

  spawnFlit() {
    const sx = Math.floor(Math.random() * this.cols);
    const sy = Math.floor(Math.random() * this.rows);
    let dx = Math.floor(Math.random() * this.cols);
    let dy = Math.floor(Math.random() * this.rows);
    while (dx === sx && dy === sy) {
      dx = Math.floor(Math.random() * this.cols);
      dy = Math.floor(Math.random() * this.rows);
    }

    const colors = ['#2563eb', '#38bdf8', '#fb923c', '#a855f7'];
    this.flits.push({
      id: Math.floor(Math.random() * 900) + 100,
      curr: { x: sx, y: sy },
      dst: { x: dx, y: dy },
      next: null,
      progress: 0,
      color: colors[Math.floor(Math.random() * colors.length)],
      isBlocked: false
    });
  }

  computeNext(curr, dst) {
    if (curr.x === dst.x && curr.y === dst.y) return null;

    if (this.policy === 'xy') {
      if (curr.x < dst.x) return { x: curr.x + 1, y: curr.y };
      if (curr.x > dst.x) return { x: curr.x - 1, y: curr.y };
      if (curr.y < dst.y) return { x: curr.x, y: curr.y + 1 };
      if (curr.y > dst.y) return { x: curr.x, y: curr.y - 1 };
    } else if (this.policy === 'west-first') {
      if (dst.x < curr.x) return { x: curr.x - 1, y: curr.y };
      const cand = [];
      if (dst.x > curr.x) cand.push({ x: curr.x + 1, y: curr.y });
      if (dst.y > curr.y) cand.push({ x: curr.x, y: curr.y + 1 });
      if (dst.y < curr.y) cand.push({ x: curr.x, y: curr.y - 1 });
      return cand[Math.floor(Math.random() * cand.length)] || null;
    } else {
      // Unrestricted adaptive (allows cycles!)
      const cand = [];
      if (dst.x > curr.x) cand.push({ x: curr.x + 1, y: curr.y });
      if (dst.x < curr.x) cand.push({ x: curr.x - 1, y: curr.y });
      if (dst.y > curr.y) cand.push({ x: curr.x, y: curr.y + 1 });
      if (dst.y < curr.y) cand.push({ x: curr.x, y: curr.y - 1 });
      return cand[Math.floor(Math.random() * cand.length)] || null;
    }
    return null;
  }

  flushEscape() {
    if (this.deadlockedNodes.size > 0) {
      this.score += this.deadlockedNodes.size * 50;
      document.getElementById("gameScore").textContent = this.score;
      this.deadlockedNodes.clear();
      // Unblock all flits by forcing XY routing on escape VC
      for (const f of this.flits) {
        f.isBlocked = false;
        f.next = this.computeNext(f.curr, f.dst);
      }
    }
  }

  update() {
    if (!this.isPlaying) return;

    this.spawnTimer++;
    const spawnRate = Math.max(20, 65 - this.wave * 8);
    if (this.spawnTimer % spawnRate === 0 && this.flits.length < 24) {
      this.spawnFlit();
    }

    if (this.spawnTimer % 400 === 0) {
      this.wave++;
      document.getElementById("gameWave").textContent = this.wave;
    }

    // Step flits
    for (let i = this.flits.length - 1; i >= 0; i--) {
      const f = this.flits[i];
      if (!f.next) {
        f.next = this.computeNext(f.curr, f.dst);
        if (!f.next) {
          // Delivered!
          this.score += 20;
          document.getElementById("gameScore").textContent = this.score;
          this.flits.splice(i, 1);
          continue;
        }
      }

      // Check for deadlock in adaptive mode
      const targetIdx = f.next.y * this.cols + f.next.x;
      if (this.policy === 'adaptive' && this.nodeBuffers[targetIdx] >= 3 && Math.random() < 0.03) {
        f.isBlocked = true;
        this.deadlockedNodes.add(targetIdx);
        this.deadlockCount++;
        document.getElementById("gameDeadlocks").textContent = this.deadlockedNodes.size;
      }

      if (!f.isBlocked) {
        f.progress += 0.04;
        if (f.progress >= 1) {
          f.progress = 0;
          f.curr = { ...f.next };
          f.next = null;
        }
      }
    }

    // Recalculate buffer counts
    this.nodeBuffers.fill(0);
    for (const f of this.flits) {
      const idx = f.curr.y * this.cols + f.curr.x;
      this.nodeBuffers[idx]++;
    }
  }

  draw() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw Links
    this.ctx.lineWidth = 2.5;
    this.ctx.strokeStyle = '#334155';
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const { px, py } = this.getNodePos(c, r);
        if (c < this.cols - 1) {
          const next = this.getNodePos(c + 1, r);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
        }
        if (r < this.rows - 1) {
          const next = this.getNodePos(c, r + 1);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
        }
      }
    }

    // Draw Flits
    for (const f of this.flits) {
      const p1 = this.getNodePos(f.curr.x, f.curr.y);
      let fx = p1.px;
      let fy = p1.py;
      if (f.next && !f.isBlocked) {
        const p2 = this.getNodePos(f.next.x, f.next.y);
        fx += (p2.px - p1.px) * f.progress;
        fy += (p2.py - p1.py) * f.progress;
      }

      this.ctx.fillStyle = f.isBlocked ? '#ef4444' : f.color;
      this.ctx.beginPath();
      this.ctx.arc(fx, fy, 8, 0, Math.PI * 2);
      this.ctx.fill();
    }

    // Draw Routers
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const { px, py } = this.getNodePos(c, r);
        const idx = r * this.cols + c;
        const isDeadlocked = this.deadlockedNodes.has(idx);

        this.ctx.beginPath();
        this.ctx.arc(px, py, this.nodeRadius, 0, Math.PI * 2);

        if (isDeadlocked) {
          const pulse = (Math.sin(Date.now() / 150) + 1) / 2;
          this.ctx.fillStyle = pulse > 0.5 ? '#ef4444' : '#7f1d1d';
        } else {
          this.ctx.fillStyle = '#0f172a';
        }
        this.ctx.fill();

        this.ctx.lineWidth = isDeadlocked ? 3 : 1.5;
        this.ctx.strokeStyle = isDeadlocked ? '#f87171' : '#38bdf8';
        this.ctx.stroke();

        // Label
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = 'bold 10px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(`R${idx}`, px, py - 3);

        // Buffer badge
        const buf = this.nodeBuffers[idx];
        this.ctx.font = '9px monospace';
        this.ctx.fillStyle = buf > 2 ? '#fb923c' : '#94a3b8';
        this.ctx.fillText(`buf:${buf}`, px, py + 8);
      }
    }

    if (!this.isPlaying) {
      this.ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 22px sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.fillText('Press "Start Game" to Play!', this.canvas.width / 2, this.canvas.height / 2);
    }
  }

  loop() {
    this.update();
    this.draw();
    requestAnimationFrame(this.loop);
  }
}

let game = null;
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('gameCanvas')) {
    game = new DeadlockGame('gameCanvas');
  }
});

function startDeadlockGame() {
  if (game) game.start();
}

function activateEscapeChannel() {
  if (game) game.flushEscape();
}

function setGamePolicy(pol) {
  if (game) game.policy = pol;
}

window.addEventListener('keydown', (e) => {
  if (e.code === 'Space') {
    e.preventDefault();
    activateEscapeChannel();
  }
});
</script>
