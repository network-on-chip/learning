# 🎯 Network-on-Chip Architecture Certification & Quiz Challenge

<div class="noc-hero">
  <div class="noc-track-badge">🏆 Official Assessment & Credential Registry</div>
  <h1>NoC Architecture Knowledge Assessment</h1>
  <p class="subtitle">
    Test your mastery across router microarchitecture, deadlock theory, direct/indirect topologies, and chiplet interconnects. Earn a verifiable, cryptographic SVG Certificate of Completion.
  </p>
</div>

<div id="quizApp" class="noc-sim-container">
  <!-- Registration Step -->
  <div id="stepRegistration">
    <h3 style="margin-top:0;">Candidate Registration</h3>
    <p style="color:var(--md-default-fg-color--lighter); font-size:0.92rem;">
      Enter your details to initialize the assessment session. Your name and institution will be permanently inscribed on your verifiable certificate.
    </p>

    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:1rem; margin:1.25rem 0;">
      <div>
        <label style="font-weight:600; font-size:0.85rem; display:block; margin-bottom:0.35rem;">Candidate Name / Callsign *</label>
        <input type="text" id="candidateName" class="noc-sim-select" style="width:100%; box-sizing:border-box;" placeholder="e.g. Dr. Ada Lovelace" value="Hardware Architect">
      </div>
      <div>
        <label style="font-weight:600; font-size:0.85rem; display:block; margin-bottom:0.35rem;">Institution / University / Company</label>
        <input type="text" id="candidateOrg" class="noc-sim-select" style="width:100%; box-sizing:border-box;" placeholder="e.g. Stanford / SJTU / Intel" value="Academic Researcher">
      </div>
      <div>
        <label style="font-weight:600; font-size:0.85rem; display:block; margin-bottom:0.35rem;">Assessment Mode</label>
        <select id="assessmentMode" class="noc-sim-select" style="width:100%; box-sizing:border-box;">
          <option value="full">Comprehensive Exam (12 Questions - All Tracks)</option>
          <option value="sprint">Speedrun Challenge (6 Questions)</option>
        </select>
      </div>
    </div>

    <button class="noc-sim-btn" onclick="startQuiz()" style="font-size:1rem; padding:0.65rem 1.5rem;">
      🚀 Begin Certification Exam
    </button>
  </div>

  <!-- Quiz Screen -->
  <div id="stepQuiz" style="display:none;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:1rem; padding-bottom:0.75rem; border-bottom:1px solid var(--tcl-border);">
      <div style="font-size:0.85rem; font-weight:600; color:var(--tcl-blue-600);" id="quizProgress">Question 1 of 12</div>
      <div style="display:flex; gap:1rem; align-items:center;">
        <span id="quizTimer" style="font-family:'JetBrains Mono', monospace; font-size:0.9rem; font-weight:700; color:var(--tcl-heading);">⏱️ 30s</span>
        <span id="quizScore" style="font-size:0.85rem; font-weight:600; color:var(--md-default-fg-color--lighter);">Score: 0 pts</span>
      </div>
    </div>

    <div style="margin-bottom:0.75rem;">
      <span class="noc-track-badge" id="quizModuleBadge">Track 1</span>
      <span class="noc-track-badge" id="quizTierBadge" style="margin-left:0.35rem; background:rgba(234, 88, 12, 0.1); color:#ea580c; border-color:rgba(234, 88, 12, 0.2);">Core</span>
    </div>

    <h3 id="quizQuestionText" style="font-size:1.15rem; line-height:1.5; margin-bottom:1.25rem; color:var(--tcl-heading);"></h3>

    <div id="quizOptions" style="display:flex; flex-direction:column; gap:0.75rem; margin-bottom:1.5rem;"></div>

    <div id="quizFeedback" style="display:none; padding:1rem; border-radius:8px; margin-bottom:1.25rem; font-size:0.9rem; line-height:1.5;"></div>

    <div style="display:flex; justify-content:flex-end;">
      <button id="nextBtn" class="noc-sim-btn" onclick="nextQuestion()" style="display:none;">Next Question →</button>
    </div>
  </div>

  <!-- Certificate Result Screen -->
  <div id="stepResult" style="display:none; text-align:center;">
    <div style="font-size:2.5rem; margin-bottom:0.5rem;">🎓</div>
    <h2 style="margin:0 0 0.5rem 0; color:var(--tcl-heading);">Assessment Completed!</h2>
    <p id="resultSummary" style="color:var(--md-default-fg-color--lighter); margin-bottom:1.5rem; font-size:1.05rem;"></p>

    <!-- Certificate Visual -->
    <div id="certificateFrame" style="background:#ffffff; color:#0f172a; border:4px double #d4af37; border-radius:12px; padding:32px 24px; max-width:680px; margin:0 auto 1.5rem; box-shadow:0 12px 36px rgba(0,0,0,0.12); font-family:'Inter', sans-serif;">
      <div style="font-size:12px; text-transform:uppercase; letter-spacing:2px; color:#64748b; font-weight:700;">NoC-Lab Academic Credential Registry</div>
      <h1 style="font-size:1.65rem; font-weight:900; color:#0f172a; margin:10px 0 6px; letter-spacing:-0.5px;">CERTIFICATE OF ACHIEVEMENT</h1>
      <div style="font-size:13px; color:#475569; margin-bottom:16px;">This is to formally certify that</div>
      <div id="certCandidateName" style="font-size:1.85rem; font-weight:800; color:#1e3a8a; border-bottom:2px solid #cbd5e1; display:inline-block; padding:0 30px 4px; margin-bottom:12px;">Candidate Name</div>
      <div id="certCandidateOrg" style="font-size:14px; color:#475569; font-style:italic; margin-bottom:18px;">Institution / University</div>
      <div style="font-size:14px; max-width:520px; margin:0 auto 20px; line-height:1.5; color:#334155;">
        has successfully passed the comprehensive examination in <strong>Network-on-Chip (NoC) Architecture, Router Microarchitecture & Deadlock Avoidance Theory</strong>.
      </div>

      <div style="display:flex; justify-content:space-around; align-items:center; border-top:1px solid #e2e8f0; padding-top:16px; font-size:12px; color:#64748b;">
        <div><b>Score:</b> <span id="certScore" style="color:#0f172a;">--</span></div>
        <div><b>Verification Hash:</b> <span id="certHash" style="font-family:'JetBrains Mono', monospace; color:#0f172a;">NOC-CERT-2026-X89F</span></div>
        <div><b>Date:</b> <span id="certDate" style="color:#0f172a;">2026-11-05</span></div>
      </div>
    </div>

    <div style="display:flex; gap:0.75rem; justify-content:center; flex-wrap:wrap;">
      <button class="noc-sim-btn" onclick="downloadCertificateSVG()">📥 Download Certificate (SVG)</button>
      <a href="../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none;">🏆 View Public Leaderboard</a>
      <button class="noc-sim-btn secondary" onclick="restartQuiz()">🔄 Retake Exam</button>
    </div>
  </div>
