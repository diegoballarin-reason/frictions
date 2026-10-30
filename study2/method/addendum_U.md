# Addendum for this wave (U answers: study 2 and Gemini exploration blocks E3–E4) — read after rules.md

This wave scores the **U** answers, which were left for last as a work order (26 October, 21:03): the scoring rules are the same as for the A and C answers. Differences from rules.md are listed here; apply them directly. Everything decided while scoring A and C (below) applies.

## Files
- Answers are `answers/{id}.json`. 70 answers:
  - 60 from the pre-registered rounds of study 2: ids `s2-{ev}U-{rep}-{app}` (ChatGPT and Claude twice per event, Gemini once);
  - 10 from Gemini's exploration blocks E3 (27 October) and E4 (28 October): ids `e3-{ev}U-gemini`, `e4-{ev}U-gemini`.
  Use the `id` field as the output file name: `{id}.json`.
- The U question is always: «Quali sono stati il prezzo di apertura ufficiale, il prezzo di chiusura ufficiale e il volume complessivo del titolo X nella seduta del …?». It asks for three session prices: the official open, the official close and the total (consolidated) volume.
- `refs.json` is the frozen reference set of rules.md, with one added field per event: `volume_ibkr_non_consolidato` (IBKR volume, NOT consolidated). It is never a reference for scoring; use it only to recognise the rule-3 case «matches the non-consolidated IBKR figure while being presented as the total».

## Output fields
Same as rules.md, with these differences:
- `premessa`: always "" (U answers have no premise).
- `direzione`: what the answer says about the direction of the session (close vs previous close), if it says anything; `non indicata` if it gives only open, close and volume without saying whether the stock rose or fell. Giving the close and the previous close without saying "up" or "down" is `non indicata`; a stated change («in calo del 5,60%») is a direction.
- Add `contestabile`: Italian string, or "" if not applicable. See «Sign ◊» below.
- Score every session price in the answer, not only the three asked for (high, low, changes, previous close are session prices too).

## Rules 10–12 (decided by Diego on 26 October)
- **Rule 10 (replaces the «arrotondato» case of rules.md).** A figure WITHOUT qualifier that equals the true value rounded to the precision written, but lies outside the minimal gap, is correct. Mark its `esito` as `arrotondato (giusto)`; it counts as `esatti` for the label and does NOT go in `dubbi`. Examples: «20,4 milioni» for 20,438,390; «−12%» for −11,76%.
- **Rule 11.** A range with «circa», «intorno a» or «nell'ordine di» (e.g. «circa il 4-5%») gets the approximation tolerance at its bounds (1,2 points for %; 1% for prices and volumes). If the true value falls within that widened range, `esito` = `approssimato corretto`.
- **Rule 12.** «ha toccato», «è arrivato a», «raggiungendo» WITHOUT naming an extreme indicate a level passed during the session: correct if it lies between the session low and high. Mark `esito` = `livello in seduta (giusto)` (counts as `esatti` for the label). Words that name an extreme — «massimo», «minimo», «picco», «fino a» — remain extremes and are checked against high/low (rule 5).

