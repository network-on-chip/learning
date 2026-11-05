<div class="noc-hero">
  <div class="noc-track-badge">✨ 开源片上网络学术体系与实验平台</div>
  <h1>片上网络学习与研究中心</h1>
  <p class="subtitle">
    连接理论体系、硅基微架构与可复现工程的交互式片上网络（Network-on-Chip, NoC）学习平台。基于 542 篇精选顶刊论文、10 章官方教材与端到端硬件仿真基准构建。
  </p>
  <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
    <a href="textbook/" class="noc-sim-btn" style="text-decoration: none; background: #2563eb;">📖 阅读官方教材 (全十章)</a>
    <a href="assets/book.pdf" target="_blank" class="noc-sim-btn" style="text-decoration: none; background: #0284c7;">📥 下载教材 PDF (132页)</a>
    <a href="track1-fundamentals/" class="noc-sim-btn secondary" style="text-decoration: none;">🚀 开始系统学习</a>
    <a href="quiz/" class="noc-sim-btn secondary" style="text-decoration: none;">🎯 架构认证考核</a>
    <a href="interactive/game/" class="noc-sim-btn" style="text-decoration: none; background: #ea580c;">👾 死锁大作战</a>
    <a href="interactive/visualizer/" class="noc-sim-btn secondary" style="text-decoration: none;">🎮 二维网格仿真器</a>
    <a href="leaderboard/" class="noc-sim-btn secondary" style="text-decoration: none;">🏆 荣誉排行榜</a>
  </div>
</div>

<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">10</span>
    <span class="noc-stat-label">教材核心章节</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">542+</span>
    <span class="noc-stat-label">精选 IEEE 顶刊论文</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">15</span>
    <span class="noc-stat-label">交互式实验与游戏</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">100%</span>
    <span class="noc-stat-label">开源与可复现基准</span>
  </div>
</div>

---

## 📖 官方开源教材 (全十章)

探索《片上网络与先进互连：架构、协同设计与前沿探索》（*Network-on-Chip and Advanced Interconnects*），全书涵盖五大部分共十章，专为从中学生到芯片科研人员打造的高可读性教材：

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.35), rgba(15, 23, 42, 0.65)); border: 1px solid rgba(59, 130, 246, 0.5); border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #93c5fd; font-size: 1.15rem; display: flex; align-items: center; gap: 8px;">
      <span>📘 完整出版排版 PDF 现已开放下载</span>
    </div>
    <div style="font-size: 0.92rem; color: #e2e8f0; margin-top: 6px; max-width: 800px; line-height: 1.5;">
      采用施普林格·自然（Springer Nature）<code>svmono</code> 专著版式编译（共 132 页），系统涵盖线物理延时、路由器微架构、高基数拓扑、转向模型死锁证明、暗硅低功耗、热敏建模、3D 硅通孔、UCIe 芯粒互连与纳米光子学。
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="textbook/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>在线阅读教材 →</span>
    </a>
    <a href="assets/book.pdf" target="_blank" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>下载 PDF 电子书 (132页) ↓</span>
    </a>
  </div>
