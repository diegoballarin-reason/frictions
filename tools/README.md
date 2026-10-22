# tells_lint

*The extraction step of the protocol in [07 · The Comma Before the Conjunction](../articles/07-punctuation-tells.en.md).*<br>
*Code under the MIT licence · → [Versione italiana](#estrattore-di-spie)*

The script does not correct and does not decide. It extracts every occurrence of the patterns that most often come out uncalibrated, prints each with a few words of context and a gloss to judge it by, and counts them. The decision stays with whoever proofreads.

## Usage

Python 3, standard library only.

```
python3 tools/tells_lint.py articles/07-punctuation-tells.en.md
python3 tools/tells_lint.py articles/*.md
python3 tools/tells_lint.py README.md
python3 tools/tells_lint.py draft.md --lang=en
```

The language comes from the file name (`.it.md`, `.en.md`), from the `# Attriti` separator in bilingual files such as the README, or from `--lang=`. Without any of these, both grids run on the whole text.

## Severity

- `[!]` probable error, almost always to fix
- `[?]` to check, legitimate in the cases the gloss names
- `[~]` density, correct one at a time and suspect as a distribution; reported per 1,000 words

## Two grids

Italian and English have separate grids, as step 4 of the protocol requires. The comma before *and* is the most reliable tell in Italian and is not diagnostic in English: the English grid lists it for review and names the one construction where it is wrong. The English grid also checks false friends and calques from Italian. The glosses are written in Italian.

Headings, tables, code fences, links and bylines are skipped.

## What a hit means

A hit marks a passage to judge. A cluster marks a passage that may need rewriting. Neither says the text was generated: that conclusion needs evidence a comma cannot carry (step 5).

[MIT licence](LICENSE) for the code. The articles remain under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

---

# Estrattore di spie

*Il passo di estrazione del protocollo in [07 · La virgola prima della congiunzione](../articles/07-punctuation-tells.it.md).*<br>
*Codice sotto licenza MIT · → [English version](#tells_lint)*

Lo script non corregge e non decide. Estrae ogni occorrenza dei pattern che più spesso risultano non calibrati, stampa ciascuna con poche parole di contesto e la glossa con cui giudicarla, e le conta. La decisione resta di chi rilegge.

## Uso

Python 3, solo libreria standard.

```
python3 tools/tells_lint.py articles/07-punctuation-tells.it.md
python3 tools/tells_lint.py articles/*.md
python3 tools/tells_lint.py README.md
python3 tools/tells_lint.py bozza.md --lang=it
```

La lingua si ricava dal nome del file (`.it.md`, `.en.md`), dal separatore `# Attriti` nei file bilingui come il README, oppure da `--lang=`. In mancanza di tutti e tre, le due griglie girano sull'intero testo.

## Severità

- `[!]` errore probabile, quasi sempre da correggere
- `[?]` da verificare, legittimo nei casi indicati dalla glossa
- `[~]` densità, corretto singolarmente e sospetto come distribuzione; riportato ogni 1.000 parole

## Due griglie

Italiano e inglese hanno griglie separate, come chiede il passo 4 del protocollo. La virgola prima della *e* è la spia più affidabile in italiano e non è diagnostica in inglese: la griglia inglese la elenca per la verifica e indica l'unica costruzione in cui è scorretta. La griglia inglese controlla anche falsi amici e calchi dall'italiano.

Titoli, tabelle, blocchi di codice, link e righe d'attribuzione vengono saltati.

## Che cosa significa un'occorrenza

Un'occorrenza segnala un passo da giudicare. Un addensamento segnala un passo che forse va riscritto. Nessuno dei due dice che il testo è stato generato: quella conclusione richiede prove che una virgola non può portare (passo 5).

[Licenza MIT](LICENSE) per il codice. Gli articoli restano sotto [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
