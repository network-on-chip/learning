# 📚 系统化课程模块：全 13 大教学模块

<div class="noc-hero">
  <div class="noc-track-badge">✨ 官方完整课程大纲 • 全 13 大模块 • 53 节深度课时</div>
  <h1>片上网络与先进互连系统全栈课程体系</h1>
  <p class="subtitle">
    1:1 严格对齐官方专著全 12 大核心章节，并以全栈“毕业设计：零信任多芯粒 MoE 混合专家加速器综合”为终极实战。专为计算机体系结构方向本科生、硕博研究生及芯片研发工程师打造。
  </p>
  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
    <span class="noc-track-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; border-color: rgba(37, 99, 235, 0.2);">📖 12 大核心教材章节</span>
    <span class="noc-track-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.2);">🏆 13 大进阶学习模块</span>
    <span class="noc-track-badge" style="background: rgba(147, 51, 234, 0.1); color: #9333ea; border-color: rgba(147, 51, 234, 0.2);">⚡ 53 节理论与实训课时</span>
    <span class="noc-track-badge" style="background: rgba(234, 88, 12, 0.1); color: #ea580c; border-color: rgba(234, 88, 12, 0.2);">💻 可综合 SystemVerilog RTL</span>
  </div>
</div>

<div class="noc-book-banner" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.25), rgba(15, 23, 42, 0.45)); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 10px; padding: 18px 22px; margin: 24px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
  <div>
    <div style="font-weight: 700; color: #60a5fa; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
      <span>📘 理论与芯片物理实现 1:1 严格对齐</span>
    </div>
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px; max-width: 800px; line-height: 1.5;">
      每一个课程模块均直接映射至教材中的对应章节。每节课均包含严格的数学推导、Nangate45 验证的可综合 SystemVerilog 硬件内核，以及基于浏览器的免安装零服务器 EDA 仿真验证环境。
    </div>
  </div>
  <a href="../textbook/" style="display: inline-flex; align-items: center; gap: 6px; background: #2563eb; color: #ffffff; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 0.85rem; text-decoration: none;">
    <span>阅读全十二章官方开源教材 →</span>
  </a>
</div>

---

## 🗺️ 全课程体系结构全景图

全 13 大模块构筑了从底层微米/纳米导线物理到晶圆级大模型集合通信加速器的完整知识链条：

```mermaid
graph TD
  subgraph Tier1["第一层次：物理层与数据链路层基础"]
    T1["第一模块：多核通信危机与物理线互连<br/>(Elmore RC延迟、中继器插入)"]
    T2["第二模块：交换技术、流控与缓存管理<br/>(虫洞交换、信用回路、AXI接口)"]
    T1 --> T2
  end

  subgraph Tier2["第二层次：路由器微架构与互连拓扑"]
    T3["第三模块：路由器微架构与仲裁调度<br/>(五级流水线、SMART多跳旁路)"]
    T4["第四模块：直接/间接与高基数互连拓扑<br/>(Mesh, Torus, Dragonfly, Clos)"]
    T2 --> T3
    T3 --> T4
  end

  subgraph Tier3["第三层次：死锁理论与物理约束管理"]
    T5["第五模块：死锁理论、转向模型与自适应路由<br/>(转向模型、CDG无环证明、Duato定理)"]
    T6["第六模块：低功耗架构与暗硅动态管理<br/>(多电压频率岛、电源门控、L*di/dt)"]
    T7["第七模块：热学建模、热点防御与容错弹性<br/>(RC紧凑热网、RCA拥塞、ML热点预测)"]
    T4 --> T5
    T5 --> T6
    T6 --> T7
  end

  subgraph Tier4["第四层次：先进封装与三维片上集成"]
    T8["第八模块：三维片上网络 (3D-NoC) 与硅通孔<br/>(TSV寄生参数、KOZ应力区、7端口开关)"]
    T9["第九模块：多芯粒先进互连与 UCIe 规范<br/>(2.5D良率模型、UCIe协议栈、In/Outbound回溯)"]
    T7 --> T8
    T8 --> T9
  end

  subgraph Tier5["第五层次：新兴前沿技术与毕业设计综合"]
    T10["第十模块：光子与无线片上网络前沿<br/>(微环谐振腔、WRONoC、激光APC微调)"]
    T11["第十一模块：硬件安全与零信任防御<br/>(隐蔽信道、HeatSense热木马检测、硅隔离区)"]
    T12["第十二模块：大模型与类脑计算领域专用互连<br/>(AllReduce归约路由器、Ruche、脉冲多播)"]
    T13["第十三模块：毕业设计：经典芯片实测与全栈系统综合<br/>(Intel SCC、Simba、3D光电、零信任MoE)"]
    T9 --> T10
    T10 --> T11
    T11 --> T12
    T12 --> T13
  end
```

