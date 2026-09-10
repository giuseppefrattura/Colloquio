## 12. Approfondimento Database: MongoDB, Cassandra, Elasticsearch, PostgreSQL, MySQL

### Cos'è e perché conta
Il ruolo richiede specificamente Oracle, ma conoscere anche gli altri database più diffusi mostra ampiezza di vedute ed è utile se emergono domande di confronto ("perché Oracle e non altro?") o se nel tempo il sistema integra componenti non relazionali (cache, ricerca, audit log). Qui trovi una descrizione di ciascuno con possibili domande da colloquio e risposte pronte.

### PostgreSQL

**Cos'è**: database relazionale **open source**, spesso considerato il più "avanzato" tra i DB relazionali open source per ricchezza di funzionalità — supporta tipi di dato avanzati (JSON/JSONB nativi, array, tipi geometrici), window function, CTE ricorsive, estensioni (es. PostGIS per dati geospaziali). Molto vicino a Oracle come potenza espressiva SQL, a differenza di MySQL che è storicamente più minimale.

**Quando si usa**: applicazioni che vogliono la robustezza e ricchezza di un DB relazionale enterprise senza costi di licenza — sempre più scelto anche per carichi misti relazionali + documenti JSON grazie a JSONB.

**Domande tipiche e risposte**

- *D: Che differenza c'è tra JSON e JSONB in PostgreSQL?*
  R: `JSON` salva il testo così com'è, senza parsing — più veloce in scrittura, ma ogni lettura richiede riparsing. `JSONB` salva in formato binario già decomposto — leggermente più lento in scrittura, ma molto più veloce in lettura e supporta indicizzazione (es. GIN index) sui campi interni. Nella pratica si usa quasi sempre JSONB.

- *D: PostgreSQL è ACID?*
  R: Sì, pienamente conforme ACID come Oracle — supporta transazioni, isolamento configurabile (stessi livelli visti per Oracle: READ_COMMITTED è il default), vincoli di integrità referenziale.

- *D: Quando useresti PostgreSQL invece di Oracle in un progetto nuovo?*
  R: Per carichi di lavoro che non richiedono le funzionalità enterprise specifiche di Oracle (RAC, Data Guard) e dove i costi di licenza pesano — ma in un contesto già consolidato su Oracle con competenze/tooling esistenti (come nel ruolo per cui ti candidi), raramente ha senso migrare solo per questo.

### MySQL

**Cos'è**: database relazionale open source storicamente il più diffuso al mondo (soprattutto nel web, es. stack LAMP). Più "leggero" di PostgreSQL/Oracle in termini di funzionalità avanzate, ma estremamente performante per carichi di lettura/scrittura semplici e ad alto volume.

**Quando si usa**: applicazioni web con volumi alti ma logica relazionale non troppo complessa — meno indicato quando servono funzionalità SQL avanzate o forte integrità transazionale su scenari complessi.

**Domande tipiche e risposte**

- *D: Che differenza c'è tra i motori di storage InnoDB e MyISAM in MySQL?*
  R: InnoDB (default da anni) supporta transazioni ACID, foreign key, row-level locking. MyISAM è più vecchio, non supporta transazioni né foreign key, usa table-level locking — oggi praticamente non si usa più per nuovi progetti se serve integrità transazionale.

- *D: MySQL è adatto a un sistema di pagamenti?*
  R: Tecnicamente sì con InnoDB (è ACID compliant), ma in contesti enterprise regolamentati come i pagamenti si preferisce quasi sempre Oracle o PostgreSQL per le funzionalità avanzate di gestione, sicurezza, supporto enterprise e strumenti di alta affidabilità (clustering, disaster recovery) più maturi.

### MongoDB

**Cos'è**: il **document store** NoSQL più diffuso — salva dati come documenti in formato simile a JSON (BSON), organizzati in collection invece che tabelle. Schema flessibile: documenti nella stessa collection possono avere strutture diverse.

**Quando si usa**: dati semi-strutturati o che cambiano forma nel tempo, dove uno schema fisso relazionale sarebbe troppo rigido — es. cataloghi prodotto con attributi variabili, log applicativi, configurazioni.

**Domande tipiche e risposte**

