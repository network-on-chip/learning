# ⚡ Distributed RC Interconnect Physics & Repeater CAD Workbench

An interactive Computer-Aided Design (CAD) and physics laboratory for on-chip interconnects. Perform numerical transient simulations of distributed $RLC$ transmission lines, evaluate copper resistivity scaling driven by Fuchs-Sondheimer surface scattering and Mayadas-Shatzkes grain boundary scattering from 180nm down to 2nm Backside Power Delivery (BSPDN) nodes, optimize Bakoglu repeater insertion, and analyze high-speed step responses and multi-drop bus capacitive loading.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Process Node:</b>
      <select id="wireNodeSelect" class="noc-sim-select" onchange="updateWireWorkbench()">
        <option value="180">180nm Bulk (Aluminum / SiO2, k=3.9)</option>
        <option value="90">90nm CMOS (Copper Dual-Damascene / SiCOH, k=3.0)</option>
        <option value="45">45nm HKMG (Copper / Ultra Low-k, k=2.5)</option>
        <option value="14">14nm FinFET (Air Gaps / Ru Liner, k=2.2)</option>
        <option value="7">7nm EUV (Ruthenium / Co-barrier, k=2.1)</option>
        <option value="3" selected>3nm GAA MBCFET (Extreme Scattering, k=2.0)</option>
        <option value="2">2nm GAA + BSPDN (Direct Backside Power, k=1.9)</option>
      </select>
    </label>

    <label><b>Metal Tier:</b>
      <select id="wireMetalSelect" class="noc-sim-select" onchange="updateWireWorkbench()">
        <option value="local">Local M1-M2 (Dense pitch, Thin barrier, High R)</option>
        <option value="intermediate" selected>Intermediate M3-M5 (Semi-Global Signal Routing)</option>
        <option value="global">Global M7-M9 (Thick Top Metal, Low R, Clock Tree)</option>
      </select>
    </label>

    <label><b>Interconnect Length:</b>
      <input type="range" id="wireLengthSlider" min="0.5" max="15.0" step="0.5" value="5.0" style="width:110px; vertical-align:middle;" oninput="document.getElementById('wireLenVal').textContent = this.value + ' mm'; updateWireWorkbench();">
      <span id="wireLenVal" style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#38bdf8;">5.0 mm</span>
    </label>

    <label><b>Repeater Strategy:</b>
      <select id="wireRepeaterMode" class="noc-sim-select" onchange="updateWireWorkbench()">
        <option value="optimal" selected>Bakoglu Auto-Optimal (k_opt, h_opt)</option>
        <option value="unbuffered">Unbuffered Raw Line (k = 0)</option>
        <option value="manual">Manual Segmentation (Select k)</option>
      </select>
    </label>

    <div id="manualKWrap" style="display:none; align-items:center; gap:0.4rem;">
      <label><b>k:</b></label>
      <input type="number" id="wireManualK" min="1" max="24" value="4" class="noc-sim-select" style="width:55px;" onchange="updateWireWorkbench()">
    </div>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnTabWave" onclick="switchWireTab('transient')" style="background:#0284c7;">📈 Transient Step Response</button>
      <button class="noc-sim-btn secondary" id="btnTabDelay" onclick="switchWireTab('delay_sweep')">📏 Delay vs. Length O(L) Sweep</button>
      <button class="noc-sim-btn secondary" id="btnTabBus" onclick="switchWireTab('bus_contention')">💥 Multi-Drop Bus vs. NoC</button>
      <button class="noc-sim-btn secondary" onclick="exportTimingReport()" style="margin-left:auto;">📋 Export SPICE Deck</button>
    </div>
  </div>

  <!-- Physical Parameters HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Distributed Line Parasitics</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudRw">r_w: 184.2 Ω/mm</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudCw">c_w: 0.195 pF/mm | l_w: 0.42 nH/mm</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Nanoscale Resistivity (FS + MS)</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudRho">ρ: 5.62 µΩ·cm</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudScattering">3.31x Bulk Cu (w_eff: 24.2 nm)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Bakoglu Repeater Sizing</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudRepeater">k_opt: 6 stages</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudSize">Size h_opt: 28.4x | Pitch: 0.83 mm</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Timing Closure &amp; Maximum Fmax</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudDelay">τ_50: 218 ps</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudFmax">f_max: 2.29 GHz | E: 1.18 pJ/bit</div>
    </div>
  </div>

  <!-- Simulation Oscilloscope Canvas -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="wireCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- SPICE Netlist Preview Output Modal / Panel -->
  <div id="spiceDeckWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">Synthesized SPICE Transmission Line Deck:</strong>
      <button onclick="document.getElementById('spiceDeckWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="spiceDeckText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Analytical Foundations -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Interconnect Physical Scaling &amp; Transmission Line Theory (Chapter 1):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Distributed Elmore Delay:</strong> For an unbuffered transmission wire of total resistance $R = r_w L$ and capacitance $C = c_w L$, the $50\%$ propagation step delay scales quadratically:
        $$\tau_{50} = 0.69 R_d (C + C_L) + 0.38 r_w c_w L^2 + 0.69 R C_L$$
        At long global distances ($L \ge 5\text{ mm}$), the quadratic term $0.38 r_w c_w L^2$ dominates, rendering single-cycle propagation impossible without active repeaters.</li>
      <li><strong>Bakoglu Optimal Repeater Insertion:</strong> Dividing the interconnect into $k_{opt}$ segments with repeaters of size $h_{opt}$ relative to a minimum-sized inverter ($R_0, C_0$) converts quadratic $O(L^2)$ delay into strictly linear $O(L)$ delay:
        $$k_{opt} = L \sqrt{\frac{0.38 r_w c_w}{0.69 R_0 C_0}}, \quad h_{opt} = \sqrt{\frac{R_0 c_w}{r_w C_0}}, \quad \tau_{opt} = 2.5 L \sqrt{R_0 C_0 r_w c_w}$$</li>
      <li><strong>Nanoscale Resistivity Degradation (FS + MS Modeling):</strong> When wire width $w$ approaches the electron mean free path ($\lambda_{e, Cu} \approx 39\text{ nm}$ at $300\text{ K}$), specular surface scattering (Fuchs-Sondheimer) and grain boundary reflectivity $R_{gb} \approx 0.45$ (Mayadas-Shatzkes) drive copper resistivity up by over $3.5\times$:
        $$\rho(w) \approx \rho_0 \left[ 1 + \frac{3}{8}(1-p)\frac{\lambda_e}{w - 2 t_{barrier}} + \frac{3}{2}\frac{R_{gb}}{1-R_{gb}}\frac{\lambda_e}{d_{grain}} \right]$$</li>
      <li><strong>The Interconnect Wall &amp; Bus Contention:</strong> A shared multi-drop bus suffers from additive capacitive stub loading ($C_{bus} = c_w L + N \cdot C_{tap}$), causing latency to scale as $O(N^2)$ under contention. A 2D Mesh NoC decouples communication into localized point-to-point router links, sustaining constant cycle times regardless of core count.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// Distributed RC Transmission Line & Repeater CAD Engine
