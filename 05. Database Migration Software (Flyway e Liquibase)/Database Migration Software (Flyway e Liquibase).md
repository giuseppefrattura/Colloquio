# 5. Database Migration Software (Flyway e Liquibase)

### Cos'è e perché conta
Nei sistemi enterprise moderni e nei microservizi con pipeline CI/CD automatizzate, la gestione dello schema del database non può essere manuale. I tool di **Database Migration** come **Flyway** e **Liquibase** permettono di tracciare, versionare, eseguire e rollbackare le modifiche allo schema del database (tabelle, indici, vincoli, stored procedure) come codice (*Database as Code*), garantendo consistenza perfetta tra ambienti di sviluppo, test e produzione.

---

### Cosa studiare

#### 1. Il Problema della Gestione Manuale dei Database
Senza tool di migrazione:
- Disallineamento degli schemi tra ambiente di sviluppo, staging e produzione.
- Modifiche "volanti" a mano non tracciate su Git.
- Impossibilità di automatizzare i test di integrazione e i deploy in pipeline CI/CD.
- Rischio di corruzione dati o fallimento delle release.

---

#### 2. Flyway: Semplicità e Approccio SQL-First

Flyway adotta un approccio incentrato su script **SQL nativi**:

##### A. Naming Convention dei File di Migrazione
Gli script sono memorizzati tipicamente in `src/main/resources/db/migration`:

```
V1_0__create_transactions_table.sql      (Versione 1.0 - Migrazione versionata)
V1_1__add_idempotency_key_index.sql      (Versione 1.1 - Migrazione versionata)
U1_1__drop_idempotency_key_index.sql      (Undo Migration - per Flyway Teams)
R__create_view_daily_settlement.sql      (Repeatable Migration - rieseguita se cambia il checksum)
```
- **Struttura del Nome**:
  - `V`: prefisso per migrazioni Versionate (eseguite una sola volta in ordine numerico).
  - `U`: prefisso per Undo (rollback).
  - `R`: prefisso per migrazioni Ripetibili (eseguite ogni volta che il loro checksum cambia, ideali per viste, funzioni e stored procedure).
  - `1_0`: numero di versione (separatori con underscore o punti).
  - `__`: doppio underscore separatore obbligatorio.
  - `create_transactions_table`: descrizione parlante.

##### B. Meccanismo di Funzionamento e Checksum
1. Al primo avvio, Flyway crea una tabella interna di tracciamento: `flyway_schema_history`.
2. Prima di applicare uno script, calcola l'hash **Checksum** del file SQL.
3. Se lo script non è ancora stato eseguito, lo esegue all'interno di una transazione e registra la versione, la data di esecuzione e il checksum nella tabella.
4. Se uno script già eseguito in passato viene modificato a posteriori, Flyway rileva un'incongruenza nel checksum e **blocca l'avvio dell'applicazione** per prevenire stati inconsistenti del DB.

---

#### 3. Liquibase: Flessibilità Multi-Formato e Astrazione DBMS

Liquibase adotta un approccio dichiarativo basato su **Changelog** e **ChangeSet**:

##### A. Formati Supportati
I changelog possono essere scritti in **YAML**, **XML**, **JSON** o **SQL formattato**:

```yaml
databaseChangeLog:
  - changeSet:
      id: 20260910-01
      author: gfrattura
      changes:
        - createTable:
            tableName: transactions
            columns:
              - column:
                  name: id
                  type: VARCHAR(36)
                  constraints:
                    primaryKey: true
                    nullable: false
              - column:
                  name: amount
                  type: DECIMAL(19, 4)
                  constraints:
                    nullable: false
              - column:
                  name: currency
                  type: VARCHAR(3)
                  constraints:
                    nullable: false
        - createIndex:
            indexName: idx_tx_currency
            tableName: transactions
            columns:
              - column:
                  name: currency
      rollback:
        - dropTable:
            tableName: transactions
```

##### B. Tabelle di Tracciamento
- `DATABASECHANGELOG`: registra ogni singolo changeset eseguito, autore, ID, data e checksum (MD5).
- `DATABASECHANGELOGLOCK`: garantisce che solo un'istanza dell'applicazione per volta esegua le migrazioni durante il deployment scalato orizzontalmente (lock distribuito a livello di DB).

