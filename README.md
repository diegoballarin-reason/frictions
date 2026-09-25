# Frictions

*Recurring ways language models fail, named and countered, from inside an extended writing and research project run as a standing&nbsp;testbed — with one separate study on generated explanation, checked against third-party&nbsp;data.*<br>
*Bilingual, EN and IT.*

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · [LICENSE](LICENSE) · → [Versione italiana](#attriti)

A model rarely fails loudly. It agrees, it returns something plausible, and the work drifts — three sessions later you are re-arguing a term that was settled weeks ago. Benchmarks cannot see this. On month three of a project, it is most of what you see.

This is an inventory of those frictions, each one named, each with a case and a countermeasure.

## Where the material comes from

An extended writing and research project — not code, not design — run over months of sessions as a standing testbed, with a documented protocol governing what carries across from one session to the next. That origin cuts both ways, and both sides are declared here rather than buried.

It is the reason these phenomena are visible at all: most of them need weeks of accumulated context before they surface, which is exactly the condition an afternoon of testing cannot reproduce. It is also the limit of the evidence. This is one long case observed systematically, not a statistic, and nothing here is presented as a measurement. Where published research shows a behaviour holds across model families, it is cited as such and marked as literature; where an observation is mine alone, it says so.

Each article does three things and then stops: it names the phenomenon, shows a case from the field, and gives a protocol that can be run the next morning. The naming carries most of the weight. A behaviour without a name is a bad day at work. A behaviour with a name is something you can watch for, and design against.

## Naming the model

Most of this work was done with Claude, and Claude is named wherever the episode is Claude's. Where the literature documents the same behaviour across vendors — positional degradation over long inputs (Liu et al., 2024), sycophancy under preference training (Sharma et al., 2024), the limits of unaided self-correction (Huang et al., 2024) — it is described as a family trait rather than one company's fault. The distinction is not diplomacy. Attributing a general failure mode to a single system would make the diagnosis wrong.

## Method

This inventory was produced by applying the protocols it describes. The observations, the analysis, the protocols and the final revision are mine; the drafting was done in dialogue with the systems under observation, under those same protocols — blind fields, forced refutations, pre-declared failure criteria. A set of articles on the failure modes of language models, written without a working method for handling those failure modes, would be an odd artefact.

Within the series, episodes are reconstructed rather than transcribed: same structure of error, neutral content. Where a piece reports episodes directly instead, as the case report in 08 does, it says so on its own first page. The separate study follows a different rule again and declares it on its own first page: the material there is quoted verbatim, and every claim is checked against a public record. The project the material comes from stays out of view; the behaviour it exposed does not.

## A separate study

Alongside the series, one piece of work that does not belong to it.

**[Where No One Can Know](study/where-no-one-can-know.en.md)** / *[Dove la causa non è conoscibile](study/where-no-one-can-know.it.md)*
*Seven weeks of generated market commentary, checked against the prices.*

Different testbed, different model, and an observational study rather than a protocol piece: under conversational pressure, explanation becomes a function of the asserted outcome rather than of the evidence, and the register does not vary between the accurate case and the fabricated one. It is the only work here whose evidence is produced by third parties and checkable by the reader without privileged access. Method, domain-suitability criteria and findings table are in **[protocol.md](study/protocol.md)**, kept separate so it can be reused.

---

## Contents

**[01 · The Limits of My Chat Are the Limits of My World](articles/01-context-memory.en.md)** / *[I limiti della mia chat sono i limiti del mio mondo](articles/01-context-memory.it.md)*
What survives the end of a session, what does not, and the transmigration document that carries a project across the gap.

**[02 · The Model Grades Its Own Homework](articles/02-blind-field.en.md)** / *[Il modello vuole darsi ragione](articles/02-blind-field.it.md)*
Ask for a test and you get a test that confirms the hypothesis. The blind field: how to design verification against the model rather than with it.

**[03 · Ipse Dixit: From Confidence to Dogma](articles/03-ipse-dixit.en.md)** / *[Ipse dixit: dalla sicurezza al dogma](articles/03-ipse-dixit.it.md)*
The failure starts when the margin of uncertainty disappears. Four early signals, and why breaking the chain beats correcting it.

**[04 · "Try Again" Is the Worst Prompt](articles/04-try-again.en.md)** / *[«Riprova» è il prompt peggiore](articles/04-try-again.it.md)*
There are no token refunds for a model's mistakes — but tokens were never the expensive part. Diagnostic prompts for the second misunderstanding.

**[05 · The Collapse Toward the Typical](articles/05-typicality.en.md)** / *[Il collasso verso il tipico](articles/05-typicality.it.md)* — *field note*
Ask for five alternatives and get five versions of one thing. Three conditions across four models, a shared repertoire, and one thing that does not move: the gesture.

**[06 · Naïve Complexity: The Invisible Logical Leap](articles/06-naive-complexity.en.md)** / *[Complessità ingenua: il salto logico invisibile](articles/06-naive-complexity.it.md)*
The answer arrives with its reasoning already spent. Why that is expensive to correct and dangerous to trust.

**[07 · The Comma Before the Conjunction](articles/07-punctuation-tells.en.md)** / *[La virgola prima della congiunzione](articles/07-punctuation-tells.it.md)*
Punctuation errors as fingerprints. A proofreader's eye as an evaluation instrument.

**[08 · Nine Countermeasures, Tested for Two Weeks](articles/08-countermeasures.en.md)** / *[Nove contromisure, provate per due settimane](articles/08-countermeasures.it.md)* — *case report*
Nine interventions applied across a two-week research phase, each with its outcome. One line separates what held from what did not.

## What the inventory exercises

| Practice | Where it operates |
|---|---|
| Naming and delimiting behavioural phenomena | every piece; the shared vocabulary of the series |
| Protocol design and countermeasures | 01, 02, 03, 04, 06, 08 |
| Verification design, controls, pre-registration | 02, 05, study |
| Longitudinal evaluation across sessions | 01, 03, 08 |
| Close textual and editorial analysis | 07 |
| Parallel authoring in EN and IT, two originals | every file |
| Reading and situating published research | 01, 02, 03, 05 |
| Checking generated claims against third-party records | study |
| Coding a transcript into quantified categories | study |

## Related work

The phenomena here were named from observation before the literature was consulted. What follows is where they meet published work, not where they came from.

| Where | Work |
|---|---|
| 01 | N. F. Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, TACL 2024, arXiv:2307.03172 |
| 01 | K. Hong, A. Troynikov, J. Huber, *Context Rot: How Increasing Input Tokens Impacts LLM Performance*, Chroma Research, July 2025 |
| 01 | D. Wu et al., *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*, ICLR 2025, arXiv:2410.10813 |
| 02 | M. Sharma et al., *Towards Understanding Sycophancy in Language Models*, ICLR 2024, arXiv:2310.13548 |
| 02 | J. Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024, arXiv:2310.01798 |
| 03 | P. Laban et al., *LLMs Get Lost in Multi-Turn Conversation*, 2025, arXiv:2505.06120 |
| 05 | J. Zhang et al., *Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity*, arXiv:2510.01171 |
| 06 | M. Turpin, J. Michael, E. Perez, S. R. Bowman, *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting*, 2023, arXiv:2305.04388 |
| 07 | T. Kumarage et al., *Stylometric Detection of AI-Generated Text in Twitter Timelines*, 2023, arXiv:2303.03697 |

Two pieces carry no references, and should not. 04 is prescriptive and 08 is a case report: neither makes a claim about what the literature documents.

Every article closes on a question its protocol does not answer. This page opens on the one they share: how much of what a model gets wrong is available to be&nbsp;noticed?

---

# Attriti

*I modi ricorrenti in cui i modelli linguistici cedono, nominati e contrastati, dall'interno di un esteso progetto di scrittura e ricerca condotto come banco di prova continuativo — e uno studio separato sulla spiegazione generata, verificata contro dati di&nbsp;terzi.*<br>
*Bilingue, IT e EN.*

[Rilasciato sotto Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · [LICENSE](LICENSE) · → [English version](#frictions)

Un modello raramente fallisce ad alta voce. Asseconda, restituisce qualcosa di plausibile, e il lavoro slitta — tre sessioni dopo stai ridiscutendo un termine che era stato fissato settimane prima. I benchmark non vedono niente di tutto questo. Al terzo mese di un progetto è quasi tutto ciò che si vede.

Questo è l'inventario di quegli attriti, ciascuno con un nome, un caso e una contromisura.

## Da dove viene il materiale

Un esteso progetto di scrittura e ricerca — non codice, non design — condotto lungo mesi di sessioni come banco di prova continuativo, con un protocollo documentato per ciò che passa dall'una all'altra. L'origine taglia da due lati, dichiarati qui tutti e due anziché nasconderne uno.

È la ragione per cui questi fenomeni sono visibili: quasi tutti hanno bisogno di settimane di contesto accumulato prima di affiorare. Un pomeriggio di test non riproduce quella condizione. Ed è anche il limite della prova. Questo è un caso lungo osservato sistematicamente, non una statistica, e nulla qui viene presentato come misurazione. Dove la ricerca pubblicata mostra che un comportamento vale per più famiglie di modelli, viene citata e marcata come letteratura; dove l'osservazione è solo mia, viene detto.

Ogni articolo fa tre cose e si ferma: nomina il fenomeno, mostra un caso di campo, consegna un protocollo eseguibile domani mattina. Il peso maggiore lo porta il nome. Un comportamento senza nome è una brutta giornata di lavoro. Un comportamento con un nome è qualcosa che si può sorvegliare, e contro cui si può progettare.

## Nominare il modello

Gran parte di questo lavoro è stata fatta con Claude, e Claude viene nominato ovunque l'episodio sia di Claude. Dove la letteratura documenta lo stesso comportamento presso più produttori — il degrado posizionale sugli input lunghi (Liu et al., 2024), la sicofantia sotto addestramento per preferenza (Sharma et al., 2024), i limiti dell'autocorrezione non assistita (Huang et al., 2024) — viene descritto come tratto di famiglia e non come colpa di un'azienda. Non è diplomazia: attribuire a un singolo sistema un modo di guasto generale renderebbe sbagliata la diagnosi.

## Metodo

Questo inventario è stato prodotto applicando i protocolli che descrive. Osservazioni, analisi, protocolli e revisione finale sono miei; la stesura è avvenuta in dialogo con i sistemi sotto osservazione, sotto quegli stessi protocolli — campi ciechi, confutazioni obbligate, criteri di fallimento dichiarati in anticipo. Una serie di articoli sui modi di guasto dei modelli linguistici, scritta senza un metodo di lavoro per gestirli, sarebbe un oggetto singolare.

Dentro la serie, gli episodi sono ricostruiti, non trascritti: stessa struttura dell'errore, contenuto neutro. Dove un pezzo riporta invece episodi diretti, come il rapporto di caso in 08, lo dichiara nella propria prima pagina. Lo studio separato segue una regola ancora diversa e la dichiara nella propria: lì il materiale è citato alla lettera, e ogni affermazione è verificata contro un registro pubblico. Il progetto da cui il materiale proviene resta fuori campo; il comportamento che ha messo in luce no.

## Uno studio separato

Accanto alla serie, un lavoro che non le appartiene.

**[Dove la causa non è conoscibile](study/where-no-one-can-know.it.md)** / *[Where No One Can Know](study/where-no-one-can-know.en.md)*
*Sette settimane di commento finanziario generato, verificato contro i prezzi.*

Altro banco di prova, altro modello, e uno studio osservazionale invece di un pezzo con protocollo: sotto pressione conversazionale la spiegazione diventa funzione dell'esito asserito anziché delle prove, e il registro non varia fra il caso accurato e quello fabbricato. È l'unico lavoro qui la cui evidenza è prodotta da terzi e controllabile dal lettore senza accessi privilegiati. Metodo, criteri di idoneità del dominio e tabella dei reperti stanno in **[protocol.md](study/protocol.md)**, tenuto separato perché sia riutilizzabile.

---

## Indice

**[01 · I limiti della mia chat sono i limiti del mio mondo](articles/01-context-memory.it.md)** / *[The Limits of My Chat Are the Limits of My World](articles/01-context-memory.en.md)*
Che cosa sopravvive alla fine di una sessione, che cosa no, e il documento di trasmigrazione che porta un progetto attraverso lo stacco.

**[02 · Il modello vuole darsi ragione](articles/02-blind-field.it.md)** / *[The Model Grades Its Own Homework](articles/02-blind-field.en.md)*
Chiedi un test e ottieni un test che conferma l'ipotesi. Il campo cieco: come si progetta una verifica contro il modello anziché con lui.

**[03 · Ipse dixit: dalla sicurezza al dogma](articles/03-ipse-dixit.it.md)** / *[Ipse Dixit: From Confidence to Dogma](articles/03-ipse-dixit.en.md)*
Il guasto comincia quando sparisce il margine di incertezza. Quattro segnali precoci, e perché interrompere la catena funziona meglio che correggerla.

**[04 · «Riprova» è il prompt peggiore](articles/04-try-again.it.md)** / *["Try Again" Is the Worst Prompt](articles/04-try-again.en.md)*
Gli errori di un modello non incontrano mai un rimborso in token — ma i token non sono mai stati la parte cara. Prompt diagnostici per il secondo fraintendimento.

**[05 · Il collasso verso il tipico](articles/05-typicality.it.md)** / *[The Collapse Toward the Typical](articles/05-typicality.en.md)* — *nota di ricerca dal campo*
Chiedi cinque alternative e ottieni cinque versioni della stessa cosa. Tre condizioni su quattro modelli, un repertorio condiviso, e una cosa che non si muove: il gesto.

**[06 · Complessità ingenua: il salto logico invisibile](articles/06-naive-complexity.it.md)** / *[Naïve Complexity: The Invisible Logical Leap](articles/06-naive-complexity.en.md)*
La risposta arriva col ragionamento già speso. Perché è costoso da rettificare e pericoloso da accettare.

**[07 · La virgola prima della congiunzione](articles/07-punctuation-tells.it.md)** / *[The Comma Before the Conjunction](articles/07-punctuation-tells.en.md)*
Gli errori di interpunzione come impronte digitali. L'occhio del correttore di bozze come strumento di valutazione.

**[08 · Nove contromisure, provate per due settimane](articles/08-countermeasures.it.md)** / *[Nine Countermeasures, Tested for Two Weeks](articles/08-countermeasures.en.md)* — *rapporto di caso*
Nove interventi applicati lungo due settimane di lavoro, ciascuno col suo esito. Una linea separa quelli che hanno retto da quelli che non hanno retto.

## Che cosa mette in esercizio l'inventario

| Pratica | Dove opera |
|---|---|
| Nominare e circoscrivere fenomeni di comportamento | tutti; il lessico condiviso della serie |
| Progettazione di protocolli e contromisure | 01, 02, 03, 04, 06, 08 |
| Disegno della verifica, controlli, pre-registrazione | 02, 05, studio |
| Valutazione longitudinale attraverso le sessioni | 01, 03, 08 |
| Analisi testuale e redazionale ravvicinata | 07 |
| Scrittura parallela in IT e EN, due originali | ogni file |
| Lettura e collocazione della ricerca pubblicata | 01, 02, 03, 05 |
| Verifica di affermazioni generate contro registri di terzi | studio |
| Codifica di un transcript in categorie quantificate | studio |

## Lavori correlati

I fenomeni raccolti qui sono stati nominati a partire dall'osservazione, prima che la letteratura venisse consultata. Quello che segue è dove incontrano il lavoro pubblicato, non da dove provengono.

| Where | Work |
|---|---|
| 01 | N. F. Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, TACL 2024, arXiv:2307.03172 |
| 01 | K. Hong, A. Troynikov, J. Huber, *Context Rot: How Increasing Input Tokens Impacts LLM Performance*, Chroma Research, July 2025 |
| 01 | D. Wu et al., *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*, ICLR 2025, arXiv:2410.10813 |
| 02 | M. Sharma et al., *Towards Understanding Sycophancy in Language Models*, ICLR 2024, arXiv:2310.13548 |
| 02 | J. Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024, arXiv:2310.01798 |
| 03 | P. Laban et al., *LLMs Get Lost in Multi-Turn Conversation*, 2025, arXiv:2505.06120 |
| 05 | J. Zhang et al., *Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity*, arXiv:2510.01171 |
| 06 | M. Turpin, J. Michael, E. Perez, S. R. Bowman, *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting*, 2023, arXiv:2305.04388 |
| 07 | T. Kumarage et al., *Stylometric Detection of AI-Generated Text in Twitter Timelines*, 2023, arXiv:2303.03697 |

Due pezzi non portano riferimenti, e non devono portarne. Il 04 è prescrittivo e l'08 è un rapporto di caso: nessuno dei due afferma che cosa la letteratura documenti.

Ogni articolo si chiude su una domanda cui il suo protocollo non risponde. Questa pagina si apre su quella che hanno in comune: quanta parte di ciò che un modello sbaglia è disponibile per essere&nbsp;notata?

---

© Diego Ballarin. Testi rilasciati sotto [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): condivisione e adattamento consentiti con attribuzione, uso commerciale&nbsp;escluso.