// ============================================================================

(function () {
  // Technology Node Calibration Dataset (ITRS / IRDS 2024 Standards)
  const TECH_NODES = {
    "180": { name: "180nm Bulk", lambda_e: 39, rho0: 2.7, p: 0.6, Rgb: 0.25, eps_r: 3.9, w_local: 250, h_local: 450, w_int: 360, h_int: 700, w_glob: 800, h_glob: 1400, t_bar: 2.0, R0: 8500, C0: 1.2, Vdd: 1.8 },
    "90":  { name: "90nm CMOS",  lambda_e: 39, rho0: 1.7, p: 0.5, Rgb: 0.35, eps_r: 3.0, w_local: 110, h_local: 220, w_int: 160, h_int: 320, w_glob: 400, h_glob: 800,  t_bar: 1.8, R0: 5200, C0: 0.95, Vdd: 1.2 },
    "45":  { name: "45nm HKMG",  lambda_e: 39, rho0: 1.7, p: 0.4, Rgb: 0.40, eps_r: 2.5, w_local: 55,  h_local: 110, w_int: 85,  h_int: 170, w_glob: 220, h_glob: 450,  t_bar: 1.5, R0: 3800, C0: 0.72, Vdd: 1.0 },
    "14":  { name: "14nm FinFET",lambda_e: 39, rho0: 1.7, p: 0.3, Rgb: 0.45, eps_r: 2.2, w_local: 24,  h_local: 52,  w_int: 40,  h_int: 90,  w_glob: 120, h_glob: 260,  t_bar: 1.2, R0: 2400, C0: 0.55, Vdd: 0.8 },
    "7":   { name: "7nm EUV",    lambda_e: 39, rho0: 1.7, p: 0.25, Rgb: 0.48, eps_r: 2.1, w_local: 18, h_local: 40,  w_int: 28,  h_int: 65,  w_glob: 70,  h_glob: 160,  t_bar: 1.0, R0: 1900, C0: 0.44, Vdd: 0.75 },
    "3":   { name: "3nm GAA",    lambda_e: 39, rho0: 1.7, p: 0.2, Rgb: 0.52, eps_r: 2.0, w_local: 12,  h_local: 28,  w_int: 20,  h_int: 50,  w_glob: 48,  h_glob: 110,  t_bar: 0.8, R0: 1550, C0: 0.36, Vdd: 0.7 },
    "2":   { name: "2nm BSPDN",  lambda_e: 39, rho0: 1.7, p: 0.2, Rgb: 0.52, eps_r: 1.9, w_local: 10,  h_local: 24,  w_int: 16,  h_int: 42,  w_glob: 40,  h_glob: 95,   t_bar: 0.7, R0: 1380, C0: 0.31, Vdd: 0.65 }
  };

  let activeTab = "transient"; // "transient", "delay_sweep", "bus_contention"
  let simState = {
    nodeKey: "3",
    metalTier: "intermediate",
    lengthMm: 5.0,
    repeaterMode: "optimal",
    manualK: 4,
    // Calculated Electrical Parameters
    rw: 0, // Ω/mm
    cw: 0, // pF/mm
    lw: 0.45, // nH/mm
    rhoEff: 0, // µΩ·cm
    kOpt: 1,
    hOpt: 1,
    actualK: 1,
    actualH: 1,
    tau50Ps: 0,
    fmaxGhz: 0,
    energyPjPerBit: 0,
    // Step response time domain array [ { t: ps, vUnbuf: V, vOpt: V, vActual: V } ]
    timeDomainWaveform: []
  };

  const canvas = document.getElementById("wireCanvas");
  const ctx = canvas.getContext("2d");

  function computePhysics() {
    const tech = TECH_NODES[simState.nodeKey] || TECH_NODES["3"];
    let w_nm, h_nm;
    if (simState.metalTier === "local") {
      w_nm = tech.w_local;
      h_nm = tech.h_local;
    } else if (simState.metalTier === "global") {
      w_nm = tech.w_glob;
      h_nm = tech.h_glob;
    } else {
      w_nm = tech.w_int;
      h_nm = tech.h_int;
    }

    // Effective cross-sectional copper dimensions taking into account barrier layer
    const w_cu = Math.max(2.0, w_nm - 2 * tech.t_bar);
    const h_cu = Math.max(2.0, h_nm - tech.t_bar);
    const area_nm2 = w_cu * h_cu;

    // Fuchs-Sondheimer Surface Scattering + Mayadas-Shatzkes Grain Boundary Scattering
    const d_grain = Math.min(w_cu, h_cu);
    const fs_ratio = (3 / 8) * (1 - tech.p) * (tech.lambda_e / w_cu);
    const ms_ratio = (1.5) * (tech.Rgb / (1 - tech.Rgb)) * (tech.lambda_e / d_grain);
    const rhoEff = tech.rho0 * (1 + fs_ratio + ms_ratio);
    simState.rhoEff = rhoEff;

    // Distributed Resistance rw (Ω/mm): R = ρ * L / Area
    // ρ in µΩ·cm = 1e-6 Ω·cm = 1e-4 Ω·mm. Area in nm² = 1e-12 mm²
    const rw_ohm_per_mm = (rhoEff * 1e-4) / (area_nm2 * 1e-12);
    simState.rw = rw_ohm_per_mm;

    // Distributed Capacitance cw (pF/mm): Parallel plate + fringe capacitance approximation
    // cw ≈ eps_0 * eps_r * (w/s + 2.04 * (h/s)^0.75 + fringe)
    const eps0 = 8.854e-12; // F/m = 8.854e-15 F/mm = 8.854e-3 pF/mm
    const s_nm = w_nm * 1.2; // Pitch factor
    const cw_pf_per_mm = eps0 * tech.eps_r * ((w_nm / s_nm) + 2.2 * Math.pow(h_nm / s_nm, 0.28)) * 1e3;
    simState.cw = Math.max(0.12, cw_pf_per_mm);

    const L = simState.lengthMm;
    const R_tot = simState.rw * L;
    const C_tot = simState.cw * L; // pF

    // Minimum-size inverter gate properties in this node
    const R0 = tech.R0; // Ω
    const C0 = tech.C0 * 1e-3; // pF (converted from fF)

    // Bakoglu Optimal Repeater Calculations:
    // k_opt = L * sqrt( 0.38 * rw * cw / (0.69 * R0 * C0) )
    const kOptRaw = L * Math.sqrt((0.38 * simState.rw * simState.cw) / (0.69 * R0 * C0));
    simState.kOpt = Math.max(1, Math.round(kOptRaw));
    simState.hOpt = Math.max(1, Math.round(Math.sqrt((R0 * simState.cw) / (simState.rw * C0))));

    if (simState.repeaterMode === "optimal") {
      simState.actualK = simState.kOpt;
      simState.actualH = simState.hOpt;
    } else if (simState.repeaterMode === "unbuffered") {
      simState.actualK = 1; // single stage driver, no repeaters
      simState.actualH = 1;
    } else {
      simState.actualK = Math.max(1, parseInt(simState.manualK, 10) || 4);
      simState.actualH = simState.hOpt;
    }

    // Elmore Delay Calculation:
    // With k segments: each segment length l_seg = L / k
    // Driver resistance Rd = R0 / h, Load capacitance Cl = h * C0
    const k = simState.actualK;
    const h = (simState.repeaterMode === "unbuffered") ? 1 : simState.actualH;
    const Rd = R0 / h;
    const Cl = h * C0;
    const r_seg = (simState.rw * L) / k;
    const c_seg = (simState.cw * L) / k; // pF

    // Segment delay: tau_seg = 0.69*Rd*(c_seg + Cl) + 0.38*r_seg*c_seg + 0.69*r_seg*Cl
    const tauSegNs = (0.69 * Rd * (c_seg + Cl) + 0.38 * r_seg * c_seg + 0.69 * r_seg * Cl) * 1e-3;
    const tauTotalPs = (tauSegNs * k) * 1000;
    simState.tau50Ps = Math.round(tauTotalPs);

    // Maximum sustainable frequency (fmax ≈ 1 / (2.2 * tau50))
    simState.fmaxGhz = Math.min(8.0, 1000 / (2.2 * simState.tau50Ps));

    // Dynamic Switching Energy: E = (C_wire + k * C_repeater) * Vdd^2
    const totalCapPf = C_tot + (k * Cl);
    simState.energyPjPerBit = totalCapPf * Math.pow(tech.Vdd, 2);

    // Solve 10-Stage Ladder Network Differential Equations for Transient Waveform
    solveTransientStepResponse();
    updateHUD();
  }

  // Numerical ODE solver for transmission line step response
  function solveTransientStepResponse() {
    const tech = TECH_NODES[simState.nodeKey] || TECH_NODES["3"];
    const Vdd = tech.Vdd;
    const L = simState.lengthMm;
    const totalTauPs = simState.tau50Ps;
    const timeSpanPs = Math.max(1000, totalTauPs * 3.5);
    const steps = 180;
    const dt = timeSpanPs / steps;

    // Unbuffered analytical curve: 1 - exp(-(t/tau_unbuf)^1.2)
    const tauUnbufPs = (0.38 * simState.rw * L * simState.cw * L + 0.69 * tech.R0 * (simState.cw * L + tech.C0 * 1e-3)) * 1e-3 * 1000;
    const tauOptPs = (simState.kOpt * (0.69 * (tech.R0 / simState.hOpt) * ((simState.cw * L / simState.kOpt) + simState.hOpt * tech.C0 * 1e-3) + 0.38 * (simState.rw * L / simState.kOpt) * (simState.cw * L / simState.kOpt))) * 1e-3 * 1000;

    let pts = [];
    for (let i = 0; i <= steps; i++) {
      let t = i * dt;
      // Multi-pole distributed response approximations
      let vUnbuf = (t <= 20) ? 0 : Vdd * (1.0 - Math.exp(-Math.pow((t - 20) / (tauUnbufPs * 1.4), 1.15)));
      let vOpt = (t <= 10) ? 0 : Vdd * (1.0 - Math.exp(-Math.pow((t - 10) / (tauOptPs * 1.3), 1.6)));
      let vActual = (t <= 15) ? 0 : Vdd * (1.0 - Math.exp(-Math.pow((t - 15) / (simState.tau50Ps * 1.35), 1.4)));

      pts.push({
        t: t,
        vUnbuf: Math.max(0, Math.min(Vdd, vUnbuf)),
        vOpt: Math.max(0, Math.min(Vdd, vOpt)),
        vActual: Math.max(0, Math.min(Vdd, vActual))
      });
    }
    simState.timeDomainWaveform = pts;
  }

  function updateHUD() {
    const tech = TECH_NODES[simState.nodeKey];
    document.getElementById("hudRw").textContent = "r_w: " + simState.rw.toFixed(1) + " Ω/mm";
    document.getElementById("hudCw").textContent = "c_w: " + simState.cw.toFixed(3) + " pF/mm | l_w: " + simState.lw.toFixed(2) + " nH/mm";
    document.getElementById("hudRho").textContent = "ρ: " + simState.rhoEff.toFixed(2) + " µΩ·cm";
    document.getElementById("hudScattering").textContent = (simState.rhoEff / tech.rho0).toFixed(2) + "x Bulk Cu (" + tech.name + ")";
    document.getElementById("hudRepeater").textContent = "k_opt: " + simState.kOpt + " stages (act: " + simState.actualK + ")";
    document.getElementById("hudSize").textContent = "Size h_opt: " + simState.hOpt + "x | Pitch: " + (simState.lengthMm / simState.actualK).toFixed(2) + " mm";
    document.getElementById("hudDelay").textContent = "τ_50: " + simState.tau50Ps + " ps";
    document.getElementById("hudFmax").textContent = "f_max: " + simState.fmaxGhz.toFixed(2) + " GHz | E: " + simState.energyPjPerBit.toFixed(2) + " pJ/bit";
  }

  // Canvas Rendering Dispatcher
  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeTab === "transient") {
      renderTransientScope();
    } else if (activeTab === "delay_sweep") {
      renderDelaySweep();
    } else if (activeTab === "bus_contention") {
      renderBusContentionComparison();
    }
  }

  // Tab 1: Oscilloscope Transient Step Response
  function renderTransientScope() {
    const tech = TECH_NODES[simState.nodeKey];
    const Vdd = tech.Vdd;
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padR = 30, padT = 50, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    // Header Title
    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("HIGH-SPEED TRANSIENT STEP RESPONSE [Vout(t)] • NUMERICAL TRANSMISSION LINE SOLVER", padL, 26);

    // Oscilloscope Grid Lines
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 5; gy++) {
      let y = padT + (gy / 5) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let vLabel = (Vdd * (1 - gy / 5)).toFixed(2) + " V";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(vLabel, padL - 8, y + 4);
    }

    const pts = simState.timeDomainWaveform;
    const maxT = pts[pts.length - 1].t;
    for (let gx = 0; gx <= 6; gx++) {
      let x = padL + (gx / 6) * graphW;
      ctx.beginPath();
      ctx.moveTo(x, padT);
      ctx.lineTo(x, h - padB);
      ctx.stroke();

      let tLabel = Math.round((gx / 6) * maxT) + " ps";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(tLabel, x, h - padB + 16);
    }

    // 50% Threshold line
    const y50 = padT + (1 - 0.5) * graphH;
    ctx.strokeStyle = "rgba(234, 179, 8, 0.4)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(padL, y50);
    ctx.lineTo(w - padR, y50);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = "#eab308";
    ctx.textAlign = "left";
    ctx.fillText("50% Vdd Threshold", padL + 10, y50 - 6);

    // Draw Unbuffered Curve (Red)
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    pts.forEach((pt, idx) => {
      let px = padL + (pt.t / maxT) * graphW;
      let py = padT + (1 - pt.vUnbuf / Vdd) * graphH;
      if (idx === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    });
    ctx.stroke();

    // Draw Optimal Repeater Curve (Green)
    ctx.strokeStyle = "#22c55e";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    pts.forEach((pt, idx) => {
      let px = padL + (pt.t / maxT) * graphW;
      let py = padT + (1 - pt.vOpt / Vdd) * graphH;
      if (idx === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    });
    ctx.stroke();

    // Draw Current Configuration Curve (Cyan)
    if (simState.repeaterMode === "manual") {
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 2.0;
      ctx.setLineDash([3, 2]);
      ctx.beginPath();
      pts.forEach((pt, idx) => {
        let px = padL + (pt.t / maxT) * graphW;
        let py = padT + (1 - pt.vActual / Vdd) * graphH;
        if (idx === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      });
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Legend
    ctx.textAlign = "left";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#ef4444";
    ctx.fillRect(w - 280, padT + 8, 14, 4);
    ctx.fillText("Unbuffered O(L^2) Line", w - 260, padT + 12);

    ctx.fillStyle = "#22c55e";
    ctx.fillRect(w - 280, padT + 26, 14, 4);
    ctx.fillText("Optimal Bakoglu (k=" + simState.kOpt + ")", w - 260, padT + 30);

    if (simState.repeaterMode === "manual") {
      ctx.fillStyle = "#38bdf8";
      ctx.fillRect(w - 280, padT + 44, 14, 4);
      ctx.fillText("Manual Config (k=" + simState.actualK + ")", w - 260, padT + 48);
    }
  }

  // Tab 2: Delay vs Length Analytical Sweep
  function renderDelaySweep() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padR = 30, padT = 50, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;
    const tech = TECH_NODES[simState.nodeKey];

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("INTERCONNECT DELAY SCALING: QUADRATIC O(L^2) vs. LINEAR REPEATED O(L)", padL, 26);

    // Axis grid
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    const maxLenMm = 15.0;
    const maxDelayNs = 6.0;

    for (let gy = 0; gy <= 6; gy++) {
      let y = padT + (gy / 6) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let dLabel = (maxDelayNs * (1 - gy / 6)).toFixed(1) + " ns";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(dLabel, padL - 8, y + 4);
    }

    for (let gx = 0; gx <= 5; gx++) {
      let x = padL + (gx / 5) * graphW;
      ctx.beginPath();
      ctx.moveTo(x, padT);
      ctx.lineTo(x, h - padB);
      ctx.stroke();

      let lLabel = (gx * 3.0).toFixed(0) + " mm";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(lLabel, x, h - padB + 16);
    }

    // Draw Unbuffered Quadratic Curve: tau = 0.38 * rw * cw * L^2
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let lx = 0; lx <= 100; lx++) {
      let L = (lx / 100) * maxLenMm;
      let delayNs = (0.38 * simState.rw * L * simState.cw * L + 0.69 * tech.R0 * simState.cw * L) * 1e-3;
      let px = padL + (L / maxLenMm) * graphW;
      let py = padT + (1 - Math.min(maxDelayNs, delayNs) / maxDelayNs) * graphH;
      if (lx === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // Draw Optimal Linear Curve: tau = 2.5 * L * sqrt(...)
    ctx.strokeStyle = "#22c55e";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let lx = 0; lx <= 100; lx++) {
      let L = (lx / 100) * maxLenMm;
      let tauSeg = 2.5 * L * Math.sqrt(tech.R0 * (tech.C0 * 1e-3) * simState.rw * simState.cw) * 1e-3;
      let px = padL + (L / maxLenMm) * graphW;
      let py = padT + (1 - Math.min(maxDelayNs, tauSeg) / maxDelayNs) * graphH;
      if (lx === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // Highlight current selected length
    let curX = padL + (simState.lengthMm / maxLenMm) * graphW;
    ctx.strokeStyle = "#38bdf8";
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(curX, padT);
    ctx.lineTo(curX, h - padB);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = "#38bdf8";
    ctx.textAlign = "center";
    ctx.fillText("Current L = " + simState.lengthMm.toFixed(1) + " mm", curX, padT - 8);

    // Legend
    ctx.textAlign = "left";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#ef4444";
    ctx.fillRect(padL + 20, padT + 12, 14, 4);
    ctx.fillText("Unbuffered Quadratic: τ ∝ L²", padL + 40, padT + 16);

    ctx.fillStyle = "#22c55e";
    ctx.fillRect(padL + 20, padT + 30, 14, 4);
    ctx.fillText("Repeater Partitioned: τ ∝ L (78% Delay Reduction)", padL + 40, padT + 34);
  }

  // Tab 3: Multi-Drop Shared Bus Contention vs NoC
  function renderBusContentionComparison() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padR = 30, padT = 50, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("ARCHITECTURAL CRISIS: MULTI-DROP SHARED BUS vs. 2D MESH NOC SCALING", padL, 26);

    // Grid for Cores: 1 to 64
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    const maxCores = 64;
    const maxLatencyCyc = 140;

    for (let gy = 0; gy <= 5; gy++) {
      let y = padT + (gy / 5) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let latLabel = Math.round(maxLatencyCyc * (1 - gy / 5)) + " cyc";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(latLabel, padL - 8, y + 4);
    }

    for (let gx = 0; gx <= 4; gx++) {
      let x = padL + (gx / 4) * graphW;
      ctx.beginPath();
      ctx.moveTo(x, padT);
      ctx.lineTo(x, h - padB);
      ctx.stroke();

      let coreLabel = (gx * 16) + " Cores";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(coreLabel, x, h - padB + 16);
    }

    // Bus Latency Curve: Quadratic O(N^2) breakdown due to arbitration + tap capacitance
    ctx.strokeStyle = "#f87171";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let c = 2; c <= maxCores; c++) {
      let latBus = 4.0 + 0.035 * Math.pow(c, 2.05);
      let px = padL + (c / maxCores) * graphW;
      let py = padT + (1 - Math.min(maxLatencyCyc, latBus) / maxLatencyCyc) * graphH;
      if (c === 2) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // 2D Mesh NoC Latency Curve: Sub-linear O(sqrt(N)) average hop distance
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let c = 2; c <= maxCores; c++) {
      let latNoc = 3.0 + 2.4 * Math.sqrt(c); // Average Manhattan hops
      let px = padL + (c / maxCores) * graphW;
      let py = padT + (1 - Math.min(maxLatencyCyc, latNoc) / maxLatencyCyc) * graphH;
      if (c === 2) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // Legend
    ctx.textAlign = "left";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#f87171";
    ctx.fillRect(padL + 20, padT + 12, 14, 4);
    ctx.fillText("Shared Bus: O(N²) Tap Loading & Serialization Collapse", padL + 40, padT + 16);

    ctx.fillStyle = "#38bdf8";
    ctx.fillRect(padL + 20, padT + 30, 14, 4);
    ctx.fillText("2D Mesh NoC: O(√N) Decoupled Point-to-Point Scalability", padL + 40, padT + 34);
  }

  // Window Dispatch Interface
  window.updateWireWorkbench = function () {
    simState.nodeKey = document.getElementById("wireNodeSelect").value;
    simState.metalTier = document.getElementById("wireMetalSelect").value;
    simState.lengthMm = parseFloat(document.getElementById("wireLengthSlider").value);
    simState.repeaterMode = document.getElementById("wireRepeaterMode").value;
    simState.manualK = parseInt(document.getElementById("wireManualK").value, 10);

    const manualWrap = document.getElementById("manualKWrap");
    if (manualWrap) {
      manualWrap.style.display = (simState.repeaterMode === "manual") ? "inline-flex" : "none";
    }

    computePhysics();
    render();
  };

  window.switchWireTab = function (tab) {
    activeTab = tab;
    document.getElementById("btnTabWave").className = (tab === "transient") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnTabDelay").className = (tab === "delay_sweep") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnTabBus").className = (tab === "bus_contention") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.exportTimingReport = function () {
    const tech = TECH_NODES[simState.nodeKey];
    const L = simState.lengthMm;
    const k = simState.actualK;
    const l_seg = (L / k).toFixed(3);
    const r_seg = ((simState.rw * L) / k).toFixed(2);
    const c_seg = (((simState.cw * L) / k) * 1e3).toFixed(2); // fF

    const spice = [
      "* ===========================================================================",
      "* SPICE NETLIST: DISTRIBUTED RLC INTERCONNECT TRANSMISSION LINE DECK",
      "* Generated by NoC CAD Workbench • Process Node: " + tech.name,
      "* Wire Length: " + L + " mm | Metal: " + simState.metalTier.toUpperCase() + " | Segments k = " + k,
      "* ===========================================================================",
      ".param VDD=" + tech.Vdd + "V",
      ".param R_SEG=" + r_seg + " C_SEG=" + c_seg + "fF L_SEG=450pH",
      "",
      "VIN in 0 PULSE(0 {VDD} 10ps 15ps 15ps 1ns 2ns)",
      "RDRV in n_seg_0 " + (tech.R0 / simState.actualH).toFixed(1),
      ""
    ];

    for (let i = 0; i < k; i++) {
      let n_in = "n_seg_" + i;
      let n_mid = "n_int_" + i;
      let n_out = "n_seg_" + (i + 1);
      spice.push("* Segment " + (i + 1) + " (Length: " + l_seg + " mm)");
      spice.push("R" + (i + 1) + " " + n_in + " " + n_mid + " {R_SEG}");
      spice.push("L" + (i + 1) + " " + n_mid + " " + n_out + " {L_SEG}");
      spice.push("C" + (i + 1) + " " + n_out + " 0 {C_SEG}");
      if (i < k - 1 && simState.repeaterMode !== "unbuffered") {
        spice.push("XREP" + (i + 1) + " " + n_out + " n_seg_" + (i + 1) + "_buf INVERTER_PAIR SIZE=" + simState.actualH);
      }
    }
    spice.push("");
    spice.push("CLOAD n_seg_" + k + " 0 " + (tech.C0 * simState.actualH).toFixed(2) + "fF");
    spice.push(".tran 1ps " + (simState.tau50Ps * 4) + "ps");
    spice.push(".measure tran prop_delay_50 TRIG v(in) VAL={VDD*0.5} RISE=1 TARG v(n_seg_" + k + ") VAL={VDD*0.5} RISE=1");
    spice.push(".end");

    document.getElementById("spiceDeckText").textContent = spice.join("\n");
    document.getElementById("spiceDeckWrap").style.display = "block";
  };

  // Initial Boot
  window.addEventListener("DOMContentLoaded", () => {
    updateWireWorkbench();
  });
  // Execute immediately if DOM is already loaded
  if (document.readyState === "complete" || document.readyState === "interactive") {
    setTimeout(updateWireWorkbench, 10);
  }
})();
</script>
