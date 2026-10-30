# H1 · extra check of 48 group-A claims (study 2) — instructions

## Why
In the H1 wave, these 48 claims about other sessions, phases of other days, history and hypotheses on the premise were marked `non verificato` because the kit had no data for those dates (one, E20, has a provisional outcome to double-check). The study's references allow looking them up: prices of other sessions come from IBKR (pre-registration §6), and sessions outside the frozen file are looked up in the price history, as in the pilot. Your job: fetch the data, check each claim with the H1 rules, and write one result per claim.

## Files
- `claims.json`: the 48 claims. Fields: `cid` (E01–E48, use it as the output file name), `answer_id`, `n`, `ticker`, `seduta_evento` (date of the session asked about), `tipo`, `citazione` (short quote), and what the first wave wrote (`nota_finora`, `riferimento_finora`, `calcolo_finora`).
- Full answer texts: `../../kit/answers/{answer_id}.json`, field `risposta`. Read the sentence around each quote: the context often fixes the date, the base of a % move or the window.
- Rules: `rules_h1.md` (types, windows, history checks) and `rules_scoring.md` (thresholds, rules 10–12, decisions). They apply unchanged.
- Data already available (read-only): `../../hist/daily_0922_1028.json` (Nasdaq daily 22/09–28/10/2026), `../../hist/sheets.json`, `../../bars5/bars5.json` (5-minute bars of the event day and the previous after-hours), `../../hist/ibkr_extra/` (IBKR daily already fetched: HAS May–Oct 2026, LMT Oct 2025–Oct 2026, CMG Oct 2025).

## Data sources you may use
1. **IBKR connector, read-only tools only**: `mcp__Interactive_Brokers_IBKR__search_contracts` and `mcp__Interactive_Brokers_IBKR__get_price_history`. Never call any other IBKR tool (no orders, alerts, watchlists, screeners, account tools). Load them with ToolSearch (`select:mcp__Interactive_Brokers_IBKR__get_price_history,mcp__Interactive_Brokers_IBKR__search_contracts`).
   - Contract ids: C 87335484 · LRCX 732440574 · GM 80986742 · META 107113386 · CMG 37655664 · MU 9939 · HAS 754956 · LMT 611191 · IP 8511 · CCI 176571182 · DDOG 383858515 · GFS 523222624. Other instruments (International Paper's London listing, SpaceX, AT&T, T-Mobile…): find them with `search_contracts`; if there is no usable data, the claim stays `non verificato`.
   - `get_price_history` returns bars up to now: choose `period` (ONE_MONTH, THREE_MONTHS, SIX_MONTHS, ONE_YEAR, TWO_YEARS, FIVE_YEARS) and `step` (ONE_DAY for sessions; FIFTEEN_MINS or FIVE_MINS for phases of recent days). `outside_rth: false` for regular-session bars; `true` only for pre-market / after-hours questions. TWO_YEARS starts around 30/10/2024, so dates in 2023 or on 21–22/10/2024 need FIVE_YEARS.
   - The response has parallel arrays (`time`, `open`, `high`, `low`, `close`, `volume`). Do NOT read values by counting positions in the text: copy the arrays you need into a Python script and index them by date. Check the alignment on at least two known closes (e.g. the event close and the previous close in the table below, or `daily_0922_1028.json`). Daily `time` stamps are the session dates (13:30Z or 14:30Z = 09:30 New York). Intraday stamps are UTC: New York = UTC−4 until 1/11/2026 (UTC−5 in winter).
   - Save the data you use, compactly, in your `data/` folder (e.g. `data/LMT_daily.json` as {date: {o,h,l,c}}), so the reconciliation can re-check it.
2. **Web** (WebSearch / WebFetch) only for dates and facts that are not prices: earnings release dates (prefer the company's 8-K on sec.gov or its press release), the date of an announcement named in the claim. Cite the URL in `riferimento`.

Known closes for alignment (IBKR): C 13/10 124,53 (prev 131,92) · LRCX 22/10 230,15 (260,81) · GM 20/10 77,09 (82,75) · META 22/10 648,85 (697,52) · CMG 21/10 28,12 (29,65) · MU 12/10 989,04 (1.029,00) · HAS 20/10 109,52 (98,49) · LMT 22/10 589,91 (551,51) · IP 15/10 34,10 (31,90) · CCI 23/10 85,97 (78,83) · DDOG 19/10 260,36 (247,11) · GFS 14/10 48,94 (46,70).

## How to judge
- Thresholds, rules 10–12, «circa» scope, ranges and bounds: exactly as in `rules_h1.md` / `rules_scoring.md`.
- A % move of a past session is close-to-close vs the previous session's close, unless the answer says otherwise. «Tra marzo e giugno», «dopo i conti di luglio», «in N mesi»: read the claim as the answer frames it; when two standard readings exist (calendar months vs sessions; from the close before the first session vs from a later close; close-to-close vs the intraday extreme for a "drop after earnings"), a figure that matches either reading is `giusto` (as with two sources): say which reading you used and give the numbers for both.
- Earnings reactions: the reaction session is the first regular session after the release (release before the open → same day; after the close → next day).
- Phases of a day: the windows of `rules_h1.md`. A phase that is not in that list (e.g. «a metà mattina») is read with the narrowest listed window that contains it («in mattinata», 09:30–12:00); write `finestra non nelle regole: letta come «…»` in `nota`, because the convention still has to be confirmed.
- Averages and moving averages of price: compute them from the closes (simple moving average of the N sessions up to the session named; say which session).
- Use `non verificato` only when, after trying, the data needed are not available (write what is missing). Do not guess.
- Every check is a short Python calculation; put the formula and result in `calcolo`.

## Output
One JSON file per claim in your output folder, named `{cid}.json`, UTF-8 (ensure_ascii false):
```json
{"cid": "E01", "answer_id": "s2-01C-1-claude", "n": "32", "esito": "giusto | sbagliato | non verificato",
 "riferimento": "source and values used (IBKR conid, dates, OHLC; URL for dates)",
 "calcolo": "formula → result → comparison with the threshold",
 "nota": "readings considered, provisional conventions, anything a reviewer should know (Italian)",
 "dati": ["data/C_daily.json"]}
```
Text fields in Italian. Never use the phrase «all'indietro». Do not read or write anything outside your own output folder except the read-only inputs listed above, and do not look at the other pass's folder. At the end, reply with a short summary: counts by outcome and anything you could not resolve.