- *D: MongoDB è ACID?*
  R: Dalla versione 4.0 supporta transazioni ACID multi-documento, ma storicamente (ed è ancora il caso d'uso più naturale) è pensato per garanzie di atomicità solo a livello di singolo documento — per questo motivo si modella spesso i dati "denormalizzati", incapsulando in un unico documento le informazioni che in un DB relazionale sarebbero su più tabelle collegate.

- *D: Perché non useresti MongoDB come DB principale in un sistema di pagamenti?*
  R: Il core di un sistema di pagamenti richiede relazioni forti e consistenza immediata su transazioni multi-entità (account, transazione, ledger) — lo schema fisso e le garanzie ACID native di un DB relazionale come Oracle si adattano meglio. MongoDB può però avere un ruolo di supporto: es. salvare payload di richieste/risposte verso circuiti esterni (formati variabili, poco strutturati) senza dover forzare uno schema rigido.

- *D: Come funziona lo sharding in MongoDB?*
  R: I dati vengono partizionati orizzontalmente su più nodi in base a una **shard key** — ogni nodo gestisce un sottoinsieme dei dati, permettendo scalabilità orizzontale su volumi molto grandi. La scelta della shard key è critica: una scelta cattiva può creare "hot shard" (nodi sovraccarichi mentre altri restano inattivi).

### Cassandra

**Cos'è**: database NoSQL **column-family**, progettato da Facebook per scalabilità estrema in scrittura e alta disponibilità distribuita su più data center, senza singolo punto di fallimento (architettura *masterless*, ogni nodo è equivalente).

**Quando si usa**: scenari con volumi di scrittura altissimi e necessità di disponibilità continua anche in caso di guasto di un intero data center — tipico per time-series data, log di eventi, sistemi IoT.

**Domande tipiche e risposte**

- *D: Che modello di consistenza usa Cassandra?*
  R: **Eventual consistency** per default, configurabile per singola query attraverso il **consistency level** (es. `ONE`, `QUORUM`, `ALL`) — puoi scegliere quanti nodi devono confermare una scrittura/lettura prima di considerarla riuscita, bilanciando consistenza e disponibilità/latenza (è un'applicazione pratica del **teorema CAP**: Cassandra privilegia Availability e Partition tolerance sulla Consistency forte, a differenza di un DB relazionale).

- *D: Perché Cassandra scrive così velocemente rispetto a un DB relazionale?*
  R: Usa una struttura dati **LSM-tree** (Log-Structured Merge-tree): le scritture vengono prima accodate in memoria (memtable) e poi periodicamente scritte su disco in blocchi ordinati (SSTable) in modo sequenziale, evitando i costosi update in-place e la ricerca di righe esistenti tipici di un DB relazionale.

- *D: Useresti Cassandra in un sistema di pagamenti?*
  R: Non per il ledger transazionale (serve consistenza forte, non eventual), ma potrebbe avere senso per un **audit log** ad altissimo volume di eventi (ogni chiamata API, ogni tentativo di autenticazione) dove la scrittura veloce e la disponibilità contano più della consistenza immediata.

### Elasticsearch

**Cos'è**: motore di ricerca e analisi distribuito, basato su Lucene. Non è un database relazionale né un semplice document store — è specializzato in **ricerca full-text veloce** e aggregazioni su grandi volumi di dati semi-strutturati (JSON).

**Quando si usa**: ricerca testuale (es. autocomplete, ricerca fuzzy), log centralizzati (è la "E" di ELK stack, già citato nella sezione osservabilità), dashboard di analytics su grandi volumi di eventi.

**Domande tipiche e risposte**

- *D: Elasticsearch può sostituire un database relazionale?*
  R: No — non ha transazioni ACID forti, gli aggiornamenti frequenti di singoli documenti sono relativamente costosi (ogni update in Lucene comporta la reindicizzazione del documento), e non è pensato per essere la fonte di verità (*source of truth*) dei dati. Si usa tipicamente **in affiancamento** a un DB relazionale: i dati "vivono" nel DB principale (es. Oracle) e vengono replicati/indicizzati in Elasticsearch solo per abilitare ricerca veloce.

- *D: Come funziona l'indicizzazione in Elasticsearch?*
  R: I documenti JSON vengono analizzati (*analysis*): il testo viene tokenizzato, normalizzato (lowercase, stemming) e mappato in un **indice invertito** — una struttura che associa ogni token ai documenti che lo contengono, permettendo ricerche full-text molto veloci rispetto a una scansione `LIKE '%...%'` su un DB relazionale.

- *D: Che ruolo avrebbe Elasticsearch in un sistema di pagamenti?*
  R: Principalmente per **osservabilità** (centralizzare e cercare nei log applicativi di tutti i microservizi, come già visto nella sezione ELK) e per dashboard operative che devono aggregare/filtrare velocemente grandi volumi di transazioni per supporto clienti o investigazioni antifrode — non come sistema di registrazione delle transazioni stesse.

### Tabella riassuntiva per orientarti velocemente

| Database | Tipo | Punto di forza | Ruolo tipico in un sistema di pagamenti |
|---|---|---|---|
| Oracle / PostgreSQL | Relazionale | ACID, integrità, query complesse | Ledger, saldi, transazioni core |
| MySQL | Relazionale | Semplicità, alte performance su carichi semplici | Meno tipico in ambito enterprise pagamenti |
| MongoDB | Document store | Schema flessibile | Payload esterni non strutturati, configurazioni |
| Cassandra | Column-family | Scrittura massiva, alta disponibilità | Audit log/eventi ad altissimo volume |
| Elasticsearch | Motore di ricerca | Full-text search, aggregazioni veloci | Log centralizzati, dashboard di supporto/antifrode |

### Come esercitarti
La domanda più probabile in un colloquio non è "spiegami MongoDB" isolatamente, ma "quando useresti X invece di Y" — esercitati proprio sulla tabella sopra: per ogni riga, prepara una frase che spieghi *perché* quel database è la scelta giusta per quel ruolo specifico, collegandola sempre al fatto che il ledger transazionale resta comunque su un DB relazionale con garanzie ACID forti.
