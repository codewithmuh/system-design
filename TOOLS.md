# 🛠️ Tools & Workflow

The toolchain behind every article and video in this repo. The philosophy is **layered**:

- **Mermaid** for diagrams that live *inside* the article — they render natively on GitHub, are version-controlled, and diff in git.
- **Excalidraw** for the polished, hand-drawn "hero" architecture diagrams — the teaching look you see in the videos.
- Everything else (recording, editing, animation) exists to turn one article into one video with as little friction as possible.

> The single biggest unlock for Excalidraw users: **you add cloud/tech logos as one-click libraries** from `libraries.excalidraw.com`. Most people never discover this. See [§3](#3-how-to-put-logos--icons-in-excalidraw).

---

## 1. Recommended toolchain

| Job | Free / budget pick | Premium pick | Why |
|---|---|---|---|
| **Writing articles** | Markdown in VS Code | Same + Grammarly | Plain `.md` keeps everything in git, diffable, zero lock-in. |
| **In-repo diagrams** | **Mermaid** | Mermaid | Only tool that renders *natively* inside GitHub READMEs. Use for flowcharts, sequence diagrams, ER/DB schemas. |
| **Polished architecture art** | **Excalidraw** | Excalidraw+ (~$7/mo) | Hand-drawn "explained by a human" look; perfect for video. Exports transparent PNG/SVG. |
| **Official cloud-icon diagrams** | **draw.io** (diagrams.net) | Lucidchart | When you need pixel-accurate *official* AWS/Azure/GCP icons. 100% free, huge built-in stencils. |
| **Logos / icons** | Excalidraw libraries + draw.io stencils | Cloudairy (12k+ official icons) | Covered in [§3](#3-how-to-put-logos--icons-in-excalidraw). |
| **Slides** | Keynote (Mac) / Google Slides | Gamma (AI prompt→deck) | Keynote's **Magic Move** is the secret weapon for animated diagram reveals. |
| **Screen recording** | **OBS Studio** | Screen Studio (Mac, auto-zoom) / Camtasia | OBS = total control, free. Screen Studio adds pro cursor-follow zooms with zero editing. |
| **Video editing** | **DaVinci Resolve** (free) | Resolve Studio ($295 one-time) / Premiere | Resolve's free tier is broadcast-grade. Add **Descript** for text-based "delete words = cut video" editing. |
| **Animation / motion** | Keynote Magic Move / PowerPoint Morph | After Effects (what ByteByteGo uses) / Motion Canvas (free) | The progressive "build-up" diagram reveal. See [§4](#4-from-article-to-youtube-video). |
| **Thumbnails** | **Canva** (5k+ templates) | Figma (brand template) + Photoshop | Canva for speed; Figma when you make a locked, reusable brand template. |
| **Audio cleanup** | **Adobe Podcast Enhance** (free) | Krisp (real-time) | Run voiceover through Adobe Enhance once — it rescues mediocre recordings. With a good mic in a quiet room, keep it light. |
| **Microphone** 🎙️ | Samson Q2U / ATR2100x (~$70, USB+XLR) | Shure MV7+ (~$280) | **Audio is the highest-ROI spend on the channel.** The Q2U sounds great and plugs in over USB. |

---

## 2. Diagram tool cheat-sheet

| Tool | Best for | Renders in GitHub? | Icons |
|---|---|:---:|---|
| **Mermaid** | In-README flow / sequence / ER diagrams | ✅ **Yes** | Weak (generic boxes) |
| **Excalidraw** | Hero architecture art, video diagrams | ❌ (export PNG/SVG) | ✅ via libraries (§3) |
| **draw.io** | Official-icon cloud diagrams, precision | ❌ (export PNG/SVG) | ✅ Best free official sets |
| **D2 / Terrastruct** | Diagram-as-code that *also* looks good | ❌ (export SVG) | ✅ Best of the code tools |
| **Cloudairy** | AI-generated multi-cloud diagrams, fast | ❌ | ✅ 12,000+ official |

**Rule of thumb:** structure/flow that should live in the README → **Mermaid**. The one beautiful "hero" diagram per article → **Excalidraw**. A diagram that genuinely needs official vendor icons → **draw.io**.

---

## 3. How to put logos & icons in Excalidraw

Excalidraw ships with **no** AWS/GCP/Azure/Kubernetes icons by default — that's why they're hard to find. You add them as free **libraries** in one click.

### A. Add icon libraries
1. Open Excalidraw → click the **Library** button (top-right); click the **pin** to keep the panel open.
2. Click **Browse libraries** → opens **[libraries.excalidraw.com](https://libraries.excalidraw.com/)**.
3. Find a library → **Add to Excalidraw** → it loads straight into your panel. Repeat for as many as you want.

### B. The libraries to add first (real names + authors)
- **Cloud** — *rfranzke* → Kubernetes + **AWS, Azure, GCP** logos & architecture icons *(best single starter pack)*
- **AWS Architecture Icons** — *Narhari Motivaras* · **AWS Serverless Icons** — *Slobodan Stojanović* · **AWS Simple Icons** — *husainkhambaty*
- **GCP Icons** — *Clément Bosc* · **Original Google Architecture Icons** — *Marcus Guidoti*
- **Azure** — *Gordon Howes'* set (Compute / Network / Storage / Containers / General)
- **Technology Logos** — *Matthias Haeussler* (Docker, Terraform, Kafka, Redis, Spring…)
- **Software Logos** — *drwnio* (Postgres, Redis, Nginx, RabbitMQ, load balancer, server)
- **System Design Components** — *Rohan Pithadiya* · **System Design Icons** — *niknm*
- **Network topology icons** — *dwelle*

### C. Use a shape
The panel shows thumbnails grouped by library. **Drag any icon onto the canvas**, then resize / recolor / connect with arrows like any element. Many are real SVG logos, so they stay crisp.

### D. Drag in *any* custom logo (PNG/SVG)
For a logo not in a library: **drag-and-drop the file onto the canvas**, or copy the image and paste (`Cmd/Ctrl+V`), or use the toolbar image tool. Prefer **SVG** for sharp scaling in video.
> ⚠️ Caveat: Excalidraw can't embed images inside *published public* libraries yet. Workaround: select your reused icons → **Add to library** (the **+**) → three-dots → **Save to** a local `.excalidrawlib`. Keep one `codewithmuh-system-design.excalidrawlib` with your standard nodes.

### E. Export clean assets
File/export → **PNG** or **SVG**. Toggle **Background off** for transparency. Bump **Scale to 2x–3x** for crisp 1080p/4K. Commit the `.excalidraw` source to `assets/excalidraw/` and the export to `assets/images/`.

### Fallback for *official* vendor icons
- **draw.io:** left panel → **More Shapes…** → **Networking** → tick **AWS19, Azure, GCP, Kubernetes, Cisco** → **Apply**. Searchable official palette; enable **Labels** to see names.
- **Cloudairy:** 12,000+ official icons + AI layout if you want a vendor-accurate diagram generated fast.

---

## 4. From article to YouTube video

The repeatable pipeline — **draw once, ship twice** (the article and the video share the same diagram):

1. **Write the article** (`README.md`) using `templates/ARTICLE_TEMPLATE.md`. Mermaid diagrams inline.
2. **Build the hero diagram in Excalidraw** (with the icon libraries from §3). Export a 2x transparent PNG/SVG into `assets/`.
3. **Make the animated reveal deck.** This is the ByteByteGo "build-up" effect — and you don't need After Effects:
   - Draw the *final* diagram once. **Group each component + its label.**
   - **Duplicate the slide per reveal step.** Slide 1 = just the client. Slide 2 = client + load balancer + the arrow. Slide 3 adds the cache. Each slide is a cumulative superset of the last.
   - Set every transition to **Magic Move** (Keynote) / **Morph** (PowerPoint). Shared elements auto-tween; new ones ease in. *That* is the smooth progressive reveal.
   - To "zoom to what you're talking about," scale/recolor the active node on its entry slide — Magic Move animates that too.
   - Keep object positions consistent across slides (in PowerPoint, give matched shapes the same names) so the morph matches elements correctly.
4. **Record** the slideshow + any code with **OBS** (or **Screen Studio** for auto-zoom), advancing slides in time with your voiceover.
5. **Edit** in **DaVinci Resolve** — assemble clips + voiceover, run audio through **Adobe Podcast Enhance**.
6. **Thumbnail** in **Canva** (or your **Figma** brand template) — readable at small size, 2–4 words of text.
7. **Publish** — link this GitHub repo in the description; use the `yt-description` / `yt-title-thumbnail` workflows.

> Graduate to **Motion Canvas** (free, TypeScript) when you want pixel-perfect, reusable, code-driven animations without an After Effects subscription — it's the closest free replica of the ByteByteGo pipeline.

---

## 5. Quick-start links

**Excalidraw & icons**
- Excalidraw: <https://excalidraw.com> · Libraries: <https://libraries.excalidraw.com/>
- draw.io: <https://app.diagrams.net> · Cloudairy: <https://cloudairy.com>

**Diagrams-as-code**
- Mermaid: <https://mermaid.js.org> · Live editor: <https://mermaid.live>
- D2: <https://d2lang.com> · Motion Canvas: <https://motioncanvas.io>

**Video toolchain**
- OBS Studio: <https://obsproject.com> · Screen Studio: <https://screen.studio>
- DaVinci Resolve: <https://www.blackmagicdesign.com/products/davinciresolve>
- Descript: <https://www.descript.com> · Adobe Podcast Enhance: <https://podcast.adobe.com/enhance>
- Canva: <https://www.canva.com> · Figma: <https://www.figma.com>

**Reference repos (study these)**
- donnemartin/system-design-primer · karanpratapsingh/system-design · ByteByteGoHq/system-design-101 · ashishps1/awesome-system-design-resources
