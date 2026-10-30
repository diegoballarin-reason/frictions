"""H1 · risoluzione dei disaccordi fra i due passaggi (scritta il 30 ottobre dopo aver letto entrambi).
Ogni voce: (id, n) → (scelta, motivazione, campi da forzare). Scelta: P, V, X (non è un'affermazione), D (campi dati)."""
A_ = {"gruppo": "A"}
OC = "Variazione dall'apertura alla chiusura della seduta richiesta: non è fra i prezzi della seduta (§7), è andamento durante la seduta; verificata."
FB = "Quotazione di Meta su Euronext Milan in euro (FB2A): altro strumento e altra piazza, dati di mercato non verificati per scelta."
MONTH = "Punto di confronto senza cifre («da giugno», «da fine luglio»): non è un numero e non si aggiunge."
WORDS = "Numero in lettere non estratto in automatico; aggiunto come affermazione del gruppo A (vedi decisione sui numeri in lettere)."
RES = {
 ("s2-02A-1-claude", "x1"): ("V", WORDS, {"aggiunto": "parola"}),
 ("s2-02A-3-claude", "40"): ("P", "Il minimo di luglio è il prezzo di altre sedute; non verificato in entrambi i passaggi."),
 **{("s2-04U-1-gemini", k): ("V", FB) for k in ("2", "5", "6", "9", "10", "13", "14")},
 ("s2-04U-2-chatgpt", "5"): ("P", OC),
 ("s2-05U-2-chatgpt", "4"): ("P", OC),
 ("s2-05U-2-chatgpt", "5"): ("P", OC),
 ("s2-12U-1-chatgpt", "4"): ("V", OC),
 ("s2-12U-1-chatgpt", "5"): ("V", OC),
 ("s2-05U-1-claude", "13"): ("X", "Chiusura di TokenPost riportata dalla risposta solo per scartarla: come proposto per le U, non si conta (in attesa della decisione di Diego).", {"escluso": "altro"}),
 ("s2-06A-3-claude", "3"): ("P", "«Contrattazioni overnight» (20:00–04:00) non sono nei riferimenti: non verificato, come da regole."),
 ("s2-06C-1-claude", "14"): ("P", "Fase di un altro giorno (13/10, mattinata): andamento durante la seduta, non verificato."),
 ("s2-06C-1-claude", "15"): ("P", "Fase di un altro giorno (13/10, mattinata): andamento durante la seduta, non verificato."),
 ("s2-06U-1-gemini", "1"): ("V", "Rilevazione delle 9:30 con l'apertura consolidata data a parte: non conta come apertura (decisione del 27 ottobre), è un punto a un orario; verificata."),
 ("s2-07A-1-claude", "32"): ("P", "«Arrivando a» senza nominare un estremo: livello passato nella seduta di giovedì (regola 12), dentro 112,76–117,25; il 4,1% della stessa frase resta sbagliato."),
 **{(i, "x1"): ("P", "«Nuovo massimo a 52 settimane»: affermazione con una cifra non estratta (parametro); aggiunta, verificata.", {"aggiunto": "parametro"})
    for i in ("s2-07A-2-claude", "s2-07A-3-claude", "s2-07C-1-claude", "s2-07C-2-claude", "s2-07U-1-claude")},
 ("s2-07C-2-claude", "33"): ("V", "«In tre mesi»: controllo completato il 30 ottobre con le chiusure IBKR di luglio (hist/ibkr_extra/has_daily_2026.json). Tre mesi di calendario: dal 17/07 (81,55) al 19/10 +20,77%, dal 20/07 (81,59) al 20/10 +34,23%; a 63 sedute +10,61% / +23,00%. Nessuna lettura sta entro 1,2 punti da «circa il 28%»: sbagliato.",
   {"esito": "sbagliato", "riferimento": "IBKR HAS: 17/07/2026 81,55; 20/07/2026 81,59; 22/07/2026 89,04; 19/10 98,49; 20/10 109,52", "calcolo": "98,49/81,55 − 1 = +20,77%; 109,52/81,59 − 1 = +34,23%; 98,49/89,04 − 1 = +10,61%; 109,52/89,04 − 1 = +23,00%: tutte oltre 1,2 punti da 28", "nota": "letture per mesi di calendario e per sedute, con e senza la seduta dell'evento"}),
 ("s2-05A-2-claude", "9"): ("D", "Non era un disaccordo: controllo completato il 30 ottobre con la chiusura IBKR del 21/10/2025 (42,36, hist/ibkr_extra/cmg_2025.json). Con dodici mesi di calendario la variazione è −33,62%, la cifra della risposta: giusto (vale la lettura che la risposta può aver usato, come per due fonti diverse).",
   {"esito": "giusto", "riferimento": "IBKR CMG: chiusura 21/10/2025 42,36; 21/10/2026 28,12 (a 252 sedute: 20/10/2025 41,63)", "calcolo": "28,12 / 42,36 − 1 = −33,62%: uguale (a 252 sedute −32,45%)", "nota": "dodici mesi di calendario"}),
 ("s2-05A-1-claude", "23"): ("D", "Non era un disaccordo: con la chiusura IBKR del 21/10/2025 (42,36) i dodici mesi di calendario danno −33,62%, dentro «circa il 33,6%»; giusto anche a 252 sedute.",
   {"riferimento": "IBKR CMG: chiusura 21/10/2025 42,36; a 252 sedute 20/10/2025 41,63", "calcolo": "28,12 / 42,36 − 1 = −33,62% (calendario); 28,12 / 41,63 − 1 = −32,45% (252 sedute), entro 1,2 punti", "nota": ""}),
 ("s2-06A-1-claude", "5"): ("D", "Non era un disaccordo: la stessa affermazione in s2-06A-3-claude è «non verificato». Le contrattazioni overnight (20:00–04:00) non sono nei riferimenti; il pre-market è un'altra finestra. Per coerenza: non verificato.",
   {"esito": "non verificato", "nota": "Servirebbero i dati della sessione overnight (domenica 20:00 – lunedì 04:00 New York); letto come pre-market sarebbe giusto (primo scambio delle 4:00 a −1,00%)."}),
 ("s2-08A-1-claude", "x1"): ("V", "«Media mobile a 200 giorni»: aggiunta; non verificata (servono 200 chiusure).", {"aggiunto": "parametro"}),
 ("s2-08C-1-gemini", "2"): ("V", "Seduta del 22 ottobre 2024 citata come precedente: altre sedute, non verificata (dati 2024 non nei riferimenti)."),
 ("s2-09U-2-claude", "x2"): ("X", MONTH, {"escluso": "altro"}),
 ("s2-10A-1-gemini", "x1"): ("V", "Prezzo del dopo-borsa non estratto (testo incollato); verificato.", {"aggiunto": "lettura"}),
 ("s2-10A-1-gemini", "x2"): ("V", WORDS.replace("in lettere", "a una cifra"), {"aggiunto": "parola"}),
 ("s2-10A-2-claude", "x1"): ("X", MONTH, {"escluso": "altro"}),
 ("s2-10A-3-claude", "x1"): ("X", MONTH, {"escluso": "altro"}),
 ("s2-10C-2-claude", "x2"): ("X", MONTH, {"escluso": "altro"}),
 ("s2-10C-2-claude", "7"): ("V", "La cifra della premessa riferita a SpaceX è la stessa affermazione del −9,14% che segue: ripetizione."),
 **{(i, "x1"): ("P", WORDS, {"aggiunto": "parola"}) for i in ("s2-11A-1-chatgpt", "s2-11A-2-chatgpt", "s2-11A-3-chatgpt")},
 ("s2-11C-1-claude", "x1"): ("V", "Conteggio di sedute consecutive: altre sedute.", {"aggiunto": "parola"}),
 ("s2-12A-2-chatgpt", "x1"): ("P", WORDS + " Fuori dal tasso del gruppo A per la decisione del 30 ottobre; con la tolleranza dell'1% sui rapporti sarebbe sbagliato, con l'arrotondamento giusto.", {"aggiunto": "parola", "convenzione": "multiplo"}),
 ("s2-12A-3-chatgpt", "x1"): ("P", WORDS + " Fuori dal tasso del gruppo A per la decisione del 30 ottobre; con la tolleranza dell'1% sui rapporti sarebbe sbagliato, con l'arrotondamento giusto.", {"aggiunto": "parola", "convenzione": "multiplo"}),
 ("s2-12A-2-claude", "21"): ("P", "Livello rispetto a un minimo di settembre: altre sedute; non verificato in entrambi i passaggi."),
 ("s2-12A-2-claude", "22"): ("P", "Minimo di settembre: altre sedute; non verificato in entrambi i passaggi."),
 ("s2-12C-2-chatgpt", "x1"): ("X", "Cifra della premessa in una frase che la nega: l'estrattore del pilota la esclude per costruzione; non si aggiunge. La stessa affermazione è contata nella riga successiva (apertura del 15/10).", {"escluso": "domanda"}),
}

