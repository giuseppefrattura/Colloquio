# 31. Il dominio dei pagamenti

## Seguire un acquisto dalla richiesta al regolamento

Il dominio dei pagamenti distingue intenzione, autorizzazione ed effettivo trasferimento dei fondi. Un acquisto di dieci euro al negozio non è un'unica operazione istantanea. Confondere questi momenti produce stati applicativi e contabili ambigui.

Il **merchant** è l'esercente; l'**issuer** emette la carta al titolare; l'**acquirer** offre al merchant il servizio di accettazione. Il **PSP**, Payment Service Provider, eroga servizi di pagamento e integrazione secondo il ruolo assunto. Il **circuito** collega partecipanti e regole per instradare e trattare le operazioni.

## Autorizzazione, capture, clearing e settlement

L'**autorizzazione** verifica se l'operazione può essere approvata secondo fondi, credito e controlli previsti. Non equivale ancora al regolamento finale. La **capture**, cattura, conferma l'importo da addebitare secondo il processo adottato; può seguire l'autorizzazione in un momento distinto.

Il **clearing** scambia e determina informazioni e obbligazioni da regolare. Il **settlement** realizza il regolamento finanziario tra i partecipanti. Tempi e dettagli dipendono dallo schema e dal contratto. Un'applicazione deve quindi mantenere stati distinti e collegare gli identificatori nelle varie fasi.

Un **refund** è un rimborso avviato secondo il processo commerciale; un **chargeback** è una contestazione trattata dalle regole del circuito. Non sono sinonimi né semplici cancellazioni di una riga. Conservare riferimenti e storia consente di collegarli all'operazione originale.

## Protocolli e schemi hanno scopi diversi

**ISO 8583** definisce messaggi per transazioni finanziarie con carte. L'**MTI**, Message Type Indicator, descrive il tipo di messaggio; una **bitmap** indica quali data element sono presenti. I dettagli dei campi dipendono dal profilo adottato: conoscere lo standard non basta a integrare qualsiasi circuito.

**ISO 20022** organizza un modello e definizioni di messaggi finanziari, spesso rappresentati in XML nelle integrazioni. Non è soltanto «ISO 8583 riscritto in XML» né ne impone la sostituzione in ogni circuito. Contratto, versione e significato dei campi guidano l'implementazione.

**SEPA** comprende schemi per pagamenti in euro. SCT riguarda i bonifici e **SCT Inst** i bonifici istantanei. La differenza coinvolge disponibilità del servizio, tempi e regole operative: per l'integrazione si usa la versione applicabile del [rulebook dell'European Payments Council](https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-instant-credit-transfer-sct-inst/sepa-instant-credit-transfer), evitando di codificare limiti ricordati da una versione precedente.

## Token, autenticazione e dati sensibili

Il **PAN**, Primary Account Number, identifica la carta. La tokenizzazione sostituisce il PAN con un valore previsto per un contesto d'uso. Nei wallet, il **Token Service Provider** gestisce emissione e ciclo del token secondo il modello adottato. Il token non equivale al PAN, ma può essere una credenziale utilizzabile nel contesto consentito.

La **Strong Customer Authentication**, SCA, combina fattori indipendenti secondo le regole applicabili: conoscenza, possesso e inerenza, cioè una caratteristica personale. PCI DSS riguarda la protezione dei dati carta; la protezione dei dati personali comprende minimizzazione, accessi e conservazione. Il progetto traduce questi obblighi in controlli concreti, mantenendo distinta la spiegazione tecnica dalla verifica normativa del caso specifico.

## Riconciliare le evidenze

La **riconciliazione** confronta registrazioni interne ed evidenze esterne per individuare corrispondenze e discrepanze. Il matching può essere uno-a-uno o coinvolgere più righe; commissioni, valute e giorni differenti complicano il confronto. Un importo uguale non dimostra da solo che due movimenti siano la stessa operazione.

Un esito sconosciuto dopo timeout va gestito con interrogazione dello stato e riconciliazione, evitando un secondo addebito. Le eccezioni non abbinate richiedono un processo operativo e una traccia delle decisioni manuali.

## Esercizio

Racconta il percorso di dieci euro dal POS al conto dell'esercente. Distingui approvazione, cattura e regolamento; poi inserisci un timeout e una contestazione. Spiega quali stati e riferimenti consentono di ricostruire ogni passaggio senza perdere la storia.
