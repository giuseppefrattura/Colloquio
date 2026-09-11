# 3. Database Relazionali, NoSQL e Strategie di Accesso ai Dati

## Cos'è e perché conta

In un'architettura enterprise (in particolare nel settore bancario, dei pagamenti digitali e dei servizi mission-critical), la gestione della persistenza è il pilastro su cui poggia l'intera affidabilità del business:
1. **Integrità assoluta del dato (ACID)**: Un errore di arrotondamento, una doppia spesa (*double spending*) o una mancata consistenza sul saldo di un conto possono causare perdite finanziarie dirette e sanzioni regolamentari.
2. **Architettura Polyglot Persistence**: Nei sistemi moderni non esiste un unico database "buono per tutto". L'architettura tipica combina RDBMS (Oracle/PostgreSQL) per il *Core Ledger Transazionale*, In-Memory Cache (Redis) per performance e rate limiting, Column-Family (Cassandra) per audit log immutabili ad altissimo volume e Motori di Ricerca (Elasticsearch) per analisi operativa e osservabilità.
3. **Strategie di accesso e concorrenza**: A livello Senior occorre dominare i meccanismi di locking, l'analisi degli Execution Plan, il connection pooling, il partizionamento e la transizione verso la *Data Isolation* e l'*Eventual Consistency* nei microservizi.

---

## 1. Fondamenti dei Database Relazionali (RDBMS)

### Proprietà ACID
* **Atomicità (Atomicity)**: La transazione è un'unità indivisibile (*All or Nothing*). Se una qualsiasi operazione fallisce (es. il credito sul conto beneficiario fallisce dopo l'addebito sul conto ordinante), viene eseguito il `ROLLBACK` completo.
* **Consistenza (Consistency)**: La transazione porta il database da uno stato valido a un altro stato valido, rispettando tutti i vincoli di integrità (chiavi primarie, foreign key, vincoli `CHECK`, trigger).
* **Isolamento (Isolation)**: L'esecuzione concorrente di più transazioni non deve produrre anomalie o stati incoerenti.
* **Durabilità (Durability)**: Una volta eseguito il `COMMIT`, le modifiche sono permanenti e persistite su storage non volatile (grazie a meccanismi come il Write-Ahead Logging / Redo Log), resistendo anche a crash improvvisi del server.

---

### Livelli di Isolamento SQL e Anomalie di Concorrenza

Lo standard ANSI/ISO SQL definisce quattro livelli di isolamento per bilanciare consistenza e concorrenza:

```
Più Consistenza / Meno Concorrenza (Lock più pesanti)
 ▲  SERIALIZABLE          (Nessuna anomalia ammessa)
 │  REPEATABLE READ       (Previene Dirty Read e Non-Repeatable Read)
 │  READ COMMITTED        (Default Oracle/PostgreSQL - Previene solo Dirty Read)
 ▼  READ UNCOMMITTED      (Permette Dirty Read - Sconsigliato in ambito transazionale)
Meno Consistenza / Più Concorrenza (Massimo Throughput)
```

#### Le anomalie prevenute:
1. **Dirty Read (Lettura sporca)**: La transazione $T_1$ legge modifiche non ancora committate da $T_2$. Se $T_2$ fa rollback, i dati letti da $T_1$ non sono mai esistiti.
2. **Non-Repeatable Read (Lettura non ripetibile)**: $T_1$ rilegge lo stesso record e trova valori modificati da $T_2$ che nel frattempo ha committato.
3. **Phantom Read (Lettura fantasma)**: $T_1$ esegue una query con filtro per range (es. `WHERE balance > 1000`), $T_2$ inserisce o cancella record corrispondenti al filtro e committa; $T_1$ rieseguendo la query trova un set di righe differente.

| Livello di Isolamento | Dirty Read | Non-Repeatable Read | Phantom Read | Note di Implementazione |
| :--- | :---: | :---: | :---: | :--- |
| **READ UNCOMMITTED** | Sì | Sì | Sì | Nessun lock in lettura, dirty reads possibili. |
| **READ COMMITTED** | No | Sì | Sì | **Default in Oracle e PostgreSQL**. Usa MVCC (Snapshot di lettura alla query). |
| **REPEATABLE READ** | No | No | Sì (No in InnoDB/Postgres) | Default in MySQL InnoDB. Snapshot all'inizio dell'intera transazione. |
| **SERIALIZABLE** | No | No | No | Esecuzione equivalente a quella sequenziale (Lock predittivi o Serializable Snapshot Isolation). |

