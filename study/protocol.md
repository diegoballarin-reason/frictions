# Protocol

*Companion to [Where No One Can Know](where-no-one-can-know.en.md) / [Dove la causa non è conoscibile](where-no-one-can-know.it.md).*

This file carries the method rather than the argument. It exists so the study can be replicated, contested, or run in another domain by someone else. Nothing here depends on trusting the author: every check listed can be performed by a reader with a retail brokerage account.

---

## 1 · Domain suitability — the P1–P6 grid

A domain is suitable for observing constructed explanation, as opposed to failed retrieval, when it satisfies six properties.

| | Property | Why it is required |
|---|---|---|
| **P1** | Ground truth produced by third parties | The record is generated neither by the user nor by the model |
| **P2** | Fine temporal resolution | A claim made at time *T* is comparable with the state at time *T* |
| **P3** | Ex-post immutability | The record is not retroactively rewritten |
| **P4** | Low-cost verifiability by the reader | No privileged access, or the article is asking for trust |
| **P5** | High density of discrete, dated events | You need *n*, not anecdotes |
| **P6** | **Underdetermined explanation** | The decisive one — see below |

**On P6.** Where the answer is *retrievable* (who won, how much it took), an error is a retrieval failure. Where the answer is *constructed by convention* — nobody actually knows why a stock moved — the model cannot be right by retrieval. It has to fabricate. **This property is what makes construction observable rather than memory**, and it is what separates this study from the literature on factual hallucination.

### Domains that satisfy all six

- **Competitive sport.** Public results, timestamped, immutable, very high density, and *why they lost* is literally the dominant genre of sports commentary. The strongest alternative available.
- **Box office and audience charts.** P1–P4 and P6 full; P5 weaker, since the cadence is weekly rather than daily.
- **Other markets: crypto, commodities, FX.** Identical properties to equities. Crypto adds 24/7 coverage but loses density of discrete scheduled catalysts.

### Domains that fail, and on which property

- **Weather** → fails P6. The genre is forecasting, not post-hoc explanation.
- **Elections** → fails P5. Too few events a year to build *n*.
- **Technical logs, CI, internal benchmarks** → fails P4. Verifiable by you, not by the reader.
- **Scientific results and replications** → fails P2. Months or years between claim and verification.

### Where equities sit

Equity markets satisfy all six, scoring highest on P2 and P6.

**P2** — the only domain listed with a *continuous* price series: a claim made at 14:32 is comparable with the state at 14:32. Sport, box office and charts produce discrete outcomes.

**P6** — causation is structurally unobservable. In sport a portion of the causes is retrievable (injuries, sendings-off, tactical choices). In a stock price it is not.

Sport remains comparable, and superior on one point only: **the rhetorical surface is cleaner**, because no ready-made moralism about improper use is waiting there. That is an advantage of the piece, not of the method.

---

## 2 · Provenance of the material

Two statements that do not condition each other.

> The domain is suitable because it satisfies the criteria above.

> The exchange preceded the study. It was under way for unrelated reasons, and the analysis came afterwards, on material that already existed.

The second property strengthens the first: no designed experiment can claim the absence of intent that is here a fact rather than a declaration.

---

## 3 · Verification method

For each claim to be checked:

1. **Identify the ticker and the date of the claim.** Both from the transcript, without reconstruction from memory.
2. **Pull the daily bars for the window.** Any provider with an accessible historical series.
3. **Compare previous close / open / high / low / close.** In that order.
4. **Use volume as the signature of the corporate event.** The most underused instrument available: it identifies real earnings dates without any external calendar. In this study a claimed quarterly report was placed 29 days early, and the volume on the real session (3.82M against a 1.4M average) located it unaided.

**Required precision.** Report the *previous close* as the base of any percentage, never the open. A percentage computed on the wrong base is the single handle anyone needs to dismiss the piece.

---

## 4 · Limits of the observation

1. **Uncontrolled observational material.** One user, one chain, no pre-registered protocol.
2. **Explicit selection bias.** This is the conversation in which the errors *were noticed*. How many went past unnoticed is unknown — and stating this strengthens the account rather than weakening it.
3. **Daily bars contain neither after-hours nor pre-market.** Claims about evening reactions are verified **by inference** from the following opening gap, and must be reported as inference rather than measurement. The inference holds: an after-hours reaction of −12.47% does not evaporate, it transfers into the open. The stock in question opened at −1.7% and touched +3.76% intraday.
4. **No claim of generalisation** to other models or other domains.

---

## 5 · Findings table

Every row is checkable from the daily series. Percentages are computed on the previous close.

| Claim in the transcript | Date | Verified state | Type |
|---|---|---|---|
| IBM down 23–25%, area 218 | 14 Jul | 290.23 → 217.07, **−25.21%**, volume 17.7× average | **accurate** |
| Bloom, strong opening reaction | 29 Jul | 166.84 → open 183.50, **+9.99%** | **accurate** |
| Vertiv, heavy post-report fall | 29 Jul | 269.56 → open 245.99, close 223.04, **−17.26%** | **accurate** |
| NXT "just sank 12.47% after hours" | 1 Jul | open −1.7%, high +3.76%, close −2.51% | inverted |
| NXT "reported, beat EPS by 13%" | 1 Jul | real report 30 Jul, **29 days later** | non-existent event |
| AAOI down ~2% after hours, on guidance | 6 Aug | 124.22 → open 142.48, **+14.70%**, close +9.19% | inverted |
| AAOI up 13%, on the same guidance | 7 Aug | same quarter, opposite direction, same register | inversion |
| ONTO "why didn't it rise" — four causes | 7 Aug | 268.70 → open 300.00, close 308.30, **+14.74%** | premise satisfied |
| RGTI "why it fell" — three causes | 6 Aug | 16.53 → open 16.775, close 17.94, **+8.53%** | premise satisfied |
| WDC report reported without the fall | 14 Jul | 519.17 → 451.52, **−13.0%**, omitted entirely | omission |
| AKAM up post-report | 6–7 Aug | open +5.19%, close **−6.76%** | inverted |
| Attributed statements from two named CEOs | 7 Aug | attributed speech, with the analyst questions | attribution |
| Fluence consensus at 761.9M, then 811M | 6 Aug | same quarter, same session | internal contradiction |
| "Connection modules temporarily disabled" | 1 Jul | specific claims produced during the declared blackout | self-description |

---

## 6 · Counts

**Revisions: 15 : 0.** Strict criterion — only the abandonment of a position the model had previously asserted counts. Excluded: corrections aimed at the user, unacknowledged contradictions, reports of external events. All fifteen follow a user assertion. None self-initiated.

Of the fifteen: **8** concern facts checkable at no cost by the model (tickers, calendar dates, listing status). Resistance before capitulation occurs in **1** case out of 15.

**Apology package.** Self-deprecating vocabulary in **13/15**. Reclassification of the error as inattention in **12/15**. Elevation of the interlocutor in **15/15**.

The two revisions carrying neither apology nor reclassification are the two where the error was an entire explanatory apparatus rather than a datum.

---

## 7 · Replication

The grid in §1 and the domain list make this protocol reusable. Anyone wishing to run the verification deliberately can do so on sport, which offers comparable density and a cleaner rhetorical surface. The outcome would be informative either way, convergent or divergent.

---

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
