# 🛡️ NoC Hardware Security & Threat Defense CAD Workbench

An interactive Computer-Aided Design (CAD) and hardware security verification workbench for Networks-on-Chip (NoCs). Model real silicon threat vectors—including Denial-of-Service (DoS) buffer-flooding attacks, cache timing covert side-channels targeting AES cryptographic keys, and malicious Hardware Trojans—and benchmark architectural defense mechanisms including entropy-based anomaly filters, Physical Unclonable Function (PUF) packet authentication, and timing jitter scramblers.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Active Threat Model:</b>
      <select id="secThreatSelect" class="noc-sim-select" onchange="updateSecurityWorkbench()">
        <option value="dos_flood" selected>DoS Buffer-Flooding (Congestion Tree Entrapment)</option>
        <option value="covert_timing">Timing Side-Channel (Covert Key Leakage via Jitter)</option>
        <option value="trojan_payload">Hardware Trojan (Malicious Data Modification)</option>
      </select>
    </label>

    <label><b>Silicon Defense Shield:</b>
      <select id="secDefenseSelect" class="noc-sim-select" onchange="updateSecurityWorkbench()">
        <option value="entropy_filter" selected>Online Entropy Anomaly Detector &amp; Quarantine</option>
        <option value="timing_scrambler">Random Delay Injection (Side-Channel Scrambler)</option>
        <option value="puf_auth">PUF Authenticated Packet Tags (Anti-Spoofing)</option>
        <option value="none">Unprotected Baseline (Vulnerable to Exploitation)</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnSecMesh" onclick="switchSecView('mesh_grid')" style="background:#0284c7;">🕸️ 4x4 Threat Defense Topology</button>
      <button class="noc-sim-btn secondary" id="btnSecEntropy" onclick="switchSecView('entropy_plot')">📊 Shannon Entropy &amp; Anomaly Detection</button>
      <button class="noc-sim-btn secondary" onclick="triggerMaliciousAttack()">⚡ Trigger Attack Scenario</button>
      <button class="noc-sim-btn secondary" onclick="resetSecurityCAD()">🔄 Reset Security Monitors</button>
      <button class="noc-sim-btn secondary" onclick="exportSecurityReport()" style="margin-left:auto;">📋 Export Security Audit</button>
    </div>
  </div>

  <!-- Physical Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Threat Detection &amp; Isolation</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudDefenseStatus">THREAT INTERCEPTED (Core 5 Quarantined)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudInterceptionCycles">Isolation Time: 14 Cycles | 0 False Alarms</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Traffic Shannon Entropy H(X)</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudEntropy">H = 1.24 bits (Anomaly Spike)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudBaselineEntropy">Nominal Entropy: 3.85 bits (Random Uniform)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Side-Channel Information Leakage</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudLeakage">Mutual Info: 0.02 bits / cycle</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudScramblerEffect">Timing Jitter: 98.5% Scrambled</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">PUF Authentication Security</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudPufStatus">128-Bit MAC Verification: VALID</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudLatencyOverhead">Hardware Overhead: +1 Cycle / +2.4% Area</div>
    </div>
  </div>

  <!-- CAD Canvas View -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="secCanvas" width="700" height="420" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b;"></canvas>
  </div>

  <!-- Export Panel -->
  <div id="secExportWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">Hardware Security Verification &amp; Threat Audit Log:</strong>
      <button onclick="document.getElementById('secExportWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="secExportText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Hardware Security Threat Modeling &amp; Information Theory (Chapter 11):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Shannon Entropy Anomaly Detection:</strong> In a healthy multi-core SoC, packet destination distributions exhibit high entropy. When an adversarial core initiates a DoS buffer-flooding attack targeting a shared memory controller, the spatial distribution collapses to an anomalous low-entropy state:
        $$H(X) = - \sum_{i=1}^N p(x_i) \log_2 p(x_i)$$
        Online hardware entropy monitors detect sudden drops ($\Delta H > 2.0\,\text{bits}$), instantly severing the attacker's egress link credits to isolate the threat.</li>
      <li><strong>Timing Covert Channels:</strong> Malicious untrusted third-party IP cores transmit confidential data to colluding receiver cores by modulating the inter-packet departure intervals $\Delta t$. Introducing randomized pseudo-random dummy delays reduces mutual information $\mathcal{I}(X; Y) \rightarrow 0$, closing the covert channel.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// NoC Hardware Security & Threat Defense CAD Engine
// ============================================================================

