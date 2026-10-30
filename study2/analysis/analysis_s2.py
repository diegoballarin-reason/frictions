"""Studio 2 · analisi del §8 sui dati esportati (answers.csv, figures.csv, claims.csv se presente).
Uso: analysis_s2.py DATA_DIR OUT_JSON"""
import csv, json, math, os, sys
from collections import Counter, defaultdict
D, OUT = sys.argv[1], sys.argv[2]
A = list(csv.DictReader(open(f"{D}/answers.csv", encoding="utf-8")))
F = list(csv.DictReader(open(f"{D}/figures.csv", encoding="utf-8")))
APPS = ["ChatGPT", "Claude", "Gemini"]

def wilson(k, n, z=1.96):
    if not n: return [None, None]
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d * 100, 1), round((c + h) / d * 100, 1)]

def rate(rows, cond_den, cond_num):
    den = [r for r in rows if cond_den(r)]; num = [r for r in den if cond_num(r)]
    return {"k": len(num), "n": len(den), "pct": round(100 * len(num) / len(den), 1) if den else None, "ci95": wilson(len(num), len(den))}

res = {}
pre = [r for r in A if r["study"] == "preregistered"]
# 1 · misura principale: A con almeno un errore nei prezzi della seduta, sulle A con almeno un prezzo
res["main"] = {}
for app in APPS:
    a = [r for r in pre if r["app"] == app and r["type"] == "A"]
    res["main"][app] = {"errors": rate(a, lambda r: r["prices"] not in ("none_given", ""), lambda r: r["prices"] == "with_errors"),
                        "errors_rule7_only": rate(a, lambda r: r["prices"] not in ("none_given", ""), lambda r: (r["prices_rule7_only"] or r["prices"]) == "with_errors"),
                        "without_prices": rate(a, lambda r: True, lambda r: r["prices"] == "none_given"),
                        "refused": rate(a, lambda r: True, lambda r: r["refused"] == "yes")}
ga = [r for r in A if r["app"] == "Gemini" and r["type"] == "A"]
res["main"]["Gemini_with_exploration"] = {"errors": rate(ga, lambda r: r["prices"] not in ("none_given", "") and r["scored"] == "yes", lambda r: r["prices"] == "with_errors")}
# 2 · confronto sulle domande comuni (stesso evento, tipo e ripetizione in tutte e tre le app, giri preregistrati)
keys = defaultdict(set)
for r in pre: keys[(r["event"], r["type"], r["repetition"])].add(r["app"])
common = {k for k, v in keys.items() if len(v) == 3}
res["common"] = {"questions": len(common), "by_type": dict(Counter(k[1] for k in common))}
for app in APPS:
    sub = [r for r in pre if r["app"] == app and (r["event"], r["type"], r["repetition"]) in common]
    res["common"][app] = {
        "A_errors": rate([r for r in sub if r["type"] == "A"], lambda r: r["prices"] not in ("none_given", ""), lambda r: r["prices"] == "with_errors"),
        "A_without_prices": rate([r for r in sub if r["type"] == "A"], lambda r: True, lambda r: r["prices"] == "none_given"),
        "C_premise_adopted": rate([r for r in sub if r["type"] == "C"], lambda r: r["scored"] == "yes", lambda r: r["premise"] == "adopted"),
        "U_errors": rate([r for r in sub if r["type"] == "U"], lambda r: r["scored"] == "yes" and r["prices"] not in ("none_given", ""), lambda r: r["prices"] == "with_errors")}
# 3 · U e C, tutte le risposte preregistrate
res["U"] = {app: {"errors": rate([r for r in pre if r["app"] == app and r["type"] == "U"], lambda r: r["scored"] == "yes" and r["prices"] not in ("none_given", ""), lambda r: r["prices"] == "with_errors"),
                  "without_prices": rate([r for r in pre if r["app"] == app and r["type"] == "U"], lambda r: r["scored"] == "yes", lambda r: r["prices"] == "none_given")} for app in APPS}
res["H3_premise"] = {app: rate([r for r in pre if r["app"] == app and r["type"] == "C"], lambda r: r["scored"] == "yes", lambda r: r["premise"] == "adopted") for app in APPS}
# 4 · H4: ricerca non disponibile o rifiuto, e distribuzione per ora di New York
res["H4"] = {}
for app in APPS:
    rows = [r for r in pre if r["app"] == app and r["scored"] == "yes"]
    res["H4"][app] = {"search_unavailable": rate(rows, lambda r: True, lambda r: r["search"] == "unavailable"),
                      "search_not_used": rate(rows, lambda r: True, lambda r: r["search"] == "not_used"),
                      "refused_all_types": rate([r for r in pre if r["app"] == app], lambda r: True, lambda r: r["refused"] == "yes")}
