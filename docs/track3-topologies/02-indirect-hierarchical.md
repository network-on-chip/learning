# 3.2 Indirect & Concentrated Networks

While direct 2D meshes are standard for homogeneous multicore processors, heterogeneous AI accelerators and large-scale chiplets often require higher path diversity or lower hop latency. This is achieved via **Indirect Networks** and **Concentrated Topologies**.

---

## 1. Indirect Topologies: Fat-Tree & Butterfly

In an **Indirect Topology**, routers are divided into dedicated intermediate switching elements, and compute/memory tiles are connected exclusively to the perimeter or leaves of the network.

```mermaid
graph TD
  subgraph Fat_Tree [2-Level Fat-Tree]
    Root0["Root Switch 0"] & Root1["Root Switch 1"]
    
    Leaf0["Leaf Switch 0"]
    Leaf1["Leaf Switch 1"]
    Leaf2["Leaf Switch 2"]
    Leaf3["Leaf Switch 3"]

    Root0 --- Leaf0 & Leaf1 & Leaf2 & Leaf3
    Root1 --- Leaf0 & Leaf1 & Leaf2 & Leaf3

    T0["Tile 0"] & T1["Tile 1"] --- Leaf0
    T2["Tile 2"] & T3["Tile 3"] --- Leaf1
    T4["Tile 4"] & T5["Tile 5"] --- Leaf2
    T6["Tile 6"] & T7["Tile 7"] --- Leaf3
  end
```

### Advantages of Fat-Tree Networks:
1. **High Bisection Bandwidth**: Bandwidth expands as you ascend the tree (hence "Fat" tree), preventing root bottlenecks.
2. **Path Diversity**: Multiple root switches provide redundant shortest paths between any pair of leaves, enabling excellent multipath load balancing.
3. **Application**: Extensively used in large AI inference clusters and memory-centric SoCs where high-throughput memory streaming dominates.

---

## 2. Concentrated Mesh (cMesh)

In a standard 2D mesh, every single CPU tile has its own dedicated router ($1 \text{ Tile} = 1 \text{ Router}$). For an $8 \times 8$ system, this requires **64 routers**, each consuming silicon area and static leakage power.

In a **Concentrated Mesh (cMesh)** (Balfour & Dally, 2006), **4 neighboring compute tiles share a single centralized high-radix router**:

```mermaid
graph TD
  subgraph Concentrated_Tile [Concentrated Router Node]
    R["High-Radix Router<br/>(4 Local + 4 Network Ports)"]
    T0["Tile 0"] --- R
    T1["Tile 1"] --- R
    T2["Tile 2"] --- R
    T3["Tile 3"] --- R
  end
```

### Why cMesh Outperforms Standard Mesh for Manycores:
1. **$4\times$ Fewer Routers**: A 64-core chip requires only **16 routers** arranged in a $4 \times 4$ cMesh, slashing overall router silicon area and clock distribution power.
2. **Halved Network Diameter**: The maximum network distance drops from 14 hops to just **6 hops**!
3. **Lower Zero-Load Latency**: Fewer router hops means packets spend less time traversing pipeline stages.
4. **Local Cluster Speed**: If Tile 0 talks to Tile 1 in the same concentration cluster, the packet is switched locally in a single hop without ever injecting onto the global inter-router mesh!

```mermaid
graph LR
  subgraph cMesh_4x4 [16-Router cMesh for 64 Cores]
    CR00["CR(0,0)<br/>4 Cores"] --- CR10["CR(1,0)<br/>4 Cores"] --- CR20["CR(2,0)<br/>4 Cores"] --- CR30["CR(3,0)<br/>4 Cores"]
    CR01["CR(0,1)<br/>4 Cores"] --- CR11["CR(1,1)<br/>4 Cores"] --- CR21["CR(2,1)<br/>4 Cores"] --- CR31["CR(3,1)<br/>4 Cores"]
    CR02["CR(0,2)<br/>4 Cores"] --- CR12["CR(1,2)<br/>4 Cores"] --- CR22["CR(2,2)<br/>4 Cores"] --- CR32["CR(3,2)<br/>4 Cores"]
    CR03["CR(0,3)<br/>4 Cores"] --- CR13["CR(1,3)<br/>4 Cores"] --- CR23["CR(2,3)<br/>4 Cores"] --- CR33["CR(3,3)<br/>4 Cores"]

    CR00 --- CR01 --- CR02 --- CR03
    CR10 --- CR11 --- CR12 --- CR13
    CR20 --- CR21 --- CR22 --- CR23
    CR30 --- CR31 --- CR32 --- CR33
  end
```

---

## Architectural Comparison: Mesh vs. cMesh (64 Cores)

| Metric | Traditional 2D Mesh | Concentrated Mesh (cMesh) |
| :--- | :--- | :--- |
| **Number of Routers** | 64 routers | **16 routers** ($75\%$ reduction!) |
| **Router Radix** | 5 ports (1 local, 4 network) | 8 ports (4 local, 4 network) |
| **Network Grid** | $8 \times 8$ | $4 \times 4$ |
| **Max Diameter** | 14 hops | **6 hops** ($57\%$ reduction!) |
| **Average Hop Count** | 5.33 hops | **2.67 hops** |
| **Uncontended Latency** | High | **Extremely Low** |

cMesh demonstrates that optimizing the topology is one of the highest-leverage architectural decisions in chip design.

In [Track 4: Routing Algorithms & Deadlock Avoidance](../track4-routing-deadlock/index.md), we will investigate the algorithms that guide packets through these networks without deadlock.
