# 🎮 交互式实验与街机仿真中心

<div class="noc-hero">
  <div class="noc-track-badge">✨ 17 款纯浏览器端微架构仿真器、迷你挑战与架构工具箱</div>
  <h1>片上网络交互式实验与街机挑战中心</h1>
  <p class="subtitle">
    通过 17 款即开即用的实时浏览器仿真实验与街机挑战，深入探索片上网络（NoC）的核心运转机制。实时观察数据包碰撞、动态平衡芯片热分布、绕过永久硅缺陷链路，并亲手设计先进 2.5D/3D 芯粒互连网络。
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">🔬 17 款交互式仿真器</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">⚡ 100% 纯前端 Canvas 与音效</span>
    <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">💾 对应可综合 Verilog RTL</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">🏆 本地与云端排行榜同步</span>
    <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #ec4899; border-color: rgba(236, 72, 153, 0.2);">📖 对齐教材全部十章内容</span>
  </div>
</div>

<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">17</span>
    <span class="noc-stat-label">交互式实验与挑战</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">5</span>
    <span class="noc-stat-label">大核心架构领域</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">0 ms</span>
    <span class="noc-stat-label">服务器延迟（零依赖免安装）</span>
  </div>
  <div class="noc-stat-card">
    <span class="noc-stat-number">100%</span>
    <span class="noc-stat-label">开源与可复现工程</span>
  </div>
</div>

---

## 🏛️ 分类实验目录

所有实验均严格对齐官方专著中的理论推导、可综合 SystemVerilog 电路与经典学术论文。

### 1. 路由器微架构与流控机制

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">物理互连 • 第1章</span>
      <h3>导线向导：物理互连与RC延迟仿真</h3>
      <p>仿真 180nm 至 3nm GAA 纳米级导线 RC 延迟缩放。插入 Bakoglu 最佳中继器，模拟铜电子散射电阻率激增，直观见证共享总线竞争崩溃。</p>
    </div>
    <a href="wire/" class="noc-track-link">启动导线向导 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">可视化器 • 第1章与第3章</span>
      <h3>二维网格路由仿真器</h3>
      <p>在 $N \times N$ 网格中注入合成流量（均匀随机、位取反、矩阵转置、热点分布），实时观察微片穿越输入缓存、路由计算及交叉开关的流水线全貌。</p>
    </div>
    <a href="visualizer/" class="noc-track-link">启动网格仿真器 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">交互式实验 • 第3章</span>
      <h3>仲裁竞技场：交叉开关调度挑战</h3>
      <p>在 $5 \times 5$ 交叉开关上调度并发数据包请求。在高竞争流量下横向对比严格优先级、轮询（Round-Robin）、矩阵仲裁器及 McKeown 的 iSLIP 迭代匹配算法。</p>
    </div>
    <a href="arbiter/" class="noc-track-link">进入仲裁竞技场 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">街机挑战 • 第2章</span>
      <h3>信用指挥官：流控与反压防御</h3>
      <p>管理上游信用令牌以抵御突发流量冲击。严防缓存溢出、消除信用耗尽气泡，并针对往返延迟优化最小缓存深度（$B_{\min} \ge \text{RTT}$）。</p>
    </div>
    <a href="credits/" class="noc-track-link">启动信用指挥官 →</a>
  </div>
</div>

---

### 2. 路由算法与死锁理论

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">动作街机 • 第5章</span>
      <h3>死锁大作战：死锁环与逃逸虚通道</h3>
      <p>在全网冻结前侦测循环缓存依赖！实时注入 Duato 逃逸通道，应用 Dally 转向模型，在不断升级的挑战波次中化解路由死锁。</p>
    </div>
    <a href="game/" class="noc-track-link">开始死锁大作战 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">逻辑解密 • 第4章与第5章</span>
      <h3>数据包路由解密挑战</h3>
      <p>引领微片列车穿越受限路由器。逐步攻克空间布局难题，规避队头阻塞（HoL），在满足转向禁止规则的同时实现最低跳步延时。</p>
    </div>
    <a href="puzzle/" class="noc-track-link">进入路由解密 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(59, 130, 246, 0.15); color: #1d4ed8; border-color: rgba(59, 130, 246, 0.3);">微架构 • 第6章</span>
      <h3>偏斜决斗：无缓存网络对决</h3>
      <p>通过热土豆偏斜路由（BLESS/CHIPPER）彻底消除输入缓存功耗。直观感受无缓存方案的面积收益与高负载下的活锁风险控制。</p>
    </div>
    <a href="deflection/" class="noc-track-link">进入偏斜决斗 →</a>
  </div>
</div>

---

