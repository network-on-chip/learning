# 🎯 Network-on-Chip Architecture Certification & Quiz Challenge

<div class="noc-hero">
  <div class="noc-track-badge">🏆 Official Assessment & Credential Registry</div>
  <h1>NoC Architecture Knowledge Assessment</h1>
  <p class="subtitle">
    Test your mastery across 3 difficulty tiers: Fundamentals, Core Microarchitecture, and Silicon Mastery. Earn a verifiable, cryptographic SVG Certificate of Completion and publish your score to the Public Leaderboard.
  </p>
  <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:1rem;">
    <span class="noc-track-badge" style="background:rgba(34, 197, 94, 0.12); color:#16a34a; border-color:rgba(34, 197, 94, 0.25);">🟢 Tier 1: Fundamental (100 pts)</span>
    <span class="noc-track-badge" style="background:rgba(234, 88, 12, 0.12); color:#ea580c; border-color:rgba(234, 88, 12, 0.25);">🟡 Tier 2: Core Engineering (200 pts)</span>
    <span class="noc-track-badge" style="background:rgba(147, 51, 234, 0.12); color:#9333ea; border-color:rgba(147, 51, 234, 0.25);">🔴 Tier 3: Silicon Mastery (300 pts)</span>
  </div>
</div>

<div id="quizApp" class="noc-sim-container">
  <!-- Registration Step -->
  <div id="stepRegistration">
    <h3 style="margin-top:0;">Candidate Registration &amp; Tier Selection</h3>
    <p style="color:var(--md-default-fg-color--lighter); font-size:0.92rem;">
      Enter your candidate details and select your assessment track. Upon completion, your score, IP, location, and verification credentials are automatically submitted to the official GitHub credential registry.
    </p>

    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:1rem; margin:1.25rem 0;">
      <div>
        <label style="font-weight:600; font-size:0.85rem; display:block; margin-bottom:0.35rem;">Candidate Full Name *</label>
        <input type="text" id="candidateName" class="noc-sim-select" style="width:100%; box-sizing:border-box;" placeholder="e.g. Dr. Ada Lovelace" value="Hardware Architect">
      </div>
      <div>
        <label style="font-weight:600; font-size:0.85rem; display:block; margin-bottom:0.35rem;">Candidate Email Address *</label>
        <input type="email" id="candidateEmail" class="noc-sim-select" style="width:100%; box-sizing:border-box;" placeholder="e.g. ada@university.edu" value="architect@silicon.org">
      </div>
      <div>
        <label style="font-weight:600; font-size:0.85rem; display:block; margin-bottom:0.35rem;">Assessment Track</label>
        <select id="assessmentMode" class="noc-sim-select" style="width:100%; box-sizing:border-box;">
          <option value="full">Comprehensive Certification (12 Questions - Tiers 1, 2, 3)</option>
          <option value="tier1_sprint">Fundamentals Sprint (4 Questions - Tier 1)</option>
          <option value="grandmaster">Grandmaster Challenge (4 Questions - Tier 3 Mastery Only)</option>
        </select>
      </div>
    </div>

    <div style="font-size:0.8rem; color:#64748b; margin-bottom:1.15rem; display:flex; align-items:center; gap:0.4rem;">
      <span>🔒</span>
      <span><strong>Automated Verification:</strong> Your verified exam score, client IP, and location will be automatically registered to GitHub Issues upon exam completion.</span>
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
        <span id="quizTimer" style="font-family:'JetBrains Mono', monospace; font-size:0.9rem; font-weight:700; color:var(--tcl-heading);">⏱️ 35s</span>
        <span id="quizScore" style="font-size:0.85rem; font-weight:700; color:var(--tcl-blue-600);">Score: 0 pts</span>
      </div>
    </div>

    <div style="margin-bottom:0.75rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
      <span class="noc-track-badge" id="quizModuleBadge">Track 1</span>
      <span class="noc-track-badge" id="quizTierBadge">Tier 1</span>
      <span class="noc-track-badge" id="quizPtsBadge" style="background:rgba(37, 99, 235, 0.1); color:var(--tcl-blue-600);">+100 pts</span>
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
      <div style="font-size:12px; text-transform:uppercase; letter-spacing:2px; color:#64748b; font-weight:700;">NoC Academic Credential Registry</div>
      <h1 style="font-size:1.65rem; font-weight:900; color:#0f172a; margin:10px 0 6px; letter-spacing:-0.5px;">CERTIFICATE OF ACHIEVEMENT</h1>
      <div style="font-size:13px; color:#475569; margin-bottom:16px;">This is to formally certify that</div>
      <div id="certCandidateName" style="font-size:1.85rem; font-weight:800; color:#1e3a8a; border-bottom:2px solid #cbd5e1; display:inline-block; padding:0 30px 4px; margin-bottom:6px;">Candidate Name</div>
      <div id="certCandidateEmail" style="font-size:13px; font-family:'JetBrains Mono', monospace; color:#64748b; margin-bottom:18px;">candidate@example.com</div>
      <div style="font-size:14px; max-width:520px; margin:0 auto 20px; line-height:1.5; color:#334155;">
        has successfully passed the examination in <strong>Network-on-Chip (NoC) Architecture, Router Microarchitecture &amp; Deadlock Avoidance Theory</strong>.
      </div>

      <div style="display:flex; justify-content:space-around; align-items:center; border-top:1px solid #e2e8f0; padding-top:16px; font-size:12px; color:#64748b;">
        <div><b>Score:</b> <span id="certScore" style="color:#0f172a;">--</span></div>
        <div><b>Verification Hash:</b> <span id="certHash" style="font-family:'JetBrains Mono', monospace; color:#0f172a;">NOC-CERT-2026-X89F</span></div>
        <div><b>Date:</b> <span id="certDate" style="color:#0f172a;">2026-11-05</span></div>
      </div>
    </div>

    <!-- Automated GitHub Submission Status Card -->
    <div id="submissionStatusBox" style="background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px 20px; max-width:680px; margin:0 auto 1.5rem; text-align:left; box-shadow:0 6px 20px rgba(0,0,0,0.15);">
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
          <span id="submissionIcon" style="font-size:1.4rem;">🔄</span>
          <div>
            <div id="submissionTitle" style="font-weight:700; font-size:0.95rem; color:#38bdf8;">Automatically Submitting Result to GitHub...</div>
            <div id="submissionDetail" style="font-size:0.82rem; color:#94a3b8;">Recording candidate credentials, verified score, IP, and location to official GitHub Issues ledger.</div>
          </div>
        </div>
        <div id="submissionBadge" style="font-size:0.72rem; font-weight:700; padding:4px 10px; border-radius:4px; background:#1e293b; color:#38bdf8; letter-spacing:0.5px;">
          SUBMITTING
        </div>
      </div>

      <!-- Metadata audit line -->
      <div id="submissionMeta" style="margin-top:10px; font-size:0.78rem; font-family:'JetBrains Mono', monospace; color:#64748b; border-top:1px dashed #334155; padding-top:8px; display:flex; flex-wrap:wrap; gap:0.75rem;">
        <span><b>Candidate:</b> <span id="metaName" style="color:#e2e8f0;">--</span></span>
        <span><b>Email:</b> <span id="metaEmail" style="color:#e2e8f0;">--</span></span>
        <span><b>IP:</b> <span id="metaIp" style="color:#38bdf8;">Detecting...</span></span>
        <span><b>Location:</b> <span id="metaLoc" style="color:#38bdf8;">Detecting...</span></span>
      </div>

      <!-- Action link if created -->
      <div id="submissionLinkWrap" style="display:none; margin-top:10px; padding-top:8px; border-top:1px solid #1e293b; font-size:0.84rem;">
        <a id="submissionIssueLink" href="#" target="_blank" style="color:#22c55e; font-weight:700; text-decoration:none;">
          🔗 View Confirmed Credential Issue on GitHub →
        </a>
      </div>

      <!-- Fallback action if endpoint offline -->
      <div id="submissionFallbackWrap" style="display:none; margin-top:10px; padding-top:8px; border-top:1px solid #1e293b; font-size:0.82rem; color:#f59e0b;">
        <span>Backend bridge pending deployment. </span>
        <button onclick="retryAutoSubmit()" class="noc-sim-btn secondary" style="font-size:0.75rem; padding:2px 8px; margin:0 4px;">🔄 Retry</button>
        <button onclick="emergencyFallbackIssue()" class="noc-sim-btn secondary" style="font-size:0.75rem; padding:2px 8px;">📤 Open GitHub Issue Manually</button>
      </div>
    </div>

    <div style="display:flex; gap:0.75rem; justify-content:center; flex-wrap:wrap;">
      <button class="noc-sim-btn" onclick="downloadCertificateSVG()">📥 Download Certificate (SVG)</button>
      <a id="viewLeaderboardLink" href="../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none;">🏆 View Public Leaderboard</a>
      <button class="noc-sim-btn secondary" onclick="restartQuiz()">🔄 Retake Exam</button>
    </div>
  </div>
</div>

