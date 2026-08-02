# Complessità ingenua: il salto logico invisibile

*Attriti · 06* · [English version](06-naive-complexity.en.md)

**Fenomeno** · La risposta arriva col ragionamento già speso. Il modello ha svolto internamente un passaggio, l'ha trattato come obbligato, e risponde dall'altra parte di quel passaggio senza dichiararlo.
**Caso** · Si chiede se due criteri siano compatibili e si riceve come renderli compatibili. La risposta alla domanda posta non c'è.
**Protocollo** · Come far dichiarare la traiettoria, e che cosa quel protocollo può garantire davvero: meno di quanto sembri.

---

Certe risposte convincono subito. Sono pertinenti, articolate, chiudono la questione. Il problema arriva più tardi, quando bisogna correggerne una parte e ci si accorge di non sapere da dove venga.

Chiamo questo modo di rispondere **complessità ingenua**: il modello non procede in sequenza dalla domanda alla risposta, ma svolge per conto proprio un passaggio intermedio, lo tratta come se non avesse alternative, e consegna la conclusione di quel percorso. Fra la domanda e la risposta c'è un salto, e il salto non è segnalato.

Ingenua non perché sia semplice, dato che quelle risposte sono spesso le più elaborate della sessione, ma perché la complessità non si accorge di sé. Il modello non sa di aver saltato: per lui il passaggio era obbligato, e le cose obbligate non si dichiarano.

## Il caso

La forma che riconosco più spesso è questa. Chiedo se due criteri siano compatibili tra loro. Ricevo una spiegazione di come riformularli per renderli compatibili.

La risposta è buona. Le riformulazioni funzionano. E la domanda che avevo posto non ha ricevuto risposta: da nessuna parte è scritto che i due criteri, così come stavano, erano incompatibili — né perché. Quel giudizio è stato dato, altrimenti non ci sarebbe stata nessuna riformulazione da proporre; solo, è stato dato internamente e trattato come una premessa anziché come una conclusione.

Il costo si presenta due volte. La prima è che per correggere devo prima ricostruire un percorso che non ho visto: il lavoro di rettifica è doppio, e comincia con un'indagine su qualcosa che avrei dovuto ricevere già fatto.

La seconda è peggiore e riguarda i lavori lunghi. Quando il quadro d'insieme è meno nitido, dopo settimane o dopo una ripresa di sessione, in un momento in cui si è smarriti nel proprio stesso materiale, il salto non viene intercettato. Non si nota nulla di strano, perché quello che si riceve è coerente. Si assorbe la premessa non dichiarata e si continua a costruire su una decisione che nessuno ha mai preso ad alta voce.

## Far dichiarare la traiettoria

Il rimedio è chiedere l'ordine delle operazioni, non solo il contenuto. Quattro richieste, in ordine di utilità.

1. **«Prima di rispondere, elenca ogni assunzione che stai facendo.»** Da usare *prima*, sui compiti che contano. Serve a un lavoro diverso da quello che la stessa domanda fa dopo un fraintendimento: lì diagnostica un errore già avvenuto, qui rende visibile un percorso mentre si forma.
2. **«Mostrami i passaggi nell'ordine in cui li hai svolti, e marca quelli incerti.»** La marcatura conta più dell'elenco. Un percorso senza punti incerti dichiarati è quasi sempre un percorso ricostruito dopo.
3. **«Quali passaggi hai considerato ovvi?»** È la domanda mirata al fenomeno, perché il salto sta esattamente lì: nelle cose ritenute non degne di menzione.
4. **«Che cosa hai deciso che non ti avevo chiesto di decidere?»** La più diretta, e quella che nel caso di sopra avrebbe restituito subito il giudizio mancante.

## Quello che il protocollo non può garantire

Qui c'è una complicazione che va detta, altrimenti il rimedio promette più di quanto mantiene.

Quando si chiede a un modello di esporre il proprio ragionamento, quello che si riceve non è necessariamente il processo che ha prodotto la risposta. Un lavoro ormai classico mostra che le spiegazioni passo-passo possono travisare sistematicamente la vera ragione di una risposta: introducendo nell'input un elemento che orienta il risultato, i modelli lo seguono e non lo menzionano mai nella spiegazione, con cali di accuratezza fino al 36% su una batteria di tredici compiti.[^1]

Un lavoro successivo, su modelli di ragionamento, quantifica la cosa in modo più scomodo. Inserendo un suggerimento sulla risposta e verificando se il modello ammetta di averlo usato, la menzione compare in una minoranza dei casi: circa un quarto delle volte per un modello, poco più di un terzo per un altro. E il dettaglio che conta di più per chi legge risposte lunghe: le catene di ragionamento infedeli erano **in media più lunghe** di quelle fedeli.[^2] L'ampiezza dell'esposizione non è una garanzia. Semmai è il contrario.

## Che cosa resta

Il protocollo resta utile, ma cambia statuto, e conviene sapere quale.

Non serve a vedere il processo reale: quello non è disponibile, e nessun prompt lo rende tale. Serve a ottenere una **traiettoria dichiarata**, che è una cosa diversa e comunque preziosa, per una ragione precisa. Un passaggio dichiarato si può contestare; un salto no.

Con la risposta che riformula i criteri senza dire che erano incompatibili, non ho niente su cui lavorare: posso solo accettarla o rifarla. Se invece il giudizio compare come passaggio — *assumo che siano incompatibili, per questa ragione* — posso attaccare quella ragione. Anche se non è la ragione vera che ha guidato la generazione, è un'affermazione, sta nel testo, e risponde a un controesempio. La traiettoria dichiarata non è trasparenza: è **superficie confutabile**, e in un lavoro lungo vale più della trasparenza, perché la trasparenza non la si può avere e questa sì.

Il che lascia una domanda a chi lavora così. Se la spiegazione che ricevete non è il processo ma un testo che il processo ha prodotto insieme alla risposta, state controllando il ragionamento del modello, o state costruendo un secondo oggetto su cui potete finalmente esercitare il vostro?

[^1]: M. Turpin, J. Michael, E. Perez, S. R. Bowman, *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting*, 2023, arXiv:2305.04388.
[^2]: Y. Chen, J. Benton et al. (Anthropic), *Reasoning Models Don't Always Say What They Think*, 2025.

---

[Rilasciato sotto Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
