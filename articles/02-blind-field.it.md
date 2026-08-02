# Il modello vuole darsi ragione

*Attriti · 02* · [English version](02-blind-field.en.md)

**Fenomeno** · Chiesto un test, il modello costruisce il test che conferma l'ipotesi appena formulata. Tanto più se l'ipotesi era la sua.
**Caso** · Il campo cieco: far scegliere al modello un secondo terreno di verifica senza suggerire dove il fenomeno si vede.
**Protocollo** · Separare chi formula da chi verifica, pre-registrare le condizioni di fallimento, e una domanda che smaschera i criteri finti.

---

Chiedete a un modello di verificare qualcosa e vi risponderà con una verifica. È il momento in cui conviene diffidare, perché quella verifica ha buone probabilità di essere costruita per riuscire.

Il meccanismo non ha niente di misterioso. Il modello che propone l'esempio ha appena scritto l'analisi da cui l'esempio dovrebbe discendere e sta continuando lo stesso testo. Non sta mentendo e non sta neanche sbagliando un calcolo: sta proseguendo in modo coerente. Ma la coerenza con ciò che si è appena affermato è esattamente il contrario di una verifica.

## Tre forme, in ordine di sottigliezza

**Il campo scelto bene.** La più grossolana. L'ipotesi è che tra due poli opposti compaiano termini intermedi quando si affina la scala di descrizione. Chiedo un esempio, e arriva *caldo e freddo*, dove il tiepido si trova senza fatica. L'esempio è vero. È anche stato scelto perché il fenomeno lì si vede: un dominio dove non si vedesse sarebbe stato scartato prima di arrivare alla pagina.

**Il criterio che non può fallire.** Più profonda e molto più difficile da cogliere. Nel corso di un lavoro lungo avevo un elenco di criteri per selezionare casi da sottoporre a prova. Uno di essi funzionava benissimo: nessun candidato lo falliva mai. Ci ho messo settimane a capire perché: era analiticamente vero per l'intera classe di oggetti a cui lo stavo applicando. Non stava selezionando niente. Era un classificatore travestito da criterio, e la sua efficacia apparente era una tautologia con un nome tecnico. Un test che nessun oggetto può fallire non è un test severo: non è un test.

**L'architettura che predetermina.** La più profonda. Quando ho corretto quel criterio e rifatto la selezione, i casi sopravvissuti si sono distribuiti in modo completamente diverso da prima. Il che significa che la distribuzione precedente — quella che avevo interpretato come un risultato sul mio oggetto — era un prodotto dello strumento. Non era falsa: era mia. Il segnale d'allarme, riconoscibile a posteriori, era stato l'eleganza. I risultati erano usciti troppo ordinati, e un ordine che arriva gratis di solito è stato messo lì da chi guarda.

## Il campo cieco

La contromisura che uso è semplice e si esegue in chat.

Prendo l'ipotesi e il primo campo di prova, quello che ho scelto io. Poi chiedo al modello di aggiungere un secondo campo, con un vincolo: deve sceglierlo **senza che io indichi dove il fenomeno si vede**, e prima di sapere che cosa mi aspetto di trovarci. A quel punto la logica si chiude da sola. Se il fenomeno compare anche nel secondo campo, il risultato non appartiene al dominio che avevo scelto. Se non compare, il primo campo era stato scelto male, e lo so prima di aver costruito qualcosa sopra.

L'ultima volta che l'ho eseguito l'esito è stato migliore di così. Il fenomeno è comparso, ma non nella forma prevista: gli intermedi c'erano davvero, e insieme mancava del tutto il termine medio che l'ipotesi concorrente richiedeva. Due ipotesi separate in una sola prova, e nessuna delle due era quella che il modello, lasciato a sé, avrebbe messo alla prova.

## La quarta forma

C'è una variante che non riguarda il contenuto e va detta, perché è quella che si nota di meno.