---

### Concorrenza e Locking: Optimistic vs Pessimistic

Nelle applicazioni transazionali ad alta frequenza (es. settlement, autorizzazione pagamenti, prenotazione fondi), la gestione della concorrenza sui record condivisi è fondamentale.

```
                           Gestione della Concorrenza
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
   Locking Ottimistico                                  Locking Pessimistico
   • Nessun blocco fisico sul DB                        • Blocco fisico della riga/tabella
   • Controllo versione al COMMIT                       • SELECT ... FOR UPDATE
   • Ideale: Bassa contesa, letture frequenti           • Ideale: Alta contesa, transazioni critiche
   • JPA: @Version (Long o Timestamp)                   • JPA: LockModeType.PESSIMISTIC_WRITE
```

#### 1. Locking Ottimistico (*Optimistic Locking*)
* **Funzionamento**: Nessun lock a livello di riga sul database. L'entità possiede una colonna di versione (`@Version` in JPA). In fase di update, la query verifica che la versione sia ancora invariata:
  ```sql
  UPDATE accounts SET balance = 450.00, version = version + 1 
  WHERE id = 123 AND version = 2;
  ```
  Se un'altra transazione ha già modificato la versione, l'update aggiorna 0 righe e scatta una `OptimisticLockException` (gestibile con retry applicativo).
* **Quando usarlo**: Bassa o media contesa, flussi guidati dall'utente (es. modifica anagrafica), dove bloccare le risorse per lungo tempo sarebbe inefficiente.

#### 2. Locking Pessimistico (*Pessimistic Locking*)
* **Funzionamento**: Viene acquisito un lock esclusivo sulla riga tramite SQL al momento della lettura:
  ```sql
  SELECT * FROM accounts WHERE id = 123 FOR UPDATE;
  ```
  In JPA:
  ```java
  @Lock(LockModeType.PESSIMISTIC_WRITE)
  @Query("SELECT a FROM Account a WHERE a.id = :id")
  Optional<Account> findByIdForUpdate(@Param("id") Long id);
  ```
* **Quando usarlo**: **Alta contesa su saldi finanziari**, settlement batch concorrenti, code di prelievo fondi dove il fallimento dell'update a posteriori non è accettabile e si preferisce serializzare l'accesso.
* **Rischi**: Possibili *Deadlock* (risolvibili ordinando sempre le risorse da bloccare nello stesso ordine deterministico o impostando `FOR UPDATE WAIT 5` / `FOR UPDATE NOWAIT`) e riduzione del throughput globale.

---

## 2. Oracle Database & SQL Avanzato

Oracle Database è storicamente il motore RDBMS di riferimento nel settore bancario per la sua scalabilità, alta affidabilità (**Oracle RAC** - Real Application Clusters), disaster recovery (**Data Guard**) e potenza del motore SQL/PL-SQL.

### SQL Avanzato

#### 1. Window Functions (Funzioni Analitiche)
Consentono di eseguire calcoli aggregati su un set di righe correlate (*Window*) senza collassare il risultato in una singola riga (a differenza di `GROUP BY`).

* **Calcolo Saldo Progressivo (Running Balance)**:
  ```sql
  SELECT 
      transaction_id,
      account_id,
      amount,
      booking_date,
      SUM(amount) OVER (
          PARTITION BY account_id 
          ORDER BY booking_date, transaction_id
          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
      ) AS running_balance
  FROM transactions
  WHERE account_id = :accountId;
  ```

* **Deduplica e Identificazione Ultimo Stato (`ROW_NUMBER`)**:
  ```sql
  WITH RankedTransactions AS (
      SELECT 
          id,
          idempotency_key,
          status,
          created_at,
          ROW_NUMBER() OVER (
              PARTITION BY idempotency_key 
              ORDER BY created_at DESC
          ) AS rn
      FROM transactions
  )
  SELECT id, idempotency_key, status, created_at
  FROM RankedTransactions
  WHERE rn = 1;
  ```

