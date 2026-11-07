# Lesson 6.3: Fine-Grained Router Power Gating

<div class="noc-hero">
  <div class="noc-track-badge">Track 06 • Lesson 03</div>
  <h1>Sleep Transistors, Wake-Up Latency &amp; State Retention</h1>
  <p class="subtitle">
    Shut down idle router crossbars and virtual channel buffers using high-threshold sleep transistors while eliminating wake-up packet stalls with lookahead wake-up tokens.
  </p>
</div>

---

## 1. Power-Gating Switch Architecture

Power gating inserts high-$V_{th}$ PMOS header or NMOS footer sleep transistors between the standard logic gates and the power rails ($V_{DD} / V_{SS}$).

* **Active Mode:** Sleep transistors are fully conducting ($V_{GS} = V_{DD}$). Minimal IR drop ($<2\% V_{DD}$).
* **Sleep Mode:** Sleep transistors cut off, reducing static leakage power by $>95\%$.
* **Wake-Up Penalty:** Charging the virtual ground/power capacitance requires $4\text{--}12\text{ clock cycles}$, generating a significant wake-up delay penalty for incoming packets.

---

## 2. Lookahead Wake-Up Tokens

To eliminate packet stalling, upstream routers transmit a 1-bit **Wake-Up Token** 2–3 hops in advance. By the time the head flit traverses intermediate links, the target router's power rails have fully stabilized.

---

👉 **Next: [Lesson 6.4: Voltage Emergencies & Resonant Clocking](04-voltage-emergencies-energy.md)**
