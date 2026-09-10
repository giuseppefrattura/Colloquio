## 24. Concorrenza in Java

### Cos'è e perché conta
Non esplicitamente richiesta nella job description, ma centrale in un sistema ad alto throughput come i pagamenti, dove più richieste vengono elaborate contemporaneamente. È un argomento classico nei colloqui senior Java.

### Cosa studiare

**Thread e Runnable**

```java
Thread t = new Thread(() -> processPayment(payment));
t.start();
```
Creare thread manualmente è raro in codice moderno — si preferisce quasi sempre un `ExecutorService`, che gestisce un pool di thread riutilizzabili invece di crearne uno nuovo per ogni task (costoso in termini di risorse).

**ExecutorService**

```java
ExecutorService executor = Executors.newFixedThreadPool(10);
Future<AuthorizationResult> future = executor.submit(() -> authorizePayment(request));
AuthorizationResult result = future.get(2, TimeUnit.SECONDS); // con timeout esplicito
```
Il pool di thread ha una dimensione fissa/gestita, evitando di saturare le risorse del sistema con troppi thread concorrenti.

**`synchronized` e i suoi limiti**

```java
public synchronized void debitAccount(String accountId, BigDecimal amount) {
    // solo un thread alla volta può eseguire questo blocco per la stessa istanza
}
```
Garantisce mutua esclusione, ma è un meccanismo "grezzo": blocca l'intero metodo/oggetto, può creare colli di bottiglia se applicato troppo largamente, e non ha timeout — un thread che aspetta il lock aspetta indefinitamente (rischio di deadlock se mal gestito).

**`CompletableFuture`**: per composizione di operazioni asincrone in modo dichiarativo, molto più espressivo di `Future` puro:

```java
CompletableFuture<AuthorizationResult> authFuture = CompletableFuture
    .supplyAsync(() -> authorizePayment(request))
    .thenApply(this::enrichWithFraudScore)
    .exceptionally(ex -> AuthorizationResult.failed(ex.getMessage()));
```
Permette di incatenare trasformazioni, gestire errori, e combinare più operazioni asincrone (`thenCombine`, `allOf`) senza bloccare thread in attesa.

**Virtual Threads (Java 21, già visto nel punto 14)**: risolvono il problema che i thread OS tradizionali sono "costosi" (ognuno occupa memoria significativa, il sistema ne regge solo migliaia) — i virtual thread sono gestiti dalla JVM e permettono di avere milioni di "thread logici" concorrenti con overhead minimo, ideali per applicazioni con molte operazioni bloccanti I/O-bound (come chiamate di rete verso circuiti di pagamento esterni).

**Collezioni concorrenti**: `ConcurrentHashMap` invece di sincronizzare manualmente una `HashMap` — offre operazioni thread-safe con granularità fine (non blocca l'intera mappa per ogni accesso, a differenza di `Collections.synchronizedMap`).

### Rilevanza per il dominio pagamenti
Il tema si collega direttamente a quanto già visto su isolation level (punto 3) e locking ottimistico/pessimistico (punto 13): la concorrenza a livello applicativo Java (thread, executor) e la concorrenza a livello database sono due facce dello stesso problema quando più richieste toccano lo stesso account contemporaneamente.

### Domande tipiche e risposte

- *D: Perché preferire `ExecutorService` alla creazione manuale di thread?*
  R: Un `ExecutorService` riutilizza un pool di thread invece di crearne uno nuovo per ogni operazione (costoso), permette di limitare la concorrenza massima (evitando di saturare risorse), e offre gestione di timeout/cancellazione tramite `Future`.

- *D: Cosa può causare un deadlock e come lo eviteresti?*
  R: Un deadlock si verifica tipicamente quando due thread acquisiscono più lock in ordine diverso, restando bloccati ad aspettarsi a vicenda. Si previene definendo un **ordine consistente** di acquisizione dei lock in tutto il codice, o preferendo strutture concorrenti di alto livello (`ConcurrentHashMap`, `CompletableFuture`) invece di `synchronized` manuale dove possibile.
