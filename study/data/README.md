# Data for *Where No One Can Know*

Two files, so that every number in the study can be recomputed by anyone.

**`daily-bars.csv`** · daily bars, regular session only, for the nine stocks with a price claim, 1 May to 27 October 2026. Downloaded from Interactive Brokers on 27 October 2026 (`ticker`, `ibkr_conid`, `date`, `open`, `high`, `low`, `close`, `volume`). NXT is the Nasdaq listing now named Nextpower. The rows are as the broker returned them: on two IBM sessions outside the study window (12 and 20 May) the close falls a cent outside the day's range, and nothing is corrected.

**`claims.csv`** · the ten claims about a price, one row each. `origin` says who introduced the figure or the premise: `model`, or `user` (me). `claimed_low_pct` and `claimed_high_pct` hold the claimed move when the claim gives a number; `claimed_direction` holds it when it gives only a direction. `checked_on` says which price answers the claim: the `open` for after-hours claims, which the daily bars cannot show and which carry into the next open; the `close` otherwise. `protocol_type` is the type in the protocol's findings table.

Percentages are always on the previous session's close, as the protocol requires. The script in `../analysis/` recomputes them and checks them against the figures in the text.