---

## 📚 全 13 大教学模块清单

<div class="noc-tracks-grid">

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第一模块 • 对齐教材第一章</span>
      <div class="noc-track-title">多核通信危机与物理线互连</div>
      <div class="noc-track-desc">
        共享总线退役背后的物理根源。导线缩放效应、Elmore RC 延迟建模、最优中继器（Repeater）插入算法及片上能耗-延迟极限推导。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 可综合 Elmore Verilog • 导线物理仿真器
      </div>
    </div>
    <a href="../track1-interconnect-crisis/" class="noc-track-link">进入第一模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第二模块 • 对齐教材第二章</span>
      <div class="noc-track-title">交换技术、流控与缓存管理</div>
      <div class="noc-track-desc">
        数据包（Packet）、微元（Flit）与物理单元（Phit）。存储转发、虚拟直通与虫洞交换（Wormhole）对比，信用（Credit）回路与 AXI 网络接口。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 信用计数器 RTL • 信用指挥官仿真器
      </div>
    </div>
    <a href="../track2-switching-flow-control/" class="noc-track-link">进入第二模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第三模块 • 对齐教材第三章</span>
      <div class="noc-track-title">路由器微架构与仲裁调度</div>
      <div class="noc-track-desc">
        经典五级流水线路由器（BW-RC-VA-SA-ST）、虚通道（Virtual Channel）组织、亚 200ps 矩阵仲裁器与 SMART 单周期多跳旁路路由。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 五级流水线 SystemVerilog • 仲裁竞技场
      </div>
    </div>
    <a href="../track3-router-microarchitecture/" class="noc-track-link">进入第三模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第四模块 • 对齐教材第四章</span>
      <div class="noc-track-title">直接/间接与高基数互连拓扑</div>
      <div class="noc-track-desc">
        直接拓扑（Mesh, Torus）、间接集中拓扑（Clos, Fat-Tree, cMesh）与高基数超算互连（Dragonfly, 扁平蝶式）。深入推导 $T_0$、$\Theta_{sat}$ 与 UGAL 路由。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 拓扑图指标 RTL • 交互式拓扑架构师
      </div>
    </div>
    <a href="../track4-topologies-and-metrics/" class="noc-track-link">进入第四模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第五模块 • 对齐教材第五章</span>
      <div class="noc-track-title">死锁理论、转向模型与自适应路由</div>
      <div class="noc-track-desc">
        确定性 XY 路由、转向模型（西向优先、北向最后、奇偶路由）、杜阿托（Duato）逃逸信道定理、信道依赖图（CDG）证明与缓存一致性 VNET 隔离。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • SMT CDG 形式化验证器 • 死锁大作战街机
      </div>
    </div>
    <a href="../track5-routing-deadlock/" class="noc-track-link">进入第五模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第六模块 • 对齐教材第六章</span>
      <div class="noc-track-title">低功耗架构与暗硅动态管理</div>
      <div class="noc-track-desc">
        暗硅物理极限、热设计功耗（TDP）、多电压频率岛（V/F 岛）、路由器微架构电源门控、唤醒状态机与电感性 $L\cdot di/dt$ 电压突降防护。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 电源门控 FSM RTL • 电压旋涡仿真器
      </div>
    </div>
    <a href="../track6-low-power-dark-silicon/" class="noc-track-link">进入第六模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第七模块 • 对齐教材第七章</span>
      <div class="noc-track-title">热学建模、热点防御与容错弹性</div>
      <div class="noc-track-desc">
        傅里叶热扩散定律、RC 紧凑热网、区域拥塞感知（RCA）、源端限流压制、机器学习热点预测与非高斯噪声下稀疏传感器重构。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 热偏斜 Verilog RTL • 硅温保卫战与故障防御
      </div>
    </div>
    <a href="../track7-thermal-fault-tolerance/" class="noc-track-link">进入第七模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第八模块 • 对齐教材第八章</span>
      <div class="noc-track-title">三维片上网络 (3D-NoC) 与硅通孔</div>
      <div class="noc-track-desc">
        三维硅通孔（TSV）寄生参数、热机械应力禁放区（KOZ）、七端口 3D 交叉开关、垂直串行化传输与 3D 纵向热沉陷抑制技术。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 7端口三维交叉开关 RTL • TSV 泰坦仿真器
      </div>
    </div>
    <a href="../track8-3d-noc-tsvs/" class="noc-track-link">进入第八模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第九模块 • 对齐教材第九章</span>
      <div class="noc-track-title">多芯粒先进互连与 UCIe 规范</div>
      <div class="noc-track-desc">
        2.5D 先进封装（CoWoS/EMIB）、负二项良率经济学、UCIe 标准物理与 D2D 适配层、跨芯粒 In/Outbound Swap 死锁回溯恢复与多芯粒旁路机制。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • In/Outbound Swap RTL • 芯粒大亨实验室
      </div>
    </div>
    <a href="../track9-chiplets-ucie/" class="noc-track-link">进入第九模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第十模块 • 对齐教材第十章</span>
      <div class="noc-track-title">光子与无线片上网络前沿</div>
      <div class="noc-track-desc">
        硅基纳米光子微环谐振腔（MRR）、波长路由光互连（WRONoC）、激光器电源门控与闭环 APC 热微调控、毫米波/太赫兹片上无线互连。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 光子微环开关 RTL • 光子领航员与无线电波
      </div>
    </div>
    <a href="../track10-optical-wireless/" class="noc-track-link">进入第十模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第十一模块 • 对齐教材第十一章</span>
      <div class="noc-track-title">硬件安全与零信任防御</div>
      <div class="noc-track-desc">
        片上威胁模型：窃听、欺骗与拒绝服务（DoS）。时间、缓存与物理热隐蔽信道。HeatSense 无乘法器 EWMA 热木马实时检测与硬件隔离区技术。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • HeatSense EWMA Verilog • 硅基哨兵街机
      </div>
    </div>
    <a href="../track11-security/" class="noc-track-link">进入第十一模块 →</a>
  </div>

  <div class="noc-track-card">
    <div>
      <span class="noc-track-badge">第十二模块 • 对齐教材第十二章</span>
      <div class="noc-track-title">大模型与类脑计算领域专用互连</div>
      <div class="noc-track-desc">
        大语言模型集合通信（AllReduce, AllGather）通信模式。网内归约路由器、超密晶圆级（Wafer-Scale）Ruche 织网与类脑脉冲（SNN）多播网络。
      </div>
      <div style="font-size:0.8rem; color:var(--noc-text-muted); margin-top:0.35rem;">
        ⚡ 4 节深度课时 • 网内归约 SystemVerilog • 变形泰坦加速实验室
      </div>
    </div>
    <a href="../track12-ai-llm-snn/" class="noc-track-link">进入第十二模块 →</a>
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
    <a href="../track13-capstone/" class="noc-track-link">进入第十三模块毕业设计 →</a>
  </div>

</div>

---

## 💻 网页端 EDA 仿真验证终端

全 13 大教学模块中配套的 SystemVerilog 硬件代码与测试激励，均可直接在网页内置的 Unix EDA 终端中一键编译与仿真验证：

👉 **[启动网页 EDA Unix 终端与交互式仿真器](../interactive/terminal/)**
