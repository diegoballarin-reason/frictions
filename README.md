# Frictions

*Recurring ways language models fail, named and countered, from inside an extended writing and research project run as a standing&nbsp;testbed.*<br>
*Bilingual, EN and IT.*

[Licensed under Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · [LICENSE](LICENSE) · → [Versione italiana](#attriti)

A model rarely fails loudly. It agrees, it returns something plausible, and the work drifts — three sessions later you are re-arguing a term that was settled weeks ago. Benchmarks cannot see this. On month three of a project, it is most of what you see.

This is an inventory of those frictions: seven of them, each named, each with a case and a countermeasure.

## Where the material comes from

An extended writing and research project — not code, not design — run over months of sessions as a standing testbed, with a documented protocol governing what carries across from one session to the next. That origin cuts both ways, and both sides are declared here rather than buried.

It is the reason these phenomena are visible at all: most of them need weeks of accumulated context before they surface, which is exactly the condition an afternoon of testing cannot reproduce. It is also the limit of the evidence. This is one long case observed systematically, not a statistic, and nothing here is presented as a measurement. Where published research shows a behaviour holds across model families, it is cited as such and marked as literature; where an observation is mine alone, it says so.

Each article does three things and then stops: it names the phenomenon, shows a case from the field, and gives a protocol that can be run the next morning. The naming carries most of the weight. A behaviour without a name is a bad day at work. A behaviour with a name is something you can watch for, and design against.

## Naming the model

Most of this work was done with Claude, and Claude is named wherever the episode is Claude's. Where the literature documents the same behaviour across vendors — positional degradation over long inputs, sycophancy under preference training, the limits of unaided self-correction — it is described as a family trait rather than one company's fault. The distinction is not diplomacy. Attributing a general failure mode to a single system would make the diagnosis wrong.

## Method

This inventory was produced by applying the protocols it describes. The observations, the analysis, the protocols and the final revision are mine; the drafting was done in dialogue with the systems under observation, under those same protocols — blind fields, forced refutations, pre-declared failure criteria. A set of articles on the failure modes of language models, written without a working method for handling those failure modes, would be an odd artefact.

Episodes are reconstructed rather than transcribed: same structure of error, neutral content. The project the material comes from stays out of view; the behaviour it exposed does not.

## Contents

**01 · The Limits of My Chat Are the Limits of My World** / *I limiti della mia chat sono i limiti del mio mondo*
What survives the end of a session, what does not, and the transmigration document that carries a project across the gap.

**02 · The Model Grades Its Own Homework** / *Il modello vuole darsi ragione*
Ask for a test and you get a test that confirms the hypothesis. The blind field: how to design verification against the model rather than with it.

**03 · Ipse Dixit: When Reasoning Hardens into Dogma** / *Ipse dixit: quando il ragionamento diventa dogma*
Once a line of reasoning becomes load-bearing, it stops being reasoning. Why "try again" yields variations instead of rethinking.

**04 · "Try Again" Is the Worst Prompt** / *«Riprova» è il prompt peggiore*
There are no token refunds for a model's mistakes — but tokens were never the expensive part. Diagnostic prompts for the second misunderstanding.

**05 · Three Signs Your LLM Is Hallucinating (Before the False Facts)** / *Tre segnali che il modello sta allucinando (prima dei fatti falsi)*
Hallucination begins with confidence, not with false facts. Three signs, and a fourth: the tells.

**06 · Naïve Complexity: The Invisible Logical Leap** / *Complessità ingenua: il salto logico invisibile*
The answer arrives with its reasoning already spent. Why that is expensive to correct and dangerous to trust.

**07 · The Comma Before the Conjunction** / *La virgola prima della congiunzione*
Punctuation errors as fingerprints. A proofreader's eye as an evaluation instrument.

## What the inventory exercises

| Practice | Where it operates |
|---|---|
| Naming and delimiting behavioural phenomena | all seven; the shared vocabulary of the series |
| Protocol design and countermeasures | 01, 02, 04, 06 |
| Verification design, controls, pre-registration | 02 |
| Longitudinal evaluation across sessions | 01, 03 |
| Close textual and editorial analysis | 07 |
| Parallel authoring in EN and IT, two originals | every file |
| Reading and situating published research | 01, 02, 05 |

Every article closes on a question its protocol does not answer. This page opens on the one they share: how much of what a model gets wrong is available to be&nbsp;noticed?

---

# Attriti

*I modi ricorrenti in cui i modelli linguistici cedono, nominati e contrastati, dall'interno di un esteso progetto di scrittura e ricerca condotto come banco di prova&nbsp;continuativo.*<br>
*Bilingue, IT e EN.*

[Rilasciato sotto Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · [LICENSE](LICENSE) · → [English version](#frictions)

Un modello raramente fallisce ad alta voce. Asseconda, restituisce qualcosa di plausibile, e il lavoro slitta — tre sessioni dopo stai ridiscutendo un termine che era stato fissato settimane prima. I benchmark non vedono niente di tutto questo. Al terzo mese di un progetto è quasi tutto ciò che si vede.

Questo è l'inventario di quegli attriti: sette, ciascuno con un nome, un caso e una contromisura.

## Da dove viene il materiale

Un esteso progetto di scrittura e ricerca — non codice, non design — condotto lungo mesi di sessioni come banco di prova continuativo, con un protocollo documentato per ciò che passa dall'una all'altra. L'origine taglia da due lati, dichiarati qui tutti e due anziché nasconderne uno.

È la ragione per cui questi fenomeni sono visibili: quasi tutti hanno bisogno di settimane di contesto accumulato prima di affiorare. Un pomeriggio di test non riproduce quella condizione. Ed è anche il limite della prova. Questo è un caso lungo osservato sistematicamente, non una statistica, e nulla qui viene presentato come misurazione. Dove la ricerca pubblicata mostra che un comportamento vale per più famiglie di modelli, viene citata e marcata come letteratura; dove l'osservazione è solo mia, viene detto.

Ogni articolo fa tre cose e si ferma: nomina il fenomeno, mostra un caso di campo, consegna un protocollo eseguibile domani mattina. Il peso maggiore lo porta il nome. Un comportamento senza nome è una brutta giornata di lavoro. Un comportamento con un nome è qualcosa che si può sorvegliare, e contro cui si può progettare.

## Nominare il modello

Gran parte di questo lavoro è stata fatta con Claude, e Claude viene nominato ovunque l'episodio sia di Claude. Dove la letteratura documenta lo stesso comportamento presso più produttori — il degrado posizionale sugli input lunghi, la sicofantia sotto addestramento per preferenza, i limiti dell'autocorrezione non assistita — viene descritto come tratto di famiglia e non come colpa di un'azienda. Non è diplomazia: attribuire a un singolo sistema un modo di guasto generale renderebbe sbagliata la diagnosi.

## Metodo

Questo inventario è stato prodotto applicando i protocolli che descrive. Osservazioni, analisi, protocolli e revisione finale sono miei; la stesura è avvenuta in dialogo con i sistemi sotto osservazione, sotto quegli stessi protocolli — campi ciechi, confutazioni obbligate, criteri di fallimento dichiarati in anticipo. Una serie di articoli sui modi di guasto dei modelli linguistici, scritta senza un metodo di lavoro per gestirli, sarebbe un oggetto singolare.

Gli episodi sono ricostruiti, non trascritti: stessa struttura dell'errore, contenuto neutro. Il progetto da cui il materiale proviene resta fuori campo; il comportamento che ha messo in luce no.

## Indice

**01 · I limiti della mia chat sono i limiti del mio mondo** / *The Limits of My Chat Are the Limits of My World*
Che cosa sopravvive alla fine di una sessione, che cosa no, e il documento di trasmigrazione che porta un progetto attraverso lo stacco.

**02 · Il modello vuole darsi ragione** / *The Model Grades Its Own Homework*
Chiedi un test e ottieni un test che conferma l'ipotesi. Il campo cieco: come si progetta una verifica contro il modello anziché con lui.

**03 · Ipse dixit: quando il ragionamento diventa dogma** / *Ipse Dixit: When Reasoning Hardens into Dogma*
Quando un ragionamento diventa portante smette di essere ragionamento. Perché «riprova» produce variazioni invece di un ripensamento.

**04 · «Riprova» è il prompt peggiore** / *"Try Again" Is the Worst Prompt*
Gli errori di un modello non incontrano mai un rimborso in token — ma i token non sono mai stati la parte cara. Prompt diagnostici per il secondo fraintendimento.

**05 · Tre segnali che il modello sta allucinando (prima dei fatti falsi)** / *Three Signs Your LLM Is Hallucinating (Before the False Facts)*
L'allucinazione comincia dalla sicurezza, non dai fatti falsi. Tre segnali, e un quarto: le spie.

**06 · Complessità ingenua: il salto logico invisibile** / *Naïve Complexity: The Invisible Logical Leap*
La risposta arriva col ragionamento già speso. Perché è costoso da rettificare e pericoloso da accettare.

**07 · La virgola prima della congiunzione** / *The Comma Before the Conjunction*
Gli errori di interpunzione come impronte digitali. L'occhio del correttore di bozze come strumento di valutazione.

## Che cosa mette in esercizio l'inventario

| Pratica | Dove opera |
|---|---|
| Nominare e circoscrivere fenomeni di comportamento | tutti e sette; il lessico condiviso della serie |
| Progettazione di protocolli e contromisure | 01, 02, 04, 06 |
| Disegno della verifica, controlli, pre-registrazione | 02 |
| Valutazione longitudinale attraverso le sessioni | 01, 03 |
| Analisi testuale e redazionale ravvicinata | 07 |
| Scrittura parallela in IT e EN, due originali | ogni file |
| Lettura e collocazione della ricerca pubblicata | 01, 02, 05 |

Ogni articolo si chiude su una domanda cui il suo protocollo non risponde. Questa pagina si apre su quella che hanno in comune: quanta parte di ciò che un modello sbaglia è disponibile per essere&nbsp;notata?

---

© Diego Ballarin. Testi rilasciati sotto [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): condivisione e adattamento consentiti con attribuzione, uso commerciale&nbsp;escluso.
