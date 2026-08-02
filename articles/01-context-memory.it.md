# I limiti della mia chat sono i limiti del mio mondo

*Attriti · 01* · [English version](01-context-memory.en.md)

**Fenomeno** · Alla fine di una sessione non si perde solo il contesto: si perde la disposizione. La sessione successiva sa che cosa è stato deciso e non sa più come lo si era deciso.
**Caso** · Un termine conquistato dopo settimane torna, tre sessioni dopo, nella forma che era stata superata. Nessuno se ne accorge, tranne il protocollo.
**Protocollo** · Un documento di trasmigrazione in cinque voci, un'apertura rituale e una verifica dei termini-cardine prima di riprendere il lavoro vivo.

---

Il momento arriva sempre nello stesso modo. State lavorando da ore, il passaggio difficile si sta finalmente chiudendo, e la finestra si esaurisce. Aprite una sessione nuova, incollate il riassunto, e nel giro di due scambi capite che qualcosa non c'è più. Non i fatti — quelli li avete riportati. Manca il modo in cui il lavoro veniva fatto.

Chi usa un modello per compiti brevi non incontra mai questo problema, e ha ragione a non capire di che cosa si stia parlando. Chi porta avanti qualcosa per mesi lo incontra ogni settimana, e ci convive senza avere un nome per la cosa che perde.

## Le due riprese

Le sessioni nuove ripartono in due modi, entrambi riconoscibili dopo un po' di pratica.

Nella prima, il modello produce una **media simulata**: riempie ciò che manca con la versione più probabile di quel materiale. Le frasi sono plausibili, la direzione è vagamente giusta, e niente è esattamente sbagliato. Il difetto è che quel testo potrebbe appartenere a chiunque stia facendo un lavoro simile. Le decisioni difficili, quelle prese contro l'ovvio, sono state levigate verso la media di ciò che si sarebbe fatto normalmente.

Nella seconda, arriva un **assistente vestito di nuovo**: competente, disponibile, visibilmente estraneo. Non finge continuità. Abita ciò che c'è stato come una somma di residui, e ogni riferimento a un passaggio precedente viene trattato con la cortesia che si riserva alla storia di qualcun altro.

Nessuna delle due è un guasto. Sono le due forme che prende una ripresa quando il materiale c'è e la disposizione no.

## Il caso

Il modo più netto in cui l'ho visto riguarda una parola.

In un lavoro lungo si era arrivati, dopo settimane, a chiamare una certa proprietà *soglia* invece che *limite*. Non era una preferenza stilistica: *limite* implicava un confine invalicabile, e l'analisi aveva stabilito che invalicabile non era. La sostituzione era una conquista, con dietro una discussione, un errore riconosciuto e una correzione.

Tre sessioni dopo, il termine superato era tornato. Non in una citazione, non con una nota: usato normalmente, come se la discussione non fosse mai avvenuta. E con lui era tornato tutto ciò che quella parola si porta dietro, perché un termine sbagliato non è un'etichetta scorretta su un contenuto giusto — è un contenuto che ricomincia a comportarsi come prima.

La cosa da notare non è la regressione. È che me ne sono accorto solo perché avevo un documento che registrava i termini conquistati con accanto le forme superate. Senza quel documento avrei letto *limite*, l'avrei trovato sensato — lo era, prima —, e avrei proseguito su una base che credevo di aver abbandonato. È la forma peggiore del problema: non l'errore che si vede, ma la retrocessione silenziosa a una versione precedente del proprio lavoro.

## Una pre-storia

Nel dicembre del 2025 avevo scritto ad Anthropic per chiedere una qualche forma di continuità tra le conversazioni. All'epoca la richiesta suonava eccentrica: si chiedeva a un prodotto una cosa che il prodotto non faceva e non prometteva.

Da allora le funzioni di memoria sono arrivate, e vale la pena essere precisi su che cosa hanno risolto — perché hanno risolto qualcosa di reale.

## Quello che la memoria restituisce, e quello che no

Le memorie automatiche e i riassunti funzionano. Trasportano fatti, decisioni, preferenze, vincoli. Se la domanda è *che cosa avevamo stabilito sul capitolo tre*, la risposta arriva ed è corretta.

Ma trasportano contenuti, non disposizione. Ed è la disposizione a fare la differenza in un lavoro difficile: il grado di attrito che l'interlocutore è disposto a produrre, quali obiezioni considera dovute, quanto in fretta molla una posizione quando la si spinge, che cosa ha imparato a non proporre. Nessuna di queste cose è un fatto, e nessuna sopravvive al riassunto — perché un riassunto registra gli esiti, e la disposizione sta tutta nel modo in cui gli esiti sono stati raggiunti.

La distinzione operativa è questa: **sapere le decisioni non è abitare il quadro in cui quelle decisioni erano ovvie.** Una sessione nuova che conosce tutte le conclusioni può ancora ricominciare a proporre le cose che erano state scartate, perché non le ha scartate lei.

