## Reactive Programming (Project Reactor, WebFlux vs Virtual Threads)

### Cos'è e perché conta
La programmazione reattiva nasce per risolvere il problema della concorrenza ad altissimo volume di richieste I/O-bound (es. gateway API di pagamento, streaming di eventi, integrazioni finanziarie ad alta frequenza), massimizzando l'efficienza delle risorse hardware senza allocare un thread del sistema operativo per ogni richiesta (*Thread-per-Request model*). Con l'introduzione dei **Virtual Threads in Java 21 (Project Loom)**, il confronto tra l'approccio reattivo e quello a thread virtuali è uno dei temi architetturali più discussi nei colloqui tecnici avanzati.

---

### Cosa studiare

#### 1. Il Paradigma Reattivo & Reactive Streams Specification

La specifica **Reactive Streams** (inclusa in Java 9 come `java.util.concurrent.Flow`) definisce lo standard per flussi asincroni non-bloccanti con gestione della contropressione:

- **I 4 Componenti Fondamentali**:
  1. **`Publisher<T>`**: il produttore di eventi (emette elementi `onNext()`, `onError()`, `onComplete()`).
  2. **`Subscriber<T>`**: il consumatore che riceve gli eventi.
  3. **`Subscription`**: rappresenta il collegamento tra Publisher e Subscriber; permette al consumatore di richiedere $N$ elementi (`request(n)`) o cancellare l'iscrizione (`cancel()`).
  4. **`Processor<T, R>`**: componente intermedio che funge sia da Subscriber che da Publisher (trasforma i dati).

##### A. Il Concetto Chiave: Backpressure (Contropressione)
Nei sistemi tradizionali o sincroni, se un produttore (es. un flusso di transazioni Kafka o un gateway POS) invia 100.000 eventi/sec a un consumatore che può processarne solo 5.000/sec, il consumatore esaurisce la memoria (*OutOfMemoryError*) o accumula code infinite.
- Con la **Backpressure**, è il **Subscriber** a comunicare esplicitamente al Publisher quanti dati è in grado di ricevere (`subscription.request(n)`), garantendo che il sistema non vada mai in sovraccarico.

---

#### 2. Project Reactor: `Mono` e `Flux`

**Project Reactor** è l'implementazione reattiva di riferimento utilizzata da Spring Framework:

- **`Mono<T>`**: rappresenta una sequenza reattiva che emette **0 o 1 elemento**, oppure un errore (`CompletableFuture` potenziato).
  - *Esempio*: recupero di un conto per ID `Mono<Account>`, esito di un pagamento `Mono<PaymentResponse>`.
- **`Flux<T>`**: rappresenta una sequenza reattiva che emette da **0 a $N$ elementi** (potenzialmente infinita).
  - *Esempio*: stream di transazioni in tempo reale `Flux<TransactionEvent>`.

##### Esempio di Codice Reattivo
```java
public Mono<PaymentResponse> processPayment(PaymentRequest request) {
    return accountClient.getAccount(request.accountId()) // Mono<Account>
        .switchIfEmpty(Mono.error(new AccountNotFoundException("Conto inesistente")))
        .filter(account -> account.getBalance().compareTo(request.amount()) >= 0)
        .switchIfEmpty(Mono.error(new InsufficientFundsException("Fondi insufficienti")))
        .flatMap(account -> acquirerClient.authorize(request)) // Chiamata HTTP non bloccante
        .map(authResult -> new PaymentResponse("SUCCESS", authResult.getAuthCode()))
        .timeout(Duration.ofMillis(3000))
        .onErrorResume(TimeoutException.class, ex -> Mono.just(new PaymentResponse("TIMEOUT", null)))
        .doOnSuccess(res -> log.info("Pagamento completato: {}", res));
}
```

---

#### 3. Spring WebFlux vs Spring MVC

```
┌─────────────────────────────────────────────────────────────┐
│                 SPRING MVC (Thread-per-Request)             │
│  Request 1 ──► [OS Thread 1] ──► Bloccato su DB/HTTP ──► Res │
│  Request 2 ──► [OS Thread 2] ──► Bloccato su DB/HTTP ──► Res │
│  (Limitato dalla dimensione del Thread Pool Tomcat: es. 200)│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                 SPRING WEBFLUX (Event Loop / Netty)         │
│  Requests ────► [Event Loop Thread (1 per Core)] ──► Netty  │
│                 (Non-Blocking I/O: registra callback        │
│                  e serve immediatamente la request succ.)   │
└─────────────────────────────────────────────────────────────┘
```

