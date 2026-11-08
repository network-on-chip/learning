# Lesson 11.1: Security Threat Models in On-Chip Networks

<div class="noc-hero">
  <div class="noc-track-badge">Track 11 • Lesson 01</div>
  <h1>Multi-Tenant SoCs, Untrusted Third-Party IPs &amp; Attack Taxonomy</h1>
  <p class="subtitle">
    Classify hardware security vulnerabilities in modern shared networks-on-chip: from malicious third-party IP cores to buffer-flooding Denial-of-Service and side-channel leakage.
  </p>
</div>

---

## 1. The Zero-Trust Silicon Paradigm

In cloud data centers and multi-tenant SoCs (e.g., AWS Graviton, Apple Silicon, heterogeneous automotive SoCs), multiple mutually distrusting applications share the same physical router fabric. Furthermore, modern chips integrate dozens of third-party IP blocks (3PIPs) whose transistor layouts cannot be fully verified:

```mermaid
flowchart TD
    SharedNoC["Shared On-Chip Interconnect"] --> Threat1["Denial of Service (DoS)<br/>Buffer Flooding & Bandwidth Starvation"]
    SharedNoC --> Threat2["Covert Timing Channels<br/>Packet Inter-Arrival Modulation"]
    SharedNoC --> Threat3["Thermal Covert Channels<br/>High-Frequency Power Throttle Attacks"]
    SharedNoC --> Threat4["Eavesdropping & Spoofing<br/>Unencrypted Packet Header Sniffing"]
```

---

## 2. Interactive Arcade Challenge

Defend against live hardware threats in our interactive CAD laboratory:

👉 **[Launch NoC Hardware Security CAD: NoC Security &amp; Threat Defense Arcade](../../interactive/security/)**

---

👉 **Next: [Lesson 11.2: Thermal & Timing Covert Channels](02-thermal-timing-covert-channels.md)**
