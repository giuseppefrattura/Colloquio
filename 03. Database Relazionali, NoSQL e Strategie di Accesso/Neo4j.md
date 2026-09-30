# Neo4j — Guida da Senior Developer

## 1. Cos'è Neo4j

**Neo4j** è un database **graph-native** progettato per rappresentare e interrogare dati in cui le relazioni tra le entità sono una parte fondamentale del dominio.

Il modello principale è:

```text
Node ── Relationship ──> Node
```

Esempio:

```text
(Alice) ──[:FRIEND_OF]──> (Bob)
   │                         │
   └──[:WORKS_AT]──> (Acme)  └──[:WORKS_AT]──> (Acme)
```

A differenza di un database relazionale, dove le relazioni vengono normalmente risolte tramite JOIN, in Neo4j le relazioni sono elementi nativi del modello.

---

# 2. Concetti fondamentali

## Node

Rappresenta un'entità.

```text
(:Person)
(:Company)
(:Product)
```

Un nodo può avere proprietà:

```cypher
CREATE (:Person {
    name: 'Mario Rossi',
    age: 40
})
```

## Label

Una label classifica un nodo:

```text
(:Person)
(:Customer)
(:Employee)
```

Lo stesso nodo può avere più label:

```text
(:Person:Employee)
```

## Relationship

Rappresenta una relazione tipizzata e direzionale:

```text
(:Person)-[:WORKS_AT]->(:Company)
```

Può avere proprietà:

```cypher
[:WORKS_AT {
    since: 2020,
    role: 'Developer'
}]
```

## Property

Sono coppie chiave/valore associate a node e relationship.

---

# 3. Quando usare Neo4j

Neo4j è particolarmente adatto quando il valore principale dell'applicazione deriva dalla **connessione tra i dati**.

Esempi:

- social network;
- recommendation engine;
- fraud detection;
- identity/access graph;
- knowledge graph;
- network/topology management;
- supply chain;
- dependency graph;
- route/path analysis;
- IT infrastructure graph;
- master data e relationship discovery;
- sistemi finanziari con relazioni complesse tra conti, persone e transazioni.

La domanda architetturale corretta è:

> **Le relazioni sono una parte primaria delle query e del valore del dominio?**

Se la risposta è sì, un graph database può essere molto interessante.

---

# 4. Quando NON usare Neo4j

Neo4j non è automaticamente migliore di PostgreSQL o MongoDB.

Un database relazionale può essere preferibile quando:

- i dati sono fortemente tabellari;
- le query sono principalmente aggregazioni e reporting SQL;
- il dominio non richiede traversal complessi;
- esistono forti requisiti relazionali e transazionali già ben rappresentati dal modello relazionale.

MongoDB può essere preferibile quando:

- il dato è principalmente documentale;
- le query lavorano su aggregate/documenti;
- le relazioni tra documenti non sono il centro del workload.

### Regola Senior

> **Non scegliere Neo4j perché "i dati hanno relazioni". Quasi tutti i dati reali hanno relazioni. Sceglilo quando le relazioni sono il principale pattern di accesso e le query richiedono traversal che diventerebbero complesse o inefficienti in un modello relazionale/documentale.**

---

# 5. Cypher

Il linguaggio principale per interrogare Neo4j è **Cypher**.

La sintassi rappresenta graficamente il pattern che vogliamo cercare.

```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p.name, c.name
```

Concettualmente:

```text
Person ──WORKS_AT──> Company
```

---

# 6. CRUD con Cypher

## CREATE

```cypher
CREATE (p:Person {
    name: 'Mario Rossi',
    age: 40
})
RETURN p
```

## MATCH

```cypher
MATCH (p:Person {name: 'Mario Rossi'})
RETURN p
```

## CREATE relationship

```cypher
MATCH (p:Person {name: 'Mario Rossi'})
MATCH (c:Company {name: 'Acme'})
CREATE (p)-[:WORKS_AT]->(c)
```

## UPDATE

```cypher
MATCH (p:Person {name: 'Mario Rossi'})
SET p.age = 41
RETURN p
```

## REMOVE

```cypher
MATCH (p:Person {name: 'Mario Rossi'})
REMOVE p.age
RETURN p
```

## DELETE

```cypher
MATCH (p:Person {name: 'Mario Rossi'})
DELETE p
```

Per cancellare un nodo con relazioni occorre gestire prima le relazioni, oppure usare `DETACH DELETE` quando appropriato:

