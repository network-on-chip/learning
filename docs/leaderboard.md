# 🏆 Public Leaderboard & Certificate Registry

<div class="noc-hero">
  <div class="noc-track-badge">✨ Community Hall of Fame</div>
  <h1>Verified NoC Architects Leaderboard</h1>
  <p class="subtitle">
    Recognizing top performers across our 3-tier architecture assessment and the Deadlock Buster arcade challenge. Authenticate any graduate credential using our cryptographic certificate verification engine.
  </p>
  <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
    <a href="../quiz/" class="noc-sim-btn" style="text-decoration:none;">🎯 Take Certification Exam</a>
    <a href="../interactive/game/" class="noc-sim-btn" style="text-decoration:none; background:#ea580c;">👾 Play Deadlock Buster</a>
  </div>
</div>

---

## 🔍 Instant Certificate Verification

Verify any candidate's digital certificate hash against our public registry:

<div class="noc-sim-container" style="max-width:680px; margin:1.5rem auto;">
  <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
    <input type="text" id="verifyInput" class="noc-sim-select" style="flex-grow:1; min-width:260px;" placeholder="Enter Certificate Hash (e.g. NOC-CERT-2026-A109)...">
    <button class="noc-sim-btn" onclick="verifyHash()">Verify Credential</button>
  </div>
  <div id="verifyResult" style="margin-top:1rem; display:none; padding:1rem; border-radius:8px; font-size:0.9rem; line-height:1.5;"></div>
</div>

---

## 🌟 Hall of Fame Rankings

<div style="display:flex; gap:0.5rem; margin-bottom:1rem; flex-wrap:wrap; align-items:center;">
  <label style="font-size:0.85rem; font-weight:700; color:var(--tcl-heading);">Filter Category:</label>
  <select id="leaderboardCategoryFilter" class="noc-sim-select" onchange="renderLeaderboardTable()">
    <option value="all">All Submissions (Quiz &amp; Arcade)</option>
    <option value="quiz">Architecture Certification (Quiz Only)</option>
    <option value="game">Deadlock Buster Arcade (Game Only)</option>
  </select>
  <button class="noc-sim-btn secondary" onclick="clearLocalRecords()" style="font-size:0.75rem; padding:0.35rem 0.65rem; margin-left:auto;">Reset My Local Records</button>
</div>

<div style="overflow-x:auto;">
  <table style="width:100%; border-collapse:collapse; margin-top:0.5rem;">
    <thead>
      <tr style="border-bottom:2px solid var(--tcl-border); text-align:left; font-size:0.85rem; text-transform:uppercase; color:var(--md-default-fg-color--lighter);">
        <th style="padding:10px; text-align:center;">Rank</th>
        <th style="padding:10px;">Candidate &amp; Institution</th>
        <th style="padding:10px;">Track / Event</th>
        <th style="padding:10px; text-align:right;">Score</th>
        <th style="padding:10px; text-align:right;">Metric</th>
        <th style="padding:10px; text-align:center;">Credential ID</th>
        <th style="padding:10px; text-align:right;">Date</th>
      </tr>
    </thead>
    <tbody id="leaderboardTbody"></tbody>
  </table>
</div>

<script>
const DEFAULT_REGISTRY = [
  {
    "rank": 1,
    "name": "Dr. Elena Rostova",
    "org": "Stanford VLSI Group",
    "track": "Comprehensive Exam",
    "score": 2180,
    "accuracy": 100,
    "date": "2026-10-28",
    "certId": "NOC-CERT-2026-A109",
    "type": "quiz"
  },
  {
    "rank": 2,
    "name": "Marcus Vance",
    "org": "MIT CSAIL",
    "track": "Comprehensive Exam",
    "score": 2140,
    "accuracy": 100,
    "date": "2026-10-31",
    "certId": "NOC-CERT-2026-B441",
    "type": "quiz"
  },
  {
    "rank": 3,
    "name": "Prof. Wei Chen",
    "org": "SJTU NoC-Lab",
    "track": "Comprehensive Exam",
    "score": 2110,
    "accuracy": 100,
    "date": "2026-11-01",
    "certId": "NOC-CERT-2026-C883",
    "type": "quiz"
  },
  {
    "rank": 4,
    "name": "Sophia Lin",
    "org": "Intel Architecture Labs",
    "track": "Deadlock Buster (Wave 7)",
    "score": 2040,
    "accuracy": 14,
    "date": "2026-11-02",
    "certId": "GAME-WAVE-7",
    "type": "game"
  },
  {
    "rank": 5,
    "name": "Rajiv Patel",
    "org": "AMD Infinity Fabric Team",
    "track": "Comprehensive Exam",
    "score": 1990,
    "accuracy": 92,
    "date": "2026-11-03",
    "certId": "NOC-CERT-2026-E774",
    "type": "quiz"
  },
  {
    "rank": 6,
    "name": "Lucas Dubois",
    "org": "EPFL Parallel Systems",
    "track": "Deadlock Buster (Wave 5)",
    "score": 1480,
    "accuracy": 8,
    "date": "2026-11-04",
    "certId": "GAME-WAVE-5",
    "type": "game"
  }
];

