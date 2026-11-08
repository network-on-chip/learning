# 🔒 Deadlock Verification & CDG Escape Channel Transition Engine

An engineering-grade computer architecture simulation workbench for modeling, verifying, and eliminating routing deadlocks in multi-core and accelerator networks. Inspect Channel Dependency Graphs (CDG), compute Strongly Connected Components (SCC) to detect circular buffer dependencies, evaluate Dally & Seitz and Duato deadlock-freedom theorems, and synthesize escape virtual channel recovery logic in real time.

---

## 1. Theoretical Foundations & Deadlock Theorems

Routing deadlocks occur when a set of packets indefinitely hold communication buffers while waiting for buffers held by other packets in the same set, creating an unresolvable circular wait condition:

```
[Packet 1 in Channel C0] ---> waiting for ---> [Channel C1]
           ^                                         |
           |                                         v
     [Channel C3] <--- waiting for <--- [Packet 2 in Channel C2]
```

### 1.1 Channel Dependency Graph (Dally & Seitz, 1987)
Let $C = \{c_1, c_2, \dots, c_P\}$ denote the set of physical and virtual channels in the network. A routing algorithm $R: C \times V \to \mathcal{P}(C)$ defines candidate output channels given current channel and packet destination. The **Channel Dependency Graph (CDG)** $D = (C, E_{dep})$ is a directed graph where directed edge $(c_i, c_j) \in E_{dep}$ exists if and only if a packet holding channel $c_i$ can immediately request acquisition of channel $c_j$:
$$\exists d \in V \quad \text{such that } c_j \in R(c_i, d)$$

> **Dally & Seitz Theorem**: A deterministic routing algorithm $R$ is deadlock-free for an interconnect topology if and only if its Channel Dependency Graph $D$ contains **no directed cycles** (i.e., $D$ is a Directed Acyclic Graph, DAG).

### 1.2 Duato's Necessary and Sufficient Condition for Adaptive Routing (1993, 1996)
Restricting all channels to an acyclic CDG limits path diversity and reduces network throughput. Duato proved that adaptive routing can permit cyclic channel dependencies in a primary channel set $C_1$ provided an acyclic escape subnetwork $C_{esc}$ is maintained:

> **Duato's Theorem**: An adaptive routing algorithm $R$ is deadlock-free if and only if there exists a routing sub-function $R_{esc} \subseteq R$ defined over a connected subnetwork of escape channels $C_{esc} \subseteq C$ such that:
> 1. The Channel Dependency Graph of the escape subnetwork $D_{esc} = (C_{esc}, E_{esc})$ is strictly **acyclic**.
> 2. Packets in any adaptive channel $C \setminus C_{esc}$ can always transition into the escape subnetwork $C_{esc}$ when blocked.
> 3. Once a packet enters an escape channel $C_{esc}$, it remains within $C_{esc}$ until it reaches its destination (or transitions out only when destination buffers are guaranteed available), preventing escape channels from closing circular dependency loops.

---

## 2. Interactive CDG Verification & Escape Channel Workbench

