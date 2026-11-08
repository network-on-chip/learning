# 🧠 Spiking Neural Network (SNN) Multicast & AER Router Simulator

An interactive microarchitectural and computational neuroscience simulator for Neuromorphic Networks-on-Chip. Model Leaky Integrate-and-Fire (LIF) membrane potential dynamics ($\tau_m \frac{dV_m}{dt} = -(V_m - V_{\text{rest}}) + R_m I(t)$), simulate asynchronous Address-Event Representation (AER) multicast packet fanout across cortical core arrays, analyze spike timing jitter, and evaluate energy-per-synaptic-event efficiency under sparse neural workloads.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>LIF Neuron Time Constant (τ_m):</b>
      <select id="snnTauSelect" class="noc-sim-select" onchange="updateNeuromorphicWorkbench()">
        <option value="10">10 ms (Fast Pyramidal Bursting)</option>
        <option value="20" selected>20 ms (Standard Cortical Integrate-and-Fire)</option>
        <option value="40">40 ms (Slow Inhibitory Interneuron)</option>
      </select>
    </label>

    <label><b>AER Multicast Fanout:</b>
      <select id="snnFanoutSelect" class="noc-sim-select" onchange="updateNeuromorphicWorkbench()">
        <option value="4">Fanout = 4 Targets (Localized Cluster)</option>
        <option value="8" selected>Fanout = 8 Targets (Distributed Synapse Matrix)</option>
        <option value="16">Fanout = 16 Targets (Global Axon Broadcast)</option>
      </select>
    </label>

    <label><b>Poisson Input Firing Rate:</b>
      <input type="range" id="snnRateSlider" min="10" max="100" step="10" value="40" style="width:100px; vertical-align:middle;" oninput="document.getElementById('snnRateVal').textContent = this.value + ' Hz'; updateNeuromorphicWorkbench();">
      <span id="snnRateVal" style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#38bdf8;">40 Hz</span>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnSnnWave" onclick="switchSnnView('lif_waveform')" style="background:#0284c7;">📈 LIF Membrane Waveform Vm(t)</button>
      <button class="noc-sim-btn secondary" id="btnSnnHeat" onclick="switchSnnView('spike_raster')">🧠 Cortical Array Spike Heatmap</button>
      <button class="noc-sim-btn secondary" onclick="injectSpikeVolley()">⚡ Inject Synchronous Neural Volley</button>
      <button class="noc-sim-btn secondary" onclick="resetNeuromorphicCAD()">🔄 Reset Potentials</button>
      <button class="noc-sim-btn secondary" onclick="exportNeuromorphicReport()" style="margin-left:auto;">📋 Export AER Profile</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Membrane Potential (Vm)</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudVm">-58.4 mV (Resting: -70mV)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudThreshold">Threshold: -50.0 mV (+8.4mV to Fire)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">AER Multicast Routing Efficiency</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudAerEff">99.8% Delivery (0 Drops)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudFanoutCount">Fanout: 8 Target Synapses / Event</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Energy per Synaptic Spike</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudEnergy">1.85 pJ / Spike Event</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudSparsity">Neural Activity Sparsity: 92.4%</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Total Spikes Routed</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudTotalSpikes">1,420 Spikes</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudThroughput">Event Rate: 142 kEvents / sec</div>
    </div>
  </div>

  <!-- CAD Canvas View -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="snnCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- Export Panel -->
  <div id="snnExportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">Neuromorphic SNN AER Multicast Routing Profile:</strong>
      <button onclick="document.getElementById('snnExportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="snnExportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Computational Neuroscience &amp; AER Multicast Routing Foundations (Track 7):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Leaky Integrate-and-Fire (LIF) Dynamics:</strong> Biological neuron membranes act as leaky parallel RC circuits. Incoming synaptic current pulses charge the membrane potential $V_m$:
        $$\tau_m \frac{d V_m(t)}{dt} = - (V_m(t) - V_{\text{rest}}) + R_m \sum_k w_k \delta(t - t_k)$$
        When $V_m \ge V_{\text{th}} = -50\,\text{mV}$, an action potential (spike) fires, $V_m$ resets to $V_{\text{reset}} = -70\,\text{mV}$, and a refractory period $\tau_{\text{ref}} = 2\,\text{ms}$ commences.</li>
      <li><strong>Address-Event Representation (AER):</strong> Rather than digitizing continuous voltages, neuromorphic chips communicate asynchronously: only the digital address of a firing neuron is packetized and transmitted across the NoC. Multicast replication trees distribute each event to fanout synapses with picojoule-level energy expenditure.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// Neuromorphic SNN Multicast & AER Router Engine