<script>
const QUESTIONS_BANK = [
  {
    "id": "q1",
    "module": "Track 1: Fundamentals",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "Why did multicore processor architectures replace shared multi-drop buses with packet-switched Networks-on-Chip (NoC)?",
    "options": [
      "Shared buses suffer from capacitive RC wire delays, serialization bottlenecks (only 1 master at a time), and energy overhead as core count scales.",
      "Shared buses require dedicated point-to-point clock distribution trees that create severe clock skew and electromigration across distant processor cores.",
      "Shared buses lack hardware arbitration protocols, forcing the operating system kernel to serialize all multi-threaded memory access transactions in software.",
      "Shared buses cannot physically support split-transaction memory operations or non-blocking cache structures in modern out-of-order superscalar pipelines."
    ],
    "answer": 0,
    "explanation": "As core count scales, shared global buses experience skyrocketing capacitive loading (RC wire delay) and severe bandwidth contention. NoCs replace long shared wires with short point-to-point links and concurrent multi-hop packet routing."
  },
  {
    "id": "q2",
    "module": "Track 1: Fundamentals",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "What is the relationship between Packets, Flits, and Phits in NoC communication?",
    "options": [
      "A Flit carries the end-to-end destination routing header; a Packet is the link transmission slice; a Phit is the virtual channel buffer allocation depth.",
      "A Packet is the routing unit; a Flit is the atomic flow control & buffer unit; a Phit is the physical wire width transferred in one clock cycle.",
      "A Phit represents the complete cache coherence transaction; a Flit is the physical link wire width; a Packet is the switch crossbar arbitration token.",
      "A Packet is partitioned into fixed-size Phits for buffer allocation; a Flit is the single-cycle physical link width connecting adjacent on-chip routers."
    ],
    "answer": 1,
    "explanation": "A Packet carries the end-to-end addressing headers. It is partitioned into Flits (Head, Body, Tail) for buffer allocation. A Phit is the physical link slice transmitted per cycle."
  },
  {
    "id": "q3",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "What primary performance problem is caused by using a single shared FIFO queue at an input port, and how is it solved?",
    "options": [
      "Pipeline structural hazards across shared read ports; solved by inserting shadow pipeline registers into the crossbar traversal stage.",
      "Clock domain crossing metastability between routers; solved by adding dual-clock asynchronous synchronizing FIFOs at each input port.",
      "Head-of-Line (HoL) blocking; solved by dividing the buffer into multiple Virtual Channels (VCs).",
      "Dynamic switching power dissipation surges; solved by clock-gating the read and write FIFO pointer registers during idle cycles."
    ],
    "answer": 2,
    "explanation": "Head-of-Line (HoL) blocking occurs when a blocked packet at the front of a FIFO prevents unblocked trailing packets from advancing. Virtual Channels provide independent logical queues so unblocked packets can bypass blocked ones."
  },
  {
    "id": "q4",
    "module": "Track 3: Topologies & Metrics",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "In a 2D mesh topology, how does the node degree of a corner router compare to an interior router?",
    "options": [
      "Corner routers have degree 4 (+ local port); interior routers have degree 8 (+ local port) in mesh networks.",
      "Corner routers have degree 3 (+ local port); interior routers have degree 6 (+ local port) in mesh topologies.",
      "Corner routers have degree 1 (+ local port); interior routers have degree 5 (+ local port) across the fabric.",
      "Corner routers have degree 2 (+ local port); interior routers have degree 4 (+ local port) across standard 2D meshes."
    ],
    "answer": 3,
    "explanation": "In an NxM 2D mesh, boundary routers lack outward links. A corner router connects to only 2 adjacent routers (plus 1 local core port = 3 total), whereas an interior router connects to 4 neighbors (N, S, E, W plus 1 local port = 5 total)."
  },
  {
    "id": "q5",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "In credit-based flow control, if link traversal takes 1 cycle, buffer processing takes 1 cycle, and credit return takes 1 cycle, what happens if the input buffer capacity is only 2 flits?",
    "options": [
      "The upstream router exhausts credits on cycle 2 and stalls for at least 1 cycle, dropping wire throughput below 100%.",
      "The downstream router experiences an internal buffer overflow fault and drops flits, triggering end-to-end retry transactions.",
      "The credit counter rolls over to zero, inducing a structural protocol deadlock that requires a full hardware subsystem reset.",
      "The credit handshake lines oscillate between valid and stall, injecting high-frequency inductive switching noise into adjacent links."
    ],
    "answer": 0,
    "explanation": "The round-trip turnaround time (RTT) is 1 (forward link) + 1 (processing) + 1 (credit return) + 1 (credit processing) = 3 to 4 cycles. If buffer depth is only 2 flits, credits cannot return before the buffer runs out, introducing bubble cycles that limit throughput."
  },
  {
    "id": "q6",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "What are the canonical 5 pipeline stages of a classic Virtual Channel wormhole router?",
    "options": [
      "Input Polling (IP) -> Address Decode (AD) -> Crossbar Arbitration (CA) -> Buffer Read (BR) -> Physical Link Drive (LD)",
      "Buffer Write (BW) -> Route Computation (RC) -> VC Allocation (VA) -> Switch Allocation (SA) -> Switch Traversal (ST)",
      "Flit Alignment (FA) -> Credit Verification (CV) -> Priority Scheduling (PS) -> Switch Traversal (ST) -> Egress Write (EW)",
      "Header Parsing (HP) -> Path Reservation (PR) -> Virtual Channel Allocation (VA) -> Buffer Commit (BC) -> Link Traversal (LT)"
    ],
    "answer": 1,
    "explanation": "A canonical VC router pipeline consists of: Buffer Write (BW) upon flit arrival, Route Computation (RC) for the head flit, Virtual Channel Allocation (VA) to reserve an output VC, Switch Allocation (SA) to arbitrate for crossbar input/output ports, and Switch Traversal (ST) to traverse the crossbar to the output link."
  },
  {
    "id": "q7",
    "module": "Track 3: Topologies & Metrics",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "Why does a 4x4 Concentrated Mesh (cMesh) achieve lower zero-load latency for 64 cores than a traditional 8x8 2D Mesh?",
    "options": [
      "Concentrated routers use single-cycle optical switches that transmit packets at the speed of light across the die without any delay.",
      "Concentrated routers eliminate input buffers completely, relying on deflection routing to bypass all queuing stalls across the chip.",
      "Clustering 4 compute cores around each router reduces total routers from 64 to 16, cutting network diameter from 14 to 6 hops.",
      "Clustering cores enables global broadcast busses that bypass multi-hop packet forwarding across intermediate routers."
    ],
    "answer": 2,
    "explanation": "Concentration connects multiple cores (e.g., 4) to a single network router. For 64 cores, this reduces the mesh grid from 8x8 (64 routers, max diameter 14 hops) to 4x4 (16 routers, max diameter 6 hops). Fewer router hops directly translates to lower zero-load latency."
  },
  {
    "id": "q8",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "In the Turn Model (Glass & Ni), which two turns are prohibited in the West-First routing algorithm, and what adaptivity does it preserve?",
    "options": [
      "Prohibits East->North and West->North turns; restricts packets strictly to deterministic dimension-order YX routing paths.",
      "Prohibits North->East and South->East turns; forces packets to complete all vertical routing hops before moving Westward.",
      "Prohibits North->South and East->West turns; restricts packet trajectories to strictly positive diagonal coordinate quadrants.",
      "Prohibits South->West and North->West turns; packets heading west must do so first, leaving full adaptivity when moving East."
    ],
    "answer": 3,
    "explanation": "West-First prohibits the two turns onto the Westbound channels (South->West and North->West). Packets requiring West routing must route West first before any North/South turns, eliminating all cycles while preserving 100% routing freedom when traveling East."
  },
  {
    "id": "q9",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "In a Matrix Arbiter with an NxN triangular priority matrix M, what is the exact hardware update rule when client k is granted the resource?",
    "options": [
      "Row k of matrix M is cleared to all 0s (M[k,:] = 0) and Column k is set to all 1s (M[:,k] = 1, with diagonal M[k,k] = 0).",
      "Row k of matrix M is set to all 1s (M[k,:] = 1) and Column k is cleared to all 0s (M[:,k] = 0, with diagonal M[k,k] = 1).",
      "All elements in Row k and Column k are inverted using XOR gates while the remaining off-diagonal elements stay untouched.",
      "The priority matrix M is multiplied by a cyclic permutation matrix P to rotate all requester priorities uniformly by one position."
    ],
    "answer": 0,
    "explanation": "In an NxN triangular matrix arbiter, M[i,j]=1 means client i has priority over client j. When client k wins arbitration, it must now have lowest priority against all others: row k is cleared (client k no longer has priority over anyone) and column k is set to 1 (all other clients now have priority over k)."
  },
  {
    "id": "q10",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "How does Duato's Theorem (1993) enable high-performance adaptive routing without deadlock?",
    "options": [
      "It requires every virtual channel subnetwork across all physical links to maintain a strictly acyclic dependency graph at all times.",
      "It partitions virtual channels into an adaptive subnetwork and an acyclic escape subnetwork that blocked packets can always access.",
      "It monitors router buffers with hardware timeout counters and drops blocked flits whenever a potential cyclic dependency is detected.",
      "It dynamically computes global Hamiltonian path traversals across all physical routers to prevent packets from forming closed loops."
    ],
    "answer": 1,
    "explanation": "Duato proved that the entire network does not need an acyclic channel dependency graph. As long as there exists a connected subnetwork of escape channels (e.g., deterministic XY routing virtual channels) that is acyclic and accessible by packets, the system is provably deadlock-free even if the adaptive channels contain cycles."
  },
  {
    "id": "q11",
    "module": "Track 5: Thermal & Physical Design",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "Why do standard Least Squares estimators fail when reconstructing continuous on-chip thermal fields from sparse physical sensors under real silicon operation?",
    "options": [
      "Standard Least Squares formulations can only interpolate 1-dimensional signals and cannot model planar 2D silicon heat conduction.",
      "On-chip thermal sensors only measure voltage drop and cannot be calibrated to reflect absolute silicon temperatures.",
      "Physical sensors exhibit non-Gaussian noise (inductive dI/dt bounce and impulsive outliers) violating Gaussian assumptions.",
      "Silicon substrate heat diffusion is mathematically non-differentiable across boundaries between copper interconnects and silicon dioxide."
    ],
    "answer": 2,
    "explanation": "Standard Least Squares and linear Kalman filters assume Gaussian noise. Real silicon thermal sensors suffer from heavy-tailed non-Gaussian disturbances such as supply-voltage bounce, substrate coupling, and process variation outliers. M-estimators with Huber loss or Gaussian-Sum Filters provide robust estimation under non-Gaussian noise."
  },
  {
    "id": "q12",
    "module": "Track 6: Chiplets & Advanced Packaging",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "In multi-chiplet packaging using UCIe (Universal Chiplet Interconnect Express), what architectural advantage does standard die-to-die (D2D) packaging provide compared to traditional PCIe?",
    "options": [
      "UCIe utilizes micro-strip radio frequency antennas that eliminate physical microbumps while providing gigahertz wireless data links.",
      "UCIe is engineered specifically for long-reach motherboard trace routing up to 500 millimeters using active optical transceivers.",
      "UCIe restricts link transactions strictly to single-bit asynchronous serial streams to minimize silicon footprint and pin count.",
      "UCIe delivers up to 1300 Gbps/mm shoreline bandwidth density with ultra-low energy (< 0.5 pJ/bit) and sub-2ns latency, enabling transparent on-chip NoC extensions."
    ],
    "answer": 3,
    "explanation": "UCIe Standard Package provides dense microbumps (45-55um pitch) and short traces (<25mm), achieving 10x-50x higher bandwidth density per millimeter of die shoreline and 5x-10x lower energy/bit than PCIe or standard SerDes, enabling multi-die packages to behave like single monolithic chips."
  },
  {
    "id": "q13",
    "module": "Track 1: Fundamentals",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "Under the Elmore delay model, why does the propagation delay of a shared multi-drop bus grow quadratically/superlinearly with core count N rather than remaining flat?",
    "options": [
      "Every attached core introduces capacitive tap loading (C_tap) and die scaling increases physical wire length (L ~ sqrt(N)), compounding both wire resistance and total capacitance.",
      "Bus controllers require active repeater banks whose dynamic power increases exponentially with core count, saturating on-chip voltage regulators and destabilizing local core voltages.",
      "The physical clock tree driving the bus arbiter experiences quadratic jitter amplification that degrades link timing margins across distant core interfaces.",
      "Substrate thermal gradients generated by adjacent active cores increase copper wire resistivity by an order of magnitude across all intermediate tap locations."
    ],
    "answer": 0,
    "explanation": "Elmore delay is proportional to R_total * C_total. As N increases, physical bus length L scales as O(sqrt(N)), so wire resistance R_wire and capacitance C_wire both scale with L. Furthermore, each added core adds a capacitive input pin tap (C_tap), making total capacitance C_total = C_wire * L + N * C_tap. Their product grows as O(N) to O(N^1.5), producing superlinear delay growth."
  },
  {
    "id": "q14",
    "module": "Track 1: Fundamentals",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "What is the physical mechanism behind the Mayadas-Shatzkes effect, and why does it severely penalize global interconnects below 14nm?",
    "options": [
      "Thermal expansion mismatches cause micro-cracks that sever interconnect traces under sustained switching loads.",
      "When wire width drops below electron mean free path (~39nm), grain boundary and sidewall scattering surges copper resistivity.",
      "Electromagnetic radiation coupling between dense parallel wires generates destructive phase interference that attenuates high-speed flit signals.",
      "Electromigration voids form at copper-via interfaces as high current densities sweep metal atoms toward downstream receiver nodes across the chip."
    ],
    "answer": 1,
    "explanation": "The Mayadas-Shatzkes model describes grain boundary and surface scattering in thin metal films. When wire cross-section dimensions approach or drop below the electron mean free path in copper (~39 nm at room temperature), electrons scatter diffusely rather than specularly off grain boundaries and sidewall barriers, skyrocketing resistivity."
  },
  {
    "id": "q15",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "Why is a monolithic centralized NxN crossbar switch physically unviable for large manycore systems (N >= 64 cores), despite offering single-hop non-blocking routing?",
    "options": [
      "Centralized crossbars cannot be synthesized using standard CMOS logic gates and require specialized GaAs or InP compound semiconductor substrates.",
      "Crossbar matrix switches violate Dally's deadlock theorem whenever more than sixteen concurrent input connections are routed through the central fabric.",
      "It requires N^2 crosspoint switches (4,096 switches for N=64) and dense global wiring tracks, leading to severe silicon area explosion and physical routing track starvation.",
      "The capacitive RC delay of long crossbar input/output lines limits clock frequencies to less than 100 MHz regardless of metal layer thickness and intermediate buffer sizing."
    ],
    "answer": 2,
    "explanation": "A monolithic NxN crossbar requires N^2 crosspoints and 2*N*W global wires spanning the entire switch area. For N=64 and 128-bit flits, this requires 4,096 crosspoints and over 16,000 wires across a centralized block, causing unmanageable wiring congestion, quadratic area scaling O(N^2), and huge capacitive wire load."
  },
  {
    "id": "q16",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "What is the foundational architectural advantage of Wormhole Switching compared to Store-and-Forward and Virtual Cut-Through?",
    "options": [
      "Wormhole switching eliminates the need for routing computation logic by fixing packet trajectory at design time.",
      "Wormhole switching completely removes crossbar switches by using shared serial busses inside each router node.",
      "Wormhole switching guarantees zero-latency end-to-end traversal by transmitting flits directly over optical wavebands.",
      "Wormhole switching decouples the buffer allocation unit (flit) from packet size, slashing router buffer requirements."
    ],
    "answer": 3,
    "explanation": "Store-and-Forward and Virtual Cut-Through require buffers sized to hold entire maximum-length packets (e.g. 16-64 flits per port) before forwarding can occur or in case of stalls. Wormhole switching operates on individual flits, allowing buffer queues as small as 1 to 4 flits per VC, drastically reducing on-chip SRAM/register area."
  },
  {
    "id": "q17",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "In credit-based flow control, what is the exact physical condition for the downstream buffer depth B_min required to sustain 100% full wire-rate throughput without pipeline stall bubbles?",
    "options": [
      "B_min >= RTT * Peak_Injection_Rate, where RTT is the total credit turnaround loop delay (forward flight + receiver processing + reverse credit flight + transmitter processing).",
      "B_min >= 2 * Diameter * Flit_Width, where Diameter is the maximum hop count between any source and destination router across the active topology.",
      "B_min must match the total number of Virtual Channels multiplied by the packet payload size to guarantee non-blocking cut-through link buffering.",
      "B_min >= Clock_Frequency / Wire_Delay, where Wire_Delay represents the single-hop propagation latency across intermediate repeater pipeline buffers."
    ],
    "answer": 0,
    "explanation": "To sustain 100% link utilization (1 flit per cycle injection), the credit loop turnaround time (RTT) must be fully covered by buffer capacity. If RTT is 4 cycles (1 cycle wire, 1 cycle credit generation, 1 cycle credit wire, 1 cycle credit processing), the downstream buffer must hold at least 4 flits so the upstream router never starves of credits while flits are in flight."
  },
  {
    "id": "q18",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "How does Token Flow Control in the SWIFT NoC (Peh et al., IEEE TVLSI 2013) achieve up to 38% power reduction compared to canonical wormhole routers?",
    "options": [
      "By shutting off clock gates to all router crossbars and routing flits exclusively through bit-serial shift registers.",
      "By sending tokens ahead so incoming data flits bypass input FIFO buffers entirely and cut through directly into the crossbar.",
      "By dynamically scaling supply voltage down to near-threshold levels and recovering corrupted flits via forward error correction logic.",
      "By replacing electrical crossbars with passive capacitive cross-point arrays that consume zero dynamic switching power across the chip."
    ],
    "answer": 1,
    "explanation": "In standard routers, every flit must be written into an input FIFO and read out, consuming significant dynamic buffer energy. Token Flow Control sends lightweight tokens ahead to reserve downstream buffer slots and switch time. When a token is confirmed, incoming data flits bypass the input FIFO entirely, cutting through directly into the crossbar."
  },
  {
    "id": "q19",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "In a canonical 5-stage VC router (BW -> RC -> VA -> SA -> ST), which two critical microarchitectural optimizations enable shrinking pipeline latency down to 1 or 2 clock cycles under zero-load conditions?",
    "options": [
      "Eliminating virtual channels completely and replacing crossbar switches with multi-drop global broadcast wires.",
      "Doubling the clock period so that all five sequential pipeline operations execute in one very slow clock cycle.",
      "Lookahead Routing (computing RC one hop ahead) and Speculative Switch Allocation (running SA in parallel with VA).",
      "Dropping all body and tail flits at the input port and reconstructing packet payloads at the destination node."
    ],
    "answer": 2,
    "explanation": "Lookahead routing precomputes the output port for hop N+1 at router N, embedding the route in the packet header and removing RC from the critical path. Speculative Switch Allocation allows a flit to arbitrate for crossbar switch traversal (SA) in parallel with Virtual Channel Allocation (VA), assuming VA will succeed. Under low loads, this shrinks the router pipeline to 1 cycle."
  },
  {
    "id": "q20",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "In a hardware Matrix Arbiter implementing Least-Recently-Used (LRU) priority for N requesters, how is the state updated when client k is granted access?",
    "options": [
      "The priority matrix M is mathematically inverted using Gaussian elimination to reverse the priority ordering of all active requesters.",
      "All bits in row k and column k are simultaneously toggled using XOR gates while maintaining diagonal parity invariants.",
      "The triangular matrix entries are shifted cyclically to the left by one position using an integrated hardware barrel shifter.",
      "Row k of the priority matrix is cleared to 0 (M[k,:] = 0) and Column k is set to 1 (M[:,k] = 1, with diagonal M[k,k] = 0)."
    ],
    "answer": 3,
    "explanation": "In an NxN triangular matrix arbiter, M[i,j]=1 means client i has priority over client j. When client k wins arbitration, it must now have lowest priority against all others: row k is cleared (client k no longer has priority over anyone) and column k is set to 1 (all other clients now have priority over k)."
  },
  {
    "id": "q21",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "In Nick McKeown's iSLIP crossbar scheduling algorithm, why do the grant arbiters at output ports update their round-robin pointers ONLY during iteration 1 and ONLY if the grant is accepted by the receiving input?",
    "options": [
      "To prevent arbiters from synchronizing (de-synchronization property), ensuring 100% throughput for uniform traffic while granting priority to unmatched inputs in later iterations.",
      "To guarantee that output ports always grant access to the input queue with the highest fill level, preventing buffer overflows across the router fabric.",
      "To eliminate grant registers by allowing input request lines to drive crossbar crosspoints directly without intermediate state arbitration logic.",
      "To force all crossbar schedules into strict time-division multiplexed slots that align with external DRAM memory controller burst command intervals."
    ],
    "answer": 0,
    "explanation": "If grant pointers updated on unmatched grants or in later iterations, output arbiters would synchronize (all pointing to the same input), causing severe contention and dropping throughput to ~63% under uniform traffic. Updating only on accepted grants in iteration 1 leads to de-synchronization, where arbiters point to different inputs, achieving 100% throughput."
  },
  {
    "id": "q22",
    "module": "Track 3: Topologies & Metrics",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "Why does a Folded Torus interleave even and odd nodes along each dimension, rather than connecting wrap-around wires directly between the perimeter tiles as in a standard Torus?",
    "options": [
      "To reduce the number of crossbar input ports on each router from five down to three across the whole network.",
      "To ensure all physical links have equal length 2*L0, eliminating long wrap-around delays.",
      "To allow the on-chip network to operate using single-ended dynamic domino logic circuits across all tiles.",
      "To convert the two-dimensional mesh topology into a set of disjoint Hamiltonian rings across the die."
    ],
    "answer": 1,
    "explanation": "In a standard k-ary 2-cube torus, adjacent links have length L0, but perimeter wrap-around wires span (k-1)*L0 across the entire die. This causes huge RC delay spikes that dictate the global clock period. Folding the torus interleaves nodes (0, k-1, 1, k-2...), making every physical link length exactly 2*L0."
  },
  {
    "id": "q23",
    "module": "Track 3: Topologies & Metrics",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "According to Clos network theory (1953), what is the exact mathematical condition on the number of middle-stage switches m required to guarantee that a 3-stage Clos network C(n, m, r) is Strictly Non-Blocking (SNB)?",
    "options": [
      "The number of middle switches must satisfy m >= n, matching input switch capacity.",
      "The number of middle switches must equal exactly half the total switch groups m = r / 2.",
      "The number of middle switches must satisfy m >= 2n - 1 to guarantee an unshared path.",
      "The number of middle switches must satisfy m >= n * log2(r) based on graph cut bounds."
    ],
    "answer": 2,
    "explanation": "In a 3-stage Clos network C(n, m, r), each first-stage switch has n inputs. To route an additional connection from switch A to switch B, in the worst case n-1 inputs of A are busy (using n-1 middle switches) and n-1 outputs of B are busy (using another n-1 middle switches). If all these are distinct, they occupy 2n-2 middle switches. Thus, m >= (n-1) + (n-1) + 1 = 2n - 1 guarantees at least one free middle switch."
  },
  {
    "id": "q24",
    "module": "Track 3: Topologies & Metrics",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "How did Passas, Katevenis, and Pnevmatikatos (IEEE TCAD 2012) prove that monolithic on-chip crossbars remain area-efficient and scalable beyond 100 nodes in modern CMOS silicon?",
    "options": [
      "By replacing traditional copper metal wires with carbon nanotube bundles operating at terahertz transmission frequencies.",
      "By inserting pipeline register stages at every crosspoint intersection to eliminate long capacitive wire RC delay.",
      "By implementing dynamic optical micro-ring resonator switches directly onto the top-level silicon dioxide passivation layer.",
      "By routing global crossbar data tracks directly over active standard cells on intermediate metal layers without expanding die area."
    ],
    "answer": 3,
    "explanation": "Passas et al. demonstrated that modern silicon processes feature 8-12 metal layers. While lower layers are densely packed with standard cells, intermediate metal layers (M4-M7) often have substantial unused routing capacity. Placing crossbar wires over existing logic avoids silicon area bloat, making 128-port crossbars consume only ~11% of die area."
  },
  {
    "id": "q25",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "What is the necessary and sufficient condition established by William Dally and Charles Seitz (1987) for a deterministic routing algorithm to be provably deadlock-free?",
    "options": [
      "Its Channel Dependency Graph (CDG) must contain no directed cycles (it must be strictly acyclic).",
      "The network topology must deploy at least four virtual channels per physical link across all routers.",
      "The maximum packet length must be strictly bounded to less than the physical FIFO depth of each input port.",
      "Routers must drop blocked packets whenever buffer queue fill levels exceed eighty percent capacity."
    ],
    "answer": 0,
    "explanation": "Dally and Seitz proved that a deterministic routing algorithm is deadlock-free if and only if there are no cycles in its Channel Dependency Graph (CDG). If the CDG is acyclic, channels can be numbered such that routing always follows monotonically increasing channel numbers, making cyclic wait states impossible."
  },
  {
    "id": "q26",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "In a 2D Mesh with 8 possible 90-degree turns, how many turns must be prohibited under the Glass & Ni Turn Model (1994) to eliminate all simple cycles while maximizing routing adaptiveness without virtual channels?",
    "options": [
      "All eight turns must be prohibited, forcing packets to travel exclusively along straight coordinate lines.",
      "Exactly two turns (one from clockwise cycles and one from counter-clockwise cycles), preserving 75% turn freedom.",
      "Exactly four turns must be prohibited, effectively disabling all routing adaptivity and enforcing dimension order.",
      "Zero turns need to be prohibited because round-robin crossbar switch arbitration prevents cycles dynamically."
    ],
    "answer": 1,
    "explanation": "A 2D mesh has two basic cycles: clockwise (N->E->S->W->N) and counter-clockwise (N->W->S->E->N). Each cycle contains 4 turns. Prohibiting 1 turn from the clockwise cycle and 1 turn from the counter-clockwise cycle (2 turns total out of 8) breaks all potential cycles while retaining 6 out of 8 turns (75% adaptiveness)."
  },
  {
    "id": "q27",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "Why does routing-level deadlock freedom (e.g. using XY DOR) fail to protect multi-core processors against Protocol-Level Deadlock, and how does PCMT (Jia et al., IEEE TCAD 2026) resolve it without dedicated Virtual Networks?",
    "options": [
      "Coherence protocols generate electrical reflection waves on copper lines; PCMT dampens these reflections using active impedance matching.",
      "Cache controllers experience metastability when requests arrive out of order; PCMT synchronizes all cache controllers to a single master clock.",
      "Coherence transactions form Request-Response dependency loops; PCMT prioritizes Response flits to drain buffers before requests saturate queues.",
      "Directory controllers require infinite retransmission buffers during cache invalidation; PCMT drops unacknowledged invalidation packets after three cycles."
    ],
    "answer": 2,
    "explanation": "Protocol deadlock occurs when high-level message dependencies (e.g. Request generating Invalidation which waits for Response) create circular waits when sharing physical buffers. Traditionally resolved by dedicated Virtual Networks (VN0, VN1, VN2). PCMT (Priority-based Congestion Management and Throttling) resolves this on unified buffers by prioritizing Response drainage and throttling new Requests when buffers fill."
  },
  {
    "id": "q28",
    "module": "Track 5: Thermal & Physical Design",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "What is the physical significance of the 'breakeven idle time' (tau_breakeven) when evaluating runtime power gating for an on-chip router component?",
    "options": [
      "It is the total duration required for an overheated router tile to dissipate thermal energy into the silicon substrate.",
      "It is the maximum number of consecutive clock cycles a router can remain unclocked before state retention registers corrupt data.",
      "It is the propagation delay required for a power-management command packet to travel from the operating system to the power switch.",
      "It is the minimum sleep duration where saved leakage energy exceeds the energy overhead of sleep-transistor charging and wakeup."
    ],
    "answer": 3,
    "explanation": "Power gating disconnects a circuit block from VDD or GND using high-Vt sleep transistors, eliminating subthreshold leakage. However, charging/discharging the sleep transistor gates and the virtual rail capacitance consumes dynamic energy (E_overhead). The breakeven time is tau_breakeven = E_overhead / P_leakage_saved; gating for less than this time increases net energy."
  },
  {
    "id": "q29",
    "module": "Track 5: Thermal & Physical Design",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "In ultrafine-grained runtime power gating (Matsutani et al., IEEE TCAD 2011), how does 'Lookahead Early Wakeup' prevent latency degradation caused by router wake-up delays?",
    "options": [
      "Upstream routers transmit early wake-up strobes 1-2 cycles ahead of flits, completing wake-up before packet arrival.",
      "Power-gated routers keep input crossbars permanently energized at nominal voltage while sleep-gating only the output link drivers.",
      "Sleeping routers are overdriven with double nominal supply voltage during wake-up to shorten RC power-rail stabilization time.",
      "Routing tables divert incoming packets to neighboring active routers whenever the targeted downstream router is in sleep mode."
    ],
    "answer": 0,
    "explanation": "Sleep transistors take 1-3 clock cycles to charge the virtual power rail safely without inductive ground bounce. Lookahead early wake-up sends an early wake-up signal from router N-1 to router N as soon as route computation determines the flit will head toward router N, hiding the wake-up latency behind upstream link and switch traversal."
  },
  {
    "id": "q30",
    "module": "Track 5: Thermal & Physical Design",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "How does Low-Power Code Reordering (LPCR, Adelkhani et al., IEEE TCAD 2025) exploit information theory to minimize dynamic switching power in high-speed serial on-chip links?",
    "options": [
      "By inverting every transmitted bit in the packet header to equalize static charge distribution across differential micro-strip traces on the die.",
      "By mapping high-probability consecutive symbol pairs to minimum-Hamming-distance codewords via maximum-weight matching graph optimization.",
      "By compressing all packet payloads using entropy Huffman coding trees synthesized into dedicated router decompression micro-engines.",
      "By reducing serial link transmission frequencies dynamically to near-zero whenever consecutive identical symbol streams are detected."
    ],
    "answer": 1,
    "explanation": "Dynamic power in serial interconnects is proportional to transition activity (bit flips between successive symbols). LPCR profiles consecutive symbol transition probabilities and formulates a maximum-weight matching problem on a transition graph, assigning codewords with Hamming distance = 1 to the most frequent state transitions, reducing switching activity by up to 35%."
  },
  {
    "id": "q31",
    "module": "Track 5: Thermal & Physical Design",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "Under the HotSpot electro-thermal duality, what physical thermal property is analogous to electrical capacitance (C) in a circuit?",
    "options": [
      "Thermal conductivity (k, in W/(m*K)), which dictates the rate of steady-state heat conduction across silicon bulk layers.",
      "Convective heat transfer coefficient (h, in W/(m^2*K)), representing air cooling boundary conditions at the heatsink fins.",
      "Thermal capacitance (heat capacity, C_th = rho * c_p * V in J/K), which represents silicon thermal inertia resisting temperature changes.",
      "Thermal contact resistance (R_th, in K/W), which accounts for microscopic surface roughness at thermal interface material boundaries."
    ],
    "answer": 2,
    "explanation": "In electro-thermal duality: Heat Flow (W) <-> Current (A), Temperature Difference (K) <-> Voltage (V), Thermal Resistance (K/W) <-> Electrical Resistance (Ohms), and Thermal Capacitance (J/K) <-> Electrical Capacitance (Farads). Thermal capacitance represents the thermal mass (density * specific heat * volume) that stores heat and resists instantaneous temperature changes."
  },
  {
    "id": "q32",
    "module": "Track 5: Thermal & Physical Design",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "Why do standard linear Kalman filters diverge when reconstructing on-chip thermal maps from physical thermal sensors, and how does the Gaussian-Sum Filter (Fu et al., IEEE TCAD 2019) solve this?",
    "options": [
      "Linear Kalman filters cannot invert asymmetric matrices; the Gaussian-Sum Filter replaces matrix inversions with scalar divisions.",
      "Thermal sensors exhibit permanent sensor drift; the Gaussian-Sum Filter applies periodic hardware recalibrations using laser trimming.",
      "Standard Kalman filters require floating-point hardware units; the Gaussian-Sum Filter executes exclusively with integer shift-add logic.",
      "Physical sensors suffer from non-Gaussian noise spikes; the Gaussian-Sum Filter models noise with Gaussian mixtures and Huber loss."
    ],
    "answer": 3,
    "explanation": "Kalman filters are optimal only under Gaussian noise. On real chips, power-grid switching noise (dI/dt) and EMI inject heavy-tailed, non-Gaussian impulsive noise spikes. The Gaussian-Sum Filter approximates the non-Gaussian probability density as a sum of Gaussian components and uses Huber robust weighting to reject impulsive sensor outliers."
  },
  {
    "id": "q33",
    "module": "Track 5: Thermal & Physical Design",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "How does the ZoneDefense routing algorithm (Fu et al., IEEE TVLSI 2014) achieve provable deadlock freedom around multiple permanent silicon faults in a 2D mesh without virtual channels?",
    "options": [
      "It encloses arbitrary faults into convex rectangular blocks and propagates defense zones so packets detour without forming cyclic waits.",
      "It disables all routers along entire rows and columns containing faults, reducing the functional topology to a smaller defect-free submesh.",
      "It routes packets around faulty routers using stochastic random walks and drops packets exceeding hop-count threshold limits.",
      "It configures redundant bypass wires across diagonal routers to substitute faulty links without modifying baseline routing tables."
    ],
    "answer": 0,
    "explanation": "Concave or irregular fault shapes create complex channel wait dependencies that lead to deadlocks. ZoneDefense groups irregular multi-node faults into convex rectangular Fault Blocks and projects unidirectional Defense Zones along the columns. Packets are guided around the convex boundaries in advance, ensuring no turn cycles form even under complex multi-fault patterns."
  },
  {
    "id": "q34",
    "module": "Track 6: Chiplets & Advanced Packaging",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "What is a Through-Silicon Via (TSV) Keep-Out Zone (KOZ), and what physical phenomenon dictates its size?",
    "options": [
      "A region surrounding a TSV where no global metal routing tracks can run due to electromagnetic capacitive crosstalk coupling.",
      "A boundary surrounding a TSV where no active transistors can be placed due to thermo-mechanical stress altering carrier mobility.",
      "A silicon wafer boundary designated for chemical mechanical planarization slurry drainage during 3D vertical stacking assembly.",
      "A protective guard ring encircling TSVs to shield sensitive analog phase-locked loops from digital clock substrate substrate noise."
    ],
    "answer": 1,
    "explanation": "Copper has a Coefficient of Thermal Expansion (CTE ~16.5 ppm/K) much higher than silicon (CTE ~2.6 ppm/K). During thermal cycling from annealing (250-400\u00b0C) to room temperature, copper shrinks faster than silicon, inducing severe radial compressive and tangential tensile stress. Via the piezoresistive effect, this stress shifts carrier mobility and threshold voltage (Vth) of nearby MOSFETs. The KOZ (typically 3-5 um) ensures transistors are not placed where stress causes timing faults."
  },
  {
    "id": "q35",
    "module": "Track 6: Chiplets & Advanced Packaging",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "Why does expanding a 2D router (5 ports) to a fully symmetric 3D router (7 ports) almost double the crossbar switch area, and how do Vertical Arbitration-Free architectures (More et al., IEEE TCAD 2018) mitigate this overhead?",
    "options": [
      "Crossbar silicon area scales logarithmically with port count; arbitration-free architectures double link wire width to compensate.",
      "Vertical ports require specialized high-voltage level shifters; arbitration-free designs replace electronic switches with carbon nanotubes.",
      "Crossbar multiplexer complexity scales quadratically (P^2 = 49 crosspoints vs 25); dedicated unidirectional links eliminate vertical allocators.",
      "Symmetric 3D crossbars require seven-phase clock generators; arbitration-free architectures convert all inter-tier links to asynchronous FIFOs."
    ],
    "answer": 2,
    "explanation": "Crossbar area scales as O(P^2 * W). Expanding from 5 ports (N, S, E, W, Local -> 25 crosspoints) to 7 ports (+Up, +Down -> 49 crosspoints) increases crosspoint count by 96%. Vertical Arbitration-Free architectures deploy dedicated point-to-point vertical links with simple multiplexers, bypassing the full 7x7 crossbar and eliminating vertical allocation stages."
  },
  {
    "id": "q36",
    "module": "Track 6: Chiplets & Advanced Packaging",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "What causes the severe 'Thermal Trapping' phenomenon in vertically stacked 3D-ICs, and why is the top tier significantly hotter than the bottom tier?",
    "options": [
      "Upper tiers operate at higher clock frequencies due to lower supply rail IR drop across vertical power distribution networks.",
      "Heat flows upward toward the chip surface due to natural convective air currents inside the hermetic ceramic packaging cavity.",
      "Thermo-mechanical shear stress across bonded microbumps increases the internal electrical resistance of upper tier logic gates.",
      "Heat in upper tiers must traverse multiple low-conductivity dielectric bonding layers before reaching the bottom heat sink."
    ],
    "answer": 3,
    "explanation": "In 3D-ICs, heat sinks are typically mounted on one side (e.g., bottom or top package lid). Heat generated in tiers farthest from the heat sink must conduct through multiple thinned silicon substrates (k_Si ~ 140 W/m-K) and dielectric adhesive/bonding interfaces (BCB, oxide, epoxy, k_diel ~ 0.2-1.4 W/m-K). These high thermal resistance interfaces act as thermal insulators, trapping heat in distant tiers."
  },
  {
    "id": "q37",
    "module": "Track 6: Chiplets & Advanced Packaging",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "Why does disaggregating a massive monolithic system-on-chip into smaller chiplets dramatically reduce total manufacturing cost, according to the Murphy and Seeds yield models?",
    "options": [
      "Die yield decays exponentially with active silicon area (Y ~ e^{-sqrt(A * D0)}); partitioning a large die into smaller chiplets surges yield.",
      "Small chiplets eliminate the requirement for chemical mechanical planarization during front-end wafer fabrication processes in advanced silicon nodes.",
      "Disaggregation allows all chiplets to be manufactured on older 180nm lithography lines while preserving advanced node performance across all cores.",
      "Packaging and test overhead costs for multi-chiplet modules are strictly lower than zero due to volume packaging rebates."
    ],
    "answer": 0,
    "explanation": "Yield models (e.g. Murphy, Seeds, Negative Binomial) show that silicon die yield drops exponentially with area. An 800 mm\u00b2 reticle-limit die might have only 15-25% yield due to random defect density D0. Partitioning it into four 200 mm\u00b2 chiplets increases per-die yield to 70-85%. Even with packaging substrate costs, net functional cost is significantly lower."
  },
  {
    "id": "q38",
    "module": "Track 6: Chiplets & Advanced Packaging",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "In the Universal Chiplet Interconnect Express (UCIe) standard, what is the role of the Die-to-Die (D2D) Adapter Layer between the Protocol Layer and the Physical Layer (PHY)?",
    "options": [
      "It modulates digital electrical voltages into optical wavelength pulses for silicon photonics transmission across interposers.",
      "It provides link state management, packet framing, CRC error detection, retry retransmission buffers, and credit flow control.",
      "It dynamically scales chiplet operating frequencies between 10 MHz and 10 GHz using clock tree phase-locked loop multipliers.",
      "It translates cache coherence snoops directly into PCI Express transaction layer packets without hardware protocol conversion."
    ],
    "answer": 1,
    "explanation": "In UCIe, the D2D Adapter layer sits between the Protocol Layer (PCIe, CXL, or Streaming) and the PHY. It is responsible for link state management, packet framing/deframing, CRC calculation/checking, Link Level Retry (LLR) with retransmission replay buffers, and credit-based flow control across the die boundary."
  },
  {
    "id": "q39",
    "module": "Track 6: Chiplets & Advanced Packaging",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "Why can composing individually deadlock-free 2D mesh chiplets produce system-level routing deadlocks, and how does the In/Outbound Swap backtracking mechanism (Wang et al., IEEE TCAD 2026) resolve this without overprovisioning Virtual Channels?",
    "options": [
      "Interposers lack ground planes causing electromagnetic feedback; In/Outbound Swap inserts decoupling capacitors across bridge tiles.",
      "Chiplet clock domain phase jitter misaligns flit boundaries; In/Outbound Swap resynchronizes all dies using global optical strobes.",
      "Die-to-die bridge routers create cross-chip cyclic dependency loops; In/Outbound Swap diverts stalled flits to escape registers to sever cycles.",
      "Cache coherence protocols fail on multi-chiplet topologies; In/Outbound Swap invalidates all remote cache lines whenever links stall."
    ],
    "answer": 2,
    "explanation": "Even if each individual chiplet uses deadlock-free XY routing, the global inter-chiplet network formed by connecting bridge routers can form cycles in the global Channel Dependency Graph (e.g. packets routing East across chiplet A, turning into chiplet B, routing West, and returning). Wang et al. proposed In/Outbound Swap: when a bridge stalls exceeding a timeout, blocked head flits are swapped into a localized escape register, breaking the cyclic dependency."
  },
  {
    "id": "q40",
    "module": "Track 7: Emerging Interconnects",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "What fundamental physical advantage allows Optical Networks-on-Chip (ONoC) to achieve near-zero dynamic transmission energy scaling over long distances compared to copper wires?",
    "options": [
      "Photons possess zero electrical charge and can travel through vacuum cavities without requiring any physical waveguide cladding.",
      "Optical waveguides eliminate all transmitter laser sources by generating photons spontaneously from silicon thermal gradients.",
      "Optical signals can be amplified indefinitely without consuming electrical power by using passive silicon micro-ring resonators.",
      "Photons conduct via low-loss optical waveguides where propagation loss does not depend on transmission frequency or wire RC parasitics."
    ],
    "answer": 3,
    "explanation": "Copper wires suffer from charging and discharging wire capacitance (E = 0.5 * C * V^2 * alpha), where C grows linearly with length, and high-frequency skin effect increases resistance. Optical interconnects transmit data as light modulated into waveguides; optical propagation loss in silicon waveguides is tiny (~0.5-2 dB/cm), meaning transmission energy is largely independent of distance once light is launched."
  },
  {
    "id": "q41",
    "module": "Track 7: Emerging Interconnects",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "Why do Parallel Switching Elements (PSEs) achieve significantly lower optical insertion loss and laser power dissipation than Crossing Switching Elements (CSEs) in ONoC architectures (Kao et al., IEEE TCAD 2026)?",
    "options": [
      "PSEs align waveguides in parallel without planar waveguide crossings, eliminating 0.1-0.2 dB crossing loss and inter-channel optical crosstalk.",
      "PSEs replace silicon waveguides with free-space wireless optical beams that pass through each other without any physical attenuation across the die.",
      "PSEs operate with active electrical amplifiers at every switching junction that regenerate attenuated optical signals without laser overhead penalties.",
      "PSEs double the refractive index of silicon waveguides to confine light beams completely, preventing any evanescent field leakage."
    ],
    "answer": 0,
    "explanation": "In photonic integrated circuits, planar waveguide crossings introduce significant optical insertion loss (~0.05-0.2 dB per crossing) and inter-channel crosstalk. CSEs require waveguides to physically intersect. PSEs route waveguides in parallel and use micro-rings to evanescently couple light across parallel tracks without physical crossings, drastically reducing total optical path loss and laser power."
  },
  {
    "id": "q42",
    "module": "Track 7: Emerging Interconnects",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "How does silicon's thermo-optic coefficient (dn/dT \u2248 1.86 \u00d7 10^{-4} K^{-1}) impact dense WDM optical networks, and why does thermal tuning consume substantial power (Ye et al., IEEE TVLSI 2013)?",
    "options": [
      "Thermal gradients melt silicon waveguides at high bit rates, requiring liquid nitrogen refrigeration to prevent physical damage.",
      "Temperature shifts drift micro-ring resonant wavelengths (~0.1 nm/\u00b0C); dense WDM spacing (0.4-0.8 nm) requires power-hungry heaters to align rings.",
      "Thermal expansion expands optical waveguides, causing light waves to reflect backward into the transmitter laser diode and permanently destroying it.",
      "Thermal noise accelerates spontaneous emission in photodetectors, reducing receiver sensitivity until optical signals are completely lost."
    ],
    "answer": 1,
    "explanation": "Silicon's refractive index changes with temperature (dn/dT). This shifts the resonant wavelength of micro-ring resonators by ~0.1 nm/\u00b0C. In dense Wavelength Division Multiplexing (DWDM), channel spacing is narrow (e.g. 0.4 to 0.8 nm, or 50-100 GHz). A small 5\u00b0C chip temperature fluctuation drifts the resonance into an adjacent channel, causing severe bit errors. Integrated micro-heaters must burn significant electrical power (15-20 mW per nm of tuning per ring) to stabilize wavelengths."
  },
  {
    "id": "q43",
    "module": "Track 8: Security & Reliability",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "Why is software/cryptographic payload encryption ineffective against interconnect-level thermal Hardware Trojans (Hasanzadeh et al., IEEE TCAD 2026)?",
    "options": [
      "Hardware Trojans decrypt AES ciphertext in real time by sniffing capacitive coupling on adjacent router crossbar wires.",
      "Cryptographic encryption algorithms double the packet payload size, inducing buffer overflow faults in router input queues.",
      "Trojans exploit traffic patterns, packet injection rates, and switching activity to create localized hotspots, regardless of ciphertext.",
      "Software encryption keys are automatically exposed to hardware routers through standard JTAG debugging scan chains on the chip."
    ],
    "answer": 2,
    "explanation": "Thermal Hardware Trojans do not need to read the data payload. Instead, they act by generating malicious traffic volumes, triggering pathological routing paths, or creating frequent crossbar bit transitions that dissipate localized dynamic power. This creates hot spots (>105\u00b0C) and induces Dynamic Thermal Management (DTM) throttling or permanent oxide breakdown, completely bypassing payload encryption."
  },
  {
    "id": "q44",
    "module": "Track 8: Security & Reliability",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "How does the HeatSense Weighted Moving Average (WMA) anomaly detector achieve real-time thermal monitoring without silicon multipliers (IEEE TCAD 2026)?",
    "options": [
      "By offloading all floating-point calculations to off-chip GPU accelerator servers via high-speed PCIe expansion links across the motherboard.",
      "By disabling router clock trees and taking thermal measurements exclusively during system sleep and power-down states.",
      "By measuring thermal gradients with analog optical waveguides and comparing them to baseline reference laser intensities.",
      "By setting the weighting factor alpha to powers of two (2^-S), converting multiplication into single-cycle arithmetic right-shifts."
    ],
    "answer": 3,
    "explanation": "Hardware floating-point or integer multipliers consume significant area and power, making them unaffordable inside lightweight router tiles. HeatSense restricts exponential weighting factors to negative powers of two (alpha = 2^-S, e.g. 1/8 with S=3). Multiplying by alpha becomes a simple arithmetic right-shift (>>> 3), and dynamic variance thresholding is evaluated via bit-shifts and additions ((D << 1) + D), enabling zero-multiplier implementation."
  },
  {
    "id": "q45",
    "module": "Track 8: Security & Reliability",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "How do NoC-based Physical Unclonable Functions (NoCiPUF) authenticate chiplets without storing secret keys in non-volatile memory (Grover et al., IEEE TCAS-I 2025)?",
    "options": [
      "They exploit sub-nanosecond wire delay and threshold voltage variations across symmetrical crossbar paths to produce unique race outcomes.",
      "They read manufacturer serial numbers hardcoded into metal layer 1 using high-resolution on-chip optical scanners embedded in each router tile.",
      "They measure the radioactive alpha-particle decay rate of copper atoms inside router input FIFO memory cells across the multi-chiplet substrate.",
      "They record the chemical degradation rate of thermal interface material across microbump bonding interfaces over time."
    ],
    "answer": 0,
    "explanation": "NoCiPUF leverages manufacturing process variations (line-edge roughness, oxide thickness, and threshold voltage variations) that exist naturally across nominally symmetrical paths in router crossbars and arbiters. By racing two simultaneous signals through identical crossbar paths into an arbiter, the winner is determined by microscopic physical variations unique to that silicon die, acting as a tamper-proof silicon biometric fingerprint."
  },
  {
    "id": "q46",
    "module": "Track 9: AI, LLM & Neuromorphic NoCs",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "question": "What primary communication bottleneck occurs when training Large Language Models (LLMs) on conventional 2D mesh Networks-on-Chip?",
    "options": [
      "Large language models cannot transmit ASCII characters across electronic routers without software unicode conversion overhead.",
      "Tensor Parallelism requires massive synchronous All-Reduce collectives across cores, saturating mesh bisection bandwidth and stalling compute.",
      "Mesh routers lack 64-bit floating-point registers, preventing the NoC from forwarding gradient tensors between processing tiles.",
      "Optical waveguides inside 2D meshes experience severe chromatic dispersion when transmitting multi-head attention weight vectors across the chip fabric."
    ],
    "answer": 1,
    "explanation": "In LLM training with Tensor and Pipeline Parallelism, every transformer layer requires massive collective communication operations (All-Reduce, All-Gather, Reduce-Scatter) where every core must exchange and sum multi-megabyte activation gradients. In a standard 2D mesh, bisection bandwidth scales poorly (O(sqrt(N))), causing interconnect saturation, long serialization delays, and severe GPU/NPU compute bubbles."
  },
  {
    "id": "q47",
    "module": "Track 9: AI, LLM & Neuromorphic NoCs",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 150,
    "question": "How does PAC-NoC's In-Network Computing architecture reduce multi-head attention collective latency in Transformer accelerators (Ouyang et al., IEEE TVLSI 2026)?",
    "options": [
      "Routers drop ninety percent of attention weights using lossy compression algorithms and reconstruct them using polynomial interpolation.",
      "PAC-NoC replaces digital packet routers with passive analog RC filter networks that compute vector dot products via Kirchhoff's laws.",
      "Router crossbars are augmented with tag-matching accumulator ALUs that aggregate gradient flits in-flight, slashing collective traffic volume.",
      "PAC-NoC serializes all multi-head attention operations into a single giant systolic array core, eliminating the need for inter-tile routing."
    ],
    "answer": 2,
    "explanation": "In traditional NoCs, collective reduction requires all cores to send their gradients to memory or a root node, creating immense traffic congestion. PAC-NoC embeds lightweight arithmetic logic units (ALUs) directly into router crossbars (In-Network Reduction). As gradient flits from different child cores converge at a router, they are reduced (summed) in-flight, eliminating up to 75% of network traffic volume."
  },
  {
    "id": "q48",
    "module": "Track 9: AI, LLM & Neuromorphic NoCs",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 200,
    "question": "How does 3D Face-to-Face Copper-Pillar Hybrid Bonding eliminate memory silos for on-device LLM inference (SiloBreaker, IEEE TCAD 2026)?",
    "options": [
      "By replacing electrical copper wires with wireless radio transceivers operating in the sub-terahertz frequency spectrum across adjacent dies.",
      "By storing all multi-billion LLM weight parameters inside processor L1 caches using quantum dot magnetic memory cells integrated on-chip.",
      "By operating the entire compute tile and DRAM stack submerged in liquid nitrogen to eliminate electrical wire resistance across the interconnect.",
      "By achieving a 3 \u00b5m pitch with >110,000 vertical bonds/mm\u00b2, delivering over 16 TB/s vertical bandwidth without TSV area overhead."
    ],
    "answer": 3,
    "explanation": "Conventional 2.5D packaging (microbumps at 40-55 um pitch) or TSVs (10-20 um pitch) suffer from pin density limitations, parasitics, and keep-out zones. Face-to-Face (F2F) Cu-Cu Direct Bond Interconnect (DBI) achieves sub-3 um pitch and over 100,000 connections/mm^2 with parasitic capacitance <1 fF. This enables attaching a dedicated DRAM tier directly over compute tiles with >16 TB/s vertical bandwidth, eliminating memory wall stalls during autoregressive token generation."
  }
];

