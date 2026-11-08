# 🔬 片上网络交互式工程 CAD 与微架构仿真工作台

<div class="noc-hero">
  <div class="noc-track-badge">✨ 20 款工程级 EDA 仿真器、CAD 工具台与微架构分析套件</div>
  <h1>片上网络交互式实验与工程 CAD 工作台</h1>
  <p class="subtitle">
    通过 20 款基于现代浏览器原生运行的工程仿真实验与 Web EDA 环境，深入探究片上网络（NoC）的核心运转机制。求解分布参数 RLC 传输线方程、计算图拉普拉斯矩阵谱与 Fiedler 代数连通度、基于 Tarjan SCC 强连通分量验证通道依赖图（CDG）死锁、求解二维傅里叶瞬态热传导与暗硅电源门控，并基准评测千亿级大模型集体通信加速器。
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">🔬 20 款工程 CAD 工作台</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">⚡ 100% 纯前端 Canvas 与物理数学求解器</span>
    <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">💾 支持可综合 Verilog RTL 与 SPICE 网表导出</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">📐 形式化 SMT 证明与不变式验证</span>
    <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #ec4899; border-color: rgba(236, 72, 153, 0.2);">📖 严格对齐教材全部 12 章深度内容</span>
  </div>
</div>

<div class="noc-stats-grid">
  <div class="noc-stat-card">
    <span class="noc-stat-number">20</span>
    <span class="noc-stat-label">工程级仿真器</span>
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

## 🏛️ 分类实验与仿真目录

所有仿真工具均严格对齐官方专著中的理论推导、可综合 SystemVerilog 电路与经典学术论文。

### 1. 路由器微架构与流控机制

<div class="noc-tracks-grid">
  <div class="noc-track-card" style="border: 1px solid rgba(59, 130, 246, 0.45); background: linear-gradient(135deg, rgba(30, 58, 138, 0.12), rgba(15, 23, 42, 0.25));">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.15); color: #3b82f6; border-color: rgba(37, 99, 235, 0.3);">💻 网页虚拟 Bash 终端 • 覆盖全书各章</span>
      <h3>网页 EDA 终端与仿真验证工作台</h3>
      <p>面向片上网络体系结构研究的纯浏览器端命令行实验环境。直接运行 <code>run-sim</code> 离散事件仿真扫描、<code>verify-deadlock</code> 形式化 SMT 证明、Nangate45 <code>sta-timing</code> 静态时序分析，以及 TCAD '26 HeatSense 与 BuffeRS 复现基准测试。</p>
    </div>
    <a href="terminal/" class="noc-track-link" style="color: #60a5fa; font-weight: 700;">启动网页 EDA 终端 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">物理互连 • 第1章</span>
      <h3>纳米导线物理与中继器插入 CAD</h3>
      <p>仿真 180nm 至 3nm GAA 纳米级分布参数 RLC 传输线。插入 Bakoglu 最佳中继器，模拟铜电子表面散射与晶界散射电阻率激增，求解瞬态阶跃响应微分方程。</p>
    </div>
    <a href="wire/" class="noc-track-link">启动导线仿真器 →</a>
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
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">微架构 • 第3章</span>
      <h3>开关分配与交叉开关仲裁微架构仿真器</h3>
      <p>在 $5 \times 5$ 交叉开关上调度并发数据包请求。在高竞争流量下横向对比严格优先级、轮询（Round-Robin）、矩阵仲裁器及 McKeown 的 iSLIP 迭代匹配算法，验证 Karol 58.6% HOL 队头阻塞吞吐极限。</p>
    </div>
    <a href="arbiter/" class="noc-track-link">启动仲裁仿真器 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">流控理论 • 第2章</span>
      <h3>基于信用的流控与缓存尺寸规划 CAD</h3>
      <p>精确仿真信用闭环往返延迟（$B_{\min} = \lceil \text{RTT} \cdot \text{BW} \rceil$），渲染时空阶梯图（Space-Time Ladder Diagram），消除信用耗尽气泡，优化吞吐拐点。</p>
    </div>
    <a href="credits/" class="noc-track-link">启动信用流控仿真器 →</a>
  </div>
</div>

---

