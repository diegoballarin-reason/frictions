"""Recompute what plate 2 says from the exported data, and check the scoring against the references.

1. Every reference recorded with a scored figure must equal the frozen reference for that session
   (events.csv): no figure was scored against the wrong number.
2. Every figure scored as correct must be within its threshold of the reference, recomputed here:
   exact and minimal gap within 0.13% for prices, 0.14 points for changes, 0.1% for volume;
   approximations within 1% or 1.2 points; ranges and bounds against the truth at the precision written.
   Volumes off Nasdaq's count are listed apart: under rule 3 another provider's consolidated count is not an error.
   Errors are listed with their recomputed gap, so each can be read.
3. The counts printed on the plate, with 95% Wilson intervals.

Usage: check_study2.py DATA_DIR
"""
import csv
import math
import re
import sys
from collections import Counter, defaultdict

D = sys.argv[1]
A = list(csv.DictReader(open(f"{D}/answers.csv", encoding="utf-8")))
F = list(csv.DictReader(open(f"{D}/figures.csv", encoding="utf-8")))
E = {r["event"]: r for r in csv.DictReader(open(f"{D}/events.csv", encoding="utf-8"))}

PRICE = {"open": "open_nasdaq", "close": "close", "high": "high", "low": "low", "previous_close": "previous_close", "volume": "volume_nasdaq"}
PCT = {"change_close_pct": "change_close_pct", "change_open_pct": "change_open_pct", "change_high_pct": "change_high_pct", "change_low_pct": "change_low_pct"}


def truth(e, q):
    if q in PRICE:
        return float(e[PRICE[q]]) if e[PRICE[q]] != "" else None
    if q in PCT:
        return float(e[PCT[q]])
    if q == "change_close_usd":
        return float(e["close"]) - float(e["previous_close"])
    return None


def gap(q, v, t, e):
    """signed gap: percent for prices and volume, points for changes; dollar changes as a share of the previous close."""
    if q in PCT:
        return v - t
    if q == "change_close_usd":
        return (v - t) / float(e["previous_close"]) * 100
    return (v / t - 1) * 100


def minimal(q):
    return 0.14 if q in PCT else 0.10 if q == "volume" else 0.13


def approx(q):
    return 1.2 if q in PCT else 1.0


def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d * 100, (c + h) / d * 100)


# ── 1 and 2: figures ─────────────────────────────────────────────────────────
wrong_ref, flags, errors, rule3 = [], [], [], []
singles = 0
for f in F:
    q, e, out = f["quantity"], E[f["event"]], f["outcome"]
    if q in ("level_in_session", "level_in_session_pct"):
        lo, hi = (float(e["low"]), float(e["high"])) if q == "level_in_session" else (float(e["change_low_pct"]), float(e["change_high_pct"]))
        v = float(f["value_low"])
        if out == "level_in_session_correct" and not lo <= v <= hi:
            flags.append((f, "level outside the day's range"))
        continue
    t = truth(e, q)
    if t is None:
        continue
    if f["reference"] not in ("", None):
        r = float(f["reference"])
        tol = 0.0051 if q in PCT else max(abs(t) * 1e-6, 0.0051)
        if abs(r - t) > tol and not (q in PCT and abs(r - round(t, 2)) <= 0.0051):
            wrong_ref.append((f, t))
    lo_v, hi_v = float(f["value_low"]), float(f["value_high"])
    qual = f["qualifier_it"].lower()
    if lo_v == hi_v:
        singles += 1
        g = gap(q, lo_v, t, e)
        half = q == "open" and round(t * 1000) % 10 == 5 and abs(abs(lo_v - t) - 0.005) < 1e-6
        why = None
        if out in ("exact", "minimal_gap") and abs(g) > minimal(q) + 1e-9 and not half:
            why = f"{out} but {g:+.3f} from the record"
        if out in ("approximate_correct", "rounded_correct"):
            bound = re.search(r"oltre|più di|superior", qual)
            if bound:
                ok = abs(t) >= abs(lo_v) - approx(q) * (1 if q in PCT else abs(t) / 100)
            else:
                ok = abs(g) <= approx(q) + 1e-9
            if not ok:
                why = f"{out.replace('_', ' ')} {g:+.3f} beyond the tolerance"
        if why and q == "volume" and abs(g) < 20:
            rule3.append((f, g))  # rule 3: no single official count of consolidated volume
        elif why:
            flags.append((f, why))
        if out == "error":
            errors.append((f, g))
    else:
        a_, b_ = sorted((lo_v, hi_v))
        w = approx(q) if q in PCT else approx(q) / 100 * abs(t)
        widened = re.search(r"circa|ordine|area|intorno", qual) is not None
        places = max(len(f["value_low"].split(".")[-1]) if "." in f["value_low"] else 0,
                     len(f["value_high"].split(".")[-1]) if "." in f["value_high"] else 0)
        tr = round(t, places)  # the truth at the precision written
        inside = (a_ - (w if widened else 0)) - 1e-9 <= tr <= (b_ + (w if widened else 0)) + 1e-9
        half = q == "open" and round(t * 1000) % 10 == 5 and (abs(a_ - t) <= 0.0051 or abs(b_ - t) <= 0.0051)
        if out != "error" and not (inside or half):
            flags.append((f, f"range {a_}–{b_} does not contain {t:.4f}"))
        if out == "error":
            errors.append((f, None))