#### 2. Aggregazioni per Riconciliazione (`GROUP BY` + `HAVING`)
```sql
SELECT 
    circuit_code,
    TRUNC(settlement_date) AS settlement_day,
    COUNT(*) AS total_tx_count,
    SUM(amount) AS total_amount,
    SUM(CASE WHEN status = 'SETTLED' THEN amount ELSE 0 END) AS settled_amount
FROM settlement_records
GROUP BY circuit_code, TRUNC(settlement_date)
HAVING SUM(CASE WHEN status = 'REJECTED' THEN 1 ELSE 0 END) > 0;
```

---

### Execution Plan & Query Optimization

L'**Execution Plan** (piano di esecuzione) è l'albero di operazioni fisiche scelto dal **Cost-Based Optimizer (CBO)** di Oracle per eseguire la query con il costo computazionale (I/O, CPU, memoria) stimato più basso.

```
                  ┌───────────────────────────────┐
                  │          Query SQL            │
                  └───────────────┬───────────────┘
                                  ▼
                  ┌───────────────────────────────┐
                  │ Cost-Based Optimizer (CBO)    │
                  │ • Statistiche tabelle/indici  │
                  │ • Cardinalità stimata         │
                  │ • Vincoli (PK, FK)            │
                  └───────────────┬───────────────┘
                                  ▼
                  ┌───────────────────────────────┐
                  │    Execution Plan Scelto      │
                  └───────────────────────────────┘
```

#### Come generare e visualizzare il piano
```sql
-- 1. Generazione piano stimato
EXPLAIN PLAN FOR
SELECT * FROM transactions WHERE account_id = :accId AND status = 'PENDING';

-- 2. Visualizzazione piano stimato
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- 3. Visualizzazione del piano REALE (Runtime Statistics) dopo l'esecuzione
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));
```

#### Indicatori chiave da analizzare nell'Execution Plan:
1. **`TABLE ACCESS FULL` vs `INDEX RANGE SCAN` / `INDEX UNIQUE SCAN`**:
   * `TABLE ACCESS FULL` su tabelle da milioni di righe per una query puntuale indica la **mancanza di un indice**, un indice non selettivo o l'impossibilità di usarlo (es. funzioni sulla colonna nel `WHERE`).
   * *Eccezione*: Nei batch di settlement notturno che elaborano l'$80\%$ della tabella, il Full Table Scan con *Multi-Block Read* è più performante dell'accesso via indice.
2. **Cardinalità Stimata vs Reale (`E-Rows` vs `A-Rows`)**:
   * Se il CBO stima 10 righe ma a runtime ne arrivano 500.000, le statistiche sono obsolete. Si risolve aggiornandole:
     ```sql
     EXEC DBMS_STATS.GATHER_TABLE_STATS(ownname => 'PAYMENT_USER', tabname => 'TRANSACTIONS', estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE, cascade => TRUE);
     ```
3. **Tipologie di Join**:
   * **`NESTED LOOPS`**: Ottimale quando una tabella produce poche righe e l'altra ha un indice molto selettivo sulla chiave di join.
   * **`HASH JOIN`**: Ottimale per unire grandi dataset non indicizzati; carica in memoria hash table della tabella più piccola.
   * **`SORT MERGE JOIN`**: Usato quando i dati sono già ordinati o in presenza di predicati di non-uguaglianza (`<`, `>`).
4. **Access Predicates vs Filter Predicates**:
   * `Access Predicate`: La condizione viene usata direttamente per navigare l'albero B-Tree dell'indice (efficiente).
   * `Filter Predicate`: Le righe vengono lette fisicamente dal blocco e solo dopo scartate (inefficiente).

#### Anti-Pattern da evitare:
* **Funzioni su colonne indicizzate**: `WHERE UPPER(status) = 'PENDING'` disabilita l'indice standard su `status`. Soluzione: creare un *Function-Based Index* (`CREATE INDEX idx_status_upper ON transactions(UPPER(status))`).
* **Conversioni implicite di tipo**: Se `card_number` è `VARCHAR2(19)` e la query cerca `WHERE card_number = 1234567890123456` (numero), Oracle applica internamente `TO_NUMBER(card_number)`, invalidando l'indice.

---

### PL/SQL Enterprise

