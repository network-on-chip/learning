# 💳 Credit-Based Flow Control & Buffer Sizing Simulator

An interactive microarchitectural simulator for Network-on-Chip (NoC) credit-based backpressure and flow control. Model forward flit flight latency, downstream router buffer consumption, reverse credit turn-around delays, quantify minimum buffer depth requirements to sustain line-rate throughput without stall bubbles ($B_{\text{min}} = \lceil t_{\text{RTD}} \times \text{BW} \rceil$), and observe space-time timing ladder waveforms under traffic bursts.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Downstream Buffer Depth (B):</b>
      <input type="range" id="creditBufSlider" min="2" max="16" step="1" value="6" style="width:100px; vertical-align:middle;" oninput="document.getElementById('creditBufVal').textContent = this.value + ' flits'; updateCreditWorkbench();">
      <span id="creditBufVal" style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#38bdf8;">6 flits</span>
    </label>

    <label><b>Link Wire Flight Latency:</b>
      <select id="creditWireSelect" class="noc-sim-select" onchange="updateCreditWorkbench()">
        <option value="1">1 Cycle (Local On-Die Interconnect, L &lt; 2mm)</option>
        <option value="2" selected>2 Cycles (Semi-Global Cross-Die Link, L ≈ 5mm)</option>
        <option value="4">4 Cycles (2.5D Interposer / UCIe D2D Bridge)</option>
        <option value="6">6 Cycles (Long Multi-Chiplet Interconnect)</option>
      </select>
    </label>

    <label><b>Ingress Packet Burst Rate:</b>
      <select id="creditRateSelect" class="noc-sim-select" onchange="updateCreditWorkbench()">
        <option value="1.0" selected>1.0 flit/cyc (Full 100% Line-Rate Injection)</option>
        <option value="0.75">0.75 flits/cyc (Heavy Burst Traffic)</option>
        <option value="0.50">0.50 flits/cyc (Moderate Traffic)</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnCredLadder" onclick="switchCreditView('space_time')" style="background:#0284c7;">🪜 Space-Time Timing Ladder</button>
      <button class="noc-sim-btn secondary" id="btnCredCurve" onclick="switchCreditView('buffer_curve')">📈 Throughput vs. Buffer Depth</button>
      <button class="noc-sim-btn secondary" onclick="stepCreditClock()">⏭ Step Clock Cycle</button>
      <button class="noc-sim-btn secondary" onclick="resetCreditCAD()">🔄 Reset Buffer State</button>
      <button class="noc-sim-btn secondary" onclick="exportCreditReport()" style="margin-left:auto;">📋 Export Flow Report</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Minimum Sustained Buffer Depth</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudBmin">B_min = 6 flits</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudRtdCycles">Round-Trip Delay: 6 Cycles</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Effective Link Throughput</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudThroughput">100.0% Line Rate (1.00 flit/cyc)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudStarveStatus">No Credit Starvation Bubbles</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Upstream Credit Counter</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudCredits">Credits: 4 / 6 Available</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudDownstreamFifo">Downstream FIFO: 2 Flits Queued</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Buffer Area Overhead</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudAreaOverhead">384 Bits SRAM (48 Bytes)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudNangateArea">Area: 184 µm² (Nangate45 Cell)</div>
    </div>
  </div>

  <!-- Simulation Canvas -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="creditCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- Flow Report Modal / Panel -->
  <div id="creditReportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">Credit Flow Control Timing Audit Log:</strong>
      <button onclick="document.getElementById('creditReportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="creditReportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Credit-Based Flow Control Mathematics (Chapter 2 &amp; 3):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Credit Round-Trip Delay ($t_{\text{RTD}}$):</strong> The total latency between an upstream router transmitting a flit and receiving the corresponding credit release notification spans four discrete pipeline segments:
        $$t_{\text{RTD}} = t_{\text{wire, fwd}} + t_{\text{router, rx}} + t_{\text{consume}} + t_{\text{credit, rev}}$$
        For a link with $2\text{ cycles}$ forward flight, $1\text{ cycle}$ input buffer write, $1\text{ cycle}$ crossbar traversal, and $2\text{ cycles}$ reverse credit flight, $t_{\text{RTD}} = 6\text{ cycles}$.</li>
      <li><strong>Sustained Full-Throughput Buffer Depth ($B_{\text{min}}$):</strong> If the downstream buffer depth $B < B_{\text{min}}$, the upstream credit counter exhausts to zero before the first credit returns, forcing the transmitter to stall:
        $$B_{\text{min}} = \lceil t_{\text{RTD}} \times \text{Bandwidth} \rceil, \quad \text{Throughput} = \min\left(1.0, \frac{B}{B_{\text{min}}}\right)$$
        Sizing buffers below $B_{\text{min}}$ permanently throttles link utilization, while sizing buffers beyond $B_{\text{min}}$ consumes unnecessary silicon area without throughput benefit.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// Credit-Based Flow Control & Buffer Sizing Simulator Engine
