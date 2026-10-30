"""Export the H1 claims of study 2 (one row per number in the 217 pre-registered answers) as claims.csv.

Reads h1/claims_final.json (outcome of each number after the two passes, the reconciliation, the extra checks and
the SEC sample) and the page collection studio2_altri_numeri (one doc per answer, confirmed by Diego). Diego confirms
answer by answer: when he corrected the counts of an answer, the claim rows of that answer are flagged
(`answer_corrected`=yes) and the confirmed counts are written in answers_h1.csv, so the analysis can use either level.

Usage: export_claims.py H1_DIR DB_DIR OUT_DIR
"""
import csv, glob, json, os, sys

h1, db, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
C = json.load(open(f"{h1}/claims_final.json", encoding="utf-8"))
DOCS = {os.path.basename(f)[:-5]: json.load(open(f, encoding="utf-8")) for f in glob.glob(f"{db}/studio2_altri_numeri/*.json")}
TYPE = {"seduta richiesta": "session_prices", "altre sedute": "other_sessions", "fuori seduta e intraday": "outside_and_intraday",
        "storico": "history", "ipotesi": "premise_hypothesis", "analisti e mercato": "analysts_market", "dati aziendali": "company_data"}
OUT = {"giusto": "right", "sbagliato": "wrong", "non verificato": "not_verified", "per scelta": "by_choice", "seduta": "session"}
APP = {"chatgpt": "ChatGPT", "claude": "Claude", "gemini": "Gemini"}
STATUS = {"proposta": "proposed", "confermata": "confirmed", "modificata": "corrected_by_diego"}
WORDS = {"aggiunto_parola", "aggiunto_parametro"}

rows, ans = [], {}
for x in C:
    if not x["claim"]:
        continue
    d = DOCS.get("h1-" + x["answer_id"], {})
    st = d.get("stato", "")
    rows.append({
        "answer_id": x["answer_id"], "n": x["n"], "app": APP[x["app"]], "event": x["event"], "question_type": x["type_q"],
        "type": TYPE[x["tipo"]], "outcome": OUT[x["esito"]],
        "in_words": "yes" if WORDS & set(x["flags"]) else "no",
        "sec_sample": x.get("campione_sec", ""),
        "answer_status": STATUS.get(st, "") if d else "no_doc",
        "answer_corrected": "yes" if st == "modificata" else "no",
        "quote_it": x["citazione"], "reference_it": x["riferimento"], "calculation_it": x["calcolo"], "note_it": x["nota"],
        "reconciliation_it": x.get("riconciliazione") or "",
    })
for k, d in sorted(DOCS.items()):
    c = d.get("conteggi", {}); l = d.get("in_lettere", {}); s = d.get("campione_sec", {})
    ans[k] = {"answer_id": d["risposta_id"], "app": APP[d["app"]], "event": d["ev"], "question_type": d["tipo"], "status": STATUS.get(d.get("stato", ""), ""),
              "right": c.get("giusti", 0), "wrong": c.get("sbagliati", 0), "not_verified": c.get("non_verificati", 0), "by_choice": c.get("per_scelta", 0),
              "in_words_right": l.get("giusti", 0), "in_words_wrong": l.get("sbagliati", 0), "in_words_not_verified": l.get("non_verificati", 0),
              "sec_right": s.get("giusti", 0), "sec_wrong": s.get("sbagliati", 0), "sec_not_verified": s.get("non_verificati", 0),
              "origin_it": d.get("origine_altri", ""), "notes_it": d.get("osservazioni", "")}
for name, rr in (("claims", rows), ("answers_h1", list(ans.values()))):
    with open(f"{out}/{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rr[0].keys())); w.writeheader(); w.writerows(rr)
print(len(rows), "claims;", len(ans), "answer docs;", sum(a["status"] == "confirmed" for a in ans.values()), "confirmed,",
      sum(a["status"] == "corrected_by_diego" for a in ans.values()), "corrected")
