# ⚡ Distributed LLM Collective Accelerator & 3D Memory Simulator

An interactive Computer-Aided Design (CAD) and microarchitectural simulator for distributed Large Language Model (LLM) collective communication and 3D memory acceleration. Benchmark Ring AllReduce, Hierarchical Tree Reduction, and Mixture-of-Experts (MoE) All-to-All token dispatch across 16-chiplet heterogeneous active interposers, quantify pipeline bubble overhead ($F_{\text{bubble}} = \frac{PP - 1}{m + PP - 1}$), and evaluate Roofline arithmetic intensity limits against 16 TB/s vertical HBM3e stacks.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Target LLM Workload:</b>
      <select id="llmModelSelect" class="noc-sim-select" onchange="updateTransformerWorkbench()">
        <option value="llama_70b" selected>LLaMA-3 70B (TP=8, Hidden Dim: 8192, 405 TFLOPs)</option>
        <option value="gpt4_moe">GPT-4 Class 1.8T MoE (8x All-to-All Experts, 160B Active)</option>
        <option value="llama_8b">LLaMA-3 8B (Low-Latency Edge AI Inference)</option>
      </select>
    </label>

    <label><b>Distributed Collective:</b>
      <select id="llmCollectiveSelect" class="noc-sim-select" onchange="updateTransformerWorkbench()">
        <option value="ring_allreduce" selected>Ring AllReduce (Scatter-Reduce + All-Gather)</option>
        <option value="tree_reduce">Hierarchical In-Network Tree Reduction</option>
        <option value="moe_alltoall">MoE All-to-All Expert Token Dispatch</option>
      </select>
    </label>

    <label><b>Interconnect Bandwidth:</b>
      <select id="llmBwSelect" class="noc-sim-select" onchange="updateTransformerWorkbench()">
        <option value="400">400 GB/s (Standard 2.5D Interposer)</option>
        <option value="900" selected>900 GB/s (Advanced UCIe 2.0 Active Interposer)</option>
        <option value="1800">1.8 TB/s (3D Hybrid Direct Cu-Cu Stacking)</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnLlmRing" onclick="switchLlmView('ring_flow')" style="background:#0284c7;">⭕ 16-Chiplet Ring Collective Flow</button>
      <button class="noc-sim-btn secondary" id="btnLlmRoof" onclick="switchLlmView('roofline')">📊 Roofline Model (Compute vs. Interconnect)</button>
      <button class="noc-sim-btn secondary" onclick="stepCollectiveCycle()">⏭ Step Collective Cycle</button>
      <button class="noc-sim-btn secondary" onclick="resetTransformerCAD()">🔄 Reset Collective</button>
      <button class="noc-sim-btn secondary" onclick="exportTransformerReport()" style="margin-left:auto;">📋 Export Acceleration Log</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Collective Duration</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudCollectiveTime">14.8 µs per Step</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudTransferVolume">Volume: 128 MB (2x (P-1)/P * M)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Roofline Operating Point</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudRoofline">342 TFLOPs (84.4% MFU)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudBoundStatus">Compute Bound (Arithmetic Intensity: 142 FLOP/B)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Pipeline Bubble Fraction</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudBubble">F_bubble: 6.2% (1F1B Schedule)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudPipelinedStages">PP = 4 Stages | m = 32 Microbatches</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Vertical HBM3e Bandwidth</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudHbmBw">14.4 TB/s Delivered</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudDramEfficiency">90.0% of 16.0 TB/s Peak Stack</div>
    </div>
  </div>

  <!-- CAD Canvas View -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="transformerCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- Export Panel -->
  <div id="llmExportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">Distributed LLM Accelerator &amp; Collective Communication Audit:</strong>
      <button onclick="document.getElementById('llmExportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="llmExportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Distributed AI Collective Communication &amp; Memory Physics (Chapter 12):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Ring AllReduce Complexity:</strong> For $P$ accelerator chiplets reducing a tensor of $M$ bytes, Ring AllReduce operates in two consecutive stages (Scatter-Reduce followed by All-Gather). Total transmitted data across all links is optimal and independent of $P$:
        $$T_{\text{Ring}} = 2 \left( \frac{P - 1}{P} \right) \frac{M}{B_{\text{link}}} + 2(P - 1) \alpha$$
        As $P \rightarrow 16$, bandwidth utilization reaches $\approx 93.8\%$, completely eliminating the hot-potato bottleneck of centralized parameter servers.</li>
      <li><strong>Roofline Model &amp; Memory Walls:</strong> An AI accelerator is bounded by either peak compute $P_{\text{peak}}$ or memory bandwidth $B_{\text{mem}}$:
        $$\text{Attainable Performance} = \min\left( P_{\text{peak}}, \; I_{\text{arith}} \times B_{\text{mem}} \right)$$
        In-network reduction units offload gradient aggregations from GPU cores, keeping the tensor core array fed at $>80\%$ Model Flops Utilization (MFU).</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// Distributed LLM Accelerator & Collective Engine