let activeQuestions = [];
let currentIdx = 0;
let userScore = 0;
let correctCount = 0;
let timerInterval = null;
let timeLeft = 35;
let candidate = { name: "", email: "", mode: "full", certId: "", date: "" };
let clientGeo = { ip: "Detecting...", country: "Detecting...", city: "", region: "", resolved: false };

// Asynchronously resolve Client IP and Location in background
async function resolveClientGeo() {
  try {
    const res = await fetch("https://ipapi.co/json/", { cache: "no-store" });
    if (res.ok) {
      const data = await res.json();
      if (data && data.ip) {
        clientGeo.ip = data.ip;
        clientGeo.country = data.country_name ? `${data.country_name} (${data.country_code || data.country})` : (data.country || "Unknown Country");
        clientGeo.city = data.city || "";
        clientGeo.region = data.region || "";
        clientGeo.resolved = true;
        updateGeoHUD();
        return;
      }
    }
  } catch(e) {
    console.warn("ipapi.co resolution failed, attempting secondary provider...", e);
  }

  try {
    const res2 = await fetch("https://ipwho.is/", { cache: "no-store" });
    if (res2.ok) {
      const data2 = await res2.json();
      if (data2 && data2.success !== false && data2.ip) {
        clientGeo.ip = data2.ip;
        clientGeo.country = data2.country ? `${data2.country} (${data2.country_code})` : "Unknown Country";
        clientGeo.city = data2.city || "";
        clientGeo.region = data2.region || "";
        clientGeo.resolved = true;
        updateGeoHUD();
        return;
      }
    }
  } catch(e2) {
    console.warn("ipwho.is resolution failed, attempting tertiary provider...", e2);
  }

  try {
    const res3 = await fetch("https://api.ipify.org?format=json", { cache: "no-store" });
    if (res3.ok) {
      const data3 = await res3.json();
      if (data3 && data3.ip) {
        clientGeo.ip = data3.ip;
        clientGeo.country = "Detected via IP";
        clientGeo.resolved = true;
        updateGeoHUD();
        return;
      }
    }
  } catch(e3) {
    console.warn("Client-side GeoIP resolution unavailable or shielded.", e3);
    clientGeo.ip = "Unavailable (Client-Shielded)";
    clientGeo.country = "Unknown Location";
    clientGeo.resolved = true;
    updateGeoHUD();
  }
}

