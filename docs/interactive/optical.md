# 💡 Silicon Photonic & Optical NoC (ONoC) Waveguide CAD Simulator

An interactive Computer-Aided Design (CAD) physical layer simulator for Silicon Photonic Networks-on-Chip (ONoCs). Model continuous-wave (CW) laser source power budgets, Micro-Ring Resonator (MRR) Lorentzian transmission spectra, thermo-optic resonance wavelength drift ($\frac{d\lambda}{dT} \approx 0.1\,\text{nm/K}$), Wavelength Division Multiplexing (WDM) inter-channel optical crosstalk noise, and photodetector Bit Error Rates (BER).

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Laser Pump Power:</b>
      <select id="optLaserSelect" class="noc-sim-select" onchange="updateOpticalWorkbench()">
        <option value="5.0">5.0 mW (Low Power / +7 dBm)</option>
        <option value="10.0" selected>10.0 mW (Standard Industrial / +10 dBm)</option>
        <option value="20.0">20.0 mW (High-Radix Photonic Crossbar / +13 dBm)</option>
      </select>
    </label>

    <label><b>Thermal Gradient (ΔT):</b>
      <input type="range" id="optTempSlider" min="0" max="50" step="5" value="20" style="width:100px; vertical-align:middle;" oninput="document.getElementById('optTempVal').textContent = '+' + this.value + '°C Drift'; updateOpticalWorkbench();">
      <span id="optTempVal" style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#f87171;">+20°C Drift</span>
    </label>

    <label><b>MRR Thermal Tuning:</b>
      <select id="optTuningSelect" class="noc-sim-select" onchange="updateOpticalWorkbench()">
        <option value="active_heater" selected>Closed-Loop Micro-Heater (Re-align Resonance)</option>
        <option value="untuned">Untuned Drift (Thermal Misalignment Loss)</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnOptSpectrum" onclick="switchOptView('spectrum')" style="background:#0284c7;">🌈 WDM Lorentzian Spectrum</button>
      <button class="noc-sim-btn secondary" id="btnOptBudget" onclick="switchOptView('power_budget')">📉 Link Budget Loss Waterfall</button>
      <button class="noc-sim-btn secondary" onclick="stepOpticalSweep()">⏭ Sweep Wavelengths</button>
      <button class="noc-sim-btn secondary" onclick="resetOpticalCAD()">🔄 Reset Laser Calibration</button>
      <button class="noc-sim-btn secondary" onclick="exportOpticalReport()" style="margin-left:auto;">📋 Export Photonic Deck</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Photodetector Received Power</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudRxPower">-14.2 dBm (Safe Margin)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudMargin">Sensitivity: -18.0 dBm (+3.8 dB Margin)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">MRR Thermo-Optic Drift</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudDrift">Δλ = +2.00 nm (Tuned)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudHeaterPwr">Micro-Heater Power: 4.8 mW</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Signal-to-Noise Ratio &amp; BER</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudBer">BER: &lt; 10⁻¹² (Error-Free)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudSnr">Optical SNR: 21.4 dB (Low Crosstalk)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Energy per Transmitted Bit</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudEnergy">0.42 pJ/bit (10 Gbps)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudLaserEff">Laser Wall-Plug Eff: 15.0%</div>
    </div>
  </div>

  <!-- CAD Canvas View -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="opticalCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- Export Panel -->
  <div id="optExportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">Optical NoC Waveguide Link Budget &amp; SPICE Deck:</strong>
      <button onclick="document.getElementById('optExportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="optExportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Nanophotonic Physics &amp; MRR Waveguide Theory (Chapter 10):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Micro-Ring Resonator (MRR) Lorentzian Response:</strong> An optical ring of radius $R$ and effective refractive index $n_{\text{eff}}$ exhibits sharp resonant transmission dips at wavelengths satisfying the constructive interference condition $m \lambda_0 = 2\pi R n_{\text{eff}}$:
        $$T(\lambda) = \frac{(\text{FWHM} / 2)^2}{(\lambda - \lambda_0)^2 + (\text{FWHM} / 2)^2}$$
        Full-Width at Half-Maximum ($\text{FWHM} \approx 0.15\,\text{nm}$) provides high quality factors ($Q \ge 10^4$), permitting dense 8-channel Wavelength Division Multiplexing (WDM).</li>
      <li><strong>Thermo-Optic Redshift Drift:</strong> Silicon possesses an extraordinarily strong positive thermo-optic coefficient ($\frac{dn_{Si}}{dT} \approx 1.86 \times 10^{-4}/\text{K}$), causing resonant peaks to drift toward longer wavelengths at a rate of $\frac{d\lambda}{dT} \approx 0.1\,\text{nm/}^\circ\text{C}$. A $20^\circ\text{C}$ on-chip hotspot shifts the resonance by $2.0\,\text{nm}$—completely detuning the optical channel unless integrated micro-heaters supply thermal compensation.</li>
      <li><strong>Optical Power Budget &amp; Insertion Loss:</strong> Received photodetector optical power $P_{\text{rx}}$ must remain above the Germanium APD sensitivity threshold ($P_{\text{sens}} \approx -18\,\text{dBm}$) to sustain $\text{BER} \le 10^{-12}$:
        $$P_{\text{rx}} = P_{\text{laser}} - \left( L_{\text{couple}} + L_{\text{mod}} + \alpha_{\text{wg}} \cdot L_{\text{prop}} + N_{\text{drop}} \cdot L_{\text{thru}} + L_{\text{drop}} \right)$$</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// Silicon Photonic & Optical NoC (ONoC) Waveguide CAD Engine
