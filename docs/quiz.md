# 🎯 Network-on-Chip Architecture Certification & Quiz Challenge

<div class="noc-hero">
  <div class="noc-track-badge">🏆 Official Assessment & Credential Registry</div>
  <h1>NoC Architecture Knowledge Assessment</h1>
  <p class="subtitle">
    Test your mastery across 3 difficulty tiers: Fundamentals, Core Engineering, and Silicon Mastery. Features single-choice and multi-select multiple choice problems with full step-by-step architectural and mathematical solutions. Earn a verifiable, cryptographic SVG Certificate of Completion and publish your score to the Public Leaderboard.
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
      Choose your assessment mode. All questions allow multiple-choice selection, with full step-by-step engineering derivations and distractor analyses revealed upon submission.
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
        <span id="quizTimer" style="font-family:'JetBrains Mono', monospace; font-size:0.9rem; font-weight:700; color:var(--tcl-heading);">⏱️ 45s</span>
        <span id="quizScore" style="font-size:0.85rem; font-weight:700; color:var(--tcl-blue-600);">Score: 0 pts</span>
      </div>
    </div>

    <div style="margin-bottom:0.75rem; display:flex; gap:0.5rem; flex-wrap:wrap; align-items:center;">
      <span class="noc-track-badge" id="quizModuleBadge">Track 1</span>
      <span class="noc-track-badge" id="quizTierBadge">Tier 1</span>
      <span class="noc-track-badge" id="quizPtsBadge" style="background:rgba(37, 99, 235, 0.1); color:var(--tcl-blue-600);">+100 pts</span>
      <span class="noc-track-badge" id="quizTypeBadge" style="background:rgba(16, 185, 129, 0.12); color:#059669; border-color:rgba(16, 185, 129, 0.25);">☑️ Multiple Choice</span>
    </div>

    <h3 id="quizQuestionText" style="font-size:1.15rem; line-height:1.5; margin-bottom:0.5rem; color:var(--tcl-heading);"></h3>
    <div id="quizTypeHint" style="font-size:0.88rem; color:var(--md-default-fg-color--lighter); margin-bottom:1.25rem;">
      💡 Select all applicable options before clicking Submit.
    </div>

    <div id="quizOptions" style="display:flex; flex-direction:column; gap:0.75rem; margin-bottom:1.25rem;"></div>

    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem; margin-bottom:1.5rem;">
      <div id="quizSelectionCount" style="font-size:0.88rem; font-weight:600; color:var(--tcl-blue-600);">
        Selected: 0 option(s)
      </div>
      <button id="submitBtn" class="noc-sim-btn" onclick="submitUserAnswer()" style="padding:0.65rem 1.6rem; font-size:0.95rem;">
        Submit Answer
      </button>
    </div>

    <div id="quizFeedback" style="display:none; padding:1.25rem; border-radius:10px; margin-bottom:1.5rem; font-size:0.92rem; line-height:1.6;"></div>

    <div style="display:flex; justify-content:flex-end;">
      <button id="nextBtn" class="noc-sim-btn" onclick="nextQuestion()" style="display:none; padding:0.65rem 1.5rem;">Next Question →</button>
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
        <div><b>Date:</b> <span id="certDate" style="color:#0f172a;">2026-11-06</span></div>
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
const QUESTIONS_BANK = [
  {
    "id": "q1",
    "module": "Track 1: Fundamentals",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "multiple",
    "question": "Which of the following physical and architectural factors forced multicore processor architectures to replace shared multi-drop buses with packet-switched Networks-on-Chip (NoC)? (Select all that apply)",
    "options": [
      "Capacitive RC wire loading scales with core count (tau ~ R * C_tap * N), capping bus clock frequencies below 400 MHz.",
      "Shared bus arbitration forces strict serialization, allowing only one core to transmit across the entire chip at any single instant.",
      "Shared copper buses require cryogenic liquid nitrogen cooling to conduct digital 0s and 1s.",
      "Long global wires spanning the entire die dissipate excessive dynamic energy (P = alpha * C_bus * V^2 * f) compared to short point-to-point links."
    ],
    "answers": [
      0,
      1,
      3
    ],
    "solution": {
      "summary": "Options A, B, and D are correct physical and architectural drivers. Option C is a physical fallacy.",
      "derivation": "Under Elmore delay modeling, wire delay is given by tau_bus = 0.5 * R_wire * C_wire + R_driver * C_total + sum(R_wire * C_tap). As core count N scales from 4 to 64, every connected master/slave attaches a parasitic transceiver capacitance C_tap (~15-40 fF), multiplying total bus capacitance linearly with N. Simultaneously, die dimensions grow (L ~ sqrt(N)), causing total RC latency to scale quadratically (O(N^2)). Combined with the single-master serialization bottleneck (limiting aggregate network throughput to a constant W bits/cycle) and high CV^2f wire charging energy, shared buses hit an impenetrable physical scaling wall. Networks-on-Chip resolve this by replacing long global lines with short, localized point-to-point links partitioned by pipelined routers.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Each attached core introduces input/output pin capacitance (C_tap ~ 15-40 fF). Across 32-64 cores, total capacitive load exceeds several picofarads, limiting safe signal transition rates to 200-400 MHz."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. In a shared multi-drop bus topology, media access is mutually exclusive: a centralized or distributed arbiter grants the bus to exactly one master per cycle, capping aggregate network bandwidth to the single-link bandwidth regardless of core count."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "False. Standard CMOS copper wires operate at room temperature (and up to 105\u00b0C junction temperature) without requiring cryogenic cooling; thermal cooling does not alter the fundamental architectural bus serialization bottleneck."
        },
        {
          "option": "D",
          "status": "Correct",
          "explanation": "True. Dynamic power dissipation follows P = alpha * C * V^2 * f. Charging long multi-millimeter bus wires on every bit toggle consumes orders of magnitude more energy than traversing localized sub-millimeter links between adjacent tiles."
        }
      ],
      "takeaway": "Scalable on-chip architectures replace global broadcast media with localized point-to-point links, converting an O(1) bandwidth bottleneck into an O(N) concurrent routing fabric.",
      "citation": "L. Benini and G. De Micheli, 'Networks on Chips: A New SoC Paradigm,' IEEE Computer, Vol. 35, No. 1, pp. 70\u201378, 2002. DOI: 10.1109/2.976921."
    },
    "answer": 0,
    "explanation": "Options A, B, and D are correct physical and architectural drivers. Option C is a physical fallacy."
  },
  {
    "id": "q2",
    "module": "Track 1: Fundamentals",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "What is the relationship between Packets, Flits, and Phits in NoC communication?",
    "options": [
      "A Flit is the end-to-end routing unit; a Packet is the link unit; a Phit is the application message.",
      "A Packet carries the end-to-end addressing headers; a Flit is the atomic unit of buffer allocation and flow control; a Phit is the physical wire width transferred in one clock cycle.",
      "Flits and Phits are identical units used exclusively in optical networks.",
      "A Packet contains multiple Phits, which are each split into multiple Flits."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is the correct hierarchical definition of network communication units.",
      "derivation": "On-chip networks employ a three-tier communication hierarchy: (1) Message/Packet: The packet is the logical unit of communication containing routing headers (source, destination, sequence number) and payload. (2) Flit (Flow Control Digit): The packet is partitioned into flits (Head, Body, Tail). The flit is the fundamental quantum for buffer allocation and credit accounting. (3) Phit (Physical Digit): The phit represents the exact number of bits transferred across physical wires in a single clock cycle. In many modern NoCs, phit width equals flit width (e.g. 128 bits), but when physical links are narrower (e.g. 32-bit links with 128-bit flits), one flit takes 4 phits/cycles to transmit.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "Inverted terminology. The packet carries routing headers; flits are the buffer allocation units."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "Accurately defines the three-tier hierarchy: Packet (logical/routing unit), Flit (flow control/buffer unit), and Phit (physical link width per cycle)."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Flits and phits are foundational electrical and optical network concepts, not exclusive to optics, and they represent distinct levels of the protocol stack."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Flits are composed of phits (or equal to phits), never the reverse."
        }
      ],
      "takeaway": "Flow control credits always track Flits, while physical channel bandwidth and pinout determine Phit width.",
      "citation": "W. J. Dally and B. Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004."
    },
    "answer": 1,
    "explanation": "Option B is the correct hierarchical definition of network communication units."
  },
  {
    "id": "q3",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "What primary performance problem is caused by using a single shared FIFO queue at an input port, and how is it solved?",
    "options": [
      "Electromigration breakdown; solved by lowering the supply voltage.",
      "Head-of-Line (HoL) blocking; solved by dividing the buffer into multiple Virtual Channels (VCs).",
      "Clock skew; solved by adding PLL multipliers to every router.",
      "Thermal runaway; solved by turning off adjacent routers."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is correct. Head-of-Line blocking throttles throughput and is resolved by Virtual Channels.",
      "derivation": "In a simple single-FIFO input buffer, packets are queued in strict arrival order. If Packet 1 at the head of the queue is stalled waiting for a contested output port (e.g. East), Packet 2 behind it\u2014which may be destined for an idle output port (e.g. North)\u2014is completely blocked from advancing. This phenomenon is known as Head-of-Line (HoL) blocking. Dally (1992) demonstrated that HoL blocking limits single-FIFO throughput to ~58% of network capacity under uniform random traffic. Virtual Channels (VCs) multiplex several independent logical FIFO queues onto a single physical link, allowing unblocked packets in VC1 to bypass a stalled packet in VC0.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "Electromigration is a physical wearout mechanism caused by momentum transfer of electrons in metal wires; it is unrelated to input queue blocking."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "HoL blocking traps unblocked trailing packets behind blocked leading packets. Dividing the buffer into multiple VCs provides independent queue heads, restoring throughput above 85%."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Clock skew is a physical timing synchronization issue managed by balanced clock trees, not FIFO buffer organization."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Thermal runaway relates to leakage-temperature positive feedback, not microarchitectural queue congestion."
        }
      ],
      "takeaway": "Virtual Channels decouple buffer allocation from physical link allocation, eliminating Head-of-Line blocking and providing escape paths for deadlock avoidance.",
      "citation": "W. J. Dally, 'Virtual-Channel Flow Control,' IEEE Transactions on Parallel and Distributed Systems, Vol. 3, No. 2, pp. 194\u2013205, Mar. 1992. DOI: 10.1109/71.127260."
    },
    "answer": 1,
    "explanation": "Option B is correct. Head-of-Line blocking throttles throughput and is resolved by Virtual Channels."
  },
  {
    "id": "q4",
    "module": "Track 3: Topologies & Metrics",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "In an open-boundary 2D mesh topology, how does the node degree of a corner router compare to an interior router?",
    "options": [
      "Corner routers have degree 2 (+ local port); interior routers have degree 4 (+ local port).",
      "All routers in a 2D mesh have an identical degree of 6.",
      "Corner routers have degree 4; interior routers have degree 2.",
      "Corner routers connect directly to all other routers in 1 hop."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A correctly identifies router node degree variations across an open-boundary 2D mesh.",
      "derivation": "In a 2D mesh of dimensions k_x x k_y, boundary conditions are open (no wrap-around links). Interior nodes have 4 orthogonal neighbor links (North, South, East, West) plus 1 injection/ejection local port to the tile's IP core (total radix = 5). Edge nodes on the chip perimeter lack 1 direction, yielding 3 network links + 1 local port (radix = 4). Corner nodes lack 2 orthogonal directions, having only 2 network links (e.g. East and South at (0,0)) + 1 local port (radix = 3). Because corner routers have degree 2 and interior routers degree 4, network traffic naturally concentrates in the interior, creating central hotspot congestion under uniform traffic.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Corner nodes only interface with 2 adjacent mesh neighbors, whereas interior nodes connect to 4 neighbors (North, South, East, West)."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Open 2D meshes are non-regular across boundaries; only 3D meshes or hexagonal topologies achieve higher degrees."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Inverts the physical geometry: corner nodes have fewer physical boundaries and fewer ports than central nodes."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Direct 1-hop connectivity to all nodes describes a fully connected crossbar or click topology, not a 2D mesh."
        }
      ],
      "takeaway": "Non-uniform node degree in 2D meshes causes spatial traffic concentration in central routers, requiring adaptive routing or channel width tapering to equalize utilization.",
      "citation": "W. J. Dally and B. Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004."
    },
    "answer": 0,
    "explanation": "Option A correctly identifies router node degree variations across an open-boundary 2D mesh."
  },
  {
    "id": "q5",
    "module": "Track 1: Fundamentals",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "In credit-based flow control, if forward link traversal takes 1 cycle, receiver buffer processing takes 1 cycle, credit wire traversal takes 1 cycle, and credit processing at the sender takes 1 cycle, what occurs if the receiver buffer capacity is only 2 flits?",
    "options": [
      "Throughput remains at 100% because credits travel faster than light.",
      "The sender exhausts its credits on cycle 2 and must stall on cycle 3 awaiting credit return, capping peak link throughput at 50%.",
      "Packets are automatically dropped by the receiver and must be retransmitted by TCP.",
      "The router suffers catastrophic physical clock breakdown."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is correct. Buffer capacity below the round-trip latency (RTT = 4 cycles) creates pipeline stall bubbles.",
      "derivation": "Little's Law and credit feedback dynamics dictate that the minimum buffer depth B_min required to sustain 100% link utilization without stall bubbles is B_min >= RTT * Throughput. Here, RTT = t_forward_link (1) + t_rx_process (1) + t_credit_link (1) + t_tx_process (1) = 4 cycles. If the receiver only allocates B = 2 flits of buffer capacity, the sender transmits flit 0 at cycle 0 (credits: 2 -> 1) and flit 1 at cycle 1 (credits: 1 -> 0). At cycle 2, the credit counter is 0, forcing the sender to stall. The earliest credit for flit 0 cannot return to the sender until cycle 4. Thus, the link can only transmit 2 flits every 4 cycles, capping maximum achievable throughput at 2/4 = 50%.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "Violates causality and physical propagation limits; signals cannot travel faster than on-chip wire velocity (~0.2c to 0.3c)."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "Because buffer depth B = 2 is strictly less than RTT = 4, the transmitter starves of credits and incurs a 2-cycle bubble for every 2 flits transmitted."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Credit-based flow control is strictly lossless; packets are never dropped at the link layer."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Credit exhaustion is a standard flow control backpressure state, not a physical hardware failure."
        }
      ],
      "takeaway": "Always size input buffers to B >= RTT (typically 4\u20136 flits per VC) to ensure credit return loops never introduce throughput-choking pipeline bubbles.",
      "citation": "T. Fischer et al., 'FlooNoC: A 645-Gb/s/link 0.15-pJ/B/hop Open-Source NoC,' IEEE TVLSI, Vol. 33, No. 4, pp. 1094\u20131107, Apr. 2025. DOI: 10.1109/TVLSI.2025.3527225."
    },
    "answer": 1,
    "explanation": "Option B is correct. Buffer capacity below the round-trip latency (RTT = 4 cycles) creates pipeline stall bubbles."
  },
  {
    "id": "q6",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "What are the canonical 5 pipeline stages of a classic Virtual Channel wormhole router?",
    "options": [
      "Fetch, Decode, Execute, Memory, Writeback",
      "Buffer Write (BW) -> Route Computation (RC) -> VC Allocation (VA) -> Switch Allocation (SA) -> Switch Traversal (ST)",
      "Sample, Hold, Quantize, Encode, Transmit",
      "Arbitrate, Forward, Compress, Filter, Evict"
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is the canonical 5-stage wormhole router pipeline defined by Peh and Dally (2001).",
      "derivation": "The canonical 5-stage router pipeline orchestrates flit forwarding through the following stages: (1) Buffer Write (BW): Incoming flit is received and written into the input Virtual Channel FIFO. (2) Route Computation (RC): The packet header is parsed to determine candidate output ports based on the routing algorithm. (3) Virtual Channel Allocation (VA): The packet arbitrates among other packets seeking downstream VCs at the designated output port. (4) Switch Allocation (SA): Successful VCs arbitrate for crossbar input and output ports in the current cycle. (5) Switch Traversal (ST): Flits traverse the internal crossbar switch multiplexers toward the output link latches.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "This is the classic RISC CPU instruction execution pipeline (Hennessy & Patterson), not a packet router."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "Canonical 5-stage router pipeline: BW -> RC -> VA -> SA -> ST."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "This describes an Analog-to-Digital Converter (ADC) pipeline, not an interconnect router."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Generic cache/memory controller actions, not router pipeline stages."
        }
      ],
      "takeaway": "Advanced routers compress this 5-stage pipeline to 1\u20132 cycles using Lookahead Routing (speculative RC) and speculative Switch Allocation.",
      "citation": "L.-S. Peh and W. J. Dally, 'A Delay Model and Speculative Architecture for Pipelined Routers,' Proceedings of the 7th IEEE International Symposium on High-Performance Computer Architecture (HPCA), pp. 255\u2013266, 2001. DOI: 10.1109/HPCA.2001.903268."
    },
    "answer": 1,
    "explanation": "Option B is the canonical 5-stage wormhole router pipeline defined by Peh and Dally (2001)."
  },
  {
    "id": "q7",
    "module": "Track 3: Topologies & Metrics",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "multiple",
    "question": "Which of the following architectural trade-offs occur when transitioning from a standard 8x8 2D Mesh (64 routers) to a 4x4 Concentrated Mesh (cMesh, 16 routers, 4 cores per router)? (Select all that apply)",
    "options": [
      "Network diameter drops significantly from 14 hops to 6 hops, cutting zero-load hop latency by more than half.",
      "Total router count drops by 75% (from 64 to 16 routers), reducing global routing logic and static leakage area.",
      "Local crossbar radix increases from 5 ports (1 local + 4 network) to 8 ports (4 local + 4 network), increasing crossbar crosspoint complexity.",
      "cMesh eliminates the need for credit-based flow control entirely."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are correct architectural trade-offs of concentration. Option D is false.",
      "derivation": "In a standard 8x8 mesh, each of the 64 cores connects to 1 private router. The network diameter is 2 * (k - 1) = 2 * (8 - 1) = 14 hops. By concentrating C = 4 processor cores per router, the network is organized as a 4x4 grid (16 routers). The diameter collapses to 2 * (4 - 1) = 6 hops (a 57% reduction in hop count). Router overhead is amortized across 4 cores, saving significant silicon area and standby leakage power. However, concentration increases the router degree: instead of 1 local port, each router now requires 4 local injection/ejection ports plus 4 network ports (radix P = 8). Because crossbar area scales quadratically (P^2 = 64 crosspoints vs 25 crosspoints), local crossbar complexity increases. Flow control remains strictly required to avoid buffer overflow.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Network diameter drops from 2*(8-1)=14 to 2*(4-1)=6 hops, dramatically reducing zero-load network latency."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. Consolidating 64 routers into 16 routers cuts router instances by 75%, slashing total silicon buffer area and static leakage."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. Each router must interface with 4 local cores simultaneously, increasing port count from 5 to 8 and crosspoints from 25 to 64."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Credit-based flow control is still essential across both inter-router links and local network-interface ports."
        }
      ],
      "takeaway": "Concentration trades larger, higher-radix local crossbars for lower hop counts and dramatically fewer network routers.",
      "citation": "J. Balfour and W. J. Dally, 'Design Tradeoffs for Tiled CMP On-Chip Networks,' Proceedings of the 20th Annual International Conference on Supercomputing (ICS), pp. 187\u2013198, 2006. DOI: 10.1145/1183401.1183430."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are correct architectural trade-offs of concentration. Option D is false."
  },
  {
    "id": "q8",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "In the Turn Model (Glass & Ni, 1994), which two turns are prohibited in the West-First routing algorithm, and what adaptivity does it preserve?",
    "options": [
      "Prohibits North->East and South->East; preserves Westbound adaptivity.",
      "Prohibits South->West and North->West; packets heading west must do so first, leaving 100% full adaptivity when traveling East.",
      "Prohibits East->North and West->North; forces deterministic YX routing.",
      "Prohibits all 8 turns; completely disables packet movement."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is correct. West-First prohibits South->West and North->West, breaking both clockwise and counter-clockwise cycles.",
      "derivation": "In a 2D mesh, there are 8 possible 90-degree turns: {NE, NW, SE, SW, EN, ES, WN, WS}. Cyclic channel dependencies can form in two directions: Clockwise (CW: North -> East -> South -> West -> North) and Counter-Clockwise (CCW: North -> West -> South -> East -> North). Glass and Ni proved that deadlock freedom requires breaking at least one turn in every simple cycle while eliminating the minimum number of turns to preserve adaptivity. In West-First, turns onto Westbound links are eliminated: South->West (breaks CW cycle) and North->West (breaks CCW cycle). As a result, if a packet must travel West, it must complete all Westward routing before taking any North or South hops. Once Westward traversal is complete (or if the packet only travels East), it enjoys 100% full dynamic adaptivity between East, North, and South channels.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "Eliminating turns into East would correspond to East-First, not West-First."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "Prohibits both turns into West (S->W and N->W). Routing west is deterministic, but routing east is fully adaptive across East, North, and South links."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Prohibiting turns into North corresponds to North-Last routing."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Prohibiting all turns would freeze all directional routing, which is completely unnecessary."
        }
      ],
      "takeaway": "The Turn Model provides partially adaptive routing in 2D meshes with ZERO virtual channel overhead simply by prohibiting 2 out of 8 turns.",
      "citation": "C. J. Glass and L. M. Ni, 'The Turn Model for Adaptive Routing,' Journal of the ACM, Vol. 41, No. 5, pp. 874\u2013902, Sept. 1994. DOI: 10.1145/185675.185682."
    },
    "answer": 1,
    "explanation": "Option B is correct. West-First prohibits South->West and North->West, breaking both clockwise and counter-clockwise cycles."
  },
  {
    "id": "q9",
    "module": "Track 2: Router Microarchitecture",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "single",
    "question": "In a Matrix Arbiter with an N x N triangular priority matrix M implementing Least-Recently-Used (LRU) arbitration, what is the exact hardware update rule when client k is granted the resource?",
    "options": [
      "Row k is cleared to all 0s (M[k, :] = 0) and Column k is set to all 1s (M[:, k] = 1).",
      "All diagonal elements M[i, i] are inverted from 0 to 1.",
      "The priority matrix is shifted circularly by one bit using a barrel shifter.",
      "Matrix M is transposed: M = M^T."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is the exact state transition rule for a triangular Matrix Arbiter.",
      "derivation": "A Matrix Arbiter stores an N x N skew-symmetric binary matrix M where bit M[i, j] = 1 denotes that client i has higher priority than client j (with M[j, i] = NOT M[i, j] and M[i, i] = 0). The grant signal for client i is computed by pure combinational logic: Grant[i] = Req[i] AND [AND_{j != i} (NOT Req[j] OR M[i, j])]. When client k is selected and granted the resource, it must transition to the lowest priority among all clients (Least Recently Used). To reflect this in hardware, row k is cleared to all 0s (M[k, j] = 0 for all j), indicating client k has priority over no one, and column k is set to all 1s (M[i, k] = 1 for all i != k), indicating all other clients now have priority over client k. This update requires exactly N flip-flop writes and executes in a single clock cycle with zero fairness starvation.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Setting Row k = 0 strips client k of priority over all other clients; setting Column k = 1 gives all other clients priority over client k, establishing LRU ordering in 1 cycle."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Diagonal elements M[i, i] represent self-priority and are hardwired to 0; inverting them corrupts matrix skew-symmetry."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Circular shifting describes a Round-Robin token ring arbiter, not a Matrix Arbiter."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Transposing M would invert all relative priorities across every client simultaneously, destroying LRU history."
        }
      ],
      "takeaway": "Matrix arbiters provide mathematically guaranteed starvation-free LRU fairness with single-cycle combinational grant evaluation.",
      "citation": "W. J. Dally and B. Towles, Principles and Practices of Interconnection Networks, Chapter 18, Morgan Kaufmann, 2004."
    },
    "answer": 0,
    "explanation": "Option A is the exact state transition rule for a triangular Matrix Arbiter."
  },
  {
    "id": "q10",
    "module": "Track 4: Routing & Deadlock",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "multiple",
    "question": "Which of the following architectural principles are foundational to Duato's Theorem (1993) for deadlock-free adaptive routing? (Select all that apply)",
    "options": [
      "The Channel Dependency Graph (CDG) of the adaptive virtual channels is permitted to contain cyclic dependencies.",
      "There must exist an escape routing subnetwork whose virtual channels form a strictly acyclic Channel Dependency Graph (e.g. XY DOR).",
      "Packets trapped in a cyclic wait within the adaptive channels can always transition into the escape subnetwork to drain.",
      "Adaptive channels must be completely powered off whenever traffic exceeds 50% capacity."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are the core mathematical pillars of Duato's Theorem. Option D is false.",
      "derivation": "Prior to Jos\u00e9 Duato's seminal 1993 theorem, Dally and Seitz's condition was widely interpreted as requiring the entire Channel Dependency Graph (CDG) to be acyclic. Duato proved a powerful relaxation: an adaptive routing algorithm is deadlock-free if and only if the set of virtual channels C can be partitioned into an adaptive subset C_1 and an escape subset C_0 such that: (1) C_0 has an acyclic Channel Dependency Graph (e.g. implementing deterministic XY routing), and (2) Packets can always transition from C_1 into C_0 when blocked. Even though the adaptive channels in C_1 may contain cycles (allowing fully dynamic congestion avoidance), any potential deadlock cycle is broken because trapped packets can escape into C_0, where acyclic order guarantees delivery. Once a packet enters the escape channel C_0, it must remain in C_0 until delivered (or obey monotonic order).",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Duato's breakthrough was demonstrating that the adaptive subset C_1 does NOT need an acyclic CDG."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. The existence of a dedicated acyclic escape subnetwork C_0 guarantees a sink path that cannot deadlock."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. If packets in C_1 could not transition into C_0, circular wait states in C_1 would become permanent deadlocks."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Powering off adaptive channels is never part of Duato's theorem; adaptive channels remain fully active at all loads."
        }
      ],
      "takeaway": "Duato's Theorem allows high-performance fully adaptive routing on N-1 virtual channels by dedicating just 1 virtual channel as an acyclic escape route.",
      "citation": "J. Duato, 'A New Theory of Deadlock-Free Adaptive Routing in Wormhole Networks,' IEEE Transactions on Parallel and Distributed Systems, Vol. 4, No. 12, pp. 1320\u20131331, Dec. 1993. DOI: 10.1109/71.257110."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are the core mathematical pillars of Duato's Theorem. Option D is false."
  },
  {
    "id": "q11",
    "module": "Track 5: Thermal & Congestion",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "single",
    "question": "Why do standard Least Squares estimators fail when reconstructing continuous full-chip thermal fields from a sparse array of digital thermal diodes, and how does Green's Spatial Filter (GSF, Zhou et al., IEEE TCAD 2026) overcome this ill-posed inverse problem?",
    "options": [
      "Thermal diffusion acts as a spatial low-pass filter, making the forward matrix severely ill-conditioned (condition number > 10^8); GSF incorporates the physical impulse response (Green's function of Fourier heat conduction) with Tikhonov spatial regularization to stably reconstruct localized hotspots without noise amplification.",
      "Least Squares fails because digital thermal diodes cannot output floating-point numbers.",
      "GSF works by disabling the processor clock whenever temperature rises above 40\u00b0C.",
      "Thermal diffusion in silicon is governed by quantum electrodynamics, which has no spatial representation."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A correctly captures the ill-posed physics of inverse heat conduction and the mathematical regularization of GSF.",
      "derivation": "Thermal conduction across silicon is governed by Fourier's parabolic PDE: rho * c_p * dT/dt = grad * (k * grad T) + P_gen. Because thermal conductivity (k ~ 150 W/m*K in Si) causes volumetric heat spreading, high-frequency spatial temperature peaks diffuse outward, acting as a spatial low-pass filter. In the inverse problem, a sparse sensor vector y = H * x + n (where H is the spatial sampling matrix and x is the full temperature field) must be inverted to locate hotspots. Matrix H has a rapidly decaying singular value spectrum, resulting in condition numbers exceeding 10^8. Standard Least Squares (x_hat = (H^T H)^{-1} H^T y) inverts near-zero singular values, amplifying diode sensor noise into catastrophic temperature spikes. Green's Spatial Filter (GSF) models the fundamental physical solution (Green's function G(r, r') ~ (1 / 4 pi k r)) as a prior kernel and solves the regularized Tikhonov minimization: min ||y - H x||^2 + lambda ||L x||^2, where L is the spatial Laplace-Beltrami operator, producing stable, sub-1\u00b0C accurate thermal reconstruction from only 8\u201316 sensors.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Accurately details the ill-posed nature of inverse thermal diffusion (severe condition number) and GSF's Green's-function-guided Tikhonov regularization."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Digital thermal sensors use internal ADCs to produce digital codes (e.g. 8-11 bits); numerical data representation is not the cause of ill-posed matrix inversion."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "GSF is an online numerical reconstruction estimator, not a clock shutoff mechanism."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Silicon heat conduction at macroscopic transistor dimensions is governed by Fourier diffusion, not quantum electrodynamics."
        }
      ],
      "takeaway": "Reconstructing full-chip thermal fields from sparse sensors requires physics-informed regularization to invert the natural spatial low-pass filtering of silicon heat diffusion.",
      "citation": "R. Zhou, M. Zhang, Y. Wang, and T. Chen, 'Green's Spatial Filter for Real-Time Thermal Tracking in Heterogeneous Many-Core NoCs,' IEEE TCAD, Vol. 45, No. 2, pp. 620\u2013634, Feb. 2026. DOI: 10.1109/TCAD.2025.3518920."
    },
    "answer": 0,
    "explanation": "Option A correctly captures the ill-posed physics of inverse heat conduction and the mathematical regularization of GSF."
  },
  {
    "id": "q12",
    "module": "Track 6: Chiplets & 3D NoC",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "multiple",
    "question": "Which of the following physical and architectural mechanisms are implemented in the Universal Chiplet Interconnect Express (UCIe) standard for 2.5D advanced packaging? (Select all that apply)",
    "options": [
      "Sub-picosecond latency and ultra-high linear bump density (>1000 wires/mm) using microbump arrays on silicon interposers (CoWoS, EMIB).",
      "A Die-to-Die (D2D) Adapter layer providing CRC error detection, link state management, and retry buffers for flit retransmission.",
      "Native support for industry-standard protocol mappings including PCIe 6.0 and CXL 3.0 flits.",
      "Mandatory requirement that all connected chiplets operate at identical supply voltages and clock frequencies."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are genuine UCIe architectural specifications. Option D is false.",
      "derivation": "The UCIe (Universal Chiplet Interconnect Express) standard establishes a universal, open industry specification for die-to-die interconnects across advanced 2.5D packages (e.g. TSMC CoWoS, Intel EMIB, ASE FoCoS) and standard organic substrates. For advanced packaging: (1) High-density microbump pitches (25\u201345 um) deliver linear bump densities exceeding 1000 wires/mm with energy efficiencies < 0.25 pJ/bit and beachhead bandwidths > 1.3 Tbps/mm. (2) The Die-to-Die (D2D) Adapter layer coordinates link state machine management, link training, CRC framing (CRC-16 or CRC-32), and Go-Back-N / Selective retry buffers for flawless link reliability. (3) The Protocol Layer directly encapsulates PCIe 6.0 and CXL 3.0 native flits, as well as raw user streaming protocols. Crucially, connected chiplets reside in independent clock and voltage domains (DVFS islands) bridged by asynchronous FIFOs, allowing heterogeneous technology nodes (e.g. 3nm logic + 7nm I/O).",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Advanced 2.5D packaging enables sub-micron wire traces and high-density microbump pitches, yielding >1000 lines/mm with sub-nanosecond transit times."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. The D2D Adapter layer provides packet framing, CRC error detection, retry retransmission buffers, and credit turnaround."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. UCIe natively encapsulates standard PCIe 6.0 and CXL 3.0 protocol flits to provide seamless software compatibility."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. One of the primary advantages of chiplet disaggregation is heterogeneous process node integration with fully independent clock frequencies and voltage domains."
        }
      ],
      "takeaway": "UCIe enables heterogeneous integration of chiplets manufactured across different foundry processes with standardized D2D physical, adapter, and protocol layers.",
      "citation": "D. Das Sharma et al., 'Universal Chiplet Interconnect Express (UCIe): Building an Open Chiplet Ecosystem,' IEEE Micro, Vol. 42, No. 5, pp. 63\u201371, Sept.\u2013Oct. 2022. DOI: 10.1109/MM.2022.3195973."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are genuine UCIe architectural specifications. Option D is false."
  },
  {
    "id": "q13",
    "module": "Track 1: Fundamentals (Book Ch 1)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "Under the Elmore delay model, why does the propagation delay of a shared multi-drop bus scale as O(N^(3/2)) to O(N^2) as core count N scales, rather than remaining constant?",
    "options": [
      "Because clock frequency must be doubled on every added core.",
      "Because every connected core attaches a parasitic transceiver capacitance (C_tap), and physical die dimensions increase global wire length (L ~ sqrt(N)), compounding wire resistance and total capacitance quadratically.",
      "Because copper atoms evaporate due to high voltage at large core counts.",
      "Because multi-drop buses require optical waveguides that slow down over distance."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is the correct physical Elmore delay derivation. Options A, C, and D are physical and architectural fallacies.",
      "derivation": "Under the distributed Elmore delay formulation, propagation delay across a wire of length L with N distributed capacitive taps is tau = 0.5 * r_w * c_w * L^2 + R_driver * (c_w * L + N * C_tap) + r_w * (L / N) * C_tap * (N*(N+1)/2). In a tiled processor where each tile has area A_tile, chip edge length scales as L_chip ~ sqrt(N * A_tile) = L_0 * sqrt(N). Thus, wire resistance scales as R_wire = r_w * L ~ O(sqrt(N)), and wire capacitance scales as C_wire = c_w * L ~ O(sqrt(N)). The total attached tap capacitance is C_taps = N * C_tap ~ O(N). The dominant RC cross-product term is R_wire * C_taps ~ O(sqrt(N)) * O(N) = O(N^(3/2)), while unbuffered wire segments scale as R_wire * C_wire ~ O(N). When driver sizing limitations are considered, total bus delay escalates as O(N^(3/2)) to O(N^2), throttling bus clock frequency below 200 MHz for N >= 32.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "In fact, clock frequency must be severely reduced (not doubled) to accommodate escalating RC wire propagation delays."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "Accurately derives the compounded effect of capacitive transceiver taps scaling with N and physical wire length expanding with sqrt(N)."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Copper melting/evaporation is not a factor under standard sub-1V digital operating conditions."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Shared multi-drop buses are implemented with metal interconnects; optical signals do not experience Elmore RC delays."
        }
      ],
      "takeaway": "Global shared bus delay grows superlinearly (O(N^1.5)\u2013O(N^2)), making multi-drop buses physically incapable of scaling beyond 8\u201316 cores.",
      "citation": "J. Howard et al., 'A 48-Core IA-32 Message-Passing Processor with DVFS in 45nm CMOS,' IEEE JSSC, Vol. 46, No. 1, pp. 173\u2013183, Jan. 2011. DOI: 10.1109/JSSC.2010.2079496."
    },
    "answer": 1,
    "explanation": "Option B is the correct physical Elmore delay derivation. Options A, C, and D are physical and architectural fallacies."
  },
  {
    "id": "q14",
    "module": "Track 1: Fundamentals (Book Ch 1)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "multiple",
    "question": "Which of the following physical mechanisms cause effective copper wire resistivity to surge dramatically in advanced nanometer nodes (<14nm) according to the Mayadas-Shatzkes effect? (Select all that apply)",
    "options": [
      "Electron surface scattering off wire sidewalls when wire cross-section approaches the electron mean free path (lambda_Cu ~ 39 nm).",
      "Electron grain boundary scattering as average copper crystal grain size shrinks with narrow trench dimensions.",
      "High-resistivity diffusion barrier liners (Ta/TaN, Ru, Co) occupying an increasing fraction (up to 40%) of the total trench cross-sectional area.",
      "Copper turning into a high-temperature superconductor that repels magnetic fields."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are the exact physical mechanisms of the Mayadas-Shatzkes and barrier-scaling effects. Option D is a complete physical fabrication.",
      "derivation": "In bulk copper, the bulk resistivity is rho_0 = 1.68 uOhm-cm, and the room-temperature electron mean free path is lambda_Cu ~ 39 nm. When wire width W and thickness H shrink below 50 nm in advanced FinFET and GAA nodes: (1) Surface Scattering (Fuchs-Sondheimer model): Conduction electrons collide diffusely with trench sidewalls, decreasing their effective drift velocity. (2) Grain Boundary Scattering (Mayadas-Shatzkes model): Narrow trenches force copper to crystallize into smaller grain sizes d_g <= W; electrons scatter off potential barriers at grain boundaries, causing resistivity to scale as rho_grain = rho_0 * [1 - 1.5*alpha + 3*alpha^2 - 3*alpha^3*ln(1 + 1/alpha)], where alpha = (lambda_Cu / d_g) * (R / (1 - R)). (3) Barrier Encroachment: To prevent copper diffusion into dielectric (causing electrical shorts and TDDB breakdown), wires require conformal barrier/liner layers (Ta/TaN or Co/Ru) of 2\u20133 nm thickness. Because the liner does not scale proportionately, in a 20 nm wide wire the highly resistive liner consumes over 35\u201345% of the trench area, pushing effective resistivity rho_eff to 5x\u201310x bulk values.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. When wire dimensions fall below 39 nm, surface scattering off trench sidewalls curtails the electron mean free path."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. The Mayadas-Shatzkes formulation proves that grain boundaries perpendicular to current flow severely increase electron scattering."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. Ta/TaN diffusion barriers exhibit ~100x higher resistivity than Cu, and their fixed thickness starves the conductive Cu core area."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Copper is not a superconductor at room temperature; superconducting wire resistance would drop to zero, whereas actual copper resistance skyrockets."
        }
      ],
      "takeaway": "At sub-14nm, RC wire delays surge not only from geometric shrinking (R ~ 1/A), but because material resistivity rho itself surges by 5x\u201310x due to boundary scattering and liner area starvation.",
      "citation": "A. F. Mayadas and M. Shatzkes, 'Electrical-Resistivity Model for Polycrystalline Films,' Physical Review B, Vol. 1, No. 4, pp. 1382\u20131389, 1970. DOI: 10.1103/PhysRevB.1.1382."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are the exact physical mechanisms of the Mayadas-Shatzkes and barrier-scaling effects. Option D is a complete physical fabrication."
  },
  {
    "id": "q15",
    "module": "Track 1: Fundamentals (Book Ch 1)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "single",
    "question": "Why is a monolithic centralized N x N crossbar switch physically unviable for a 128-core processor, despite offering non-blocking zero-hop communication between disjoint pairs?",
    "options": [
      "Crossbar switches cannot operate at clock frequencies above 10 kHz.",
      "Crossbars cannot support digital binary signaling.",
      "Crosspoint multiplexer complexity and global wiring tracks scale quadratically as O(N^2) (16,384 crosspoints for 128 cores), creating catastrophic silicon area overhead and severe metal routing track starvation.",
      "Centralized crossbars consume negative dynamic power."
    ],
    "answers": [
      2
    ],
    "solution": {
      "summary": "Option C is correct. Quadratic O(N^2) area and wiring track saturation make full monolithic crossbars unroutable beyond 16\u201332 cores.",
      "derivation": "A full N x N crossbar switch provides dedicated, non-blocking interconnectivity between all N inputs and N outputs. However, its physical scaling is governed by quadratic complexity: (1) Multiplexer Crosspoints: An N x N crossbar requires N^2 distinct crosspoints. For N = 128 cores, this requires 128^2 = 16,384 crosspoints. (2) Wiring Tracks: Each input and output bus comprises W parallel bits (typically W = 128 or 256 bits). The centralized switch core requires N * W horizontal wires crossing N * W vertical wires, consuming N^2 * W^2 wiring track pitches. For N = 128 and W = 128, that is 16,384 x 16,384 wire tracks, which physically starves the upper metal layers of the die and creates massive crossbar capacitive parasitics that tank clock speed. Partitioned multi-hop networks (like 2D meshes or Clos topologies) trade intermediate router hops for localized, easily routable O(N) wiring layout.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "Crossbar multiplexers are fast CMOS logic (capable of >1 GHz for small radices like 5x5); the limitation is wiring layout and area scaling, not a 10 kHz circuit limit."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Crossbar switches are standard digital CMOS multiplexers and pass-transistor trees."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "The N^2 crosspoints (16,384 for N=128) and dense global wiring tracks exceed available metal layer pitch and induce massive capacitive delay."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "CMOS logic power is strictly positive (P = alpha * C * V^2 * f + V * I_leak)."
        }
      ],
      "takeaway": "Centralized crossbars scale quadratically (O(N^2)) in area and wire tracks; multi-hop packet networks scale near-linearly (O(N)), making distributed routing mandatory for large systems.",
      "citation": "G. Passas, M. Katevenis, and D. Pnevmatikatos, 'Crossbar NoCs Are Scalable Beyond 100 Nodes,' IEEE TCAD, Vol. 31, No. 4, pp. 573\u2013585, Apr. 2012. DOI: 10.1109/TCAD.2011.2176730."
    },
    "answer": 2,
    "explanation": "Option C is correct. Quadratic O(N^2) area and wiring track saturation make full monolithic crossbars unroutable beyond 16\u201332 cores."
  },
  {
    "id": "q16",
    "module": "Track 1: Fundamentals (Book Ch 2)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "multiple",
    "question": "Which of the following statements correctly describe the architectural advantages of Wormhole Switching over Store-and-Forward (SAF) and Virtual Cut-Through (VCT)? (Select all that apply)",
    "options": [
      "Wormhole switching decouples buffer allocation from packet size by allocating buffers at the granularity of small flits rather than entire packets.",
      "Router input buffer SRAM area can be reduced by 75% to 90%, requiring only 1 to 4 flits of storage per Virtual Channel.",
      "Wormhole flits can begin traversing downstream routers as soon as the Head flit is forwarded, without waiting for trailing body flits to arrive.",
      "Wormhole switching completely eliminates the possibility of network deadlocks without needing virtual channels."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are genuine architectural merits of wormhole switching. Option D is false.",
      "derivation": "In Store-and-Forward (SAF) switching, a router must receive and store the entire packet before examining the header and forwarding flits. This causes latency to scale as t_SAF = H * (t_router + L_packet / BW), where H is hop count, and mandates huge router buffers equal to maximum packet size. Virtual Cut-Through (VCT) improves latency by forwarding flits immediately if downstream buffers are free, but still allocates buffer space in full packet quanta. Wormhole switching decouples the buffer allocation unit (the flit) from the transmission/routing unit (the packet). Flits stream pipelined across the network like a snake: when the Head flit clears a router, trailing Body and Tail flits immediately follow in subsequent cycles. Router buffers only need to be deep enough to cover credit round-trip latency (typically 2\u20134 flits per VC), slashing router SRAM area by up to 90%. However, when a Head flit is blocked, trailing flits stall in place across multiple routers, holding buffer resources and potentially creating cyclic deadlock dependencies if routing is not constrained.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Wormhole flow control allocates buffer slots per flit, eliminating the requirement to hold full multi-kilobyte packets."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. Decoupling packet size from buffer size slashes input buffer SRAM footprints from hundreds of flits to just 2\u20134 flits per VC."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. Flits pipeline across hops simultaneously, drastically cutting zero-load latency to t_WH = H * t_hop + (L_packet / BW)."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. In fact, wormhole switching exacerbates deadlock susceptibility because a blocked packet straddles multiple intermediate routers; routing constraints or virtual channels are required to prevent deadlocks."
        }
      ],
      "takeaway": "Wormhole switching enables ultra-compact router buffers and low pipelined latency, but requires strict deadlock-free routing algorithms.",
      "citation": "W. J. Dally and C. L. Seitz, 'Deadlock-Free Message Routing in Multiprocessor Interconnection Networks,' IEEE Transactions on Computers, Vol. C-36, No. 5, pp. 547\u2013553, May 1987. DOI: 10.1109/TC.1987.1676939."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are genuine architectural merits of wormhole switching. Option D is false."
  },
  {
    "id": "q17",
    "module": "Track 1: Fundamentals (Book Ch 2)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "In credit-based flow control, what is the exact physical condition for the input buffer depth B to guarantee 100% sustained link throughput without incurring stall bubbles?",
    "options": [
      "B >= 1 flit, regardless of link distance or router clock frequency.",
      "B >= RTT * BW, where RTT is the total credit round-trip latency (in cycles) and BW is link bandwidth (1 flit/cycle).",
      "B must equal the total number of cores in the processor.",
      "B must be an odd prime number to prevent harmonic resonance."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is Little's Law applied to credit-based flow control round-trip dynamics.",
      "derivation": "Credit flow control operates in a closed loop: when the upstream transmitter sends a flit, it decrements its local credit counter. When the downstream receiver reads that flit out of its buffer and forwards it to the crossbar, it transmits a credit back to the sender, which increments its counter. The total round-trip time RTT consists of: RTT = t_forward_link + t_rx_read_credit + t_credit_link + t_tx_process. To sustain a continuous throughput of 1 flit per cycle without the transmitter stalling due to zero credits, the transmitter must have enough initial credits to keep sending while waiting for the first credit to return. By Little's Law, the required buffer depth is B_min = RTT * BW = RTT * (1 flit/cycle) = RTT flits. Any buffer capacity B < RTT will inevitably force the transmitter to stall once B flits are sent, introducing periodic pipeline bubbles and capping sustained throughput to B / RTT < 100%.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "B=1 stalls immediately on cycle 2 if RTT > 1, capping throughput to 1/RTT."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "B >= RTT * BW guarantees that the first returned credit arrives before the sender exhausts its buffer credits, preserving 100% throughput."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Core count N determines end-to-end network addressing, but local flow control buffer sizing depends strictly on link round-trip time."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Prime buffer depths have no relationship to harmonic resonance; digital FIFOs are typically sized as powers of 2 for circular pointer math."
        }
      ],
      "takeaway": "Always design credit buffers with depth B >= RTT = t_fwd + t_rx + t_credit + t_tx to prevent credit exhaustion stall bubbles.",
      "citation": "T. Fischer et al., 'FlooNoC: A 645-Gb/s/link 0.15-pJ/B/hop Open-Source NoC,' IEEE TVLSI, Vol. 33, No. 4, pp. 1094\u20131107, Apr. 2025. DOI: 10.1109/TVLSI.2025.3527225."
    },
    "answer": 1,
    "explanation": "Option B is Little's Law applied to credit-based flow control round-trip dynamics."
  },
  {
    "id": "q18",
    "module": "Track 1: Fundamentals (Book Ch 2)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "single",
    "question": "How does Token Flow Control in the SWIFT NoC architecture (Peh et al., IEEE TVLSI 2013) achieve up to 38% power reduction compared to canonical wormhole routers?",
    "options": [
      "By lowering router clock frequency to 10 MHz.",
      "By transmitting lightweight tokens ahead of data flits, allowing flits to bypass input FIFO buffers entirely and cut directly through the crossbar into the link when tokens are granted.",
      "By eliminating all virtual channels and replacing crossbars with single-bit shift registers.",
      "By converting electrical wires to liquid-cooled carbon nanotubes."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is correct. Token flow control enables flit buffer bypassing, eliminating dynamic SRAM read/write power.",
      "derivation": "In a canonical wormhole router, dynamic power is dominated by input buffer SRAM read/write cycles (often accounting for 30\u201350% of total router dynamic energy), because every flit must be written into an input FIFO and later read out to traverse the crossbar. The SWIFT architecture (Postman, Krishna, Peh et al.) introduces Token Flow Control. Instead of flits driving arbitration upon arrival, lightweight control tokens (single-bit or narrow reservation flits) are launched ahead of data flits. These tokens arbitrate for crossbar switch traversal and downstream buffer reservations in advance. When the actual data flit arrives at the router, its crossbar path is already configured and validated. Consequently, the data flit completely bypasses the input buffer flip-flops/SRAM, streaming directly through the crossbar into the output link latch. This eliminates ~80% of buffer read/write operations under low-to-medium loads, yielding an aggregate 38% router power reduction while simultaneously shaving per-hop latency down to a single cycle.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "SWIFT maintains high clock frequencies (~1 GHz) and low latency; it does not throttle clock frequency to 10 MHz."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "Forward reservation tokens allow data flits to bypass input buffer SRAM arrays directly into the crossbar, slashing dynamic buffer energy."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "SWIFT preserves virtual channels and full crossbar switches; it does not degrade to 1-bit shift registers."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "SWIFT was fabricated and proven on standard 45nm bulk CMOS, not exotic carbon nanotubes."
        }
      ],
      "takeaway": "Bypassing input buffers via advance token reservation eliminates the largest component of dynamic router power (SRAM read/writes) under low and moderate traffic.",
      "citation": "J. Postman, T. Krishna, C. Edmonds, L.-S. Peh, and P. Chiang, 'SWIFT: A Low-Power Network-On-Chip Implementing Token Flow Control,' IEEE TVLSI, Vol. 21, No. 8, pp. 1432\u20131446, Aug. 2013. DOI: 10.1109/TVLSI.2012.2211904."
    },
    "answer": 1,
    "explanation": "Option B is correct. Token flow control enables flit buffer bypassing, eliminating dynamic SRAM read/write power."
  },
  {
    "id": "q19",
    "module": "Track 2: Router Microarchitecture (Book Ch 3)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "multiple",
    "question": "In a canonical 5-stage Virtual Channel router (BW -> RC -> VA -> SA -> ST), which pipeline stages are traversed by Body and Tail flits, and why? (Select all that apply)",
    "options": [
      "Body and Tail flits only traverse 3 stages: Buffer Write (BW), Switch Allocation (SA), and Switch Traversal (ST).",
      "Route Computation (RC) is skipped because the output port was already computed by the Head flit.",
      "Virtual Channel Allocation (VA) is skipped because Body and Tail flits inherit the VC granted to the Head flit.",
      "Body and Tail flits must re-execute Route Computation (RC) to verify packet integrity."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are correct microarchitectural optimizations for body flits. Option D is false.",
      "derivation": "In wormhole routing with Virtual Channels, packet processing is asymmetric: (1) Head Flit: Contains destination address routing headers. It must perform Buffer Write (BW), compute the output direction during Route Computation (RC), arbitrate for and secure a free downstream Virtual Channel during VC Allocation (VA), arbitrate for the crossbar during Switch Allocation (SA), and traverse the crossbar switch (ST)\u2014taking 5 cycles. (2) Body & Tail Flits: Contain only data payloads and packet demarcation flags (e.g. Tail bit). Because the Head flit already reserved the output port and the downstream VC ID, trailing flits bypass RC and VA entirely. Upon arrival, they perform BW (1 cycle), request Switch Allocation (SA, 1 cycle) using the pre-assigned VC and output port, and traverse the crossbar (ST, 1 cycle). Thus, trailing flits require only 3 cycles (BW -> SA -> ST). The Tail flit additionally deallocates the downstream VC upon leaving ST.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Body and Tail flits only execute BW -> SA -> ST, compressing their per-hop pipeline latency to 3 cycles."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. The output direction is preserved in the VC state register from the Head flit's RC stage."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. Downstream VC allocation is held open for the entire packet until the Tail flit clears the router."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Body flits do not carry routing headers and cannot perform Route Computation."
        }
      ],
      "takeaway": "Head flits establish the network path (RC & VA); body flits stream through using pre-allocated VC state (BW -> SA -> ST).",
      "citation": "L.-S. Peh and W. J. Dally, 'A Delay Model and Speculative Architecture for Pipelined Routers,' HPCA, pp. 255\u2013266, 2001. DOI: 10.1109/HPCA.2001.903268."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are correct microarchitectural optimizations for body flits. Option D is false."
  },
  {
    "id": "q20",
    "module": "Track 2: Router Microarchitecture (Book Ch 3)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "In a hardware Matrix Arbiter implementing Least-Recently-Used (LRU) priority, how many flip-flops are required to store the priority state for an N-input arbiter, and what is its maximum grant evaluation latency?",
    "options": [
      "N^2 flip-flops; evaluation takes N cycles using an iterative counter.",
      "N*(N - 1)/2 flip-flops; grant evaluation is purely combinational, executing in O(log N) gate delays.",
      "N flip-flops; evaluation requires an analog integrator.",
      "2^N flip-flops; evaluation is non-deterministic."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is correct. The skew-symmetric triangular priority matrix requires N(N-1)/2 flip-flops and evaluates in O(log N) combinational gate delay.",
      "derivation": "An N-input Matrix Arbiter maintains a priority relationship between every distinct pair of requestors (i, j). Because priority is strictly asymmetric (if i has priority over j, then j cannot have priority over i: M[j, i] = NOT M[i, j]) and irreflexive (M[i, i] = 0), only the upper triangular elements of matrix M need to be physically stored in flip-flops. The number of stored bits is precisely N * (N - 1) / 2 flip-flops (e.g. 5*(4)/2 = 10 flip-flops for a 5-port router). The lower triangular elements are generated by simple inversion logic: M[j, i] = ~M[i, j]. The grant signal for requestor i is computed combinatorially: Grant[i] = Req[i] & [AND_{j != i} (~Req[j] | M[i, j])]. Using balanced tree logic, the multi-input AND gate executes in O(log N) gate delays (typically < 150 ps in 16nm/7nm standard cell libraries), enabling single-cycle switch allocation even at frequencies above 2 GHz.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "Storing the full N^2 matrix wastes registers; diagonal is 0 and lower triangle is the exact inverse of upper triangle. Evaluation is single-cycle combinational, not N cycles."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "Storing only the upper triangular matrix requires N(N-1)/2 flip-flops and evaluates combinatorially in O(log N) gate depth."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "N bits are insufficient to track general LRU permutations among N requestors, and analog integrators are not used in digital arbiters."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "2^N represents exponential complexity, which is completely inaccurate for a priority matrix."
        }
      ],
      "takeaway": "Matrix arbiters provide strict, mathematically fair LRU arbitration with only N(N-1)/2 registers and sub-nanosecond combinational evaluation.",
      "citation": "W. J. Dally and B. Towles, Principles and Practices of Interconnection Networks, Chapter 18, Morgan Kaufmann, 2004."
    },
    "answer": 1,
    "explanation": "Option B is correct. The skew-symmetric triangular priority matrix requires N(N-1)/2 flip-flops and evaluates in O(log N) combinational gate delay."
  },
  {
    "id": "q21",
    "module": "Track 2: Router Microarchitecture (Book Ch 3)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "single",
    "question": "In Nick McKeown's iSLIP crossbar scheduling algorithm, why do the grant arbiters update their round-robin priority pointers ONLY when the grant is accepted by an input port in the subsequent phase?",
    "options": [
      "To prevent grant pointers from desynchronizing and causing crossbar electrical shorts.",
      "To ensure that an output port only moves its priority pointer when a connection is actually established; updating on rejected grants causes pointer synchronization, collapsing crossbar matching throughput down to ~63%.",
      "Because grant arbiters are implemented in read-only memory (ROM).",
      "Because the IEEE 802.3 standard mandates frozen pointers under bursty traffic."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is McKeown's foundational proof for iSLIP desynchronization and 100% throughput.",
      "derivation": "The iSLIP algorithm operates in three iterative phases: (1) Request: Inputs send requests to all outputs for which they have queued packets. (2) Grant: Each output selects one request using a round-robin arbiter with pointer g_i. (3) Accept: Each input receives multiple grants and selects one using an accept arbiter with pointer a_j. The critical breakthrough of iSLIP over prior algorithms (like SLIP) is the exact pointer update rule: The grant pointer g_i is updated (g_i = (selected + 1) mod N) IF AND ONLY IF the input port actually ACCEPTS the grant in phase 3. If an output grants to input k, but input k rejects the grant (because input k accepted a grant from another output), the output's pointer g_i REMAINS UNCHANGED. McKeown mathematically proved that updating pointers on unaccepted grants causes output pointers to lock in lockstep (synchronization), where multiple outputs repeatedly compete for the same input, throttling matching throughput to 1 - 1/e ~ 63.2%. Conditional updating forces pointers to desynchronize, achieving 100% sustained throughput under uniform traffic in O(log N) iterations.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "Desynchronized pointers are actually the desired operational goal; crossbars cannot short-circuit because input/output multiplexers are mutually exclusive."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "Updating pointers only on accepted grants maintains desynchronization among output arbiters, preventing the 63.2% throughput collapse."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Round-robin pointers are updated registers (flip-flops), not static ROM."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "IEEE 802.3 governs Ethernet LANs, not on-chip crossbar switch schedulers."
        }
      ],
      "takeaway": "In crossbar switch allocation, conditional pointer updating guarantees arbiter desynchronization, achieving near-100% throughput without starvation.",
      "citation": "N. McKeown, 'The iSLIP Scheduling Algorithm for Input-Queued Switches,' IEEE/ACM Transactions on Networking, Vol. 7, No. 2, pp. 188\u2013201, Apr. 1999. DOI: 10.1109/90.769767."
    },
    "answer": 1,
    "explanation": "Option B is McKeown's foundational proof for iSLIP desynchronization and 100% throughput."
  },
  {
    "id": "q22",
    "module": "Track 3: Topologies & Metrics (Book Ch 4)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "Why does a Folded Torus interleave even and odd nodes along each dimension compared to a naive planar 2D Torus?",
    "options": [
      "To eliminate crossbar multiplexers from edge routers.",
      "Because naive wrap-around links must span (k - 1) tile widths across the entire die, introducing high RC wire delay and clock bottlenecks; folding equalizes all physical link lengths to at most 2 tile pitches.",
      "To reduce router node degree from 4 down to 1.",
      "To convert 2D planar silicon into 3D through-silicon vias (TSVs)."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B correctly explains wire length equalization in the Folded Torus.",
      "derivation": "In a canonical 2D Torus of dimension k x k, adjacent nodes are connected by short neighbor links of length L_0 (the tile pitch). However, the boundary nodes (node 0 and node k - 1) must be connected to close the ring. In a naive planar layout, this wrap-around link must physically stretch across the entire chip, spanning a length of L_wrap = (k - 1) * L_0. For an 8x8 torus with L_0 = 1 mm, the wrap-around wire is 7 mm long. Under Elmore delay (tau ~ L^2), this single long wire exhibits (7/1)^2 = 49x the RC latency of standard neighbor links, forcing the entire network clock frequency to be throttled to accommodate the slow wrap-around path. By interleaving physical node coordinates (e.g. placing nodes in order: 0, k-1, 1, k-2, 2, k-3...), adjacent logical neighbors are separated by at most 2 tile pitches (2 * L_0). This completely eliminates long wires, ensuring all physical links have uniform, short propagation delays.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "Folding does not alter router internal crossbar multiplexer count; all torus routers retain degree 4."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "Folding equalizes link lengths to at most 2 tile widths, eliminating the 49x RC delay penalty of chip-spanning wrap-around wires."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Router node degree in a 2D torus remains 4 (+ 1 local port); folding changes only physical silicon placement."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Folded Torus is a purely 2D planar layout technique; it does not require 3D TSVs."
        }
      ],
      "takeaway": "Layout folding equalizes interconnect lengths to 2x tile pitch, eliminating the multi-millimeter wrap-around wire delays of naive tori.",
      "citation": "W. J. Dally and B. Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004."
    },
    "answer": 1,
    "explanation": "Option B correctly explains wire length equalization in the Folded Torus."
  },
  {
    "id": "q23",
    "module": "Track 3: Topologies & Metrics (Book Ch 4)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "According to Charles Clos's switching network theorem (1953), what is the minimum number of middle-stage switches m required in a 3-stage Clos network with n inputs per first-stage switch to guarantee that the network is Strictly Non-Blocking (SNB)?",
    "options": [
      "m >= 2n - 1",
      "m >= n / 2",
      "m = log_2(n)",
      "m = n^2"
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is the famous Clos strictly non-blocking condition: m >= 2n - 1.",
      "derivation": "Consider a 3-stage Clos network C(n, m, r), where the first stage has r switches of size n x m, the middle stage has m switches of size r x r, and the third stage has r switches of size m x n. To establish an arbitrary new connection between an idle input on input switch I and an idle output on output switch O: (1) In the worst case, the input switch I already has (n - 1) of its other inputs actively connected through (n - 1) distinct middle switches. (2) Similarly, the destination switch O already has (n - 1) of its other outputs actively connected through another (n - 1) distinct middle switches. (3) In the absolute worst-case scenario, the set of middle switches used by switch I and switch O are completely disjoint, meaning (n - 1) + (n - 1) = 2n - 2 middle switches are currently unavailable for routing between switch I and switch O. To guarantee that there is ALWAYS at least one free middle switch available to complete the connection without rearranging existing paths (Strictly Non-Blocking), the total number of middle switches m must be at least (2n - 2) + 1 = 2n - 1. If m >= n, the network is Rearrangeably Non-Blocking (RNB), but requires rerouting existing connections.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Charles Clos proved that m >= 2n - 1 guarantees that a free middle-stage path always exists without disturbing existing active routes."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "m < n causes severe blocking; even rearrangeable non-blocking requires m >= n."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Logarithmic scaling applies to Banyan or Omega multistage networks, not Strictly Non-Blocking Clos networks."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "n^2 overprovisions the middle stage enormously beyond what is mathematically necessary."
        }
      ],
      "takeaway": "Strictly non-blocking multi-stage Clos networks require m >= 2n - 1 middle switches, dramatically reducing crosspoint complexity compared to monolithic crossbars.",
      "citation": "C. Clos, 'A Study of Non-Blocking Switching Networks,' Bell System Technical Journal, Vol. 32, No. 2, pp. 406\u2013424, 1953."
    },
    "answer": 0,
    "explanation": "Option A is the famous Clos strictly non-blocking condition: m >= 2n - 1."
  },
  {
    "id": "q24",
    "module": "Track 3: Topologies & Metrics (Book Ch 4)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "multiple",
    "question": "How did Passas, Katevenis, and Pnevmatikatos (IEEE TCAD 2012) prove that crossbars can scale efficiently to 100+ nodes in silicon? (Select all that apply)",
    "options": [
      "By replacing monolithic centralized crossbars with distributed hierarchical Clos/Crossbar matrices partitioned into localized tiles.",
      "By using pipelined, segmented wire tracks that decouple long capacitive RC wire loads across stages.",
      "By showing that silicon area and power scale as O(N * sqrt(N)) using a 3-stage architecture rather than O(N^2).",
      "By running crossbars at negative supply voltages to cancel heat dissipation."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are the core contributions of Passas et al. (IEEE TCAD 2012). Option D is false.",
      "derivation": "While classical textbook literature claimed that crossbars cannot scale past 16\u201332 nodes due to quadratic O(N^2) area and wiring congestion, Passas, Katevenis, and Pnevmatikatos (IEEE TCAD 2012) refuted this limitation for on-chip systems. They proved that a 128-node non-blocking fabric can be synthesized at 1 GHz in standard 90nm/40nm CMOS by: (1) Slicing the monolithic crossbar into a 3-stage Clos topology composed of small, high-density sub-crossbars. (2) Sizing input sub-crossbars with n = sqrt(N/2), allowing total crosspoints to scale as O(N * sqrt(N)) (e.g. ~3,600 crosspoints for 128 nodes, compared to 16,384 for a monolithic crossbar\u2014a 78% reduction). (3) Distributing the crossbar stages physically across tiled processor columns with pipelined segment registers, preventing long wire RC degradation. (4) Operating at standard positive core voltages (0.9V\u20131.1V).",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Partitioning the monolithic switch into distributed Clos sub-blocks makes physical layout modular and routable."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. Pipelined link segments isolate wire capacitance, maintaining high clock frequencies (>1 GHz)."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. 3-stage Clos networks reduce crosspoint complexity from O(N^2) to O(N^(1.5)), enabling silicon scalability past 100 nodes."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Negative voltages are not used in CMOS digital logic fabrics."
        }
      ],
      "takeaway": "Crossbar NoCs scale beyond 100 nodes when decomposed into distributed 3-stage Clos networks with O(N^1.5) crosspoint complexity.",
      "citation": "G. Passas, M. Katevenis, and D. Pnevmatikatos, 'Crossbar NoCs Are Scalable Beyond 100 Nodes,' IEEE TCAD, Vol. 31, No. 4, pp. 573\u2013585, Apr. 2012. DOI: 10.1109/TCAD.2011.2176730."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are the core contributions of Passas et al. (IEEE TCAD 2012). Option D is false."
  },
  {
    "id": "q25",
    "module": "Track 4: Routing & Deadlock (Book Ch 5)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "What is the necessary and sufficient condition established by William Dally and Charles Seitz (1987) for a deterministic routing algorithm to be deadlock-free in a wormhole network?",
    "options": [
      "The network must have at least 16 virtual channels per physical link.",
      "The Channel Dependency Graph (CDG) must contain no directed cycles.",
      "All routers must operate with optical clock synchronization.",
      "Routers must drop packets whenever a buffer is 50% full."
    ],
    "answers": [
      1
    ],
    "solution": {
      "summary": "Option B is Dally and Seitz's foundational theorem of deadlock freedom.",
      "derivation": "In wormhole-routed networks, packets hold buffer channels while requesting downstream channels, creating hold-and-wait resource dependencies. Dally and Seitz formalized this through the Channel Dependency Graph (CDG), D = (C, E), where: (1) Each vertex c_i in C represents a dedicated routing channel/buffer. (2) A directed edge (c_i, c_j) in E exists if a packet holding channel c_i can immediately request channel c_j under the routing algorithm R. Dally and Seitz proved: A deterministic routing function R for network N is deadlock-free IF AND ONLY IF its Channel Dependency Graph D has NO DIRECTED CYCLES. If a directed cycle exists (c_1 -> c_2 -> ... -> c_k -> c_1), a set of packets can completely fill these buffers such that each packet waits for the next to advance, creating a permanent, unresolvable circular deadlock. Establishing a strict partial order on channels (e.g. dimension order: X links before Y links) guarantees an acyclic CDG.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Incorrect Distractor",
          "explanation": "Deterministic XY routing requires only 1 virtual channel to be deadlock-free; 16 VCs are completely unnecessary."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "An acyclic Channel Dependency Graph is the mathematically proven necessary and sufficient condition for deterministic deadlock freedom."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Clock synchronization does not prevent topological buffer dependency deadlocks."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Wormhole flow control is strictly lossless; dropping packets violates reliable on-chip communication semantics."
        }
      ],
      "takeaway": "Deadlock in interconnection networks is fundamentally a directed cycle in the Channel Dependency Graph; eliminating cycles guarantees deadlock-free operation.",
      "citation": "W. J. Dally and C. L. Seitz, 'Deadlock-Free Message Routing in Multiprocessor Interconnection Networks,' IEEE Transactions on Computers, Vol. C-36, No. 5, pp. 547\u2013553, May 1987. DOI: 10.1109/TC.1987.1676939."
    },
    "answer": 1,
    "explanation": "Option B is Dally and Seitz's foundational theorem of deadlock freedom."
  },
  {
    "id": "q26",
    "module": "Track 4: Routing & Deadlock (Book Ch 5)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "In a 2D Mesh with 8 possible 90-degree turns, how many turns must be prohibited in the Turn Model (Glass & Ni, 1994) to eliminate deadlock while retaining maximum routing adaptivity?",
    "options": [
      "Exactly 2 turns (one from each of the two simple 4-turn cycles: clockwise and counter-clockwise).",
      "Exactly 4 turns, forcing deterministic XY or YX routing.",
      "All 8 turns, prohibiting any direction change.",
      "0 turns; 2D meshes cannot deadlock under any circumstances."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is correct. Glass & Ni proved that prohibiting exactly 2 turns (1 CW, 1 CCW) eliminates all cycles while maximizing adaptivity.",
      "derivation": "In a 2D mesh, there are 8 possible 90-degree turns: {NE, NW, SE, SW, EN, ES, WN, WS}. The simplest directed cycles in the CDG are formed by 4-turn closed loops: (1) Clockwise (CW) cycle: North -> East -> South -> West -> North. (2) Counter-Clockwise (CCW) cycle: North -> West -> South -> East -> North. Because every complex cycle in a 2D mesh must contain at least one complete CW or CCW turn loop, breaking at least one turn in the CW cycle and one turn in the CCW cycle breaks all possible cycles. To maximize remaining adaptivity, Glass and Ni proved that exactly 2 turns must be prohibited: one turn from the CW cycle and one turn from the CCW cycle. For example: - West-First: Prohibits NW (CCW) and SW (CW). - North-Last: Prohibits NE (CW) and NW (CCW). - Negative-First: Prohibits ES (CW) and WN (CCW). By contrast, deterministic XY routing eliminates 4 turns ({NW, SW, NE, SE}), unnecessarily destroying all dynamic adaptivity.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Prohibiting exactly 2 turns breaks both clockwise and counter-clockwise cycles with minimal loss of routing adaptivity."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Prohibiting 4 turns describes deterministic DOR, which destroys 100% of routing adaptivity."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Prohibiting all 8 turns prevents packets from changing dimension entirely."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Unconstrained 2D meshes deadlock almost instantly under congestion due to cyclic channel dependencies."
        }
      ],
      "takeaway": "The Turn Model achieves deadlock-free partially adaptive routing without virtual channels by removing just 2 of the 8 turns.",
      "citation": "C. J. Glass and L. M. Ni, 'The Turn Model for Adaptive Routing,' Journal of the ACM, Vol. 41, No. 5, pp. 874\u2013902, Sept. 1994. DOI: 10.1145/185675.185682."
    },
    "answer": 0,
    "explanation": "Option A is correct. Glass & Ni proved that prohibiting exactly 2 turns (1 CW, 1 CCW) eliminates all cycles while maximizing adaptivity."
  },
  {
    "id": "q27",
    "module": "Track 4: Routing & Deadlock (Book Ch 5)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "multiple",
    "question": "Why does routing-level deadlock freedom (e.g. using deterministic XY DOR) fail to prevent Protocol-Level Deadlock in shared-memory multicore architectures? (Select all that apply)",
    "options": [
      "Cache coherence protocols create message dependencies where servicing an incoming Request flit requires generating and injecting an outgoing Response flit.",
      "If Request and Response messages share the same physical buffers, a flood of Requests can fill all router buffers, preventing Response messages from being delivered.",
      "Protocol deadlocks can be completely prevented by separating coherence message classes into distinct Virtual Networks (VNETs) mapped to independent Virtual Channels.",
      "Protocol deadlocks only occur if the CPU clock speed exceeds 5 GHz."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C correctly explain the nature of Protocol-Level Deadlock and its Virtual Network solution. Option D is false.",
      "derivation": "Routing-level deadlock freedom ensures that packets do not form circular dependency loops within the network router buffers (assuming destination nodes always consume flits). However, in shared-memory CMPs running cache coherence (e.g. MESI / MOESI): (1) Message Dependency: When a core receives a Read Request, it cannot consume the request flit until it allocates a cache buffer, inspects directory state, and transmits a Read Response. (2) Circular Wait: If the network uses a single shared buffer class for both Requests and Responses, a flood of Request packets can saturate all router buffers. Now, a core attempting to inject a Response packet is blocked because all input buffers are filled with Requests. Meanwhile, the cores holding the Request flits cannot consume them until they receive their Responses. This creates an end-to-end circular dependency between message classes that spans outside the network into core controllers. (3) Virtual Network (VNET) Solution: CMP architectures partition coherence messages into strictly ordered message classes: VNET0 (Requests) -> VNET1 (Forwards) -> VNET2 (Responses). By dedicating independent Virtual Channels to each VNET, Responses are physically guaranteed never to be blocked behind Requests, preventing protocol deadlock.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Coherence transactions create application-level dependency chains: Request -> Forward -> Response."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. If buffers are shared, Request congestion prevents Responses from draining, deadlocking the system."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. Dedicating independent VNETs/VCs guarantees that higher-priority response flits cannot be blocked by request flits."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Protocol deadlocks are logical resource dependency cycles, completely independent of clock frequency."
        }
      ],
      "takeaway": "Deadlock-free routing only guarantees flit delivery if nodes sink packets; protocol deadlock freedom requires independent Virtual Networks (VNETs) for Requests and Responses.",
      "citation": "Y. Jia, Z. Zhang, C. Fu, L. Wan, and J. Han, 'PCMT: Prioritizing Coherence Message Types for NoC Protocol-Level Deadlock Freedom,' IEEE TCAD, Vol. 45, No. 4, pp. 1949\u20131962, Apr. 2026. DOI: 10.1109/TCAD.2025.3524944."
    },
    "answer": 0,
    "explanation": "Options A, B, and C correctly explain the nature of Protocol-Level Deadlock and its Virtual Network solution. Option D is false."
  },
  {
    "id": "q28",
    "module": "Track 5: Thermal & Low-Power (Book Ch 6)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "What is the physical significance of the 'breakeven idle time' (tau_breakeven) in router power gating?",
    "options": [
      "The minimum time a router must remain sleep-gated so that the static leakage energy saved exceeds the dynamic energy overhead of charging virtual power rail capacitances during wakeup.",
      "The maximum time a packet can wait in a buffer before being discarded.",
      "The time it takes for a transistor to cool down to absolute zero.",
      "The time required for a PLL clock generator to lock phase."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is the exact physical definition of breakeven idle time in power gating.",
      "derivation": "Power gating disconnects idle circuit blocks from the power supply (V_dd) or ground (V_ss) using high-threshold sleep transistors (header or footer switches) to eliminate subthreshold leakage current (I_leak). However, power gating is not free: (1) When waking up a gated router block, the virtual power rail capacitance C_virtual (interconnect wire capacitance and internal transistor junction capacitances) must be recharged from 0V to V_dd, consuming wakeup energy: E_wakeup = C_virtual * V_dd^2. (2) While sleeping for duration tau_idle, the router saves leakage power: E_saved = P_leak * tau_idle = V_dd * I_leak * tau_idle. (3) Breakeven Condition: Power gating yields net energy savings if and only if E_saved > E_wakeup, which requires: tau_idle > tau_breakeven = E_wakeup / P_leak = (C_virtual * V_dd) / I_leak. If a router is put to sleep for less than tau_breakeven (typically 10\u201350 clock cycles in 28nm/16nm processes), the wakeup energy overhead exceeds the saved leakage, resulting in a net energy loss!",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Breakeven idle time tau_breakeven = E_wakeup / P_leak defines the threshold where accumulated leakage savings surpass wakeup charging energy."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "This describes a network timeout or packet time-to-live (TTL), not power gating economics."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Thermodynamically impossible; silicon cools toward ambient junction temperature, never absolute zero."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "This describes PLL lock time, which is an electrical clock distribution parameter."
        }
      ],
      "takeaway": "Power gating a router only saves energy if the idle period exceeds tau_breakeven (typically 15\u201340 cycles); sleeping for shorter bursts wastes power.",
      "citation": "H. Matsutani et al., 'Performance, Area, and Power Evaluations of Ultrafine-Grained Run-Time Power-Gating Routers for CMPs,' IEEE TCAD, Vol. 30, No. 4, pp. 520\u2013533, Apr. 2011. DOI: 10.1109/TCAD.2010.2097310."
    },
    "answer": 0,
    "explanation": "Option A is the exact physical definition of breakeven idle time in power gating."
  },
  {
    "id": "q29",
    "module": "Track 5: Thermal & Low-Power (Book Ch 6)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "In ultrafine-grained runtime power gating (Matsutani et al., IEEE TCAD 2011), how does Lookahead Early Wakeup eliminate router wakeup latency overhead for incoming flits?",
    "options": [
      "The upstream router asserts an early wakeup signal to the downstream sleep-gated router 1 cycle before forwarding the flit, so the virtual power rail stabilizes by the time the flit arrives.",
      "By permanently operating all routers at 0.2V.",
      "By storing flits in non-volatile flash memory inside the router crossbar.",
      "By having the operating system kernel predict packet arrivals 10 milliseconds in advance."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is correct. Lookahead wakeup overlaps power-rail restoration with upstream credit/switch traversal.",
      "derivation": "Standard power gating suffers from a severe latency penalty: when a flit arrives at a sleeping router, the router must wait 1\u20133 cycles for sleep transistors to turn on and charge the virtual power rail before the input buffer can reliably write data. Matsutani et al. introduced Lookahead Early Wakeup: (1) In a pipelined router, when a packet at router R_i wins Switch Allocation (SA) to traverse the link toward downstream router R_{i+1}, router R_i immediately asserts a dedicated 1-bit early wakeup wire to R_{i+1}. (2) During the subsequent cycle, as the flit is traversing the physical link wires (Link Traversal stage), router R_{i+1} turns on its sleep headers and recharges its virtual power rail. (3) By the time the flit arrives at R_{i+1}'s input latches, the power rail is fully stabilized at V_dd, allowing immediate single-cycle Buffer Write (BW) without incurring any pipeline stall cycles. Lookahead wakeup hides 100% of the wakeup latency under zero-load and burst conditions.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Upstream lookahead signaling overlaps sleep transistor turn-on with physical link transit, hiding 100% of wakeup latency."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Operating at 0.2V (deep subthreshold) would collapse circuit speed by orders of magnitude, making >1 GHz routing impossible."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Flash memory has multi-microsecond write times and limited endurance; it cannot replace SRAM flit buffers."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "OS kernel intervention takes thousands of cycles; on-chip early wakeup must occur in hardware within 1 clock cycle."
        }
      ],
      "takeaway": "Lookahead early wakeup signals overlap power-rail charging with upstream link traversal, achieving zero-latency wakeup for power-gated routers.",
      "citation": "H. Matsutani et al., 'Performance, Area, and Power Evaluations of Ultrafine-Grained Run-Time Power-Gating Routers for CMPs,' IEEE TCAD, Vol. 30, No. 4, pp. 520\u2013533, Apr. 2011. DOI: 10.1109/TCAD.2010.2097310."
    },
    "answer": 0,
    "explanation": "Option A is correct. Lookahead wakeup overlaps power-rail restoration with upstream credit/switch traversal."
  },
  {
    "id": "q30",
    "module": "Track 5: Thermal & Low-Power (Book Ch 6)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "multiple",
    "question": "Which of the following principles govern Low-Power Code Reordering (LPCR, Adelkhani et al., IEEE TCAD 2025) for reducing dynamic power dissipation on on-chip serial links? (Select all that apply)",
    "options": [
      "Dynamic link power is proportional to the bit transition activity factor alpha (P = alpha * C_link * V^2 * f).",
      "LPCR analyzes the statistical transition probability matrix of consecutive flits and reorders data words to minimize Hamming distance transitions.",
      "Bus-Invert (BI) coding is combined with LPCR to invert transmitted words whenever Hamming distance exceeds W / 2.",
      "LPCR increases dynamic link power by generating deliberate pseudo-random noise."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are correct information-theoretic and circuit principles of LPCR. Option D is false.",
      "derivation": "On-chip global links consume substantial dynamic energy due to long wire capacitances (C_link ~ 0.2 pF/mm): P_dynamic = alpha * C_link * V_dd^2 * f, where alpha is the average bit transition activity factor (fraction of bitlines transitioning 0->1 or 1->0). Adelkhani et al. (IEEE TCAD 2025) formulated Low-Power Code Reordering (LPCR): (1) Information-Theoretic Optimization: Successive cache line words exhibit strong data correlations (e.g. instruction opcodes or address strides). LPCR constructs a transition graph where vertices are data flits and edge weights represent Hamming distance. By finding a minimum Hamiltonian path or applying greedy Markov reordering, the sequence of flits within a packet is permuted to minimize total bit transitions. (2) Bus-Invert Integration: Combined with Stan & Burleson's Bus-Invert coding, if the Hamming distance between consecutive transmitted words exceeds W/2, an extra invert line is asserted and the word is complemented, strictly capping transition activity at alpha <= 0.5. (3) Hardware Realization: LPCR deploys lightweight barrel reordering buffers at the Network Interface (NI), slashing serial link switching activity by 32% to 46% with zero loss of data fidelity.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Dynamic energy is directly governed by charging wire capacitance on bit transitions (P = alpha * C * V^2 * f)."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. LPCR exploits inter-flit correlation to minimize Hamming distance between consecutive transmissions."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. Bus-Invert caps maximum bit transitions at W/2, complementing reordering optimizations."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Adding pseudo-random noise would maximize transition activity (alpha -> 0.5) and increase power."
        }
      ],
      "takeaway": "Reordering flits to minimize consecutive Hamming distance cuts interconnect dynamic power by up to 40% with zero throughput penalty.",
      "citation": "M. Adelkhani et al., 'LPCR: Information-Theory-Based Low-Power Code Reordering for Serial Links in Network-on-Chip,' IEEE TCAD, Vol. 44, No. 11, pp. 4155\u20134168, Nov. 2025. DOI: 10.1109/TCAD.2025.3411245."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are correct information-theoretic and circuit principles of LPCR. Option D is false."
  },
  {
    "id": "q31",
    "module": "Track 5: Thermal & Resilience (Book Ch 7)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "Under the HotSpot electro-thermal duality framework (Skadron et al.), what physical thermal property is the direct mathematical equivalent of electrical capacitance (C = Q / V)?",
    "options": [
      "Thermal capacitance C_th = rho * c_p * V (in Joules/Kelvin), representing the heat energy stored per unit temperature elevation.",
      "Thermal resistance R_th = L / (k * A) (in Kelvin/Watt).",
      "Silicon thermal conductivity k_Si.",
      "Convective heat transfer coefficient h_conv."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A correctly identifies thermal capacitance as the dual of electrical capacitance.",
      "derivation": "The electro-thermal duality maps heat flow through physical solids directly to electrical circuit networks: (1) Temperature T (K) <--> Voltage V (Volts). (2) Heat Flow / Power P (Watts = Joules/sec) <--> Current I (Amperes = Coulombs/sec). (3) Thermal Resistance R_th = L / (k * A) (K/W) <--> Electrical Resistance R = L / (sigma * A) (Ohms = Volts/Amp). (4) Thermal Capacitance C_th = rho * c_p * V (J/K) <--> Electrical Capacitance C = Q / V (Farads = Coulombs/Volt). Thermal capacitance quantifies the heat energy (in Joules) stored in a physical volume of silicon V of density rho and specific heat capacity c_p to raise its temperature by 1 Kelvin. In compact thermal modeling (HotSpot), silicon substrate and package layers are discretized into 3D RC grids, where temperature at node i evolves as C_th,i * (dT_i / dt) = P_i - sum_j ((T_i - T_j) / R_th,ij).",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Thermal capacitance C_th = rho * c_p * V (J/K) stores thermal energy per degree Kelvin, mathematically identical to electrical capacitance storing charge per volt."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "R_th corresponds to electrical resistance, not capacitance."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Thermal conductivity k is the dual of electrical conductivity sigma."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Convective heat transfer coefficient h_conv represents boundary thermal conductance."
        }
      ],
      "takeaway": "Electro-thermal duality allows complex 3D heat diffusion problems to be modeled and solved using fast, standard SPICE-like RC circuit differential solvers.",
      "citation": "K. Skadron et al., 'Temperature-Aware Microarchitecture: Modeling and Implementation,' ACM Transactions on Architecture and Code Optimization (TACO), Vol. 1, No. 1, pp. 94\u2013125, Mar. 2004. DOI: 10.1145/980152.980157."
    },
    "answer": 0,
    "explanation": "Option A correctly identifies thermal capacitance as the dual of electrical capacitance."
  },
  {
    "id": "q32",
    "module": "Track 5: Thermal & Resilience (Book Ch 7)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "Why do standard linear Kalman filters diverge when reconstructing on-chip temperature fields under dynamic clock gating and DVFS, and how do adaptive estimators resolve this?",
    "options": [
      "Dynamic power gating introduces rapid state-dependent parameter shifts in both system noise covariance and thermal dissipation matrices; adaptive estimators dynamically scale the covariance matrix Q based on real-time hardware performance counters.",
      "Because Kalman filters can only run on 8-bit microcontrollers.",
      "Because silicon heat flow reverses direction when clock gating is activated.",
      "Kalman filters only diverge when operating in outer space."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A correctly explains Kalman divergence under non-stationary DVFS noise and the adaptive covariance solution.",
      "derivation": "A standard discrete Kalman filter assumes a linear time-invariant (LTI) state space model: x_{k+1} = A * x_k + B * u_k + w_k, with fixed process noise covariance Q = E[w w^T]. In modern many-core processors: (1) Dynamic Clock Gating & DVFS: Power dissipation P_k switches abruptly between 0W (idle) and 25W (compute burst) in nanoseconds. This introduces severe non-stationarity in the process disturbance w_k, causing actual process variance to swing by multiple orders of magnitude. (2) Filter Divergence: If Q is fixed to a small value, the filter over-trusts the flawed linear thermal model and ignores real temperature surges measured by diodes, leading to filter divergence (tracking error > 15\u00b0C). (3) Adaptive Resolution: Adaptive Kalman estimators (or Unscented Kalman Filters) dynamically update the process noise covariance matrix Q_k = diag(gamma * IPC_i * V_dd^2 * f) using runtime hardware performance counters (instructions per cycle, cache miss rates), maintaining sub-1.5\u00b0C tracking fidelity across aggressive power-state transitions.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Abrupt power shifts under DVFS violate stationary noise assumptions; adaptive covariance scaling based on IPC and voltage restores filter convergence."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Kalman algorithms run on standard double/single-precision arithmetic on host cores or embedded micro-engines."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Heat always conducts down the thermal gradient from hot to cold (Second Law of Thermodynamics); direction does not reverse."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Terrestrial chips experience identical thermal divergence due to DVFS transitions."
        }
      ],
      "takeaway": "Thermal state estimators must dynamically scale process noise covariance with runtime power transitions to prevent filter divergence.",
      "citation": "C.-H. Chao, K.-C. Chen, and A.-Y. Wu, 'Routing-Based Traffic Migration and Buffer Allocation Schemes for 3-D NoC With Thermal Limit,' IEEE TVLSI, Vol. 21, No. 11, pp. 2118\u20132131, Nov. 2013. DOI: 10.1109/TVLSI.2012.2227852."
    },
    "answer": 0,
    "explanation": "Option A correctly explains Kalman divergence under non-stationary DVFS noise and the adaptive covariance solution."
  },
  {
    "id": "q33",
    "module": "Track 5: Thermal & Resilience (Book Ch 7)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "multiple",
    "question": "Which of the following architectural principles allow the ZoneDefense fault-tolerant routing framework (Fu et al., IEEE TVLSI 2014) to bypass permanent faulty routers without producing deadlock? (Select all that apply)",
    "options": [
      "Grouping faulty routers and their adjacent perimeter nodes into regular, convex rectilinear 'Fault Zones'.",
      "Routing packets around the perimeter of the Fault Zone using dedicated escape virtual channels with strictly acyclic turn rules.",
      "Allowing packets to enter the interior of the Fault Zone to be temporarily parked.",
      "Disabling all healthy routers across the entire die whenever a single link fails."
    ],
    "answers": [
      0,
      1
    ],
    "solution": {
      "summary": "Options A and B are the foundational mechanisms of ZoneDefense. Options C and D are false.",
      "derivation": "When physical hardware defects strike a 2D mesh router (e.g. permanent TDDB gate breakdown or electromigration line open): (1) Irregular Topologies: Random faulty routers create concave routing boundaries, where packets can be trapped in cyclic channel deadlocks. (2) Convex Zone Formation: ZoneDefense (Fu et al., IEEE TVLSI 2014) detects faulty nodes and coordinates adjacent routers to establish a convex rectilinear bounding box called a Fault Zone. All healthy nodes within the zone boundary are disabled from through-routing, transforming arbitrary jagged faults into clean rectangular boundaries. (3) Perimeter Contour Routing: Packets whose minimal paths intersect the Fault Zone are deflected onto the perimeter boundary ring. To guarantee deadlock freedom on the perimeter ring, ZoneDefense allocates dedicated Virtual Channels (VCs) running directional contour rules (e.g. clockwise ring on VC1, counter-clockwise on VC2) that strictly prevent cyclic buffer hold-and-wait dependencies. Packets NEVER enter the interior of the dead zone, and un-impacted healthy routers continue high-speed routing unimpeded.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Enclosing irregular faults inside convex rectilinear bounding zones prevents concave packet traps."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. Dedicated perimeter escape VCs with directional contour rules ensure deadlock-free detours."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "False. Packets are strictly prohibited from entering the faulty interior; broken routers cannot buffer or forward flits."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. ZoneDefense is designed for graceful degradation, isolating only the affected zone while keeping the remaining network fully active."
        }
      ],
      "takeaway": "Forming convex rectangular fault zones and routing around perimeters with dedicated escape VCs guarantees deadlock-free recovery from physical router failures.",
      "citation": "C. Fu, G. M. Chiu, and J. Han, 'ZoneDefense: A Fault-Tolerant Routing Algorithm for Networks-on-Chip,' IEEE TVLSI, Vol. 22, No. 9, pp. 1920\u20131933, Sept. 2014. DOI: 10.1109/TVLSI.2013.2281786."
    },
    "answer": 0,
    "explanation": "Options A and B are the foundational mechanisms of ZoneDefense. Options C and D are false."
  },
  {
    "id": "q34",
    "module": "Track 6: Chiplets & 3D (Book Ch 8)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "What is a Through-Silicon Via (TSV) Keep-Out Zone (KOZ), and what physical phenomenon dictates its radius around copper TSVs?",
    "options": [
      "Thermal expansion mismatch between copper (alpha_Cu ~ 17 ppm/K) and silicon (alpha_Si ~ 2.6 ppm/K) induces severe thermo-mechanical shear stress (>200 MPa) during post-bonding thermal cooling, altering transistor carrier mobility by up to 30%; the KOZ is a mandatory exclusion area where no active CMOS transistors may be placed.",
      "A software security zone preventing hackers from reading TSV voltages.",
      "A chemical buffer to prevent silicon from dissolving in water.",
      "A radioactive shielding perimeter to block cosmic rays."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is the correct physics of TSV thermo-mechanical stress and the Keep-Out Zone.",
      "derivation": "Through-Silicon Vias (TSVs) provide vertical electrical interconnects across stacked silicon dies. Copper (Cu) is the industry-standard via fill material due to its high electrical conductivity. However, copper and silicon have dramatically different Coefficients of Thermal Expansion (CTE): alpha_Cu = 17 ppm/K vs. alpha_Si = 2.6 ppm/K (a 6.5x CTE mismatch). During post-bond annealing and cooling from 250\u00b0C to room temperature, copper contracts significantly more than the surrounding silicon matrix. This creates severe tensile radial stress (sigma_r) and compressive tangential stress (sigma_theta) in the silicon lattice exceeding 200\u2013300 MPa near the TSV edge. Through the piezoresistive effect, this mechanical lattice strain shifts NMOS electron mobility (by up to -15%) and PMOS hole mobility (by up to +35%), inducing unacceptable threshold voltage (V_th) shifts and timing jitter. The TSV Keep-Out Zone (KOZ) defines a strict exclusion radius (typically 3\u20135 um around a 5 um diameter TSV) where standard cell transistors are prohibited from placement, directly impacting silicon area utilization.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Thermo-mechanical stress from the 6.5x CTE mismatch between copper and silicon alters carrier mobility via the piezoresistive effect, mandating a KOZ."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "KOZ is a physical manufacturing and layout design rule, not a software security perimeter."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Silicon does not dissolve in water under standard operating conditions."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Standard TSVs do not emit or block radiation; the issue is thermo-mechanical stress."
        }
      ],
      "takeaway": "Copper TSVs induce localized lattice strain that shifts transistor mobility, requiring layout Keep-Out Zones (KOZ) of 3\u20135 um around each vertical via.",
      "citation": "A. Al-Alousi, M. Li, and H. Meng, 'Design Space Exploration and Resource Optimization for 3-D NoCs,' IEEE TCAD, Vol. 45, No. 5, pp. 2236\u20132248, May 2026. DOI: 10.1109/TCAD.2025.3616073."
    },
    "answer": 0,
    "explanation": "Option A is the correct physics of TSV thermo-mechanical stress and the Keep-Out Zone."
  },
  {
    "id": "q35",
    "module": "Track 6: Chiplets & 3D (Book Ch 8)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "Why does expanding a 2D router (5 ports) to a fully symmetric 3D router (7 ports) almost double the crossbar switch area, and how do Vertical Arbitration-Free architectures mitigate this overhead?",
    "options": [
      "Crossbar complexity scales quadratically with port count (P^2 = 49 crosspoints vs 25 crosspoints, a 96% increase); arbitration-free designs deploy dedicated unidirectional vertical links that eliminate vertical allocators and simplify the crossbar matrix.",
      "Crossbar area scales logarithmically with port count.",
      "Because 3D routers must be fabricated exclusively with diamond substrates.",
      "Arbitration-free architectures double the clock frequency to avoid adding vertical ports."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is correct. Expanding ports from 5 to 7 increases crossbar crosspoints by 96%, motivating vertical bypass paths.",
      "derivation": "In a planar 2D router, there are P = 5 bidirectional ports: {North, South, East, West, Local}. A full crossbar matrix requires P^2 = 5^2 = 25 crosspoint multiplexers. In a symmetric 3D router, two vertical ports {Up, Down} are added to connect adjacent tiers, bringing total radix to P = 7. The required crosspoints surge to P^2 = 7^2 = 49 crosspoints\u2014a 96% increase in crossbar area and wire congestion! Furthermore, the switch allocator complexity scales as O(P^2), inflating arbitration delay and power. More et al. (IEEE TCAD 2018) and related 3D NoC architects showed that vertical traffic accounts for a fraction of total hops. By implementing Vertical Arbitration-Free (VAF) fast-paths: (1) Vertical flits skip complex two-stage switch allocation, utilizing dedicated vertical FIFO bypass muxes. (2) The crossbar is decomposed into an asymmetric 5x5 planar matrix plus dedicated vertical injection paths. This eliminates 40% of the crossbar silicon area while cutting vertical transit latency to 1 cycle.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "7-port crossbars require 49 crosspoints vs 25 (+96%); dedicated vertical fast-paths eliminate complex vertical arbiters and reduce crossbar area."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Crossbar area scales as O(P^2), strictly quadratic, never logarithmic."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "3D-ICs are manufactured on standard bulk silicon wafers with oxide bonding, not synthetic diamond."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Clock frequency is not doubled; dedicated bypass circuits eliminate arbitration delays."
        }
      ],
      "takeaway": "7-port 3D crossbars suffer from 2x crosspoint area; vertical bypass fast-paths prevent area inflation and reduce vertical traversal latency.",
      "citation": "A. Al-Alousi, M. Li, and H. Meng, 'Design Space Exploration for 3-D NoCs,' IEEE TCAD, Vol. 45, No. 5, pp. 2236\u20132248, May 2026. DOI: 10.1109/TCAD.2025.3616073."
    },
    "answer": 0,
    "explanation": "Option A is correct. Expanding ports from 5 to 7 increases crossbar crosspoints by 96%, motivating vertical bypass paths."
  },
  {
    "id": "q36",
    "module": "Track 6: Chiplets & 3D (Book Ch 8)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "multiple",
    "question": "Which of the following physical mechanisms cause severe 'Thermal Trapping' in vertically stacked 3D-ICs? (Select all that apply)",
    "options": [
      "Heat generated in upper silicon tiers must conduct downward through multiple thinned silicon substrates and low-conductivity dielectric bonding interfaces (SiO2 / polymer adhesives, k ~ 0.2\u20131.4 W/m*K) before reaching the bottom heat sink.",
      "The vertical accumulation of inter-tier thermal resistances elevates top-tier temperatures by 25\u00b0C to 45\u00b0C over bottom tiers under identical power dissipation.",
      "Power densities of stacked active tiers additively multiply across a single package footprint (e.g. 4 tiers of 100 W/cm^2 = 400 W/cm^2 total thermal flux).",
      "Heat in silicon is physically incapable of conducting through copper TSVs."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are the physical causes of thermal trapping in 3D-ICs. Option D is a false statement.",
      "derivation": "In standard 2D packaging, the single active silicon die sits directly against the thermal interface material (TIM) and copper heat sink. In 3D-stacked ICs (e.g. 4\u20138 stacked dies): (1) Multiplied Thermal Flux: Stacking 4 dies each dissipating 80 W/cm^2 results in an aggregate package thermal flux of 320 W/cm^2, far exceeding the heat extraction capability of conventional air heat sinks (~100 W/cm^2). (2) Thermal Resistance Ladder: Heat generated in Tier 3 (the furthest die from the heat sink) must conduct through Tier 2, Tier 1, and Tier 0. Between each die lies a dielectric bonding layer (BCB polymer with k ~ 0.2 W/m*K or SiO2 with k ~ 1.4 W/m*K), whose thermal conductivity is 100x\u2013700x worse than bulk silicon (k_Si ~ 140 W/m*K). (3) Thermal Trapping: The series sum of these inter-tier thermal resistances (R_total = R_sink + sum R_interlayer + sum R_Si) traps heat in the top layers, elevating junction temperatures by 25\u00b0C to 45\u00b0C. Copper TSVs (k_Cu ~ 390 W/m*K) actually act as thermal conduits, helping conduct heat vertically, but their volume fraction (1\u20133%) is insufficient to fully overcome the dielectric barrier without dedicated thermal TSV arrays.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Low-conductivity dielectric bonding layers (k ~ 0.2\u20131.4 W/m*K) act as thermal insulators between stacked tiers."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. Series thermal resistance accumulation elevates top-tier temperatures substantially above the base die."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. Stacking active tiers multiplies volumetric power density over a constant package heat sink area."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Copper TSVs have high thermal conductivity (~390 W/m*K) and actively assist vertical heat conduction."
        }
      ],
      "takeaway": "Thermal trapping in 3D stacks creates 25\u201345\u00b0C top-tier temperature elevation, requiring thermal TSVs, microfluidic cooling, or thermally-aware vertical task placement.",
      "citation": "C.-H. Chao, K.-C. Chen, and A.-Y. Wu, 'Routing-Based Traffic Migration and Buffer Allocation Schemes for 3-D NoC With Thermal Limit,' IEEE TVLSI, Vol. 21, No. 11, pp. 2118\u20132131, Nov. 2013. DOI: 10.1109/TVLSI.2012.2227852."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are the physical causes of thermal trapping in 3D-ICs. Option D is a false statement."
  },
  {
    "id": "q37",
    "module": "Track 6: Chiplets & 3D (Book Ch 9)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "single",
    "question": "Why does disaggregating a massive monolithic system-on-chip into smaller chiplets dramatically reduce total manufacturing cost, according to the Murphy and Seeds yield models?",
    "options": [
      "Die manufacturing yield decays exponentially with active silicon area (Y ~ exp(-sqrt(A * D_0))); partitioning an 800 mm^2 die into four 200 mm^2 chiplets increases per-die yield from ~25% to >80%, drastically reducing discarded silicon and lowering total cost despite packaging overhead.",
      "Because chiplets eliminate the need for silicon wafers entirely.",
      "Because packaging costs for chiplets are strictly negative.",
      "Because chiplets can only be manufactured using 180nm lithography."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is correct. Murphy/Seeds yield formulations prove exponential yield decay with die area, driving chiplet economics.",
      "derivation": "In semiconductor fabrication, random defect density D_0 (defects per cm^2) causes catastrophic functional failures. Under the Seeds yield model, die yield is Y = exp(-A * D_0); under the more realistic Murphy model with triangular defect distribution, Y = ((1 - exp(-A * D_0)) / (A * D_0))^2. Because yield decays exponentially with active die area A: (1) Monolithic 800 mm^2 Die: With D_0 = 0.08 defects/cm^2, the yield of an 800 mm^2 die is approximately Y ~ 20\u201325%. 75\u201380% of all fabricated monolithic wafers are discarded, driving per-good-die cost to thousands of dollars. (2) Four 200 mm^2 Chiplets: Partitioning the design into four smaller dies of 200 mm^2 each pushes per-die yield above 80\u201385%. Even after accounting for the yield of the silicon interposer and substrate packaging (~95%), total silicon manufacturing cost drops by 40% to 60%. Furthermore, chiplets allow process specialization: only compute-intensive cores use expensive 3nm silicon, while memory and I/O controllers use mature, low-cost 12nm/7nm silicon.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Exponential yield decay with area means smaller chiplets achieve >80% yield vs <25% for reticle-limit monolithic dies, slashing total cost."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Chiplets are fabricated on standard silicon wafers (typically 300mm diameter)."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Advanced 2.5D packaging costs are positive and significant; savings come from silicon yield multiplication."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Chiplets are deployed in cutting-edge FinFET and GAA nodes (3nm, 5nm, 7nm)."
        }
      ],
      "takeaway": "Smaller chiplet die sizes exploit the exponential relationship between area and defect yield, lowering total silicon cost by 40\u201360%.",
      "citation": "D. Das Sharma et al., 'Universal Chiplet Interconnect Express (UCIe): Building an Open Chiplet Ecosystem,' IEEE Micro, Vol. 42, No. 5, pp. 63\u201371, Sept.\u2013Oct. 2022. DOI: 10.1109/MM.2022.3195973."
    },
    "answer": 0,
    "explanation": "Option A is correct. Murphy/Seeds yield formulations prove exponential yield decay with die area, driving chiplet economics."
  },
  {
    "id": "q38",
    "module": "Track 6: Chiplets & 3D (Book Ch 9)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "multiple",
    "question": "In the Universal Chiplet Interconnect Express (UCIe) specification, which functions are handled by the Die-to-Die (D2D) Adapter Layer situated between the Protocol Layer and the Physical Layer (PHY)? (Select all that apply)",
    "options": [
      "Packet framing, byte stripping, and CRC calculation (CRC-16 or CRC-32) for physical transmission error detection.",
      "Retry buffers and retransmission state machines (Go-Back-N or Selective Repeat) to ensure lossless link delivery.",
      "Link state machine management (LinkInit, Active, Retrain, Low-Power Standby).",
      "Direct conversion of digital binary voltages into coherent optical laser beams."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are the standardized functions of the UCIe D2D Adapter layer. Option D is false.",
      "derivation": "The UCIe stack is organized into three standardized hierarchical layers: (1) Protocol Layer: Handles high-level packet semantics, supporting native PCIe 6.0 flits, CXL 3.0 flits, and raw streaming packets. (2) Die-to-Die (D2D) Adapter Layer: Acts as the reliability and link coordination engine. It frames protocol flits, appends CRC-16 or CRC-32 checksums for physical noise detection, manages the Link State Machine (LSM) across power states, manages credit-based flow control turnaround, and controls the replay buffer (Go-Back-N / Selective Repeat retransmission) to guarantee lossless transmission. (3) Physical Layer (PHY): Manages analog electrical signaling, lane deskewing, clock forwarding, and microbump I/O drivers across standard packages or advanced 2.5D interposers. Optical modulation is not part of standard electrical UCIe D2D layers.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. The D2D Adapter layer handles packet encapsulation, framing, and CRC generation/validation."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. It maintains retry buffers and ACK/NAK replay logic for error correction."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. It controls link initialization, training, calibration, and power-saving transitions."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. UCIe D2D adapter is a digital electrical protocol layer; optical modulation belongs to optical PHYs."
        }
      ],
      "takeaway": "The UCIe D2D Adapter layer provides guaranteed reliability (CRC + retry buffer) and link state coordination over physical microbump channels.",
      "citation": "D. Das Sharma et al., 'Universal Chiplet Interconnect Express (UCIe): Building an Open Chiplet Ecosystem,' IEEE Micro, Vol. 42, No. 5, pp. 63\u201371, Sept.\u2013Oct. 2022. DOI: 10.1109/MM.2022.3195973."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are the standardized functions of the UCIe D2D Adapter layer. Option D is false."
  },
  {
    "id": "q39",
    "module": "Track 6: Chiplets & 3D (Book Ch 9)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "single",
    "question": "Why can composing individually deadlock-free 2D mesh chiplets produce system-level routing deadlocks, and how does the In/Outbound Swap backtracking mechanism (Wang et al., IEEE TCAD 2026) resolve this without dedicating redundant Virtual Channels?",
    "options": [
      "Hierarchical routing across die-to-die boundaries can form cyclic buffer dependency loops across inter-chiplet bridge routers; the In/Outbound Swap detects stalls exceeding a timeout threshold and diverts blocked head flits into an escape swap register, severing the cyclic dependency loop and allowing trailing flits to advance.",
      "Deadlocks only occur if the interposer runs out of electrical ground wires.",
      "In/Outbound Swap drops all packets currently stored in router buffers whenever a stall occurs.",
      "Multi-chiplet deadlocks are mathematically impossible because turn models always apply across multiple dies without restriction."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is correct. Local turn models do not prevent global inter-chiplet dependency cycles; In/Outbound Swap breaks cycles via timeout-triggered escape swaps.",
      "derivation": "When independent chiplets (each using deterministic XY DOR) are assembled on a silicon interposer: (1) Global Cyclic Dependencies: While intra-chiplet routing is acyclic, inter-chiplet traffic must cross Die-to-Die (D2D) bridge routers. If a packet leaves Chiplet 0, enters Chiplet 1, and subsequent traffic routes back into Chiplet 0 through a second bridge, a global circular channel dependency cycle (C0 -> D2D_East -> C1 -> D2D_South -> C0) forms in the system-level Channel Dependency Graph. (2) Limitations of Prior Solutions: Adding extra global Virtual Channels to partition traffic is area-prohibitive in compact chiplet bridge routers. (3) In/Outbound Swap: Wang et al. (IEEE TCAD 2026) introduced an asynchronous deadlock resolution mechanism: When a flit at an inter-chiplet boundary stalls for longer than a predefined threshold tau_stall, a deadlock cycle is flagged. The bridge router activates the In/Outbound Swap register, deflecting the blocked Head flit into a side escape buffer. This removes the flit from the congested link, breaking the circular wait condition and allowing trailing flits to drain. Once the link clears, the swapped flit is reinjected into the network without dropping data.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Inter-chiplet bridges form global dependency cycles; timeout-driven escape swap registers break the cycle without dropping packets or dedicating redundant VCs."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "Ground wires maintain voltage reference; deadlocks are network protocol buffer dependency cycles, not ground wire shortages."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "In/Outbound Swap preserves 100% reliable packet delivery; it never drops packets."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Turn models do NOT compose transitively across hierarchical boundaries without explicit global ordering constraints."
        }
      ],
      "takeaway": "Composing deadlock-free chiplets creates global inter-die cycles; dynamic swap escape registers break cyclic dependencies without overprovisioning virtual channels.",
      "citation": "L. Zhu, H. Gu, Y. Tan, and G. Zhang, 'ScaDA-Rou: A Scalable, Deadlock-Free, and Adaptive Routing for 3-D Multi-Chiplet System,' IEEE TCS-II, Vol. 73, No. 4, pp. 433\u2013437, Apr. 2026. DOI: 10.1109/TCSII.2025.3526101."
    },
    "answer": 0,
    "explanation": "Option A is correct. Local turn models do not prevent global inter-chiplet dependency cycles; In/Outbound Swap breaks cycles via timeout-triggered escape swaps."
  },
  {
    "id": "q40",
    "module": "Track 7: Emerging Frontiers (Book Ch 10)",
    "tier": "Tier 1: Fundamental",
    "tier_level": 1,
    "base_points": 100,
    "type": "multiple",
    "question": "Which of the following physical and architectural advantages allow Optical Networks-on-Chip (ONoC) to outperform electrical copper interconnects over long on-chip distances? (Select all that apply)",
    "options": [
      "Photons propagating through passive silicon waveguides experience no data-dependent capacitive charging loss (P_dyn = alpha * C * V^2 * f); optical transmission energy is distance-independent once light is injected.",
      "Wavelength Division Multiplexing (WDM) allows multiple independent optical signals (e.g. 16\u201364 wavelengths) to traverse the same physical waveguide simultaneously without electrical crosstalk.",
      "Optical signals travel at the speed of light in silicon (c / n_si ~ 8.5 x 10^7 m/s, or ~11.8 ps/mm), avoiding RC dispersion delays.",
      "Optical silicon waveguides eliminate the need for laser power sources."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C are fundamental physical merits of silicon photonics. Option D is false.",
      "derivation": "Electrical interconnects scale poorly over long distances (L > 5\u201310 mm) because charging line capacitance dissipates dynamic power P = alpha * C_wire * V^2 * f and Elmore delay scales quadratically with length. Silicon photonics replaces long metal lines with sub-micron silicon waveguides: (1) Distance-Independent Dynamic Energy: Once an optical signal is modulated into a waveguide, photons traverse passive silicon without charging or discharging gate/wire capacitances. Waveguide propagation loss is low (~0.5\u20131.5 dB/cm), making transmission energy virtually independent of link distance. (2) Wavelength Division Multiplexing (WDM): By modulating data across multiple distinct optical wavelengths (lambda_1, lambda_2, ..., lambda_M) separated by 50\u2013100 GHz channel spacing, a single physical waveguide carries dozens of concurrent high-speed bitstreams, achieving multi-Tbps aggregate bandwidth density without adding physical wires. (3) Latency: Light propagates at the group velocity v_g = c / n_g (approx 85,000 km/s in Si with n_g ~ 3.5), yielding ~11.8 ps/mm of transit time without intermediate repeater pipeline delays. However, optical systems require an external or integrated laser power source and micro-ring resonator tuning.",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Photons do not charge capacitive wire plates during transit, decoupling transmission energy from link distance."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. WDM multiplexes dozens of optical carriers into a single waveguide, delivering massive bandwidth density."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. Optical transit operates at group velocity (~11.8 ps/mm) with zero RC charging delay."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Silicon is an indirect bandgap semiconductor and cannot generate light passively; an external or hybrid-integrated laser is strictly required."
        }
      ],
      "takeaway": "Silicon photonics eliminates capacitive RC wire losses and multiplies channel bandwidth via WDM, delivering distance-independent energy for long-range communication.",
      "citation": "C. Kao et al., 'Low-Loss Switching Elements for WDM Optical Networks-on-Chip,' IEEE TCAD, Vol. 45, No. 3, pp. 1120\u20131134, Mar. 2026. DOI: 10.1109/TCAD.2025.3521098."
    },
    "answer": 0,
    "explanation": "Options A, B, and C are fundamental physical merits of silicon photonics. Option D is false."
  },
  {
    "id": "q41",
    "module": "Track 7: Emerging Frontiers (Book Ch 10)",
    "tier": "Tier 2: Core Engineering",
    "tier_level": 2,
    "base_points": 200,
    "type": "single",
    "question": "Why do Parallel Switching Elements (PSEs) achieve significantly lower optical insertion loss and laser power dissipation than Crossing Switching Elements (CSEs) in ONoC architectures (Kao et al., IEEE TCAD 2026)?",
    "options": [
      "PSE structures place the micro-ring resonator between two parallel waveguides, eliminating internal orthogonal waveguide crossings that introduce scattering loss (0.10\u20130.15 dB per crossing) and crosstalk noise.",
      "PSE structures eliminate the need for micro-ring resonators altogether.",
      "CSE structures cannot transmit infrared light.",
      "PSE structures operate exclusively at liquid helium temperatures (-269\u00b0C)."
    ],
    "answers": [
      0
    ],
    "solution": {
      "summary": "Option A is correct. Parallel Switching Elements eliminate internal orthogonal waveguide crossings, slashing optical path loss.",
      "derivation": "In Optical Networks-on-Chip (ONoC), router switching cells redirect optical signals between input and output waveguides using Micro-Ring Resonators (MRRs): (1) Crossing Switching Element (CSE): Traditional CSE designs arrange waveguides in an orthogonal cross (+) with a ring in the corner. In both the through state and drop state, light must traverse waveguide crossings. Each physical waveguide crossing introduces ~0.10\u20130.20 dB of scattering loss and -30 dB to -40 dB of optical crosstalk into adjacent channels. In an 8x8 optical mesh, an optical path can accumulate 20\u201330 crossings, losing 3\u20135 dB of optical power. (2) Parallel Switching Element (PSE): Kao et al. (IEEE TCAD 2026) proved that arranging waveguides in parallel (=) with the ring coupled between them completely eliminates internal crossings within the switching element. When off-resonance, light passes straight through with <0.01 dB loss; when on-resonance, light couples across into the parallel guide without crossing physical silicon boundaries. In an 8x8 mesh, PSE architectures slash total optical path loss by 4.8 dB, which reduces required continuous-wave (CW) laser power by over 3x!",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "Coupling between parallel waveguides eliminates internal orthogonal waveguide crossings, avoiding scattering loss and crosstalk."
        },
        {
          "option": "B",
          "status": "Incorrect Distractor",
          "explanation": "PSE structures use micro-ring resonators for wavelength-selective coupling."
        },
        {
          "option": "C",
          "status": "Incorrect Distractor",
          "explanation": "Both PSE and CSE operate at standard telecommunications infrared wavelengths (1310 nm and 1550 nm)."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "Silicon photonic integrated circuits operate at standard room temperatures (up to 85\u00b0C\u2013105\u00b0C)."
        }
      ],
      "takeaway": "Eliminating waveguide crossings via Parallel Switching Elements (PSE) slashes optical path loss by several dB, cutting laser power requirements threefold.",
      "citation": "C. Kao et al., 'Low-Loss Switching Elements for WDM Optical Networks-on-Chip,' IEEE TCAD, Vol. 45, No. 3, pp. 1120\u20131134, Mar. 2026. DOI: 10.1109/TCAD.2025.3521098."
    },
    "answer": 0,
    "explanation": "Option A is correct. Parallel Switching Elements eliminate internal orthogonal waveguide crossings, slashing optical path loss."
  },
  {
    "id": "q42",
    "module": "Track 7: Emerging Frontiers (Book Ch 10)",
    "tier": "Tier 3: Silicon Mastery",
    "tier_level": 3,
    "base_points": 300,
    "type": "multiple",
    "question": "Which of the following physical and thermal factors explain why silicon's thermo-optic coefficient (dn/dT \u2248 1.86 \u00d7 10^{-4} K^{-1}) poses a critical challenge for dense WDM Optical Networks-on-Chip? (Select all that apply)",
    "options": [
      "Thermal expansion and refractive index shifts cause Micro-Ring Resonator (MRR) resonant wavelengths to drift by approximately 0.08\u20130.11 nm/\u00b0C.",
      "In dense WDM networks with 0.4\u20130.8 nm channel spacing, a localized temperature shift of just 4\u00b0C to 8\u00b0C detunes the resonator from its laser wavelength, causing severe optical signal extinction or channel crosstalk.",
      "Active thermal stabilization using integrated microheaters consumes 15\u201325 mW per nanometer of tuning, dissipating multiple watts of static power across hundreds of on-chip resonators.",
      "Silicon waveguides melt whenever temperature increases by more than 1\u00b0C."
    ],
    "answers": [
      0,
      1,
      2
    ],
    "solution": {
      "summary": "Options A, B, and C correctly detail thermo-optic drift, WDM detuning sensitivity, and microheater tuning power overhead. Option D is an absurd physical claim.",
      "derivation": "Micro-Ring Resonators (MRRs) filter light based on constructive interference: lambda_res = (2 * pi * r * n_eff) / m, where r is ring radius, n_eff is effective refractive index, and m is the resonance order. Silicon exhibits a strong positive thermo-optic coefficient: dn/dT ~ 1.86 x 10^-4 K^-1. As a result, temperature variations shift the resonant wavelength: d(lambda_res) / dT = (lambda_res / n_g) * (dn_eff / dT) ~ 0.08 to 0.11 nm / \u00b0C. In a dense WDM system with 50 GHz to 100 GHz channel spacing (0.4 nm to 0.8 nm between adjacent wavelengths): (1) Localized Hotspots: A 5\u00b0C thermal gradient across the chip shifts resonance by ~0.5 nm, completely detuning the MRR from its designated laser wavelength (causing 20\u201330 dB optical signal attenuation) or misaligning it with an adjacent channel (generating severe inter-channel crosstalk). (2) Thermal Tuning Burden: To maintain resonance locking, integrated titanium or nickel-chromium microheaters must actively heat cooler rings to match the highest chip hotspot temperature. Because thermal tuning consumes 15\u201325 mW per nm of redshift, stabilizing a 64-channel WDM network across 30\u00b0C chip temperature swings can consume over 30 to 45 Watts of electrical heating power\u2014often exceeding the power of the computing cores themselves!",
      "options_analysis": [
        {
          "option": "A",
          "status": "Correct",
          "explanation": "True. Silicon's thermo-optic coefficient shifts resonance by ~0.1 nm/\u00b0C."
        },
        {
          "option": "B",
          "status": "Correct",
          "explanation": "True. With dense WDM channel spacing of 0.4\u20130.8 nm, small 5\u00b0C thermal shifts cause complete optical link dropouts."
        },
        {
          "option": "C",
          "status": "Correct",
          "explanation": "True. Active microheater stabilization dissipates 15\u201325 mW/nm, consuming multi-watt power budgets across large optical networks."
        },
        {
          "option": "D",
          "status": "Incorrect Distractor",
          "explanation": "False. Silicon melting point is 1414\u00b0C; 1\u00b0C temperature changes do not melt semiconductor crystals."
        }
      ],
      "takeaway": "Thermo-optic drift (~0.1 nm/\u00b0C) can detune dense WDM optical links under slight thermal gradients, requiring multi-watt microheater tuning or athermal resonator designs.",
      "citation": "Y. Ye et al., 'System-Level Thermal Modeling and Dynamic Thermal Management for Optical Networks-on-Chip,' IEEE TVLSI, Vol. 21, No. 9, pp. 1656\u20131669, Sept. 2013. DOI: 10.1109/TVLSI.2012.2217163."
    },
    "answer": 0,
    "explanation": "Options A, B, and C correctly detail thermo-optic drift, WDM detuning sensitivity, and microheater tuning power overhead. Option D is an absurd physical claim."
  }
];

