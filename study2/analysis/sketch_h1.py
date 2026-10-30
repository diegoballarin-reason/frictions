"""Sketch of plate 2, panel 4 (for discussion): session prices against the other numbers (H1), one row per app,
with Diego's titles for the three apps. Black and white, from the exported data (answers.csv, figures.csv, claims.csv)."""
import csv, math, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

D, OUT = sys.argv[1], sys.argv[2]
for f in fm.findSystemFonts():
    if "Inter" in f:
        fm.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Inter", "font.size": 8.5, "axes.linewidth": 0.6})
A = list(csv.DictReader(open(f"{D}/answers.csv", encoding="utf-8")))
F = list(csv.DictReader(open(f"{D}/figures.csv", encoding="utf-8")))
C = list(csv.DictReader(open(f"{D}/claims.csv", encoding="utf-8")))
GA = ("other_sessions", "outside_and_intraday", "history", "premise_hypothesis")
TITLES = {"ChatGPT": "The sun is yellow!", "Claude": "To know means to be mistaken.", "Gemini": "I am always ready – until I'm not."}

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)

fig = plt.figure(figsize=(11, 6.2), dpi=150)
fig.text(0.05, 0.94, "Plate 2 · panel 4 (sketch for discussion): session prices and the other numbers", fontsize=13, weight="bold")
fig.text(0.05, 0.885, "Share of wrong figures in the 217 pre-registered answers.   ○ prices of the session asked about   ● other numbers that can be checked   — 95% interval\n"
         "Other numbers: other sessions, pre-market, after-hours and moments of the day, comparisons with history, hypotheses on the false premise (figures only).",
         fontsize=7.5, color="#333")
ax = fig.add_axes([0.30, 0.14, 0.42, 0.70])
rows = ["ChatGPT", "Claude", "Gemini"]
info = {}
for i, app in enumerate(rows):
    y = 2 - i
    pre = [r for r in A if r["app"] == app and r["study"] == "preregistered"]
    sp = [f for f in F if f["app"] == app and f["study"] == "preregistered"]
    k1, n1 = sum(f["outcome"] == "error" for f in sp), len(sp)
    ga = [c for c in C if c["app"] == app and c["type"] in GA and c["in_words"] == "no"]
    v = [c for c in ga if c["outcome"] in ("right", "wrong")]
    k2, n2 = sum(c["outcome"] == "wrong" for c in v), len(v)
    for k, n, mk, dy in ((k1, n1, "o", 0.12), (k2, n2, "o", -0.12)):
        lo, hi = wilson(k, n)
        ax.plot([lo, hi], [y + dy, y + dy], color="#000", lw=0.8)
        if dy > 0:
            ax.scatter([100 * k / n], [y + dy], s=42, facecolor="#fff", edgecolor="#000", lw=1, zorder=3)
        else:
            ax.scatter([100 * k / n], [y + dy], s=42, color="#000", zorder=3)
        ax.text(hi + 0.8, y + dy, f"{k}/{n}", va="center", fontsize=7.5, color="#333")
    info[app] = (len(pre), len(ga), k2)
    fig.text(0.05, 0.14 + 0.70 * (y + 0.5) / 3 + 0.02, app, fontsize=10, weight="bold", va="center")
    fig.text(0.05, 0.14 + 0.70 * (y + 0.5) / 3 - 0.025, TITLES[app], fontsize=9, style="italic", va="center")
    fig.text(0.75, 0.14 + 0.70 * (y + 0.5) / 3, f"{len(ga) / len(pre):.1f} other numbers per answer\n{k2 / len(pre):.2f} wrong per answer",
             fontsize=8.5, va="center")
ax.set_ylim(-0.5, 2.5)
ax.set_xlim(0, 35)
ax.set_yticks([])
ax.set_xlabel("% of figures wrong", fontsize=8)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.text(0.05, 0.04, "Titles: Diego. Per answer: answers of the pre-registered rounds, refusals included (Gemini: 49).", fontsize=7, color="#555")
fig.savefig(OUT)
print(info)
