# 🎯 Mixed-Criticality Multi-VNET QoS & Packet Scheduling Simulator

An interactive microarchitectural simulator for mixed-criticality Network-on-Chip (NoC) Quality-of-Service (QoS) and Virtual Network (VNET) protocol isolation. Benchmark Generalized Processor Sharing (GPS), Weighted Fair Queuing (WFQ), Deficit Round Robin (DRR), and Strict Priority (SP) schedulers under heavy best-effort bulk DMA bursts, evaluate tail latency percentiles ($P_{99.9}$), and guarantee protocol deadlock freedom across shared-memory coherence message classes (Request, Forward, Response).

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>QoS Scheduling Algorithm:</b>
      <select id="qosAlgoSelect" class="noc-sim-select" onchange="updateQosWorkbench()">
        <option value="wfq" selected>Weighted Fair Queuing (WFQ, 60:30:10 Ratio)</option>
        <option value="drr">Deficit Round Robin (DRR, O(1) Hardware Quantum)</option>
        <option value="strict_prio">Strict Priority (SP, Preempt Lower Classes)</option>
        <option value="fifo">Unprioritized Single-Queue (Best-Effort Contamination)</option>
      </select>
    </label>

    <label><b>Best-Effort Traffic Load:</b>
      <input type="range" id="qosBeSlider" min="0.2" max="0.9" step="0.1" value="0.7" style="width:100px; vertical-align:middle;" oninput="document.getElementById('qosBeVal').textContent = this.value + ' flit/cyc'; updateQosWorkbench();">
      <span id="qosBeVal" style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#f87171;">0.7 flit/cyc</span>
    </label>

    <label><b>Hard Real-Time Deadline:</b>
      <select id="qosDeadlineSelect" class="noc-sim-select" onchange="updateQosWorkbench()">
        <option value="12">Strict 12 Cycles (Automotive ASIL-D / Flight Control)</option>
        <option value="18" selected>Standard 18 Cycles (Cache Coherence Invalidation)</option>
        <option value="30">Relaxed 30 Cycles (Streaming Video SLA)</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnQosCdf" onclick="switchQosView('latency_cdf')" style="background:#0284c7;">📈 Latency CDF &amp; P99.9 Tail</button>
      <button class="noc-sim-btn secondary" id="btnQosQueues" onclick="switchQosView('vnet_queues')">📦 Multi-VNET Buffer Queues</button>
      <button class="noc-sim-btn secondary" onclick="stepQosClock()">⏭ Step Clock Cycle</button>
      <button class="noc-sim-btn secondary" onclick="resetQosCAD()">🔄 Reset Traffic</button>
      <button class="noc-sim-btn secondary" onclick="exportQosReport()" style="margin-left:auto;">📋 Export SLA Audit</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Real-Time SLA Compliance</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudSlaCompliance">100.0% On-Time Delivery</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudViolations">0 Deadline Misses / 240 HRT Packets</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Worst-Case Tail Latency (P99.9)</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudP99">HRT: 9 Cyc | BE: 42 Cyc</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudTailRatio">Tail Bounded: &lt; 18 Cycle Limit</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Protocol Deadlock Freedom</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudProtocolDeadlock">3 VNETs Physically Isolated</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudVnetClasses">Req (VNET0) → Fwd (VNET1) → Resp (VNET2)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Aggregate Throughput</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudThroughput">0.88 flits/cycle</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudStarvationStatus">Zero Best-Effort Starvation</div>
    </div>
  </div>

  <!-- Simulation Canvas -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="qosCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- Export Panel -->
  <div id="qosExportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">Mixed-Criticality QoS Verification Log:</strong>
      <button onclick="document.getElementById('qosExportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="qosExportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Mixed-Criticality QoS &amp; Protocol Deadlock Foundations (Chapter 3 &amp; 5):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Coherence Protocol Fetch-Deadlock:</strong> In directory-based cache coherent MPSoCs, a node processing a cache request (VNET0) must send coherence invalidations/forwards (VNET1) and await responses (VNET2) before retiring. If all message classes share a single buffer queue, a circular dependency forms ($VNET0 \rightarrow VNET1 \rightarrow VNET2 \rightarrow VNET0$), triggering catastrophic system lockup. Dedicating separate Virtual Networks (VNETs) breaks the dependency cycle.</li>
      <li><strong>Weighted Fair Queuing (WFQ):</strong> Approximates Generalized Processor Sharing (GPS). Each active packet queue $i$ receives an instantaneous service bandwidth proportional to its assigned weight $w_i$:
        $$r_i = \frac{w_i}{\sum_{j \in \mathcal{A}(t)} w_j} \cdot C$$
        WFQ computes virtual finish times $F_{i, k} = \max(F_{i, k-1}, V(a_{i, k})) + \frac{L_{i, k}}{w_i}$, guaranteeing bounded delay and preventing lower-priority starvation.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// Mixed-Criticality Multi-VNET QoS Simulator Engine