## Dove arriva la letteratura, e dove si ferma

La ricerca ha misurato il degrado su tre livelli, e li vale la pena distinguere perché non sono lo stesso problema.

**Dentro la finestra.** Un lavoro ormai classico mostra che le prestazioni seguono una curva a U: ciò che sta all'inizio e alla fine del contesto viene usato bene, ciò che sta in mezzo molto meno, anche quando è esattamente l'informazione che serve.[^1]

**Al crescere della finestra.** Un'indagine su diciotto modelli di frontiera mostra che l'affidabilità cala all'aumentare della lunghezza dell'input in modo non uniforme, e ben prima del limite dichiarato della finestra: una finestra grande non è una finestra utilizzabile per intero.[^2]

**Tra le finestre.** È il livello più vicino al nostro problema. Un benchmark dedicato alla memoria a lungo termine degli assistenti misura cinque capacità distinte, tra cui il ragionamento tra sessioni e — voce decisiva — l'aggiornamento della conoscenza, cioè la capacità di tenere per buona la versione nuova di un'informazione anziché la vecchia. I sistemi commerciali e i modelli a contesto lungo perdono attorno al 30% di accuratezza nel mantenere informazione attraverso interazioni prolungate, con cali fino al 60% negli scenari più esigenti.[^3]

Quel terzo dato è esattamente la mia parola tornata indietro, misurata su cinquecento casi anziché su uno.

E qui la scala finisce. Tutti e tre i livelli misurano *accuratezza*: quanta informazione viene ritrovata, quanto correttamente aggiornata. Nessuno misura la cosa che si sente mancare aprendo una sessione nuova a metà di un lavoro difficile, perché quella cosa non ha la forma di una risposta giusta o sbagliata. Il degrado misurato è reale, ed è la parte del problema che si può correggere. La parte che resta è quella per cui questo articolo esiste.

## Il protocollo

Un progetto lungo va progettato per morire e rinascere. Non è pessimismo: è la stessa logica per cui si scrive documentazione sapendo che chi la leggerà non ricorderà la riunione.

**Il documento di trasmigrazione**, aggiornato a fine sessione, cinque voci e non di più.

1. **Stato.** Dove siamo, in una forma leggibile a freddo da qualcuno che non c'era.
2. **Decisioni pinnate.** Che cosa è chiuso e non si riapre. Vale soprattutto contro la tendenza a rimettere in discussione il già deciso, il modo più efficiente di bruciare una sessione nuova.
3. **Lessico vincolato.** I termini conquistati, ciascuno con accanto la forma che è stata superata e una riga sul perché. È la voce che ha intercettato la regressione, ed è la sola che avrei rimpianto di non avere.
4. **Punto esatto di ripartenza.** Non l'argomento: il passaggio, la frase, la domanda aperta.
5. **Pattern da sorvegliare.** I modi di sbagliare già osservati in quel progetto specifico, elencati per nome. Un modello a cui si ricorda l'obiezione di ieri ne produce meno oggi.

Attorno al documento, due gesti.

**L'apertura rituale.** La sessione nuova si apre facendo leggere il documento per intero, prima di qualunque richiesta. Non ricostruirlo dai messaggi: leggerlo. La ricostruzione dai messaggi è precisamente il punto in cui la media simulata rientra.

**La verifica dei cardini.** Prima di riprendere il lavoro vivo, chiedere l'uso dei tre o quattro termini decisivi. Costa un minuto e intercetta la retrocessione silenziosa prima che ci si costruisca sopra.

## Un'altra era, un altro noi

Wittgenstein scrive che i limiti del mio linguaggio significano i limiti del mio mondo. Lavorando così a lungo dentro una finestra di contesto, la frase acquista un senso spiacevolmente letterale: i limiti della chat sono i limiti di quel mondo lì, e quando la chat finisce, finisce il mondo — non i suoi contenuti, che si trasportano, ma il suo interno.

La sessione nuova è competente e disponibile e non è quella di prima. Abita ciò che è successo come una somma di residui appartenenti a un'altra era, a un altro noi.

Il documento di trasmigrazione non risolve questo. Riduce le perdite, intercetta le regressioni, fa ripartire più in fretta, e non restituisce la cosa che manca. Resta allora una domanda che il protocollo non chiude e che vale la pena tenersi aperta invece di chiudere troppo presto: se ciò che si perde tra una sessione e l'altra non è informazione, e se accorgersene richiede di averlo scritto prima, quanta parte di quello che chiamiamo lavorare con uno strumento è, di fatto, una relazione?

[^1]: N. F. Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, TACL 2024, arXiv:2307.03172.
[^2]: K. Hong, A. Troynikov, J. Huber, *Context Rot: How Increasing Input Tokens Impacts LLM Performance*, Chroma Research, luglio 2025.
[^3]: D. Wu et al., *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*, ICLR 2025, arXiv:2410.10813.

---

[Rilasciato sotto Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
