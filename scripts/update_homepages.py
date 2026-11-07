import re

# 1. Update index.md
with open('share/learning/docs/index.md', 'r', encoding='utf-8') as f:
    en_content = f.read()

# Update stats and hero links
en_content = en_content.replace(
    '<a href="track1-fundamentals/" class="noc-sim-btn secondary" style="text-decoration: none;">🚀 Start Curriculum</a>',
    '<a href="track1-interconnect-crisis/" class="noc-sim-btn secondary" style="text-decoration: none;">🚀 Start Curriculum</a>'
)

old_en_stats = """<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">12</span>
    <span class="noc-stat-label">Core Textbook Chapters</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">266</span>
    <span class="noc-stat-label">Monograph Pages</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">20</span>
    <span class="noc-stat-label">Interactive Labs &amp; Games</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">100%</span>
    <span class="noc-stat-label">Open &amp; Reproducible</span>
  </div>
</div>"""

new_en_stats = """<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">12</span>
    <span class="noc-stat-label">Core Textbook Chapters</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">266</span>
    <span class="noc-stat-label">Monograph Pages</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">13</span>
    <span class="noc-stat-label">Curriculum Tracks</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">53</span>
    <span class="noc-stat-label">Lessons &amp; RTL Cores</span>
  </div>
</div>"""

en_content = en_content.replace(old_en_stats, new_en_stats)

old_en_tracks_block = """  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 1</span>
      <div class="noc-track-title">Interconnect Fundamentals</div>
      <div class="noc-track-desc">
        Why shared buses failed. Packets, flits, and phits. Store-and-Forward vs Virtual Cut-Through vs Wormhole switching, credit turnaround latency loops, and Network Interface (NI) AXI packetization.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Interactive Simulators &amp; Calculators
      </div>
    </div>
    <a href="track1-fundamentals/" class="noc-track-link">Explore Track 1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 2</span>
      <div class="noc-track-title">Router Microarchitecture</div>
      <div class="noc-track-desc">
        Canonical 5-stage router pipelines (BW-RC-VA-SA-ST), Virtual Channel allocation, sub-200ps LRU matrix arbiters, and SMART single-cycle multi-hop bypass routers.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Interactive Simulators &amp; Verilog RTL
      </div>
    </div>
    <a href="track2-router-architecture/" class="noc-track-link">Explore Track 2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 3</span>
      <div class="noc-track-title">Topologies &amp; Interconnect Metrics</div>
      <div class="noc-track-desc">
        Direct (Mesh, Torus, Folded Torus), Indirect (Clos, Fat-Tree, cMesh), and High-Radix (Dragonfly, Flattened Butterfly). Mathematical derivations of $T_0$, $\Theta_{sat}$, bisection bandwidth, and UGAL adaptive routing.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; High-Radix Analyzer
      </div>
    </div>
    <a href="track3-topologies/" class="noc-track-link">Explore Track 3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 4</span>
      <div class="noc-track-title">Routing &amp; Deadlock Avoidance</div>
      <div class="noc-track-desc">
        Deterministic Dimension-Order Routing (DOR), Glass &amp; Ni's Turn Model, Chiu's Odd-Even algorithm, Duato's Escape Channels, Up*/Down* tree routing, and Cache Coherence VNET isolation.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; Arcade Links
      </div>
    </div>
    <a href="track4-routing-deadlock/" class="noc-track-link">Explore Track 4 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 5</span>
      <div class="noc-track-title">Thermal &amp; Congestion Management</div>
      <div class="noc-track-desc">
        Fourier heat diffusion, compact RC ladder models, Regional Congestion Awareness (RCA), source quenching, proactive ML hotspot forecasting, and sparse sensor reconstruction under non-Gaussian noise.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; Arcade Links
      </div>
    </div>
    <a href="track5-congestion-thermal/" class="noc-track-link">Explore Track 5 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 6</span>
      <div class="noc-track-title">Chiplets, 3D NoC &amp; Frontiers</div>
      <div class="noc-track-desc">
        Through-Silicon Vias (TSVs), 7-port 3D routers, negative binomial yield economics, 2.5D packaging (CoWoS, EMIB), the UCIe standard stack, 3D thermal stacking, Optical NoC (ONoC), and Wireless NoC (WNoC).
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; Arcade Links
      </div>
    </div>
    <a href="track6-chiplets-and-3d/" class="noc-track-link">Explore Track 6 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 7</span>
      <div class="noc-track-title">Landmark Paper Deep Dives</div>
      <div class="noc-track-desc">
        Undergraduate-readable walkthroughs of seminal IEEE JSSC, TCAD, and TVLSI papers: Intel 48-Core SCC (2-TB/s DVFS Mesh), NVIDIA Simba (36-chiplet GRS MCM), 3D Optical NoC (TSVs + Micro-Rings), and In-Network Computing neuromorphic routers.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Synthesizable Verilog RTLs • 4 Interactive Simulators &amp; Arcade Links
      </div>
    </div>
    <a href="track7-paper-walkthroughs/" class="noc-track-link">Explore Track 7 →</a>
  </div>"""