// ============================================================================

(function () {
  let activeView = "spectrum"; // "spectrum", "power_budget"

  const WDM_CHANNELS = [
    { id: 1, lambda0: 1548.0, color: "#38bdf8" },
    { id: 2, lambda0: 1549.6, color: "#34d399" },
    { id: 3, lambda0: 1551.2, color: "#eab308" },
    { id: 4, lambda0: 1552.8, color: "#f87171" }
  ];

  let optMetrics = {
    laserDbm: 10.0,
    rxDbm: -14.2,
    marginDb: 3.8,
    driftNm: 2.0,
    heaterPwrMw: 4.8,
    berExp: -12,
    snrDb: 21.4,
    energyPjBit: 0.42
  };

  const canvas = document.getElementById("opticalCanvas");
  const ctx = canvas.getContext("2d");

  function computeOpticalPhysics() {
    const laserMw = parseFloat(document.getElementById("optLaserSelect").value) || 10.0;
    const laserDbm = 10 * Math.log10(laserMw);
    optMetrics.laserDbm = laserDbm;

    const deltaT = parseFloat(document.getElementById("optTempSlider").value) || 20.0;
    const tuningMode = document.getElementById("optTuningSelect").value;

    // dLambda / dT = 0.1 nm/°C
    const driftRaw = deltaT * 0.10;
    optMetrics.driftNm = driftRaw;

    // Cumulative losses: Coupler (1.5dB) + Modulator (2.5dB) + Waveguide 2cm (3.0dB) + Drop MRR (1.2dB) + Detector (0.5dB) = 8.7 dB
    let nominalLossDb = 8.7;
    let detuningLossDb = 0;

    if (tuningMode === "active_heater") {
      // Micro-heater burns 2.4 mW per nm of tuning
      optMetrics.heaterPwrMw = driftRaw * 2.4;
      detuningLossDb = 0.4; // residual tuning imperfection
    } else {
      optMetrics.heaterPwrMw = 0;
      // Severe detuning loss: Lorentzian drop off-resonance
      detuningLossDb = Math.min(22.0, Math.pow(driftRaw / 0.15, 2) * 2.5);
    }

    const rxDbm = laserDbm - (nominalLossDb + detuningLossDb);
    optMetrics.rxDbm = rxDbm;
    optMetrics.marginDb = rxDbm - (-18.0);

    // SNR and BER
    if (optMetrics.marginDb > 0) {
      optMetrics.snrDb = 18.0 + optMetrics.marginDb * 0.9;
      optMetrics.berExp = -12;
    } else {
      optMetrics.snrDb = Math.max(4.0, 18.0 + optMetrics.marginDb * 2.2);
      optMetrics.berExp = Math.max(-2, Math.round(-12 - optMetrics.marginDb * 1.5));
    }

    optMetrics.energyPjBit = (laserMw * 1e-3 + optMetrics.heaterPwrMw * 1e-3) / 10e9 * 1e12; // at 10 Gbps

    updateHUD();
  }

  function updateHUD() {
    document.getElementById("hudRxPower").textContent = optMetrics.rxDbm.toFixed(1) + " dBm (" + (optMetrics.marginDb >= 0 ? "Safe Margin" : "BELOW SENSITIVITY") + ")";
    document.getElementById("hudMargin").textContent = "Sensitivity: -18.0 dBm (" + (optMetrics.marginDb >= 0 ? "+" : "") + optMetrics.marginDb.toFixed(1) + " dB Margin)";
    document.getElementById("hudDrift").textContent = "Δλ = +" + optMetrics.driftNm.toFixed(2) + " nm (" + (optMetrics.heaterPwrMw > 0 ? "Tuned" : "Untuned") + ")";
    document.getElementById("hudHeaterPwr").textContent = "Micro-Heater: " + optMetrics.heaterPwrMw.toFixed(1) + " mW Power";
    document.getElementById("hudBer").textContent = "BER: " + (optMetrics.berExp <= -12 ? "< 10⁻¹² (Error-Free)" : "10^(" + optMetrics.berExp + ") UNRELIABLE");
    document.getElementById("hudSnr").textContent = "Optical SNR: " + optMetrics.snrDb.toFixed(1) + " dB";
    document.getElementById("hudEnergy").textContent = optMetrics.energyPjBit.toFixed(2) + " pJ/bit (10 Gbps)";
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "spectrum") {
      renderSpectrumView();
    } else if (activeView === "power_budget") {
      renderPowerBudgetView();
    }
  }

  // 1. WDM Lorentzian Spectrum View
  function renderSpectrumView() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("WDM OPTICAL TRANSMISSION SPECTRUM T(λ) • LORENTZIAN RESONANCE PROFILES", padL, 28);

    const minLambda = 1546.0;
    const maxLambda = 1555.0;
    const fwhm = 0.18; // nm

    // Axes
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let tLabel = (1.0 - gy / 4).toFixed(2);
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(tLabel, padL - 8, y + 4);
    }

    for (let gx = 0; gx <= 9; gx++) {
      let x = padL + (gx / 9) * graphW;
      ctx.beginPath();
      ctx.moveTo(x, padT);
      ctx.lineTo(x, h - padB);
      ctx.stroke();

      let lLabel = (minLambda + gx * 1.0).toFixed(0) + " nm";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(lLabel, x, h - padB + 16);
    }

    const tuningMode = document.getElementById("optTuningSelect").value;
    const activeDrift = (tuningMode === "active_heater") ? 0.0 : optMetrics.driftNm;

    // Draw Lorentzian peaks for each WDM channel
    WDM_CHANNELS.forEach(ch => {
      let center = ch.lambda0 + activeDrift;
      ctx.strokeStyle = ch.color;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (let s = 0; s <= 200; s++) {
        let lam = minLambda + (s / 200) * (maxLambda - minLambda);
        let transmission = 1.0 - (Math.pow(fwhm / 2, 2) / (Math.pow(lam - center, 2) + Math.pow(fwhm / 2, 2)));
        let px = padL + ((lam - minLambda) / (maxLambda - minLambda)) * graphW;
        let py = padT + (1 - transmission) * graphH;
        if (s === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();
    });

    // Legend
    ctx.textAlign = "left";
    ctx.font = "11px 'JetBrains Mono', monospace";
    WDM_CHANNELS.forEach((ch, idx) => {
      ctx.fillStyle = ch.color;
      ctx.fillRect(w - 240, padT + 10 + idx * 18, 12, 12);
      ctx.fillStyle = "#ffffff";
      ctx.fillText("Channel " + ch.id + " (" + ch.lambda0.toFixed(1) + " nm)", w - 220, padT + 20 + idx * 18);
    });
  }

  // 2. Optical Power Budget Waterfall View
  function renderPowerBudgetView() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("OPTICAL LINK BUDGET WATERFALL [LASER SOURCE -> DETECTOR ATTENUATION]", padL, 28);

    const stages = [
      { name: "Laser Launch", pDbm: optMetrics.laserDbm, color: "#eab308" },
      { name: "Grating Coupler", pDbm: optMetrics.laserDbm - 1.5, color: "#38bdf8" },
      { name: "MRR Modulator", pDbm: optMetrics.laserDbm - 4.0, color: "#38bdf8" },
      { name: "Si3N4 Waveguide", pDbm: optMetrics.laserDbm - 7.0, color: "#38bdf8" },
      { name: "MRR Drop Filter", pDbm: optMetrics.rxDbm + 0.5, color: "#38bdf8" },
      { name: "Rx Photodetector", pDbm: optMetrics.rxDbm, color: (optMetrics.rxDbm >= -18.0 ? "#22c55e" : "#ef4444") }
    ];

    // Y-Axis: +15 dBm to -25 dBm
    const maxDb = 15, minDb = -25;
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;

    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let dLabel = (maxDb - (gy / 4) * (maxDb - minDb)) + " dBm";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(dLabel, padL - 8, y + 4);
    }

    // -18 dBm Sensitivity threshold line
    let ySens = padT + (1 - (-18.0 - minDb) / (maxDb - minDb)) * graphH;
    ctx.strokeStyle = "#ef4444";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(padL, ySens);
    ctx.lineTo(w - padR, ySens);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = "#ef4444";
    ctx.textAlign = "left";
    ctx.fillText("Detector Sensitivity Limit (-18.0 dBm)", padL + 10, ySens - 6);

    // Bars
    const barW = graphW / stages.length - 20;
    stages.forEach((stg, idx) => {
      let x = padL + idx * (graphW / stages.length) + 10;
      let yVal = padT + (1 - (stg.pDbm - minDb) / (maxDb - minDb)) * graphH;
      let barH = padT + graphH - yVal;

      ctx.fillStyle = stg.color;
      ctx.fillRect(x, yVal, barW, barH);
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 1;
      ctx.strokeRect(x, yVal, barW, barH);

      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(stg.pDbm.toFixed(1) + " dBm", x + barW / 2, yVal - 6);

      ctx.fillStyle = "#94a3b8";
      ctx.font = "9px 'JetBrains Mono', monospace";
      ctx.fillText(stg.name.split(" ")[0], x + barW / 2, h - padB + 16);
      ctx.fillText(stg.name.split(" ")[1] || "", x + barW / 2, h - padB + 28);
    });
  }

  // Window Dispatch Interface
  window.updateOpticalWorkbench = function () {
    computeOpticalPhysics();
    render();
  };

  window.switchOptView = function (v) {
    activeView = v;
    document.getElementById("btnOptSpectrum").className = (v === "spectrum") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnOptBudget").className = (v === "power_budget") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.stepOpticalSweep = function () {
    let cur = parseFloat(document.getElementById("optTempSlider").value);
    document.getElementById("optTempSlider").value = (cur + 5) % 55;
    document.getElementById("optTempVal").textContent = "+" + document.getElementById("optTempSlider").value + "°C Drift";
    computeOpticalPhysics();
    render();
  };

  window.resetOpticalCAD = function () {
    document.getElementById("optTempSlider").value = 20;
    document.getElementById("optTempVal").textContent = "+20°C Drift";
    computeOpticalPhysics();
    render();
  };

  window.exportOpticalReport = function () {
    let rpt = [
      "===============================================================================",
      "SILICON PHOTONIC & OPTICAL NoC (ONoC) LINK BUDGET REPORT",
      "===============================================================================",
      "Laser Launch Power       : " + optMetrics.laserDbm.toFixed(1) + " dBm (" + document.getElementById("optLaserSelect").value + " mW)",
      "Photodetector Rx Power   : " + optMetrics.rxDbm.toFixed(1) + " dBm (Margin: " + optMetrics.marginDb.toFixed(1) + " dB)",
      "Thermo-Optic Drift       : Δλ = +" + optMetrics.driftNm.toFixed(2) + " nm (Temp Gradient: " + document.getElementById("optTempSlider").value + " °C)",
      "Tuning Heater Overhead   : " + optMetrics.heaterPwrMw.toFixed(1) + " mW (Closed-loop micro-heater)",
      "Bit Error Rate (BER)     : " + (optMetrics.berExp <= -12 ? "< 10^-12 (Error-Free)" : "10^(" + optMetrics.berExp + ")"),
      "Optical SNR              : " + optMetrics.snrDb.toFixed(1) + " dB",
      "Transmitter Energy/Bit   : " + optMetrics.energyPjBit.toFixed(2) + " pJ/bit at 10 Gbps",
      "==============================================================================="
    ];
    document.getElementById("optExportText").textContent = rpt.join("\n");
    document.getElementById("optExportWrap").style.display = "block";
  };

  // Initial Boot
  computeOpticalPhysics();
  render();
})();
</script>
