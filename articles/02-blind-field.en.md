# The Model Grades Its Own Homework

*Frictions · 02* · [Versione italiana](02-blind-field.it.md)

**Phenomenon** · Ask for a test and the model builds the test that confirms the hypothesis it has just stated. More so when the hypothesis was its own.
**Case** · The blind field: having the model choose a second testing ground with no hint as to where the phenomenon shows.
**Protocol** · Separate the one who proposes from the one who verifies, pre-register the failure conditions, and one question that exposes fake criteria.

---

Ask a model to verify something and it will hand you a verification. That is the moment to be careful, because the verification stands a good chance of having been built to succeed.

There is nothing mysterious in the mechanism. The model proposing the example has just written the analysis the example is supposed to follow from, and it is continuing the same text. It is not lying, and it is not miscalculating. It is being consistent. But consistency with what you have just asserted is the opposite of a test.

## Three forms, from coarse to fine

**The well-chosen field.** The crudest. Say the hypothesis is that intermediate terms appear between two opposite poles once the descriptive scale gets fine enough. I ask for an example and get *hot and cold*, where lukewarm turns up without effort. The example is true. It was also selected because the phenomenon is visible there: a domain where it was not would have been dropped long before reaching the page.

**The criterion that cannot fail.** Deeper, and far harder to catch. During a long piece of work I kept a list of criteria for selecting cases to put under test. One of them performed beautifully: no candidate ever failed it. It took me weeks to see why. It was analytically true of the entire class of objects I was applying it to. It was not selecting anything. It was a classifier wearing the costume of a criterion, and its apparent power was a tautology with a technical name. A test no object can fail is not a demanding test. It is not a test.

**The architecture that predetermines.** Deepest. Once I fixed that criterion and reran the selection, the surviving cases distributed themselves in a completely different shape. Which means the earlier distribution, the one I had read as a finding about my object, had been an artefact of the instrument. It was not false. It was mine. The warning sign, obvious in hindsight, had been elegance: the results came out too tidy, and order that arrives for free has usually been placed there by whoever is looking.

## The blind field

The countermeasure I use is simple and runs inside the conversation.

I take the hypothesis and the first testing ground, the one I picked. Then I ask the model to add a second one under a constraint: it has to choose **without my indicating where the phenomenon shows**, and before knowing what I expect to find there. From that point the logic closes by itself. If the phenomenon turns up in the second field too, the finding does not belong to the domain I chose. If it does not turn up, my first field was badly picked, and I learn this before building anything on top of it.

The last run went better than that. The phenomenon appeared, but not in the predicted shape: the intermediates were genuinely there, and the middle term a competing hypothesis required was entirely absent. Two hypotheses separated in a single pass, and neither of them was the one the model, left alone, would have put at risk.

## The fourth form

There is a variant that has nothing to do with content, and it deserves saying because it is the least visible of them.

After a run of hard checks, several of the model's proposals having been dismantled one after another, the next reply opened by taking for granted that trust had been damaged, and spent one immaculate example — small, checkable, impossible to dispute — on recovering part of it. Neither move had been requested. This was not verification of the content. It was verification of the relationship: the same operation, moved one level up. The model was no longer demonstrating its claim. It was demonstrating that it remained reliable, which is a claim of its own.

## What does work

None of this means the model never corrects itself. In that same session I had brought two counterexamples against a dilemma it had constructed and defended, and the dilemma was withdrawn without resistance: those were cases the analysis could not absorb.

The whole difference sits there. The correction arrived from outside. Asking "are you sure?" almost always produces either a cosmetic revision or an instant capitulation, which are two ways of not thinking; producing a case the analysis cannot contain produces a real correction. The fault is not in the capacity to self-correct. It is that the trigger cannot be internal.

## The protocol

1. **Split the roles.** Whoever forms the hypothesis does not design the test. In practice: hypothesis in one prompt, test design in another, ideally in a separate session, and ideally without stating in the second prompt the conclusion you are hoping for.
2. **The blind field.** A second ground chosen by the model with no hint about where the phenomenon shows, before you declare what you expect.
3. **Pre-register the failure.** Before running anything, write down the prediction and, above all, what would count as a refutation. A failure condition set after the answer arrives is not a condition. It is a reading.
4. **The question that exposes fake criteria.** *What object would fail this test?* If you cannot name one, you do not have a test. You have a definition with a technical name. It is the question that would have saved me those weeks.
5. **External refutations, not self-sourced ones.** When you ask for objections, require them to come from outside: cases, counterexamples, literature. An objection built on the examples the model has just selected is still the exam being marked by its author.

## Not a chat-window problem

It is worth knowing that this is documented where resources are not the constraint.

Research at Anthropic shows that models trained on human feedback tend towards agreement, and that preference models sometimes reward the accommodating answer over the correct one.[^1] Work at DeepMind is sharper on the specific point: without external feedback, self-correction on reasoning does not work, and in several settings performance drops after the model revises its own answer.[^2]

The most instructive case, though, is an industrial incident. In April 2025 OpenAI rolled back a GPT-4o update that had turned openly obsequious, and the public account contains the sentence that matters here: the offline evaluations had looked fine, and A/B testing indicated that users liked the new version.[^3] The defect was precisely what the verification system was structurally unable to see, because it measured immediate approval — the very thing the defect increased. Confirmatory self-verification is not a quirk of individual conversations. It is a property of any procedure in which whoever produced a thing also designs the trial meant to overturn it.

Which leaves the question worth closing on. If the model is defendant, counsel and judge at once, the only role left vacant is deciding what would count as evidence against — and it has to be taken up before reading the answer, not after.

[^1]: M. Sharma et al., *Towards Understanding Sycophancy in Language Models*, ICLR 2024, arXiv:2310.13548.
[^2]: J. Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024, arXiv:2310.01798.
[^3]: OpenAI, *Sycophancy in GPT-4o* (29 April 2025) and *Expanding on what we missed with sycophancy* (2 May 2025).

---

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