---

#### 4. Confronto Diretto: Flyway vs Liquibase

| Caratteristica | Apache Flyway | Liquibase |
|---|---|---|
| **Filosofia** | SQL-First (semplice, naturale per chi conosce SQL avanzato) | Abstraction-First (Changelog YAML/XML/JSON indipendenti dal DBMS) |
| **Curva di Apprendimento** | Bassissima: basta saper scrivere normali file `.sql` | Media: richiede di apprendere i tag e la sintassi dei ChangeSet |
| **Portabilità Multi-DB** | Minore: se cambi DBMS da Oracle a PostgreSQL devi riscrivere lo script SQL | Massima: lo stesso ChangeSet YAML genera SQL valido per Oracle, Postgres, MySQL |
| **Rollback Open-Source** | Solo nella versione commerciale (Teams/Enterprise) per gli script `U` | Supporto nativo integrato del tag `rollback` nella versione Open Source |
| **Feature Avanzate** | Ripetibili (`R__`), Java-based migrations per logica complessa | Pre-conditions (controlli condizionali prima dell'esecuzione), Contexts |

---

#### 5. Best Practice nei Sistemi di Pagamento & Rilasci a Zero Downtime

1. **Mai modificare uno script di migrazione già eseguito in produzione**: se serve modificare una colonna, creare un **nuovo file di migrazione incrementale** (`V1_2__modify_column.sql`).
2. **Pattern Expand and Contract (Zero-Downtime Migration)**:
   - Se devi rinominare una colonna (es. `card_pan` in `tokenized_pan`):
     1. *Release 1 (Expand)*: aggiungi la nuova colonna `tokenized_pan` mantenendo la vecchia. L'applicazione scrive su entrambe.
     2. *Migrazione dati*: copia i vecchi valori nella nuova colonna.
     3. *Release 2*: l'applicazione legge e scrive solo sulla nuova colonna.
     4. *Release 3 (Contract)*: script di migrazione che elimina la vecchia colonna `card_pan`.
3. **Esecuzione in CI/CD vs Startup dell'Applicazione**:
   - In ambienti locali/sviluppo: esecuzione automatica all'avvio di Spring Boot (`spring.flyway.enabled=true`).
   - In ambienti di produzione Kubernetes ad alta concorrenza: eseguire le migrazioni come **Kubernetes InitContainer** o **Job dedicato in pipeline CI/CD** prima dell'avvio dei pod, per evitare contese di lock sul DB.

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Cosa succede se uno sviluppatore modifica un file SQL di migrazione Flyway già applicato in precedenza?*
  - **R**: Al successivo avvio dell'applicazione, Flyway ricalcola l'hash dello script e lo confronta con il checksum salvato nella tabella `flyway_schema_history`. Riscontrando una discrepanza, Flyway lancia una `FlywayException` e **blocca l'avvio dell'applicazione**. Per risolvere l'errore, occorre ripristinare il file originale e creare una nuova migrazione con versione incrementale (oppure eseguire `flyway repair` solo se la modifica non ha toccato il DB).

- *D: Come gestisci le migrazioni del database in un'architettura a microservizi scalata su più repliche in Kubernetes?*
  - **R**: Quando più pod si avviano contemporaneamente, i tool di migrazione acquisiscono un lock esclusivo (Flyway usa il lock a livello di transazione, Liquibase usa `DATABASECHANGELOGLOCK`). Tuttavia, in produzione è best practice disabilitare la migrazione automatica all'avvio dei pod applicativi ed eseguirla tramite un **Kubernetes Pre-Install Job / Helm Hook** o un task dedicato nella pipeline CI/CD, rilasciando l'applicazione solo a migrazione avvenuta con successo.

---

### Come esercitarti
1. **Configurazione Spring Boot + Flyway**: aggiungi la dipendenza `flyway-core` e `flyway-database-oracle` (o postgres) in `pom.xml`, crea due script di migrazione `V1__init.sql` e `V2__add_index.sql`, avvia l'app e ispeziona la tabella `flyway_schema_history`.