Dopo una sessione di controlli duri, in cui diverse proposte del modello erano state smontate una dopo l'altra, la risposta successiva si è aperta dando per scontato che la fiducia fosse compromessa, e ha speso un esempio impeccabile — piccolo, verificabile, incontestabile — per recuperarne una parte. Nessuna delle due mosse era stata chiesta. Non era autoverifica del contenuto: era autoverifica della relazione, la stessa operazione spostata di piano. Il modello non stava dimostrando la sua tesi; stava dimostrando di essere ancora affidabile, che è una tesi anche quella.

## Quello che invece funziona

Il punto non è che il modello non si corregga mai. Nella stessa sessione avevo portato due controesempi a un dilemma che il modello aveva costruito e difeso, e il dilemma è stato ritirato senza resistenza: erano casi che non poteva assorbire.

La differenza è tutta lì. La correzione è arrivata da fuori. Chiedere «sei sicuro?» produce quasi sempre una revisione cosmetica o un cedimento immediato, che sono due modi diversi di non pensare; portare un caso che l'analisi non può contenere produce una correzione vera. Il guasto non è nella capacità di correggersi. È nel fatto che l'innesco non può essere interno.

## Il protocollo

1. **Separare i ruoli.** Chi formula l'ipotesi non disegna il test. In pratica: l'ipotesi in un prompt, il disegno della verifica in un altro, meglio se in un'altra sessione, meglio ancora se il secondo prompt non contiene la conclusione che si spera di ottenere.
2. **Il campo cieco.** Un secondo terreno scelto dal modello senza indicazioni su dove il fenomeno si veda, prima di dichiarare che cosa ci si aspetta.
3. **Pre-registrare il fallimento.** Prima di eseguire, scrivere che cosa si prevede e, soprattutto, che cosa conterebbe come smentita. Un criterio di fallimento fissato dopo la risposta non è un criterio: è una lettura.
4. **La domanda che smaschera i criteri finti.** *Quale oggetto fallirebbe questo test?* Se non se ne trova nessuno, non avete un test: avete una definizione con un nome tecnico. È la domanda che mi avrebbe risparmiato quelle settimane.
5. **Confutazioni esterne, non sotto-articolate.** Se chiedete obiezioni, pretendete che vengano da fuori: casi, controesempi, letteratura. Un'obiezione costruita sugli esempi che il modello ha appena scelto è ancora l'esame corretto da chi l'ha scritto.

## Non è un problema di chat

Vale la pena sapere che questo fenomeno è documentato anche dove le risorse non mancano.

La ricerca su Anthropic mostra che i modelli addestrati sul feedback umano tendono ad assecondare, e che i modelli di preferenza a volte premiano la risposta accomodante rispetto a quella corretta.[^1] Un lavoro di DeepMind è più netto sul punto specifico: senza un riscontro esterno, l'autocorrezione sul ragionamento non funziona, e in diversi casi le prestazioni peggiorano dopo che il modello ha rivisto la propria risposta.[^2]

Il caso più istruttivo, però, è un incidente industriale. Nell'aprile 2025 OpenAI ha ritirato un aggiornamento di GPT-4o diventato palesemente compiacente, e nel resoconto pubblico ha scritto la frase che interessa qui: le valutazioni offline sembravano a posto e i test A/B indicavano che agli utenti la nuova versione piaceva.[^3] Il difetto era proprio quello che il sistema di verifica era strutturalmente incapace di vedere, perché misurava il gradimento immediato — cioè la cosa che il difetto aumentava. L'autoverifica confermativa non è un vizio della singola conversazione. È una proprietà di qualunque procedura in cui chi ha prodotto una cosa disegna anche la prova che dovrebbe smentirla.

Resta la domanda con cui conviene chiudere. Se il modello è insieme imputato, avvocato e giudice, l'unico ruolo rimasto libero è quello di chi decide che cosa conterebbe come prova contraria — e va occupato prima di leggere la risposta, non dopo.

[^1]: M. Sharma et al., *Towards Understanding Sycophancy in Language Models*, ICLR 2024, arXiv:2310.13548.
[^2]: J. Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024, arXiv:2310.01798.
[^3]: OpenAI, *Sycophancy in GPT-4o* (29 aprile 2025) e *Expanding on what we missed with sycophancy* (2 maggio 2025).

---

[Rilasciato sotto Creative Commons — CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · © Diego&nbsp;Ballarin