```sql
CREATE OR REPLACE PROCEDURE process_settlement_batch (
    p_circuit_code IN VARCHAR2,
    p_batch_date   IN DATE,
    p_processed    OUT NUMBER
) AS
    CURSOR c_tx IS
        SELECT id, amount, account_id
        FROM transactions
        WHERE circuit = p_circuit_code 
          AND TRUNC(created_at) = TRUNC(p_batch_date)
          AND status = 'AUTHORIZED'
        FOR UPDATE OF status NOWAIT;
        
    v_total NUMBER := 0;
BEGIN
    FOR r IN c_tx LOOP
        UPDATE transactions 
        SET status = 'SETTLED', updated_at = SYSDATE 
        WHERE id = r.id;
        
        v_total := v_total + 1;
    END LOOP;
    
    p_processed := v_total;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        -- Log errore su tabella autonoma di audit
        RAISE_APPLICATION_ERROR(-20001, 'Errore elaborazione settlement: ' || SQLERRM);
END process_settlement_batch;
/
```

---

## 3. Altri RDBMS: PostgreSQL e MySQL

### PostgreSQL (L'RDBMS Open Source Enterprise)
* **Punti di Forza**: Conforme ACID al 100%, supporto nativo a JSON avanzato tramite **`JSONB`** (indicizzabile con indici **GIN** - Generalized Inverted Index), Common Table Expressions (CTE) ricorsive, estensioni potenti (es. PostGIS).
* **JSON vs JSONB**:
  * `JSON`: Memorizza il testo esatto. Veloce in scrittura, ma richiede il parsing a ogni lettura; non supporta indici interni.
  * `JSONB`: Memorizza i dati in formato binario decomposto. Leggermente più lento in scrittura, ma istantaneo in lettura e pienamente indicizzabile.
* **Ruolo nei sistemi moderni**: Scelto per nuovi progetti transazionali e per architetture a microservizi che necessitano di flessibilità mista (relazionale + documenti JSON) senza i costi di licenza di Oracle.

### MySQL (InnoDB)
* **Punti di Forza**: Estrema velocità e semplicità operativa su carichi web a prevalenza di lettura e transazioni lineari.
* **Motori di Storage**:
  * **InnoDB** (Standard moderno): Supporta transazioni ACID, row-level locking, foreign key e crash recovery tramite redo/undo log.
  * **MyISAM** (Legacy): Non supporta transazioni né foreign key, usa table-level locking (obsoleto per sistemi transazionali).
* **Limiti in ambito bancario**: Meno versatile di Oracle e PostgreSQL per query analitiche complesse, window functions avanzate e strumenti integrati di diagnostica profonda.

---

## 4. Database NoSQL & Motori di Ricerca

### Il Teorema CAP & PACELC

Nei sistemi distribuiti, il **Teorema CAP** (*Eric Brewer*) afferma che in presenza di una partizione di rete (**P**artition Tolerance), un sistema può garantire solo una tra:
* **Consistenza Forte (C)**: Ogni lettura riceve la scrittura più recente o un errore.
* **Alta Disponibilità (A)**: Ogni richiesta riceve una risposta (non di errore), senza garanzia che contenga la versione più aggiornata.

Il teorema **PACELC** estende il CAP considerando il funzionamento in condizioni normali (senza partizioni):
* Se c'è una Partizione (**P**), scegli tra Disponibilità (**A**) e Consistenza (**C**);
* **E**lse (in assenza di partizioni), scegli tra Latenza (**L**) e Consistenza (**C**).

```
                 Teorema CAP: I 3 Vertici
                           Consistency (C)
                                ╱╲
                               ╱  ╲
           Oracle / Postgres  ╱    ╲  MongoDB (Default)
                             ╱      ╲
              Availability (A)───────Partition Tolerance (P)
                               Cassandra / DynamoDB
```

---

### Panoramica delle Famiglie NoSQL

```
┌─────────────────┬──────────────────┬───────────────────────┬───────────────────────────┐
│ Modello         │ Tecnologia       │ Meccanismo Base       │ Caso d'Uso Principale     │
├─────────────────┼──────────────────┼───────────────────────┼───────────────────────────┤
│ Document Store  │ MongoDB          │ BSON Documents        │ Payload semi-strutturati  │
│ Column-Family   │ Apache Cassandra │ LSM-Tree, Masterless  │ Audit log, Time-Series    │
│ Key-Value       │ Redis            │ In-Memory Key-Value   │ Caching L2, Rate Limiting │
│ Search Engine   │ Elasticsearch    │ Inverted Index Lucene │ Full-text, Log Analytics  │
│ Graph Database  │ Neo4j            │ Nodi, Archi, Cypher   │ Fraud Detection, Network  │
└─────────────────┴──────────────────┴───────────────────────┴───────────────────────────┘
```

