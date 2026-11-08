# 🏢 3D-NoC Interconnect & TSV Thermo-Mechanical Stress CAD Analyzer

An interactive Computer-Aided Design (CAD) workbench for Three-Dimensional Networks-on-Chip (3D-NoCs) and Through-Silicon Vias (TSVs). Model cylindrical high-frequency electrical parasitics ($R_{tsv}, L_{tsv}, C_{tsv}$), calculate thermo-mechanical thermal expansion mismatch ($\Delta\alpha_{Cu-Si} \approx 14.9\times 10^{-6}/\text{K}$) and Lamé stress fields ($\sigma_r, \sigma_\theta$), compute piezoresistive carrier mobility Keep-Out Zones (KOZ), and optimize thermal dummy TSV placement across multi-tier vertical silicon stacks.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>TSV Diameter (2*r):</b>
      <select id="tsvDiameterSelect" class="noc-sim-select" onchange="updateTsvWorkbench()">
        <option value="2.0">2.0 µm High-Density (Aspect Ratio 10:1, Fine Pitch)</option>
        <option value="5.0" selected>5.0 µm Standard Production (Aspect Ratio 8:1)</option>
        <option value="10.0">10.0 µm Power/Thermal Via (Aspect Ratio 5:1, Low R)</option>
      </select>
    </label>

    <label><b>Dielectric Liner:</b>
      <select id="tsvLinerSelect" class="noc-sim-select" onchange="updateTsvWorkbench()">
        <option value="sio2" selected>SiO2 Thermal Oxide (t_ox = 120 nm, k = 3.9)</option>
        <option value="sin">Si3N4 Nitride Liner (t_ox = 80 nm, k = 7.0)</option>
        <option value="polymer">Low-k Polymer / BCB (t_ox = 250 nm, k = 2.6)</option>
      </select>
    </label>

    <label><b>Thermal Gradient (ΔT):</b>
      <input type="range" id="tsvDeltaTSlider" min="20" max="120" step="5" value="70" style="width:100px; vertical-align:middle;" oninput="document.getElementById('tsvDeltaTVal').textContent = this.value + '°C'; updateTsvWorkbench();">
      <span id="tsvDeltaTVal" style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#f87171;">70°C</span>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnTsvStress" onclick="switchTsvView('stress')" style="background:#0284c7;">🎯 Von Mises Stress &amp; KOZ</button>
      <button class="noc-sim-btn secondary" id="btnTsvParasitics" onclick="switchTsvView('parasitics')">⚡ Electrical Parasitics (RLC)</button>
      <button class="noc-sim-btn secondary" id="btnTsvStack" onclick="switchTsvView('stack_profile')">🏢 Vertical 4-Tier Stacking</button>
      <button class="noc-sim-btn secondary" onclick="toggleDummyTsvs()">🔥 Insert Dummy Thermal TSVs</button>
      <button class="noc-sim-btn secondary" onclick="exportTsvReport()" style="margin-left:auto;">📋 Export 3D SPICE Deck</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Electrical Parasitics</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudTsvRlc">R: 42.4 mΩ | C: 54.2 fF</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudTsvInd">L: 28.5 pH | RC Delay: 2.3 ps</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Thermo-Mechanical Stress</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudPeakStress">σ_vM: 412.5 MPa</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudCteMismatch">CTE Mismatch: Δα = 14.9 ppm/K</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Transistor Keep-Out Zone</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudKozRadius">r_KOZ: 4.82 µm</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudKozMobility">Exclusion Area: 73.0 µm² (|Δµ| &gt; 5%)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Vertical Stack Thermal Relief</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudThermalRelief">32 Dummy Conduits (-18.4°C)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudBottomTierTemp">Bottom Tier: 68.2°C (Safe)</div>
    </div>
  </div>

  <!-- CAD Canvas View -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="tsvCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- Export Report Modal / Panel -->
  <div id="tsvExportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">3D TSV High-Frequency SPICE Equivalent Deck:</strong>
      <button onclick="document.getElementById('tsvExportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="tsvExportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 3D TSV Physical Modeling &amp; Thermo-Mechanical Mechanics (Chapter 8):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Cylindrical TSV Parasitic Formulation:</strong> For a copper cylinder of radius $r_{tsv}$, height $h_{tsv} \approx 40\,\mu\text{m}$, and dielectric liner thickness $t_{ox}$, capacitance and resistance are given by:
        $$C_{tsv} = \frac{2\pi \varepsilon_0 \varepsilon_{ox} h_{tsv}}{\ln\left(1 + \frac{t_{ox}}{r_{tsv}}\right)}, \quad R_{tsv} = \rho_{Cu} \frac{h_{tsv}}{\pi r_{tsv}^2}$$
        A $5\,\mu\text{m}$ TSV exhibits sub-$60\text{ fF}$ capacitance and sub-$50\text{ m}\Omega$ resistance, enabling sub-$5\text{ ps}$ vertical transit times.</li>
      <li><strong>Lamé Thermo-Mechanical Stress Field:</strong> Differential thermal expansion between Copper ($\alpha_{Cu} = 17.5\times 10^{-6}/\text{K}$) and Silicon ($\alpha_{Si} = 2.6\times 10^{-6}/\text{K}$) induces intense compressive radial stress $\sigma_r$ and tensile hoop stress $\sigma_\theta$:
        $$\sigma_r(r) = - \frac{\Delta\alpha \cdot \Delta T \cdot E_{si}}{1 + \nu_{si}} \left(\frac{r_{tsv}}{r}\right)^2, \quad \sigma_\theta(r) = - \sigma_r(r)$$
        $$\sigma_{vM}(r) = \sqrt{\sigma_r^2 + \sigma_\theta^2 - \sigma_r \sigma_\theta} = \sqrt{3} |\sigma_r(r)|$$</li>
      <li><strong>Transistor Keep-Out Zone (KOZ):</strong> Piezoresistive stress shifts NMOS electron mobility and PMOS hole mobility ($\Delta\mu / \mu = \Pi_{11} \sigma_{xx} + \Pi_{12} \sigma_{yy}$). Standard cell transistors must be strictly excluded within a radius $r_{KOZ} \approx 2.5 \times r_{tsv}$ to prevent clock jitter and threshold voltage mismatch.</li>
      <li><strong>Thermal Stacking Crisis &amp; Dummy Conduits:</strong> Silicon dioxide bonding layers ($k_{ox} \approx 1.2\text{ W/m}\cdot\text{K}$) act as severe thermal insulators. Inserting passive copper dummy TSVs ($k_{Cu} \approx 400\text{ W/m}\cdot\text{K}$) provides vertical heat conduits, sinking heat from trapped bottom compute tiers directly into the package heatsink.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// 3D-NoC TSV Electrical & Thermo-Mechanical Stress CAD Engine
