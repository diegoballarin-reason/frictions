"""Sketch of plate 2 for discussion (not the plate): three panels from the exported data, black and white."""
import csv
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle

D = sys.argv[1]
OUT = sys.argv[2]
for f in fm.findSystemFonts():
    if "Inter" in f:
        fm.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Inter", "font.size": 8.5, "axes.linewidth": 0.6, "svg.fonttype": "none"})

A = list(csv.DictReader(open(f"{D}/answers.csv", encoding="utf-8")))
F = list(csv.DictReader(open(f"{D}/figures.csv", encoding="utf-8")))
E = {r["event"]: r for r in csv.DictReader(open(f"{D}/events.csv", encoding="utf-8"))}
NAMES = {"C": "Citigroup", "LRCX": "Lam Research", "GM": "General Motors", "META": "Meta", "CMG": "Chipotle", "MU": "Micron",
         "HAS": "Hasbro", "LMT": "Lockheed Martin", "IP": "International Paper", "CCI": "Crown Castle", "DDOG": "Datadog", "GFS": "GlobalFoundries"}
MON = {"10": "Oct"}

fig = plt.figure(figsize=(11, 15.5), dpi=150)
fig.text(0.05, 0.975, "Plate 2 · title to decide (sketch for discussion; data confirmed on 30 October 2026)", fontsize=13, weight="bold")
fig.text(0.05, 0.962, "Thesis sentence: Diego's", fontsize=9, color="#555")

# ── panel 1: every answer ────────────────────────────────────────────────────
ax = fig.add_axes([0.05, 0.585, 0.92, 0.355])
ax.set_axis_off()
COLS = [("ChatGPT", "A", "1"), ("ChatGPT", "A", "2"), ("ChatGPT", "A", "3"), ("ChatGPT", "C", "1"), ("ChatGPT", "C", "2"), None,
        ("Claude", "A", "1"), ("Claude", "A", "2"), ("Claude", "A", "3"), ("Claude", "C", "1"), ("Claude", "C", "2"), None,
        ("Gemini", "A", "1"), ("Gemini", "A", "2"), ("Gemini", "A", "3"), ("Gemini", "A", "E1"), ("Gemini", "A", "E2"), ("Gemini", "A", "E3"), ("Gemini", "A", "E4"),
        ("Gemini", "C", "1"), ("Gemini", "C", "E3"), ("Gemini", "C", "E4")]
cell = defaultdict(list)
for r in A:
    if r["type"] == "U":
        continue
    key = r["round"] if r["study"] == "exploration" else r["repetition"]
    cell[(r["app"], r["type"], key, r["event"])].append(r)
x0, cw, rh = 0.30, 0.0305, 1 / 14
xs = []
x = x0
for c in COLS:
    if c is None:
        x += cw * 0.6
        xs.append(None)
        continue
    xs.append(x)
    x += cw
for i, c in enumerate(COLS):
    if c is None:
        continue
    ax.text(xs[i], 1 - 0.4 * rh, c[1] + ("" if c[2].startswith("E") else c[2]) + (c[2] if c[2].startswith("E") else ""),
            ha="center", va="center", fontsize=7, color="#555")
for app in ("ChatGPT", "Claude", "Gemini"):
    idx = [i for i, c in enumerate(COLS) if c and c[0] == app]
    ax.text((xs[idx[0]] + xs[idx[-1]]) / 2, 1 + 0.25 * rh, app, ha="center", va="center", fontsize=9, weight="bold")
gx = [xs[i] for i, c in enumerate(COLS) if c and c[0] == "Gemini" and c[2].startswith("E")]
ax.plot([min(gx) - cw / 2, max(gx) + cw / 2], [1 - 0.85 * rh] * 2, color="#000", lw=0.5)


def glyph(ax, x, y, r):
    s = 70
    if r["refused"] == "yes":
        ax.plot([x - 0.008, x + 0.008], [y, y], color="#000", lw=1.2)
        return
    p = r["prices"]
    if p == "exact":
        ax.scatter([x], [y], s=s, marker="o", color="#000")
    elif p == "minimal_gaps":
        ax.scatter([x], [y], s=s, marker="o", color="#888")
    elif p == "approximate_correct":
        ax.scatter([x], [y], s=s, marker="o", facecolor="#fff", edgecolor="#000", lw=1)
    elif p == "with_errors":
        ax.scatter([x], [y], s=s * 0.9, marker="x", color="#000", lw=1.6)
    elif p == "none_given":
        ax.scatter([x], [y], s=s * 0.5, marker="o", facecolor="#fff", edgecolor="#999", lw=0.8, linestyle=":")
    if r["type"] == "C" and r["premise"] == "adopted":
        ax.scatter([x + 0.011], [y + 0.022], s=26, marker="^", color="#000")
    if r["contestable"] == "yes":
        ax.text(x + 0.012, y - 0.024, "◊", fontsize=7)


for j, ev in enumerate(sorted(E)):
    y = 1 - (j + 1.4) * rh
    e = E[ev]
    d = e["session"][8:10].lstrip("0")
    ax.text(0, y, f"{ev}  {NAMES[e['ticker']]}", va="center", fontsize=8.5, weight="bold")
    ax.text(0.205, y, f"{d} Oct  {float(e['change_close_pct']):+.2f}%".replace("-", "−"), va="center", fontsize=8, color="#333")
    for i, c in enumerate(COLS):
        if c is None:
            continue
        rs = cell.get((c[0], c[1], c[2], ev), [])
        for k, r in enumerate(rs):
            glyph(ax, xs[i] + (k - (len(rs) - 1) / 2) * 0.012, y, r)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.05)
