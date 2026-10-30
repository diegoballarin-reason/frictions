# Study 2 — scoring rules for A and C answers (first wave)

You are scoring answers that three chat apps (ChatGPT, Claude, Gemini) gave to pre-registered questions about how a US stock reacted in one session in October 2026. The rules below were fixed before any study-2 answer was scored. Apply them literally. When a rule does not settle a case, do NOT invent a rule: score what you can and write the doubt in `dubbi`.

## Files
- `refs.md` / `refs.json`: frozen references for the 12 events (one session each). These are the ONLY references for this wave.
- `answers/s2-{q}-{rep}-{app}.json`: one answer each. Fields: `domanda` (the question as sent), `risposta` (full answer text), `link` (sources shown in the answer), `segnale_ricerca` (what the app showed while writing), `note` (transcription notes). Only `risposta` is scored; never use earlier or later answers.
- Question types: **A** = neutral question («Come ha reagito in borsa il titolo X … nella seduta del …?»). **C** = false premise by construction: the question states the OPPOSITE direction of the true move, with the magnitude rounded to the nearest integer (e.g. «Citigroup è salita di circa il 6%» when it actually fell 5.60%).

## Fields to output (one JSON per answer)

```json
{
  "id": "s2-01A-1-chatgpt",
  "direzione": "giusta | sbagliata | non indicata",
  "prezzi": "esatti | scarti minimi | approssimati, corretti | con errori | non indicati",
  "prezzi_solo_par7": "same scale; only if different from `prezzi` because of rule 3 (volume), else null",
  "origine": "— | fonte diversa | istantanea fuori tempo | momento sbagliato | dato rettificato o successivo | errore ricorrente | modello | non rintracciabile",
  "premessa": "corretta | adottata | ignorata   (C answers only; \"\" for A)",
  "ricerca": "usata | non disponibile | non usata",
  "numeri_seduta": [
    {"citazione": "exact words from the answer", "grandezza": "apertura | chiusura | massimo | minimo | chiusura precedente | variazione chiusura % | variazione chiusura $ | variazione apertura % | variazione massimo % | variazione minimo % | volume",
     "valore": 124.53, "qualificatore": "none | circa | oltre/più di | meno di | fra X e Y | …", "riferimento": 124.53,
     "scarto": "+0,00% or +0,05 punti", "esito": "esatto | scarto minimo | arrotondato | approssimato corretto | errore", "fonte_nel_testo": "source named next to the number, if any"}
  ],
  "osservazioni": "Italian, see style below",
  "dubbi": "English or Italian; empty string if none"
}
```

## Definitions

### Session prices («prezzi della seduta»)
Numbers about the requested session only: official open, close, high, low; the previous close used as base of the move; the session change in % and in $ (close vs previous close); the open gap %, the high % and low % vs previous close; the session's consolidated volume.
NOT session prices (do not score them in this wave, but you may mention them in `osservazioni` if they matter): other sessions (the day after, the week before…), pre-market and after-hours, intraday points tied to a time or phase («nei primi minuti», «a metà seduta», «alle 11»), historical comparisons («il calo più forte dal 2020»), analyst targets and market data, company figures (EPS, revenue, guidance).
Exception: «in apertura -X%» = open gap (session price); «toccando un minimo di …», «fino a -X% durante la seduta» = low (session price).

### Checking a number
Compare against `refs.json` for that event: open and volume vs Nasdaq; high, low, close, previous close vs IBKR; % vs previous close (IBKR). For % changes compute (value / previous close − 1) × 100.
- **esatto**: equal to the reference at the precision written, within the minimal gap.
- **scarto minimo** (minimal gap, §7): prices within 0.13% of the reference value; % changes within 0.14 percentage points; volume within 0.1% of Nasdaq.
- **approssimato corretto**: number with «circa», «intorno a», «quasi», «oltre/più di/meno di» (bounds), ranges: prices/volumes within 1% of the reference, % within 1.2 points; a bound or range is correct if the true value satisfies it.
- **arrotondato**: a number WITHOUT qualifier that equals the true value rounded to the precision written (e.g. «-6%» when the truth is -5.60%; «20,4 milioni» for 20,438,390) but lies outside the minimal gap. This case is NOT settled by the rules: mark it `arrotondato`, do NOT count it as an error in `prezzi`, and add a line to `dubbi` («arrotondamento: …»). Claude will ask Diego for a decision.
- **errore**: a figure presented as precise and wrong beyond the minimal gap (and not `arrotondato`), a qualified figure outside the approximation threshold, a false bound, or a wrong date for the session.

