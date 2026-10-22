#!/usr/bin/env python3
"""
tells_lint v2 — estrattore di spie per la revisione di consegna.

Non corregge e non decide: ESTRAE ogni occorrenza dei pattern che più spesso
risultano non calibrati, e per ciascuno stampa la glossa con cui giudicarlo.
La decisione resta di chi rilegge.

Severità:
  [!]  errore probabile — quasi sempre da correggere
  [?]  da verificare    — legittimo in casi precisi, indicati nella glossa
  [~]  densità          — corretto singolarmente, sospetto come distribuzione

Uso:
    python3 tells_lint.py FILE.md [ALTRO.md ...] [--lang=it|en]

La lingua si deduce dal nome (`.it.md` / `.en.md`) o dal separatore `# Attriti`
nei file bilingui; `--lang=` la forza.

Protocollo: articles/07-punctuation-tells.{en,it}.md
Licenza: MIT, vedi LICENSE in questa cartella.
"""

import re
import sys

# ─────────────────────────────────────────────────────────────────────────────
#  (categoria, etichetta, regex, glossa, severità)
# ─────────────────────────────────────────────────────────────────────────────

CHECKS = {
    "it": [
        # ── punteggiatura ────────────────────────────────────────────────────
        ("connettivo", "virgola + e / ed", r",\s+ed?\s",
         "Legittima solo se: cambia il soggetto tra le proposizioni; la virgola "
         "chiude un inciso aperto prima; la 'e' vale 'eppure'/'e dunque'; chiude "
         "una serie enumerativa lunga; è pausa ritmica voluta. Test: che cosa "
         "separa? Se niente, è un tic.", "?"),
        ("connettivo", "virgola + o / od", r",\s+od?\s",
         "Stesse condizioni della 'e'. Scorretta tra alternative omogenee "
         "coordinate strettamente.", "?"),
        ("duepunti", "due punti", r":\s",
         "Reggono elenco, spiegazione, citazione, conseguenza. NON si frappongono "
         "tra verbo e completiva ('dimostra che: X'). Contare anche la densità.", "?"),
        ("densita", "trattino lungo", r"—",
         "Raramente scorretto. Soglia di lavoro: 6-7 ogni 1.000 parole.", "~"),
        ("trattino", "trattino breve tra spazi", r"(?<=\S)\s-\s",
         "Trattino breve al posto della lineetta: va sostituito con —. "
         "Legittimo solo come segno meno.", "?"),
        ("puntovirgola", "punto e virgola", r";\s",
         "Corretto tra proposizioni autonome ma collegate. Sospetto se ripetuto "
         "in serie ravvicinate.", "~"),
        # ── grammatica ───────────────────────────────────────────────────────
        ("splice", "virgola splice",
         r",\s+(questo|questa|ciò|esso|essa|lui|lei|loro)\s+(è|sono|era|erano|ha|hanno)\b",
         "Due proposizioni indipendenti unite dalla sola virgola: serve punto, "
         "punto e virgola o congiunzione. Falso positivo frequente: subordinata "
         "anteposta, inciso, apposizione.", "?"),
        ("congiuntivo", "contesto che regge il congiuntivo",
         r"\b(credo|penso|ritengo|sembra|pare|suppongo|immagino|temo|dubito|spero)\s+che\b"
         r"|\b(sebbene|benché|nonostante|affinché|qualora|purché|malgrado|prima\s+che)\b",
         "Ispezionare il verbo che segue: questi contesti reggono il congiuntivo. "
         "'Credo che è' -> 'credo che sia'.", "?"),
        ("consecutio", "se + condizionale",
         r"\bse\s+\w*\s*(avrei|sarei|farei|potrei|vorrei|dovrei|andrei|direi)\b",
         "Errore netto: nella protasi va il congiuntivo, non il condizionale. "
         "'Se avrei' -> 'se avessi'.", "!"),
        ("ortografia", "accenti e apostrofi frequenti",
         r"\b(?:perch|poich|affinch|bench|purch|finch|sicch|nonch)(?:è|e['’])"
         r"|\bqual['’]\s?[eè]\b|\bun\s+po\b(?!['’])|\bpò\b",
         "Forme scorrette: perchè/poichè/affinchè/benchè (accento grave o "
         "apostrofo) -> perché, poiché, affinché, benché; qual'è -> qual è; "
         "un po / pò -> un po'.", "!"),
        ("ripetizione", "che ... che ravvicinati", r"\bche\b[^.!?]{0,45}\bche\b",
         "Due 'che' nella stessa frase breve: quasi sempre riscrivibile.", "~"),
    ],

    "en": [
        # ── punteggiatura ────────────────────────────────────────────────────
        ("connettivo", "comma + and / or / but", r",\s+(and|or|but)\s",
         "NON diagnostico in inglese: richiesto tra due proposizioni indipendenti, "
         "standard come seriale prima dell'ultimo elemento (Chicago/MLA). "
         "Scorretto solo col predicato composto a soggetto unico: "
         "'was taken at noon, and analyzed later'.", "?"),
        ("duepunti", "colon", r":\s",
         "Deve essere preceduto da una proposizione sintatticamente completa. "
         "'The three families are: X, Y, Z' lascia 'are' sospeso.", "?"),
        ("densita", "em dash", r"—",
         "Raramente scorretto. Soglia di lavoro: 6-7 ogni 1.000 parole.", "~"),
        ("trattino", "hyphen between spaces", r"(?<=\S)\s-\s",
         "Trattino breve al posto della lineetta: va sostituito con —. "
         "Legittimo solo come segno meno.", "?"),
        ("puntovirgola", "semicolon", r";\s",
         "Corretto tra proposizioni indipendenti collegate. Sospetto in serie.", "~"),
        ("splice", "comma splice",
         r",\s+(it|this|that|they|we|you|he|she|there)\s+(is|are|was|were|has|have|can|will|does|do)\b",
         "Due indipendenti unite dalla sola virgola: serve punto, semicolon o "
         "congiunzione. Falso positivo frequente: subordinata o avverbiale anteposta "
         "('Where X holds, it is cited'), relativa, inciso.", "?"),
        # ── marcatori lessicali della generazione ────────────────────────────
        ("marcatore", "connettivo formale in apertura",
         r"(?m)^(Moreover|Furthermore|Additionally|Notably|Importantly|Ultimately"
         r"|In conclusion|In summary|Overall|That said|Indeed)\b",
         "Aprire il paragrafo con questi è il tic più riconoscibile. Quasi sempre "
         "si elimina senza perdita.", "~"),
        ("marcatore", "costruzione antitetica",
         r"\b(is|are|was|were|isn't|aren't)\s+not\s+(just|only|merely|simply)\b"
         r"|\bit'?s\s+not\s+\w+[,—]\s*it'?s\b",
         "'It's not X, it's Y' e 'not just X but Y': efficaci una volta, marcatori "
         "se ripetute.", "~"),
        ("marcatore", "lessico da modello",
         r"\b(delve|tapestry|realm|testament|underscore[sd]?|leverage|robust|crucial"
         r"|pivotal|seamless|vibrant|landscape of|navigate the|stands? as|serves? as"
         r"|it'?s worth noting)\b",
         "Lessico ad altissima frequenza nei testi generati. Non scorretto: "
         "sostituibile con una parola più concreta.", "~"),
        ("marcatore", "not only ... but also", r"(?<!do )(?<!does )(?<!did )(?<!can )(?<!could )\bnot only\b",
         "Costruzione corretta ma sovrarappresentata. Verificare che il 'but also' "
         "ci sia e che la simmetria regga.", "?"),
        # ── falsi amici e calchi dall'italiano ───────────────────────────────
        ("falsoamico", "falso amico IT->EN",
         r"\b(actually|eventually|argument|sensible|comprehensive|confront|attend"
         r"|delusion|casually|pretend|morbid|individuate|assist to)\b",
         "Verificare il senso voluto: actually!=attualmente(currently); "
         "eventually!=eventualmente(possibly); argument!=argomento(topic); "
         "sensible!=sensibile(sensitive); comprehensive!=comprensivo(understanding); "
         "confront!=confrontare(compare); attend!=attendere(wait); "
         "delusion!=delusione(disappointment); casually!=casualmente(by chance); "
         "pretend!=pretendere(demand); morbid!=morbido(soft).", "?"),
        ("calco", "'in fact' confermativo", r"\bin fact\b",
         "In inglese 'in fact' corregge o contrasta, non conferma come l'italiano "
         "'infatti'. Se serve conferma: 'indeed' o niente.", "?"),
        ("calco", "'also' a inizio frase", r"(?m)^Also[,\s]",
         "Calco di 'inoltre'. In inglese 'also' sta di norma dentro la frase.", "?"),
        ("calco", "preposizione sospetta",
         r"\b(depend of|different (than|to)|interested to|possibility to"
         r"|in the moment|control (if|whether))\b",
         "Reggenze calcate dall'italiano: depend ON, different FROM, interested IN, "
         "possibility OF, at the moment, check (non control).", "!"),
        ("calco", "plurale di non numerabile",
         r"\b(informations|advices|researches|feedbacks|evidences|softwares|knowledges)\b",
         "Non numerabili in inglese: information, advice, research, feedback, "
         "evidence, software, knowledge.", "!"),
    ],
}

