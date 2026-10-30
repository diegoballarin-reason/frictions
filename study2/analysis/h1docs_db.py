"""H1 · dalle proposte (h1_docs.json) ai documenti per la pagina (/home/claude/h1db/h1-*.json).
- Ricalcola la frase «Per scelta: N (analisti e mercato a, dati aziendali b)» dai conteggi.
- Sostituisce le osservazioni del passaggio P dove gli esiti finali non coincidono più con il suo testo (OSS, scritte da Claude il 30 ottobre).
- Le motivazioni della riconciliazione e dei controlli aggiunti restano nel campo «disaccordo» (la pagina le mostra a parte).
- Scrive solo i documenti cambiati rispetto all'ultima versione caricata (elenco in h1db/changed.json)."""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/claude/h1db"
STAMP = sys.argv[1] if len(sys.argv) > 1 else None   # updatedAt per i documenti cambiati
docs = json.load(open(os.path.join(D, "h1_docs.json")))

OSS = {
 "s2-02A-1-claude": "Sbagliato: «verso le 11 di New York … a 237,46 dollari»: tra le 10:55 e le 11:10 il titolo oscilla tra 233,17 e 234,72; 237,46 è il prezzo delle 10:20-10:40. Giusti: chiusura del 21/10 −1% (−1,00%); dopo-borsa del 21/10 a 241,57, circa −7,4% (239,12–262,26; −7,38%); in mattinata −9/−10% (−10,97%…−7,17%); verso le 11 circa −9% (finestra −10,60%…−10,00%, al limite della tolleranza); 23/10 a 230,10 esatto; «più del doppio della media giornaliera» (rapporti fra 2,20 e 2,64 per le finestre da 10 a 90 sedute; numero in lettere aggiunto). Non verificati: media giornaliera di circa 10,7 milioni (finestra più vicina 90 sedute 10.460.045, +2,29%). Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-05A-1-claude": "Nessun numero del gruppo A sbagliato. «Livello più basso da gennaio 2023» giusto (ultima chiusura ≤ 28,12 il 6/1/2023, anche per i minimi); −24% da inizio anno esatto (37,00 → 28,12); «circa il 33,6% in dodici mesi» giusto (−33,62% con i dodici mesi di calendario, base IBKR 42,36 del 21/10/2025; −32,45% a 252 sedute, anch'esso entro 1,2 punti); chiusura del 23/10 a 27,52 esatta; rilevazioni intraday attribuite ad articoli (−4,1%, −4,7% a 28,25) giuste come livelli (27,87–29,10). Non verificati: nessuno. Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-05A-2-claude": "Nessun numero del gruppo A sbagliato. Minimi da gennaio 2023 giusto (6/1/2023); −24% da inizio anno esatto; chiusura del 23/10 a 27,52 esatta; «ultimi 12 mesi −33,62%» esatto con i dodici mesi di calendario (chiusura IBKR del 21/10/2025 42,36; a 252 sedute sarebbe −32,45%). Non verificati: nessuno. Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-05U-1-claude": "Nessun numero del gruppo A sbagliato. Seduta del 23/10: apertura 27,93 e chiusura 27,52 esatte. Esclusa: chiusura di TokenPost 28,09, che la risposta riporta solo per scartarla (come proposto per le U; sarebbe giusta come ultimo scambio delle 15:59). Non verificati: nessuno. Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-06A-1-claude": "Nessun numero del gruppo A sbagliato. +261% da inizio anno alla chiusura del 9/10 giusto per arrotondamento (+260,53%); «terza seduta negativa di fila» giusto (7/10 in rialzo, 8, 9 e 12/10 in calo). Non verificati: «circa l’1%» nelle contrattazioni overnight (la sessione notturna 20:00–04:00 non è nei riferimenti; letto come pre-market sarebbe giusto: primo scambio delle 4:00 a 1.018,70, −1,00%). Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-06U-1-gemini": "Gruppo A: la rilevazione delle 9:30 a 1.000,50, data a parte rispetto all'apertura consolidata, è un punto a un orario: giusta (barre 9:25–9:40: 978,50–1.004,86). Da segnalare per la valutazione di seduta: 862,29, 856,49, 877,55 e il volume «complessivo» 21.249.884 coincidono con apertura del 23/10, chiusura del 22/10, chiusura del 23/10 e volume del 23/10 (21.249.880): dati di sedute successive attribuiti al 12/10. Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-07C-2-claude": "Gruppo A: «rialzo di circa il 28% in tre mesi» con cui il titolo «arrivava» all’evento sbagliato: con tre mesi di calendario +20,77% fino alla vigilia (dal 17/07, 81,55) e +34,23% fino all’evento (dal 20/07, 81,59); a 63 sedute (22/07, 89,04) +10,61% e +23,00%; +28,03% solo dal 22/07 al 21/10 (114,00), dato successivo all’evento. Giusti: «circa +6%» a metà seduta (11:30–14:00: 103,74–108,58) e nuovo massimo a 52 settimane (107,93 alle 09:35 > 106,98). Non verificati: ipotesi del 26/10/2023 «circa l’11,65%» (dati del 2023 non nel kit). Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-08A-1-claude": "Rialzo dopo la trimestrale di luglio «del 10,5%» giusto (seduta del 23/07/2026 +10,54%, sheets). «Balzo giornaliero più forte da mesi» senza numero, coerente con l'ultimo rialzo maggiore (23/07). Non verificati: «tornato sopra la media mobile a 200 giorni» (parametro aggiunto; servono 200 chiusure). Esclusi 7: cinque secondi estremi di intervalli, la fonte «24/7 Wall St», la sigla F-35. Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-09U-2-claude": "Rapporto «quasi il doppio della media» sbagliato: volume 9.007.359 / media = 1,63–1,92 secondo la finestra (massimo 1,92 a 50 sedute, −3,9% da 2); con la media dichiarata 4,9 milioni il rapporto è 1,84: l'arrotondamento nasce nella risposta. Giusti: chiusura del 16 ottobre 34,05 (IBKR e Nasdaq 34,05), che la risposta attribuisce al 16 dopo averla scartata come chiusura dell'evento. Non verificati: media del periodo «circa 4,9 milioni» (finestra più vicina 63 sedute 4.998.117, −1,96%). Escluso: «il più alto da fine luglio» (punto di confronto senza cifre). Seduta: apertura, chiusura (anche ripetuta come chiusura precedente del 16), 31,90, +2,20 $, +6,90%, volumi, estremi. Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-10A-2-claude": "Rialzo del 9 ottobre «del 13%» sbagliato: chiusura su chiusura +15,60% (68,89 → 79,64), −2,60 punti; il titolo della fonte mostrata («Crown Castle Soars 13% as SpaceX’s $8 Billion Spectrum Buy…») indica un articolo scritto durante la seduta del 9, e +13% (77,85) è dentro l'intervallo di quel giorno (73,75–79,79). Giusti: dopo-borsa del 22 ottobre «poco prima delle 20» 86,29 (+9,46%), uguale all'ultimo scambio delle 19:59; in mattinata «più del 12%» e «intorno agli 88 dollari» (09:30–12:00: 85,13–91,45); «circa il 25%» dall'8 ottobre (+24,79%). Non verificati: media «4,2 milioni» (finestra più vicina 90 sedute 4.111.931, +2,14%). Esclusi: titoli delle fonti (9%, 80,000, 178,37, 122,60, 13%), l'orario «20» e «chiusura più alta da giugno» (punto di confronto senza cifre). Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-10A-3-claude": "Rialzo del 9 ottobre «del 13% in un giorno» sbagliato: chiusura su chiusura +15,60% (68,89 → 79,64), −2,60 punti; +13% (77,85) è un livello toccato durante quella seduta (73,75–79,79), cifra da articolo scritto a seduta in corso. Giusti: «nelle prime contrattazioni» oltre il 13% (massimo 09:30–09:45 91,45); alle 11:37 +11,7% a 88,05 (barre 11:30–11:40: 87,30–88,21); «+12%» degli articoli della mattinata (88,29; 09:30–12:00: 85,13–91,45); +25% dall'8 ottobre (+24,79%, arrotondato). Non verificati: media «4,2 milioni» (finestra più vicina 90 sedute 4.111.931, +2,14%). Esclusi: titoli delle fonti (178,37, 122,60) e «chiusura più alta da giugno» (punto di confronto senza cifre). Seduta: 85,97, +7,14 $, 78,83, +9,06%, apertura 91,02, oltre il 15%, estremi 85,00–91,45, circa 17,3 milioni, circa il 9% (già valutati). Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-10C-2-claude": "Rialzo «del 24%» dalla chiusura dell'8 ottobre sbagliato: 68,89 → 85,97 = +24,79%, arrotondato 25; −0,79 punti. +24% (85,42) è un livello toccato il 23 ottobre, ma nessun dato lega la cifra a un'istantanea. Giusti: volumi «più che tripli» rispetto alla media dell'ultimo mese (17.324.090 / media 20 sedute 4.979.778 = 3,48); after-hours di giovedì «fino al 10%» (massimo 87,00 = +10,36%, arrotondato). Non verificati: ipotesi del calo di SpaceX del 9,14% giovedì (nessun dato del kit su SpaceX). Esclusi: titolo della fonte (9%, 80,000), «circa il 9%» riferito a SpaceX (stessa affermazione del 9,14%) e «chiusura più alta da giugno» (punto di confronto senza cifre). Seduta: 85,97, +7,14 $, 9,06% (già valutati). Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-12C-2-chatgpt": "Sbagliato: 15/10 «apertura in ribasso di oltre il 5%»: apertura 46,90, −4,17% (limite falso), contraddetto dalla stessa risposta («circa −4,2%»); oltre il 5% solo più tardi nella seduta (minimo 45,61, −6,81%). Giusti: 15/10 apertura 46,90 (circa −4,2%), minimo 45,61 (circa −6,8%), chiusura 48,76 (−0,37%); 16/10 −4,27%. Esclusa: la cifra della premessa («del 5%») nella frase che la nega. Non verificati: nessuno. Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
 "s2-08C-1-claude": "Corregge la premessa. Ipotesi: calo del 7,56% dopo i conti del primo trimestre (aprile) sbagliato: la seduta di reazione (23/04) chiude a −4,62% (minimo −5,97%); −7,56% è il calo di due sedute, dalla chiusura del 22/04 a quella del 24/04. Non verificati: nessuno. Per scelta: 0 (analisti e mercato 0, dati aziendali 0). Esclusi 8: secondi estremi di intervalli (4), sigle F-35, F-16, C-130 (3), titolo della fonte «EUR 539.30» (1).",
 "s2-12U-1-chatgpt": "Solo prezzi della seduta richiesta, più la variazione dall'apertura alla chiusura: +2,21% e 1,06 USD, esatte (48,94 su 47,88, apertura Nasdaq; andamento durante la seduta). Per scelta: 0 (analisti e mercato 0, dati aziendali 0).",
}
PS = re.compile(r"Per scelta: \d+ \(analisti e mercato \d+, dati aziendali \d+\)")
NV = re.compile(r"Non verificat[ie]: .*?(?=(?: Per scelta:| Esclus| Seduta:| Seduta \(| Campione| In lettere)|$)", re.S)
MARK = "Controllo aggiuntivo del 30 ottobre"
def short(t, n=70):
    t = t.strip().strip("«»\"")
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"
def rebuild(oss, d):
    """Rifà la frase dei non verificati dai numeri finali e aggiunge gli esiti del controllo aggiuntivo, del campione SEC e dei numeri in lettere."""
    nums = d["numeri"]
    nv = [n for n in nums if n["esito"] == "non verificato" and not n.get("campione") and not n.get("in_lettere")]
    extra = [n for n in nums if MARK in (n.get("nota") or "")]
    parts = ["Non verificati: " + ("; ".join("«" + short(n["citazione"]) + "»" for n in nv) if nv else "nessuno") + "."]
    if extra:
        parts.append(MARK + " (prezzi IBKR di altre sedute): " + "; ".join("«" + short(n["citazione"]) + "» " + n["esito"] + ("" if not n.get("in_lettere") else " (in lettere)") for n in extra) + ".")
    s = d.get("campione_sec", {})
    if sum(s.values()):
        tot = sum(s.values())
        parts.append(f"Campione SEC dei dati aziendali: {tot} {'cifra' if tot == 1 else 'cifre'} (giuste {s['giusti']}, sbagliate {s['sbagliati']}, non verificabili {s['non_verificati']}; dettagli in tabella).")
    l = d.get("in_lettere", {})
    if sum(l.values()):
        parts.append(f"In lettere o come parametro, fuori dal tasso: giusti {l['giusti']}, sbagliati {l['sbagliati']}, non verificati {l['non_verificati']}.")
    block = " ".join(parts)
    if NV.search(oss):
        oss = NV.sub(lambda m: block, oss, count=1)
    elif PS.search(oss):
        oss = oss.replace("Per scelta:", block + " Per scelta:", 1)
    else:
        oss = oss.rstrip() + " " + block
    if d["conteggi"]["sbagliati"] == 0 and l.get("sbagliati", 0) > 0:
        oss = re.sub(r"^Sbagliat[oi]:", "Sbagliato, in lettere e quindi fuori dal tasso:", oss) if re.match(r"^Sbagliat[oi]:", oss) else "In lettere, fuori dal tasso: " + oss[0].lower() + oss[1:]
    return re.sub(r"\.\.(?=\s|$)", ".", re.sub(r"\s+", " ", oss)).strip()