new_en_tracks_block = """  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 1</span>
      <div class="noc-track-title">Interconnect Crisis &amp; Wire Physics</div>
      <div class="noc-track-desc">
        Why shared buses failed. Wire scaling, Elmore RC delay modeling, optimal repeater insertion, and fundamental limits of on-chip energy and latency.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Synthesizable Elmore Verilog • Interactive Wire Simulator
      </div>
    </div>
    <a href="track1-interconnect-crisis/" class="noc-track-link">Explore Track 1 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 2</span>
      <div class="noc-track-title">Switching, Flow Control &amp; Buffers</div>
      <div class="noc-track-desc">
        Packets, flits, and phits. Store-and-Forward vs Virtual Cut-Through vs Wormhole switching, credit turnaround latency loops, and Network Interface (NI) AXI packetization.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Credit Counter RTL • Credit Commander Simulator
      </div>
    </div>
    <a href="track2-switching-flow-control/" class="noc-track-link">Explore Track 2 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 3</span>
      <div class="noc-track-title">Router Microarchitecture &amp; Arbitration</div>
      <div class="noc-track-desc">
        Canonical 5-stage router pipelines (BW-RC-VA-SA-ST), Virtual Channel allocation, sub-200ps LRU matrix arbiters, and SMART single-cycle multi-hop bypass routers.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • 5-Stage SystemVerilog Router • Arbiter Arena Lab
      </div>
    </div>
    <a href="track3-router-microarchitecture/" class="noc-track-link">Explore Track 3 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 4</span>
      <div class="noc-track-title">Direct, Indirect &amp; High-Radix Topologies</div>
      <div class="noc-track-desc">
        Direct (Mesh, Torus, Folded Torus), Indirect (Clos, Fat-Tree, cMesh), and High-Radix (Dragonfly, Flattened Butterfly). Mathematical derivations of $T_0$, $\Theta_{sat}$, and UGAL routing.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Topology Graph Metrics RTL • Interactive Topology Architect
      </div>
    </div>
    <a href="track4-topologies-and-metrics/" class="noc-track-link">Explore Track 4 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 5</span>
      <div class="noc-track-title">Deadlock Theory, Turn Models &amp; Routing</div>
      <div class="noc-track-desc">
        Deterministic Dimension-Order Routing (DOR), Glass &amp; Ni's Turn Model, Chiu's Odd-Even algorithm, Duato's Escape Channels, CDG acyclic proofs, and VNET isolation.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • SMT CDG Verifier • Deadlock Buster Arcade Game
      </div>
    </div>
    <a href="track5-routing-deadlock/" class="noc-track-link">Explore Track 5 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 6</span>
      <div class="noc-track-title">Low-Power Architectures &amp; Dark Silicon</div>
      <div class="noc-track-desc">
        Dark silicon physics, Thermal Design Power (TDP), multiple V/F islands, microarchitectural power gating, sleep state wakeups, and inductive $L\cdot di/dt$ emergencies.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Power Gating FSM RTL • Volt Vortex Simulator
      </div>
    </div>
    <a href="track6-low-power-dark-silicon/" class="noc-track-link">Explore Track 6 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 7</span>
      <div class="noc-track-title">Thermal Modeling &amp; Fault Tolerance</div>
      <div class="noc-track-desc">
        Fourier heat diffusion, compact RC ladder models, Regional Congestion Awareness (RCA), source quenching, proactive ML hotspot forecasting, and sparse sensor reconstruction.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Thermal Deflection RTL • Hotspot Hero &amp; Fault Defender
      </div>
    </div>
    <a href="track7-thermal-fault-tolerance/" class="noc-track-link">Explore Track 7 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 8</span>
      <div class="noc-track-title">3D Networks-on-Chip (3D-NoC) &amp; TSVs</div>
      <div class="noc-track-desc">
        Through-Silicon Vias (TSVs), Keep-Out Zones (KOZ), thermo-mechanical stress, 7-port 3D crossbars, vertical serialization, and 3D thermal stacking mitigation.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • 7-Port 3D Crossbar RTL • TSV Titan Simulator
      </div>
    </div>
    <a href="track8-3d-noc-tsvs/" class="noc-track-link">Explore Track 8 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 9</span>
      <div class="noc-track-title">Multi-Chiplet Interconnects &amp; UCIe</div>
      <div class="noc-track-desc">
        2.5D packaging economics, negative binomial yield, UCIe standard physical &amp; D2D adapter stacks, In/Outbound Swap deadlock recovery, and multi-chiplet bypassing.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • In/Outbound Swap RTL • Chiplet Tycoon Lab
      </div>
    </div>
    <a href="track9-chiplets-ucie/" class="noc-track-link">Explore Track 9 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 10</span>
      <div class="noc-track-title">Optical &amp; Wireless Networks-on-Chip</div>
      <div class="noc-track-desc">
        Silicon nanophotonic microring resonators (MRRs), wavelength-routed ONoCs (WRONoCs), laser power gating with APC loops, and on-chip mmWave/THz fabrics.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • Photonic MRR Switch RTL • Photon Pilot &amp; Wireless Wave
      </div>
    </div>
    <a href="track10-optical-wireless/" class="noc-track-link">Explore Track 10 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 11</span>
      <div class="noc-track-title">Hardware Security &amp; Trust in NoCs</div>
      <div class="noc-track-desc">
        On-chip threat models: eavesdropping, spoofing, and DoS. Timing, buffer, and thermal covert channels. HeatSense zero-multiplier EWMA thermal Trojan detection.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • HeatSense EWMA Verilog • Silicon Sentinel Arcade
      </div>
    </div>
    <a href="track11-security/" class="noc-track-link">Explore Track 11 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">Track 12</span>
      <div class="noc-track-title">Domain-Specific NoCs for AI &amp; LLMs</div>
      <div class="noc-track-desc">
        Large Language Models &amp; Collective Communication (AllReduce, AllGather). In-Network Reduction Routers, ultra-dense wafer-scale Ruche fabrics, and SNN multicasting.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 Lessons • In-Network Reduction SystemVerilog • Transformer Titan Lab
      </div>
    </div>
    <a href="track12-ai-llm-snn/" class="noc-track-link">Explore Track 12 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border-color: rgba(16, 185, 129, 0.3);">Track 13 • Capstone</span>
      <div class="noc-track-title">Capstone: Landmark Systems &amp; MoE Synthesis</div>
      <div class="noc-track-desc">
        Walkthroughs of seminal chips (Intel SCC 48-Core, NVIDIA Simba 36-Chiplet, 3D Optical NoC, In-Network TVLSI) culminating in the Grand Capstone: Zero-Trust Multi-Chiplet MoE Accelerator.
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 5 Lessons • Full SystemVerilog SoC RTL • Web EDA Auto-Grader Verification
      </div>
    </div>
    <a href="track13-capstone/" class="noc-track-link">Explore Capstone Track 13 →</a>
  </div>"""