```cypher
MATCH (p:Person {name: 'Mario Rossi'})
DETACH DELETE p
```

---

# 7. MERGE vs CREATE

`CREATE` crea sempre il pattern richiesto.

`MERGE` cerca il pattern e lo crea se non esiste.

```cypher
MERGE (p:Person {email: 'mario@example.com'})
RETURN p
```

È molto utile per operazioni di upsert, ma bisogna progettare correttamente le proprietà utilizzate per identificare l'entità e gli indici/constraint associati.

---

# 8. Query sulle relazioni

Trova gli amici di Mario:

```cypher
MATCH (m:Person {name: 'Mario'})-[:FRIEND_OF]->(friend:Person)
RETURN friend
```

Trova gli amici a due livelli:

```cypher
MATCH (m:Person {name: 'Mario'})
      -[:FRIEND_OF*1..2]->(friend:Person)
RETURN DISTINCT friend
```

Il traversal è uno dei punti in cui Neo4j può essere molto efficace.

---

# 9. Shortest path

Un caso tipico dei graph database è trovare un percorso:

```cypher
MATCH (a:Person {name: 'Mario'}),
      (b:Person {name: 'Luigi'})
MATCH p = shortestPath(
    (a)-[:FRIEND_OF*]-(b)
)
RETURN p
```

La disponibilità e le caratteristiche delle funzioni di path dipendono dalla versione e dal tipo di query; in produzione è importante verificare sempre il piano e i limiti del traversal.

---

# 10. Pattern matching

Cypher permette di descrivere pattern complessi:

```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.industry = 'Finance'
RETURN p.name
```

Oppure:

```cypher
MATCH (p:Person)-[:BOUGHT]->(product:Product)
      <-[:BOUGHT]-(other:Person)
WHERE p.name = 'Mario'
RETURN DISTINCT other
```

Questo può esprimere facilmente query di raccomandazione basate sul comportamento di altri utenti.

---

# 11. Indici e constraint

Gli indici sono importanti soprattutto per trovare rapidamente i punti di ingresso del traversal.

Esempio:

```cypher
CREATE INDEX person_email_index
FOR (p:Person)
ON (p.email)
```

Constraint di unicità:

```cypher
CREATE CONSTRAINT person_email_unique
FOR (p:Person)
REQUIRE p.email IS UNIQUE
```

In una query:

```cypher
MATCH (p:Person {email: 'mario@example.com'})
RETURN p
```

l'indice può rendere efficiente il lookup iniziale.

### Concetto importante

Un graph database non significa "non servono indici".

Gli indici sono fondamentali per evitare di cercare inutilmente tra tutti i nodi quando si determina il punto di partenza del traversal.

---

# 12. Query optimization

Neo4j mette a disposizione `EXPLAIN` e `PROFILE`.

```cypher
EXPLAIN
MATCH (p:Person {email: 'mario@example.com'})
RETURN p
```

`EXPLAIN` permette di analizzare il piano senza eseguire la query.

```cypher
PROFILE
MATCH (p:Person {email: 'mario@example.com'})
RETURN p
```

`PROFILE` esegue la query e fornisce informazioni sul lavoro effettuato dai vari operatori.

Un approccio Senior è:

```text
Query lenta
   ↓
PROFILE
   ↓
Identifica il costoso operator
   ↓
Verifica starting point
   ↓
Verifica index/constraint
   ↓
Riduci traversal inutile
   ↓
Limita cardinalità
   ↓
Misura nuovamente
```

---

# 13. Il problema delle cardinalità

Un errore comune è partire da un nodo con un numero enorme di relazioni e attraversare il grafo senza limiti.

Esempio potenzialmente problematico:

```cypher
MATCH (p:Person)-[:KNOWS*1..10]->(x)
RETURN x
```

La quantità di percorsi possibili può crescere rapidamente.

Meglio:

- limitare la profondità;
- filtrare presto;
- scegliere un starting point selettivo;
- usare indici/constraint;
- evitare traversals inutilmente esplosivi;
- usare `PROFILE`.

---

# 14. Modellazione: node vs relationship

Domanda importante:

> "Quando qualcosa deve essere un nodo e quando una relationship?"

Se un'entità ha identità e viene interrogata autonomamente, spesso è un **node**.

```text
Person
Company
Product
```

Se rappresenta principalmente una connessione tra due entità, spesso è una **relationship**.

