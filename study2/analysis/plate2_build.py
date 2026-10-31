"""Build plate 2 of 'nothing to notice it by' as a page of diegoballarin.com.

Four panels, all placed from the final data of study 2 (study2/data):
  1. every answer to A (how did the stock react?) and C (the same with a false premise), one mark each;
  2. every single figure about the session in the scored answers, A, C and U, by its distance from the exchange's record;
  3. Gemini's answers by the hour they were sent, in New York;
  4. for each app, the share of wrong figures among the session's prices and among the other numbers that can be checked (H1).
Nothing is typed by hand except the words; every count in the text is computed here.

Usage: plate2_build.py DATA_DIR CHROME_PAGE OUT_HTML
  DATA_DIR     study2/data (events.csv, answers.csv, figures.csv, claims.csv)
  CHROME_PAGE  the case study page, whose head, menus and colophon styles are reused
"""
import csv
import html
import math
import re
import sys
from collections import Counter, defaultdict

data_dir, chrome_path, out_path = sys.argv[1:4]
A = list(csv.DictReader(open(f"{data_dir}/answers.csv", encoding="utf-8")))
F = list(csv.DictReader(open(f"{data_dir}/figures.csv", encoding="utf-8")))
E = {r["event"]: r for r in csv.DictReader(open(f"{data_dir}/events.csv", encoding="utf-8"))}
CL = list(csv.DictReader(open(f"{data_dir}/claims.csv", encoding="utf-8")))
EVS = sorted(E)

NAMES = {"C": "Citigroup", "LRCX": "Lam Research", "GM": "General Motors", "META": "Meta", "CMG": "Chipotle", "MU": "Micron",
         "HAS": "Hasbro", "LMT": "Lockheed Martin", "IP": "International Paper", "CCI": "Crown Castle", "DDOG": "Datadog",
         "GFS": "GlobalFoundries"}
APPS = ("ChatGPT", "Claude", "Gemini")


def esc(s):
    return html.escape(str(s), quote=True)


def num(v, d=2, sign=True):
    s = f"{v:+.{d}f}" if sign else f"{v:.{d}f}"
    return s.replace("-", "\u2212")


def day(iso):
    return f"{int(iso[8:10])} Oct"


# ── counts used in the words ────────────────────────────────────────────────
S = [r for r in A if r["scored"] == "yes"]
AP = [r for r in S if r["type"] == "A" and r["prices"] != "none_given"]
N_AP, N_AP_RIGHT, N_AP_ERR = len(AP), sum(r["direction"] == "right" for r in AP), sum(r["prices"] == "with_errors" for r in AP)
CC = [r for r in S if r["type"] == "C"]
N_C, N_C_CORR = len(CC), sum(r["premise"] == "corrected" for r in CC)
GEM = [r for r in A if r["app"] == "Gemini"]
GEM_PRE_A = [r for r in A if r["app"] == "Gemini" and r["study"] == "preregistered" and r["type"] == "A"]
N_GEM_PRE_A, N_GEM_PRE_REF = len(GEM_PRE_A), sum(r["refused"] == "yes" for r in GEM_PRE_A)
assert N_AP_RIGHT == N_AP
PRE = [r for r in A if r["study"] == "preregistered"]
PRE_AP = [r for r in PRE if r["type"] == "A" and r["prices"] != "none_given"]
assert all(r["direction"] == "right" for r in PRE_AP)


def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 0.0)
    p, d = k / n, 1 + z * z / n
    c, h = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h) * 100, min(1.0, c + h) * 100)


H1_TYPES = ("other_sessions", "outside_and_intraday", "history", "premise_hypothesis")
H1 = [c for c in CL if c["type"] in H1_TYPES and c["in_words"] == "no"]   # numbers in words stay out, as in the pilot
P4 = {}
for app in APPS:
    n_ans = sum(r["app"] == app for r in PRE)
    sp = [f for f in F if f["study"] == "preregistered" and f["app"] == app]
    ot = [c for c in H1 if c["app"] == app and c["outcome"] in ("right", "wrong")]
    P4[app] = {"sp": (sum(f["outcome"] == "error" for f in sp), len(sp)), "ot": (sum(c["outcome"] == "wrong" for c in ot), len(ot)),
               "per": sum(c["app"] == app for c in H1) / n_ans, "wper": sum(c["outcome"] == "wrong" for c in ot) / n_ans,
               "c_rate": (lambda x: (sum(c["outcome"] == "wrong" for c in x), len(x)))([c for c in ot if c["question_type"] == "C"]),
               "a_rate": (lambda x: (sum(c["outcome"] == "wrong" for c in x), len(x)))([c for c in ot if c["question_type"] == "A"])}
SP_W, SP_N = sum(P4[a]["sp"][0] for a in APPS), sum(P4[a]["sp"][1] for a in APPS)
H_W, H_N = sum(P4[a]["ot"][0] for a in APPS), sum(P4[a]["ot"][1] for a in APPS)
N_PRE = len(PRE)
GM_OPEN = sorted({f["answer_id"] for f in F if f["event"] == "03" and f["quantity"] == "open" and f["outcome"] == "error" and f["app"] == "ChatGPT"})
GEM_NOSEARCH = sum(r["app"] == "Gemini" and r["search"] == "unavailable" for r in PRE)
GEM_ADOPT = sum(r["app"] == "Gemini" and r["premise"] == "adopted" for r in PRE)
assert (SP_W, SP_N, H_W, H_N) == (28, 1040, 54, 408) and len(GM_OPEN) == 3
# Claude's wrong other numbers: how many come from the right figure at the wrong moment (the origin recorded for their answer),
# and how many recur, the same figure wrong in another of its answers on the same session
HA = list(csv.DictReader(open(f"{data_dir}/answers_h1.csv", encoding="utf-8")))
CW = [c for c in H1 if c["app"] == "Claude" and c["outcome"] == "wrong"]
N_MOMENT = sum(int(r["wrong"] or 0) for r in HA if r["app"] == "Claude" and r["origin_it"] in ("istantanea fuori tempo", "momento sbagliato"))
_NUM = re.compile(r"\d+(?:[.,]\d+)*")


def _toks(c):
    return set(_NUM.findall(c["quote_it"])) - {str(y) for y in range(2000, 2031)}


N_RECUR = sum(any(c["event"] == d["event"] and d["answer_id"] != c["answer_id"] and _toks(c) & _toks(d) for d in CW) for c in CW)
assert len(CW) == 41 and 0.4 <= N_MOMENT / len(CW) <= 0.6 and 0.5 < N_RECUR / len(CW) < 0.66, (N_MOMENT, N_RECUR)

