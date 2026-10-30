"""H1 · dai numeri riuniti (merged_numbers.json) alle proposte per la pagina (una per risposta) e alla tabella dei numeri.
Segna i numeri che dipendono da una convenzione ancora da decidere con Diego."""
import json, os, re
from collections import Counter, defaultdict
D = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(D, "merged_numbers.json")))
P = {f[:-5]: json.load(open(os.path.join(D, "passP", f))) for f in os.listdir(os.path.join(D, "passP")) if f.endswith(".json")}
GA = ["altre sedute", "fuori seduta e intraday", "storico", "ipotesi"]
LETTERE = {"aggiunto_parola", "aggiunto_parametro"}
import importlib.util as _iu
_sp = _iu.spec_from_file_location("R", os.path.join(D, "h1recon.py")); _R = _iu.module_from_spec(_sp); _sp.loader.exec_module(_R); ORIGINE = getattr(_R, "ORIGINE", {})
# campione dei dati aziendali verificato sui documenti SEC (due passaggi, sec/out_P e sec/out_V)
SECK = {k["sid"]: k for k in json.load(open(os.path.join(D, "sec", "sample_kit.json")))}
SEC = {}
for sid, k in SECK.items():
    p = json.load(open(os.path.join(D, "sec", "out_P", sid + ".json"))); v = json.load(open(os.path.join(D, "sec", "out_V", sid + ".json")))
    assert p["esito"] == v["esito"], ("disaccordo SEC", sid)
    SEC[(k["answer_id"], str(k["n"]))] = {"sid": sid, "esito": p["esito"], "riferimento": (p["citazione_filing"] + " · " + p["filing"]).strip(" ·"),
        "calcolo": p["calcolo"], "nota": p["nota"] + (" Origine probabile: " + p["origine"] + "." if p.get("origine") else "") + " Secondo passaggio concorde."}
PARAM_X = re.compile(r"^(52|15|200|2012)$")
LETTURA_X = {("s2-07A-1-gemini", "x1"), ("s2-10A-1-gemini", "x1"), ("s2-12C-1-chatgpt", "x1"), ("s2-12C-1-chatgpt", "x2")}
VERSO = {("s2-02A-1-claude", "19"), ("s2-11A-2-claude", "7"), ("s2-11A-2-claude", "8")}
FINOA = {("s2-04A-2-claude", "12"), ("s2-04A-2-claude", "13"), ("s2-04C-1-claude", "7"), ("s2-04C-2-claude", "8"), ("s2-09A-1-claude", "7"), ("s2-06A-1-gemini", "8")}
def flags(i, x):
    f = []
    k = (i, str(x["n"]))
    if str(x["n"]).startswith("x") and x.get("affermazione"):
        if k in LETTURA_X: f.append("aggiunto_lettura")
        elif PARAM_X.match(str(x.get("num", "")).strip()): f.append("aggiunto_parametro")
        else: f.append("aggiunto_parola")
        if re.search(r"doppi|tripl|quadrupl|volte|la metà", (x.get("num", "") + " " + x.get("citazione", "")).lower()) and x.get("tipo") in GA: f.append("multiplo")
    if k in VERSO: f.append("orario_approssimato")
    if k in FINOA: f.append("fino_a_esteso")
    if x.get("esito") and re.search(r"settimana|sette giorni", x.get("citazione", "").lower()) and re.search(r"14", x.get("citazione", "")) and i.startswith("s2-11"): f.append("settimana")
    return f
