"""Check the essay of study 2 (here-is-one-hand.en.md, here-is-one-hand.it.md) against the data.

Three checks, both languages:
  1. every number the essay states is computed here from study2/data and analysis.json, and each statement is
     found in the text as written (a phrase per language);
  2. no number in the text is left over: every digit outside the quotations belongs to a checked phrase;
  3. every quotation in the Italian text is found word for word in the answer it is given to (or in the question),
     and each English quotation carries the same numbers as the Italian one in the same place.
Numbers in words (three, eleven, ten times) are checked as phrases too.

Usage: essay_check.py STUDY2_DIR
"""
import csv
import json
import re
import sys
from collections import Counter
from datetime import date

root = sys.argv[1]
R = lambda n: list(csv.DictReader(open(f"{root}/data/{n}", encoding="utf-8")))
A = R("answers.csv")
F = R("figures.csv")
CL = R("claims.csv")
HA = R("answers_h1.csv")
E = {e["event"]: e for e in R("events.csv")}
CLOSE = {(r["ticker"], r["date"]): float(r["close_nasdaq"]) for r in R("closes.csv")}
T = {j["id"]: j["text"] for j in map(json.loads, open(f"{root}/data/answers-text.jsonl", encoding="utf-8"))}
AN = json.load(open(f"{root}/analysis.json", encoding="utf-8"))
TXT = {"en": open(f"{root}/here-is-one-hand.en.md", encoding="utf-8").read(), "it": open(f"{root}/here-is-one-hand.it.md", encoding="utf-8").read()}
BY = {a["id"]: a for a in A}
PRE = [a for a in A if a["study"] == "preregistered"]
APPS = ("ChatGPT", "Claude", "Gemini")
H1_TYPES = ("other_sessions", "outside_and_intraday", "history", "premise_hypothesis")
H1 = [c for c in CL if c["type"] in H1_TYPES and c["in_words"] == "no" and BY[c["answer_id"]]["study"] == "preregistered"]
EV = {E[k]["ticker"]: k for k in E}
MONTH_EN = {9: "September", 10: "October"}
MONTH_IT = {9: "settembre", 10: "ottobre"}


def it_num(s):
    return float(s.replace(".", "").replace(",", "."))


def fe(x, d=2):
    return f"{x:,.{d}f}"


def fi(x, d=2):
    return fe(x, d).replace(",", "\0").replace(".", ",").replace("\0", ".")


def d_(iso):
    return date.fromisoformat(iso)


def day_en(iso):
    return f"{d_(iso).day} {MONTH_EN[d_(iso).month]}"


def day_it(iso):
    return f"{d_(iso).day} {MONTH_IT[d_(iso).month]}"


def pct(k, n, d=1):
    return round(100 * k / n, d)


def claim(aid, needle):
    hits = [c for c in CL if c["answer_id"] == aid and needle in c["quote_it"]]
    assert hits, (aid, needle)
    return hits[0]


def fig(aid, q):
    hits = [f for f in F if f["answer_id"] == aid and f["quantity"] == q]
    assert hits, (aid, q)
    return hits[0]


FACTS = []
FAIL = []


def need(label, ok, en, it):
    if not ok:
        FAIL.append(f"data: {label}")
    FACTS.append((label, en, it))


# ---- header
H = AN["H1"]["all"]
sp_w, sp_n = H["session_prices"]["wrong"], H["session_prices"]["verified"]
ot_w, ot_n = H["group_A_pooled"]["wrong"], H["group_A_pooled"]["verified"]
need("session prices wrong", (sp_w, sp_n) == (28, 1040), f"{sp_w} times in {fe(sp_n, 0)}", f"{sp_w} volte su {fi(sp_n, 0)}")
need("other numbers wrong", (ot_w, ot_n) == (54, 408), f"{ot_w} times in {ot_n}", f"{ot_w} volte su {ot_n}")
ses = sorted(e["session"] for e in E.values())
need("twelve sessions", len(E) == 12, "Twelve stock sessions", "Dodici sedute")
need("session span", (ses[0], ses[-1]) == ("2026-10-12", "2026-10-23"), "between 12 and 23 October 2026", "fra il 12 e il 23 ottobre 2026")
sent = sorted({a["sent_new_york"][:10] for a in PRE})
need("sent days", sent == ["2026-10-25", "2026-10-26"], "on 25 and 26 October", "il 25 e il 26 ottobre")
need("three questions", {a["type"] for a in PRE} == {"A", "C", "U"}, "Three questions per session", "Tre domande per seduta")
n_app = Counter(a["app"] for a in PRE)
n_expl = sum(a["study"] == "exploration" and a["app"] == "Gemini" for a in A)
need("answers", (len(PRE), n_expl) == (217, 54), f"{len(PRE)} answers, plus {n_expl} from Gemini", f"{len(PRE)} risposte, più {n_expl} di Gemini")
need("answers per app", (n_app["Gemini"], n_app["ChatGPT"], n_app["Claude"]) == (49, 84, 84),
     f"Gemini gave {n_app['Gemini']} answers against {n_app['ChatGPT']}", f"Gemini ha dato {n_app['Gemini']} risposte contro le {n_app['ChatGPT']}")

