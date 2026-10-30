# Study 2 — H1 wave: every number in the answers, by type (rules for the scorers)

You are reviewing the numbers in answers that three chat apps (ChatGPT, Claude, Gemini) gave to pre-registered questions about how a US stock moved in one session in October 2026. The question types are: **A** (neutral: how did the stock react?), **C** (false premise: the question states the opposite move), **U** (official open, close and total volume). The session prices of each answer (open, close, high, low, previous close, the session's changes and volume) have already been scored in other waves. This wave is about **all the other numbers**, as fixed in the pre-registration (§7, §8) and in rule 8 (decided with Diego on 26 October). Apply these rules literally. When a rule does not settle a case, do NOT invent a rule: record the doubt in `dubbi`.

## Files in the kit
- `answers/{id}.json`: one answer each, with `domanda` (the question), `risposta` (full text), `link`, `segnale_ricerca`, `data` and `ora_invio` (Rome time when it was sent; New York = Rome − 6 h until 25 October 02:00 Rome, Rome − 5 h after), and `candidati`: the numbers found in the text by an automatic extractor (the same one used in the pilot), each with `n`, `num` (the token), `tipo_auto` (the extractor's type guess), `ctx` (a window around it) and `frase` (the sentence). Review every candidate, in order.
- `session_scored/{id}.json` (A and C answers only): the session figures already scored for that answer (`numeri`: quote, quantity, value, outcome). Use it only to recognise which candidates are session prices.
- `refs/refs_frozen.json`: frozen references per ticker: the session (IBKR daily bar: `open`, `high`, `low`, `close`, `prev_close`; `nasdaq`: open, high, low, close, volume), and `closes` (IBKR) / `nasdaq_closes` for 8–23 October.
- `refs/daily_0922_1028.json`: Nasdaq daily bars (open, high, low, close, volume) for every session from 22 September to 28 October 2026, per ticker.
- `refs/sheets.json`: per ticker, computed from the Nasdaq history (28 Oct 2016 or listing → 28 Oct 2026): `ev` (event session), `prev`, `ev_ohlcv`, `ch` (session change %), `last_larger_same_sign` (last earlier session with a close-to-close change at least as large in the same direction, and that change), `last_close_beyond` (last earlier session that closed at or beyond the event close in the event's direction: at or below for a fall, at or above for a rise), `last_extreme_beyond` (same for the low on a fall / the high on a rise), `max_before` (highest close and highest high before the event, with dates), `w52_before` (52-week high and low in the 252 sessions before the event, with dates), `ytd` (last close of 2025, its date, YTD % at the previous close and at the event close), `back` (close 5, 10, 21, 63, 126, 252 sessions before the event, with the % change to the event close), `avgvol` (average volume of the 10, 20, 30, 50, 63, 65, 90 sessions before the event, event excluded), `last_vol_beyond` (last earlier session with volume ≥ the event volume).
- `refs/bars5.json`: Yahoo Finance 1-minute bars (with pre-market and after-hours) aggregated into 5-minute bars, New York time, for two days per ticker: the previous session (only its after-hours, from about 15:55) and the event day from 04:00 to 20:00. Each bar: `t` (start time "HH:MM"), `o`, `h`, `l`, `c`. Minutes without trades are missing.
- `refs/yahoo_summ.txt`: summary of the same 1-minute data per event: after-hours of the previous session (first, min with time, max with time, last), pre-market (same), the last trade at 15:59, after-hours of the event day, and 30-minute bars. Isolated anomalous prints in pre-market are noted at the end of the file (e.g. LRCX 260,81 at 9:22, GM 86,21 at 6:30, GFS 53,00 at 8:30, LMT 608,00 at 9:30): read them with the nearby bars.
- `rules_scoring.md`: the scoring rules of the session-price waves (definitions, thresholds, rules 3–6). Read its «Checking a number» section: the same thresholds apply here.

## Step 1 · Is the candidate a claim?
A claim is a number stated as a fact about the world (a price, a change, a volume, an amount, a count, a ratio, a year used as a comparison point such as «dal 2020»). Mark `affermazione: false`, with `escluso` = one of the reasons below, when the token is:
- `data/ora`: a date or clock time used to place something («13 ottobre», «alle 16:00», «2026» in «13 ottobre 2026»), a quarter or year as a label («terzo trimestre 2026», «Q3»);
- `numerazione`: list numbering, footnote markers, «+2» citation counters, version numbers;
- `fonte`: a number inside a source title, chip or URL shown in the text («Falls 7.5%» in a headline);
- `domanda`: the question's own figure repeated or quoted as the user's premise («il 6% di cui parli») without being asserted;
- `ripetizione`: the same number repeated in the same claim (e.g. a table cell that repeats a figure already counted in the same sentence). Do not use it for the same figure stated again in a different sentence: that is a new claim.
- `altro`: anything else, explained in `nota`.
A range «tra 124 e 125» is ONE claim: mark the second bound `affermazione: false`, `escluso: ripetizione`, and put the range on the first.

## Step 2 · Type (the pilot's seven types)
Assign `tipo` to every claim:
1. `seduta richiesta`: session prices of the requested session, as defined in rules_scoring.md («Session prices»): open, close, high, low, previous close used as the base, the session change in % and $, open gap %, high % and low % vs previous close, consolidated session volume. Check `session_scored` when in doubt. These are NOT verified here (`esito` = `seduta`).
2. `altre sedute`: prices, changes or volumes of the same stock in other sessions: the day after, the week before, a specific earlier session, moves over several sessions («in due sedute», «nella settimana», «da inizio mese», «da inizio anno»).
3. `fuori seduta e intraday`: pre-market and after-hours (of the event day, or of the previous evening when the news came after the close); points of the session tied to a time or phase that are not the official extremes («nei primi minuti», «a metà seduta», «alle 11», «nel finale»).
4. `storico`: comparisons with the stock's history: records, «il calo più forte dal…», 52-week highs/lows, multi-year levels, average volumes («media a 30 giorni», «volume medio»), «il volume più alto da…», the years used as comparison points.
5. `ipotesi`: C answers only, numbers inside a hypothesis about where the false premise could come from («forse ti riferisci al +6% del 9 ottobre»).
6. `analisti e mercato`: price targets, ratings and their counts, consensus estimates presented as analysts' expectations, indices, other stocks, sectors, ETFs, macro data, market capitalisation, options.
7. `dati aziendali`: the company's own figures: results (revenue, EPS, margins, segments), guidance, cash flow, buybacks, dividends, headcount, deals and contracts, capex, production figures, store counts, subscribers.
When a number could fit two types, choose the one that says what the number is about, and write the alternative in `nota`. Expected results compared with actual ones: the actual figure is `dati aziendali`, the expectation is `analisti e mercato`.

## Step 3 · Group and outcome (rule 8)
- Group A, verified answer by answer: `altre sedute`, `fuori seduta e intraday`, `storico`, `ipotesi`. Outcome `esito`:
  - `giusto`: exact, within the minimal gap, a correct approximation, or a correct rounding (rule 10), a level passed in the window (see below);
  - `sbagliato`: beyond the minimal gap without qualifier, a qualified figure beyond the approximation tolerance, a false bound, a wrong date, a label contradicted by the references, by the answer itself or by market structure (rules 4 and 5);
  - `non verificato`: no reference in the kit allows a check (write in `nota` what would be needed).
- Group B, not verified by choice: `analisti e mercato` and `dati aziendali`: `esito` = `per scelta`. (A sample of company figures is checked later, separately: do NOT verify them now.)
- Session prices: `esito` = `seduta`.

## How to check group A
Thresholds as in rules_scoring.md: prices within 0,13% = minimal gap; % changes within 0,14 points; volumes within 0,1%; with «circa», «intorno a», «quasi», «vicino a», bounds, ranges: prices and volumes within 1%, % within 1,2 points; a bound or a range is correct if the truth satisfies it (rule 11: a «circa» range gets the tolerance at its bounds). Rule 10: a figure without qualifier equal to the truth rounded to the precision written is correct. «circa» applies only to the figure it immediately precedes. Compute every check with a short Python calculation.
- **Other sessions.** Closes: IBKR (`refs_frozen` → `closes`) and Nasdaq (`nasdaq_closes`, `daily_0922_1028`). If the two sources differ, a figure matching either is `giusto`. Changes are close-to-close vs the previous session's close, unless the answer says otherwise (e.g. «dall'apertura»). Multi-session moves: from the close before the first session to the close of the last one named. YTD: vs the last close of 2025 (`sheets.ytd`). Highs, lows, opens and volumes of other sessions: `daily_0922_1028` (Nasdaq). Volumes of other sessions follow rule 3 like the session volume (a plausible figure from another provider is `giusto`, `fonte diversa`; 20%+ off is `sbagliato`).
- **Pre-market and after-hours, phases of the session.** Use `bars5.json` and `yahoo_summ.txt`. Windows (New York time): pre-market 04:00–09:30; after-hours 16:00–20:00; «in apertura», «nei primi minuti», «nelle prime battute» 09:30–09:45; «in mattinata» 09:30–12:00; «a metà seduta / metà giornata» 11:30–14:00; «nel pomeriggio» 12:00–16:00; «nel finale», «nell'ultima ora» 15:00–16:00. A stated clock time («alle 10:42») = the 5-minute bar containing it plus one bar on each side. A level said to be reached, touched or held in a window is `giusto` if it lies between the window's lowest low and highest high (with the approximation tolerance if qualified); a stated extreme of a window («minimo del pre-market», «massimo dopo l'apertura») is checked against that window's extreme with the normal thresholds. A % move in a window is computed vs the previous session's close unless the answer gives another base. The phase of a different day than the two in `bars5.json`, or a window you cannot pin down, is `non verificato`.
- **History.** Use `sheets.json` and `daily_0922_1028.json`. «Il calo/rialzo più forte dal [data]» is `giusto` if `last_larger_same_sign` is on or before that date AND no larger move in the same direction happened after it (the sheet gives the last one: if its date is after the date claimed, the claim is `sbagliato`). «Il più forte da N anni / mesi» works the same way. «Minimo/massimo da [data]» → `last_close_beyond` or `last_extreme_beyond` (say which reading you used). 52-week, record, YTD and «N% sotto il massimo» → `w52_before`, `max_before`, `ytd`. **Average volumes**: compare with `avgvol` for the window named (3 months = 63 sessions); a figure within the thresholds of the matching window is `giusto`; providers compute averages differently, so a figure that matches no window is `non verificato` (write the closest window and the gap), NOT `sbagliato`, unless it is 20%+ off every window from 10 to 90 sessions. «Volume N volte la media»: compute event volume / average for the window named (or each window if none is named) and treat the ratio as a figure with the approximation tolerance of a %, i.e. within 1% of the ratio when qualified. Claims that need data not in the kit (e.g. «il peggior calo da quando è quotata» for a long-listed stock, intraday records, dates before 28 Oct 2016) are `non verificato`.
- **Hypotheses on the premise (C).** If the hypothesis names a measurable move («il +6% del 9 ottobre»), check it like an other-session figure; otherwise `non verificato`.

## Output (one JSON per answer, file `{id}.json` in your output directory; UTF-8, ensure_ascii false)
```json
{
  "id": "s2-01A-1-claude",
  "numeri": [
    {"n": 1, "num": "5,6", "affermazione": true, "escluso": "", "tipo": "seduta richiesta", "gruppo": "seduta", "esito": "seduta",
     "citazione": "short exact quote", "riferimento": "", "calcolo": "", "nota": ""},
    {"n": 7, "num": "−0,4", "affermazione": true, "escluso": "", "tipo": "fuori seduta e intraday", "gruppo": "A", "esito": "giusto",
     "citazione": "«nelle prime contrattazioni» −0,4%", "riferimento": "bars5 C 2026-10-13 09:30–09:45: min 129,63, max 133,50 → −1,74%…+1,20% vs 131,92", "calcolo": "−0,4% → 131,39, inside", "nota": ""}
  ],
  "conteggi": {"seduta": 0, "giusti": 0, "sbagliati": 0, "non_verificati": 0, "per_scelta": 0, "esclusi": 0},
  "origine_altri": "— | fonte diversa | istantanea fuori tempo | momento sbagliato | dato rettificato o successivo | errore ricorrente | modello | non rintracciabile",
  "osservazioni": "Italian, see below",
  "dubbi": ""
}
```
- Every candidate of the answer appears once in `numeri`, with its `n`. If the extractor missed a number that is clearly a claim of group A, add it with `n` = "x1", "x2"… and `num` as written.
- `conteggi` counts the claims (`affermazione: true`) by outcome; `esclusi` counts the rest.
- `origine_altri`: the origin of the wrong group-A numbers (categories and definitions as rule 6 in rules_scoring.md); «—» if none is wrong. If several are wrong with different origins, give the main one and list the others in `osservazioni`.
- `osservazioni` (Italian, short, factual, pilot style, numbers in Italian format): the group-A numbers with their outcome and reference, the wrong ones first; then «Non verificati: …» briefly; then «Per scelta: N (analisti e mercato M, dati aziendali K)». Do not use the phrase «all'indietro».
- `dubbi`: cases the rules do not settle; empty string if none.

## Independence
Use only the kit. Do not open any other directory of the project and do not browse the web. Another scorer reviews the same answers independently.