// ============================================================================

(function () {
  let activeView = "space_time"; // "space_time", "buffer_curve"
  let currentCycle = 0;

  // Discrete-event queues for Space-Time Ladder
  // Forward link queue: [ { flitId, remainingCycles } ]
  let fwdWireQueue = [];
  // Reverse credit wire queue: [ { remainingCycles } ]
  let revWireQueue = [];

  let creditState = {
    bufferDepth: 6,
    wireLatency: 2,
    rtdCycles: 6,
    bMin: 6,
    upstreamCredits: 6,
    downstreamQueued: 0,
    deliveredFlits: 0,
    stalledCycles: 0,
    historyEvents: [] // for space-time diagram
  };

  const canvas = document.getElementById("creditCanvas");
  const ctx = canvas.getContext("2d");

  function computeCreditPhysics() {
    creditState.bufferDepth = parseInt(document.getElementById("creditBufSlider").value, 10) || 6;
    creditState.wireLatency = parseInt(document.getElementById("creditWireSelect").value, 10) || 2;

    // t_RTD = wire_fwd (L) + rx_write (1) + consume (1) + wire_rev (L)
    creditState.rtdCycles = 2 * creditState.wireLatency + 2;
    creditState.bMin = creditState.rtdCycles;

    let maxTp = Math.min(1.0, creditState.bufferDepth / creditState.bMin);
    let isStarving = creditState.bufferDepth < creditState.bMin;

    document.getElementById("hudBmin").textContent = "B_min = " + creditState.bMin + " flits";
    document.getElementById("hudRtdCycles").textContent = "Round-Trip Delay: " + creditState.rtdCycles + " Cycles";
    document.getElementById("hudThroughput").textContent = (maxTp * 100).toFixed(1) + "% Line Rate (" + maxTp.toFixed(2) + " flit/cyc)";
    document.getElementById("hudStarveStatus").textContent = isStarving ? "STARVATION BUBBLES: Buffer Undersized!" : "Full Line-Rate Sustained";
    document.getElementById("hudCredits").textContent = "Credits: " + creditState.upstreamCredits + " / " + creditState.bufferDepth;
    document.getElementById("hudDownstreamFifo").textContent = "Downstream FIFO: " + creditState.downstreamQueued + " Flits";
    document.getElementById("hudAreaOverhead").textContent = (creditState.bufferDepth * 64) + " Bits SRAM (" + (creditState.bufferDepth * 8) + " Bytes)";
    document.getElementById("hudNangateArea").textContent = "Area: " + (creditState.bufferDepth * 30.5).toFixed(1) + " µm² (Nangate45)";
  }

  function stepClockCycle() {
    currentCycle++;
    const injRate = parseFloat(document.getElementById("creditRateSelect").value) || 1.0;

    // 1. Upstream Injection
    let wantsInject = Math.random() < injRate;
    let injected = false;
    if (wantsInject) {
      if (creditState.upstreamCredits > 0) {
        creditState.upstreamCredits--;
        injected = true;
        fwdWireQueue.push({ id: currentCycle, remaining: creditState.wireLatency });
      } else {
        creditState.stalledCycles++;
      }
    }

    // 2. Advance Forward Link Wires
    for (let i = fwdWireQueue.length - 1; i >= 0; i--) {
      fwdWireQueue[i].remaining--;
      if (fwdWireQueue[i].remaining <= 0) {
        // Arrived at downstream router
        fwdWireQueue.splice(i, 1);
        creditState.downstreamQueued++;
      }
    }

    // 3. Downstream Router Consumes Flits & Generates Credit
    if (creditState.downstreamQueued > 0) {
      creditState.downstreamQueued--;
      creditState.deliveredFlits++;
      // Release credit back to upstream router
      revWireQueue.push({ remaining: creditState.wireLatency });
    }

    // 4. Advance Reverse Credit Wires
    for (let i = revWireQueue.length - 1; i >= 0; i--) {
      revWireQueue[i].remaining--;
      if (revWireQueue[i].remaining <= 0) {
        revWireQueue.splice(i, 1);
        creditState.upstreamCredits = Math.min(creditState.bufferDepth, creditState.upstreamCredits + 1);
      }
    }

    // Record space-time snapshot
    if (creditState.historyEvents.length > 20) creditState.historyEvents.shift();
    creditState.historyEvents.push({
      cyc: currentCycle,
      injected: injected,
      credits: creditState.upstreamCredits,
      downstream: creditState.downstreamQueued
    });

    computeCreditPhysics();
    render();
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "space_time") {
      renderSpaceTimeDiagram();
    } else if (activeView === "buffer_curve") {
      renderBufferThroughputCurve();
    }
  }

  // 1. Space-Time Timing Ladder View
  function renderSpaceTimeDiagram() {
    const w = canvas.width;
    const h = canvas.height;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("SPACE-TIME TIMING LADDER: FORWARD FLIT FLIGHT & REVERSE CREDIT RELEASE", 60, 30);

    const xUpstream = 140;
    const xDownstream = 560;
    const startY = 70;
    const endY = 380;

    // Upstream & Downstream Router Vertical Rails
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(xUpstream, startY);
    ctx.lineTo(xUpstream, endY);
    ctx.stroke();

    ctx.strokeStyle = "#10b981";
    ctx.beginPath();
    ctx.moveTo(xDownstream, startY);
    ctx.lineTo(xDownstream, endY);
    ctx.stroke();

    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 12px 'JetBrains Mono', monospace";
    ctx.textAlign = "center";
    ctx.fillText("Upstream Router (Tx)", xUpstream, startY - 15);

    ctx.fillStyle = "#10b981";
    ctx.fillText("Downstream Router (Rx)", xDownstream, startY - 15);

    // Draw In-Flight Forward Flits (Orange arrows)
    fwdWireQueue.forEach((f, idx) => {
      let progress = 1.0 - (f.remaining / creditState.wireLatency);
      let fx = xUpstream + progress * (xDownstream - xUpstream);
      let fy = startY + 60 + idx * 30;

      ctx.strokeStyle = "#f59e0b";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(xUpstream, fy - 15);
      ctx.lineTo(fx, fy);
      ctx.stroke();

      ctx.fillStyle = "#f59e0b";
      ctx.beginPath();
      ctx.arc(fx, fy, 5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#ffffff";
      ctx.font = "9px 'JetBrains Mono', monospace";
      ctx.fillText("FLIT", fx, fy - 8);
    });

    // Draw In-Flight Returning Credits (Green dashed arrows)
    revWireQueue.forEach((c, idx) => {
      let progress = 1.0 - (c.remaining / creditState.wireLatency);
      let cx = xDownstream - progress * (xDownstream - xUpstream);
      let cy = startY + 180 + idx * 30;

      ctx.strokeStyle = "#4ade80";
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 3]);
      ctx.beginPath();
      ctx.moveTo(xDownstream, cy - 15);
      ctx.lineTo(cx, cy);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = "#4ade80";
      ctx.beginPath();
      ctx.arc(cx, cy, 4, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#ffffff";
      ctx.font = "9px 'JetBrains Mono', monospace";
      ctx.fillText("+CREDIT", cx, cy + 14);
    });

    // Cycle & State Annotations
    ctx.fillStyle = "#94a3b8";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.textAlign = "left";
    ctx.fillText("Clock Cycle: " + currentCycle, 60, endY + 24);
    ctx.fillText("Forward Flight: " + creditState.wireLatency + " Cyc | Reverse Flight: " + creditState.wireLatency + " Cyc", 220, endY + 24);
  }

  // 2. Throughput vs Buffer Depth Curve View
  function renderBufferThroughputCurve() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("LINK THROUGHPUT vs. DOWNSTREAM FIFO BUFFER DEPTH [B_min KNEE]", padL, 28);

    // Axes
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 5; gy++) {
      let y = padT + (gy / 5) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let tpLabel = (1.0 - gy / 5).toFixed(1);
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(tpLabel, padL - 8, y + 4);
    }

    const maxB = 16;
    for (let gx = 0; gx <= 8; gx++) {
      let x = padL + (gx / 8) * graphW;
      ctx.beginPath();
      ctx.moveTo(x, padT);
      ctx.lineTo(x, h - padB);
      ctx.stroke();

      let bLabel = (gx * 2) + " flits";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(bLabel, x, h - padB + 16);
    }

    // Plot Saturation Curve
    ctx.strokeStyle = "#22c55e";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let b = 1; b <= maxB; b++) {
      let tp = Math.min(1.0, b / creditState.bMin);
      let px = padL + (b / maxB) * graphW;
      let py = padT + (1 - tp) * graphH;
      if (b === 1) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // Mark B_min Knee Point
    let kneeX = padL + (creditState.bMin / maxB) * graphW;
    ctx.strokeStyle = "#38bdf8";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(kneeX, padT);
    ctx.lineTo(kneeX, h - padB);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 11px 'JetBrains Mono', monospace";
    ctx.textAlign = "center";
    ctx.fillText("B_min = " + creditState.bMin + " flits (Knee Point)", kneeX, padT - 8);

    // Mark Current Selection
    let curX = padL + (creditState.bufferDepth / maxB) * graphW;
    let curTp = Math.min(1.0, creditState.bufferDepth / creditState.bMin);
    let curY = padT + (1 - curTp) * graphH;

    ctx.fillStyle = "#eab308";
    ctx.beginPath();
    ctx.arc(curX, curY, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillText("Current B = " + creditState.bufferDepth, curX, curY - 12);
  }

  // Window Dispatch Interface
  window.updateCreditWorkbench = function () {
    computeCreditPhysics();
    render();
  };

  window.switchCreditView = function (v) {
    activeView = v;
    document.getElementById("btnCredLadder").className = (v === "space_time") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnCredCurve").className = (v === "buffer_curve") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.stepCreditClock = function () {
    stepClockCycle();
  };

  window.resetCreditCAD = function () {
    fwdWireQueue = [];
    revWireQueue = [];
    currentCycle = 0;
    creditState.upstreamCredits = creditState.bufferDepth;
    creditState.downstreamQueued = 0;
    creditState.deliveredFlits = 0;
    creditState.stalledCycles = 0;
    creditState.historyEvents = [];
    computeCreditPhysics();
    render();
  };

  window.exportCreditReport = function () {
    let rpt = [
      "===============================================================================",
      "CREDIT-BASED FLOW CONTROL & BUFFER SIZING TIMING AUDIT",
      "===============================================================================",
      "Forward Wire Flight Time : " + creditState.wireLatency + " Clock Cycles",
      "Reverse Credit Wire Time : " + creditState.wireLatency + " Clock Cycles",
      "Total Round-Trip Delay   : " + creditState.rtdCycles + " Clock Cycles",
      "Minimum Buffer Threshold : " + creditState.bMin + " flits for 100% throughput",
      "Configured Buffer Depth  : " + creditState.bufferDepth + " flits",
      "Sustained Link Bandwidth : " + (Math.min(1.0, creditState.bufferDepth / creditState.bMin) * 100).toFixed(1) + "% Line Rate",
      "Total Delivered Flits    : " + creditState.deliveredFlits + " flits",
      "Total Stalled Bubbles    : " + creditState.stalledCycles + " cycles",
      "Buffer Memory Allocation : " + (creditState.bufferDepth * 64) + " bits per Virtual Channel",
      "==============================================================================="
    ];
    document.getElementById("creditReportText").textContent = rpt.join("\n");
    document.getElementById("creditReportWrap").style.display = "block";
  };

  // Initial Boot
  computeCreditPhysics();
  render();
})();
</script>
