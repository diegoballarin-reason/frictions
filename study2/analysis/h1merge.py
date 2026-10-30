"""H1 · unione dei due passaggi (passP, passV) numero per numero.
Accordo → si tiene P. Disaccordi che toccano il gruppo A → risoluzione manuale in h1recon.py (RES);
disaccordi solo fra tipi del gruppo B, o fra B e prezzi della seduta → si tiene P e si annota.
Uso: python3 h1merge.py [report]"""
import json, os, sys, importlib.util
from collections import Counter, defaultdict
D = os.path.dirname(os.path.abspath(__file__))
def load(p): return {f[:-5]: json.load(open(os.path.join(D, p, f))) for f in os.listdir(os.path.join(D, p)) if f.endswith(".json")}
P, V = load("passP"), load("passV")
ANS = sorted(f[:-5] for f in os.listdir(os.path.join(D, "kit", "answers")))
GA = {"altre sedute", "fuori seduta e intraday", "storico", "ipotesi"}
GB = {"analisti e mercato", "dati aziendali"}
def grp(n):
    if not n or not n.get("affermazione"): return "X"
    t = n.get("tipo", "")
    return "A" if t in GA else "B" if t in GB else "S" if t == "seduta richiesta" else "?"
RES = {}
if os.path.exists(os.path.join(D, "h1recon.py")):
    spec = importlib.util.spec_from_file_location("R", os.path.join(D, "h1recon.py")); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R); RES = R.RES
missing = [i for i in ANS if i not in P or i not in V]
if missing: print("MISSING", missing)
conf, auto, merged = [], Counter(), {}
for i in ANS:
    if i not in P or i not in V: continue
    pn = {str(n["n"]): n for n in P[i]["numeri"]}; vn = {str(n["n"]): n for n in V[i]["numeri"]}
    out = []
    for k in sorted(set(pn) | set(vn), key=lambda x: (x.startswith("x"), int(x) if x.isdigit() else 0, x)):
        a, b = pn.get(k), vn.get(k)
        ga, gb = grp(a), grp(b)
        key = (i, k)
        if key in RES:
            r = RES[key]
            if r[0] == "P": base = dict(a)
            elif r[0] == "V": base = dict(b)
            elif r[0] == "X": base = dict(a or b); base.update({"affermazione": False, "tipo": "", "gruppo": "", "esito": ""})
            else: base = dict(a or b)
            base.update(r[2] if len(r) > 2 else {})
            base["n"] = (a or b)["n"]; base["riconciliazione"] = r[1]
            out.append(base); continue
        same = ga == gb and (a or {}).get("tipo") == (b or {}).get("tipo") and (a or {}).get("esito") == (b or {}).get("esito")
        if same or (a is None and gb in ("X", "S", "B")) or (b is None and ga in ("X", "S", "B")):
            out.append(dict(a or b)); continue
        if "A" in (ga, gb) or ((a or {}).get("esito") in ("giusto", "sbagliato", "non verificato")) or ((b or {}).get("esito") in ("giusto", "sbagliato", "non verificato")):
            conf.append((i, k, a, b)); out.append(dict(a or b, _conflict=True)); continue
        auto[(ga, gb, (a or {}).get("tipo"), (b or {}).get("tipo"))] += 1
        x = dict(a or b); x["alt_V"] = {"affermazione": (b or {}).get("affermazione"), "tipo": (b or {}).get("tipo"), "escluso": (b or {}).get("escluso")}
        out.append(x)
    merged[i] = out
print("answers", len(merged), "conflicts in group A:", len(conf))
print("auto-resolved (kept P):", sum(auto.values()))
for k, v in auto.most_common(12): print("  ", v, k)
if len(sys.argv) > 1 and sys.argv[1] == "report":
    with open(os.path.join(D, "conflicts.txt"), "w") as f:
        for i, k, a, b in conf:
            f.write(f"=== {i} n={k}\n")
            for lab, x in (("P", a), ("V", b)):
                if not x: f.write(f"  {lab}: (assente)\n"); continue
                f.write(f"  {lab}: aff={x.get('affermazione')} escl={x.get('escluso','')} tipo={x.get('tipo','')} esito={x.get('esito','')}\n      cit: {x.get('citazione','')}\n      rif: {x.get('riferimento','')}\n      calc: {x.get('calcolo','')}\n      nota: {x.get('nota','')}\n")
    print("written conflicts.txt")
json.dump(merged, open(os.path.join(D, "merged_numbers.json"), "w"), ensure_ascii=False)
