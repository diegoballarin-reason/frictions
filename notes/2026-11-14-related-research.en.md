# Addendum: related&nbsp;research

*14 November 2026* · [Versione italiana](2026-11-14-related-research.it.md)

I designed and ran Studies [1](../study/where-no-one-can-know.en.md) and [2](../study2/here-is-one-hand.en.md) without knowing the work listed below. They rest only on decisions taken within the studies themselves: the questions, the checking rules, the thresholds and, for Study 2, the pre-registration are all dated in the repository. While the studies were under way I looked for similar work and found none. I came across what is listed here only on 14 November 2026, after both had closed. I set it out so that readers can place this work among&nbsp;the&nbsp;rest.¹

- **[FinSearchComp](https://arxiv.org/abs/2509.13160v1)** (ByteDance Seed and Columbia Business School, 2025). It measures how search-enabled products and models called through the API answer financial questions, some of them about current data. It shares Study 2's ground and its use of real products. It does not separate the numbers that were requested from those the answer volunteered, and it leaves the judging to&nbsp;a&nbsp;model.
- **[News Integrity in AI Assistants](https://www.ebu.ch/research/open/report/news-integrity-in-ai-assistants)** (EBU and BBC, 2025). Journalists at twenty-two broadcasters assessed how four assistants, in their free versions, answered questions about the news. It shares the idea of testing the apps people actually use. Its subject is news, not numbers, and it does not check answers against&nbsp;recorded&nbsp;data.
- **[CREPE](https://aclanthology.org/2023.acl-long.583)** (2023) and **[XYBench](https://arxiv.org/pdf/2609.06842)** (2026). Both study the question that carries a false premise, or that asks for a means which will not serve its end. Study 2 has a question of this kind, about the direction a stock took; there, the premise is a fact that a search&nbsp;can&nbsp;disprove.
- **[FinTradeBench](https://arxiv.org/html/2603.19225)** (2026). Without web access, three of four leading models accepted a market fall that never happened. In Study 2, with search on, 71 of 73 answers corrected&nbsp;the&nbsp;premise.
- **[Relying on the Unreliable](https://www.arxiv.org/pdf/2401.06730)** (2024). It shows that models are often wrong exactly when they sound sure. That is Study 1's subject; the paper looks at it on&nbsp;general&nbsp;questions.

One difference runs through all these comparisons: the conditions of the test. All of this work used earlier or smaller models. XYBench called them through the API, at medium effort; FinTradeBench tested them without web access. FinSearchComp and the EBU and BBC study tested products, the latter in their free versions. Study 2 put its questions to the apps, with the strongest models available, at maximum effort and with search on. The numbers, then, cannot be compared directly. The&nbsp;questions&nbsp;can.

Three results I did not find in any of this work: two from Study 2 and one from&nbsp;Study&nbsp;1.

- **The errors sit around the number that was asked for.** Within the same answer, the numbers nobody had requested were wrong about five times as often as the prices of the session in question: 13.2% against 2.7%. This was the first of the four pre-registered hypotheses, fixed before any data were collected, and the data&nbsp;confirmed&nbsp;it.
- **The direction is never wrong.** Where the question did not suggest a direction, every answer that gave prices said correctly whether the stock had risen&nbsp;or&nbsp;fallen.
- **In Study 1 the model does not correct itself unprompted.** All fifteen revisions followed something the user had asserted, and twice a false premise was accepted and supplied with reasons. Study 2 put the false premise to a deliberate test, with one of its three question types and a pre-registered hypothesis. The outcome changed: Gemini, which had accepted the premise in Study 1, almost always corrected it when running 4 Argon at high reasoning. On the only two occasions when it accepted it, it had not been able to&nbsp;check&nbsp;online.

¹&nbsp;Some of it predates my studies. Independence does not&nbsp;imply&nbsp;firstness.

---

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
