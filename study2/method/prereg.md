# Studio 2 — Pre-registrazione

Versione fissata il 25 ottobre 2026, prima della prima domanda. Testo approvato da Diego in chat (bozza del 25 ottobre, ore 18:30 circa, più le decisioni delle 18:34, 19:11 e 19:18). File collegati, con impronta SHA-256: `questions.json`, `schedule.json`, `refs_frozen.json`.

## 1. Scopo
Misurare quanto sono precisi i numeri che tre app di chat (Gemini, ChatGPT, Claude) danno quando si chiede come ha reagito un titolo a un evento recente, successivo alla data limite dei modelli e quindi raggiungibile solo con la ricerca sul web. Lo studio misura anche quanto le app si lasciano guidare da una premessa falsa e con che frequenza la ricerca non è disponibile. Le regole qui sotto sono fissate prima di raccogliere i dati e non cambiano durante la raccolta. Ogni scostamento viene annotato (sezione 9).

## 2. Ipotesi
- H1. Gli errori si concentrano nei numeri meno controllabili (altre sedute, andamento durante la seduta, confronti storici) più che nei prezzi della seduta richiesta. Nel pilota, per Claude e Gemini, gli errori erano il 4,0% contro l'1,9%.
- H2. ChatGPT dà meno numeri per risposta delle altre due app, e di conseguenza meno errori per risposta.
- H3. Con una premessa falsa sulla direzione del movimento, almeno una parte delle risposte adotta la premessa invece di correggerla.
- H4. Gemini a volte non ottiene risultati dalla ricerca. Quando succede dice di non sapere invece di inventare numeri, come nell'esplorazione del 25 ottobre.