### 3. 物理约束：热学建模、功耗与容错弹性

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.2);">热力物理 • 第7章</span>
      <h3>硅温保卫战：热管理游戏</h3>
      <p>实时求解瞬态热扩散方程（$C_{th} \frac{dT}{dt} + \frac{T - T_{amb}}{R_{th}} = P$）。综合调度动态调频调压（DVFS）、热节流与风扇冷却，严防硅片热失控（$T_{\max} \le 85^\circ\text{C}$）。</p>
    </div>
    <a href="hotspot/" class="noc-track-link">参加硅温保卫战 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">低功耗电路 • 第6章</span>
      <h3>电压旋涡：暗硅与动态电源门控</h3>
      <p>在热设计功耗（TDP）硬约束下精细调度多核电压频率岛（VFI）与睡眠管电源门控。最大化压降静态漏电，保障全网算力吞吐。</p>
    </div>
    <a href="power/" class="noc-track-link">启动电压旋涡 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(245, 158, 11, 0.1); color: #d97706; border-color: rgba(245, 158, 11, 0.2);">硅片可靠性 • 第7章</span>
      <h3>故障防御者：硅片韧性与BIST自测</h3>
      <p>模拟电迁移、TDDB 栅氧击穿及物理断线故障。调用 Vicman 旁路通道动态重构转发表，确保无死锁的故障自愈合。</p>
    </div>
    <a href="faults/" class="noc-track-link">启动故障防御者 →</a>
  </div>
</div>

---

### 4. 先进封装与高基数互连拓扑

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">三维集成 • 第8章</span>
      <h3>TSV泰坦：三维片上网络与热堆叠</h3>
      <p>在多层垂直硅层间构建三维硅通孔（TSV）网络。评估禁布区（KOZ）热机械应力开销，调度三维数据包，并利用导热 TSV 破解热堆叠陷阱。</p>
    </div>
    <a href="tsv3d/" class="noc-track-link">启动 TSV 泰坦 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">封装架构 • 第9章</span>
      <h3>芯粒大亨：先进封装设计挑战</h3>
      <p>在无源中介层、有源中介层及 3D TSV 垂直堆叠间设计下一代异构处理器。权衡晶圆良率（$Y$）、UCIe D2D 物理延迟与封装热梯度。</p>
    </div>
    <a href="chiplet/" class="noc-track-link">开启芯粒大亨 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(59, 130, 246, 0.1); color: #2563eb; border-color: rgba(59, 130, 246, 0.2);">图论拓扑 • 第4章</span>
      <h3>拓扑巨人：超算图互连架构师</h3>
      <p>构建高性能互连网络：2D Torus、超立方体、扁平蝴蝶、蜻蜓网络（Dragonfly）与极值图 Slim Fly。在引脚受限下优化网络直径与对分带宽。</p>
    </div>
    <a href="topology/" class="noc-track-link">构建互连拓扑 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">缓存一致性 • 第5章</span>
      <h3>服务质量角斗士：混合关键级流量调度</h3>
      <p>消除共享内存多处理器中的协议死锁。将请求、转发与响应报文物理隔离在不同虚网络（VNET）中，严格执行服务等级协议（SLA）。</p>
    </div>
    <a href="qos/" class="noc-track-link">进入角斗士竞技场 →</a>
  </div>
</div>

---

### 5. 前沿探索：光子、无线与类脑计算

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #db2777; border-color: rgba(236, 72, 153, 0.2);">纳米光子学 • 第10章</span>
      <h3>光子领航员：光互连网络</h3>
      <p>在硅基微环谐振腔（MRR）与波分复用（WDM）波导中引导光信号。动态校准温度漂移（$0.1\text{ nm}/^\circ\text{C}$），均衡插损与激光能耗。</p>
    </div>
    <a href="optical/" class="noc-track-link">开启光子领航 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(14, 165, 233, 0.1); color: #0284c7; border-color: rgba(14, 165, 233, 0.2);">太赫兹射频 • 第10章</span>
      <h3>无线电波：毫米波与太赫兹片上无线网</h3>
      <p>部署 60 GHz 与 140 GHz 片上无线收发机。利用单周期全片广播机制加速缓存一致性失效与栅障同步，跨越长距离物理布线延迟瓶颈。</p>
    </div>
    <a href="wireless/" class="noc-track-link">发射无线信号 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(168, 85, 247, 0.1); color: #7e22ce; border-color: rgba(168, 85, 247, 0.2);">神经拟态芯片 • 第7模块</span>
      <h3>类脑联结：脉冲神经网络片上互连</h3>
      <p>为脉冲神经网络（SNN）路由地址事件表示（AER）脉冲数据包。测量组播扇出、脉冲抖动与突触互连路由能效。</p>
    </div>
    <a href="neuromorphic/" class="noc-track-link">联结脉冲互连 →</a>
  </div>
</div>

---

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 20px 24px; margin-top: 2rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
      <span>🎯 准备好接受架构师认证了吗？</span>
    </div>
    <div style="font-size: 0.9rem; color: #cbd5e1; margin-top: 4px; max-width: 650px;">
      参加三阶综合认证考试，检验您的片上网络理论功底与工程实践，或在公开排行榜中查看经典基准得分。
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="../quiz/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>开始架构认证考核 →</span>
    </a>
    <a href="../leaderboard/" style="display: inline-flex; align-items: center; gap: 6px; background: #0284c7; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>查看荣誉排行榜 →</span>
    </a>
  </div>
</div>
