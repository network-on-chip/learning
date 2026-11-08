# Lesson 12.1: LLM Collective Communication Bottlenecks

<div class="noc-hero">
  <div class="noc-track-badge">Track 12 • Lesson 01</div>
  <h1>All-Reduce, All-to-All &amp; The Transformer Interconnect Wall</h1>
  <p class="subtitle">
    Quantify communication-to-computation ratios in 100B+ Large Language Models (LLMs), analyze tensor and pipeline parallelism, and evaluate the Ring All-Reduce bottleneck.
  </p>
</div>

---

## 1. Generative AI Interconnect Scaling

Large Language Models (LLMs) such as Llama-3 (70B/405B) and DeepSeek-V3 rely on massive distributed clusters. During multi-head attention and feed-forward training passes, tensor cores must synchronize gradients across all nodes:

$$
\text{Volume}_{\text{All-Reduce}} = 2 \cdot \frac{N-1}{N} \cdot M
$$

where $N$ is the number of accelerator cores and $M$ is the tensor model parameter size in bytes. When computing 70B parameter models, memory and interconnect communication dominate over $70\%$ of total cycle time.

---

## 2. Interactive Arcade Challenge

Accelerate generative AI models live in our interactive CAD laboratory:

👉 **[Launch LLM Collective Simulator: LLM &amp; AI Collective Accelerator Arcade](../../interactive/transformer/)**

---

👉 **Next: [Lesson 12.2: In-Network Reduction Crossbars (PAC-NoC)](02-in-network-reduction-crossbars.md)**