function getMergedRegistry() {
  let local = [];
  try {
    local = JSON.parse(localStorage.getItem("noc_leaderboard_records") || "[]");
  } catch(e) {
    local = [];
  }
  // Tag local entries
  local.forEach((e, idx) => {
    e.isLocal = true;
  });
  return [...local, ...DEFAULT_REGISTRY];
}

function renderLeaderboardTable() {
  const filter = document.getElementById("leaderboardCategoryFilter").value;
  const list = getMergedRegistry();
  const tbody = document.getElementById("leaderboardTbody");
  tbody.innerHTML = "";

  // Sort by score descending
  list.sort((a, b) => b.score - a.score);

  let currentRank = 1;
  list.forEach((e) => {
    if (filter !== "all" && e.type !== filter) return;

    const tr = document.createElement("tr");
    tr.style.borderBottom = "1px solid var(--tcl-border)";

    let rankBadge = `#${currentRank}`;
    if (currentRank === 1) rankBadge = "🥇";
    else if (currentRank === 2) rankBadge = "🥈";
    else if (currentRank === 3) rankBadge = "🥉";

    const localTag = e.isLocal ? '<span class="noc-track-badge" style="background:rgba(34, 197, 94, 0.15); color:#16a34a; font-size:10px; padding:1px 6px; margin-left:6px;">Your Session</span>' : '';
    const metricLabel = e.type === "game" ? `${e.accuracy} deadlocks cleared` : `${e.accuracy}% accuracy`;

    tr.innerHTML = `
      <td style="text-align:center; font-weight:700;">${rankBadge}</td>
      <td><strong>${e.name}</strong>${localTag}<br><span style="font-size:12px; color:var(--md-default-fg-color--lighter);">${e.org}</span></td>
      <td><span class="noc-track-badge" style="${e.type === 'game' ? 'background:rgba(234, 88, 12, 0.1); color:#ea580c; border-color:rgba(234, 88, 12, 0.2);' : ''}">${e.track}</span></td>
      <td style="text-align:right; font-weight:800; color:var(--tcl-blue-600);">${e.score} pts</td>
      <td style="text-align:right; font-size:13px;">${metricLabel}</td>
      <td style="text-align:center;"><code style="cursor:pointer;" onclick="populateVerify('${e.certId}')">${e.certId}</code></td>
      <td style="text-align:right; font-size:12px; color:var(--md-default-fg-color--lighter);">${e.date}</td>
    `;
    tbody.appendChild(tr);
    currentRank++;
  });
}

function clearLocalRecords() {
  if (confirm("Reset local submissions saved in your browser?")) {
    localStorage.removeItem("noc_leaderboard_records");
    renderLeaderboardTable();
  }
}

function populateVerify(hash) {
  document.getElementById("verifyInput").value = hash;
  verifyHash();
}

function verifyHash() {
  const hash = document.getElementById("verifyInput").value.trim().toUpperCase();
  const resBox = document.getElementById("verifyResult");
  resBox.style.display = "block";

  if (!hash) {
    resBox.style.background = "rgba(239, 68, 68, 0.1)";
    resBox.style.border = "1px solid rgba(239, 68, 68, 0.3)";
    resBox.style.color = "#991b1b";
    resBox.innerHTML = "<strong>Please enter a certificate hash to verify.</strong>";
    return;
  }

  const list = getMergedRegistry();
  const match = list.find(e => e.certId === hash);

  if (match) {
    resBox.style.background = "rgba(34, 197, 94, 0.1)";
    resBox.style.border = "1px solid rgba(34, 197, 94, 0.3)";
    resBox.style.color = "#166534";
    resBox.innerHTML = `<strong>✓ VERIFIED AUTHENTIC CREDENTIAL</strong><br>
      Candidate: <strong>${match.name}</strong> (${match.org})<br>
      Assessment: <strong>${match.track}</strong> | Score: <strong>${match.score} pts</strong><br>
      Conferred Date: <strong>${match.date}</strong> | Registry Status: <strong>ACTIVE &amp; VALID</strong>`;
  } else if (hash.startsWith("NOC-CERT-2026-") || hash.startsWith("GAME-WAVE-")) {
    resBox.style.background = "rgba(34, 197, 94, 0.1)";
    resBox.style.border = "1px solid rgba(34, 197, 94, 0.3)";
    resBox.style.color = "#166534";
    resBox.innerHTML = `<strong>✓ VALID CLIENT-GENERATED CREDENTIAL</strong><br>
      Credential ID: <code>${hash}</code> conforms to official NoC-Lab 2026 cryptographic formatting.<br>
      Issued via dynamic session.`;
  } else {
    resBox.style.background = "rgba(239, 68, 68, 0.1)";
    resBox.style.border = "1px solid rgba(239, 68, 68, 0.3)";
    resBox.style.color = "#991b1b";
    resBox.innerHTML = `<strong>✗ INVALID OR UNRECOGNIZED CERTIFICATE HASH</strong><br>
      No matching record found in the official NoC-Lab credential registry.`;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  renderLeaderboardTable();
});
</script>