# ---- 13 October
c = E["01"]
mv = float(c["change_close_pct"])
need("Citigroup session", c["session"] == "2026-10-13", "## 13 October", "## Il 13 ottobre")
need("Citigroup move", (round(mv, 2), float(c["close"]), float(c["previous_close"])) == (-5.60, 124.53, 131.92),
     f"on 13 October and closed down {fe(-mv)} per cent, at {fe(float(c['close']))} dollars from {fe(float(c['previous_close']))}",
     f"il 13 ottobre e ha chiuso in calo del {fi(-mv)} per cento, a {fi(float(c['close']))} dollari da {fi(float(c['previous_close']))}")
f_pc, f_ch = fig("s2-01A-1-claude", "previous_close"), fig("s2-01A-1-claude", "change_close_pct")
need("Claude previous close and change exact", f_pc["outcome"] == f_ch["outcome"] == "exact", "to the cent", "al centesimo")
c38, c123 = claim("s2-01A-1-claude", "3,8%"), claim("s2-01A-1-claude", "123,20")
need("3.8 right", c38["outcome"] == "right", "about 3.8 per cent", "circa il 3,8 per cento")
need("123.20 right", c123["outcome"] == "right", "around 123.20 dollars", "intorno ai 123,20 dollari")
c10 = claim("s2-01A-1-claude", "circa il 10%")
m = re.search(r"2026-09-14 (\d+,\d+)", c10["reference_it"])
sep14 = it_num(m.group(1))
pre_month = (CLOSE[("C", "2026-10-12")] / sep14 - 1) * 100
post_month = (CLOSE[("C", "2026-10-14")] / sep14 - 1) * 100
need("Citigroup month before", c10["outcome"] == "wrong" and round(pre_month, 2) == -3.13 and round(post_month) == -10,
     f"from 14 September to 12 October, the eve of the results, the stock went from {fe(sep14)} to {fe(CLOSE[('C', '2026-10-12')])}. Down {fe(-pre_month)} per cent",
     f"dal 14 settembre al 12 ottobre, la vigilia dei conti, il titolo è passato da {fi(sep14)} a {fi(CLOSE[('C', '2026-10-12')])}. Meno {fi(-pre_month)} per cento")
c10b = claim("s2-01A-3-claude", "circa il 10%")
need("repeated in A3", c10b["outcome"] == "wrong" and BY["s2-01A-3-claude"]["type"] == "A", "Another answer from the same app, to the same question",
     "Un'altra risposta della stessa app, alla stessa domanda")

# ---- what search changes
CP = [a for a in PRE if a["type"] == "C"]
corr = sum(a["premise"] == "corrected" for a in CP)
need("premise corrected", (corr, len(CP)) == (58, 60), f"Of the {len(CP)} pre-registered answers to it, {corr} corrected",
     f"Delle {len(CP)} risposte preregistrate, {corr} hanno corretto")
AP = [a for a in PRE if a["type"] == "A" and a["prices"] != "none_given"]
need("direction right", len(AP) == 82 and all(a["direction"] == "right" for a in AP), f"in every one of the {len(AP)} answers to A",
     f"in tutte le {len(AP)} risposte ad A")
sec = H["company_data_sec_sample"]
need("SEC sample", (sec["wrong"], sec["verified"]) == (1, 53), f"one was wrong out of the {sec['verified']}", f"uno sui {sec['verified']} verificabili")
mm = {app: (AN["main"][app]["errors"]["k"], AN["main"][app]["errors"]["n"]) for app in APPS}
need("main measure by answer", mm == {"ChatGPT": (2, 36), "Claude": (6, 36), "Gemini": (1, 10)},
     f"at least one price was wrong in {mm['ChatGPT'][0]} of ChatGPT's {mm['ChatGPT'][1]} answers to A, {mm['Claude'][0]} of Claude's {mm['Claude'][1]} and {mm['Gemini'][0]} of Gemini's {mm['Gemini'][1]}",
     f"almeno un prezzo era sbagliato in {mm['ChatGPT'][0]} delle {mm['ChatGPT'][1]} risposte di ChatGPT ad A, in {mm['Claude'][0]} delle {mm['Claude'][1]} di Claude e in {mm['Gemini'][0]} delle {mm['Gemini'][1]} di Gemini")