```text
WORKS_AT
BOUGHT
FRIEND_OF
```

Se la relazione possiede molte proprietà o deve essere interrogata come entità autonoma, può essere opportuno rivalutare il modello e considerare se una struttura esplicita a nodi rappresenti meglio il dominio.

---

# 15. Modellazione temporale

Esempio:

```text
(Person)-[:WORKED_AT {from: 2020, to: 2024}]->(Company)
```

Permette query come:

```cypher
MATCH (p:Person)-[r:WORKED_AT]->(c:Company)
WHERE r.from <= 2022
  AND (r.to IS NULL OR r.to >= 2022)
RETURN p, c
```

È utile per rappresentare la storia delle relazioni.

---

# 16. Transazioni e atomicità

Neo4j supporta transazioni ACID.

Questo permette di modificare più nodi e relazioni come una singola unità transazionale.

Esempio concettuale:

```text
Create Person
     +
Create Company
     +
Create WORKS_AT
     ↓
   COMMIT
```

Oppure rollback dell'intera operazione se qualcosa fallisce.

La gestione delle transazioni deve comunque tenere conto di durata, concorrenza e dimensione dell'operazione.

---

# 17. Concorrenza e locking

In scenari concorrenti, Neo4j deve garantire consistenza delle modifiche.

Un problema Senior tipico è chiedere:

> "Cosa succede se due richieste modificano contemporaneamente la stessa entità?"

La risposta deve partire da:

- natura della transazione;
- proprietà modificate;
- isolation/locking;
- eventuale retry;
- idempotenza dell'operazione.

Non assumere che qualsiasi operazione concorrente sia automaticamente priva di conflitti solo perché si usa un graph database.

---

# 18. Neo4j e microservizi

Neo4j può essere utilizzato come database di un singolo microservizio:

```text
                  ┌── PostgreSQL
Order Service ────┤
                  └── Kafka

Recommendation Service
        │
        ▼
     Neo4j
```

Un servizio di recommendation potrebbe usare Neo4j per il grafo delle relazioni mentre gli ordini rimangono in PostgreSQL.

È importante evitare di introdurre Neo4j come database condiviso da tutti i microservizi solo perché contiene relazioni.

Principio:

> **Ogni bounded context dovrebbe mantenere ownership dei propri dati.**

---

# 19. Integrazione con Spring Boot

Neo4j si integra con Spring tramite **Spring Data Neo4j**.

Esempio concettuale:

```java
@Node
public class Person {

    @Id
    private String id;

    private String name;
}
```

Repository:

```java
public interface PersonRepository
        extends Neo4jRepository<Person, String> {

    Optional<Person> findByName(String name);
}
```

Query custom:

```java
@Query("""
    MATCH (p:Person)-[:WORKS_AT]->(c:Company)
    WHERE c.name = $company
    RETURN p
    """)
List<Person> findEmployees(String company);
```

Spring Data Neo4j permette di lavorare con mapping object-graph, repository e query Cypher.

---

# 20. Neo4j e REST API

Un'architettura tipica:

```text
Client
  ↓
REST API
  ↓
Spring Boot
  ↓
Service
  ↓
Repository / Cypher
  ↓
Neo4j
```

Esempio:

```http
GET /customers/123/recommendations
```

Il service potrebbe eseguire una query Cypher per trovare prodotti acquistati da utenti con comportamenti simili.

Il client non dovrebbe conoscere direttamente la struttura del grafo.

---

# 21. Neo4j e Kafka

Una combinazione interessante in architetture event-driven:

```text
Order Service
    │
    ├── PostgreSQL
    │
    └── Kafka
          │
          ▼
Recommendation Service
          │
          ▼
        Neo4j
```

Un evento:

```json
{
  "type": "ORDER_COMPLETED",
  "customerId": "C1",
  "productId": "P10"
}
```

può aggiornare il grafo:

```text
(Customer)-[:BOUGHT]->(Product)
```

### Attenzione

L'integrazione asincrona introduce problemi come:

- duplicate events;
- ordering;
- eventual consistency;
- retry;
- consumer failure;
- idempotency.

Il consumer deve essere progettato per gestire questi casi.

---

# 22. Neo4j e CDC / Event-driven architecture

Un database relazionale può essere il system of record mentre Neo4j è una **read model specializzata**.

