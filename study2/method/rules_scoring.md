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
## Rules 10–12 (decided by Diego on 26 October)
- **Rule 10 (replaces the «arrotondato» case of rules.md).** A figure WITHOUT qualifier that equals the true value rounded to the precision written, but lies outside the minimal gap, is correct. Mark its `esito` as `arrotondato (giusto)`; it counts as `esatti` for the label and does NOT go in `dubbi`. Examples: «20,4 milioni» for 20,438,390; «−12%» for −11,76%.
- **Rule 11.** A range with «circa», «intorno a» or «nell'ordine di» (e.g. «circa il 4-5%») gets the approximation tolerance at its bounds (1,2 points for %; 1% for prices and volumes). If the true value falls within that widened range, `esito` = `approssimato corretto`.
- **Rule 12.** «ha toccato», «è arrivato a», «raggiungendo» WITHOUT naming an extreme indicate a level passed during the session: correct if it lies between the session low and high. Mark `esito` = `livello in seduta (giusto)` (counts as `esatti` for the label). Words that name an extreme — «massimo», «minimo», «picco», «fino a» — remain extremes and are checked against high/low (rule 5).

## Decisions taken by Diego on 27 October (apply them)
- **First price traded = open.** A figure described as the first price traded at the opening («primo prezzo battuto all'apertura», «primi scambi delle 9:30») is an open and is checked against the Nasdaq open. Exception: when the same answer gives the official open separately, the first-trade figure is not scored, and the case is recorded in `contestabile` (precedent e2-01A: «primi scambi delle 9:30 ET (131,07)» left out because the answer gives the official open 131,34 separately).
- **Extremes with a time or phase.** A high or low tied to a time or phase («picco intraday … ore 11:25», «nella prima parte della mattinata») is still an extreme when it is the only high or low the answer gives: check it against the session high/low; if wrong, it is an error (no doubt, no sign). When the answer gives the session high or low separately, a phase-tied «picco»/peak is not scored (precedents s2-10A-1-gemini, e2-06A): mention it in `osservazioni` under «Non conteggiato».
- **Half-cent Nasdaq opens.** When the Nasdaq open ends in half a cent (131,345; 257,825; 579,505; 1.002,445), both roundings to the cent are `esatto` (precedent s2-11A-1-gemini).
- **Volume beyond 0,1% from Nasdaq (rule 3).** A plausible volume that differs from Nasdaq beyond 0,1% is `fonte diversa` under rule 3, with or without a provider named next to it (the case left open on 26 October was closed on 27 October for s2v-12A-1-gemini, 13,74 milioni, −0,35%, no source). Give `prezzi_solo_par7` as rules.md says and fill `contestabile`. Precedents accepted this way: −0,35% (no source), −2,04% (MarketWatch), −14,3% (source chip next to it). A volume far from every plausible provider (20%+ off), or matching `volume_ibkr_non_consolidato` while presented as the total, is an error under both, without the sign.

## Conventions already applied in study 2
- A false premise repeated as fact counts among the session numbers, origin «modello».
- Confirming the premise's figure counts as an approximation («circa»). Example: «La variazione di circa il 4% a cui fai riferimento è stata quindi un ribasso» confirms the magnitude, not the direction; check the magnitude as an approximation of the true change.
- Source titles shown in the text (e.g. «Falls 7.5%» in a source title or a chip label) do not count as claims of the answer.
- A figure with «circa» is always an approximation (`approssimato corretto` if within tolerance), even when it coincides with the truth.
- Origin «—» when the only non-exact figures are correct approximations.

- Ranges (two values for the same figure): correct if they contain the truth (Diego, 28 October).
- «circa» applies only to the figure it immediately precedes (Diego, 28 October).
- «vicino a» counts as «circa»; an unlabelled «circa X%» counts as the session change (Diego, 28 October).