assert old_en_tracks_block in en_content, 'old_en_tracks_block not found in index.md'
en_content = en_content.replace(old_en_tracks_block, new_en_tracks_block)

en_content = en_content.replace(
    '[Track 1: Interconnect Fundamentals](track1-fundamentals/index.md)',
    '[Track 1: Interconnect Crisis & Wire Physics](track1-interconnect-crisis/index.md)'
)

with open('share/learning/docs/index.md', 'w', encoding='utf-8') as f:
    f.write(en_content)
print('Updated index.md successfully!')

# 2. Update index.zh.md
with open('share/learning/docs/index.zh.md', 'r', encoding='utf-8') as f:
    zh_content = f.read()

zh_content = zh_content.replace(
    '<a href="track1-fundamentals/" class="noc-sim-btn secondary" style="text-decoration: none;">🚀 开始系统学习</a>',
    '<a href="track1-interconnect-crisis/" class="noc-sim-btn secondary" style="text-decoration: none;">🚀 开始系统学习</a>'
)

old_zh_stats = """<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">12</span>
    <span class="noc-stat-label">教材完整核心章节</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">266</span>
    <span class="noc-stat-label">正式出版级专著页数</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">20</span>
    <span class="noc-stat-label">交互式实验室与街机</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">100%</span>
    <span class="noc-stat-label">开源且可完全复现</span>
  </div>
</div>"""