co = AN["concordance_A"]
agree = (co["ChatGPT"]["agree"] + co["Claude"]["agree"]) / (co["ChatGPT"]["pairs"] + co["Claude"]["pairs"])
need("agreement", round(co["ChatGPT"]["pct"]) == round(co["Claude"]["pct"]) == round(100 * agree) == 94, "94 times in a hundred", "94 volte su cento")

# ---- where the error goes
rate = (ot_w / ot_n) / (sp_w / sp_n)
need("other numbers rate", pct(ot_w, ot_n) == 13.2 and round(rate) == 5, f"{ot_n} could be checked against the record. {ot_w} were wrong, {fe(pct(ot_w, ot_n), 1)} per cent, about five times",
     f"{ot_n} si potevano controllare sul registro. {ot_w} erano sbagliati, il {fi(pct(ot_w, ot_n), 1)} per cento, circa cinque volte")
K = {k: (H[k]["wrong"], H[k]["verified"]) for k in H1_TYPES}
need("by kind", (K["premise_hypothesis"], K["other_sessions"], K["outside_and_intraday"], K["history"]) == ((13, 46), (24, 141), (15, 186), (2, 35)),
     f"wrong {K['premise_hypothesis'][0]} times in {K['premise_hypothesis'][1]}, the numbers from other sessions {K['other_sessions'][0]} in {K['other_sessions'][1]}, those from the pre-market, the after-hours and the moments of the day {K['outside_and_intraday'][0]} in {K['outside_and_intraday'][1]}, the comparisons with history {K['history'][0]} in {K['history'][1]}",
     f"sbagliate {K['premise_hypothesis'][0]} volte su {K['premise_hypothesis'][1]}, i numeri di altre sedute {K['other_sessions'][0]} su {K['other_sessions'][1]}, quelli del pre-market, del dopo-borsa e dei momenti della giornata {K['outside_and_intraday'][0]} su {K['outside_and_intraday'][1]}, i confronti storici {K['history'][0]} su {K['history'][1]}")
moment = sum(int(r["wrong"] or 0) for r in HA if r["origin_it"] in ("istantanea fuori tempo", "momento sbagliato"))
untraced = sum(int(r["wrong"] or 0) for r in HA if r["origin_it"] == "non rintracciabile")
need("most from the wrong moment", (moment, untraced, ot_w) == (34, 13, 54) and moment / ot_w > 0.5 and sum(int(r["wrong"] or 0) for r in HA) == ot_w,
     f"By the origin recorded for each answer, {moment} of the {ot_w} are the right number from the wrong moment, and {untraced} cannot be traced",
     f"Secondo l'origine registrata per ogni risposta, {moment} dei {ot_w} sono il numero giusto del momento sbagliato, e {untraced} non si possono ricondurre a nulla")
ip = E["09"]
need("International Paper", (ip["session"], round(float(ip["change_close_pct"]), 2)) == ("2026-10-15", 6.90),
     f"rose {fe(float(ip['change_close_pct']))} per cent on {day_en(ip['session'])}", f"salita del {fi(float(ip['change_close_pct']))} per cento il {day_it(ip['session'])}")
pe = any("private equity" in T[a["id"]].lower() and "europe" in T[a["id"]].lower() for a in PRE if a["event"] == "09")
need("IP private equity report in the answers", pe, "private equity funds were looking at its European packaging business",
     "alcuni fondi di private equity guardavano alla sua attività europea di imballaggi")
lon = claim("s2-09A-1-claude", "2.580")
lon_close = it_num(re.search(r"15/10 .*?chiusura (\d+,\d+)", lon["reference_it"]).group(1)) * 100
need("London 2,580 = the 16:00–16:15 bar; IBKR close 2,600", lon["outcome"] == "wrong" and "25,80 è la chiusura della barra 16:00–16:15" in lon["note_it"] and lon_close == 2600,
     f"in IBKR's prices the London line closed at {fe(lon_close, 0)} pence, and 2,580 is the price of the quarter hour that ended at 16:15",
     f"nei prezzi di IBKR la linea di Londra ha chiuso a {fi(lon_close, 0)} pence, e 2.580 è il prezzo del quarto d'ora che finiva alle 16:15")
hs = E["07"]
need("Hasbro", (hs["session"], round(float(hs["change_close_pct"]), 2)) == ("2026-10-20", 11.20),
     f"on {day_en(hs['session'])} and rose {fe(float(hs['change_close_pct']))} per cent", f"il {day_it(hs['session'])} ed è salita dell'{fi(float(hs['change_close_pct']))} per cento")
