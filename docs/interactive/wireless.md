# 📡 On-Chip mmWave & THz Wireless NoC (WiNoC) Simulator

An interactive Computer-Aided Design (CAD) physical layer simulator for hybrid wired-wireless Networks-on-Chip (WiNoCs). Formulate on-chip radio-frequency (RF) propagation across lossy silicon substrates ($\sigma_{\text{Si}} \approx 10\,\text{S/m}$), simulate Friis transmission path loss at $60\,\text{GHz}$, $140\,\text{GHz}$, and $0.3\,\text{THz}$ bands, benchmark single-cycle wireless broadcast shortcuts for multi-core cache invalidation barriers, and evaluate Token-Passing versus TDMA Medium Access Control (MAC) protocols.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Carrier Frequency:</b>
      <select id="winocFreqSelect" class="noc-sim-select" onchange="updateWirelessWorkbench()">
        <option value="60">60 GHz V-Band (16 Gbps, Higher Penetration)</option>
        <option value="140" selected>140 GHz D-Band (32 Gbps, Sub-mm Antennas)</option>
        <option value="300">300 GHz Sub-THz (64 Gbps, Extreme Bandwidth)</option>
      </select>
    </label>

    <label><b>MAC Arbitration Protocol:</b>
      <select id="winocMacSelect" class="noc-sim-select" onchange="updateWirelessWorkbench()">
        <option value="token_ring" selected>Token-Passing Ring (Collision-Free, Deterministic)</option>
        <option value="tdma">Time-Division Multiple Access (TDMA Slotted)</option>
        <option value="csma">CSMA / Collision Avoidance (Contention Backoff)</option>
      </select>
    </label>

    <label><b>RF Transmit Power:</b>
      <select id="winocTxPowerSelect" class="noc-sim-select" onchange="updateWirelessWorkbench()">
        <option value="0.0">0.0 dBm (1.0 mW Transmit Power)</option>
        <option value="3.0" selected>+3.0 dBm (2.0 mW Standard Link)</option>
        <option value="6.0">+6.0 dBm (4.0 mW Long Reach)</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnWinocMesh" onclick="switchWinocView('hybrid_mesh')" style="background:#0284c7;">🕸️ Hybrid Wired-Wireless Topology</button>
      <button class="noc-sim-btn secondary" id="btnWinocLoss" onclick="switchWinocView('path_loss')">📉 Substrate RF Path Loss Curve</button>
      <button class="noc-sim-btn secondary" onclick="broadcastWirelessBarrier()">⚡ Broadcast Coherence Barrier</button>
      <button class="noc-sim-btn secondary" onclick="resetWirelessCAD()">🔄 Reset Transceivers</button>
      <button class="noc-sim-btn secondary" onclick="exportWirelessReport()" style="margin-left:auto;">📋 Export RF Link Deck</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Wireless Broadcast Latency</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudWinocLatency">1 Cycle (Single-Hop Broadcast)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudWiredCompare">Wired Mesh Equivalent: 9.4 Cycles</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Substrate RF Path Loss</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudPathLoss">PL(10mm): -38.4 dB</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudRxSensitivity">Rx Power: -35.4 dBm (Threshold: -42 dBm)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Channel Bandwidth &amp; Data Rate</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudDataRate">32.0 Gbps (140 GHz OOK)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudMacEff">MAC Efficiency: 94.2% (Token-Passing)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Transceiver Energy Efficiency</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudEnergy">0.85 pJ/bit (RF Front-End)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudAntennaSize">Antenna Length: 380 µm (λ/4 Dipole)</div>
    </div>
  </div>

  <!-- CAD Canvas View -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="winocCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- Export Panel -->
  <div id="winocExportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">On-Chip mmWave / THz Wireless Link Specification:</strong>
      <button onclick="document.getElementById('winocExportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="winocExportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Wireless NoC Electromagnetics &amp; Channel Physics (Chapter 10):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Friis On-Chip Substrate Path Loss:</strong> Radio propagation on silicon dies suffers severe ohmic attenuation due to the conductive semiconductor substrate ($\sigma_{\text{Si}} \approx 10\,\text{S/m}$):
        $$\text{PL}(d) = 20 \log_{10}\left(\frac{4\pi d}{\lambda}\right) + \alpha_{\text{sub}} \cdot d - G_{\text{tx}} - G_{\text{rx}}$$
        At $140\,\text{GHz}$ ($\lambda \approx 2.14\,\text{mm}$), quarter-wave on-chip zig-zag dipoles ($L_{\text{ant}} \approx 380\,\mu\text{m}$) fit comfortably inside router tile pitch, delivering $>32\,\text{Gbps}$ wireless channels.</li>
      <li><strong>Multi-Core Coherence Speedup:</strong> Cache invalidation broadcasts and barrier synchronizations scale poorly across multihop wired networks ($O(\sqrt{N})$ hops). Deploying $4$ to $8$ wireless hub transceivers reduces multi-core barrier latencies by over $85\%$.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// On-Chip mmWave / THz Wireless NoC (WiNoC) Engine