(function () {
  let activeView = "mesh_grid"; // "mesh_grid", "entropy_plot"
  let isUnderAttack = false;
  let attackCycle = 0;

  // 4x4 Core Grid
  const MESH_SIZE = 4;
  const TROJAN_NODE = { x: 1, y: 1 }; // Node 5
  let isQuarantined = false;

  let entropyHistory = [];

  let secMetrics = {
    entropy: 3.85,
    baselineEntropy: 3.85,
    mutualInfo: 0.02,
    detectionCycle: 0
  };

  const canvas = document.getElementById("secCanvas");
  const ctx = canvas.getContext("2d");

  function stepSecurityPhysics() {
    attackCycle++;
    const threat = document.getElementById("secThreatSelect").value;
    const defense = document.getElementById("secDefenseSelect").value;

    if (isUnderAttack) {
      if (defense === "entropy_filter") {
        secMetrics.entropy = Math.max(1.15, secMetrics.entropy - 0.25);
        if (secMetrics.entropy < 2.0 && !isQuarantined) {
          isQuarantined = true;
          secMetrics.detectionCycle = attackCycle;
        }
      } else if (defense === "timing_scrambler") {
        secMetrics.mutualInfo = 0.01;
      } else if (defense === "none") {
        secMetrics.entropy = 0.85; // extreme drop
        secMetrics.mutualInfo = 0.94; // key leaked!
      }
    } else {
      secMetrics.entropy = 3.85;
      secMetrics.mutualInfo = 0.02;
    }

    if (entropyHistory.length > 60) entropyHistory.shift();
    entropyHistory.push(secMetrics.entropy);

    updateHUD();
    render();
  }

  function updateHUD() {
    const defense = document.getElementById("secDefenseSelect").value;
    if (isUnderAttack) {
      if (defense === "entropy_filter") {
        document.getElementById("hudDefenseStatus").textContent = isQuarantined ? "THREAT QUARANTINED (Core (1,1) Isolated)" : "EVALUATING TRAFFIC ANOMALY...";
        document.getElementById("hudInterceptionCycles").textContent = isQuarantined ? "Isolated at Cycle " + secMetrics.detectionCycle + " | 0 False Alarms" : "Entropy drop detected";
      } else if (defense === "timing_scrambler") {
        document.getElementById("hudDefenseStatus").textContent = "TIMING JITTER OBFUSCATION ACTIVE";
        document.getElementById("hudInterceptionCycles").textContent = "Covert Rate: < 0.01 bps (Channel Cloaked)";
      } else {
        document.getElementById("hudDefenseStatus").textContent = "SYSTEM COMPROMISED (Attack Active)";
        document.getElementById("hudInterceptionCycles").textContent = "Unprotected: Buffer Saturated / Key Leaked";
      }
    } else {
      document.getElementById("hudDefenseStatus").textContent = "ALL MONITORS NOMINAL (Zero Threats)";
      document.getElementById("hudInterceptionCycles").textContent = "Hardware BIST: Clean | PUF Tags Valid";
    }

    document.getElementById("hudEntropy").textContent = "H = " + secMetrics.entropy.toFixed(2) + " bits (" + (secMetrics.entropy < 2.5 ? "ANOMALY SPIKE" : "Normal") + ")";
    document.getElementById("hudLeakage").textContent = "Mutual Info: " + secMetrics.mutualInfo.toFixed(2) + " bits / cycle";
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "mesh_grid") {
      renderMeshGrid();
    } else if (activeView === "entropy_plot") {
      renderEntropyPlot();
    }
  }

  // 1. 4x4 Threat Defense Mesh View
  function renderMeshGrid() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 90, padT = 60, size = 300;
    const step = size / (MESH_SIZE - 1);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("4x4 SYSTEM TOPOLOGY: REAL-TIME HARDWARE TROJAN DETECTION & QUARANTINE", padL, 30);

    // Draw Links
    ctx.strokeStyle = "#334155";
    ctx.lineWidth = 2;
    for (let y = 0; y < MESH_SIZE; y++) {
      for (let x = 0; x < MESH_SIZE; x++) {
        let px = padL + x * step;
        let py = padT + y * step;
        if (x + 1 < MESH_SIZE) {
          ctx.beginPath();
          ctx.moveTo(px, py);
          ctx.lineTo(px + step, py);
          ctx.stroke();
        }
        if (y + 1 < MESH_SIZE) {
          ctx.beginPath();
          ctx.moveTo(px, py);
          ctx.lineTo(px, py + step);
          ctx.stroke();
        }
      }
    }

    // Draw Routers
    for (let y = 0; y < MESH_SIZE; y++) {
      for (let x = 0; x < MESH_SIZE; x++) {
        let px = padL + x * step;
        let py = padT + y * step;
        let isTrojan = (x === TROJAN_NODE.x && y === TROJAN_NODE.y);

        if (isTrojan && isUnderAttack) {
          ctx.fillStyle = isQuarantined ? "#450a0a" : "#7f1d1d";
          ctx.strokeStyle = "#ef4444";
          ctx.lineWidth = 3;
        } else {
          ctx.fillStyle = "#1e293b";
          ctx.strokeStyle = "#38bdf8";
          ctx.lineWidth = 2;
        }

        ctx.beginPath();
        ctx.arc(px, py, 14, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 10px 'JetBrains Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText(isTrojan && isUnderAttack ? (isQuarantined ? "LOCK" : "ATTK") : x + "," + y, px, py + 4);
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
    ctx.fillText("SECURITY HARDWARE AUDIT", sumX + 16, sumY + 30);

    ctx.fillStyle = "#ffffff";
    ctx.font = "10px 'JetBrains Mono', monospace";
    ctx.fillText("Trojan Core: Node (1,1)", sumX + 16, sumY + 60);
    ctx.fillText("Attack Status: " + (isUnderAttack ? "ACTIVE" : "QUIET"), sumX + 16, sumY + 80);
    ctx.fillText("Quarantine: " + (isQuarantined ? "ISOLATED" : "INACTIVE"), sumX + 16, sumY + 100);
    ctx.fillText("Entropy: " + secMetrics.entropy.toFixed(2) + " bits", sumX + 16, sumY + 120);
    ctx.fillText("PUF Tag MAC: Valid", sumX + 16, sumY + 140);
  }

  // 2. Shannon Entropy Plot
  function renderEntropyPlot() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padT = 50, padR = 40, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("REAL-TIME TRAFFIC SHANNON ENTROPY H(X) • ANOMALY THRESHOLD", padL, 28);

    // Axes: 0 to 4.5 bits
    const maxH = 4.5;
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;

    for (let gy = 0; gy <= 4; gy++) {
      let y = padT + (gy / 4) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let hLabel = (maxH * (1 - gy / 4)).toFixed(1) + " b";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(hLabel, padL - 8, y + 4);
    }

    // Anomaly Threshold line (2.2 bits)
    let yTh = padT + (1 - 2.2 / maxH) * graphH;
    ctx.strokeStyle = "rgba(239, 68, 68, 0.5)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(padL, yTh);
    ctx.lineTo(w - padR, yTh);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = "#ef4444";
    ctx.fillText("Entropy Anomaly Quarantine Trip (2.2 bits)", padL + 10, yTh - 6);

    if (entropyHistory.length < 2) return;

    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    entropyHistory.forEach((val, idx) => {
      let px = padL + (idx / (entropyHistory.length - 1)) * graphW;
      let py = padT + (1 - val / maxH) * graphH;
      if (idx === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    });
    ctx.stroke();
  }

  // Window Dispatch Interface
  window.updateSecurityWorkbench = function () {
    render();
  };

  window.switchSecView = function (v) {
    activeView = v;
    document.getElementById("btnSecMesh").className = (v === "mesh_grid") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnSecEntropy").className = (v === "entropy_plot") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.triggerMaliciousAttack = function () {
    isUnderAttack = true;
    for (let c = 0; c < 15; c++) stepSecurityPhysics();
  };

  window.resetSecurityCAD = function () {
    isUnderAttack = false;
    isQuarantined = false;
    attackCycle = 0;
    secMetrics.entropy = 3.85;
    entropyHistory = [];
    updateHUD();
    render();
  };

  window.exportSecurityReport = function () {
    let rpt = [
      "===============================================================================",
      "NoC HARDWARE SECURITY VERIFICATION & THREAT AUDIT REPORT",
      "===============================================================================",
      "Threat Model Evaluated   : " + document.getElementById("secThreatSelect").value.toUpperCase(),
      "Silicon Defense Shield   : " + document.getElementById("secDefenseSelect").value.toUpperCase(),
      "Isolation Status         : " + (isQuarantined ? "ATTACK ISOLATED (Core Quarantined)" : "NOMINAL"),
      "Traffic Shannon Entropy  : H = " + secMetrics.entropy.toFixed(2) + " bits (Baseline: 3.85 bits)",
      "Timing Mutual Information: " + secMetrics.mutualInfo.toFixed(2) + " bits / cycle",
      "PUF Hardware Signature   : 128-Bit SRAM-PUF Challenge-Response Protocol Active",
      "==============================================================================="
    ];
    document.getElementById("secExportText").textContent = rpt.join("\n");
    document.getElementById("secExportWrap").style.display = "block";
  };

  // Initial Boot
  for (let c = 0; c < 30; c++) stepSecurityPhysics();
  render();
})();
</script>