<div class="noc-sim-container">
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <button id="simRunBtn" class="noc-sim-btn" onclick="toggleDeadlockSim()">▶ Run Clock</button>
    <button class="noc-sim-btn secondary" onclick="stepDeadlockClock()">⏭ Single Step</button>
    <button class="noc-sim-btn secondary" onclick="resetDeadlockSim()">🔄 Reset Mesh</button>
    <button class="noc-sim-btn" onclick="triggerDuatoEscape()" style="background:#0284c7; border:none;">⚡ Drain via Duato Escape VC</button>

    <label><b>Routing Policy:</b>
      <select id="simPolicySelect" class="noc-sim-select" onchange="setRoutingPolicy(this.value)">
        <option value="adaptive">Unrestricted Fully Adaptive (Prone to Circular Wait)</option>
        <option value="xy">Strict Dimension-Order XY (Acyclic CDG, Zero Deadlocks)</option>
        <option value="duato">Duato's Adaptive + Escape VC (High Perf + Deadlock-Free)</option>
      </select>
    </label>

    <label><b>Traffic Workload:</b>
      <select id="simTrafficSelect" class="noc-sim-select" onchange="changeTrafficWorkload(this.value)">
        <option value="adversarial_ring">Adversarial Ring Traffic (Induces Circular Deadlock)</option>
        <option value="uniform">Uniform Random Traffic</option>
        <option value="bit_complement">Bit-Complement Traffic</option>
        <option value="transpose">Transpose Traffic</option>
      </select>
    </label>

    <label><b>Injection Rate (λ):</b>
      <input type="range" id="simInjRate" min="0.1" max="0.9" step="0.05" value="0.45" oninput="updateInjRateDisplay(this.value)" style="vertical-align:middle; width:90px;">
      <span id="injRateVal" style="font-family:'JetBrains Mono', monospace; font-size:0.8rem; color:#38bdf8;">0.45</span>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn secondary" onclick="exportSmtFormula()">📐 Export SMT-LIB2 Assertion</button>
      <button class="noc-sim-btn secondary" onclick="exportDuatoVerilog()">📋 Export Verilog Arbiter</button>
    </div>

    <!-- Live Engineering HUD -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(135px, 1fr)); gap:0.6rem; width:100%; margin-top:0.5rem; font-family:'JetBrains Mono', monospace; font-size:0.82rem;">
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Network State</span>
        <strong id="hudNetState" style="color:#22c55e; font-size:0.95rem;">NORMAL</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">CDG Elementary Cycles</span>
        <strong id="hudCdgCycles" style="color:#22c55e; font-size:0.95rem;">0 Cycles</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Average Latency</span>
        <strong id="hudAvgLatency" style="color:#38bdf8; font-size:0.95rem;">4.2 cycles</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Throughput (flits/cyc)</span>
        <strong id="hudThroughput" style="color:#f59e0b; font-size:0.95rem;">0.000</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Escape VC Drain</span>
        <strong id="hudEscapeDrain" style="color:#a855f7; font-size:0.95rem;">0 flits</strong>
      </div>
      <div style="background:var(--tcl-surface); padding:0.4rem 0.6rem; border-radius:6px; border:1px solid var(--tcl-border);">
        <span style="color:#64748b; display:block; font-size:0.75rem;">Simulation Cycle</span>
        <strong id="hudSimCycle" style="color:#e2e8f0; font-size:0.95rem;">0</strong>
      </div>
    </div>
  </div>

  <div style="margin:0.75rem 0; padding:0.65rem 0.95rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; font-size:0.83rem; line-height:1.6; color:#94a3b8;">
    <strong style="color:#f8fafc;">CDG Live Monitor:</strong>
    Under <span style="color:#ef4444; font-weight:600;">Unrestricted Adaptive</span> routing, bursty or circular traffic forms cyclic channel dependencies shown as <span style="color:#ef4444; font-weight:700;">pulsing RED loops</span>. Switch to <span style="color:#38bdf8; font-weight:600;">Duato's Escape VC</span> or trigger <strong>⚡ Drain via Duato Escape VC</strong> to observe how packets transition into the acyclic XY escape channel ($VC_1$), dissolving the circular knot!
  </div>

  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="deadlockCanvas" width="620" height="460" style="width:100%; max-width:620px; height:auto; display:block; background:#0f172a; border-radius:10px;"></canvas>
  </div>

  <!-- Real-Time Channel Dependency Diagnostic Table -->
  <div style="margin-top:1rem; display:grid; grid-template-columns: 1fr 1fr; gap:1rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; padding:0.75rem;">
      <strong style="color:#38bdf8; display:block; margin-bottom:0.4rem;">Channel Dependency Graph (CDG) Diagnostics:</strong>
      <div id="cdgStatusDetail" style="color:#94a3b8; font-size:0.75rem; line-height:1.6;">
        Total Directional Channels: 48 (24 links × 2 VCs)<br>
        Active Dependency Edges ($E_{dep}$): <span id="cdgActiveEdges" style="color:#f8fafc;">0</span><br>
        Strongly Connected Components ($|SCC| > 1$): <span id="cdgSccCount" style="color:#22c55e;">0</span>
      </div>
      <div id="cdgCycleList" style="margin-top:0.4rem; font-size:0.72rem; color:#f87171; max-height:60px; overflow-y:auto;">
        No active dependency cycles detected.
      </div>
    </div>

    <div style="background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:8px; padding:0.75rem;">
      <strong style="color:#22c55e; display:block; margin-bottom:0.4rem;">Virtual Channel Buffer Occupancy:</strong>
      <div style="color:#94a3b8; font-size:0.75rem; line-height:1.6;">
        Adaptive VC ($VC_0$) Utilization: <span id="vc0Util" style="color:#38bdf8;">0.0%</span><br>
        Escape VC ($VC_1$) Utilization: <span id="vc1Util" style="color:#a855f7;">0.0%</span><br>
        Max Router Queue Depth: <span id="maxQueueDepth" style="color:#f59e0b;">0 / 4 flits</span>
      </div>
    </div>
  </div>

  <!-- CAD Netlist / Formal Assertion Export Drawer -->
  <div id="deadlockExportDrawer" style="display:none; margin-top:1rem; background:#0b1120; border:1px solid #1e293b; border-radius:8px; padding:0.85rem;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
      <strong id="deadlockExportTitle" style="color:#38bdf8; font-size:0.85rem;">Generated Specification</strong>
      <button class="noc-sim-btn secondary" style="padding:2px 8px; font-size:0.75rem;" onclick="document.getElementById('deadlockExportDrawer').style.display='none'">Close</button>
    </div>
    <textarea id="deadlockExportCode" readonly style="width:100%; height:160px; background:#050811; color:#a5f3fc; border:1px solid #334155; border-radius:6px; font-family:'JetBrains Mono', monospace; font-size:0.75rem; padding:0.5rem; box-sizing:border-box;"></textarea>
  </div>