- **Spring MVC**: basato su servlet sincrone (Tomcat). Ogni richiesta occupa un thread dall'inizio alla fine. Se l'applicazione fa chiamate lente a DB o API esterne, i thread restano bloccati in attesa (*I/O wait*), portando all'esaurimento del thread pool sotto carico elevato (*Thread Starvation*).
- **Spring WebFlux**: basato su server asincroni non-bloccanti (**Netty**). Utilizza un numero ridottissimo di thread (pari al numero di core della CPU) che gestiscono eventi I/O in modo continuo tramite callback e socket non-bloccanti (epoll/kqueue).

---

#### 4. Il Grande Dilemma: Reactive Programming vs Virtual Threads (Java 21)

Con l'arrivo dei **Virtual Threads (Project Loom)** in Java 21, il panorama è cambiato radicalmente:

| Caratteristica | Reactive Programming (WebFlux / Reactor) | Virtual Threads (Java 21 + Spring MVC) |
|---|---|---|
| **Stile di Programmazione** | Funzionale, dichiarativo, a pipeline (`Mono/Flux`) | Imperativo tradizionale e sincrono (`try/catch`, sequenziale) |
| **Scalabilità I/O** | Altissima (non-blocking I/O) | Altissima (i Virtual Thread vengono smontati durante I/O bloccante) |
| **Complessità & Debugging** | Molto complessa: stack trace frammentati, difficile tracciare thread context | Semplicissima: stack trace standard, debug riga per riga ordinario |
| **ThreadLocal & Logging** | Complesso: richiede `Reactor Context` o `MDC.put` manuale | Trasparente: supporto nativo completo a `ThreadLocal` e Scoped Values |
| **Compatibilità Librerie Legacy** | Richiede driver reattivi (R2DBC, WebClient); un blocco JDBC blocca Netty | Compatibile al 100% con JDBC, Hibernate e qualsiasi libreria bloccante |

**Posizione da Senior a colloquio**:
> *"WebFlux e la programmazione reattiva rimangono eccellenti per scenari di streaming continuo di eventi (SSE, WebSocket, stream Kafka infiniti) o API Gateway puri. Tuttavia, per il 90% delle applicazioni backend enterprise transazionali (CRUD, pagamenti, interrogazioni DB relazionali), i **Virtual Threads di Java 21** rappresentano oggi la scelta migliore: offrono la stessa scalabilità massiva dell'approccio reattivo senza sacrificare la semplicità del codice imperativo, la facilità di debugging e la compatibilità con l'ecosistema JPA/JDBC standard."*

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Cosa succede se inserisci una chiamata bloccante JDBC (`Thread.sleep()` o query JPA tradizionale) all'interno di un flusso WebFlux?*
  - **R**: Si verifica un disastro di performance. Poiché Netty dispone solo di un numero di thread pari ai core della CPU (es. 4 o 8 thread totali per l'intero server), bloccare uno di questi thread con un'operazione I/O sincrona paralizza una frazione enorme dell'intera applicazione. Se è assolutamente necessario chiamare codice bloccante legacy in Reactor, occorre isolarlo esplicitamente su un thread pool dedicato tramite `.subscribeOn(Schedulers.boundedElastic())`.

- *D: Cos'è la Backpressure e perché è vitale nei sistemi di pagamento?*
  - **R**: È il meccanismo mediante il quale un consumatore controlla la velocità di emissione del produttore, richiedendo solo il numero di messaggi che è effettivamente in grado di elaborare. In un sistema di pagamento, evita che picchi improvvisi di transazioni saturino la memoria del microservizio o mandino in crash i database a valle.

---

### Come esercitarti
1. **Pipeline Reattiva**: scrivi una catena reattiva in Reactor che effettua una chiamata `WebClient`, filtra i risultati, applica un timeout di 2 secondi, un retry con backoff esponenziale in caso di errore di rete e un fallback su un valore di default.