new_zh_stats = """<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">12</span>
    <span class="noc-stat-label">教材完整核心章节</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">266</span>
    <span class="noc-stat-label">正式出版级专著页数</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">13</span>
    <span class="noc-stat-label">系统化教学模块</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">53</span>
    <span class="noc-stat-label">深度课时与硬件内核</span>
  </div>
</div>"""

zh_content = zh_content.replace(old_zh_stats, new_zh_stats)

old_zh_tracks_block = """  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第一模块</span>
      <div class="noc-track-title">片上互连基础</div>
      <div class="noc-track-desc">
        从共享总线瓶颈到片上网络架构。数据包（Packet）、微元（Flit）与物理传输单元（Phit）。存储转发、虚拟直通与虫洞交换（Wormhole）、信用（Credit）回路与网络接口（NI）微架构。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 包含 4 大交互式仿真器与计算器
      </div>
    </div>
    <a href="track1-fundamentals/" class="noc-track-link">进入模块一 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第二模块</span>
      <div class="noc-track-title">路由器微架构</div>
      <div class="noc-track-desc">
        标准五级流水线路由器（BW-RC-VA-SA-ST）、虚通道（Virtual Channel）管理、亚200ps矩阵仲裁器（Matrix Arbiter）与SMART单周期多跳旁路微架构。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 包含 4 大交互式仿真器与 Verilog RTL 实现
      </div>
    </div>
    <a href="track2-router-architecture/" class="noc-track-link">进入模块二 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第三模块</span>
      <div class="noc-track-title">拓扑结构与互连指标</div>
      <div class="noc-track-desc">
        直接拓扑（Mesh, Torus, 折叠环）、间接与集中拓扑（Fat-Tree, cMesh）与高基数拓扑（Dragonfly, 扁平蝶式网络）。深入推导 $T_0$、$\Theta_{sat}$、对分带宽与 UGAL 自适应路由。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 包含 4 大可综合 Verilog RTL • 4 大交互式仿真器与高基数权衡分析仪
      </div>
    </div>
    <a href="track3-topologies/" class="noc-track-link">进入模块三 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第四模块</span>
      <div class="noc-track-title">路由算法与死锁避免</div>
      <div class="noc-track-desc">
        确定性维序路由（XY 路由）、转向模型（西向优先、北向最后）、奇偶路由、杜阿托逃逸信道定理（Duato's Theorem）、生成树容错路由与缓存一致性协议死锁消除（VNET）。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 包含 4 大可综合 Verilog RTL 模块、4 大交互式仿真器与街机实战链接
      </div>
    </div>
    <a href="track4-routing-deadlock/" class="noc-track-link">进入模块四 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第五模块</span>
      <div class="noc-track-title">热管理与拥塞控制</div>
      <div class="noc-track-desc">
        傅里叶热扩散定律、RC紧凑热网络、区域拥塞感知（RCA）、源端限流压制、机器学习热点前瞻预测与非高斯噪声下稀疏传感器重构（深度融合实验室开源复现成果）。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 包含 4 大可综合 Verilog RTL 模块、4 大交互式仿真器与街机实战链接
      </div>
    </div>
    <a href="track5-congestion-thermal/" class="noc-track-link">进入模块五 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第六模块</span>
      <div class="noc-track-title">芯粒与三维片上网络</div>
      <div class="noc-track-desc">
        三维硅通孔（TSV）寄生与热应力禁放区（KOZ）、七端口三维路由器、负二项式良率经济学、先进封装（CoWoS/EMIB）、UCIe 协议栈、3D 堆叠热沉陷、光互连片上网络（ONoC）与无线射频（WNoC）前沿。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 包含 4 大可综合 Verilog RTL 模块、4 大交互式仿真器与街机实战链接
      </div>
    </div>
    <a href="track6-chiplets-and-3d/" class="noc-track-link">进入模块六 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第七模块</span>
      <div class="noc-track-title">经典论文深度精读</div>
      <div class="noc-track-desc">
        顶刊论文精读手册：英特尔 48 核 SCC 处理器（2-TB/s DVFS 网格）、英伟达 Simba 36 芯粒 GRS 封装、三维光互连片上网络（3D ONoC）以及类脑网内计算路由器。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 包含 4 大可综合 Verilog RTL 模块、4 大真实芯片仿真器与街机实战链接
      </div>
    </div>
    <a href="track7-paper-walkthroughs/" class="noc-track-link">进入模块七 →</a>
  </div>"""

