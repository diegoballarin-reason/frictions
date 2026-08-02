# «Riprova» è il prompt peggiore

*Attriti · 04* · [English version](04-try-again.en.md)

**Fenomeno** · Gli errori di un modello non incontrano mai un rimborso in token. Ma i token non sono mai stati la parte cara.
**Caso** · La correzione silenziosa: si chiede di sistemare una cosa, ne tornano tre cambiate, e nessuno dice quali.
**Protocollo** · Quattro domande diagnostiche al posto di «riprova», più il modo di capire quando il problema era invece il vostro prompt.

---

Il modello ha frainteso. Voi rispondete «riprova», o «non è quello che intendevo», o riscrivete la richiesta cambiando due aggettivi. Torna qualcosa di molto simile a prima. Riprovate ancora. È il punto in cui una mezz'ora si trasforma in un pomeriggio.

Vale la pena vedere perché quel prompt, che sembra il più naturale del mondo, è quasi il peggiore disponibile.

## L'economia dell'errore

Un modello che vi fraintende consuma i vostri token. Quelli spesi nel percorso sbagliato, quelli della richiesta rifatta, quelli del lavoro da rifare: nessuno viene restituito. Non esiste rimborso per un errore che non era vostro.

Ma i token non sono il problema. Sono la cosa più economica in gioco, e concentrarsi su quelli fa perdere di vista che cosa si stia spendendo davvero. Il costo vero è **il contesto che dovete ricostruire**, la spiegazione che dovete ripetere, il filo del ragionamento che avevate in testa mentre scrivevate la richiesta iniziale e che alla terza riformulazione non c'è più. È un problema di attenzione, non di consumo. Dopo due fraintendimenti la cosa peggiore che avete perso non è nel conto, è nella testa.

Da qui la regola pratica: **al secondo fraintendimento si smette di lucidare il prompt e si cambia il processo.**

## Perché «riprova» non funziona

Per due ragioni distinte, che conviene tenere separate perché suggeriscono rimedi diversi.

La prima è che il modello non sa cosa dovrebbe cambiare. «Riprova» comunica insoddisfazione e nessuna informazione. Quello che ottenete è una variazione: sinonimi, ordine diverso, un paragrafo in più. Il percorso di ragionamento resta quello, perché non gli avete dato niente per costruirne un altro.

La seconda è peggiore. La richiesta ripetuta arriva dopo la risposta sbagliata, ormai nel contesto. State chiedendo di ricominciare a qualcuno che ha davanti agli occhi il proprio tentativo precedente. Ripetere la stessa istruzione tende a rinforzare l'interpretazione che l'aveva prodotta, invece di scalzarla.

## La correzione silenziosa

C'è una variante che costa più di tutte perché non si vede subito.

Chiedete di correggere una cosa specifica in un testo. Torna il testo intero, con la correzione richiesta e altre due o tre modifiche che nessuno ha chiesto: una parola sostituita, una frase riordinata, un passaggio semplificato. Nessuna è segnalata. Voi leggete, la correzione che vi interessava c'è, approvate. Tre passaggi dopo non sapete più quale versione sia in vigore, e una scelta che avevate ponderato è sparita senza che nessuno l'abbia mai discussa.

Il rimedio è una richiesta esplicita, da fare una volta e poi tenere ferma. **Le correzioni si registrano, non si sostituiscono.** In pratica, «prima del testo nuovo, elencami che cosa hai cambiato e perché, voce per voce». Costa dieci righe e restituisce il controllo su ciò che si sta approvando.

## Le quattro domande

Al posto di «riprova», queste. Nessuna chiede una risposta migliore. Chiedono di rendere visibile il punto in cui la risposta si è staccata dalla richiesta.

1. **«Che assunzioni hai fatto?»** Fa emergere quello che è stato dato per scontato. È la domanda che risolve più casi da sola.
2. **«Quale parte della mia richiesta hai dedotto invece di leggerla?»** Più mirata della precedente e più scomoda per il modello, perché separa ciò che c'era scritto da ciò che è stato inferito.
3. **«Che cosa ti manca per rispondere bene?»** Rovescia la direzione. Spesso la risposta è un'informazione che avevate e non avete pensato di dare.
4. **«Fammi tre domande di chiarimento prima di rispondere.»** Da usare *prima*, sui compiti che valgono il tempo. È l'unica delle quattro che previene invece di diagnosticare.

E quando il fraintendimento riguarda un compito lungo, quattro mosse strutturali che valgono più di qualunque riformulazione: spezzare in stadi con una consegna per stadio; ridurre il contesto a quello che serve davvero, perché la lunghezza non è gratis; mettere checkpoint espliciti; chiedere un riassunto di ciò che si è capito **prima** di procedere alla parte successiva. Quest'ultima è la più sottovalutata: un riassunto sbagliato costa dieci secondi, un capitolo sbagliato costa un pomeriggio.

## Quando invece il prompt era il problema

Sarebbe comodo concludere che la colpa è sempre dall'altra parte. Non lo è, e c'è un modo abbastanza netto per distinguere i due casi. Sta nella risposta alla prima domanda.

Se il modello elenca un'assunzione che la vostra richiesta **non escludeva**, il prompt era il problema: avete lasciato aperta una porta e lui c'è passato, cosa che avrebbe fatto chiunque. Si corregge chiudendo la porta, non ripetendo la frase.

Se elenca un'assunzione che la richiesta **escludeva esplicitamente**, il problema è dall'altra parte, e nessuna riformulazione lo risolverà: quella è l'occasione in cui conviene ricominciare in una sessione pulita, dove la risposta sbagliata non è più nel contesto a fare da attrattore.

Il criterio non è infallibile, ma è meglio del riflesso a cui sostituirsi. Il riflesso dice di riformulare. La riformulazione è la risposta giusta a uno solo dei due casi, e non è quello in cui vi trovate più spesso.

## Dove va a finire l'attenzione

Il fenomeno da cui siamo partiti si riassume in una riga: gli errori non si rimborsano. La versione utile della stessa riga è che il conto non arriva dove lo state guardando.

Il che porta a una domanda ragionevole da farsi la prossima volta che vi trovate alla terza riformulazione dello stesso prompt: state ancora lavorando al problema, o state lavorando alla richiesta?

---

[Rilasciato sotto Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
