# 🏗️ 2.5D/3D Multi-Die Chiplet CAD Workbench & Yield Optimizer

An interactive Computer-Aided Design (CAD) workbench for heterogeneous 2.5D and 3D multi-die chiplet systems. Formulate and solve defect-driven wafer yield economics (Poisson & Murphy models) comparing reticle-busting monolithic dies against modular chiplets, simulate Universal Chiplet Interconnect Express (UCIe) and Bunch-of-Wires (BoW) physical layer D2D links, analyze substrate shoreline bandwidth density, and evaluate thermal coupling to high-bandwidth memory (HBM3e) stacks.

<div class="noc-sim-container">
  <!-- Controls Panel -->
  <div class="noc-sim-controls" style="display:flex; flex-wrap:wrap; gap:0.75rem; align-items:center;">
    <label><b>Packaging Substrate:</b>
      <select id="chipletPackageType" class="noc-sim-select" onchange="updateChipletWorkbench()">
        <option value="cowos_s" selected>2.5D Silicon Interposer (TSMC CoWoS-S / Intel EMIB, 40µm Bump, 0.22 pJ/bit)</option>
        <option value="organic_mcm">Standard Organic Substrate (MCM / BoW, 110µm Bump, 0.55 pJ/bit)</option>
        <option value="hybrid_3d">3D Direct Cu-Cu Hybrid Bonding (TSMC SoIC, &lt;9µm Pitch, 0.08 pJ/bit)</option>
        <option value="foveros_omni">2.5D/3D Multi-Stack Bridge (Intel Foveros Omni, 25µm Pitch, 0.15 pJ/bit)</option>
      </select>
    </label>

    <label><b>Defect Density (D0):</b>
      <select id="chipletDefectSelect" class="noc-sim-select" onchange="updateChipletWorkbench()">
        <option value="0.05">Mature 5nm Fab (D0 = 0.05 /cm²)</option>
        <option value="0.09" selected>Leading-Edge 3nm Fab (D0 = 0.09 /cm²)</option>
        <option value="0.18">Early R&amp;D 2nm Fab (D0 = 0.18 /cm²)</option>
      </select>
    </label>

    <label><b>Active Component Tile:</b>
      <select id="chipletPalette" class="noc-sim-select">
        <option value="npu">🧠 Tensor NPU Corelet (140W, 110 mm²)</option>
        <option value="cpu">⚡ High-Performance CPU (90W, 75 mm²)</option>
        <option value="hbm">💾 HBM3e Memory Stack (32W, 1.2 TB/s, Max 85°C)</option>
        <option value="io">🌐 UCIe / PCIe-Gen6 I/O Hub (25W, 60 mm²)</option>
        <option value="l3">📦 Distributed SRAM Cache Hub (20W, 45 mm²)</option>
        <option value="clear">🧹 Remove / Clear Socket</option>
      </select>
    </label>

    <div style="display:flex; gap:0.5rem; flex-wrap:wrap; width:100%; margin-top:0.25rem;">
      <button class="noc-sim-btn" id="btnChipFloor" onclick="switchChipletView('floorplan')" style="background:#0284c7;">📐 Floorplan &amp; D2D Links</button>
      <button class="noc-sim-btn secondary" id="btnChipYield" onclick="switchChipletView('yield_curve')">📊 Wafer Yield &amp; Cost Curve</button>
      <button class="noc-sim-btn secondary" id="btnChipThermal" onclick="switchChipletView('thermal_map')">🔥 Thermal Coupling &amp; HBM Map</button>
      <button class="noc-sim-btn secondary" onclick="autoRouteChipletMesh()">🔗 Auto-Route 2.5D Mesh</button>
      <button class="noc-sim-btn secondary" onclick="resetChipletCAD()">🔄 Clear Layout</button>
      <button class="noc-sim-btn secondary" onclick="exportChipletBOM()" style="margin-left:auto;">📋 Export Packaging BOM</button>
    </div>
  </div>

  <!-- Live Physical & Economic Metrics HUD -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; margin-top:0.75rem; margin-bottom:0.75rem; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Packaging Cost vs. Monolithic</div>
      <div style="font-size:1.05rem; font-weight:700; color:#22c55e; margin:3px 0;" id="hudChipletCost">$385 (54% Savings)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudMonoCost">Monolithic 840mm²: $840 (Yield: 14.2%)</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Compound Packaging Yield</div>
      <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin:3px 0;" id="hudChipletYield">74.8% (KGD + Bond)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudBondYield">Die Yield: 81.2% | Bonding: 99.6%</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Total D2D Bisection Throughput</div>
      <div style="font-size:1.05rem; font-weight:700; color:#eab308; margin:3px 0;" id="hudThroughput">3.84 TB/s</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudD2DEnergy">UCIe PHY: 0.22 pJ/bit | Latency: 1.8 ns</div>
    </div>

    <div style="background:var(--tcl-surface); padding:0.6rem 0.85rem; border-radius:8px; border:1px solid var(--tcl-border);">
      <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase;">Peak Junction Temperature</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f87171; margin:3px 0;" id="hudTemp">78.4°C (Nominal)</div>
      <div style="color:#64748b; font-size:0.75rem;" id="hudHbmMargin">HBM Margin: +6.6°C to Throttling</div>
    </div>
  </div>

  <!-- CAD Interactive Canvas -->
  <div class="noc-sim-canvas-wrap" style="position:relative;">
    <canvas id="chipletCanvas" width="700" height="440" style="width:100%; max-width:700px; height:auto; display:block; border-radius:8px; background:#0b1120; border:1px solid #1e293b; cursor:pointer;"></canvas>
  </div>

  <!-- Packaging BOM Modal / Panel -->
  <div id="chipletBomWrap" style="display:none; margin-top:0.75rem; background:#0f172a; border:1px solid #334155; border-radius:8px; padding:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#e2e8f0;">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
      <strong style="color:#38bdf8;">2.5D/3D Packaging Bill of Materials (BOM) &amp; Yield Audit:</strong>
      <button onclick="document.getElementById('chipletBomWrap').style.display='none'" style="background:transparent; border:none; color:#94a3b8; cursor:pointer;">✕ Close</button>
    </div>
    <pre id="chipletBomText" style="margin:0; white-space:pre-wrap; max-height:220px; overflow-y:auto; color:#a5f3fc;"></pre>
  </div>

  <!-- Theory & Formulation -->
  <div style="margin-top:1rem; padding:1.1rem 1.25rem; background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:10px; font-size:0.86rem; color:var(--md-default-fg-color--lighter); line-height:1.7;">
    <strong style="color:var(--tcl-heading); font-size:0.95rem;">🔬 Multi-Die Packaging Economics &amp; D2D Interconnect Physics (Chapter 9):</strong>
    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0;">
      <li><strong>Wafer Defect Yield Scaling (Murphy Model):</strong> When building monolithic gigascale dies, yield plunges exponentially as area $A$ approaches reticle limits ($858\text{ mm}^2$ in EUV). The Murphy defect clustering formulation predicts die yield $Y_{die}$:
        $$Y_{die} = \left(\frac{1 - e^{-D_0 A}}{D_0 A}\right)^2$$
        Splitting a monolithic $800\text{ mm}^2$ design into four $200\text{ mm}^2$ chiplets elevates raw silicon yield from $14\%$ to over $78\%$.</li>
      <li><strong>Compound Multi-Die System Yield:</strong> The net yield of a packaged multi-chiplet module incorporates Known Good Die (KGD) probe test coverage $Y_{test}$ and micro-bump bonding yield $Y_{bond}$:
        $$Y_{system} = Y_{sub} \times \prod_{i=1}^{N} \left( Y_{die, i} \times Y_{test} \times Y_{bond} \right)$$
        Even with $Y_{bond} = 99.8\%$, assembling 16 chiplets requires rigorous testing to avoid catastrophic compound yield loss.</li>
      <li><strong>UCIe &amp; BoW Shoreline Bandwidth:</strong> Microbump arrays along the chiplet perimeter dictate escape routing density:
        $$\text{Density} = \frac{N_{lanes} \times f_{lane}}{\text{Shoreline Length}} \quad [\text{Tbps/mm}]$$
        Silicon interposers with $40\,\mu\text{m}$ pitch achieve $>1.3\text{ Tbps/mm}$ at $<0.25\text{ pJ/bit}$, whereas standard organic substrates are constrained to $<0.4\text{ Tbps/mm}$ at $>0.55\text{ pJ/bit}$.</li>
      <li><strong>Thermal Cross-Coupling to HBM:</strong> High-power compute corelets ($>1.2\text{ W/mm}^2$) transfer heat through the high-thermal-conductivity silicon interposer ($k_{Si} \approx 149\text{ W/m}\cdot\text{K}$) directly into adjacent HBM3e DRAM stacks, requiring thermal relief spacing ($\ge 1.5\text{ mm}$) to remain below the $85^\circ\text{C}$ DRAM retention limit.</li>
    </ul>
  </div>
