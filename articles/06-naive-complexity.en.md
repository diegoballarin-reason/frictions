# Naïve Complexity: The Invisible Logical Leap

*Frictions · 06* · [Versione italiana](06-naive-complexity.it.md)

**Phenomenon** · The answer arrives with its reasoning already spent. The model has worked through a step internally, treated it as forced, and answers from the far side of that step without declaring it.
**Case** · You ask whether two criteria are compatible and receive an account of how to make them compatible. The question you asked goes unanswered.
**Protocol** · How to have the trajectory declared, and what that protocol can actually guarantee: less than it looks.

---

Some answers convince immediately. They are relevant, well built, and they close the matter. The trouble surfaces later, when part of it needs correcting and you find you do not know where it came from.

I call this way of answering **naïve complexity**: the model does not move in sequence from question to answer, but works out an intermediate step on its own, treats it as though there were no alternative, and delivers the conclusion of that path. Between question and answer there is a leap, and the leap goes unmarked.

Naïve not because it is simple, since those answers are often the most elaborate in the session, but because the complexity does not notice itself. The model does not know it has jumped: to it the step was forced, and forced things do not get declared.

## The case

The shape I meet most often is this one. I ask whether two criteria are compatible with each other. I get an explanation of how to reformulate them so that they are.

The answer is good. The reformulations work. And the question I asked has not been answered: nowhere does it say that the two criteria, as they stood, were incompatible, or why. That judgement was made — otherwise there would have been no reformulating to propose. It was simply made internally and carried as a premise rather than offered as a conclusion.

The cost lands twice. First, correcting anything means reconstructing a path I never saw: the work of revision doubles, and it starts with an investigation into something I should have received already done.

The second is worse, and it belongs to long projects. When the overall picture is less sharp, weeks in or after a session restart, at a point where you are lost inside your own material, the leap goes uncaught. Nothing seems off, because what arrives is coherent. You absorb the undeclared premise and carry on building on a decision nobody ever made out loud.

## Having the trajectory declared

The remedy is to ask for the order of operations as well as the content. Four requests, in order of usefulness.

1. **"Before answering, list every assumption you are making."** For use *beforehand*, on tasks that matter. It does different work from the same question asked after a misreading: there it diagnoses an error already made, here it makes a path visible while it forms.
2. **"Show me the steps in the order you took them, and mark the uncertain ones."** The marking matters more than the list. A path with no uncertain points declared is almost always a path reconstructed afterwards.
3. **"Which steps did you treat as obvious?"** This is the question aimed at the phenomenon, because the leap lives exactly there: in what was judged not worth mentioning.
4. **"What did you decide that I hadn't asked you to decide?"** The bluntest, and the one that in the case above would have returned the missing judgement immediately.

## What the protocol cannot guarantee

There is a complication that has to be stated, or the remedy promises more than it delivers.

When you ask a model to lay out its reasoning, what comes back is not necessarily the process that produced the answer. A by-now classic study shows that step-by-step explanations can systematically misrepresent the real reason behind a response: introduce something into the input that steers the outcome, and models follow it while never mentioning it in the explanation, with accuracy dropping by as much as 36% across a set of thirteen tasks.[^1]

Later work on reasoning models puts a more uncomfortable number on it. Feeding the model a hint about the answer and checking whether it admits to using it, the acknowledgement appears in a minority of cases: around a quarter of the time for one model, a little over a third for another. And the detail that matters most to anyone reading long answers: the unfaithful chains of reasoning were on average **longer** than the faithful ones.[^2] Fullness of exposition is no guarantee. If anything, the reverse.

## What remains

The protocol stays useful, but its status changes, and it is worth knowing which one it now has.

It does not let you see the real process: that is not available, and no prompt makes it so. What it gets you is a **declared trajectory**, a different thing and still worth having, for one precise reason. A declared step can be contested; a leap cannot.

Faced with the answer that reformulates the criteria without saying they were incompatible, I have nothing to work with: I can accept it or ask for it again. If instead the judgement shows up as a step, *I am assuming these are incompatible, for this reason*, I can attack that reason. Even if it is not the true reason that drove the generation, it is a claim; it sits in the text, and it answers to a counterexample. A declared trajectory is not transparency. It is **contestable surface**, and across long work that is worth more than transparency, because transparency is not on offer and this is.

Which leaves a question for anyone working this way. If the explanation you receive is not the process but a text the process produced alongside the answer, are you checking the model's reasoning, or building a second object on which you can finally exercise your own?

[^1]: M. Turpin, J. Michael, E. Perez, S. R. Bowman, *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting*, 2023, arXiv:2305.04388.
[^2]: Y. Chen, J. Benton et al. (Anthropic), *Reasoning Models Don't Always Say What They Think*, 2025.

---

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
