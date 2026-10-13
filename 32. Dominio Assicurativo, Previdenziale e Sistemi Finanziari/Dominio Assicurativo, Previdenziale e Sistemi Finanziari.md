# 32. Assicurazioni, previdenza e sistemi finanziari

## Modellare ruoli e processi prima delle tabelle

In questi domini il medesimo soggetto può avere ruoli differenti. La precisione del linguaggio evita errori applicativi: chi firma un contratto non è sempre chi riceverà la prestazione. Regole, tariffe e obblighi cambiano nel tempo, quindi versioni e date di efficacia fanno parte del modello.

## Il contratto assicurativo

La **compagnia** assume un rischio secondo il contratto. Il **contraente** stipula e sostiene il premio; l'**assicurato** è il soggetto o interesse cui il rischio si riferisce; il **beneficiario** riceve la prestazione prevista. Questi ruoli possono coincidere oppure essere distinti.

Il **premio** è il corrispettivo della copertura. L'**underwriting** valuta il rischio e le condizioni di assunzione. Il **quietanzamento** registra il pagamento del premio; eventuali rate introducono scadenze e stati distinti. Un mancato pagamento va interpretato secondo il contratto, non tradotto automaticamente in cancellazione immediata.

Nel ramo vita si incontrano contratti tradizionali, unit-linked o index-linked e operazioni di capitalizzazione, spesso richiamati con le classificazioni Ramo I, III e V. Nei danni, o **P&C**, Property and Casualty, le coperture riguardano rischi come responsabilità, furto o danni ai beni. Classificazione, garanzie e rischio assunto si leggono sul prodotto concreto, senza presumere una garanzia uniforme da un'etichetta.

## Sinistri e riserve

La **FNOL**, First Notice of Loss, è la prima comunicazione del sinistro. Il processo comprende raccolta delle evidenze, valutazione, decisione e liquidazione. La **franchigia** è una parte dell'importo che rimane a carico secondo il contratto; lo **scoperto** è spesso espresso come percentuale, con condizioni specifiche.

Le **riserve tecniche** rappresentano obbligazioni e impegni valutati secondo regole e basi pertinenti. Un backend deve tracciare cambiamenti, riferimenti e approvazioni, invece di aggiornare soltanto l'ultimo importo. IVASS è l'autorità italiana di vigilanza; Solvency II riguarda il quadro prudenziale e IFRS 17 la rappresentazione contabile dei contratti nel proprio ambito applicabile. La configurazione delle regole richiede la versione e il contesto pertinenti.

## Previdenza: accumulare e poi erogare

La previdenza complementare gestisce contribuzioni e prestazioni per finalità pensionistiche. Fondi e **PIP**, piani individuali pensionistici, hanno caratteristiche e regole proprie. Nell'**accumulo** arrivano contributi e, nei casi previsti, TFR, Trattamento di Fine Rapporto. Il patrimonio viene investito secondo comparti e regole del prodotto.

Una **quota** rappresenta una frazione del patrimonio del comparto. Il **NAV**, Net Asset Value, è il valore netto; il valore per quota deriva dal patrimonio netto e dalle quote secondo la metodologia applicabile. Data del contributo, data di valorizzazione e data di acquisto non devono essere confuse.

Nel **decumulo** il montante finanzia prestazioni in capitale o rendita secondo le condizioni. Una **rendita vitalizia** prosegue per la vita del beneficiario nei termini contrattuali; i coefficienti attuariali collegano capitale e prestazione usando basi demografiche e finanziarie. Anticipazioni e riscatti sono processi distinti con condizioni proprie. COVIP è l'autorità di vigilanza pertinente. Limiti fiscali e percentuali non dovrebbero essere costanti «eterne» nel codice: si modellano con efficacia e provenienza della regola.

## OMS: dalla richiesta all'esecuzione

Un **Order Management System**, OMS, gestisce ordini su strumenti finanziari. I controlli **pre-trade** verificano condizioni prima dell'inoltro: mandato, limiti e disponibilità. Lo **Smart Order Routing** sceglie sedi o percorsi secondo la politica prevista. Un ordine può essere eseguito parzialmente; quantità richiesta, eseguita e residua devono restare distinguibili.

**FIX**, Financial Information eXchange, offre messaggi e regole di sessione per integrazioni finanziarie. Nei profili tag-value, un campo è identificato da un tag; gli execution report descrivono aggiornamenti dello stato. Versione, profilo e gestione della sequenza sono parte del contratto. Il quadro MiFID II e altri vincoli applicabili guidano i controlli, senza implicare un unico algoritmo o una soglia di latenza universale.

## Portafoglio, rendimenti e rischio

L'**asset allocation** ripartisce esposizioni tra classi di attività. La valorizzazione combina posizioni, prezzi e cambi con riferimenti temporali coerenti. Gli **AuM**, Assets under Management, rappresentano il patrimonio gestito secondo la definizione utilizzata.

Il **Time-Weighted Return**, TWR, collega rendimenti di sottoperiodi per ridurre l'effetto dei flussi esterni. Il **Money-Weighted Return**, MWR, considera importi e tempi dei flussi; l'IRR è un modo di esprimerlo attraverso un tasso interno di rendimento. Misurano prospettive diverse, perciò non sono intercambiabili.

La volatilità descrive dispersione dei rendimenti. Il **Value at Risk**, VaR, stima un quantile di perdita entro un orizzonte e un modello: non è la perdita massima possibile. Lo **Sharpe ratio** rapporta rendimento in eccesso e volatilità nella metodologia scelta. Dati, ipotesi e periodo devono accompagnare i valori.

## Commissioni e riconciliazione

Le management fee remunerano la gestione secondo base, tasso e calendario contrattuali. Le performance fee possono dipendere da risultati, benchmark e **High-Water Mark**, HWM, una soglia collegata a massimi precedenti secondo il metodo previsto. Entry ed exit fee riguardano ingresso e uscita; retrocessioni e rebates regolano ripartizioni e restituzioni contrattuali.

Un HWM non va implementato con la sola formula «NAV attuale meno massimo storico» senza definire flussi, quote, cristallizzazione e base al netto o al lordo delle commissioni. Un esempio numerico può illustrare la logica, ma la specifica del prodotto governa il calcolo reale.

La riconciliazione confronta posizioni e movimenti di sistemi diversi. Il matching uno-a-uno usa riferimenti; quello uno-a-molti collega un movimento cumulativo a più registrazioni. Il **net settlement** può includere commissioni trattenute e generare differenze previste. Un **break** o unmatched item è una discrepanza da investigare, non una riga da cancellare per far tornare il totale.

## Esercizio

Progetta la storia di un ordine parzialmente eseguito e poi riconciliato con un rendiconto esterno. Definisci identificatori, date, importi e rettifiche. Spiega quali regole sono invarianti del software e quali provengono da contratti o normative da versionare.
