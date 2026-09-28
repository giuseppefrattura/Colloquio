# MongoDB — Guida Senior Developer

## 1. Cos'è MongoDB

MongoDB è un database **NoSQL document-oriented**. I dati vengono memorizzati come documenti BSON (Binary JSON) organizzati in collection.

```text
MongoDB
 └── Database
      └── Collection
           ├── Document
           ├── Document
           └── Document
```

Un documento può avere struttura simile a:

```json
{
  "_id": "123",
  "customerId": "C001",
  "status": "PAID",
  "total": 149.90,
  "items": [
    { "productId": "P10", "quantity": 2, "price": 49.95 },
    { "productId": "P20", "quantity": 1, "price": 50.00 }
  ],
  "shipping": {
    "city": "Milan",
    "country": "IT"
  }
}
```

La differenza fondamentale rispetto a un RDBMS è che il modello dati non richiede necessariamente tabelle normalizzate e JOIN tra molte entità. Il documento può contenere dati correlati tramite **embedding**.

---

## 2. Quando usare MongoDB

MongoDB è particolarmente interessante quando:

- il modello dati è naturalmente documentale;
- lo schema evolve frequentemente;
- le applicazioni leggono/scrivono aggregate completi;
- è utile avere dati correlati nello stesso documento;
- serve scalare orizzontalmente;
- il carico richiede elevata disponibilità e distribuzione;
- si gestiscono cataloghi, profili, contenuti, configurazioni, eventi o dati semi-strutturati.

Esempi:

- cataloghi prodotto;
- customer/profile data;
- CMS e contenuti;
- configurazioni applicative;
- eventi e audit data;
- IoT/time-series workloads quando il modello è appropriato;
- applicazioni con documenti eterogenei.

### Quando NON scegliere MongoDB

Non scegliere MongoDB semplicemente perché "NoSQL è più scalabile".

Un RDBMS può essere preferibile quando il dominio richiede:

- relazioni fortemente strutturate;
- molte JOIN complesse;
- vincoli referenziali sofisticati;
- transazioni multi-entità frequenti;
- reporting relazionale complesso;
- forte dipendenza da SQL e strumenti BI.

La domanda corretta è:

> **Qual è il modello di accesso ai dati e quali proprietà di consistenza/scalabilità richiede il dominio?**

---

## 3. Document Model: embedding vs referencing

### Embedding

I dati correlati vengono inseriti nello stesso documento.

```json
{
  "orderId": "O100",
  "customer": {
    "id": "C10",
    "name": "Mario Rossi"
  },
  "items": [
    { "productId": "P1", "quantity": 2 },
    { "productId": "P2", "quantity": 1 }
  ]
}
```

Vantaggi:

- una singola lettura può restituire l'aggregate;
- meno round-trip;
- niente JOIN applicativi per i dati embedded;
- buona località dei dati.

Svantaggi:

- duplicazione dei dati;
- aggiornamenti più complessi se lo stesso dato è duplicato in molti documenti;
- dimensione del documento potenzialmente elevata.

### Referencing

Si memorizza un riferimento a un altro documento:

```json
{
  "orderId": "O100",
  "customerId": "C10"
}
```

È utile quando:

- il dato referenziato cambia frequentemente;
- viene condiviso da molti documenti;
- la cardinalità è elevata;
- il documento embedded diventerebbe troppo grande.

### Regola pratica

> **Modellare in base ai pattern di accesso, non in base alla normalizzazione tipica dei database relazionali.**

---

## 4. BSON e ObjectId

MongoDB utilizza BSON, una rappresentazione binaria estesa di JSON.

BSON supporta anche tipi come:

- Date;
- Decimal128;
- Binary;
- ObjectId;
- int32/int64.

Un `_id` comune è `ObjectId`.

```javascript
db.orders.findOne({ _id: ObjectId("...") })
```

L'ObjectId contiene informazioni temporali e viene progettato per essere praticamente unico nel contesto previsto.

