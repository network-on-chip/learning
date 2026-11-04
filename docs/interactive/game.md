# 🎮 Deadlock Buster: The NoC Buffer Defense Game

Welcome to **Deadlock Buster**, an interactive arcade challenge where you serve as the router arbiter. Keep the chip alive by preventing circular buffer deadlocks as traffic waves intensify! High scores can be directly published to the **Community Leaderboard**.

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

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="gameCanvas" width="620" height="460"></canvas>
    
    <!-- Game Over / Victory Modal -->
    <div id="gameOverModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.92); border-radius:12px; display:none; flex-direction:column; justify-content:center; align-items:center; padding:2rem; box-sizing:border-box; color:#ffffff; text-align:center;">
      <div style="font-size:2.5rem; margin-bottom:0.5rem;">💥</div>
      <h2 style="margin:0 0 0.5rem 0; font-size:1.8rem; color:#f87171;">CHIP NETWORK DEADLOCKED!</h2>
      <p id="gameOverSummary" style="color:#cbd5e1; font-size:1rem; max-width:480px; margin-bottom:1.25rem;">
        Circular buffer dependencies locked 4 routers simultaneously.
      </p>

      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.5rem; width:100%; max-width:420px; box-sizing:border-box; text-align:left;">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Enter Your Callsign / Name:</label>
        <input type="text" id="playerCallsign" class="noc-sim-select" style="width:100%; box-sizing:border-box; margin-bottom:0.75rem;" placeholder="e.g. Master Arbiter" value="NoC Defender">
        <label style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:0.35rem;">Institution / Handle:</label>
        <input type="text" id="playerOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box;" placeholder="e.g. Stanford / SJTU" value="Silicon Lab">
      </div>

      <div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
        <button class="noc-sim-btn" onclick="saveGameRecord()" style="background:#22c55e;">💾 Inscribe on Leaderboard</button>
        <button class="noc-sim-btn" onclick="submitGameToGithub()" style="background:#0284c7;">📤 Submit to GitHub</button>
        <a href="../../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none; color:#ffffff !important;">🏆 View Leaderboard</a>
        <button class="noc-sim-btn secondary" onclick="restartGame()" style="color:#ffffff !important;">🔄 Play Again</button>
      </div>
      <div id="saveConfirmMsg" style="margin-top:0.75rem; color:#4ade80; font-size:0.85rem; font-weight:600; display:none;">
        ✓ Score successfully recorded in your browser Leaderboard!
      </div>
    </div>
  </div>

  <div id="gameInstructions" style="margin-top:1rem; padding:0.85rem 1rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; font-size:0.85rem; color:var(--md-default-fg-color--lighter); line-height:1.6;">
    <strong>How to Play:</strong>
    Packets spawn and navigate between routers. Under <em>Unrestricted Adaptive</em> routing, high traffic creates circular channel dependencies (routers will glow <span style="color:#ef4444; font-weight:700;">pulsing RED</span>!).
    When a deadlock forms, press <strong>SPACEBAR</strong> or click <strong>Flush Escape Channel</strong> to deploy Duato's escape mechanism and drain the frozen flits before 4 routers freeze simultaneously!
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
    this.deadlockFlushed = 0;
    this.wave = 1;
    this.isPlaying = false;
    this.isOver = false;
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
    this.deadlockFlushed = 0;
    this.wave = 1;
    this.flits = [];
    this.deadlockedNodes.clear();
    this.nodeBuffers.fill(0);
    this.isPlaying = true;
    this.isOver = false;

    document.getElementById("gameOverModal").style.display = "none";
    document.getElementById("saveConfirmMsg").style.display = "none";
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
      const count = this.deadlockedNodes.size;
      this.score += count * 60;
      this.deadlockFlushed += count;
      document.getElementById("gameScore").textContent = this.score;
      this.deadlockedNodes.clear();
      document.getElementById("gameDeadlocks").textContent = "0";

      // Unblock flits via escape VC
      for (const f of this.flits) {
        f.isBlocked = false;
        f.next = this.computeNext(f.curr, f.dst);
      }
    }
  }

  gameOver() {
    this.isPlaying = false;
    this.isOver = true;
    const modal = document.getElementById("gameOverModal");
    modal.style.display = "flex";
    document.getElementById("gameOverSummary").innerHTML = 
      `Final Score: <strong>${this.score} pts</strong> | Wave Reached: <strong>Wave ${this.wave}</strong> | Deadlocks Cleared: <strong>${this.deadlockFlushed}</strong>`;
    saveGameRecord();
  }

  update() {
    if (!this.isPlaying || this.isOver) return;

    this.spawnTimer++;
    const spawnRate = Math.max(16, 55 - this.wave * 6);
    if (this.spawnTimer % spawnRate === 0 && this.flits.length < 24) {
      this.spawnFlit();
    }

    if (this.spawnTimer % 350 === 0) {
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
          this.score += 25;
          document.getElementById("gameScore").textContent = this.score;
          this.flits.splice(i, 1);
          continue;
        }
      }

      // Check for deadlock in adaptive mode
      const targetIdx = f.next.y * this.cols + f.next.x;
      if (this.policy === 'adaptive' && this.nodeBuffers[targetIdx] >= 3 && Math.random() < 0.035) {
        f.isBlocked = true;
        this.deadlockedNodes.add(targetIdx);
        document.getElementById("gameDeadlocks").textContent = this.deadlockedNodes.size;

        // Trigger Game Over if 4 or more nodes are locked!
        if (this.deadlockedNodes.size >= 4) {
          this.gameOver();
          return;
        }
      }

      if (!f.isBlocked) {
        f.progress += 0.045;
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

    if (!this.isPlaying && !this.isOver) {
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

function restartGame() {
  if (game) game.start();
}

function activateEscapeChannel() {
  if (game) game.flushEscape();
}

function setGamePolicy(pol) {
  if (game) game.policy = pol;
}

function saveGameRecord() {
  if (!game) return;
  const name = document.getElementById("playerCallsign").value.trim() || "NoC Defender";
  const org = document.getElementById("playerOrg").value.trim() || "Silicon Lab";
  const dateStr = new Date().toISOString().split("T")[0];

  const record = {
    name: name,
    org: org,
    track: `Deadlock Buster (Wave ${game.wave})`,
    score: game.score,
    accuracy: game.deadlockFlushed, // Cleared deadlocks
    certId: `GAME-WAVE-${game.wave}`,
    date: dateStr,
    type: "game"
  };

  try {
    const list = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    list.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(list.slice(0, 50)));
    document.getElementById("saveConfirmMsg").style.display = "block";
  } catch(e) {
    console.error(e);
  }
}

function submitGameToGithub() {
  if (!game) return;
  const name = document.getElementById("playerCallsign").value.trim() || "NoC Defender";
  const org = document.getElementById("playerOrg").value.trim() || "Silicon Lab";
  const title = `[game-highscore] ${name} — ${game.score} pts (Wave ${game.wave})`;
  const body = [
    "### Deadlock Buster Arcade High Score Submission",
    `- **Player**: ${name}`,
    `- **Institution/Handle**: ${org}`,
    `- **High Score**: ${game.score} pts`,
    `- **Wave Reached**: Wave ${game.wave}`,
    `- **Deadlocks Cleared**: ${game.deadlockFlushed}`,
    `- **Date**: ${new Date().toISOString().split("T")[0]}`,
    "",
    "```json",
    JSON.stringify({
      player: name,
      org: org,
      score: game.score,
      wave: game.wave,
      cleared: game.deadlockFlushed,
      type: "game"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/network-on-chip/learning/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=game-score,leaderboard`;
  window.open(url, '_blank');
}

window.addEventListener('keydown', (e) => {
  if (e.code === 'Space') {
    e.preventDefault();
    activateEscapeChannel();
  }
});
</script>
