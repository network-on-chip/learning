#!/usr/bin/env python3
"""Quiz Challenge, 3-Tier Difficulty Engine, and Verifiable Certificate Generator for NoC Learning Hub."""

from __future__ import annotations
import json
from pathlib import Path

# 3-Tier Structured Question Bank
QUESTIONS = [
    # --- TIER 1: FUNDAMENTAL (100 pts) ---
    {
        "id": "q1",
        "module": "Track 1: Fundamentals",
        "tier": "Tier 1: Fundamental",
        "tier_level": 1,
        "base_points": 100,
        "question": "Why did multicore processor architectures replace shared multi-drop buses with packet-switched Networks-on-Chip (NoC)?",
        "options": [
            "Shared buses suffer from capacitive RC wire delays, serialization bottlenecks (only 1 master at a time), and energy overhead as core count scales.",
            "Shared buses require optical fibers that are too expensive for consumer silicon.",
            "Shared buses cannot transmit binary 0s and 1s simultaneously.",
            "Shared buses consume zero power when idle."
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
            "A Flit is the routing unit; a Packet is the link unit; a Phit is the application message.",
            "A Packet is the routing unit; a Flit is the atomic flow control & buffer unit; a Phit is the physical wire width transferred in one clock cycle.",
            "Flits and Phits are identical units used exclusively in optical networks.",
            "A Packet contains multiple Phits, which are each split into multiple Flits."
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
            "Electromigration breakdown; solved by lowering the supply voltage.",
            "Head-of-Line (HoL) blocking; solved by dividing the buffer into multiple Virtual Channels (VCs).",
            "Clock skew; solved by adding PLL multipliers to every router.",
            "Thermal runaway; solved by turning off adjacent routers."
        ],
        "answer": 1,
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
            "Corner routers have degree 2 (+ local port); interior routers have degree 4 (+ local port).",
            "All routers in a 2D mesh have an identical degree of 6.",
            "Corner routers have degree 4; interior routers have degree 2.",
            "Corner routers connect directly to all other routers in 1 hop."
        ],
        "answer": 0,
        "explanation": "In an open-boundary 2D mesh, corner nodes only have 2 inter-router channels (e.g. East and South), edge nodes have 3, and interior nodes have 4 orthogonal channels (North, South, East, West)."
    },

    # --- TIER 2: CORE ENGINEERING (200 pts) ---
    {
        "id": "q5",
        "module": "Track 1: Fundamentals",
        "tier": "Tier 2: Core Engineering",
        "tier_level": 2,
        "base_points": 200,
        "question": "In credit-based flow control, if link traversal takes 1 cycle, buffer processing takes 1 cycle, and credit return takes 1 cycle, what happens if the input buffer capacity is only 2 flits?",
        "options": [
            "Throughput remains at 100% because credits travel faster than light.",
            "The upstream router exhausts its credits on cycle 2 and stalls for at least 1 cycle before the first credit returns, capping throughput below 100%.",
            "Packets are automatically dropped and must be resent by TCP.",
            "The router experiences an immediate hardware deadlock."
        ],
        "answer": 1,
        "explanation": "Round-Trip Time is RTT = 1 + 1 + 1 = 3 cycles. With only 2 buffer slots, the transmitter sends 2 flits and must stall on cycle 3 awaiting credit arrival, introducing pipeline bubbles."
    },
    {
        "id": "q6",
        "module": "Track 2: Router Microarchitecture",
        "tier": "Tier 2: Core Engineering",
        "tier_level": 2,
        "base_points": 200,
        "question": "What are the canonical 5 pipeline stages of a classic Virtual Channel wormhole router?",
        "options": [
            "Fetch, Decode, Execute, Memory, Writeback",
            "Buffer Write (BW) -> Route Computation (RC) -> VC Allocation (VA) -> Switch Allocation (SA) -> Switch Traversal (ST)",
            "Sample, Hold, Quantize, Encode, Transmit",
            "Arbitrate, Forward, Compress, Filter, Evict"
        ],
        "answer": 1,
        "explanation": "The canonical 5-stage router pipeline performs Buffer Write (BW), Route Computation (RC), Virtual Channel Allocation (VA), Switch Allocation (SA), and Crossbar Switch Traversal (ST)."
    },
    {
        "id": "q7",
        "module": "Track 3: Topologies & Metrics",
        "tier": "Tier 2: Core Engineering",
        "tier_level": 2,
        "base_points": 200,
        "question": "Why does a 4x4 Concentrated Mesh (cMesh) achieve lower zero-load latency for 64 cores than a traditional 8x8 2D Mesh?",
        "options": [
            "By clustering 4 compute cores around each router, total routers decrease from 64 to 16, cutting network diameter from 14 hops to just 6 hops.",
            "cMesh routers eliminate the need for crossbar switches.",
            "cMesh operates at double the clock frequency because wires are longer.",
            "cMesh replaces packet routing with broadcast radio signals."
        ],
        "answer": 0,
        "explanation": "Concentrating 4 tiles per router reduces router count by 75% (from 64 to 16), reducing the network grid to 4x4. The diameter drops from 2(8-1)=14 to 2(4-1)=6 hops, significantly cutting per-hop traversal delays."
    },
    {
        "id": "q8",
        "module": "Track 4: Routing & Deadlock",
        "tier": "Tier 2: Core Engineering",
        "tier_level": 2,
        "base_points": 200,
        "question": "In the Turn Model (Glass & Ni), which two turns are prohibited in the West-First routing algorithm, and what adaptivity does it preserve?",
        "options": [
            "Prohibits North->East and South->East; preserves Westbound adaptivity.",
            "Prohibits South->West and North->West; packets heading west must do so first, leaving 100% full adaptivity when traveling East.",
            "Prohibits East->North and West->North; forces deterministic YX routing.",
            "Prohibits all 8 turns; completely disables packet movement."
        ],
        "answer": 1,
        "explanation": "West-First eliminates South->West (breaking clockwise cycle) and North->West (breaking counter-clockwise cycle). Traveling west is deterministic, but traveling east is fully adaptive across East, North, and South links."
    },

    # --- TIER 3: ADVANCED SILICON MASTERY (300 pts) ---
    {
        "id": "q9",
        "module": "Track 2: Router Microarchitecture",
        "tier": "Tier 3: Silicon Mastery",
        "tier_level": 3,
        "base_points": 300,
        "question": "In a Matrix Arbiter with an NxN triangular priority matrix M, what is the exact hardware update rule when client k is granted the resource?",
        "options": [
            "Row k is cleared to all 0s (M[k,:] = 0) and Column k is set to all 1s (M[:,k] = 1).",
            "All diagonal elements M[i,i] are inverted from 0 to 1.",
            "The priority matrix is shifted circularly by one bit using a barrel shifter.",
            "Matrix M is transposed: M = M^T."
        ],
        "answer": 0,
        "explanation": "To make client k the lowest priority (Least Recently Used), row k is set to 0 (k has priority over no one) and column k is set to 1 (all other active clients take priority over k). This takes effect in 2 gate levels."
    },
    {
        "id": "q10",
        "module": "Track 4: Routing & Deadlock",
        "tier": "Tier 3: Silicon Mastery",
        "tier_level": 3,
        "base_points": 300,
        "question": "How does Duato's Theorem (1993) enable high-performance adaptive routing without deadlock?",
        "options": [
            "It requires every single virtual channel to be strictly acyclic at all times.",
            "It partitions virtual channels into an adaptive subnetwork (which may contain cycles) and an acyclic escape subnetwork (e.g. XY VCs) that blocked packets can always access to guarantee forward progress.",
            "It drops packets as soon as a cycle is detected and requests an end-to-end retransmission.",
            "It forces all packets to take random Hamiltonian walks across the network."
        ],
        "answer": 1,
        "explanation": "Duato proved that the adaptive channel subnetwork can contain cycles in its Channel Dependency Graph, provided there exists a connected acyclic escape subnetwork that packets can always enter when congested."
    },
    {
        "id": "q11",
        "module": "Track 5: Thermal & Congestion",
        "tier": "Tier 3: Silicon Mastery",
        "tier_level": 3,
        "base_points": 300,
        "question": "Why do standard Least Squares estimators fail when reconstructing continuous on-chip thermal fields from sparse physical sensors under real silicon operation?",
        "options": [
            "Physical thermal sensors exhibit non-Gaussian disturbances (inductive dI/dt noise, process variations, and heavy-tailed impulsive outliers) that violate Gaussian assumptions.",
            "Least Squares can only interpolate 1-dimensional signals, not 2-dimensional chip planes.",
            "Thermal sensors only measure voltage, not temperature.",
            "Silicon substrate temperature is mathematically non-differentiable."
        ],
        "answer": 0,
        "explanation": "On-chip sensors experience high-frequency switching noise and heavy-tailed non-Gaussian outliers from adjacent clock trees. Robust M-estimators or robust Kalman filters must be used to downweight outlier spikes."
    },
    {
        "id": "q12",
        "module": "Track 6: Chiplets & 3D NoC",
        "tier": "Tier 3: Silicon Mastery",
        "tier_level": 3,
        "base_points": 300,
        "question": "In multi-chiplet packaging using UCIe (Universal Chiplet Interconnect Express), what architectural advantage does standard die-to-die (D2D) packaging provide compared to traditional PCIe?",
        "options": [
            "UCIe delivers up to 1300 Gbps/mm shoreline bandwidth density with ultra-low energy (< 0.5 pJ/bit) and sub-2ns latency, enabling transparent on-chip NoC extensions across dies.",
            "UCIe uses wireless RF antennas that eliminate all physical microbumps.",
            "UCIe is limited to board-to-board cables up to 2 meters in length.",
            "UCIe only supports serial 1-bit asynchronous communication."
        ],
        "answer": 0,
        "explanation": "UCIe achieves over 28x higher bandwidth density than PCIe with sub-0.5 pJ/bit energy efficiency, allowing routers on adjacent chiplets to be linked transparently into a unified global mesh."
    },

    # --- TEXTBOOK CHAPTER 1: INTERCONNECT PHYSICS EXTENSIONS ---
    {
        "id": "q13",
        "module": "Track 1: Fundamentals (Book Ch 1)",
        "tier": "Tier 1: Fundamental",
        "tier_level": 1,
        "base_points": 100,
        "question": "Under the Elmore delay model, why does the propagation delay of a shared multi-drop bus grow quadratically/superlinearly with core count N rather than remaining flat?",
        "options": [
            "Every attached core introduces capacitive tap loading (C_tap) and die scaling increases physical wire length (L ~ sqrt(N)), compounding both wire resistance and total capacitance.",
            "Buses require optical repeaters whose laser efficiency drops with core count.",
            "Transistors on a bus automatically divide their supply voltage by N.",
            "Clock frequencies in multi-core chips must be slowed down by quantum tunneling."
        ],
        "answer": 0,
        "explanation": "Elmore delay tau_bus ~ R_wire * C_wire + R_driver * (C_wire + N * C_tap) + 0.5 * R_wire * (N * C_tap). Both wire resistance (proportional to wire length) and tap capacitance scale with N, causing delay to surge."
    },
    {
        "id": "q14",
        "module": "Track 1: Fundamentals (Book Ch 1)",
        "tier": "Tier 2: Core Engineering",
        "tier_level": 2,
        "base_points": 200,
        "question": "What is the physical mechanism behind the Mayadas-Shatzkes effect, and why does it severely penalize global interconnects below 14nm?",
        "options": [
            "Thermal expansion melts copper traces when packets exceed 100 Gbps.",
            "When wire width shrinks below the electron mean free path (~39nm in Cu), diffuse scattering off grain boundaries and sidewalls causes effective copper resistivity to surge by 5x-15x.",
            "Electromagnetic radiation creates destructive interference that erases packet flits.",
            "Copper wires convert spontaneously into silicon dioxide under high clock frequencies."
        ],
        "answer": 1,
        "explanation": "In nanoscale wires, electron scattering off grain boundaries (Mayadas-Shatzkes) and sidewall surfaces (Fuchs-Sondheimer), compounded by high-resistance Ta/TaN diffusion barrier liners, causes effective resistivity to spike dramatically."
    },
    {
        "id": "q15",
        "module": "Track 1: Fundamentals (Book Ch 1)",
        "tier": "Tier 3: Silicon Mastery",
        "tier_level": 3,
        "base_points": 300,
        "question": "Why is a monolithic centralized NxN crossbar switch physically unviable for large manycore systems (N >= 64 cores), despite offering single-hop non-blocking routing?",
        "options": [
            "It requires N^2 crosspoint switches (4,096 switches for N=64) and dense global wiring tracks, leading to severe silicon area explosion and physical routing track starvation.",
            "Crossbars cannot route digital binary signals.",
            "Crossbar switches cannot be built using CMOS transistors.",
            "Crossbars violate Duato's deadlock theorem by definition."
        ],
        "answer": 0,
        "explanation": "Full NxN crossbars exhibit quadratic O(N^2) area complexity and require O(N) global wires per port. For N >= 64, wiring congestion and crosspoint area overwhelm the silicon floorplan, whereas modular 2D Mesh NoCs scale linearly in local router area."
    },

    # --- TEXTBOOK CHAPTER 2: SWITCHING & FLOW CONTROL EXTENSIONS ---
    {
        "id": "q16",
        "module": "Track 1: Fundamentals (Book Ch 2)",
        "tier": "Tier 1: Fundamental",
        "tier_level": 1,
        "base_points": 100,
        "question": "What is the foundational architectural advantage of Wormhole Switching compared to Store-and-Forward and Virtual Cut-Through?",
        "options": [
            "Wormhole switching decouples the buffer allocation unit (flit) from packet size, allowing router buffers to be as small as 1 to 4 flits, slashing SRAM buffer area by 75% to 90%.",
            "Wormhole switching eliminates the need for clock trees across the chip.",
            "Wormhole switching guarantees zero-latency light-speed optical traversal.",
            "Wormhole switching drops packets automatically when congested."
        ],
        "answer": 0,
        "explanation": "By allocating buffer storage at the flit granularity rather than requiring full packet buffering, Wormhole switching allows routers to operate with compact 2-4 flit queues, dramatically reducing router silicon area and power."
    },
    {
        "id": "q17",
        "module": "Track 1: Fundamentals (Book Ch 2)",
        "tier": "Tier 2: Core Engineering",
        "tier_level": 2,
        "base_points": 200,
        "question": "In credit-based flow control, what is the exact physical condition for the downstream buffer depth B_min required to sustain 100% full wire-rate throughput without pipeline stall bubbles?",
        "options": [
            "B_min must be equal to 1 flit regardless of link latency.",
            "B_min >= RTT * Peak_Injection_Rate, where RTT is the total credit turnaround loop delay (forward flight + receiver processing + reverse credit flight + transmitter processing).",
            "B_min must equal the total number of cores on the chip.",
            "B_min must be zero (bufferless deflection only)."
        ],
        "answer": 1,
        "explanation": "If buffer depth B < RTT, the upstream transmitter runs out of credits before the first credit pulse returns from downstream, forcing the forward physical link to sit idle during credit turnaround cycles."
    },
    {
        "id": "q18",
        "module": "Track 1: Fundamentals (Book Ch 2)",
        "tier": "Tier 3: Silicon Mastery",
        "tier_level": 3,
        "base_points": 300,
        "question": "How does Token Flow Control in the SWIFT NoC (Peh et al., IEEE TVLSI 2013) achieve up to 38% power reduction compared to canonical wormhole routers?",
        "options": [
            "By shutting off power to 90% of the router tiles permanently.",
            "By transmitting tokens ahead of data flits, allowing incoming flits to bypass input FIFO buffers entirely and cut through directly into the crossbar when tokens are granted.",
            "By routing packets exclusively through analog operational amplifiers.",
            "By replacing packet flits with radio-frequency pulses."
        ],
        "answer": 1,
        "explanation": "Token flow control enables flit buffer bypassing. Because flits avoid writing and reading SRAM buffer cells under low-to-medium network contention, dynamic buffer energy is dramatically slashed."
    }
]