---

# 5. CRUD e query MongoDB

## Insert

```javascript
db.users.insertOne({
  name: "Mario",
  age: 40,
  active: true
})
```

Inserimento multiplo:

```javascript
db.users.insertMany([
  { name: "Mario", age: 40 },
  { name: "Luigi", age: 35 }
])
```

## Find

Tutti i documenti:

```javascript
db.users.find()
```

Filtro:

```javascript
db.users.find({ age: { $gte: 30 } })
```

AND implicito:

```javascript
db.users.find({
  active: true,
  age: { $gte: 30 }
})
```

OR:

```javascript
db.users.find({
  $or: [
    { role: "ADMIN" },
    { role: "SUPPORT" }
  ]
})
```

## Projection

Non recuperare campi inutili:

```javascript
db.users.find(
  { active: true },
  { name: 1, email: 1, _id: 0 }
)
```

## Sort e limit

```javascript
db.users.find({ active: true })
  .sort({ createdAt: -1 })
  .limit(20)
```

## Update

```javascript
db.users.updateOne(
  { _id: ObjectId("...") },
  {
    $set: { active: false },
    $currentDate: { updatedAt: true }
  }
)
```

Incremento atomico:

```javascript
db.products.updateOne(
  { _id: "P1" },
  { $inc: { stock: -1 } }
)
```

## Delete

```javascript
db.users.deleteOne({ _id: ObjectId("...") })
```

---

# 6. Query su array e documenti embedded

Dato:

```json
{
  "name": "Mario",
  "addresses": [
    { "city": "Milan", "primary": true },
    { "city": "Rome", "primary": false }
  ]
}
```

Ricerca su array:

```javascript
db.users.find({ "addresses.city": "Milan" })
```

Con condizioni sullo stesso elemento dell'array usare `$elemMatch` quando necessario:

```javascript
db.users.find({
  addresses: {
    $elemMatch: {
      city: "Milan",
      primary: true
    }
  }
})
```

---

# 7. Aggregation Framework

L'Aggregation Framework permette di costruire pipeline per trasformare e aggregare documenti.

Esempio:

```javascript
db.orders.aggregate([
  { $match: { status: "PAID" } },
  {
    $group: {
      _id: "$customerId",
      total: { $sum: "$total" },
      orders: { $sum: 1 }
    }
  },
  { $sort: { total: -1 } }
])
```

Concetto:

```text
Documents
   ↓
$match
   ↓
$group
   ↓
$sort
   ↓
Result
```

Operatori importanti:

- `$match`
- `$project`
- `$set`
- `$unset`
- `$group`
- `$sort`
- `$limit`
- `$skip`
- `$unwind`
- `$lookup`
- `$facet`
- `$count`

### `$lookup`

Permette una forma di join tra collection.

```javascript
db.orders.aggregate([
  {
    $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
    }
  }
])
```

Attenzione: usare MongoDB come se fosse un RDBMS pieno di JOIN spesso indica che il modello dati non è stato progettato bene per i pattern di accesso.

---

# 8. Indexes — argomento fondamentale da Senior

Un indice accelera le query evitando, quando possibile, di scansionare tutti i documenti.

Creazione:

```javascript
db.users.createIndex({ email: 1 })
```

Compound index:

```javascript
db.orders.createIndex({
  customerId: 1,
  createdAt: -1
})
```

Query:

```javascript
db.orders.find({ customerId: "C1" })
  .sort({ createdAt: -1 })
```

L'indice `{ customerId: 1, createdAt: -1 }` è adatto a questo pattern.

## ESR Rule
Quando si progettano compound index, una regola pratica importante è **ESR**:

- **E — Equality**
- **S — Sort**
- **R — Range**

Esempio:

```javascript
db.orders.createIndex({
  customerId: 1,
  status: 1,
  createdAt: -1
})
```

se il pattern applicativo è:

