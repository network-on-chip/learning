<div class="noc-hero">
  <div class="noc-track-badge">✨ 开源片上网络学术体系与实验平台</div>
  <h1>片上网络学习与研究中心</h1>
  <p class="subtitle">
    连接理论体系、硅基微架构与可复现工程的交互式片上网络（Network-on-Chip, NoC）学习平台。基于 541 篇 IEEE 顶刊论文与端到端硬件仿真基准构建。
  </p>
  <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
    <a href="track1-fundamentals/" class="noc-sim-btn" style="text-decoration: none;">🚀 开始学习</a>
    <a href="interactive/visualizer.md" class="noc-sim-btn secondary" style="text-decoration: none;">🎮 启动二维网格仿真器</a>
    <a href="https://network-on-chip.github.io/.github/" target="_blank" class="noc-sim-btn secondary" style="text-decoration: none;">🗺️ 交互式论文地图</a>
  </div>
</div>

<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">541</span>
    <span class="noc-stat-label">精选 IEEE 顶刊论文</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">37,400+</span>
    <span class="noc-stat-label">高精图表与架构图</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">7</span>
    <span class="noc-stat-label">进阶学习模块</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">100%</span>
    <span class="noc-stat-label">开源与可复现基准</span>
  </div>
</div>

---

## 📚 课程模块导航

面向本科生、研究生、芯片架构师及硬件工程师量身打造的系统性进阶路径：

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第一模块</span>
      <div class="noc-track-title">片上互连基础</div>
      <div class="noc-track-desc">
        从共享总线瓶颈到片上网络架构。数据包（Packet）、微元（Flit）与物理传输单元（Phit）。存储转发、虚拟直通与虫洞交换（Wormhole）及基于信用（Credit）的流控机制。
      </div>
    </div>
    <a href="track1-fundamentals/" class="noc-track-link">进入模块一 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第二模块</span>
      <div class="noc-track-title">路由器微架构</div>
      <div class="noc-track-desc">
        标准五级流水线路由器（BW-RC-VA-SA-ST）、单周期前瞻投机路由器、虚通道（Virtual Channel）分配、矩阵仲裁器与交叉开关（Crossbar Switch）微架构设计。
      </div>
    </div>
    <a href="track2-router-architecture/" class="noc-track-link">进入模块二 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第三模块</span>
      <div class="noc-track-title">拓扑结构与评估指标</div>
      <div class="noc-track-desc">
        直接拓扑（Mesh, Torus, 折叠环）与间接拓扑（Clos, Butterfly, Fat-Tree）。网络直径、零负载延迟、对分带宽（Bisection Bandwidth）以及聚集网格（cMesh）理论分析。
      </div>
    </div>
    <a href="track3-topologies/" class="noc-track-link">进入模块三 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第四模块</span>
      <div class="noc-track-title">路由算法与死锁避免</div>
      <div class="noc-track-desc">
        确定性维序路由（XY 路由）、转向模型（西向优先、北向最后）、奇偶路由算法，以及基于信道依赖图（CDG）与杜阿托定理（Duato's Theorem）的形式化无死锁证明。
      </div>
    </div>
    <a href="track4-routing-deadlock/" class="noc-track-link">进入模块四 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第五模块</span>
      <div class="noc-track-title">热管理与拥塞控制</div>
      <div class="noc-track-desc">
        空间温度梯度、动态热管理（DTM）、基于机器学习的热点预测控制，以及在高斯与非高斯噪声下的最佳温度传感器布局与重建算法（直接源自实际复现工程）。
      </div>
    </div>
    <a href="track5-congestion-thermal/" class="noc-track-link">进入模块五 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第六模块</span>
      <div class="noc-track-title">芯粒与三维片上网络</div>
      <div class="noc-track-desc">
        多芯片集成（UCIe, BoW 接口标准）、三维硅通孔（TSV）片上网络架构、光互连片上网络（ONoC）与无线射频片上网络（WNoC）前沿探索。
      </div>
    </div>
    <a href="track6-chiplets-and-3d/" class="noc-track-link">进入模块六 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第七模块</span>
      <div class="noc-track-title">经典论文深度精读</div>
      <div class="noc-track-desc">
        通俗易懂的顶刊论文精读手册。紧扣 541 篇经过细致标注与消歧的 IEEE TCAD, TVLSI, JSSC 经典文献，图文并茂剖析体系结构创新点。
      </div>
    </div>
    <a href="track7-paper-walkthroughs/" class="noc-track-link">进入模块七 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">交互式仿真</span>
      <div class="noc-track-title">二维网格路由仿真器</div>
      <div class="noc-track-desc">
        在浏览器中动态观察数据包生成、微元逐跳转发、虚通道仲裁与拥塞排队，实时对比 XY 维序路由与自适应转向模型的流动行为。
      </div>
    </div>
    <a href="interactive/visualizer.md" class="noc-track-link">启动仿真器 →</a>
  </div>
</div>