// ============================================================================

(function () {
  let activeView = "ring_flow"; // "ring_flow", "roofline"
  let collectiveStep = 0;

  // 16 Chiplets arranged in ring around interposer
  const NUM_CHIPLETS = 16;
  let ringPhase = 0; // 0: Scatter-Reduce, 1: All-Gather

  let llmMetrics = {
    collectiveTimeUs: 14.8,
    volumeMb: 128,
    mfuPct: 84.4,
    tflops: 342,
    bubblePct: 6.2,
    hbmBwTbps: 14.4
  };

  const canvas = document.getElementById("transformerCanvas");
  const ctx = canvas.getContext("2d");

  function computeTransformerPhysics() {
    const model = document.getElementById("llmModelSelect").value;
    const collective = document.getElementById("llmCollectiveSelect").value;
    const linkBwGbps = parseFloat(document.getElementById("llmBwSelect").value) || 900;

    let tensorMb = (model === "llama_70b") ? 128 : (model === "gpt4_moe" ? 384 : 16);
    llmMetrics.volumeMb = tensorMb;

    // Ring AllReduce transfer time: 2 * (P-1)/P * M / BW
    const P = 16;
    const transferBytes = 2 * ((P - 1) / P) * (tensorMb * 1e6);
    const linkBwBytesPerSec = linkBwGbps * 1e9;
    const timeUs = (transferBytes / linkBwBytesPerSec) * 1e6 + (2 * P * 0.15); // include latency

    llmMetrics.collectiveTimeUs = timeUs.toFixed(1);

    if (model === "llama_70b") {
      llmMetrics.tflops = Math.round(405 * (linkBwGbps / 1100));
      llmMetrics.mfuPct = Math.min(88.5, (llmMetrics.tflops / 405) * 100).toFixed(1);
    } else if (model === "gpt4_moe") {
      llmMetrics.tflops = Math.round(750 * (linkBwGbps / 1200));
      llmMetrics.mfuPct = Math.min(82.0, (llmMetrics.tflops / 900) * 100).toFixed(1);
    } else {
      llmMetrics.tflops = 120;
      llmMetrics.mfuPct = 92.0;
    }

    document.getElementById("hudCollectiveTime").textContent = llmMetrics.collectiveTimeUs + " µs per Step";
    document.getElementById("hudTransferVolume").textContent = "Volume: " + tensorMb + " MB (2x (P-1)/P * M)";
    document.getElementById("hudRoofline").textContent = llmMetrics.tflops + " TFLOPs (" + llmMetrics.mfuPct + "% MFU)";
    document.getElementById("hudHbmBw").textContent = (linkBwGbps * 0.016).toFixed(1) + " TB/s Delivered";
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "ring_flow") {
      renderRingFlow();
    } else if (activeView === "roofline") {
      renderRoofline();
    }
  }

  // 1. 16-Chiplet Ring Flow View
  function renderRingFlow() {
    const w = canvas.width;
    const h = canvas.height;
    const cx = 350, cy = 215, rRing = 145;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("16-CHIPLET HETEROGENEOUS ACTIVE INTERPOSER RING ALLREDUCE COLLECTIVE FLOW", 60, 26);

    // Draw Interposer Ring Backbone
    ctx.strokeStyle = "rgba(56, 189, 248, 0.4)";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(cx, cy, rRing, 0, Math.PI * 2);
    ctx.stroke();

    // Draw 16 Accelerator Chiplets in a Ring
    for (let i = 0; i < NUM_CHIPLETS; i++) {
      let angle = (i / NUM_CHIPLETS) * Math.PI * 2 - Math.PI / 2;
      let px = cx + Math.cos(angle) * rRing;
      let py = cy + Math.sin(angle) * rRing;

      // Chiplet Die
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(px, py, 14, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 9px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText("C" + i, px, py + 3);

      // Draw Token Flow Sprites moving clockwise
      let tokenAngle = angle + (collectiveStep * 0.15);
      let tx = cx + Math.cos(tokenAngle) * rRing;
      let ty = cy + Math.sin(tokenAngle) * rRing;

      ctx.fillStyle = "#eab308";
      ctx.beginPath();
      ctx.arc(tx, ty, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    // Center Hub: HBM3e Memory Controller
    ctx.fillStyle = "#0c4a6e";
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, 42, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 11px 'JetBrains Mono', monospace";
    ctx.textAlign = "center";
    ctx.fillText("HBM3e Stack", cx, cy - 6);
    ctx.font = "9px 'JetBrains Mono', monospace";
    ctx.fillText("16.0 TB/s", cx, cy + 10);
  }

  // 2. Roofline Model View
  function renderRoofline() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("ROOFLINE ARITHMETIC INTENSITY MODEL: PEAK TFLOPs vs. FLOP/BYTE", padL, 28);

    // Axes
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let tLabel = Math.round(500 * (1 - gy / 4)) + " TF";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(tLabel, padL - 8, y + 4);
    }

    // Roofline Slanted Knee Curve
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    // Memory-bound slant
    ctx.moveTo(padL, padT + graphH);
    ctx.lineTo(padL + graphW * 0.45, padT + graphH * 0.2);
    // Compute-bound plateau
    ctx.lineTo(padL + graphW, padT + graphH * 0.2);
    ctx.stroke();

    // Mark Operating Point
    let opX = padL + graphW * 0.65;
    let opY = padT + graphH * 0.2;
    ctx.fillStyle = "#22c55e";
    ctx.beginPath();
    ctx.arc(opX, opY, 6, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#22c55e";
    ctx.font = "bold 10px 'JetBrains Mono', monospace";
    ctx.textAlign = "left";
    ctx.fillText("LLaMA-70B (342 TFLOPs, 84.4% MFU)", opX + 12, opY - 6);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "10px 'JetBrains Mono', monospace";
    ctx.fillText("Memory-Bound Region", padL + 30, padT + graphH * 0.7);
    ctx.fillText("Compute-Bound Plateau (Roof: 405 TF)", padL + graphW * 0.6, padT + graphH * 0.12);
  }

  // Window Dispatch Interface
  window.updateTransformerWorkbench = function () {
    computeTransformerPhysics();
    render();
  };

  window.switchLlmView = function (v) {
    activeView = v;
    document.getElementById("btnLlmRing").className = (v === "ring_flow") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnLlmRoof").className = (v === "roofline") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.stepCollectiveCycle = function () {
    collectiveStep++;
    render();
  };

  window.resetTransformerCAD = function () {
    collectiveStep = 0;
    computeTransformerPhysics();
    render();
  };

  window.exportTransformerReport = function () {
    let rpt = [
      "===============================================================================",
      "DISTRIBUTED LLM ACCELERATOR & COLLECTIVE COMMUNICATION AUDIT",
      "===============================================================================",
      "Target Architecture      : " + document.getElementById("llmModelSelect").value.toUpperCase(),
      "Collective Algorithm     : " + document.getElementById("llmCollectiveSelect").value.toUpperCase(),
      "Active Interposer BW     : " + document.getElementById("llmBwSelect").value + " GB/s",
      "Per-Step Reduction Time  : " + llmMetrics.collectiveTimeUs + " µs",
      "Attained Compute Rate    : " + llmMetrics.tflops + " TFLOPs (" + llmMetrics.mfuPct + "% MFU)",
      "Pipeline Bubble Overhead : " + llmMetrics.bubblePct + "% (1F1B Schedule)",
      "Vertical HBM3e Feed Rate : " + llmMetrics.hbmBwTbps + " TB/s Delivered",
      "==============================================================================="
    ];
    document.getElementById("llmExportText").textContent = rpt.join("\n");
    document.getElementById("llmExportWrap").style.display = "block";
  };

  // Initial Boot
  computeTransformerPhysics();
  render();
})();
</script>