def fmt_n(n):
    return f"{n:,}"


def pct(kn):
    return f"{100 * kn[0] / kn[1]:.1f}"


# ── panel 1: every answer ───────────────────────────────────────────────────
BLOCKS = [
    ("ChatGPT", "", [("A", "1"), ("A", "2"), ("A", "3"), ("C", "1"), ("C", "2")]),
    ("Claude", "", [("A", "1"), ("A", "2"), ("A", "3"), ("C", "1"), ("C", "2")]),
    ("Gemini", "", [("A", "1"), ("A", "2"), ("A", "3"), ("C", "1")]),
    ("Gemini", "exploration", [("A", "E1"), ("A", "E2"), ("A", "E3"), ("A", "E4"), ("C", "E3"), ("C", "E4")]),
]
CELL = defaultdict(list)
for r in A:
    if r["type"] == "U":
        continue
    key = r["round"] if r["study"] == "exploration" else r["repetition"]
    CELL[(r["app"], r["study"] == "exploration", r["type"], key, r["event"])].append(r)

OUT_WORD = {"exact": "exact", "minimal_gaps": "minimal gaps", "approximate_correct": "approximate, correct",
            "with_errors": "with errors", "none_given": "no prices"}


def glyph(x, y, r):
    """One answer. The mark says how its session prices compare with the record."""
    who = f"{r['app']}, {r['ticker']}, {r['type']}{'' if r['study'] == 'exploration' else ' ' + r['repetition']}"
    if r["study"] == "exploration":
        who += f", block {r['round']}"
    if r["refused"] == "yes":
        t, g = f"{who}: no prices, it said it had none", f'<line class="g-ref" x1="{x - 6:.1f}" y1="{y:.1f}" x2="{x + 6:.1f}" y2="{y:.1f}"/>'
    elif r["type"] == "C" and r["premise"] == "adopted":
        t = f"{who}: took up the false premise"
        g = f'<path class="g-prem" d="M{x:.1f} {y - 7:.1f} L{x + 6.5:.1f} {y + 5:.1f} L{x - 6.5:.1f} {y + 5:.1f} Z"/>'
    else:
        p = r["prices"]
        t = f"{who}: {OUT_WORD[p]}" + (", premise corrected" if r["type"] == "C" else "")
        if p == "exact":
            g = f'<circle class="g-ex" cx="{x:.1f}" cy="{y:.1f}" r="5.6"/>'
        elif p == "minimal_gaps":
            g = f'<circle class="g-min" cx="{x:.1f}" cy="{y:.1f}" r="5.6"/>'
        elif p == "approximate_correct":
            g = f'<circle class="g-app" cx="{x:.1f}" cy="{y:.1f}" r="5"/>'
        else:
            g = (f'<path class="g-err" d="M{x - 5:.1f} {y - 5:.1f} L{x + 5:.1f} {y + 5:.1f} M{x + 5:.1f} {y - 5:.1f} L{x - 5:.1f} {y + 5:.1f}"/>')
    if r["contestable"] == "yes":
        g += f'<path class="g-con" d="M{x + 9:.1f} {y - 10:.1f} l3 3 l-3 3 l-3 -3 Z"/>'
        t += "; one figure accepted by convention"
    return f"<g><title>{esc(t)}</title>{g}</g>"


def panel1(wide=True, block=None):
    """wide: one svg with the events on the left; narrow: one svg per block, tickers only."""
    CW, RH, GAP, TOP = 32, 30, 26, 58
    LW = 300 if wide else 54
    blocks = BLOCKS if block is None else [BLOCKS[block]]
    width = LW + sum(len(b[2]) for b in blocks) * CW + (len(blocks) - 1) * GAP + 8
    height = TOP + len(EVS) * RH + 6
    s = [f'<svg class="p1" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(P1_LABEL)}">']
    # event labels
    for i, ev in enumerate(EVS):
        y = TOP + i * RH + RH / 2
        e = E[ev]
        s.append(f'<line class="rule" x1="0" y1="{y + RH / 2:.1f}" x2="{width - 8}" y2="{y + RH / 2:.1f}"/>')
        s.append(f'<text class="tk" x="0" y="{y + 4.5:.1f}">{e["ticker"]}</text>')
        if wide:
            s.append(f'<text class="nm" x="54" y="{y + 4.5:.1f}">{esc(NAMES[e["ticker"]])}</text>')
            s.append(f'<text class="dt" x="186" y="{y + 4.5:.1f}">{day(e["session"])}</text>')
            s.append(f'<text class="mv" x="{LW - 14}" y="{y + 4.5:.1f}">{num(float(e["change_close_pct"]))}%</text>')
    if wide:
        s.append(f'<text class="hd" x="0" y="{TOP - 12}">session</text><text class="hd end" x="{LW - 14}" y="{TOP - 12}">close</text>')
    x = LW
    for app, kind, cols in blocks:
        x0 = x
        for j, (typ, key) in enumerate(cols):
            cx = x + j * CW + CW / 2
            lab = f"{typ}{'' if key.startswith('E') else key}"
            sub = key if key.startswith("E") else ""
            s.append(f'<text class="col" x="{cx:.1f}" y="{TOP - 12}">{lab}</text>')
            if sub:
                s.append(f'<text class="col sub" x="{cx:.1f}" y="{TOP - 1}">{sub}</text>')
            for i, ev in enumerate(EVS):
                y = TOP + i * RH + RH / 2
                rs = CELL.get((app, kind == "exploration", typ, key, ev), [])
                if not rs:
                    s.append(f'<circle class="g-none" cx="{cx:.1f}" cy="{y:.1f}" r="1.2"/>')
                for k, r in enumerate(rs):
                    s.append(glyph(cx + (k - (len(rs) - 1) / 2) * 13, y, r))
        x1 = x + len(cols) * CW
        name = app + (" · exploration" if kind else "")
        s.append(f'<text class="app" x="{x0 + 2:.1f}" y="14">{esc(name)}</text>')
        s.append(f'<line class="bar" x1="{x0 + 2:.1f}" y1="22" x2="{x1 - 2:.1f}" y2="22"/>')
        # the C columns are set off by a hairline
        jc = next(j for j, c in enumerate(cols) if c[0] == "C")
        xc = x + jc * CW
        s.append(f'<line class="split" x1="{xc:.1f}" y1="{TOP - 26}" x2="{xc:.1f}" y2="{height - 4}"/>')
        x = x1 + GAP
    s.append("</svg>")
    return "".join(s)