def write_quiz_page(output_path: Path) -> None:
    questions_json = json.dumps(QUESTIONS, indent=2)

    content = f"""# 🎯 Network-on-Chip Architecture Certification & Quiz Challenge

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
      Choose your assessment mode. Your final score, accuracy, and cryptographic verification hash will be recorded and published to the Community Leaderboard.
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
        <label style="font-weight:600; font-size:0.85rem; display:block; margin-bottom:0.35rem;">Assessment Track</label>
        <select id="assessmentMode" class="noc-sim-select" style="width:100%; box-sizing:border-box;">
          <option value="full">Comprehensive Certification (12 Questions - Tiers 1, 2, 3)</option>
          <option value="tier1_sprint">Fundamentals Sprint (4 Questions - Tier 1)</option>
          <option value="grandmaster">Grandmaster Challenge (4 Questions - Tier 3 Mastery Only)</option>
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
      <div style="font-size:12px; text-transform:uppercase; letter-spacing:2px; color:#64748b; font-weight:700;">NoC-Lab Academic Credential Registry</div>
      <h1 style="font-size:1.65rem; font-weight:900; color:#0f172a; margin:10px 0 6px; letter-spacing:-0.5px;">CERTIFICATE OF ACHIEVEMENT</h1>
      <div style="font-size:13px; color:#475569; margin-bottom:16px;">This is to formally certify that</div>
      <div id="certCandidateName" style="font-size:1.85rem; font-weight:800; color:#1e3a8a; border-bottom:2px solid #cbd5e1; display:inline-block; padding:0 30px 4px; margin-bottom:12px;">Candidate Name</div>
      <div id="certCandidateOrg" style="font-size:14px; color:#475569; font-style:italic; margin-bottom:18px;">Institution / University</div>
      <div style="font-size:14px; max-width:520px; margin:0 auto 20px; line-height:1.5; color:#334155;">
        has successfully passed the examination in <strong>Network-on-Chip (NoC) Architecture, Router Microarchitecture &amp; Deadlock Avoidance Theory</strong>.
      </div>

      <div style="display:flex; justify-content:space-around; align-items:center; border-top:1px solid #e2e8f0; padding-top:16px; font-size:12px; color:#64748b;">
        <div><b>Score:</b> <span id="certScore" style="color:#0f172a;">--</span></div>
        <div><b>Verification Hash:</b> <span id="certHash" style="font-family:'JetBrains Mono', monospace; color:#0f172a;">NOC-CERT-2026-X89F</span></div>
        <div><b>Date:</b> <span id="certDate" style="color:#0f172a;">2026-11-05</span></div>
      </div>
    </div>

    <div style="display:flex; gap:0.75rem; justify-content:center; flex-wrap:wrap;">
      <button class="noc-sim-btn" onclick="submitToGithubIssue()" style="background:#16a34a;">📤 Submit Score to GitHub Leaderboard</button>
      <button class="noc-sim-btn" onclick="downloadCertificateSVG()">📥 Download Certificate (SVG)</button>
      <a href="../leaderboard/" class="noc-sim-btn secondary" style="text-decoration:none;">🏆 View Public Leaderboard</a>
      <button class="noc-sim-btn secondary" onclick="restartQuiz()">🔄 Retake Exam</button>
    </div>
  </div>
</div>

<script>
const QUESTIONS_BANK = {questions_json};

let activeQuestions = [];
let currentIdx = 0;
let userScore = 0;
let correctCount = 0;
let timerInterval = null;
let timeLeft = 35;
let candidate = {{ name: "", org: "", mode: "full", certId: "", date: "" }};

function startQuiz() {{
  candidate.name = document.getElementById("candidateName").value.trim() || "Hardware Architect";
  candidate.org = document.getElementById("candidateOrg").value.trim() || "Research Laboratory";
  candidate.mode = document.getElementById("assessmentMode").value;

  if (candidate.mode === "tier1_sprint") {{
    activeQuestions = QUESTIONS_BANK.filter(q => q.tier_level === 1);
  }} else if (candidate.mode === "grandmaster") {{
    activeQuestions = QUESTIONS_BANK.filter(q => q.tier_level === 3);
  }} else {{
    activeQuestions = [...QUESTIONS_BANK];
  }}

  currentIdx = 0;
  userScore = 0;
  correctCount = 0;

  document.getElementById("stepRegistration").style.display = "none";
  document.getElementById("stepResult").style.display = "none";
  document.getElementById("stepQuiz").style.display = "block";

  loadQuestion(currentIdx);
}}

function loadQuestion(idx) {{
  if (idx >= activeQuestions.length) {{
    finishQuiz();
    return;
  }}

  const q = activeQuestions[idx];
  document.getElementById("quizProgress").textContent = `Question ${{idx + 1}} of ${{activeQuestions.length}}`;
  document.getElementById("quizModuleBadge").textContent = q.module;
  document.getElementById("quizTierBadge").textContent = q.tier;
  document.getElementById("quizPtsBadge").textContent = `+${{q.base_points}} pts`;

  // Tier badge color
  const tBadge = document.getElementById("quizTierBadge");
  if (q.tier_level === 1) {{
    tBadge.style.background = "rgba(34, 197, 94, 0.12)";
    tBadge.style.color = "#16a34a";
    tBadge.style.borderColor = "rgba(34, 197, 94, 0.25)";
  }} else if (q.tier_level === 2) {{
    tBadge.style.background = "rgba(234, 88, 12, 0.12)";
    tBadge.style.color = "#ea580c";
    tBadge.style.borderColor = "rgba(234, 88, 12, 0.25)";
  }} else {{
    tBadge.style.background = "rgba(147, 51, 234, 0.12)";
    tBadge.style.color = "#9333ea";
    tBadge.style.borderColor = "rgba(147, 51, 234, 0.25)";
  }}

  document.getElementById("quizQuestionText").textContent = q.question;

  const optionsContainer = document.getElementById("quizOptions");
  optionsContainer.innerHTML = "";

  q.options.forEach((opt, oIdx) => {{
    const btn = document.createElement("button");
    btn.className = "noc-sim-select";
    btn.style.textAlign = "left";
    btn.style.padding = "0.75rem 1rem";
    btn.style.cursor = "pointer";
    btn.style.width = "100%";
    btn.style.fontSize = "0.92rem";
    btn.style.transition = "all 0.15s ease";
    btn.innerHTML = `<strong>${{String.fromCharCode(65 + oIdx)}}.</strong> ${{opt}}`;
    btn.onclick = () => checkAnswer(oIdx);
    optionsContainer.appendChild(btn);
  }});

  document.getElementById("quizFeedback").style.display = "none";
  document.getElementById("nextBtn").style.display = "none";

  // Start Timer
  clearInterval(timerInterval);
  timeLeft = 35;
  document.getElementById("quizTimer").textContent = `⏱️ ${{timeLeft}}s`;
  timerInterval = setInterval(() => {{
    timeLeft--;
    document.getElementById("quizTimer").textContent = `⏱️ ${{timeLeft}}s`;
    if (timeLeft <= 0) {{
      clearInterval(timerInterval);
      checkAnswer(-1); // Timeout
    }}
  }}, 1000);
}}

function checkAnswer(selectedIdx) {{
  clearInterval(timerInterval);
  const q = activeQuestions[currentIdx];
  const isCorrect = (selectedIdx === q.answer);

  if (isCorrect) {{
    correctCount++;
    const speedBonus = timeLeft * 3;
    userScore += q.base_points + speedBonus;
  }}

  document.getElementById("quizScore").textContent = `Score: ${{userScore}} pts`;

  // Disable option clicks
  const optionBtns = document.getElementById("quizOptions").children;
  for (let i = 0; i < optionBtns.length; i++) {{
    optionBtns[i].onclick = null;
    optionBtns[i].style.cursor = "default";
    if (i === q.answer) {{
      optionBtns[i].style.background = "rgba(34, 197, 94, 0.15)";
      optionBtns[i].style.borderColor = "#22c55e";
    }} else if (i === selectedIdx && !isCorrect) {{
      optionBtns[i].style.background = "rgba(239, 68, 68, 0.15)";
      optionBtns[i].style.borderColor = "#ef4444";
    }}
  }}

  // Show Feedback
  const fb = document.getElementById("quizFeedback");
  fb.style.display = "block";
  if (isCorrect) {{
    fb.style.background = "rgba(34, 197, 94, 0.1)";
    fb.style.border = "1px solid rgba(34, 197, 94, 0.3)";
    fb.style.color = "#166534";
    fb.innerHTML = `<strong>✓ Correct!</strong> ${{q.explanation}}`;
  }} else {{
    fb.style.background = "rgba(239, 68, 68, 0.1)";
    fb.style.border = "1px solid rgba(239, 68, 68, 0.3)";
    fb.style.color = "#991b1b";
    fb.innerHTML = `<strong>✗ Incorrect.</strong> The correct answer is <strong>${{String.fromCharCode(65 + q.answer)}}</strong>.<br>${{q.explanation}}`;
  }}

  document.getElementById("nextBtn").style.display = "inline-flex";
}}

function nextQuestion() {{
  currentIdx++;
  loadQuestion(currentIdx);
}}

function finishQuiz() {{
  document.getElementById("stepQuiz").style.display = "none";
  document.getElementById("stepResult").style.display = "block";

  const accuracy = Math.round((correctCount / activeQuestions.length) * 100);
  document.getElementById("resultSummary").innerHTML = `Candidate: <strong>${{candidate.name}}</strong> | Total Score: <strong>${{userScore}}</strong> pts | Accuracy: <strong>${{accuracy}}%</strong> (${{correctCount}}/${{activeQuestions.length}} correct)`;

  // Set Certificate Fields
  document.getElementById("certCandidateName").textContent = candidate.name;
  document.getElementById("certCandidateOrg").textContent = candidate.org;
  document.getElementById("certScore").textContent = `${{userScore}} pts (${{accuracy}}%)`;

  const now = new Date();
  candidate.date = now.toISOString().split("T")[0];
  document.getElementById("certDate").textContent = candidate.date;

  // Generate deterministic verification hash
  let hashVal = 0;
  const hashRaw = `${{candidate.name}}-${{userScore}}-${{candidate.date}}`;
  for (let i = 0; i < hashRaw.length; i++) {{
    hashVal = (hashVal << 5) - hashVal + hashRaw.charCodeAt(i);
    hashVal |= 0;
  }}
  candidate.certId = `NOC-CERT-${{now.getFullYear()}}-${{Math.abs(hashVal).toString(16).toUpperCase().padStart(6, '0')}}`;
  document.getElementById("certHash").textContent = candidate.certId;

  // Auto-record to local browser leaderboard storage
  saveScoreToLocalStorage({{
    name: candidate.name,
    org: candidate.org,
    track: candidate.mode === "grandmaster" ? "Grandmaster (Tier 3)" : (candidate.mode === "tier1_sprint" ? "Fundamentals Sprint" : "Comprehensive Exam"),
    score: userScore,
    accuracy: accuracy,
    certId: candidate.certId,
    date: candidate.date,
    type: "quiz"
  }});
}}

function saveScoreToLocalStorage(record) {{
  try {{
    const current = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
    current.unshift(record);
    localStorage.setItem("noc_leaderboard_records", JSON.stringify(current.slice(0, 50)));
  }} catch(e) {{
    console.error(e);
  }}
}}

function submitToGithubIssue() {{
  const repo = "network-on-chip/learning";
  const title = `[quiz-result] ${{candidate.name}} — ${{userScore}} pts — ${{candidate.certId}}`;
  const accuracy = Math.round((correctCount / activeQuestions.length) * 100);
  const body = [
    "### NoC Architecture Assessment Submission",
    `- **Candidate**: ${{candidate.name}}`,
    `- **Institution**: ${{candidate.org}}`,
    `- **Assessment Mode**: ${{candidate.mode}}`,
    `- **Total Score**: ${{userScore}} pts`,
    `- **Accuracy**: ${{accuracy}}% (${{correctCount}}/${{activeQuestions.length}} correct)`,
    `- **Credential Hash**: \`${{candidate.certId}}\``,
    `- **Date**: ${{candidate.date}}`,
    "",
    "```json",
    JSON.stringify({{
      candidate: candidate.name,
      org: candidate.org,
      mode: candidate.mode,
      score: userScore,
      accuracy: accuracy,
      certId: candidate.certId,
      date: candidate.date,
      type: "quiz"
    }}, null, 2),
    "```"
  ].join("\\n");

  const url = `https://github.com/${{repo}}/issues/new?title=${{encodeURIComponent(title)}}&body=${{encodeURIComponent(body)}}&labels=quiz-result,leaderboard`;
  window.open(url, '_blank');
}}

function downloadCertificateSVG() {{
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
    
    <text x="400" y="235" text-anchor="middle" font-family="'Inter', sans-serif" font-size="32" font-weight="800" fill="#1e3a8a">${{name}}</text>
    <line x1="200" y1="250" x2="600" y2="250" stroke="#cbd5e1" stroke-width="2" />
    
    <text x="400" y="285" text-anchor="middle" font-family="'Inter', sans-serif" font-size="16" font-style="italic" fill="#475569">${{org}}</text>
    <text x="400" y="340" text-anchor="middle" font-family="'Inter', sans-serif" font-size="15" fill="#334155">has mastered Network-on-Chip (NoC) Architecture,</text>
    <text x="400" y="365" text-anchor="middle" font-family="'Inter', sans-serif" font-size="15" fill="#334155">Router Microarchitecture &amp; Deadlock Avoidance Theory.</text>
    
    <line x1="80" y1="440" x2="720" y2="440" stroke="#e2e8f0" stroke-width="1" />
    
    <text x="120" y="475" font-family="'Inter', sans-serif" font-size="12" fill="#64748b">SCORE: <tspan font-weight="700" fill="#0f172a">${{score}}</tspan></text>
    <text x="400" y="475" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="12" fill="#64748b">HASH: <tspan font-weight="700" fill="#0f172a">${{hash}}</tspan></text>
    <text x="680" y="475" text-anchor="end" font-family="'Inter', sans-serif" font-size="12" fill="#64748b">DATE: <tspan font-weight="700" fill="#0f172a">${{date}}</tspan></text>
  </svg>`;

  const blob = new Blob([svgContent], {{ type: "image/svg+xml" }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Certificate_${{name.replace(/\s+/g, '_')}}_NoC.svg`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}}

function restartQuiz() {{
  document.getElementById("stepResult").style.display = "none";
  document.getElementById("stepRegistration").style.display = "block";
}}
</script>
"""
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote {output_path} ({len(QUESTIONS)} questions across 3 tiers).")


if __name__ == "__main__":
    docs = Path(__file__).resolve().parents[1] / "docs"
    write_quiz_page(docs / "quiz.md")