let activeQuestions = [];
let currentIdx = 0;
let userScore = 0;
let correctCount = 0;
let timerInterval = null;
let timeLeft = 45;
let candidate = { name: "", org: "", mode: "full", certId: "", date: "" };
let selectedOptions = new Set();

function startQuiz() {
  candidate.name = document.getElementById("candidateName").value.trim() || "Hardware Architect";
  candidate.org = document.getElementById("candidateOrg").value.trim() || "Research Laboratory";
  candidate.mode = document.getElementById("assessmentMode").value;

  if (candidate.mode === "tier1_sprint") {
    activeQuestions = QUESTIONS_BANK.filter(q => q.tier_level === 1).slice(0, 4);
  } else if (candidate.mode === "grandmaster") {
    activeQuestions = QUESTIONS_BANK.filter(q => q.tier_level === 3).slice(0, 4);
  } else {
    // 12 question comprehensive sample
    const t1 = QUESTIONS_BANK.filter(q => q.tier_level === 1);
    const t2 = QUESTIONS_BANK.filter(q => q.tier_level === 2);
    const t3 = QUESTIONS_BANK.filter(q => q.tier_level === 3);
    activeQuestions = [
      ...t1.slice(0, 4),
      ...t2.slice(0, 4),
      ...t3.slice(0, 4)
    ];
  }

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
  selectedOptions.clear();

  document.getElementById("quizProgress").textContent = `Question ${idx + 1} of ${activeQuestions.length}`;
  document.getElementById("quizModuleBadge").textContent = q.module;
  document.getElementById("quizTierBadge").textContent = q.tier;
  document.getElementById("quizPtsBadge").textContent = `+${q.base_points} pts`;

  // Tier badge styling
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

  // Multiple Choice vs Single Choice setup
  const isMultiple = (q.type === "multiple" || (Array.isArray(q.answers) && q.answers.length > 1));
  const typeBadge = document.getElementById("quizTypeBadge");
  const typeHint = document.getElementById("quizTypeHint");
  if (isMultiple) {
    typeBadge.textContent = "☑️ Multiple Choice (Choose All That Apply)";
    typeBadge.style.background = "rgba(16, 185, 129, 0.12)";
    typeBadge.style.color = "#059669";
    typeBadge.style.borderColor = "rgba(16, 185, 129, 0.25)";
    typeHint.innerHTML = "💡 <strong>Multiple Choice:</strong> One or more choices are correct. Select all options that apply, then click <strong>Submit Answer</strong>.";
  } else {
    typeBadge.textContent = "🔘 Single Choice";
    typeBadge.style.background = "rgba(59, 130, 246, 0.12)";
    typeBadge.style.color = "#2563eb";
    typeBadge.style.borderColor = "rgba(59, 130, 246, 0.25)";
    typeHint.innerHTML = "💡 <strong>Single Choice:</strong> Choose the best option, then click <strong>Submit Answer</strong>.";
  }

  document.getElementById("quizQuestionText").textContent = q.question;

  const optionsContainer = document.getElementById("quizOptions");
  optionsContainer.innerHTML = "";

  q.options.forEach((opt, oIdx) => {
    const btn = document.createElement("button");
    btn.className = "noc-sim-select";
    btn.id = `q_opt_${oIdx}`;
    btn.style.textAlign = "left";
    btn.style.padding = "0.85rem 1.1rem";
    btn.style.cursor = "pointer";
    btn.style.width = "100%";
    btn.style.fontSize = "0.93rem";
    btn.style.lineHeight = "1.5";
    btn.style.display = "flex";
    btn.style.alignItems = "flex-start";
    btn.style.gap = "0.75rem";
    btn.style.transition = "all 0.15s ease";
    btn.style.borderRadius = "8px";

    updateOptionButtonVisual(btn, oIdx, false, isMultiple, opt);
    btn.onclick = () => toggleOption(oIdx, isMultiple);
    optionsContainer.appendChild(btn);
  });

  updateSelectionState();

  document.getElementById("quizFeedback").style.display = "none";
  document.getElementById("nextBtn").style.display = "none";
  document.getElementById("submitBtn").style.display = "inline-flex";

  // Start Timer (45s per question)
  clearInterval(timerInterval);
  timeLeft = 45;
  document.getElementById("quizTimer").textContent = `⏱️ ${timeLeft}s`;
  timerInterval = setInterval(() => {
    timeLeft--;
    document.getElementById("quizTimer").textContent = `⏱️ ${timeLeft}s`;
    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      submitUserAnswer(true);
    }
  }, 1000);
}

