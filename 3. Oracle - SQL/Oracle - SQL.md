## 3. Oracle / SQL

### Cos'è e perché conta
In un sistema di pagamento la correttezza dei dati transazionali è tutto: sapranno se capisci davvero ACID o se lo sai solo a memoria.

### Cosa studiare

**SQL avanzato**
- Join (INNER, LEFT, self-join) su schemi con più tabelle collegate (transazioni, conti, movimenti) — proprio come nello schema di riconciliazione che hai già costruito
- Window function (`ROW_NUMBER`, `RANK`, `SUM() OVER`) utili per calcolare saldi progressivi o identificare duplicati
- Aggregazioni con `GROUP BY` + `HAVING` per riconciliazioni/quadrature

**Concorrenza e lock**
- Differenza tra lock ottimistico (versioning, `@Version` in JPA) e pessimistico (`SELECT FOR UPDATE`)
- Perché in ambito settlement, dove più processi batch possono toccare lo stesso saldo, la scelta del lock ha impatti reali su correttezza e throughput
- ACID: atomicità e isolamento spiegati con un esempio concreto (es. trasferimento tra due conti: se il debit va a buon fine ma il credit fallisce, serve rollback)

**PL/SQL (base)**
- Struttura di una stored procedure/function, cursori, gestione eccezioni (`EXCEPTION WHEN`)
- Non serve essere esperti, ma sapere leggerne una e spiegare cosa fa

### Come esercitarti
Scrivi una query che, data una tabella `transazioni(id, importo, stato, data)`, calcola il saldo progressivo giorno per giorno con una window function — è l'esempio più vicino al mondo reale che ti chiederanno.

### Execution plan: come ottimizzare query lente

L'**execution plan** (piano di esecuzione) è la sequenza di operazioni che il database sceglie per eseguire una query — mostra come il DBMS accede fisicamente ai dati (quali indici usa, in che ordine fa i join, quanti record stima di leggere) per arrivare al risultato. È lo strumento principale per capire *perché* una query è lenta, non solo *che* è lenta.

**Come funziona concettualmente**

Quando lanci una query SQL, il database non la esegue "alla lettera" — un **query optimizer** (in Oracle si chiama *Cost-Based Optimizer*, CBO) valuta diverse strategie possibili per ottenere lo stesso risultato e sceglie quella con il costo stimato più basso, basandosi su:

- **Statistiche** sulle tabelle (numero di righe, distribuzione dei valori, cardinalità)
- **Indici disponibili** e la loro selettività
- **Vincoli** (chiavi primarie/esterne) che permettono ottimizzazioni

L'execution plan è la "traduzione leggibile" di quella strategia scelta.

**Dove si usa (Oracle)**

```sql
EXPLAIN PLAN FOR
SELECT * FROM transactions WHERE account_id = 123 AND status = 'PENDING';

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

Oppure, per vedere il piano **realmente usato** (non solo quello stimato) dopo l'esecuzione:

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));
```

Strumenti pratici dove lo trovi:
- **SQL Developer**: pulsante "Explain Plan" (F10) con visualizzazione grafica
- **AWR/ASH reports** in Oracle Enterprise: per analizzare query lente già eseguite in produzione
- Equivalenti in altri DB: `EXPLAIN` in PostgreSQL/MySQL — stesso concetto, sintassi diversa

**Cosa cercare nel piano per ottimizzare una query lenta**

1. **Full Table Scan vs Index Access** — la voce più importante da controllare. Se vedi `TABLE ACCESS FULL` su una tabella grande dove ti aspetti un filtro selettivo, è spesso il primo campanello d'allarme:

```
| Id | Operation                   | Name         | Rows |
|  0 | SELECT STATEMENT            |               |      |
|  1 |  TABLE ACCESS FULL          | TRANSACTIONS  | 50000|  <- problema
```
vs.
```
|  1 |  TABLE ACCESS BY INDEX ROWID| TRANSACTIONS  |    12|  <- ottimizzato
|  2 |   INDEX RANGE SCAN          | IDX_ACC_STAT  |    12|
```

2. **Cost e Cardinality stimata vs reale** — il piano mostra un costo stimato e un numero di righe attese (`Rows`). Se la stima è molto diversa dal reale (es. stima 10 righe ma in realtà ne processa 500.000), spesso significa **statistiche obsolete** — si risolve con `DBMS_STATS.GATHER_TABLE_STATS`.

3. **Tipo di Join e ordine**:
   - `NESTED LOOPS`: efficiente quando una delle due tabelle produce poche righe (filtro molto selettivo) e l'altra ha un buon indice sulla colonna di join
   - `HASH JOIN`: più efficiente su grandi volumi senza indici utili, ma richiede più memoria
   - `MERGE JOIN`: utile quando i dati sono già ordinati sulla colonna di join

   Un join scelto male (es. `NESTED LOOPS` su due tabelle enormi) è una causa comune di query lente.

4. **Filtro applicato prima o dopo** — verifica se una condizione `WHERE` viene applicata a livello di indice (`INDEX RANGE SCAN` con la condizione nell'`Access Predicates`) oppure solo dopo aver già letto le righe (`Filter Predicates`) — nel secondo caso il DB ha comunque dovuto leggere più dati del necessario prima di scartarli.

**Rilevanza specifica per il dominio pagamenti**

In un sistema transazionale con volumi alti, l'execution plan è cruciale per query su tabelle di transazioni/movimenti che crescono continuamente:

- Query di **riconciliazione** che fanno join tra `transactions` e `ledger_entries` su range di date — un indice mancante su `created_at` può far degenerare tutto in full table scan
- Query di **lookup per idempotency key** — deve essere garantito un accesso via indice univoco, altrimenti ogni controllo di idempotenza rallenta a mano a mano che la tabella cresce
- Batch di **settlement notturno** che processano grandi volumi — qui a volte è persino corretto *forzare* un full table scan con un hint se stai leggendo comunque la maggior parte della tabella, perché un indice sarebbe più lento

**Come esercitarti**

Prepara questo aneddoto: "ho una query lenta, il primo passo è guardare l'execution plan per capire se c'è un full table scan inatteso o statistiche obsolete, poi valuto se serve un indice nuovo, o se riscrivere la query per aiutare l'optimizer a scegliere un piano migliore (es. evitando funzioni sulla colonna indicizzata nel WHERE, che impediscono l'uso dell'indice — `WHERE UPPER(status) = 'PENDING'` blocca l'indice su `status` a meno di un indice a funzione)."