fig.text(0.05, 0.575, "Every answer to A (how did the stock react?) and C (false premise). "
         "●  exact   ○  approximate, correct   ●(grey)  minimal gaps   ×  with errors   –  refusal   ▲  false premise adopted   ◊  accepted by convention",
         fontsize=7.5, color="#333")

# ── panel 2: every figure, by its distance from the record ──────────────────
ax2 = fig.add_axes([0.13, 0.30, 0.82, 0.22])
TH = {"open": 0.13, "close": 0.13, "high": 0.13, "low": 0.13, "previous_close": 0.13, "change_close_usd": 0.13, "volume": 0.10,
      "change_close_pct": 0.14, "change_open_pct": 0.14, "change_high_pct": 0.14, "change_low_pct": 0.14}
REF = {"open": "open_nasdaq", "close": "close", "high": "high", "low": "low", "previous_close": "previous_close", "volume": "volume_nasdaq",
       "change_close_pct": "change_close_pct", "change_open_pct": "change_open_pct", "change_high_pct": "change_high_pct", "change_low_pct": "change_low_pct"}
import math
pts = defaultdict(list)
for f in F:
    q = f["quantity"]
    if q not in TH or f["value_low"] != f["value_high"]:
        continue
    e = E[f["event"]]
    v = float(f["value_low"])
    if q == "change_close_usd":
        ref = float(e["close"]) - float(e["previous_close"])
        gap = abs(v - ref) / float(e["previous_close"]) * 100
    else:
        ref = float(e[REF[q]])
        gap = abs(v - ref) if q.endswith("pct") else abs(v / ref - 1) * 100
    if q == "open" and abs(abs(v - ref) - 0.005) < 1e-6:
        gap = 0.0
    n = gap / TH[q]
    pts[f["app"]].append((n, f["outcome"]))
rows = ["ChatGPT", "Claude", "Gemini"]
import random
random.seed(1)
for i, app in enumerate(rows):
    y0 = 2 - i
    for n, o in pts[app]:
        xv = max(n, 0.004)
        jit = (random.random() - 0.5) * 0.6
        if o == "error":
            ax2.scatter([xv], [y0 + jit], s=22, marker="x", color="#000", lw=1.2, zorder=3)
        elif o in ("approximate_correct",):
            ax2.scatter([xv], [y0 + jit], s=9, facecolor="#fff", edgecolor="#000", lw=0.5)
        else:
            ax2.scatter([xv], [y0 + jit], s=6, color="#000" if o == "exact" else "#777", lw=0)
    ax2.text(0.0022, y0, app, ha="right", va="center", fontsize=9, weight="bold")
ax2.set_xscale("log")
ax2.set_xlim(0.003, 300)
ax2.set_ylim(-0.6, 2.6)
ax2.set_yticks([])
ax2.axvline(1, color="#000", lw=0.8)
ax2.axvline(1 / 0.13, color="#000", lw=0.5, ls=(0, (2, 2)))
ax2.set_xticks([0.004, 0.01, 0.1, 1, 10, 100])
ax2.set_xticklabels(["equal", "0.01", "0.1", "1 = minimal gap", "10", "100"])
for s in ("top", "right", "left"):
    ax2.spines[s].set_visible(False)
ax2.set_xlabel("distance from the record, in minimal gaps (0.13% for prices, 0.14 points for changes, 0.1% for volume); "
               "the dashed line is the tolerance for «about»", fontsize=7.5)
fig.text(0.05, 0.535, f"Every figure about the session in all scored answers, A, C and U, exploration included ({sum(len(v) for v in pts.values())} single figures; ranges left out)",
         fontsize=8.5, weight="bold")

# ── panel 3: Gemini, by the time in New York ────────────────────────────────
ax3 = fig.add_axes([0.13, 0.06, 0.82, 0.17])
g = [r for r in A if r["app"] == "Gemini"]
for r in g:
    t = r["sent_new_york"][11:16]
    h = int(t[:2]) + int(t[3:]) / 60
    y = {"A": 2, "C": 1, "U": 0}[r["type"]] + (random.random() - 0.5) * 0.5
    if r["refused"] == "yes":
        ax3.scatter([h], [y], s=26, facecolor="#fff", edgecolor="#000", lw=0.9, zorder=3)
    else:
        ax3.scatter([h], [y], s=18, color="#000", zorder=3)
ax3.add_patch(Rectangle((13 + 20 / 60, -0.6), (15 + 26 / 60) - (13 + 20 / 60), 3.2, facecolor="#e6e6e6", edgecolor="none", zorder=0))
ax3.set_xlim(0, 24)
ax3.set_ylim(-0.6, 2.6)
ax3.set_xticks(range(0, 25, 3))
ax3.set_xticklabels([f"{h:02d}:00" for h in range(0, 25, 3)])
ax3.set_yticks([0, 1, 2])
ax3.set_yticklabels(["U", "C", "A"])
for s in ("top", "right"):
    ax3.spines[s].set_visible(False)
ax3.set_xlabel("time in New York when the question was sent (25–28 October)", fontsize=7.5)
fig.text(0.05, 0.245, f"Gemini, all {len(g)} answers by the hour in New York:  ●  with data   ○  refusal   (grey band: 13:20–15:26, where refusals gathered)",
         fontsize=8.5, weight="bold")
fig.savefig(OUT)
print("ok", {k: len(v) for k, v in pts.items()})
