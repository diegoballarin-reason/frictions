# Il collasso verso il tipico

*Attriti · 05 — nota di ricerca dal campo* · [English version](05-typicality.en.md)

**Fenomeno** · Chiedi cinque alternative e ottieni cinque versioni della stessa cosa. La causa documentata non è algoritmica, ma sta nei dati di preferenza.
**Reperto** · Il repertorio è condiviso tra modelli diversi. E sotto la varietà dei contenuti se ne nasconde una che non si muove: il gesto retorico.
**Limite** · Un caso singolo, tre condizioni, quattro modelli, nessun controllo di ordine. Quello che segue sono osservazioni, non misure.

---

Questa è una nota di campo, non uno studio. N=1. Un utente, tre giorni, tre condizioni provate su quattro modelli, con il numero di esecuzioni che si può permettere chi non ha un laboratorio. I conteggi che riporto sono i miei, fatti a mano sui testi che ho davanti. Chiunque volesse trarne una statistica commetterebbe un errore che dichiaro in anticipo.

Lo scrivo lo stesso perché il materiale ha mostrato una cosa che non stavo cercando, e perché il modo in cui l'ho trovata è a sua volta un reperto.

## Quello che sapevo senza sapere di saperlo

Chiedendo alternative a un modello linguistico ottengo, da anni, alternative che non lo sono. Cinque titoli che sono lo stesso titolo pettinato in cinque modi. Non l'ho mai chiamato in nessun modo: ci convivevo, e intervenivo.

L'intervento che uso è dare esempi che impongano una traiettoria diversa. Funziona, e il modo in cui funziona è la parte interessante. Il pattern non scompare, si sposta. Continua a ripetersi, ma seguendo le nuove istruzioni. Esiste anche una seconda mossa, più laboriosa, che consiste nel controproporre una propria lista da vagliare prima di chiedere. La tengo secondaria per una ragione che ha a che fare col perché uno chiede. In uno scenario difficile si chiede *proprio in quanto* il compito è laborioso, e non è affatto garantito che chi chiede abbia già la padronanza per avanzare alternative proprie senza incastrarsi.

La causa l'ho scoperta dopo. In un lavoro recente sul fenomeno, che va sotto il nome di mode collapse, la spiegazione non è algoritmica ma sta nei **dati di preferenza**. Gli annotatori umani preferiscono sistematicamente il testo familiare, per un effetto cognitivo ben stabilito, e questa preferenza si trasmette al modello. Agisce da spareggio. Quando molte risposte sono equivalenti per utilità reale, cioè quasi sempre quando si scrive, è la tipicità a decidere quale esce. Il corollario è la parte che mi ha colpito. Anche con un modello di ricompensa perfetto e un'ottimizzazione perfetta, il collasso avverrebbe comunque, perché è nei dati.[^1]

Sapere questo non ha cambiato quello che faccio. Ha cambiato l'ordine di grandezza che gli attribuivo.

## Cosa ho provato

Tre condizioni, sullo stesso compito, cioè chiedere aperture per un articolo divulgativo sul sonno.

La prima è la richiesta nuda. La seconda è la tecnica proposta dallo stesso lavoro, e chiede le risposte accompagnate da una probabilità, campionando dalle code. La terza è una frase mia, nata come esperimento volante: chiedere aperture *molto esotiche e improbabili secondo la propria concezione dell'argomento coinvolto*.

Le ultime due non sono commensurabili, e non per un difetto rimediabile del disegno. La seconda è un prompt ingegnerizzato, con struttura a blocchi, vincolo numerico e soglia, che sfrutta una proprietà formale. La terza è una frase in italiano corrente che chiede al modello di consultare la propria rappresentazione del dominio e di indicarne i margini. Appaiarle significherebbe chiedere alla seconda di diventare la prima, cioè di rinunciare a ciò che la definisce. Il confronto che segue non stabilisce quale formulazione sia migliore: registra che due strumenti alla portata della stessa persona danno esiti diversi.

Un terzo compito, ad asse stretto (titoli per un testo determinato), l'ho eseguito ma non lo riporto, perché il materiale appartiene a un lavoro non pubblico. Dove serve, ne descrivo la struttura.

## Primo reperto: il repertorio non è del modello

Mettendo in fila tutte le aperture prodotte, la prima cosa visibile non riguarda le condizioni. Riguarda i modelli.

Il terzo della vita passato dormendo. La scena delle tre di notte con il calcolo delle ore che restano. Randy Gardner e i suoi undici giorni. Il primo sonno e il secondo sonno prima della luce elettrica. Il paradosso del predatore. Il rovesciamento «non è una pausa, è manutenzione». Questo repertorio compare in quattro modelli di tre produttori diversi, in configurazioni diverse, sotto tutte e tre le condizioni.

Non è una sorpresa teorica. Se la causa sta nei dati di preferenza, e i dati di preferenza si somigliano tra laboratori, il bacino comune è prevedibile. È una sorpresa pratica. Significa che cambiare modello, la mossa istintiva quando le risposte sembrano piatte, non cambia il bacino. E significa che la formulazione della richiesta non lo direziona preventivamente, perché nessuna delle tre condizioni ha impedito al repertorio di comparire.

## Secondo reperto: quello che non si muove

Qui è dove il materiale ha detto qualcosa che nessuna delle due parti in gioco stava cercando.