```javascript
db.orders.find({
  customerId: "C1",
  status: "PAID"
}).sort({ createdAt: -1 })
```

---

# 9. Explain e query optimization

Non ottimizzare "a intuito". Analizzare il piano:

```javascript
db.orders.find({
  customerId: "C1",
  status: "PAID"
}).explain("executionStats")
```

Indicatori importanti:

- `executionTimeMillis`
- `totalDocsExamined`
- `totalKeysExamined`
- `nReturned`
- `IXSCAN`
- `COLLSCAN`

### COLLSCAN

```text
Query
 ↓
COLLSCAN
 ↓
Scansione collection
 ↓
Filtra documenti
```

Può essere costoso su collection grandi.

### IXSCAN

```text
Query
 ↓
Index
 ↓
Documenti rilevanti
```

Non significa automaticamente che la query sia ottimale: bisogna verificare cardinalità, documenti esaminati e dati restituiti.

### Regola pratica

> Una query veloce non è quella che "usa un indice" in astratto, ma quella che esamina il minor lavoro necessario per produrre il risultato richiesto.

---

# 10. Covered Query

Una query può essere particolarmente efficiente quando l'indice contiene tutti i campi necessari alla ricerca e alla proiezione.

Esempio:

```javascript
db.users.createIndex({
  email: 1,
  name: 1
})
```

```javascript
db.users.find(
  { email: "a@company.com" },
  { name: 1, _id: 0 }
)
```

In questo caso il database può evitare di leggere il documento completo se il piano può soddisfare la query direttamente dall'indice.

---

# 11. Performance: principi fondamentali

## 11.1 Progettare il modello in base alle query

Prima domanda:

> **Come verranno letti i dati?**

Non:

> "Come normalizzo queste tabelle?"

Definire i principali access pattern:

```text
GET customer by id
GET customer orders
GET latest orders
GET orders by status
GET product by SKU
```

Poi progettare documenti e indici per questi pattern.

## 11.2 Evitare documenti giganteschi

Documenti enormi aumentano:

- I/O;
- memoria;
- network traffic;
- costo delle operazioni di update;
- pressione sul working set.

MongoDB impone inoltre un limite di dimensione per singolo documento; non bisogna progettare un aggregate che cresca senza controllo.

Per collection/array potenzialmente illimitati valutare referencing o bucket pattern.

## 11.3 Projection

Restituire solo ciò che serve:

```javascript
db.orders.find(
  { customerId: "C1" },
  { orderId: 1, total: 1, status: 1 }
)
```

Riduce dati letti e trasferiti.

## 11.4 Pagination

Evitare pagine profonde con grandi `skip` quando il dataset è enorme.

Approccio tradizionale:

```javascript
db.orders.find({})
  .sort({ createdAt: -1 })
  .skip(100000)
  .limit(50)
```

Può diventare costoso perché il database deve attraversare molte entry prima di arrivare alla pagina richiesta.

Preferire spesso **range/cursor pagination**:

```javascript
db.orders.find({
  createdAt: { $lt: lastSeenDate }
})
.sort({ createdAt: -1 })
.limit(50)
```

In produzione usare un cursore stabile, spesso combinando timestamp e `_id` per gestire valori duplicati.

---

# 12. Ottimizzazione dello spazio

Performance e spazio sono collegati ma non sono lo stesso problema.

## Ridurre la dimensione dei documenti

- evitare duplicazioni inutili;
- usare nomi campo ragionevoli;
- evitare array illimitati;
- non salvare dati che possono essere ricalcolati se non servono;
- scegliere correttamente il tipo BSON;
- usare referencing quando la duplicazione è eccessiva.

Attenzione: abbreviare artificialmente tutti i field name può ridurre spazio, ma peggiorare drasticamente leggibilità e manutenibilità. Il trade-off va valutato sui dataset reali.

## Indici = spazio aggiuntivo

Ogni indice occupa storage e memoria.

Un numero eccessivo di indici comporta:

