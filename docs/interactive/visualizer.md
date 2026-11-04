# 2D Mesh & Torus Routing Visualizer

An interactive cycle-accurate routing laboratory. Directly observe how flits navigate on-chip routers, arbitrate channels, and avoid deadlocks across different network topologies and routing algorithms.

<div class="noc-sim-container">
  <div class="noc-sim-controls">
    <label><b>Topology:</b>
      <select id="topoSelect" class="noc-sim-select" onchange="window.sim.setTopology(this.value)">
        <option value="mesh">2D Mesh (4x4)</option>
        <option value="torus">2D Torus (4x4 with Wrap-around)</option>
      </select>
    </label>
    
    <label><b>Algorithm:</b>
      <select id="algoSelect" class="noc-sim-select" onchange="window.sim.setAlgorithm(this.value)">
        <option value="xy">Dimension-Order (XY Routing)</option>
        <option value="west-first">West-First (Turn Model)</option>
        <option value="odd-even">Odd-Even (Adaptive Deadlock-Free)</option>
      </select>
    </label>

    <label><b>Speed:</b>
      <select id="speedSelect" class="noc-sim-select" onchange="window.sim.speed = parseFloat(this.value)">
        <option value="1">1.0x Normal</option>
        <option value="2">2.0x Fast</option>
        <option value="0.5">0.5x Slow Motion</option>
      </select>
    </label>

    <button class="noc-sim-btn" onclick="injectRandomPacket()">🎲 Inject Random Packet</button>
    <button class="noc-sim-btn secondary" onclick="toggleSim(this)">⏸ Pause</button>
    <button class="noc-sim-btn secondary" onclick="clearPackets()">Clear</button>
  </div>

  <div id="nocStats" style="margin-bottom: 0.75rem; font-size: 0.9rem; color: var(--noc-text-main);">
    <b>Cycle:</b> 0 | <b>Active Flits:</b> 0 | <b>Delivered:</b> 0 | <b>Avg Hops:</b> 0
  </div>

  <div class="noc-sim-canvas-wrap">
    <canvas id="nocCanvas"></canvas>
  </div>

  <div id="nocLog" class="noc-sim-log"></div>
</div>

<script src="../assets/js/noc-visualizer.js"></script>
<script>
  function injectRandomPacket() {
    if (!window.sim) return;
    const sx = Math.floor(Math.random() * window.sim.cols);
    const sy = Math.floor(Math.random() * window.sim.rows);
    let dx = Math.floor(Math.random() * window.sim.cols);
    let dy = Math.floor(Math.random() * window.sim.rows);
    while (dx === sx && dy === sy) {
      dx = Math.floor(Math.random() * window.sim.cols);
      dy = Math.floor(Math.random() * window.sim.rows);
    }
    window.sim.injectPacket({x: sx, y: sy}, {x: dx, y: dy});
  }

  function toggleSim(btn) {
    if (!window.sim) return;
    window.sim.isRunning = !window.sim.isRunning;
    btn.textContent = window.sim.isRunning ? "⏸ Pause" : "▶ Resume";
  }

  function clearPackets() {
    if (!window.sim) return;
    window.sim.packets = [];
    window.sim.log("Active packets cleared.");
  }
</script>

---

## How to Experiment

1. **Manual Injection**: Click on any router node $(x,y)$ to select it as the **source** (turns cyan). Then click another router to set the **destination** (turns orange).
2. **Dimension-Order Routing (DOR / XY)**:
   - Notice that packets strictly traverse along the horizontal axis ($X$) until reaching the target column, then turn onto the vertical axis ($Y$).
   - Turns from $Y$ to $X$ are strictly prohibited, guaranteeing that the Channel Dependency Graph (CDG) is acyclic.
3. **West-First Turn Model**:
   - In West-First, packets heading West must do so first. Once a packet turns North or South, it can never turn West again. This eliminates two turns ($\text{North} \rightarrow \text{West}$ and $\text{South} \rightarrow \text{West}$), preventing routing cycles while retaining adaptive path diversity towards the East.
4. **Odd-Even Turn Model**:
   - Odd-Even restricts turns depending on whether the current node's column is even or odd. It provides minimal restriction without requiring virtual channels!

> [!TIP]
> Dive deeper into the mathematical proof of deadlock freedom in [Track 4: Routing & Deadlock Avoidance](../track4-routing-deadlock/01-deterministic-dor.md).