### 2. 路由算法与死锁理论

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">死锁形式化验证 • 第5章</span>
      <h3>死锁验证与 CDG 逃逸虚通道转换引擎</h3>
      <p>构建通道依赖图（CDG），利用 Tarjan 强连通分量算法实时探测循环等待死锁。验证 Dally &amp; Seitz 无环定理与 Duato 自适应逃逸虚通道恢复机制，导出 SMT-LIB2 验证断言。</p>
    </div>
    <a href="game/" class="noc-track-link">启动死锁验证引擎 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">路由优化 • 第4章与第5章</span>
      <h3>转向模型限制与无死锁路径优化 CAD</h3>
      <p>深入探索 Glass &amp; Ni 转向模型（西向先行、北向后行、负向先行）及邱氏（Chiu）奇偶空间变化转向模型。动态渲染合法路由锥体，在硅片缺陷阻断下自适应绕行。</p>
    </div>
    <a href="puzzle/" class="noc-track-link">启动转向模型优化器 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(59, 130, 246, 0.15); color: #1d4ed8; border-color: rgba(59, 130, 246, 0.3);">无缓存网络 • 第6章</span>
      <h3>无缓存偏斜路由（BLESS &amp; CHIPPER）仿真器</h3>
      <p>通过热土豆偏斜路由彻底消除输入缓存静态漏电。直观评估偏斜率曲线、基于最老优先（Oldest-First）年龄优先级的活锁避免保证与负载饱和拐点。</p>
    </div>
    <a href="deflection/" class="noc-track-link">启动偏斜路由仿真器 →</a>
  </div>
</div>

---

### 3. 物理约束：热学建模、功耗与容错弹性

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.2);">热力物理 • 第7章</span>
      <h3>硅片热传导与动态热管理（DTM）有限差分求解器</h3>
      <p>实时求解二维傅里叶瞬态热扩散方程（$C_{th} \frac{dT}{dt} + \frac{T - T_{amb}}{R_{th}} = P$）及亚阈值漏电正反馈热失控。部署闭环 PI-DVFS 调频与 TAAR 热感知路由。</p>
    </div>
    <a href="hotspot/" class="noc-track-link">启动热分析求解器 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">低功耗电路 • 第6章</span>
      <h3>暗硅物理与电源门控 CAD 工作台</h3>
      <p>量化登纳德缩放定律失效导致的利用率墙限制（$\chi \propto \theta^{-\alpha}$）。计算头管/脚管睡眠晶体管尺寸与浪涌冲击电流，导出统一功耗格式（UPF）规范。</p>
    </div>
    <a href="power/" class="noc-track-link">启动电源门控 CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(245, 158, 11, 0.1); color: #d97706; border-color: rgba(245, 158, 11, 0.2);">硅片可靠性 • 第7章</span>
      <h3>硅片容错与弹性路由 CAD 工作台</h3>
      <p>模拟电迁移、TDDB 击穿与链路永久断裂故障。执行 ZoneDefense 凸多边形周长绕行路由，评估随机失效率下的报文存活率曲线，生成 BIST 诊断报告。</p>
    </div>
    <a href="faults/" class="noc-track-link">启动容错仿真工作台 →</a>
  </div>
</div>

---

### 4. 先进封装与高基数互连拓扑

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);">三维集成 • 第8章</span>
      <h3>三维片上网络 TSV 热应力 CAD 分析器</h3>
      <p>求解 Lamé 径向与环向热机械应力张量方程，确定压阻效应载流子迁移率禁布区（KOZ），并建立包含散热伪 TSV 的 4 层垂直硅堆叠热传导模型。</p>
    </div>
    <a href="tsv3d/" class="noc-track-link">启动 TSV 应力 CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">先进封装 • 第9章</span>
      <h3>2.5D/3D 多芯粒先进封装 CAD 与良率优化器</h3>
      <p>基于 Murphy 缺陷模型计算多芯粒拆分良率优势，评估 UCIe D2D 物理延迟与岸线带宽密度，求解有源/无源中介层上的多芯片热耦合梯度。</p>
    </div>
    <a href="chiplet/" class="noc-track-link">启动芯粒优化器 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(59, 130, 246, 0.1); color: #2563eb; border-color: rgba(59, 130, 246, 0.2);">图论拓扑 • 第4章</span>
      <h3>互连拓扑 CAD 与谱图分析器</h3>
      <p>计算图拉普拉斯矩阵特征值谱，求解 Fiedler 向量代数连通度（$\lambda_2$）、精确对分带宽与网络直径，覆盖 2D Torus、超立方体与蜻蜓网络（Dragonfly）。</p>
    </div>
    <a href="topology/" class="noc-track-link">启动拓扑 CAD 分析器 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">缓存一致性 • 第5章</span>
      <h3>混合关键级多虚网络 QoS 与报文调度器</h3>
      <p>消除共享内存多处理器中的缓存一致性协议死锁。将请求、转发与响应报文物理隔离在独立虚网络（VNET）中，仿真加权公平排队（WFQ）与差额轮询（DRR）。</p>
    </div>
    <a href="qos/" class="noc-track-link">启动 QoS 调度仿真器 →</a>
  </div>