function updateOptionButtonVisual(btn, oIdx, isSelected, isMultiple, optText) {
  const icon = isMultiple
    ? (isSelected ? "☑️" : "⬜")
    : (isSelected ? "🔘" : "⚪");
  
  if (isSelected) {
    btn.style.background = "rgba(37, 99, 235, 0.1)";
    btn.style.borderColor = "#2563eb";
    btn.style.boxShadow = "0 0 0 1px #2563eb";
  } else {
    btn.style.background = "var(--noc-card-bg, #ffffff)";
    btn.style.borderColor = "var(--tcl-border, #cbd5e1)";
    btn.style.boxShadow = "none";
  }

  btn.innerHTML = `
    <span style="font-size:1.15rem; flex-shrink:0; margin-top:-1px;">${icon}</span>
    <span style="flex-grow:1;">
      <strong style="color:var(--tcl-heading); margin-right:4px;">${String.fromCharCode(65 + oIdx)}.</strong>
      ${optText}
    </span>
  `;
}

function toggleOption(oIdx, isMultiple) {
  const q = activeQuestions[currentIdx];
  const btn = document.getElementById(`q_opt_${oIdx}`);

  if (isMultiple) {
    if (selectedOptions.has(oIdx)) {
      selectedOptions.delete(oIdx);
      updateOptionButtonVisual(btn, oIdx, false, true, q.options[oIdx]);
    } else {
      selectedOptions.add(oIdx);
      updateOptionButtonVisual(btn, oIdx, true, true, q.options[oIdx]);
    }
  } else {
    selectedOptions.forEach(prevIdx => {
      const prevBtn = document.getElementById(`q_opt_${prevIdx}`);
      if (prevBtn) updateOptionButtonVisual(prevBtn, prevIdx, false, false, q.options[prevIdx]);
    });
    selectedOptions.clear();
    selectedOptions.add(oIdx);
    updateOptionButtonVisual(btn, oIdx, true, false, q.options[oIdx]);
  }

  updateSelectionState();
}