new_zh_tracks_block = """  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第一模块</span>
      <div class="noc-track-title">多核通信危机与物理线互连</div>
      <div class="noc-track-desc">
        共享总线退役背后的物理根源。导线缩放效应、Elmore RC 延迟建模、最优中继器（Repeater）插入算法及片上能耗-延迟极限推导。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 可综合 Elmore Verilog • 导线物理仿真器
      </div>
    </div>
    <a href="track1-interconnect-crisis/" class="noc-track-link">进入模块一 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第二模块</span>
      <div class="noc-track-title">交换技术、流控与缓存管理</div>
      <div class="noc-track-desc">
        数据包（Packet）、微元（Flit）与物理单元（Phit）。存储转发、虚拟直通与虫洞交换（Wormhole）对比，信用（Credit）回路与 AXI 网络接口。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 信用计数器 RTL • 信用指挥官仿真器
      </div>
    </div>
    <a href="track2-switching-flow-control/" class="noc-track-link">进入模块二 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第三模块</span>
      <div class="noc-track-title">路由器微架构与仲裁调度</div>
      <div class="noc-track-desc">
        经典五级流水线路由器（BW-RC-VA-SA-ST）、虚通道（Virtual Channel）组织、亚 200ps 矩阵仲裁器与 SMART 单周期多跳旁路路由。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 五级流水线 SystemVerilog • 仲裁竞技场
      </div>
    </div>
    <a href="track3-router-microarchitecture/" class="noc-track-link">进入模块三 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第四模块</span>
      <div class="noc-track-title">直接/间接与高基数互连拓扑</div>
      <div class="noc-track-desc">
        直接拓扑（Mesh, Torus）、间接集中拓扑（Clos, Fat-Tree, cMesh）与高基数超算互连（Dragonfly, 扁平蝶式）。深入推导 $T_0$、$\Theta_{sat}$ 与 UGAL 路由。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 拓扑图指标 RTL • 交互式拓扑架构师
      </div>
    </div>
    <a href="track4-topologies-and-metrics/" class="noc-track-link">进入模块四 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第五模块</span>
      <div class="noc-track-title">死锁理论、转向模型与自适应路由</div>
      <div class="noc-track-desc">
        确定性 XY 路由、转向模型（西向优先、北向最后、奇偶路由）、杜阿托（Duato）逃逸信道定理、信道依赖图（CDG）证明与缓存一致性 VNET 隔离。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • SMT CDG 形式化验证器 • 死锁大作战街机
      </div>
    </div>
    <a href="track5-routing-deadlock/" class="noc-track-link">进入模块五 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第六模块</span>
      <div class="noc-track-title">低功耗架构与暗硅动态管理</div>
      <div class="noc-track-desc">
        暗硅物理极限、热设计功耗（TDP）、多电压频率岛（V/F 岛）、路由器微架构电源门控、唤醒状态机与电感性 $L\cdot di/dt$ 电压突降防护。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 电源门控 FSM RTL • 电压旋涡仿真器
      </div>
    </div>
    <a href="track6-low-power-dark-silicon/" class="noc-track-link">进入模块六 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第七模块</span>
      <div class="noc-track-title">热学建模、热点防御与容错弹性</div>
      <div class="noc-track-desc">
        傅里叶热扩散定律、RC 紧凑热网、区域拥塞感知（RCA）、源端限流压制、机器学习热点预测与非高斯噪声下稀疏传感器重构。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 热偏斜 Verilog RTL • 硅温保卫战与故障防御
      </div>
    </div>
    <a href="track7-thermal-fault-tolerance/" class="noc-track-link">进入模块七 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第八模块</span>
      <div class="noc-track-title">三维片上网络 (3D-NoC) 与硅通孔</div>
      <div class="noc-track-desc">
        三维硅通孔（TSV）寄生参数、热机械应力禁放区（KOZ）、七端口 3D 交叉开关、垂直串行化传输与 3D 纵向热沉陷抑制技术。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 7端口三维交叉开关 RTL • TSV 泰坦仿真器
      </div>
    </div>
    <a href="track8-3d-noc-tsvs/" class="noc-track-link">进入模块八 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第九模块</span>
      <div class="noc-track-title">多芯粒先进互连与 UCIe 规范</div>
      <div class="noc-track-desc">
        2.5D 先进封装（CoWoS/EMIB）、负二项良率经济学、UCIe 标准物理与 D2D 适配层、跨芯粒 In/Outbound Swap 死锁回溯恢复与多芯粒旁路机制。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • In/Outbound Swap RTL • 芯粒大亨实验室
      </div>
    </div>
    <a href="track9-chiplets-ucie/" class="noc-track-link">进入模块九 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第十模块</span>
      <div class="noc-track-title">光子与无线片上网络前沿</div>
      <div class="noc-track-desc">
        硅基纳米光子微环谐振腔（MRR）、波长路由光互连（WRONoC）、激光器电源门控与闭环 APC 热微调控、毫米波/太赫兹片上无线互连。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 光子微环开关 RTL • 光子领航员与无线电波
      </div>
    </div>
    <a href="track10-optical-wireless/" class="noc-track-link">进入模块十 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第十一模块</span>
      <div class="noc-track-title">硬件安全与零信任防御</div>
      <div class="noc-track-desc">
        片上威胁模型：窃听、欺骗与拒绝服务（DoS）。时间、缓存与物理热隐蔽信道。HeatSense 无乘法器 EWMA 热木马实时检测与硬件隔离区技术。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • HeatSense EWMA Verilog • 硅基哨兵街机
      </div>
    </div>
    <a href="track11-security/" class="noc-track-link">进入模块十一 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第十二模块</span>
      <div class="noc-track-title">大模型与类脑计算领域专用互连</div>
      <div class="noc-track-desc">
        大语言模型集合通信（AllReduce, AllGather）通信模式。网内归约路由器、超密晶圆级（Wafer-Scale）Ruche 织网与类脑脉冲（SNN）多播网络。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 网内归约 SystemVerilog • 变形泰坦加速实验室
      </div>
    </div>
    <a href="track12-ai-llm-snn/" class="noc-track-link">进入模块十二 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border-color: rgba(16, 185, 129, 0.3);">第十三模块 • 毕业设计</span>
      <div class="noc-track-title">毕业设计：经典芯片实测与全栈系统综合</div>
      <div class="noc-track-desc">
        精读经典芯片（英特尔 SCC 48核、英伟达 Simba 36芯粒、三维光互连、网内计算TVLSI），挑战终极毕业设计：零信任多芯粒 MoE 混合专家加速器全栈综合。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 5 节深度课时 • 完整 SystemVerilog SoC RTL • 网页 EDA 终端自动评分
      </div>
    </div>
    <a href="track13-capstone/" class="noc-track-link">进入第十三模块毕业设计 →</a>
  </div>"""

assert old_zh_tracks_block in zh_content, 'old_zh_tracks_block not found in index.zh.md'
zh_content = zh_content.replace(old_zh_tracks_block, new_zh_tracks_block)

zh_content = zh_content.replace(
    'B["体系化课程模块<br/>(模块 1–7)"]',
    'B["体系化课程模块<br/>(全13大模块)"]'
)

zh_content = zh_content.replace(
    '[第一模块：片上网络基础](track1-fundamentals/index.md)',
    '[第一模块：多核通信危机与物理线互连](track1-interconnect-crisis/index.md)'
)

with open('share/learning/docs/index.zh.md', 'w', encoding='utf-8') as f:
    f.write(zh_content)
print('Updated index.zh.md successfully!')