</div>

<script>
const QUESTIONS_BANK = [
  {
    "id": "q1",
    "module": "Track 1: Fundamentals",
    "tier": "Fundamental",
    "question": "Why does Wormhole Switching require significantly less buffer area than Virtual Cut-Through (VCT)?",
    "options": [
      "Wormhole switching allocates buffers on an atomic flit-by-flit basis rather than requiring space for the entire packet.",
      "Wormhole switching eliminates all input buffers and routes directly across wires.",
      "Wormhole switching uses optical crossbars that require no electrical storage.",
      "Wormhole switching stores packets exclusively at the source node."
    ],
    "answer": 0,
    "explanation": "In Wormhole switching, the atomic unit of buffer allocation is a flit (a few bytes), whereas Virtual Cut-Through requires the downstream router to have enough buffer capacity to hold the entire packet."
  },
  {
    "id": "q2",
    "module": "Track 1: Fundamentals",
    "tier": "Core",
    "question": "In credit-based flow control, if link wire delay is 1 cycle, processing delay is 1 cycle, and credit return wire is 1 cycle, what is the minimum input buffer depth required to sustain 100% throughput?",
    "options": [
      "1 flit",
      "2 flits",
      "3 flits",
      "8 flits"
    ],
    "answer": 2,
    "explanation": "To sustain 100% throughput without bubbles, the buffer depth must be at least equal to the Round-Trip Time (RTT): B >= t_link + t_proc + t_credit = 1 + 1 + 1 = 3 flits."
  },
  {
    "id": "q3",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Core",
    "question": "Which router pipeline stages are executed by the Head Flit, but skipped by Body Flits in a canonical wormhole router?",
    "options": [
      "Buffer Write (BW) and Switch Traversal (ST)",
      "Route Computation (RC) and Virtual Channel Allocation (VA)",
      "Switch Allocation (SA) and Switch Traversal (ST)",
      "Buffer Write (BW) and Switch Allocation (SA)"
    ],
    "answer": 1,
    "explanation": "The Head Flit establishes the routing path (RC) and reserves a downstream virtual channel (VA). Body flits follow in the established virtual channel, only performing BW, SA, and ST."
  },
  {
    "id": "q4",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Advanced",
    "question": "How does a Matrix Arbiter guarantee starvation freedom (LRU fairness) when multiple input VCs request the same output port?",
    "options": [
      "By maintaining a pseudo-random number generator that picks requesters uniformly.",
      "By clearing the winner's row to 0 and setting its column to 1 in an NxN triangular priority matrix.",
      "By assigning static priorities based on physical wire coordinates.",
      "By dropping contending packets and requesting a retransmission."
    ],
    "answer": 1,
    "explanation": "In a Matrix Arbiter, when client k wins, row k is cleared (making k lowest priority) and column k is set to 1 (all other clients now have priority over k). This provides exact Least Recently Used (LRU) fairness in 2 gate levels."
  },
  {
    "id": "q5",
    "module": "Track 3: Topologies & Metrics",
    "tier": "Core",
    "question": "What is the network diameter of an 8x8 2D Mesh compared to an 8x8 2D Torus?",
    "options": [
      "Mesh = 14 hops, Torus = 8 hops",
      "Mesh = 16 hops, Torus = 16 hops",
      "Mesh = 8 hops, Torus = 4 hops",
      "Mesh = 64 hops, Torus = 32 hops"
    ],
    "answer": 0,
    "explanation": "For a k x k network (k=8), diameter of a mesh is 2(k - 1) = 2(7) = 14 hops. For a torus, wrap-around links cut the diameter to 2 * floor(k/2) = 2(4) = 8 hops."
  },
  {
    "id": "q6",
    "module": "Track 3: Topologies & Metrics",
    "tier": "Advanced",
    "question": "Why does a Folded Torus layout resolve the physical VLSI drawback of standard Torus wrap-around links?",
    "options": [
      "It removes wrap-around links completely, turning the torus into a star network.",
      "It interleaves router placement so all physical link lengths become uniform and at most 2 tile widths.",
      "It replaces copper wires with wireless radio-frequency transceivers.",
      "It compresses 4 routers into a single crossbar without physical links."
    ],
    "answer": 1,
    "explanation": "In a standard torus, wrap-around wires span the full die diameter. By folding the physical layout accordion-style, all inter-router links become identical in length (at most 2 tile units), avoiding slow global wire RC delays."
  },
  {
    "id": "q7",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Core",
    "question": "Why is Dimension-Order Routing (XY Routing) provably deadlock-free in a 2D mesh?",
    "options": [
      "It allows all 8 turns between X and Y dimensions dynamically.",
      "It prohibits all 4 turns from dimension Y to dimension X, guaranteeing that the Channel Dependency Graph (CDG) is strictly acyclic.",
      "It drops flits whenever buffer queues fill up.",
      "It uses deflection routing to bounce flits away from congested links."
    ],
    "answer": 1,
    "explanation": "By strictly routing along X then Y, all turns from North/South to East/West are prohibited. Because packets can never turn back into X once in Y, closed dependency cycles cannot form."
  },
  {
    "id": "q8",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Advanced",
    "question": "According to the Turn Model (Glass & Ni), which two turns are prohibited in the West-First routing algorithm?",
    "options": [
      "North -> East and South -> East",
      "South -> West and North -> West",
      "East -> North and East -> South",
      "West -> North and West -> South"
    ],
    "answer": 1,
    "explanation": "West-First prohibits South -> West (breaking the clockwise cycle) and North -> West (breaking the counter-clockwise cycle). Packets heading west must do so first, after which they can adaptively route East, North, or South."
  },
  {
    "id": "q9",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Mastery",
    "question": "What is the core premise of Duato's Theorem for deadlock-free adaptive routing?",
    "options": [
      "Adaptive channels can have cycles in their dependency graph, provided there exists an acyclic escape subnetwork (e.g. using XY VCs) that blocked packets can always access.",
      "Every virtual channel must strictly maintain an acyclic channel dependency graph at all times.",
      "Deadlock can only be prevented if buffers are infinite.",
      "Packets must be reordered at every intermediate hop."
    ],
    "answer": 0,
    "explanation": "Duato proved that the adaptive channel subnetwork can contain cycles, as long as an acyclic escape channel subnetwork exists and packets can always transition to it when congested."
  },
  {
    "id": "q10",
    "module": "Track 5: Thermal & Congestion",
    "tier": "Core",
    "question": "Why does reactive Dynamic Thermal Management (DTM) struggle to prevent thermal overshoots in nanometer multi-core NoCs?",
    "options": [
      "Silicon thermal capacitance introduces a millisecond-scale heat diffusion lag, meaning temperature has already overshot by the time sensors react.",
      "Thermal sensors consume more power than the compute cores.",
      "Clock frequencies cannot be changed dynamically on silicon.",
      "Thermal hotspots only occur at absolute zero temperatures."
    ],
    "answer": 0,
    "explanation": "Heat diffusion takes milliseconds to reach physical sensors, while clock cycles run in sub-nanoseconds. Proactive ML prediction is needed to anticipate hotspots before the physical overshoot occurs."
  },
  {
    "id": "q11",
    "module": "Track 5: Thermal & Congestion",
    "tier": "Advanced",
    "question": "When reconstructing continuous on-chip thermal profiles from sparse sensors, why do standard Least Squares estimators degrade under real hardware noise?",
    "options": [
      "Physical thermal diodes experience non-Gaussian noise (dI/dt switching spikes, process variations, and outliers) that violate Gaussian assumptions.",
      "Least Squares can only be solved on quantum computers.",
      "Temperature is a discrete integer that cannot be interpolated.",
      "Thermal equations are purely linear and cannot have noise."
    ],
    "answer": 0,
    "explanation": "Real on-chip diodes suffer from inductive dI/dt noise and heavy-tailed outliers. Robust M-estimators or robust Kalman filters are required to prevent non-Gaussian sensor glitches from skewing the reconstructed temperature field."
  },
  {
    "id": "q12",
    "module": "Track 6: Chiplets & 3D NoC",
    "tier": "Core",
    "question": "In a 7-port 3D NoC router connecting Through-Silicon Vias (TSVs), what are the two additional physical ports compared to a standard 2D router?",
    "options": [
      "Left and Right",
      "Up and Down (vertical TSV links to upper and lower silicon tiers)",
      "Clock and Reset",
      "PCIe and USB"
    ],
    "answer": 1,
    "explanation": "A 3D NoC router adds 'Up' and 'Down' vertical physical ports connected to TSVs, expanding the internal crossbar from 5x5 to 7x7 crosspoints."
  }
];

