# Contributing

Thanks for helping improve this system-design learning resource! 🙌

## Ways to contribute
- **Fix errors** — technical inaccuracies, typos, broken Mermaid diagrams.
- **Improve diagrams** — clearer Excalidraw architecture diagrams or Mermaid flows.
- **Add depth** — extra deep-dives, trade-offs, or real-world references to an existing article.

## Adding / editing an article
1. Copy [`templates/ARTICLE_TEMPLATE.md`](./templates/ARTICLE_TEMPLATE.md) into the relevant `case-studies/<name>/` folder as `README.md`.
2. Keep it **beginner-friendly first, advanced later** — define jargon the first time it appears.
3. Prefer **Mermaid** for inline diagrams (renders on GitHub). For polished architecture art, add the `.excalidraw` source to `assets/excalidraw/` and the exported PNG/SVG to `assets/images/`.
4. Every claim about how a real system works should cite a source in the **References** section.

## Diagram conventions
- Mermaid for flowcharts (`graph TD`), sequences (`sequenceDiagram`), and data models (`erDiagram`).
- Excalidraw for the main "hero" architecture diagram of each case study.
- Keep colors/icons consistent — see [TOOLS.md](./TOOLS.md) for the icon libraries we use.

## Style
- Short paragraphs, lots of headings, and a diagram whenever words get heavy.
- Use tables for comparisons (SQL vs NoSQL, trade-offs, etc.).