```text
                    ┌── PostgreSQL
                    │    System of Record
                    │
Domain Service ──────┤
                    │
                    └── Outbox → Kafka
                                  │
                                  ▼
                           Graph Projector
                                  │
                                  ▼
                                Neo4j
```

Questo approccio è particolarmente interessante quando il grafo viene usato per query e analisi relazionali ma non deve diventare il proprietario del dato transazionale principale.

---

# 23. Neo4j come Read Model / CQRS

Neo4j può essere usato come read model specializzato:

```text
Command side
    ↓
PostgreSQL
    ↓
Events
    ↓
Neo4j projection
    ↓
Graph queries
```

Vantaggi:

- query grafiche ottimizzate;
- separazione tra write model e read model;
- possibilità di progettare il grafo specificamente per le query.

Svantaggi:

- eventual consistency;
- pipeline di sincronizzazione;
- gestione dei failure;
- complessità operativa.

---

# 24. Caching

Neo4j non sostituisce automaticamente Redis o una cache applicativa.

Un'architettura può essere:

```text
API
 ↓
Redis
 ↓ cache miss
Neo4j
```

La cache è utile per query costose e altamente ripetitive, ma bisogna gestire:

- invalidation;
- TTL;
- stale data;
- cache stampede;
- memory usage.

---

# 25. Backup e disaster recovery

In produzione bisogna definire:

- RPO;
- RTO;
- backup frequency;
- retention;
- restore procedure;
- replica strategy;
- disaster recovery.

Una replica non deve essere automaticamente considerata un backup.

È importante verificare periodicamente che i backup siano realmente ripristinabili.

---

# 26. Alta disponibilità e clustering

In ambienti production bisogna valutare architetture clusterizzate e ridondanza.

```text
        Application
             │
        Neo4j cluster
       /      |      \
    Node    Node     Node
```

Gli aspetti da considerare includono:

- failure handling;
- quorum;
- routing;
- driver configuration;
- network partition;
- backup;
- monitoring.

La topologia esatta dipende dalla versione/edizione Neo4j e dal deployment scelto; in un colloquio è importante ragionare sui requisiti invece di memorizzare una singola topologia.

---

# 27. Casi limite e problemi reali

## Traversal esplosivo

Una query con molte relazioni e profondità elevata può produrre un numero enorme di percorsi.

Soluzione:

- limitare depth;
- filtrare presto;
- ridurre cardinalità;
- profilare.

## Supernode

Un nodo con milioni di relazioni può diventare problematico.

Esempio:

```text
                 ┌─ Product
                 ├─ Product
                 ├─ Product
Customer ────────┼─ Product
                 ├─ Product
                 └─ ... milioni
```

Possibili strategie:

- ripensare il modello;
- introdurre nodi intermedi;
- partizionare il grafo;
- usare aggregati/materialized relationships quando appropriato.

## Dati altamente dinamici

Se le relazioni cambiano continuamente e il sistema richiede query fortemente consistenti, bisogna valutare attentamente transaction throughput e contention.

## Query troppo generiche

Traversal generici su grandi porzioni del grafo possono consumare molta CPU e memoria.

## Graph usato come document store

Se le query sono principalmente:

```text
get entity by id
get entity by status
get latest records
```

probabilmente Neo4j non è la scelta naturale.

---

# 28. Security

Aspetti da considerare:

- autenticazione;
- autorizzazione;
- TLS;
- gestione delle credenziali;
- least privilege;
- protezione delle API;
- audit;
- gestione dei secret.

L'applicazione Spring non dovrebbe costruire query Cypher concatenando input utente.

Da evitare:

```java
String query = "MATCH (p:Person {name: '" + name + "'}) RETURN p";
```

Preferire parametri:

```cypher
MATCH (p:Person {name: $name})
RETURN p
```

con:

```text
{name: userInput}
```

Questo migliora sicurezza e riuso del piano di query.

---

# 29. Monitoring e troubleshooting

Metriche importanti:

- query latency;
- throughput;
- CPU;
- memory;
- page cache;
- transaction rate;
- failed transactions;
- connection pool;
- cluster health;
- replication/cluster state;
- slow queries.

Approccio:

```text
API latency ↑
      ↓
Trace
      ↓
Neo4j query lenta?
      ↓
PROFILE
      ↓
Cardinality / index / traversal
      ↓
Fix
      ↓
Benchmark
```

L'observability dovrebbe integrare:

