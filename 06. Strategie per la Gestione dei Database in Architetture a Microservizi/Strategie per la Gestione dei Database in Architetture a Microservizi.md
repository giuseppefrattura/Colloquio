# 6. Strategie per la Gestione dei Database in Architetture a Microservizi

### Cos'è e perché conta
Riassume e completa in chiave pratica i pattern già visti nelle sezioni sui microservizi e sull'accesso ai database (punti 8 e 10), rispondendo alla domanda "come gestisco letture/scritture concorrenti quando i dati sono sparsi su più servizi?" — un tema molto probabile in un colloquio senior, perché è dove la teoria dei microservizi incontra i problemi reali di concorrenza e consistenza.

### Cosa studiare

**1. Database per Microservizio (Database per Service)**

Ogni microservizio ha il proprio database dedicato — pattern già visto nel punto 8. I vantaggi principali:
- **Isolamento dei dati**: un servizio non può corrompere accidentalmente i dati di un altro
- **Indipendenza tecnologica**: ogni servizio può usare il DB più adatto al proprio caso d'uso (vedi tabella comparativa nel punto 12 — es. Oracle per il ledger, Redis per cache di un servizio specifico)
- **Riduzione delle dipendenze**: un servizio può evolvere lo schema del proprio DB senza coordinarsi con tutti gli altri

Il rovescio della medaglia (utile menzionarlo per dimostrare visione equilibrata): niente più join SQL tra dati di servizi diversi, e niente più transazione ACID unica che copre più servizi — da qui nascono i pattern successivi.

**2. Event Sourcing e CQRS**

Già introdotti nel punto 8, li ripercorriamo con focus sulla gestione della concorrenza:
- Gli eventi vengono memorizzati in un **log di eventi** immutabile (append-only) — invece di sovrascrivere lo stato, si registra ogni cambiamento come nuovo evento
- I comandi (scritture) modificano lo stato generando nuovi eventi, mentre le query (letture) leggono da una **vista materializzata** separata, costruita e aggiornata a partire dagli eventi
- Perché riduce i conflitti di concorrenza: dato che le scritture sono append-only (si aggiunge un nuovo evento, non si modifica uno esistente), il classico problema del "lost update" tra due scritture concorrenti sullo stesso record si riduce drasticamente
- Offre **tracciabilità completa**: ogni cambiamento di stato è ricostruibile — molto rilevante in un dominio regolamentato come i pagamenti, dove poter dimostrare "chi ha cambiato cosa e quando" è spesso un requisito di audit/compliance

**3. Transazioni Distribuite**

