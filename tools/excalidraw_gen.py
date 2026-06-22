#!/usr/bin/env python3
"""
Diagrams-as-code → Excalidraw scene files (.excalidraw).

Emits guaranteed-valid Excalidraw JSON so diagrams are reproducible and editable.
Open the output in https://excalidraw.com (File ▸ Open), refine the hand-drawn
look, then export a 2x transparent PNG/SVG into ../assets/images/.

Usage:  python3 tools/excalidraw_gen.py
"""
import json, os

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "excalidraw")

# ---------------------------------------------------------------- engine -----
class Scene:
    def __init__(self):
        self.els = []
        self.n = 0
        self.boxes = {}  # id -> dict element (so arrows can bind + we can anchor)

    def _id(self):
        self.n += 1
        return f"el{self.n}"

    def _seed(self):
        return 100000 + self.n * 7919

    def _base(self, t, x, y, w, h, **kw):
        e = {
            "id": kw.get("id") or self._id(),
            "type": t, "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": kw.get("strokeColor", "#1e1e1e"),
            "backgroundColor": kw.get("backgroundColor", "transparent"),
            "fillStyle": kw.get("fillStyle", "solid"),
            "strokeWidth": kw.get("strokeWidth", 2),
            "strokeStyle": kw.get("strokeStyle", "solid"),
            "roughness": kw.get("roughness", 1),
            "opacity": kw.get("opacity", 100),
            "groupIds": kw.get("groupIds", []),
            "frameId": None,
            "roundness": kw.get("roundness", None),
            "seed": self._seed(),
            "version": 1, "versionNonce": self._seed() + 1, "isDeleted": False,
            "boundElements": kw.get("boundElements", None),
            "updated": 1, "link": None, "locked": False,
        }
        return e

    def text(self, s, x, y, size=20, color="#1e1e1e", align="left",
             w=None, container=None, family=1):
        lines = s.split("\n")
        lh = 1.25
        h = round(size * lh * len(lines))
        if w is None:
            w = round(max(len(l) for l in lines) * size * 0.55) + 8
        e = self._base("text", x, y, w, h,
                       strokeColor=color, roundness=None)
        e.update({
            "text": s, "fontSize": size, "fontFamily": family,
            "textAlign": align, "verticalAlign": "middle" if container else "top",
            "containerId": container, "originalText": s,
            "lineHeight": lh, "baseline": round(size * 0.9),
        })
        self.els.append(e)
        return e

    def lane(self, title, x, y, w, h, header_color, bg):
        r = self._base("rectangle", x, y, w, h,
                       strokeColor=header_color, backgroundColor=bg,
                       fillStyle="solid", strokeWidth=1.5, strokeStyle="solid",
                       roughness=1, roundness={"type": 3}, opacity=100)
        self.els.append(r)
        self.text(title, x + 14, y + 12, size=18, color=header_color,
                  align="left", family=1)
        return r

    def node(self, nid, label, x, y, w, h, stroke, bg, size=16, strokeWidth=2):
        rect = self._base("rectangle", x, y, w, h,
                          id=nid, strokeColor=stroke, backgroundColor=bg,
                          fillStyle="solid", strokeWidth=strokeWidth,
                          roughness=1, roundness={"type": 3},
                          boundElements=[])
        self.els.append(rect)
        tid = self._id()
        rect["boundElements"].append({"type": "text", "id": tid})
        self.text(label, x + 8, y + 8, size=size, color="#1e1e1e",
                  align="center", w=w - 16, container=nid)
        self.els[-1]["id"] = tid
        self.boxes[nid] = rect
        return rect

    @staticmethod
    def _anchor(box, side):
        x, y, w, h = box["x"], box["y"], box["width"], box["height"]
        return {"L": (x, y + h / 2), "R": (x + w, y + h / 2),
                "T": (x + w / 2, y), "B": (x + w / 2, y + h)}[side]

    def arrow(self, a, sa, b, sb, color="#1e1e1e", width=2, dashed=False,
              label=None, both=False, waypoints=None, size=14):
        boxa, boxb = self.boxes[a], self.boxes[b]
        p0 = self._anchor(boxa, sa)
        p1 = self._anchor(boxb, sb)
        pts = [p0] + (waypoints or []) + [p1]
        x0, y0 = pts[0]
        rel = [[round(px - x0, 1), round(py - y0, 1)] for px, py in pts]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        e = self._base("arrow", x0, y0, round(max(xs) - min(xs), 1),
                       round(max(ys) - min(ys), 1),
                       strokeColor=color, strokeWidth=width,
                       strokeStyle="dashed" if dashed else "solid",
                       roughness=1, roundness={"type": 2}, boundElements=[])
        e.update({
            "points": rel, "lastCommittedPoint": None,
            "startBinding": {"elementId": a, "focus": 0, "gap": 4},
            "endBinding": {"elementId": b, "focus": 0, "gap": 4},
            "startArrowhead": "arrow" if both else None,
            "endArrowhead": "arrow",
        })
        self.els.append(e)
        boxa.setdefault("boundElements", []) or boxa["boundElements"]
        if boxa["boundElements"] is None: boxa["boundElements"] = []
        if boxb["boundElements"] is None: boxb["boundElements"] = []
        boxa["boundElements"].append({"type": "arrow", "id": e["id"]})
        boxb["boundElements"].append({"type": "arrow", "id": e["id"]})
        if label:
            mid = pts[len(pts) // 2]
            tid = self._id()
            e["boundElements"].append({"type": "text", "id": tid})
            t = self.text(label, mid[0], mid[1], size=size, color=color,
                          align="center", w=len(label) * size * 0.6,
                          container=e["id"])
            t["id"] = tid
        return e

    def dump(self, path):
        scene = {
            "type": "excalidraw", "version": 2,
            "source": "https://github.com/codewithmuh/system-design",
            "elements": self.els,
            "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
            "files": {},
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(scene, f, indent=2)
        # validate round-trip
        json.loads(open(path, encoding="utf-8").read())
        print(f"  ✓ {os.path.relpath(path)}  ({len(self.els)} elements)")


# palette
CLR = {
    "client": ("#1971c2", "#d0ebff", "#f1f8ff"),
    "edge":   ("#0ca678", "#c3fae8", "#ebfbf5"),
    "ctrl":   ("#f08c00", "#ffec99", "#fff9ef"),
    "infra":  ("#e03131", "#ffc9c9", "#fff5f5"),
    "data":   ("#2f9e44", "#d3f9d8", "#f4fcf5"),
}
INK = "#1e1e1e"; PURPLE = "#7048e8"; ORANGE = "#e8590c"; GRAY = "#868e96"


def lane_nodes(s, lane_x, labels, kind, nw=190, nh=50, gap=12,
               area_top=185, area_bot=595):
    stroke, bg, _ = CLR[kind]
    k = len(labels)
    total = k * nh + (k - 1) * gap
    start = area_top + (area_bot - area_top - total) / 2
    ids = []
    sw = 3 if kind == "infra" else 2
    for i, (nid, lbl) in enumerate(labels):
        y = start + i * (nh + gap)
        s.node(nid, lbl, lane_x + 20, y, nw, nh, stroke, bg, strokeWidth=sw)
        ids.append(nid)
    return ids


def build_hero():
    s = Scene()
    s.text("How ChatGPT & Claude Work — Request Architecture", 40, 34,
           size=28, color=INK, family=1)
    s.text("A cheap, near-infinite web tier (green) feeding a scarce, expensive GPU tier (red) — the bottleneck.",
           40, 78, size=15, color="#495057", family=1)

    LY, LH, LW, STEP, X0 = 120, 480, 230, 270, 40
    lanes = [("Client", "client"), ("Edge / Gateway", "edge"),
             ("Control / Orchestration", "ctrl"), ("Inference Cluster", "infra")]
    for i, (title, kind) in enumerate(lanes):
        hc, _, bg = CLR[kind]
        t = title + ("  ⚠ BOTTLENECK" if kind == "infra" else "")
        s.lane(t, X0 + i * STEP, LY, LW, LH, hc, bg)

    lane_nodes(s, X0 + 0 * STEP, [("user", "User\nbrowser / app")], "client")
    lane_nodes(s, X0 + 1 * STEP, [
        ("cdn", "Global edge / CDN\nTLS terminate"),
        ("gw", "API gateway"),
        ("auth", "Auth\nhashed key → org"),
        ("rl", "Rate limiter\nRPM + TPM · Redis")], "edge")
    lane_nodes(s, X0 + 2 * STEP, [
        ("router", "Request router\nmodel · ctx · HW"),
        ("orch", "Orchestrator\nprompt · stream"),
        ("lb", "Load balancer\nKV-cache sticky"),
        ("queue", "Inference queue\nadmission · TTFT")], "ctrl")
    lane_nodes(s, X0 + 3 * STEP, [
        ("sched", "Batching scheduler\ncontinuous"),
        ("prefill", "GPU · PREFILL\ncompute-bound"),
        ("decode", "GPU · DECODE\nmemory-bound"),
        ("kv", "KV cache\nPagedAttention")], "infra")

    # backing data stores (bottom row)
    s.text("Backing services", 560, 632, size=15, color=CLR["data"][0], family=1)
    dstroke, dbg, _ = CLR["data"]
    for nid, lbl, dx in [("conv", "Conversation store\nmessage tree · NoSQL", 560),
                          ("redis", "Redis\nhot session state", 760),
                          ("vec", "Vector DB\nRAG", 960)]:
        s.node(nid, lbl, dx, 655, 175, 56, dstroke, dbg, strokeWidth=2)

    # ---- forward spine ----
    s.arrow("user", "R", "cdn", "L", color=INK, width=2.5, label="HTTPS")
    s.arrow("rl", "R", "router", "L", color=INK, width=2.5, label="admit")
    s.arrow("queue", "R", "sched", "L", color=INK, width=2.5, label="enqueue")
    # ---- vertical chains ----
    for a, b in [("cdn", "gw"), ("gw", "auth"), ("auth", "rl")]:
        s.arrow(a, "B", b, "T", color=INK)
    for a, b in [("router", "orch"), ("orch", "lb"), ("lb", "queue")]:
        s.arrow(a, "B", b, "T", color=INK)
    for a, b in [("sched", "prefill"), ("prefill", "decode")]:
        s.arrow(a, "B", b, "T", color=INK)
    s.arrow("decode", "B", "kv", "T", color=INK, both=True, label="read / write")
    # ---- highlighted returns ----
    s.arrow("decode", "L", "orch", "R", color=ORANGE, width=2.5,
            label="tokens, 1 at a time")
    # SSE punchline routed along the bottom
    s.arrow("orch", "B", "user", "B", color=PURPLE, width=3.5,
            waypoints=[(695, 740), (155, 740)],
            label="SSE token stream → your screen", size=15)
    # 429 reject
    s.arrow("rl", "L", "user", "R", color="#e03131", width=1.5, dashed=True,
            label="429 if over")
    # ---- backing services ----
    for tgt in ["conv", "redis", "vec"]:
        s.arrow("orch", "R", tgt, "T", color=GRAY, width=1.5, dashed=True,
                waypoints=[(830, 359)])
    return s


def build_two_fleets():
    s = Scene()
    s.text("The Big Idea: Two Fleets in Tension", 40, 34, size=28, color=INK, family=1)
    s.text("Every quirk of ChatGPT & Claude — slowness, forgetting, cost — flows from this split.",
           40, 78, size=15, color="#495057", family=1)

    # web tier (left)
    s.lane("WEB / API TIER", 60, 140, 360, 320, CLR["edge"][0], CLR["edge"][2])
    s.text("stateless · scales in SECONDS · cheap · ~infinite", 78, 168,
           size=14, color="#2b8a3e", family=1)
    web = [("edge2", "Edge / CDN"), ("gw2", "API gateway + auth"),
           ("rl2", "Rate limiter (RPM/TPM)"), ("orch2", "Orchestrator")]
    for i, (nid, lbl) in enumerate(web):
        s.node(nid, lbl, 95, 205 + i * 60, 290, 46, CLR["edge"][0], CLR["edge"][1], size=15)
    for a, b in [("edge2", "gw2"), ("gw2", "rl2"), ("rl2", "orch2")]:
        s.arrow(a, "B", b, "T", color=INK)

    # gpu tier (right)
    s.lane("GPU INFERENCE TIER", 620, 140, 360, 320, CLR["infra"][0], CLR["infra"][2])
    s.text("stateful · scales in MINUTES · $$$ · hard-capped by physical GPUs", 638, 168,
           size=13, color="#c92a2a", family=1)
    gpu = [("sch2", "Continuous batching scheduler"), ("pf2", "PREFILL — compute-bound"),
           ("dec2", "DECODE — memory-bound"), ("kv2", "KV cache (PagedAttention)")]
    for i, (nid, lbl) in enumerate(gpu):
        s.node(nid, lbl, 655, 205 + i * 60, 290, 46, CLR["infra"][0], CLR["infra"][1], size=14, strokeWidth=3)
    for a, b in [("sch2", "pf2"), ("pf2", "dec2"), ("dec2", "kv2")]:
        s.arrow(a, "B", b, "T", color=INK)

    # the tension
    s.arrow("orch2", "R", "sch2", "L", color=PURPLE, width=3, label="requests →")
    s.arrow("dec2", "L", "orch2", "R", color=ORANGE, width=3,
            waypoints=[(540, 470), (540, 470)], label="← tokens stream back")
    return s


if __name__ == "__main__":
    print("Generating Excalidraw scenes:")
    build_hero().dump(os.path.join(OUT_DIR, "chatgpt-claude-hero.excalidraw"))
    build_two_fleets().dump(os.path.join(OUT_DIR, "chatgpt-claude-two-fleets.excalidraw"))
    print("Done. Open in https://excalidraw.com (File ▸ Open) to refine + export.")