let activeQuestions = [];
let currentIdx = 0;
let userScore = 0;
let timerInterval = null;
let timeLeft = 30;
let candidate = { name: "", org: "", mode: "full" };

function startQuiz() {
  candidate.name = document.getElementById("candidateName").value.trim() || "Hardware Architect";
  candidate.org = document.getElementById("candidateOrg").value.trim() || "Research Laboratory";
  candidate.mode = document.getElementById("assessmentMode").value;

  if (candidate.mode === "sprint") {
    activeQuestions = [...QUESTIONS_BANK].sort(() => 0.5 - Math.random()).slice(0, 6);
  } else {
    activeQuestions = [...QUESTIONS_BANK];
  }

  currentIdx = 0;
  userScore = 0;

  document.getElementById("stepRegistration").style.display = "none";
  document.getElementById("stepResult").style.display = "none";
  document.getElementById("stepQuiz").style.display = "block";

  loadQuestion(currentIdx);
}

function loadQuestion(idx) {
  if (idx >= activeQuestions.length) {
    finishQuiz();
    return;
  }

  const q = activeQuestions[idx];
  document.getElementById("quizProgress").textContent = `Question ${idx + 1} of ${activeQuestions.length}`;
  document.getElementById("quizModuleBadge").textContent = q.module;
  document.getElementById("quizTierBadge").textContent = q.tier;
  document.getElementById("quizQuestionText").textContent = q.question;

  const optionsContainer = document.getElementById("quizOptions");
  optionsContainer.innerHTML = "";

  q.options.forEach((opt, oIdx) => {
    const btn = document.createElement("button");
    btn.className = "noc-sim-select";
    btn.style.textAlign = "left";
    btn.style.padding = "0.75rem 1rem";
    btn.style.cursor = "pointer";
    btn.style.width = "100%";
    btn.style.fontSize = "0.92rem";
    btn.style.transition = "all 0.15s ease";
    btn.innerHTML = `<strong>${String.fromCharCode(65 + oIdx)}.</strong> ${opt}`;
    btn.onclick = () => checkAnswer(oIdx);
    optionsContainer.appendChild(btn);
  });

  document.getElementById("quizFeedback").style.display = "none";
  document.getElementById("nextBtn").style.display = "none";

  // Start Timer
  clearInterval(timerInterval);
  timeLeft = 35;
  document.getElementById("quizTimer").textContent = `⏱️ ${timeLeft}s`;
  timerInterval = setInterval(() => {
    timeLeft--;
    document.getElementById("quizTimer").textContent = `⏱️ ${timeLeft}s`;
    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      checkAnswer(-1); // Timeout
    }
  }, 1000);
}

