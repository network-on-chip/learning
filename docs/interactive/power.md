# ⚡ Dark Silicon Physics & Power Gating CAD Workbench

An interactive Computer-Aided Design (CAD) workbench for nanoscale CMOS power dissipation and the Dark Silicon Utilization Wall. Quantify the breakdown of Dennard scaling, evaluate dynamic switching versus subthreshold and gate-tunneling leakage power across advanced technology nodes (45nm down to 2nm GAA), calculate permissible active silicon fractions under fixed Thermal Design Power (TDP) budgets, and optimize fine-grained sleep transistor sizing, inrush current peaks, and wake-up transient latencies.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Process Node:</b>
      <select id="pwrNodeSelect" class="noc-sim-select" onchange="updatePowerWorkbench()">
        <option value="45">45nm HKMG (Classical Scaling Transition, Vdd = 1.0V)</option>
        <option value="14">14nm FinFET (Sub-threshold Control, Vdd = 0.8V)</option>
        <option value="7">7nm EUV (Severe Leakage / Dark Silicon Onset, Vdd = 0.75V)</option>
        <option value="3" selected>3nm GAA MBCFET (82% Dark Silicon Limit, Vdd = 0.70V)</option>
        <option value="2">2nm GAA + Backside PDN (Extreme Power Density, Vdd = 0.65V)</option>
      </select>
    </label>

    <label><b>Thermal Design Power (TDP):</b>
      <input type="range" id="tdpSlider" min="60" max="300" step="10" value="150" style="width:110px; vertical-align:middle;" oninput="document.getElementById('tdpVal').textContent = this.value + ' W'; updatePowerWorkbench();">
      <span id="tdpVal" style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#f87171;">150 W</span>
    </label>

    <label><b>Sleep Transistor Sizing:</b>
      <select id="sleepSizeSelect" class="noc-sim-select" onchange="updatePowerWorkbench()">
        <option value="0.02">2% Area Overhead (High IR Drop, Fast Turn-On)</option>
        <option value="0.05" selected>5% Area Overhead (Balanced IR Drop &lt; 25mV)</option>
        <option value="0.10">10% Area Overhead (Ultra-Low IR Drop, High Inrush)</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnPwrFloor" onclick="switchPowerView('dark_floorplan')" style="background:#0284c7;">🧱 Dark Silicon Floorplan</button>
      <button class="noc-sim-btn secondary" id="btnPwrScaling" onclick="switchPowerView('scaling_curve')">📊 Dennard Scaling Breakdown</button>
      <button class="noc-sim-btn secondary" id="btnPwrWakeup" onclick="switchPowerView('wakeup_transient')">⚡ Sleep Wake-Up &amp; Inrush</button>
      <button class="noc-sim-btn secondary" onclick="optimizePowerGating()">🎯 Auto-Gate to TDP Budget</button>
      <button class="noc-sim-btn secondary" onclick="exportPowerReport()" style="margin-left:auto;">📋 Export Power Audit</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Active Silicon Utilization</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudUtilization">18.8% Active (12 / 64 Cores)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudDarkFraction">Dark Silicon: 81.2% (52 Cores Gated)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Total Dissipated Power</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudTotalPower">148.2 W / 150 W TDP</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudPowerBreakdown">Dynamic: 134.0W | Sub-Vth: 14.2W</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Sleep Transistor Penalty</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudIrDrop">IR Drop: 18.5 mV (2.6%)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudWakeupLat">Wake-Up Latency: 12 Cycles (Inrush: 4.8A)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Thermal Density Status</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudPowerDensity">1.18 W/mm² (Safe Limit)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudUngatedDensity">If Fully Active: 6.25 W/mm² (MELTDOWN)</div>
    </div>
  </div>

  <!-- CAD Canvas View -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="powerCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b; cursor:pointer;"></canvas>
  </div>

  <!-- Export Panel -->
  <div id="powerExportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">SoC Power Gating Architecture &amp; UPF / CPF Specification:</strong>
      <button onclick="document.getElementById('powerExportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="powerExportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Dark Silicon Physics &amp; Low-Power Architecture (Chapter 6):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Dennard Classical Scaling Breakdown:</strong> Historically, scaling physical dimensions by $\kappa > 1$ reduced voltage by $1/\kappa$, keeping power density constant ($P/A \approx 1$). Below 90nm, subthreshold slope constraints ($S \ge 60\text{ mV/decade}$ at $300\text{ K}$) prevented further $V_{dd}$ reductions without intolerable leakage:
        $$S = \left(\frac{d \log_{10} I_d}{d V_{gs}}\right)^{-1} = \frac{k_B T}{q} \ln(10) \left(1 + \frac{C_d}{C_{ox}}\right) \ge 60\text{ mV/dec}$$
        Consequently, power density surges as $\kappa^2$, forcing architects to power-gate large swaths of the die.</li>
      <li><strong>The Utilization Wall (Esmaeilzadeh et al., ISCA):</strong> Under a fixed cooling TDP budget, the maximum fraction $U$ of simultaneously active transistors drops quadratically:
        $$U(Node) = \frac{\text{TDP}}{N_{\text{cores}} \cdot (\alpha C V_{dd}^2 f + V_{dd} I_{\text{leak}})}$$
        In leading-edge 3nm and 2nm nodes, $U$ falls below $20\%$, meaning over $80\%$ of on-chip silicon must remain powered off at any instant.</li>
      <li><strong>Power Gating &amp; Inrush Transient:</strong> Header PMOS sleep transistors disconnect the $V_{dd}$ supply rail. Upon wakeup, charging the virtual rail capacitance $C_{virtual}$ creates a dangerous current surge:
        $$I_{\text{inrush}}(t) = C_{\text{virtual}} \frac{d V_{\text{virtual}}}{dt}$$
        Staged turn-on through daisy-chained sleep buffers is mandatory to avoid inductive $L \frac{di}{dt}$ supply noise that could corrupt adjacent retention flip-flops.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// Dark Silicon & CMOS Power Gating Optimization Engine
