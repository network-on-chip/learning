# Track 3: Topologies & Interconnect Metrics

<div class="noc-hero">
  <div class="noc-track-badge">Network Architecture • Module 03</div>
  <h1>Interconnect Topologies &amp; Quantitative Performance Metrics</h1>
  <p class="subtitle">
    Master the spatial roadmap of silicon chips. Explore how routers and processing elements are physically and logically wired to maximize bisection bandwidth, minimize hop diameter, and conquer the physical layout constraints of 2D and 3D silicon.
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">⏱️ 4 In-Depth Lessons</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">💻 4 Synthesizable Verilog RTL Modules</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">🔬 4 Interactive Calculators &amp; Simulators</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">🎯 3-Question Self-Assessment Quizzes</span>
  </div>
</div>

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>📚 Aligned with Official Textbook Chapter 4</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
      For complete mathematical derivations of bisection bandwidth, zero-load latency formulas, folded torus wire balancing, Clos routing, and Dragonfly exascale networks, read <strong>Chapter 4: Direct, Indirect &amp; High-Radix Topologies</strong>.
    </div>
  </div>
  <a href="../textbook/ch04-topologies-and-metrics/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none; transition: background 0.2s;">
    <span>Read Chapter 4 Online →</span>
  </a>
</div>

---

## 🗺️ Topological Taxonomy & Learning Roadmap

The diagram below categorizes on-chip and system-level interconnect topologies by their architectural structure:

```mermaid
graph TD
  subgraph Topologies_Taxonomy ["Interconnect Topology Classification"]
    RootTop["Network Topology"] --> Direct["Direct Topologies<br/>(Every router pairs with compute node)"]
    RootTop --> Indirect["Indirect Topologies<br/>(Dedicated switches distinct from nodes)"]
    RootTop --> HighRadix["High-Radix & Hybrid<br/>(Trade crossbar radix for low diameter)"]

    Direct --> Mesh2D["2D Mesh<br/>(Intel Xeon, Tilera)"]
    Direct --> Torus2D["2D Torus & Folded Torus<br/>(Wrap-around symmetry)"]
    Direct --> Rings["Ring & Concentric Rings<br/>(Intel Nehalem/Broadwell)"]

    Indirect --> FatTree["Fat-Tree / Spine-Leaf<br/>(Constant bisection bandwidth)"]
    Indirect --> Clos["Clos & Butterfly Networks<br/>(Multistage MINs)"]

    HighRadix --> cMesh["Concentrated Mesh (cMesh)<br/>(4 cores per high-radix router)"]
    HighRadix --> Dfly["Dragonfly Topology<br/>(Hierarchical cliques & global links)"]
    HighRadix --> FBFly["Flattened Butterfly<br/>(Minimal diameter D=2)"]
  end

  classDef directStyle fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px,color:#1e3a8a;
  classDef indirectStyle fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px,color:#991b1b;
  classDef highRadixStyle fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#166534;

  class Direct,Mesh2D,Torus2D,Rings directStyle;
  class Indirect,FatTree,Clos indirectStyle;
  class HighRadix,cMesh,Dfly,FBFly highRadixStyle;
```

---

## 📚 Syllabus & Chapters in Track 3

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 3.1</span>
      <div class="noc-track-title">Direct Topologies: Mesh, Torus &amp; Folded Torus</div>
      <div class="noc-track-desc">
        Mathematical foundations of planar networks. Derive node degree, diameter, average hop count ($H_{avg} = \frac{2}{3}\sqrt{N}$), and bisection bandwidth ($B_b = 2\sqrt{N} \cdot w$). Solve the long wrap-around wire crisis using the Folded Torus layout.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable <code>folded_torus_node_map.v</code>, Interactive Mesh vs. Torus Topology Explorer &amp; Shortest-Path Visualizer, 3-Question Self-Check Quiz, 🌐 <em>Topology Titans</em> Arcade Mission.
      </div>
    </div>
    <a href="01-direct-topologies.md" class="noc-track-link">Launch Lesson 3.1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 3.2</span>
      <div class="noc-track-title">Indirect &amp; Concentrated Networks (Fat-Tree &amp; cMesh)</div>
      <div class="noc-track-desc">
        Separate switching elements from compute nodes. Explore Multistage Interconnection Networks (MINs), Clos networks, and Balfour &amp; Dally's Concentrated Mesh (cMesh), reducing router count by 75% and halving network diameter.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable <code>cmesh_concentrator.v</code>, Interactive 64-Core Mesh vs. cMesh Area &amp; Latency Calculator, 3-Question Self-Check Quiz, 🏗️ <em>Chiplet Tycoon</em> Lab.
      </div>
    </div>
    <a href="02-indirect-hierarchical.md" class="noc-track-link">Launch Lesson 3.2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 3.3</span>
      <div class="noc-track-title">Interconnect Metrics &amp; Benchmark Traffic Patterns</div>
      <div class="noc-track-desc">
        Formal mathematical modeling of Zero-Load Latency ($T_0$), Saturation Throughput ($\Theta_{sat}$), and Bisection Channel Load ($\gamma_{max}$). Benchmark networks under Uniform Random, Bit-Complement, Transpose, Tornado, and Rentian traffic locality.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable <code>traffic_pattern_generator.v</code>, Interactive Synthetic Traffic &amp; Bisection Stress Visualizer, Bit-Complement mathematical proof, 3-Question Self-Check Quiz, 🛡️ <em>Hotspot Hero</em> Arcade.
      </div>
    </div>
    <a href="03-metrics-traffic-patterns.md" class="noc-track-link">Launch Lesson 3.3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Lesson 3.4</span>
      <div class="noc-track-title">High-Radix Topologies: Dragonfly &amp; Flattened Butterfly</div>
      <div class="noc-track-desc">
        The high-radix revolution (Kim, Dally et al.). Trading crossbar radix for ultra-low diameter ($D \le 3$). Explore the Flattened Butterfly, Dragonfly hierarchical groups, Cray Slingshot, and NVIDIA NVLink NVSwitch architectures.
      </div>
      <div style="font-size:0.8rem; color:var(--md-default-fg-color--lighter); margin-bottom:1rem;">
        ⚡ <strong>Features:</strong> Synthesizable <code>dragonfly_ugal_arbiter.v</code>, Interactive High-Radix vs. Low-Radix Trade-off Explorer, Slingshot case study, 3-Question Self-Check Quiz, ⚔️ <em>Arbiter Arena</em>.
      </div>
    </div>
    <a href="04-high-radix-topologies.md" class="noc-track-link">Launch Lesson 3.4 →</a>
  </div>
</div>

---

## 🎯 Track Learning Objectives

Upon completing Track 3, you will be able to:

1. **Calculate network metrics rigorously** for any $k$-ary $n$-cube topology: node degree, diameter, bisection bandwidth, and average hop distance.
2. **Apply the Folded Torus layout** to eliminate global wrap-around wires, equalizing all inter-router link lengths on a planar die.
3. **Dimension Concentrated Meshes (cMesh)** to balance router radix complexity against network hop count and wire density.
4. **Evaluate throughput limits under benchmark traffic patterns** (Uniform Random, Bit-Complement, Transpose, Tornado) and identify bottleneck bisection channels.
5. **Architect High-Radix topologies** (Flattened Butterfly and Dragonfly) to compress network diameter down to 2–3 hops for exascale AI and server fabrics.

Ready to begin? Start with **[Lesson 3.1: Direct Topologies (Mesh & Torus)](01-direct-topologies.md)**.

