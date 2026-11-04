# Network-on-Chip Learning Hub (`network-on-chip/learning`)

[![Deploy Network-on-Chip Learning Hub](https://github.com/network-on-chip/learning/actions/workflows/deploy.yml/badge.svg)](https://github.com/network-on-chip/learning/actions/workflows/deploy.yml)
[![Live Learning Hub](https://img.shields.io/badge/Live%20Site-network--on--chip.github.io%2Flearning-0f766e?style=flat&logo=github)](https://network-on-chip.github.io/learning/)
[![Curated Papers](https://img.shields.io/badge/Curated%20Papers-541%20IEEE-ea580c?style=flat)](https://network-on-chip.github.io/.github/)

An open-source, interactive curriculum and laboratory bridging theoretical computer architecture, silicon router microarchitecture, and open-source reproducible research.

---

## 🚀 Live Site
- **Portal URL**: [https://network-on-chip.github.io/learning/](https://network-on-chip.github.io/learning/)
- **Interactive Simulator**: [https://network-on-chip.github.io/learning/interactive/visualizer/](https://network-on-chip.github.io/learning/interactive/visualizer/)
- **NoC Papers Map**: [https://network-on-chip.github.io/.github/](https://network-on-chip.github.io/.github/)

---

## 📚 Curriculum Structure

- **Track 1: Interconnect Fundamentals**: Why NoC, packets/flits/phits, switching mechanisms (SAF, VCT, Wormhole), and credit-based flow control.
- **Track 2: Router Microarchitecture**: Canonical 5-stage pipeline (BW-RC-VA-SA-ST), 1-stage bypass routers, Virtual Channels, Matrix arbiters, crossbars.
- **Track 3: Topologies & Metrics**: 2D Mesh, 2D Torus, Folded Torus, Fat-Tree, Concentrated Mesh (cMesh).
- **Track 4: Routing & Deadlock Avoidance**: Deterministic DOR (XY), Turn Models (West-First, Odd-Even), CDGs, Dally-Seitz & Duato's Theorem.
- **Track 5: Thermal & Congestion Management**: Proactive ML hotspot prediction, robust sensor placement under non-Gaussian noise.
- **Track 6: Chiplets & 3D NoC**: 3D TSVs, 7-port 3D routers, 2.5D interposers, UCIe and BoW standards.
- **Track 7: Landmark Paper Studies**: Deep dives into seminal IEEE TCAD, TVLSI, and JSSC papers from our 541-paper repository.
- **Interactive Lab**: Browser-based HTML5 Canvas cycle-accurate routing visualizer.

---

## 🛠️ Local Development

### 1. Install Dependencies
```bash
make install
# or: pip install -r requirements.txt
```

### 2. Run Local Preview Server
```bash
make serve
# Server will start at http://127.0.0.1:8000
```

### 3. Build Static Site
```bash
make build
# Compiles into site/
```

---

## 🤝 Contributing & Synchronization
This repository is synchronized from the parent research laboratory [`network-on-chip/noc-lab`](https://github.com/network-on-chip/noc-lab).

To push updates from the root repository:
```bash
bash share/sync_learning.sh
```
