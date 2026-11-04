<div class="noc-hero">
  <div class="noc-track-badge">✨ 开源片上网络学术体系与实验平台</div>
  <h1>片上网络学习与研究中心</h1>
  <p class="subtitle">
    连接理论体系、硅基微架构与可复现工程的交互式片上网络（Network-on-Chip, NoC）学习平台。基于 541 篇 IEEE 顶刊论文与端到端硬件仿真基准构建。
  </p>
    <a href="track1-fundamentals/" class="noc-sim-btn" style="text-decoration: none;">🚀 开始学习</a>
    <a href="quiz/" class="noc-sim-btn" style="text-decoration: none; background: #0284c7;">🎯 芯片架构认证考核</a>
    <a href="interactive/game/" class="noc-sim-btn" style="text-decoration: none; background: #ea580c;">👾 死锁大作战游戏</a>
    <a href="interactive/puzzle/" class="noc-sim-btn" style="text-decoration: none; background: #8b5cf6;">🧩 路由解密挑战</a>
    <a href="interactive/visualizer/" class="noc-sim-btn secondary" style="text-decoration: none;">🎮 启动二维网格仿真器</a>
    <a href="leaderboard/" class="noc-sim-btn secondary" style="text-decoration: none;">🏆 荣誉排行榜</a>
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
        ⚡ 包含 4 大交互式仿真器与高基数权衡分析仪
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
        ⚡ 包含 4 大交互式仿真器与前瞻路由 Verilog RTL
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
        ⚡ 包含 4 大交互式仿真器与实验室机器学习模型
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
        ⚡ 包含 4 大交互式仿真器与 UCIe 权衡分析引擎
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
        ⚡ 包含 4 大真实芯片仿真器与 541 篇顶刊库溯源
      </div>
    </div>
    <a href="track7-paper-walkthroughs/" class="noc-track-link">进入模块七 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(234, 88, 12, 0.1); color:#ea580c; border-color:rgba(234, 88, 12, 0.2);">街机游戏</span>
      <div class="noc-track-title">死锁大作战挑战</div>
      <div class="noc-track-desc">
        在高并发流量潮汐下担任芯片路由器仲裁者！基于杜阿托定理（Duato's Theorem）激活逃逸虚通道，在时钟冻结与过热熔毁前化解环形死锁！
      </div>
    </div>
    <a href="interactive/game/" class="noc-track-link">进入死锁大作战 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(139, 92, 246, 0.1); color:#8b5cf6; border-color:rgba(139, 92, 246, 0.2);">架构解密</span>
      <div class="noc-track-title">数据包路由解密挑战</div>
      <div class="noc-track-desc">
        配置路由器转向偏好、规避介质击穿故障节点、化解交叉开关端口竞争，在限定周期内引导多色彩数据微元无碰撞送达！
      </div>
    </div>
    <a href="interactive/puzzle/" class="noc-track-link">进入路由解密挑战 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(239, 68, 68, 0.1); color:#ef4444; border-color:rgba(239, 68, 68, 0.2);">热管理街机</span>
      <div class="noc-track-title">硅温保卫战挑战</div>
      <div class="noc-track-desc">
        控制动态电压频率调节（DVFS）、迁移沸腾算力负载、释放微流控低温脉冲，在热失控熔毁前守住硅片安全温区！
      </div>
    </div>
    <a href="interactive/hotspot/" class="noc-track-link">进入硅温保卫战 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(16, 185, 129, 0.1); color:#10b981; border-color:rgba(16, 185, 129, 0.2);">封装大亨</span>
      <div class="noc-track-title">芯粒先进封装设计挑战</div>
      <div class="noc-track-desc">
        基于 UCIe 与 3D TSV 在硅中介层上组装异构多芯粒超算芯片，权衡对分带宽、互连延迟、良率经济学与封装总成本！
      </div>
    </div>
    <a href="interactive/chiplet/" class="noc-track-link">进入芯粒封装挑战 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">交互式仿真</span>
      <div class="noc-track-title">二维网格路由仿真器</div>
      <div class="noc-track-desc">
        在浏览器中动态观察数据包生成、微元逐跳转发、虚通道仲裁与拥塞排队，实时对比 XY 维序路由与自适应转向模型的流动行为。
      </div>
    </div>
    <a href="interactive/visualizer/" class="noc-track-link">启动仿真器 →</a>
  </div>
</div>