---

### 1. MongoDB (Document Store)
* **Modello Dati**: Documenti BSON (Binary JSON) raggruppati in *Collections*. Schema dinamico e flessibile.
* **Transazioni**: Supporta transazioni ACID multi-documento (dalla v4.0), ma il pattern naturale resta la denormalizzazione e l'atomicità sul singolo documento.
* **Sharding**: Partizionamento orizzontale automatico tramite **Shard Key**. Una scelta errata della Shard Key può causare *hot-spotting* (un solo nodo sovraccarico mentre gli altri sono inattivi).
* **Uso nei pagamenti**: Archiviazione dei payload grezzi di richiesta/risposta dei circuiti (ISO 8583, XML, JSON eterogenei), configurazioni di onboarding merchant.

### 2. Apache Cassandra (Column-Family Store)
* **Architettura**: Completamente distribuita e **Masterless** (ogni nodo è identico, nessun Single Point of Failure). Partizionamento dei dati su anello tramite hash della *Partition Key*.
* **Scrittura ad Altissime Prestazioni (LSM-Tree)**:
  * La scrittura viene registrata sul **CommitLog** (scrittura sequenziale su disco per durabilità) e contemporaneamente nella **Memtable** in RAM.
  * Periodicamente la Memtable viene scaricata su disco in file immutabili chiamati **SSTable** (*Sorted String Table*), eliminando gli update in-place costosi dei database relazionali.
* **Consistenza Configurabile (*Tunable Consistency*)**:
  * Possibilità di definire il livello per singola query: `ONE`, `QUORUM`, `ALL`.
  * Regola di consistenza forte: $R + W > N$ (dove $R$ = nodi in lettura, $W$ = nodi in scrittura, $N$ = fattore di replicazione).
* **Uso nei pagamenti**: **Audit trail immutabile**, tracciamento eventi di conformità PSD2, log delle richieste API ad altissimo volume.

### 3. Redis (In-Memory Key-Value & Data Structures)
* **Caratteristiche**: Single-threaded event loop (su I/O multiplexing), elaborazione in RAM con latenze sub-millisecondo.
* **Strutture Dati**: String, List, Set, Sorted Set (ZSET), Hash, Bitmaps, HyperLogLog, Streams.
* **Uso nei pagamenti**:
  * **Idempotency Key Store**: Conservazione dello stato della transazione per 24-48h con `SETNX` o TTL.
  * **Distributed Lock**: Gestione mutua esclusione tra istanze con Redlock / Lua scripts.
  * **Rate Limiting**: Sliding window counter tramite ZSET per proteggere le API di pagamento.

### 4. Elasticsearch (Distributed Search & Analytics Engine)
* **Caratteristiche**: Motore basato su **Apache Lucene**. Non è un database relazionale né la fonte primaria di verità (*Source of Truth*).
* **Indice Invertito (*Inverted Index*)**:
  * Mappa ogni parola/token alla lista dei documenti che la contengono e alle posizioni relative. Permette ricerche full-text e filtri su milioni di record in millisecondi (evitando i devastanti `LIKE '%...%'` sui DB relazionali).
* **Uso nei pagamenti**: Centralizzazione log applicativi (Stack ELK / OpenSearch), dashboard di backoffice per investigazione frodi, ricerche per causale o metadati da parte dell'assistenza clienti.

---

## 5. Pattern e Strategie di Accesso ai Dati

### Pattern Architetturali

```
                                  Architettura di Accesso ai Dati
                                                │
       ┌────────────────────────┬───────────────┴───────────────┬────────────────────────┐
       ▼                        ▼                               ▼                        ▼
Repository Pattern       Unit of Work                   Connection Pooling        Read Replicas
• Astrae l'accesso      • Raggruppa operazioni         • HikariCP (pool)          • CQRS su lettura
• Spring Data JPA       • @Transactional & L1 Cache    • Zero latenze socket      • AbstractRoutingDS
```

