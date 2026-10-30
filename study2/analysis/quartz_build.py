"""Build plate 2, shown (diegoballarin.com/work/on-precision/shown): the quartz crystal.

The page is quartz.html, next to this script; the data are placed into it from study2/data:
  - every pre-registered answer to A and C, with every figure about the session: its quantity, its words,
    the reference, the outcome and its signed distance from the record in minimal gaps (0 for a figure
    equal to the record at the precision written, and for ranges, bounds and levels, which have none);
  - the twelve sessions, in date order;
  - the other numbers that can be checked (H1) in those answers, numbers in words left out as in the pilot.
In the crystal a figure stands off its veil only when its outcome is an error; the distance sets how far.

Usage: quartz_build.py DATA_DIR OUT_HTML
"""
import csv
import json
import os
import re
import sys

data_dir, out_path = sys.argv[1:3]
here = os.path.dirname(os.path.abspath(__file__))


def rows(name):
    return list(csv.DictReader(open(f"{data_dir}/{name}", encoding="utf-8")))


A = [a for a in rows("answers.csv") if a["study"] == "preregistered" and a["type"] in ("A", "C")]
F = rows("figures.csv")
E = {e["event"]: e for e in rows("events.csv")}
C = rows("claims.csv")
NAMES = {"C": "Citigroup", "LRCX": "Lam Research", "GM": "General Motors", "META": "Meta", "CMG": "Chipotle", "MU": "Micron",
         "HAS": "Hasbro", "LMT": "Lockheed Martin", "IP": "International Paper", "CCI": "Crown Castle", "DDOG": "Datadog",
         "GFS": "GlobalFoundries"}
PRICE = {"open": "open_nasdaq", "close": "close", "high": "high", "low": "low", "previous_close": "previous_close", "volume": "volume_nasdaq"}
PCT = {"change_close_pct", "change_open_pct", "change_high_pct", "change_low_pct"}
NUMRE = re.compile(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?")
BOUND_RE = re.compile(r"oltre|più di|superior|inferior|almeno|sotto")


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
    return len(f["value_low"].split(".")[1]) if "." in f["value_low"] else 0


def minimal(q):
    return 0.14 if q in PCT else 0.10 if q == "volume" else 0.13


def placed(f):
    """(signed distance in minimal gaps, kind) for one figure."""
    q, e, o = f["quantity"], E[f["event"]], f["outcome"]
    frosted = o in ("approximate_correct", "level_in_session_correct") or f["value_low"] != f["value_high"] or bool(BOUND_RE.search(f["qualifier_it"]))
    kind = "error" if o == "error" else "frosted" if frosted else "clear"
    if o == "accepted_rule3":
        kind = "rule3"
    if o == "level_in_session_correct" or q.startswith("level") or f["value_low"] != f["value_high"] or (BOUND_RE.search(f["qualifier_it"]) and o != "error"):
        return 0.0, kind
    t = truth(e, q)
    if t is None:
        return 0.0, kind
    v = float(f["value_low"])
    if abs(round(t, written_places(f)) - v) < 1e-9 or (q == "open" and round(t * 1000) % 10 == 5 and abs(abs(v - t) - 0.005) < 1e-6):
        return 0.0, kind
    g = (v - t) if q in PCT else (v - t) / float(e["previous_close"]) * 100 if q == "change_close_usd" else (v / t - 1) * 100
    return g / minimal(q), kind


FIGS = {}
for f in F:
    FIGS.setdefault(f["answer_id"], []).append(f)
answers = []
for a in sorted(A, key=lambda a: (a["app"], a["sent_new_york"])):
    figs = []
    for f in sorted(FIGS.get(a["id"], []), key=lambda f: int(f["n"])):
        d, kind = placed(f)
        figs.append({"q": f["quantity"], "quote": f["quote_it"], "ref": f["reference"], "o": f["outcome"], "d": round(d, 3), "kind": kind})
    answers.append({"id": a["id"], "app": a["app"], "study": a["study"], "type": a["type"], "rep": a["repetition"], "event": a["event"],
                    "refused": a["refused"] == "yes", "premise": a["premise"], "figs": figs})
ids = {a["id"] for a in answers}
events = [{"event": k, "ticker": e["ticker"], "name": NAMES.get(e["ticker"], e["ticker"]), "session": e["session"], "move": float(e["change_close_pct"])}
          for k, e in sorted(E.items(), key=lambda kv: (kv[1]["session"], kv[1]["ticker"]))]
H1 = ("other_sessions", "outside_and_intraday", "history", "premise_hypothesis")
h1 = [{"a": c["answer_id"], "n": c["n"], "t": c["type"], "o": c["outcome"], "q": c["quote_it"].strip()}
      for c in C if c["type"] in H1 and c["in_words"] == "no" and c["answer_id"] in ids and c["outcome"] in ("right", "wrong", "not_verified")]

blob = json.dumps({"answers": answers, "events": events, "h1": h1}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
page = open(os.path.join(here, "quartz.html"), encoding="utf-8").read().replace("/*DATA*/", blob)
if not page.rstrip().endswith("</html>"):
    page = page.rstrip() + "\n</body>\n</html>\n"
open(out_path, "w", encoding="utf-8").write(page)
n_fig = sum(len(a["figs"]) for a in answers)
print("wrote", out_path, "|", len(answers), "answers,", n_fig, "figures,", sum(f["o"] == "error" for a in answers for f in a["figs"]),
      "errors on needles,", len(h1), "other numbers,", sum(h["o"] == "wrong" for h in h1), "wrong")