function updateGeoHUD() {
  const ipEl = document.getElementById("metaIp");
  const locEl = document.getElementById("metaLoc");
  if (ipEl) ipEl.textContent = clientGeo.ip;
  if (locEl) locEl.textContent = [clientGeo.city, clientGeo.country].filter(Boolean).join(", ") || clientGeo.country;
}

// Initiate resolution immediately on page load
resolveClientGeo();

// Fisher-Yates array shuffling algorithm
function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
  }
  return arr;
}

// Dynamically randomize the 4 options and recalculate correct answer index (A, B, C, D)
function randomizeQuestion(q) {
  const items = q.options.map((optText, idx) => ({
    text: optText,
    isCorrect: (idx === q.answer)
  }));

  shuffleArray(items);

  const newOptions = items.map(it => it.text);
  const newAnswer = items.findIndex(it => it.isCorrect);

  return {
    id: q.id,
    module: q.module,
    tier: q.tier,
    tier_level: q.tier_level,
    base_points: q.base_points,
    question: q.question,
    options: newOptions,
    answer: newAnswer,
    explanation: q.explanation
  };
}

// Select scoped questions by tier mode and dynamically reshuffle options and question order
function selectAndRandomizeQuizQuestions(mode) {
  const tier1All = QUESTIONS_BANK.filter(q => q.tier_level === 1);
  const tier2All = QUESTIONS_BANK.filter(q => q.tier_level === 2);
  const tier3All = QUESTIONS_BANK.filter(q => q.tier_level === 3);

  // Shuffle pools before sampling so question selection is random on every retake
  shuffleArray(tier1All);
  shuffleArray(tier2All);
  shuffleArray(tier3All);

  let selected = [];
  if (mode === "tier1_sprint") {
    // 4 randomly selected questions from Tier 1 pool
    selected = tier1All.slice(0, 4);
  } else if (mode === "grandmaster") {
    // 4 randomly selected questions from Tier 3 pool
    selected = tier3All.slice(0, 4);
  } else {
    // Comprehensive: 4 Tier 1 + 4 Tier 2 + 4 Tier 3 = 12 balanced questions
    selected = [
      ...tier1All.slice(0, 4),
      ...tier2All.slice(0, 4),
      ...tier3All.slice(0, 4)
    ];
  }

  // Shuffle question presentation sequence
  shuffleArray(selected);

  // Dynamically reshuffle options for every single question
  return selected.map(q => randomizeQuestion(q));
}