- logs;
- metrics;
- distributed tracing.

---

# 30. Neo4j vs PostgreSQL vs MongoDB

| Caratteristica | Neo4j | PostgreSQL | MongoDB |
|---|---|---|---|
| Modello | Graph | Relazionale | Document |
| Relazioni | Core | JOIN | Secondarie |
| Traversal | Eccellente | Possibile, ma non core | Possibile, ma non core |
| Schema | Graph model | Relazionale | Flexible document model |
| Query | Cypher | SQL | MongoDB Query Language |
| Transazioni | ACID | ACID | ACID, incl. multi-document |
| Caso tipico | Relationship-heavy | Transaction/reporting | Document/access-pattern driven |
| Recommendation | Ottimo | Possibile | Possibile |
| Fraud graph | Ottimo | Possibile ma spesso complesso | Possibile ma non naturale |

---

# 31. Domande da Senior Developer

## 1. Cos'è Neo4j?

È un database graph-native che rappresenta dati come nodi, relazioni e proprietà. È particolarmente adatto a domini in cui le relazioni sono centrali e le query richiedono traversal del grafo.

## 2. Quando sceglieresti Neo4j invece di PostgreSQL?

Quando il workload è dominato da traversal e relationship queries, per esempio recommendation, fraud detection o dependency analysis. Se il workload è principalmente CRUD relazionale e reporting SQL, PostgreSQL può essere più appropriato.

## 3. Perché un graph database può essere vantaggioso per le relazioni?

Perché le relazioni sono primitive del modello e possono essere attraversate direttamente, mentre in un modello relazionale molti livelli di relazione possono richiedere JOIN complessi.

## 4. Cos'è Cypher?

È il linguaggio dichiarativo utilizzato per descrivere pattern e operazioni sul grafo Neo4j.

## 5. Differenza tra node e relationship?

Un node rappresenta un'entità; una relationship rappresenta il legame tra due entità e può avere tipo, direzione e proprietà.

## 6. CREATE vs MERGE?

`CREATE` crea il pattern. `MERGE` cerca un pattern e lo crea se non esiste. `MERGE` è utile per upsert, ma deve essere progettato con identificatori e constraint appropriati.

## 7. Come ottimizzi una query Cypher?

Parto da `PROFILE`, verifico il starting point, gli indici/constraint, cardinalità, traversal depth e operatori costosi. Evito traversals troppo ampi e applico filtri il prima possibile.

## 8. Perché un indice è importante in Neo4j?

Per trovare rapidamente il punto di ingresso del traversal. L'indice non elimina il costo del traversal successivo, quindi bisogna ottimizzare anche la cardinalità delle relazioni attraversate.

## 9. Cos'è un supernode?

Un nodo con un numero enorme di relazioni. Può diventare un hotspot e rendere costosi traversal e aggiornamenti. Va gestito con un modello appropriato, eventuali nodi intermedi o strategie di partizionamento.

## 10. Perché un traversal può diventare molto costoso?

Perché il numero di percorsi può crescere rapidamente con branching factor e profondità. Un traversal `*1..10` su un grafo molto connesso può esplodere in cardinalità.

## 11. Neo4j è adatto a milioni di nodi?

Sì, il numero assoluto di nodi non è sufficiente per giudicare l'idoneità. Bisogna analizzare dimensione, densità del grafo, cardinalità delle relazioni, query pattern, memory/IO e deployment.

## 12. Neo4j è sempre più veloce di PostgreSQL per i grafi?

Non necessariamente in ogni query. Il vantaggio emerge soprattutto nei workload relationship-heavy e nei traversal complessi. Bisogna benchmarkare il caso reale.

## 13. Come integreresti Neo4j in una architettura a microservizi?

Lo assegnerei a un bounded context o servizio che possiede il relativo modello graph. Eviterei un database condiviso tra microservizi.

## 14. Come sincronizzeresti PostgreSQL e Neo4j?

Preferibilmente tramite eventi, per esempio Transactional Outbox → Kafka → Graph Projector → Neo4j. Questo introduce eventual consistency e richiede idempotenza e gestione dei retry.

## 15. Perché usare Neo4j come read model?

Per ottenere un modello ottimizzato per query grafiche senza spostare necessariamente il system of record transazionale. È un buon caso d'uso CQRS.

## 16. Neo4j può sostituire Redis?

No, sono sistemi con scopi differenti. Neo4j è un database graph; Redis è principalmente un in-memory data store/cache. Possono essere usati insieme.

