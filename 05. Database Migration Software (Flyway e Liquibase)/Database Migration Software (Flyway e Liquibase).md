# 5. Database Migration Software (Flyway e Liquibase)
## Il problema da cui partire
Una **migrazione** è una modifica versionata allo schema o ai dati, da applicare con condizioni definite. Lo schema descrive tabelle, colonne e vincoli; i dati sono le informazioni già memorizzate. Un nuovo schema valido non dimostra che tutti i dati precedenti rispettino la nuova regola.
Il **checksum** riassume il contenuto del file e permette di rilevare cambiamenti. Un **changelog** organizza la storia delle modifiche e un **changeset** è un'unità di cambiamento identificabile. Questi strumenti rendono visibile che cosa è stato applicato, ma non rendono ogni modifica reversibile. Eliminare una colonna può perdere informazioni che un rollback dello schema non ricostruisce.
Durante un rilascio graduale convivono versioni diverse dell'applicazione. Il percorso **expand and contract** aggiunge prima elementi compatibili, migra e verifica l'uso, poi rimuove ciò che non serve più. Il vincolo guida il lavoro: le versioni ancora in esecuzione devono poter leggere e scrivere dati validi.
#### 1. Il Problema della Gestione Manuale dei Database
Senza tool di migrazione: Disallineamento degli schemi tra ambiente di sviluppo, staging e produzione. Modifiche "volanti" a mano non tracciate su Git. Impossibilità di automatizzare i test di integrazione e i deploy in pipeline CI/CD. Rischio di corruzione dati o fallimento delle release.
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
**Struttura del Nome**: `V`: prefisso per migrazioni Versionate (eseguite una sola volta in ordine numerico). `U`: prefisso per Undo (rollback). `R`: prefisso per migrazioni Ripetibili (eseguite ogni volta che il loro checksum cambia, ideali per viste, funzioni e stored procedure). `1_0`: numero di versione (separatori con underscore o punti). `__`: doppio underscore separatore obbligatorio. `create_transactions_table`: descrizione parlante.
##### B. Meccanismo di Funzionamento e Checksum

Al primo avvio, Flyway crea una tabella interna di tracciamento: `flyway_schema_history`.

Prima di applicare uno script, calcola l'hash **Checksum** del file SQL.

Se lo script non è ancora stato eseguito, lo esegue con il supporto transazionale disponibile per quel database e per quelle istruzioni e registra la versione, la data di esecuzione e il checksum nella tabella.

Se uno script già eseguito in passato viene modificato a posteriori, Flyway rileva un'incongruenza nel checksum e **blocca l'avvio dell'applicazione** per prevenire stati inconsistenti del DB.

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
`DATABASECHANGELOG`: registra ogni singolo changeset eseguito, autore, ID, data e checksum (MD5). `DATABASECHANGELOGLOCK`: garantisce che solo un'istanza dell'applicazione per volta esegua le migrazioni durante il deployment scalato orizzontalmente (lock distribuito a livello di DB).
---
#### 4. Confronto Diretto: Flyway vs Liquibase
| Caratteristica | Flyway | Liquibase |
|---|---|---|
| **Filosofia** | SQL-First (semplice, naturale per chi conosce SQL avanzato) | Abstraction-First (Changelog YAML/XML/JSON indipendenti dal DBMS) |
| **Curva di Apprendimento** | Bassissima: basta saper scrivere normali file `.sql` | Media: richiede di apprendere i tag e la sintassi dei ChangeSet |
| **Portabilità Multi-DB** | Minore: se cambi DBMS da Oracle a PostgreSQL devi riscrivere lo script SQL | Dipende dai change type e dai database: occorre verificare SQL generato e comportamento |
| **Rollback Open-Source** | Solo nella versione commerciale (Teams/Enterprise) per gli script `U` | Supporto nativo integrato del tag `rollback` nella versione Open Source |
| **Feature Avanzate** | Ripetibili (`R__`), Java-based migrations per logica complessa | Pre-conditions (controlli condizionali prima dell'esecuzione), Contexts |
---
#### 5. Migrazioni e rilasci graduali

Una migrazione già applicata è parte della storia. Se occorre cambiare una colonna, si aggiunge una nuova migrazione invece di riscrivere lo script precedente. Il checksum aiuta a individuare questa riscrittura; una correzione dei metadati non applica automaticamente una modifica allo schema.

Il rollback dipende dal database e dalle istruzioni. Alcuni DDL non sono annullabili come una normale modifica dati; eliminare una colonna può perdere contenuti che l'undo non ricostruisce. Si verificano quindi SQL generato, dati rappresentativi e recupero, controllando anche funzionalità ed edizione dello strumento adottato.

Per rinominare `merchant_name` in `merchant_display_name`, il percorso expand and contract introduce prima la nuova colonna mantenendo la vecchia. Una fase compatibile mantiene allineate le informazioni, poi migra i dati e verifica il risultato. Il solo backfill non basta se nuove scritture possono arrivare durante la copia: occorre definire come sincronizzarle.

Una versione successiva usa il nuovo nome; la vecchia colonna viene rimossa soltanto dopo aver verificato che nessuna versione in esecuzione la richieda e che la finestra di rollback sia coerente con la rimozione. La compatibilità temporanea è una proprietà del processo, non del nome del pattern.

In sviluppo può essere utile eseguire le migrazioni all'avvio. In produzione un Job dedicato o un passo della pipeline può rendere più espliciti controllo ed esito. Un init container su ogni replica può comunque introdurre concorrenza: lock dello strumento, timeout e responsabilità del processo di rilascio devono essere definiti.

### Domande tipiche a colloquio (e risposte da Senior)
*D: Cosa succede se uno sviluppatore modifica un file SQL di migrazione Flyway già applicato in precedenza?*
**R**: Al successivo avvio dell'applicazione, Flyway ricalcola l'hash dello script e lo confronta con il checksum salvato nella tabella `flyway_schema_history`. Riscontrando una discrepanza, Flyway lancia una `FlywayException` e **blocca l'avvio dell'applicazione**. Per risolvere l'errore, occorre ripristinare il file originale e creare una nuova migrazione con versione incrementale `flyway repair` modifica metadati: si usa soltanto dopo aver ricostruito e verificato lo stato reale, non come scorciatoia per nascondere una discrepanza.
*D: Come gestisci le migrazioni del database in un'architettura a microservizi scalata su più repliche in Kubernetes?*
**R**: Quando più pod si avviano contemporaneamente, i tool di migrazione acquisiscono un lock esclusivo (Flyway usa il lock a livello di transazione, Liquibase usa `DATABASECHANGELOGLOCK`). Tuttavia, in produzione è best practice disabilitare la migrazione automatica all'avvio dei pod applicativi ed eseguirla tramite un **Kubernetes Pre-Install Job / Helm Hook** o un task dedicato nella pipeline CI/CD, rilasciando l'applicazione solo a migrazione avvenuta con successo.
---
### Come esercitarti

1. **Configurazione Spring Boot + Flyway**: aggiungi la dipendenza `flyway-core` e `flyway-database-oracle` (o postgres) in `pom.xml`, crea due script di migrazione `V1__init.sql` e `V2__add_index.sql`, avvia l'app e ispeziona la tabella `flyway_schema_history`.