- **Saga pattern** (già visto nel punto 8): sequenza di transazioni locali con compensazioni in caso di fallimento — l'approccio oggi preferito nei microservizi
- **Two-Phase Commit (2PC)**: protocollo classico per garantire consistenza tra più risorse — un coordinatore chiede a tutti i partecipanti di "prepararsi" (fase 1, ognuno conferma che può eseguire l'operazione), e solo se **tutti** confermano invia il comando di commit definitivo (fase 2); se anche uno solo fallisce nella fase di prepare, tutti fanno rollback
  - *Perché in pratica si evita nei microservizi moderni*: 2PC richiede che tutte le risorse restino bloccate (lock) per tutta la durata del protocollo, in attesa della decisione finale del coordinatore — questo riduce drasticamente la disponibilità e non scala bene, oltre a creare un singolo punto di fallimento nel coordinatore. Per questo la Saga (che rinuncia alla atomicità immediata in cambio di eventual consistency con compensazioni) è preferita nella maggior parte dei sistemi distribuiti moderni
- **Transazioni di compensazione**: l'azione di "annullamento logico" usata nella Saga quando un passo successivo fallisce — non è un vero rollback (impossibile su DB separati), ma un'operazione inversa esplicita (es. se hai già addebitato un conto, la compensazione è un accredito di pari importo, non la cancellazione della scrittura originale)

**4. Architettura Event-Driven**

Un message broker (Kafka, RabbitMQ) disaccoppia i servizi:
- Il produttore pubblica un evento senza sapere chi lo consumerà, né aspettare che venga processato
- Garantisce consistenza attraverso **code di messaggi** persistenti: se un consumer è temporaneamente giù, i messaggi restano in coda e vengono processati al suo ritorno, invece di perdersi
- Permette operazioni **asincrone**, già discusso nel punto 8 per il caso della notifica post-transazione

**5. Locking e Concurrency Control**

Già accennato nella sezione Oracle (punto 3) parlando di isolation level, qui si generalizza al contesto applicativo:
- **Pessimistic locking**: si blocca la risorsa (es. `SELECT FOR UPDATE`) per tutta la durata dell'operazione, impedendo ad altri di modificarla nel frattempo — sicuro ma riduce la concorrenza, utile quando i conflitti sono frequenti
- **Optimistic locking**: non si blocca nulla in anticipo; si verifica invece, al momento del salvataggio, che i dati non siano stati modificati da qualcun altro nel frattempo — tipicamente con una colonna di versione (`@Version` in JPA): se la versione letta non coincide più con quella a DB, l'update fallisce e va gestito un retry o un errore applicativo. Preferibile quando i conflitti sono rari, perché non paga il costo del lock quando non serve
- **Meccanismi di retry e gestione dei conflitti**: quando un optimistic lock fallisce, la strategia comune è ritentare l'operazione (spesso con backoff, collegandosi al punto sulla resilienza nel punto 11) invece di propagare subito l'errore all'utente

**6. Sharding e Partizionamento**

Già visto nel punto 10 per il contesto Oracle/tabelle grandi, qui nella lente della gestione dati distribuita tra servizi:
- **Suddivisione orizzontale dei dati** su più istanze/nodi in base a una chiave (es. per range di data, per hash di un ID account)
- Migliora prestazioni e scalabilità perché ogni nodo gestisce solo una porzione dei dati e del carico
- Riduce i colli di bottiglia, ma introduce complessità: query che devono aggregare dati da più shard diventano più costose, e la scelta della shard key è una decisione difficile da cambiare in seguito senza una migrazione onerosa

**7. Caching Distribuito**

Già visto nel punto 10 come pattern di ottimizzazione, qui nel contesto specifico della concorrenza tra servizi:
- Redis/Memcached come cache condivisa tra più istanze di uno stesso servizio (o tra servizi diversi, se il dato è comune)
- Riduce il carico sul database per i dati letti più di frequente
- Attenzione alla **coerenza tra cache e DB**: in un sistema con più scritture concorrenti, una cache non invalidata correttamente può restituire dati obsoleti — un problema di concorrenza a sé, spesso sottovalutato

### Considerazioni chiave e raccomandazioni

Nessuna di queste soluzioni è universale — la scelta dipende da:
- Dimensioni del sistema e volumi di dati
- Requisiti di consistenza (forte vs eventual)
- Complessità delle operazioni coinvolte
- Performance richieste (latenza, throughput)

Un buon approccio, utile anche come risposta "da senior" a colloquio:
- **Iniziare semplice** e aggiungere complessità solo quando serve realmente — introdurre Saga/Event Sourcing/sharding fin da subito su un sistema piccolo è spesso over-engineering
- **Valutare i requisiti specifici** prima di scegliere il pattern, non il contrario
- **Testare accuratamente i meccanismi di concorrenza** — sono la categoria di bug più insidiosa perché spesso non si manifestano in ambienti di test a basso carico
- **Implementare monitoraggio e logging** (collegandosi al punto 11 sull'osservabilità) per individuare rapidamente conflitti, retry falliti, o incoerenze tra servizi in produzione

### Come esercitarti
Prepara una risposta strutturata alla domanda "come garantiresti la consistenza di un pagamento che coinvolge tre microservizi diversi (autorizzazione, contabilità, notifica)?" — la risposta ideale cita: database per service come punto di partenza architetturale, Saga con compensazioni per coordinare i tre servizi, eventi asincroni via Kafka/RabbitMQ per disaccoppiarli, e idempotenza (già vista più volte nel documento) per gestire in sicurezza eventuali retry.
