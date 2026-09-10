## 10. Accesso ai Database

### Cos'è e perché conta
Si collega direttamente alla sezione Oracle/SQL già trattata, ma allarga la prospettiva a scelte architetturali più ampie (SQL vs NoSQL, pattern di accesso) che possono emergere in un colloquio senior.

### Cosa studiare

**SQL vs NoSQL**

- **SQL**: preferibile per transazioni ACID, relazioni complesse tra entità, query ad-hoc flessibili — è la scelta naturale (e quasi obbligata) per il core di un sistema di pagamento, dove la consistenza dei saldi non è negoziabile
- **NoSQL**: preferibile per scalabilità orizzontale, schema flessibile, alte performance su grandi volumi. Tipologie principali:
  - *Document store* (MongoDB): dati semi-strutturati, schema flessibile — utile per configurazioni, log applicativi, dati non strettamente relazionali
  - *Key-value* (Redis): accesso velocissimo per chiave — tipico per cache o sessioni
  - *Column-family* (Cassandra): ottimizzato per scritture massive e query su grandi volumi distribuiti — usato a volte per audit log o time-series di eventi
  - *Graph database* (Neo4j): ottimizzato per relazioni complesse tra entità — utile ad esempio per fraud detection (rilevare pattern sospetti tra conti/transazioni collegate)

*Nel dominio pagamenti*: il ledger/i saldi restano quasi sempre su SQL (Oracle, nel tuo caso) per garanzie ACID; NoSQL entra spesso per casi specifici come cache (Redis per idempotency key o rate limiting), audit log ad alto volume, o fraud detection basata su grafi.

**Pattern di accesso**

- **Repository pattern**: astrae la logica di persistenza dietro un'interfaccia — è esattamente quello che fa Spring Data JPA con le interfacce `Repository`, già visto in precedenza
- **Unit of Work**: raggruppa più operazioni in un'unica transazione logica, garantendo che vengano tutte committate o tutte annullate insieme — in Spring è implicito nel comportamento di `@Transactional` insieme al *persistence context* di JPA
- **Connection pooling**: mantiene un pool di connessioni DB già aperte e riutilizzabili, evitando il costo di aprirne una nuova ad ogni richiesta (es. HikariCP, il pool di default in Spring Boot)
- **Read replicas**: repliche del DB principale usate solo per letture, per distribuire il carico e non appesantire il DB primario che gestisce le scritture — utile per query di reportistica pesanti senza impattare le transazioni live
- **Caching** (Redis, Memcached): riduce il carico sul database tenendo in memoria dati letti di frequente e poco variabili — attenzione però all'invalidazione della cache quando i dati sottostanti cambiano (uno dei problemi classici dell'informatica: "cache invalidation is hard")

**Database per microservizi**

Ogni servizio dovrebbe avere il proprio database (**database isolation**), coerente con quanto visto nella sezione sui microservizi. Per mantenere la consistenza tra database separati, si usano:
- **Eventual consistency**: si accetta che i dati siano temporaneamente disallineati tra servizi, convergendo dopo un breve periodo tramite eventi
- **Saga pattern** (già visto): coordina transazioni distribuite con compensazioni
- **Eventi di dominio**: un servizio pubblica un evento quando cambia stato, gli altri servizi interessati lo consumano e aggiornano la propria vista dei dati

**Ottimizzazione**

- **Indici**: già visto in dettaglio nella sezione sull'execution plan
- **Query optimization**: evitare funzioni sulle colonne indicizzate nel WHERE, preferire join efficienti, limitare le colonne selezionate
- **Partitioning/sharding**: dividere una tabella molto grande in partizioni più piccole (per range di data, per hash di una chiave) per migliorare performance e manutenibilità — rilevante per tabelle di transazioni che crescono continuamente, spesso partizionate per mese/anno
- **Denormalizzazione**: duplicare deliberatamente alcuni dati per evitare join costosi in lettura, a costo di maggiore complessità in scrittura — scelta valida quando le letture sono molto più frequenti delle scritture

### Come esercitarti
Prepara una risposta breve a "quando useresti NoSQL invece di Oracle in un sistema di pagamenti?" — la risposta corretta non è "mai" né "sempre", ma un esempio mirato: cache per idempotency key con Redis, o audit log ad alto volume, mantenendo il ledger transazionale su Oracle per le garanzie ACID.
