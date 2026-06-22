# Excalidraw diagrams (diagrams-as-code)

The polished "hero" architecture diagrams for this repo are **generated as code** by
[`tools/excalidraw_gen.py`](../../tools/excalidraw_gen.py), then refined by hand and
exported as images. This keeps diagrams reproducible, version-controlled, and consistent
across every case study — instead of one-off files that drift.

## Workflow

1. **Generate / regenerate** the scene files:
   ```bash
   python3 tools/excalidraw_gen.py
   ```
2. **Open** the `.excalidraw` file at [excalidraw.com](https://excalidraw.com) → **File ▸ Open**
   (or drag it onto the canvas).
3. **Refine** — nudge boxes, drop in real logos from the icon libraries (see
   [`TOOLS.md`](../../TOOLS.md) §3: AWS/GCP/Azure/tech packs), tweak the hand-drawn style.
4. **Export** — File ▸ Export image → **PNG**, *Background off*, **Scale 2×** (or **SVG**) →
   save to [`../images/`](../images/) and reference it from the article.

## Current scenes

| File | Used by | Shows |
|---|---|---|
| `chatgpt-claude-hero.excalidraw` | [ChatGPT & Claude](../../case-studies/chatgpt-claude/README.md) | Full request architecture: Client → Edge → Control → GPU inference + backing stores, with the purple SSE token-stream return path |
| `chatgpt-claude-two-fleets.excalidraw` | [ChatGPT & Claude](../../case-studies/chatgpt-claude/README.md) | The "two fleets in tension" mental model: cheap infinite web tier vs scarce expensive GPU tier |

> Mermaid handles the in-README diagrams (they render natively on GitHub). Excalidraw is
> for the one polished hero image per article and for the YouTube visuals.
