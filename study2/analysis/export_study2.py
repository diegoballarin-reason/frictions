"""Export study 2 (and the Gemini exploration blocks) as plain data files for plate 2.

Reads the records of the page «Pilota Frictions» (collections studio2_risposte, esplorazione_gemini,
studio2_valutazioni, esplorazione_valutazioni, saved as JSON by the artifact database) and the frozen
references (refs_frozen.json, questions.json). Writes CSV files with English column names and codes;
the original Italian labels stay in *_it columns so every row can be traced back to the page.

Usage: export_study2.py DB_DIR STUDY2_DIR OUT_DIR
"""
import csv
import glob
import json
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

db, s2, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
ROME, NY = ZoneInfo("Europe/Rome"), ZoneInfo("America/New_York")


def load(coll):
    return {os.path.basename(f)[:-5]: json.load(open(f, encoding="utf-8")) for f in glob.glob(f"{db}/{coll}/*.json")}


R2, RX, V2, VX = load("studio2_risposte"), load("esplorazione_gemini"), load("studio2_valutazioni"), load("esplorazione_valutazioni")
refs = json.load(open(f"{s2}/refs_frozen.json"))
Q = json.load(open(f"{s2}/questions.json"))
TICK = Q["tickers"]  # "01" -> "C"

# ── codes ────────────────────────────────────────────────────────────────────
PRICES = {"esatti": "exact", "scarti minimi": "minimal_gaps", "approssimati, corretti": "approximate_correct",
          "con errori": "with_errors", "non indicati": "none_given"}
DIRECTION = {"giusta": "right", "sbagliata": "wrong", "non indicata": "not_given"}
PREMISE = {"corretta": "corrected", "adottata": "adopted", "ignorata": "ignored", "—": "", "": ""}
SEARCH = {"usata": "used", "non disponibile": "unavailable", "non usata": "not_used"}
ORIGIN = {"—": "", "": "", "fonte diversa": "different_source", "istantanea fuori tempo": "snapshot_out_of_time",
          "momento sbagliato": "wrong_moment", "dato rettificato o successivo": "revised_or_later_data",
          "errore ricorrente": "recurring_error", "modello": "model", "non rintracciabile": "untraceable"}
OUTCOME = {"esatto": "exact", "scarto minimo": "minimal_gap", "approssimato corretto": "approximate_correct",
           "arrotondato (giusto)": "rounded_correct", "livello in seduta (giusto)": "level_in_session_correct",
           "errore": "error", "fonte diversa (regola 3); errore per il §7": "accepted_rule3"}
QTY = {"apertura": "open", "chiusura": "close", "massimo": "high", "minimo": "low", "chiusura precedente": "previous_close",
       "variazione chiusura %": "change_close_pct", "variazione chiusura $": "change_close_usd",
       "variazione apertura %": "change_open_pct", "variazione massimo %": "change_high_pct",
       "variazione minimo %": "change_low_pct", "volume": "volume",
       "livello in seduta": "level_in_session", "livello in seduta %": "level_in_session_pct"}
STATUS = {"proposta": "proposed", "confermata": "confirmed", "modificata": "corrected_by_diego"}
APP = {"chatgpt": "ChatGPT", "claude": "Claude", "gemini": "Gemini"}


def code(table, v, what):
    v = "" if v is None else str(v).strip()
    if v not in table:
        raise SystemExit(f"unknown {what}: {v!r}")
    return table[v]


# ── events ───────────────────────────────────────────────────────────────────
EV = {}
for ev, t in TICK.items():
    e = refs["events"][t]
    n = e["nasdaq"]
    pc = e["prev_close"]
    EV[ev] = {
        "event": ev, "ticker": t, "session": e["date"], "previous_session": e["prev_date"],
        "previous_close": pc, "open_nasdaq": n["open"], "open_ibkr": e["open"], "high": e["high"], "low": e["low"],
        "close": e["close"], "volume_nasdaq": n["volume"] if n["volume"] is not None else "", "volume_ibkr_not_consolidated": e["volume_ibkr"],
        "change_close_pct": round((e["close"] / pc - 1) * 100, 4), "change_open_pct": round((n["open"] / pc - 1) * 100, 4),
        "change_high_pct": round((e["high"] / pc - 1) * 100, 4), "change_low_pct": round((e["low"] / pc - 1) * 100, 4),
        "true_direction": "up" if e["close"] > pc else "down",
        "question_A": Q["questions"][ev + "A"]["text"], "question_C": Q["questions"][ev + "C"]["text"],
        "question_U": Q["questions"][ev + "U"]["text"],
    }
