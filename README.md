<div align="center">

# 🏗️ System Design — From Beginner to Advanced

**Learn how the biggest systems in the world are actually built.**
Clear explanations, real diagrams, and full case studies — for the [@codewithmuh](https://youtube.com/@codewithmuh) YouTube series.

</div>

---

## 📺 What is this?

This repo is the companion to a YouTube series where we learn **system design** from scratch and then design real products step by step. Every topic is written as a **detailed article with diagrams** (not just walls of text), and each one maps to a video.

The goal: **a complete beginner** should be able to follow along, understand *why* each decision is made, and walk away able to reason about large-scale systems.

> 🚧 This repo is actively being built. Star ⭐ it and subscribe to follow along.

## 🧭 How to use this repo

1. **Start with the [Fundamentals](./fundamentals/README.md)** — the vocabulary and building blocks (load balancing, caching, databases, sharding, CAP, queues, …).
2. **Then pick a case study** below and design a real system end-to-end.
3. Each article follows the same repeatable framework, so the *approach* becomes second nature.

## 📚 Learning path

### Part 1 — Foundations
- [**System Design Fundamentals**](./fundamentals/README.md) — the framework + every core building block, beginner → advanced.

### Part 2 — Case studies (design a real system)

| # | System | What you'll learn | Status |
|---|--------|-------------------|:------:|
| 1 | [Cloud Platform (AWS / Google Cloud)](./case-studies/cloud-platform/README.md) | Control plane vs data plane, virtualization, multi-tenancy, IAM | 🚧 |
| 2 | [ChatGPT & Claude (AI Assistant)](./case-studies/chatgpt-claude/README.md) | LLM inference serving, batching, KV cache, token streaming | 🚧 |
| 3 | [Instagram](./case-studies/instagram/README.md) | News feed, media storage, fan-out | ⬜ |
| 4 | [WhatsApp](./case-studies/whatsapp/README.md) | Real-time messaging, presence, delivery receipts | ⬜ |
| 5 | [Facebook](./case-studies/facebook/README.md) | Social graph, feed ranking, notifications | ⬜ |
| 6 | [TikTok](./case-studies/tiktok/README.md) | Recommendation feed, video delivery at scale | ⬜ |
| 7 | [YouTube](./case-studies/youtube/README.md) | Video upload/transcode, streaming, CDN | ⬜ |
| 8 | [Twitter / X](./case-studies/twitter-x/README.md) | Timeline, fan-out on write vs read | ⬜ |
| 9 | [Uber](./case-studies/uber/README.md) | Geospatial matching, real-time location | ⬜ |
| 10 | [Netflix](./case-studies/netflix/README.md) | Adaptive streaming, CDN, recommendations | ⬜ |

`✅ Published · 🚧 In progress · ⬜ Planned`

## 🖊️ How the diagrams work

We use a layered approach so diagrams are both **version-controlled** and **beautiful on video**:

- **Mermaid** — rendered *natively inside GitHub* for inline flowcharts & sequence diagrams (no image hosting needed).
- **Excalidraw** — for the polished, hand-drawn architecture diagrams (source `.excalidraw` files live in [`assets/excalidraw/`](./assets/excalidraw/), exported PNG/SVG in [`assets/images/`](./assets/images/)).

See [**TOOLS.md**](./TOOLS.md) for the full recommended toolchain — including **how to add cloud/logo icons in Excalidraw** and the **article → YouTube video** workflow.

## 📐 Writing a new article

Copy [`templates/ARTICLE_TEMPLATE.md`](./templates/ARTICLE_TEMPLATE.md) into a new case-study folder and fill it in. Every system-design problem uses the same framework:

> **Requirements → Capacity estimation → API design → Data model → High-level design → Deep dives → Bottlenecks & trade-offs**

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Issues, corrections, and diagram improvements are welcome.

---

<div align="center">
Made with ❤️ for learners · <a href="https://youtube.com/@codewithmuh">YouTube @codewithmuh</a>
</div>