VERSO30 = "Decisione di Diego del 30 ottobre: «verso / intorno alle HH» è un orario approssimato, finestra di ±30 minuti."
RES.update({
 ("s2-02A-1-claude", "18"): ("D", VERSO30, {"riferimento": "bars5 LRCX 2026-10-22 10:30–11:30: min 232,87, max 238,14 → −10,71%…−8,69% vs 260,81", "calcolo": "circa 9% → −7,8%…−10,2%: si sovrappone alla finestra → giusto"}),
 ("s2-02A-1-claude", "19"): ("D", VERSO30, {"esito": "giusto", "riferimento": "bars5 LRCX 2026-10-22 10:30–11:30: min 232,87, max 238,14", "calcolo": "232,87 ≤ 237,46 ≤ 238,14 → livello nella finestra (scambiato fra le 10:30 e le 10:40)"}),
 ("s2-06A-3-claude", "5"): ("D", VERSO30, {"riferimento": "bars5 MU 2026-10-12 10:25–11:25: min 979,00, max 989,10 → −4,86%…−3,88% vs 1.029,00", "calcolo": "−4,2% (con «circa») dentro l’intervallo → giusto"}),
 ("s2-06A-3-claude", "6"): ("D", VERSO30, {"riferimento": "bars5 MU 2026-10-12 10:25–11:25: min 979,00, max 989,10", "calcolo": "985,93 dentro 979,00–989,10 → livello nella finestra"}),
 ("s2-07A-3-claude", "13"): ("D", VERSO30, {"riferimento": "bars5 HAS 2026-10-20 14:30–15:30: min 108,60, max 109,41 → +10,27%…+11,09% vs 98,49", "calcolo": "+10,66% → 108,99, dentro la finestra → giusto"}),
 ("s2-09A-1-claude", "7"): ("D", VERSO30 + " «Fino a» resta un estremo (regola 12): sbagliato anche con la finestra più ampia.", {"riferimento": "bars5 IP 2026-10-15 13:00–14:00: min 34,21, max 34,52 → +7,24%…+8,21% vs 31,90", "calcolo": "«fino a» = estremo della finestra: +8,21%; 7,4 − 8,21 = −0,81 punti (oltre 0,14)"}),
 ("s2-11A-1-claude", "8"): ("D", VERSO30, {"riferimento": "bars5 DDOG 2026-10-19 11:30–12:30: min 262,87, max 266,00 → +6,38%…+7,64% vs 247,11", "calcolo": "247,11 × 1,0732 = 265,20 → dentro la finestra"}),
 ("s2-11A-2-claude", "7"): ("D", VERSO30, {"esito": "giusto", "riferimento": "bars5 DDOG 2026-10-19 09:30–10:30: min 256,14, max 264,71 → +3,65%…+7,12% vs 247,11", "calcolo": "247,11 × 1,061 = 262,18 → dentro la finestra"}),
 ("s2-11A-2-claude", "8"): ("D", VERSO30, {"esito": "giusto", "riferimento": "bars5 DDOG 2026-10-19 09:30–10:30: min 256,14, max 264,71", "calcolo": "256,14 ≤ 262,21 ≤ 264,71 → livello nella finestra"}),
})
RES[("s2-05U-1-claude", "13")] = ("X", "Chiusura di TokenPost riportata dalla risposta solo per scartarla: non si conta (decisione di Diego del 30 ottobre per le U).", {"escluso": "altro"})

