# 6.1 3D TSV Interconnects

In monolithic 2D chips, expanding network size from $N$ to $2N$ nodes increases the horizontal wire distance and hop count. 

By stacking multiple silicon dies vertically and connecting them with microscopic vertical copper pillars called **Through-Silicon Vias (TSVs)**, we unlock **3D Network-on-Chip (3D NoC)**.

---

## 1. Physical Anatomy of 3D Integration

In a 3D IC, multiple wafer-thinned active silicon layers (e.g., Layer 0 for Logic, Layer 1 for SRAM Cache, Layer 2 for DRAM) are bonded face-to-back or face-to-face:

```mermaid
graph TD
  subgraph Layer_2 [Layer 2: Memory / DRAM Tier]
    R20["R(0,0,2)"] --- R21["R(1,0,2)"]
  end

  subgraph Layer_1 [Layer 1: Compute / L2 Cache Tier]
    R10["R(0,0,1)"] --- R11["R(1,0,1)"]
  end

  subgraph Layer_0 [Layer 0: Host CPU / Base Die]
    R00["R(0,0,0)"] --- R01["R(1,0,0)"]
  end

  R20 ===|TSV Vertical Link| R10
  R10 ===|TSV Vertical Link| R00
  R21 ===|TSV Vertical Link| R11
  R11 ===|TSV Vertical Link| R01
```

### The Magic of TSVs:
- **Vertical Distance**: A typical thinned silicon die is only $20 \text{ to } 50 \ \mu\text{m}$ thick.
- **Microscopic Delay**: While a horizontal inter-router link might span $1000 \ \mu\text{m}$ ($1 \text{ mm}$), the vertical TSV link is $20\times \text{ shorter}$! Vertical latency is negligible (often sub-cycle).

---

## 2. 7-Port 3D Router Microarchitecture

To support vertical communication, the canonical 5-port 2D router is expanded into a **7-port 3D router**:

```mermaid
graph TD
  subgraph Router_3D [7-Port 3D NoC Router]
    North["North Port (Horizontal)"]
    South["South Port (Horizontal)"]
    East["East Port (Horizontal)"]
    West["West Port (Horizontal)"]
    Local["Local Core Port"]
    Up["UP Port (TSV to Upper Layer)"]
    Down["DOWN Port (TSV to Lower Layer)"]
    
    North & South & East & West & Local & Up & Down --> Crossbar["7x7 Crossbar Switch"]
  end
```

### Architectural Implications:
- **Crossbar Size**: Increases from $5 \times 5$ to $7 \times 7$ crosspoints ($49$ vs $25$ crosspoints, nearly double the crossbar area).
- **Dimension-Order Routing in 3D (XYZ Routing)**:
  1. Route along $X$ dimension.
  2. Route along $Y$ dimension.
  3. Route along $Z$ dimension (via TSVs).
  4. Delivers deterministic, deadlock-free communication across 3D meshes!

---

## 3. The 3D Thermal Challenge

While 3D NoCs dramatically reduce wire length and hop count, they present a major physical obstacle: **Severe Thermal Trapping**.

In a 2D chip, heat escapes directly out through the silicon substrate into the heat spreader and heatsink. In a 3-layer 3D stack:
- Active tiers in the middle layer are insulated by low-thermal-conductivity dielectric bonding layers ($\text{SiO}_2$ or polymer adhesives).
- Power density multiplies ($3\times$ higher power per unit footprint).
- Temperatures can easily spike over $110^\circ\text{C}$ unless dynamic thermal-aware routing policies steer packets away from vertical hotspot columns!

In the next lesson, we will see how the industry solves these manufacturing and thermal yield challenges using **2.5D Multi-Chiplet Interconnects**.