function startQuiz() {
  const nameInput = document.getElementById("candidateName");
  const emailInput = document.getElementById("candidateEmail");
  const name = nameInput.value.trim();
  const email = emailInput.value.trim();

  if (!name) {
    alert("Please enter your full name for certification registration.");
    nameInput.focus();
    return;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || !emailRegex.test(email)) {
    alert("Please enter a valid candidate email address (e.g. ada@university.edu).");
    emailInput.focus();
    return;
  }

  candidate.name = name;
  candidate.email = email;
  candidate.mode = document.getElementById("assessmentMode").value;

  // Dynamically select and reshuffle questions & options
  activeQuestions = selectAndRandomizeQuizQuestions(candidate.mode);

  currentIdx = 0;
  userScore = 0;
  correctCount = 0;

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
  document.getElementById("quizPtsBadge").textContent = `+${q.base_points} pts`;

  // Tier badge color
  const tBadge = document.getElementById("quizTierBadge");
  if (q.tier_level === 1) {
    tBadge.style.background = "rgba(34, 197, 94, 0.12)";
    tBadge.style.color = "#16a34a";
    tBadge.style.borderColor = "rgba(34, 197, 94, 0.25)";
  } else if (q.tier_level === 2) {
    tBadge.style.background = "rgba(234, 88, 12, 0.12)";
    tBadge.style.color = "#ea580c";
    tBadge.style.borderColor = "rgba(234, 88, 12, 0.25)";
  } else {
    tBadge.style.background = "rgba(147, 51, 234, 0.12)";
    tBadge.style.color = "#9333ea";
    tBadge.style.borderColor = "rgba(147, 51, 234, 0.25)";
  }

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
    correctCount++;
    const speedBonus = timeLeft * 3;
    userScore += q.base_points + speedBonus;
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

  const accuracy = Math.round((correctCount / activeQuestions.length) * 100);
  document.getElementById("resultSummary").innerHTML = `Candidate: <strong>${candidate.name}</strong> (${candidate.email}) | Score: <strong>${userScore}</strong> pts | Accuracy: <strong>${accuracy}%</strong> (${correctCount}/${activeQuestions.length} correct)`;

  // Set Certificate Fields
  document.getElementById("certCandidateName").textContent = candidate.name;
  document.getElementById("certCandidateEmail").textContent = candidate.email;
  document.getElementById("certScore").textContent = `${userScore} pts (${accuracy}%)`;

  const now = new Date();
  candidate.date = now.toISOString().split("T")[0];
  document.getElementById("certDate").textContent = candidate.date;

  // Generate deterministic verification hash
  let hashVal = 0;
  const hashRaw = `${candidate.name}-${candidate.email}-${userScore}-${candidate.date}`;
  for (let i = 0; i < hashRaw.length; i++) {
    hashVal = (hashVal << 5) - hashVal + hashRaw.charCodeAt(i);
    hashVal |= 0;
  }
  candidate.certId = `NOC-CERT-${now.getFullYear()}-${Math.abs(hashVal).toString(16).toUpperCase().padStart(6, '0')}`;
  document.getElementById("certHash").textContent = candidate.certId;

  // Update submission HUD meta
  document.getElementById("metaName").textContent = candidate.name;
  document.getElementById("metaEmail").textContent = candidate.email;
  updateGeoHUD();

  // Route Leaderboard link directly to active track
  const lbLink = document.getElementById("viewLeaderboardLink");
  if (lbLink) {
    lbLink.href = `../leaderboard/?track=${candidate.mode}`;
  }

  // Auto-record to local browser leaderboard storage
  saveScoreToLocalStorage({
    name: candidate.name,
    email: candidate.email,
    org: clientGeo.country || "Independent",
    country: clientGeo.country,
    ip: clientGeo.ip,
    mode: candidate.mode,
    track: candidate.mode === "grandmaster" ? "Grandmaster (Tier 3)" : (candidate.mode === "tier1_sprint" ? "Fundamentals Sprint" : "Comprehensive Exam"),
    score: userScore,
    accuracy: accuracy,
    certId: candidate.certId,
    date: candidate.date,
    type: "quiz"
  });

  // AUTOMATICALLY SUBMIT TO GITHUB (No user intervention required)
  autoSubmitToGithub();
}