SKIP = re.compile(r"^\s*(#|\||```|→|\[|©|<|\*Attriti|\*Frictions|\*\*Fenomeno|\*\*Phenomenon)")
SEV_ORDER = {"!": 0, "?": 1, "~": 2}


def detect_lang(path, text, forced=None):
    if forced:
        return [(forced, text)]
    if ".it." in path:
        return [("it", text)]
    if ".en." in path:
        return [("en", text)]
    i = text.find("\n# Attriti")
    if i != -1:
        return [("en", text[:i]), ("it", text[i:])]
    return [("it", text), ("en", text)]


def scan(path, forced=None):
    text = open(path, encoding="utf-8").read()
    print(f"\n{'=' * 74}\n  {path}   ({len(text.split())} parole)\n{'=' * 74}")

    for lang, chunk in detect_lang(path, text, forced):
        words = max(1, len(chunk.split()))
        lines = [l for l in chunk.split("\n") if l.strip() and not SKIP.match(l)]
        print(f"\n---- LINGUA: {lang.upper()} ({words} parole) " + "-" * 40)
        total = 0
        for _, label, rx, gloss, sev in sorted(CHECKS[lang], key=lambda c: SEV_ORDER[c[4]]):
            hits = []
            for line in lines:
                for m in re.finditer(rx, line):
                    a, b = max(0, m.start() - 50), min(len(line), m.end() + 40)
                    hits.append(f"…{line[a:b]}…")
            if not hits:
                continue
            total += len(hits)
            dens = f"   [{len(hits) / words * 1000:.1f} ogni 1000]" if sev == "~" else ""
            print(f"\n  [{sev}] {label} — {len(hits)}{dens}")
            print(f"      > {gloss}")
            for h in hits[:12]:
                print(f"      · {h}")
            if len(hits) > 12:
                print(f"      · … e altre {len(hits) - 12}")
        print(f"\n  == occorrenze da giudicare: {total}")
    print()


if __name__ == "__main__":
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    forced = next((a.split("=", 1)[1].strip().lower()
                   for a in sys.argv[1:] if a.startswith("--lang=")), None) or None
    if forced and forced not in CHECKS:
        sys.exit(f"Lingua non riconosciuta: '{forced}'. Valori ammessi: "
                 f"{', '.join(CHECKS)}.")
    if not files:
        print(__doc__)
        sys.exit(1)
    unreadable = 0
    for p in files:
        try:
            scan(p, forced)
        except OSError:
            print(f"Impossibile aprire il file: {p}", file=sys.stderr)
            unreadable += 1
    sys.exit(1 if unreadable else 0)