rows, docs = [], {}
for i, L in sorted(M.items()):
    q = i.split("-")[1]; app = i.split("-")[-1]; rep = i.split("-")[2]
    cnt = Counter(); per = defaultdict(Counter); ga = []; let = Counter(); camp = Counter(); secn = []
    for x in L:
        x.pop("_conflict", None)
        fl = flags(i, x)
        if x.get("affermazione"):
            e = {"giusto": "giusti", "sbagliato": "sbagliati", "non verificato": "non_verificati", "per scelta": "per_scelta", "seduta": "seduta"}[x["esito"]]
            sk = SEC.get((i, str(x["n"])))
            if sk:
                e2 = {"giusto": "giusti", "sbagliato": "sbagliati", "non verificato": "non_verificati"}[sk["esito"]]
                camp[e2] += 1; per[x["tipo"]]["campione_" + e2] += 1
            elif LETTERE & set(fl) and x.get("tipo") in GA: let[e] += 1   # numeri in lettere o parametri: fuori dal tasso (decisione del 30 ottobre)
            else: cnt[e] += 1; per[x["tipo"]][e] += 1
        else: cnt["esclusi"] += 1
        sk = SEC.get((i, str(x["n"]))) if x.get("affermazione") else None
        rows.append({"answer_id": i, "n": str(x["n"]), "app": app, "event": q[:2], "type_q": q[2], "num": x.get("num", ""), "claim": bool(x.get("affermazione")),
                     "excluded": x.get("escluso", ""), "tipo": x.get("tipo", ""), "esito": sk["esito"] if sk else x.get("esito", ""), "citazione": x.get("citazione", ""),
                     "riferimento": sk["riferimento"] if sk else x.get("riferimento", ""), "calcolo": sk["calcolo"] if sk else x.get("calcolo", ""),
                     "nota": sk["nota"] if sk else x.get("nota", ""), "flags": fl + (["campione_sec"] if sk else []), "riconciliazione": x.get("riconciliazione", ""),
                     "campione_sec": sk["sid"] if sk else ""})
        if sk:
            secn.append({"n": str(x["n"]), "citazione": x.get("citazione", ""), "tipo": "dati aziendali (campione SEC)", "esito": sk["esito"], "riferimento": sk["riferimento"],
                         "calcolo": sk["calcolo"], "nota": sk["sid"] + ". " + sk["nota"], "convenzione": "", "in_lettere": False, "campione": True})
        if x.get("affermazione") and x.get("tipo") in GA:
            pre = "In lettere o parametro: fuori dal tasso del gruppo A (decisione del 30 ottobre). " if LETTERE & set(fl) else ""
            ga.append({"n": str(x["n"]), "citazione": x.get("citazione", ""), "tipo": x["tipo"], "esito": x["esito"], "riferimento": x.get("riferimento", ""),
                       "calcolo": x.get("calcolo", ""), "nota": (pre + x.get("nota", "") + (" · Riconciliazione: " + x["riconciliazione"] if x.get("riconciliazione") else "")).strip(" ·"),
                       "convenzione": ", ".join(fl), "in_lettere": bool(LETTERE & set(fl))})
    p = P[i]
    wrong = [g for g in ga if g["esito"] == "sbagliato" and not g["in_lettere"]]
    orig = ORIGINE.get(i) or p.get("origine_altri") or "—"
    if not wrong: orig = "—"
    dub = []   # le convenzioni segnate sono state decise da Diego il 30 ottobre (kit/decisioni_30ott.md): nessun dubbio aperto da qui
    rec = [g for g in ga if "Riconciliazione" in g["nota"]]
    dis = [f"n. {g['n']}: {g['nota'].split('Riconciliazione: ')[-1]}" for g in rec]
    docs["h1-" + i] = {"id": "h1-" + i, "risposta_id": i, "app": app, "ev": q[:2], "q": q, "tipo": q[2], "rep": int(rep),
                       "conteggi": {k: cnt.get(k, 0) for k in ("seduta", "giusti", "sbagliati", "non_verificati", "per_scelta", "esclusi")},
                       "in_lettere": {k: let.get(k, 0) for k in ("giusti", "sbagliati", "non_verificati")},
                       "campione_sec": {k: camp.get(k, 0) for k in ("giusti", "sbagliati", "non_verificati")},
                       "per_tipo": {t: dict(c) for t, c in per.items()}, "origine_altri": orig,
                       "osservazioni": p.get("osservazioni", ""), "numeri": ga + secn, "dubbi": " ".join(dub), "disaccordo": dis,
                       "stato": "proposta", "updatedAt": ""}
json.dump(rows, open(os.path.join(D, "claims_final.json"), "w"), ensure_ascii=False)
json.dump(docs, open(os.path.join(D, "h1_docs.json"), "w"), ensure_ascii=False)
withA = [d for d in docs.values() if d["numeri"]]
print("SEC sample in docs:", sum(sum(d["campione_sec"].values()) for d in docs.values()), "answers with only sample numbers:", sum(1 for d in docs.values() if d["numeri"] and all(n.get("campione") for n in d["numeri"])))
print("answers", len(docs), "with group-A numbers", len(withA), "claims", sum(r["claim"] for r in rows), "excluded", sum(not r["claim"] for r in rows))
print("flags", Counter(f for r in rows for f in r["flags"]))