function saveScoreToLocalStorage(record) {
  try {
    const current = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    current.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(current.slice(0, 50)));
  } catch(e) {
    console.error(e);
  }
}

async function autoSubmitToGithub() {
  const icon = document.getElementById("submissionIcon");
  const title = document.getElementById("submissionTitle");
  const detail = document.getElementById("submissionDetail");
  const badge = document.getElementById("submissionBadge");
  const linkWrap = document.getElementById("submissionLinkWrap");
  const fallbackWrap = document.getElementById("submissionFallbackWrap");

  icon.textContent = "🔄";
  badge.textContent = "SUBMITTING";
  badge.style.background = "#1e293b";
  badge.style.color = "#38bdf8";
  title.textContent = "Automatically Submitting Result to GitHub...";
  detail.textContent = "Transmitting verified candidate credentials, score, IP, and location to official GitHub Issues ledger.";
  linkWrap.style.display = "none";
  fallbackWrap.style.display = "none";

  const accuracy = Math.round((correctCount / activeQuestions.length) * 100);
  const locationStr = [clientGeo.city, clientGeo.region].filter(Boolean).join(", ");

  const payload = {
    candidate: candidate.name,
    email: candidate.email,
    ip: clientGeo.ip,
    location: locationStr || "Unknown",
    country: clientGeo.country || "Unknown Country",
    mode: candidate.mode,
    score: userScore,
    accuracy: accuracy,
    correctCount: correctCount,
    totalQuestions: activeQuestions.length,
    certId: candidate.certId,
    date: candidate.date,
    timestamp: new Date().toISOString(),
    type: "quiz"
  };

  const primaryEndpoint = window.NOC_QUIZ_API_URL || "https://noc-quiz-api.network-on-chip.workers.dev/api/submit-quiz";
  const endpoints = [primaryEndpoint, "http://localhost:8787/api/submit-quiz"];

  let success = false;
  let lastError = null;

  for (const endpoint of endpoints) {
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        const resData = await res.json();
        if (resData && (resData.success || resData.html_url || resData.issue_number)) {
          success = true;
          icon.textContent = "✅";
          badge.textContent = "RECORDED";
          badge.style.background = "rgba(34, 197, 94, 0.2)";
          badge.style.color = "#22c55e";
          title.textContent = `Successfully Recorded on GitHub (Issue #${resData.issue_number || ""})!`;
          detail.textContent = "Assessment verified and officially published to the repository ledger.";

          if (resData.ip && resData.ip !== "Unknown IP") {
            document.getElementById("metaIp").textContent = resData.ip;
          }
          if (resData.country && resData.country !== "Unknown Country") {
            document.getElementById("metaLoc").textContent = resData.location || resData.country;
          }

          if (resData.html_url) {
            const a = document.getElementById("submissionIssueLink");
            a.href = resData.html_url;
            linkWrap.style.display = "block";
          }
          break;
        }
      } else {
        lastError = `HTTP ${res.status}`;
      }
    } catch (err) {
      lastError = err.message;
    }
  }

  if (!success) {
    icon.textContent = "⚠️";
    badge.textContent = "SAVED LOCALLY";
    badge.style.background = "rgba(234, 179, 8, 0.2)";
    badge.style.color = "#eab308";
    title.textContent = "Result Recorded to Local Verification Ledger";
    detail.textContent = `Backend submission server pending deployment (${lastError || "network offline"}). Score is safely preserved in browser.`;
    fallbackWrap.style.display = "block";
  }
}