// ============================================================================

(function () {
  let activeView = "stress"; // "stress", "parasitics", "stack_profile"
  let hasDummyTsvs = true;

  let tsvMetrics = {
    radiusUm: 2.5,
    heightUm: 40.0,
    rOhm: 0.042,
    cFf: 54.2,
    lPh: 28.5,
    rcDelayPs: 2.3,
    peakStressMpa: 412.5,
    kozRadiusUm: 4.82,
    kozAreaUm2: 73.0,
    deltaT: 70.0,
    bottomTierTempC: 68.2
  };

  const canvas = document.getElementById("tsvCanvas");
  const ctx = canvas.getContext("2d");

  function computeTsvPhysics() {
    const diamUm = parseFloat(document.getElementById("tsvDiameterSelect").value) || 5.0;
    const linerType = document.getElementById("tsvLinerSelect").value;
    const deltaT = parseFloat(document.getElementById("tsvDeltaTSlider").value) || 70.0;

    const r_um = diamUm * 0.5;
    const h_um = 40.0;
    tsvMetrics.radiusUm = r_um;
    tsvMetrics.heightUm = h_um;
    tsvMetrics.deltaT = deltaT;

    let t_ox_um = (linerType === "polymer") ? 0.25 : (linerType === "sin" ? 0.08 : 0.12);
    let eps_r = (linerType === "polymer") ? 2.6 : (linerType === "sin" ? 7.0 : 3.9);

    // 1. Electrical Parasitics
    // R = rho * h / (pi * r^2)  (rho_Cu = 1.7e-8 Ohm*m = 1.7e-2 Ohm*um)
    const rhoCu = 0.022; // Ohm*um accounting for thin barrier
    const rTsv = (rhoCu * h_um) / (Math.PI * Math.pow(r_um, 2));
    tsvMetrics.rOhm = rTsv;

    // C = 2 * pi * eps0 * eps_r * h / ln(1 + t_ox / r)
    // eps0 = 8.854e-18 F/um = 8.854e-3 fF/um
    const eps0 = 8.854e-3; // fF/um
    const cTsv = (2 * Math.PI * eps0 * eps_r * h_um) / Math.log(1 + t_ox_um / r_um);
    tsvMetrics.cFf = cTsv;

    // Loop Inductance: L ≈ (mu0 * h / 2pi) * [ln(2h/r) - 0.75]
    // mu0 / 2pi = 0.2 pH/um
    const lPh = 0.2 * h_um * (Math.log((2 * h_um) / r_um) - 0.75);
    tsvMetrics.lPh = lPh;

    tsvMetrics.rcDelayPs = (rTsv * cTsv) * 1e3;

    // 2. Thermo-Mechanical Stress (Lamé Equations)
    // E_si = 130 GPa, nu_si = 0.28, delta_alpha = 14.9e-6 /K
    const E_si_gpa = 130.0;
    const nu_si = 0.28;
    const deltaAlpha = 14.9e-6; // 1/K

    // At interface r = r_tsv:
    // sigma_r = - delta_alpha * deltaT * E_si / (1 + nu_si)
    const sigmaR_interface_Mpa = Math.abs((deltaAlpha * deltaT * (E_si_gpa * 1e3)) / (1 + nu_si));
    const sigmaVm_interface_Mpa = Math.sqrt(3) * sigmaR_interface_Mpa;
    tsvMetrics.peakStressMpa = sigmaVm_interface_Mpa;

    // KOZ Radius: Distance r where delta_mu / mu drops below 5% (sigma_vM < 120 MPa)
    // sigma_vM(r) = sigma_vM_interface * (r_tsv / r)^2  =>  r_koz = r_tsv * sqrt(sigma_vM_interface / 120)
    const kozRatio = Math.sqrt(sigmaVm_interface_Mpa / 120.0);
    const rKozUm = r_um * Math.max(1.0, kozRatio);
    tsvMetrics.kozRadiusUm = rKozUm;
    tsvMetrics.kozAreaUm2 = Math.PI * Math.pow(rKozUm, 2);

    // 3. Thermal Stacking
    let baselineBottomTemp = 86.6;
    let coolingOffset = hasDummyTsvs ? 18.4 : 0.0;
    tsvMetrics.bottomTierTempC = baselineBottomTemp - coolingOffset;

    updateHUD();
  }

  function updateHUD() {
    document.getElementById("hudTsvRlc").textContent = "R: " + (tsvMetrics.rOhm * 1e3).toFixed(1) + " mΩ | C: " + tsvMetrics.cFf.toFixed(1) + " fF";
    document.getElementById("hudTsvInd").textContent = "L: " + tsvMetrics.lPh.toFixed(1) + " pH | RC Delay: " + tsvMetrics.rcDelayPs.toFixed(2) + " ps";
    document.getElementById("hudPeakStress").textContent = "σ_vM: " + tsvMetrics.peakStressMpa.toFixed(1) + " MPa";
    document.getElementById("hudCteMismatch").textContent = "CTE Mismatch: Δα = 14.9 ppm/K (ΔT=" + tsvMetrics.deltaT + "°C)";
    document.getElementById("hudKozRadius").textContent = "r_KOZ: " + tsvMetrics.kozRadiusUm.toFixed(2) + " µm (5% Mobility Threshold)";
    document.getElementById("hudKozMobility").textContent = "Exclusion Area: " + tsvMetrics.kozAreaUm2.toFixed(1) + " µm² per TSV";
    document.getElementById("hudThermalRelief").textContent = hasDummyTsvs ? "32 Conduits Active (-18.4°C)" : "NO DUMMY CONDUITS (Trapped Heat)";
    document.getElementById("hudBottomTierTemp").textContent = "Bottom Tier: " + tsvMetrics.bottomTierTempC.toFixed(1) + "°C (" + (tsvMetrics.bottomTierTempC > 85 ? "THROTTLED" : "SAFE") + ")";
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "stress") {
      renderStressView();
    } else if (activeView === "parasitics") {
      renderParasiticsView();
    } else if (activeView === "stack_profile") {
      renderStackProfile();
    }
  }

  // 1. Stress Field & Keep-Out Zone (KOZ)
  function renderStressView() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("RADIAL THERMO-MECHANICAL VON MISES STRESS FIELD [σ_vM(r)] & KOZ", padL, 28);

    const maxR = tsvMetrics.radiusUm * 6.0;
    const maxStress = tsvMetrics.peakStressMpa * 1.15;

    // Grid
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let sLabel = Math.round(maxStress * (1 - gy / 4)) + " MPa";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(sLabel, padL - 8, y + 4);
    }

    for (let gx = 0; gx <= 5; gx++) {
      let x = padL + (gx / 5) * graphW;
      ctx.beginPath();
      ctx.moveTo(x, padT);
      ctx.lineTo(x, h - padB);
      ctx.stroke();

      let rLabel = ((gx / 5) * maxR).toFixed(1) + " µm";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(rLabel, x, h - padB + 16);
    }

    // Critical 120 MPa Mobility Degradation Line
    let y120 = padT + (1 - 120 / maxStress) * graphH;
    ctx.strokeStyle = "rgba(234, 179, 8, 0.5)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(padL, y120);
    ctx.lineTo(w - padR, y120);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = "#eab308";
    ctx.textAlign = "left";
    ctx.fillText("5% Mobility Threshold (120 MPa)", padL + 10, y120 - 6);

    // Plot Stress Decay Curve: sigma(r) = sigma_interface * (r_tsv / r)^2
    ctx.strokeStyle = "#f87171";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let step = 0; step <= 100; step++) {
      let r = tsvMetrics.radiusUm + (step / 100) * (maxR - tsvMetrics.radiusUm);
      let s = tsvMetrics.peakStressMpa * Math.pow(tsvMetrics.radiusUm / r, 2);
      let px = padL + (r / maxR) * graphW;
      let py = padT + (1 - Math.min(maxStress, s) / maxStress) * graphH;
      if (step === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // Mark TSV Edge & KOZ Boundary
    let tsvX = padL + (tsvMetrics.radiusUm / maxR) * graphW;
    ctx.strokeStyle = "#38bdf8";
    ctx.beginPath();
    ctx.moveTo(tsvX, padT);
    ctx.lineTo(tsvX, h - padB);
    ctx.stroke();
    ctx.fillStyle = "#38bdf8";
    ctx.textAlign = "center";
    ctx.fillText("TSV Edge (" + tsvMetrics.radiusUm.toFixed(1) + "µm)", tsvX, padT - 8);

    let kozX = padL + (tsvMetrics.kozRadiusUm / maxR) * graphW;
    ctx.strokeStyle = "#22c55e";
    ctx.beginPath();
    ctx.moveTo(kozX, padT);
    ctx.lineTo(kozX, h - padB);
    ctx.stroke();
    ctx.fillStyle = "#22c55e";
    ctx.fillText("r_KOZ = " + tsvMetrics.kozRadiusUm.toFixed(2) + "µm", kozX, padT - 8);
  }

  // 2. High-Frequency Parasitics View
  function renderParasiticsView() {
    const w = canvas.width;
    const h = canvas.height;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("HIGH-FREQUENCY TSV EQUIVALENT PI-NETWORK TRANSMISSION MODEL", 70, 36);

    // Draw Cylindrical TSV Structure on Left
    const cx = 160, cy = 230;
    const rPx = tsvMetrics.radiusUm * 12;
    const hPx = 180;

    // Copper Core
    ctx.fillStyle = "#b45309";
    ctx.strokeStyle = "#f59e0b";
    ctx.lineWidth = 2;
    ctx.fillRect(cx - rPx, cy - hPx / 2, rPx * 2, hPx);
    ctx.strokeRect(cx - rPx, cy - hPx / 2, rPx * 2, hPx);

    // Dielectric Liner
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 3;
    ctx.strokeRect(cx - rPx - 4, cy - hPx / 2, (rPx + 4) * 2, hPx);

    ctx.fillStyle = "#f59e0b";
    ctx.font = "bold 11px 'JetBrains Mono', monospace";
    ctx.textAlign = "center";
    ctx.fillText("Copper Core", cx, cy);
    ctx.fillStyle = "#38bdf8";
    ctx.fillText("Dielectric Liner (SiO2)", cx, cy + 20);

    // Equivalent Lumped R-L-C Circuit Diagram on Right
    const eqX = 360, eqY = 230;
    ctx.strokeStyle = "#64748b";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(eqX, eqY);
    ctx.lineTo(eqX + 260, eqY);
    ctx.stroke();

    // R_tsv box
    ctx.fillStyle = "#1e293b";
    ctx.strokeStyle = "#eab308";
    ctx.strokeRect(eqX + 40, eqY - 14, 60, 28);
    ctx.fillRect(eqX + 40, eqY - 14, 60, 28);
    ctx.fillStyle = "#eab308";
    ctx.font = "10px 'JetBrains Mono', monospace";
    ctx.fillText("R_tsv", eqX + 70, eqY + 4);
    ctx.fillText((tsvMetrics.rOhm * 1e3).toFixed(1) + " mΩ", eqX + 70, eqY - 18);

    // L_tsv symbol
    ctx.fillStyle = "#1e293b";
    ctx.strokeStyle = "#38bdf8";
    ctx.strokeRect(eqX + 130, eqY - 14, 60, 28);
    ctx.fillRect(eqX + 130, eqY - 14, 60, 28);
    ctx.fillStyle = "#38bdf8";
    ctx.fillText("L_tsv", eqX + 160, eqY + 4);
    ctx.fillText(tsvMetrics.lPh.toFixed(1) + " pH", eqX + 160, eqY - 18);

    // C_tsv shunt capacitors
    ctx.strokeStyle = "#22c55e";
    ctx.beginPath();
    ctx.moveTo(eqX + 20, eqY);
    ctx.lineTo(eqX + 20, eqY + 50);
    ctx.moveTo(eqX + 220, eqY);
    ctx.lineTo(eqX + 220, eqY + 50);
    ctx.stroke();

    ctx.fillStyle = "#22c55e";
    ctx.fillText("C_tsv/2", eqX + 20, eqY + 70);
    ctx.fillText((tsvMetrics.cFf * 0.5).toFixed(1) + " fF", eqX + 20, eqY + 84);
    ctx.fillText("C_tsv/2", eqX + 220, eqY + 70);
    ctx.fillText((tsvMetrics.cFf * 0.5).toFixed(1) + " fF", eqX + 220, eqY + 84);
  }

  // 3. Vertical 4-Tier Stacking Profile
  function renderStackProfile() {
    const w = canvas.width;
    const h = canvas.height;
    const startX = 140, startY = 80, tierW = 420, tierH = 50, gap = 24;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("VERTICAL 4-TIER SILICON TEMPERATURE PROFILE & THERMAL DUMMY TSVS", 70, 36);

    const tiers = [
      { name: "Tier 4: Heat Spreader & Package Sink", temp: 42.0, color: "#38bdf8" },
      { name: "Tier 3: Cache / SRAM Memory Tier", temp: hasDummyTsvs ? 52.4 : 64.2, color: "#22c55e" },
      { name: "Tier 2: Host CPU Control Cluster", temp: hasDummyTsvs ? 61.8 : 77.5, color: "#eab308" },
      { name: "Tier 1: High-Density NPU Compute (Trapped)", temp: tsvMetrics.bottomTierTempC, color: (tsvMetrics.bottomTierTempC > 85 ? "#ef4444" : "#f97316") }
    ];

    tiers.forEach((t, i) => {
      let y = startY + i * (tierH + gap);
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = t.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(startX, y, tierW, tierH, 6);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 12px 'JetBrains Mono', monospace";
      ctx.textAlign = "left";
      ctx.fillText(t.name, startX + 16, y + 30);

      ctx.fillStyle = t.color;
      ctx.font = "bold 13px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(t.temp.toFixed(1) + "°C", startX + tierW - 16, y + 30);

      // Draw Vertical TSVs connecting tiers
      if (i < 3) {
        ctx.strokeStyle = hasDummyTsvs ? "#eab308" : "#64748b";
        ctx.lineWidth = 4;
        for (let vx = startX + 60; vx < startX + tierW; vx += 50) {
          ctx.beginPath();
          ctx.moveTo(vx, y + tierH);
          ctx.lineTo(vx, y + tierH + gap);
          ctx.stroke();
        }
      }
    });
  }

  // Window Dispatch Interface
  window.updateTsvWorkbench = function () {
    computeTsvPhysics();
    render();
  };

  window.switchTsvView = function (v) {
    activeView = v;
    document.getElementById("btnTsvStress").className = (v === "stress") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnTsvParasitics").className = (v === "parasitics") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnTsvStack").className = (v === "stack_profile") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.toggleDummyTsvs = function () {
    hasDummyTsvs = !hasDummyTsvs;
    computeTsvPhysics();
    render();
  };

  window.exportTsvReport = function () {
    let rpt = [
      "* ===========================================================================",
      "* 3D THROUGH-SILICON VIA (TSV) HIGH-FREQUENCY SPICE SUBCIRCUIT DECK",
      "* Modeled Radius: " + tsvMetrics.radiusUm + " µm | Height: " + tsvMetrics.heightUm + " µm",
      "* ===========================================================================",
      ".subckt TSV_PAIR in_top in_bot",
      "  R_core in_top n_mid " + tsvMetrics.rOhm.toFixed(5),
      "  L_loop n_mid in_bot " + (tsvMetrics.lPh * 1e-12).toExponential(3),
      "  C_ox1 in_top 0 " + ((tsvMetrics.cFf * 0.5) * 1e-15).toExponential(3),
      "  C_ox2 in_bot 0 " + ((tsvMetrics.cFf * 0.5) * 1e-15).toExponential(3),
      ".ends TSV_PAIR",
      "",
      "* THERMO-MECHANICAL KEEP-OUT ZONE (KOZ) SPECIFICATION",
      "* Peak Von Mises Stress : " + tsvMetrics.peakStressMpa.toFixed(1) + " MPa",
      "* Transistor KOZ Radius : " + tsvMetrics.kozRadiusUm.toFixed(2) + " µm (|Δµ/µ| < 5%)",
      "* Total Exclusion Area  : " + tsvMetrics.kozAreaUm2.toFixed(1) + " µm² per TSV"
    ];
    document.getElementById("tsvExportText").textContent = rpt.join("\n");
    document.getElementById("tsvExportWrap").style.display = "block";
  };

  // Initial Boot
  computeTsvPhysics();
  render();
})();
</script>