// ============================================================================

(function () {
  const GRID_SIZE = 8; // 64 Cores
  const TECH_DATA = {
    "45": { name: "45nm HKMG", Vdd: 1.0, fmaxGhz: 2.5, pDynPerCore: 1.8, pLeakPerCore: 0.15, areaMm2: 180 },
    "14": { name: "14nm FinFET", Vdd: 0.8, fmaxGhz: 3.4, pDynPerCore: 4.2, pLeakPerCore: 0.45, areaMm2: 120 },
    "7":  { name: "7nm EUV", Vdd: 0.75, fmaxGhz: 4.2, pDynPerCore: 7.8, pLeakPerCore: 1.20, areaMm2: 85 },
    "3":  { name: "3nm GAA", Vdd: 0.70, fmaxGhz: 5.0, pDynPerCore: 11.2, pLeakPerCore: 2.10, areaMm2: 60 },
    "2":  { name: "2nm BSPDN", Vdd: 0.65, fmaxGhz: 5.6, pDynPerCore: 14.5, pLeakPerCore: 3.40, areaMm2: 45 }
  };

  let activeView = "dark_floorplan"; // "dark_floorplan", "scaling_curve", "wakeup_transient"

  // Core power-gating state: true = ACTIVE, false = POWER-GATED (DARK)
  let coreActiveState = [];

  let pwrMetrics = {
    activeCount: 12,
    darkCount: 52,
    utilizationPct: 18.8,
    totDynW: 134.0,
    totLeakW: 14.2,
    totPowerW: 148.2,
    irDropMv: 18.5,
    wakeupCycles: 12,
    inrushPeakA: 4.8
  };

  const canvas = document.getElementById("powerCanvas");
  const ctx = canvas.getContext("2d");

  function initCores() {
    coreActiveState = [];
    for (let r = 0; r < GRID_SIZE; r++) {
      coreActiveState[r] = [];
      for (let c = 0; c < GRID_SIZE; c++) {
        // Default: 12 active cores in center, rest dark
        let isCenter = (r >= 2 && r <= 4 && c >= 2 && c <= 5);
        coreActiveState[r][c] = isCenter;
      }
    }
  }

  function computePowerPhysics() {
    const nodeKey = document.getElementById("pwrNodeSelect").value;
    const tech = TECH_DATA[nodeKey] || TECH_DATA["3"];
    const tdpBudget = parseFloat(document.getElementById("tdpSlider").value) || 150.0;
    const sleepSize = parseFloat(document.getElementById("sleepSizeSelect").value) || 0.05;

    let active = 0;
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        if (coreActiveState[r][c]) active++;
      }
    }

    const dark = 64 - active;
    pwrMetrics.activeCount = active;
    pwrMetrics.darkCount = dark;
    pwrMetrics.utilizationPct = (active / 64) * 100;

    // Active power = Dyn + Active Leakage
    // Dark core power = Gated leakage (suppressed by 98% via sleep transistor)
    const pDynTot = active * tech.pDynPerCore;
    const pActiveLeak = active * tech.pLeakPerCore;
    const pDarkLeak = dark * (tech.pLeakPerCore * 0.02); // 98% leakage reduction
    const pTot = pDynTot + pActiveLeak + pDarkLeak;

    pwrMetrics.totDynW = pDynTot;
    pwrMetrics.totLeakW = pActiveLeak + pDarkLeak;
    pwrMetrics.totPowerW = pTot;

    // Sleep Transistor Metrics
    // IR drop: V_ir = I_active * R_sleep
    // Larger sleep size => lower R_sleep, lower IR drop, but higher inrush
    const rSleepNorm = 0.04 / sleepSize;
    pwrMetrics.irDropMv = Math.round(rSleepNorm * tech.Vdd * 15.0);
    pwrMetrics.wakeupCycles = Math.round(6 + (0.10 / sleepSize) * 3);
    pwrMetrics.inrushPeakA = (sleepSize * 85.0).toFixed(1);

    // Update HUD
    document.getElementById("hudUtilization").textContent = pwrMetrics.utilizationPct.toFixed(1) + "% Active (" + active + " / 64 Cores)";
    document.getElementById("hudDarkFraction").textContent = "Dark Silicon: " + (100 - pwrMetrics.utilizationPct).toFixed(1) + "% (" + dark + " Cores Gated)";
    document.getElementById("hudTotalPower").textContent = pTot.toFixed(1) + " W / " + tdpBudget + " W TDP";
    document.getElementById("hudPowerBreakdown").textContent = "Dynamic: " + pDynTot.toFixed(1) + "W | Sub-Vth: " + (pActiveLeak + pDarkLeak).toFixed(1) + "W";
    document.getElementById("hudIrDrop").textContent = "IR Drop: " + pwrMetrics.irDropMv + " mV (" + ((pwrMetrics.irDropMv / (tech.Vdd * 1000)) * 100).toFixed(1) + "%)";
    document.getElementById("hudWakeupLat").textContent = "Wake-Up: " + pwrMetrics.wakeupCycles + " Cyc | Inrush: " + pwrMetrics.inrushPeakA + " A";

    let pwrDensity = (pTot / tech.areaMm2).toFixed(2);
    let ungatedPwr = (64 * (tech.pDynPerCore + tech.pLeakPerCore) / tech.areaMm2).toFixed(2);
    document.getElementById("hudPowerDensity").textContent = pwrDensity + " W/mm² (" + (pTot > tdpBudget ? "EXCEEDS TDP!" : "Within TDP") + ")";
    document.getElementById("hudUngatedDensity").textContent = "If Fully Active: " + ungatedPwr + " W/mm² (" + (ungatedPwr > 3.0 ? "THERMAL MELTDOWN" : "Hot") + ")";
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "dark_floorplan") {
      renderFloorplan();
    } else if (activeView === "scaling_curve") {
      renderScalingCurve();
    } else if (activeView === "wakeup_transient") {
      renderWakeupTransient();
    }
  }

  // 1. Dark Silicon 64-Core Floorplan
  function renderFloorplan() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, gridW = 340, gridH = 340;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("64-CORE SYSTEM-ON-CHIP DARK SILICON FLOORPLAN [CLICK TILES TO TOGGLE]", padL, 28);

    const cellW = gridW / GRID_SIZE;
    const cellH = gridH / GRID_SIZE;

    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        let x = padL + c * cellW;
        let y = padT + r * cellH;
        let isActive = coreActiveState[r][c];

        if (isActive) {
          // Powered Active Tile (Cyan / Amber)
          ctx.fillStyle = "#0284c7";
          ctx.strokeStyle = "#38bdf8";
          ctx.lineWidth = 1.5;
          ctx.fillRect(x + 2, y + 2, cellW - 4, cellH - 4);
          ctx.strokeRect(x + 2, y + 2, cellW - 4, cellH - 4);

          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 10px 'JetBrains Mono', monospace";
          ctx.textAlign = "center";
          ctx.fillText("ON", x + cellW / 2, y + cellH / 2 + 3);
        } else {
          // Gated Dark Tile (Dim Charcoal)
          ctx.fillStyle = "#0f172a";
          ctx.strokeStyle = "#1e293b";
          ctx.lineWidth = 1;
          ctx.fillRect(x + 2, y + 2, cellW - 4, cellH - 4);
          ctx.strokeRect(x + 2, y + 2, cellW - 4, cellH - 4);

          // Diagonal slash indicating power-gating
          ctx.strokeStyle = "rgba(100, 116, 139, 0.3)";
          ctx.beginPath();
          ctx.moveTo(x + 4, y + cellH - 4);
          ctx.lineTo(x + cellW - 4, y + 4);
          ctx.stroke();

          ctx.fillStyle = "#475569";
          ctx.font = "9px 'JetBrains Mono', monospace";
          ctx.textAlign = "center";
          ctx.fillText("DARK", x + cellW / 2, y + cellH / 2 + 3);
        }
      }
    }

    // Right-side Summary Panel
    const sumX = padL + gridW + 40;
    const sumY = padT;

    ctx.fillStyle = "#1e293b";
    ctx.strokeStyle = "#334155";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(sumX, sumY, 210, gridH, 8);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 11px 'JetBrains Mono', monospace";
    ctx.textAlign = "left";
    ctx.fillText("POWER BUDGET AUDIT", sumX + 16, sumY + 30);

    const tdp = parseFloat(document.getElementById("tdpSlider").value);
    const pTot = pwrMetrics.totPowerW;
    const isOver = pTot > tdp;

    ctx.fillStyle = isOver ? "#ef4444" : "#22c55e";
    ctx.font = "bold 14px 'JetBrains Mono', monospace";
    ctx.fillText(pTot.toFixed(1) + " W / " + tdp + " W", sumX + 16, sumY + 65);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "10px 'JetBrains Mono', monospace";
    ctx.fillText("Active Cores: " + pwrMetrics.activeCount, sumX + 16, sumY + 105);
    ctx.fillText("Dark Gated Cores: " + pwrMetrics.darkCount, sumX + 16, sumY + 125);
    ctx.fillText("Leakage Power: " + pwrMetrics.totLeakW.toFixed(1) + " W", sumX + 16, sumY + 145);
    ctx.fillText("Dynamic Power: " + pwrMetrics.totDynW.toFixed(1) + " W", sumX + 16, sumY + 165);

    // Progress Bar
    ctx.fillStyle = "#0f172a";
    ctx.fillRect(sumX + 16, sumY + 190, 178, 14);
    ctx.fillStyle = isOver ? "#ef4444" : "#22c55e";
    ctx.fillRect(sumX + 16, sumY + 190, Math.min(178, (pTot / tdp) * 178), 14);
  }

  // 2. Dennard Scaling Breakdown Curve
  function renderScalingCurve() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("DENNARD SCALING COLLAPSE: PERMISSIBLE ACTIVE SILICON FRACTION U(Node)", padL, 28);

    const nodes = [45, 28, 20, 14, 10, 7, 5, 3, 2];
    const uPct = [100, 88, 72, 48, 35, 24, 19, 14, 9];

    // Grid
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(Math.round(100 * (1 - gy / 4)) + "%", padL - 8, y + 4);
    }

    // Plot Curve
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    nodes.forEach((n, idx) => {
      let px = padL + (idx / (nodes.length - 1)) * graphW;
      let py = padT + (1 - uPct[idx] / 100) * graphH;
      if (idx === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);

      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(n + "nm", px, h - padB + 16);
    });
    ctx.stroke();

    // Fill Under Curve
    ctx.fillStyle = "rgba(239, 68, 68, 0.12)";
    ctx.lineTo(padL + graphW, padT + graphH);
    ctx.lineTo(padL, padT + graphH);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = "#f87171";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.textAlign = "left";
    ctx.fillText("Dark Silicon Region (>80% Transistors Inactive)", padL + graphW * 0.4, padT + graphH * 0.3);
  }

  // 3. Sleep Transistor Wake-Up Transient
  function renderWakeupTransient() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("POWER-GATING WAKE-UP TRANSIENT: VIRTUAL RAIL CHARGING & INRUSH CURRENT", padL, 28);

    // Waveforms: Voltage charging (0 to Vdd) and Inrush pulse (0 to Peak A)
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();
    }

    // Voltage Curve (Cyan)
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let t = 0; t <= 100; t++) {
      let v = (t < 15) ? 0 : (1 - Math.exp(-(t - 15) / 18.0));
      let px = padL + (t / 100) * graphW;
      let py = padT + (1 - v) * graphH;
      if (t === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // Inrush Current Spike (Yellow)
    ctx.strokeStyle = "#eab308";
    ctx.lineWidth = 2.0;
    ctx.beginPath();
    for (let t = 0; t <= 100; t++) {
      let iVal = (t < 15) ? 0 : Math.exp(-(t - 15) / 8.0) * Math.sin((t - 15) * 0.15);
      iVal = Math.max(0, iVal);
      let px = padL + (t / 100) * graphW;
      let py = padT + (1 - iVal * 0.85) * graphH;
      if (t === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // Legend
    ctx.textAlign = "left";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#38bdf8";
    ctx.fillRect(padL + 20, padT + 10, 14, 4);
    ctx.fillText("Virtual Vdd Rail [V(t)]", padL + 40, padT + 14);

    ctx.fillStyle = "#eab308";
    ctx.fillRect(padL + 20, padT + 28, 14, 4);
    ctx.fillText("Inrush Charging Current Surge [I(t)]", padL + 40, padT + 32);
  }

  // Interactive Tile Toggling
  canvas.addEventListener("click", function (e) {
    if (activeView !== "dark_floorplan") return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const mx = (e.clientX - rect.left) * scaleX;
    const my = (e.clientY - rect.top) * scaleY;

    const padL = 70, padT = 50, gridW = 340, gridH = 340;
    const cellW = gridW / GRID_SIZE;
    const cellH = gridH / GRID_SIZE;

    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        let x = padL + c * cellW;
        let y = padT + r * cellH;
        if (mx >= x && mx <= x + cellW && my >= y && my <= y + cellH) {
          coreActiveState[r][c] = !coreActiveState[r][c];
          computePowerPhysics();
          render();
          return;
        }
      }
    }
  });

  // Window Dispatch Interface
  window.updatePowerWorkbench = function () {
    computePowerPhysics();
    render();
  };

  window.switchPowerView = function (v) {
    activeView = v;
    document.getElementById("btnPwrFloor").className = (v === "dark_floorplan") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnPwrScaling").className = (v === "scaling_curve") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnPwrWakeup").className = (v === "wakeup_transient") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.optimizePowerGating = function () {
    const nodeKey = document.getElementById("pwrNodeSelect").value;
    const tech = TECH_DATA[nodeKey] || TECH_DATA["3"];
    const tdpBudget = parseFloat(document.getElementById("tdpSlider").value);

    // Max cores allowed without exceeding budget
    const maxActive = Math.floor(tdpBudget / (tech.pDynPerCore + tech.pLeakPerCore));

    let count = 0;
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        if (count < maxActive) {
          coreActiveState[r][c] = true;
          count++;
        } else {
          coreActiveState[r][c] = false;
        }
      }
    }
    computePowerPhysics();
    render();
  };

  window.exportPowerReport = function () {
    const nodeKey = document.getElementById("pwrNodeSelect").value;
    const tech = TECH_DATA[nodeKey];
    let rpt = [
      "===============================================================================",
      "DARK SILICON & POWER GATING COMPREHENSIVE CAD AUDIT REPORT",
      "===============================================================================",
      "Technology Process       : " + tech.name + " (Nominal Vdd = " + tech.Vdd + " V)",
      "Total Active Cores       : " + pwrMetrics.activeCount + " / 64 (" + pwrMetrics.utilizationPct.toFixed(1) + "% Active)",
      "Total Dark Silicon Cores : " + pwrMetrics.darkCount + " (" + (100 - pwrMetrics.utilizationPct).toFixed(1) + "% Power Gated)",
      "Total Chip Power         : " + pwrMetrics.totPowerW.toFixed(1) + " W (Budget: " + document.getElementById("tdpSlider").value + " W TDP)",
      "Dynamic Switching Power  : " + pwrMetrics.totDynW.toFixed(1) + " W",
      "Total Leakage Power      : " + pwrMetrics.totLeakW.toFixed(1) + " W (Sub-Vth + Gate Tunneling)",
      "-------------------------------------------------------------------------------",
      "POWER GATING MACRO-CELL IMPLEMENTATION METRICS",
      "-------------------------------------------------------------------------------",
      "Sleep Transistor Area    : " + (document.getElementById("sleepSizeSelect").value * 100) + "% Silicon Footprint",
      "Active Mode IR Drop      : " + pwrMetrics.irDropMv + " mV (" + ((pwrMetrics.irDropMv / (tech.Vdd * 1000)) * 100).toFixed(1) + "% Margin)",
      "Wake-Up Latency Penalty  : " + pwrMetrics.wakeupCycles + " Clock Cycles",
      "Peak Inrush Current      : " + pwrMetrics.inrushPeakA + " Amperes",
      "==============================================================================="
    ];
    document.getElementById("powerExportText").textContent = rpt.join("\n");
    document.getElementById("powerExportWrap").style.display = "block";
  };

  // Initial Boot
  initCores();
  computePowerPhysics();
  render();
})();
</script>