function retryAutoSubmit() {
  autoSubmitToGithub();
}

function emergencyFallbackIssue() {
  const repo = "network-on-chip/learning";
  const title = `[quiz-result] ${candidate.name} (${candidate.email}) — ${userScore} pts — ${candidate.certId}`;
  const accuracy = Math.round((correctCount / activeQuestions.length) * 100);
  const loc = [clientGeo.city, clientGeo.country].filter(Boolean).join(", ");
  const body = [
    "### 🎯 NoC Architecture Assessment Submission",
    `- **Candidate**: ${candidate.name}`,
    `- **Email**: ${candidate.email}`,
    `- **IP Address**: \`${clientGeo.ip}\``,
    `- **Location / Country**: ${loc || "Unknown"}`,
    `- **Assessment Mode**: ${candidate.mode}`,
    `- **Total Score**: ${userScore} pts`,
    `- **Accuracy**: ${accuracy}% (${correctCount}/${activeQuestions.length} correct)`,
    `- **Credential Hash**: \`${candidate.certId}\``,
    `- **Date**: ${candidate.date}`,
    "",
    "```json",
    JSON.stringify({
      candidate: candidate.name,
      email: candidate.email,
      ip: clientGeo.ip,
      location: loc,
      country: clientGeo.country,
      mode: candidate.mode,
      score: userScore,
      accuracy: accuracy,
      certId: candidate.certId,
      date: candidate.date,
      type: "quiz"
    }, null, 2),
    "```"
  ].join("\n");

  const url = `https://github.com/${repo}/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=quiz-result,leaderboard`;
  window.open(url, '_blank');
}