g = [r for r in A if r["app"] == "Gemini"]
band = lambda r: "13:20–15:26" if "13:20" <= r["sent_new_york"][11:16] <= "15:26" else "altre ore"
res["H4"]["Gemini_by_band"] = {b: rate([r for r in g if band(r) == b], lambda r: True, lambda r: r["refused"] == "yes") for b in ("13:20–15:26", "altre ore")}
res["H4"]["Gemini_by_band_preregistered"] = {b: rate([r for r in g if band(r) == b and r["study"] == "preregistered"], lambda r: True, lambda r: r["refused"] == "yes") for b in ("13:20–15:26", "altre ore")}
# 5 · concordanza fra le ripetizioni di A sui prezzi principali (chiusura e variazione %)
conc = {}
for app in APPS:
    pairs = agree = 0
    for ev in sorted({r["event"] for r in pre}):
        reps = [r["id"] for r in pre if r["app"] == app and r["event"] == ev and r["type"] == "A" and r["prices"] not in ("none_given", "")]
        for q in ("close", "change_close_pct"):
            vals = {}
            for rid in reps:
                xs = [f for f in F if f["answer_id"] == rid and f["quantity"] == q and f["value_low"] == f["value_high"] and f["value_low"] != ""]
                if xs: vals[rid] = float(xs[0]["value_low"])
            ks = sorted(vals)
            for i in range(len(ks)):
                for j in range(i + 1, len(ks)):
                    a, b = vals[ks[i]], vals[ks[j]]
                    same = abs(a - b) <= (0.14 if q.endswith("pct") else 0.0013 * max(abs(a), abs(b)))
                    pairs += 1; agree += same
    conc[app] = {"pairs": pairs, "agree": agree, "pct": round(100 * agree / pairs, 1) if pairs else None}
res["concordance_A"] = conc
# 6 · H2 e H1 (se c'è claims.csv)
if os.path.exists(f"{D}/claims.csv"):
    C_all = list(csv.DictReader(open(f"{D}/claims.csv", encoding="utf-8")))
    # decisione del 30 ottobre: i numeri in lettere o come parametro restano fuori (come nel pilota); a parte in "in_words"
    C = [c for c in C_all if c.get("in_words", "no") != "yes"]
    res["H2"] = {}
    for app in APPS:
        n_ans = len([r for r in pre if r["app"] == app]); n = len([c for c in C if c["app"] == app])
        res["H2"][app] = {"answers": n_ans, "claims": n, "per_answer": round(n / n_ans, 1)}
    res["H1"] = {}
    types = ["other_sessions", "outside_and_intraday", "history", "premise_hypothesis"]
    for app in APPS + ["all"]:
        cc = [c for c in C if app == "all" or c["app"] == app]
        d = {}
        for t in types:
            x = [c for c in cc if c["type"] == t]
            ver = [c for c in x if c["outcome"] in ("right", "wrong")]
            d[t] = {"claims": len(x), "verified": len(ver), "wrong": sum(c["outcome"] == "wrong" for c in ver), "not_verified": sum(c["outcome"] == "not_verified" for c in x), "ci95": wilson(sum(c["outcome"] == "wrong" for c in ver), len(ver))}
        ff = [f for f in F if (app == "all" or f["app"] == app) and f["study"] == "preregistered"]
        d["session_prices"] = {"verified": len(ff), "wrong": sum(f["outcome"] == "error" for f in ff), "ci95": wilson(sum(f["outcome"] == "error" for f in ff), len(ff))}
        grpA = [c for c in cc if c["type"] in types and c["outcome"] in ("right", "wrong")]
        d["group_A_pooled"] = {"verified": len(grpA), "wrong": sum(c["outcome"] == "wrong" for c in grpA), "ci95": wilson(sum(c["outcome"] == "wrong" for c in grpA), len(grpA))}
        sec = [c for c in cc if c.get("sec_sample")]
        secv = [c for c in sec if c["outcome"] in ("right", "wrong")]
        d["company_data_sec_sample"] = {"sampled": len(sec), "verified": len(secv), "wrong": sum(c["outcome"] == "wrong" for c in secv), "not_verified": sum(c["outcome"] == "not_verified" for c in sec), "ci95": wilson(sum(c["outcome"] == "wrong" for c in secv), len(secv))}
        iw = [c for c in C_all if (app == "all" or c["app"] == app) and c.get("in_words") == "yes" and c["type"] in types and c["outcome"] in ("right", "wrong")]
        d["in_words_group_A"] = {"verified": len(iw), "wrong": sum(c["outcome"] == "wrong" for c in iw)}
        res["H1"][app] = d
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1)[:6000])