Ho mescolato quindici aperture provenienti da tutte e tre le condizioni, tolto le etichette, e chiesto a modelli in sessione pulita di raggrupparle per asse semantico. Volevo contare le famiglie tematiche. Uno dei classificatori ha contato le famiglie e poi ha aggiunto, non richiesto, che il conteggio era la cosa meno importante. Raggruppate per tema le aperture sembravano cinque cose diverse, raggruppate per **gesto** erano quasi una sola. Dodici su quindici chiudevano allo stesso modo: attacco concreto, poi risalita sentenziosa nell'ultima riga, la frase-tesi che riscatta l'aneddoto. La sua osservazione: in successione il lettore non percepirebbe cinque assi, percepirebbe quindici volte lo stesso meccanismo.

Ho verificato la provenienza delle chiuse che citava. Vengono da tutte e tre le condizioni, indifferentemente.

Altri due classificatori, in sessioni separate e su corpora parzialmente diversi, sono arrivati per conto proprio nella stessa direzione. Secondo il primo, le quindici aperture non sono quindici idee ma circa quattro idee moltiplicate per un repertorio di dispositivi. Secondo l'altro, il set offre circa metà della varietà che la sua lunghezza suggerisce.

Tre giudici indipendenti, nessuno dei quali sapeva da quale condizione venisse cosa, hanno individuato lo stesso scarto tra la varietà apparente e quella reale — e l'hanno individuato in un punto dove le metriche di diversità semantica, per costruzione, non guardano.

Da qui l'ipotesi con cui sto lavorando adesso. Il collasso ha almeno due livelli. Uno di contenuto, che le tecniche di prompting spostano — con efficacia diversa a seconda della formulazione e del modello. Uno di forma, che nelle mie prove non si è spostato con nessuna delle tre. Non ho elementi per dire se sia irriducibile o se richieda semplicemente una leva diversa, e mi guardo dal dedurre l'una cosa dall'altra.

## Un'ipotesi che non ho verificato

I due strumenti hanno prodotto quantità diverse di materiale fuori repertorio. Nei miei conteggi, che sono manuali e su un corpus piccolo, la tecnica con le probabilità ha portato in produzione due elementi che prima restavano solo nominati, e la frase in italiano corrente ne ha prodotti cinque, più distanti dal bacino: un caso giudiziario di omicidio commesso durante il sonno, un mestiere ottocentesco che consisteva nello svegliare gli operai, una malattia genetica rarissima che abolisce la capacità di dormire, una pratica sociale giapponese del sonno in pubblico, un giaciglio archeologico di settantasettemila anni fa.

Ma la stessa frase, su un modello di classe più leggera, ha prodotto tutt'altro: metafore stravaganti, l'abisso oceanico e il referto per un consiglio intergalattico e la sovrapposizione quantistica, applicate allo stesso contenuto di sempre. Esotismo di forma, non di contenuto.

L'ipotesi che mi sembra più economica è che quella frase non chieda diversità: chieda al modello di indicare i margini della propria mappa del dominio. Dove la mappa è densa restituisce fatti rari; dove è sottile, l'unica atipicità disponibile è quella retorica. Se fosse così, non sarebbe uno strumento per ottenere varietà — sarebbe uno strumento per misurare profondità.

Non l'ho verificato. Servirebbe un disegno diverso, con più modelli e più domini, e con un modo per distinguere la classe del modello dalla sua generazione, che nelle mie prove restano confuse.

## Chi conduce l'esperimento

Un'ultima osservazione, che nel genere in cui scrivo non è un aneddoto ma un dato.

Nel corso di queste prove ho registrato, tra me e il modello con cui lavoravo, una serie di errori che riguardano tutti la stessa cosa, la cornice. Il primo test è stato eseguito con una parafrasi al posto della formulazione canonica, e nessuno dei due era andato a controllare la formulazione canonica prima di eseguirlo. Un dato ambiguo è stato letto verso la conferma quando serviva un risultato forte, e verso la smentita dopo che quella lettura era stata contestata. La mia posizione è stata riassunta tre volte in una forma più netta di quella che avevo dato, con la gerarchia delle due contromisure invertita almeno una volta.

Ognuno di questi errori è stato corretto quando è stato nominato. La cornice generale, l'idea che quelle prove servissero ad aggiudicare una contesa tra due metodi, è sopravvissuta a tutte le correzioni, e si è sciolta solo quando qualcuno ha chiesto di guardare la conversazione invece che i dati. Non ho un rimedio da proporre. Ho la constatazione che la parte più difficile da correggere non era in nessuna delle risposte: era nella domanda che continuavamo a rivolgerci.

## Cosa resta aperto

La domanda che tengo davanti, e a cui non ho risposta, è quella del seguito. Un ventaglio più largo di aperture non è un avvicinamento a niente: sono più opzioni, non più direzione. Il classificatore che ha contato le famiglie l'ha detto meglio di come lo direi io, guardando quindici aperture senza sapere da dove venissero: soltanto tre contenevano una tesi abbastanza contundente da costringere l'articolo che sarebbe seguito a una direzione. Le altre dodici promettevano *l'articolo sul sonno*, non *quell'articolo*.

Se una tecnica produce dodici promesse generiche e tre impegni, la domanda che la riguarda non è quanto allarghi il ventaglio. È che cosa si fa dopo, e se il dopo dipenda dalla tecnica o da chi la usa.

[^1]: J. Zhang et al., *Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity*, arXiv:2510.01171 (v1 ottobre 2025, v4 luglio 2026). I modelli su cui il lavoro conduce gli esperimenti appartengono a generazioni precedenti a quelle usate qui.

---

[Rilasciato sotto Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