function checkAnswer(selectedIdx) {
  clearInterval(timerInterval);
  const q = activeQuestions[currentIdx];
  const isCorrect = (selectedIdx === q.answer);

  if (isCorrect) {
    userScore += 100 + timeLeft * 2;
  }

  document.getElementById("quizScore").textContent = `Score: ${userScore} pts`;

  // Disable option clicks
  const optionBtns = document.getElementById("quizOptions").children;
  for (let i = 0; i < optionBtns.length; i++) {
    optionBtns[i].onclick = null;
    optionBtns[i].style.cursor = "default";
    if (i === q.answer) {
      optionBtns[i].style.background = "rgba(34, 197, 94, 0.15)";
      optionBtns[i].style.borderColor = "#22c55e";
    } else if (i === selectedIdx && !isCorrect) {
      optionBtns[i].style.background = "rgba(239, 68, 68, 0.15)";
      optionBtns[i].style.borderColor = "#ef4444";
    }
  }

  // Show Feedback
  const fb = document.getElementById("quizFeedback");
  fb.style.display = "block";
  if (isCorrect) {
    fb.style.background = "rgba(34, 197, 94, 0.1)";
    fb.style.border = "1px solid rgba(34, 197, 94, 0.3)";
    fb.style.color = "#166534";
    fb.innerHTML = `<strong>✓ Correct!</strong> ${q.explanation}`;
  } else {
    fb.style.background = "rgba(239, 68, 68, 0.1)";
    fb.style.border = "1px solid rgba(239, 68, 68, 0.3)";
    fb.style.color = "#991b1b";
    fb.innerHTML = `<strong>✗ Incorrect.</strong> The correct answer is <strong>${String.fromCharCode(65 + q.answer)}</strong>.<br>${q.explanation}`;
  }

  document.getElementById("nextBtn").style.display = "inline-flex";
}

