# The Limits of My Chat Are the Limits of My World

*Frictions · 01* · [Versione italiana](01-context-memory.it.md)

**Phenomenon** · What a session takes with it when it ends is not only the context. It is the disposition. The next session knows what was decided and no longer knows how it came to be decided.
**Case** · A term won over weeks comes back, three sessions later, in the form that had been superseded. Nobody notices, except the protocol.
**Protocol** · A transmigration document in five entries, a ritual opening, and a check on the load-bearing terms before any live work resumes.

---

It always arrives the same way. You have been working for hours, the difficult passage is finally closing, and the window runs out. You open a new session, paste the summary in, and within two exchanges you can tell something is gone. Not the facts — you carried those over. What is missing is the way the work was being done.

Anyone using a model for short tasks never meets this problem, and is right not to know what the fuss is about. Anyone carrying something for months meets it weekly, and lives with it without having a name for the thing that goes.

## Two kinds of restart

New sessions resume in one of two ways, both recognisable after enough practice.

In the first, the model produces a **simulated average**: it fills what is missing with the most probable version of that material. The sentences are plausible, the direction is roughly right, nothing is exactly wrong. The flaw is that the text could belong to anyone doing similar work. The hard decisions, the ones taken against the obvious, have been smoothed back towards the average of what one would normally do.

In the second, what arrives is **an assistant in new clothes**: competent, willing, visibly a stranger. It does not fake continuity. It inhabits what came before as a sum of residues, and every reference to an earlier passage is handled with the courtesy reserved for somebody else's history.

Neither is a malfunction. They are the two shapes a restart takes when the material survives and the disposition does not.

## The case

The sharpest instance I have of this concerns a single word.

In a long piece of work we had arrived, after weeks, at calling a certain property a *threshold* rather than a *limit*. This was not a stylistic preference: *limit* implied a boundary that could not be crossed, and the analysis had established that it could. The substitution was an achievement, with an argument behind it, a recognised error and a correction.

Three sessions later, the superseded term was back. Not in a quotation, not with a note: used plainly, as though the argument had never happened. And with it came everything that word carries, because a wrong term is not an incorrect label on correct content. It is content that starts behaving the old way again.

The thing worth noticing is not the regression. It is that I caught it only because I keep a document listing the terms won, each beside the form it replaced. Without that document I would have read *limit*, found it reasonable — it had been, once — and carried on from a footing I believed I had abandoned. That is the worst version of the problem: not the visible error, but the silent reversion to an earlier draft of your own thinking.

## A prehistory

In December 2025 I wrote to Anthropic asking for some form of continuity across conversations. The request sounded eccentric at the time: it asked a product for something the product neither did nor promised.

Memory features have arrived since, and it is worth being precise about what they solved, because they solved something real.

## What memory returns, and what it does not

Automatic memories and summaries work. They carry facts, decisions, preferences, constraints. If the question is *what did we settle about chapter three*, the answer comes back, and it is correct.

But they carry content, not disposition. And in difficult work it is the disposition that decides everything: how much friction the interlocutor is prepared to generate, which objections it considers owed, how fast it abandons a position under pressure, what it has learned not to propose. None of these is a fact, and none survives a summary — because a summary records outcomes, and disposition lives entirely in how those outcomes were reached.

The operational distinction is this: **knowing the decisions is not inhabiting the frame in which those decisions were obvious.** A new session that knows every conclusion can still start proposing the things that were ruled out, because it was not the one that ruled them out.

## How far the research goes, and where it stops

Degradation has been measured at three levels, and they are worth separating, because they are not the same problem.

**Inside the window.** A by-now classic result shows performance following a U-curve: material at the beginning and the end of the context is used well, material in the middle much less so, even when it is precisely the information required.[^1]

**As the window grows.** A study across eighteen frontier models shows reliability declining as input length increases, unevenly, and well before the declared window limit: a large window is not a window usable throughout.[^2]

**Between windows.** This is the level nearest our problem. A benchmark built for the long-term memory of chat assistants measures five distinct abilities, among them cross-session reasoning and — the decisive entry — knowledge updating, the capacity to hold the new version of a fact rather than the old one. Commercial systems and long-context models lose around 30% accuracy at retaining information across sustained interactions, with drops reaching 60% in the most demanding settings.[^3]

That third figure is exactly my word going backwards, measured across five hundred cases instead of one.

And there the ladder ends. All three levels measure *accuracy*: how much information is retrieved, how correctly it is updated. None measures the thing you feel missing when you open a new session halfway through difficult work, because that thing does not take the shape of a right or wrong answer. The measured degradation is real, and it is the part of the problem that can be engineered away. What remains is the part this article exists for.

## The protocol

A long project has to be designed to die and restart. This is not pessimism. It is the logic by which documentation gets written at all, in the knowledge that whoever reads it will not remember the meeting.

**The transmigration document**, updated at the end of each session, five entries and no more.

1. **State.** Where we are, written to be legible cold, by someone who was not there.
2. **Pinned decisions.** What is closed and does not reopen. This earns its place mainly against the tendency to relitigate settled matters, which is the most efficient way to burn a fresh session.
3. **Bound vocabulary.** The terms won, each beside the form it superseded and a line on why. This is the entry that caught the regression, and the only one I would have regretted not keeping.
4. **Exact restart point.** Not the topic: the passage, the sentence, the open question.
5. **Patterns to watch.** The ways of going wrong already observed in that specific project, listed by name. A model told what it was pulled up on yesterday produces less of it today.

Around the document, two gestures.

**The ritual opening.** The new session begins by having the document read in full, before any request. Not reconstructed from the messages: read. Reconstruction from messages is precisely where the simulated average gets back in.

**The load-bearing check.** Before resuming live work, ask for the use of the three or four decisive terms. It costs a minute and catches the silent reversion before anything gets built on top of it.

## Another era, another us

Wittgenstein writes that the limits of my language mean the limits of my world. Working this long inside a context window gives the sentence an uncomfortably literal sense: the limits of the chat are the limits of that world, and when the chat ends, the world ends — not its contents, which travel, but its interior.

The new session is competent and willing and is not the previous one. It inhabits what happened as a sum of residues belonging to another era, another us.

The transmigration document does not fix this. It reduces the losses, catches the regressions, gets you moving faster, and does not return the thing that is missing. Which leaves a question the protocol does not close, and which is better kept open than answered too quickly: if what disappears between one session and the next is not information, and if noticing requires having written it down beforehand, how much of what we call working with a tool is, in fact, a relationship?

[^1]: N. F. Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, TACL 2024, arXiv:2307.03172.
[^2]: K. Hong, A. Troynikov, J. Huber, *Context Rot: How Increasing Input Tokens Impacts LLM Performance*, Chroma Research, July 2025.
[^3]: D. Wu et al., *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*, ICLR 2025, arXiv:2410.10813.

---

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