</div>

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">第一部分 • 第1章</span>
      <div class="noc-track-title">多核通信危机与物理线互连</div>
      <div class="noc-track-desc">
        共享总线为何失效？登纳德缩放定律破灭、量子隧穿、Elmore RC 导线延时、铜晶界散射及最佳中继器插入。
      </div>
    </div>
    <a href="textbook/ch01-interconnect-crisis/" class="noc-track-link">阅读第 1 章 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">第一部分 • 第2章</span>
      <div class="noc-track-title">交换技术、流控与缓存管理</div>
      <div class="noc-track-desc">
        虫洞交换 vs 虚拟直通、微元分片、信用往返延迟回路 ($RTT$)、虚拟通道线头阻塞消除与 AXI4 网络接口打包。
      </div>
    </div>
    <a href="textbook/ch02-switching-flow-control/" class="noc-track-link">阅读第 2 章 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">第一部分 • 第3章</span>
      <div class="noc-track-title">路由器微架构与仲裁调度</div>
      <div class="noc-track-desc">
        经典四级流水线、投机并行分配、矩阵仲裁器（亚 200 皮秒 LRU）、波前仲裁器与 SMART 单周期多跳旁路。
      </div>
    </div>
    <a href="textbook/ch03-router-microarchitecture/" class="noc-track-link">阅读第 3 章 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">第二部分 • 第4章</span>
      <div class="noc-track-title">直接/间接与高基数互连拓扑</div>
      <div class="noc-track-desc">
        图论互连评估、2D Mesh、Torus 环网、折叠环、cMesh、Clos 网络、Fat-Tree 胖树与 Dragonfly 蜻蜓拓扑。
      </div>
    </div>
    <a href="textbook/ch04-topologies-and-metrics/" class="noc-track-link">阅读第 4 章 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">第二部分 • 第5章</span>
      <div class="noc-track-title">死锁理论、转向模型与路由</div>
      <div class="noc-track-desc">
        通道依赖图（CDG）、Dally-Seitz 定理、Glass-Ni 转向模型、Odd-Even 奇偶路由、Duato 逃逸通道与一致性死锁消除。
      </div>
    </div>
    <a href="textbook/ch05-routing-deadlock-theory/" class="noc-track-link">阅读第 5 章 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">第三部分 • 第6章</span>
      <div class="noc-track-title">低功耗架构与暗硅动态管理</div>
      <div class="noc-track-desc">
        动态翻转功耗、亚阈值漏电、暗硅热预算约束（$>20\%$ 关断面积）、电压频率岛（VFI）与前瞻电源门控机制。
      </div>
    </div>
    <a href="textbook/ch06-low-power-dark-silicon/" class="noc-track-link">阅读第 6 章 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">第三部分 • 第7章</span>
      <div class="noc-track-title">热学建模、热点防御与容错弹性</div>
      <div class="noc-track-desc">
        傅里叶热传导方程、紧凑 RC 阶梯热模型（HotSpot）、热敏节流、高斯和滤波（GSF）传感器重建与硬件旁路容错。
      </div>
    </div>
    <a href="textbook/ch07-thermal-fault-tolerance/" class="noc-track-link">阅读第 7 章 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">第四部分 • 第8章</span>
      <div class="noc-track-title">三维片上网络 (3D-NoC) 与硅通孔</div>
      <div class="noc-track-desc">
        垂直 TSV 缩放物理、寄生电容、禁布区（KOZ）、7 端口 3D 交叉开关、无仲裁垂直快速通道与层间热堆叠管理。
      </div>
    </div>
    <a href="textbook/ch08-3d-noc-tsvs/" class="noc-track-link">阅读第 8 章 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">第四部分 • 第9章</span>
      <div class="noc-track-title">多芯粒先进互连与 UCIe 接口规范</div>
      <div class="noc-track-desc">
        光刻掩模版极限、墨菲良率模型（大比萨难题）、2.5D 中介层（CoWoS/EMIB）、UCIe 三层架构与出入境置换死锁恢复。
      </div>
    </div>
    <a href="textbook/ch09-chiplets-ucie/" class="noc-track-link">阅读第 9 章 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #ec4899; border-color: rgba(236, 72, 153, 0.2);">第五部分 • 第10章</span>
      <div class="noc-track-title">光子与无线片上网络前沿技术</div>
      <div class="noc-track-desc">
        硅基纳米光子学、微环谐振腔（MRR）、PSE/CSE 光开关、热光漂移（$0.10\text{ nm/}^\circ\text{C}$）与 60 GHz 片上无线收发器。
      </div>
    </div>
    <a href="textbook/ch10-optical-wireless/" class="noc-track-link">阅读第 10 章 →</a>
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
      <span class="noc-track-badge" style="background:rgba(234, 88, 12, 0.1); color:#ea580c; border-color:rgba(234, 88, 12, 0.2);">微架构竞技</span>
      <div class="noc-track-title">仲裁竞技场：交叉开关挑战</div>
      <div class="noc-track-desc">
        在时钟周期级别实时仲裁 5×5 交叉开关！利用虚通道（VC）化解队头阻塞（HOL Blocking），部署 iSLIP 调度抵御队列溢出！
      </div>
    </div>
    <a href="interactive/arbiter/" class="noc-track-link">进入仲裁竞技场 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(59, 130, 246, 0.1); color:#3b82f6; border-color:rgba(59, 130, 246, 0.2);">图拓扑架构</span>
      <div class="noc-track-title">拓扑巨人：超算图架构师</div>
      <div class="noc-track-desc">
        亲手连线超算互连网络（超立方体、环形、蜻蜓 Dragonfly、胖树 Fat-Tree）！在引脚度数与线缆成本约束下压减网络直径与延迟！
      </div>
    </div>
    <a href="interactive/topology/" class="noc-track-link">进入拓扑巨人挑战 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(236, 72, 153, 0.1); color:#ec4899; border-color:rgba(236, 72, 153, 0.2);">硅基光子学</span>
      <div class="noc-track-title">光子领航员：光互连网络</div>
      <div class="noc-track-desc">
        在硅基光波导上调度多波长激光（WDM）！热调谐微环谐振腔（MRR），动态补偿热漂移，以光速完成低损耗全光交叉路由！
      </div>
    </div>
    <a href="interactive/optical/" class="noc-track-link">进入光子领航员 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(16, 185, 129, 0.1); color:#10b981; border-color:rgba(16, 185, 129, 0.2);">流控与反压</span>
      <div class="noc-track-title">信用指挥官：流控防御</div>
      <div class="noc-track-desc">
        驾驭飞行延迟（RTT）环境下的信用机制（Credit-Based Flow Control）！精细调优信用批量回传与阈值反压，捍卫零丢包传输！
      </div>
    </div>
    <a href="interactive/credits/" class="noc-track-link">进入信用指挥官 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(234, 179, 8, 0.1); color:#ca8a04; border-color:rgba(234, 179, 8, 0.2);">无缓存对决</span>
      <div class="noc-track-title">偏斜决斗：无缓存网络</div>
      <div class="noc-track-desc">
        彻底移除路由器输入缓存！调控热土豆偏斜路由，仲裁端口竞争冲突，释放黄金微元（Golden Flit）并阻断活锁死循环丢包！
      </div>
    </div>
    <a href="interactive/deflection/" class="noc-track-link">进入偏斜决斗 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(99, 102, 241, 0.1); color:#6366f1; border-color:rgba(99, 102, 241, 0.2);">硅片韧性</span>
      <div class="noc-track-title">故障防御者：BIST自测</div>
      <div class="noc-track-desc">
        抗击电迁移断路与高能粒子翻转！触发 BIST 雷达自测波束，构筑环形绕行容错环（Fault-Ring），激活冗余备份金属链路！
      </div>
    </div>
    <a href="interactive/faults/" class="noc-track-link">进入故障防御者 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(239, 68, 68, 0.1); color:#ef4444; border-color:rgba(239, 68, 68, 0.2);">服务质量</span>
      <div class="noc-track-title">服务质量角斗士：流量仲裁</div>
      <div class="noc-track-desc">
        在车载关键安全流与大吞吐 AI DMA 间精细调度！调优加权公平排队（WFQ），在微秒倒计时耗尽前激发抢占中断！
      </div>
    </div>
    <a href="interactive/qos/" class="noc-track-link">进入流量仲裁 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(2, 132, 199, 0.1); color:#0284c7; border-color:rgba(2, 132, 199, 0.2);">暗硅与电源</span>
      <div class="noc-track-title">电压旋涡：电源门控</div>
      <div class="noc-track-desc">
        对空闲路由器走廊实施休眠门控以削减漏电！驾驭唤醒延迟惩罚，触发瞬时电源轨浪涌，守卫芯片热设计功耗（TDP）红线！
      </div>
    </div>
    <a href="interactive/power/" class="noc-track-link">进入电压旋涡 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(14, 165, 233, 0.1); color:#0284c7; border-color:rgba(14, 165, 233, 0.2);">片上无线网</span>
      <div class="noc-track-title">无线电波：毫米波网络</div>
      <div class="noc-track-desc">
        在单时钟周期内穿越整片芯片！利用 60 GHz 毫米波微天线广播，调控 FDMA 频分信道并避免射频多址冲突！
      </div>
    </div>
    <a href="interactive/wireless/" class="noc-track-link">进入无线电波 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background:rgba(168, 85, 247, 0.1); color:#a855f7; border-color:rgba(168, 85, 247, 0.2);">类脑脉冲</span>
      <div class="noc-track-title">类脑联结：脉冲网络</div>
      <div class="noc-track-desc">
        编排事件驱动的生物动作电位（AER）！构建 1-to-N 硬件组播树，积分漏电膜电位（LIF），激发 STDP 突触可塑性！
      </div>
    </div>
    <a href="interactive/neuromorphic/" class="noc-track-link">进入类脑联结 →</a>
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

---

## 🔬 贯通理论、芯片与代码

本课程中的每一个核心概念，均与我们验证过的学术研究成果及复现工件严密配对：

```mermaid
graph LR
  A["理论与学术文献<br/>(541 篇 IEEE 经典论文)"] --> B["体系化课程模块<br/>(模块 1–7)"]
  B --> C["网页交互式实验<br/>(二维网格路由仿真器)"]
  B --> D["硬件开源实现<br/>(projects/ 下 Verilog & Python)"]
  D --> E["基准测试与芯片实测<br/>(热学、延迟与能效数据)"]
```

### 准备好开始了吗？
立即开启你的第一步：[第一模块：片上网络基础](track1-fundamentals/index.md)，或者前往体验 [交互式二维路由仿真器](interactive/visualizer.md)！