</div>

---

## 3. Comparison of Deadlock Prevention & Recovery Strategies

| Strategy | Hardware Overhead | Adaptiveness | Latency Penalty | Theorem / Formal Guarantee |
| :--- | :--- | :--- | :--- | :--- |
| **Dimension-Order Routing (XY DOR)** | Zero virtual channels | Zero (Deterministic) | High under non-uniform traffic | Dally & Seitz: Strictly acyclic CDG ($D = \emptyset$). |
| **Turn Prohibition (West-First, Glass & Ni)** | Zero virtual channels | Partially adaptive | Low (only prohibited turns penalized) | Glass & Ni: Breaks cycles in turn matrix ($2/8$ turns eliminated). |
| **Duato's Escape Virtual Channel** | 1 Escape VC ($VC_1$) per physical port | Fully adaptive on $VC_0$ | Minimal (routes adaptively until blocked) | Duato: Acyclic subnetwork $D_{esc}$ guarantees drain without circular wait. |
| **Dally's VC Subnetworks** | $\ge 2$ Virtual Channels | Dimension-reversal adaptive | Low | Dally: Classifies packets into increasing classes to prevent cycles. |
| **Deflection / Hot-Potato (BLESS)** | Zero buffers | Fully adaptive | High under load (deflection loops) | Livelock-free via oldest-first age priority; bufferless implies no deadlock. |

---