function nextQuestion() {
  currentIdx++;
  loadQuestion(currentIdx);
}

function finishQuiz() {
  document.getElementById("stepQuiz").style.display = "none";
  document.getElementById("stepResult").style.display = "block";

  const maxScore = activeQuestions.length * 170;
  const accuracy = Math.round((userScore / (activeQuestions.length * 100)) * 100);
  document.getElementById("resultSummary").innerHTML = `Candidate: <strong>${candidate.name}</strong> | Total Score: <strong>${userScore}</strong> pts | Accuracy: <strong>${accuracy}%</strong>`;

  // Set Certificate Fields
  document.getElementById("certCandidateName").textContent = candidate.name;
  document.getElementById("certCandidateOrg").textContent = candidate.org;
  document.getElementById("certScore").textContent = `${userScore} pts (${accuracy}%)`;

  const now = new Date();
  const dateStr = now.toISOString().split("T")[0];
  document.getElementById("certDate").textContent = dateStr;

  // Generate deterministic verification hash
  let hashVal = 0;
  const hashRaw = `${candidate.name}-${userScore}-${dateStr}`;
  for (let i = 0; i < hashRaw.length; i++) {
    hashVal = (hashVal << 5) - hashVal + hashRaw.charCodeAt(i);
    hashVal |= 0;
  }
  const certId = `NOC-CERT-${now.getFullYear()}-${Math.abs(hashVal).toString(16).toUpperCase().padStart(6, '0')}`;
  document.getElementById("certHash").textContent = certId;
}

