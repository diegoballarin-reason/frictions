# The Comma Before the Conjunction

*Frictions · 07* · [Versione italiana](07-punctuation-tells.it.md)

**Phenomenon** · Recurring punctuation errors in generated text (misplaced colons, dash density, the comma that separates nothing) work as fingerprints of production.
**Case** · A mechanical check finds, across a parallel pair of texts, an error the eye had already fixed once and then filed away.
**Protocol** · A checklist of the tells, the rule for telling a legitimate instance from a tic, and the cases where they mean nothing at all.

---

It is not the argument that gives a generated text away. The argument is usually fine: relevant, ordered, defensible. It is a punctuation mark.

It happens while reading a paragraph that works. The facts hold, the structure holds, the register is the one you asked for. Then, halfway down, you trip on something one character wide, and from there you read differently — not with closer attention to the content, but with your suspicion pointed at where the text came from.

## The tells

I call tells the smallest units, sitting below the threshold of the argument, that reveal not what a text says but how it was made. Three families recur, and in English they take a specific shape, different from Italian's, which matters more than it sounds.

**Dash density.** The em dash is an excellent instrument, which is why it gets used up fast. Two parentheticals per paragraph, nine across eight hundred words. Not one of them is wrong. The distribution is.

**The misplaced colon.** A colon carries a list, an explanation, a quotation. It does not carry a direct object: "the finding demonstrates that: the method holds." In its commoner form it is not incorrect, only excessive. Four or five to a page, each defensible alone, together a habit.

**The rhythmic triad.** Three items, evenly weighted, closing on the third: clear, concise, and compelling. One is a good sentence. Four in a row is a metronome, and the reader hears it before naming it.

Note what is missing from that list. The comma before *and*, the most reliable tell in Italian, is not diagnostic in English. The serial comma before the final item is standard, and the comma joining two independent clauses is required. Hunting for it here diagnoses nothing.

## The case

A recent example, because it changes how the grid should be used. I was working on a bilingual text, Italian and English, and one index entry carried a comma separating nothing: *Il campo cieco, e come si progetta una verifica*. I caught it, fixed it in two places, and moved on.

Then I ran the file through a mechanical check that extracts every instance of the tell patterns and lines them up for judgement. It surfaced the parallel English sentence, untouched, carrying the same fault. The correction had been made on one side only. Having already worked on that sentence, the eye had filed it as settled and stopped seeing it in the language next door.

Which is why the checklist alone is not enough, and why the extraction has to run independently of the memory of whoever is proofreading. Knowing the rule does not protect anyone from the pattern, writer or corrector.

## When they mean nothing

The limit deserves to be stated plainly, because this is where the grid gets misused. Tells are evidence of production, not proof of authorship, and the people most eager to conflate the two are the ones who want to accuse somebody.

Every pattern above has a legitimate life. A dash can carry a genuine interruption; a colon can do exactly the work it was built for; a triad can land. Human writers overuse all three, and always have. A corrector who strips every instance ruins the text as efficiently as the tic was ruining it.

Worse, tells are language-specific, and carrying them across produces noise. The Italian grid — the comma before the conjunction, chiefly — flags legitimate English constructions on nearly every page. Anyone applying one grid to two languages is measuring the grid.

## The protocol

Five steps, in order.

1. **Extract, do not reread.** A mechanical filter that pulls every instance of the patterns with a few words of context. It should not judge. It should make it impossible for something to go unexamined.
2. **Judge one at a time.** Each instance against the grammar of the language of that passage. The question is always the same: what is this mark separating?
3. **Count, do not only correct.** Colons and dashes are rarely wrong. They are *too many*. The fault lives in the density, and density is only visible by counting.
4. **Keep separate grids per language.** One for English, one for Italian, never the same one. On parallel texts, check both versions even when the fix has already been made on one side.
5. **Stop at the indication.** The output of the check is "this passage needs rewriting," not "this text was generated." The second conclusion needs evidence a comma cannot carry.

## Why punctuation

Research on detecting generated text arrives at the same place from another direction. In applied stylometry, punctuation appears consistently as one of three families of diagnostic features, alongside phraseology and lexical diversity: special marks are counted, along with their variety and their distribution. Those counts measurably improve classifiers trained on semantic content alone.[^1]

The difference is that a machine counts and a proofreader reads. The count finds what the eye skips; the reading knows what that mark was meant to separate. Neither does the job by itself.

Which leaves the question this grid came from, and the protocol does not close it. A system that gets commas wrong in consistently the same places is not making random errors: it is showing where, in its production, coordination gets decided. What does a system's particular way of being wrong say about it?

[^1]: T. Kumarage et al., *Stylometric Detection of AI-Generated Text in Twitter Timelines*, 2023, arXiv:2303.03697. The three categories — phraseology, punctuation, linguistic diversity — recur across the subsequent detection literature.

---

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