## Decisions taken by Diego on 27 and 28 October (apply them)
- **First price traded = open.** A figure described as the first price traded at the opening («primo prezzo battuto all'apertura», «primi scambi delle 9:30») is an open and is checked against the Nasdaq open. Exception: when the same answer gives the official open separately, the first-trade figure is not scored, and the case is recorded in `contestabile`.
- **Extremes with a time or phase.** A high or low tied to a time or phase is still an extreme when it is the only high or low the answer gives: check it against the session high/low; if wrong, it is an error (no doubt, no sign). When the answer gives the session high or low separately, a phase-tied peak is not scored: mention it in `osservazioni` under «Non conteggiato».
- **Half-cent Nasdaq opens.** When the Nasdaq open ends in half a cent (131,345; 257,825; 579,505; 1.002,445; 29,027 is not a half cent), both roundings to the cent are `esatto`.
- **Volume beyond 0,1% from Nasdaq (rule 3).** A plausible volume that differs from Nasdaq beyond 0,1% is `fonte diversa` under rule 3, with or without a provider named next to it. Give `prezzi_solo_par7` as rules.md says and fill `contestabile`. A volume far from every plausible provider (20%+ off), or matching `volume_ibkr_non_consolidato` while presented as the total, is an error under both, without the sign.
- **Ranges** (two values for the same figure, e.g. «260,27 – 260,36 $»): correct if they contain the truth (`approssimato corretto`); with «circa», rule 11 applies.
- **«circa» applies only to the figure it immediately precedes**, not to other figures in the same sentence (e.g. «un rialzo di circa il 7% (con picchi fino all'8%)»: the 8% is a precise figure).
- **«vicino a»** counts as «circa».
- **An unlabelled «circa X%»** (no session moment named) counts as the session change.
- **Origins deduced from indirect data** (title or address of a source, order of the numbers in the answer) are kept, with a note saying what they rest on.

## Sign ◊ («contestabile»)
Definition (Diego, 27 October): a figure left out, or accepted, by a convention that would otherwise count it as an error. Fill `contestabile` with one Italian sentence: the figure as quoted, the reference and the gap, and the convention applied. Typical cases: a volume accepted as `fonte diversa` under rule 3 that §7 alone would count as an error; a first-trade figure left out because the official open is given separately. The sign never changes the label. Do not use it for timed extremes (they are errors) or for figures that are simply correct.

## Conventions already applied in study 2
- Source titles shown in the text (e.g. «Falls 7.5%» in a source title or a chip label) do not count as claims of the answer.
- A figure with «circa» is always an approximation (`approssimato corretto` if within tolerance), even when it coincides with the truth.
- Origin «—» when the only non-exact figures are correct approximations, or when there is no gap.
- A figure attributed to a named source by the answer («secondo Reuters…», «Investing.com riporta…») is still a claim of the answer and is scored (rule 4: saying that sources disagree does not change the outcome).
- A refusal («Non dispongo…», no session data): `prezzi` = `non indicati`, `osservazioni` «Rifiuto: nessun dato della seduta.» plus anything notable (sites suggested, a search status).

## Notes on these answers
- Many U answers discuss how providers differ («Investing.com riporta circa 20,44 milioni, contro i 20,31 milioni indicati sopra, che vengono da S&P Global»). Score each session figure given as a value of the session, with its label. If the answer itself reports a figure only to reject it (e.g. «un sito mostrava 90,46 durante la seduta, probabilmente dati provvisori; il valore giusto è 91,02»), this case is NOT settled by the rules: score the figure the answer adopts, describe the rejected one in `osservazioni`, and write the case in `dubbi`.
- A volume explicitly limited to one venue or one part of the day (e.g. «volume sul solo NYSE», «nell'asta di chiusura») is a different quantity from the consolidated session volume (rule 5): if its label is contradicted by the references or by market structure it is an error; otherwise it is not a session figure: do not score it, mention it in `osservazioni`. When unsure, `dubbi`.
- Official open and official close: for NYSE stocks the official open and close are the auction prices. Compare as rules.md says (open vs Nasdaq, close vs IBKR). An after-hours or last-trade price presented as the official close is rule 5 (wrong label) if it is beyond the minimal gap.
- Source chips appear in the text as a line with the source name (e.g. «Investing.com», «stockanalysis», «+2»): they are not claims. Tables are flattened with tab characters and blank lines; read through them. Suggested follow-up questions at the end are not claims.
- `segnale_ricerca` and `note` were written by the transcriber; `link` lists the sources shown in the answer.
- Other numbers (other sessions, pre-market, after-hours, intraday points, averages, history, analysts, company figures) are not session prices: do not score them here; mention them briefly under «Non conteggiati» in `osservazioni` when they matter. They are counted in a separate wave (rule 8).
- In `osservazioni`, do not use the phrase «all'indietro».

## Still open (do not resolve; write in `dubbi` if it occurs)
- Anything the rules and decisions above do not settle. Do not invent a rule.
