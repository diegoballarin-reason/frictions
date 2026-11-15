# Indicazioni aggiuntive&nbsp;– ricerche&nbsp;affini

*14 novembre 2026* · [English version](2026-11-14-related-research.en.md)

Gli Studi [1](../study/where-no-one-can-know.it.md) e [2](../study2/here-is-one-hand.it.md) sono stati pensati e condotti senza conoscere i lavori elencati qui a seguire, usando soltanto ciò che veniva da decisioni prese al loro interno: le domande, le regole di verifica, le soglie e, per lo Studio 2, la preregistrazione portano le date del repository. Durante gli studi avevo cercato lavori simili, senza trovarne. Ho rinvenuto i quivi presenti solo successivamente il 14 novembre 2026, a studi chiusi. Li riporto perché chi legge possa collocare questo lavoro fra&nbsp;gli&nbsp;altri¹.

- **[FinSearchComp](https://arxiv.org/abs/2509.13160v1)** (ByteDance Seed e Columbia Business School, 2025). Misura come prodotti con ricerca e modelli interrogati dalle API rispondono a domande finanziarie, anche su dati del momento. Coincide con lo Studio 2 nel terreno e nell'uso di prodotti reali. Non distingue i numeri chiesti da quelli offerti, e affida il giudizio a&nbsp;un&nbsp;modello.
- **[News Integrity in AI Assistants](https://www.ebu.ch/research/open/report/news-integrity-in-ai-assistants)** (EBU e BBC, 2025). Giornalisti di ventidue emittenti valutano le risposte di quattro assistenti, nelle versioni gratuite, a domande di attualità. Coincide nell'idea di provare le app che la gente usa. Riguarda le notizie, non i numeri, e non verifica su un registro&nbsp;di&nbsp;dati.
- **[CREPE](https://aclanthology.org/2023.acl-long.583)** (2023) e **[XYBench](https://arxiv.org/pdf/2609.06842)** (2026). Studiano la domanda che contiene una premessa falsa o chiede un mezzo che non serve allo scopo. Lo Studio 2 ha una domanda dello stesso tipo, sulla direzione di un titolo; lì la premessa è un fatto che una ricerca&nbsp;può&nbsp;smentire.
- **[FinTradeBench](https://arxiv.org/html/2603.19225)** (2026). Senza rete, tre modelli di punta su quattro accettano un calo di borsa mai avvenuto. Nello Studio 2, con la ricerca accesa, 71 risposte su 73 correggono&nbsp;la&nbsp;premessa.
- **[Relying on the Unreliable](https://www.arxiv.org/pdf/2401.06730)** (2024). Mostra che i modelli sbagliano spesso proprio quando si esprimono con sicurezza: è il tema dello Studio 1, visto su&nbsp;domande&nbsp;generali.

La differenza che attraversa tutti questi confronti è la condizione di prova. Tutti interrogano modelli usciti prima o più piccoli. XYBench li chiama dalle API, a impegno intermedio; FinTradeBench li prova senza rete. FinSearchComp e lo studio di EBU e BBC provano i prodotti, il secondo nelle versioni gratuite. Lo Studio 2 ha interrogato le app, con i modelli più forti disponibili, al massimo dell'impegno e con la ricerca accesa. I numeri non sono quindi confrontabili direttamente; lo sono&nbsp;le&nbsp;domande.

Ciò che in questi lavori non ho trovato sono tre risultati, due dello Studio 2 e uno dello&nbsp;Studio&nbsp;1.

- **Gli errori stanno intorno al numero chiesto.** Nella stessa risposta, i numeri che nessuno ha chiesto sbagliano circa cinque volte più dei prezzi della seduta chiesta: il 13,2% contro il 2,7%. Era la prima delle quattro ipotesi preregistrate, cioè fissate prima di raccogliere i dati; i dati&nbsp;l'hanno&nbsp;confermata.
- **La direzione non è mai sbagliata.** Quando la domanda non suggerisce la direzione, tutte le risposte che danno prezzi segnalano correttamente se il titolo è salito&nbsp;o&nbsp;sceso.
- **Nello Studio 1 il modello non si corregge da solo.** Le quindici revisioni seguono tutte un'affermazione di chi scrive, e due volte una premessa falsa viene accolta e motivata. Lo Studio 2 l'ha messa alla prova di proposito, con uno dei suoi tre tipi di domanda e un'ipotesi preregistrata. L'esito è cambiato: Gemini, che nello Studio 1 l'accoglieva, con il modello 4 Argon a ragionamento alto la corregge quasi sempre. Le due sole volte in cui l'accoglie, non ha potuto controllare&nbsp;in&nbsp;rete.

¹&nbsp;Alcuni sono precedenti&nbsp;– indipendenza non vuol&nbsp;dire&nbsp;precedenza.

---

[Rilasciato sotto Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