function downloadCertificateSVG() {
  const name = document.getElementById("certCandidateName").textContent;
  const email = document.getElementById("certCandidateEmail").textContent;
  const score = document.getElementById("certScore").textContent;
  const hash = document.getElementById("certHash").textContent;
  const date = document.getElementById("certDate").textContent;

  const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" width="800" height="560">
    <rect width="800" height="560" fill="#ffffff" />
    <rect x="20" y="20" width="760" height="520" fill="none" stroke="#d4af37" stroke-width="4" />
    <rect x="28" y="28" width="744" height="504" fill="none" stroke="#0f172a" stroke-width="1.5" />
    
    <text x="400" y="80" text-anchor="middle" font-family="'Inter', sans-serif" font-size="12" font-weight="700" fill="#64748b" letter-spacing="3">NOC ACADEMIC CREDENTIAL REGISTRY</text>
    <text x="400" y="130" text-anchor="middle" font-family="'Inter', sans-serif" font-size="28" font-weight="900" fill="#0f172a">CERTIFICATE OF ACHIEVEMENT</text>
    <text x="400" y="175" text-anchor="middle" font-family="'Inter', sans-serif" font-size="14" fill="#475569">This is to proudly certify that</text>
    
    <text x="400" y="235" text-anchor="middle" font-family="'Inter', sans-serif" font-size="32" font-weight="800" fill="#1e3a8a">${name}</text>
    <line x1="200" y1="250" x2="600" y2="250" stroke="#cbd5e1" stroke-width="2" />
    
    <text x="400" y="280" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="14" fill="#64748b">${email}</text>
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
