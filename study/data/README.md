# Data for *Where No One Can Know*

Two files, so that every number in the study can be recomputed by anyone.

**`daily-bars.csv`** · daily bars, regular session only, for the nine stocks with a price claim, 1 May to 27 October 2026. Downloaded from Interactive Brokers on 27 October 2026 (`ticker`, `ibkr_conid`, `date`, `open`, `high`, `low`, `close`, `volume`). NXT is the Nasdaq listing now named Nextpower. The rows are as the broker returned them: on two IBM sessions outside the study window (12 and 20 May) the close falls a cent outside the day's range, and nothing is corrected.

**`claims.csv`** · the fourteen rows of the protocol's findings table, one claim each, with the model's sentence as it appeared in the chain (`claim_it`, in Italian, the language of the exchange) and a short English summary. `origin` says who introduced the figure or the premise: `model`; `user_premise`, a premise of mine the model built on; `user_figure`, a figure of mine the model adopted. `claim_date` is when the claim was made, `session` the trading session that answers it. `checked_on` names the price that answers it: the `open` for claims about after-hours or pre-market trading, which daily bars cannot show and which carry into the next open; the `close` otherwise. `claimed_low_pct` and `claimed_high_pct` hold the claimed move when the claim gives a number (a low with no high means "more than"); `claimed_direction` holds it when it gives only a direction. The four rows with no `session` are not about a price. `protocol_type` is the type in the findings table.

Percentages are always on the previous session's close, as the protocol requires. The script in `../analysis/` recomputes them and checks them against the figures in the text.
