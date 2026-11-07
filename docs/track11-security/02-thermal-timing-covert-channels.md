# Lesson 11.2: Thermal & Timing Covert Channels

<div class="noc-hero">
  <div class="noc-track-badge">Track 11 • Lesson 02</div>
  <h1>Covert Timing Leakage, Substrate Thermal Coupling &amp; Key Exfiltration</h1>
  <p class="subtitle">
    Model how malicious hardware trojans exfiltrate 256-bit AES encryption keys across physically isolated virtual networks using packet delay variations and substrate thermal conduction.
  </p>
</div>

---

## 1. Timing Covert Channels

Even when an SoC enforces strict software process isolation, tenants share physical crossbars and virtual channels. An attacker core modulates the inter-arrival latency of benign packets:
* Bit `1`: Inject a burst of high-priority packets, congesting shared router buffers and delaying victim traffic.
* Bit `0`: Remain idle, allowing victim traffic to pass with minimal zero-load latency.

A receiver core measuring packet round-trip times can decode the transmitted bits at rates up to **$50\text{ kb/s}$**, bypassing all software firewalls!

---

👉 **Next: [Lesson 11.3: Online WMA Anomaly Detection (HeatSense)](03-heatsense-wma-anomaly-detection.md)**