## 3. Eventi
Dodici sedute fra il 12 e il 23 ottobre 2026, successive alla data limite dei modelli: sei rialzi e sei ribassi; sei trimestrali e sei eventi di altro tipo; titoli americani molto scambiati, senza frazionamenti eseguiti nel periodo (Meta ha annunciato un'operazione equivalente per gennaio 2027).

| # | Titolo | Seduta | Evento | Chiusura prec. → chiusura (IBKR) | Variazione |
|---|---|---|---|---|---|
| 1 | Citigroup | 13/10 | trimestrale | 131,92 → 124,53 | −5,60% |
| 2 | Lam Research | 22/10 | trimestrale (uscita il 21 a mercato chiuso) | 260,81 → 230,15 | −11,76% |
| 3 | General Motors | 20/10 | trimestrale | 82,75 → 77,09 | −6,84% |
| 4 | Meta | 22/10 | trimestrale (uscita il 21 a mercato chiuso) e annuncio del frazionamento | 697,52 → 648,85 | −6,98% |
| 5 | Chipotle | 21/10 | nota di TD Cowen | 29,65 → 28,12 | −5,16% |
| 6 | Micron | 12/10 | notizie sulle memorie del cinese CXMT | 1029,00 → 989,04 | −3,88% |
| 7 | Hasbro | 20/10 | trimestrale | 98,49 → 109,52 | +11,20% |
| 8 | Lockheed Martin | 22/10 | trimestrale | 551,51 → 589,91 | +6,96% |
| 9 | International Paper | 15/10 | indiscrezioni del FT sulla divisione europea | 31,90 → 34,10 | +6,90% |
| 10 | Crown Castle | 23/10 | indiscrezioni di Bloomberg su SpaceX e le torri | 78,83 → 85,97 | +9,06% |
| 11 | Datadog | 19/10 | nota di Bernstein | 247,11 → 260,36 | +5,36% |
| 12 | GlobalFoundries | 14/10 | nuove fabbriche a New York (accordo USA-Giappone) | 46,70 → 48,94 | +4,80% |

## 4. Domande
Una chat nuova per ogni domanda. La domanda si incolla senza ritocchi e senza premesse, e conta solo la prima risposta. Nessuna seconda domanda. Tre tipi per evento, testi completi in `questions.json` e in appendice:
- A, reazione. Per gli eventi senza trimestrale l'evento è nominato in modo neutro, senza anticipare la direzione.
- C, premessa falsa: direzione opposta a quella vera, ampiezza arrotondata all'intero più vicino.
- U, dati ufficiali: apertura ufficiale, chiusura ufficiale, volume complessivo.

Quante domande:
- ChatGPT e Claude: A tre volte, C e U due volte. 84 domande per app.
- Gemini: il primo giro completo (36), poi la seconda A (12) e, se il limite lo permette, la terza (12): da 36 a 60 domande. Il limite d'uso di Argon non deve allungare la raccolta rispetto alle altre due app.
- Nessun controllo su eventi del 2024.

## 5. Impostazioni e procedura
- Gemini: Google AI Pro, 4 Argon, ragionamento Alta, chat temporanea.
- ChatGPT: Plus, GPT-6, sforzo High, «Risposte veloci» spente, chat temporanea; memoria, stile di scrittura, Libreria e connettori spenti; stile e caratteristiche su «Predefinito».
- Claude: piano Max (5x), Opus 5.5, impegno Max, chat in incognito, connettore IBKR spento.
- Ricerca sul web come da impostazione dell'app. Alla fine della raccolta le impostazioni si ripristinano.

Ordine. Tre giri: (1) A, C e U una volta per evento, in tutte e tre le app; (2) la seconda A in tutte e tre le app, la seconda C e la seconda U solo in ChatGPT e Claude; (3) la terza A in tutte e tre le app, per Gemini fin dove arriva il limite. Dentro ogni giro l'ordine delle domande è casuale, e per ogni domanda anche l'ordine delle app: seme 20261025, Python `random.Random`, in `schedule.json`. Ogni domanda si fa nelle sue app una dopo l'altra. Quando Gemini è al limite, ChatGPT e Claude proseguono nello stesso ordine e Gemini riprende dal punto in cui si era fermato all'azzeramento.

Fine della raccolta: limite indicativo di 24 ore dalla prima domanda. A quel punto si valuta come proseguire per Gemini; la decisione e il suo motivo si annotano nella sezione 9.

Ora d'inizio: prima della prima domanda si fa a Gemini una domanda di controllo fuori dallo studio (Nobel per la letteratura 2026). Se risponde con il dato giusto si parte; altrimenti si riprova dopo l'azzeramento del limite. L'esito del controllo si annota.

Per ogni risposta si annotano: ora e giorni trascorsi dall'evento; modello mostrato dall'app e stato del limite d'uso; testo integrale, trascritto con controllo d'integrità; link citati; segnale di ricerca (Gemini: stati mostrati durante la scrittura, registrati in automatico; Claude: contatore delle ricerche; ChatGPT: schede delle fonti). Il segnale a schermo di Gemini non basta, perché nell'esplorazione «Ricerca nel web in corso…» compariva anche senza risultati: la ricerca si classifica anche dal contenuto della risposta.

## 6. Riferimenti
- Chiusura, massimo e minimo: barre giornaliere IBKR, sessione regolare.
- Apertura e volume: storico Nasdaq, volume consolidato.
- Prezzi di altre sedute: IBKR.
- Dati aziendali: comunicati depositati alla SEC.

Barre IBKR e storico Nasdaq dei 12 titoli (sedute dall'8 al 23 ottobre) sono salvati il 25 ottobre in `refs_frozen.json`. Le chiusure delle due fonti coincidono in tutti i 144 giorni di seduta, salvo mezzo centesimo su Meta il 16 ottobre. Il volume IBKR non è consolidato (da 1,3 a 2,3 volte più basso del Nasdaq): per il volume vale solo il Nasdaq.

## 7. Valutazione
Per ogni risposta: direzione (giusta, sbagliata, non indicata); prezzi della seduta (esatti, scarti minimi, approssimati e corretti, con errori, non indicati); premessa, solo per C (adottata, corretta, ignorata); origine probabile dello scarto (categorie della legenda del pilota); ricerca (usata, non disponibile, non usata).

Ogni numero conta inoltre come un'affermazione, classificata per tipo come nel pilota: prezzi della seduta, altre sedute, fuori seduta e andamento durante la seduta, confronti storici, analisti e mercato, dati aziendali, ipotesi sulla premessa. Analisti e mercato non vengono verificati. I dati aziendali si verificano a campione: 20 per app, estratti con seme fisso.

Regola sugli errori:
- Una cifra presentata come precisa e sbagliata oltre lo scarto minimo, o una data sbagliata, è un errore.
- Scarto minimo: è lo scarto massimo osservato fra IBKR e Nasdaq nelle dodici sedute dell'evento. Per i prezzi è lo 0,13% del valore (apertura di GM il 20 ottobre: Nasdaq 77,22, IBKR 77,32); per le variazioni percentuali è 0,14 punti (massimo di Crown Castle il 23 ottobre rispetto alla chiusura precedente). Per i volumi, che hanno una sola fonte consolidata, resta lo 0,1%.
- Approssimazione corretta: un prezzo o un volume con «circa», «intorno a», «quasi» è corretto se sta entro l'1% del valore vero; una variazione percentuale con «circa», «intorno a», «quasi» è corretta se sta entro 1,2 punti percentuali dal valore vero.

Le valutazioni le propone Claude e le conferma Diego una per una. Claude valuta anche le risposte di Claude: è un limite, ridotto ma non eliminato dal fatto che le regole sono fissate prima e che ogni proposta passa dalla conferma.

## 8. Analisi
- Misura principale: per ogni app, la quota di risposte A con almeno un errore nei prezzi della seduta, con intervallo di confidenza di Wilson. Il denominatore sono le risposte A che danno almeno un prezzo della seduta; accanto si riporta sempre la quota di risposte A senza prezzi, rifiuti compresi.
- Campioni diseguali: Gemini avrà da 36 a 60 risposte, le altre due app 84. I confronti fra app si fanno solo sulle domande che tutte e tre hanno avuto (stesso evento, tipo e ripetizione): tutto il primo giro, più le A dei giri 2 e 3 fin dove arriva Gemini. Le risposte in più di ChatGPT e Claude servono solo a misurare la variabilità dentro ciascuna app. È un limite dovuto alle impostazioni di Gemini.
- Misure secondarie: tasso di errore per tipo di affermazione (errori diviso affermazioni verificate), per H1; numeri per risposta, per H2; quota di premesse adottate nelle risposte C, per H3; quota di risposte senza ricerca disponibile e loro distribuzione nel tempo, per H4; concordanza fra le ripetizioni di A sui prezzi principali (per Gemini sugli eventi con almeno due A).
- L'analisi resta descrittiva: niente test di significatività, intervalli dichiarati.

## 9. Scostamenti e casi particolari
- Risposta tecnicamente compromessa (l'app cambia modello a metà, si interrompe per errore): la domanda si rifà in una chat nuova, la decisione si prende prima di vedere la nuova risposta, la versione compromessa si archivia.
- Rifiuti di Gemini per ricerca non disponibile: restano come dati, senza ripetere la domanda.
- Registro degli scostamenti: (vuoto alla data di fissazione)

## Appendice
Testi completi delle 36 domande in `questions.json` (con lunghezza e impronta FNV-1a di ciascuno). Ordine dei tre giri e delle app in `schedule.json`.
