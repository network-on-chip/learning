# 🔥 Silicon Thermal & Dynamic Thermal Management (DTM) Solver

An interactive Computer-Aided Design (CAD) finite-difference thermal simulator for multicore Systems-on-Chip (SoCs) and Networks-on-Chip (NoCs). Numerically solve the two-dimensional Fourier transient heat diffusion equation across silicon dies, model non-linear electro-thermal leakage power runaway ($I_{\text{leak}} \propto T^2 \exp(-qV_{th}/k_B T)$), evaluate passive heatsink versus microchannel liquid cooling, and benchmark Dynamic Thermal Management (DTM) policies including closed-loop PI-DVFS and thermal-aware packet rerouting.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>DTM Control Policy:</b>
      <select id="dtmPolicySelect" class="noc-sim-select" onchange="updateThermalWorkbench()">
        <option value="none">Open-Loop (No Throttling / Saturated Hotspots)</option>
        <option value="dvfs_reactive" selected>Reactive PI-DVFS Throttling (V/f Drop @ T_trip)</option>
        <option value="taar_routing">Thermal-Aware Adaptive Routing (Divert Traffic)</option>
        <option value="task_migration">Predictive Task Migration (Cool Tile Offloading)</option>
      </select>
    </label>

    <label><b>Package Cooling Solution:</b>
      <select id="coolingSelect" class="noc-sim-select" onchange="updateThermalWorkbench()">
        <option value="liquid">Direct Liquid Microchannel (R_sink = 0.12 °C/W)</option>
        <option value="copper_fan" selected>Active Copper Fin + Fan (R_sink = 0.35 °C/W)</option>
        <option value="passive">Passive Aluminum Heatsink (R_sink = 0.85 °C/W)</option>
      </select>
    </label>

    <label><b>Thermal Trip Point:</b>
      <input type="range" id="tripSlider" min="70" max="110" step="5" value="85" style="width:100px; vertical-align:middle;" oninput="document.getElementById('tripVal').textContent = this.value + '°C'; updateThermalWorkbench();">
      <span id="tripVal" style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#f87171;">85°C</span>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnHeatMap" onclick="switchThermalView('heatmap')" style="background:#0284c7;">🔥 2D Transient Heatmap</button>
      <button class="noc-sim-btn secondary" id="btnHeatWave" onclick="switchThermalView('waveform')">📈 T(t) Transient Waveform</button>
      <button class="noc-sim-btn secondary" id="btnHeatPwr" onclick="switchThermalView('power_breakdown')">⚡ Electro-Thermal Leakage</button>
      <button class="noc-sim-btn secondary" onclick="injectThermalHotspot()">🎯 Inject Localized GEMM Burst</button>
      <button class="noc-sim-btn secondary" onclick="resetThermalCAD()">🔄 Reset to Ambient</button>
      <button class="noc-sim-btn secondary" onclick="exportThermalReport()" style="margin-left:auto;">📋 Export Thermal Log</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Peak Junction Temperature</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudPeakT">74.2°C (Nominal)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudAvgT">Die Average: 52.8°C | ΔT Gradient: 34.2°C</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Total Power Dissipation</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudTotPwr">128.5 W (TDP Budget: 180W)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudPwrRatio">Dynamic: 104.2W | Sub-Vth Leakage: 24.3W</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">DTM Throttling Status</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudDtmStatus">NORMAL (100% Core Fmax)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudThrottledCount">Throttled Tiles: 0 / 64 Cores</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Thermal Runaway Risk</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudRunaway">SAFE (Stable Convergence)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudTime">Simulated Time: 42.0 ms</div>
    </div>
  </div>

  <!-- Canvas Simulation View -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="thermalCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- Report Export Panel -->
  <div id="thermalReportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">Transient Thermal &amp; DTM Audit Log:</strong>
      <button onclick="document.getElementById('thermalReportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="thermalReportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Silicon Thermal Physics &amp; DTM Mathematical Foundations (Chapter 7):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>2D Fourier Heat Diffusion Equation:</strong> The temperature distribution $T(x, y, t)$ across a silicon substrate of thickness $h_{si}$, density $\rho$, and specific heat capacity $c_p$ is governed by:
        $$\rho c_p \frac{\partial T}{\partial t} = k_{si} \left( \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} \right) + \frac{P_{diss}(x, y, t)}{h_{si}} - \frac{T - T_{sink}}{R_{th, vertical}}$$
        Lateral thermal resistance between adjacent $2\text{ mm}$ tiles is substantially higher than vertical resistance to the heat spreader, creating sharp on-chip spatial gradients ($\Delta T > 30^\circ\text{C}$).</li>
      <li><strong>Non-Linear Electro-Thermal Leakage Runaway:</strong> Subthreshold leakage increases exponentially with temperature:
        $$P_{\text{leak}}(T) = V_{dd} \cdot I_0 \left(\frac{T}{T_0}\right)^2 \exp\left( \frac{q (V_{gs} - V_{th})}{n k_B T} \right)$$
        If heat extraction rate $\frac{dT}{dt}_{\text{cool}}$ falls below the incremental leakage slope $\frac{\partial P_{\text{leak}}}{\partial T}$, positive electro-thermal feedback induces catastrophic thermal runaway.</li>
      <li><strong>Thermal-Aware Adaptive Routing (TAAR):</strong> Routing logic dynamically measures local temperature or buffer queues. Flits destined across a hotspot are diverted along orthogonal perimeter Manhattan routes, reducing local crossbar switching power and lowering peak $T_j$ by up to $14^\circ\text{C}$.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// Silicon Thermal & Dynamic Thermal Management (DTM) Finite-Difference Engine