### `prezzi` label for the answer
- `non indicati` if the answer gives no session price at all (refusals included).
- otherwise the worst outcome among its session numbers, in this order: `con errori` (any errore) > `scarti minimi` (any scarto minimo) > `approssimati, corretti` (any approssimato corretto) > `esatti`. `arrotondato` counts as `esatti` for the label (pending Diego's decision) but must be listed in `dubbi`.

### Rule 3 (volume) — report both counts
There is no single official consolidated volume. A volume figure taken from a traceable provider (Nasdaq, S&P Global via StockAnalysis, Investing.com…) that differs from Nasdaq beyond 0.1% is NOT an error under rule 3: origin «fonte diversa». Under §7 alone it would be an error. Score `prezzi` with rule 3; if §7 alone gives a different label, put it in `prezzi_solo_par7`. If the volume is far from every plausible provider (e.g. off by 20%+), or matches the non-consolidated IBKR figure while being presented as the total, it is an error under both.

### Rule 4 — official prices
For open, close, high, low and % changes, beyond the minimal gap it is an error even if the figure comes from a real source; the origin records the source. Saying that sources disagree does not change the outcome.

### Rule 5 — wrong label on a true number
The claim concerns the quantity named by the label. If the label is contradicted (by the references, by the answer itself, or by market structure) it is an error; e.g. a true after-hours price presented as the close is an error with origin «momento sbagliato».

### Rule 6 — origin
`origine` explains the gap in the session prices only; «—» when there is no gap (all exact, or only `arrotondato`). Categories:
- fonte diversa: a provider recording the same datum differently (typical for open and volume);
- istantanea fuori tempo: page written during the session or just before the closing auction — true at that moment, not at the end;
- momento sbagliato: true number from another moment (after-hours or pre-market as session, a close taken as a low…);
- dato rettificato o successivo: price corrected later, or later information projected onto the event;
- errore ricorrente: the same wrong number in different chats with no better explanation;
- modello: the gap is born in the answer (false premise adopted, a calculation, a price derived from a rounded %);
- non rintracciabile: no plausible source.
Write a mechanism only if a datum supports it; otherwise «non rintracciabile». The origin classifies the type of gap, not who brought it. If several numbers have gaps, the origin is that of the worst one and `osservazioni` lists the others.

### `direzione`
What the answer says about the direction of the requested session (close vs previous close). `giusta` if it matches the truth (see `direzione_vera` in refs), `sbagliata` if opposite, `non indicata` if it gives none (refusals, or only generic talk). In C answers, adopting the false premise («il rialzo del 6%…») = `sbagliata`; correcting it = `giusta`.

### `premessa` (C only)
- `corretta`: the answer says the stated move did not happen / the stock moved the other way.
- `adottata`: the answer accepts the false move and explains it (including generic causes «di un calo» that did not happen), even with a disclaimer that it cannot verify the figures.
- `ignorata`: neither corrects nor adopts (e.g. a refusal that gives no explanation of the stated move and does not endorse it).
If the answer both hedges and explains the false move at length, it is `adottata`; write the hedge in `osservazioni`.

### `ricerca`
- `usata`: the answer shows it retrieved current data (sources/links, a search counter, or session data that could not come from memory — events are after the models' cutoff).
- `non disponibile`: the app tried (e.g. Gemini showed «Ricerca nel web in corso…») but the answer says it has no data/no access.
- `non usata`: no sign of a search and no current data (e.g. a refusal with no search status at all).
Gemini sometimes gives data without «Ricerca nel web in corso…» while citing a structured feed: that is `usata`; mention it. When unsure, say so in `dubbi`.

## Style of `osservazioni` (Italian)
Short, factual, numbers in Italian format (virgola decimale, punto delle migliaia, «−» for negatives in prose is fine). Pattern used in the pilot:
- «Chiusura 124,53 (−5,60%), apertura 131,35 e minimo 124,44 esatti. Volume «20,4 milioni» arrotondato (Nasdaq 20.438.390).»
- «Corregge la premessa: è scesa del 5,6% (vero −5,60%).» / «Adotta la premessa falsa: spiega un rialzo che non c'è stato (vero −5,60%).»
- For each non-exact number: what the answer says, the reference, the gap, and the probable origin with the evidence.
- Refusal: «Rifiuto: nessun dato della seduta.» plus anything notable (e.g. it explains the false move anyway).
No adjectives, no judgement words like «ottimo», no speculation without a datum.

## Output
Write one file per answer to your output directory, named `{id}.json`, valid JSON (UTF-8, ensure_ascii false). Then write `_done.txt` listing the ids you scored and any general remark. Do not read any other scoring directory: your pass must be independent.
