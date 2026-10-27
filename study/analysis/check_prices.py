#!/usr/bin/env python3
"""
Recompute every price figure in *Where No One Can Know* from the daily bars,
check it against the figure printed in the protocol, and write the geometry
for the infographic.

    python3 study/analysis/check_prices.py            # check, print the table
    python3 study/analysis/check_prices.py --svg DIR  # also write SVG geometry

Standard library only. Percentages are always on the previous session's
close, as the protocol requires (§3).
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


# ── reading the data ─────────────────────────────────────────────────────────

def load_bars(path):
    """Return {ticker: [ {date, open, high, low, close, volume}, ... ]} in date order."""
    bars = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            bar = {"date": row["date"], "volume": int(row["volume"])}
            for key in ("open", "high", "low", "close"):
                bar[key] = float(row[key])
            bars.setdefault(row["ticker"], []).append(bar)
    for series in bars.values():
        series.sort(key=lambda b: b["date"])
    return bars


def load_claims(path):
    """The claims that can be checked on a price: those with a session to check."""
    with open(path, newline="", encoding="utf-8") as f:
        return [c for c in csv.DictReader(f) if c["session"]]


def claimed_label(c):
    lo, hi = c["claimed_low_pct"], c["claimed_high_pct"]
    if lo and not hi:
        return f"over {float(lo):+.0f}"
    if lo:
        return f"{float(lo):+.2f}" if lo == hi else f"{float(lo):+.0f} to {float(hi):+.0f}"
    return c["claimed_direction"]


def session(bars, ticker, date):
    """The bar for `date` and the bar before it."""
    series = bars[ticker]
    for i, bar in enumerate(series):
        if bar["date"] == date:
            return series[i - 1], bar, i
    raise KeyError(f"{ticker} has no session on {date}")


def pct(new, base):
    return (new / base - 1) * 100


# ── the figures printed in the protocol (§3 and §5) ──────────────────────────
# (ticker, session, measure, value as printed). A measure is a price of the
# session compared with the previous close, or a volume ratio.

PRINTED = [
    ("IBM", "2026-07-14", "close", -25.21),
    ("IBM", "2026-07-14", "volume_ratio", 17.7),
    ("BE", "2026-07-29", "open", 9.99),
    ("VRT", "2026-07-29", "close", -17.26),
    ("NXT", "2026-07-01", "open", -1.7),
    ("NXT", "2026-07-01", "high", 3.76),
    ("NXT", "2026-07-01", "close", -2.51),
    ("NXT", "2026-07-31", "volume_ratio", 1.8),
    ("AAOI", "2026-08-07", "open", 14.70),
    ("AAOI", "2026-08-07", "close", 9.19),
    ("ONTO", "2026-08-07", "close", 14.74),
    ("RGTI", "2026-08-07", "open", 1.48),
    ("RGTI", "2026-08-07", "close", 8.53),
    ("WDC", "2026-08-06", "close", -13.0),
    ("AKAM", "2026-08-07", "open", 5.19),
    ("AKAM", "2026-08-07", "close", -6.76),
]


def measure(bars, ticker, date, what):
    prev, bar, _ = session(bars, ticker, date)
    if what == "volume_ratio":
        return bar["volume"] / prev["volume"]
    return pct(bar[what], prev["close"])


def check_printed(bars):
    """Every printed figure must match the recomputed one at the precision printed."""
    failures = 0
    print("Printed figures, recomputed from the bars")
    for ticker, date, what, printed in PRINTED:
        value = measure(bars, ticker, date, what)
        decimals = len(str(printed).split(".")[1]) if "." in str(printed) else 0
        ok = round(value, decimals) == round(printed, decimals)
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {ticker:5} {date} {what:12} printed {printed:>7}   recomputed {value:8.3f}")
    return failures


def check_volume_signature(bars):
    """§3.4: the real NXT report is found by volume alone (highest since 26 June)."""
    series = bars["NXT"]
    _, bar, i = session(bars, "NXT", "2026-07-31")
    earlier_higher = [b["date"] for b in series[:i] if b["volume"] > bar["volume"] and b["date"] >= "2026-06-01"]
    last = earlier_higher[-1] if earlier_higher else None
    ok = last == "2026-06-26"
    print(f"  {'ok  ' if ok else 'FAIL'} NXT   2026-07-31 volume {bar['volume']:,}, last higher session since June: {last}")
    return 0 if ok else 1


def claims_table(bars, claims):
    """One line per claim: what was claimed, what the record says."""
    print("\nClaims against the record (percent on the previous close)")
    print(f"  {'id':3} {'ticker':5} {'origin':12} {'claimed':>12}  on    {'open':>7} {'close':>7}   type")
    for c in claims:
        prev, bar, _ = session(bars, c["ticker"], c["session"])
        print(f"  {c['id']:3} {c['ticker']:5} {c['origin']:12} {claimed_label(c):>12}  {c['checked_on']:5} "
              f"{pct(bar['open'], prev['close']):+7.2f} {pct(bar['close'], prev['close']):+7.2f}   {c['protocol_type']}")


# ── geometry for the infographic ─────────────────────────────────────────────
# Plain black marks with ids, for finishing by hand. Every coordinate comes
# from the data through the scale functions below; nothing is placed by eye.

def svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" fill="none" stroke="#000" stroke-width="1">\n{body}</svg>\n')


def scale(domain_lo, domain_hi, range_lo, range_hi):
    span = domain_hi - domain_lo
    return lambda v: range_lo + (v - domain_lo) / span * (range_hi - range_lo)


def geometry_claims(bars, claims, path):
    """One row per claim on a common percent axis: the claim and the record."""
    width, row, top, left, right = 900, 48, 40, 40, 860
    lo, hi = -30, 25
    x = scale(lo, hi, left, right)
    parts = ['<g id="axis">']
    for tick in range(lo, hi + 1, 5):
        parts.append(f'  <line id="tick{tick:+d}" x1="{x(tick):.2f}" y1="{top - 10}" x2="{x(tick):.2f}" '
                     f'y2="{top + row * len(claims)}" stroke-width="{1 if tick == 0 else 0.25}"/>')
    parts.append("</g>")
    for n, c in enumerate(claims):
        y = top + row * n + row / 2
        prev, bar, _ = session(bars, c["ticker"], c["session"])
        p = {k: pct(bar[k], prev["close"]) for k in ("open", "high", "low", "close")}
        parts.append(f'<g id="{c["id"]}">')
        parts.append(f'  <line id="{c["id"]}-range" x1="{x(p["low"]):.2f}" y1="{y:.2f}" x2="{x(p["high"]):.2f}" y2="{y:.2f}" stroke-width="0.5"/>')
        parts.append(f'  <circle id="{c["id"]}-open" cx="{x(p["open"]):.2f}" cy="{y:.2f}" r="3"/>')
        parts.append(f'  <circle id="{c["id"]}-close" cx="{x(p["close"]):.2f}" cy="{y:.2f}" r="3" fill="#000"/>')
        if c["claimed_low_pct"] and not c["claimed_high_pct"]:  # "more than": open to the right or left
            a = x(float(c["claimed_low_pct"]))
            d = 1 if float(c["claimed_low_pct"]) > 0 else -1
            parts.append(f'  <path id="{c["id"]}-claim" d="M{a:.2f} {y - 9:.2f} V{y + 9:.2f} M{a:.2f} {y:.2f} h{d * 30}" stroke-width="2"/>')
        elif c["claimed_low_pct"]:
            a, b = x(float(c["claimed_low_pct"])), x(float(c["claimed_high_pct"]))
            if a == b:
                parts.append(f'  <path id="{c["id"]}-claim" d="M{a:.2f} {y - 9:.2f} V{y + 9:.2f}" stroke-width="2"/>')
            else:
                parts.append(f'  <rect id="{c["id"]}-claim" x="{a:.2f}" y="{y - 9:.2f}" width="{b - a:.2f}" height="18" stroke-width="2"/>')
        elif c["claimed_direction"] in ("up", "down"):
            d = 1 if c["claimed_direction"] == "up" else -1
            x0 = x(0)
            parts.append(f'  <path id="{c["id"]}-claim" d="M{x0:.2f} {y - 14:.2f} h{d * 24} l{-d * 6} -4 m{d * 6} 4 l{-d * 6} 4" stroke-width="2"/>')
        parts.append("</g>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg(width, top + row * len(claims) + 20, "\n".join(parts) + "\n"))


def geometry_window(bars, c, path, before=10, after=5):
    """Daily bars around the claimed session, as percent of the previous close.
    Every window shares one vertical scale, so the charts compare."""
    width, height, pad = 300, 200, 10
    prev, bar, i = session(bars, c["ticker"], c["session"])
    series = bars[c["ticker"]][max(0, i - before): i + after + 1]
    base = prev["close"]
    lo, hi = -35, 25
    y = scale(hi, lo, pad, height - pad)
    step = (width - 2 * pad) / len(series)
    parts = [f'<line id="zero" x1="{pad}" y1="{y(0):.2f}" x2="{width - pad}" y2="{y(0):.2f}" stroke-width="0.25"/>']
    for n, b in enumerate(series):
        cx = pad + step * (n + 0.5)
        mark = ' stroke-width="2"' if b["date"] == c["session"] else ""
        parts.append(f'<g id="{b["date"]}"{mark}>')
        parts.append(f'  <line x1="{cx:.2f}" y1="{y(pct(b["high"], base)):.2f}" x2="{cx:.2f}" y2="{y(pct(b["low"], base)):.2f}"/>')
        parts.append(f'  <line x1="{cx - step / 3:.2f}" y1="{y(pct(b["open"], base)):.2f}" x2="{cx:.2f}" y2="{y(pct(b["open"], base)):.2f}"/>')
        parts.append(f'  <line x1="{cx:.2f}" y1="{y(pct(b["close"], base)):.2f}" x2="{cx + step / 3:.2f}" y2="{y(pct(b["close"], base)):.2f}"/>')
        parts.append("</g>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg(width, height, "\n".join(parts) + "\n"))


def geometry_volume(bars, path, start="2026-06-01", end="2026-08-14"):
    """NXT volume: the claimed report (1 July) and the real one (31 July)."""
    series = [b for b in bars["NXT"] if start <= b["date"] <= end]
    width, height, pad = 600, 160, 10
    vmax = max(b["volume"] for b in series)
    y = scale(0, vmax, height - pad, pad)
    step = (width - 2 * pad) / len(series)
    parts = []
    for n, b in enumerate(series):
        x0 = pad + step * n + step * 0.15
        h = y(0) - y(b["volume"])
        mark = {"2026-07-01": ' id="claimed-report" stroke-width="2"', "2026-07-31": ' id="real-report" fill="#000"'}.get(b["date"], f' id="v{b["date"]}"')
        parts.append(f'<rect{mark} x="{x0:.2f}" y="{y(b["volume"]):.2f}" width="{step * 0.7:.2f}" height="{h:.2f}"/>')
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg(width, height, "\n".join(parts) + "\n"))


def main(argv):
    bars = load_bars(os.path.join(DATA, "daily-bars.csv"))
    claims = load_claims(os.path.join(DATA, "claims.csv"))
    failures = check_printed(bars) + check_volume_signature(bars)
    claims_table(bars, claims)
    if "--svg" in argv:
        out = argv[argv.index("--svg") + 1]
        os.makedirs(os.path.join(out, "windows"), exist_ok=True)
        geometry_claims(bars, claims, os.path.join(out, "claims.svg"))
        for c in claims:
            geometry_window(bars, c, os.path.join(out, "windows", f"{c['id']}-{c['ticker'].lower()}.svg"))
        geometry_volume(bars, os.path.join(out, "nxt-volume.svg"))
        print(f"\nGeometry written to {out}")
    print(f"\n{'All printed figures match.' if not failures else f'{failures} figure(s) do not match.'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