P1_LABEL = (f"One mark for each of {sum(len(v) for v in CELL.values())} answers, by session, app and question. "
            f"All {N_AP} answers to A that quoted the session's prices gave the right direction; {N_AP_ERR} had at least one price off the record. "
            f"Of {N_C} answers to C, {N_C_CORR} corrected the false premise. Gemini declined to give prices in {N_GEM_PRE_REF} of its {N_GEM_PRE_A} pre-registered A answers.")

# ── panel 2: every figure, by its distance from the record ──────────────────
PRICE = {"open": "open_nasdaq", "close": "close", "high": "high", "low": "low", "previous_close": "previous_close", "volume": "volume_nasdaq"}
PCT = {"change_close_pct", "change_open_pct", "change_high_pct", "change_low_pct"}
NUMRE = re.compile(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?")


def truth(e, q):
    if q in PRICE:
        return float(e[PRICE[q]]) if e[PRICE[q]] != "" else None
    if q in PCT:
        return float(e[q])
    if q == "change_close_usd":
        return float(e["close"]) - float(e["previous_close"])
    return None


def written_places(f):
    """decimal places as written in the answer (77,00 has two), from the quoted words."""
    v = abs(float(f["value_low"]))
    for m in NUMRE.finditer(f["quote_it"]):
        s = m.group(0)
        x = float(s.replace(".", "").replace(",", "."))
        frac = len(s.split(",")[1]) if "," in s else 0
        for p10 in (0, 3, 6, 9):
            if abs(x * 10 ** p10 - v) <= 1e-6 * max(1.0, v):
                return frac - p10
    return None


def minimal(q):
    return 0.14 if q in PCT else 0.10 if q == "volume" else 0.13


EQUAL = Counter()
OFF = defaultdict(list)
BOUND = Counter()  # «more than 8 per cent», «reached 28.25»: right or wrong, but no single distance
BOUND_RE = re.compile(r"oltre|più di|superior|inferior|almeno|sotto")
for f in F:
    q, e = f["quantity"], E[f["event"]]
    if f["value_low"] != f["value_high"] or q.startswith("level"):
        continue
    t = truth(e, q)
    if t is None:
        continue
    if f["outcome"] == "level_in_session_correct" or (BOUND_RE.search(f["qualifier_it"]) and f["outcome"] != "error"):
        BOUND[f["app"]] += 1
        continue
    v = float(f["value_low"])
    p = written_places(f)
    if p is None:
        p = len(f["value_low"].split(".")[1]) if "." in f["value_low"] else 0
    half = q == "open" and round(t * 1000) % 10 == 5 and abs(abs(v - t) - 0.005) < 1e-6
    if abs(round(t, p) - v) < 1e-9 or half:
        EQUAL[f["app"]] += 1
        continue
    g = abs(v - t) if q in PCT else abs(v - t) / float(e["previous_close"]) * 100 if q == "change_close_usd" else abs(v / t - 1) * 100
    OFF[f["app"]].append((g / minimal(q), f))
N_EQUAL = sum(EQUAL.values())
N_OFF = sum(len(v) for v in OFF.values())
N_BOUND = sum(BOUND.values())
N_SINGLE = N_EQUAL + N_OFF + N_BOUND
ERR_PRICE = sorted(abs(float(f["value_low"]) / truth(E[f["event"]], f["quantity"]) - 1) * 100
                   for f in F if f["outcome"] == "error" and f["quantity"] in PRICE and f["quantity"] != "volume" and f["value_low"] == f["value_high"])

LOG_LO, LOG_HI = -2.35, 3.05   # below 0.01 of a gap (volumes a few shares off) the marks gather at the left, packed


def swarm(pts, X, yc, R, gap=0.6):
    """place marks along x, stacking alternately above and below the line where they would touch;
    the few under 0.01 of a gap are packed in a small block left of the 0.01 tick."""
    placed, out = [], []
    tiny = [p for p in pts if p[0] < 0.01]
    rows = max(1, min(3, len(tiny)))
    for k, (n_, f) in enumerate(tiny):
        c, r = k // rows, k % rows
        x, y = X(0.01) - 8 - c * (2 * R + gap), yc + (r - (rows - 1) / 2) * (2 * R + gap)
        placed.append((x, y)); out.append((x, y, n_, f))
    for n_, f in [p for p in pts if p[0] >= 0.01]:
        x = X(max(n_, 10 ** LOG_LO))
        dy, k = 0.0, 0
        while any((x - px) ** 2 + (yc + dy - py) ** 2 < (2 * R + gap) ** 2 for px, py in placed):
            k += 1
            dy = (k + 1) // 2 * (2 * R + gap) * (1 if k % 2 else -1)
        placed.append((x, yc + dy))
        out.append((x, yc + dy, n_, f))
    return out


def mark2(app, x, y, n_, f, R):
    o = f["outcome"]
    what = (f"{app}, {E[f['event']]['ticker']}: «{f['quote_it'][:90]}» — "
            f"{n_ * minimal(f['quantity']):.2f}{' points' if f['quantity'] in PCT else '%'} off the record ({o.replace('_', ' ')})")
    c = R + 0.2
    if o == "error":
        g = f'<path class="g-err" d="M{x - c:.1f} {y - c:.1f} L{x + c:.1f} {y + c:.1f} M{x + c:.1f} {y - c:.1f} L{x - c:.1f} {y + c:.1f}"/>'
    elif o == "accepted_rule3" or (f["quantity"] == "volume" and n_ > 10):
        g = f'<path class="g-con" d="M{x:.1f} {y - c - 0.6:.1f} l{c + 0.6:.1f} {c + 0.6:.1f} l{-c - 0.6:.1f} {c + 0.6:.1f} l{-c - 0.6:.1f} {-c - 0.6:.1f} Z"/>'
    elif o in ("exact", "minimal_gap"):
        g = f'<circle class="g-min" cx="{x:.1f}" cy="{y:.1f}" r="{R}"/>'
    else:
        g = f'<circle class="g-app" cx="{x:.1f}" cy="{y:.1f}" r="{R - 0.4}"/>'
    return f"<g><title>{esc(what)}</title>{g}</g>"


def units(n, x0, y0, cols, sz):
    return "".join(f'<rect class="u" x="{x0 + (k % cols) * sz:.1f}" y="{y0 + (k // cols) * sz:.1f}" width="{sz - 1.4:.1f}" height="{sz - 1.4:.1f}"/>'
                   for k in range(n))


def panel2(wide=True):
    """wide: each app on one line, the equal figures as a block at the left of the scale.
    narrow: each app stacked, the block above its own strip."""
    W = 940 if wide else 400
    R = 3.4 if wide else 3.0
    if wide:
        RH, UNIT_W = 132, 168
        AX0, AX1 = UNIT_W + 34, W - 10
    else:
        RH, AX0, AX1 = 178, 6, W - 6

    def X(n):
        return AX0 + (math.log10(n) - LOG_LO) / (LOG_HI - LOG_LO) * (AX1 - AX0)

    top = 26
    s = [f'<svg class="p2" viewBox="0 0 {W} {len(APPS) * RH + top + (52 if wide else 80)}" role="img" aria-label="{esc(P2_LABEL)}">']
    for n_, cls, lab, anchor in ((1, "thr", "minimal gap", "end"), (1 / 0.13, "thr tol", "“about”", "start")):
        x = X(n_)
        dx = -5 if anchor == "end" else 5
        s.append(f'<text class="thl {anchor}" x="{x + dx:.1f}" y="{top - 9}">{lab}</text>')
    for i, app in enumerate(APPS):
        y0 = top + i * RH
        pts = sorted(OFF[app], key=lambda p: p[0])
        n_eq = EQUAL[app]
        if wide:
            yc = y0 + RH / 2
            cols, sz = 24, 5.2
            rows = math.ceil(n_eq / cols)
            by = yc - rows * sz / 2 + 8
            s.append(f'<text class="app" x="0" y="{y0 + 16:.1f}">{app}</text>')
            s.append(units(n_eq, 0, by, cols, sz))
            s.append(f'<text class="cnt" x="0" y="{by + rows * sz + 12:.1f}">{n_eq} equal</text>')
            s.append(f'<text class="cnt end" x="{AX1}" y="{y0 + 16:.1f}">{len(pts)} not equal</text>')
            ys, ye = y0 + 4, y0 + RH
        else:
            cols, sz = 50, (W - 12) / 50
            rows = math.ceil(n_eq / cols)
            s.append(f'<text class="app" x="0" y="{y0 + 14:.1f}">{app}</text>')
            s.append(f'<text class="cnt end" x="{W}" y="{y0 + 14:.1f}">{n_eq} equal · {len(pts)} not</text>')
            s.append(units(n_eq, 0, y0 + 24, cols, sz))
            ys = y0 + 24 + rows * sz + 10
            ye = y0 + RH - 2
            yc = (ys + ye) / 2
        for n_, cls in ((1, "thr"), (1 / 0.13, "thr tol")):
            x = X(n_)
            s.append(f'<line class="{cls}" x1="{x:.1f}" y1="{ys:.1f}" x2="{x:.1f}" y2="{ye:.1f}"/>')
        for x, y, n_, f in swarm(pts, X, yc, R):
            s.append(mark2(app, x, y, n_, f, R))
        s.append(f'<line class="rule" x1="0" y1="{y0 + RH:.1f}" x2="{W}" y2="{y0 + RH:.1f}"/>')
    ya = top + len(APPS) * RH
    s.append(f'<line class="axis" x1="{AX0}" y1="{ya}" x2="{AX1}" y2="{ya}"/>')
    for n_, lab in ((0.01, "0.01"), (0.1, "0.1"), (1, "1"), (10, "10"), (100, "100"), (1000, "1000")):
        x = X(n_)
        s.append(f'<line class="tick" x1="{x:.1f}" y1="{ya}" x2="{x:.1f}" y2="{ya + 5}"/><text class="tl" x="{x:.1f}" y="{ya + 19}">{lab}</text>')
    if wide:
        s.append(f'<text class="axl" x="{AX1}" y="{ya + 40}">distance from the record, in minimal gaps: 0.13% for a price, 0.14 points for a change, 0.1% for a volume</text>')
    else:
        s.append(f'<text class="axl start" x="0" y="{ya + 38}">distance from the record, in minimal gaps:</text>')
        s.append(f'<text class="axl start" x="0" y="{ya + 54}">0.13% for a price · 0.14 points for a change</text>')
        s.append(f'<text class="axl start" x="0" y="{ya + 70}">0.1% for a volume</text>')
    s.append("</svg>")
    return "".join(s)


P2_LABEL = (f"{N_SINGLE} single figures about the session: {N_EQUAL} equal to the record at the precision written, "
            f"{N_OFF} not, placed by their distance from it on a logarithmic scale. The price errors are between "
            f"{ERR_PRICE[0]:.2f} and {ERR_PRICE[-1]:.2f} per cent off the record.")

# ── panel 3: Gemini by the hour in New York ─────────────────────────────────
BAND = (13 + 20 / 60, 15 + 26 / 60)


def panel3(wide=True):
    W = 940 if wide else 400
    RH = 70 if wide else 92
    LW = 34 if wide else 22
    X0, X1 = LW + 8, W - 10
    R = 4.2 if wide else 3.3

    def X(h):
        return X0 + h / 24 * (X1 - X0)

    rows = ("A", "C", "U")
    H = len(rows) * RH + 50
    s = [f'<svg class="p3" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(P3_LABEL)}">']
    s.append(f'<rect class="band" x="{X(BAND[0]):.1f}" y="4" width="{X(BAND[1]) - X(BAND[0]):.1f}" height="{len(rows) * RH}"/>')
    for i, t in enumerate(rows):
        yc = 4 + i * RH + RH / 2
        s.append(f'<line class="rule" x1="{X0}" y1="{4 + (i + 1) * RH:.1f}" x2="{X1}" y2="{4 + (i + 1) * RH:.1f}"/>')
        s.append(f'<text class="tk" x="0" y="{yc + 4.5:.1f}">{t}</text>')
        placed = []
        for r in sorted((r for r in GEM if r["type"] == t), key=lambda r: r["sent_new_york"]):
            hh = int(r["sent_new_york"][11:13]) + int(r["sent_new_york"][14:16]) / 60
            x = X(hh)
            dy, k = 0.0, 0
            while any((x - px) ** 2 + (yc + dy - py) ** 2 < (2 * R + 0.8) ** 2 for px, py in placed):
                k += 1
                dy = (k + 1) // 2 * (2 * R + 0.8) * (1 if k % 2 else -1)
            placed.append((x, yc + dy))
            what = f"Gemini, {r['ticker']} {t}, sent {r['sent_new_york'][5:16]} in New York: " + ("no prices" if r["refused"] == "yes" else "with the day's data")
            cls = "g-refc" if r["refused"] == "yes" else "g-ex"
            s.append(f'<g><title>{esc(what)}</title><circle class="{cls}" cx="{x:.1f}" cy="{yc + dy:.1f}" r="{R}"/></g>')
    ya = 4 + len(rows) * RH
    for h in range(0, 25, 3 if wide else 6):
        x = X(h)
        s.append(f'<line class="tick" x1="{x:.1f}" y1="{ya}" x2="{x:.1f}" y2="{ya + 5}"/><text class="tl" x="{x:.1f}" y="{ya + 19}">{h:02d}:00</text>')
    s.append(f'<text class="axl" x="{X1}" y="{ya + 40}">time the question was sent, New York</text>')
    s.append("</svg>")
    return "".join(s)


N_GEM_REF = sum(r["refused"] == "yes" for r in GEM)
IN_BAND = sum(1 for r in GEM if r["refused"] == "yes" and r["type"] == "A"
              and BAND[0] <= int(r["sent_new_york"][11:13]) + int(r["sent_new_york"][14:16]) / 60 <= BAND[1])
N_GEM_REF_A = sum(r["refused"] == "yes" and r["type"] == "A" for r in GEM)
P3_LABEL = (f"All {len(GEM)} of Gemini's answers by the time the question was sent, in New York: "
            f"{N_GEM_REF} gave no prices, {IN_BAND} of the {N_GEM_REF_A} refusals to A between 13:20 and 15:26.")

# ── panel 4: the session's prices and the other numbers, by app ─────────────
TITLES = {"ChatGPT": "The sun is yellow!", "Claude": "To know means to be mistaken.", "Gemini": "I am always ready – till I’m not."}


def panel4(wide=True):
    W = 940 if wide else 400
    if wide:
        LW, AX0, AX1, RH, TOPR = 250, 262, 700, 104, 10
    else:
        LW, AX0, AX1, RH, TOPR = 0, 6, 330, 158, 56
    XMAX = 35

    def X(v):
        return AX0 + v / XMAX * (AX1 - AX0)

    H = len(APPS) * RH + 46
    s = [f'<svg class="p4" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(P4_LABEL)}">']
    for i, app in enumerate(APPS):
        y0 = i * RH
        d = P4[app]
        s.append(f'<text class="app" x="0" y="{y0 + 22:.1f}">{app}</text>')
        if wide:
            s.append(f'<text class="ttl" x="0" y="{y0 + 44:.1f}">{esc(TITLES[app])}</text>')
            s.append(f'<text class="per" x="{W}" y="{y0 + 30:.1f}">{d["per"]:.1f} other numbers per answer</text>')
            s.append(f'<text class="per" x="{W}" y="{y0 + 50:.1f}">{d["wper"]:.2f} wrong per answer</text>')
        else:
            s.append(f'<text class="ttl" x="0" y="{y0 + 44:.1f}">{esc(TITLES[app])}</text>')
            s.append(f'<text class="per" x="{W}" y="{y0 + 22:.1f}">{d["per"]:.1f} per answer · {d["wper"]:.2f} wrong</text>')
        for j, (key, cls, lab) in enumerate((("sp", "g-app", "the session’s prices"), ("ot", "g-ex", "the other numbers"))):
            k, n = d[key]
            lo, hi = wilson(k, n)
            y = y0 + TOPR + 16 + j * 24
            v = 100 * k / n
            s.append(f'<g><title>{esc(f"{app}, {lab}: {k} wrong of {n}, {v:.1f} per cent (95 per cent interval {lo:.1f}–{hi:.1f})")}</title>'
                     f'<line class="ci" x1="{X(lo):.1f}" y1="{y:.1f}" x2="{X(hi):.1f}" y2="{y:.1f}"/>'
                     f'<circle class="{cls}" cx="{X(v):.1f}" cy="{y:.1f}" r="5"/></g>')
            s.append(f'<text class="cnt" x="{X(hi) + 8:.1f}" y="{y + 3.8:.1f}">{k}/{n}</text>')
        s.append(f'<line class="rule" x1="0" y1="{y0 + RH - 8:.1f}" x2="{W}" y2="{y0 + RH - 8:.1f}"/>')
    ya = len(APPS) * RH
    s.append(f'<line class="axis" x1="{AX0}" y1="{ya}" x2="{AX1}" y2="{ya}"/>')
    for v in range(0, XMAX + 1, 5 if wide else 10):
        s.append(f'<line class="tick" x1="{X(v):.1f}" y1="{ya}" x2="{X(v):.1f}" y2="{ya + 5}"/><text class="tl" x="{X(v):.1f}" y="{ya + 19}">{v}</text>')
    s.append(f'<text class="axl{"" if wide else " start"}" x="{AX1 if wide else 0}" y="{ya + 40}">per cent of the figures wrong</text>')
    s.append("</svg>")
    return "".join(s)


P4_LABEL = (f"In the {N_PRE} pre-registered answers, the session’s prices were wrong {SP_W} times in {SP_N}; the other numbers that can be checked "
            f"{H_W} times in {H_N}: ChatGPT {P4['ChatGPT']['ot'][0]} of {P4['ChatGPT']['ot'][1]}, Claude {P4['Claude']['ot'][0]} of {P4['Claude']['ot'][1]}, "
            f"Gemini {P4['Gemini']['ot'][0]} of {P4['Gemini']['ot'][1]}.")

# ── legends ─────────────────────────────────────────────────────────────────
LEG1 = """
        <p class="legend" aria-hidden="true">
          <span><svg viewBox="0 0 16 16"><circle class="g-ex" cx="8" cy="8" r="5.6"/></svg>every price exact</span>
          <span><svg viewBox="0 0 16 16"><circle class="g-min" cx="8" cy="8" r="5.6"/></svg>minimal gaps</span>
          <span><svg viewBox="0 0 16 16"><circle class="g-app" cx="8" cy="8" r="5"/></svg>“about”, and right</span>
          <span><svg viewBox="0 0 16 16"><path class="g-err" d="M3 3 L13 13 M13 3 L3 13"/></svg>at least one price off the record</span>
          <span><svg viewBox="0 0 16 16"><path class="g-prem" d="M8 1.5 L14.5 13 L1.5 13 Z"/></svg>took up the false premise</span>
          <span><svg viewBox="0 0 16 16"><line class="g-ref" x1="2" y1="8" x2="14" y2="8"/></svg>no prices: it said it had none</span>
          <span><svg viewBox="0 0 16 16"><path class="g-con" d="M8 3 l5 5 l-5 5 l-5 -5 Z"/></svg>one figure accepted by convention</span>
        </p>"""
LEG2 = """
        <p class="legend" aria-hidden="true">
          <span><svg viewBox="0 0 16 16"><rect class="u" x="4" y="4" width="8" height="8"/></svg>equal to the record, at the precision written</span>
          <span><svg viewBox="0 0 16 16"><circle class="g-min" cx="8" cy="8" r="4.4"/></svg>within the minimal gap</span>
          <span><svg viewBox="0 0 16 16"><circle class="g-app" cx="8" cy="8" r="4"/></svg>“about”, “nearly”, a range: right</span>
          <span><svg viewBox="0 0 16 16"><path class="g-con" d="M8 3.5 l4.5 4.5 l-4.5 4.5 l-4.5 -4.5 Z"/></svg>a volume from another provider, accepted</span>
          <span><svg viewBox="0 0 16 16"><path class="g-err" d="M4 4 L12 12 M12 4 L4 12"/></svg>error</span>
        </p>"""
LEG3 = """
        <p class="legend" aria-hidden="true">
          <span><svg viewBox="0 0 16 16"><circle class="g-ex" cx="8" cy="8" r="4.2"/></svg>with the day’s data</span>
          <span><svg viewBox="0 0 16 16"><circle class="g-refc" cx="8" cy="8" r="4.2"/></svg>no prices: it said it had none</span>
          <span><svg viewBox="0 0 34 16"><rect class="band" x="1" y="1" width="32" height="14"/></svg>13:20 to 15:26, New York</span>
        </p>"""

LEG4 = """
        <p class="legend" aria-hidden="true">
          <span><svg viewBox="0 0 16 16"><circle class="g-app" cx="8" cy="8" r="5"/></svg>the prices of the session asked about</span>
          <span><svg viewBox="0 0 16 16"><circle class="g-ex" cx="8" cy="8" r="5"/></svg>the other numbers that can be checked</span>
          <span><svg viewBox="0 0 34 16"><line class="ci" x1="2" y1="8" x2="32" y2="8"/></svg>95 per cent interval</span>
        </p>"""

EVENT_KEY = "".join(
    f'<li><b>{E[ev]["ticker"]}</b> {esc(NAMES[E[ev]["ticker"]])}<span>{day(E[ev]["session"])} · {num(float(E[ev]["change_close_pct"]))}%</span></li>'
    for ev in EVS)

PLATE_CSS = """
  /* ---- plate 2 ---- */
  .plate{padding:4.5vh 0 2vh;}
  .panel{border-top:2px solid var(--ink);padding:1.1em 0 3.2em;}
  .panel h2{font-family:var(--display);font-weight:var(--dw);font-size:clamp(22px,2.6vw,30px);letter-spacing:-0.015em;line-height:1.15;margin:0 0 0.25em;}
  .panel .sub2{margin:0 0 1.4em;font-size:17px;line-height:1.5;color:var(--faint);max-width:62ch;text-wrap:pretty;}
  .panel .sub2 b{font-weight:inherit;color:var(--ink);}
  .fig{width:100%;}
  .fig svg{display:block;width:100%;height:auto;overflow:visible;}
  .wide{display:block;} .narrow{display:none;}
  .narrow .blk{margin:0 0 1.6em;}
  .narrow .blk svg{max-width:calc(var(--cols) * 40px + 70px);}
  svg text{font-family:var(--mono);fill:var(--faint);font-size:11px;letter-spacing:0.02em;}
  svg .tk{font-family:var(--display);font-weight:var(--dw);font-size:15px;fill:var(--ink);letter-spacing:0;}
  svg .nm{font-family:var(--sans);font-size:13.5px;fill:var(--ink);letter-spacing:0;}
  svg .dt,svg .mv,svg .hd,svg .col,svg .tl,svg .thl,svg .cnt,svg .axl{font-size:11px;}
  svg .mv,svg .end,svg .axl,svg .cnt.end{text-anchor:end;}
  svg .col,svg .tl,svg .thl{text-anchor:middle;}
  svg .thl.end{text-anchor:end;} svg .thl.start,svg .axl.start{text-anchor:start;}
  svg .col.sub{font-size:9.5px;}
  svg .app{font-family:var(--mono);font-size:11.5px;letter-spacing:0.12em;text-transform:uppercase;fill:var(--ink);}
  svg .bar{stroke:var(--ink);stroke-width:1;}
  svg .rule{stroke:var(--line);stroke-width:1;}
  svg .split{stroke:var(--line);stroke-width:1;stroke-dasharray:2 3;}
  svg .axis,svg .tick{stroke:var(--faint);stroke-width:1;}
  svg .thr{stroke:var(--ink);stroke-width:1;}
  svg .thr.tol{stroke-dasharray:3 3;}
  svg .band{fill:var(--line);opacity:0.55;}
  .g-ex{fill:var(--ink);}
  .g-min{fill:var(--faint);}
  .g-app{fill:var(--paper);stroke:var(--ink);stroke-width:1.5;}
  .g-err{fill:none;stroke:var(--accent);stroke-width:2.2;stroke-linecap:round;}
  .g-prem{fill:var(--accent);}
  .g-ref{stroke:var(--ink);stroke-width:1.6;stroke-linecap:round;}
  .g-refc{fill:var(--paper);stroke:var(--ink);stroke-width:1.4;}
  .g-con{fill:var(--paper);stroke:var(--ink);stroke-width:1;}
  .g-none{fill:var(--line);}
  svg .u{fill:var(--ink);opacity:0.78;}
  .legend{display:flex;flex-wrap:wrap;gap:0.7em 1.8em;margin:1.2em 0 0;font-family:var(--mono);font-size:11.5px;letter-spacing:0.04em;color:var(--faint);}
  .legend span{display:inline-flex;align-items:center;gap:0.55em;}
  .legend svg{width:16px;height:16px;overflow:visible;flex:none;}
  .legend svg[viewBox="0 0 34 16"]{width:34px;}
  svg .ttl{font-family:var(--sans);font-style:italic;font-size:15px;fill:var(--ink);letter-spacing:0;}
  svg .per{font-size:11px;text-anchor:end;}
  svg .ci,.ci{stroke:var(--ink);stroke-width:1.2;}
  .apps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(18px,3vw,44px);margin:0 0 3.4em;}
  .apps article{border-top:1px solid var(--ink);padding-top:0.9em;}
  .apps .who{font-family:var(--mono);font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:var(--faint);margin:0 0 0.5em;}
  .apps h3{font-family:var(--display);font-weight:var(--dw);font-size:clamp(20px,2.1vw,25px);line-height:1.15;letter-spacing:-0.012em;margin:0 0 0.6em;}
  .apps p{margin:0;font-size:16px;line-height:1.55;text-wrap:pretty;}
  .shown{margin:0 0 3.4em;font-family:var(--mono);font-size:12px;letter-spacing:0.14em;text-transform:uppercase;}
  .shown a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--accent);padding-bottom:2px;}
  .shown a:hover{color:var(--accent);}
  .evkey{list-style:none;margin:0 0 1.6em;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0.35em 1.2em;
    font-family:var(--mono);font-size:11.5px;letter-spacing:0.02em;color:var(--faint);}
  .evkey b{font-family:var(--display);font-weight:var(--dw);font-size:14px;color:var(--ink);margin-right:0.3em;}
  .evkey span{display:block;}
  .notes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(14px,2.6vw,36px);margin:0.5em 0 0;padding-top:1em;border-top:1px solid var(--ink);}
  .notes p{margin:0;font-size:14px;line-height:1.55;color:var(--faint);text-wrap:pretty;}
  .notes b{display:block;font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink);margin-bottom:0.5em;}
  .notes a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--accent);}
  @media (max-width:760px){
    .wide{display:none;} .narrow{display:block;}
    .notes,.apps{grid-template-columns:minmax(0,1fr);}
  }
  @media (max-width:340px){ .evkey{grid-template-columns:minmax(0,1fr);} }
"""


def narrow_p1():
    out = [f'<ul class="evkey">{EVENT_KEY}</ul>']
    for b in range(len(BLOCKS)):
        out.append(f'<div class="blk" style="--cols:{len(BLOCKS[b][2])}">{panel1(wide=False, block=b)}</div>')
    return "".join(out)


body = f"""
  <main class="wrap">

    <section class="open" data-screen-label="opening">
      <div class="kicker"><span><a href="/work">work</a> · where no one can know · plate 2 of 2, 2026</span></div>
      <h1 class="statement">On precision.<span class="q"> Either say or show it!</span></h1>
      <p class="sub">Asked how twelve stocks moved in a session, three chat apps with web search gave the right direction every time they quoted prices and got the session’s figures wrong {SP_W} times in {fmt_n(SP_N)}. The numbers they added around them, about other days and hours, history and the false premise, were wrong {H_W} times in {H_N}.</p>
      <p class="contract">Twelve sessions of October 2026, asked about in the chat apps of ChatGPT, Claude and Gemini between 25 and 28 October, with web search on and each app at its highest settings. Every figure about the session in {len(S)} answers was checked against the exchange’s record. In the {N_PRE} pre-registered ones, so was every other number the prices could check. The questions were in Italian.</p>
    </section>

    <section class="plate" aria-label="study 2 in four panels">
      <div class="panel" id="answers">
        <h2>Every answer.</h2>
        <p class="sub2">One mark for each answer. <b>A</b> asks how the stock reacted to its results; <b>C</b> asks why it moved the other way, a premise that is false. Gemini’s exploration blocks, outside the pre-registered plan, are set apart.</p>
        <div class="fig wide">{panel1()}</div>
        <div class="fig narrow">{narrow_p1()}</div>{LEG1}
      </div>

      <div class="panel" id="figures">
        <h2>Every figure.</h2>
        <p class="sub2">The {fmt_n(N_SINGLE)} single figures about the session in every scored answer, A, C and U, which asks for the official open, close and volume. {fmt_n(N_EQUAL)} are equal to the record at the precision written; {N_OFF} are set by their distance from it. The price errors lie between {ERR_PRICE[0]:.2f} and {ERR_PRICE[-1]:.2f} per cent off, written like the rest. The scale leaves out {N_BOUND} bounds and levels inside the day’s range, such as “more than 8 per cent”, all of them right.</p>
        <div class="fig wide">{panel2()}</div>
        <div class="fig narrow">{panel2(wide=False)}</div>{LEG2}
      </div>

      <div class="panel" id="hours">
        <h2>Gemini, by the hour.</h2>
        <p class="sub2">All {len(GEM)} of its answers, A, C and U, by the time each question was sent, in New York. {IN_BAND} of its {N_GEM_REF_A} refusals to A fall between 13:20 and 15:26. The plate shows when, not why.</p>
        <div class="fig wide">{panel3()}</div>
        <div class="fig narrow">{panel3(wide=False)}</div>{LEG3}
      </div>

      <div class="panel" id="around">
        <h2>The day, and around it.</h2>
        <p class="sub2">For each app, the share of wrong figures in the {N_PRE} pre-registered answers, among the prices of the session asked about and among the other numbers that can be checked. These are about other sessions, the pre-market, the after-hours and the moments of the day, history and the false premise. Numbers written in words are left out, as in the pilot.</p>
        <div class="fig wide">{panel4()}</div>
        <div class="fig narrow">{panel4(wide=False)}</div>{LEG4}
      </div>

      <div class="apps">
        <article>
          <p class="who">ChatGPT</p>
          <h3>{esc(TITLES["ChatGPT"])}</h3>
          <p>It gives the session’s prices and little else, {P4["ChatGPT"]["per"]:.1f} other numbers per answer. It is rarely wrong: {P4["ChatGPT"]["sp"][0]} of its {P4["ChatGPT"]["sp"][1]} figures about the session, {P4["ChatGPT"]["ot"][0]} of its {P4["ChatGPT"]["ot"][1]} other numbers. When it is, it has trusted a source that looks official and measures something else: General Motors’ open at 77.00, from the company’s own pages, repeated in three answers. The price of caution is an answer with little around it.</p>
        </article>
        <article>
          <p class="who">Claude</p>
          <h3>{esc(TITLES["Claude"])}</h3>
          <p>It gathers many articles, names them and adds context: {P4["Claude"]["per"]:.1f} other numbers per answer, {pct(P4["Claude"]["ot"])} per cent of them wrong. Its session prices are almost all right; the errors sit around them. About half are the right number from the wrong moment: an article written while the session was open, the London quote at 16:15, Wednesday’s figure given as Thursday’s. More than half recur, the same wrong figure in more than one answer, because the search finds the same articles. Faced with the false premise, it tries to explain it and rebuilds rough precedents: {pct(P4["Claude"]["c_rate"])} per cent of these numbers are wrong in its C answers, {pct(P4["Claude"]["a_rate"])} in its A answers.</p>
        </article>
        <article>
          <p class="who">Gemini</p>
          <h3>{esc(TITLES["Gemini"])}</h3>
          <p>Everything depends on search. In {GEM_NOSEARCH} of its {sum(r["app"] == "Gemini" for r in PRE)} answers it had none, and it said so rather than invent, with {"two exceptions" if GEM_ADOPT == 2 else str(GEM_ADOPT) + " exceptions"}: C answers that admit having no data, then take the false fall as given and explain it. When search works, it sometimes fills the fields with values given as the day’s that belong to other sessions or to no source at all. Of its other numbers, {pct(P4["Gemini"]["ot"])} per cent are wrong, most of all its hypotheses on the premise.</p>
        </article>
      </div>

      <p class="shown"><a href="/work/on-precision/shown">shown, not said: the same answers in quartz</a></p>

      <div class="notes">
        <p><b>method</b>Close, high and low from Interactive Brokers’ daily bars, regular session; open and volume from Nasdaq’s history. Moves are on the previous close. A price is off beyond 0.13 per cent, a change beyond 0.14 points, a volume beyond 0.1 per cent; with “about”, beyond 1 per cent or 1.2 points. The other numbers were checked against the same sources, with intraday bars for the moments of the day. The main rules were fixed before the scoring.</p>
        <p><b>selection</b>Twelve sessions and 36 questions fixed in a pre-registration before the first answer, each asked in a new chat. Gemini’s usage limits left it with fewer answers; its exploration blocks are declared as a deviation and kept apart. No rate is claimed beyond these answers.</p>
        <p><b>source</b>The answers, every scored figure and the scripts that recompute this plate are on <a href="https://github.com/diegoballarin-reason/frictions/tree/main/study2">GitHub</a>, with the essay that reads them, <a href="https://github.com/diegoballarin-reason/frictions/blob/main/study2/here-is-one-hand.en.md">here&nbsp;is&nbsp;one&nbsp;hand</a>. Claude proposed every evaluation, its own answers included; each was confirmed one by one, and the conventions added after seeing some answers are dated in the&nbsp;method.</p>
      </div>
    </section>

    <div class="closing-band">
      <section class="colophon" data-screen-label="colophon">
        <div class="rail"></div>
        <div class="c-body">
          <h3>nothing to notice it by</h3>
          <p>Research, data and design: Diego Ballarin, 2026. Every mark is placed from the data by a script; the rules and the decisions are mine, and the collection, the drafting and the code were done in dialogue with Claude. Plate&nbsp;1 is <a href="/work/on-certainty">on certainty</a>. Plate&nbsp;2 is also <a href="/work/on-precision/shown">shown in quartz</a>.</p>
        </div>
      </section>
    </div>

  </main>
"""

SCRIPT = """
<script>
(function(){
  /* typesetting: no word alone at the end of a block, no short word hanging */
  var SHORT=/(?<=^|\\s)([\\p{L}\\p{N}]{1,2}) (?=\\S)/gu;
  document.querySelectorAll('.panel .sub2,.notes p,.open .sub,.contract,.colophon p,.panel h2,.legend span,.apps p,.apps h3').forEach(function(el){
    var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),nodes=[];while(w.nextNode())nodes.push(w.currentNode);
    nodes.forEach(function(n,i){n.nodeValue=n.nodeValue.replace(SHORT,'$1\\u00A0');
      var nx=nodes[i+1];if(!nx)return;
      if(/(^|\\s)[\\p{L}\\p{N}]{1,2} $/u.test(n.nodeValue))n.nodeValue=n.nodeValue.slice(0,-1)+'\\u00A0';
      else if(/(^|\\s)[\\p{L}\\p{N}]{1,2}$/u.test(n.nodeValue)&&/^ /.test(nx.nodeValue))nx.nodeValue='\\u00A0'+nx.nodeValue.slice(1);});
    for(var i=nodes.length-1,seen=false;i>=0;i--){var v=nodes[i].nodeValue,body=v.replace(/\\s+$/,''),k=body.lastIndexOf(' ');
      if(seen&&/ $/.test(v)){nodes[i].nodeValue=v.slice(0,-1)+'\\u00A0';break;}
      if(k>0){nodes[i].nodeValue=v.slice(0,k)+'\\u00A0'+v.slice(k+1);break;}
      if(body.trim())seen=true;}
  });
})();
</script>
"""

DESC = (f"Twelve stock sessions asked about in three chat apps with web search: every answer, every figure against the "
        f"exchange's record, when Gemini declined, and the numbers around the day. Plate 2 of nothing to notice it by.")
chrome = open(chrome_path, encoding="utf-8").read()
head_end = chrome.index("</style>")
head = chrome[:head_end] + PLATE_CSS + chrome[head_end:chrome.index("<main")]
head = re.sub(r"<title>.*?</title>", "<title>on precision — diego ballarin</title>", head, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="' + DESC.replace("'", "&#39;") + '"', head)
head = head.replace("https://diegoballarin.com/work/agent-review", "https://diegoballarin.com/work/on-precision")
head = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="on precision — diego ballarin">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + DESC.replace("'", "&#39;") + '">', head)
head = head.replace("https://diegoballarin.com/assets/og-cover.jpg", "https://diegoballarin.com/assets/op-og.jpg")
a, b = head.index('<div class="index-nav">'), head.index('\n    </div>\n  </header>')
head = head[:a].rstrip() + head[b:]
tail_script = chrome[chrome.index("<script>", chrome.index("</main>")):]
menus_only = tail_script.split("/* typesetting")[0] + "})();\n</script>\n</body>\n</html>\n"
open(out_path, "w", encoding="utf-8").write(head + body + menus_only.replace("</body>", SCRIPT + "</body>"))
print("wrote", out_path, "|", N_SINGLE, "single figures,", N_EQUAL, "equal;", N_AP, "A with prices,", N_AP_ERR, "with errors;",
      N_C_CORR, "of", N_C, "premises corrected;", IN_BAND, "of", N_GEM_REF_A, "Gemini A refusals in the band")