print(f"figures checked: {len(F)} ({singles} single values, {len(F) - singles - 2} ranges, 2 levels in session)")
print(f"references different from the frozen record: {len(wrong_ref)}")
for f, t in wrong_ref:
    print(f"   {f['answer_id']} {f['quantity']}: recorded {f['reference']}, frozen {t:.4f}")
print(f"correct outcomes outside their threshold: {len(flags)}")
for f, why in flags:
    print(f"   {f['answer_id']} {f['quantity']} «{f['quote_it'][:60]}» {f['outcome']}, qualifier «{f['qualifier_it']}»: {why}")
print(f"volumes off Nasdaq's count but accepted under rule 3 (another provider's consolidated count): {len(rule3)}")
for f, g in rule3:
    print(f"   {f['answer_id']} «{f['quote_it'][:50]}» {g:+.2f}% ({f['outcome']})")
print(f"figures scored as errors: {len(errors)}")
for f, g in errors:
    gs = "range" if g is None else f"{g:+.2f} {'points' if f['quantity'] in PCT else '%'}"
    print(f"   {f['answer_id']:<20} {f['quantity']:<18} {f['value_low']:>10}  {gs:>14}  qualifier «{f['qualifier_it']}»")

# ── 3: counts ────────────────────────────────────────────────────────────────
S = [r for r in A if r["scored"] == "yes"]
pre = [r for r in S if r["study"] == "preregistered"]
print("\nanswers:", len(A), "| scored (A and C):", len(S), "| figures:", len(F))
Ap = [r for r in S if r["type"] == "A" and r["prices"] != "none_given"]
print(f"A answers that quote the session's prices: {len(Ap)}, right direction {sum(r['direction'] == 'right' for r in Ap)}, "
      f"with at least one price error {sum(r['prices'] == 'with_errors' for r in Ap)}")
C = [r for r in S if r["type"] == "C"]
print(f"C answers (false premise): {len(C)}, corrected {sum(r['premise'] == 'corrected' for r in C)}, adopted {sum(r['premise'] == 'adopted' for r in C)}")
print("\nby app, pre-registered rounds:")
for app in ("ChatGPT", "Claude", "Gemini"):
    a = [r for r in pre if r["app"] == app and r["type"] == "A"]
    wp = [r for r in a if r["prices"] != "none_given"]
    k = sum(r["prices"] == "with_errors" for r in wp)
    lo, hi = wilson(k, len(wp))
    c = [r for r in pre if r["app"] == app and r["type"] == "C"]
    print(f"   {app:<8} A {len(a)}, with prices {len(wp)}, with errors {k} ({k / max(1, len(wp)) * 100:.0f}%, {lo:.0f}–{hi:.0f}), "
          f"refused {sum(r['refused'] == 'yes' for r in a)} | C {len(c)}, premise adopted {sum(r['premise'] == 'adopted' for r in c)}")
g = [r for r in S if r["app"] == "Gemini" and r["type"] == "A" and r["prices"] != "none_given"]
k = sum(r["prices"] == "with_errors" for r in g)
lo, hi = wilson(k, len(g))
print(f"   Gemini, rounds and exploration: A with prices {len(g)}, with errors {k} ({k / len(g) * 100:.0f}%, {lo:.0f}–{hi:.0f})")
gc = [r for r in S if r["app"] == "Gemini" and r["type"] == "C"]
print(f"   Gemini, rounds and exploration: C {len(gc)}, premise adopted {sum(r['premise'] == 'adopted' for r in gc)}")
gall = [r for r in A if r["app"] == "Gemini"]
print(f"   Gemini, all answers: {len(gall)}, refusals {sum(r['refused'] == 'yes' for r in gall)}")
errs = [abs(gg) for f, gg in errors if gg is not None and f["quantity"] in PRICE and f["quantity"] != "volume"]
print(f"\nprice errors (single values): {len(errs)}, from {min(errs):.2f}% to {max(errs):.2f}% off the record")
print("outcomes of all figures:", dict(Counter(f["outcome"] for f in F)))
bad = len(wrong_ref) + len(flags)
print("\nAll scored figures agree with the references." if not bad else f"\n{bad} figure(s) to read again.")
sys.exit(1 if bad else 0)