- maggiore occupazione disco;
- maggiore working set;
- costi di write più elevati;
- tempi di insert/update maggiori.

Quindi:

> **Non creare un indice per ogni query immaginabile. Creare gli indici necessari per i workload reali e misurarne il beneficio.**

Analizzare anche gli indici inutilizzati e valutare la loro rimozione.

---

# 13. WiredTiger, cache e working set

MongoDB utilizza **WiredTiger** come storage engine nelle installazioni moderne.

Concetti importanti:

- document-level concurrency;
- journaling;
- compression;
- cache;
- indexes;
- working set.

### Working set

Il working set è, in termini pratici, l'insieme dei dati e degli indici utilizzati frequentemente dall'applicazione.

Se il working set entra efficacemente nella memoria disponibile, le performance possono essere molto migliori rispetto a un workload che richiede continuamente accessi a storage.

Per questo un database può essere "grande 500 GB" ma avere performance eccellenti se il working set caldo è molto più piccolo.

---

# 14. Read Concern e Write Concern

MongoDB permette di controllare le garanzie di lettura e scrittura.

### Write Concern

Definisce quanto una scrittura deve essere confermata prima di essere considerata completata.

Esempio concettuale:

```javascript
db.collection.insertOne(
  document,
  { writeConcern: { w: "majority" } }
)
```

`w: "majority"` richiede conferma dalla maggioranza appropriata del replica set secondo le regole del sistema.

### Read Concern

Definisce le garanzie relative alla consistenza dei dati letti.

Per il colloquio è importante capire il trade-off:

```text
Più garanzie di consistenza
        ↕
Più latenza / minore disponibilità in alcuni scenari
```

La scelta deve dipendere dal requisito business.

---

# 15. Replica Set e High Availability

Un Replica Set contiene più nodi:

```text
          Primary
         /       \
        /         \
 Secondary       Secondary
```

Le scritture vengono normalmente gestite dal primary e replicate agli altri nodi.

Se il primary fallisce, il sistema può eleggere un nuovo primary.

Concetti da conoscere:

- election;
- replication;
- oplog;
- read preference;
- write concern;
- failover.

### Read preference

Può essere possibile indirizzare letture verso secondary, ma bisogna valutare il rischio di leggere dati non ancora replicati.

---

# 16. Sharding e scalabilità orizzontale

Lo sharding distribuisce i dati tra più shard.

```text
                 Router
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      Shard 1    Shard 2    Shard 3
```

La scelta della **shard key** è critica.

Una buona shard key dovrebbe considerare:

- cardinalità;
- distribuzione;
- frequenza delle query;
- possibilità di evitare hotspot;
- pattern di scrittura;
- necessità di targeting delle query.

Una shard key mal progettata può creare un singolo shard sovraccarico.

---

# 17. Atomicità e transazioni

MongoDB garantisce atomicità delle operazioni sul singolo documento.

Questo è uno dei motivi per cui il document modeling è importante.

```text
One document
     ↓
Atomic update
```

MongoDB supporta anche **multi-document transactions**.

Tuttavia non bisogna progettare tutto come se fosse un RDBMS tradizionale. Le transazioni distribuite/multi-document possono avere costi in termini di performance e complessità.

Domanda da Senior:

> "Quando useresti una transazione MongoDB?"

Risposta:

> Quando l'operazione richiede realmente atomicità su più documenti e non può essere modellata in modo efficace come singolo aggregate. Non la userei automaticamente per sostituire un buon document model.

---

# 18. MongoDB e Spring Boot

Con Spring Data MongoDB si può utilizzare un repository:

```java
public interface OrderRepository
        extends MongoRepository<Order, String> {

    List<Order> findByCustomerId(String customerId);

    List<Order> findByStatusOrderByCreatedAtDesc(String status);
}
```

Query custom:

```java
@Query("{ 'customerId': ?0, 'status': ?1 }")
List<Order> findOrders(String customerId, String status);
```