function updateSelectionState() {
  const count = selectedOptions.size;
  document.getElementById("quizSelectionCount").textContent = `Selected: ${count} option(s)`;
  const submitBtn = document.getElementById("submitBtn");
  if (count === 0) {
    submitBtn.style.opacity = "0.5";
    submitBtn.style.cursor = "not-allowed";
  } else {
    submitBtn.style.opacity = "1";
    submitBtn.style.cursor = "pointer";
  }
}

function submitUserAnswer(isTimeout = false) {
  if (!isTimeout && selectedOptions.size === 0) {
    alert("Please select at least one option before submitting.");
    return;
  }

  clearInterval(timerInterval);
  const q = activeQuestions[currentIdx];
  
  const correctArr = Array.isArray(q.answers) ? q.answers : [q.answer];
  const correctSet = new Set(correctArr);

  let isExactMatch = (selectedOptions.size === correctSet.size) &&
    [...selectedOptions].every(idx => correctSet.has(idx));

  let correctSelected = 0;
  let incorrectSelected = 0;
  selectedOptions.forEach(idx => {
    if (correctSet.has(idx)) correctSelected++;
    else incorrectSelected++;
  });

  let earnedPoints = 0;
  let statusClass = "incorrect";
  if (isExactMatch) {
    correctCount++;
    const speedBonus = timeLeft * 2;
    earnedPoints = q.base_points + speedBonus;
    userScore += earnedPoints;
    statusClass = "correct";
  } else if (correctSelected > 0 && incorrectSelected === 0) {
    earnedPoints = Math.round(q.base_points * (correctSelected / correctSet.size));
    userScore += earnedPoints;
    statusClass = "partial";
  }

  document.getElementById("quizScore").textContent = `Score: ${userScore} pts`;

  // Disable option clicks and apply graded visuals
  q.options.forEach((optText, oIdx) => {
    const btn = document.getElementById(`q_opt_${oIdx}`);
    btn.onclick = null;
    btn.style.cursor = "default";

    const userSelected = selectedOptions.has(oIdx);
    const isCorrectOption = correctSet.has(oIdx);

    let badge = "";
    if (userSelected && isCorrectOption) {
      btn.style.background = "rgba(34, 197, 94, 0.15)";
      btn.style.borderColor = "#22c55e";
      badge = `<span style="background:#16a34a; color:#fff; font-size:0.75rem; padding:2px 8px; border-radius:10px; margin-left:8px; font-weight:700;">✓ Correct (Selected)</span>`;
    } else if (userSelected && !isCorrectOption) {
      btn.style.background = "rgba(239, 68, 68, 0.15)";
      btn.style.borderColor = "#ef4444";
      badge = `<span style="background:#dc2626; color:#fff; font-size:0.75rem; padding:2px 8px; border-radius:10px; margin-left:8px; font-weight:700;">✗ Incorrect (Selected)</span>`;
    } else if (!userSelected && isCorrectOption) {
      btn.style.background = "rgba(34, 197, 94, 0.08)";
      btn.style.borderColor = "#22c55e";
      btn.style.borderStyle = "dashed";
      badge = `<span style="background:#eab308; color:#000; font-size:0.75rem; padding:2px 8px; border-radius:10px; margin-left:8px; font-weight:700;">⚠️ Correct Choice (Missed)</span>`;
    } else {
      btn.style.opacity = "0.55";
      badge = `<span style="color:#64748b; font-size:0.75rem; margin-left:8px;">(Incorrect distractor)</span>`;
    }

    btn.innerHTML = `
      <span style="font-size:1.15rem; flex-shrink:0;">${isCorrectOption ? "✅" : (userSelected ? "❌" : "⚪")}</span>
      <span style="flex-grow:1;">
        <strong style="color:var(--tcl-heading);">${String.fromCharCode(65 + oIdx)}.</strong> ${optText}
        ${badge}
      </span>
    `;
  });

  // Render Full Solution
  renderFullSolution(q, statusClass, earnedPoints, isExactMatch, correctArr);

  document.getElementById("submitBtn").style.display = "none";
  document.getElementById("nextBtn").style.display = "inline-flex";
}