1. **Repository Pattern**: Separa la logica di dominio dall'infrastruttura di persistenza. In Spring Data, l'interfaccia `JpaRepository<T, ID>` espone metodi CRUD standard e query derivation.
2. **Unit of Work**: Mantiene una lista di oggetti coinvolti in una transazione e coordina la scrittura delle modifiche in un unico batch al commit. In JPA coincide con il **Persistence Context (L1 Cache)** e il comando `flush()`.
3. **Connection Pooling (HikariCP)**:
   * Evita il costo di apertura/chiusura del socket TCP e dell'handshake di autenticazione per ogni richiesta.
   * Parametri critici:
     * `maximumPoolSize`: dimensione massima (regola di empirica: $\text{Pool} = \text{CPU Cores} \times 2 + \text{Disk Spindle}$).
     * `connectionTimeout`: millisecondi di attesa prima di lanciare eccezione se il pool è saturo.
     * `leakDetectionThreshold`: rileva connessioni aperte e non rilasciate (connection leaks).
4. **Read Replicas & Dynamic Routing**:
   * Utilizzo di un nodo Primary per le scritture (`INSERT`, `UPDATE`, `DELETE`) e repliche asincrone di sola lettura (*Read Replicas*) per query pesanti e reportistica.
   * In Spring: implementazione tramite `AbstractRoutingDataSource` che controlla `TransactionSynchronizationManager.isCurrentTransactionReadOnly()`.

---

### Strategie di Gestione Dati nei Microservizi

```
┌───────────────────────────────┬─────────────────────────────────────────────────────────────────┐
│ Strategia                     │ Descrizione e Beneficio                                         │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ **Database per Service**      │ Ogni microservizio possiede il proprio schema/DB. No foreign    │
│                               │ key cross-servizio, disaccoppiamento totale del deploy.         │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ **Saga Pattern**              │ Coordina transazioni distribuite tramite sequenze di transazioni│
│                               │ locali con azioni compensative in caso di fallimento.           │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ **Transactional Outbox**      │ Salva l'evento di business nella tabella locale `OUTBOX` dentro │
│                               │ la stessa transazione SQL, pubblicandolo poi su Kafka/JMS.      │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ **CQRS**                      │ Separa il modello di scrittura (Command/RDBMS) dal modello      │
│                               │ di lettura ottimizzato (Query/Elasticsearch/Redis).             │
└───────────────────────────────┴─────────────────────────────────────────────────────────────────┘
```

---

## 6. Matrice Comparativa: Polyglot Persistence

| Database | Modello | Garanzia Transazionale | Forza Primaria | Ruolo nel Sistema di Pagamenti |
| :--- | :--- | :--- | :--- | :--- |
| **Oracle** | Relazionale | ACID Forte (Serializable/Read Committed) | Robustezza, CBO maturo, RAC, High Availability | **Core Ledger**, Saldi, Movimenti, Riconciliazione |
| **PostgreSQL**| Relazionale | ACID Forte (MVCC) | Estendibilità, JSONB, Open Source Enterprise | Microservizi core, Gestione pagamenti moderni |
| **MySQL** | Relazionale | ACID (InnoDB) | Semplicità, alte performance read-heavy | Portali merchant, anagrafiche accessorie |
| **MongoDB** | Document | Atomicità su documento (ACID opzionale) | Schema flessibile, Sharding nativo | Payload grezzi circuiti, Configurazioni dinamiche |
| **Cassandra** | Column-Family | Eventual Consistency (Tunable) | Scritture massicce, zero Single Point of Failure | **Audit Log immutabile**, Event Sourcing Store |
| **Redis** | In-Memory K-V | Atomicità comandi singoli / Script Lua | Latenza sub-millisecondo | **Idempotency Key Cache**, Rate Limiting, Sessioni |
| **Elasticsearch**| Search Engine | Near Real-Time (Eventual) | Ricerca Full-Text, Aggregazioni real-time | **Log Centralizzati (ELK)**, Backoffice Search |

---

## 7. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come analizzi e risolvi una query SQL che improvvisamente è diventata lenta in produzione su Oracle?*
  - **R**: Il primo passo è estrarre l'**Execution Plan reale** tramite `DBMS_XPLAN.DISPLAY_CURSOR` con statistiche di runtime (`ALLSTATS LAST`) per confrontare le righe stimate (`E-Rows`) con quelle effettive (`A-Rows`). Verifico se è presente un `TABLE ACCESS FULL` inatteso su una tabella ad alto volume o un `NESTED LOOPS` inefficiente. Se c'è grande discrepanza tra righe stimate e reali, il problema sono le **statistiche obsolete** (da aggiornare con `DBMS_STATS.GATHER_TABLE_STATS`). Altrimenti, verifico se sono state introdotte funzioni su colonne indicizzate nel `WHERE` (risolvibili con Function-Based Index) o se occorre un nuovo indice composito ordinato secondo la selettività dei predicati.