Per query più complesse si può usare `MongoTemplate` e l'Aggregation Framework.

### Attenzione

Come con JPA, non bisogna nascondere la complessità del database dietro repository apparentemente semplici. Bisogna conoscere:

- query generate;
- indici;
- cardinalità;
- execution plan;
- projection;
- pagination;
- gestione delle connessioni;
- serializzazione BSON/Java.

---

# 19. MongoDB vs PostgreSQL

| Caratteristica | MongoDB | PostgreSQL |
|---|---|---|
| Modello | Document | Relazionale |
| Schema | Flessibile | Strutturato |
| JOIN | Possibili, ma non core del modello | Fondamentali |
| Transactions | Supportate | Core feature |
| JSON | Nativo | JSON/JSONB |
| Horizontal scaling | Sharding | Possibile tramite soluzioni/strategie aggiuntive |
| Data model | Aggregate/document oriented | Relational |
| Ideale | Document/access-pattern driven | Relational/transaction-heavy |

La domanda non è "chi è migliore?", ma:

> **Quale modello rappresenta meglio il dominio e il workload?**

---

# 20. Problemi di performance tipici

### Problema 1 — Query senza indice

```javascript
db.orders.find({ customerId: "C1" })
```

Soluzione possibile:

```javascript
db.orders.createIndex({ customerId: 1 })
```

Ma verificare sempre con `explain("executionStats")`.

### Problema 2 — Troppi indici

Risultato:

```text
Read performance ↑
Write performance ↓
Storage usage ↑
Memory pressure ↑
```

### Problema 3 — Documenti troppo grandi

Possibili conseguenze:

- più I/O;
- maggiore memoria;
- maggiore network traffic;
- update costosi.

### Problema 4 — Array che cresce senza limite

Esempio pericoloso:

```json
{
  "customerId": "C1",
  "allTransactions": [ ... milioni di elementi ... ]
}
```

Meglio separare i dati o applicare pattern come bucket/reference.

### Problema 5 — `skip` enorme

Preferire cursor/range pagination.

### Problema 6 — `$lookup` massivi

Verificare schema, indici e cardinalità prima di introdurre pipeline che simulano numerose JOIN.

### Problema 7 — Hot shard

Una shard key con distribuzione sbilanciata può concentrare il traffico su uno shard.

---

# 21. Troubleshooting MongoDB

Approccio Senior:

```text
Sintomo
  ↓
Metriche
  ↓
Query lenta?
  ↓
explain("executionStats")
  ↓
Index / cardinalità / schema?
  ↓
CPU / memory / disk I/O?
  ↓
Replica lag?
  ↓
Connection pool?
  ↓
Rete?
  ↓
Fix + benchmark
```

Non aumentare semplicemente CPU/RAM senza capire il bottleneck.

Controllare almeno:

- latency;
- throughput;
- CPU;
- memory;
- disk I/O;
- cache/working set;
- query execution;
- connection pool;
- replication lag;
- lock/concurrency indicators;
- slow queries.

---

# 22. Domande da Senior Developer con risposte

## 1. Cos'è MongoDB e quando lo useresti?

MongoDB è un database NoSQL document-oriented che memorizza documenti BSON in collection. Lo userei quando il dominio è naturalmente documentale, lo schema evolve, le query lavorano bene su aggregate/documenti e sono importanti flessibilità e scalabilità orizzontale. Non lo sceglierei automaticamente per un dominio fortemente relazionale e transaction-heavy.

## 2. MongoDB è schema-less?

È più corretto parlare di **schema flexibility**. MongoDB non impone necessariamente uno schema rigido a livello di collection, ma l'applicazione dovrebbe comunque definire e validare un modello coerente. MongoDB supporta anche schema validation.

## 3. Embedding o referencing?

Embedding quando i dati appartengono allo stesso aggregate e vengono letti insieme. Referencing quando i dati sono condivisi, crescono molto, cambiano indipendentemente o non è conveniente duplicarli.