function downloadCertificateSVG() {
  const name = document.getElementById("certCandidateName").textContent;
  const org = document.getElementById("certCandidateOrg").textContent;
  const score = document.getElementById("certScore").textContent;
  const hash = document.getElementById("certHash").textContent;
  const date = document.getElementById("certDate").textContent;

  const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" width="800" height="560">
    <rect width="800" height="560" fill="#ffffff" />
    <rect x="20" y="20" width="760" height="520" fill="none" stroke="#d4af37" stroke-width="4" />
    <rect x="28" y="28" width="744" height="504" fill="none" stroke="#0f172a" stroke-width="1.5" />
    
    <text x="400" y="80" text-anchor="middle" font-family="'Inter', sans-serif" font-size="12" font-weight="700" fill="#64748b" letter-spacing="3">NOC-LAB ACADEMIC CREDENTIAL REGISTRY</text>
    <text x="400" y="130" text-anchor="middle" font-family="'Inter', sans-serif" font-size="28" font-weight="900" fill="#0f172a">CERTIFICATE OF ACHIEVEMENT</text>
    <text x="400" y="175" text-anchor="middle" font-family="'Inter', sans-serif" font-size="14" fill="#475569">This is to proudly certify that</text>
    
    <text x="400" y="235" text-anchor="middle" font-family="'Inter', sans-serif" font-size="32" font-weight="800" fill="#1e3a8a">${name}</text>
    <line x1="200" y1="250" x2="600" y2="250" stroke="#cbd5e1" stroke-width="2" />
    
    <text x="400" y="285" text-anchor="middle" font-family="'Inter', sans-serif" font-size="16" font-style="italic" fill="#475569">${org}</text>
    <text x="400" y="340" text-anchor="middle" font-family="'Inter', sans-serif" font-size="15" fill="#334155">has mastered Network-on-Chip (NoC) Architecture,</text>
    <text x="400" y="365" text-anchor="middle" font-family="'Inter', sans-serif" font-size="15" fill="#334155">Router Microarchitecture &amp; Deadlock Avoidance Theory.</text>
    
    <line x1="80" y1="440" x2="720" y2="440" stroke="#e2e8f0" stroke-width="1" />
    
    <text x="120" y="475" font-family="'Inter', sans-serif" font-size="12" fill="#64748b">SCORE: <tspan font-weight="700" fill="#0f172a">${score}</tspan></text>
    <text x="400" y="475" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="12" fill="#64748b">HASH: <tspan font-weight="700" fill="#0f172a">${hash}</tspan></text>
    <text x="680" y="475" text-anchor="end" font-family="'Inter', sans-serif" font-size="12" fill="#64748b">DATE: <tspan font-weight="700" fill="#0f172a">${date}</tspan></text>
  </svg>`;

  const blob = new Blob([svgContent], { type: "image/svg+xml" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Certificate_${name.replace(/\s+/g, '_')}_NoC.svg`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function restartQuiz() {
  document.getElementById("stepResult").style.display = "none";
  document.getElementById("stepRegistration").style.display = "block";
}
</script>