## 17. Come gestiresti un evento Kafka duplicato che aggiorna Neo4j?

Il consumer deve essere idempotente. Userei un identificatore evento/event version e operazioni progettate per poter essere ripetute senza produrre inconsistenze.

## 18. Come gestiresti un consumer Kafka che aggiorna Neo4j ma fallisce dopo aver scritto?

Progetterei l'operazione in modo idempotente e userei retry/DLQ secondo il caso. Se l'evento è stato applicato ma l'ack non è arrivato, il retry deve poter rieseguire l'operazione senza duplicare lo stato.

## 19. Come affronteresti un supernode?

Prima misurerei il workload. Poi valuterei se il modello può essere modificato introducendo nodi intermedi, partizionando le relazioni o materializzando alcune informazioni. Non applicherei una soluzione senza capire il pattern di accesso.

## 20. Come proteggeresti Cypher da injection?

Usando query parametrizzate e non concatenando input utente direttamente nella query.

## 21. Neo4j supporta transazioni?

Sì. Le operazioni possono essere eseguite in transazioni ACID. Bisogna comunque gestire correttamente durata, concorrenza, retry e dimensione delle transazioni.

## 22. Come monitoreresti Neo4j in produzione?

Con metriche, log e tracing, osservando query latency, CPU, memory, cache, transaction throughput, connection pool, cluster health e query lente.

---

# 32. Scenario Senior: Recommendation Engine

### Requisito

Un e-commerce vuole:

> "Mostrami prodotti acquistati da clienti simili a me che io non ho ancora acquistato."

### Modello

```text
(Customer)-[:BOUGHT]->(Product)
```

Query concettuale:

```cypher
MATCH (me:Customer {id: $customerId})-[:BOUGHT]->(p:Product)
      <-[:BOUGHT]-(other:Customer)
MATCH (other)-[:BOUGHT]->(recommended:Product)
WHERE NOT (me)-[:BOUGHT]->(recommended)
RETURN recommended, count(*) AS score
ORDER BY score DESC
LIMIT 20
```

### Considerazioni Senior

Non basta scrivere la query.

Bisogna considerare:

- cardinalità dei clienti;
- clienti con milioni di acquisti;
- supernode sui prodotti molto popolari;
- caching delle recommendation;
- eventuale pre-calcolo;
- latency SLA;
- aggiornamento asincrono del grafo;
- eventual consistency;
- fallback se Neo4j non è disponibile.

Una possibile architettura:

```text
Order Service
    │
 PostgreSQL
    │
 Outbox
    │
 Kafka
    │
 Graph Projector
    │
 Neo4j
    │
 Recommendation Service
    │
 Redis
    │
 REST API
```

---

# 33. Checklist da colloquio

Dovresti saper spiegare:

- [ ] cos'è un graph database;
- [ ] Neo4j;
- [ ] node;
- [ ] relationship;
- [ ] label;
- [ ] property;
- [ ] Cypher;
- [ ] CREATE;
- [ ] MATCH;
- [ ] MERGE;
- [ ] DELETE / DETACH DELETE;
- [ ] pattern matching;
- [ ] variable-length paths;
- [ ] shortest path;
- [ ] index;
- [ ] constraint;
- [ ] EXPLAIN;
- [ ] PROFILE;
- [ ] cardinality;
- [ ] traversal explosion;
- [ ] supernode;
- [ ] transazioni;
- [ ] concorrenza;
- [ ] Spring Data Neo4j;
- [ ] Spring Boot integration;
- [ ] REST integration;
- [ ] Kafka integration;
- [ ] CQRS/read model;
- [ ] Transactional Outbox;
- [ ] eventual consistency;
- [ ] idempotenza;
- [ ] caching;
- [ ] security/Cypher injection;
- [ ] backup/DR;
- [ ] clustering/HA;
- [ ] monitoring;
- [ ] confronto Neo4j/PostgreSQL/MongoDB.

## Regola finale da Senior

> **Neo4j non è semplicemente "un database per dati collegati": è una scelta architetturale particolarmente interessante quando il grafo delle relazioni è parte integrante del dominio e delle query. La competenza Senior consiste nel saper progettare il modello, controllare cardinalità e traversal, ottimizzare le query e integrarlo correttamente nell'architettura complessiva, eventualmente come system of record o come read model specializzato.**