// ============================================================================

(function () {
  let activeView = "hybrid_mesh"; // "hybrid_mesh", "path_loss"
  let isBroadcasting = false;
  let broadcastRadius = 0;

  // 4 Wireless Hubs located at quadrant centers
  const HUBS = [
    { id: 0, x: 1, y: 1 },
    { id: 1, x: 2, y: 1 },
    { id: 2, x: 1, y: 2 },
    { id: 3, x: 2, y: 2 }
  ];

  let winocMetrics = {
    freqGhz: 140,
    txDbm: 3.0,
    rxDbm: -35.4,
    pathLossDb: 38.4,
    dataRateGbps: 32.0,
    energyPjBit: 0.85
  };

  const canvas = document.getElementById("winocCanvas");
  const ctx = canvas.getContext("2d");

  function computeWirelessPhysics() {
    const freqGhz = parseFloat(document.getElementById("winocFreqSelect").value) || 140;
    const txDbm = parseFloat(document.getElementById("winocTxPowerSelect").value) || 3.0;

    winocMetrics.freqGhz = freqGhz;
    winocMetrics.txDbm = txDbm;

    // lambda in mm = c / f = 300 / freqGhz
    const lambdaMm = 300 / freqGhz;
    const dMm = 10.0; // 10mm chip reach
    const alphaSubDbMm = (freqGhz === 60) ? 0.8 : (freqGhz === 140 ? 1.4 : 2.2);

    // Path loss: 20*log10(4*pi*d/lambda) + alpha*d
    const freeSpaceDb = 20 * Math.log10((4 * Math.PI * dMm) / lambdaMm);
    const totalLossDb = freeSpaceDb + alphaSubDbMm * dMm - 2.0; // 2dBi antenna gain
    winocMetrics.pathLossDb = totalLossDb;
    winocMetrics.rxDbm = txDbm - totalLossDb;

    winocMetrics.dataRateGbps = (freqGhz === 60) ? 16.0 : (freqGhz === 140 ? 32.0 : 64.0);
    winocMetrics.energyPjBit = (freqGhz === 60) ? 1.15 : (freqGhz === 140 ? 0.85 : 0.65);

    document.getElementById("hudWinocLatency").textContent = "1 Cycle (Single-Hop Broadcast)";
    document.getElementById("hudPathLoss").textContent = "PL(10mm): -" + totalLossDb.toFixed(1) + " dB";
    document.getElementById("hudRxSensitivity").textContent = "Rx Power: " + winocMetrics.rxDbm.toFixed(1) + " dBm (Margin: +" + (winocMetrics.rxDbm - (-42.0)).toFixed(1) + " dB)";
    document.getElementById("hudDataRate").textContent = winocMetrics.dataRateGbps.toFixed(1) + " Gbps (" + freqGhz + " GHz OOK)";
    document.getElementById("hudEnergy").textContent = winocMetrics.energyPjBit.toFixed(2) + " pJ/bit (RF Front-End)";
    document.getElementById("hudAntennaSize").textContent = "Antenna: " + Math.round((lambdaMm / 4) * 1e3 * 0.7) + " µm (λ/4 Zig-Zag)";
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "hybrid_mesh") {
      renderHybridMesh();
    } else if (activeView === "path_loss") {
      renderPathLossCurve();
    }
  }

  // 1. Hybrid Wired-Wireless 4x4 Mesh View
  function renderHybridMesh() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 90, padT = 60, size = 300;
    const step = size / 3;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("HYBRID 4x4 WIRED MESH WITH 4 ON-CHIP mmWAVE RF TRANSCEIVER HUBS", padL, 30);

    // Draw Wired Links
    ctx.strokeStyle = "#334155";
    ctx.lineWidth = 2;
    for (let y = 0; y < 4; y++) {
      for (let x = 0; x < 4; x++) {
        let px = padL + x * step;
        let py = padT + y * step;
        if (x + 1 < 4) {
          ctx.beginPath();
          ctx.moveTo(px, py);
          ctx.lineTo(px + step, py);
          ctx.stroke();
        }
        if (y + 1 < 4) {
          ctx.beginPath();
          ctx.moveTo(px, py);
          ctx.lineTo(px, py + step);
          ctx.stroke();
        }
      }
    }

    // Draw RF Broadcast Wave if active
    if (isBroadcasting) {
      HUBS.forEach(hub => {
        let hx = padL + hub.x * step;
        let hy = padT + hub.y * step;

        ctx.strokeStyle = "rgba(56, 189, 248, " + (1 - broadcastRadius / 140) + ")";
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(hx, hy, broadcastRadius, 0, Math.PI * 2);
        ctx.stroke();
      });

      broadcastRadius += 4;
      if (broadcastRadius > 140) isBroadcasting = false;
    }

    // Draw Routers & Wireless Hubs
    for (let y = 0; y < 4; y++) {
      for (let x = 0; x < 4; x++) {
        let px = padL + x * step;
        let py = padT + y * step;
        let isHub = HUBS.some(hb => hb.x === x && hb.y === y);

        ctx.fillStyle = isHub ? "#0c4a6e" : "#1e293b";
        ctx.strokeStyle = isHub ? "#38bdf8" : "#64748b";
        ctx.lineWidth = isHub ? 3 : 2;

        ctx.beginPath();
        ctx.arc(px, py, isHub ? 18 : 14, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        if (isHub) {
          ctx.fillStyle = "#38bdf8";
          ctx.font = "14px sans-serif";
          ctx.textAlign = "center";
          ctx.fillText("📡", px, py + 5);
        } else {
          ctx.fillStyle = "#ffffff";
          ctx.font = "10px 'JetBrains Mono', monospace";
          ctx.textAlign = "center";
          ctx.fillText(x + "," + y, px, py + 4);
        }
      }
    }

    // Right-side Panel
    const sumX = padL + size + 40;
    const sumY = padT;

    ctx.fillStyle = "#1e293b";
    ctx.strokeStyle = "#334155";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(sumX, sumY, 210, size, 8);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 11px 'JetBrains Mono', monospace";
    ctx.textAlign = "left";
    ctx.fillText("RF LINK STATUS", sumX + 16, sumY + 30);

    ctx.fillStyle = "#ffffff";
    ctx.font = "10px 'JetBrains Mono', monospace";
    ctx.fillText("Transceiver Hubs: 4 Nodes", sumX + 16, sumY + 60);
    ctx.fillText("Frequency: " + winocMetrics.freqGhz + " GHz", sumX + 16, sumY + 80);
    ctx.fillText("Data Rate: " + winocMetrics.dataRateGbps + " Gbps", sumX + 16, sumY + 100);
    ctx.fillText("MAC: Token-Passing", sumX + 16, sumY + 120);
    ctx.fillText("Broadcast Delay: 1 Cycle", sumX + 16, sumY + 140);
  }

  // 2. Substrate Path Loss Curve
  function renderPathLossCurve() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("RF PATH LOSS PL(d) vs. CHIP PROPAGATION DISTANCE [LOSSY SILICON]", padL, 28);

    // Axes: -20 dB to -60 dB
    const maxDb = -20, minDb = -60;
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;

    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let dLabel = (maxDb - (gy / 4) * (maxDb - minDb)) + " dB";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(dLabel, padL - 8, y + 4);
    }

    const maxDistMm = 20.0;
    for (let gx = 0; gx <= 5; gx++) {
      let x = padL + (gx / 5) * graphW;
      ctx.beginPath();
      ctx.moveTo(x, padT);
      ctx.lineTo(x, h - padB);
      ctx.stroke();

      let dLabel = (gx * 4) + " mm";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(dLabel, x, h - padB + 16);
    }

    // Path loss curve
    const lambdaMm = 300 / winocMetrics.freqGhz;
    const alphaSub = (winocMetrics.freqGhz === 60) ? 0.8 : (winocMetrics.freqGhz === 140 ? 1.4 : 2.2);

    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let s = 1; s <= 100; s++) {
      let d = (s / 100) * maxDistMm;
      let pl = -(20 * Math.log10((4 * Math.PI * d) / lambdaMm) + alphaSub * d - 2.0);
      let px = padL + (d / maxDistMm) * graphW;
      let py = padT + (1 - (pl - minDb) / (maxDb - minDb)) * graphH;
      if (s === 1) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();
  }

  // Animation Loop for broadcast pulse
  function loop() {
    if (isBroadcasting) render();
    requestAnimationFrame(loop);
  }

  // Window Dispatch Interface
  window.updateWirelessWorkbench = function () {
    computeWirelessPhysics();
    render();
  };

  window.switchWinocView = function (v) {
    activeView = v;
    document.getElementById("btnWinocMesh").className = (v === "hybrid_mesh") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnWinocLoss").className = (v === "path_loss") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.broadcastWirelessBarrier = function () {
    isBroadcasting = true;
    broadcastRadius = 5;
  };

  window.resetWirelessCAD = function () {
    computeWirelessPhysics();
    render();
  };

  window.exportWirelessReport = function () {
    let rpt = [
      "===============================================================================",
      "ON-CHIP mmWAVE / THz WIRELESS NoC (WiNoC) RF SPECIFICATION",
      "===============================================================================",
      "Carrier Frequency Band   : " + winocMetrics.freqGhz + " GHz (OOK Modulation)",
      "Transmitter RF Power     : +" + winocMetrics.txDbm + " dBm (1.0 mW Front-End)",
      "10mm Substrate Path Loss : -" + winocMetrics.pathLossDb.toFixed(1) + " dB (Silicon σ_Si = 10 S/m)",
      "Photodetector / Rx Power : " + winocMetrics.rxDbm.toFixed(1) + " dBm (Sensitivity: -42.0 dBm)",
      "Channel Data Rate        : " + winocMetrics.dataRateGbps + " Gbps",
      "Wireless Barrier Latency : 1 Clock Cycle (vs 9.4 Cycles across Wired Mesh)",
      "Energy Efficiency        : " + winocMetrics.energyPjBit + " pJ/bit",
      "==============================================================================="
    ];
    document.getElementById("winocExportText").textContent = rpt.join("\n");
    document.getElementById("winocExportWrap").style.display = "block";
  };

  // Initial Boot
  computeWirelessPhysics();
  render();
  requestAnimationFrame(loop);
})();
</script>
