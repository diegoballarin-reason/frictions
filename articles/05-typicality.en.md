# The Collapse Toward the Typical

*Frictions · 05 — a field note* · [Versione italiana](05-typicality.it.md)

**Phenomenon** · Ask for five alternatives and get five versions of one thing. The documented cause is not algorithmic. It sits in the preference data.
**Finding** · The repertoire is shared across models. And underneath the variety of content lies one that does not move: the rhetorical gesture.
**Limit** · A single case, three conditions, four models, no control for ordering. What follows are observations, not measurements.

---

This is a field note, not a study. N=1. One user, three days, three conditions across four models, with the number of runs available to someone who has no laboratory. The counts are mine, done by hand on the texts in front of me. Anyone extracting a statistic from them would be making an error I am declaring in advance.

I am writing it anyway, because the material showed something I was not looking for, and because how I found it is itself part of the finding.

## What I knew without knowing I knew it

For years, asking a language model for alternatives has got me alternatives that are not. Five titles that are one title combed five ways. I never had a name for it: I lived with it, and intervened.

The intervention I use is to supply examples that force a different trajectory. It works, and how it works is the interesting part. The pattern does not disappear; it relocates. It goes on repeating, but along the new instructions. There is a second move as well, more laborious, which is to put forward your own list before asking for theirs. I keep it secondary for a reason bound up with why anyone asks in the first place. In difficult work you ask *precisely because* the task is hard, and there is no guarantee at all that the person asking already has the command to advance alternatives of their own without getting stuck.

I found the cause afterwards. In recent work on the phenomenon, which goes by the name of mode collapse, the explanation is not algorithmic but sits in the **preference data**. Human annotators systematically favour familiar text, through a well-established cognitive effect, and that preference transfers to the model. It acts as a tiebreaker. When many responses are equivalent in real usefulness, which is nearly always in writing, typicality decides which one comes out. The corollary is the part that struck me. Even with a perfect reward model and perfect optimisation, the collapse would still occur, because it is in the data.[^1]

Knowing this changed nothing about what I do. It changed the order of magnitude I assigned to it.

## What I tried

Three conditions, on one task, namely asking for openings to a popular-science article about sleep.

The first is the bare request. The second is the technique proposed in that same work, and asks for responses each carrying a probability, sampled from the tails. The third is a sentence of my own, improvised: asking for openings that are *highly exotic and improbable given your own conception of the subject involved*.

The last two are not commensurable, and not through some fixable flaw in the design. The second is an engineered prompt, with block structure, numeric constraint and threshold, exploiting a formal property. The third is a sentence in ordinary Italian that asks the model to consult its own representation of the domain and point at its margins. Pairing them would mean asking the second to become the first, which is to say to give up what defines it. What follows does not establish which formulation is better. It records that two tools within reach of the same person yield different results.

A third task on a narrow axis (titles for a specific text) was run but is not reported, because the material belongs to unpublished work. Where it matters, I describe its shape instead.

## First finding: the repertoire does not belong to the model

Lining up every opening produced, the first visible thing has nothing to do with conditions. It has to do with models.

The third of life spent asleep. The three-in-the-morning scene with the calculation of hours remaining. Randy Gardner and his eleven days. First sleep and second sleep before electric light. The predator paradox. The reversal by which sleep is not a pause but maintenance. This repertoire turns up across four models from three different producers, in different configurations, under all three conditions.

Theoretically this is unsurprising: if the cause lies in preference data, and preference data resemble each other across labs, a shared pool is what you would predict. Practically it is another matter. It means that switching model, the instinctive move when answers feel flat, does not switch the pool. And it means the wording of a request does not steer it in advance, since none of the three conditions kept the repertoire from surfacing.

## Second finding: what does not move

This is where the material said something neither party involved was looking for.

I mixed fifteen openings drawn from all three conditions, stripped the labels, and asked models in clean sessions to group them by semantic axis. I wanted a count of thematic families. One classifier counted them and then added, unprompted, that the count was the least important thing. Grouped by theme the openings looked like five different things, grouped by **gesture** they were nearly one. Twelve of fifteen closed the same way: concrete hook, then a sententious lift in the final line, the thesis sentence that redeems the anecdote. Its observation: read in sequence, a reader would not perceive five axes, but the same mechanism fifteen times.

I checked where those closing lines came from. All three conditions, indifferently.

Two other classifiers, in separate sessions and on partly different corpora, reached the same place on their own. According to the first, the fifteen openings are not fifteen ideas but roughly four ideas multiplied by a repertoire of devices. According to the other, the set offers about half the variety its length suggests.

Three independent judges, none of whom knew which item came from which condition, located the same gap between apparent and actual variety, and located it where metrics of semantic diversity, by construction, do not look.

Hence the hypothesis I am now working with. The collapse has at least two levels. One of content, which prompting techniques do shift, with efficacy varying by formulation and by model. One of form, which in my runs did not shift under any of the three. I have no grounds for saying whether it is irreducible or simply needs a different lever, and I am wary of deducing either from the other.

## A hypothesis I have not tested

The two tools produced different quantities of off-repertoire material. In my counts, which are hand counts on a small corpus and should be read as such, the probability technique brought into production two items that had previously only been named, while the plain-Italian sentence produced five, further from the pool: a criminal case of a killing committed while asleep, a nineteenth-century trade that consisted of waking factory workers, a rare genetic illness that abolishes the capacity to sleep, a Japanese social practice of sleeping in public, and a bedding site seventy-seven thousand years old.

But the same sentence, on a lighter-class model, produced something else entirely: extravagant metaphors, the ocean trench and the report to an intergalactic council and quantum superposition, applied to the usual content. Exotic in form, not in substance.

The most economical hypothesis I have is that the sentence does not ask for diversity at all: it asks the model to point at the margins of its own map of the domain. Where the map is dense it returns rare facts. Where it is thin, the only available atypicality is rhetorical. If that held, it would not be a tool for obtaining variety. It would be a tool for measuring depth.

I have not tested it. Doing so would need a different design, more models and more domains, and some way of separating a model's class from its generation, which in my runs remain confounded.

## Who is running the experiment

One last observation, which in this genre is a datum rather than an anecdote.

Across these runs I recorded, between myself and the model I was working with, a series of errors all concerning the same thing, the frame. The first test was run with a paraphrase in place of the canonical formulation, and neither of us had gone to check the canonical formulation beforehand. An ambiguous result was read toward confirmation while a strong outcome was wanted, and toward refutation once that reading had been challenged. My own position was summarised three times in a sharper form than I had given it, with the ranking of my two countermeasures inverted at least once.

Each of those errors was corrected once it was named. The general frame, the idea that these runs existed to adjudicate a contest between two methods, survived every correction, and dissolved only when somebody asked to look at the conversation instead of the data. I have no remedy to offer. I have the observation that the hardest thing to correct was in none of the answers. It was in the question we kept putting to each other.

## What stays open

The question I keep in front of me, and cannot answer, concerns what comes next. A wider fan of openings is not an approach to anything. It is more options, not more direction. The classifier that counted the families said it better than I would, looking at fifteen openings without knowing their provenance. Only three carried a thesis pointed enough to commit the article that followed to a direction. The other twelve promised *an article about sleep*, not *that* article.

If a technique yields twelve generic promises and three commitments, the question worth asking of it is not how far it widens the fan. It is what happens afterwards, and whether the afterwards depends on the technique or on whoever is using it.

[^1]: J. Zhang et al., *Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity*, arXiv:2510.01171 (v1 October 2025, v4 July 2026). The models the work runs its experiments on belong to generations earlier than those used here.

---

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