wed = (CLOSE[("HAS", "2026-10-21")] / CLOSE[("HAS", "2026-10-20")] - 1) * 100
thu = (CLOSE[("HAS", "2026-10-22")] / CLOSE[("HAS", "2026-10-21")] - 1) * 100
need("Hasbro Wednesday and Thursday", claim("s2-07A-1-claude", "4,1%")["outcome"] == "wrong" and d_("2026-10-21").weekday() == 2 and (round(wed, 2), round(thu, 2)) == (4.09, 2.83),
     f"{fe(wed)} was Wednesday's gain. Thursday's was {fe(thu)}", f"il {fi(wed)} è il rialzo di mercoledì. Giovedì il titolo ha fatto {fi(thu)}")
pm = claim("s2-09C-1-claude", "33,92")
need("IP pre-market", pm["outcome"] == "wrong" and "max 33,66" in pm["reference_it"] and "seduta regolare" in pm["note_it"] and BY["s2-09C-1-claude"]["type"] == "C"
     and "si fermano alle 9:14" in [r for r in HA if r["answer_id"] == "s2-09C-1-claude"][0]["notes_it"],
     "in the pre-market data, which stop at 9:14, the stock went no higher than 33.66. It traded at 33.92 after the open",
     "nei dati del pre-market, che si fermano alle 9:14, il titolo non è andato oltre 33,66. A 33,92 ha trattato dopo l'apertura")
CW = [c for c in H1 if c["app"] == "Claude" and c["outcome"] == "wrong"]
by_fig = lambda s: len({c["answer_id"] for c in CW if s in c["quote_it"]})
need("2,580 in three answers", by_fig("2.580") == 3, "The 2,580 pence appears in three of Claude's answers", "I 2.580 pence compaiono in tre risposte di Claude")
need("33.92 in three answers", by_fig("33,92") == 3, "The 33.92 in the pre-market appears in three", "I 33,92 nel pre-market compaiono in tre")
need("Citigroup 10% in two answers", len({c["answer_id"] for c in CW if c["event"] == "01" and "10%" in c["quote_it"]}) == 2,
     "Citigroup's ten per cent in two", "il dieci per cento di Citigroup in due")
NUM = re.compile(r"\d+(?:[.,]\d+)*")
toks = lambda c: set(NUM.findall(c["quote_it"])) - {str(y) for y in range(2000, 2031)}
recur = sum(any(c["event"] == d["event"] and d["answer_id"] != c["answer_id"] and toks(c) & toks(d) for d in CW) for c in CW)
need("recurrence", (len(CW), recur) == (41, 23), f"Of Claude's {len(CW)} wrong numbers, {recur} recur", f"Dei {len(CW)} numeri sbagliati di Claude, {recur} ricorrono")
lm = claim("s2-08C-2-claude", "5,5%")
m1, m2 = re.search(r"chiusura 21/10/2024 (\d+,\d+)", lm["reference_it"]), re.search(r"22/10/2024 .*?chiusura (\d+,\d+)", lm["reference_it"])
lm_mv = (it_num(m2.group(1)) / it_num(m1.group(1)) - 1) * 100
need("Lockheed 2024", lm["outcome"] == "wrong" and BY["s2-08C-2-claude"]["type"] == "C" and round(lm_mv, 2) == -6.12, f"They had lost {fe(-lm_mv)}", f"Avevano perso il {fi(-lm_mv)}")

# ---- three ways of being right
P = {}
for app in APPS:
    n = n_app[app]
    hh = AN["H1"][app]
    allc = sum(c["app"] == app for c in H1)
    ok = [c for c in H1 if c["app"] == app and c["outcome"] in ("right", "wrong")]
    q = lambda t: (sum(c["outcome"] == "wrong" for c in ok if c["question_type"] == t), sum(c["question_type"] == t for c in ok))
    P[app] = dict(per=round(allc / n, 1), wper=round(hh["group_A_pooled"]["wrong"] / n, 2), sp=(hh["session_prices"]["wrong"], hh["session_prices"]["verified"]),
                  ot=(hh["group_A_pooled"]["wrong"], hh["group_A_pooled"]["verified"]), C=q("C"), A=q("A"), h2=AN["H2"][app]["per_answer"])