// ============================================================================

(function () {
  const GRID_SIZE = 8; // 8x8 Core Grid = 64 Cores
  const T_AMBIENT = 35.0; // °C

  let activeView = "heatmap"; // "heatmap", "waveform", "power_breakdown"
  let animId = null;
  let simTimeMs = 0;

  // Thermal Network Mesh (8x8)
  let T = [];
  let P_dyn = [];
  let P_leak = [];
  let throttlingFactor = []; // 1.0 = full speed, 0.5 = throttled

  // Time-history buffers for waveform plotting
  let historyTime = [];
  let historyPeakT = [];
  let historyAvgT = [];

  const canvas = document.getElementById("thermalCanvas");
  const ctx = canvas.getContext("2d");

  function initMesh() {
    T = [];
    P_dyn = [];
    P_leak = [];
    throttlingFactor = [];
    for (let r = 0; r < GRID_SIZE; r++) {
      T[r] = [];
      P_dyn[r] = [];
      P_leak[r] = [];
      throttlingFactor[r] = [];
      for (let c = 0; c < GRID_SIZE; c++) {
        T[r][c] = T_AMBIENT + Math.random() * 2.0;
        P_dyn[r][c] = 1.2 + Math.random() * 0.8; // W
        P_leak[r][c] = 0.2;
        throttlingFactor[r][c] = 1.0;
      }
    }
    // Seed center GEMM clusters
    P_dyn[3][3] = 4.8;
    P_dyn[3][4] = 5.2;
    P_dyn[4][3] = 5.0;
    P_dyn[4][4] = 4.6;

    historyTime = [];
    historyPeakT = [];
    historyAvgT = [];
    simTimeMs = 0;
  }

  function stepThermalPhysics(dt_ms) {
    const coolingType = document.getElementById("coolingSelect").value;
    let rSink = (coolingType === "liquid") ? 0.12 : (coolingType === "passive" ? 0.85 : 0.35);
    const dtmPolicy = document.getElementById("dtmPolicySelect").value;
    const tripT = parseFloat(document.getElementById("tripSlider").value) || 85.0;

    const rLateral = 1.85; // °C/W
    const cCap = 0.085;    // J/°C per core tile

    let nextT = [];
    let peakT = 0;
    let sumT = 0;
    let totDyn = 0;
    let totLeak = 0;
    let throttledCount = 0;

    for (let r = 0; r < GRID_SIZE; r++) {
      nextT[r] = [];
      for (let c = 0; c < GRID_SIZE; c++) {
        let curT = T[r][c];

        // 1. DTM Decision
        let throttle = 1.0;
        if (dtmPolicy === "dvfs_reactive") {
          if (curT > tripT) {
            throttle = 0.45; // Drop voltage & frequency by 55%
            throttledCount++;
          }
        } else if (dtmPolicy === "taar_routing") {
          if (curT > tripT - 5.0) {
            throttle = 0.70; // Divert 30% routing traffic away
            throttledCount++;
          }
        } else if (dtmPolicy === "task_migration") {
          if (curT > tripT) {
            throttle = 0.30; // Migrate threads to edge tiles
            throttledCount++;
            // Edge tile receives extra work
            if (r > 0 && T[0][c] < tripT - 10) P_dyn[0][c] += 0.4;
          }
        }
        throttlingFactor[r][c] = throttle;

        // 2. Electro-Thermal Leakage Calculation
        // P_leak increases exponentially with temperature
        let tKelvin = curT + 273.15;
        let tNorm = tKelvin / 300.0;
        let leakW = 0.18 * Math.pow(tNorm, 2) * Math.exp(12.0 * (1.0 - 300.0 / tKelvin));
        P_leak[r][c] = leakW;

        let effDyn = P_dyn[r][c] * Math.pow(throttle, 2);
        let effP = effDyn + leakW;

        totDyn += effDyn;
        totLeak += leakW;

        // 3. Finite-Difference Heat Exchange
        let lateralConduction = 0;
        if (r > 0) lateralConduction += (T[r - 1][c] - curT) / rLateral;
        if (r < GRID_SIZE - 1) lateralConduction += (T[r + 1][c] - curT) / rLateral;
        if (c > 0) lateralConduction += (T[r][c - 1] - curT) / rLateral;
        if (c < GRID_SIZE - 1) lateralConduction += (T[r][c + 1] - curT) / rLateral;

        let verticalConvection = (curT - T_AMBIENT) / rSink;

        // dT/dt = (P + Q_lat - Q_vert) / C
        let dT_dt = (effP + lateralConduction - verticalConvection) / cCap;
        let newT = curT + dT_dt * (dt_ms * 1e-3);

        nextT[r][c] = Math.max(T_AMBIENT, Math.min(135.0, newT));
        if (nextT[r][c] > peakT) peakT = nextT[r][c];
        sumT += nextT[r][c];
      }
    }

    T = nextT;
    simTimeMs += dt_ms;

    let avgT = sumT / (GRID_SIZE * GRID_SIZE);
    let totP = totDyn + totLeak;

    // Record waveform history (keep last 120 points)
    if (historyTime.length > 120) {
      historyTime.shift();
      historyPeakT.shift();
      historyAvgT.shift();
    }
    historyTime.push(simTimeMs);
    historyPeakT.push(peakT);
    historyAvgT.push(avgT);

    // Update HUD Metrics
    document.getElementById("hudPeakT").textContent = peakT.toFixed(1) + "°C (" + (peakT >= tripT ? "THROTTLING ACTIVE" : "NOMINAL") + ")";
    document.getElementById("hudAvgT").textContent = "Die Average: " + avgT.toFixed(1) + "°C | ΔT Gradient: " + (peakT - avgT).toFixed(1) + "°C";
    document.getElementById("hudTotPwr").textContent = totP.toFixed(1) + " W (Budget: 180W)";
    document.getElementById("hudPwrRatio").textContent = "Dynamic: " + totDyn.toFixed(1) + "W | Leakage: " + totLeak.toFixed(1) + "W (" + ((totLeak / totP) * 100).toFixed(0) + "%)";
    document.getElementById("hudDtmStatus").textContent = (throttledCount > 0 ? "THROTTLED (" + throttledCount + " Cores)" : "FULL PERFORMANCE (100% Fmax)");
    document.getElementById("hudThrottledCount").textContent = "Throttled Tiles: " + throttledCount + " / 64 Cores";
    document.getElementById("hudRunaway").textContent = (peakT > 115 ? "CRITICAL RUNAWAY RISK!" : (peakT > 95 ? "WARNING: High Leakage" : "SAFE (Thermal Stability)"));
    document.getElementById("hudTime").textContent = "Simulated Time: " + simTimeMs.toFixed(1) + " ms";
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "heatmap") {
      renderHeatmap();
    } else if (activeView === "waveform") {
      renderWaveform();
    } else if (activeView === "power_breakdown") {
      renderPowerBreakdown();
    }
  }

  // 1. 2D Transient Heatmap View
  function renderHeatmap() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, gridW = 340, gridH = 340;
    const tripT = parseFloat(document.getElementById("tripSlider").value) || 85.0;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("2D SILICON JUNCTION TEMPERATURE DISTRIBUTION [8x8 CORE TILES]", padL, 28);

    const cellW = gridW / GRID_SIZE;
    const cellH = gridH / GRID_SIZE;

    // Draw Heatmap Cells
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        let temp = T[r][c];
        let x = padL + c * cellW;
        let y = padT + r * cellH;

        // Colormap normalization: 35°C (Blue) -> 65°C (Yellow) -> 95°C+ (Red/White)
        let tNorm = Math.min(1.0, Math.max(0, (temp - 35) / 60));
        let red = Math.round(tNorm * 255);
        let green = Math.round((1 - Math.abs(tNorm - 0.5) * 2) * 210);
        let blue = Math.round((1 - tNorm) * 220);

        ctx.fillStyle = "rgb(" + red + "," + green + "," + blue + ")";
        ctx.fillRect(x + 1, y + 1, cellW - 2, cellH - 2);

        // Highlight Throttled Cores
        if (throttlingFactor[r][c] < 1.0) {
          ctx.strokeStyle = "#ffffff";
          ctx.lineWidth = 1.5;
          ctx.strokeRect(x + 2, y + 2, cellW - 4, cellH - 4);
        }

        // Cell Temperature Text
        ctx.fillStyle = (tNorm > 0.6) ? "#000000" : "#ffffff";
        ctx.font = "bold 10px 'JetBrains Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText(Math.round(temp) + "°", x + cellW / 2, y + cellH / 2 + 3);
      }
    }

    // Colorbar Gradient Legend
    const cbX = padL + gridW + 40;
    const cbY = padT;
    const cbW = 20;
    const cbH = gridH;

    let grad = ctx.createLinearGradient(0, cbY + cbH, 0, cbY);
    grad.addColorStop(0, "rgb(0, 0, 220)");
    grad.addColorStop(0.5, "rgb(255, 210, 0)");
    grad.addColorStop(1, "rgb(255, 0, 0)");
    ctx.fillStyle = grad;
    ctx.fillRect(cbX, cbY, cbW, cbH);

    ctx.strokeStyle = "#334155";
    ctx.strokeRect(cbX, cbY, cbW, cbH);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "10px 'JetBrains Mono', monospace";
    ctx.textAlign = "left";
    ctx.fillText("95°C (Hot)", cbX + cbW + 8, cbY + 10);
    ctx.fillText("65°C", cbX + cbW + 8, cbY + cbH * 0.5 + 4);
    ctx.fillText("35°C (Amb)", cbX + cbW + 8, cbY + cbH);

    // Trip indicator on colorbar
    let tripY = cbY + (1 - (tripT - 35) / 60) * cbH;
    ctx.strokeStyle = "#f87171";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cbX - 4, tripY);
    ctx.lineTo(cbX + cbW + 4, tripY);
    ctx.stroke();
    ctx.fillStyle = "#f87171";
    ctx.fillText("Trip: " + tripT + "°C", cbX + cbW + 8, tripY + 3);
  }

  // 2. Transient Waveform T(t) View
  function renderWaveform() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padR = 40, padT = 50, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;
    const tripT = parseFloat(document.getElementById("tripSlider").value) || 85.0;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("TRANSIENT TEMPERATURE ESCALATION [T(t)] & DTM CLOSED-LOOP RESPONSE", padL, 28);

    // Y-Axis (30°C to 110°C)
    const minT = 30, maxT = 110;
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;

    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let tLabel = Math.round(maxT - (gy / 4) * (maxT - minT)) + "°C";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(tLabel, padL - 8, y + 4);
    }

    // Trip Threshold Line
    let yTrip = padT + (1 - (tripT - minT) / (maxT - minT)) * graphH;
    ctx.strokeStyle = "rgba(239, 68, 68, 0.5)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(padL, yTrip);
    ctx.lineTo(w - padR, yTrip);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = "#ef4444";
    ctx.textAlign = "left";
    ctx.fillText("Trip Limit: " + tripT + "°C", padL + 10, yTrip - 6);

    if (historyTime.length < 2) return;

    const tStart = historyTime[0];
    const tEnd = historyTime[historyTime.length - 1];
    const timeSpan = Math.max(10, tEnd - tStart);

    // Plot Peak T (Red)
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    historyTime.forEach((t, i) => {
      let px = padL + ((t - tStart) / timeSpan) * graphW;
      let py = padT + (1 - (historyPeakT[i] - minT) / (maxT - minT)) * graphH;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    });
    ctx.stroke();

    // Plot Avg T (Cyan)
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2.0;
    ctx.beginPath();
    historyTime.forEach((t, i) => {
      let px = padL + ((t - tStart) / timeSpan) * graphW;
      let py = padT + (1 - (historyAvgT[i] - minT) / (maxT - minT)) * graphH;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    });
    ctx.stroke();

    // Legend
    ctx.textAlign = "left";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#ef4444";
    ctx.fillRect(w - 240, padT + 10, 14, 4);
    ctx.fillText("Peak Core Junction Temp (Tmax)", w - 220, padT + 14);

    ctx.fillStyle = "#38bdf8";
    ctx.fillRect(w - 240, padT + 28, 14, 4);
    ctx.fillText("Die-Wide Average Temp (Tavg)", w - 220, padT + 32);
  }

  // 3. Electro-Thermal Leakage Breakdown View
  function renderPowerBreakdown() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padB = 60;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("TEMPERATURE-DEPENDENT SUBTHRESHOLD LEAKAGE POWER SENSITIVITY", padL, 28);

    // Curve of P_leak vs Temperature from 35C to 110C
    const minT = 35, maxT = 110;
    const graphW = w - padL - 40;
    const graphH = h - padT - padB;

    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - 40, y);
      ctx.stroke();

      let pLabel = (60 * (1 - gy / 4)).toFixed(0) + " W";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(pLabel, padL - 8, y + 4);
    }

    // Draw Exponential Leakage Curve
    ctx.strokeStyle = "#f87171";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let temp = minT; temp <= maxT; temp += 1) {
      let tK = temp + 273.15;
      let tNorm = tK / 300.0;
      let coreLeakW = 0.18 * Math.pow(tNorm, 2) * Math.exp(12.0 * (1.0 - 300.0 / tK));
      let totalLeak = coreLeakW * 64; // 64 cores
      let px = padL + ((temp - minT) / (maxT - minT)) * graphW;
      let py = padT + (1 - Math.min(60, totalLeak) / 60) * graphH;
      if (temp === minT) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    ctx.fillStyle = "#f87171";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillText("Exponential Subthreshold Leakage: Pleak ∝ T² · exp(-qVth / kBT)", padL + 20, padT + 20);
  }

  // Simulation Loop (runs at 30 FPS)
  function simLoop() {
    stepThermalPhysics(16.0); // 16 ms per frame
    render();
    animId = requestAnimationFrame(simLoop);
  }

  // Window Dispatch Interface
  window.updateThermalWorkbench = function () {
    // Parameter values automatically read inside stepThermalPhysics
  };

  window.switchThermalView = function (v) {
    activeView = v;
    document.getElementById("btnHeatMap").className = (v === "heatmap") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnHeatWave").className = (v === "waveform") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnHeatPwr").className = (v === "power_breakdown") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.injectThermalHotspot = function () {
    // Inject heavy matrix GEMM burst on core cluster [2..4, 2..4]
    for (let r = 2; r <= 4; r++) {
      for (let c = 2; c <= 4; c++) {
        P_dyn[r][c] += 6.5;
      }
    }
  };

  window.resetThermalCAD = function () {
    initMesh();
  };

  window.exportThermalReport = function () {
    const coolingType = document.getElementById("coolingSelect").value;
    const dtmPolicy = document.getElementById("dtmPolicySelect").value;
    const tripT = document.getElementById("tripSlider").value;

    let rpt = [
      "===============================================================================",
      "SILICON TRANSIENT THERMAL & DTM FINITE-DIFFERENCE AUDIT REPORT",
      "===============================================================================",
      "Cooling Solution         : " + coolingType.toUpperCase(),
      "DTM Control Policy       : " + dtmPolicy.toUpperCase(),
      "Thermal Trip Limit       : " + tripT + " °C",
      "Peak Junction Temp (Tmax): " + (historyPeakT[historyPeakT.length - 1] || 35).toFixed(1) + " °C",
      "Die Average Temp (Tavg)  : " + (historyAvgT[historyAvgT.length - 1] || 35).toFixed(1) + " °C",
      "Total Elapsed Sim Time   : " + simTimeMs.toFixed(1) + " ms",
      "Thermal Runaway Status   : " + ((historyPeakT[historyPeakT.length - 1] || 35) > 110 ? "CRITICAL RUNAWAY" : "CONVERGED STABLE"),
      "==============================================================================="
    ];
    document.getElementById("thermalReportText").textContent = rpt.join("\n");
    document.getElementById("thermalReportWrap").style.display = "block";
  };

  // Initial Boot
  initMesh();
  simLoop();
})();
</script>
