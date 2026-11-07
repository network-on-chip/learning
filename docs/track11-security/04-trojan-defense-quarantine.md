# Lesson 11.4: Hardware Trojan Defense & Zero-Trust Quarantine

<div class="noc-hero">
  <div class="noc-track-badge">Track 11 • Lesson 04</div>
  <h1>Autonomous Isolation Protocols &amp; Physical Unclonable Functions (PUFs)</h1>
  <p class="subtitle">
    Quarantine rogue silicon cores in real time, scramble timing covert channels using LFSR phase jitter, and authenticate multi-die chiplets using intrinsic wire-delay PUFs.
  </p>
</div>

---

## 1. Autonomous Quarantine Protocol

When the WMA detector triggers an anomaly pulse, the router's Network Interface (NI) executes an autonomous containment sequence:
1. **Clock Gating:** Immediately gate the clock to the compromised tile to halt further thermal escalation.
2. **Packet Deflection:** Reconfigure routing arbitration masks to drop or reroute egress packets from the malicious port.
3. **Security Interrup:** Raise a trusted cryptographic interrupt to the secure root-of-trust core.

---

👉 **Advance to [Track 12: Domain-Specific NoCs for LLMs, Transformers & SNNs](../track12-ai-llm-snn/index.md)**