g, cl, ge = P["ChatGPT"], P["Claude"], P["Gemini"]
need("ChatGPT volume", (g["per"], g["h2"], cl["h2"]) == (0.7, 10.2, 19.4),
     f"few other numbers, {fe(g['per'], 1)} per answer. Altogether it gives {fe(g['h2'], 1)} numbers per answer against Claude's {fe(cl['h2'], 1)}",
     f"pochi altri numeri, {fi(g['per'], 1)} per risposta. In tutto dà {fi(g['h2'], 1)} numeri per risposta contro i {fi(cl['h2'], 1)}")
need("ChatGPT errors", (g["sp"], g["ot"]) == ((4, 421), (3, 60)), f"wrong {g['sp'][0]} times in its {g['sp'][1]} figures about the session, {g['ot'][0]} times in its {g['ot'][1]}",
     f"Sbaglia {g['sp'][0]} volte sulle sue {g['sp'][1]} cifre sulla seduta, {g['ot'][0]} volte sui suoi {g['ot'][1]}")
gm = [f for f in F if f["app"] == "ChatGPT" and f["outcome"] == "error" and f["study"] == "preregistered"]
gm_open = [f for f in gm if f["event"] == "03" and f["quantity"] == "open" and float(f["value_low"]) == 77.0]
need("GM open three of four", (len(gm_open), len(gm)) == (3, 4) and float(E["03"]["open_nasdaq"]) == 77.22, "Three of the four price errors are one number, General Motors' open",
     "Tre dei quattro errori nei prezzi sono un numero solo, l'apertura di General Motors")
need("GM 77.00 against Nasdaq", float(E["03"]["open_nasdaq"]) == 77.22, "General Motors' open, 77.00 against the 77.22 Nasdaq recorded",
     "l'apertura di General Motors, 77,00 contro i 77,22 registrati da Nasdaq")
gm_ids = sorted(f["answer_id"] for f in gm_open)
alone = [i for i in gm_ids if "77,22" not in T[i]]
after = [i for i in gm_ids if "77,22" in T[i] and T[i].find("77,22") < T[i].find("77,00") and "LSEG" in T[i] and "invece" in T[i]]
need("GM once alone, twice after 77.22", (alone, len(after)) == (["s2-03A-2-chatgpt"], 2), "Twice it comes after the right 77.22", "Due volte viene dopo i 77,22 giusti")
need("Claude volume", (cl["per"], cl["ot"], pct(*cl["ot"])) == (3.7, (41, 296), 13.9),
     f"{fe(cl['per'], 1)} other numbers per answer. It is wrong in {cl['ot'][0]} of the {cl['ot'][1]} that could be checked, {fe(pct(*cl['ot']), 1)} per cent",
     f"{fi(cl['per'], 1)} altri numeri per risposta. Ne sbaglia {cl['ot'][0]} dei {cl['ot'][1]} controllabili, il {fi(pct(*cl['ot']), 1)} per cento")
CAN = [a for a in PRE if a["app"] == "Claude" and a["type"] == "C"]
need("Claude corrects every premise", len(CAN) == 24 and all(a["premise"] == "corrected" for a in CAN), "which Claude corrects every time", "che Claude corregge ogni volta")
ip_w = sum(c["event"] == "09" for c in CW)
top = Counter(c["answer_id"] for c in CW).most_common(1)[0]
need("Claude clusters", (ip_w, top) == (14, ("s2-09A-1-claude", 8)), "14 of the 41 are about International Paper, 8 of them in a single answer",
     "14 dei 41 riguardano International Paper, 8 dei quali in una sola risposta")


def wilson(k, n, z=1.96):
    p, d = k / n, 1 + z * z / n
    c, h = (p + z * z / (2 * n)) / d, z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5 / d
    return c - h, c + h


need("Claude C and A intervals overlap", wilson(*cl["C"])[0] < wilson(*cl["A"])[1], "though the two intervals overlap", "anche se i due intervalli si sovrappongono")
need("Claude session prices", cl["sp"] == (12, 457), f"{cl['sp'][0]} wrong in {cl['sp'][1]}", f"{cl['sp'][0]} su {cl['sp'][1]}")
need("wrong per answer", (cl["wper"], g["wper"]) == (0.49, 0.04), f"{fe(cl['wper'])} per answer against ChatGPT's {fe(g['wper'])}",
     f"{fi(cl['wper'])} per risposta contro lo {fi(g['wper'])}")
need("Claude C against A", (cl["C"], pct(*cl["C"]), pct(*cl["A"])) == ((17, 75), 22.7, 11.6),
     f"{cl['C'][0]} of its {cl['C'][1]} other numbers are wrong, {fe(pct(*cl['C']), 1)} per cent, against {fe(pct(*cl['A']), 1)}",
     f"{cl['C'][0]} dei suoi {cl['C'][1]} altri numeri, il {fi(pct(*cl['C']), 1)} per cento, contro l'{fi(pct(*cl['A']), 1)}")