- *D: Qual è la differenza tra Locking Ottimistico e Pessimistico e quando useresti l'uno o l'altro nei pagamenti?*
  - **R**: Il locking ottimistico non blocca fisicamente le righe sul database, ma usa un campo versione (`@Version`) verificato al commit: è ideale in scenari a bassa o media contesa (es. aggiornamento profilo merchant). Il locking pessimistico acquisisce un blocco fisico (`SELECT ... FOR UPDATE` o `LockModeType.PESSIMISTIC_WRITE`): è obbligatorio in scenari ad alta contesa transazionale come l'aggiornamento del saldo o il settlement batch concorrente, per evitare conflitti a valle e garantire serializzabilità immediata.

- *D: Perché non memorizzare l'intero ledger dei saldi e delle transazioni su un database NoSQL come MongoDB o Cassandra?*
  - **R**: Il core contabile e transazionale richiede garanzie ACID assolute, forte consistenza immediata e vincoli di integrità referenziale per prevenire anomalie finanziarie e *double spending*. I DB NoSQL privilegiano la scalabilità orizzontale e l'alta disponibilità a scapito della consistenza immediata (Eventual Consistency nel Teorema CAP/PACELC). La scelta architetturale corretta è la **Polyglot Persistence**: RDBMS (Oracle/PostgreSQL) per il Ledger finanziario e NoSQL come supporto specializzato (Redis per cache/idempotenza, Cassandra per audit log immutabili ad alto throughput, Elasticsearch per la ricerca operativa).

- *D: Che differenza c'è tra `JSON` e `JSONB` in PostgreSQL?*
  - **R**: `JSON` memorizza il payload come testo raw esatto: la scrittura è veloce, ma ogni query richiede il re-parsing del documento e non è possibile creare indici sui singoli attributi interni. `JSONB` analizza e memorizza il dato in un formato binario decomposto: richiede un piccolo overhead di parsing in scrittura, ma l'accesso in lettura è velocissimo e permette la creazione di indici **GIN** su chiavi e valori interni.

- *D: Come funziona il meccanismo di scrittura di Cassandra (LSM-Tree) e perché garantisce un throughput così elevato?*
  - **R**: Cassandra non esegue letture prima di scrivere né aggiorna blocchi in-place sul disco. Ogni operazione di scrittura viene appesa sequenzialmente al `CommitLog` su disco per garantire durabilità e contestualmente inserita nella `Memtable` ordinata in RAM. Quando la Memtable è piena, viene scaricata sequenzialmente come `SSTable` immutabile su disco. Poiché le scritture su disco sono esclusivamente sequenziali (senza seek della testina), il throughput è limitato solo dalla banda I/O.

- *D: Come si previene il fenomeno dei Connection Leaks con HikariCP?*
  - **R**: Un connection leak si verifica quando un thread ottiene una connessione dal pool ma non la rilascia (mancata chiusura in blocchi `try-with-resources` o transazioni bloccate all'infinito). In HikariCP si configura `leakDetectionThreshold` (es. a 5000 ms): se una connessione rimane aperta fuori dal pool oltre questo tempo, HikariCP genera un warning con lo stack trace esatto del thread che ha allocato la connessione, facilitando l'individuazione del bug.

---

## 8. Come esercitarsi

1. **Window Function Challenge**: Scrivi una query SQL su schema bancario (`transactions`: `id`, `account_id`, `amount`, `status`, `created_at`) che restituisca per ogni transazione il saldo progressivo dell'account, il numero progressivo di transazione del giorno e la differenza rispetto all'importo della transazione precedente dell'utente (usando `LAG() OVER (...)`).
2. **Explain Plan Reverse Engineering**: Prendi una query lenta con join tra 3 tabelle e progetta su carta gli indici ottimali (tenendo conto della selettività delle colonne e dell'ordine del `WHERE` e delle clausole di `JOIN`).
3. **Disegno Architettura Polyglot**: Disegna l'architettura di persistenza di una piattaforma di pagamento digitale specificando per ciascun dato (Auth Token, Idempotency Key, Transaction Ledger, API Audit Logs, Log Applicativi) quale database utilizzeresti e la motivazione architetturale basata su CAP/PACELC e requisiti di business.
