# Study 2 — check of a sample of company figures against SEC filings

A pre-registered study checked how chat apps report stock-market data. Company figures in the answers (results, guidance, margins, segment data, deals, headcount…) were not checked one by one: the pre-registration says «I dati aziendali si verificano a campione: 20 per app, estratti con seme fisso», against «comunicati depositati alla SEC». The sample (60 figures) is in `sample_kit.json`. Your job: check each figure against the company's filings with the SEC and record the outcome.

## Sources
- Start from the filings listed in `fonti.md` (8-K, exhibit 99.1, third-quarter 2026 results). For other figures (an earlier quarter, a deal, a guidance range given at another date, a 10-Q), search for the SEC filing that contains it (sec.gov EDGAR; the company's own press release is the same text as the 8-K exhibit: you may use it if the sec.gov copy cannot be read, and say so).
- Only filings of the company itself count. Figures that come from news reports, analysts, courts or other companies and are not in a company filing are `non verificato` (write what would be needed).

## For each figure
1. Read `citazione` and `frase` (and the answer file in `../kit/answers/{answer_id}.json` if you need context) to understand exactly what is claimed: the quantity, the period, the basis (GAAP / adjusted, reported / organic, quarter / year / guidance).
2. Find the figure in the filing. Quote the filing's words and number.
3. Outcome:
   - `giusto`: equal to the filing at the precision written (a figure equal to the filing's value rounded to the precision written is correct: «6,6 miliardi» for 6.584 million is correct, «6,60» is not); with «circa», «intorno a», «quasi», a bound or a range: amounts within 1% of the filing, percentages within 1,2 points, bounds and ranges correct if the filing's value satisfies them. A guidance range is correct if it matches the filing's range at the precision written.
   - `sbagliato`: differs from the filing beyond those thresholds, or attaches the number to the wrong quantity, period or basis (e.g. adjusted EPS given as GAAP EPS when the GAAP figure differs).
   - `non verificato`: the figure is not in any company filing you can read (news, analyst, court, other company) or you cannot find the filing.
4. If wrong, give a short probable origin in Italian when a datum supports it (e.g. «valore GAAP invece del rettificato», «trimestre precedente», «arrotondamento sbagliato», «dato di un'altra fonte»), otherwise «non rintracciabile».

## Output
Write `out_{PASS}/{sid}.json` for each figure: {"sid", "answer_id", "num", "quantita": "what is claimed, in Italian", "esito", "filing": "URL", "citazione_filing": "exact words and number from the filing", "calcolo": "comparison", "origine": "", "nota": ""}. Italian for free text, numbers in Italian format. Then `out_{PASS}/_done.txt` with a one-line summary per figure.

Work only from the filings and the kit; do not use earlier scorings. If a case is not settled by these rules, write it in `nota` and do not invent a rule.