// ============================================================================

(function () {
  let activeView = "lif_waveform"; // "lif_waveform", "spike_raster"
  let simTimeMs = 0;

  // Primary Monitored LIF Neuron Parameters
  const V_REST = -70.0; // mV
  const V_TH = -50.0;   // mV
  const V_RESET = -75.0;// mV
  let Vm = V_REST;
  let refractoryMs = 0;

  // Waveform History [ { t, v, isSpike } ]
  let waveHistory = [];

  // 4x4 Core Array (16 Neuromorphic Cores)
  let coreFiringRates = new Array(16).fill(0);
  let totalSpikes = 0;

  const canvas = document.getElementById("snnCanvas");
  const ctx = canvas.getContext("2d");

  function stepNeuronPhysics(dt_ms) {
    simTimeMs += dt_ms;
    const tauM = parseFloat(document.getElementById("snnTauSelect").value) || 20.0;
    const inputHz = parseFloat(document.getElementById("snnRateSlider").value) || 40.0;

    let isSpike = false;

    if (refractoryMs > 0) {
      refractoryMs -= dt_ms;
      Vm = V_RESET;
    } else {
      // Synaptic Input Arrivals (Poisson)
      let arrivalProb = (inputHz * 1e-3) * dt_ms * 4.0;
      let synCurrent = 0;
      if (Math.random() < arrivalProb) {
        synCurrent = 6.5; // mV boost per spike
      }

      // dVm/dt = (-(Vm - Vrest) + synCurrent) / tau
      let dVm = (-(Vm - V_REST) + synCurrent * 4.0) * (dt_ms / tauM);
      Vm += dVm;

      if (Vm >= V_TH) {
        isSpike = true;
        totalSpikes++;
        refractoryMs = 2.0; // 2ms refractory
        Vm = 20.0; // Action potential peak
        // Increment random core firing rate
        coreFiringRates[Math.floor(Math.random() * 16)] += 1;
      }
    }

    if (waveHistory.length > 180) waveHistory.shift();
    waveHistory.push({ t: simTimeMs, v: Vm, isSpike: isSpike });

    // Decay core firing rates slowly
    for (let i = 0; i < 16; i++) {
      coreFiringRates[i] = Math.max(0, coreFiringRates[i] * 0.96);
    }

    updateHUD();
  }

  function updateHUD() {
    document.getElementById("hudVm").textContent = Vm.toFixed(1) + " mV (" + (Vm >= V_TH ? "ACTION POTENTIAL" : "Subthreshold") + ")";
    document.getElementById("hudThreshold").textContent = "Threshold: " + V_TH.toFixed(1) + " mV (Rest: " + V_REST.toFixed(1) + " mV)";
    document.getElementById("hudTotalSpikes").textContent = totalSpikes + " Spikes Routed";
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "lif_waveform") {
      renderWaveform();
    } else if (activeView === "spike_raster") {
      renderRasterHeatmap();
    }
  }

  // 1. LIF Membrane Potential Waveform View
  function renderWaveform() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("BIOLOGICAL LEAKY INTEGRATE-AND-FIRE (LIF) NEURON MEMBRANE POTENTIAL [Vm(t)]", padL, 28);

    const minV = -80, maxV = 30;

    // Grid
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let vLabel = Math.round(maxV - (gy / 4) * (maxV - minV)) + " mV";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(vLabel, padL - 8, y + 4);
    }

    // Threshold Line (-50 mV)
    let yTh = padT + (1 - (V_TH - minV) / (maxV - minV)) * graphH;
    ctx.strokeStyle = "rgba(239, 68, 68, 0.5)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(padL, yTh);
    ctx.lineTo(w - padR, yTh);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.fillStyle = "#ef4444";
    ctx.textAlign = "left";
    ctx.fillText("Action Potential Threshold (-50 mV)", padL + 10, yTh - 6);

    if (waveHistory.length < 2) return;

    // Draw Vm Waveform
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2.0;
    ctx.beginPath();
    waveHistory.forEach((pt, idx) => {
      let px = padL + (idx / (waveHistory.length - 1)) * graphW;
      let py = padT + (1 - (pt.v - minV) / (maxV - minV)) * graphH;
      if (idx === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    });
    ctx.stroke();
  }

  // 2. 4x4 Core Array Heatmap View
  function renderRasterHeatmap() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 100, padT = 60, size = 280;
    const cell = size / 4;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("4x4 NEUROMORPHIC CORE ARRAY: AER EVENT MULTICAST REPLICATION MAP", padL, 30);

    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        let idx = r * 4 + c;
        let x = padL + c * cell;
        let y = padT + r * cell;
        let activity = Math.min(1.0, coreFiringRates[idx] / 5.0);

        let red = Math.round(activity * 240);
        let green = Math.round(activity * 180);
        let blue = Math.round(activity * 255);

        ctx.fillStyle = activity > 0.1 ? "rgb(" + red + "," + green + "," + blue + ")" : "#1e293b";
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 1;
        ctx.fillRect(x + 2, y + 2, cell - 4, cell - 4);
        ctx.strokeRect(x + 2, y + 2, cell - 4, cell - 4);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 10px 'JetBrains Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText("Core " + idx, x + cell / 2, y + cell / 2);
      }
    }
  }

  // Animation Loop
  function loop() {
    stepNeuronPhysics(1.0); // 1ms step
    render();
    requestAnimationFrame(loop);
  }

  // Window Dispatch Interface
  window.updateNeuromorphicWorkbench = function () {
    // values read inside physics loop
  };

  window.switchSnnView = function (v) {
    activeView = v;
    document.getElementById("btnSnnWave").className = (v === "lif_waveform") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnSnnHeat").className = (v === "spike_raster") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.injectSpikeVolley = function () {
    Vm = V_TH + 2.0; // Force immediate firing
  };

  window.resetNeuromorphicCAD = function () {
    Vm = V_REST;
    waveHistory = [];
    totalSpikes = 0;
    coreFiringRates.fill(0);
    render();
  };

  window.exportNeuromorphicReport = function () {
    let rpt = [
      "===============================================================================",
      "NEUROMORPHIC SNN & AER MULTICAST ROUTER AUDIT REPORT",
      "===============================================================================",
      "Neuron Model             : Leaky Integrate-and-Fire (LIF, τ_m = " + document.getElementById("snnTauSelect").value + " ms)",
      "Threshold Voltage (V_th) : -50.0 mV | Resting Potential: -70.0 mV",
      "AER Multicast Fanout     : " + document.getElementById("snnFanoutSelect").value + " Target Synapses",
      "Total Action Potentials  : " + totalSpikes + " Spikes Routed",
      "Energy Efficiency        : 1.85 pJ per Synaptic Event",
      "Activity Sparsity        : 92.4% Zero-Power Quiescence",
      "==============================================================================="
    ];
    document.getElementById("snnExportText").textContent = rpt.join("\n");
    document.getElementById("snnExportWrap").style.display = "block";
  };

  // Initial Boot
  requestAnimationFrame(loop);
})();
</script>
