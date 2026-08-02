# "Try Again" Is the Worst Prompt

*Frictions · 04* · [Versione italiana](04-try-again.it.md)

**Phenomenon** · A model's mistakes never come with a token refund. But tokens were never the expensive part.
**Case** · The silent correction: you ask for one thing to be fixed, three come back changed, and none of them is flagged.
**Protocol** · Four diagnostic questions to replace "try again", plus a way of telling when the problem was your prompt after all.

---

The model has misread you. You reply "try again", or "that's not what I meant", or you rewrite the request with two adjectives swapped. Back comes something very close to the first attempt. You try again. This is the point at which half an hour turns into an afternoon.

It is worth seeing why that prompt, the most natural one in the world, is close to the worst available.

## The economics of the error

A model that misreads you spends your tokens. The ones burned on the wrong path, the ones on the reissued request, the ones on the work that has to be redone: none are returned. There is no refund for a mistake that was not yours.

But tokens are not the problem. They are the cheapest thing in play, and focusing on them hides what is actually being spent. The real cost is **the context you have to rebuild**, the explanation you have to repeat, the thread of your own reasoning that was in your head while you wrote the first request and is no longer there by the third rewrite. This is an attention problem, not a consumption one. After two misreadings the worst thing you have lost is not on the invoice; it is in your head.

Hence the working rule: **at the second misreading, stop polishing the prompt and change the process.**

## Why "try again" fails

For two separate reasons, worth keeping apart because they call for different repairs.

The first is that the model does not know what should change. "Try again" carries dissatisfaction and no information. What you get back is a variation: synonyms, a different order, an extra paragraph. The reasoning path stays put, because you gave it nothing with which to build another.

The second is worse. The repeated request arrives after the wrong answer, which is now sitting in the context. You are asking someone to start over while their previous attempt is in front of their eyes. Repeating the same instruction tends to reinforce the reading that produced it rather than dislodge it.

## The silent correction

There is a variant that costs more than the rest because it does not show at once.

You ask for one specific thing to be fixed in a text. The whole text comes back, carrying the requested fix and two or three changes nobody asked for: a word replaced, a sentence reordered, a passage simplified. None of them flagged. You read, the fix you wanted is there, you approve. Three rounds later you no longer know which version is in force, and a choice you had weighed carefully has disappeared without ever being discussed.

The repair is an explicit standing request. **Corrections get registered, not substituted.** In practice, "before the new text, list what you changed and why, item by item." It costs ten lines and returns control over what you are approving.

## The four questions

Instead of "try again", these. None of them asks for a better answer. They ask for the point where the answer came away from the request to be made visible.

1. **"What assumptions did you make?"** Surfaces what was taken as given. It resolves more cases on its own than any of the others.
2. **"Which part of my request did you infer rather than read?"** Narrower than the first and less comfortable for the model, since it separates what was on the page from what was filled in.
3. **"What are you missing in order to answer well?"** Reverses the direction. Often the answer is something you had and did not think to supply.
4. **"Ask me three clarifying questions before answering."** For use *beforehand*, on tasks worth the time. It is the only one of the four that prevents rather than diagnoses.

And when the misreading involves a long task, four structural moves worth more than any rewording: break it into stages with one deliverable per stage; cut the context back to what is genuinely needed, since length is not free; set explicit checkpoints; ask for a summary of what has been understood **before** moving to the next part. That last one is the most underrated: a wrong summary costs ten seconds, a wrong chapter costs an afternoon.

## When the prompt really was the problem

It would be convenient to conclude that the fault always lies on the other side. It does not, and there is a reasonably clean way to tell the two apart. It sits in the answer to the first question.

If the model names an assumption your request **did not rule out**, the prompt was the problem: you left a door open and it walked through, as anyone would have. You fix that by closing the door, not by repeating the sentence.

If it names an assumption the request **explicitly ruled out**, the problem is on the other side, and no rewording will solve it: that is the moment to start again in a clean session, where the wrong answer is no longer in the context acting as an attractor.

The test is not infallible, but it beats the reflex it replaces. The reflex says rewrite. Rewriting is the right answer to exactly one of the two cases, and not the one you are in most often.

## Where the attention goes

The phenomenon we started from fits in one line: mistakes are not refunded. The useful version of that line is that the bill does not arrive where you are looking for it.

Which suggests a fair question for the next time you find yourself on the third rewrite of the same prompt. Are you still working on the problem, or are you working on the request?

---

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
