// Interactive Network-on-Chip (NoC) 2D Mesh & Torus Routing Simulator

class NoCSimulator {
  constructor(canvasId, logId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.logEl = document.getElementById(logId);

    this.rows = 4;
    this.cols = 4;
    this.topology = 'mesh'; // 'mesh' or 'torus'
    this.algorithm = 'xy'; // 'xy', 'west-first', 'odd-even'
    this.speed = 1; // 1x, 2x, 4x

    this.selectedSrc = null;
    this.selectedDst = null;
    this.cycle = 0;
    this.isRunning = true;
    this.packets = []; // Active flits
    this.packetCounter = 0;
    this.stats = { injected: 0, delivered: 0, totalHops: 0 };

    this.nodeRadius = 22;
    this.padding = 60;

    this.initCanvas();
    this.bindEvents();
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
    this.log("NoC Simulator initialized. Click a source node, then a destination node to inject packets.");
  }

  initCanvas() {
    this.width = this.canvas.width = 620;
    this.height = this.canvas.height = 460;
    this.stepX = (this.width - 2 * this.padding) / (this.cols - 1);
    this.stepY = (this.height - 2 * this.padding) / (this.rows - 1);
  }

  setTopology(topo) {
    this.topology = topo;
    this.packets = [];
    this.log(`Topology switched to: ${topo.toUpperCase()}`);
  }

  setAlgorithm(algo) {
    this.algorithm = algo;
    this.log(`Routing algorithm switched to: ${algo.toUpperCase()}`);
  }

  getNodePos(x, y) {
    return {
      px: this.padding + x * this.stepX,
      py: this.padding + y * this.stepY
    };
  }