</div>

<script>
// ============================================================================
// 2.5D/3D Multi-Die Chiplet CAD Engine & Yield Optimizer
// ============================================================================

(function () {
  const SUBSTRATE_SPECS = {
    "cowos_s": { name: "2.5D Silicon Interposer (CoWoS-S)", bumpPitchUm: 40, energyPjBit: 0.22, costPerMm2: 0.25, latencyNs: 1.8, bwPerLaneGbps: 32, maxShorelineTbps: 1.4 },
    "organic_mcm": { name: "Standard Organic Substrate (MCM)", bumpPitchUm: 110, energyPjBit: 0.55, costPerMm2: 0.05, latencyNs: 3.4, bwPerLaneGbps: 16, maxShorelineTbps: 0.38 },
    "hybrid_3d": { name: "3D Direct Cu-Cu Hybrid Bonding (SoIC)", bumpPitchUm: 9, energyPjBit: 0.08, costPerMm2: 0.50, latencyNs: 0.6, bwPerLaneGbps: 64, maxShorelineTbps: 4.2 },
    "foveros_omni": { name: "Bridge Multi-Stack (Foveros Omni)", bumpPitchUm: 25, energyPjBit: 0.15, costPerMm2: 0.35, latencyNs: 1.2, bwPerLaneGbps: 40, maxShorelineTbps: 2.1 }
  };

  const CHIPLET_TYPES = {
    "npu": { name: "Tensor NPU", icon: "🧠", powerW: 140, areaMm2: 110, baseCost: 45, maxTemp: 105, isHbm: false },
    "cpu": { name: "CPU Cluster", icon: "⚡", powerW: 90, areaMm2: 75, baseCost: 35, maxTemp: 100, isHbm: false },
    "hbm": { name: "HBM3e Stack", icon: "💾", powerW: 32, areaMm2: 95, baseCost: 65, maxTemp: 85, isHbm: true },
    "io":  { name: "UCIe/PCIe IO", icon: "🌐", powerW: 25, areaMm2: 60, baseCost: 20, maxTemp: 95, isHbm: false },
    "l3":  { name: "SRAM Cache Hub", icon: "📦", powerW: 20, areaMm2: 45, baseCost: 18, maxTemp: 95, isHbm: false }
  };

  let activeView = "floorplan"; // "floorplan", "yield_curve", "thermal_map"

  // 4x4 Placement Grid on Package
  const GRID_COLS = 4;
  const GRID_ROWS = 4;
  let layoutGrid = [
    ["io",  "cpu", "cpu", "io"],
    ["hbm", "npu", "npu", "hbm"],
    ["hbm", "npu", "npu", "hbm"],
    ["io",  "l3",  "l3",  "io"]
  ];

  // Inter-chiplet links [ [r1, c1, r2, c2] ]
  let d2dLinks = [];

  let cadMetrics = {
    totalAreaMm2: 0,
    totalPowerW: 0,
    compositeCost: 0,
    monoCost: 0,
    savingsPct: 0,
    compoundYieldPct: 0,
    monoYieldPct: 0,
    bisectionTbps: 0,
    peakTempC: 45,
    hbmMarginC: 15
  };

  const canvas = document.getElementById("chipletCanvas");
  const ctx = canvas.getContext("2d");

  function autoRouteMeshLinks() {
    d2dLinks = [];
    for (let r = 0; r < GRID_ROWS; r++) {
      for (let c = 0; c < GRID_COLS; c++) {
        if (!layoutGrid[r][c]) continue;
        // Connect East
        if (c + 1 < GRID_COLS && layoutGrid[r][c + 1]) {
          d2dLinks.push([r, c, r, c + 1]);
        }
        // Connect South
        if (r + 1 < GRID_ROWS && layoutGrid[r + 1][c]) {
          d2dLinks.push([r, c, r + 1, c]);
        }
      }
    }
  }

  function computeCADPhysics() {
    const pkgKey = document.getElementById("chipletPackageType").value;
    const subSpec = SUBSTRATE_SPECS[pkgKey] || SUBSTRATE_SPECS["cowos_s"];
    const D0 = parseFloat(document.getElementById("chipletDefectSelect").value) || 0.09;

    let totalSiliconArea = 0;
    let totalPower = 0;
    let chipletCount = 0;
    let placedChips = [];

    for (let r = 0; r < GRID_ROWS; r++) {
      for (let c = 0; c < GRID_COLS; c++) {
        let typeKey = layoutGrid[r][c];
        if (typeKey && CHIPLET_TYPES[typeKey]) {
          let spec = CHIPLET_TYPES[typeKey];
          totalSiliconArea += spec.areaMm2;
          totalPower += spec.powerW;
          chipletCount++;
          placedChips.push({ r, c, spec });
        }
      }
    }

    // Murphy Wafer Yield Model: Y = ((1 - exp(-D0 * A)) / (D0 * A))^2
    function murphyYield(areaCm2) {
      const x = D0 * areaCm2;
      if (x < 1e-4) return 0.99;
      return Math.pow((1 - Math.exp(-x)) / x, 2);
    }

    // Monolithic comparison (equivalent monolithic mega-die with 1.15x routing overhead)
    const monoAreaMm2 = totalSiliconArea * 1.15;
    const monoYield = murphyYield(monoAreaMm2 / 100);
    const monoWaferCost = 14000; // 300mm wafer in 3nm
    const monoDiesPerWafer = Math.max(1, Math.floor((Math.PI * Math.pow(150, 2)) / (monoAreaMm2 * 1.2)));
    const monoWorkingDies = Math.max(1, monoDiesPerWafer * monoYield);
    const monoDieCost = monoWaferCost / monoWorkingDies;

    // Multi-Chiplet Cost Breakdown
    let totalChipletBareCost = 0;
    let compoundDieYield = 1.0;
    const kgdTestYield = 0.994;
    const bondingYield = 0.997;

    placedChips.forEach(chip => {
      let areaCm2 = chip.spec.areaMm2 / 100;
      let y = murphyYield(areaCm2);
      compoundDieYield *= (y * kgdTestYield * bondingYield);

      let diesPerWafer = Math.floor((Math.PI * Math.pow(150, 2)) / (chip.spec.areaMm2 * 1.2));
      let costPerGood = monoWaferCost / (diesPerWafer * y);
      totalChipletBareCost += costPerGood;
    });

    const interposerAreaMm2 = totalSiliconArea * 1.45;
    const interposerCost = interposerAreaMm2 * subSpec.costPerMm2;
    const packagingAssemblyCost = chipletCount * 8.5;
    const totalChipletCost = totalChipletBareCost + interposerCost + packagingAssemblyCost;

    cadMetrics.totalAreaMm2 = totalSiliconArea;
    cadMetrics.totalPowerW = totalPower;
    cadMetrics.compositeCost = Math.round(totalChipletCost);
    cadMetrics.monoCost = Math.round(monoDieCost);
    cadMetrics.savingsPct = Math.round(((monoDieCost - totalChipletCost) / monoDieCost) * 100);
    cadMetrics.compoundYieldPct = (compoundDieYield * 100);
    cadMetrics.monoYieldPct = (monoYield * 100);

    // Bisection Bandwidth: cut across horizontal middle of grid
    let cutLinks = d2dLinks.filter(([r1, c1, r2, c2]) => (r1 < 2 && r2 >= 2) || (r2 < 2 && r1 >= 2)).length;
    let linkBwTbps = subSpec.bwPerLaneGbps * (64 / 8) * 1e-3; // 64-wire bus
    cadMetrics.bisectionTbps = (cutLinks * linkBwTbps * 1.5).toFixed(2);

    // Thermal Simulation: Simple 2D diffusion approximation across tiles
    let ambientTemp = 35;
    let rthSubstrate = 0.32; // °C/W
    let peakT = ambientTemp;
    let minHbmMargin = 999;

    placedChips.forEach(c1 => {
      let localHeat = c1.spec.powerW * rthSubstrate;
      // Add cross-coupling from neighbors
      let coupling = 0;
      placedChips.forEach(c2 => {
        if (c1 === c2) return;
        let dist = Math.hypot(c1.c - c2.c, c1.r - c2.r);
        coupling += (c2.spec.powerW * 0.08) / Math.max(1, dist * 1.5);
      });
      let tileT = ambientTemp + localHeat + coupling;
      if (tileT > peakT) peakT = tileT;
      if (c1.spec.isHbm) {
        let margin = c1.spec.maxTemp - tileT;
        if (margin < minHbmMargin) minHbmMargin = margin;
      }
    });

    cadMetrics.peakTempC = peakT.toFixed(1);
    cadMetrics.hbmMarginC = minHbmMargin.toFixed(1);

    updateHUD();
  }

  function updateHUD() {
    const pkgKey = document.getElementById("chipletPackageType").value;
    const subSpec = SUBSTRATE_SPECS[pkgKey] || SUBSTRATE_SPECS["cowos_s"];

    document.getElementById("hudChipletCost").textContent = "$" + cadMetrics.compositeCost + " (" + cadMetrics.savingsPct + "% Savings)";
    document.getElementById("hudMonoCost").textContent = "Monolithic " + cadMetrics.totalAreaMm2 + "mm²: $" + cadMetrics.monoCost + " (Yield: " + cadMetrics.monoYieldPct.toFixed(1) + "%)";
    document.getElementById("hudChipletYield").textContent = cadMetrics.compoundYieldPct.toFixed(1) + "% Compound Yield";
    document.getElementById("hudBondYield").textContent = "Substrate: " + subSpec.name.split(" ")[0] + " | KGD Probe: 99.4%";
    document.getElementById("hudThroughput").textContent = cadMetrics.bisectionTbps + " TB/s (" + d2dLinks.length + " Links)";
    document.getElementById("hudD2DEnergy").textContent = "D2D Energy: " + subSpec.energyPjBit + " pJ/bit | Latency: " + subSpec.latencyNs + " ns";
    document.getElementById("hudTemp").textContent = cadMetrics.peakTempC + "°C Peak (" + cadMetrics.totalPowerW + "W TDP)";
    document.getElementById("hudHbmMargin").textContent = "HBM3e Margin: " + (cadMetrics.hbmMarginC > 0 ? "+" : "") + cadMetrics.hbmMarginC + "°C to 85°C Limit";
  }

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (activeView === "floorplan") {
      renderFloorplanCAD();
    } else if (activeView === "yield_curve") {
      renderYieldCurve();
    } else if (activeView === "thermal_map") {
      renderThermalMap();
    }
  }

  // 1. Floorplan CAD View
  function renderFloorplanCAD() {
    const w = canvas.width;
    const h = canvas.height;
    const pkgKey = document.getElementById("chipletPackageType").value;
    const subSpec = SUBSTRATE_SPECS[pkgKey] || SUBSTRATE_SPECS["cowos_s"];

    // Background Interposer Boundary
    const interL = 60, interT = 50, interW = 580, interH = 340;
    ctx.fillStyle = "#1e293b";
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(interL, interT, interW, interH, 12);
    ctx.fill();
    ctx.stroke();

    // Interposer Microbump Grid Texture
    ctx.fillStyle = "rgba(56, 189, 248, 0.08)";
    for (let bx = interL + 15; bx < interL + interW; bx += 20) {
      for (let by = interT + 15; by < interT + interH; by += 20) {
        ctx.fillRect(bx, by, 2, 2);
      }
    }

    // Title / Substrate Info Banner
    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("2.5D INTERPOSER FLOORPLAN & UCIe MICRO-BUMP ESCAPE CHANNELS", interL + 15, interT - 16);

    ctx.fillStyle = "#38bdf8";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillText("Substrate: " + subSpec.name + " (" + subSpec.bumpPitchUm + "µm Pitch)", interL + interW - 320, interT - 16);

    const cellW = (interW - 50) / GRID_COLS;
    const cellH = (interH - 50) / GRID_ROWS;

    // Draw D2D Interconnect Wires
    ctx.strokeStyle = "rgba(234, 179, 8, 0.85)";
    ctx.lineWidth = 3;
    d2dLinks.forEach(([r1, c1, r2, c2]) => {
      let x1 = interL + 25 + c1 * cellW + cellW * 0.5;
      let y1 = interT + 25 + r1 * cellH + cellH * 0.5;
      let x2 = interL + 25 + c2 * cellW + cellW * 0.5;
      let y2 = interT + 25 + r2 * cellH + cellH * 0.5;

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();

      // Small high-density bus indicator
      let mx = (x1 + x2) * 0.5;
      let my = (y1 + y2) * 0.5;
      ctx.fillStyle = "#eab308";
      ctx.fillRect(mx - 4, my - 4, 8, 8);
    });

    // Draw Socket Sockets & Placed Chiplets
    for (let r = 0; r < GRID_ROWS; r++) {
      for (let c = 0; c < GRID_COLS; c++) {
        let x = interL + 25 + c * cellW + 6;
        let y = interT + 25 + r * cellH + 6;
        let cw = cellW - 12;
        let ch = cellH - 12;
        let typeKey = layoutGrid[r][c];

        if (!typeKey) {
          // Empty Socket
          ctx.strokeStyle = "rgba(100, 116, 139, 0.4)";
          ctx.setLineDash([4, 4]);
          ctx.strokeRect(x, y, cw, ch);
          ctx.setLineDash([]);
          ctx.fillStyle = "#475569";
          ctx.font = "11px 'JetBrains Mono', monospace";
          ctx.textAlign = "center";
          ctx.fillText("Empty", x + cw / 2, y + ch / 2 + 4);
          continue;
        }

        let spec = CHIPLET_TYPES[typeKey];
        // Chiplet Die Body
        ctx.fillStyle = spec.isHbm ? "#064e3b" : (typeKey === "npu" ? "#312e81" : "#1e1b4b");
        ctx.strokeStyle = spec.isHbm ? "#10b981" : (typeKey === "npu" ? "#6366f1" : "#38bdf8");
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.roundRect(x, y, cw, ch, 6);
        ctx.fill();
        ctx.stroke();

        // Icon & Labels
        ctx.fillStyle = "#f8fafc";
        ctx.font = "16px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText(spec.icon, x + cw / 2, y + ch / 2 - 8);

        ctx.font = "bold 10px 'JetBrains Mono', monospace";
        ctx.fillStyle = "#ffffff";
        ctx.fillText(spec.name, x + cw / 2, y + ch / 2 + 10);

        ctx.font = "9px 'JetBrains Mono', monospace";
        ctx.fillStyle = "#94a3b8";
        ctx.fillText(spec.powerW + "W | " + spec.areaMm2 + "mm²", x + cw / 2, y + ch / 2 + 22);
      }
    }
  }

  // 2. Wafer Yield & Cost Curve View
  function renderYieldCurve() {
    const w = canvas.width;
    const h = canvas.height;
    const padL = 70, padR = 40, padT = 60, padB = 60;
    const graphW = w - padL - padR;
    const graphH = h - padT - padB;
    const D0 = parseFloat(document.getElementById("chipletDefectSelect").value) || 0.09;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("WAFER YIELD & DIE COST vs. DIE AREA (MURPHY MODEL, D0 = " + D0 + " /cm²)", padL, 30);

    // Axes
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    const maxAreaMm2 = 900;
    const maxYld = 100;

    for (let gy = 0; gy <= 5; gy++) {
      let y = padT + (gy / 5) * graphH;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();

      let yLabel = Math.round(maxYld * (1 - gy / 5)) + "%";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "right";
      ctx.fillText(yLabel, padL - 8, y + 4);
    }

    for (let gx = 0; gx <= 6; gx++) {
      let x = padL + (gx / 6) * graphW;
      ctx.beginPath();
      ctx.moveTo(x, padT);
      ctx.lineTo(x, h - padB);
      ctx.stroke();

      let aLabel = Math.round((gx / 6) * maxAreaMm2) + "mm²";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(aLabel, x, h - padB + 16);
    }

    // Yield Curve: Murphy equation
    ctx.strokeStyle = "#22c55e";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let a = 10; a <= maxAreaMm2; a += 10) {
      let xVal = D0 * (a / 100);
      let yld = Math.pow((1 - Math.exp(-xVal)) / xVal, 2) * 100;
      let px = padL + (a / maxAreaMm2) * graphW;
      let py = padT + (1 - yld / maxYld) * graphH;
      if (a === 10) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // Mark Monolithic Point vs Modular Chiplet Point
    let monoA = Math.min(maxAreaMm2, cadMetrics.totalAreaMm2 * 1.15);
    let monoPx = padL + (monoA / maxAreaMm2) * graphW;
    let monoPy = padT + (1 - cadMetrics.monoYieldPct / maxYld) * graphH;

    ctx.fillStyle = "#ef4444";
    ctx.beginPath();
    ctx.arc(monoPx, monoPy, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#f87171";
    ctx.font = "bold 10px 'JetBrains Mono', monospace";
    ctx.textAlign = "left";
    ctx.fillText("Monolithic (" + Math.round(monoA) + "mm²: " + cadMetrics.monoYieldPct.toFixed(1) + "%)", monoPx + 10, monoPy);

    let avgChipA = cadMetrics.totalAreaMm2 / 8;
    let chipPx = padL + (avgChipA / maxAreaMm2) * graphW;
    let chipXVal = D0 * (avgChipA / 100);
    let chipYld = Math.pow((1 - Math.exp(-chipXVal)) / chipXVal, 2) * 100;
    let chipPy = padT + (1 - chipYld / maxYld) * graphH;

    ctx.fillStyle = "#38bdf8";
    ctx.beginPath();
    ctx.arc(chipPx, chipPy, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#38bdf8";
    ctx.fillText("Individual Chiplet (" + Math.round(avgChipA) + "mm²: " + chipYld.toFixed(1) + "%)", chipPx + 10, chipPy - 8);
  }

  // 3. Thermal Map View
  function renderThermalMap() {
    const w = canvas.width;
    const h = canvas.height;
    const interL = 60, interT = 50, interW = 580, interH = 340;

    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 12px 'JetBrains Mono', monospace";
    ctx.fillText("2.5D INTERPOSER HEAT DIFFUSION & HBM THERMAL STRESS ISOTHERMS", interL + 15, interT - 16);

    const cellW = (interW - 50) / GRID_COLS;
    const cellH = (interH - 50) / GRID_ROWS;

    for (let r = 0; r < GRID_ROWS; r++) {
      for (let c = 0; c < GRID_COLS; c++) {
        let x = interL + 25 + c * cellW;
        let y = interT + 25 + r * cellH;
        let typeKey = layoutGrid[r][c];

        let p = typeKey ? CHIPLET_TYPES[typeKey].powerW : 0;
        let temp = 35 + p * 0.35;

        // Thermal colormap (Blue: 35C -> Yellow: 70C -> Red: 100C)
        let tNorm = Math.min(1.0, Math.max(0, (temp - 35) / 65));
        let rCol = Math.round(tNorm * 255);
        let gCol = Math.round((1 - Math.abs(tNorm - 0.5) * 2) * 200);
        let bCol = Math.round((1 - tNorm) * 220);

        ctx.fillStyle = "rgb(" + rCol + "," + gCol + "," + bCol + ")";
        ctx.fillRect(x + 4, y + 4, cellW - 8, cellH - 8);

        ctx.fillStyle = tNorm > 0.6 ? "#000000" : "#ffffff";
        ctx.font = "bold 12px 'JetBrains Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText(temp.toFixed(1) + "°C", x + cellW / 2, y + cellH / 2);
        if (typeKey) {
          ctx.font = "10px 'JetBrains Mono', monospace";
          ctx.fillText(CHIPLET_TYPES[typeKey].name, x + cellW / 2, y + cellH / 2 + 16);
        }
      }
    }
  }

  // Interactive Socket Placement
  canvas.addEventListener("click", function (e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const mx = (e.clientX - rect.left) * scaleX;
    const my = (e.clientY - rect.top) * scaleY;

    const interL = 60, interT = 50, interW = 580, interH = 340;
    const cellW = (interW - 50) / GRID_COLS;
    const cellH = (interH - 50) / GRID_ROWS;

    for (let r = 0; r < GRID_ROWS; r++) {
      for (let c = 0; c < GRID_COLS; c++) {
        let x = interL + 25 + c * cellW;
        let y = interT + 25 + r * cellH;
        if (mx >= x && mx <= x + cellW && my >= y && my <= y + cellH) {
          const selectedPalette = document.getElementById("chipletPalette").value;
          layoutGrid[r][c] = (selectedPalette === "clear") ? null : selectedPalette;
          autoRouteMeshLinks();
          computeCADPhysics();
          render();
          return;
        }
      }
    }
  });

  // Window Dispatch Interface
  window.updateChipletWorkbench = function () {
    computeCADPhysics();
    render();
  };

  window.switchChipletView = function (v) {
    activeView = v;
    document.getElementById("btnChipFloor").className = (v === "floorplan") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnChipYield").className = (v === "yield_curve") ? "noc-sim-btn" : "noc-sim-btn secondary";
    document.getElementById("btnChipThermal").className = (v === "thermal_map") ? "noc-sim-btn" : "noc-sim-btn secondary";
    render();
  };

  window.autoRouteChipletMesh = function () {
    autoRouteMeshLinks();
    computeCADPhysics();
    render();
  };

  window.resetChipletCAD = function () {
    for (let r = 0; r < GRID_ROWS; r++) {
      for (let c = 0; c < GRID_COLS; c++) {
        layoutGrid[r][c] = null;
      }
    }
    d2dLinks = [];
    computeCADPhysics();
    render();
  };

  window.exportChipletBOM = function () {
    const pkgKey = document.getElementById("chipletPackageType").value;
    const subSpec = SUBSTRATE_SPECS[pkgKey] || SUBSTRATE_SPECS["cowos_s"];
    let bomLines = [
      "===============================================================================",
      "2.5D/3D HETEROGENEOUS CHIPLET SYSTEM PACKAGING AUDIT & BILL OF MATERIALS (BOM)",
      "===============================================================================",
      "Packaging Technology     : " + subSpec.name,
      "D2D PHY Bump Pitch       : " + subSpec.bumpPitchUm + " µm | Energy Efficiency: " + subSpec.energyPjBit + " pJ/bit",
      "Total Silicon Footprint  : " + cadMetrics.totalAreaMm2 + " mm² (Aggregate Interposer Area: " + (cadMetrics.totalAreaMm2 * 1.45).toFixed(0) + " mm²)",
      "Total Thermal Design Pwr : " + cadMetrics.totalPowerW + " W (Peak Junction Temp: " + cadMetrics.peakTempC + "°C)",
      "D2D Bisection Bandwidth  : " + cadMetrics.bisectionTbps + " TB/s (" + d2dLinks.length + " UCIe Physical Channels)",
      "-------------------------------------------------------------------------------",
      "ECONOMIC & WAFER YIELD ANALYSIS (MURPHY DEFECT MODEL)",
      "-------------------------------------------------------------------------------",
      "Modular Chiplet BOM Cost : $" + cadMetrics.compositeCost + " per packaged unit",
      "Monolithic 840mm² Cost   : $" + cadMetrics.monoCost + " per tested unit",
      "Silicon Cost Reduction   : " + cadMetrics.savingsPct + "% Economic Savings",
      "Compound Packaging Yield : " + cadMetrics.compoundYieldPct.toFixed(1) + "% (Tested KGD & Microbump Array)",
      "HBM3e Thermal Margin     : " + (cadMetrics.hbmMarginC > 0 ? "+" : "") + cadMetrics.hbmMarginC + "°C relative to 85°C limit",
      "==============================================================================="
    ];
    document.getElementById("chipletBomText").textContent = bomLines.join("\n");
    document.getElementById("chipletBomWrap").style.display = "block";
  };

  // Initial Boot
  autoRouteMeshLinks();
  computeCADPhysics();
  render();
})();
</script>
