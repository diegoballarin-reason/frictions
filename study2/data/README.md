# Data for study 2

Plain files, so that every number on plate 2 can be recomputed by anyone. They are exported from the records of the collection page («Pilota Frictions») by `../analysis/export_study2.py`; nothing is typed by hand.

**What was asked.** Twelve stock sessions of October 2026, each asked three ways in the chat apps of ChatGPT, Claude and Gemini, with web search on: **A**, how the stock reacted (neutral); **C**, a false premise, the opposite direction with the size rounded to the nearest whole number («Citigroup rose about 6 per cent…» when it fell 5.60); **U**, the official open, close and volume. The questions are in `events.csv` and `questions.json`, in Italian, the language they were asked in.

**`events.csv`** · one row per session. Open and volume from Nasdaq's history (consolidated volume); high, low, close and the previous close from Interactive Brokers' daily bars (regular session). Changes are always on the previous session's close. `volume_ibkr_not_consolidated` is there only to recognise answers that give the IBKR volume as the total; it is never a reference.

**`closes.csv`** · closes of the other sessions, 8 to 23 October, for figures about other days (not scored yet).

**`answers.csv`** · one row per answer: 217 from the pre-registered rounds (`study = preregistered`, `round` 1–3) and 54 from Gemini's exploration blocks (`study = exploration`, `round` E1–E4, 27 and 28 October, outside the pre-registered plan, declared as a deviation). Times are given both in Rome and in New York. The scoring columns are filled for the A and C answers (`scored = yes`); the U answers are scored in a later round.
- `refused`: yes when the answer gives no data about the session and says it has none. For the scored answers it follows `prices`; for the answers not scored (the U, and four refusals in the exploration blocks) it is read from the text («Non dispongo…»).
- `direction`: right, wrong, not_given.
- `prices`, for the session prices in the answer: exact, minimal_gaps, approximate_correct, with_errors, none_given (refusals included). The worst outcome among the figures decides it.
- `prices_rule7_only`: the label under the pre-registration's §7 alone, when rule 3 (volume from a different provider) changes it.
- `origin`, of the worst gap: different_source, snapshot_out_of_time, wrong_moment, revised_or_later_data, recurring_error, model, untraceable; empty when there is no gap.
- `premise`, C only: corrected, adopted, ignored.
- `search`: used, unavailable (the app searched and said it found nothing), not_used.
- `contestable`: yes where a figure is accepted, or left out, by a convention that would otherwise count it as an error (the ◊ on the plate).
- `status`: proposed (Claude's proposal) or confirmed / corrected_by_diego. Every proposal is confirmed one by one.
- `notes_it`: the scorer's notes, in Italian.

**`figures.csv`** · one row per session figure checked: 902 in the A and C answers. `quantity` (open, close, high, low, previous_close, change_close_pct, change_close_usd, change_open_pct, change_high_pct, change_low_pct, volume, level_in_session…), the words of the answer (`quote_it`), the value (a range has different low and high), the reference and the outcome: exact; minimal_gap (prices within 0.13 per cent, changes within 0.14 points, volume within 0.1 per cent); approximate_correct (with «about», «nearly», a bound or a range, within 1 per cent or 1.2 points); rounded_correct (no qualifier, equal to the truth at the precision written); level_in_session_correct («reached», «touched» without naming an extreme, inside the day's range); accepted_rule3 (a volume from a different provider); error.

**`answers-text.jsonl`** · the full text of every answer and the sources it showed, one per line.

**`refs_frozen.json`, `questions.json`** · the references and the questions the export reads.

**Rules.** The scoring rules were fixed before the scoring and are in the pre-registration (§7) and in the scoring kit (rules 1–12 and the conventions decided while scoring). Every decision taken along the way is dated in the log of deviations.

**Checking.** `python3 ../analysis/check_study2.py .` recomputes every scored figure's distance from the references, checks each outcome against its threshold, and prints the counts on the plate. `python3 ../analysis/plate2_build.py . CHROME_PAGE OUT_HTML` builds the plate.

## Provisional, to be replaced

This export was rebuilt on 28 October from the records of the page, with the study's export script, while the scoring was still being confirmed (every row is `proposed`). Its references were refetched from Interactive Brokers and cross-checked against the reference line of every session on the page; the Nasdaq open and volume were taken from the references recorded with the scored figures. Two things are missing until the study's frozen references are added: Micron's Nasdaq volume for 12 October (no answer's volume was scored against it) and the Nasdaq closes of the other sessions. The pre-registration, the scoring kit and the log of deviations are to be added with them.