  bindEvents() {
    this.canvas.addEventListener('click', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.canvas.width / rect.width;
      const scaleY = this.canvas.height / rect.height;
      const mx = (e.clientX - rect.left) * scaleX;
      const my = (e.clientY - rect.top) * scaleY;

      for (let r = 0; r < this.rows; r++) {
        for (let c = 0; c < this.cols; c++) {
          const { px, py } = this.getNodePos(c, r);
          const dist = Math.hypot(mx - px, my - py);
          if (dist <= this.nodeRadius + 6) {
            this.handleNodeClick(c, r);
            return;
          }
        }
      }
    });
  }

  handleNodeClick(x, y) {
    if (!this.selectedSrc) {
      this.selectedSrc = { x, y };
      this.log(`Source selected: R(${x},${y}). Now click a destination node.`);
    } else if (!this.selectedDst) {
      if (this.selectedSrc.x === x && this.selectedSrc.y === y) {
        this.selectedSrc = null;
        this.log("Selection cancelled.");
        return;
      }
      this.selectedDst = { x, y };
      this.injectPacket(this.selectedSrc, this.selectedDst);
      this.selectedSrc = null;
      this.selectedDst = null;
    }
  }

  injectPacket(src, dst) {
    this.packetCounter++;
    const flitColors = ['#2563eb', '#38bdf8', '#fb923c'];
    const p = {
      id: this.packetCounter,
      src: { ...src },
      dst: { ...dst },
      curr: { ...src },
      next: null,
      hops: 0,
      progress: 0,
      color: flitColors[this.packetCounter % flitColors.length],
      done: false
    };
    p.next = this.computeNextHop(p.curr, p.dst, p.src);
    this.packets.push(p);
    this.stats.injected++;
    this.log(`[Cycle ${this.cycle}] Injected Pkt #${p.id}: R(${src.x},${src.y}) -> R(${dst.x},${dst.y}) via ${this.algorithm.toUpperCase()}`);
  }

  computeNextHop(curr, dst, src) {
    if (curr.x === dst.x && curr.y === dst.y) return null;

    if (this.algorithm === 'xy') {
      // Dimension Order Routing (X then Y)
      if (curr.x < dst.x) return { x: curr.x + 1, y: curr.y };
      if (curr.x > dst.x) return { x: curr.x - 1, y: curr.y };
      if (curr.y < dst.y) return { x: curr.x, y: curr.y + 1 };
      if (curr.y > dst.y) return { x: curr.x, y: curr.y - 1 };
    } else if (this.algorithm === 'west-first') {
      // West-First Turn Model: If heading west, must turn west first
      if (dst.x < curr.x) {
        return { x: curr.x - 1, y: curr.y };
      }
      // Can adaptively choose East, North, or South
      const cand = [];
      if (dst.x > curr.x) cand.push({ x: curr.x + 1, y: curr.y });
      if (dst.y > curr.y) cand.push({ x: curr.x, y: curr.y + 1 });
      if (dst.y < curr.y) cand.push({ x: curr.x, y: curr.y - 1 });
      return cand[Math.floor(Math.random() * cand.length)] || null;
    } else if (this.algorithm === 'odd-even') {
      // Odd-Even Deadlock-Free Turn Model
      const e0 = (curr.x % 2 === 0);
      const cand = [];
      if (dst.x > curr.x) cand.push({ x: curr.x + 1, y: curr.y });
      if (dst.x < curr.x && !e0) cand.push({ x: curr.x - 1, y: curr.y });
      if (dst.y > curr.y) cand.push({ x: curr.x, y: curr.y + 1 });
      if (dst.y < curr.y) cand.push({ x: curr.x, y: curr.y - 1 });
      return cand[0] || { x: curr.x, y: (curr.y < dst.y ? curr.y + 1 : curr.y - 1) };
    }
    return null;
  }

  step() {
    this.cycle++;
    for (let i = this.packets.length - 1; i >= 0; i--) {
      const p = this.packets[i];
      if (p.done) continue;

      p.progress += 0.05 * this.speed;
      if (p.progress >= 1) {
        p.progress = 0;
        p.curr = { ...p.next };
        p.hops++;

        if (p.curr.x === p.dst.x && p.curr.y === p.dst.y) {
          p.done = true;
          this.stats.delivered++;
          this.stats.totalHops += p.hops;
          this.log(`[Cycle ${this.cycle}] Pkt #${p.id} DELIVERED to R(${p.dst.x},${p.dst.y}) in ${p.hops} hops.`);
          this.packets.splice(i, 1);
        } else {
          p.next = this.computeNextHop(p.curr, p.dst, p.src);
        }
      }
    }
  }

  log(msg) {
    if (!this.logEl) return;
    const item = document.createElement('div');
    item.textContent = msg;
    this.logEl.appendChild(item);
    this.logEl.scrollTop = this.logEl.scrollHeight;
  }

  draw() {
    this.ctx.clearRect(0, 0, this.width, this.height);

    // Draw Links
    this.ctx.lineWidth = 3;
    this.ctx.strokeStyle = '#cbd5e1';

    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const { px, py } = this.getNodePos(c, r);

        // East link
        if (c < this.cols - 1) {
          const next = this.getNodePos(c + 1, r);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
        } else if (this.topology === 'torus') {
          // Wrap-around East link
          const next = this.getNodePos(0, r);
          this.ctx.setLineDash([4, 4]);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(px + 20, py);
          this.ctx.moveTo(next.px - 20, next.py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
          this.ctx.setLineDash([]);
        }

        // South link
        if (r < this.rows - 1) {
          const next = this.getNodePos(c, r + 1);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
        } else if (this.topology === 'torus') {
          // Wrap-around South link
          const next = this.getNodePos(c, 0);
          this.ctx.setLineDash([4, 4]);
          this.ctx.beginPath();
          this.ctx.moveTo(px, py);
          this.ctx.lineTo(px, py + 20);
          this.ctx.moveTo(next.px, next.py - 20);
          this.ctx.lineTo(next.px, next.py);
          this.ctx.stroke();
          this.ctx.setLineDash([]);
        }
      }
    }

    // Draw Active Flits
    for (const p of this.packets) {
      if (!p.next) continue;
      const p1 = this.getNodePos(p.curr.x, p.curr.y);
      const p2 = this.getNodePos(p.next.x, p.next.y);
      const fx = p1.px + (p2.px - p1.px) * p.progress;
      const fy = p1.py + (p2.py - p1.py) * p.progress;

      // Flit head
      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(fx, fy, 9, 0, Math.PI * 2);
      this.ctx.fill();

      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 9px sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(p.id, fx, fy);
    }

    // Draw Router Nodes
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const { px, py } = this.getNodePos(c, r);
        const isSrc = this.selectedSrc && this.selectedSrc.x === c && this.selectedSrc.y === r;
        const isDst = this.selectedDst && this.selectedDst.x === c && this.selectedDst.y === r;

        this.ctx.beginPath();
        this.ctx.arc(px, py, this.nodeRadius, 0, Math.PI * 2);

        if (isSrc) {
          this.ctx.fillStyle = '#2563eb'; // Source Royal Blue
        } else if (isDst) {
          this.ctx.fillStyle = '#ea580c'; // Dst Orange
        } else {
          this.ctx.fillStyle = '#0f172a'; // Default Slate 900
        }
        this.ctx.fill();

        this.ctx.lineWidth = 2.5;
        this.ctx.strokeStyle = '#ffffff';
        this.ctx.stroke();

        // Node label: (c, r)
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = 'bold 11px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(`${c},${r}`, px, py);
      }
    }

    // Update Stats Display if elements exist
    const statEl = document.getElementById('nocStats');
    if (statEl) {
      const avg = this.stats.delivered > 0 ? (this.stats.totalHops / this.stats.delivered).toFixed(2) : '0';
      statEl.innerHTML = `<b>Cycle:</b> ${this.cycle} | <b>Active Flits:</b> ${this.packets.length} | <b>Delivered:</b> ${this.stats.delivered} | <b>Avg Hops:</b> ${avg}`;
    }
  }

  animate() {
    if (this.isRunning) {
      this.step();
    }
    this.draw();
    requestAnimationFrame(this.animate);
  }
}

// Global initialization
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('nocCanvas')) {
    window.sim = new NoCSimulator('nocCanvas', 'nocLog');
  }
});