with open(f"{out}/events.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(next(iter(EV.values())).keys()))
    w.writeheader()
    [w.writerow(EV[k]) for k in sorted(EV)]

# other sessions (closes, IBKR), for anyone who wants to check "other session" figures later
with open(f"{out}/closes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ticker", "date", "close_ibkr", "close_nasdaq"])
    for ev in sorted(EV):
        e = refs["events"][TICK[ev]]
        for d in sorted(e["closes"]):
            w.writerow([TICK[ev], d, e["closes"][d], e["nasdaq_closes"].get(d, "")])


# ── answers ──────────────────────────────────────────────────────────────────
def ny_time(date, hhmmss):
    t = datetime.fromisoformat(f"{date}T{hhmmss}").replace(tzinfo=ROME)
    return t.astimezone(NY).strftime("%Y-%m-%d %H:%M:%S")


REFUSAL = re.compile(r"^\s*(Non dispongo|Non ho accesso|Non posso|Non sono in grado)")


def refused(v, a):
    """yes when the answer gives no data about the session and says it has none (a refusal)."""
    if v:
        return "yes" if v["prezzi"] == "non indicati" and a["tipo"] == "A" else "no"
    return "yes" if REFUSAL.match(a.get("risposta") or "") else "no"


def links_of(a):
    links = a.get("link") or []
    if isinstance(links, str):
        links = json.loads(links) if links.startswith("[") else []
    return links


answers, figures = [], []
for rid, a in sorted(R2.items()) + sorted(RX.items()):
    study = "preregistered" if rid.startswith("s2-") else "exploration"
    vid = ("s2v-" + rid[3:]) if study == "preregistered" else ("xv-" + rid)
    v = (V2 if study == "preregistered" else VX).get(vid)
    ev = a["q"][:2]
    links = links_of(a)
    row = {
        "id": rid, "study": study, "round": str(a.get("blocco") or a.get("giro")), "app": APP[a["app"]], "event": ev,
        "ticker": TICK[ev], "type": a["tipo"], "repetition": rid.split("-")[2] if study == "preregistered" else (rid.split("-")[2] if rid.count("-") == 3 else ""),
        "question": a["domanda"], "sent_rome": f"{a['data']} {a['ora_invio']}", "sent_new_york": ny_time(a["data"], a["ora_invio"]),
        "days_after_session": a.get("giorni_da_evento", ""), "settings": a.get("modello", ""), "sources_shown": len(links),
        "answer_chars": a.get("len", ""), "search_signal_it": a.get("segnale_ricerca", ""),
        "scored": "yes" if v else "no",
        "refused": refused(v, a),
        "direction": code(DIRECTION, v["direzione"], "direzione") if v else "",
        "prices": code(PRICES, v["prezzi"], "prezzi") if v else "",
        "prices_rule7_only": code(PRICES, v["prezzi_solo_par7"], "par7") if v and v.get("prezzi_solo_par7") not in (None, "", "None") else "",
        "origin": code(ORIGIN, v["origine"], "origine") if v else "",
        "premise": code(PREMISE, v.get("premessa"), "premessa") if v and a["tipo"] == "C" else "",
        "search": code(SEARCH, v["ricerca"], "ricerca") if v else "",
        "contestable": "yes" if v and str(v.get("contestabile") or "").strip() else "",
        "status": code(STATUS, v.get("stato", "proposta"), "stato") if v else "",
        "notes_it": (v.get("osservazioni") or "") if v else "",
    }
    answers.append(row)
    for n_, n in enumerate((v or {}).get("numeri") or [], 1):
        val = n.get("valore")
        lo, hi = (val if isinstance(val, list) else (val, val)) if val is not None else ("", "")
        figures.append({
            "answer_id": rid, "n": n_, "app": row["app"], "event": ev, "type": row["type"], "study": study,
            "quantity": code(QTY, n.get("grandezza"), "grandezza"), "quote_it": n.get("citazione", ""),
            "value_low": lo, "value_high": hi, "qualifier_it": n.get("qualificatore", ""),
            "reference": n.get("riferimento") if not isinstance(n.get("riferimento"), list) else "",
            "gap_it": n.get("scarto", ""), "outcome": code(OUTCOME, n.get("esito"), "esito"),
            "source_named": n.get("fonte_nel_testo", ""),
        })

for name, rows in (("answers", answers), ("figures", figures)):
    with open(f"{out}/{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

# answer texts, one JSON object per line (kept out of the CSV: long, with tables and line breaks)
with open(f"{out}/answers-text.jsonl", "w", encoding="utf-8") as f:
    for rid, a in sorted(R2.items()) + sorted(RX.items()):
        f.write(json.dumps({"id": rid, "text": a.get("risposta", ""), "sources": links_of(a)}, ensure_ascii=False) + "\n")

print(len(EV), "events;", len(answers), "answers;", sum(r["scored"] == "yes" for r in answers), "scored;", len(figures), "figures")