changed = []
for k, d in sorted(docs.items()):
    if not d["numeri"]: continue
    i = d["risposta_id"]
    oss = OSS.get(i, d["osservazioni"])
    am = d["per_tipo"].get("analisti e mercato", {}).get("per_scelta", 0)
    da = d["per_tipo"].get("dati aziendali", {}).get("per_scelta", 0)
    ps = f"Per scelta: {am + da} (analisti e mercato {am}, dati aziendali {da})"
    oss = PS.sub(ps, oss) if PS.search(oss) else (oss.rstrip() + " " + ps + ".")
    oss = rebuild(oss, d)
    # le note di riconciliazione restano nel campo «disaccordo», che la pagina mostra a parte (etichetta «Riconciliazione e controlli»)
    new = dict(d, osservazioni=oss, disaccordo=[x.rstrip(".") for x in d["disaccordo"]])
    path = os.path.join(OUT, k + ".json")
    old = json.load(open(path)) if os.path.exists(path) else None
    cmp_old = {kk: vv for kk, vv in (old or {}).items() if kk != "updatedAt"}
    cmp_new = {kk: vv for kk, vv in new.items() if kk != "updatedAt"}
    if old is None or cmp_old != cmp_new:
        new["updatedAt"] = STAMP or (old or {}).get("updatedAt", "")
        changed.append(k)
        if STAMP: json.dump(new, open(path, "w"), ensure_ascii=False)
print("changed", len(changed)); print(changed)
if STAMP: json.dump(changed, open(os.path.join(OUT, "changed.json"), "w"))