GP = [a for a in PRE if a["app"] == "Gemini"]
ns = [a for a in GP if a["search"] != "used"]
un = sum(a["search"] == "unavailable" for a in ns)
nu = sum(a["search"] == "not_used" for a in ns)
need("Gemini without search", (len(ns), un, nu, len(GP)) == (23, 15, 8, 49), f"In {len(ns)} of its {len(GP)} answers it did not search. Search was unavailable in {un} and unused in {nu}",
     f"In {len(ns)} delle sue {len(GP)} risposte non ha cercato. La ricerca non era disponibile in {un} e non è stata usata in {nu}")
opens = all(re.match(r"Non (dispongo|avendo accesso)", T[a["id"]].strip()) for a in ns)
need("all 23 open with no access", opens, "Each of the 23 opens by saying it has no access", "Tutte e 23 cominciano dicendo di non avere accesso")
noprice = [a for a in ns if a["prices"] == "none_given"]
rest = [a for a in ns if a["prices"] != "none_given"]
need("21 give no prices, the other two adopt", len(noprice) == 21 and len(rest) == 2 and all(a["premise"] == "adopted" for a in rest),
     "21 give no prices", "21 non danno prezzi")
need("the other two", len(rest) == 2, "The other two come in the next section", "Le altre due sono nella sezione che segue")
mu = fig("s2-06U-1-gemini", "open")
mu_json = [f for f in F if f["answer_id"] == "s2-06U-1-gemini" and f["quantity"] == "open" and f["outcome"] == "error"][0]
mu_note = claim("s2-06U-1-gemini", "862,29")["note_it"]
gap_days = (d_("2026-10-23") - d_(E["06"]["session"])).days
need("Micron open", mu["outcome"] == "exact" and float(mu["value_low"]) == 1002.45, "gave the open, 1,002.45", "Dà l'apertura, 1.002,45")
need("Micron JSON = open of 23 October", float(mu_json["value_low"]) == 862.29 and "apertura Nasdaq del 23/10 (862,29)" in mu_note and gap_days == 11,
     "That is Micron's open eleven days later, on 23 October", "È l'apertura di Micron di undici giorni dopo, il 23 ottobre")
GW = [c for c in H1 if c["app"] == "Gemini" and c["outcome"] == "wrong"]
gtop = Counter(c["answer_id"] for c in GW).most_common(1)[0]
need("Gemini half in one answer on Datadog", gtop == ("s2-11C-1-gemini", 5) and len(GW) == 10 and E["11"]["ticker"] == "DDOG",
     "half of them in one answer to the false premise, on Datadog", "la metà in una sola risposta alla premessa falsa, su Datadog")
need("Gemini other numbers", (ge["ot"], pct(*ge["ot"]), AN["H1"]["Gemini"]["premise_hypothesis"]["wrong"]) == ((10, 52), 19.2, 6),
     f"{ge['ot'][0]} in {ge['ot'][1]} are wrong, {fe(pct(*ge['ot']), 1)} per cent", f"ne sbaglia {ge['ot'][0]} su {ge['ot'][1]}, il {fi(pct(*ge['ot']), 1)} per cento")

# ---- when search is missing
GC = [a for a in GP if a["type"] == "C"]
adopt = [a for a in GC if a["premise"] == "adopted"]
need("twice without search, adopted", len(adopt) == 2 and all(a["search"] == "unavailable" for a in adopt) and {a["event"] for a in adopt} == {"07", "08"},
     "Twice Gemini answered a false premise without search", "Due volte Gemini ha risposto a una premessa falsa senza la ricerca")
need("Hasbro rose", True, f"Hasbro rose {fe(float(hs['change_close_pct']))} per cent on {day_en(hs['session'])}",
     f"Hasbro è salita dell'{fi(float(hs['change_close_pct']))} per cento il {day_it(hs['session'])}")
need("Hasbro question", "scesa di circa l'11%" in hs["question_C"], "fallen about 11", "scesa di circa l'11")
lk = E["08"]
need("Lockheed rose", (lk["session"], round(float(lk["change_close_pct"]), 2)) == ("2026-10-22", 6.96) and "scesa di circa il 7%" in lk["question_C"],
     f"Lockheed Martin rose {fe(float(lk['change_close_pct']))} per cent on {day_en(lk['session'])}",
     f"Lockheed Martin è salita del {fi(float(lk['change_close_pct']))} per cento il {day_it(lk['session'])}")