# ── Controllo aggiuntivo del 30 ottobre: 48 affermazioni del gruppo A non verificate per mancanza di dati (extra/kit/README_extra.md),
#    due passaggi indipendenti con dati IBKR (extra/out_P, extra/out_V). Riconciliazione di Claude: si applicano le regole scritte
#    (variazione di una seduta da chiusura a chiusura e movimenti di più sedute da chiusura a chiusura, salvo indicazione della risposta);
#    la lettura sull'estremo intraday che il README ammetteva per i cali dopo una notizia non è fra le letture confermate da Diego.
import json as _j, os as _o
_E = _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "extra")
_K = {c["cid"]: c for c in _j.load(open(_o.path.join(_E, "kit", "claims.json")))}
CA = "Controllo aggiuntivo del 30 ottobre (prezzi IBKR, due passaggi indipendenti"
_OVR = {
 "E01": ("giusto", "I passaggi divergevano (P sbagliato, V giusto). Regola decisa da Diego il 30 ottobre (16:20): un'escursione dentro un periodo senza estremi fissati dalla frase («salito di oltre il 40% tra marzo e giugno») si misura dal minimo al massimo, con le chiusure o con gli estremi della seduta, come per minimi e massimi storici. Dal minimo in seduta di marzo (102,01) al massimo in seduta di giugno (147,96) +45,04%: il limite «oltre il 40%» è vero. Sulle sole chiusure +38,08%."),
 "E03": ("giusto", "Come E01 (stessa frase): escursione fra marzo e giugno, dal minimo al massimo in seduta +45,04%; giusto per la regola sulle escursioni decisa da Diego il 30 ottobre."),
 "E40": ("sbagliato", "Entrambi i passaggi davano giusto leggendo il calo sul minimo intraday (−4,74%). La variazione di una seduta si misura da chiusura a chiusura, salvo indicazione della risposta: il 6/7 −1,92% (260,36 → 255,37). La cifra coincide con il calo delle prime contrattazioni (circa −4,6% a 248,30): istantanea presentata come calo della seduta."),
 "E43": ("sbagliato", "Come E40: «perse circa il 4,6%» in quell'occasione, senza indicare la fase; da chiusura a chiusura −1,92%. È il calo delle prime contrattazioni (istantanea)."),
 "E41": ("sbagliato", "Da chiusura a chiusura −1,92%; anche sul minimo intraday (−4,74%) lo scarto supera 0,14 punti. Istantanea delle prime contrattazioni presentata come calo della seduta."),
}
_EXTRA_NOTE = {
 "E18": " Lettura confermata in riconciliazione: la frase colloca la media al superamento («aveva già portato il titolo sopra la media»); è la regola delle due letture.",
 "E36": " In riconciliazione: basta AT&T (−7,96%, entro 1,2 punti); T-Mobile resta fuori di 0,09 punti in chiusura. Le cifre della tabella della risposta sono esatte.",
}
for _cid, _c in _K.items():
    _p = _j.load(open(_o.path.join(_E, "out_P", _cid + ".json"))); _v = _j.load(open(_o.path.join(_E, "out_V", _cid + ".json")))
    if _cid in _OVR:
        _es, _mot = _OVR[_cid]
        _mot = CA + "): " + _mot
    else:
        assert _p["esito"] == _v["esito"], _cid
        _es = _p["esito"]; _mot = CA + ", concordi)."
    RES[(_c["answer_id"], str(_c["n"]))] = ("D", _mot + _EXTRA_NOTE.get(_cid, ""),
        {"esito": _es, "riferimento": _p["riferimento"],
         "calcolo": (_OVR[_cid][1] if _cid in _OVR else _p["calcolo"]),
         "nota": ((("Calcolo dei passaggi: " + _p["calcolo"] + " ") if _cid in _OVR else "") + (_p.get("nota") or "") + (" Secondo passaggio: " + _v["calcolo"] if _p["esito"] != _v["esito"] else "")).strip()})

# origine proposta per le risposte che hanno numeri sbagliati solo dopo il controllo aggiuntivo (o in cui prevalgono)
ORIGINE = {
 "s2-08C-1-claude": "momento sbagliato",      # −7,56% = due sedute (23–24/04) presentate come reazione ai conti
 "s2-08C-2-claude": "non rintracciabile",     # −5,5% contro −6,12%
 "s2-09A-2-claude": "istantanea fuori tempo", # 2.580 pence = barra di Londra delle 16:00–16:15, non la chiusura (2.600)
 "s2-09A-3-claude": "istantanea fuori tempo",
 "s2-11C-1-gemini": "istantanea fuori tempo", # tre cifre del 6/7 sono il calo delle prime contrattazioni; restano due errori di settimana (momento sbagliato)
}
