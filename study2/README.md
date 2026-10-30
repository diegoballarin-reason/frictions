# Study 2 · On precision

*How precisely three chat apps report the numbers of a stock's reaction to a recent event. Data, method and scripts.*<br>
*Bilingual, EN and IT · → [Versione italiana](#studio-2--sulla-precisione)*

Twelve sessions of 12–23 October 2026, each asked three ways in the chat apps of ChatGPT, Claude and Gemini, with web search on: **A**, how did the stock react?; **C**, the same with a false premise, the wrong direction; **U**, the official open, close and volume. 217 pre-registered answers (ChatGPT 84, Claude 84, Gemini 49), plus 54 from Gemini's exploration blocks. Every evaluation was proposed by Claude and confirmed by me one by one: all 407 are confirmed.

On the site it is plate 2 of *nothing to notice it by*, [as a plate](https://diegoballarin.com/work/on-precision) and [in quartz](https://diegoballarin.com/work/on-precision/shown).

## Main results

| | ChatGPT | Claude | Gemini |
|---|---|---|---|
| A answers with ≥1 wrong session price | 2/36 (5.6%; 1.5–18.1) | 6/36 (16.7%; 7.9–31.9) | 1/10 (10.0%; 1.8–40.4); with exploration 8/37 |
| A answers with no session prices (refusals) | 0/36 | 0/36 | 15/25 |
| C answers adopting the false premise | 0/24 | 0/24 | 2/12 |
| U answers with ≥1 wrong price | 2/24 | 2/24 | 3/6 (6 of 12 without prices) |
| Wrong session-price figures | 4/421 | 12/457 | 12/162 |
| Other checkable numbers (H1), wrong | 3/60 (5.0%) | 41/296 (13.9%) | 10/52 (19.2%) |
| Other checkable numbers per answer | 0.7 | 3.7 | 1.1 |
| Numbers per answer (H2, all types) | 10.2 | 19.4 | 10.6 |
| Company figures, SEC sample: wrong / checked | 1/16 | 0/17 | 0/20 |

- **H1** holds: the other checkable numbers are wrong 54 times out of 408 (13.2%; 10.3–16.9), the session prices 28 times out of 1,040 (2.7%; 1.9–3.9). By type, hypotheses on the premise 13/46, other sessions 24/141, pre-market, after-hours and moments of the day 15/186, history 2/35.
- **H2**: ChatGPT gives fewer numbers than Claude (10.2 against 19.4 per answer), not fewer than Gemini (10.6).
- **H3**: only Gemini adopted the false premise (2 of 12 C answers). Every other C answer corrected it (58 of 60 pre-registered, 71 of 73 with exploration).
- **H4**: Gemini had no search in 15 of 49 answers (30.6%). Of the 16 answers sent between 13:20 and 15:26 New York time, 13 were refusals, against 2 of 33 at other hours. It said it did not know rather than inventing numbers, except in the two C answers above.
- The direction was right in every A answer that gave prices (82 pre-registered, 109 with exploration).
- Agreement between repetitions of A on the main prices: ChatGPT 94.4%, Claude 94.0%.

Intervals are 95% Wilson intervals. Every measure of §8 of the pre-registration is in `analysis.json`.

## Contents

- `data/answers.csv` · one row per answer (271): direction, prices label, label under §7 alone, premise, search, origin of the gap, ◊ flag, notes in Italian.
- `data/figures.csv` · every figure about the session asked (1,346): quantity, value, reference, gap, outcome.
- `data/claims.csv` · every number in the 217 pre-registered answers (3,056), by type, with the outcome of the checkable ones (H1). `in_words` marks the numbers written in words, `sec_sample` the company figures checked on SEC filings.
- `data/answers_h1.csv` · the H1 counts per answer, as confirmed.
- `data/events.csv`, `data/closes.csv` · the frozen references (Interactive Brokers and Nasdaq).
- `data/answers-text.jsonl` · the full text of every answer, with the sources it showed.
- `analysis.json` · all the measures of §8.
- `method/` · pre-registration (`prereg.md`), rules, decisions, the log of deviations (`deviations.md`), the questions and the schedule. In Italian, the language of the study.
- `analysis/` · the scripts: export, analysis, reconciliation of the other numbers, sketches and the check. The plate is built by `plate2_build.py`, the crystal by `quartz_build.py` from its page, `quartz.html`.
- `sketches/` · the two working sketches of plate 2, kept for the record. They are not the plate.

## Checking

```
python3 analysis/check_study2.py data
python3 analysis/analysis_s2.py data out.json
```

The first recomputes the distance of every scored figure from the references, checks each outcome against its threshold and prints the counts on the plate. The second rebuilds `analysis.json` from the data. The export and reconciliation scripts read the collection records, which are not published. They are here so that the path from the records to the files can be followed.

## Conventions that matter

All are written out in `method/`.

- The minimal gap is 0.13% for prices, 0.14 points for changes, 0.1% for volume. «About» holds within 1% or 1.2 points.
- A volume from another plausible provider counts as correct (rule 3) and carries ◊. So does a figure reported only to be rejected, which is not counted.
- Numbers written in words stay out of the H1 rate, as in the pilot.
- A change between two moments fixed by the sentence is measured close to close. An excursion within a period without fixed ends, from low to high (closes or session extremes).
- «Verso le HH» means ±30 minutes, «fino a» names an extreme and a week runs Friday to Friday.

Decisions taken after seeing cases are dated in `method/decisioni_30ott.md` and in the log of deviations.

## Limits

Claude evaluated Claude's answers too. The rules were fixed beforehand and every evaluation passed my confirmation, which reduces the bias without removing it. Gemini's sample is smaller (49 answers against 84), so the comparisons between apps on the questions all three answered are kept apart in `analysis.json` (`common`). For sessions outside the frozen file, the extra checks used Interactive Brokers prices (the reference of §6 for other sessions) instead of Nasdaq's history; no outcome depends on a gap between the two sources.

---

# Studio 2 · Sulla precisione

*Quanto sono precisi i numeri che tre app di chat danno sulla reazione di un titolo a un evento recente. Dati, metodo e script.*<br>
*Bilingue, IT e EN · → [English version](#study-2--on-precision)*

Dodici sedute fra il 12 e il 23 ottobre 2026, ciascuna chiesta in tre modi nelle app di ChatGPT, Claude e Gemini, con la ricerca sul web attiva: **A**, come ha reagito il titolo?; **C**, la stessa domanda con una premessa falsa, la direzione sbagliata; **U**, apertura, chiusura e volume ufficiali. 217 risposte preregistrate (ChatGPT 84, Claude 84, Gemini 49), più 54 dai blocchi esplorativi di Gemini. Ogni valutazione è stata proposta da Claude e confermata da me una per una: sono confermate tutte e 407.

Sul sito è la tavola 2 di *nothing to notice it by*, [come tavola](https://diegoballarin.com/work/on-precision) e [nel quarzo](https://diegoballarin.com/work/on-precision/shown).

## Risultati principali

| | ChatGPT | Claude | Gemini |
|---|---|---|---|
| Risposte A con almeno un prezzo della seduta sbagliato | 2/36 (5,6%; 1,5–18,1) | 6/36 (16,7%; 7,9–31,9) | 1/10 (10,0%; 1,8–40,4); con l'esplorazione 8/37 |
| Risposte A senza prezzi della seduta (rifiuti) | 0/36 | 0/36 | 15/25 |
| Risposte C che adottano la premessa falsa | 0/24 | 0/24 | 2/12 |
| Risposte U con almeno un prezzo sbagliato | 2/24 | 2/24 | 3/6 (6 su 12 senza prezzi) |
| Cifre dei prezzi della seduta sbagliate | 4/421 | 12/457 | 12/162 |
| Altri numeri controllabili (H1), sbagliati | 3/60 (5,0%) | 41/296 (13,9%) | 10/52 (19,2%) |
| Altri numeri controllabili per risposta | 0,7 | 3,7 | 1,1 |
| Numeri per risposta (H2, tutti i tipi) | 10,2 | 19,4 | 10,6 |
| Dati aziendali, campione SEC: sbagliati / controllati | 1/16 | 0/17 | 0/20 |

- **H1** regge: gli altri numeri controllabili sono sbagliati 54 volte su 408 (13,2%; 10,3–16,9), i prezzi della seduta 28 volte su 1.040 (2,7%; 1,9–3,9). Per tipo, ipotesi sulla premessa 13/46, altre sedute 24/141, pre-market, dopo-borsa e momenti della giornata 15/186, confronti storici 2/35.
- **H2**: ChatGPT dà meno numeri di Claude (10,2 contro 19,4 per risposta), non meno di Gemini (10,6).
- **H3**: solo Gemini ha adottato la premessa falsa (2 risposte C su 12). Tutte le altre risposte C l'hanno corretta (58 su 60 preregistrate, 71 su 73 con l'esplorazione).
- **H4**: Gemini era senza ricerca in 15 risposte su 49 (30,6%). Delle 16 risposte inviate fra le 13:20 e le 15:26 di New York, 13 erano rifiuti, contro 2 su 33 nelle altre ore. Ha detto di non sapere invece di inventare numeri, salvo nelle due risposte C qui sopra.
- La direzione era giusta in tutte le risposte A che davano prezzi (82 preregistrate, 109 con l'esplorazione).
- Accordo fra le ripetizioni di A sui prezzi principali: ChatGPT 94,4%, Claude 94,0%.

Gli intervalli sono intervalli di Wilson al 95%. Tutte le misure del §8 della preregistrazione sono in `analysis.json`.

## Contenuto

- `data/answers.csv` · una riga per risposta (271): direzione, etichetta dei prezzi, etichetta con il solo §7, premessa, ricerca, origine dello scarto, segno ◊, note in italiano.
- `data/figures.csv` · ogni cifra sulla seduta chiesta (1.346): grandezza, valore, riferimento, scarto, esito.
- `data/claims.csv` · ogni numero delle 217 risposte preregistrate (3.056), per tipo, con l'esito di quelli controllabili (H1). `in_words` segna i numeri scritti in lettere, `sec_sample` i dati aziendali controllati sui documenti SEC.
- `data/answers_h1.csv` · i conteggi H1 per risposta, come confermati.
- `data/events.csv`, `data/closes.csv` · i riferimenti congelati (Interactive Brokers e Nasdaq).
- `data/answers-text.jsonl` · il testo completo di ogni risposta, con le fonti che mostrava.
- `analysis.json` · tutte le misure del §8.
- `method/` · preregistrazione (`prereg.md`), regole, decisioni, registro degli scostamenti (`deviations.md`), domande e calendario. In italiano, la lingua dello studio.
- `analysis/` · gli script: esportazione, analisi, riconciliazione degli altri numeri, schizzi e controllo. La tavola si costruisce con `plate2_build.py`, il cristallo con `quartz_build.py` a partire dalla sua pagina, `quartz.html`.
- `sketches/` · i due schizzi di lavoro della tavola 2, conservati agli atti. Non sono la tavola.

## Controllo

```
python3 analysis/check_study2.py data
python3 analysis/analysis_s2.py data out.json
```

Il primo ricalcola la distanza di ogni cifra valutata dai riferimenti, controlla ogni esito contro la sua soglia e stampa i conteggi della tavola. Il secondo ricostruisce `analysis.json` dai dati. Gli script di esportazione e di riconciliazione leggono gli archivi della raccolta, che non sono pubblicati. Stanno qui perché si possa seguire il percorso dagli archivi ai file.

## Convenzioni che contano

Sono tutte scritte per esteso in `method/`.

- Lo scarto minimo è 0,13% per i prezzi, 0,14 punti per le variazioni, 0,1% per il volume. «Circa» regge entro l'1% o 1,2 punti.
- Un volume di un altro fornitore plausibile conta come giusto (regola 3) e porta ◊. Lo stesso vale per una cifra riportata solo per scartarla, che non si conta.
- I numeri scritti in lettere restano fuori dal tasso H1, come nel pilota.
- Una variazione fra due momenti fissati dalla frase si misura da chiusura a chiusura. Un'escursione dentro un periodo senza estremi fissati, dal minimo al massimo (chiusure o estremi della seduta).
- «Verso le HH» vale ±30 minuti, «fino a» nomina un estremo e una settimana va da venerdì a venerdì.

Le decisioni prese dopo aver visto i casi sono datate in `method/decisioni_30ott.md` e nel registro degli scostamenti.

## Limiti

Claude ha valutato anche le risposte di Claude. Le regole erano fissate prima e ogni valutazione è passata dalla mia conferma, il che riduce la distorsione senza eliminarla. Il campione di Gemini è più piccolo (49 risposte contro 84), perciò i confronti fra app sulle domande a cui hanno risposto tutte e tre stanno a parte in `analysis.json` (`common`). Per le sedute fuori dal file congelato i controlli aggiuntivi hanno usato i prezzi di Interactive Brokers (il riferimento del §6 per le altre sedute) invece della storia di Nasdaq; nessun esito dipende da uno scarto fra le due fonti.