## 4. Perché gli indici migliorano le performance?

Permettono al database di individuare più rapidamente i documenti interessanti evitando, quando possibile, una scansione completa della collection. Hanno però un costo in storage, memoria e scritture.

## 5. Come analizzi una query lenta?

Uso `explain("executionStats")` e guardo `executionTimeMillis`, `nReturned`, `totalDocsExamined`, `totalKeysExamined` e il piano (`IXSCAN`/`COLLSCAN`). Poi verifico schema, indice, cardinalità, projection e workload reale.

## 6. Cos'è un compound index?

È un indice su più campi. L'ordine delle chiavi è fondamentale perché determina quali pattern di query possono sfruttarlo efficacemente.

## 7. Cosa significa ESR?

Equality, Sort, Range. È una regola pratica per ordinare i campi di un compound index in molti workload: prima equality, poi sort e range, valutando sempre il caso reale e il query planner.

## 8. Perché troppi indici possono essere dannosi?

Occupano spazio e memoria e devono essere aggiornati durante insert/update/delete. Possono quindi peggiorare il write throughput e aumentare la pressione sul working set.

## 9. Come riduci l'occupazione di spazio?

Riducendo duplicazioni inutili, evitando documenti/array giganteschi, scegliendo tipi BSON appropriati, eliminando indici inutilizzati e usando embedding/reference in base al workload. Bisogna misurare: ottimizzare lo spazio può avere trade-off sulle performance e sulla semplicità.

## 10. Perché `skip` può diventare lento?

Con offset elevati il database deve attraversare molte entry prima di restituire i risultati. Per dataset grandi preferisco cursor/range pagination basata su un indice.

## 11. MongoDB supporta le transazioni?

Sì, supporta transazioni multi-documento. Tuttavia il modello ideale resta quello in cui un aggregate può essere aggiornato atomicamente come documento quando possibile. Le transazioni multi-documento vanno usate quando sono realmente necessarie.

## 12. Come funziona la replica?

Un Replica Set contiene un primary e secondary. Le scritture vengono normalmente effettuate sul primary e replicate. In caso di failure il cluster può eleggere un nuovo primary.

## 13. Read da secondary: quali rischi?

Possibile lettura di dati non ancora replicati, quindi stale reads. Bisogna scegliere read preference e read concern in funzione dei requisiti di consistenza.

## 14. Cos'è lo sharding?

È la distribuzione dei dati su più shard per scalare orizzontalmente. La shard key è critica perché determina distribuzione e routing delle operazioni.

## 15. Come scegli una shard key?

Analizzo cardinalità, distribuzione, query pattern, frequenza delle scritture, possibilità di hotspot e necessità di targeted queries. Non scelgo la shard key guardando solo la cardinalità.

## 16. MongoDB è sempre più veloce di PostgreSQL?

No. Le performance dipendono da workload, schema, query, indici, dataset e infrastruttura. Il database deve essere scelto in base ai requisiti del dominio.

## 17. Come modelleresti un e-commerce?

Dipende dagli access pattern. Un ordine può essere un documento con gli item embedded perché rappresentano lo snapshot dell'ordine. Catalogo e customer profile possono essere separati se hanno lifecycle indipendenti. Progetterei gli indici in base a query come ricerca ordine per customer, stato e data.

## 18. Come gestiresti milioni di ordini?

Definirei access pattern, indici compound, pagination cursor-based, retention/archiving, replica set e valuterei sharding solo quando il volume e il workload lo richiedono. Monitorerei working set, I/O, query latency e replication lag.

## 19. Come ridurresti la latenza di una API che legge MongoDB?

Misurerei prima il bottleneck. Poi valuterei index, projection, query shape, document size, connection pool, network, cache e pagination. Non introdurrei Redis automaticamente senza sapere se MongoDB è realmente il collo di bottiglia.

## 20. Come gestisci dati che crescono senza limite?