</div>

---

### 5. 前沿探索：光子、无线与类脑计算

<div class="noc-tracks-grid">
  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(236, 72, 153, 0.1); color: #db2777; border-color: rgba(236, 72, 153, 0.2);">纳米光子学 • 第10章</span>
      <h3>硅基光电与光片上网络（ONoC）波导 CAD</h3>
      <p>建立微环谐振腔（MRR）洛伦兹共振光谱模型，量化热光波长漂移（$0.1\text{ nm}/^\circ\text{C}$）与微加热器闭环补偿，分析级联插入损耗与误码率（BER）。</p>
    </div>
    <a href="optical/" class="noc-track-link">启动光网络 CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(14, 165, 233, 0.1); color: #0284c7; border-color: rgba(14, 165, 233, 0.2);">太赫兹射频 • 第10章</span>
      <h3>片上毫米波与太赫兹无线片上网络（WiNoC）仿真器</h3>
      <p>求解电导硅衬底中的 Friis 路径损耗与复介电常数衰减。建立混合网格-无线拓扑，利用单周期无线全片广播消除栅障同步长导线延迟。</p>
    </div>
    <a href="wireless/" class="noc-track-link">启动无线网络仿真器 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(168, 85, 247, 0.1); color: #7e22ce; border-color: rgba(168, 85, 247, 0.2);">神经拟态芯片 • 第12章</span>
      <h3>脉冲神经网络（SNN）组播与 AER 路由器仿真器</h3>
      <p>求解 Leaky Integrate-and-Fire（LIF）膜电位常微分方程，仿真地址事件表示（AER）树形组播，评测皮层阵列中的脉冲到达抖动与突触路由能效。</p>
    </div>
    <a href="neuromorphic/" class="noc-track-link">启动类脑仿真器 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(239, 68, 68, 0.1); color: #dc2626; border-color: rgba(239, 68, 68, 0.2);">硬件安全 • 第11章</span>
      <h3>片上网络硬件安全与威胁防御 CAD 工作台</h3>
      <p>通过香农熵异常检测识别隐蔽硬件木马，通过数据包注入随机抖动混淆防御 AES 定时侧信道泄露，并利用 PUF 硬件指纹认证拦截 DoS 缓冲区洪泛攻击。</p>
    </div>
    <a href="security/" class="noc-track-link">启动硬件安全 CAD →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge" style="background: rgba(139, 92, 246, 0.1); color: #9333ea; border-color: rgba(139, 92, 246, 0.2);">大模型计算加速 • 第12章</span>
      <h3>分布式大模型 AI 集体通信加速器与 3D 内存仿真器</h3>
      <p>仿真 Ring AllReduce 的 Scatter-Reduce 与 All-Gather 阶段微片流动，求解 Roofline 算力与内存带宽约束，分析 1F1B 流水线气泡，连接 >16 TB/s 垂直 3D HBM3e 内存堆栈。</p>
    </div>
    <a href="transformer/" class="noc-track-link">启动大模型集体通信仿真器 →</a>
  </div>
</div>

---

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 20px 24px; margin-top: 2rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
      <span>🎯 准备好检验您的芯片架构实力了吗？</span>
    </div>
    <div style="font-size: 0.9rem; color: #cbd5e1; margin-top: 4px; max-width: 650px;">
      参加包含 3 级梯度的 <strong>综合架构认证考核</strong>，全面评测您在物理互连、流控算法、热力学建模与 AI 大模型加速领域的专业知识储备。
    </div>
  </div>
  <div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="../quiz/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; text-decoration: none;">
      <span>开始认证考试 →</span>
    </a>
  </div>
</div>