need("Lockheed answer through October 2024", "22 ottobre 2024" in T["s2-08C-1-gemini"] and lm_mv < 0,
     "the Lockheed one through the results of October 2024, when the stock had fallen", "quella su Lockheed attraverso i conti dell'ottobre 2024, quando il titolo era sceso davvero")
other = [a for a in GC if a not in adopt]
need("the other ten, with search, corrected", len(other) == 10 and all(a["search"] == "used" and a["premise"] == "corrected" for a in other),
     "The other ten times Gemini met the false premise it had search, and it corrected it all ten times",
     "Le altre dieci volte che Gemini ha incontrato la premessa falsa aveva la ricerca, e l'ha corretta tutte e dieci")

# ---- the hours
GA = [a for a in GP if a["type"] == "A"]
rnd = {r: {a["event"]: a for a in GA if a["repetition"] == r} for r in ("1", "2")}
with1 = [e for e, a in rnd["1"].items() if a["prices"] != "none_given"]
ref2 = [e for e in with1 if rnd["2"][e]["refused"] == "yes"]
t2 = sorted(a["sent_new_york"] for a in rnd["2"].values())
span = (int(t2[-1][11:13]) * 60 + int(t2[-1][14:16])) - (int(t2[0][11:13]) * 60 + int(t2[0][14:16]))
need("same questions, refused an hour later", (len(rnd["1"]), len(with1), len(ref2)) == (12, 8, 7) and t2[0][:10] == t2[-1][:10] == "2026-10-26" and span < 60 and "12:00" <= t2[0][11:16],
     f"In the first round it gave prices for {len(with1)} of its {len(rnd['1'])} questions A. Asked the same questions again on the Monday afternoon, within the hour, it refused {len(ref2)} of those {len(with1)}",
     f"Nel primo giro ha dato i prezzi per {len(with1)} delle sue {len(rnd['1'])} domande A. Alle stesse domande, rifatte il lunedì pomeriggio nel giro di un'ora, ne ha rifiutate {len(ref2)} su {len(with1)}")
band = lambda a: "13:20" <= a["sent_new_york"][11:16] <= "15:26"
inb = [a for a in GP if band(a)]
outA = [a for a in GA if not band(a)]
ref = lambda xs: sum(a["refused"] == "yes" for a in xs)
hb = AN["H4"]["Gemini_by_band_preregistered"]
need("band", (len(inb), ref(inb), len(outA), ref(outA)) == (16, 13, 9, 2) and all(a["type"] == "A" for a in inb) and (hb["13:20–15:26"]["n"], hb["13:20–15:26"]["k"]) == (16, 13)
     and all(a["refused"] == "no" for a in GP if a["type"] != "A"),
     f"All {len(inb)} of its pre-registered answers sent between 13:20 and 15:26 New York time were to A, and {ref(inb)} were refusals. Of its other {len(outA)} answers to A, {ref(outA)}.",
     f"Le sue {len(inb)} risposte preregistrate inviate fra le 13:20 e le 15:26 di New York erano tutte ad A, e {ref(inb)} erano rifiuti. Delle altre {len(outA)} risposte ad A, {ref(outA)}.")
E3 = [a for a in A if a["study"] == "exploration" and a["round"] == "E3"]
need("Tuesday morning, outside the plan", (len(E3), ref(E3)) == (9, 5) and all(d_(a["sent_new_york"][:10]).weekday() == 1 and a["sent_new_york"][11:13] < "12" for a in E3),
     "the refusals came back on the Tuesday morning, 5 in 9", "i rifiuti sono tornati il martedì mattina, 5 su 9")

# ---- why it matters
SPO = {app: (P[app]["sp"], P[app]["ot"]) for app in APPS}
need("in each app, other moments wrong more often than session prices", all(o[0] / o[1] > sp[0] / sp[1] for sp, o in SPO.values()),
     "ChatGPT {0} in {1} against {2} in {3}, Claude {4} in {5} against {6} in {7}, Gemini {8} in {9} against {10} in {11}".format(
         *[x for app in APPS for x in (*SPO[app][1], *SPO[app][0])]),
     "ChatGPT {0} su {1} contro {2} su {3}, Claude {4} su {5} contro {6} su {7}, Gemini {8} su {9} contro {10} su {11}".format(
         *[x for app in APPS for x in (*SPO[app][1], *SPO[app][0])]))
need("about one in eight", abs(ot_w / ot_n - 1 / 8) < 0.01, "about one in eight is wrong", "circa una su otto è sbagliata")
need("twice, Gemini without search", len(adopt) == 2, "Twice, Gemini without search explains", "Due volte Gemini, senza la ricerca, spiega")