Non li metterei in un singolo documento. Valuterei collection separate, referencing, bucket pattern, time-series collections quando appropriate e retention/archiving.

## 21. Cosa significa covered query?

Una query è covered quando l'indice contiene tutti i dati necessari per soddisfare filtro e projection, consentendo potenzialmente di evitare il fetch del documento.

## 22. `$lookup` sostituisce i JOIN SQL?

Può effettuare una forma di join, ma non significa che MongoDB debba essere modellato come un RDBMS. Se l'applicazione usa continuamente `$lookup` complessi, bisogna verificare se document model e access pattern sono stati progettati correttamente.

## 23. Come gestisci la consistenza in MongoDB?

Valuto replica, write concern, read concern, read preference e necessità di transazioni. La consistenza è una decisione architetturale legata al requisito business.

## 24. Come fai troubleshooting di una query lenta in produzione?

Parto da metriche e slow query, riproduco il pattern in ambiente controllato, analizzo `explain("executionStats")`, verifico gli indici e confronto `docsExamined`/`keysExamined` con `nReturned`. Poi modifico query/index/schema e misuro nuovamente.

---

# 23. Scenario da colloquio: progettare MongoDB per 100 milioni di documenti

Domanda:

> Hai 100 milioni di ordini. Devi mostrare gli ultimi 50 ordini di un cliente e filtrare per stato. Come progetti MongoDB?

### Risposta ragionata

1. Identifico il query pattern:

```text
customerId + status + createdAt DESC
```

2. Valuto il modello documento.

3. Creo un compound index coerente con il pattern:

```javascript
db.orders.createIndex({
  customerId: 1,
  status: 1,
  createdAt: -1
})
```

4. Uso projection se l'API non necessita del documento completo.

5. Uso cursor/range pagination invece di grandi `skip`.

6. Misuro con:

```javascript
db.orders.find({
  customerId: "C1",
  status: "PAID"
})
.sort({ createdAt: -1 })
.limit(50)
.explain("executionStats")
```

7. Se il dataset e il throughput superano le capacità del singolo replica set, valuto sharding.

8. Scelgo la shard key analizzando il workload reale e il rischio di hotspot.

9. Monitoro:

- query latency;
- CPU;
- memory;
- disk I/O;
- working set;
- replication lag;
- connection pool;
- distribution degli shard.

### Cosa NON rispondere

> "Metto un indice e faccio sharding."

Una risposta Senior deve spiegare **perché**, partendo da workload, access pattern, misurazioni e requisiti non funzionali.

---

# 24. Checklist MongoDB per colloquio

Prima del colloquio dovresti saper spiegare senza esitazione:

- [ ] Document model
- [ ] BSON
- [ ] ObjectId
- [ ] Collection
- [ ] Embedding vs referencing
- [ ] CRUD
- [ ] Query operators
- [ ] Projection
- [ ] Array e `$elemMatch`
- [ ] Aggregation Framework
- [ ] `$lookup`
- [ ] Index
- [ ] Compound index
- [ ] ESR
- [ ] `explain("executionStats")`
- [ ] `COLLSCAN` vs `IXSCAN`
- [ ] Covered query
- [ ] Pagination e cursor pagination
- [ ] Document size e array illimitati
- [ ] Storage/index overhead
- [ ] WiredTiger
- [ ] Working set
- [ ] Read concern
- [ ] Write concern
- [ ] Read preference
- [ ] Replica Set
- [ ] Failover/election
- [ ] Sharding
- [ ] Shard key
- [ ] Transactions
- [ ] MongoDB vs PostgreSQL
- [ ] Spring Data MongoDB
- [ ] Troubleshooting query lente

## Regola Senior

> **MongoDB non va scelto perché "NoSQL è più veloce". Va scelto quando il document model, gli access pattern, la consistenza richiesta e le caratteristiche di scalabilità del workload rendono MongoDB una scelta architetturalmente appropriata.**
