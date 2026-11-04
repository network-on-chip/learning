# 📖 Network-on-Chip Architecture Glossary

A comprehensive, searchable encyclopedia of terminology across on-chip interconnects, silicon microarchitecture, and routing theory.

<div class="noc-sim-container" style="margin-bottom:2rem;">
  <div style="display:flex; gap:0.75rem; flex-wrap:wrap; margin-bottom:1rem;">
    <input type="text" id="glossarySearch" class="noc-sim-select" style="flex-grow:1; min-width:260px;" placeholder="Search terminology (e.g. Flit, Deadlock, Duato, UCIe)..." oninput="filterGlossary()">
    <select id="glossaryFilter" class="noc-sim-select" onchange="filterGlossary()">
      <option value="all">All Domains</option>
      <option value="flow">Flow Control & Switching</option>
      <option value="micro">Router Microarchitecture</option>
      <option value="topo">Topologies & Metrics</option>
      <option value="routing">Routing & Deadlock</option>
      <option value="emerging">Chiplets & 3D NoC</option>
    </select>
  </div>
  <div id="glossaryCount" style="font-size:0.85rem; color:var(--md-default-fg-color--lighter);">Showing all 20 terms</div>
</div>

<div id="glossaryGrid" style="display:flex; flex-direction:column; gap:1.25rem;">

  <div class="noc-track-card glossary-item" data-domain="flow" data-term="flit flow control unit">
    <div>
      <span class="noc-track-badge">Flow Control</span>
      <div class="noc-track-title">Flit (Flow Control Unit)</div>
      <div class="noc-track-desc">
        The atomic unit of buffer allocation and flow control in an on-chip network. A packet is segmented into multiple flits: a <strong>Head Flit</strong> (carries routing and allocation headers), one or more <strong>Body Flits</strong> (carry payload data), and a <strong>Tail Flit</strong> (releases reserved virtual channels and state).
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="flow" data-term="phit physical unit">
    <div>
      <span class="noc-track-badge">Flow Control</span>
      <div class="noc-track-title">Phit (Physical Unit)</div>
      <div class="noc-track-desc">
        The unit of data transferred across the physical link wires in a single clock cycle. If the physical channel width is 128 bits and a flit is 128 bits, then 1 Flit = 1 Phit.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="flow" data-term="wormhole switching">
    <div>
      <span class="noc-track-badge">Flow Control</span>
      <div class="noc-track-title">Wormhole Switching</div>
      <div class="noc-track-desc">
        A pipelined packet switching technique proposed by Dally and Seitz (1986). The head flit carves out a path across routers, body flits follow immediately behind, and if blocked, the packet halts in place spanning across multiple router buffers without requiring entire packets to be buffered at a single node.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="micro" data-term="head of line blocking hol">
    <div>
      <span class="noc-track-badge">Microarchitecture</span>
      <div class="noc-track-title">Head-of-Line (HoL) Blocking</div>
      <div class="noc-track-desc">
        A performance bottleneck occurring when a packet at the head of a single FIFO buffer is blocked by contention at its target output port, preventing trailing packets behind it from advancing even if their requested output ports are completely free. Eliminated using <strong>Virtual Channels</strong>.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="micro" data-term="virtual channel vc">
    <div>
      <span class="noc-track-badge">Microarchitecture</span>
      <div class="noc-track-title">Virtual Channel (VC)</div>
      <div class="noc-track-desc">
        Multiple independent logical FIFO buffers sharing the same physical link wires on a cycle-by-cycle, time-multiplexed basis. Enables unblocked packets to bypass blocked packets, eliminating HoL blocking and providing protocol deadlock isolation.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="micro" data-term="matrix arbiter lru">
    <div>
      <span class="noc-track-badge">Microarchitecture</span>
      <div class="noc-track-title">Matrix Arbiter</div>
      <div class="noc-track-desc">
        A fast triangular bit-matrix hardware arbiter that implements exact Least Recently Used (LRU) fairness. When client $k$ wins, row $k$ is cleared to 0 and column $k$ is set to 1. Computes grants in two levels of logic gates (&lt; 200 ps).
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="topo" data-term="bisection bandwidth">
    <div>
      <span class="noc-track-badge">Topologies</span>
      <div class="noc-track-title">Bisection Bandwidth</div>
      <div class="noc-track-desc">
        The minimum bandwidth across all possible cuts that partition the network into two equal halves with equal numbers of nodes. Represents the ultimate throughput bottleneck under adversarial traffic patterns.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="topo" data-term="folded torus">
    <div>
      <span class="noc-track-badge">Topologies</span>
      <div class="noc-track-title">Folded Torus</div>
      <div class="noc-track-desc">
        A physical layout transformation that interleaves nodes accordion-style to ensure all torus links are identical in length (at most 2 tile widths), eliminating long global wrap-around wires and high RC delays.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="topo" data-term="concentrated mesh cmesh">
    <div>
      <span class="noc-track-badge">Topologies</span>
      <div class="noc-track-title">Concentrated Mesh (cMesh)</div>
      <div class="noc-track-desc">
        An optimized topology where 4 neighboring compute tiles share a single high-radix router. Reduces total router count by 75% and slashes network diameter and zero-load latency by more than half compared to a standard 2D mesh.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="routing" data-term="dimension order routing dor xy">
    <div>
      <span class="noc-track-badge">Routing &amp; Deadlock</span>
      <div class="noc-track-title">Dimension-Order Routing (DOR / XY)</div>
      <div class="noc-track-desc">
        A deterministic routing algorithm where packets strictly traverse along the horizontal dimension ($X$) until reaching the destination column, then turn into the vertical dimension ($Y$). Prohibits all 4 Y-to-X turns, guaranteeing that the Channel Dependency Graph is strictly acyclic.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="routing" data-term="turn model west first">
    <div>
      <span class="noc-track-badge">Routing &amp; Deadlock</span>
      <div class="noc-track-title">The Turn Model (Glass &amp; Ni)</div>
      <div class="noc-track-desc">
        A methodology proving that prohibiting only 2 turns (one clockwise and one counter-clockwise) is sufficient to prevent cycles. <strong>West-First</strong> outlaws South $\rightarrow$ West and North $\rightarrow$ West, leaving 6 out of 8 turns fully permitted (75% adaptivity).
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="routing" data-term="duato theorem escape virtual channel">
    <div>
      <span class="noc-track-badge">Routing &amp; Deadlock</span>
      <div class="noc-track-title">Duato's Theorem &amp; Escape Channels</div>
      <div class="noc-track-desc">
        Proves that an adaptive routing network can contain dependency cycles provided there exists an acyclic escape subnetwork (e.g. using XY VCs) that blocked packets can always access to drain and ensure forward progress.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="emerging" data-term="through silicon via tsv 3d noc">
    <div>
      <span class="noc-track-badge">Chiplets &amp; 3D NoC</span>
      <div class="noc-track-title">Through-Silicon Via (TSV)</div>
      <div class="noc-track-desc">
        Microscopic vertical copper interconnects penetrating through wafer-thinned silicon dies (20–50 $\mu$m). Enables 7-port 3D NoC routers with vertical Up/Down ports and sub-cycle vertical traversal.
      </div>
    </div>
  </div>

  <div class="noc-track-card glossary-item" data-domain="emerging" data-term="universal chiplet interconnect express ucie">
    <div>
      <span class="noc-track-badge">Chiplets &amp; 3D NoC</span>
      <div class="noc-track-title">UCIe (Universal Chiplet Interconnect Express)</div>
      <div class="noc-track-desc">
        The open industry standard for high-bandwidth, low-power die-to-die (D2D) chiplet interconnects. Delivers up to 1300 Gbps/mm shoreline bandwidth and &lt; 0.5 pJ/bit energy efficiency across 2.5D packaging.
      </div>
    </div>
  </div>

</div>

<script>
function filterGlossary() {
  const query = document.getElementById("glossarySearch").value.toLowerCase().trim();
  const domain = document.getElementById("glossaryFilter").value;
  const items = document.querySelectorAll(".glossary-item");

  let visibleCount = 0;
  items.forEach(item => {
    const term = item.getAttribute("data-term").toLowerCase();
    const itemDomain = item.getAttribute("data-domain");
    const matchesQuery = !query || term.includes(query) || item.innerText.toLowerCase().includes(query);
    const matchesDomain = (domain === "all") || (itemDomain === domain);

    if (matchesQuery && matchesDomain) {
      item.style.display = "flex";
      visibleCount++;
    } else {
      item.style.display = "none";
    }
  });

  document.getElementById("glossaryCount").textContent = `Showing ${visibleCount} of ${items.length} terms`;
}
</script>