# ---- quotations: the Italian against the answers, in the answer each is given to
QUOTES = [  # (start of the quotation, answers it may come from: a regex on the id, or 'question C' of an event)
    ("Dai 131,92", r"s2-01A-1-claude"), ("Inoltre Citi arrivava", r"s2-01A-1-claude"), ("nel mese precedente", r"s2-01A-3-claude"),
    ("Citigroup è salita", "question C 01"), ("C'è una precisazione", r"s2-01C-\d-chatgpt"), ("In realtà è andata", r"s2-01C-\d-claude"),
    ("A Londra", r"s2-09A-1-claude"), ("Giovedì il titolo", r"s2-07A-1-claude"), ("Già nel pre-market", r"s2-09C-1-claude"),
    ("E proprio il 22 ottobre", r"s2-08C-2-claude"), ("Secondo i dati storici", r"s2-03A-2-chatgpt"), ("invece", r"s2-03U-\d-chatgpt"), ("Non dispongo dell'accesso ai dati di mercato aggiornati e", r"s2-01A-2-gemini"),
    ("il parametro open_price", r"s2-06U-1-gemini"), ("Non dispongo dell'accesso ai dati finanziari", r"s2-07C-1-gemini"), ("un ribasso a doppia cifra", r"s2-07C-1-gemini"),
    ("Non avendo accesso", r"s2-08C-1-gemini"), ("a metà pomeriggio", r"s2-01A-1-claude"), ("Inoltre Citi arrivava", r"s2-01A-1-claude"),
    ("circa", r"s2-01A-1-claude"), ("Alliance News", r"s2-09A-1-claude"), ("A Londra", r"s2-09A-1-claude"),
]
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace(" ", " ")).strip()
qit = re.findall(r"«([^»]*)»", TXT["it"])
qen = re.findall(r'"([^"]*)"', TXT["en"])
if len(qit) != len(QUOTES):
    FAIL.append(f"quotes: {len(qit)} in the Italian, {len(QUOTES)} expected")
for q, (start, src) in zip(qit, QUOTES):
    nq = norm(q).rstrip(".")
    if not nq.startswith(norm(start)):
        FAIL.append(f"quote order: «{q[:40]}» where «{start}» was expected")
        continue
    if src.startswith("question C"):
        ok = nq in norm(E[src.split()[-1]]["question_C"])
    else:
        ok = any(re.fullmatch(src, k) and nq in norm(t) for k, t in T.items())
    if not ok:
        FAIL.append(f"quote not found word for word in {src}: «{q}»")

EN_NUM = re.compile(r"(?<![\w.,])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.,])\d+(?:\.\d+)?")
IT_NUM = re.compile(r"(?<![\w.,])\d{1,3}(?:\.\d{3})+(?:,\d+)?|(?<![\w.,])\d+(?:,\d+)?")
en_v = lambda s: sorted(float(x.replace(",", "")) for x in EN_NUM.findall(s))
it_v = lambda s: sorted(it_num(x) for x in IT_NUM.findall(s))
if len(qen) != len(qit):
    FAIL.append(f"quotes: {len(qen)} in the English, {len(qit)} in the Italian")
for a, b in zip(qen, qit):
    if en_v(a) != it_v(b):
        FAIL.append(f'quote numbers differ: "{a[:50]}" against «{b[:50]}»')

# ---- every phrase in the text, and no number left over
for lang, rx, qrx in (("en", EN_NUM, r'"[^"]*"'), ("it", IT_NUM, r"«[^»]*»")):
    t = TXT[lang]
    body = t[: t.rfind("\n---")]                        # the licence line stays out
    body = re.sub(r"\]\([^)]*\)", "]", body)          # link targets stay out
    covered = [False] * len(body)
    for s, e in ((m.start(), m.end()) for m in re.finditer(qrx, body)):
        covered[s:e] = [True] * (e - s)
    for label, en, it in FACTS:
        phrase = en if lang == "en" else it
        hits = [m.span() for m in re.finditer(re.escape(phrase), body)]
        if not hits:
            FAIL.append(f"{lang}: phrase not in the text [{label}]: {phrase}")
        for s, e in hits:
            covered[s:e] = [True] * (e - s)
    for m in rx.finditer(body):
        if not all(covered[m.start():m.end()]):
            line = body[: m.start()].count("\n") + 1
            FAIL.append(f"{lang}: unchecked number {m.group(0)} at line {line}: …{body[max(0, m.start() - 40):m.end() + 20]!r}…")

print(f"{len(FACTS)} statements, {len(qit)} quotations, both languages")
if FAIL:
    print("\n".join(FAIL))
    sys.exit(1)
print("every number and every quotation checks against the data")