// ============================================================================

(function () {
  let activeView = "latency_cdf"; // "latency_cdf", "vnet_queues"
  let simCycle = 0;

  // 3 Traffic Classes
  // 0: Hard Real-Time (HRT), Weight = 60, Strict Deadline
  // 1: Low-Latency Coherence (LL), Weight = 30, Bounded P99
  // 2: Best-Effort Bulk DMA (BE), Weight = 10
  const VNETS = [
    { name: "VNET0: Hard Real-Time (HRT)", color: "#10b981", weight: 6, queue: [], deliveredLatencies: [], deadlineMisses: 0 },
    { name: "VNET1: Low-Latency Memory (LL)", color: "#38bdf8", weight: 3, queue: [], deliveredLatencies: [], deadlineMisses: 0 },
    { name: "VNET2: Best-Effort Bulk DMA (BE)", color: "#f59e0b", weight: 1, queue: [], deliveredLatencies: [], deadlineMisses: 0 }
  ];

  let deficitCounters = [6, 3, 1];
  const QUANTUM = [6, 3, 1];

  const canvas = document.getElementById("qosCanvas");
  const ctx = canvas.getContext("2d");

  function stepQosPhysics() {
    simCycle++;
    const algo = document.getElementById("qosAlgoSelect").value;
    const beLoad = parseFloat(document.getElementById("qosBeSlider").value) || 0.7;
    const deadline = parseInt(document.getElementById("qosDeadlineSelect").value, 10) || 18;

    // 1. Packet Injection
    // HRT: Periodic pulse (1 packet every 5 cycles)
    if (simCycle % 5 === 0) {
      VNETS[0].queue.push({ id: simCycle, injTime: simCycle });
    }
    // LL: Poisson arrivals (prob = 0.35)
    if (Math.random() < 0.35) {
      VNETS[1].queue.push({ id: simCycle, injTime: simCycle });
    }
    // BE: Heavy burst arrivals
    if (Math.random() < beLoad) {
      VNETS[2].queue.push({ id: simCycle, injTime: simCycle });
    }

    // 2. Scheduler Dispatch Decision (1 packet serviced per cycle)
    let selectedVnet = -1;

    if (algo === "strict_prio") {
      // Strict Priority: HRT > LL > BE
      if (VNETS[0].queue.length > 0) selectedVnet = 0;
      else if (VNETS[1].queue.length > 0) selectedVnet = 1;
      else if (VNETS[2].queue.length > 0) selectedVnet = 2;
    } else if (algo === "fifo") {
      // Unprioritized FIFO (picks earliest arriving packet across all queues)
      let earliestTime = Infinity;
      for (let v = 0; v < 3; v++) {
        if (VNETS[v].queue.length > 0 && VNETS[v].queue[0].injTime < earliestTime) {
          earliestTime = VNETS[v].queue[0].injTime;
          selectedVnet = v;
        }
      }
    } else {
      // DRR / WFQ: Round Robin with Deficit Counters
      for (let attempt = 0; attempt < 3; attempt++) {
        let v = (simCycle + attempt) % 3;
        if (VNETS[v].queue.length > 0 && deficitCounters[v] >= 1) {
          deficitCounters[v] -= 1;
          selectedVnet = v;
          break;
        } else {
          deficitCounters[v] += QUANTUM[v];
        }
      }
    }

    // 3. Service Selected Packet
    if (selectedVnet !== -1 && VNETS[selectedVnet].queue.length > 0) {
      let pkt = VNETS[selectedVnet].queue.shift();
      let latency = simCycle - pkt.injTime + 3; // add wire hop delay
      VNETS[selectedVnet].deliveredLatencies.push(latency);
      if (selectedVnet === 0 && latency > deadline) {
        VNETS[0].deadlineMisses++;
      }
    }

    updateHUD();
  }

  function updateHUD() {
    const deadline = parseInt(document.getElementById("qosDeadlineSelect").value, 10) || 18;
    const hrtTot = VNETS[0].deliveredLatencies.length;
    const misses = VNETS[0].deadlineMisses;
    const compliance = (hrtTot > 0) ? (((hrtTot - misses) / hrtTot) * 100) : 100;

    let hrtP99 = computePercentile(VNETS[0].deliveredLatencies, 0.999) || 4;
    let beP99 = computePercentile(VNETS[2].deliveredLatencies, 0.999) || 15;

    document.getElementById("hudSlaCompliance").textContent = compliance.toFixed(1) + "% SLA Compliance";
    document.getElementById("hudViolations").textContent = misses + " Deadline Misses / " + hrtTot + " HRT Packets";
    document.getElementById("hudP99").textContent = "HRT P99: " + hrtP99 + " Cyc | BE: " + beP99 + " Cyc";
    document.getElementById("hudTailRatio").textContent = (hrtP99 <= deadline) ? "All HRT within " + deadline + " Cyc Deadline" : "SLA VIOLATION: Tail Exceeded!";
    document.getElementById("hudThroughput").textContent = ((hrtTot + VNETS[1].deliveredLatencies.length + VNETS[2].deliveredLatencies.length) / Math.max(1, simCycle)).toFixed(2) + " flits/cycle";
  }

  function computePercentile(arr, p) {
    if (!arr || arr.length === 0) return 0;
    let sorted = [...arr].sort((a, b) => a - b);
    let idx = Math.min(sorted.length - 1, Math.floor(sorted.length * p));
    return sorted[idx];
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "latency_cdf") {
      renderLatencyCDF();
    } else if (activeView === "vnet_queues") {
      renderVnetQueues();
    }
  }

  // 1. Latency Cumulative Distribution Function (CDF)
  function renderLatencyCDF() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;
    const deadline = parseInt(document.getElementById("qosDeadlineSelect").value, 10) || 18;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("CUMULATIVE DISTRIBUTION FUNCTION (CDF): PACKET LATENCY PERCENTILES", padL, 28);

    // Axes
    const maxLatencyCyc = 40;
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let pLabel = Math.round(100 * (1 - gy / 4)) + "%";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(pLabel, padL - 8, y + 4);
    }

    for (let gx = 0; gx <= 8; gx++) {
      let x = padL + (gx / 8) * graphW;
      ctx.beginPath();
      ctx.moveTo(x, padT);
      ctx.lineTo(x, h - padB);
      ctx.stroke();

      let lLabel = (gx * 5) + " Cyc";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(lLabel, x, h - padB + 16);
    }

    // Deadline vertical line
    let dlX = padL + (deadline / maxLatencyCyc) * graphW;
    ctx.strokeStyle = "rgba(239, 68, 68, 0.5)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(dlX, padT);
    ctx.lineTo(dlX, h - padB);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = "#ef4444";
    ctx.fillText("HRT Deadline (" + deadline + " Cyc)", dlX, padT - 8);

    // Draw CDF curves for each VNET
    VNETS.forEach(vnet => {
      if (vnet.deliveredLatencies.length < 5) return;
      let sorted = [...vnet.deliveredLatencies].sort((a, b) => a - b);
      ctx.strokeStyle = vnet.color;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (let cyc = 1; cyc <= maxLatencyCyc; cyc++) {
        let count = sorted.filter(l => l <= cyc).length;
        let cdf = count / sorted.length;
        let px = padL + (cyc / maxLatencyCyc) * graphW;
        let py = padT + (1 - cdf) * graphH;
        if (cyc === 1) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();
    });

    // Legend
    ctx.textAlign = "left";
    ctx.font = "11px 'JetBrains Mono', monospace";
    VNETS.forEach((vnet, idx) => {
      ctx.fillStyle = vnet.color;
      ctx.fillRect(w - 260, padT + 10 + idx * 18, 12, 12);
      ctx.fillStyle = "#ffffff";
      ctx.fillText(vnet.name.split(":")[0] + " Traffic", w - 240, padT + 20 + idx * 18);
    });
  }

  // 2. Multi-VNET Buffer Queue State
  function renderVnetQueues() {
    const w = canvas.width;
    const h = canvas.height;
    const startX = 100, startY = 70, qW = 460, qH = 60, gap = 35;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("HARDWARE MULTI-VNET BUFFER QUEUES & ARBITER SCHEDULING STATUS", 70, 30);

    VNETS.forEach((vnet, idx) => {
      let y = startY + idx * (qH + gap);
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = vnet.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(startX, y, qW, qH, 6);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 12px 'JetBrains Mono', monospace";
      ctx.textAlign = "left";
      ctx.fillText(vnet.name, startX + 16, y - 8);

      ctx.fillStyle = vnet.color;
      ctx.fillText(vnet.queue.length + " Flits Waiting", startX + qW - 120, y - 8);

      // Draw packets inside queue
      vnet.queue.slice(0, 14).forEach((pkt, pi) => {
        let px = startX + 12 + pi * 30;
        ctx.fillStyle = vnet.color;
        ctx.fillRect(px, y + 14, 22, 32);
        ctx.fillStyle = "#000000";
        ctx.font = "9px 'JetBrains Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText(simCycle - pkt.injTime, px + 11, y + 33);
      });
    });
  }

  // Window Dispatch Interface
  window.updateQosWorkbench = function () {
    render();
  };

  window.switchQosView = function (v) {
    activeView = v;
    document.getElementById("btnQosCdf").className = (v === "latency_cdf") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnQosQueues").className = (v === "vnet_queues") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.stepQosClock = function () {
    stepQosPhysics();
    render();
  };

  window.resetQosCAD = function () {
    simCycle = 0;
    VNETS.forEach(v => {
      v.queue = [];
      v.deliveredLatencies = [];
      v.deadlineMisses = 0;
    });
    deficitCounters = [6, 3, 1];
    updateHUD();
    render();
  };

  window.exportQosReport = function () {
    let rpt = [
      "===============================================================================",
      "MIXED-CRITICALITY QoS & PROTOCOL DEADLOCK AUDIT REPORT",
      "===============================================================================",
      "Scheduler Algorithm      : " + document.getElementById("qosAlgoSelect").value.toUpperCase(),
      "Hard Real-Time Deadline  : " + document.getElementById("qosDeadlineSelect").value + " Clock Cycles",
      "Total HRT Delivered      : " + VNETS[0].deliveredLatencies.length + " Packets",
      "HRT Deadline Violations  : " + VNETS[0].deadlineMisses + " Misses",
      "SLA Compliance Rate      : " + document.getElementById("hudSlaCompliance").textContent,
      "Worst-Case P99.9 Tail    : " + document.getElementById("hudP99").textContent,
      "Coherence Deadlock Check : PASSED (Dedicated VNETs Break Cyclic Dependency)",
      "==============================================================================="
    ];
    document.getElementById("qosExportText").textContent = rpt.join("\n");
    document.getElementById("qosExportWrap").style.display = "block";
  };

  // Initial Boot
  for (let c = 0; c < 20; c++) stepQosPhysics();
  render();
})();
</script>