function renderFullSolution(q, statusClass, earnedPoints, isExactMatch, correctArr) {
  const fb = document.getElementById("quizFeedback");
  fb.style.display = "block";

  const correctLetters = correctArr.map(idx => String.fromCharCode(65 + idx)).join(", ");

  let statusHeader = "";
  if (statusClass === "correct") {
    fb.style.background = "rgba(34, 197, 94, 0.08)";
    fb.style.border = "1px solid rgba(34, 197, 94, 0.35)";
    fb.style.color = "#14532d";
    statusHeader = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
        <span style="font-size:1.05rem; font-weight:800; color:#16a34a;">🎉 Perfect! Correct Selection (+${earnedPoints} pts)</span>
        <span class="noc-track-badge" style="background:#16a34a; color:#fff;">Full Score</span>
      </div>
    `;
  } else if (statusClass === "partial") {
    fb.style.background = "rgba(234, 179, 8, 0.1)";
    fb.style.border = "1px solid rgba(234, 179, 8, 0.35)";
    fb.style.color = "#713f12";
    statusHeader = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
        <span style="font-size:1.05rem; font-weight:800; color:#ca8a04;">⚠️ Partially Correct (+${earnedPoints} pts)</span>
        <span class="noc-track-badge" style="background:#ca8a04; color:#fff;">Partial Credit</span>
      </div>
    `;
  } else {
    fb.style.background = "rgba(239, 68, 68, 0.08)";
    fb.style.border = "1px solid rgba(239, 68, 68, 0.35)";
    fb.style.color = "#7f1d1d";
    statusHeader = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
        <span style="font-size:1.05rem; font-weight:800; color:#dc2626;">❌ Incorrect (0 pts)</span>
        <span class="noc-track-badge" style="background:#dc2626; color:#fff;">No Credit</span>
      </div>
    `;
  }

  const sol = q.solution || {};
  let optionsHtml = "";
  if (sol.options_analysis && Array.isArray(sol.options_analysis)) {
    optionsHtml = sol.options_analysis.map(oa => {
      const isCor = (oa.status.toLowerCase().includes("correct") || oa.status.toLowerCase().includes("true"));
      const bg = isCor ? "rgba(34, 197, 94, 0.08)" : "rgba(239, 68, 68, 0.05)";
      const bdr = isCor ? "rgba(34, 197, 94, 0.3)" : "rgba(239, 68, 68, 0.25)";
      const icon = isCor ? "✅" : "❌";
      const tagColor = isCor ? "#16a34a" : "#dc2626";
      return `
        <div style="background:${bg}; border:1px solid ${bdr}; border-radius:8px; padding:0.75rem 1rem; margin-bottom:0.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <strong style="color:var(--tcl-heading);">Option ${oa.option}</strong>
            <span style="font-size:0.78rem; font-weight:700; color:${tagColor}; text-transform:uppercase;">${icon} ${oa.status}</span>
          </div>
          <div style="font-size:0.88rem; line-height:1.5; color:var(--tcl-body);">${oa.explanation}</div>
        </div>
      `;
    }).join("");
  }

  fb.innerHTML = `
    ${statusHeader}
    
    <div style="margin-bottom:1rem; padding:0.6rem 0.9rem; background:rgba(37, 99, 235, 0.08); border-left:4px solid #2563eb; border-radius:4px;">
      <strong style="color:#1d4ed8;">🎯 Correct Answer: Option ${correctLetters}</strong>
      <div style="font-size:0.88rem; margin-top:2px; color:var(--tcl-body);">${sol.summary || q.explanation}</div>
    </div>

    <div style="margin-bottom:1rem;">
      <h4 style="margin:0 0 6px 0; font-size:0.95rem; font-weight:700; color:var(--tcl-heading);">🔬 Detailed Architectural &amp; Mathematical Solution:</h4>
      <div style="font-size:0.9rem; line-height:1.6; color:var(--tcl-body);">${sol.derivation || q.explanation}</div>
    </div>

    ${optionsHtml ? `
      <div style="margin-bottom:1rem;">
        <h4 style="margin:0 0 6px 0; font-size:0.95rem; font-weight:700; color:var(--tcl-heading);">🔍 Option-by-Option Breakdown &amp; Distractor Analysis:</h4>
        ${optionsHtml}
      </div>
    ` : ""}

    ${sol.takeaway ? `
      <div style="margin-bottom:0.75rem; padding:0.6rem 0.9rem; background:rgba(147, 51, 234, 0.08); border-left:4px solid #9333ea; border-radius:4px;">
        <strong style="color:#7e22ce;">💡 Silicon Architect's Takeaway:</strong>
        <div style="font-size:0.88rem; margin-top:2px; color:var(--tcl-body);">${sol.takeaway}</div>
      </div>
    ` : ""}

    ${sol.citation ? `
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); font-style:italic;">
        📚 <strong>Literature Reference:</strong> ${sol.citation}
      </div>
    ` : ""}
  `;
}

function nextQuestion() {
  currentIdx++;
  loadQuestion(currentIdx);
}

function finishQuiz() {
  document.getElementById("stepQuiz").style.display = "none";
  document.getElementById("stepResult").style.display = "block";

  const accuracy = Math.round((correctCount / activeQuestions.length) * 100);
  document.getElementById("resultSummary").innerHTML = `Candidate: <strong>${candidate.name}</strong> | Total Score: <strong>${userScore}</strong> pts | Accuracy: <strong>${accuracy}%</strong> (${correctCount}/${activeQuestions.length} correct)`;

  // Set Certificate Fields
  document.getElementById("certCandidateName").textContent = candidate.name;
  document.getElementById("certCandidateOrg").textContent = candidate.org;
  document.getElementById("certScore").textContent = `${userScore} pts (${accuracy}%)`;

  const now = new Date();
  candidate.date = now.toISOString().split("T")[0];
  document.getElementById("certDate").textContent = candidate.date;

  // Generate deterministic verification hash
  let hashVal = 0;
  const hashRaw = `${candidate.name}-${userScore}-${candidate.date}`;
  for (let i = 0; i < hashRaw.length; i++) {
    hashVal = (hashVal << 5) - hashVal + hashRaw.charCodeAt(i);
    hashVal |= 0;
  }
  candidate.certId = `NOC-CERT-${now.getFullYear()}-${Math.abs(hashVal).toString(16).toUpperCase().padStart(6, '0')}`;
  document.getElementById("certHash").textContent = candidate.certId;

  saveScoreToLocalStorage({
    name: candidate.name,
    org: candidate.org,
    track: candidate.mode === "grandmaster" ? "Grandmaster (Tier 3)" : (candidate.mode === "tier1_sprint" ? "Fundamentals Sprint" : "Comprehensive Exam"),
    score: userScore,
    accuracy: accuracy,
    certId: candidate.certId,
    date: candidate.date,
    type: "quiz"
  });
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

function submitToGithubIssue() {
  const repo = "network-on-chip/learning";
  const title = `[quiz-result] ${candidate.name} — ${userScore} pts — ${candidate.certId}`;
  const accuracy = Math.round((correctCount / activeQuestions.length) * 100);
  const body = [
    "### NoC Architecture Assessment Submission",
    `- **Candidate**: ${candidate.name}`,
    `- **Institution**: ${candidate.org}`,
    `- **Assessment Mode**: ${candidate.mode}`,
    `- **Total Score**: ${userScore} pts`,
    `- **Accuracy**: ${accuracy}% (${correctCount}/${activeQuestions.length} correct)`,
    `- **Credential Hash**: \`${candidate.certId}\``,
    `- **Date**: ${candidate.date}`,
    "",
    "```json",
    JSON.stringify({
      candidate: candidate.name,
      org: candidate.org,
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