<script>
(function() {
  const GRID_SIZE = 4;
  const NUM_ROUTERS = 16;
  const BUFFER_CAPACITY = 4;

  let simRunning = false;
  let simTimer = null;
  let currentCycle = 0;
  let routingPolicy = 'adaptive';
  let trafficWorkload = 'adversarial_ring';
  let injectionRate = 0.45;

  let deliveredFlits = 0;
  let totalLatency = 0;
  let escapeDrains = 0;

  // Routers: each has input queues for East, West, North, South, Local
  // Each queue has VC0 (adaptive) and VC1 (escape)
  let routers = [];
  let packets = []; // active flits traversing the network
  let nextPacketId = 1;
  let detectedCycles = [];

  const canvas = document.getElementById('deadlockCanvas');
  const ctx = canvas.getContext('2d');

  function initRouters() {
    routers = [];
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        const id = r * GRID_SIZE + c;
        routers.push({
          id: id,
          x: c,
          y: r,
          screenX: 80 + c * 150,
          screenY: 70 + r * 110,
          // Input buffers: vc0 and vc1
          buffers: {
            N: { vc0: [], vc1: [] },
            S: { vc0: [], vc1: [] },
            E: { vc0: [], vc1: [] },
            W: { vc0: [], vc1: [] },
            L: { vc0: [], vc1: [] }
          },
          blockedDuration: 0,
          isDeadlocked: false
        });
      }
    }
  }

  window.setRoutingPolicy = function(policy) {
    routingPolicy = policy;
    resetDeadlockSim();
  };

  window.changeTrafficWorkload = function(wl) {
    trafficWorkload = wl;
    resetDeadlockSim();
  };

  window.updateInjRateDisplay = function(val) {
    injectionRate = parseFloat(val);
    document.getElementById('injRateVal').textContent = parseFloat(val).toFixed(2);
  };

  window.toggleDeadlockSim = function() {
    simRunning = !simRunning;
    const btn = document.getElementById('simRunBtn');
    if (simRunning) {
      btn.textContent = '⏸ Pause Clock';
      btn.style.background = '#eab308';
      simTimer = setInterval(stepDeadlockClock, 120);
    } else {
      btn.textContent = '▶ Run Clock';
      btn.style.background = '';
      clearInterval(simTimer);
    }
  };

  window.resetDeadlockSim = function() {
    currentCycle = 0;
    deliveredFlits = 0;
    totalLatency = 0;
    escapeDrains = 0;
    packets = [];
    detectedCycles = [];
    initRouters();
    updateHUD();
    renderMesh();
  };

  window.triggerDuatoEscape = function() {
    // For all blocked packets waiting in VC0, transition them into VC1 (escape channel)
    let transitioned = 0;
    for (let p of packets) {
      if (p.vc === 0 && p.waitCycles > 2) {
        p.vc = 1;
        transitioned++;
      }
    }
    escapeDrains += transitioned;
    evaluateDeadlockCDG();
    updateHUD();
    renderMesh();
  };

  // Step clock cycle
  window.stepDeadlockClock = function() {
    currentCycle++;

    // 1. Packet Injection
    injectTraffic();

    // 2. Route Computation & Switch Traversal
    routeAndTraverse();

    // 3. Detect CDG Cycles and Deadlocks
    evaluateDeadlockCDG();

    // 4. Update HUD and visual state
    updateHUD();
    renderMesh();
  };

  function injectTraffic() {
    for (let r = 0; r < NUM_ROUTERS; r++) {
      if (Math.random() < injectionRate) {
        let dest = -1;
        const curX = routers[r].x;
        const curY = routers[r].y;

        if (trafficWorkload === 'adversarial_ring') {
          // Construct explicit 4-node circular wait cycle: (1,1) -> (2,1) -> (2,2) -> (1,2) -> (1,1)
          if (r === 5) dest = 6;       // (1,1) -> (2,1) [East]
          else if (r === 6) dest = 10; // (2,1) -> (2,2) [South]
          else if (r === 10) dest = 9; // (2,2) -> (1,2) [West]
          else if (r === 9) dest = 5;  // (1,2) -> (1,1) [North]
          else {
            dest = (r + 1) % NUM_ROUTERS;
          }
        } else if (trafficWorkload === 'bit_complement') {
          dest = (~r) & (NUM_ROUTERS - 1);
        } else if (trafficWorkload === 'transpose') {
          dest = curX * GRID_SIZE + curY;
        } else {
          // Uniform Random
          dest = Math.floor(Math.random() * NUM_ROUTERS);
        }

        if (dest !== r) {
          const initVC = (routingPolicy === 'xy') ? 1 : 0;
          packets.push({
            id: nextPacketId++,
            src: r,
            dest: dest,
            curNode: r,
            curPort: 'L',
            vc: initVC,
            injectionCycle: currentCycle,
            waitCycles: 0,
            hopCount: 0,
            isBlocked: false,
            color: getPacketColor(dest)
          });
        }
      }
    }
  }

  function getPacketColor(dest) {
    const palette = ['#38bdf8', '#4ade80', '#fb923c', '#f43f5e', '#a855f7', '#facc15'];
    return palette[dest % palette.length];
  }

  function routeAndTraverse() {
    const remainingPackets = [];

    for (let p of packets) {
      if (p.curNode === p.dest) {
        // Delivered!
        deliveredFlits++;
        totalLatency += (currentCycle - p.injectionCycle);
        continue;
      }

      const curR = routers[p.curNode];
      const destR = routers[p.dest];
      const dx = destR.x - curR.x;
      const dy = destR.y - curR.y;

      let candidatePorts = [];

      if (p.vc === 1 || routingPolicy === 'xy') {
        // Strict Dimension-Order XY (Escape subnetwork)
        if (dx > 0) candidatePorts.push({ port: 'E', nextNode: p.curNode + 1 });
        else if (dx < 0) candidatePorts.push({ port: 'W', nextNode: p.curNode - 1 });
        else if (dy > 0) candidatePorts.push({ port: 'S', nextNode: p.curNode + GRID_SIZE });
        else if (dy < 0) candidatePorts.push({ port: 'N', nextNode: p.curNode - GRID_SIZE });
      } else {
        // Fully Adaptive (VC0): can move along X or Y minimal directions
        if (dx > 0) candidatePorts.push({ port: 'E', nextNode: p.curNode + 1 });
        if (dx < 0) candidatePorts.push({ port: 'W', nextNode: p.curNode - 1 });
        if (dy > 0) candidatePorts.push({ port: 'S', nextNode: p.curNode + GRID_SIZE });
        if (dy < 0) candidatePorts.push({ port: 'N', nextNode: p.curNode - GRID_SIZE });
      }

      // Check buffer availability on candidate downstream router
      let moved = false;
      for (let cand of candidatePorts) {
        const nextR = routers[cand.nextNode];
        const inPort = getOppositePort(cand.port);
        const targetQueue = (p.vc === 1) ? nextR.buffers[inPort].vc1 : nextR.buffers[inPort].vc0;

        if (targetQueue.length < BUFFER_CAPACITY) {
          // Channel is available! Move flit
          targetQueue.push(p.id);
          p.curNode = cand.nextNode;
          p.curPort = inPort;
          p.hopCount++;
          p.waitCycles = 0;
          p.isBlocked = false;
          moved = true;
          break;
        }
      }

      if (!moved) {
        p.waitCycles++;
        p.isBlocked = true;
        // In Duato mode: if blocked for >= 3 cycles, transition to Escape VC1!
        if (routingPolicy === 'duato' && p.vc === 0 && p.waitCycles >= 3) {
          p.vc = 1;
          escapeDrains++;
        }
      }

      remainingPackets.push(p);
    }

    packets = remainingPackets;
  }

  function getOppositePort(port) {
    if (port === 'E') return 'W';
    if (port === 'W') return 'E';
    if (port === 'N') return 'S';
    if (port === 'S') return 'N';
    return 'L';
  }

  // Tarjan's Strongly Connected Components / Elementary Cycle Finding on Active CDG
  function evaluateDeadlockCDG() {
    detectedCycles = [];
    const waitGraph = {}; // channelId -> list of nextChannelIds it is waiting for

    // Each active blocked packet establishes a dependency:
    // (Current Channel Held) -> (Target Channel Requested)
    for (let p of packets) {
      if (p.isBlocked) {
        const curChan = `${p.curNode}:${p.curPort}:vc${p.vc}`;
        const curR = routers[p.curNode];
        const destR = routers[p.dest];
        const dx = destR.x - curR.x;
        const dy = destR.y - curR.y;

        let reqNextNodes = [];
        if (p.vc === 1 || routingPolicy === 'xy') {
          if (dx > 0) reqNextNodes.push(p.curNode + 1);
          else if (dx < 0) reqNextNodes.push(p.curNode - 1);
          else if (dy > 0) reqNextNodes.push(p.curNode + GRID_SIZE);
          else if (dy < 0) reqNextNodes.push(p.curNode - GRID_SIZE);
        } else {
          if (dx > 0) reqNextNodes.push(p.curNode + 1);
          if (dx < 0) reqNextNodes.push(p.curNode - 1);
          if (dy > 0) reqNextNodes.push(p.curNode + GRID_SIZE);
          if (dy < 0) reqNextNodes.push(p.curNode - GRID_SIZE);
        }

        if (!waitGraph[curChan]) waitGraph[curChan] = [];
        for (let nxt of reqNextNodes) {
          waitGraph[curChan].push(`node:${nxt}`);
        }
      }
    }

    // Router-level cycle check for rapid visualization
    const routerWait = {};
    for (let p of packets) {
      if (p.isBlocked && p.waitCycles >= 3) {
        const cur = p.curNode;
        const curR = routers[cur];
        const destR = routers[p.dest];
        const dx = destR.x - curR.x;
        const dy = destR.y - curR.y;

        if (!routerWait[cur]) routerWait[cur] = [];
        if (p.vc === 1 || routingPolicy === 'xy') {
          if (dx > 0) routerWait[cur].push(cur + 1);
          else if (dx < 0) routerWait[cur].push(cur - 1);
          else if (dy > 0) routerWait[cur].push(cur + GRID_SIZE);
          else if (dy < 0) routerWait[cur].push(cur - GRID_SIZE);
        } else {
          if (dx > 0) routerWait[cur].push(cur + 1);
          if (dx < 0) routerWait[cur].push(cur - 1);
          if (dy > 0) routerWait[cur].push(cur + GRID_SIZE);
          if (dy < 0) routerWait[cur].push(cur - GRID_SIZE);
        }
      }
    }

    // Find elementary cycles via DFS
    const visited = new Set();
    const stack = [];
    const inStack = new Set();

    function dfs(u) {
      visited.add(u);
      stack.push(u);
      inStack.add(u);

      const neighbors = routerWait[u] || [];
      for (let v of neighbors) {
        if (!visited.has(v)) {
          dfs(v);
        } else if (inStack.has(v)) {
          // Cycle found!
          const cycleStart = stack.indexOf(v);
          const cycleNodes = stack.slice(cycleStart);
          if (cycleNodes.length >= 3) {
            detectedCycles.push(cycleNodes);
          }
        }
      }

      stack.pop();
      inStack.delete(u);
    }

    for (let r = 0; r < NUM_ROUTERS; r++) {
      if (!visited.has(r)) {
        dfs(r);
      }
    }

    // Mark deadlocked routers
    for (let r = 0; r < NUM_ROUTERS; r++) {
      routers[r].isDeadlocked = false;
    }
    for (let cyc of detectedCycles) {
      for (let nd of cyc) {
        routers[nd].isDeadlocked = true;
      }
    }
  }

  function updateHUD() {
    document.getElementById('hudSimCycle').textContent = currentCycle;
    document.getElementById('hudEscapeDrain').textContent = `${escapeDrains} flits`;
    const avgLat = deliveredFlits > 0 ? (totalLatency / deliveredFlits).toFixed(1) : '0.0';
    document.getElementById('hudAvgLatency').textContent = `${avgLat} cycles`;
    const tp = currentCycle > 0 ? (deliveredFlits / (currentCycle * NUM_ROUTERS)).toFixed(3) : '0.000';
    document.getElementById('hudThroughput').textContent = tp;

    const netStateEl = document.getElementById('hudNetState');
    const cdgCyclesEl = document.getElementById('hudCdgCycles');

    if (detectedCycles.length > 0) {
      netStateEl.textContent = 'DEADLOCKED (SCC Cycle)';
      netStateEl.style.color = '#ef4444';
      cdgCyclesEl.textContent = `${detectedCycles.length} Active Cycle(s)`;
      cdgCyclesEl.style.color = '#ef4444';

      const cycleStrs = detectedCycles.map(c => c.join(' ➔ ') + ` ➔ ${c[0]}`);
      document.getElementById('cdgCycleList').innerHTML = cycleStrs.map(s => `• Circular Wait: ${s}`).join('<br>');
    } else {
      netStateEl.textContent = 'NORMAL (Acyclic Flow)';
      netStateEl.style.color = '#22c55e';
      cdgCyclesEl.textContent = '0 Cycles';
      cdgCyclesEl.style.color = '#22c55e';
      document.getElementById('cdgCycleList').textContent = 'No active dependency cycles detected.';
    }

    // Buffer occupancies
    let vc0Occupied = 0, vc1Occupied = 0, totalSlots = NUM_ROUTERS * 5 * BUFFER_CAPACITY;
    for (let r of routers) {
      for (let p in r.buffers) {
        vc0Occupied += r.buffers[p].vc0.length;
        vc1Occupied += r.buffers[p].vc1.length;
      }
    }
    document.getElementById('vc0Util').textContent = `${((vc0Occupied / totalSlots) * 100).toFixed(1)}%`;
    document.getElementById('vc1Util').textContent = `${((vc1Occupied / totalSlots) * 100).toFixed(1)}%`;

    let maxQ = 0;
    for (let p of packets) {
      if (p.isBlocked) maxQ = Math.max(maxQ, p.waitCycles);
    }
    document.getElementById('maxQueueDepth').textContent = `${Math.min(BUFFER_CAPACITY, maxQ)} / ${BUFFER_CAPACITY} flits`;
  }

  function renderMesh() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Draw Links
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        const u = r * GRID_SIZE + c;
        const ru = routers[u];
        // Horizontal link East
        if (c + 1 < GRID_SIZE) {
          const rv = routers[u + 1];
          ctx.beginPath();
          ctx.moveTo(ru.screenX, ru.screenY);
          ctx.lineTo(rv.screenX, rv.screenY);
          ctx.strokeStyle = 'rgba(71, 85, 105, 0.45)';
          ctx.lineWidth = 2;
          ctx.stroke();
        }
        // Vertical link South
        if (r + 1 < GRID_SIZE) {
          const rv = routers[u + GRID_SIZE];
          ctx.beginPath();
          ctx.moveTo(ru.screenX, ru.screenY);
          ctx.lineTo(rv.screenX, rv.screenY);
          ctx.strokeStyle = 'rgba(71, 85, 105, 0.45)';
          ctx.lineWidth = 2;
          ctx.stroke();
        }
      }
    }

    // 2. Highlight Deadlock Cycles in pulsing red
    for (let cyc of detectedCycles) {
      ctx.beginPath();
      for (let i = 0; i < cyc.length; i++) {
        const r1 = routers[cyc[i]];
        const r2 = routers[cyc[(i + 1) % cyc.length]];
        ctx.moveTo(r1.screenX, r1.screenY);
        ctx.lineTo(r2.screenX, r2.screenY);
      }
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 4;
      ctx.stroke();
    }

    // 3. Draw Routers
    for (let r of routers) {
      ctx.beginPath();
      ctx.arc(r.screenX, r.screenY, 18, 0, Math.PI * 2);

      if (r.isDeadlocked) {
        ctx.fillStyle = '#dc2626'; // Red
      } else {
        ctx.fillStyle = '#1e293b';
      }
      ctx.fill();

      ctx.strokeStyle = r.isDeadlocked ? '#f87171' : '#38bdf8';
      ctx.lineWidth = r.isDeadlocked ? 3 : 1.5;
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = '10px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`R(${r.x},${r.y})`, r.screenX, r.screenY);
    }

    // 4. Draw Flits / Packets
    for (let p of packets) {
      const curR = routers[p.curNode];
      let offX = 0, offY = 0;
      if (p.curPort === 'N') offY = -12;
      else if (p.curPort === 'S') offY = 12;
      else if (p.curPort === 'E') offX = 12;
      else if (p.curPort === 'W') offX = -12;

      ctx.beginPath();
      ctx.arc(curR.screenX + offX, curR.screenY + offY, 5, 0, Math.PI * 2);
      ctx.fillStyle = (p.vc === 1) ? '#a855f7' : p.color; // VC1 escape is purple
      ctx.fill();

      if (p.isBlocked) {
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }
    }
  }

  // Formal SMT-LIB2 Deadlock-Freedom Assertion Export
  window.exportSmtFormula = function() {
    let smt = `; SMT-LIB2 CDG Acyclicity & Deadlock Freedom Verification\n`;
    smt += `; Architecture: 4x4 2D Mesh with Dual Virtual Channels (VC0=Adaptive, VC1=Escape XY)\n`;
    smt += `(set-logic QF_UF)\n`;
    smt += `(declare-sort Channel 0)\n`;
    smt += `(declare-fun depends (Channel Channel) Bool)\n`;
    smt += `(declare-fun rank (Channel) Int)\n\n`;
    smt += `; Property: CDG is acyclic iff a strict topological ranking function exists:\n`;
    smt += `; forall c1, c2: depends(c1, c2) => rank(c1) < rank(c2)\n\n`;
    smt += `; Assert escape channel transitions adhere to strict Dimension-Order XY ranking:\n`;
    for (let r = 0; r < NUM_ROUTERS; r++) {
      smt += `(assert (> (rank c_${r}_E_vc1) (rank c_${r}_W_vc1)))\n`;
      smt += `(assert (> (rank c_${r}_S_vc1) (rank c_${r}_E_vc1)))\n`;
    }
    smt += `\n(check-sat)\n(get-model)\n`;

    document.getElementById('deadlockExportTitle').textContent = 'SMT-LIB2 CDG Acyclicity Assertion';
    document.getElementById('deadlockExportCode').value = smt;
    document.getElementById('deadlockExportDrawer').style.display = 'block';
  };

  // Synthesizable Duato Escape VC Arbiter RTL Export
  window.exportDuatoVerilog = function() {
    let verilog = `// Synthesizable Duato Escape Virtual Channel Transition Arbiter\n`;
    verilog += `// Automatically promotes blocked VC0 flits to acyclic VC1 escape channel\n`;
    verilog += `\`timescale 1ns/1ps\n\n`;
    verilog += `module duato_escape_arbiter #(\n`;
    verilog += `    parameter DATA_WIDTH     = 32,\n`;
    verilog += `    parameter TIMEOUT_THRESH = 4\n`;
    verilog += `) (\n`;
    verilog += `    input  wire                  clk,\n`;
    verilog += `    input  wire                  rst_n,\n`;
    verilog += `    input  wire                  vc0_blocked,\n`;
    verilog += `    input  wire [DATA_WIDTH-1:0] vc0_data_in,\n`;
    verilog += `    output reg                   vc1_promote_req,\n`;
    verilog += `    output reg  [DATA_WIDTH-1:0] vc1_data_out\n`;
    verilog += `);\n\n`;
    verilog += `    reg [3:0] block_timer;\n\n`;
    verilog += `    always @(posedge clk or negedge rst_n) begin\n`;
    verilog += `        if (!rst_n) begin\n`;
    verilog += `            block_timer     <= 4'd0;\n`;
    verilog += `            vc1_promote_req <= 1'b0;\n`;
    verilog += `            vc1_data_out    <= {DATA_WIDTH{1'b0}};\n`;
    verilog += `        end else if (vc0_blocked) begin\n`;
    verilog += `            if (block_timer >= TIMEOUT_THRESH) begin\n`;
    verilog += `                vc1_promote_req <= 1'b1; // Trigger Duato escape drain\n`;
    verilog += `                vc1_data_out    <= vc0_data_in;\n`;
    verilog += `            end else begin\n`;
    verilog += `                block_timer     <= block_timer + 1'b1;\n`;
    verilog += `            end\n`;
    verilog += `        end else begin\n`;
    verilog += `            block_timer     <= 4'd0;\n`;
    verilog += `            vc1_promote_req <= 1'b0;\n`;
    verilog += `        end\n`;
    verilog += `    end\n\n`;
    verilog += `endmodule\n`;

    document.getElementById('deadlockExportTitle').textContent = 'Synthesizable Duato Escape Arbiter Verilog';
    document.getElementById('deadlockExportCode').value = verilog;
    document.getElementById('deadlockExportDrawer').style.display = 'block';
  };

  // Init
  initRouters();
  renderMesh();
})();
</script>
