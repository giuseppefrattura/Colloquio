================================================================================
GUIDA DI STUDIO COMPLETA — COLLOQUIO SENIOR JAVA BACKEND DEVELOPER
Generato automaticamente il: 2026-09-18 05:53:09 UTC
Totale capitoli inclusi: 46
================================================================================

INDICE DEI CAPITOLI:
  - 01. Java (JVM, Strutture Dati, Versioni 8-25, Concorrenza e Reactive)
  - 02. Linguaggi Alternativi: Go e Scala (Paradigmi Funzionali)
  - 03. Database Relazionali, NoSQL e Strategie di Accesso
  - 04. Redis
  - 05. Database Migration Software (Flyway e Liquibase)
  - 06. Strategie per la Gestione dei Database in Architetture a Microservizi
  - 07. Design Pattern e Principi SOLID
  - 08. Spring & Spring Boot
  - 09. API REST e RESTful Design
  - 10. Microservizi: Concetti Fondamentali
  - 11. WebSocket
  - 12. Apache Kafka
  - 13. JMS (Java Message Service)
  - 14. Tecnologie Specialistiche: OSGi e MQTT
  - 15. Tecnologie Streaming, Media e Broadcast
  - 16. Comparazioni: OpenShift vs Kubernetes, RabbitMQ vs Kafka
  - 17. Containerizzazione (Docker e OCI)
  - 18. Kubernetes
  - 19. Architettura Cloud
  - 20. Dependency Management (Maven e Gradle)
  - 21. Git e Branching Strategies
  - 22. Toolchain (Eclipse, Git, Maven, JUnit, Jenkins, Nexus)
  - 23. Unit Testing e Test Automation (JUnit 5, Mockito, Testcontainers)
  - 24. SAST e Qualità del Software (SonarQube)
  - 25. CI-CD e Release Management (Jenkins, GitLab CI, Nexus)
  - 26. Sicurezza e Qualità del Software (i "plus")
  - 27. Troubleshooting e Gestione Incident in Produzione
  - 28. Coding IA
  - 29. Metodologie Agile, Product Mindset, Documentazione e Soft Skill
  - 30. Concetti Trasversali Importanti
  - 31. Dominio Pagamenti
  - 32. Dominio Assicurativo, Previdenziale e Sistemi Finanziari
  - 33. Distributed Systems Fundamentals
  - 34. System Design
  - 35. Performance Engineering
  - 36. Advanced Microservices e Event Driven
  - 37. DDD e Software Architecture
  - 38. Advanced Security e API Governance
  - 39. SRE Reliability e Chaos Engineering
  - 40. Messaging Technologies Advanced
  - 41. Automated Testing Advanced
  - 42. Advanced Observability
  - 43. Advanced Infrastructure as Code
  - 44. OAuth2 OpenID Connect e JWT Advanced
  - 45. LDAP e Active Directory
  - 46. Sicurezza J2EE SOA e API

================================================================================



################################################################################
### CAPITOLO: 01. Java (JVM, Strutture Dati, Versioni 8-25, Concorrenza e Reactive)
################################################################################

# 1. Java: JVM, Strutture Dati, Versioni (8-25), Concorrenza e Programmazione Reattiva

## Cos'è e perché conta

È il pilastro fondante per qualsiasi ruolo da **Senior Backend Developer**. I colloqui tecnici approfondiscono non solo la sintassi di Java 8+, ma la comprensione intima del **funzionamento della JVM**, la scelta ottimale delle **strutture dati** in termini di complessità computazionale (Big-O) e gestione della memoria, la padronanza della programmazione funzionale, l'evoluzione delle versioni da **Java 8 fino a Java 25 LTS**, la gestione avanzata della **concorrenza e multithreading** e il confronto architetturale tra **Programmazione Reattiva (WebFlux/Reactor)** e **Virtual Threads (Project Loom)**.

---

## 1. Java 8+ Fondamentali e Programmazione Funzionale

### Stream API
* **Operazioni intermedie (Lazy Evaluation)**: `filter`, `map`, `flatMap`, `distinct`, `sorted`, `peek`. Non eseguono alcun calcolo finché non viene invocata un'operazione terminale.
* **Operazioni terminali (Eager Execution)**: `collect`, `forEach`, `reduce`, `count`, `anyMatch`, `allMatch`, `findFirst`. Chiudono lo stream e producono un risultato o un effetto collaterale.
* **Collector avanzati**: `Collectors.groupingBy`, `partitioningBy`, `joining`, `toMap`, `toUnmodifiableList`.
* **`parallelStream()`**:
  * *Quando ha senso*: Computazioni CPU-intensive pure, prive di lock o stato condiviso, su dataset molto grandi in memoria.
  * *Quando evitarlo*: In ambienti Web/Spring Servlet; `parallelStream()` utilizza il pool globale condiviso `ForkJoinPool.commonPool()`. Se un task si blocca su I/O, satura i thread bloccando altre richieste dell'applicazione.

---

### Optional API
* **Best Practice**: Utilizzare `Optional<T>` esclusivamente come tipo di ritorno per metodi che possono non avere un valore. Evitare `Optional` come parametro di metodo, come campo di classe o all'interno di entità JPA.
* **Evitare `.get()` diretto**: Preferire `.orElseGet(() -> ...)`, `.orElseThrow(() -> new NotFoundException(...))`, `.map()`, `.flatMap()`, `.ifPresentOrElse()`.

---

### Lambda & Functional Interfaces (`java.util.function`)
Un'interfaccia funzionale ha **esattamente un metodo astratto** (annotata con `@FunctionalInterface`):
* **`Function<T, R>`** (`T -> R`, metodo `apply`): Trasformazione di un dato in un altro.
* **`Predicate<T>`** (`T -> boolean`, metodo `test`): Filtri e condizioni booleane.
* **`Consumer<T>`** (`T -> void`, metodo `accept`): Esecuzione di effetti collaterali (es. logging, invio notifiche).
* **`Supplier<T>`** (`() -> T`, metodo `get`): Lazy evaluation e factory di oggetti.
* **`BiFunction<T, U, R>`, `UnaryOperator<T>`, `BinaryOperator<T>`**.
* **Method Reference**: Sintassi compatta `Class::staticMethod`, `instance::method`, `Class::instanceMethod`, `Class::new`.

---

## 2. Java Collections Framework & Strutture Dati

```
                        ┌──────────────┐
                        │  Iterable<E> │
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │ Collection<E>│
                        └──────┬───────┘
          ┌────────────────────┼────────────────────┐
          │                    │                    │
   ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐      ┌─────────────┐
   │   List<E>   │      │    Set<E>   │      │   Queue<E>  │      │  Map<K, V>  │ (A parte)
   └──────┬──────┘      └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
          │                    │                    │                    │
   • ArrayList          • HashSet            • ArrayDeque         • HashMap
   • LinkedList         • LinkedHashSet      • PriorityQueue      • LinkedHashMap
                        • TreeSet                                 • TreeMap
                                                                  • ConcurrentHashMap
```

### A. List — Sequenza ordinata con duplicati ammessi
* **`ArrayList`**: Backed da un array dinamico.
  * Accesso per indice: $O(1)$.
  * Inserimento in coda: $O(1)$ ammortizzato (quando si riempie, alloca un nuovo array con capacità $1.5\times$ e copia gli elementi).
  * Inserimento/rimozione nel mezzo: $O(n)$ (shift di memoria tramite `System.arraycopy`).
  * **Scelta standard nel 99% dei casi** grazie alla contiguità di memoria e ottima cache locality della CPU.
* **`LinkedList`**: Lista doppiamente concatenata.
  * Inserimento/cancellazione con nodo già noto: $O(1)$. Accesso per indice: $O(n)$.
  * Forte overhead di memoria (ogni nodo alloca un oggetto con puntatori `prev` e `next`) e scarsa cache locality.

---

### B. Set — Elementi unici, nessun duplicato
* **`HashSet`**: Backed internamente da una `HashMap`. Operazioni `add`, `contains`, `remove` in $O(1)$ medio. Nessun ordine garantito.
* **`LinkedHashSet`**: Mantiene una lista doppiamente concatenata; preserva l'**ordine di inserimento**.
* **`TreeSet`**: Backed da un Red-Black Tree bilanciato. Operazioni in $O(\log n)$. Mantiene gli elementi ordinati secondo `Comparable` o `Comparator`.
* **Comportamento duplicati**: `set.add(elem)` restituisce `false` se l'elemento esiste già e **non modifica il Set** (non lancia eccezioni).

#### Il Contratto `equals()` e `hashCode()`:
1. Se $a.\text{equals}(b) == \text{true}$, allora $a.\text{hashCode}() == b.\text{hashCode}()$ **deve essere sempre vero**.
2. Se $a.\text{hashCode}() == b.\text{hashCode}()$, $a.\text{equals}(b)$ **può essere false** (collisione hash).
3. **Violazione del contratto**: Se si fa l'override di `equals()` senza aggiornare `hashCode()`, oggetti logicamente identici finiranno in bucket diversi in `HashSet` o `HashMap`, causando duplicati non rilevati o fallimento del metodo `get()`.

---

### C. Map — Coppie chiave-valore con chiavi uniche
* **`HashMap`**:
  * Operazioni `put`, `get`, `containsKey` in $O(1)$ medio.
  * *Funzionamento interno*: Calcola `hash(key)`, determina l'indice del bucket (`index = (n - 1) & hash`). In caso di collisione, gli elementi formano una lista concatenata; se il numero di elementi nel bucket supera la soglia (**TREEIFY_THRESHOLD = 8**), la lista viene convertita in un albero rosso-nero ($O(\log n)$ nel caso peggiore anziché $O(n)$).
  * `map.put(key, val)` con chiave esistente **sovrascrive il valore precedente** e ritorna il vecchio valore.
* **`LinkedHashMap`**: Mantiene l'ordine di inserimento (o di accesso, ideale per implementare cache LRU).
* **`TreeMap`**: Chiavi ordinate in Red-Black Tree ($O(\log n)$), non ammette chiavi `null`.
* **`ConcurrentHashMap`**: Thread-safe ad altissime prestazioni; non blocca l'intera mappa ma usa lock a livello di singolo bucket (striping/CAS) e letture lock-free.

---

### D. Queue & Deque
* **`ArrayDeque`**: Implementazione basata su array circolare ridimensionabile. Più efficiente e performante di `Stack` e `LinkedList`.
* **`PriorityQueue`**: Coda basata su min-heap ($O(\log n)$ per inserimento ed estrazione). Ideale per scheduling prioritario di task e transazioni.

---

## 3. Panoramica delle Versioni Java (da Java 8 a Java 25 LTS)

```
                            TIMELINE DELLE VERSIONI JAVA LTS
    Java 8 (2014) ──► Java 11 (2018) ──► Java 17 (2021) ──► Java 21 (2023) ──► Java 25 (2025)
    • Lambda/Stream   • HTTP Client      • Sealed Classes   • Virtual Threads  • Scoped Values
    • Optional        • String utils     • Record standard  • Switch Pattern   • Gen-Shenandoah
    • Date/Time API   • var nei lambda   • Strong Encaps.   • Sequenced Coll.  • Compact Headers
```

### Sintesi delle Feature per Versione:
* **Java 8 (LTS)**: Lambda, Stream API, `Optional`, Date/Time API (`java.time`), default/static methods nelle interfacce.
* **Java 9**: Module System (JPMS - Project Jigsaw), JShell REPL, miglioramenti a Stream e `CompletableFuture`.
* **Java 10**: Local Variable Type Inference (`var`).
* **Java 11 (LTS)**: Standard HTTP Client (HTTP/2 e WebSocket), `var` nei parametri lambda, rimozione moduli Java EE.
* **Java 14**: Switch Expressions standard, Helpful NullPointerExceptions.
* **Java 16**: **Records** standard (classi dati immutabili), Pattern Matching per `instanceof`.
* **Java 17 (LTS)**: **`sealed` Classes & Interfaces** standard, rimozione RMI Activation, strong encapsulation degli internals JDK.
* **Java 21 (LTS)**: **Virtual Threads (Project Loom)**, Pattern Matching per `switch`, Record Patterns, **Sequenced Collections** (`getFirst()`, `reversed()`), Generational ZGC.
* **Java 25 (LTS)**: **Scoped Values** (alternativa moderna e leggera a `ThreadLocal`), Generational Mode di Shenandoah GC promosso a standard, Compact Object Headers, Pattern matching esteso ai tipi primitivi.

---

### Deep Dive: Feature di Linguaggio Moderne

#### A. `sealed` Classes e Interfaces (Java 17)
Permette di restringere esplicitamente quali classi o interfacce possono estendere o implementare un tipo:

```java
public sealed interface PaymentMethod permits CardPayment, WalletPayment, BankTransferPayment {}

public final class CardPayment implements PaymentMethod { ... }
public final class WalletPayment implements PaymentMethod { ... }
public non-sealed class BankTransferPayment implements PaymentMethod { ... }
```
* **Vantaggio**: Consente il pattern matching su `switch` **senza bisogno del ramo `default`**, perché il compilatore verifica l'esaustività di tutti i casi a tempo di compilazione:
```java
BigDecimal fee = switch (paymentMethod) {
    case CardPayment c -> c.getAmount().multiply(new BigDecimal("0.02"));
    case WalletPayment w -> BigDecimal.ZERO;
    case BankTransferPayment b -> new BigDecimal("0.50");
};
```

#### B. Java Records (Java 16+)
Classi dati immutabili e concise: generano automaticamente campi `private final`, costruttore canonico, getter, `equals()`, `hashCode()` e `toString()`.

```java
public record PaymentRequest(String transactionId, BigDecimal amount, String currency) {
    // Compact constructor per validazioni di business
    public PaymentRequest {
        Objects.requireNonNull(transactionId, "Transaction ID cannot be null");
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
    }
}
```

---

## 4. Concorrenza e Multithreading in Java

```
                       MODELLI DI CONCORRENZA IN JAVA
   THREAD TRADIZIONALI (OS Threads)             VIRTUAL THREADS (Java 21 - Loom)
 ┌─────────────────────────────────┐           ┌─────────────────────────────────┐
 │ • 1 Thread Java = 1 Thread OS   │           │ • Milioni di Virtual Threads    │
 │ • Stack fisso (~1 MB)           │           │ • Stack dinamico (~poche centinaia Byte)│
 │ • Costoso cambio di contesto    │           │ • Smontati su I/O bloccante     │
 │ • Limite fisico: poche migliaia │           │ • Scalabilità I/O massiva       │
 └─────────────────────────────────┘           └─────────────────────────────────┘
```

### 1. Thread Pool ed `ExecutorService`
Mai creare thread manualmente con `new Thread()`. Si utilizzano thread pool gestiti:
```java
ExecutorService executor = Executors.newFixedThreadPool(10);
Future<AuthorizationResult> future = executor.submit(() -> authorizePayment(request));
AuthorizationResult result = future.get(2, TimeUnit.SECONDS); // Timeout esplicito obbligatorio
```

### 2. `CompletableFuture` (Composizione Asincrona)
Permette di costruire pipeline di calcolo asincrone non bloccanti:
```java
CompletableFuture<PaymentResponse> responseFuture = CompletableFuture
    .supplyAsync(() -> fraudService.validate(request), executor)
    .thenCompose(fraudResult -> acquirerClient.authorizeAsync(request))
    .thenApply(auth -> new PaymentResponse("APPROVED", auth.getCode()))
    .exceptionally(ex -> new PaymentResponse("REJECTED", ex.getMessage()));
```

### 3. Sincronizzazione, Concorrenza Lock-Free e Collezioni Thread-Safe
* **`synchronized`**: Mutua esclusione basata su intrinsic lock (monitor). Semplice ma rigido (nessun timeout, rischio di blocco indefinito).
* **`ReentrantLock`**: Supporta timeout (`tryLock(timeout)`), fairness policy e lock interrompibili.
* **Operazioni Atomiche (CAS - Compare-And-Swap)**: `AtomicInteger`, `AtomicLong`, `AtomicReference`, `LongAdder` (ad altissimo throughput in scrittura). Nessun lock sul thread, solo istruzioni CPU hardware atomiche.
* **`ConcurrentHashMap`**: Letture lock-free e lock granulare solo sui singoli nodi di collisione.

---

## 5. Programmazione Reattiva (Project Reactor & WebFlux)

La specifica **Reactive Streams** (`java.util.concurrent.Flow`) standardizza flussi asincroni non bloccanti con gestione della **Backpressure**:

```
                       REACTIVE STREAMS WORKFLOW
   ┌───────────────┐     1. subscribe()      ┌───────────────┐
   │               │ ◄────────────────────── │               │
   │  PUBLISHER    │     2. onSubscribe(sub) │  SUBSCRIBER   │
   │ (Mono / Flux) │ ──────────────────────► │               │
   │               │     3. request(n)       │               │
   │               │ ◄────────────────────── │ (Contropressione)
   │               │     4. onNext(data)     │               │
   └───────────────┘ ──────────────────────► └───────────────┘
```

### Componenti di Project Reactor:
* **`Mono<T>`**: Emittente reattivo per **0 o 1 elemento** (`CompletableFuture` potenziato).
* **`Flux<T>`**: Emittente reattivo per **$0 \dots N$ elementi** (stream potenzialmente infinito).
* **Backpressure**: Il Subscriber comunica al Publisher quanti dati può ricevere (`request(n)`), impedendo che un flusso rapido saturi la memoria del consumatore (*OutOfMemoryError*).

```java
public Mono<PaymentResponse> processPayment(PaymentRequest request) {
    return accountClient.getAccount(request.accountId())
        .switchIfEmpty(Mono.error(new AccountNotFoundException("Conto inesistente")))
        .filter(account -> account.getBalance().compareTo(request.amount()) >= 0)
        .switchIfEmpty(Mono.error(new InsufficientFundsException("Fondi insufficienti")))
        .flatMap(account -> acquirerClient.authorize(request)) // Chiamata HTTP non bloccante
        .map(authResult -> new PaymentResponse("SUCCESS", authResult.getAuthCode()))
        .timeout(Duration.ofMillis(3000))
        .onErrorResume(TimeoutException.class, ex -> Mono.just(new PaymentResponse("TIMEOUT", null)));
}
```

---

## 6. Architettura della JVM e Garbage Collection

```
┌────────────────────────────────────────────────────────────────────────┐
│                               JVM MEMORY                               │
├────────────────────────────────────────┬───────────────────────────────┤
│               HEAP MEMORY              │       NON-HEAP (Native)       │
│  (Condiviso tra tutti i thread)        │                               │
│                                        │  ┌─────────────────────────┐  │
│  ┌───────────────────┬──────────────┐  │  │        METASPACE        │  │
│  │    YOUNG GEN      │   OLD GEN    │  │  │ (Class metadata,        │  │
│  │ ┌──────┬────────┐ │  (Tenured)   │  │  │  Constant pool,        │  │
│  │ │ Eden │ S0│ S1 │ │  Oggetti a   │  │  │  Method bytecode)       │  │
│  │ └──────┴────────┘ │  lunga vita  │  │  └─────────────────────────┘  │
│  └───────────────────┴──────────────┘  │                               │
├────────────────────────────────────────┴───────────────────────────────┤
│            PER-THREAD MEMORY (Isolata per ciascun thread)              │
│  ┌───────────────────────────┐         ┌────────────────────────────┐  │
│  │       THREAD STACK        │         │   PC REGISTER & NATIVE     │  │
│  │ (Frames, primitive, refs) │         │   STACK                    │  │
│  └───────────────────────────┘         └────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

### Struttura della Memoria:
* **Heap**: Spazio condiviso dove risiedono tutti gli oggetti istanziati e i Bean Spring.
  * **Young Gen (Eden, S0, S1)**: Oggetti a vita breve.
  * **Old Gen (Tenured)**: Oggetti sopravvissuti a più cicli di GC.
* **Thread Stack**: Privato per ciascun thread (`-Xss`), contiene variabili primitive locali e puntatori a oggetti.
* **Metaspace**: Memoria nativa OS per metadati di classi caricate, bytecode e reflection info.

### Algoritmi di Garbage Collection:
* **G1 GC (Default)**: Divide lo heap in regioni (1-32MB), colleziona prioritariamente le regioni con più immondizia nel rispetto del tempo target `-XX:MaxGCPauseMillis`.
* **ZGC & Shenandoah**: GC a bassissima latenza (pause **$< 1\text{ ms}$** indipendentemente dalla dimensione dell'heap fino a Terabyte), eseguono marking e compattazione in parallelo con i thread dell'applicazione.

---

## 7. Reactive Programming vs Virtual Threads (Java 21)

| Caratteristica | Reactive Programming (WebFlux / Reactor) | Virtual Threads (Java 21 + Spring MVC) |
| :--- | :--- | :--- |
| **Stile di Codice** | Dichiarativo, a pipeline funzionale (`Mono/Flux`) | Imperativo sincrono e lineare (`try/catch`, sequenziale) |
| **Scalabilità I/O** | Altissima (non-blocking event loop su Netty) | Altissima (i thread virtuali si smontano durante I/O bloccante) |
| **Complessità & Debug** | Molto elevata: stack trace frammentati | Minima: stack trace standard lineari |
| **Thread Context / MDC**| Complesso (richiede `Reactor Context`) | Trasparente (`ThreadLocal` e Scoped Values nativi) |
| **Compatibilità Legacy**| Richiede driver reattivi (R2DBC, WebClient) | **Compatibile 100% con JDBC, Hibernate e librerie standard** |

---

## 8. Domande tipiche a colloquio (e risposte da Senior)

- *D: Qual è la differenza tra `ArrayList` e `LinkedList` e perché quasi sempre si sceglie `ArrayList`?*
  - **R**: `ArrayList` usa un array contiguo in memoria con accesso per indice in $O(1)$ e ottima cache locality CPU. `LinkedList` alloca oggetti sparsi collegati da puntatori: l'accesso per indice è $O(n)$, l'overhead di memoria per i puntatori è elevato e la frammentazione in memoria rende le prestazioni reali quasi sempre inferiori rispetto ad `ArrayList`.

- *D: Come funzionano i Virtual Threads di Java 21 rispetto ai Platform Threads?*
  - **R**: I Platform Threads mappano 1:1 sui thread del sistema operativo (costosi in RAM ~1MB ciascuno e limitati nel numero). I Virtual Threads sono gestiti dal runtime della JVM con un'occupazione di pochi byte: quando un Virtual Thread esegue un'operazione I/O bloccante (es. query SQL o chiamata HTTP), viene "smontato" dal carrier thread del sistema operativo, liberandolo per servire altri Virtual Thread. Questo consente milioni di connessioni concorrenti con codice sincrono e leggibile.

- *D: Cosa succede se in un'applicazione Spring WebFlux esegui una chiamata JDBC bloccante o `Thread.sleep()`?*
  - **R**: WebFlux esegue su un Event Loop (Netty) con un numero ridottissimo di thread (pari ai core CPU). Bloccare uno di questi thread paralizza un quarto o metà dell'intera capacità elaborativa dell'applicazione. Per chiamare codice bloccante legacy in Reactor, occorre isolarlo esplicitamente su uno scheduler elastico separato (`.subscribeOn(Schedulers.boundedElastic())`).

---

## 9. Come esercitarsi

1. **Stream & Collections Mastery**: Scrivi un metodo che, data una lista di transazioni finanziarie, le raggruppi per valuta e stato, calcoli l'importo medio per gruppo, escluda i gruppi con meno di 5 transazioni e restituisca una mappa ordinata.
2. **Virtual Threads Benchmark**: Configura un'applicazione Spring Boot 3.2+ con `spring.threads.virtual.enabled=true` e verifica come un endpoint che simula un I/O bloccante da 200 ms gestisce 10.000 richieste concorrenti senza saturare il sistema operativo.



################################################################################
### CAPITOLO: 02. Linguaggi Alternativi: Go e Scala (Paradigmi Funzionali)
################################################################################

# 2. Linguaggi Alternativi: Go e Scala (Paradigmi Funzionali)

## Cos'è e perché conta

In molte aziende tech, fintech e scale-up moderne, i team backend operano in contesti **poliglotti**:
* **Go (Golang)**: Scelto per microservizi cloud-native ad altissimo throughput, proxy di rete, strumenti infrastrutturali e servizi con vincoli stringenti di latenza e memoria.
* **Scala**: Scelto per sistemi distribuiti ad altissima affidabilità, architetture a messaggi reattive (Actor Model con Akka/Pekko), data engineering (Apache Spark) ed espressione pura della **Programmazione Funzionale (FP)** sulla JVM.

Per un ingegnere backend Senior Java, conoscere questi linguaggi e i rispettivi paradigmi (CSP in Go, FP pura e Monadi in Scala) amplia drasticamente il ventaglio di soluzioni architetturali e fa la differenza nei colloqui di alto livello.

---

## 1. Go (Golang): Architettura e Concorrenza per Sviluppatori Java

Creato da Google (Robert Griesemer, Rob Pike, Ken Thompson), Go privilegia la **semplicità radicale**, la facilità di lettura e l'efficienza esecutiva.

```
                  CONFRONTO ARCHITETTURALE: JAVA vs GO
   JAVA APPLICATION                            GO APPLICATION
 ┌───────────────────────────┐               ┌───────────────────────────┐
 │ Bytecode (.class / .jar)  │               │ Singolo Binario Nativo    │
 ├───────────────────────────┤               │ (Compilazione Diretta)    │
 │ Java Virtual Machine (JVM)│               ├───────────────────────────┤
 ├───────────────────────────┤               │ Runtime Go Minimale (GC,  │
 │ OS Kernel (Pthreads)      │               │ Go Scheduler, Network)    │
 └───────────────────────────┘               └───────────────────────────┘
```

### Caratteristiche Fondamentali di Go

#### 1. Zero Classi, Solo Structs e Metodi
In Go non esiste la parola chiave `class` né l'ereditarietà classica. I dati sono incapsulati in `struct` e i metodi sono collegati tramite un **Receiver**:

```go
type Payment struct {
    ID     string
    Amount float64
    Status string
}

// Metodo con Value Receiver (riceve una copia)
func (p Payment) IsCompleted() bool {
    return p.Status == "COMPLETED"
}

// Metodo con Pointer Receiver (modifica la struct originale in-place)
func (p *Payment) Complete() {
    p.Status = "COMPLETED"
}
```

#### 2. Interfacce Implicite ("Duck Typing" Statico)
In Go non esiste la clausola `implements`. Se una struct implementa tutti i metodi definiti da un'interfaccia, implementa **automaticamente** quell'interfaccia.

```go
type Processor interface {
    Process(amount float64) error
}

type StripeService struct{}

// StripeService implementa Processor automaticamente
func (s StripeService) Process(amount float64) error {
    // Chiamata API Stripe
    return nil
}
```

---

### La Concorrenza in Go: CSP (Communicating Sequential Processes)

Il principio cardine di Go è: *"Do not communicate by sharing memory; instead, share memory by communicating."*

```
                       GOROUTINES E CHANNELS IN GO
   ┌─────────────────┐       ch <- payment       ┌─────────────────┐
   │ Producer        │ ────────────────────────► │ Channel (chan)  │
   │ (Goroutine 1)   │                           │ [ Buffer Coda ] │
   └─────────────────┘                           └────────┬────────┘
                                                          │ payment := <-ch
                                                          ▼
                                                 ┌─────────────────┐
                                                 │ Consumer Worker │
                                                 │ (Goroutine 2)   │
                                                 └─────────────────┘
```

#### 1. Goroutines
* Thread ultra-leggeri gestiti in user-space dal runtime Go (M:N scheduler multiplexato sui thread del kernel).
* Occupano solo **2 KB di stack** iniziale (che cresce e decresce dinamicamente), contro l'1 MB fisso dei classici thread del sistema operativo / JVM platform threads. (Concetto simile ai *Virtual Threads* di Java 21).
* Avvio istantaneo con la parola chiave `go`:
  ```go
  go processTransaction(tx)
  ```

#### 2. Channels (`chan T`) & `select`
I canali consentono il passaggio sicuro di dati e sincronizzazione tra goroutine senza ricorrere a lock espliciti:

```go
func worker(jobs <-chan int, results chan<- int) {
    for n := range jobs {
        results <- n * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // Avvio di 3 goroutine concorrenti
    for w := 1; w <= 3; w++ {
        go worker(jobs, results)
    }
    
    // Invio job e lettura risultati con select / timeouts
}
```

#### 3. Gestione degli Errori: Error Values vs Eccezioni
In Go non esistono `try-catch-finally`. Le funzioni restituiscono un valore di errore esplicito come valore di ritorno multiplo:

```go
func Transfer(from, to string, amount float64) (string, error) {
    if amount <= 0 {
        return "", fmt.Errorf("importo non valido: %f", amount)
    }
    // Esecuzione trasferimento
    return "TX_12345", nil
}

// Idiomatic Go error handling
txId, err := Transfer("ACC_1", "ACC_2", 150.00)
if err != nil {
    log.Printf("Trasferimento fallito: %v", err)
    return
}
```

---

## 2. Scala & la Programmazione Funzionale (FP) sulla JVM

**Scala** (Scalable Language) è un linguaggio ibrido ad alta espressività che gira sulla **JVM** e combina la Programmazione ad Oggetti con la **Programmazione Funzionale pura**.

### Concetti Chiave di Scala & FP

#### 1. Immutabilità & Case Classes
In Scala l'immutabilità è la scelta predefinita (`val` per variabili immutabili, `var` per mutabili).
Le **Case Classes** sono classi immutabili ricche (l'ispirazione diretta per i *Java Records*):

```scala
case class Transaction(id: String, amount: BigDecimal, currency: String = "EUR")

val tx1 = Transaction("TX_01", BigDecimal(100.0))
// Modifica non-distruttiva tramite copy()
val tx2 = tx1.copy(amount = BigDecimal(150.0))
```

#### 2. Pattern Matching & Algebraic Data Types (ADTs)
Gli ADT consentono di modellare gli stati di business con precisione matematica (`sealed trait` + `case class`/`case object`):

```scala
sealed trait PaymentStatus
case object Pending extends PaymentStatus
case class Authorized(authCode: String) extends PaymentStatus
case class Settled(settlementDate: java.time.LocalDate) extends PaymentStatus
case class Rejected(errorCode: String, reason: String) extends PaymentStatus

def handleStatus(status: PaymentStatus): String = status match {
  case Pending                  => "In attesa di elaborazione"
  case Authorized(code)         => s"Autorizzato con codice: $code"
  case Settled(date)            => s"Regolato in data $date"
  case Rejected("ERR_01", msg)  => s"Rifiutato per frode: $msg"
  case Rejected(_, msg)         => s"Rifiuto generico: $msg"
}
```

#### 3. Le Monadi per la Gestione degli Effetti e degli Errori
In FP pura, le funzioni non devono avere effetti collaterali (*Side Effects*) e non devono lanciare eccezioni impreviste. Si usano i tipi monadici:

* **`Option[T]` (`Some(v)` / `None`)**: Elimina il `NullPointerException`.
* **`Try[T]` (`Success(v)` / `Failure(e)`)**: Incapsula operazioni che possono lanciare eccezioni.
* **`Either[L, R]` (`Left(error)` / `Right(value)`)**: Gestione funzionale degli errori di business (*Railway-Oriented Programming*).

```scala
def parseAmount(raw: String): Either[String, BigDecimal] =
  Try(BigDecimal(raw)).toEither.left.map(_ => "Formato importo non valido")

def validatePositive(amount: BigDecimal): Either[String, BigDecimal] =
  if (amount > 0) Right(amount) else Left("L'importo deve essere positivo")

// Composizione con For-Comprehension (sintassi fluida monadica)
def processInput(raw: String): Either[String, BigDecimal] = for {
  amount   <- parseAmount(raw)
  validAmt <- validatePositive(amount)
} yield validAmt
```

---

### Ecosistemi Concorrenti in Scala

1. **Actor Model (Akka / Apache Pekko)**:
   * I componenti sono **Attori** isolati con stato privato che comunicano esclusivamente tramite invio asincrono di messaggi immutabili nella propria *Mailbox*.
   * Strategie di supervisione gerarchica (*Let it crash* pattern) per auto-riparazione e tolleranza ai guasti distribuita.
2. **Functional Effect Systems (Cats Effect / ZIO)**:
   * Framework basati sulla purezza referenziale, dove i programmi sono descritti come valori (*Effect Data Types*) eseguiti da un runtime a **Fibre** (micro-thread ad altissime prestazioni).

---

## 3. Matrice Comparativa: Java vs Go vs Scala

| Categoria | Java (17/21+) | Go (Golang) | Scala (3.x) |
| :--- | :--- | :--- | :--- |
| **Runtime** | JVM (HotSpot / GraalVM) | Nativo (Singolo Binario compilato) | JVM |
| **Paradigma** | OOP con elementi FP (Stream, Record) | Imperativo / Procedurale + CSP | Ibrido OOP + Pure Functional (FP) |
| **Concorrenza** | Thread OS / Virtual Threads (Project Loom) | **Goroutines & Channels (CSP)** | **Actor Model (Pekko) / Fibre (ZIO)** |
| **Error Handling** | Eccezioni (`try-catch`, Checked/Unchecked) | Valori di ritorno espliciti (`err != nil`) | Tipi Monadici (`Option`, `Either`, `Try`) |
| **Memory Footprint**| Medio-Alto (Heap JVM) | **Bassissimo (poche decine di MB)** | Medio-Alto (JVM) |
| **Startup Time** | Più lento (JIT warmup) / Veloce con GraalVM Native | **Istantaneo (< 10 ms)** | Più lento (JIT) |
| **Casi d'Uso Ideali**| Enterprise Core, Banking, Spring Microservices | Microservizi Cloud-Native, CLI, Proxy, K8s | Sistemi Reattivi, Big Data (Spark), FP pura |

---

## 4. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come si confrontano le Goroutine di Go con i Thread tradizionali di Java e i nuovi Virtual Threads di Java 21?*
  - **R**: I thread tradizionali di Java sono 1:1 con i thread del kernel OS, con stack fisso (~1 MB) e cambi di contesto costosi gestiti dall'OS. Le goroutine di Go sono thread leggeri in user-space con stack iniziale di 2 KB, multiplexate su thread OS dal runtime Go. I **Virtual Threads di Java 21 (Project Loom)** introducono un modello M:N molto simile a Go sulla JVM, consentendo milioni di thread concorrenti con stack dinamico senza bloccare i carrier thread dell'OS durante le operazioni di I/O bloccante.

- *D: Perché Go non supporta l'ereditarietà classica delle classi e come realizza il polimorfismo?*
  - **R**: Go favorisce esplicitamente la **composizione rispetto all'ereditarietà** (*Composition over Inheritance*) per evitare gerarchie di classi fragili e accoppiate. Il riuso del codice si ottiene incorporando (*struct embedding*) una struct dentro un'altra. Il polimorfismo è garantito dalle **interfacce implicite** (*structural typing / duck typing*): qualunque tipo che implementi la firma dei metodi richiesti soddisfa automaticamente l'interfaccia senza bisogno di dichiararlo esplicitamente.

- *D: Qual è il vantaggio di usare `Either[Error, Value]` in Scala rispetto al lanciare un'eccezione tradizionale in Java?*
  - **R**: Lanciare un'eccezione interrompe il flusso di controllo, è invisibile nella firma dei metodi (se unchecked) e rende il codice impuro (*non referenzialmente trasparente*), oltre a comportare il costo computazionale del riempimento dello stack trace. `Either` rende l'eventualità di fallimento un valore di ritorno esplicito e tipizzato nel contratto del metodo, permettendo di comporre flussi di calcolo complessi in modo sicuro e dichiarativo tramite monadi o for-comprehension (*Railway-Oriented Programming*).



################################################################################
### CAPITOLO: 03. Database Relazionali, NoSQL e Strategie di Accesso
################################################################################

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



################################################################################
### CAPITOLO: 04. Redis
################################################################################

# 4. Redis e Caching Distribuito

### Cos'è
Database **in-memory key-value**, estremamente veloce (dati tenuti in RAM), usato principalmente come cache, ma anche come message broker leggero (pub/sub), store di sessioni, o per strutture dati specializzate (contatori, code, set, sorted set).

### Caratteristiche principali

- **Strutture dati ricche**: non solo stringhe, ma anche liste, set, hash, sorted set (utili per classifiche/ranking), tutte con operazioni atomiche native
- **Persistenza opzionale**: pur essendo in-memory, supporta snapshot su disco (RDB) o log delle operazioni (AOF) per non perdere tutto in caso di riavvio — comunque non sostituisce un DB transazionale
- **TTL (Time To Live)**: ogni chiave può avere una scadenza automatica — fondamentale per cache che non deve restare stale indefinitamente
- **Operazioni atomiche**: es. `INCR` per contatori concorrenti senza race condition, utile per rate limiting
- **Pub/Sub**: meccanismo di messaggistica semplice (non persistente come Kafka — se non c'è un subscriber attivo, il messaggio si perde)
- **Cluster mode**: sharding automatico dei dati su più nodi per scalabilità orizzontale

### Esempio di utilizzo (Spring Boot)

```java
// Cache di un risultato costoso da ricalcolare
@Cacheable(value = "accountBalance", key = "#accountId")
public BigDecimal getBalance(String accountId) {
    return accountRepository.calculateBalance(accountId); // query pesante
}

// Idempotency key con TTL, via RedisTemplate
public boolean tryLockIdempotencyKey(String key) {
    Boolean success = redisTemplate.opsForValue()
        .setIfAbsent(key, "PROCESSED", Duration.ofMinutes(10));
    return Boolean.TRUE.equals(success); // true solo se la chiave non esisteva già
}
```

### Rilevanza per il dominio pagamenti
Due casi d'uso molto naturali: **cache** per dati letti di frequente e poco variabili (es. configurazioni, dati anagrafici merchant), e **gestione dell'idempotenza** tramite `SETNX`/`setIfAbsent` con TTL — un modo rapido per verificare "questa richiesta è già stata processata?" senza appesantire il DB transazionale principale. Anche utile per **rate limiting** sulle chiamate verso circuiti esterni, con `INCR` + TTL per contare le richieste in una finestra temporale.

### Domande tipiche e risposte

- *D: Redis è adatto a salvare il saldo di un conto come fonte di verità?*
  R: No — è in-memory e pensato per velocità, non per le garanzie ACID complete che servono per il ledger. Il saldo "vero" resta su Oracle; Redis può cachearne una copia in lettura, ma ogni scrittura deve passare dal DB transazionale.

- *D: Come implementeresti un idempotency check con Redis?*
  R: Con `SETNX` (o `setIfAbsent` in Spring Data Redis) usando l'idempotency key come chiave — l'operazione è atomica, quindi se due richieste concorrenti arrivano nello stesso istante, solo una riuscirà a impostare la chiave, l'altra saprà che la richiesta è già in corso/completata. Si imposta un TTL per non accumulare chiavi indefinitamente.



################################################################################
### CAPITOLO: 05. Database Migration Software (Flyway e Liquibase)
################################################################################

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



################################################################################
### CAPITOLO: 06. Strategie per la Gestione dei Database in Architetture a Microservizi
################################################################################

# 6. Strategie per la Gestione dei Database in Architetture a Microservizi

### Cos'è e perché conta
Riassume e completa in chiave pratica i pattern già visti nelle sezioni sui microservizi e sull'accesso ai database (punti 8 e 10), rispondendo alla domanda "come gestisco letture/scritture concorrenti quando i dati sono sparsi su più servizi?" — un tema molto probabile in un colloquio senior, perché è dove la teoria dei microservizi incontra i problemi reali di concorrenza e consistenza.

### Cosa studiare

**1. Database per Microservizio (Database per Service)**

Ogni microservizio ha il proprio database dedicato — pattern già visto nel punto 8. I vantaggi principali:
- **Isolamento dei dati**: un servizio non può corrompere accidentalmente i dati di un altro
- **Indipendenza tecnologica**: ogni servizio può usare il DB più adatto al proprio caso d'uso (vedi tabella comparativa nel punto 12 — es. Oracle per il ledger, Redis per cache di un servizio specifico)
- **Riduzione delle dipendenze**: un servizio può evolvere lo schema del proprio DB senza coordinarsi con tutti gli altri

Il rovescio della medaglia (utile menzionarlo per dimostrare visione equilibrata): niente più join SQL tra dati di servizi diversi, e niente più transazione ACID unica che copre più servizi — da qui nascono i pattern successivi.

**2. Event Sourcing e CQRS**

Già introdotti nel punto 8, li ripercorriamo con focus sulla gestione della concorrenza:
- Gli eventi vengono memorizzati in un **log di eventi** immutabile (append-only) — invece di sovrascrivere lo stato, si registra ogni cambiamento come nuovo evento
- I comandi (scritture) modificano lo stato generando nuovi eventi, mentre le query (letture) leggono da una **vista materializzata** separata, costruita e aggiornata a partire dagli eventi
- Perché riduce i conflitti di concorrenza: dato che le scritture sono append-only (si aggiunge un nuovo evento, non si modifica uno esistente), il classico problema del "lost update" tra due scritture concorrenti sullo stesso record si riduce drasticamente
- Offre **tracciabilità completa**: ogni cambiamento di stato è ricostruibile — molto rilevante in un dominio regolamentato come i pagamenti, dove poter dimostrare "chi ha cambiato cosa e quando" è spesso un requisito di audit/compliance

**3. Transazioni Distribuite**

- **Saga pattern** (già visto nel punto 8): sequenza di transazioni locali con compensazioni in caso di fallimento — l'approccio oggi preferito nei microservizi
- **Two-Phase Commit (2PC)**: protocollo classico per garantire consistenza tra più risorse — un coordinatore chiede a tutti i partecipanti di "prepararsi" (fase 1, ognuno conferma che può eseguire l'operazione), e solo se **tutti** confermano invia il comando di commit definitivo (fase 2); se anche uno solo fallisce nella fase di prepare, tutti fanno rollback
  - *Perché in pratica si evita nei microservizi moderni*: 2PC richiede che tutte le risorse restino bloccate (lock) per tutta la durata del protocollo, in attesa della decisione finale del coordinatore — questo riduce drasticamente la disponibilità e non scala bene, oltre a creare un singolo punto di fallimento nel coordinatore. Per questo la Saga (che rinuncia alla atomicità immediata in cambio di eventual consistency con compensazioni) è preferita nella maggior parte dei sistemi distribuiti moderni
- **Transazioni di compensazione**: l'azione di "annullamento logico" usata nella Saga quando un passo successivo fallisce — non è un vero rollback (impossibile su DB separati), ma un'operazione inversa esplicita (es. se hai già addebitato un conto, la compensazione è un accredito di pari importo, non la cancellazione della scrittura originale)

**4. Architettura Event-Driven**

Un message broker (Kafka, RabbitMQ) disaccoppia i servizi:
- Il produttore pubblica un evento senza sapere chi lo consumerà, né aspettare che venga processato
- Garantisce consistenza attraverso **code di messaggi** persistenti: se un consumer è temporaneamente giù, i messaggi restano in coda e vengono processati al suo ritorno, invece di perdersi
- Permette operazioni **asincrone**, già discusso nel punto 8 per il caso della notifica post-transazione

**5. Locking e Concurrency Control**

Già accennato nella sezione Oracle (punto 3) parlando di isolation level, qui si generalizza al contesto applicativo:
- **Pessimistic locking**: si blocca la risorsa (es. `SELECT FOR UPDATE`) per tutta la durata dell'operazione, impedendo ad altri di modificarla nel frattempo — sicuro ma riduce la concorrenza, utile quando i conflitti sono frequenti
- **Optimistic locking**: non si blocca nulla in anticipo; si verifica invece, al momento del salvataggio, che i dati non siano stati modificati da qualcun altro nel frattempo — tipicamente con una colonna di versione (`@Version` in JPA): se la versione letta non coincide più con quella a DB, l'update fallisce e va gestito un retry o un errore applicativo. Preferibile quando i conflitti sono rari, perché non paga il costo del lock quando non serve
- **Meccanismi di retry e gestione dei conflitti**: quando un optimistic lock fallisce, la strategia comune è ritentare l'operazione (spesso con backoff, collegandosi al punto sulla resilienza nel punto 11) invece di propagare subito l'errore all'utente

**6. Sharding e Partizionamento**

Già visto nel punto 10 per il contesto Oracle/tabelle grandi, qui nella lente della gestione dati distribuita tra servizi:
- **Suddivisione orizzontale dei dati** su più istanze/nodi in base a una chiave (es. per range di data, per hash di un ID account)
- Migliora prestazioni e scalabilità perché ogni nodo gestisce solo una porzione dei dati e del carico
- Riduce i colli di bottiglia, ma introduce complessità: query che devono aggregare dati da più shard diventano più costose, e la scelta della shard key è una decisione difficile da cambiare in seguito senza una migrazione onerosa

**7. Caching Distribuito**

Già visto nel punto 10 come pattern di ottimizzazione, qui nel contesto specifico della concorrenza tra servizi:
- Redis/Memcached come cache condivisa tra più istanze di uno stesso servizio (o tra servizi diversi, se il dato è comune)
- Riduce il carico sul database per i dati letti più di frequente
- Attenzione alla **coerenza tra cache e DB**: in un sistema con più scritture concorrenti, una cache non invalidata correttamente può restituire dati obsoleti — un problema di concorrenza a sé, spesso sottovalutato

### Considerazioni chiave e raccomandazioni

Nessuna di queste soluzioni è universale — la scelta dipende da:
- Dimensioni del sistema e volumi di dati
- Requisiti di consistenza (forte vs eventual)
- Complessità delle operazioni coinvolte
- Performance richieste (latenza, throughput)

Un buon approccio, utile anche come risposta "da senior" a colloquio:
- **Iniziare semplice** e aggiungere complessità solo quando serve realmente — introdurre Saga/Event Sourcing/sharding fin da subito su un sistema piccolo è spesso over-engineering
- **Valutare i requisiti specifici** prima di scegliere il pattern, non il contrario
- **Testare accuratamente i meccanismi di concorrenza** — sono la categoria di bug più insidiosa perché spesso non si manifestano in ambienti di test a basso carico
- **Implementare monitoraggio e logging** (collegandosi al punto 11 sull'osservabilità) per individuare rapidamente conflitti, retry falliti, o incoerenze tra servizi in produzione

### Come esercitarti
Prepara una risposta strutturata alla domanda "come garantiresti la consistenza di un pagamento che coinvolge tre microservizi diversi (autorizzazione, contabilità, notifica)?" — la risposta ideale cita: database per service come punto di partenza architetturale, Saga con compensazioni per coordinare i tre servizi, eventi asincroni via Kafka/RabbitMQ per disaccoppiarli, e idempotenza (già vista più volte nel documento) per gestire in sicurezza eventuali retry.



################################################################################
### CAPITOLO: 07. Design Pattern e Principi SOLID
################################################################################

# 7. Principi di Architettura Software, Design Pattern, NFR, TDD, BDD e Refactoring

## Cos'è e perché conta

Per un ingegnere software Senior, la "buona architettura" non è una nozione teorica astratta, ma la capacità quotidiana di **scrivere software manutenibile, testabile, resiliente e facilmente estendibile**, guidando il team nell'applicazione rigorosa dei principi di design (**SOLID, DRY, KISS, Law of Demeter**), nella scelta consapevole dei **Design Pattern**, nella definizione e rispetto dei **Requisiti Non Funzionali (NFR)** e nell'adozione di pratiche di sviluppo disciplinate come **TDD, BDD e Refactoring Continuo**.

---

## 1. Principi Fondamentali di Architettura e Design

```
                               PRINCIPI ARCHITETTURALI CORE
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ SOLID (S - Single Resp, O - Open/Closed, L - Liskov, I - Segreg, D - Invers)│
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ DRY (Don't Repeat Yourself)      │ Evita duplicazione di logica di business │
  ├──────────────────────────────────┼──────────────────────────────────────────┤
  │ KISS (Keep It Simple, Stupid)    │ Preferisci la soluzione più semplice     │
  ├──────────────────────────────────┼──────────────────────────────────────────┤
  │ YAGNI (You Aren't Gonna Need It) │ Non scrivere codice per requisiti futuri │
  ├──────────────────────────────────┼──────────────────────────────────────────┤
  │ Law of Demeter (Least Knowledge) │ Non parlare con gli "sconosciuti"        │
  └──────────────────────────────────┴──────────────────────────────────────────┘
```

### I Principi SOLID nel Dettaglio

#### 1. Single Responsibility Principle (SRP)
* *Regola*: Una classe deve avere **una sola ragione per cambiare** (un solo attore/responsabilità di business).
* *Esempio*: Separare `PaymentExecutionService` (orchestra il pagamento), `PaymentReceiptGenerator` (genera il PDF) e `NotificationSender` (invia email/SMS), anziché concentrare tutto in un'unica classe monolitica da 2000 righe.

#### 2. Open/Closed Principle (OCP)
* *Regola*: Le entità software devono essere **aperte all'estensione, ma chiuse alla modifica**.
* *Esempio*: Per supportare un nuovo gateway di pagamento (es. *Apple Pay*), non si modifica la classe `PaymentService` esistente con nuovi blocchi `if-else`, ma si crea una nuova classe `ApplePayGateway` che implementa l'interfaccia `PaymentGateway`.

#### 3. Liskov Substitution Principle (LSP)
* *Regola*: I sottotipi devono poter sostituire i tipi base senza alterare la correttezza del programma.
* *Violazione tipica*: Lanciare `UnsupportedOperationException` in un metodo ereditato (es. una classe `ReadOnlyAccount` che estende `Account` e lancia eccezione sul metodo `debit()`).
* *Soluzione*: Ristrutturare la gerarchia separando `ReadableAccount` e `TransactableAccount`.

#### 4. Interface Segregation Principle (ISP)
* *Regola*: I client non devono essere costretti a dipendere da metodi che non utilizzano. Preferire molte interfacce piccole e coese a un'unica interfaccia "grassa".
* *Esempio*: Separare `PaymentProcessor`, `RefundProcessor` e `ReconciliationProcessor` invece di un'unica interfaccia `AllInOnePaymentManager`.

#### 5. Dependency Inversion Principle (DIP)
* *Regola*: I moduli di alto livello (logica di business) non devono dipendere da moduli di basso livello (database, client HTTP), ma entrambi devono dipendere da **astrazioni (interfacce)**.
* *In Spring*: È il fondamento della *Dependency Injection* e dell'**Architettura Esagonale (Ports & Adapters)**.

---

### Altri Principi Chiave:
* **Law of Demeter (Principio della Minima Conoscenza)**:
  * Un metodo deve invocare solo metodi dei propri campi, parametri passati o oggetti istanziati localmente.
  * *Anti-Pattern (Train Wreck)*: `order.getCustomer().getAddress().getCity().toUpperCase()` $\to$ accoppia la classe con 4 livelli interni.
  * *Soluzione*: `order.getCustomerCity()`.
* **DRY vs Duplicazione Accidentale**:
  * DRY si riferisce alla duplicazione di **conoscenza di business**, non a righe di codice superficialmente identiche che evolvono per ragioni diverse (es. il DTO di un'API REST e l'Entità JPA di persistenza non devono essere forzatamente unificati).

---

## 2. GoF Design Pattern per il Backend Enterprise

```
┌──────────────────┬──────────────────────┬────────────────────────────────────────────────────────┐
│ Categoria        │ Pattern              │ Caso d'Uso Tipico in Java / Spring                     │
├──────────────────┼──────────────────────┼────────────────────────────────────────────────────────┤
│ **Creational**   │ **Factory Method**   │ Creazione gateway corretto in base al tipo transazione │
│                  │ **Builder**          │ Costruzione immutabile di oggetti ricchi e complessi   │
│                  │ **Singleton**        │ Scope predefinito dei bean Spring nel container IoC    │
├──────────────────┼──────────────────────┼────────────────────────────────────────────────────────┤
│ **Structural**   │ **Strategy**         │ Algoritmi di calcolo commissioni o instradamento carte │
│                  │ **Adapter**          │ Adattamento tracciati ISO 8583 a modelli interni JSON   │
│                  │ **Decorator / Proxy**│ Logging, Caching (`@Cacheable`), Spring AOP transazioni│
├──────────────────┼──────────────────────┼────────────────────────────────────────────────────────┤
│ **Behavioral**   │ **Observer**         │ Eventi di dominio asincroni (`ApplicationEventPublisher`)│
│                  │ **Chain of Resp.**   │ Pipeline di validazione transazioni o Security Filters │
│                  │ **State Pattern**    │ Macchina a stati di un pagamento (Created/Auth/Settled)│
└──────────────────┴──────────────────────┴────────────────────────────────────────────────────────┘
```

### Esempio Applicato: Strategy + Factory con Spring
```java
// Interfaccia Strategy
public interface FeeCalculator {
    BigDecimal calculate(Payment payment);
    PaymentType getSupportedType();
}

@Component
public class CardFeeCalculator implements FeeCalculator {
    public BigDecimal calculate(Payment p) { return p.getAmount().multiply(new BigDecimal("0.015")); }
    public PaymentType getSupportedType() { return PaymentType.CARD; }
}

@Component
public class SepaFeeCalculator implements FeeCalculator {
    public BigDecimal calculate(Payment p) { return new BigDecimal("0.50"); }
    public PaymentType getSupportedType() { return PaymentType.SEPA; }
}

// Factory dinamica tramite Spring Dependency Injection
@Service
public class FeeCalculatorFactory {
    private final Map<PaymentType, FeeCalculator> calculators;

    public FeeCalculatorFactory(List<FeeCalculator> calculatorList) {
        this.calculators = calculatorList.stream()
            .collect(Collectors.toMap(FeeCalculator::getSupportedType, Function.identity()));
    }

    public FeeCalculator getCalculator(PaymentType type) {
        return Optional.ofNullable(calculators.get(type))
            .orElseThrow(() -> new IllegalArgumentException("Nessun calcolatore per: " + type));
    }
}
```

---

## 3. Requisiti Non Funzionali (NFRs - Non-Functional Requirements)

Gli NFR definiscono i **criteri di qualità e i vincoli architetturali** con cui il sistema deve operare:

```
                            LE DIMENSIONI DEGLI NFR
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │   Scalability    │    │   Performance    │    │   Availability   │    │     Security     │
  │ • Throughput TPS │    │ • Latency p95/p99│    │ • SLA / 99.99%   │    │ • Zero Trust     │
  │ • Orizzontale    │    │ • Response Time  │    │ • MTBF & MTTR    │    │ • Encryption     │
  └──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
```

1. **Scalabilità (Scalability & Throughput)**:
   * Capacità di gestire carichi crescenti (es. picco Black Friday da 5.000 TPS) aggiungendo risorse orizzontalmente senza degrado prestazionale.
2. **Performance e Latenza**:
   * Misurazione basata su percentili (non sulla media che nasconde i picchi anomali):
     * **p95 < 100 ms**: il 95% delle richieste risponde in meno di 100 ms.
     * **p99 < 300 ms**: il 99% delle richieste risponde in meno di 300 ms.
3. **Disponibilità (Availability & Resiliency)**:
   * **SLA (Service Level Agreement)**:
     * *99.9% (Three Nines)*: Massimo 8.76 ore di downtime all'anno.
     * *99.99% (Four Nines)*: Massimo 52.6 minuti di downtime all'anno (standard per circuiti carte).
     * *99.999% (Five Nines)*: Massimo 5.26 minuti di downtime all'anno (core banking mission-critical).
   * **MTBF (Mean Time Between Failures)** e **MTTR (Mean Time To Recovery)**.
4. **Sicurezza e Conformità**:
   * Cifratura in transito (TLS 1.3) e at-rest (AES-256), conformità PCI-DSS, tracciabilità immutabile di tutte le operazioni (*Auditability*).

---

## 4. Metodologie di Sviluppo: TDD & BDD

```
                                  IL CICLO DEL TDD
               ┌────────────────────────────────────────────────────┐
               │                                                    │
               ▼                                                    │
        ┌──────────────┐     Scrivi Codice Minimo     ┌───────────┐ │
        │     RED      │ ───────────────────────────► │   GREEN   │ │
        │ (Test Fallito│                              │ (Test OK) │ │
        └──────────────┘                              └─────┬─────┘ │
                                                            │       │
                                                 Refactoring│       │
                                                            ▼       │
                                                      ┌───────────┐ │
                                                      │  REFACTOR │ ┘
                                                      │ (Pulisci) │
                                                      └───────────┘
```

### 1. Test-Driven Development (TDD)
* **Filosofia**: Scrivere il test *prima* del codice di produzione (*Test-First Development*).
* **I 3 Passi**:
  1. **RED**: Scrivi un test unitario per il nuovo comportamento desiderato; il test fallisce (o non compila).
  2. **GREEN**: Scrivi la quantità minima di codice necessaria a far passare il test (anche con valori hardcoded).
  3. **REFACTOR**: Ristruttura il codice eliminando duplicazioni e migliorando il design, garantendo che tutti i test rimangano verdi.
* **Vantaggi**: Design modulare e disaccoppiato emergente, copertura del codice vicina al 100%, eliminazione della paura di rompere funzionalità esistenti (*Regression Safety*).

### 2. Behavior-Driven Development (BDD)
* **Filosofia**: Estensione del TDD orientata alla collaborazione tra **Business/Product Management, QA e Sviluppatori** tramite un linguaggio ubiquo e condiviso.
* **Struttura Given-When-Then (Gherkin Syntax)**:
  ```gherkin
  Feature: Autorizzazione Pagamento con Carta
    Scenario: Saldo disponibile sufficiente
      Given un conto con saldo disponibile di 100.00 EUR
      When richiedo un pagamento con carta di 35.00 EUR
      Then il pagamento viene approvato con stato "AUTHORIZED"
      And il saldo disponibile residuo diventa 65.00 EUR
  ```

---

## 5. Refactoring Continuo e Code Smells

Il **Refactoring** è il processo di modifica di un sistema software volto a migliorarne la struttura interna, la leggibilità e l'estensibilità **senza alterarne il comportamento osservabile esterno**.

### I Principali "Code Smells" (Martin Fowler) e Soluzioni:

1. **Long Method (Metodo Troppo Lungo)**:
   * *Problema*: Metodo con oltre 40-50 righe contenente logiche di validazione, calcolo e persistenza.
   * *Soluzione*: **Extract Method** per isolare funzioni coese con nomi auto-esplicativi.
2. **God Class / Large Class (Classe Onnipotente)**:
   * *Problema*: Classe con decine di campi e migliaia di righe che sa e fa troppo.
   * *Soluzione*: **Extract Class** applicando il *Single Responsibility Principle*.
3. **Primitive Obsession**:
   * *Problema*: Uso continuo di tipi primitivi (`String`, `Long`, `BigDecimal`) per rappresentare concetti di dominio (es. passare `String iban, String currency, BigDecimal amount`).
   * *Soluzione*: **Value Objects / Records** (es. `record Money(BigDecimal amount, Currency currency)`, `record IBAN(String value)`).
4. **Feature Envy (Invidia di Funzionalità)**:
   * *Problema*: Un metodo di una classe accede costantemente ai getter di un'altra classe per fare calcoli.
   * *Soluzione*: **Move Method** spostando il metodo all'interno della classe che possiede i dati.
5. **Shotgun Surgery**:
   * *Problema*: Ogni volta che si apporta una modifica di business, occorre modificare piccoli pezzi di codice in decine di classi diverse.
   * *Soluzione*: Centralizzare la logica coesa in una classe dedicata.

---

## 6. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come applichi concretamente il principio Open/Closed (OCP) in un'applicazione Spring Boot?*
  - **R**: Definisco un'interfaccia di servizio (astrazione) per il comportamento variabile (es. `NotificationSender` o `FraudCheckRule`). In Spring inietto una lista di bean `List<NotificationSender>` o una mappa, popolata automaticamente dal container IoC. Quando in futuro dobbiamo supportare un nuovo canale (es. notifica WhatsApp), creiamo semplicemente un nuovo bean `@Component` che implementa l'interfaccia: il codice chiamante non subisce alcuna modifica, rispettando pienamente l'OCP.

- *D: Perché il TDD migliora il design del software e non è solo una tecnica di test?*
  - **R**: Perché costringere lo sviluppatore a scrivere il test prima dell'implementazione lo obbliga a pensare alla classe dal punto di vista del suo utilizzatore (*API Design*). Una classe difficile da testare è quasi sempre una classe con cattivo design (troppo accoppiata, troppe responsabilità o dipendenze nascoste). Il TDD forza naturalmente a creare classi coese, a iniettare dipendenze tramite interfacce e a minimizzare la complessità ciclomatica.

- *D: Come definisci e garantisci un requisito di latenza p99 in un microservizio di pagamento?*
  - **R**: Il percentile 99 significa che il 99% delle richieste deve completarsi sotto una determinata soglia (es. 150 ms), ignorando l'1% dei casi estremi anomali. Per garantirlo:
    1. Strumento il codice con metriche **Micrometer / Prometheus** esportando histogram dei tempi di esecuzione sui metodi critici.
    2. Evito operazioni bloccanti o query N+1 al database ottimizzando indici e connection pool (HikariCP).
    3. Utilizzo cache in-memory (Redis) per dati calcolati di frequente e timeout aggressivi con Circuit Breaker sulle chiamate HTTP a servizi esterni.
    4. Eseguo test di carico prestazionali (*Load & Stress Testing* con Gatling/JMeter) durante la pipeline di release.



################################################################################
### CAPITOLO: 08. Spring & Spring Boot
################################################################################

# 8. Spring & Spring Boot

### Cos'è e perché conta
Spring e Spring Boot costituiscono lo standard de facto per lo sviluppo di applicazioni enterprise Java nel settore bancario e dei pagamenti elettronici. A livello Senior, non basta saper usare le annotazioni: occorre comprendere come funziona il container **IoC/DI**, come gestire la concorrenza e le **transazioni distribuite**, come ottimizzare l'accesso ai dati con **Spring Data JPA/Hibernate**, come blindare le API con **Spring Security** e come orchestrare flussi complessi con **Spring Integration**.

---

### Cosa studiare

#### 1. Core Spring, IoC Container & Dependency Injection

##### A. Il concetto chiave: Inversion of Control (IoC) e Bean
Un **bean** è un oggetto istanziato, configurato e gestito interamente dal container Spring (ApplicationContext) anziché manualmente tramite `new`.
- **Dichiarazione Bean**:
  1. *Annotazioni di stereotipo*: `@Component`, `@Service`, `@Repository`, `@Controller` / `@RestController`.
  2. *Configurazione esplicita*: `@Configuration` con metodi annotati `@Bean` (ideale per istanziare classi di librerie esterne o con logica di inizializzazione custom).
- **Scope dei Bean**:
  - `singleton` (default): un'unica istanza condivisa in tutta l'applicazione (thread-safety a carico dello sviluppatore: non memorizzare stato mutabile nei campi).
  - `prototype`: una nuova istanza creata ad ogni richiesta di injection.
  - Scope web: `request`, `session`, `application`.
- **Ciclo di vita del Bean**:
  - Istanziazione → Injection delle dipendenze → Callback `@PostConstruct` (`InitializingBean`) → Bean pronto all'uso → Callback `@PreDestroy` (`DisposableBean`) in fase di shutdown dell'applicazione.

##### B. Stereotipi: `@Component` vs `@Service` vs `@Repository`
- `@Component`: annotazione generica per qualsiasi componente gestito.
- `@Service`: marca la classe come layer di **business logic** (chiarezza architetturale).
- `@Repository`: marca il layer di **accesso ai dati**. Ha una funzionalità fondamentale in più: attiva la **traduzione automatica delle eccezioni** del database (JDBC/Hibernate) nella gerarchia unchecked coerente di Spring `DataAccessException`.

##### C. Constructor Injection vs Field Injection (`@Autowired`)
```java
// ❌ Field Injection (sconsigliata in produzione)
@Service
public class PaymentService {
    @Autowired
    private AccountRepository accountRepository;
}

// ✅ Constructor Injection (Best Practice)
@Service
public class PaymentService {
    private final AccountRepository accountRepository;

    public PaymentService(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }
}
```
**Motivazioni Senior a favore della Constructor Injection**:
1. **Immutabilità**: il campo può essere dichiarato `final`.
2. **Testabilità pura**: la classe può essere istanziata nei test unitari passando mock tramite costruttore senza avviare il contesto Spring (`new PaymentService(mockRepo)`).
3. **Fail-Fast all'avvio**: dipendenze mancanti bloccano l'avvio dell'applicazione prevenendo `NullPointerException` a runtime.
4. **Rilevazione dipendenze circolari**: evidenzia errori di design architetturale fin da subito.
*(Nota: da Spring 4.3+, se la classe ha un solo costruttore `@Autowired` è implicito).*

##### D. Risoluzione delle ambiguità: `@Qualifier` e `@Primary`
Quando sono presenti più bean che implementano la stessa interfaccia:
- `@Primary`: definisce l'implementazione predefinita in assenza di specificazioni.
- `@Qualifier("nomeBean")`: seleziona esplicitamente il bean desiderato nel punto di injection (vince su `@Primary`).
- `@Qualifier custom`: creazione di annotazioni tipizzate per evitare stringhe hardcoded (es. `@VisaGateway`, `@MastercardGateway`).

---

#### 2. Gestione delle Transazioni (`@Transactional`) & Isolation Levels

##### A. Funzionamento di `@Transactional`
Spring utilizza proxy dinamici (AOP) per intercettare le chiamate ai metodi `@Transactional`, aprendo la transazione prima dell'esecuzione e facendo commit/rollback al termine.
- *Attenzione al Self-Invocation Trap*: se un metodo chiama un altro metodo `@Transactional` della **stessa classe**, la chiamata non passa attraverso il proxy Spring e la transazione **non** viene applicata.

##### B. Livelli di Propagazione Transazionale
- **`REQUIRED` (default)**: partecipa alla transazione corrente se esiste, altrimenti ne crea una nuova. Se un metodo fallisce, l'intera transazione fa rollback.
- **`REQUIRES_NEW`**: sospende la transazione corrente e ne avvia una nuova, completamente indipendente. Il rollback della transazione esterna non influisce su quella interna (e viceversa).
  - *Caso d'uso pagamenti*: salvataggio dei **log di audit** o dei tentativi di frode: devono essere persistiti a DB anche se la transazione di pagamento principale fallisce e va in rollback.
- **`NESTED`**: crea un savepoint all'interno della transazione esistente. Un errore nel metodo nested permette il rollback fino al savepoint senza annullare l'intera transazione esterna.
- **`SUPPORTS` / `MANDATORY` / `NOT_SUPPORTED` / `NEVER`**.

##### C. Isolation Level del Database
- **`READ_COMMITTED`** (default in Oracle/PostgreSQL): previene *dirty read*, ma ammette *non-repeatable read*.
- **`REPEATABLE_READ`**: garantisce letture consistenti dello stesso record all'interno della transazione, ma ammette *phantom read*.
- **`SERIALIZABLE`**: massimo isolamento, previene ogni anomalia eseguendo le transazioni in serie logica; comporta elevata contesa di lock e impatto sul throughput.

##### D. Politiche di Rollback
Per default Spring esegue il rollback automatico **solo per eccezioni unchecked (`RuntimeException` ed `Error`)**, mentre fa commit in caso di checked exception.
- Per forzare il rollback su qualsiasi eccezione: `@Transactional(rollbackFor = Exception.class)`.

---

#### 3. Spring Data JPA & Hibernate

```
Spring Data JPA  ──►  JPA (Specifiche/Annotazioni)  ──►  Hibernate (ORM Engine)  ──►  JDBC Driver / Database
```

- **JPA (Jakarta Persistence)**: specifica standard per l'ORM (interfacce come `EntityManager`, annotazioni `@Entity`, `@Id`, `@OneToMany`, `@ManyToOne`, `@JoinColumn`).
- **Hibernate**: implementazione concreta di JPA che genera le query SQL, gestisce la sessione (persistence context), il dirty checking e la cache di primo/secondo livello.
- **Spring Data JPA**: layer ad alto livello che elimina il boilerplate generando automaticamente l'implementazione dei repository (`JpaRepository`).

##### A. Tipologie di Query
- **Derived Query Methods**: `findByStatusAndCreatedAtBetween(...)`.
- **JPQL con `@Query`**: per query complesse orientate agli oggetti (`@Query("SELECT t FROM Transaction t WHERE t.amount > :min")`).
- **Native SQL Query**: `@Query(value = "SELECT * FROM transactions WHERE ROWNUM <= 100", nativeQuery = true)` quando occorrono feature proprietarie di Oracle/PostgreSQL.

##### B. Il Problema N+1 (Lazy Loading) e Soluzioni
Si verifica quando si carica una lista di $N$ entità principali e, accedendo a una relazione `@ManyToOne` o `@OneToMany` lazy, Hibernate esegue 1 query per la lista $+ N$ query per ciascun figlio ($1 + N$ query totali).
- **Soluzioni**:
  1. `JOIN FETCH` esplicito in JPQL: `SELECT a FROM Account a JOIN FETCH a.transactions WHERE a.id = :id`.
  2. `@EntityGraph`: specifica dichiarativa delle relazioni da caricare eagerly per quel metodo.
  3. Batch Fetching (`@BatchSize` in Hibernate): raggruppa le $N$ query in batch con clausola `IN (...)`.

##### C. Concorrenza e Locking nei Dati Finanziari
- **Locking Ottimistico (`@Version`)**: aggiunge una colonna numerica di versione. Al momento dell'UPDATE, verifica che la versione non sia cambiata (`UPDATE ... WHERE version = :expected`). In caso di collisione lancia `OptimisticLockException`. Ideale per scenari con bassa contesa.
- **Locking Pessimistico (`@Lock(LockModeType.PESSIMISTIC_WRITE)`)**: esegue una query `SELECT ... FOR UPDATE`, bloccando fisicamente la riga a livello di DB finché la transazione non termina. Necessario per aggiornamenti concorrenti di saldi e conti correnti.

---

#### 4. Gestione Centralizzata delle Eccezioni in Spring Boot

- **`@RestControllerAdvice` e `@ExceptionHandler`**:
  Intercettano le eccezioni lanciate da qualsiasi `@Controller` / `@Service`, restituendo una risposta HTTP standardizzata (es. conforme a RFC 7807 Problem Details).

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(InsufficientFundsException.class)
    public ResponseEntity<ErrorResponse> handleInsufficientFunds(InsufficientFundsException ex, HttpServletRequest request) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.UNPROCESSABLE_ENTITY.value(),
            "INSUFFICIENT_FUNDS",
            ex.getMessage(),
            request.getRequestURI(),
            Instant.now()
        );
        return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY).body(error);
    }

    @ExceptionHandler(PaymentGatewayTimeoutException.class)
    public ResponseEntity<ErrorResponse> handleTimeout(PaymentGatewayTimeoutException ex, HttpServletRequest request) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.GATEWAY_TIMEOUT.value(),
            "GATEWAY_TIMEOUT",
            "Il circuito di pagamento non ha risposto in tempo",
            request.getRequestURI(),
            Instant.now()
        );
        return ResponseEntity.status(HttpStatus.GATEWAY_TIMEOUT).body(error);
    }
}
```
- **Best Practice Senior**:
  - Creare eccezioni di business checked/unchecked specifiche (`DuplicateTransactionException`, `CardExpiredException`).
  - Distinguere rigorosamente tra errori 4xx (errore del client/validazione) e 5xx (errore di sistema/infrastruttura).
  - Non restituire mai stack trace o dettagli interni di DB al client (rischio di sicurezza).

---

#### 5. Spring Security (Modern Boot 3+)

- **`SecurityFilterChain`**: catena di filtri Servlet che intercetta e protegge le richieste prima che raggiungano i controller.
- **OAuth2 Resource Server & JWT**:
  Nei microservizi di pagamento, l'autenticazione avviene tramite Bearer JWT emesso da un Identity Provider (Keycloak / Okta). Il microservizio agisce da Resource Server validando la firma del token in modo stateless.

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity // Abilita @PreAuthorize
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable()) // Stateless REST API con token
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health", "/api/v1/public/**").permitAll()
                .requestMatchers("/api/v1/payments/admin/**").hasRole("PAYMENT_ADMIN")
                .requestMatchers("/api/v1/payments/**").hasAuthority("SCOPE_payment.write")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .build();
    }
}
```

- **Method-Level Security**:
  Controllo granulare dell'autorizzazione sui metodi di business:
  ```java
  @PreAuthorize("hasRole('ADMIN') or #accountId == authentication.principal.claims['account_id']")
  public AccountDetails getAccountDetails(String accountId) { ... }
  ```

---

#### 6. Spring Integration & Enterprise Integration Patterns (EIP)

- **Cosa sono gli EIP**: Gli *Enterprise Integration Patterns* (formalizzati da *Gregor Hohpe & Bobby Woolf*) sono un catalogo di pattern architetturali standard per risolvere il problema dell'integrazione tra sistemi enterprise eterogenei, distribuiti e legacy, basandosi sul paradigma della **messaggistica asincrona e disaccoppiata**.
- **I 4 Pilastri Fondamentali di EIP**:
  1. **Message**: l'unità di informazione composta da **Payload** (dati di business) e **Headers** (metadati come ID, correlation ID, timestamp, security token).
  2. **Message Channel**: la condotta logica che collega i componenti, disaccoppiando mittente e destinatario sia a livello spaziale che temporale (es. *Point-to-Point* o *Publish-Subscribe*).
  3. **Pipes and Filters**: l'architettura a pipeline in cui piccoli componenti indipendenti (*Filters*) elaborano o trasformano il messaggio e lo rilasciano sul canale (*Pipe*) successivo.
  4. **Message Endpoint**: l'adattatore che connette il codice dell'applicazione al sistema di messaggistica (*Channel Adapter* e *Messaging Gateway*).

##### Catalogo dei principali Pattern EIP (con esempi nel dominio Pagamenti)

* **Routing Patterns (Instradamento)**:
  * **Content-Based Router**: instrada il messaggio verso canali differenti esaminandone il payload o gli header (es. instrada verso circuito *CARD* vs bonifico *SEPA* in base al tipo pagamento).
  * **Message Filter**: valuta un predicato booleano ed elimina i messaggi non validi (es. scarta transazioni con importo negativo o nulle).
  * **Recipient List**: calcola dinamicamente a runtime una lista di destinatari a cui inviare una copia del messaggio.
  * **Wire Tap**: duplica il flusso di messaggi inviando una copia a un canale secondario (es. audit trail, monitoraggio frodi o metriche) senza bloccare o alterare il flusso principale.
  * **Scatter-Gather**: invia in broadcast una richiesta a più provider esterni e aggrega le risposte per selezionare la migliore (es. richiesta miglior tasso di cambio a più banche).

* **Transformation Patterns (Trasformazione & Arricchimento)**:
  * **Message Translator / Transformer**: converte i dati da un formato a un altro (es. da tracciato legacy ISO 8583 / CBI a JSON REST interno).
  * **Content Enricher**: interroga una sorgente dati esterna (DB, cache Redis, servizio anagrafica) per completare il messaggio con dati mancanti (es. aggiunge i tassi FX correnti).
  * **Content Filter**: rimuove campi superflui o sensibili prima dell'inoltro (es. mascheramento del PAN della carta di credito per conformità PCI-DSS).
  * **Claim Check**: quando il payload è pesante (es. file report di quadratura), salva il payload in uno storage (es. S3/Blob) e passa nel messaggio solo l'identificativo/token di riferimento (*claim ticket*).

* **Composition & Re-sequencing (Composizione e Flusso)**:
  * **Splitter**: suddivide un messaggio composito in messaggi atomici (es. estrae 10.000 singole disposizioni da un unico file batch SEPA XML).
  * **Aggregator**: raggruppa più messaggi correlati (`correlationId`) e li combina in un unico messaggio aggregato al raggiungimento di una condizione (es. timeout o ricezione di tutte le transazioni di un lotto).
  * **Resequencer**: riordina i messaggi arrivati disallineati in base a un sequence number o timestamp prima di inoltrarli al consumatore.

* **Resilience & Reliability (Resilienza)**:
  * **Dead Letter Channel (DLC / DLQ)**: canale dedicato dove vengono dirottati i messaggi che non è possibile elaborare dopo $N$ tentativi di retry.
  * **Idempotent Receiver**: verifica la chiave di unicità (`idempotencyKey`) per evitare l'elaborazione duplicata della stessa transazione.

##### Esempio pratico in Spring Integration (Java DSL)

```java
@Bean
public IntegrationFlow paymentProcessingFlow() {
    return IntegrationFlow.from("paymentInboundChannel")
        .filter((PaymentMessage p) -> p.getAmount().compareTo(BigDecimal.ZERO) > 0)
        .transform(this::enrichWithExchangeRates)
        .route(PaymentMessage::getPaymentType, mapping -> mapping
            .subFlowMapping("CARD", sf -> sf.handle(Http.outboundGateway("https://card-acquirer/api/auth")))
            .subFlowMapping("SEPA", sf -> sf.handle(Jms.outboundAdapter(jmsTemplate).destination("sepaQueue")))
        )
        .get();
}
```

##### Confronto: Spring Integration vs Apache Camel

Entrambi i framework nascono per implementare gli **Enterprise Integration Patterns (EIP)** (*Hohpe & Woolf*) e condividono il modello a messaggi (*Payload + Headers*), ma differiscono per filosofia ed ecosistema:

| Aspetto | Spring Integration | Apache Camel |
| :--- | :--- | :--- |
| **Ecosistema & Dipendenze** | Strettamente integrato nell'ecosistema **Spring** (Spring Boot, Spring Cloud, Spring Messaging). | **Agnostico**: gira standalone, con Spring Boot, Quarkus, Micronaut, Karaf/OSGi, ecc. |
| **Paradigma di Flusso** | **Pipe-and-Filter / Channel-centric** (connessione tra `MessageChannel` ed endpoint). | **Route-centric** (definizione fluida basata su URI `from("...").to("...")`). |
| **Connettori / Componenti** | Ottima copertura per standard enterprise (JMS, AMQP, Kafka, File, HTTP, JDBC, MQTT). | **Catalogo enorme (300+)** con connettori pronti per servizi SaaS e Cloud specifici. |
| **Evoluzione Cloud** | Motore sottostante di **Spring Cloud Stream**. | Evoluto in **Camel K** (ottimizzato per Serverless e Kubernetes). |

* **Quando scegliere Spring Integration**: se lo stack è 100% Spring Boot e si desidera un'integrazione nativa con il ciclo di vita dei bean Spring e con Spring Cloud Stream.
* **Quando scegliere Apache Camel**: se servono connettori out-of-the-box verso centinaia di servizi eterogenei/SaaS terzi o se l'architettura include framework diversi (es. Quarkus) o ambienti Kubernetes-native (Camel K).

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Qual è la differenza principale tra Spring Integration e Apache Camel?*
  - **R**: Entrambi implementano i pattern EIP (Enterprise Integration Patterns) e il modello a messaggi (payload + headers). Spring Integration è strettamente integrato nell'ecosistema Spring (rappresenta anche il motore sotto Spring Cloud Stream) e usa un approccio *channel-centric*. Apache Camel è agnostico rispetto al framework (utilizzabile con Quarkus, standalone, ecc.), adotta un approccio *route-centric* basato su URI e possiede un ecosistema di connettori/componenti out-of-the-box molto più vasto (oltre 300 connettori verso sistemi terzi e SaaS).

- *D: Perché preferisci la Constructor Injection rispetto all'annotazione `@Autowired` sui campi?*
  - **R**: La Constructor Injection garantisce l'immutabilità dei campi (`final`), facilita i test unitari permettendo di passare mock senza avviare il container Spring o usare reflection, e garantisce il principio di fail-fast impedendo che l'applicazione si avvii con dipendenze mancanti.

- *D: Cosa succede se un metodo `@Transactional` chiama internamente un altro metodo `@Transactional(propagation = Propagation.REQUIRES_NEW)` della stessa classe?*
  - **R**: A causa del meccanismo dei proxy dinamici di Spring AOP, la chiamata interna non attraversa il proxy. Di conseguenza, la configurazione `REQUIRES_NEW` viene ignorata e il metodo viene eseguito all'interno della transazione originaria. Per risolvere questo problema, occorre spostare il metodo in un bean separato o iniettare il bean stesso.

- *D: Come risolvi il problema N+1 con Spring Data JPA?*
  - **R**: Utilizzando una query JPQL esplicita con clausola `JOIN FETCH` sulla relazione desiderata, oppure applicando l'annotazione `@EntityGraph` sul metodo del repository per specificare quali attributi caricare eagermente solo per quella specifica query.

- *D: Perché è buona pratica disabilitare il CSRF su API RESTful protette da JWT?*
  - **R**: Gli attacchi CSRF sfruttano l'invio implicito e automatico dei cookie di sessione da parte del browser in richieste cross-site. In un'API REST stateless protetta da Bearer Token (JWT) inserito esplicitamente nell'header HTTP `Authorization`, il browser non invia automaticamente il token, rendendo la protezione CSRF standard superflua.

---

### Come esercitarti
1. **Configurazione Spring Security**: scrivi a mano una configurazione `SecurityFilterChain` con validazione JWT stateless, esclusione degli endpoint di health check Actuator e autorizzazioni differenziate per ruoli operatore e admin.
2. **Global Exception Handler**: implementa un `@RestControllerAdvice` con gestione di 3 eccezioni di business custom, restituendo un oggetto di errore strutturato con codice errore univoco, messaggio human-readable e timestamp.



################################################################################
### CAPITOLO: 09. API REST e RESTful Design
################################################################################

# 9. API REST, Tecnologie Web, Sicurezza e Framework

## Cos'è e perché conta

Le API e le tecnologie web costituiscono l'interfaccia fondamentale tra i microservizi backend, le applicazioni frontend (web e mobile), i gateway di pagamento e i partner esterni. Uno sviluppatore Senior deve dominare sia l'**evoluzione del protocollo HTTP** (HTTP/1.1, HTTP/2, HTTP/3), sia le problematiche di sicurezza web (**Cookies, JWT, CORS, CSRF**), le strategie avanzate di **HTTP Caching** (ETag, Cache-Control, CDN) e saper orientarsi con disinvoltura tra i principali framework REST Java (**Spring MVC, JAX-RS/Jersey, Dropwizard**).

---

## 1. Evoluzione dei Protocolli Web: HTTP/1.1 vs HTTP/2 vs HTTP/3

```
                                EVOLUZIONE DEL PROTOCOLLO HTTP
       HTTP/1.1 (1997)                     HTTP/2 (2015)                     HTTP/3 (2020+)
 ┌───────────────────────────┐       ┌───────────────────────────┐       ┌───────────────────────────┐
 │ • Testuale                │       │ • Binario (Binary Framing)│       │ • Basato su QUIC (su UDP) │
 │ • 1 Richiesta per TCP     │       │ • Multiplexing su 1 TCP   │       │ • Zero Head-of-Line Block │
 │ • Head-of-Line Blocking   │       │ • Compressione HPACK      │       │ • Handshake 0-RTT / 1-RTT │
 └─────────────┬─────────────┘       └─────────────┬─────────────┘       └─────────────┬─────────────┘
               ▼                                   ▼                                   ▼
        Trasporto: TCP                      Trasporto: TCP                      Trasporto: UDP
```

### 1. HTTP/1.1
* Protocollo testuale basato su TCP. Supporta connessioni persistenti (`Keep-Alive`), ma soffre di **Head-of-Line (HoL) Blocking a livello applicativo**: su una singola connessione TCP, una richiesta lenta blocca tutte le richieste successive.

### 2. HTTP/2
* **Binary Framing Layer**: I messaggi sono suddivisi in frame binari (HEADERS, DATA) raggruppati in stream indipendenti.
* **Multiplexing Completo**: Centinaia di richieste e risposte viaggiano contemporaneamente su un'**unica connessione TCP** senza bloccarsi a vicenda.
* **Compressione HPACK**: Gli header HTTP ripetitivi vengono compressi eliminando ridondanze.

### 3. HTTP/3 & Protocollo QUIC
* Sostituisce il protocollo TCP con **QUIC (basato su UDP)**.
* **Elimina l'HoL Blocking a livello di trasporto**: Se un pacchetto va perso, solo il singolo stream interessato subisce il ritardo di ritrasmissione, mentre tutti gli altri stream continuano senza interruzioni.
* **Connection Migration**: Se un dispositivo mobile passa da rete Wi-Fi a 4G/5G, la connessione non si interrompe perché è identificata da un *Connection ID* a 64 bit e non dalla quadrupla IP/Porta TCP.

---

## 2. Gestione dello Stato, Sessioni, Cookies e JWT

```
                  SESSIONI STATEFUL vs TOKEN STATELESS (JWT)
        SESSION-BASED (Stateful)                      JWT TOKEN-BASED (Stateless)
   ┌─────────────────────────────────┐           ┌─────────────────────────────────┐
   │ • Server memorizza la sessione  │           │ • Server non memorizza stato    │
   │   in RAM o Redis (JSESSIONID)   │           │ • Il token contiene i claims    │
   │ • Revoca immediata facilissima  │           │ • Scalabilità orizzontale nativa│
   │ • Richiede memoria centralizzata│           │ • Revoca immediata complessa    │
   └─────────────────────────────────┘           └─────────────────────────────────┘
```

### 1. Sicurezza dei Cookie
I cookie HTTP inviati tramite l'header `Set-Cookie` devono essere blindati con 3 flag essenziali:
* **`HttpOnly`**: Impedisce l'accesso al cookie tramite script JavaScript (`document.cookie`), proteggendo il token da attacchi **XSS (Cross-Site Scripting)**.
* **`Secure`**: Il browser invia il cookie solo su connessioni cifrate **HTTPS** (TLS).
* **`SameSite`** (Protezione anti-CSRF):
  * `SameSite=Strict`: Il cookie non viene mai inviato in richieste cross-site (neppure cliccando su un link esterno).
  * `SameSite=Lax` (*Default moderno*): Il cookie viene inviato solo su navigazioni top-level sicure (GET da link esterni), ma bloccato su `POST` cross-site.
  * `SameSite=None`: Il cookie viene sempre inviato (richiede obbligatoriamente `Secure=true`).

---

### 2. Architettura JWT (JSON Web Token) & Token Rotation
Un JWT è composto da 3 parti separate da punti (`header.payload.signature`):
$$\text{Signature} = \text{HMAC-SHA256}(\text{Base64Url}(Header) + "." + \text{Base64Url}(Payload), \text{SecretKey})$$

* **Pattern di Autenticazione Robusto (Access Token + Refresh Token)**:
  1. **Access Token (JWT)**: Durata brevissima (5-15 minuti), memorizzato in memoria JavaScript o cookie `HttpOnly`, utilizzato nell'header `Authorization: Bearer <token>`.
  2. **Refresh Token**: Durata lunga (7-30 giorni), salvato in un cookie sicuro `HttpOnly` e su database/Redis.
  3. **Refresh Token Rotation**: Ogni volta che viene richiesto un nuovo Access Token, il server invalida il vecchio Refresh Token ed emette una nuova coppia; se un vecchio Refresh Token viene riutilizzato, scatta un allarme di furto credenziali e tutte le sessioni dell'utente vengono revocate.

---

### 3. Problematiche Web: CORS & CSRF

#### CORS (Cross-Origin Resource Sharing)
* Meccanismo di sicurezza del browser che impedisce a un'applicazione web caricata su un dominio (es. `https://app.frontend.com`) di fare chiamate API verso un'origine diversa (`https://api.bank.com`).
* **Richiesta Pre-Flight (`OPTIONS`)**: Per richieste non semplici (es. con header custom `Authorization` o `Content-Type: application/json`), il browser invia prima una `OPTIONS` con gli header:
  * `Origin: https://app.frontend.com`
  * `Access-Control-Request-Method: POST`
  * `Access-Control-Request-Headers: Authorization, Content-Type`
* Il backend risponde con:
  * `Access-Control-Allow-Origin: https://app.frontend.com` (mai `*` se si usano credenziali)
  * `Access-Control-Allow-Credentials: true`

#### CSRF (Cross-Site Request Forgery)
* Attacco in cui un sito malevolo induce il browser dell'utente a eseguire un'azione indesiderata su un'applicazione autenticata sfruttando l'invio automatico dei cookie di sessione.
* **Difesa**: Su API REST stateless protette da token JWT nell'header `Authorization`, il CSRF non sussiste (il browser non allega l'header automaticamente). Se si usano cookie di sessione, si impiega il flag `SameSite=Lax/Strict` e il pattern del **CSRF Synchronizer Token**.

---

## 3. HTTP Caching Avanzato & Strategie CDN

```
                              VALIDAZIONE DELLA CACHE HTTP
             Client / Browser                             Server Backend
                    │   GET /api/v1/tariffs                      │
                    │ ─────────────────────────────────────────► │
                    │   200 OK                                   │
                    │   ETag: "w/33a64df5514aa1"                 │
                    │   Cache-Control: public, max-age=3600      │
                    │ ◄───────────────────────────────────────── │
                    │                                            │
                    │   (Dopo 1 ora: Richiesta Condizionale)     │
                    │   GET /api/v1/tariffs                      │
                    │   If-None-Match: "w/33a64df5514aa1"        │
                    │ ─────────────────────────────────────────► │
                    │   304 Not Modified (Body Vuoto)            │
                    │ ◄───────────────────────────────────────── │
```

### Direttive `Cache-Control`:
* `public`: La risposta può essere memorizzata in cache da browser e intermediari (CDN, proxy).
* `private`: La risposta è destinata a un singolo utente e non deve essere salvata su cache condivise/CDN.
* `no-cache`: La risorsa può essere salvata in cache, ma **deve essere rivalidata con il server** (`ETag`) prima di ogni riutilizzo.
* `no-store`: La risposta contiene dati sensibili e **non deve mai essere memorizzata su disco o memoria di cache**.
* `max-age=N`: Durata di validità in secondi per il browser.
* `s-maxage=N`: Durata specifica per le cache condivise (CDN / Reverse Proxy).

### Validazione Condizionale con ETag:
* L'**ETag** è un identificatore univoco o hash del contenuto della risorsa.
* Il client memorizza l'ETag e, alla scadenza, invia una richiesta condizionale con l'header `If-None-Match: "<etag>"`.
* Se la risorsa non è cambiata, il server restituisce **`304 Not Modified` senza inviare il payload**, risparmiando banda e CPU.

---

## 4. Framework REST in Java: Spring MVC vs JAX-RS vs Dropwizard

```
┌──────────────────┬──────────────────────────┬─────────────────────────────┬───────────────────────────┐
│ Caratteristica   │ Spring Boot (Spring MVC) │ JAX-RS (Jersey / RESTEasy)  │ Dropwizard                │
├──────────────────┼──────────────────────────┼─────────────────────────────┼───────────────────────────┤
│ **Natura**       │ Framework completo enterprise│ Standard Jakarta EE / Spec  │ Lightweight REST Framework│
│ **Iniezione**    │ Spring Core IoC / DI     │ CDI / HK2                   │ Google Guice / Manuale    │
│ **Web Server**   │ Tomcat / Jetty / Undertow│ Qualsiasi servlet container │ Jetty embedded integrato  │
│ **JSON Engine**  │ Jackson (default)        │ Jackson / JSON-B            │ Jackson integrato         │
│ **Annotazioni**  │ `@RestController`        │ `@Path`, `@GET`, `@POST`    │ `@Path` (usa Jersey)      │
│                  │ `@GetMapping`, `@PostMapping`│ `@Produces`, `@Consumes`│                           │
│ **Filosofia**    │ Ecosistema onnicomprensivo│ Standard portabile         │ Minimalista e "out-of-box"│
└──────────────────┴──────────────────────────┴─────────────────────────────┴───────────────────────────┘
```

### 1. Spring MVC / Spring Web
Lo standard de facto dell'ecosistema enterprise Java:
```java
@RestController
@RequestMapping("/api/v1/payments")
public class PaymentRestController {

    private final PaymentService paymentService;

    public PaymentRestController(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    @PostMapping
    public ResponseEntity<PaymentResponse> create(@Valid @RequestBody PaymentRequest request) {
        PaymentResponse response = paymentService.execute(request);
        URI location = URI.create("/api/v1/payments/" + response.id());
        return ResponseEntity.created(location).body(response);
    }
}
```

### 2. JAX-RS (Jakarta RESTful Web Services / Jersey)
La specifica standard Java (molto usata in **Quarkus, WildFly, Micronaut**):
```java
@Path("/api/v1/payments")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class PaymentResource {

    @Inject
    private PaymentService paymentService;

    @POST
    public Response create(@Valid PaymentRequest request) {
        PaymentResponse response = paymentService.execute(request);
        URI location = URI.create("/api/v1/payments/" + response.getId());
        return Response.created(location).entity(response).build();
    }
}
```

### 3. Dropwizard
* Creato originariamente da Yammer; raggruppa librerie mature e collaudate (**Jetty per HTTP, Jersey per REST, Jackson per JSON, Metrics per monitoraggio**) in un pacchetto leggero e veloce, senza la complessità o il runtime pesante di Spring.

---

## 5. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come gestisci il caching a livello di CDN per evitare che gli utenti ricevano dati obsoleti dopo una modifica?*
  - **R**: Utilizzo due strategie complementari:
    1. **Cache-Control & ETag**: Imposto direttive `s-maxage` appropriate per la CDN e restituisco header `ETag` (hash del contenuto).
    2. **Cache Invalidation / Surrogate-Keys**: Per risorse a bassa frequenza di modifica, imposto cache lunga sulla CDN ma configuro un webhook di backend che esegue un *Purge/Invalidation* esplicito della cache sulla CDN (tramite API CloudFront/Akamai o invalidazione per tag) nel momento esatto in cui un'operazione di `UPDATE/DELETE` modifica il dato.

- *D: Perché non è sicuro memorizzare un token JWT sensibile nel `localStorage` del browser?*
  - **R**: Perché qualsiasi script JavaScript in esecuzione sulla pagina ha accesso completo a `localStorage`. Se l'applicazione subisce una vulnerabilità di tipo **XSS (Cross-Site Scripting)** tramite una libreria npm compromessa o un input non sanificato, l'attaccante può rubare il JWT ed impersonare l'utente. La memorizzazione sicura prevede un **cookie con flag `HttpOnly`, `Secure` e `SameSite=Strict/Lax`**, totalmente inaccessibile a JavaScript.

- *D: Che differenza c'è tra le annotazioni `@RestController` di Spring e `@Path` di JAX-RS?*
  - **R**: `@RestController` è un'annotazione proprietaria di Spring che combina `@Controller` e `@ResponseBody`, indicando che i valori di ritorno dei metodi vengono serializzati direttamente nel body HTTP tramite HttpMessageConverter. `@Path` fa parte dello standard formale JAX-RS (Jakarta REST) e viene utilizzata da framework compatibili (Jersey, RESTEasy, Quarkus) per definire l'URI base della risorsa, garantendo portabilità tra diversi application server conformi alle specifiche Jakarta EE.



################################################################################
### CAPITOLO: 10. Microservizi: Concetti Fondamentali
################################################################################

# 10. Microservizi: Concetti Fondamentali

### Cos'è e perché conta
Anche se non esplicitamente nella job description, un'architettura di pagamenti mission-critical con integrazioni multiple (circuiti, banche, provider terzi) è quasi certamente organizzata a microservizi o comunque a servizi distribuiti. Vale la pena arrivare preparato anche su questo fronte.

### Cosa studiare

**Principi di base**

I microservizi sono un'architettura dove l'applicazione è scomposta in servizi indipendenti, ciascuno responsabile di una specifica funzionalità di business. Ogni servizio ha il proprio database (**database per service pattern**), può essere deployato indipendentemente e comunica con gli altri attraverso API ben definite.

*Esempio nel dominio pagamenti*: un servizio `authorization-service` (gestisce le autorizzazioni), uno `settlement-service` (gestisce clearing/settlement), uno `reconciliation-service` (riconciliazione) — ognuno con il proprio DB, deployabile e scalabile in autonomia.

**Vantaggi e trade-off**

Devi essere pronto a discutere quando conviene usarli:
- **Vantaggi**: scalabilità indipendente (es. scalare solo il servizio di autorizzazione nei picchi di traffico, senza toccare il resto), isolamento dei guasti (un servizio che cade non abbatte tutto il sistema), libertà tecnologica per ogni servizio, team autonomi che possono rilasciare senza coordinarsi con tutti gli altri
- **Svantaggi**: complessità nella gestione distribuita, necessità di orchestrazione, monitoraggio avanzato (vedi osservabilità più sotto), gestione delle transazioni distribuite (niente più semplice `@Transactional` locale quando l'operazione coinvolge più servizi)

**Comunicazione tra servizi**

- **Sincrona** (REST, gRPC): il chiamante aspetta la risposta. Più semplice da ragionare, ma accoppia temporalmente i servizi — se il servizio chiamato è lento o giù, blocca anche il chiamante
- **Asincrona** (message broker come RabbitMQ, Kafka, AWS SQS): il chiamante pubblica un messaggio/evento e prosegue, senza aspettare. Preferibile per disaccoppiare i servizi e gestire meglio i picchi di carico

*Esempio pagamenti*: l'autorizzazione di una transazione richiede tipicamente comunicazione **sincrona** (il cliente al POS aspetta una risposta in millisecondi), mentre l'invio di notifiche, l'aggiornamento di sistemi di reportistica o l'innesco della riconciliazione post-transazione sono tipicamente **asincroni** via evento (es. `TransactionCompletedEvent` pubblicato su Kafka).

**Pattern essenziali**

- **API Gateway**: punto d'ingresso unico per i client, che instrada le richieste ai servizi interni, gestendo trasversalmente autenticazione, rate limiting, routing
- **Service Discovery** (Consul, Eureka): permette ai servizi di trovarsi dinamicamente a runtime, senza indirizzi IP hardcoded — essenziale quando i servizi scalano e le istanze cambiano continuamente
- **Circuit Breaker** (pattern reso popolare da Hystrix, oggi più spesso Resilience4j): se un servizio a valle inizia a fallire ripetutamente, il circuit breaker "apre il circuito" e smette temporaneamente di chiamarlo, restituendo subito un errore/fallback invece di continuare a intasarlo con richieste che falliranno comunque — fondamentale per evitare che un servizio in difficoltà (es. un circuito di pagamento esterno lento) faccia collassare a cascata anche i servizi che lo chiamano
- **Saga pattern**: per gestire transazioni distribuite su più servizi senza un "commit" globale come nel mondo relazionale — una saga è una sequenza di transazioni locali, ciascuna con una **compensazione** (azione di rollback logico) se un passo successivo fallisce. Due varianti: *orchestrazione* (un coordinatore centrale dirige i passi) o *coreografia* (ogni servizio reagisce a eventi e decide autonomamente il passo successivo)
  - *Esempio pagamenti*: un pagamento che coinvolge debit dell'account, notifica al merchant e aggiornamento del ledger — se l'ultimo passo fallisce, la saga esegue le compensazioni (es. re-credit dell'account) invece di un rollback atomico impossibile su più DB separati
- **Event Sourcing e CQRS**: Event Sourcing salva lo stato di un'entità come sequenza di eventi immutabili (invece che come stato corrente sovrascritto) — utilissimo in ambito finanziario per audit trail completo, dato che ogni cambiamento di stato è tracciato. CQRS (Command Query Responsibility Segregation) separa il modello usato per le scritture da quello usato per le letture, spesso ottimizzati diversamente — combinato con Event Sourcing è un pattern molto comune in sistemi di pagamento/contabilità dove la tracciabilità storica è un requisito normativo

### Come esercitarti
Prepara un esempio in cui spieghi perché il **Circuit Breaker** è particolarmente rilevante in un sistema che chiama circuiti di pagamento esterni: se Visa/Mastercard rispondono lentamente, senza circuit breaker rischi di saturare i thread/connessioni del tuo servizio in attesa, propagando il problema a cascata.



################################################################################
### CAPITOLO: 11. WebSocket
################################################################################

# 11. WebSocket e Comunicazione Real-Time

### Cos'è
Protocollo di comunicazione che stabilisce una connessione **full-duplex persistente** tra client e server su un singolo socket TCP — a differenza di HTTP tradizionale (richiesta/risposta, connessione chiusa dopo ogni scambio), con WebSocket sia client che server possono inviare messaggi in qualsiasi momento sulla stessa connessione aperta.

### Caratteristiche principali

- **Handshake iniziale via HTTP**: la connessione parte come una normale richiesta HTTP con header `Upgrade: websocket`, poi "sale di livello" a una connessione WebSocket persistente
- **Full-duplex**: comunicazione bidirezionale simultanea, non serve che il client "chieda" per ricevere un aggiornamento dal server (a differenza del polling HTTP tradizionale)
- **Basso overhead**: dopo l'handshake iniziale, i messaggi successivi hanno un overhead molto ridotto rispetto a ripetute richieste HTTP, rendendolo adatto ad aggiornamenti frequenti e a bassa latenza
- **STOMP su WebSocket**: in Spring, si usa spesso il protocollo STOMP sopra WebSocket per avere un modello a messaggi/topic più strutturato (simile a un message broker), invece di gestire i frame WebSocket grezzi

### Esempio di utilizzo (Spring Boot)

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws-notifications").withSockJS();
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic");
        registry.setApplicationDestinationPrefixes("/app");
    }
}

// Invio di un aggiornamento in tempo reale
@Autowired
private SimpMessagingTemplate messagingTemplate;

public void notifyTransactionStatus(String accountId, TransactionStatus status) {
    messagingTemplate.convertAndSend("/topic/account/" + accountId, status);
}
```

### Rilevanza per il dominio pagamenti
Utile per **notifiche in tempo reale** verso un frontend/dashboard — ad esempio aggiornare istantaneamente lo stato di una transazione mentre viene processata (in attesa → autorizzata → completata), senza che il client debba fare polling continuo. Rilevante anche per dashboard operative interne che monitorano transazioni live o alert su anomalie.

### Domande tipiche e risposte

- *D: Perché non usare semplicemente il polling HTTP per aggiornamenti in tempo reale?*
  R: Il polling genera traffico costante anche quando non ci sono aggiornamenti reali, introduce latenza (l'aggiornamento arriva solo al prossimo poll) e non scala bene con molti client. WebSocket mantiene una connessione aperta e il server può inviare aggiornamenti nell'istante in cui accadono, con overhead molto minore.

- *D: WebSocket è adatto per comunicazione tra microservizi?*
  R: Non è la scelta tipica — tra servizi backend si preferisce REST/gRPC (sincrono) o un message broker come Kafka/RabbitMQ (asincrono), entrambi più adatti a comunicazione server-to-server con garanzie di delivery/retry. WebSocket è pensato principalmente per comunicazione client-server in tempo reale (es. verso un frontend o un'app mobile).



################################################################################
### CAPITOLO: 12. Apache Kafka
################################################################################

# 12. Apache Kafka

### Cos'è
Piattaforma di **event streaming distribuita**, pensata per gestire flussi di eventi ad altissimo volume con durabilità e riproducibilità. Non è un semplice message broker "spedisci e dimentica" come RabbitMQ — Kafka **conserva** i messaggi per un periodo configurabile (anche a tempo indeterminato), permettendo a più consumer di rileggerli in momenti diversi.

### Caratteristiche principali

- **Topic**: canale logico dove vengono pubblicati gli eventi (es. `transaction-events`)
- **Partition**: ogni topic è diviso in partizioni, distribuite su più broker — permettono parallelismo: più consumer possono leggere partizioni diverse dello stesso topic contemporaneamente
- **Producer/Consumer**: chi pubblica e chi legge i messaggi. Un **consumer group** permette a più istanze dello stesso servizio di dividersi il carico di lettura: ogni partizione viene assegnata a un solo consumer del gruppo
- **Offset**: ogni messaggio in una partizione ha una posizione progressiva (offset); il consumer tiene traccia di quale offset ha già processato, permettendo di riprendere esattamente da dove si era interrotto in caso di riavvio
- **Retention**: i messaggi restano nel topic per un periodo configurabile (giorni, o "per sempre" con compaction), indipendentemente dal fatto che siano già stati letti — a differenza di una coda tradizionale dove un messaggio letto viene rimosso
- **Ordinamento**: garantito **solo all'interno di una singola partizione**, non tra partizioni diverse — un dettaglio spesso chiesto a colloquio

### Esempio di utilizzo (Spring Boot)

```java
// Producer
@Service
public class TransactionEventPublisher {
    private final KafkaTemplate<String, TransactionEvent> kafkaTemplate;

    public void publish(TransactionEvent event) {
        // la chiave (account id) determina la partizione: garantisce
        // che tutti gli eventi dello stesso account mantengano l'ordine
        kafkaTemplate.send("transaction-events", event.getAccountId(), event);
    }
}

// Consumer
@KafkaListener(topics = "transaction-events", groupId = "reconciliation-service")
public void onTransactionEvent(TransactionEvent event) {
    reconciliationService.process(event);
}
```

### Rilevanza per il dominio pagamenti
Kafka è la scelta tipica per propagare eventi come `TransactionAuthorized`, `TransactionSettled`, `PaymentFailed` a tutti i servizi interessati (contabilità, notifiche, reportistica, riconciliazione) senza accoppiarli direttamente. La **retention** è particolarmente utile per audit e per poter "rigiocare" gli eventi se serve ricostruire lo stato di un servizio (si collega a Event Sourcing, già visto nel punto 8).

### Domande tipiche e risposte

- *D: Come garantisci l'ordinamento dei messaggi di uno stesso account?*
  R: Usando l'account ID come **chiave** del messaggio — Kafka instrada sempre la stessa chiave sulla stessa partizione, e l'ordine è garantito all'interno di una partizione.

- *D: Cosa succede se un consumer si blocca o crasha?*
  R: Se il commit dell'offset non è ancora avvenuto, al riavvio (o alla riassegnazione della partizione a un altro consumer del gruppo) il messaggio verrà riletto — Kafka garantisce **at-least-once delivery** di default, quindi l'elaborazione deve essere idempotente (di nuovo, il concetto di idempotenza visto più volte nel documento).

- *D: Differenza tra Kafka e un broker tradizionale come RabbitMQ?*
  R: Kafka è ottimizzato per throughput altissimo e retention/replay degli eventi, con un modello a log distribuito; RabbitMQ è più orientato al routing flessibile dei messaggi (exchange, binding) e alla semantica di coda classica, dove un messaggio consumato viene rimosso. Kafka si sceglie per event streaming/architetture event-driven su larga scala, RabbitMQ per task queue e routing complesso su volumi più contenuti.



################################################################################
### CAPITOLO: 13. JMS (Java Message Service)
################################################################################

# 13. JMS (Java Message Service)

### Cos'è
API standard Java (parte di Jakarta EE) per la messaggistica asincrona — definisce un'interfaccia comune indipendente dal broker sottostante (ActiveMQ, IBM MQ, e con adattatori anche altri). È concettualmente più "vecchio" e enterprise-oriented rispetto a Kafka, molto diffuso in sistemi bancari/finanziari legacy.

### Caratteristiche principali

- **Due modelli di messaggistica**:
  - **Point-to-Point (Queue)**: un messaggio viene consumato da **un solo** consumer, anche se più consumer sono in ascolto sulla stessa coda — modello classico "task queue"
  - **Publish/Subscribe (Topic)**: un messaggio viene consegnato a **tutti** i subscriber attivi sul topic
- **Message-Driven Bean / `@JmsListener`**: componenti che reagiscono automaticamente all'arrivo di un messaggio
- **Transazionalità**: JMS supporta l'integrazione con transazioni JTA (Java Transaction API), permettendo di coordinare l'invio/ricezione di un messaggio con un'operazione su database nella stessa transazione — un caso d'uso enterprise classico che Kafka non supporta nello stesso modo nativo
- **Acknowledgment modes**: controllano quando un messaggio è considerato "consumato con successo" (automatico, manuale, transazionale) — rilevante per garantire che un messaggio non vada perso se il processing fallisce a metà

### Esempio di utilizzo (Spring Boot)

```java
// Producer
@Autowired
private JmsTemplate jmsTemplate;

public void sendPaymentRequest(PaymentRequest request) {
    jmsTemplate.convertAndSend("payment.requests.queue", request);
}

// Consumer
@JmsListener(destination = "payment.requests.queue")
public void onPaymentRequest(PaymentRequest request) {
    paymentProcessor.process(request);
}
```

### Rilevanza per il dominio pagamenti
JMS è storicamente molto diffuso in ambito bancario/finanziario per l'integrazione tra sistemi legacy — è plausibile trovarlo in un'azienda di pagamenti con un'architettura consolidata da anni, magari in coesistenza con Kafka per i flussi più moderni. La sua integrazione nativa con transazioni JTA lo rende adatto a scenari dove serve la garanzia "o il messaggio viene inviato E la modifica al DB viene committata, oppure nessuna delle due" — un caso che Kafka gestisce diversamente (tramite pattern come outbox, non nativamente).

### Domande tipiche e risposte

- *D: Differenza principale tra JMS e Kafka?*
  R: JMS è pensato per code/topic con semantica di consegna "classica" (un messaggio consumato sparisce dalla coda, salvo configurazioni particolari) e forte integrazione transazionale enterprise; Kafka è un log distribuito con retention configurabile, pensato per throughput altissimo e replay degli eventi, più adatto ad architetture event-driven moderne su larga scala. In sintesi: JMS per messaging enterprise classico e transazionale, Kafka per event streaming ad alto volume.

- *D: Cosa succede se il consumer JMS fallisce durante l'elaborazione di un messaggio?*
  R: Dipende dall'acknowledgment mode: con acknowledgment automatico il messaggio potrebbe risultare già confermato anche se il processing fallisce dopo; per questo in scenari critici si usa acknowledgment manuale o transazionale, così il messaggio torna disponibile (redelivery) se l'elaborazione non è completata con successo — di nuovo, un caso dove l'idempotenza del consumer è essenziale per gestire in sicurezza eventuali redelivery.



################################################################################
### CAPITOLO: 14. Tecnologie Specialistiche: OSGi e MQTT
################################################################################

# 14. Tecnologie Specialistiche: OSGi e MQTT

## Cos'è e perché conta

In diversi contesti enterprise, industriali, IoT e sistemi di integrazione legacy o ad alta modularità (es. Adobe Experience Manager, piattaforme di telemetria, gateway di pagamento embedded o smart POS), emergono tecnologie specializzate come **OSGi** (per la modularità a caldo del codice Java) e **MQTT** (lo standard de facto per la messaggistica IoT leggera ed efficiente). Dimostrare competenza su questi temi evidenzia versatilità e comprensione dei protocolli di rete a basso livello e del classloading avanzato della JVM.

---

## 1. OSGi (Open Services Gateway initiative)

**OSGi** è una specifica e un framework per la **modularità dinamica** in Java. Consente di estendere la JVM per supportare il caricamento, l'aggiornamento e la disinstallazione di moduli software (*Bundle*) a runtime **senza riavviare l'applicazione** (*Hot Swapping / Dynamic Modular System*).

```
 ┌─────────────────────────────────────────────────────────────┐
 │                      OSGi FRAMEWORK                         │
 │                                                             │
 │  ┌───────────────────────────────────────────────────────┐  │
 │  │ SERVICE LAYER: Dynamic Service Registry (@Reference)  │  │
 │  ├───────────────────────────────────────────────────────┤  │
 │  │ LIFECYCLE LAYER: Manage bundle lifecycle states        │  │
 │  ├───────────────────────────────────────────────────────┤  │
 │  │ MODULE LAYER: Classloading, Export/Import Packages    │  │
 │  ├───────────────────────────────────────────────────────┤  │
 │  │ SECURITY LAYER: Java Security permissions             │  │
 │  └───────────────────────────────────────────────────────┘  │
 └──────────────────────────────┬──────────────────────────────┘
                                ▼
                       JAVA VIRTUAL MACHINE
```

### I Tre Livelli Fondamentali di OSGi

#### 1. Module Layer (I Bundle)
* Un **Bundle** è un normale file JAR che include metadati aggiuntivi nel file `META-INF/MANIFEST.MF`:
  ```ini
  Bundle-SymbolicName: com.bank.payment.gateway.visa
  Bundle-Version: 2.1.0
  Export-Package: com.bank.payment.api;version="2.1.0"
  Import-Package: org.osgi.framework;version="[1.8,2.0)",com.bank.common.crypto
  Bundle-Activator: com.bank.payment.internal.VisaActivator
  ```
* **Classloading Isolato**: A differenza della classica JVM flat classpath (dove tutto è visibile a tutti e si possono avere conflitti di versioni *JAR Hell*), in OSGi **ogni Bundle possiede il proprio ClassLoader dedicato**. Un bundle espone all'esterno solo i package dichiarati in `Export-Package` e può accedere solo ai package dichiarati in `Import-Package`.

#### 2. Lifecycle Layer (Ciclo di Vita del Bundle)
Il framework gestisce gli stati operativi di ciascun bundle:

```
           install            resolve              start
 [INSTALLED] ────► [RESOLVED] ───────► [STARTING] ──────► [ACTIVE]
      │               │                    │                 │
      │ uninstall     │                    │ stop            │ stop
      ▼               ▼                    ▼                 ▼
 [UNINSTALLED]   [INSTALLED]          [RESOLVED]        [STOPPING]
```

* **INSTALLED**: JAR scaricato e registrato nel framework.
* **RESOLVED**: Tutte le dipendenze (`Import-Package`) sono state soddisfatte da altri bundle attivi.
* **STARTING / ACTIVE**: L'attivatore o i componenti del bundle sono in esecuzione.
* **STOPPING**: Fase di rilascio risorse e deregistrazione servizi.
* **UNINSTALLED**: Bundle rimosso completamente dalla memoria.

#### 3. Service Layer & Declarative Services (OSGi DS)
* **Service Registry**: I bundle possono pubblicare servizi Java (*Service Registration*) o consumarli (*Service Lookup/Tracking*).
* **Declarative Services (SCR - Service Component Runtime)**: Meccanismo dichiarativo basato su annotazioni (analogo alla Dependency Injection di Spring):
  ```java
  @Component(service = PaymentProcessor.class, immediate = true)
  public class VisaPaymentProcessor implements PaymentProcessor {

      @Reference
      private CryptoService cryptoService; // Iniettato dinamicamente

      @Override
      public void process(Transaction tx) {
          byte[] signature = cryptoService.sign(tx.getPayload());
          // Logica di instradamento Visa
      }
  }
  ```

### Principali Implementazioni e Ambiti d'Uso:
* **Framework OSGi**: Apache Felix, Eclipse Equinox (motore di Eclipse IDE), Knopflerfish.
* **Runtime Enterprise**: Adobe Experience Manager (AEM), Apache Karaf, Red Hat Fuse.
* **Confronto con JPMS (Java Modules / Jigsaw)**: JPMS (introdotto in Java 9) offre incapsulamento a livello di compilazione ed esecuzione ma è statico (richiede riavvio della JVM). OSGi offre modularità e service registry **pienamente dinamici a runtime**.

---

## 2. MQTT (Message Queuing Telemetry Transport)

**MQTT** è un protocollo di messaggistica standard ISO (*ISO/IEC 20922*) estremamente **leggero, orientato agli eventi e basato su Publish/Subscribe**. È progettato specificamente per connessioni instabili, reti a bassa banda (3G/4G/Satellite) e dispositivi a risorse limitate (dispositivi IoT, POS portatili, sensori).

```
                         ARCHITETTURA PUB/SUB MQTT
  ┌──────────────┐         PUBLISH: "pos/terminal_12/payment"        ┌──────────────┐
  │ POS Terminal │ ────────────────────────────────────────────────► │ MQTT BROKER  │
  │ (Publisher)  │                                                   │ (Mosquitto/  │
  └──────────────┘                                                   │   HiveMQ)    │
                                                                     └──────┬───────┘
                                                                            │
                                   SUBSCRIBE: "pos/+/payment"               │
                                   ─────────────────────────────────────────┤
                                                                            ▼
                                                                     ┌──────────────┐
                                                                     │ Payment Core │
                                                                     │ (Subscriber) │
                                                                     └──────────────┘
```

### Caratteristiche Chiave del Protocollo:
* **Header Binario Minimale**: L'header fisso di un pacchetto MQTT occupa appena **2 byte**, contro le centinaia di byte degli header HTTP.
* **Trasporto**: Gira su protocollo affidabile **TCP/IP** (o WebSocket tramite TLS su porta 8883 / 443).
* **Topic Gerarchici & Wildcards**:
  * Topic strutturati a livelli con slash `/`: es. `terminals/italy/milan/pos_042/status`.
  * **Wildcard a Singolo Livello (`+`)**: `terminals/italy/+/pos_042/status` intercetta tutte le città.
  * **Wildcard Multi-Livello (`#`)**: `terminals/italy/#` intercetta qualsiasi topic che inizi con quel prefisso.

---

### Livelli di Quality of Service (QoS) in MQTT

La scelta del QoS determina il compromesso tra latenza/consumo di banda e affidabilità della consegna:

```
QoS 0 (At most once)         QoS 1 (At least once)            QoS 2 (Exactly once)
Client           Broker      Client            Broker         Client            Broker
  │  PUBLISH       │           │  PUBLISH        │              │  PUBLISH        │
  │ ─────────────► │           │ ──────────────► │              │ ──────────────► │
                               │  PUBACK         │              │  PUBREC         │
                               │ ◄────────────── │              │ ◄────────────── │
                                                                │  PUBREL         │
                                                                │ ──────────────► │
                                                                │  PUBCOMP        │
                                                                │ ◄────────────── │
```

1. **QoS 0 — At most once (Al massimo una volta)**:
   * "Fire and Forget": il messaggio viene inviato una sola volta senza conferma (*PUBACK*).
   * Rischio di perdita se la connessione cade. Adatto per metriche telemetriche ad altissima frequenza (es. temperatura ogni secondo).
2. **QoS 1 — At least once (Almeno una volta)**:
   * Il messaggio viene ritrasmesso finché il destinatario non risponde con un pacchetto **`PUBACK`**.
   * Garantisce la consegna, ma possono verificarsi messaggi duplicati se il `PUBACK` va perso nella rete. Richiede **idempotenza** lato consumer.
3. **QoS 2 — Exactly once (Esattamente una volta)**:
   * Protocollo di handshake a 4 vie (**PUBLISH $\to$ PUBREC $\to$ PUBREL $\to$ PUBCOMP**).
   * **Garantisce che il messaggio sia consegnato esattamente una volta senza perdite né duplicati**.
   * Ideale per transazioni finanziarie su smart POS, allarmi critici o addebiti dove la duplicazione causerebbe disastri.

---

### Funzionalità Avanzate di MQTT

* **Retained Messages (Messaggio Trattenuto)**:
  * Il publisher può impostare il flag `retain = true`. Il broker memorizza l'ultimo messaggio inviato su quel topic. Quando un nuovo subscriber si connette e fa la subscribe, riceve immediatamente l'ultimo stato valido senza attendere la pubblicazione successiva.
* **Last Will and Testament (LWT - Testamento)**:
  * In fase di connessione (`CONNECT`), il client registra un messaggio di "testamento" presso il broker (es. topic `devices/dev1/status`, payload `"OFFLINE"`).
  * Se il client si disconnette bruscamente per caduta di rete o crash, il broker pubblica automaticamente il messaggio LWT a tutti i subscriber, garantendo il rilevamento istantaneo dei guasti.
* **Persistent Session (Clean Session = false)**:
  * Il broker mantiene in memoria le sottoscrizioni e i messaggi QoS 1/2 pendenti per un dato `ClientID` anche mentre il dispositivo è disconnesso, consegnandoli tutti alla riconnessione.
* **Keep-Alive & PING**:
  * Scambio leggerissimo di pacchetti `PINGREQ` e `PINGRESP` (2 byte) per mantenere aperto il canale TCP ed evitare timeout dei firewall/NAT.

---

### Matrice Comparativa: MQTT vs HTTP vs WebSocket vs Kafka

| Caratteristica | MQTT | HTTP / REST | WebSocket | Apache Kafka |
| :--- | :--- | :--- | :--- | :--- |
| **Paradigma** | Pub/Sub Topic-based | Request/Response | Full-Duplex Bi-direzionale | Distributed Commit Log |
| **Overhead Header** | **Minimo (2 byte)** | Alto (centinaia di byte) | Molto basso (2-14 byte) | Medio-basso |
| **Garanzia Consegna**| QoS 0, QoS 1, QoS 2 | Nessuna nativa (a livello app) | Nessuna (TCP stream) | At-least-once, Exactly-once |
| **Consumo Batteria/CPU**| **Bassissimo** | Medio/Alto | Basso | N/A (Server-side) |
| **Persistenza Storica**| Solo ultimo (Retained) | Nessuna | Nessuna | **Persistenza su disco a lungo termine** |
| **Caso d'Uso Tipico** | Dispositivi IoT, Smart POS | API REST pubbliche | Notifiche Real-time su Browser | Event Streaming Backbone Enterprise |

---

## 3. Domande tipiche a colloquio (e risposte da Senior)

- *D: Perché in un'applicazione IoT o smart POS si preferisce MQTT rispetto a HTTP REST?*
  - **R**: Perché HTTP è un protocollo sincrono basato su polling o connessioni request/response pesanti con un overhead elevato di header (centinaia di byte per chiamata), che consumano molta banda e batteria su reti mobili. MQTT è asincrono basato su push, mantiene una singola connessione TCP persistente con un header di appena 2 byte, supporta la Quality of Service (QoS 0/1/2) e include feature native per la gestione delle disconnessioni di rete come *Last Will and Testament* e *Retained Messages*.

- *D: Come funziona il meccanismo di QoS 2 in MQTT e perché è più costoso in termini di latenza?*
  - **R**: Il QoS 2 garantisce la consegna *Exactly Once* attraverso un doppio handshake a 4 vie: il sender invia `PUBLISH`, il receiver memorizza il message ID e risponde con `PUBREC` (Publish Received); il sender invia `PUBREL` (Publish Release) e il receiver completa l'elaborazione rispondendo con `PUBCOMP` (Publish Complete). Questo scambio previene qualsiasi duplicazione o perdita anche in caso di retry, ma quadruplica i pacchetti scambiati rispetto a QoS 0, aumentando la latenza e l'overhead di rete.

- *D: Qual è il vantaggio principale di OSGi rispetto al classico Classpath di Java?*
  - **R**: Il classpath tradizionale di Java è "piatto" e non supporta l'isolamento: tutte le classi caricate sono visibili a tutti i componenti e non è possibile caricare due versioni diverse della stessa libreria (problema del *JAR Hell*). In OSGi ogni bundle ha un proprio ClassLoader che incapsula i package interni ed espone solo quelli esplicitamente dichiarati (`Export-Package`), permettendo la modularità dinamica, l'aggiornamento a caldo dei singoli bundle senza riavviare la JVM e la coesistenza di versioni multiple della stessa libreria nello stesso runtime.



################################################################################
### CAPITOLO: 15. Tecnologie Streaming, Media e Broadcast
################################################################################

# 15. Tecnologie Streaming, Media e Broadcast

## Cos'è e perché conta

L'ingegneria del software applicata al mondo **Media, OTT (Over-The-Top), Broadcast e Video Streaming** (es. piattaforme stile Netflix, DAZN, Sky, Twitch o piattaforme di live shopping e media asset management) affronta sfide estreme di scalabilità, throughput di rete, latenza e caching. Uno sviluppatore backend Senior deve comprendere l'intera **Media Pipeline**: dall'ingestion del segnale video grezzo alla transcodifica, dal packaging adattivo (HLS/DASH) alla distribuzione geografica su CDN, fino alla gestione di DRM, metadati sincronizzati e inserimento pubblicitario.

---

## 1. La Media Pipeline End-to-End

```
                      END-TO-END VIDEO STREAMING PIPELINE
  ┌──────────────┐      RTMP / SRT      ┌─────────────────────────┐
  │ Camera / Live│ ───────────────────► │ Ingestion & Transcoding │
  │ Video Source │                      │ (FFmpeg / AWS Elemental)│
  └──────────────┘                      └────────────┬────────────┘
                                                     │ Multi-bitrate (fMP4)
                                                     ▼
  ┌──────────────┐     HLS / DASH       ┌─────────────────────────┐
  │ Video Player │ ◄─────────────────── │ Packaging & DRM Engine  │
  │ (Web/Mobile) │                      │ (Widevine / FairPlay)   │
  └──────┬───────┘                      └────────────┬────────────┘
         │                                           │ Segments (.m4s, .ts)
         └───────────────────┐                       ▼
                             │           ┌─────────────────────────┐
                             └─────────► │ CDN Edge Caching        │
                                         │ (CloudFront / Akamai)   │
                                         └─────────────────────────┘
```

### Le Fasi della Pipeline:
1. **Ingestion (Acquisizione)**: La sorgente video (es. regia broadcast o encoder live) invia il flusso grezzo via protocolli a bassa latenza (SRT, RTMP) verso i server di acquisizione.
2. **Transcoding & Encoding (Transcodifica)**: Il flusso sorgente ad altissimo bitrate viene decodificato e ricompresso in più risoluzioni e bitrate (*Rendition Ladder*: es. 1080p a 5 Mbps, 720p a 2.5 Mbps, 480p a 1 Mbps, 360p a 500 Kbps) utilizzando codec moderni.
3. **Packaging**: Il video transcodificato viene spezzettato in piccoli file temporali (*Chunks / Segments* di 2-6 secondi) e vengono generati i file indice (*Manifest*).
4. **DRM & Encryption (Protezione del Contenuto)**: Cifratura dei segmenti video con AES-128 e integrazione con server di licenze DRM.
5. **CDN Distribution**: I segmenti video e i manifest vengono memorizzati e distribuiti sui nodi Edge delle CDN mondiali.
6. **Playback & ABR**: Il player sul dispositivo client seleziona dinamicamente il bitrate ottimale in base alla banda disponibile (*Adaptive Bitrate Streaming*).

---

## 2. Codecs, Container e Formati

* **Codec Video**:
  * **H.264 / AVC**: Lo standard universale compatibile con il 99.9% dei dispositivi.
  * **H.265 / HEVC**: Efficienza di compressione doppia rispetto ad H.264 (fondamentale per flussi 4K/UHD e HDR).
  * **AV1 / VP9**: Codec open-source ad altissima efficienza (supportati da YouTube, Netflix, Chrome).
* **Codec Audio**: **AAC** (Advanced Audio Coding), **Opus** (bassa latenza), **Dolby Digital Plus (E-AC-3)** (audio surround multicanale).
* **Formati Container**:
  * **fMP4 (Fragmented MP4 / CMAF)**: Standard moderno universale; separa i video in un file di inizializzazione (`init.mp4`) e singoli frammenti temporali indipendenti (`.m4s`).
  * **MPEG-2 TS (`.ts`)**: Container legacy a pacchetti da 188 byte storicamente usato da HLS.

---

## 3. Protocolli di Streaming: HLS vs MPEG-DASH vs WebRTC

```
┌───────────────┬────────────────────────────┬─────────────────────────────┬───────────────────────────┐
│ Caratteristica│ HLS (HTTP Live Streaming)  │ MPEG-DASH                   │ WebRTC                    │
├───────────────┼────────────────────────────┼─────────────────────────────┼───────────────────────────┤
│ **Creatore**  │ Apple (Standard IETF)      │ Standard Internazionale ISO │ W3C / IETF                │
│ **Manifest**  │ `.m3u8` (Playlist M3U)     │ `.mpd` (XML Presentation)   │ Nessuno (Signaling SDP)   │
│ **Segmenti**  │ `.ts`, `.m4s` (fMP4/CMAF)  │ `.mp4`, `.m4s` (fMP4/CMAF)  │ Nessun segmento (RTP/SRTP)│
│ **Latenza**   │ 6 - 30 sec (Standard)      │ 6 - 30 sec (Standard)       │ **< 500 ms (Sub-second)** │
│               │ 2 - 4 sec (LL-HLS)         │ 2 - 4 sec (LL-DASH)         │                           │
│ **Trasporto** │ HTTP/1.1, HTTP/2, HTTP/3   │ HTTP/1.1, HTTP/2, HTTP/3    │ UDP (SRTP con ICE/STUN)   │
│ **Scalabilità**│ **Massima (Cache su CDN)** │ **Massima (Cache su CDN)**  │ Media (Richiede SFU/MCU)  │
│ **Uso Tipico**│ OTT, Live TV, Video On Dem.│ Smart TV, Android, Web OTT  │ Live Betting, Aste, Meet  │
└───────────────┴────────────────────────────┴─────────────────────────────┴───────────────────────────┘
```

---

### HLS nel Dettaglio: Master Playlist e Media Playlist

Un flusso HLS è strutturato con una **Master Playlist** che elenca tutte le varianti di qualità (risoluzioni e bitrate) e rimanda a singole **Media Playlist**:

#### 1. Master Playlist (`master.m3u8`):
```m3u
#EXTM3U
#EXT-X-VERSION:6
#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080,CODECS="avc1.64002a,mp4a.40.2"
1080p/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2500000,RESOLUTION=1280x720,CODECS="avc1.4d401f,mp4a.40.2"
720p/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360,CODECS="avc1.42e01e,mp4a.40.2"
360p/index.m3u8
```

#### 2. Media Playlist per 1080p (`1080p/index.m3u8`):
```m3u
#EXTM3U
#EXT-X-VERSION:6
#EXT-X-TARGETDURATION:4
#EXT-X-MEDIA-SEQUENCE:101

#EXTINF:4.000,
segment_101.m4s
#EXTINF:4.000,
segment_102.m4s
#EXTINF:4.000,
segment_103.m4s
```

---

### Adaptive Bitrate Streaming (ABR)

L'algoritmo ABR implementato nel player client monitora continuamente:
1. **Throughput di download stimato**: Tempo impiegato per scaricare l'ultimo segmento video.
2. **Buffer Occupancy (Livello di riempimento del buffer)**: Secondi di video già scaricati e pronti in RAM.
3. Se la banda cala o il buffer si svuota, il player passa senza interruzioni (*seamlessly*) alla playlist con bitrate inferiore; non appena la rete torna stabile, effettua un *upscale* alla qualità superiore.

---

### Low-Latency Streaming: LL-HLS & Chunked Transfer

Nel broadcast tradizionale via HTTP, la latenza tipica è di 15-30 secondi (il player attende di avere 3 segmenti da 6 secondi nel buffer).
* **LL-HLS (Low-Latency HLS)**:
  * Divide ogni segmento in micro-frammenti (**Partial Segments / Chunks** da 200-300 ms).
  * Il server invia i partial segment al client man mano che vengono codificati tramite **HTTP/2 Chunked Transfer Encoding**, abbattendo la latenza a **2-3 secondi** (pari o inferiore al broadcast televisivo satellitare).

---

## 4. Content Protection: DRM (Digital Rights Management)

Per impedire la pirateria e rispettare i contratti dei content provider (Hollywood studio, leghe sportive), i media OTT utilizzano standard di cifratura e DRM:

* **CMAF & Common Encryption (CENC - ISO/IEC 23001-7)**:
  * Il file video viene cifrato una sola volta con algoritmo AES-128 in modalità CTR o CBCS.
  * Il file cifrato può essere decifrato da diversi sistemi DRM compatibili:
    * **Google Widevine**: Utilizzato su Android, Chrome, Smart TV Android/Google.
    * **Apple FairPlay**: Utilizzato su iOS, iPadOS, macOS, Safari, Apple TV.
    * **Microsoft PlayReady**: Utilizzato su Windows, Edge, Xbox.

---

## 5. Inserimento Pubblicitario e Metadati Sincronizzati

* **SSAI (Server-Side Ad Insertion / Dynamic Ad Insertion - DAI)**:
  * Il backend cuce dinamicamente gli spot pubblicitari direttamente nel flusso video (manifest e segmenti) personalizzandoli per singolo utente.
  * **Vantaggi**: Impossibile da bloccare con gli *Ad-Blocker* tradizionali, transizione fluida senza lag nel player.
* **CSAI (Client-Side Ad Insertion)**:
  * Il player client interrompe il video e richiede lo spot a un server ad-server (es. via protocolli VAST/VMAP).
* **SCTE-35 & ID3 Metadata**:
  * Segnali digitali incorporati nel flusso broadcast per indicare con precisione al millisecondo l'inizio e la fine dei break pubblicitari (*Cue-In / Cue-Out*).

---

## 6. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come funziona l'Adaptive Bitrate Streaming (ABR) e perché i segmenti video devono essere allineati temporalmente su tutte le qualità?*
  - **R**: In ABR il player client seleziona dinamicamente il bitrate più idoneo misurando la banda e la capienza del buffer. Affinché il cambio di qualità avvenga in modo trasparente e senza scatti (*seamless switching*), tutti i segmenti video di tutte le risoluzioni devono avere la **stessa durata temporale esatta** e iniziare con un **Keyframe (I-Frame / IDR frame)** allineato al millisecondo, consentendo al decoder di riprodurre il nuovo segmento senza dover ricalcolare i frame precedenti.

- *D: Qual è la differenza tra HLS/DASH e WebRTC, e quando sceglieresti WebRTC?*
  - **R**: HLS e DASH si basano su HTTP/TCP e architettura a segmenti: sfruttano le cache delle CDN standard permettendo di scalare a milioni di spettatori contemporanei con latenze tra 2 e 15 secondi. WebRTC si basa su UDP (SRTP) e streaming continuo senza segmentazione, offrendo latenza **sub-secondo (< 500 ms)**. Sceglierei WebRTC per applicazioni interattive real-time (aste live, scommesse in-play, videochiamate, cloud gaming), mentre per grandi eventi sportivi broadcast con milioni di utenti si preferisce LL-HLS/DASH per l'imbattibile scalabilità e costi delle CDN.

- *D: Come gestisci il caching a livello di CDN per i file manifest rispetto ai segmenti video?*
  - **R**: I **segmenti video** (`.m4s` o `.ts`) sono immutabili e vengono memorizzati in cache sulla CDN con un `Cache-Control: public, max-age=31536000` (1 anno) per massimizzare il cache-hit ratio. Al contrario, i **manifest di flussi live** (`.m3u8` o `.mpd`) cambiano continuamente perché vengono aggiunti nuovi segmenti ogni pochi secondi: su di essi si imposta una cache brevissima (`max-age=1` o `no-cache`), assicurando che i player ricevano sempre l'aggiornamento dell'ultimo segmento live disponibile.



################################################################################
### CAPITOLO: 16. Comparazioni: OpenShift vs Kubernetes, RabbitMQ vs Kafka
################################################################################

# 16. Comparazioni: OpenShift vs Kubernetes, RabbitMQ vs Kafka

### Cos'è e perché conta
In un colloquio senior, le domande di confronto ("quando useresti X invece di Y?") sono tra le più frequenti, perché rivelano se hai capito i trade-off e non solo la sintassi. Qui trovi due confronti diretti, molto probabili dato lo stack già discusso.

### OpenShift vs Kubernetes

**Cos'è OpenShift**: piattaforma enterprise di Red Hat **basata su Kubernetes** — non è un'alternativa, è una distribuzione di Kubernetes "batterie incluse", con funzionalità aggiuntive, opinionated defaults e supporto commerciale. Molto diffusa in contesti enterprise regolamentati (banche, assicurazioni, pagamenti) proprio per il supporto e la maggiore rigidità/sicurezza di default.

**Differenze principali**

| Aspetto | Kubernetes (vanilla) | OpenShift |
|---|---|---|
| Natura | Progetto open source, componenti da assemblare | Distribuzione completa "pronta all'uso" di Red Hat |
| Console/UI | Non inclusa di default (serve aggiungere Dashboard) | Console web integrata, ricca di funzionalità |
| Build integrato | Non nativo | **Source-to-Image (S2I)**: build dell'immagine container direttamente da codice sorgente, integrato nella piattaforma |
| Sicurezza di default | Configurazione più permissiva, da irrobustire manualmente | **Security Context Constraints (SCC)** più restrittive di default (es. i container non girano come root per default) — importante in ambienti regolamentati |
| Routing esterno | `Ingress` (richiede un controller a parte) | `Route`, concetto nativo di OpenShift equivalente ma integrato out-of-the-box |
| CLI | `kubectl` | `oc` (superset di `kubectl`, con comandi aggiuntivi) |
| Supporto commerciale | Community/vendor dipendente | Supporto enterprise Red Hat incluso — spesso decisivo in ambito bancario/regolamentato |
| Portabilità | Stesso "motore" sotto entrambi | I concetti base (Pod, Deployment, Service) restano identici — le competenze Kubernetes si trasferiscono direttamente a OpenShift |

**Perché è rilevante**: le competenze Kubernetes (Pod, Deployment, Service, ConfigMap, probe, autoscaling — già visti nel punto 17) restano valide identiche su OpenShift, che aggiunge principalmente governance, sicurezza di default più stringente e tooling enterprise sopra lo stesso motore. In un colloquio, sapere dire "conosco Kubernetes, e so che OpenShift è una distribuzione enterprise costruita sopra, con SCC più stringenti e strumenti di build integrati" è una risposta solida anche senza esperienza diretta su OpenShift.

**Domande tipiche e risposte**

- *D: OpenShift e Kubernetes sono alternativi?*
  R: No, OpenShift **è** Kubernetes — nello specifico è una distribuzione certificata e supportata commercialmente da Red Hat, con componenti aggiuntivi (console, S2I, SCC, Route). Chi sa usare Kubernetes ha già la base per lavorare su OpenShift.

- *D: Perché un'azienda regolamentata come una fintech sceglierebbe OpenShift invece di Kubernetes vanilla?*
  R: Per il supporto commerciale enterprise (SLA, patch di sicurezza garantite), le policy di sicurezza più stringenti di default (rilevante per compliance PCI-DSS), e strumenti di governance/multi-tenancy già integrati — riducendo il lavoro di hardening che andrebbe fatto manualmente su Kubernetes vanilla.

### RabbitMQ vs Kafka

Entrambi sono message broker, ma nascono con filosofie diverse: RabbitMQ è un **broker di messaggistica tradizionale** orientato al routing flessibile, Kafka è un **log distribuito di eventi** orientato a throughput e retention.

**Differenze principali**

| Aspetto | RabbitMQ | Kafka |
|---|---|---|
| Modello | Broker con code (AMQP), il messaggio viene rimosso dopo il consumo | Log distribuito partizionato, i messaggi restano per la retention configurata anche dopo la lettura |
| Routing | Molto flessibile: exchange (direct, topic, fanout, headers) permettono routing complesso dei messaggi verso code diverse | Routing più semplice, basato su topic/partition — il routing complesso va gestito applicativamente |
| Throughput | Alto, ma generalmente inferiore a Kafka su volumi molto grandi | Ottimizzato per throughput altissimo (milioni di messaggi/secondo) |
| Ordinamento | Garantito per coda (FIFO), con alcune eccezioni su retry/priorità | Garantito solo all'interno di una singola partizione |
| Replay dei messaggi | Non nativo — un messaggio consumato è normalmente perso | Nativo, grazie alla retention: un consumer può rileggere eventi passati semplicemente ripartendo da un offset precedente |
| Casi d'uso tipici | Task queue, RPC, routing complesso di messaggi tra servizi, scenari dove serve consegna puntuale e prioritizzazione | Event streaming, event sourcing, pipeline di dati, audit trail, integrazione tra molti servizi/consumer sullo stesso stream di eventi |
| Complessità operativa | Generalmente più semplice da gestire su piccola/media scala | Più complessa da operare (Zookeeper/KRaft, partizionamento, tuning), ma pensata per scalare su volumi enterprise |

**Come sceglierli nel dominio pagamenti**

- **RabbitMQ**: adatto per task puntuali con routing condizionale (es. instradare una richiesta di autorizzazione verso il gestore giusto in base al circuito), o per pattern RPC asincroni tra due servizi specifici
- **Kafka**: adatto per propagare eventi di dominio (`TransactionAuthorized`, `TransactionSettled`) a **molti** consumer diversi contemporaneamente (contabilità, notifiche, reportistica, riconciliazione, audit) con necessità di retention/replay per motivi di compliance — coerente con quanto già visto nel punto 15

**Domande tipiche e risposte**

- *D: Se dovessi scegliere uno dei due per un sistema di notifiche transazionali con audit trail, quale sceglieresti e perché?*
  R: Kafka, perché la retention permette di conservare lo storico degli eventi per audit/compliance e di far leggere lo stesso evento a più consumer indipendenti (notifiche, reportistica, riconciliazione) senza che si "consumino" a vicenda — con RabbitMQ, per ottenere lo stesso effetto multi-consumer servirebbe un exchange fanout con una coda dedicata per ogni consumer, più complesso da gestire e senza il replay nativo degli eventi passati.

- *D: RabbitMQ garantisce l'ordine dei messaggi?*
  R: Sì, all'interno di una singola coda i messaggi vengono consegnati nell'ordine di arrivo (salvo l'uso di funzionalità come priorità o retry che possono alterarlo) — ma se più producer scrivono sulla stessa coda o se ci sono più consumer che leggono in parallelo dalla stessa coda, l'ordine di elaborazione non è comunque garantito end-to-end, un dettaglio simile al vincolo di Kafka sull'ordinamento per singola partizione.

### Come esercitarti
Prepara una frase riassuntiva unica per ciascun confronto, da avere pronta: "OpenShift è Kubernetes con più governance e sicurezza di default, utile in contesti regolamentati"; "RabbitMQ per routing flessibile e task puntuali, Kafka per event streaming ad alto volume con retention e replay" — sono le sintesi che un intervistatore si aspetta di sentire in pochi secondi, prima di eventuali approfondimenti.



################################################################################
### CAPITOLO: 17. Containerizzazione (Docker e OCI)
################################################################################

# 17. Containerizzazione (Docker e OCI)

### Cos'è e perché conta
La containerizzazione è il fondamento del deployment moderno su cloud e ambienti Kubernetes. Un'immagine container incapsula il codice applicativo, il runtime Java (JRE), le librerie e la configurazione del sistema operativo, garantendo che l'applicazione si comporti in modo identico in locale, in ambiente di staging e in produzione. Un Senior Developer deve saper scrivere `Dockerfile` sicuri, ottimizzati e leggeri usando **Multi-Stage Builds**.

---

### Cosa studiare

#### 1. Architettura dei Container: Container vs Macchine Virtuali (VM)

```
┌───────────────────────────────┐     ┌───────────────────────────────┐
│     CONTAINER ARCHITECTURE    │     │    VIRTUAL MACHINE (VM)       │
├───────────────────────────────┤     ├───────────────────────────────┤
│ App 1 (Java)   App 2 (Node)   │     │ App 1 (Java)   App 2 (Node)   │
│ Bins/Libs      Bins/Libs      │     │ Bins/Libs      Bins/Libs      │
├───────────────────────────────┤     │ Guest OS 1     Guest OS 2     │
│   CONTAINER ENGINE (Docker)   │     ├───────────────────────────────┤
├───────────────────────────────┤     │          HYPERVISOR           │
│   HOST OPERATING SYSTEM       │     ├───────────────────────────────┤
├───────────────────────────────┤     │     HOST OPERATING SYSTEM     │
│   PHYSICAL INFRASTRUCTURE    │     │    PHYSICAL INFRASTRUCTURE   │
└───────────────────────────────┘     └───────────────────────────────┘
```

- **Macchina Virtuale**: virtualizza l'hardware; ogni VM include un intero sistema operativo guest (Guest OS), occupando diversi GB di RAM/disco con tempi di avvio nell'ordine dei minuti.
- **Container**: virtualizza l'OS; condivide il **Kernel Linux** dell'host isolando i processi tramite due primitive fondamentali del kernel:
  1. **Namespaces**: isolamento delle risorse (PID per i processi, NET per la rete, MNT per il filesystem, IPC per la memoria condivisa).
  2. **cgroups (Control Groups)**: limitazione e monitoraggio dell'uso di risorse hardware (massima CPU, massima memoria RAM assegnabile al container).

---

#### 2. Anatomia di un'Immagine Docker e Layer Caching

Un'immagine Docker è composta da una pila di **layer di sola lettura (Read-Only)** memorizzati tramite un Union File System (overlay2). Quando si avvia un container, Docker aggiunge in cima un sottile layer di lettura/scrittura (**Container/Writable Layer**).

- **Principio del Layer Caching**:
  - Docker riutilizza la cache per ogni istruzione (`COPY`, `RUN`) finché i file sorgente di quell'istruzione non cambiano.
  - **Best Practice per Java**: copiare prima i file di configurazione Maven/Gradle (`pom.xml` / `mvnw`) e scaricare le dipendenze (`RUN ./mvnw dependency:go-offline`), e solo successivamente copiare il codice sorgente `src/`. In questo modo, modificando solo il codice Java, Docker riutilizza la cache dei layer delle dipendenze velocizzando drasticamente la build da minuti a secondi.

---

#### 3. Dockerfile Multi-Stage per Applicazioni Spring Boot

Nei contesti di produzione bancari/enterprise, l'immagine finale non deve contenere il compilatore Maven/JDK, il codice sorgente o strumenti di sviluppo (per motivi di sicurezza e dimensione). Si usa il pattern **Multi-Stage Build**:

```dockerfile
# ==========================================
# STAGE 1: Build & Package (con Maven/JDK)
# ==========================================
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app

# Copia solo i file di build per sfruttare il layer caching
COPY pom.xml mvnw ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline -B

# Copia i sorgenti e compila il JAR
COPY src ./src
RUN ./mvnw clean package -DskipTests

# Estrae i layer del fat-jar Spring Boot per ottimizzare il caching dei container
RUN java -Djarmode=layertools -jar target/*.jar extract

# ==========================================
# STAGE 2: Runtime Image (Minimale & Sicura)
# ==========================================
FROM eclipse-temurin:21-jre-alpine AS runner
WORKDIR /workspace

# Creazione di un utente non-root per conformità di sicurezza
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser:appgroup

# Copia i layer Spring Boot estratti dallo stage precedente
COPY --from=builder /app/dependencies/ ./
COPY --from=builder /app/spring-boot-loader/ ./
COPY --from=builder /app/snapshot-dependencies/ ./
COPY --from=builder /app/application/ ./

# Esposizione porta e variabili JVM
EXPOSE 8080
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75.0 -XX:+UseG1GC -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS org.springframework.boot.loader.launch.JarLauncher"]
```

---

#### 4. Sicurezza dei Container & Best Practice di Produzione

1. **Mai eseguire come utente `root`**: usare sempre `USER appuser` per prevenire attacchi di container breakout.
2. **Usare Immagini Base Minimali (Distroless / Alpine / Chainguard)**: riduce la superficie di attacco eliminando package manager, shell non necessarie e utility obsolete.
3. **Gestione della Memoria JVM nei Container (`-XX:MaxRAMPercentage`)**:
   - Nelle versioni moderne di Java (8u191+, 11, 17, 21), la JVM riconosce i limiti di memoria del cgroup del container.
   - Usare `-XX:MaxRAMPercentage=75.0` anziché fissare `-Xmx` con valori statici in MB, permettendo al container di scalare dinamicamente in base ai limiti assegnati da Kubernetes.
4. **Scansione delle Vulnerabilità delle Immagini (Trivy / Snyk / Docker Scout)**: integrata nella pipeline CI per bloccare immagini con CVE critiche a livello di sistema operativo.
5. **Mai inserire Segreti o Certificati nell'Immagine**: iniettarli a runtime tramite Environment Variables o Secret montati come volumi (Kubernetes Secrets / HashiCorp Vault).

---

#### 5. Docker Compose per lo Sviluppo Locale

Strumento per orchestrare ambienti multi-container locali (Spring Boot + Oracle XE + Kafka + Redis):

```yaml
version: '3.8'
services:
  payment-db:
    image: gvenzl/oracle-xe:21-slim-faststart
    environment:
      - ORACLE_PASSWORD=topsecret
      - APP_USER=payment_user
      - APP_USER_PASSWORD=payment_pass
    ports:
      - "1521:1521"
    volumes:
      - oracle_data:/opt/oracle/oradata

  kafka-broker:
    image: confluentinc/cp-kafka:7.4.0
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: 'CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT'
      KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka-broker:29092,PLAINTEXT_HOST://localhost:9092'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"

volumes:
  oracle_data:
```

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Perché utilizzi il Multi-Stage Build nel Dockerfile?*
  - **R**: Perché permette di separare nettamente l'ambiente di compilazione (che necessita di JDK completo, Maven/Gradle, codice sorgente e file di configurazione) dall'ambiente di runtime (che necessita solo del JRE minimale e dei file `.class`). Questo riduce la dimensione dell'immagine finale da oltre 600MB a meno di 150MB ed elimina dalla produzione strumenti di compilazione che aumenterebbero la superficie di attacco.

- *D: Come si comporta la memoria della JVM all'interno di un container Docker/Kubernetes?*
  - **R**: Storicamente la JVM leggeva la memoria fisica totale dell'host ignorando i limiti del cgroup, causando l'uccisione del container da parte dell'OOM Killer del kernel Linux. Dalle versioni recenti (Java 11/17/21), la JVM supporta nativamente i cgroups: impostando il flag `-XX:MaxRAMPercentage=75.0`, la JVM alloca come dimensione massima dello Heap il 75% della memoria RAM assegnata al container, lasciando il restante 25% per Metaspace, thread stack e memoria off-heap del sistema operativo.

---

### Come esercitarti
1. **Scrittura Dockerfile**: prendi un progetto Spring Boot e scrivi un `Dockerfile` a due stadi con Alpine JRE, utente non-root e flag JVM container-aware; compilalo ed esegui `docker run` verificando che l'utente non sia root con `docker exec -it <id> whoami`.



################################################################################
### CAPITOLO: 18. Kubernetes
################################################################################

# 18. Kubernetes

### Cos'è
Piattaforma di **orchestrazione container**, che gestisce automaticamente deployment, scaling, self-healing e networking di applicazioni containerizzate (tipicamente Docker). Non esegue direttamente il codice: coordina container su un cluster di macchine (nodi).

### Caratteristiche principali

- **Pod**: unità minima di deployment — uno o più container che condividono rete e storage, eseguiti sempre insieme sullo stesso nodo
- **Deployment**: definisce quante repliche di un pod devono essere in esecuzione e gestisce gli aggiornamenti (rolling update) senza downtime
- **Service**: espone un insieme di pod come un endpoint di rete stabile, con load balancing automatico tra le repliche — anche se i pod vengono ricreati con IP diversi, il Service resta raggiungibile allo stesso indirizzo
- **ConfigMap e Secret**: configurazione esterna all'immagine del container (coerente col principio 12-factor già visto nel punto 9) — ConfigMap per configurazioni non sensibili, Secret per credenziali/chiavi
- **Horizontal Pod Autoscaler**: scala automaticamente il numero di pod in base a metriche (es. CPU) — implementazione concreta dell'auto-scaling già visto nel punto 9
- **Liveness/Readiness probe**: health check che Kubernetes usa per capire se un pod è vivo (liveness — altrimenti lo riavvia) e se è pronto a ricevere traffico (readiness — altrimenti lo esclude temporaneamente dal load balancing) — implementazione concreta di health check e self-healing (punto 9)
- **Namespace**: partizione logica del cluster, utile per isolare ambienti (dev, staging, produzione) o team diversi

### Esempio concettuale (non serve saperlo scrivere a memoria, ma riconoscerlo)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: authorization-service
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: authorization-service
          image: registry.company.com/authorization-service:1.4.0
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
```

### Rilevanza per il dominio pagamenti
In un sistema mission-critical, Kubernetes garantisce che un servizio come `authorization-service` resti sempre disponibile con più repliche, si riavvii automaticamente in caso di crash (self-healing), e scali automaticamente nei picchi di traffico — tutto senza intervento manuale. I probe di readiness sono particolarmente importanti: un servizio di pagamento non ancora pronto (es. connessione DB non ancora stabilita all'avvio) non deve ricevere traffico prematuramente.

### Domande tipiche e risposte

- *D: Che differenza c'è tra liveness e readiness probe?*
  R: La liveness probe dice a Kubernetes "sono vivo o devo essere riavviato?" — se fallisce, il pod viene ucciso e ricreato. La readiness probe dice "sono pronto a ricevere traffico in questo momento?" — se fallisce, il pod resta in esecuzione ma viene temporaneamente escluso dal load balancing, utile ad esempio durante l'avvio o se una dipendenza esterna è momentaneamente non raggiungibile.

- *D: Come gestisce Kubernetes un deployment senza downtime?*
  R: Con un **rolling update**: crea gradualmente i nuovi pod con la versione aggiornata, aspetta che passino la readiness probe, e solo allora rimuove gradualmente i pod vecchi — mantenendo sempre un numero minimo di repliche disponibili durante la transizione. Si collega al blue-green/canary già visti nel punto 11, che in Kubernetes si implementano con strategie di deployment più sofisticate sopra questo meccanismo base.



################################################################################
### CAPITOLO: 19. Architettura Cloud
################################################################################

# 19. Architettura Cloud, Servizi AWS e Infrastructure as Code (IaC)

## Cos'è e perché conta

La progettazione di applicazioni enterprise moderne richiede una profonda padronanza dei paradigmi **Cloud-Native**. Un Senior Software Engineer non si limita a scrivere codice applicativo, ma comprende l'ambiente distribuito in cui il software viene eseguito: architettura dei servizi **AWS**, strategie di alta disponibilità e disaster recovery, pattern di deployment a zero-downtime, sicurezza IAM e gestione dell'infrastruttura tramite codice (**Infrastructure as Code - IaC** con Terraform e CDK).

---

## 1. Modelli Cloud e Principi Cloud-Native

```
                            I MODELLI DI SERVIZIO CLOUD
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ SaaS (Software as a Service)       │ Salesforce, Microsoft 365, Jira        │
 ├────────────────────────────────────┼────────────────────────────────────────┤
 │ PaaS (Platform as a Service)       │ AWS Elastic Beanstalk, Heroku          │
 ├────────────────────────────────────┼────────────────────────────────────────┤
 │ FaaS (Function as a Service)       │ AWS Lambda, Google Cloud Functions     │
 ├────────────────────────────────────┼────────────────────────────────────────┤
 │ IaaS (Infrastructure as a Service) │ AWS EC2, VPC, EBS, Azure VMs           │
 └────────────────────────────────────┴────────────────────────────────────────┘
```

### I Principi della 12-Factor App & Cloud-Native Design:
1. **Stateless Processes**: L'applicazione non mantiene stato in memoria locale tra una richiesta HTTP e l'altra. Lo stato (sessioni, token, carrelli) è esternalizzato su DB o cache distribuita (Redis), permettendo a qualsiasi istanza di servire qualsiasi richiesta e abilitando l'auto-scaling orizzontale istantaneo.
2. **Externalized Configuration**: Credenziali, URL dei database, feature flag ed endpoint sono iniettati tramite variabili d'ambiente o secret manager (AWS Secrets Manager / SSM Parameter Store), mai hardcoded nel codice sorgente.
3. **Disposability & Fast Startup**: I processi devono potersi avviare rapidamente e terminare in modo pulito (*Graceful Shutdown* intercettando `SIGTERM` per completare le transazioni in volo prima di chiudere le connessioni).
4. **Cattle, Not Pets**: Le istanze e i container sono considerati risorse effimere e sostituibili automaticamente (bestiame), non server unici configurati manualmente e accuditi nel tempo (animali domestici).

---

## 2. Deep Dive sui Servizi Core AWS

```
                           ARCHITETTURA APPLICATIVA AWS
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                           AMAZON ROUTE 53 (DNS)                             │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                     APPLICATION LOAD BALANCER (ALB)                         │
  └──────────────────┬───────────────────────────────────────┬──────────────────┘
                     │                                       │
            Public Subnet 1                         Public Subnet 2
                     │                                       │
     ┌───────────────▼───────────────┐       ┌───────────────▼───────────────┐
     │ NAT Gateway                   │       │ NAT Gateway                   │
     └───────────────┬───────────────┘       └───────────────┬───────────────┘
                     │                                       │
            Private Subnet 1                        Private Subnet 2
                     │                                       │
     ┌───────────────▼───────────────┐       ┌───────────────▼───────────────┐
     │ ECS Fargate / EKS Pods        │◄─────►│ ECS Fargate / EKS Pods        │
     │ (Spring Boot Backend)         │       │ (Spring Boot Backend)         │
     └───────────────┬───────────────┘       └───────────────┬───────────────┘
                     │                                       │
                     ├───────────────────┬───────────────────┤
                     ▼                   ▼                   ▼
            ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
            │ Amazon Aurora   │ │ Amazon ElastiCache││ Amazon SQS /   │
            │ (Multi-AZ DB)   │ │ (Redis Cluster) │ │ SNS Messaging   │
            └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 1. Compute
* **Amazon EC2 (Elastic Compute Cloud)**: Macchine virtuali IaaS scalabili.
* **Amazon ECS (Elastic Container Service) & AWS Fargate**:
  * Orchestratore container proprietario AWS.
  * **Fargate (Serverless Container)**: Esegue container Docker senza dover gestire o fare patching delle istanze EC2 sottostanti; si paga solo per CPU e memoria allocate al task.
* **Amazon EKS (Elastic Kubernetes Service)**: Kubernetes gestito enterprise per cluster multi-container ad alta complessità.
* **AWS Lambda (Serverless FaaS)**:
  * Esecuzione di codice guidata dagli eventi (*Event-Driven*) con scalabilità da zero a migliaia di istanze concorrenti.
  * *Considerazioni per Java*: Attenzione al **Cold Start** (tempo di avvio della JVM); mitigabile tramite *Provisioned Concurrency*, SnapStart (CRaC - Coordinated Restore at Checkpoint) o GraalVM Native Image.

### 2. Networking & Security
* **Amazon VPC (Virtual Private Cloud)**: Rete virtuale isolata logicamente.
* **Public vs Private Subnet**:
  * *Public Subnet*: Ha una rotta verso l'**Internet Gateway (IGW)**; ospita risorse che devono ricevere traffico da internet (es. Application Load Balancer).
  * *Private Subnet*: Non ha accesso diretto da internet; ospita i microservizi backend e i database. Accede a internet in uscita (es. per scaricare patch o chiamare API terze) tramite un **NAT Gateway** posizionato nella public subnet.
* **Security Groups vs Network ACLs (NACL)**:
  * *Security Group*: Firewall virtuale **stateful** associato alla singola istanza/interfaccia di rete (se il traffico in ingresso è consentito, la risposta in uscita è permessa automaticamente).
  * *NACL*: Firewall **stateless** a livello di intera subnet (richiede regole esplicite sia per Inbound che per Outbound).
* **AWS IAM (Identity and Access Management)**:
  * Principio del **Privilegio Minimo (*Least Privilege*)**.
  * Uso di **IAM Roles** e *Instance Profiles* (i container/istanze assumono ruoli temporanei tramite token STS senza memorizzare mai credenziali o access key nei file di configurazione).

### 3. Storage & Database Gestiti
* **Amazon S3 (Simple Storage Service)**: Storage ad oggetti altamente affidabile (99.999999999% - 11 nine di durabilità). Utilizzato per backup, report finanziari, tracciati batch e media.
* **Amazon RDS (Relational Database Service)**:
  * Motori relazionali gestiti (PostgreSQL, MySQL, Oracle).
  * **Multi-AZ Deployment**: Replica sincrona su una seconda Availability Zone con failover automatico trasparente in caso di guasto hardware.
  * **Read Replicas**: Repliche asincrone per distribuire il carico di lettura.
* **Amazon Aurora**:
  * Motore DB cloud-native compatibile Postgres/MySQL con storage distribuito a 6 copie su 3 AZ, throughput fino a 5x rispetto a MySQL standard e failover in meno di 30 secondi.
* **Amazon DynamoDB**:
  * NoSQL Key-Value e Document Store completamente gestito con latenze a singola cifra di millisecondo su qualsiasi scala di traffico.

### 4. Messaging ed Event-Driven nel Cloud
* **Amazon SQS (Simple Queue Service)**:
  * Coda di messaggi punto a punto completamente gestita.
  * *Standard Queue*: Throughput illimitato, garanzia di consegna *At-least-once*, ordinamento non garantito.
  * *FIFO Queue*: Consegna rigorosa nell'ordine esatto (*First-In-First-Out*) ed elaborazione *Exactly-Once* basata su `MessageGroupId` e `MessageDeduplicationId`.
  * *Dead Letter Queue (DLQ)*: Coda di smistamento per messaggi falliti dopo $N$ tentativi di retry (*MaxReceiveCount*).
* **Amazon SNS (Simple Notification Service)**:
  * Sistema Publish/Subscribe per notificare messaggi a molteplici destinatari contemporaneamente (*Fan-out pattern* verso code SQS, endpoint HTTP, email o funzioni Lambda).
* **Amazon EventBridge**:
  * Event Bus serverless per instradare eventi tra microservizi, servizi SaaS (Datadog, Zendesk) e risorse AWS tramite regole di filtraggio dichiarative sul payload JSON.

---

## 3. Cloud Deployment Patterns & Resilienza

```
                           BLUE / GREEN DEPLOYMENT
                    ┌─────────────────────────────────────┐
                    │       Router / Load Balancer        │
                    └──────────────────┬──────────────────┘
                                       │ Switch 100% traffico
                     ┌─────────────────┴─────────────────┐
                     ▼                                   ▼
        ┌────────────────────────┐          ┌────────────────────────┐
        │     Ambiente BLUE      │          │     Ambiente GREEN     │
        │   (Versione Attuale)   │          │    (Nuova Versione)    │
        │     • Istanze v1.0     │          │     • Istanze v2.0     │
        └────────────────────────┘          └────────────────────────┘
```

1. **Blue/Green Deployment**:
   * Due ambienti di produzione identici (Blue attivo, Green inattivo). Si rilascia la nuova versione su Green, si eseguono i test di fumo e poi si sposta istantaneamente il traffico del Load Balancer / DNS da Blue a Green. **Rollback istantaneo** in caso di anomalie.
2. **Canary Deployment**:
   * Il nuovo rilascio viene esposto inizialmente solo a una percentuale ridotta di traffico reale (es. $5\%$). Se i tassi di errore e la latenza rimangono nominali, il traffico viene incrementato progressivamente ($25\% \to 50\% \to 100\%$).
3. **Rolling Updates**:
   * Aggiornamento progressivo istanza per istanza (o pod per pod) mantenendo sempre una capacità minima operativa (*min healthy percentage*).
4. **Disaster Recovery Multi-Region**:
   * **RTO (Recovery Time Objective)**: Tempo massimo accettabile per ripristinare il servizio dopo un disastro.
   * **RPO (Recovery Point Objective)**: Quantità massima di dati che si è disposti a perdere (espressa in tempo: es. dati degli ultimi 5 minuti).
   * Strategie: *Backup & Restore* $\to$ *Pilot Light* $\to$ *Warm Standby* $\to$ *Active-Active Multi-Region*.

---

## 4. Infrastructure as Code (IaC)

L'**Infrastructure as Code** è la pratica di definire, configurare e gestire l'infrastruttura cloud tramite file di codice dichiarativi versionati su Git, eliminando la configurazione manuale via console (*Click-Ops*).

```
 ┌─────────────────┐      terraform plan      ┌─────────────────┐      terraform apply     ┌─────────────────┐
 │ File .tf (HCL)  │ ───────────────────────► │ Preview Modifiche│ ──────────────────────► │ Provider Cloud  │
 │ (Git Repo)      │                          │ (Diff vs State)  │                         │ (AWS Resources) │
 └─────────────────┘                          └─────────────────┘                          └─────────────────┘
```

### 1. Terraform (HashiCorp / OpenTofu)
* **Approccio Dichiarativo**: Si dichiara lo stato desiderato finale dell'infrastruttura; Terraform calcola il piano di esecuzione per raggiungerlo.
* **Componenti Chiave**:
  * **HCL (HashiCorp Configuration Language)**: Sintassi leggibile per descrivere risorse, variabili e output.
  * **Terraform State File (`terraform.tfstate`)**: Mappa le risorse definite nel codice con gli oggetti reali nel cloud. Deve essere salvato su un backend remoto sicuro (es. Bucket S3 con cifratura e lock distribuito su tabella DynamoDB per evitare scritture concorrenti).
  * **Drift Detection**: Terraform confronta lo stato reale del cloud con il file di stato, rilevando modifiche manuali non autorizzate.

```hcl
# Esempio Terraform: Creazione Coda SQS con Dead Letter Queue
resource "aws_sqs_queue" "payment_dlq" {
  name                      = "payment-processing-dlq"
  message_retention_seconds = 1209600 # 14 giorni
}

resource "aws_sqs_queue" "payment_queue" {
  name                      = "payment-processing-queue"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.payment_dlq.arn
    maxReceiveCount     = 3
  })
}
```

### 2. AWS CDK (Cloud Development Kit)
* Consente di definire l'infrastruttura AWS utilizzando veri linguaggi di programmazione orientati agli oggetti (**Java**, TypeScript, Python).
* Compila (*synthesizes*) il codice in template standard **AWS CloudFormation**, offrendo costrutti di alto livello riutilizzabili con type safety a tempo di compilazione.

---

## 5. Domande tipiche a colloquio (e risposte da Senior)

- *D: Perché i database e i microservizi backend vanno sempre posizionati in Private Subnet e come comunicano con l'esterno?*
  - **R**: Vengono posizionati in Private Subnet per sicurezza e conformità (difesa in profondità): non possiedono indirizzi IP pubblici e non sono raggiungibili direttamente dalla rete internet, prevenendo attacchi diretti. Il traffico in ingresso dall'esterno attraversa un **Application Load Balancer (ALB)** pubblico posizionato nella Public Subnet. Se i servizi privati devono effettuare chiamate in uscita verso API esterne (es. gateway Visa/Mastercard), il traffico in uscita viene instradato attraverso un **NAT Gateway** con IP elastico posizionato nella Public Subnet.

- *D: Qual è la differenza tra SQS Standard e SQS FIFO e quando è obbligatorio usare FIFO?*
  - **R**: SQS Standard offre throughput quasi illimitato ma garantisce solo la consegna *At-least-once* (possibili duplicati) e un ordinamento "best-effort". SQS FIFO garantisce l'ordinamento rigoroso dei messaggi e la consegna *Exactly-once* tramite deduplica automatica su 5 minuti, con un throughput massimo limitato (300 o 3000 msg/sec con batching). Nei sistemi di pagamento e contabili, SQS FIFO è obbligatorio per flussi in cui l'ordine cronologico è vitale (es. sequenza: `AUTHORIZED` $\to$ `CAPTURED` $\to$ `SETTLED`) e dove duplicare un messaggio causerebbe addebiti doppi.

- *D: Come gestisci il file di stato (`terraform.tfstate`) in un team enterprise con pipeline CI/CD?*
  - **R**: Il file di stato non deve mai essere salvato nel repository Git (perché contiene dati sensibili e porta a disallineamenti). Si configura un **Remote Backend** su un bucket **Amazon S3** con versioning abilitato e cifratura server-side (SSE-KMS), abbinato a un meccanismo di **State Locking** tramite tabella **DynamoDB**. In questo modo, quando una pipeline CI/CD o uno sviluppatore esegue `terraform plan/apply`, viene acquisito un lock esclusivo che impedisce esecuzioni concorrenti distruttive.



################################################################################
### CAPITOLO: 20. Dependency Management (Maven e Gradle)
################################################################################

# 20. Dependency Management (Maven e Gradle)

### Cos'è e perché conta
La gestione delle dipendenze, del ciclo di vita di compilazione e della risoluzione dei conflitti tra librerie (Jar Hell) è fondamentale in progetti enterprise complessi e multi-modulo. Sapere come Maven e Gradle risolvono i grafi delle dipendenze, come gestire i BOM (Bill of Materials) e come isolare gli scope è una competenza chiave per un Senior Developer.

---

### Cosa studiare

#### 1. Apache Maven: Fondamenti e Architettura

##### A. Il Modello a Coordinate (GAV)
Ogni artefatto Maven è identificato univocamente da una terna **GAV**:
- `groupId`: package namespace univoco dell'organizzazione (es. `org.springframework.boot`, `com.nexi.payments`).
- `artifactId`: nome del modulo/progetto (es. `payment-core`, `spring-boot-starter-web`).
- `version`: versione semantica (es. `3.2.4`, `1.0.0-SNAPSHOT`).

##### B. Il Build Lifecycle di Maven
Maven definisce tre cicli di vita standard: `default` (compilazione e rilascio), `clean` (pulizia della directory `target`) e `site` (generazione documentazione).

Fasi ordinate del ciclo **`default`**:
1. `validate`: convalida la correttezza del `pom.xml` e la disponibilità di tutte le informazioni.
2. `compile`: compila il codice sorgente in `src/main/java` dentro `target/classes`.
3. `test`: esegue i test unitari (Surefire plugin) in `src/test/java` senza fare il package.
4. `package`: impacchetta il codice compilato nel formato di distribuzione (`jar`, `war`) in `target/`.
5. `verify`: esegue i test di integrazione (Failsafe plugin) e controlli di qualità/SAST.
6. `install`: copia l'artefatto nel repository Maven locale (`~/.m2/repository`).
7. `deploy`: invia l'artefatto definitivo al repository manager remoto aziendale (Nexus / Artifactory).

##### C. Gli Scope delle Dipendenze Maven
- **`compile`** (default): disponibile in compilazione, test e runtime; viene inclusa nel pacchetto finale (JAR) e propagata ai progetti a valle.
- **`provided`**: necessaria per compilare e testare, ma non inclusa nel pacchetto finale perché fornita dal container a runtime (es. `jakarta.servlet-api`, `lombok`).
- **`runtime`**: necessaria solo per l'esecuzione, non per la compilazione (es. driver JDBC `com.oracle.database.jdbc:ojdbc8`).
- **`test`**: necessaria solo per compilare ed eseguire i test (es. `junit-jupiter`, `mockito-core`, `testcontainers`). Non viene inclusa nel JAR finale.
- **`import`**: utilizzabile solo all'interno di `<dependencyManagement>` con tipo `pom`, per importare un BOM (Bill of Materials).

##### D. Transitive Dependencies e Risoluzione dei Conflitti
Quando il progetto dipende da `Lib A` che a sua volta dipende da `Lib C:1.0`, e da `Lib B` che dipende da `Lib C:2.0`:
- **Regola di Maven "Nearest Definition" (Più vicino nell'albero)**: Maven sceglie la versione della dipendenza che si trova al livello di profondità minore nell'albero delle dipendenze. Se sono alla stessa profondità, vince la prima dichiarata nel `pom.xml`.
- **Esclusioni esplicite**:
  ```xml
  <dependency>
      <groupId>com.example</groupId>
      <artifactId>legacy-service</artifactId>
      <version>1.0.0</version>
      <exclusions>
          <exclusion>
              <groupId>commons-logging</groupId>
              <artifactId>commons-logging</artifactId>
          </exclusion>
      </exclusions>
  </dependency>
  ```
- **Analisi dell'albero delle dipendenze**:
  ```bash
  mvn dependency:tree -Dverbose -Dincludes=commons-logging
  ```

##### E. `<dependencyManagement>` vs `<dependencies>` e i BOM (Bill of Materials)
- `<dependencies>`: dichiara e scarica effettivamente le dipendenze nel modulo corrente.
- `<dependencyManagement>`: definisce centralmente le **versioni** e le configurazioni delle librerie per tutti i moduli figli, senza forzarne l'inclusione finché un sottomodulo non la dichiara in `<dependencies>` (senza specificare il tag `<version>`).
- **BOM di Spring Boot o Spring Cloud**:
  ```xml
  <dependencyManagement>
      <dependencies>
          <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-dependencies</artifactId>
              <version>3.2.4</version>
              <type>pom</type>
              <scope>import</scope>
          </dependency>
      </dependencies>
  </dependencyManagement>
  ```

---

#### 2. Gradle: Caratteristiche e Confronto con Maven

- **Modello Basato su DAG (Directed Acyclic Graph)**:
  - Anziché un ciclo di vita rigido a fasi fisse come Maven, Gradle modella la build come un grafo orientato aciclico di **Tasks** con dipendenze esplicite (`dependsOn`).
- **Linguaggio di Build**: basato su Kotlin DSL (`build.gradle.kts`) o Groovy DSL (`build.gradle`), offrendo piena programmabilità.
- **Configurazioni delle Dipendenze in Gradle**:
  - `implementation`: la dipendenza è interna al modulo e non viene esposta ai moduli che dipendono da esso (migliora drasticamente i tempi di ricompilazione incrementale).
  - `api`: la dipendenza viene esportata ai consumatori del modulo.
  - `compileOnly`: analogo a `provided` di Maven.
  - `runtimeOnly`: analogo a `runtime` di Maven.
  - `testImplementation`: analogo a `test` di Maven.
- **Performance e Caching**:
  - **Build Daemon**: processo in background sempre attivo per evitare il cold start della JVM.
  - **Incremental Builds**: esegue solo i task i cui input/output sono cambiati (`UP-TO-DATE`).
  - **Build Cache**: condivisione dei binari compilati tra sviluppatori e pipeline CI/CD.

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Come risolvi un conflitto di versioni transitivo in Maven (Jar Hell)?*
  - **R**: Eseguo il comando `mvn dependency:tree -Dverbose` per individuare quale dipendenza sta portando la versione obsoleta o in conflitto. Per risolverlo in modo pulito posso: (1) dichiarare esplicitamente la versione corretta all'interno del blocco `<dependencyManagement>`, oppure (2) aggiungere un tag `<exclusion>` nella dipendenza che trascina la versione indesiderata.

- *D: Qual è la differenza tra `implementation` e `api` in Gradle?*
  - **R**: `implementation` nasconde le dipendenze transitive ai moduli a valle, evitando di "inquinare" il loro classpath di compilazione. Questo significa che se cambio un'implementazione interna in un modulo, Gradle non deve ricompilare tutti i progetti che dipendono da esso, riducendo sensibilmente i tempi di build. `api` espone invece la dipendenza pubblicamente.

- *D: A cosa serve il file `mvnw` (Maven Wrapper) / `gradlew` (Gradle Wrapper) presente nei repository?*
  - **R**: Il Wrapper è uno script shell che scarica e utilizza automaticamente la versione esatta di Maven/Gradle specificata nel progetto (`.mvn/wrapper/maven-wrapper.properties`). Garantisce che tutti gli sviluppatori del team e i server di CI/CD compilino il software esattamente con la stessa identica versione del build tool, eliminando il problema "funziona sulla mia macchina".

---

### Come esercitarti
1. **Analisi dipendenze**: crea un `pom.xml` con Spring Boot e aggiungi due librerie con versioni discordanti di Jackson; usa `mvn dependency:tree` per verificare quale versione viene selezionata e forza la versione corretta con `<dependencyManagement>`.



################################################################################
### CAPITOLO: 21. Git e Branching Strategies
################################################################################

# 21. Git e Branching Strategies

### Cos'è e perché conta
Nei team di sviluppo enterprise e nei sistemi mission-critical (come i pagamenti), Git non è solo un sistema di version control, ma la spina dorsale della collaborazione, del rilascio controllato e della tracciabilità delle modifiche (fondamentale per audit bancari e compliance PCI-DSS). A un profilo Senior viene richiesta padronanza dei comandi avanzati, capacità di risolvere conflitti complessi e comprensione profonda dei flussi di branching.

---

### Cosa studiare

#### 1. Architettura e Modello Interno di Git
- **I 4 oggetti fondamentali** (memorizzati nel database a oggetti content-addressable `.git/objects` tramite hash SHA-1/SHA-256):
  1. **Blob**: memorizza il contenuto puro dei file (senza metadati né nome file).
  2. **Tree**: memorizza la struttura delle directory, associando i nomi dei file ai rispettivi hash dei blob o di altri sotto-alberi.
  3. **Commit**: punta a un root tree e contiene metadati (autore, committer, timestamp, messaggio) e uno o più puntatori ai commit genitori (*parents*).
  4. **Annotated Tag**: puntatore immutabile a uno specifico commit, con messaggio e firma PGP.
- **I 3 stadi dell'albero di lavoro**:
  - *Working Directory*: i file effettivi modificati su disco.
  - *Staging Area (Index)*: snapshot preparato per il prossimo commit (`git add`).
  - *Repository (`.git`)*: storico immutabile dei commit.
  - *HEAD*: puntatore simbolico al branch attualmente estratto o a uno specifico commit (*detached HEAD*).

---

#### 2. Strategie di Branching Enterprise

```
[Trunk-Based]  ──●───●───●───●───●───●───► main (Deploy continui, feature flag)
                  \     /
                   ●───● (Short-lived branch, < 1-2 giorni)

[GitFlow]      main ──●────────────────────────● (Release tag v1.0.0)
                       \                      /
               develop ─●───●───●───●────────●
                             \     /
                              ●───● (feature/payment-routing)
```

- **Trunk-Based Development (Standard moderno nei Microservizi)**:
  - Tutti gli sviluppatori effettuano il merge su `main`/`master` frequentemente (almeno una volta al giorno) tramite branch a vita brevissima (*short-lived branches*).
  - Previene "merge hell" e conflitti titanici.
  - Richiede forte automazione CI/CD e l'uso di **Feature Flags** (Toggles) per disabilitare funzionalità incomplete in produzione.
- **GitFlow (Tradizionale / Ambienti a rilascio cadenzato)**:
  - `main`: codice sempre in produzione con tag di versione.
  - `develop`: ramo di integrazione per il prossimo rilascio.
  - `feature/*`: sviluppo nuove funzionalità, staccate da `develop`.
  - `release/*`: stabilizzazione, bug fix minori e preparazione documentazione prima del merge su `main` e `develop`.
  - `hotfix/*`: correzioni critiche urgenti staccate direttamente da `main` e reintegrate sia su `main` che su `develop`.
- **GitHub Flow / GitLab Flow**:
  - Più snelli di GitFlow: `main` protetto + feature branches + Pull/Merge Request con review obbligatoria e CI verde prima del merge.

---

#### 3. Comandi Avanzati e Operazioni Critiche

##### A. Rebase vs Merge
- **`git merge <branch>`**: crea un commit di merge esplicito con due genitori (*non-fast-forward* per default su PR). Mantiene la cronologia fedele ma non lineare.
- **`git rebase <target>`**: "sposta" i commit correnti in cima al target, riscrivendo la storia dei commit (nuovi hash SHA). Crea una cronologia perfettamente lineare.
- **`git rebase -i HEAD~N` (Rebase interattivo)**: fondamentale prima di aprire una PR per fare *squash* (fondere commit temporanei "wip", "fix typo" in commit atomici e descrittivi), *reword* (modificare messaggi), o riordinare i commit.
- **Regola d'oro del Rebase**: **mai fare rebase di commit già pubblicati su branch condivisi/pubblici** (es. `main` o `develop`), perché altera gli hash e corrompe lo storico degli altri colleghi.

##### B. Reset vs Revert
- **`git reset`** (modifica la storia locale, arretra il puntatore del branch):
  - `--soft`: sposta `HEAD` indietro; lascia le modifiche nella Staging Area.
  - `--mixed` (default): sposta `HEAD`; lascia le modifiche nella Working Directory (un-staged).
  - `--hard`: distrugge tutte le modifiche sia in Staging che in Working Directory (pericoloso).
- **`git revert <commit_hash>`**: crea un **nuovo commit opposto** che annulla gli effetti del commit indicato. È l'unico modo sicuro per annullare modifiche già pushate su un branch remoto condiviso.

##### C. Cherry-pick, Stash & Bisect
- **`git cherry-pick <commit_hash>`**: applica un singolo specifico commit da un altro branch sul branch corrente (es. portare un bugfix urgente da una release successiva a una legacy).
- **`git stash` / `git stash pop`**: salva temporaneamente le modifiche non committate per liberare la working tree (utile quando bisogna cambiare branch d'urgenza per un hotfix).
- **`git bisect`**: algoritmo di ricerca binaria nello storico dei commit per individuare con precisione chirurgica quale commit ha introdotto una regressione o un bug (`git bisect start`, `git bisect bad`, `git bisect good <commit_vecchio>`).

---

#### 4. Best Practice, Conventional Commits e Sicurezza
- **Conventional Commits**: convenzione per messaggi di commit leggibili e automazione del changelog:
  - `feat(payment): add 3DS2 biometric authentication support`
  - `fix(reconciliation): prevent duplicate transaction entry on retry`
  - `refactor(core): extract currency conversion to dedicated service`
  - `test(auth): add parameterized tests for expired token scenarios`
- **Sicurezza del Repository**:
  - File `.gitignore` rigoroso: mai versionare file `.env`, file di configurazione con password in chiaro, certificati `.p12`/`.pem` o directory `.idea`/`target`.
  - **Git Pre-commit Hooks** (es. con Husky / Gitleaks): scansione automatica per bloccare il commit di segreti (token AWS, chiavi private, credenziali DB).

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Qual è la differenza tra `git rebase` e `git merge` e quando preferisci l'uno o l'altro?*
  - **R**: `git merge` unisce i rami preservando la cronologia esatta con un commit di merge, ma può rendere l'albero della storia disordinato. `git rebase` riscrive la storia applicando i propri commit sopra la punta del branch target, creando una cronologia lineare e pulita. La best practice consiste nell'utilizzare `rebase` sul proprio feature branch locale per allinearsi a `main` ed effettuare lo squash prima della PR, mentre si utilizza `merge` (o Squash & Merge) per integrare la PR nel branch principale.

- *D: Hai pushato per errore un commit con un bug in produzione su `main`. Come intervieni?*
  - **R**: Eseguo immediatamente un `git revert <commit_hash>` e pusho il commit di rollback. Non uso mai `git reset --hard` con force push su `main`, perché riscriverebbe la storia di un branch pubblico condiviso, rompendo i repository dei colleghi e i runner di CI/CD.

- *D: Cos'è il comando `git reflog` e quando ti ha salvato?*
  - **R**: Il `reflog` (reference log) tiene traccia di ogni singolo spostamento di `HEAD` sul computer locale, anche dopo operazioni distruttive come `git reset --hard` o eliminazione accidentale di branch. Permette di recuperare lo SHA di commit che sono diventati orfani ("dangling") prima che vengano ripuliti dal garbage collector di Git.

---

### Come esercitarti
1. **Esercizio di Rebase interattivo**: crea un branch di prova, fai 4 commit fittizi, poi usa `git rebase -i HEAD~4` per fondere i commit intermedi in uno solo (*squash*) e cambiare il messaggio del primo commit.
2. **Simulazione di Merge Conflict**: modifica la stessa riga di un file su due branch diversi, tenta il merge e risolvi il conflitto manualmente esaminando i marker `<<<<<<<`, `=======`, `>>>>>>>`.



################################################################################
### CAPITOLO: 22. Toolchain (Eclipse, Git, Maven, JUnit, Jenkins, Nexus)
################################################################################

# 22. Toolchain (Eclipse, Git, Maven, JUnit, Jenkins, Nexus)

### Cos'è e perché conta
Meno peso tecnico ma segnala autonomia operativa — in un contesto enterprise regolamentato, il processo di rilascio è spesso rigido e vogliono sapere che ti inserisci senza frizioni.

### Cosa studiare

- **Eclipse IDE**: se lavori principalmente con IntelliJ, rinfresca le scorciatoie base (refactor, debug, gestione workspace/progetti Maven) — non serve diventare esperto, basta non essere spiazzato
- **Git**: flussi di branching enterprise (Git Flow o simili), rebase vs merge, gestione conflitti — spesso chiedono "come gestisci un conflitto di merge" più che comandi esotici
- **Maven**: struttura di un `pom.xml`, gestione dipendenze e scope (`compile`, `test`, `provided`), lifecycle (`validate`, `compile`, `test`, `package`, `install`, `deploy`)
- **JUnit**: differenza tra unit test e integration test, uso di Mockito per il mocking, test parametrizzati (già nel tuo bagaglio recente)
- **Jenkins**: concetto di pipeline (dichiarativa vs scripted), stage tipici (build, test, quality gate, deploy) — non serve saperci scrivere una pipeline complessa, ma capire cosa fa un job CI/CD
- **Nexus**: repository manager per artifact Maven/npm — sapere a cosa serve (versioning, cache di dipendenze, distribuzione interna di librerie)

### Come esercitarti
Se non hai mai usato Jenkins/Nexus in prima persona, guarda un video introduttivo di 10 minuti su ciascuno: l'obiettivo è poter dire "ho capito il concetto anche se non l'ho usato quotidianamente", che è una risposta onesta e accettabile.



################################################################################
### CAPITOLO: 23. Unit Testing e Test Automation (JUnit 5, Mockito, Testcontainers)
################################################################################

# 23. Unit Testing e Test Automation (JUnit 5, Mockito, Testcontainers)

### Cos'è e perché conta
Nei sistemi transazionali finanziari, una regressione non identificata in fase di test può causare ammanchi economici o disservizi legali critici. Un Senior Backend Developer deve saper padroneggiare la **piramide dei test**, scrivere test unitari veloci e deterministici con **JUnit 5 & Mockito**, ed eseguire integration test affidabili su database e message broker reali tramite **Testcontainers**.

---

### Cosa studiare

#### 1. La Piramide dei Test e Strategia di Test

```
        / \
       / E2E \        (Pochi, lenti, costosi, testano flussi utente completi)
      /───────\
     / Integr. \      (Medi, testano interazione tra moduli, DB reale, Testcontainers)
    /───────────\
   / Unit Tests  \    (Migliaia, isolati, velocissimi < ms, mock delle dipendenze)
  /───────────────\
```

- **Unit Test**: testano una singola classe/metodo in totale isolamento. Tutte le dipendenze esterne (altri Service, Repository, Web Client) vengono simulate con mock.
- **Integration Test**: verificano che più componenti lavorino correttamente insieme (es. test di un repository JPA contro un database reale, serializzazione JSON, controller HTTP).
- **End-to-End (E2E) Test**: testano l'intero sistema distribuito da endpoint a database/code.

---

#### 2. JUnit 5 (Jupiter): Lifecycle e Funzionalità Avanzate

- **Annotazioni di Lifecycle**:
  - `@BeforeAll` / `@AfterAll`: eseguiti una sola volta prima/dopo tutti i test della classe (metodi `static` per default).
  - `@BeforeEach` / `@AfterEach`: eseguiti prima/dopo ogni singolo metodo di test (ideali per resettare mock e stato).
  - `@Test`: definisce un metodo di test.
  - `@DisplayName`: nome descrittivo leggibile per i report di test.
- **Asserzioni JUnit 5 & AssertJ**:
  - JUnit 5 standard: `assertEquals(expected, actual)`, `assertThrows(InsufficientFundsException.class, () -> service.pay(...))`.
  - **AssertJ** (Fluent API, standard de facto per leggibilità):
    ```java
    assertThat(payment.getStatus()).isEqualTo(PaymentStatus.COMPLETED);
    assertThat(payment.getAmount()).isGreaterThan(BigDecimal.ZERO);
    assertThat(payment.getTransactions())
        .hasSize(2)
        .extracting(Transaction::getCurrency)
        .containsExactly("EUR", "USD");
    ```
- **Test Parametrici (`@ParameterizedTest`)**:
  - Consentono di eseguire lo stesso test con dataset differenti, fondamentale per verificare casi limite finanziari (algoritmi di arrotondamento, validazione carte, BIN):
  ```java
  @ParameterizedTest
  @ValueSource(strings = {"4111111111111111", "5500000000000004", "378282246310005"})
  void shouldValidateValidCardNumbers(String pan) {
      assertThat(cardValidator.isValidPan(pan)).isTrue();
  }

  @ParameterizedTest
  @CsvSource({
      "100.00, EUR, 2.00",
      "50.00, USD, 1.50",
      "0.00, EUR, 0.00"
  })
  void shouldCalculateCorrectFee(BigDecimal amount, String currency, BigDecimal expectedFee) {
      BigDecimal fee = feeCalculator.calculate(amount, currency);
      assertThat(fee).isEqualByComparingTo(expectedFee);
  }
  ```

---

#### 3. Mocking con Mockito

- **Annotazioni Principali**:
  - `@ExtendWith(MockitoExtension.class)`: abilita Mockito in JUnit 5 senza avviare il contesto Spring.
  - `@Mock`: crea un'istanza fittizia di una dipendenza (tutti i metodi ritornano valori di default: null, 0, false).
  - `@InjectMocks`: crea l'istanza della classe sotto test, iniettando automaticamente i mock creati nei campi/costruttore.
  - `@Spy`: crea un wrapper su un'istanza reale, permettendo di intercettare o fare override solo di alcuni metodi (*partial mock*).
- **Stubbing (`when ... thenReturn / thenThrow`)**:
  ```java
  when(accountRepository.findById(123L)).thenReturn(Optional.of(testAccount));
  when(acquirerGateway.authorize(any())).thenThrow(new GatewayTimeoutException("Timeout"));
  ```
- **Verifica delle Interazioni (`verify`)**:
  ```java
  // Verifica che il metodo debit() sia stato chiamato esattamente 1 volta con il parametro specificato
  verify(accountRepository, times(1)).save(testAccount);
  verify(notificationService, never()).sendAlert(any());
  ```
- **Cattura di Parametri (`ArgumentCaptor`)**:
  - Ispeziona gli oggetti passati ai mock per validarne i campi interni:
  ```java
  ArgumentCaptor<PaymentEvent> eventCaptor = ArgumentCaptor.forClass(PaymentEvent.class);
  verify(eventPublisher).publish(eventCaptor.capture());
  PaymentEvent capturedEvent = eventCaptor.getValue();
  assertThat(capturedEvent.getAmount()).isEqualTo(new BigDecimal("100.00"));
  ```

---

#### 4. Slice Testing in Spring Boot

Anziché avviare l'intero `@SpringBootTest` (che carica tutti i bean ed è lento), Spring Boot permette di caricare solo la "fetta" (*slice*) di applicazione necessaria:

##### A. `@WebMvcTest` (Test del Controller Layer)
- Carica solo controller, filtri, advice e security; mocka il layer di servizio con `@MockBean`:
```java
@WebMvcTest(PaymentController.class)
class PaymentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PaymentService paymentService;

    @Test
    void shouldReturn201WhenPaymentCreated() throws Exception {
        when(paymentService.processPayment(any())).thenReturn("pay_123");

        mockMvc.perform(post("/api/v1/payments")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"amount\": 100.00, \"currency\": \"EUR\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value("pay_123"));
    }
}
```

##### B. `@DataJpaTest` (Test del Repository Layer)
- Configura solo `EntityManager`, Spring Data JPA e un database (in-memory o reale via Testcontainers), eseguendo ogni test all'interno di una transazione con rollback automatico alla fine del test.

---

#### 5. Integration Testing Moderno con Testcontainers

- **Il problema dei DB in-memory (H2)**: H2 ha una sintassi SQL, lock, tipi di dati e funzioni proprietarie diverse da Oracle o PostgreSQL. I test passano su H2 ma falliscono in produzione su Oracle.
- **La Soluzione Testcontainers**: libreria Java che avvia container Docker reali e isolati (Oracle XE, PostgreSQL, Kafka, Redis) durante l'esecuzione dei test di integrazione (`mvn verify`).
- **Configurazione con `@ServiceConnection` (Spring Boot 3.1+)**:
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class PaymentIntegrationTest {

    @Container
    @ServiceConnection // Configura automaticamente datasource url, user e password di Spring
    static OracleContainer oracle = new OracleContainer("gvenzl/oracle-xe:21-slim-faststart");

    @Container
    @ServiceConnection
    static KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.4.0"));

    @Autowired
    private PaymentRepository paymentRepository;

    @Test
    void shouldPersistTransactionOnRealOracleDatabase() {
        Payment payment = new Payment("tx_01", new BigDecimal("50.00"), "EUR");
        paymentRepository.save(payment);

        assertThat(paymentRepository.findById("tx_01")).isPresent();
    }
}
```

---

#### 6. TDD (Test-Driven Development) & BDD (Behavior-Driven Development)
- **Ciclo Red-Green-Refactor**:
  1. *Red*: scrivi un test unitario che definisce il comportamento atteso prima del codice (il test fallisce).
  2. *Green*: scrivi il codice minimo necessario per far passare il test.
  3. *Refactor*: ripulisci il codice eliminando duplicazioni e migliorando il design, mantenendo i test sempre verdi.
- **Struttura BDD Given-When-Then**:
  - *Given* (Dato un contesto/stato iniziale: conto con saldo 100€).
  - *When* (Quando avviene un'azione: richiesta di prelievo di 30€).
  - *Then* (Allora si verifica il risultato: saldo aggiornato a 70€ e transazione memorizzata).

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Qual è la differenza tra `@Mock` e `@MockBean`?*
  - **R**: `@Mock` appartiene a Mockito puro e viene istanziato velocemente senza alcun contesto Spring. `@MockBean` è un'annotazione di Spring Boot Test che crea un mock Mockito e lo registra all'interno dell'**ApplicationContext di Spring**, sostituendo qualsiasi bean reale dello stesso tipo; è necessario per i test di integrazione o slice test (`@WebMvcTest`).

- *D: Perché oggi si preferisce Testcontainers a un database in-memory come H2 per i test di integrazione?*
  - **R**: Perché H2 non replica fedelmente il comportamento, le funzioni proprietarie (es. PL/SQL, sequenze, JSON functions), i livelli di isolamento e la concorrenza di un DBMS di produzione come Oracle o PostgreSQL. Testcontainers esegue il vero motore di database in un container Docker usa-e-getta, garantendo test di integrazione affidabili al 100% senza falsi positivi.

- *D: Come testi un metodo asincrono o un listener Kafka?*
  - **R**: Utilizzando la libreria **Awaitility** (`await().atMost(5, SECONDS).untilAsserted(() -> assertThat(...))`), che effettua un polling non-bloccante fino a quando la condizione o l'evento asincrono non viene soddisfatto, evitando l'uso deprecato di `Thread.sleep()`.

---

### Come esercitarti
1. **Scrittura Test Unitario Isolato**: scrivi una classe di test per un `ReconciliationService` usando JUnit 5, `@ExtendWith(MockitoExtension.class)`, `@Mock`, `@InjectMocks`, simulando la risposta di un repository con `when` e verificando le interazioni con `verify` e `ArgumentCaptor`.



################################################################################
### CAPITOLO: 24. SAST e Qualità del Software (SonarQube)
################################################################################

# 24. SAST e Qualità del Software (SonarQube)

### Cos'è e perché conta
In ambienti finanziari e di pagamento soggetti a regolamentazioni stringenti (PCI-DSS, PSD2, standard bancari ISO 27001), la qualità del codice e la sicurezza applicativa non sono opzionali. Il **SAST (Static Application Security Testing)** con strumenti come **SonarQube** permette di individuare bug, vulnerabilità di sicurezza, falle crittografiche e debito tecnico automaticamente all'interno delle pipeline di CI/CD, prima ancora che il codice arrivi in ambiente di test.

---

### Cosa studiare

#### 1. Tipologie di Security Testing: SAST vs DAST vs IAST vs SCA

| Metodologia | Definizione | Modalità | Quando si esegue | Cosa trova |
|---|---|---|---|---|
| **SAST** (SonarQube, Checkmarx) | Static Application Security Testing | White-box (analizza il codice sorgente/bytecode senza eseguirlo) | In fase di Build / CI (Pull Request) | SQL Injection, hardcoded secrets, NPE, cattiva crittografia, violazioni di stile |
| **SCA** (OWASP Dependency-Check, Snyk, Dependabot) | Software Composition Analysis | Analizza le librerie terze nel `pom.xml` / `build.gradle` | In fase di Build / CI | CVE note in dipendenze esterne (es. vulnerabilità in Spring, Log4j, Jackson) |
| **DAST** (OWASP ZAP, Burp Suite) | Dynamic Application Security Testing | Black-box (analizza l'applicazione in esecuzione dall'esterno) | In ambienti Staging / QA | XSS a runtime, misconfigurazioni TLS/SSL, header HTTP insicuri, broken auth |
| **IAST** | Interactive Application Security Testing | Gray-box (agente interno all'app durante test funzionali) | In esecuzione durante integration test | Combinazione di vulnerabilità interne e comportamenti runtime |

---

#### 2. Concetti Chiave di SonarQube

```
┌────────────────────────────────────────────────────────────────────────┐
│                          SONARQUBE ANALYSIS                            │
├────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────────┐  ┌────────────────────┐  │
│  │       BUGS        │  │  VULNERABILITIES  │  │    CODE SMELLS     │  │
│  │ (Errori logici e  │  │ (Falle di sicu-   │  │ (Debito tecnico e  │  │
│  │  rischi runtime)  │  │  rezza sfruttabili│  │  scarsa manutenib.)│  │
│  └───────────────────┘  └───────────────────┘  └────────────────────┘  │
│  ┌───────────────────┐  ┌───────────────────┐  ┌────────────────────┐  │
│  │ SECURITY HOTSPOTS │  │   CODE COVERAGE   │  │   DUPLICATIONS     │  │
│  │ (Codice critico   │  │ (Percentuale test │  │ (Codice duplicato  │  │
│  │  da revisionare)  │  │  unitari / JaCoCo)│  │  copia-incolla)    │  │
│  └───────────────────┘  └───────────────────┘  └────────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │    QUALITY GATE     │
                         │   [PASSED / FAILED] │ ──► Blocca la Pipeline CI
                         └─────────────────────┘
```

##### A. Le Categorie di Issues in SonarQube
1. **Bugs**: codice errato o che causerà sicuramente anomalie a runtime (es. `NullPointerException`, risorse non chiuse/leak di connessioni DB, race conditions).
2. **Vulnerabilities**: falle di sicurezza concrete che espongono il sistema ad attacchi (es. concatenazione SQL non parametrizzata, log di dati sensibili/PAN in chiaro, uso di cifrari deboli come DES o MD5).
3. **Security Hotspots**: punti di codice che toccano aree sensibili dal punto di vista della sicurezza (es. configurazione CORS permissiva, generazione di numeri casuali, hashing di password), che richiedono una **revisione umana esplicita** per verificare che il contesto sia sicuro.
4. **Code Smells**: problemi di manutenibilità, leggibilità e debito tecnico (es. metodi troppo lunghi, classi con troppe responsabilità, complessità ciclomatica elevata, parametri non utilizzati).

##### B. Metriche Fondamentali
- **Complessità Ciclomatica (Cyclomatic Complexity)**: misura il numero di cammini linearmente indipendenti nel codice (calcolata in base a `if`, `for`, `while`, `case`, operatori logici `&&`, `||`). Un valore alto indica codice difficile da testare e manutenere.
- **Complessità Cognitiva (Cognitive Complexity)**: misura quanto sia difficile per un essere umano comprendere il flusso del codice (penalizza maggiormente i cicli o blocchi annidati).
- **Code Coverage (con JaCoCo)**: percentuale di linee e branch coperti dai test unitari e di integrazione. In genere il Quality Gate impone almeno l'80% di coverage sul **nuovo codice** (*Clean as You Go*).
- **Duplicated Lines Density**: percentuale di righe di codice duplicate che dovrebbero essere refattorizzate.

##### C. Il Quality Gate (Cancello di Qualità)
È un insieme di condizioni booleane che il codice deve superare per essere considerato idoneo al rilascio o al merge della Pull Request.
- **Politica "Clean as You Go"**: focalizzarsi sul codice modificato/aggiunto nella PR (*New Code*), bloccando la build se:
  - 0 Nuove Vulnerability
  - 0 Nuovi Bug
  - Security Rating = `A` (nessuna vulnerabilità aperta)
  - Code Coverage sul nuovo codice $\ge 80\%$
  - Duplicazioni sul nuovo codice $< 3\%$
  - 100% dei Security Hotspots revisionati

---

#### 3. OWASP Top 10 e Regole Critiche SonarQube per Java Backend

- **Injection (A03:2021)**:
  - *Problema*: concatenare stringhe in query SQL/JPQL (`"SELECT * FROM accounts WHERE id = " + inputId`).
  - *Regola Sonar*: S2077 / S3649 (uso obbligatorio di `PreparedStatement` o parameterized queries in Spring Data `@Param`).
- **Cryptographic Failures (A02:2021)**:
  - *Problema*: uso di MD5/SHA-1 per hashing o `DES`/`AES/ECB` per cifratura dati carta.
  - *Regola Sonar*: S4790 (uso obbligatorio di algoritmi robusti: `AES/GCM/NoPadding`, `BCrypt`/`Argon2` per password).
- **Insecure Randomness**:
  - *Problema*: uso di `java.util.Random` o `Math.random()` per token di autenticazione o codici OTP.
  - *Regola Sonar*: S2245 (uso obbligatorio di `java.security.SecureRandom`).
- **Sensitive Data Exposure / Logging**:
  - *Problema*: stampare nei log tramite Logback/Log4j2 oggetti contenenti PAN di carte di credito o CVV.
  - *Regola*: mascheramento dati (pattern masking nei log: `4111-XXXX-XXXX-1111`) e annotazioni custom `@ToString.Exclude` o record con `toString()` oscurato.
- **Resource Leaks**:
  - *Problema*: mancata chiusura di connessioni `Connection`, `ResultSet`, `InputStream`.
  - *Regola*: uso obbligatorio del `try-with-resources` (Java 7+).

---

#### 4. Integrazione di SonarQube nella Pipeline CI/CD

Nel file di build (`pom.xml`) tramite il plugin Sonar Maven:

```xml
<plugin>
    <groupId>org.sonarsource.scanner.maven</groupId>
    <artifactId>sonar-maven-plugin</artifactId>
    <version>3.10.0.2594</version>
</plugin>
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
                <goal>report</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

Comando di esecuzione in pipeline Jenkins / GitLab CI:
```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=payment-service \
  -Dsonar.host.url=https://sonarqube.internal.bank \
  -Dsonar.token=$SONAR_TOKEN \
  -Dsonar.qualitygate.wait=true
```
*(Il flag `-Dsonar.qualitygate.wait=true` fa attendere a Maven l'esito dell'analisi; se il Quality Gate fallisce, la pipeline si interrompe immediatamente bloccando il merge).*

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Come utilizzi SonarQube nel tuo flusso di lavoro quotidiano?*
  - **R**: Utilizzo il plugin **SonarLint** direttamente nell'IDE per ricevere feedback istantaneo mentre scrivo codice (*shift-left testing*), prevenendo code smell e falle prima del commit. Nella pipeline CI/CD di GitLab/Jenkins, ad ogni Pull Request viene eseguita l'analisi con SonarScanner e generato il report di copertura JaCoCo; la PR non può essere approvata né unita al branch principale se il Quality Gate fallisce.

- *D: Che differenza c'è tra una Vulnerability e un Security Hotspot in SonarQube?*
  - **R**: Una **Vulnerability** è una falla di sicurezza accertata nel codice che va corretta immediatamente (es. una SQL injection o una risorsa non chiusa). Un **Security Hotspot** evidenzia codice che fa uso di funzioni sensibili per la sicurezza (es. generazione di numeri random, upload di file, cookie HTTP) la cui pericolosità dipende dal contesto architetturale: richiede che uno sviluppatore o security champion analizzi il codice e lo marchi esplicitamente come "Safe" o lo converta in bug/fix.

- *D: Come convinci un team a rispettare la metrica del Quality Gate senza rallentare le consegne?*
  - **R**: Adottando la strategia **Clean as You Go**: non si blocca il team per sanare migliaia di righe di debito tecnico legacy pregresso, ma si impone il Quality Gate rigido esclusivamente sul **nuovo codice o codice modificato nella PR** (nuove righe con 0 vulnerabilità e coverage $\ge 80\%$). In questo modo la qualità complessiva della codebase migliora gradualmente a ogni rilascio senza arrestare il business.

---

### Come esercitarti
1. **Analisi di vulnerabilità**: scrivi un metodo Java con un'evidente falla di concatenazione SQL e un uso improprio di `Math.random()`, poi rifattorizzalo applicando `PreparedStatement` e `SecureRandom` per renderlo conforme alle regole Sonar.
2. **Configurazione JaCoCo**: verifica come impostare nel `pom.xml` una regola di esclusione per DTO, Record e classi di configurazione Spring in modo che non falsino le percentuali di Code Coverage complessive.



################################################################################
### CAPITOLO: 25. CI-CD e Release Management (Jenkins, GitLab CI, Nexus)
################################################################################

# 25. CI-CD e Release Management (Jenkins, GitLab CI, Nexus)

### Cos'è e perché conta
In ambienti ad alta affidabilità come i pagamenti digitali, il processo che porta il codice dal repository Git alla produzione deve essere completamente automatizzato, ripetibile e tracciabile. Il paradigma **CI/CD (Continuous Integration / Continuous Delivery & Deployment)** azzera l'errore umano, garantisce che ogni commit superi controlli di qualità e test automatici, e permette rilasci frequenti e a zero downtime.

---

### Cosa studiare

#### 1. I Concetti Fondamentali: CI vs CD

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTINUOUS INTEGRATION (CI)              │
│  [Code / Git] ──► [Build] ──► [Unit Test] ──► [SAST / Sonar]│
└──────────────────────────────┬──────────────────────────────┘
                               │ (Artifact generato: JAR/Image)
┌──────────────────────────────▼──────────────────────────────┐
│                    CONTINUOUS DELIVERY (CD)                 │
│  [Integration Test] ──► [Nexus/Registry] ──► [Deploy Staging]
└──────────────────────────────┬──────────────────────────────┘
                               │ (Approvazione Manuale / Gate)
┌──────────────────────────────▼──────────────────────────────┐
│                    CONTINUOUS DEPLOYMENT (CD)               │
│  [Deploy Produzione Automatico] ──► [Health Check / Canary] │
└─────────────────────────────────────────────────────────────┘
```

- **Continuous Integration (CI)**: gli sviluppatori integrano il codice su un branch condiviso frequentemente. Ad ogni push o Pull Request, un server CI compila automaticamente l'applicazione, esegue tutti i test unitari e avvia l'analisi statica (SonarQube/SAST). Obiettivo: scoprire i bug immediatamente (*Fail Fast*).
- **Continuous Delivery (CD)**: ogni build che supera la CI viene automaticamente pacchettizzata come artefatto versionato (JAR in Nexus, immagine in Container Registry) e rilasciata negli ambienti di Staging/UAT, pronta per essere promossa in produzione con un clic (*Manual Gate*).
- **Continuous Deployment**: evoluzione della Continuous Delivery in cui la promozione in produzione avviene in modo **100% automatizzato** se tutti i test e i controlli superano i Quality Gate stabiliti.

---

#### 2. Pipeline as Code: Jenkins vs GitLab CI vs GitHub Actions

##### A. Jenkins Pipeline (Dichiarativa in `Jenkinsfile`)
Standard tradizionale in molte banche e grandi enterprise:

```groovy
pipeline {
    agent {
        docker {
            image 'eclipse-temurin:21-jdk-alpine'
        }
    }
    environment {
        NEXUS_CREDENTIALS = credentials('nexus-auth')
        SONAR_TOKEN = credentials('sonar-token')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build & Test') {
            steps {
                sh './mvnw clean verify'
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                    jacoco execFile: '**/target/jacoco.exec'
                }
            }
        }
        stage('SAST Quality Gate') {
            steps {
                withSonarQubeEnv('Internal-Sonar') {
                    sh './mvnw sonar:sonar -Dsonar.qualitygate.wait=true'
                }
            }
        }
        stage('Publish Artifact') {
            steps {
                sh './mvnw deploy -DskipTests'
            }
        }
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh 'kubectl apply -f k8s/staging/ -n payment-staging'
            }
        }
    }
}
```

##### B. GitLab CI (`.gitlab-ci.yml`)
Standard moderno basato su file YAML, container runner dedicati e registry integrato:

```yaml
stages:
  - build_test
  - quality
  - package
  - deploy

build_and_test:
  stage: build_test
  image: maven:3.9-eclipse-temurin-21
  script:
    - mvn clean verify
  artifacts:
    reports:
      junit: target/surefire-reports/*.xml

sonarqube_check:
  stage: quality
  image: sonarsource/sonar-scanner-cli:latest
  script:
    - sonar-scanner -Dsonar.qualitygate.wait=true
  only:
    - merge_requests
    - main

docker_build_push:
  stage: package
  image: docker:24-cli
  services:
    - docker:24-dind
  script:
    - docker login -u $REGISTRY_USER -p $REGISTRY_PASSWORD $REGISTRY_URL
    - docker build -t $REGISTRY_URL/payment-service:$CI_COMMIT_SHORT_SHA .
    - docker push $REGISTRY_URL/payment-service:$CI_COMMIT_SHORT_SHA
```

---

#### 3. Repository Management con Sonatype Nexus / JFrog Artifactory

- **A cosa serve un Repository Manager aziendale**:
  1. **Proxy & Cache**: memorizza localmente le dipendenze scaricate da Maven Central / Docker Hub, velocizzando le build e proteggendo l'azienda da downtime di rete esterni.
  2. **Hosted Repositories**: archivia gli artefatti privati aziendali (JAR delle librerie core, starter interni, DTO condivisi) suddivisi tra:
     - `releases`: artefatti immutabili definitivi (es. `1.0.0`). Non possono mai essere sovrascritti.
     - `snapshots`: versioni di sviluppo modificabili (es. `1.0.1-SNAPSHOT`).
  3. **Container Registry**: funge da registro Docker privato per le immagini dei microservizi prima del deploy in Kubernetes/OpenShift.

---

#### 4. Strategie di Deployment a Zero-Downtime

In un sistema di pagamento attivo 24/7 non sono ammesse finestre di manutenzione con downtime del servizio:

```
[Rolling Update]       Pod v1 ──► Pod v2 (Aggiornamento incrementale 1 ad 1)

[Blue/Green]           Traffic Router (Load Balancer)
                               │
                       ┌───────┴───────┐
                       ▼               ▼
                  [Blue: v1]      [Green: v2] (Testato e promosso al 100%)
                   (Attivo)        (Inattivo)

[Canary Deployment]    Traffic Router ──► 95% al Pod v1 (Produzione stabile)
                                      └─►  5% al Pod v2 (Nuova release monitorata)
```

1. **Rolling Update (Default Kubernetes)**:
   - Sostituisce i vecchi pod con i nuovi uno alla volta.
   - Non richiede il doppio dell'infrastruttura, ma durante il roll-out convivono due versioni diverse (richiede retrocompatibilità sul DB).
2. **Blue/Green Deployment**:
   - Vengono mantenuti due ambienti identici: *Blue* (versione corrente in produzione) e *Green* (nuova versione).
   - Quando la versione *Green* supera tutti i test di fumo, il Load Balancer (o Ingress) commuta istantaneamente il 100% del traffico su *Green*.
   - *Rollback istantaneo*: basta commutare nuovamente il router su *Blue*.
3. **Canary Deployment**:
   - La nuova versione viene rilasciata a una piccola percentuale di traffico reale (es. 2% degli utenti).
   - Se le metriche di errore (Prometheus/Grafana) e i log di business restano nominali, la percentuale viene incrementata gradualmente fino al 100%.

---

#### 5. GitOps e Deployment Dichiarativo (ArgoCD / Flux)
- L'intero stato desiderato dell'infrastruttura e dei microservizi Kubernetes è descritto dichiarativamente in un repository Git dedicato (*Infrastructure as Code*).
- Un controller in Kubernetes (**ArgoCD**) monitora il repository Git: quando un nuovo commit approva una nuova versione dell'immagine, ArgoCD sincronizza automaticamente lo stato del cluster (*Auto-Sync*).

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Qual è la differenza tra Continuous Delivery e Continuous Deployment?*
  - **R**: In entrambi i casi il codice supera l'intera pipeline di CI (build, test, analisi di sicurezza) e viene rilasciato automaticamente in un ambiente di staging. Nella **Continuous Delivery** il passaggio finale in produzione richiede un'approvazione umana esplicita (click su un pulsante o approvazione formale di release). Nel **Continuous Deployment** l'intero flusso è 100% automatico e ogni commit che supera i test atterra direttamente in produzione senza alcun intervento umano.

- *D: Come gestisci un rilascio Blue/Green se la nuova versione include modifiche allo schema del database?*
  - **R**: Applicando il pattern **Expand and Contract (Parallel Run)**: le modifiche al database devono essere sempre retrocompatibili. Nel primo step (*Expand*) si aggiungono nuove colonne o tabelle senza eliminare quelle vecchie, garantendo che sia la versione *Blue* che la *Green* possano funzionare simultaneamente. Solo dopo che la versione *Green* è promossa definitivamente e la vecchia versione viene dismessa, una successiva migrazione DB (*Contract*) rimuove le colonne deprecate.

---

### Come esercitarti
1. **Pipeline Scripting**: scrivi un file `Jenkinsfile` o `.gitlab-ci.yml` che esegue `mvn clean verify`, invoca l'analisi SonarQube con stop on quality gate failure, compila l'immagine Docker con hash del commit e notifica l'esito su Slack/Teams.



################################################################################
### CAPITOLO: 26. Sicurezza e Qualità del Software (i "plus")
################################################################################

# 26. Sicurezza e Qualità del Software (i "plus")

### Cos'è e perché conta
Sono competenze plus, quindi non decisive, ma menzionarle bene ti differenzia dagli altri candidati con solo skill tecniche pure.

### Cosa studiare

**Secure coding**
- OWASP Top 10 a grandi linee: injection (SQL injection soprattutto, vista la centralità di Oracle), broken authentication, exposure di dati sensibili
- Gestione segreti: perché non si mettono credenziali/chiavi in chiaro nel codice, uso di vault/secret manager (anche solo a livello concettuale)

**Tokenizzazione**
- Concetto chiave: sostituire un dato sensibile (es. numero carta/PAN) con un token senza valore fuori dal sistema che lo ha generato, così se il token viene intercettato è inutile
- Differenza tra tokenizzazione e cifratura (la tokenizzazione non è reversibile matematicamente, richiede una tabella di mapping protetta)

**Test automation**
- Piramide dei test: unit (tanti, veloci) → integration (meno, più lenti) → end-to-end (pochi, costosi)
- Mockito per isolare le unità sotto test dai servizi esterni (banche, circuiti) — rilevante perché in ambito pagamenti non puoi testare contro sistemi bancari reali in ogni build

### Come esercitarti
Prepara un esempio concreto (anche dal tuo lavoro recente con Jackson/SOAP-to-JSON o dal progetto di riconciliazione) in cui hai scritto test che isolano una dipendenza esterna — è il tipo di aneddoto che rende credibile questa sezione.



################################################################################
### CAPITOLO: 27. Troubleshooting e Gestione Incident in Produzione
################################################################################

# 27. Troubleshooting e Gestione Incident in Produzione

### Cos'è e perché conta
È un requisito esplicito della job description ("analisi tecnica, troubleshooting e gestione di incident in ambienti di produzione") ma finora mai trattato nel documento. A un senior spesso si chiede non solo "conosci la tecnologia X" ma "come ragioni quando qualcosa si rompe in produzione alle 3 di notte" — è una domanda quasi certa in un colloquio per questo ruolo.

### Metodologia generale (framework da avere pronto)

1. **Individuare e circoscrivere l'impatto**: cosa non funziona, per chi, da quando — prima capire la portata (un cliente? tutti i pagamenti con un circuito specifico? tutti?) che approfondire la causa
2. **Stabilizzare prima di capire**: se esiste un modo rapido per limitare il danno (rollback, feature flag, circuit breaker manuale, failover) si applica **prima** di investigare a fondo la causa — specialmente in un dominio dove ogni minuto di downtime ha un costo diretto
3. **Raccogliere evidenze**: log applicativi, metriche (latenza, error rate — golden signals visti nel punto 11), tracing distribuito se il problema attraversa più servizi
4. **Formulare e verificare ipotesi**: partire dal cambiamento più recente (un deploy? una configurazione? un picco di traffico?) — la causa più probabile di un incident è spesso "cosa è cambiato di recente", non un bug dormiente da mesi
5. **Root cause analysis**: una volta risolto l'impatto immediato, capire la causa profonda — non fermarsi al sintomo (es. "un servizio è andato in OOM" non è la causa, ma il sintomo di un memory leak o di un carico non previsto)
6. **Post-mortem senza colpevolizzazione (blameless)**: documentare cosa è successo, perché, e quali azioni preventive si adottano — pratica standard in ambienti enterprise maturi

### Strumenti concreti da citare

- **Log centralizzati** (ELK, già visto nel punto 11): cercare errori/eccezioni nel periodo dell'incident, correlando per un ID di correlazione/transaction ID che attraversa i vari servizi
- **Tracing distribuito** (Jaeger/Zipkin): capire in quale servizio della catena si è verificato il rallentamento/errore, quando il problema attraversa più microservizi
- **Metriche e dashboard** (Prometheus/Grafana): capire se il problema è graduale (memory leak, saturazione risorse) o improvviso (deploy, picco di traffico)
- **Execution plan** (già visto nel punto 3): se il sintomo è una query lenta, è il primo strumento da controllare

### Esempio di scenario ragionato (utile da avere pronto)

*"Se ricevo un alert che il tasso di errore sulle autorizzazioni carta è salito improvvisamente, per prima cosa controllo se è isolato a un circuito specifico o generale — se è isolato, probabilmente il problema è a valle (es. il circuito esterno è lento o giù) e valuto se attivare un circuit breaker/fallback; se è generale, controllo se c'è stato un deploy recente e valuto un rollback immediato prima di investigare a fondo la causa, perché ripristinare il servizio ha priorità sul capire esattamente cosa è successo."*

### Domande tipiche e risposte

- *D: Qual è il tuo primo passo quando ricevi un alert di produzione?*
  R: Capire l'impatto reale (quanti utenti/transazioni coinvolti, da quando) prima di iniziare a investigare la causa — questo determina l'urgenza e se serve una mitigazione immediata (rollback, failover) prima ancora di capire il "perché".

- *D: Come distingui un problema applicativo da un problema infrastrutturale?*
  R: Guardo le metriche di sistema (CPU, memoria, rete, connessioni DB) insieme ai log applicativi — se le risorse sono normali ma ci sono eccezioni applicative, è probabile un bug o un problema di dati; se le risorse sono sature, è più probabile un problema di capacità/infrastruttura o un memory leak.



################################################################################
### CAPITOLO: 28. Coding IA
################################################################################

# 28. Coding con IA e Coding Agent

### Cos'è e perché conta
Nei colloqui tecnici moderni (soprattutto per ruoli Senior) non ci si aspetta più che uno sviluppatore ignori gli strumenti di Intelligenza Artificiale, ma che dimostri una **forte maturità nel loro utilizzo**: saper sfruttare l'IA e gli **Agenti Autonomi di sviluppo (Coding Agents)** come acceleratori di produttività, mantenendo il controllo rigoroso su architettura del software, sicurezza, privacy dei dati finanziari (PCI-DSS/GDPR) e qualità del codice.

---

### Cosa studiare

#### 1. I Principali Coding Agent ed Ecosistemi
I coding agent sono sistemi basati su LLM capaci non solo di suggerire testo, ma di **agire autonomamente nell'ambiente di sviluppo** (eseguire comandi shell, navigare codebase complesse, modificare file, eseguire test e correggere bug iterativamente):

- **Claude Code (Anthropic)**:
  - Agent a riga di comando (CLI) ad altissima autonomia progettato per sviluppatori.
  - Opera direttamente nel terminale locale: esegue comandi Git, analizza l'intero workspace, applica modifiche a più file, esegue suite di test Maven/Gradle e crea Pull Request in autonomia.
  - Ottimizzato per modelli della famiglia Claude 3.5/3.7 Sonnet con supporto esteso al reasoning e tool use nativo.
- **OpenAI Codex & Canvas / Operator**:
  - Pioniere dei modelli di code generation (da cui è nato GitHub Copilot).
  - L'ecosistema OpenAI attuale include interfacce collaborative (Canvas) e agenti capaci di operare su sandbox con esecuzione Python/Shell per debugging e analisi di problemi complessi.
- **Cursor & Antigravity (Agentic IDEs)**:
  - IDE e ambienti di sviluppo con supporto agentico nativo multi-file e background tasks.
  - Capacità di analizzare semanticamente l'intera codebase, creare piani di implementazione (`implementation_plan.md`), invocare sotto-agenti e validare i risultati via terminale.
- **Aider & OpenHands / SWE-agent**:
  - Tool open-source per il pair programming agentico da terminale, basati sul ciclo Git (un commit atomico per ogni task eseguito con successo) e benchmarkati su SWE-bench per la risoluzione reale di issue GitHub.
- **Assistenti Conversazionali & Pi (Inflection)**:
  - Strumenti di supporto al ragionamento, brain-storming architetturale e chiarimento dei requisiti di business prima della fase di stesura del codice.

---

#### 2. Anatomia di un Coding Agent: MCP, Skills, Rules e Tool Use

Per comprendere e pilotare un coding agent a livello Senior, occorre padroneggiarne l'architettura interna:

```
┌─────────────────────────────────────────────────────────────┐
│                       LLM / AGENT CORE                      │
│      (Reasoning, Planning, Execution Loop: ReAct / Act-Obs) │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
      ┌────────▼────────┐             ┌────────▼────────┐
      │   KNOWLEDGE &   │             │   TOOLS & MCP   │
      │   CONVENTIONS   │             │   INTEGRATION   │
      └────────┬────────┘             └────────┬────────┘
               │                               │
   ┌───────────┴───────────┐       ┌───────────┴───────────┐
   │ • Rules (AGENTS.md)   │       │ • Built-in Tools      │
   │ • Skills (On-demand)  │       │   (view, edit, bash)  │
   │ • System Prompts      │       │ • MCP Servers (DB,    │
   │ • Project Memory      │       │   GitHub, Jira, API)  │
   └───────────────────────┘       └───────────────────────┘
```

##### A. MCP (Model Context Protocol)
- **Cos'è**: è uno **standard aperto e universale** (introdotto da Anthropic e adottato da tutto l'ecosistema) che standardizza il modo in cui i modelli di intelligenza artificiale comunicano con tool e sorgenti dati esterne.
- **Il problema che risolve**: prima di MCP, ogni integrazione (es. collegare un agente a un DB Oracle, a un cluster Kubernetes o a Jira) richiedeva connettori custom e codice proprietario. Con MCP, uno sviluppatore scrive un server MCP una volta sola e qualsiasi agent/client compatibile può utilizzarlo.
- **Architettura**:
  - **Host / Client**: l'ambiente dell'agente (es. Claude Code, Cursor, Antigravity).
  - **Server MCP**: un processo leggero locale o remoto che espone *Risorse* (dati da leggere), *Prompt* (template) e *Tools* (funzioni eseguibili, es. `query_oracle_db`, `inspect_kafka_topic`).
  - **Protocollo JSON-RPC**: comunicazione standard via `stdio` o `SSE` (Server-Sent Events).

##### B. Skills (Competenze On-Demand)
- **Cos'è**: un set modulare di istruzioni specializzate, script, checklist e regole di dominio caricate **on-demand** dall'agente solo quando il task lo richiede.
- **Perché è fondamentale**: la context window dei modelli ha un costo e un limite di attenzione. Anziché riempire il system prompt con 500 pagine di linee guida, le Skills permettono all'agente di "consultare il manuale" solo quando deve svolgere uno specifico compito (es. skill per refactoring Spring Boot 3.x, skill per ISO 20022 XML, skill per tuning query Oracle).

##### C. Rules & Project Conventions (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`)
- File posti nella root del progetto per istruire l'agente sulle convenzioni inderogabili:
  - Build command (`mvn clean test`, `gradle check`).
  - Stile architetturale (Package-by-feature, DTO immutabili con record, Constructor Injection obbligatoria).
  - Regole di sicurezza e gestione segreti (mai loggare PAN, mai fare commit di credenziali).

##### D. Tool Use (Function Calling) & Execution Loop
- Il pattern **ReAct (Reasoning + Acting)**:
  1. **Think / Plan**: l'agente analizza l'obiettivo e scompone il problema.
  2. **Call Tool**: invoca un'azione (es. `grep_search`, `view_file`, `run_command`).
  3. **Observe**: riceve l'output del tool (es. errore di compilazione Maven).
  4. **Self-Correction**: deduce la causa dell'errore, corregge il file sorgente e re-itera fino a completamento.

##### E. Subagents & Multi-Agent Orchestration
- Per task complessi, l'agente principale può orchestrare **sotto-agenti specializzati** con context window isolate (es. un agente analizza i requisiti, un secondo modifica il codice, un terzo esegue i test e fa review di sicurezza).

---

#### 3. Esempi di Skill e Framework di Riferimento: Ponytail, Matt Pocock e Ratel

Nel panorama dello sviluppo agentico, alcune skill e framework sono diventati standard di riferimento della community per risolvere problemi specifici di affidabilità ed efficienza:

##### 🪮 Ponytail (di Dietrich Gebert)
- **Scopo**: contrastare il **code bloat** e l'**over-engineering** tipico degli LLM, costringendo l'agente ad adottare la mentalità pragmatica di un senior developer "pigro ma rigoroso".
- **Come funziona (La Decision Ladder)**:
  Inietta nell'agente una scala di priorità inderogabile prima di scrivere qualsiasi riga di codice:
  1. **YAGNI (You Aren't Gonna Need It)**: la feature/modifica deve davvero esistere o è superflua?
  2. **Reuse**: esiste già qualcosa di analogo nel codice del progetto?
  3. **Stdlib/Native**: si può risolvere usando solo le librerie standard di Java o feature native della piattaforma invece di installare nuove dipendenze?
  4. **Existing Dependency**: c'è già una libreria presente nel `pom.xml` adatta allo scopo?
  5. **One-liner / Minimalism**: implementa la soluzione più sintetica, pulita e minimale possibile.
- **Sicurezza garantita**: pur riducendo il codice al minimo, impone esplicitamente di non toccare o indebolire mai la validazione dei dati, l'error handling e la sicurezza.
- **Impatto**: riduce fino al 50-70% i token generati, i tempi di risposta e la complessità accidentale del codice.

##### 🎯 Matt Pocock Skills (`mattpocock/skills`)
- **Scopo**: trasformare il cosiddetto *"vibe coding"* (programmazione basata su prompt vaghi e improvvisati) in un **processo ingegneristico disciplinato e ripetibile** per Claude Code, Cursor e agenti compatibili.
- **I comandi e workflow principali**:
  - **`/grill-me` (o `/grill-with-docs`)**: l'agente assume il ruolo di un severo intervistatore/architetto che mette sotto stress l'idea o il piano dello sviluppatore con domande mirate, scovando edge case e ambiguità *prima* di toccare qualsiasi riga di codice.
  - **`/to-spec` & `/to-tickets`**: scompone una feature complessa in specifiche tecniche formali e ticket atomici implementabili singolarmente.
  - **`/tdd` & `/implement`**: guida l'agente a seguire rigorosamente il ciclo Test-Driven Development (scrivi il test che fallisce → scrivi il codice minimo per farlo passare → refactoring).
  - **`/wayfinder`**: skill per analizzare e orientarsi rapidamente in codebase monolitiche o non documentate.

##### 🦡 Ratel (`ratel-ai/ratel`)
- **Scopo**: piattaforma di **Context Engineering** e gestione del catalogo di tool/skills, creata per risolvere il problema del **Context Bloat** (quando un agente ha troppi tool caricati e spreca token o si confonde nella scelta).
- **Come funziona (Progressive Disclosure)**:
  - Motore di retrieval ad altissime prestazioni (scritto in Rust) che indicizza tutte le skill e i tool disponibili tramite ricerca ibrida (BM25 + semantica).
  - Anziché iniettare l'intero catalogo nel prompt iniziale, presenta all'agente solo i tool e le skill pertinenti al sotto-task corrente.
  - Espone un proprio **server MCP**, integrabile nativamente con Claude Code, Cursor e Codex, abbattendo il consumo di token fino all'80% e riducendo drasticamente la latenza.

---

#### 4. Casi d'uso ad alto impatto per uno sviluppatore Java Backend
- **Generazione e arricchimento di Test (TDD & BDD)**:
  - Creazione di test unitari parametrici (`@ParameterizedTest` con JUnit 5) per coprire edge case limite (es. arrotondamenti finanziari, validazioni di stringhe ISO 8583/20022).
  - Scrittura rapida di test di integrazione con Mockito, `@MockBean` e `@DataJpaTest`.
- **Refactoring e modernizzazione codice legacy**:
  - Conversione di codice Java 8 imperativo in flussi Stream / Functional Programming.
  - Migrazione a nuove feature di linguaggio (Records, Pattern Matching su `switch`, `sealed` classes, Virtual Threads di Java 21).
  - Isolamento di classi monolitiche e introduzione di design pattern (Strategy, Factory, Adapter).
- **Scrittura e ottimizzazione di query complesse**:
  - Bozza di query SQL avanzate (Window Functions, Common Table Expressions - CTE) e conversione in JPQL o Spring Data Specifications.
- **Boilerplate e configurazioni**:
  - Scrittura di DTO, Mapper (MapStruct), configurazioni Spring Cloud / Kafka / Redis, schemi OpenAPI (Swagger) e script Docker / Kubernetes manifests.

---

#### 5. Rischi critici, Sicurezza e Regolamentazione (dominio Pagamenti / Bancario)
Questo è il tema chiave su cui un intervistatore valuterà la seniority: **l'uso sconsiderato dell'IA è pericoloso in contesti mission-critical**.

- **Privacy dei dati e conformità (PCI-DSS & GDPR)**:
  - **Zero PII / Zero Card Data**: mai condividere con modelli di IA esterni dati sensibili, PAN delle carte, token di autenticazione, password o secret di connessione DB.
  - Policy aziendali: utilizzo di modelli enterprise self-hosted o con garanzie contrattuali di non-training sui dati inseriti (es. Azure OpenAI con tenancy privata, AWS Bedrock, Copilot Enterprise).
- **Allucinazioni e falsi positivi**:
  - L'IA può inventare metodi inesistenti, API deprecate o implementare algoritmi crittografici non sicuri (es. uso improprio di `Math.random()` anziché `SecureRandom` per token di pagamento).
  - *Regola aurea*: "Non si committa mai codice generato dall'IA che non si sia compreso riga per riga e validato tramite test automatici".
- **Debito tecnico e "Vibe Coding"**:
  - Rischio di inserire codice apparentemente funzionante ma architetturalmente disallineato rispetto ai principi SOLID, pattern del team o convenzioni di isolamento transazionale (`@Transactional`).
- **Proprietà intellettuale e licenze**:
  - Attenzione alla generazione di codice soggetto a licenze restrittive (es. GPL) in progetti proprietari.

---

#### 6. Prompt Engineering & Context Management per Backend Developer
- **Fornire contesto esplicito**: passare sempre tipi, interfacce, vincoli di dominio ed esempi di input/output attesi invece di istruzioni generiche.
- **Approccio iterativo**: decomporre problemi architetturali complessi in step progressivi (Design interfaccia → Implementazione business logic → Validazioni → Test suite).
- **Inversione del controllo nel prompt**: chiedere all'IA di fare una code review, cercare falle di concorrenza/race conditions, o identificare potenziali memory leak ed eccezioni non gestite.

---

### Domande tipiche a colloquio (e come rispondere da Senior)

- *D: Come utilizzi l'Intelligenza Artificiale nel tuo lavoro quotidiano?*
  - **R**: La uso quotidianamente come moltiplicatore di produttività ("pair programmer virtuale"), sfruttando sia assistenti contestuali nell'IDE sia coding agent da terminale (come Claude Code o Cursor). Li guido con skill e workflow strutturati (es. regole TDD stile Matt Pocock o principi di minimalismo anti-bloat stile Ponytail) per velocizzare la scrittura di test unitari, generare boilerplate (DTO, script Flyway) ed esplorare refactoring, mantenendo sempre la revisione critica e test automatici su ogni riga.

- *D: Cos'è l'MCP (Model Context Protocol) e perché è rilevante?*
  - **R**: È uno standard aperto creato per normalizzare la connessione tra modelli LLM/agenti e sorgenti dati o tool esterni (database, repository Git, issue tracker, log di produzione). Invece di scrivere integrazioni ad-hoc per ogni strumento, un server MCP espone funzioni e risorse riutilizzabili da qualsiasi agent compatibile, rendendo l'ecosistema agentico modulare e sicuro.

- *D: Come eviti che un coding agent introduca over-engineering o codice superfluo?*
  - **R**: Utilizzo convenzioni esplicite e skill dedicate (come il pattern Ponytail) che forzano l'agente a seguire il principio YAGNI, a riutilizzare librerie e componenti già presenti nella codebase o nella Java standard library prima di creare nuove astrazioni o aggiungere dipendenze. Inoltre, definisco regole di progetto (`AGENTS.md` o `.cursorrules`) con vincoli chiari di architettura.

- *D: Quali sono i rischi dell'uso dell'IA in un'architettura bancaria / pagamenti elettronici?*
  - **R**: Il primo rischio è la **privacy e compliance**: dati di carte (PAN), PII e credenziali non devono mai transitare su LLM pubblici, per rispettare PCI-DSS e GDPR. Il secondo è l'**affidabilità transazionale**: in sistemi a forte consistenza ACID e con rigide regole di idempotenza, l'IA può generare codice che "sembra" corretto ma ha race conditions nascoste o gestione transazionale errata (`REQUIRES_NEW` improprio). Per questo il controllo umano e una solida suite di integration test restano insostituibili.

- *D: Se un'IA suggerisce una soluzione alternativa a un problema architetturale, come ti comporti?*
  - **R**: Valuto il suggerimento confrontandolo con i vincoli del sistema: carico atteso, throughput, scalabilità, manutenibilità da parte del team e consistenza con lo stack esistente. L'IA è eccellente per aprire ventagli di opzioni e trade-off (es. lock ottimistico vs pessimistico, code Kafka vs JMS), ma la decisione finale deve sempre basarsi sulla conoscenza profonda del contesto di business.

---

### Come esercitarti
1. **Spiegazione a voce (2 minuti)**: preparati un discorso chiaro in cui spieghi come l'IA e i coding agent ti rendono più rapido senza intaccare il tuo senso critico e la sicurezza del software.
2. **Esercizio pratico**: prendi una logica di calcolo commissioni o un parser ISO 8583 e chiedi a un assistente/agente IA di trovare potenziali bug di arrotondamento o casi limite non coperti; analizza criticamente i risultati.



################################################################################
### CAPITOLO: 29. Metodologie Agile, Product Mindset, Documentazione e Soft Skill
################################################################################

# 29. Metodologie Agile, Product Mindset, Documentazione e Soft Skill

## Cos'è e perché conta

Nei colloqui per posizioni Senior e Lead Developer, le competenze tecniche pure valgono solo il 50% della valutazione. L'altra metà valuta la **maturità professionale**: come lavori in team, come gestisci conflitti e priorità di business, come applichi le metodologie **Agile (Scrum e Kanban)**, come documenti requisiti e decisioni architetturali (**ADR, C4 Model, OpenAPI**) e come dimostri un autentico **Product Mindset** (trasformare requisiti di business complessi in valore misurabile per l'utente finale).

---

## 1. Metodologie Agile: Scrum vs Kanban

```
                      CONFRONTO FRAMEWORK AGILE
         SCRUM (Flusso a Sprint)                 KANBAN (Flusso Continuo)
   ┌─────────────────────────────────┐     ┌─────────────────────────────────┐
   │ • Iterazioni fisse (1-4 sett.)  │     │ • Nessuna iterazione fissa      │
   │ • Ruoli definiti (PO, SM, Dev)  │     │ • Focus sui WIP Limits          │
   │ • Cerimonie strutturate         │     │ • Consegna continua su richiesta│
   │ • Metrica: Velocity / Burndown  │     │ • Metrica: Lead & Cycle Time    │
   └─────────────────────────────────┘     └─────────────────────────────────┘
```

### 1. Scrum nel Dettaglio
* **I 3 Ruoli**:
  * **Product Owner (PO)**: Definisce la vision di prodotto, gestisce e ordina per priorità di business il *Product Backlog*.
  * **Scrum Master (SM)**: Facilita il processo, rimuove gli ostacoli (*impediments*) e protegge il team da distrazioni esterne.
  * **Development Team**: Team auto-organizzato, cross-funzionale e responsabile della stima e della consegna dell'incremento.
* **Le 5 Cerimonie (Eventi)**:
  1. **Sprint Planning**: Definizione dello *Sprint Goal* e selezione delle User Story da includere nello *Sprint Backlog*.
  2. **Daily Scrum (15 min)**: Allineamento quotidiano su cosa si è fatto, cosa si farà e blocchi operativi.
  3. **Sprint Review**: Demo dell'incremento funzionante agli stakeholder di business per raccogliere feedback immediato.
  4. **Sprint Retrospective**: Analisi interna del team su processi, strumenti e relazioni umane (*Cosa ha funzionato? Cosa migliorare? Action item concreti*).
  5. **Backlog Refinement (Grooming)**: Chiarimento delle User Story future, suddivisione e stima.
* **Artefatti & Criteri di Qualità**:
  * **Definition of Ready (DoR)**: Criteri affinché una storia possa essere inserita nello Sprint (requisiti chiari, dipendenze risolte, acceptance criteria definiti).
  * **Definition of Done (DoD)**: Criteri inderogabili affinché una storia sia considerata completata (codice scritto, test unitari e integrati verdi, code review approvata, documentazione aggiornata, deploy in ambiente di staging).

### 2. Kanban nel Dettaglio
* **Principi Chiave**:
  * **Visualizzare il Flusso**: Board con colonne chiare (*To Do $\to$ In Analysis $\to$ In Dev $\to$ In Review $\to$ In Test $\to$ Done*).
  * **WIP Limits (Work In Progress Limits)**: Numero massimo di task ammessi contemporaneamente in una colonna. Impedisce il multitasking inefficiente, fa emergere i colli di bottiglia e favorisce il *"Stop starting, start finishing"*.
* **Metriche di Flusso**:
  * **Lead Time**: Tempo totale dal momento in cui il task viene richiesto/creato a quando è rilasciato in produzione.
  * **Cycle Time**: Tempo effettivo impiegato da quando si inizia a lavorare sul task a quando è completato.

---

## 2. Product Mindset & Orientamento al Valore di Business

Un Senior Developer non è un "esecutore di ticket", ma un **partner strategico del business**:

```
                              PRODUCT MINDSET vs OUTPUT MINDSET
      OUTPUT MINDSET (Junior/Mid)                   PRODUCT MINDSET (Senior/Lead)
   ┌───────────────────────────────┐             ┌───────────────────────────────┐
   │ "Ho completato 8 ticket in    │ ──────────► │ "Abbiamo ridotto il tasso di  │
   │  questo Sprint: 40 Story Point│             │  abbandono al checkout del 3% │
   │  consegnati."                 │             │  velocizzando le API di auth."│
   └───────────────────────────────┘             └───────────────────────────────┘
```

### Le Dimensioni del Product Mindset:
1. **Outcome over Output**: Misurare il successo dall'impatto reale sul cliente e sul business, non solo dal numero di righe di codice o story point prodotti.
2. **Metriche di Business & KPI FinTech/Enterprise**:
   * **Conversion Rate**: Percentuale di utenti che completano con successo un pagamento o un onboarding.
   * **Churn Rate**: Tasso di abbandono del servizio da parte dei clienti.
   * **CAC (Customer Acquisition Cost)** vs **LTV (Customer Lifetime Value)**.
   * **Time-to-Market**: Velocità nel validare nuove ipotesi di business sul mercato.
3. **Collaborazione Cross-Funzionale**:
   * Lavorare in sintonia con **Product Manager** (per comprendere il *perché* di una feature), **UI/UX Designer** (per garantire fattibilità tecnica e reattività delle API), **QA Engineers** (per strategie di test automation) e **Compliance/Legal** (per vincoli normativi).
4. **Prioritizzazione con Framework RICE**:
   $$\text{RICE Score} = \frac{\text{Reach (Quanti utenti)} \times \text{Impact (Impatto sul business)} \times \text{Confidence (Grado di certezza)}}{\text{Effort (Giorni/Uomo)}}$$

---

## 3. Analisi dei Requisiti e Documentazione Tecnica e Funzionale

Un software non documentato o con requisiti ambigui genera bug costosi e disallineamenti nel team.

### 1. User Story e Criteri di Accettazione (INVEST Model)
Le User Story devono seguire l'acronimo **INVEST** (*Independent, Negotiable, Valuable, Estimable, Small, Testable*) con formato standard:
* **Template**: *Come [ruolo utente], voglio [funzionalità/azione], affinché [beneficio/valore di business].*
* **Acceptance Criteria (Formato Gherkin BDD)**:
  ```gherkin
  Scenario: Blocco automatico per tentativo di pagamento superiore al plafond
    Given un utente titolare di carta con plafond residuo di 500.00 EUR
    When richiede un'autorizzazione di pagamento di 600.00 EUR
    Then la richiesta viene rifiutata con codice "LIMIT_EXCEEDED"
    And viene inviata una notifica push di avviso all'utente
  ```

---

### 2. Architecture Decision Records (ADR)
L'**ADR** è un documento sintetico e versionato nel repository Git che traccia **il contesto e la motivazione di una scelta architetturale cruciale**, evitando che nel tempo si perda il motivo di una decisione (*"Perché abbiamo scelto Kafka invece di RabbitMQ?"*).

```markdown
# ADR 005: Utilizzo di Redis come Idempotency Store

## Stato
Approvato (2026-09-14)

## Contesto
I picchi di traffico di pagamento causano frequenti retry di rete da parte dei client mobile,
rischiando doppi addebiti. La verifica di idempotenza su Oracle DB impatta le prestazioni di I/O.

## Decisione
Implementiamo il pattern Idempotency-Key salvando la chiave su un cluster Redis dedicato,
con operazione atomica SETNX e TTL di 48 ore.

## Conseguenze
- Positive: Latenza di verifica abbattuta a < 2 ms; zero lock sul database Oracle.
- Negative: Aggiunta di una dipendenza infrastrutturale (cluster Redis) da monitorare in alta disponibilità.
```

---

### 3. Visualizzazione Architetturale: Il Modello C4

Creato da Simon Brown, il modello **C4** struttura i diagrammi architetturali su 4 livelli di zoom gerarchici:

```
                            I 4 LIVELLI DEL MODELLO C4
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ 1. CONTEXT DIAGRAM    │ Mostra il sistema globale, utenti e sistemi esterni │
 ├───────────────────────┼─────────────────────────────────────────────────────┤
 │ 2. CONTAINER DIAGRAM  │ Mostra le applicazioni web, microservizi, DB, code  │
 ├───────────────────────┼─────────────────────────────────────────────────────┤
 │ 3. COMPONENT DIAGRAM  │ Mostra i controller, servizi e repository interni   │
 ├───────────────────────┼─────────────────────────────────────────────────────┤
 │ 4. CODE DIAGRAM       │ Diagrammi UML di classi e relazioni specifiche      │
 └───────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 4. Problem Solving Strutturato e Gestione del Rischio

Nei colloqui di selezione Senior viene valutato il processo mentale di risoluzione dei problemi (*Problem Solving*):

1. **Decomposizione e Isolamento del Problema**:
   * Scomporre un problema complesso o un incidente di produzione in sotto-problemi isolati verificabili indipendentemente (*Divide et Impera*).
2. **Data-Driven Investigation**:
   * Non basarsi su supposizioni o "sensazioni", ma analizzare **metriche (Prometheus), log correlati tramite `traceId` e profili di esecuzione CPU/Memory**.
3. **Gestione del Rischio Tecnico**:
   * Identificare proattivamente i rischi prima del rilascio (punti singoli di fallimento, saturazione pool DB, dipendenze non ridondate) e definire piani di mitigazione o *Rollback Strategy*.

---

## 5. Risposte Comportamentali con il Metodo STAR

Per rispondere in modo strutturato, conciso e autorevole a domande situazionali:
* **S (Situation)**: Descrivi brevemente il contesto o la sfida.
* **T (Task)**: Qual era la tua responsabilità specifica o l'obiettivo da raggiungere.
* **A (Action)**: Quali azioni concrete hai intrapreso (sia tecniche che relazionali).
* **R (Result)**: Qual è stato il risultato misurabile ottenuto (in termini di tempo, performance o valore per il business).

### Esempi Pratici per Colloquio Senior:

- *D: Raccontami di una volta in cui hai avuto un disaccordo tecnico con un collega o architetto.*
  - **R (STAR)**:
    - *S*: Durante la progettazione di un nuovo servizio di settlement, l'architetto proponeva di usare chiamate REST sincrone a cascata tra 4 microservizi, mentre io ritenevo che introducesse accoppiamento temporale e rischio di timeout a catena.
    - *T*: Il mio obiettivo era garantire l'affidabilità e il throughput del sistema senza creare attriti nel team.
    - *A*: Anziché scontrarmi sul piano personale, ho preparato un rapido benchmark (*Proof of Concept*) simulando un degrado di rete sul terzo servizio, dimostrando che l'architettura REST andava in cascata di timeout, mentre un'architettura a eventi con **Outbox Pattern e Kafka** isolava completamente i servizi garantendo consistenza eventuale.
    - *R*: Il team e l'architetto hanno concordato sulla soluzione a eventi, che è andata in produzione senza registrare alcun incidente di timeout durante i picchi di fine mese.

- *D: Come ti comporti quando un Product Owner chiede una feature urgente tagliando sulla qualità del codice o sui test?*
  - **R (STAR)**:
    - Spiego al PO l'impatto in termini di **Trade-off e Rischio di Business**: rilasciare senza test automatizzati una logica finanziaria espone l'azienda a bug contabili e a tempi di rilascio più lunghi per i fix futuri (*Technical Debt*). Concordo un approccio pragmatico: riduciamo lo *Scope* della feature (rilasciando un MVP funzionale più piccolo) mantenendo però intatta la suite di test essenziali e la sicurezza transazionale, pianificando il completamento nel backlog successivo.



################################################################################
### CAPITOLO: 30. Concetti Trasversali Importanti
################################################################################

# 30. Concetti Trasversali Importanti

### Cos'è e perché conta
Sono temi che attraversano tutta l'architettura (sicurezza, osservabilità, CI/CD, resilienza) e che spesso emergono in domande "da senior" — non tanto "sai scrivere questo codice" quanto "sai ragionare sul sistema nel suo complesso".

### Cosa studiare

**Sicurezza**

- **Autenticazione vs autorizzazione**: l'autenticazione verifica *chi sei* (login), l'autorizzazione verifica *cosa puoi fare* (permessi) — distinzione base ma spesso confusa, utile da avere chiara e pronta
- **OAuth 2.0**: protocollo standard per delegare l'accesso senza condividere le credenziali — flussi principali (Authorization Code, Client Credentials per comunicazione server-to-server, rilevante in integrazioni B2B tra sistemi di pagamento)
- **JWT (JSON Web Token)**: token firmato che incapsula informazioni (claims) verificabili senza dover interrogare un DB centrale ad ogni richiesta — attenzione alla differenza tra firma (integrità, chiunque può leggere il contenuto) e cifratura (contenuto nascosto)
- **Gestione dei secrets** (Vault, AWS Secrets Manager): mai credenziali/chiavi hardcoded nel codice o in config in chiaro — un secret manager centralizza, ruota e audita l'accesso a credenziali sensibili
- **Principio del least privilege**: ogni componente/utente ha solo i permessi minimi indispensabili per il proprio compito — riduce l'impatto di una compromissione
- **Encryption at rest e in transit**: dati cifrati sia quando salvati su disco (at rest) sia durante la trasmissione in rete (in transit, tipicamente TLS) — requisito quasi sempre esplicito in ambito PCI-DSS

**Osservabilità**

I tre pilastri:
- **Logging** (ELK stack — Elasticsearch/Logstash/Kibana, Splunk): registrazione di eventi discreti, utile per debug e audit trail
- **Metrics** (Prometheus, Grafana): valori numerici aggregati nel tempo (latenza media, throughput, error rate) — utili per dashboard e alerting
- **Tracing distribuito** (Jaeger, Zipkin): traccia il percorso di una singola richiesta attraverso più microservizi, fondamentale per capire dove si perde tempo o dove fallisce una chiamata in una catena di servizi

**Golden signals** da monitorare: latenza, error rate, throughput (spesso si aggiunge saturazione delle risorse come quarto segnale) — in un sistema di pagamenti questi si traducono direttamente in SLA verso i partner (es. tempo massimo di risposta per un'autorizzazione).

**CI/CD**

- **Pipeline di deployment**: sequenza automatizzata di build, test, quality gate, deploy — collegabile a Jenkins già visto nella sezione toolchain
- **Blue-green deployment**: due ambienti identici (blue e green), il traffico viene spostato istantaneamente dall'uno all'altro dopo il deploy della nuova versione — rollback immediato se qualcosa va storto, semplicemente reindirizzando il traffico indietro
- **Canary release**: la nuova versione viene rilasciata prima a una piccola percentuale di traffico/utenti, per verificarne il comportamento in produzione prima di un rollout completo — riduce il rischio in sistemi critici
- **Rollback automatici**: se le metriche post-deploy peggiorano oltre soglia, il sistema torna automaticamente alla versione precedente
- **Infrastructure as Code** (Terraform, CloudFormation): l'infrastruttura è definita come codice versionabile, invece che configurata manualmente — garantisce riproducibilità e tracciabilità delle modifiche

**Resilienza**

- **Timeout**: ogni chiamata a un servizio esterno deve avere un timeout esplicito, altrimenti un servizio lento può bloccare indefinitamente il chiamante
- **Retry con exponential backoff**: se una chiamata fallisce, riprovare aumentando progressivamente l'attesa tra un tentativo e l'altro (es. 1s, 2s, 4s, 8s), per non sovraccaricare un servizio già in difficoltà
- **Idempotenza delle operazioni**: già vista nella sezione su `@Transactional` — un'operazione ripetuta (es. per un retry) deve avere lo stesso effetto di eseguita una sola volta, cruciale per evitare doppi addebiti
- **Graceful degradation**: se una funzionalità non essenziale fallisce, il sistema continua a funzionare offrendo un servizio ridotto invece di fallire completamente (es. se il servizio di scoring frodi è giù, si può decidere di procedere comunque con un pagamento a basso rischio invece di bloccare tutto)

### Come esercitarti
Collega esplicitamente **retry + idempotenza** al punto già visto su `@Transactional`: è uno dei fili conduttori più forti del colloquio, perché tocca dominio, Spring e architettura distribuita nello stesso concetto — un ottimo esempio da avere pronto e ben padroneggiato.



################################################################################
### CAPITOLO: 31. Dominio Pagamenti
################################################################################

# 31. Dominio Pagamenti

### Cos'è e perché è il punto più importante
Essendo "esperienza mandatoria", il colloquio probabilmente dedicherà tempo a domande discorsive sul dominio, non solo tecniche. Devi essere in grado di spiegare il ciclo di vita di una transazione come lo spiegheresti a un collega nuovo del team.

### Cosa studiare

**Ciclo di vita di una transazione carta**
- *Autorizzazione*: il merchant chiede all'issuer (banca del titolare carta) se i fondi/il credito sono disponibili — risposta in tempo reale (millisecondi)
- *Cattura (capture)*: il merchant conferma l'addebito effettivo (a volte avviene subito, a volte dopo giorni — es. hotel, noleggio auto)
- *Clearing*: gli istituti si scambiano le informazioni sulle transazioni da regolare, di solito in batch notturni
- *Settlement*: il movimento di denaro effettivo tra le banche coinvolte
- *Chargeback*: la contestazione da parte del titolare carta, con reverse del flusso

**Attori del sistema**
- *Issuer*: la banca che ha emesso la carta al cliente
- *Acquirer*: la banca che fornisce il servizio di accettazione pagamenti al merchant
- *PSP (Payment Service Provider)*: intermediario tecnologico tra merchant e acquirer/circuiti (es. Nexi, Stripe)
- *Circuito*: la rete che instrada e regola le transazioni (Visa, Mastercard, ecc.)

**Circuiti e protocolli**
- *ISO 8583*: protocollo a messaggi (non XML/JSON) storicamente usato per l'autorizzazione carte — capire la struttura a campi (MTI, bitmap, data elements) anche solo a livello concettuale
- *ISO 20022*: standard più moderno basato su XML, usato per bonifici SEPA e sempre più anche per carte — capire perché sta sostituendo ISO 8583 (interoperabilità, dati più ricchi)
- *SEPA*: SCT (bonifico standard, T+1) vs SCT Inst (bonifico istantaneo, esecuzione in secondi, 24/7)
- *Digital wallet*: come Apple Pay/Google Pay generano un token di dispositivo al posto del PAN reale (tokenizzazione EMV), il ruolo del Token Service Provider

**Normative**
- *PSD2*: obbligo di Strong Customer Authentication (SCA) — autenticazione a due fattori tra possesso, conoscenza, inerenza; le eccezioni (basso importo, transazioni ricorrenti)
- *PCI-DSS*: standard di sicurezza per chi tratta dati carta — perché la tokenizzazione riduce lo "scope" di compliance
- *GDPR* applicato a dati finanziari: minimizzazione, retention, diritto alla cancellazione in tensione con obblighi di conservazione fiscale/antiriciclaggio

**Riconciliazione (il tuo punto di forza)**
- Ripassa mentalmente il progetto Castelmonte: matching automatico vs manuale, gestione delle eccezioni/discrepanze, allocazione di più righe a un movimento
- Collega questo esplicitamente a "clearing/settlement/provisioning" nella job description: la riconciliazione bancaria che hai costruito è concettualmente lo stesso problema che risolvono in ambito clearing — preparati a raccontarlo come esperienza rilevante, anche se il contesto di partenza era diverso

### Come esercitarti
Prova a spiegare ad alta voce, in 2 minuti, il percorso di 10€ pagati con carta in un negozio, dal POS fino a quando il negozio vede i soldi sul conto. Se riesci a farlo fluido, sei pronto per questa parte.



################################################################################
### CAPITOLO: 32. Dominio Assicurativo, Previdenziale e Sistemi Finanziari
################################################################################

# 32. Dominio Assicurativo, Previdenziale e Sistemi Finanziari (OMS, Portfolio, Billing, Reconciliation)

## Cos'è e perché conta

Nei settori **FinTech, InsurTech, Wealth Management e Banking**, i requisiti tecnici si intrecciano indissolubilmente con la complessità del dominio di business e i vincoli normativi (IVASS, COVIP, Solvency II, MiFID II, IFRS 17). Uno sviluppatore Senior deve dimostrare non solo eccellenza tecnologica (Java, microservizi, architetture a eventi), ma anche **padronanza del linguaggio ubiquo di business**, comprendendo come i flussi di dati impattano contratti, calcoli attuariali, gestione ordini, portafogli, fatturazione e riconciliazioni contabili.

---

## 1. Il Dominio Assicurativo (Insurance / InsurTech)

```
                            CICLO DI VITA ASSICURATIVO
  ┌────────────────┐      ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
  │  Underwriting  │ ───► │  Policy Issue  │ ───► │   Collection   │ ───► │     Claims     │
  │ (Assunzione)   │      │  (Emissione)   │      │   (Incasso)    │      │   (Sinistri)   │
  └────────────────┘      └────────────────┘      └────────────────┘      └────────────────┘
```

### Concetti Fondamentali
1. **Tipologie di Polizze**:
   * **Ramo Vita (Life Insurance)**:
     * *Ramo I*: Polizze rivalutabili tradizionali (a capitale garantito con gestione separata).
     * *Ramo III (Unit-Linked / Index-Linked)*: Polizze il cui rendimento è legato a fondi comuni di investimento o indici finanziari (il rischio di mercato è a carico del contraente).
     * *Ramo V*: Operazioni di capitalizzazione.
   * **Ramo Danni (Non-Life / P&C - Property & Casualty)**:
     * Coperture per eventi accidentali: RC Auto/Moto, Infortuni, Malattia, Incendio, Furto, Responsabilità Civile Generale, Tutela Legale.
2. **I Soggetti del Contratto**:
   * **Compagnia (Assicuratore)**: L'ente che assume il rischio dietro pagamento del premio.
   * **Contraente**: Chi stipula la polizza e paga il premio.
   * **Assicurato**: La persona fisica o giuridica la cui vita/beni sono esposti al rischio.
   * **Beneficiario**: Chi riceve la prestazione economica (indennizzo o capitale) al verificarsi dell'evento.
3. **Flussi Operativi di Core Insurance**:
   * **Underwriting (Assunzione del Rischio)**: Valutazione del profilo di rischio (score anamnestico, peritale o telemetrico) e determinazione della tariffa/premio.
   * **Gestione Premi (Premium Management)**: Calcolo del premio (puro + caricamenti per costi di gestione e provvigioni), piani di frazionamento (annuale, semestrale, mensile con addebito SDD) e quietanzamento.
   * **Gestione Sinistri (Claims Management)**: Denuncia del sinistro (*First Notice of Loss - FNOL*), perizia, calcolo della franchigia/scoperto, costituzione della riserva sinistri e liquidazione dell'indennizzo.
   * **Riserve Tecniche (Technical Reserves)**: Accantonamenti obbligatori a bilancio per garantire la solvibilità futura delle prestazioni (Riserva Premi, Riserva Sinistri, Riserva Matematica).
4. **Normativa di Riferimento**:
   * **IVASS**: Istituto per la Vigilanza sulle Assicurazioni (regolamentazione trasparenza, IDD - Insurance Distribution Directive).
   * **Solvency II**: Requisiti patrimoniali basati sul rischio per evitare insolvenze delle compagnie.
   * **IFRS 17**: Standard contabile internazionale per i contratti assicurativi.

---

## 2. Il Dominio Previdenziale (Pension Funds / Previdenza Complementare)

La previdenza si basa sul sistema a "tre pilastri":
1. *Primo Pilastro*: Previdenza pubblica obbligatoria (INPS).
2. *Secondo Pilastro*: Fondi pensione chiusi/negoziali di categoria (es. Cometa, Fonte) o aperti.
3. *Terzo Pilastro*: Piani Individuali Pensionistici (PIP) e polizze previdenziali individuali.

```
                          LE DUE FASI DELLA PREVIDENZA
   FASE DI ACCUMULO (Versamenti)                  FASE DI EROGAZIONE (Rendita)
 ┌───────────────────────────────┐              ┌───────────────────────────────┐
 │ • Contributo Lavoratore       │   CONVERSIONE│ • Rendita Vitalizia Immediata │
 │ • Contributo Datore di Lavoro │ ───────────► │ • Rendita Reversibile         │
 │ • Conferimento TFR            │              │ • Liquidazione Capitale (max  │
 │ • Rivalutazione Quote/NAV     │              │   50% o 100% per casi limite) │
 └───────────────────────────────┘              └───────────────────────────────┘
```

### Flussi e Meccanismi Chiave
* **Fase di Accumulo**:
  * Gestione dei flussi contributivi (contribuzione volontaria + contributo datoriale + TFR).
  * Acquisto periodico di **quote del comparto** (Garantito, Prudente, Bilanciato, Azionario) valorizzate al **NAV** (*Net Asset Value*).
  * Fiscalità agevolata: deducibilità dei versamenti fino al tetto di legge (€ 5.164,57 annui).
* **Fase di Erogazione (Decumulo)**:
  * Al raggiungimento dei requisiti pensionistici: liquidazione in capitale (fino al 50%) e conversione del montante residuo in **Rendita Vitalizia** tramite coefficienti di conversione attuariali.
  * Anticipazioni (per spese sanitarie, acquisto prima casa) e Riscatti (in caso di disoccupazione o invalidità).
* **Vigilanza**: **COVIP** (Commissione di Vigilanza sui Fondi Pensione).

---

## 3. Order Management System (OMS) & Esecuzione Ordini

Un **Order Management System (OMS)** è la piattaforma finanziaria che gestisce l'intero ciclo di vita degli ordini di compravendita di strumenti finanziari (azioni, obbligazioni, ETF, derivati, fondi).

```
 ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
 │  Portfolio   │ ──► │     OMS      │ ──► │  Smart Order │ ──► │ Execution    │
 │  Manager     │     │  (Compliance │     │  Router      │     │ Venues       │
 │  (Creazione) │     │   Pre-Trade) │     │  (SOR)       │     │ (Borse/Dark) │
 └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### Il Ciclo di Vita dell'Ordine:
1. **Generazione dell'Ordine**: Il gestore crea una proposta di investimento o disinvestimento.
2. **Pre-Trade Compliance & Risk Check**: Controlli bloccanti automatici real-time:
   * Verifica limiti normativi (MiFID II, UCITS) e mandati contrattuali del cliente.
   * Controllo disponibilità fondi / capienza titoli (*Short Selling check*).
3. **Smart Order Routing (SOR)**: Algoritmo che seleziona la *Execution Venue* ottimale (Borsa Italiana, Euronext, MTF, Internalizzatori Sistematici) in termini di prezzo, costo, velocità e probabilità di esecuzione (*Best Execution*).
4. **Protocollo FIX (Financial Information eXchange)**:
   * Standard universale di messaggistica finanziaria TCP basato su tag-value (es. `35=D` New Order Single, `35=8` Execution Report).
5. **Execution Report & Post-Trade**: Ricezione degli eseguiti parziali/totali, allocazione sui conti dei singoli clienti e invio al sistema di regolamento (*Clearing & Settlement* via Monte Titoli / Euroclear).

---

## 4. Portfolio Management & Wealth Tech

I sistemi di **Portfolio Management (PMS)** calcolano l'esposizione, la valorizzazione e il rendimento dei patrimoni in gestione.

### Concetti Chiave:
* **Asset Allocation**: Ripartizione del portafoglio tra classi di asset (Azionario, Obbligazionario, Liquidità, Real Estate, Commodities) secondo profili di rischio (Conservativo, Moderato, Aggressivo).
* **Valorizzazione e NAV (Net Asset Value)**:
  $$\text{NAV} = \frac{\text{Valore di Mercato degli Attivi} - \text{Passività}}{\text{Numero di Quote in Circolazione}}$$
* **Calcolo delle Performance**:
  * **TWR (Time-Weighted Return)**: Misura l'abilità del gestore isolando l'impatto dei flussi di cassa (versamenti/prelievi del cliente). Standard istituzionale GIPS.
  * **MWR / IRR (Money-Weighted Return)**: Tasso interno di rendimento che tiene conto dei tempi e volumi dei versamenti/prelievi del cliente.
* **Metriche di Rischio**:
  * **Volatilità (Deviazione Standard)**: Misura la dispersione dei rendimenti rispetto alla media.
  * **Value at Risk (VaR)**: Massima perdita potenziale stimata con un dato intervallo di confidenza (es. 99%) su un dato orizzonte temporale.
  * **Sharpe Ratio**: Misura dell'extra-rendimento per unità di rischio rispetto al tasso privo di rischio (*risk-free rate*).

---

## 5. Billing, Commissioning & Revenue Split

I sistemi di **Billing Finanziario e Assicurativo** gestiscono il calcolo automatico, la fatturazione e la ripartizione delle commissioni.

```
                             MODELLO DI FEE SPLITTING
   ┌────────────────────────────────────────────────────────────────────────┐
   │ Commissione di Gestione Totale (es. 1.50% annuo sul patrimonio medio)  │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
   Management Company / SGR (0.60%)                       Distributore / Rete (0.90%)
   (Gestione e Manutenzione Prodotto)                     (Provvigione di Mantenimento)
```

### Tipologie di Commissioni (Fees):
* **Management Fees (Commissioni di Gestione)**: Calcolate pro-quota giornaliera sul patrimonio medio gestito (AuM - *Assets under Management*) e liquidate mensilmente o trimestralmente.
* **Performance Fees (Commissioni di Performance / Overperformance)**: Calcolate secondo la metodologia **High-Water Mark (HWM)**: la commissione viene prelevata solo se il valore del fondo supera il massimo storico precedente.
* **Entry / Exit Fees (Commissioni di Sottoscrizione / Rimborso)**: Commissioni una-tantum applicate al momento dell'investimento o del disinvestimento.
* **Retrocession & Rebates**: Ripartizione contrattuale delle commissioni tra la fabbrica prodotto (SGR/Compagnia) e la rete distributiva (Banca collocatrice, Promotori finanziari, Broker).

---

## 6. Riconciliazione Finanziaria e Bancaria (Reconciliation Engines)

La riconciliazione è il processo contabile che garantisce che due set di dati indipendenti (es. il registro interno delle transazioni e l'estratto conto della banca depositaria o del circuito di carte) siano perfettamente allineati.

```
       SISTEMA INTERNO (Ledger)                BANCA DEPOSITARIA / ESTRATTO CONTO
    ┌─────────────────────────────┐               ┌─────────────────────────────┐
    │ TX_001 | 150.00 EUR | 10:00 │               │ MOV_88 | 150.00 EUR | 10:01 │
    │ TX_002 | 320.50 EUR | 10:15 │               │ MOV_89 | 320.50 EUR | 10:16 │
    │ TX_003 |  45.00 EUR | 10:30 │               │ MOV_90 |  90.00 EUR | 11:00 │ ◄── UNMATCHED!
    └──────────────┬──────────────┘               └──────────────┬──────────────┘
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          ▼
                             RECONCILIATION ENGINE
                             • 1-to-1 Match (Esatto)
                             • 1-to-N Match (Split/Cumulativi)
                             • Exception Management & Break Report
```

### Algoritmi e Strategie di Matching:
1. **Deterministic / Exact Match (1-to-1)**:
   * Matching basato su identificativi univoci: `Transaction ID`, `End-to-End ID (SEPA)`, `Reference Number` o combinazione esatta (`Data Contabile` + `Importo Esatto` + `Codice Divisa`).
2. **Aggregated Match (1-to-N o N-to-1)**:
   * Una singola voce di bonifico cumulativo (*batch payout*) ricevuta dalla banca corrisponde alla somma di $N$ singoli pagamenti nel registro interno.
3. **Fuzzy / Rule-Based Matching**:
   * Tolleranza su differenze di data contabile ($\pm 1-2$ giorni lavorativi per compensazioni bancarie), normalizzazione delle stringhe di causale o gestione di commissioni bancarie trattenute all'origine (*Net Settlement*).
4. **Exception Management (Squadrature e Sospesi)**:
   * Generazione automatica di record di "Break" o "Unmatched Items".
   * Workflow di investigazione per l'ufficio contabilità/operations con tracciamento degli storni e delle rettifiche.

---

## 7. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come progetteresti un sistema di riconciliazione ad alto volume scalabile e affidabile?*
  - **R**: Utilizzerei un'architettura asincrona a pipeline:
    1. **Ingestion & Normalization**: Ricezione degli estratti conto esterni (es. file ISO 20022 `camt.053` o tracciati CBI) tramite SFTP o Kafka, convertendoli in un modello canonico normalizzato.
    2. **Rule-Based Engine**: Una prima fase di matching deterministico esatto in-memory o tramite query batch indicizzate (su ID univoco, importo e valuta).
    3. **Two-Pass Matching**: Per i record non abbinati (*unmatched*), esecuzione di regole di matching aggregato (1-a-N) o con finestre temporali di tolleranza ($\pm 2$ giorni per valuta).
    4. **Persistenza & Idempotenza**: Gli abbinamenti vengono salvati con stato `RECONCILED` in transazione ACID, mentre i disallineamenti finiscono in una tabella/coda di `RECONCILIATION_EXCEPTIONS` per gestione manuale o rielaborazione successiva.

- *D: In un sistema di Order Management (OMS), perché il controllo di compliance Pre-Trade deve essere sincrono e a bassissima latenza?*
  - **R**: Perché la normativa (MiFID II) impone di prevenire violazioni dei limiti di rischio, scoperti non autorizzati o manipolazioni di mercato *prima* che l'ordine sia immesso sul mercato. Se il controllo fosse asincrono, l'ordine potrebbe essere già eseguito a mercato quando il controllo fallisce, esponendo la società a perdite finanziarie e sanzioni legali. Si implementa caricando le posizioni e i limiti in memoria (es. Redis o strutture in-memory clusterizzate) con algoritmi deterministici a latenza sub-millisecondo.

- *D: Qual è la differenza tra un fondo di accumulo e un fondo pensione nella gestione delle quote e del NAV?*
  - **R**: Entrambi dividono il patrimonio in quote valorizzate periodicamente al NAV. Tuttavia, nel fondo pensione la contribuzione è vincolata fino al pensionamento, gode di deducibilità fiscale specifica ed è suddivisa in comparti di rischio (garantito per il TFR silente vs azionario per i giovani). Inoltre, nella fase finale il montante accumulato viene convertito in rendita vitalizia applicando basi demografiche e coefficienti attuariali certificati da COVIP.

- *D: Come implementeresti il calcolo delle commissioni di performance con la regola dell'High-Water Mark (HWM)?*
  - **R**: L'High-Water Mark memorizza il valore NAV di picco storico al quale è stata pagata l'ultima commissione di performance. Ad ogni data di calcolo (es. fine anno), la commissione viene calcolata solo sulla quota di sovraperformance: $\text{Fee} = (\text{NAV}_{\text{attuale}} - \text{HWM}) \times \text{PerformanceRate} \times \text{Quote}$, e solo se $\text{NAV}_{\text{attuale}} > \text{HWM}$. Se l'anno si chiude con profitto, il valore dell'HWM viene aggiornato al nuovo NAV; se il fondo è in perdita, l'HWM resta invariato e il gestore non incassa nulla finché non recupera interamente la perdita precedente.



################################################################################
### CAPITOLO: 33. Distributed Systems Fundamentals
################################################################################

# 33. Distributed Systems Fundamentals

## Obiettivo
Capire i problemi fondamentali dei sistemi distribuiti e saper ragionare sui trade-off architetturali.

## CAP Theorem
- **Consistency**: ogni lettura osserva un valore coerente secondo il modello scelto
- **Availability**: ogni richiesta riceve una risposta, anche in presenza di failure
- **Partition Tolerance**: il sistema continua a operare nonostante una partizione di rete

In un sistema distribuito la partition tolerance è un requisito pratico; il trade-off riguarda principalmente consistency vs availability durante una partizione.

## Consistency Models
- Strong consistency
- Eventual consistency
- Causal consistency
- Read-your-writes
- Monotonic reads

## Problemi tipici
- Network partition
- Partial failure
- Message loss
- Duplicate messages
- Message reordering
- Timeout
- Retry storm
- Clock skew
- Split brain

## Distributed Coordination
- Leader election
- Quorum
- Consensus
- Distributed locking
- Fencing token

## Domande da colloquio
1. Cos'è il CAP theorem?
2. Perché la Partition Tolerance è praticamente inevitabile?
3. Strong consistency vs eventual consistency?
4. Cosa succede durante una network partition?
5. Come gestisci messaggi duplicati o fuori ordine?
6. Come implementeresti un distributed lock e quali problemi introduce?
7. Perché i timeout sono fondamentali nei sistemi distribuiti?

## Concetto chiave
Un sistema distribuito deve essere progettato assumendo che **la rete possa fallire** e che i failure possano essere parziali: un servizio può essere vivo mentre una sua dipendenza è irraggiungibile o lenta.



################################################################################
### CAPITOLO: 34. System Design
################################################################################

# 34. System Design

## Obiettivo
Preparare il ragionamento strutturato richiesto nelle domande di System Design da Senior Software Engineer / Architect.

## Framework di risposta
1. Functional requirements
2. Non-functional requirements
3. Assumptions e capacity estimation
4. API design
5. Data model e storage
6. High-level architecture
7. Scalability
8. Availability e reliability
9. Resilience
10. Security
11. Observability
12. Cost
13. Trade-offs

## Concetti fondamentali
- Horizontal vs vertical scaling
- Stateless vs stateful services
- Load balancing
- Caching
- CDN
- Queues e asynchronous processing
- Replication
- Partitioning e sharding
- Single Point of Failure
- Fault tolerance
- SLA, SLI, SLO, Error Budget

## Capacity Planning
Esempio: 1M requests/min ≈ 16.667 requests/sec.
Stimare quindi RPS, peak RPS, database throughput, storage growth, network bandwidth, cache size e CPU/memory.

## Architecture Styles
- Layered Architecture
- Modular Monolith
- Microservices
- Event-Driven Architecture
- Hexagonal Architecture
- Clean Architecture
- CQRS
- Event Sourcing

## Pattern architetturali
- API Gateway
- Backend for Frontend
- Saga
- Transactional Outbox
- Inbox Pattern
- Strangler Fig
- Anti-Corruption Layer

## Domande da colloquio
1. Progetta un e-commerce.
2. Progetta un payment system.
3. Progetta una API da 1M requests/min.
4. Progetta un sistema di order processing event-driven.
5. Quando useresti un modular monolith invece dei microservizi?
6. Come elimineresti un Single Point of Failure?
7. Come gestiresti un picco di traffico 10x?
8. Quali trade-off hai scelto e perché?

## Regola Senior
Non partire dalle tecnologie. Parti da requisiti, vincoli e trade-off, poi scegli le tecnologie che meglio supportano la soluzione.



################################################################################
### CAPITOLO: 35. Performance Engineering
################################################################################

# 35. Performance Engineering

## Obiettivo
Imparare a diagnosticare e migliorare le performance di applicazioni Java/Spring e sistemi distribuiti.

## Metriche
- Latency
- Throughput
- RPS
- Concurrency
- CPU utilization
- Memory utilization
- Error rate
- Saturation

## JVM
- Heap e allocation rate
- Garbage Collection
- GC pauses
- Thread contention
- Java Flight Recorder
- JDK Mission Control
- Thread dump
- Heap dump
- Profiling

## Database
- Slow queries
- EXPLAIN / EXPLAIN ANALYZE
- Index selectivity
- Cardinality
- Composite indexes
- Execution plan
- Lock contention
- Connection pool

## Load testing
- Load test
- Stress test
- Spike test
- Soak test
- Baseline

## Approccio al troubleshooting
1. Misurare il problema
2. Definire baseline e SLO
3. Identificare il bottleneck
4. Formulare un'ipotesi
5. Misurare/profilare
6. Applicare una modifica
7. Verificare il risultato

## Domande da colloquio
1. Un endpoint è diventato lento: da dove parti?
2. CPU bassa ma latency alta: cosa controlli?
3. Come analizzi un GC problem?
4. Come trovi una query lenta?
5. Come distingui CPU-bound da I/O-bound?
6. Come dimensioni un connection pool?

## Regola Senior
Non ottimizzare a intuito: **measure first, identify the bottleneck, change one thing, measure again**.



################################################################################
### CAPITOLO: 36. Advanced Microservices e Event Driven
################################################################################

# 36. Advanced Microservices e Event Driven

## Obiettivo
Portare la conoscenza dei microservizi dal livello tecnologico al livello architetturale.

## Microservice patterns
- API Gateway
- Backend for Frontend
- Saga
- Transactional Outbox
- Inbox Pattern
- Strangler Fig
- Anti-Corruption Layer

## Event Driven Architecture
- Event
- Command
- Producer
- Consumer
- Broker
- Event schema
- Event versioning
- Schema evolution
- Event replay
- Dead Letter Queue
- Eventual consistency

## Messaging semantics
- At-most-once
- At-least-once
- Exactly-once / effectively-once
- Ordering
- Deduplication
- Idempotency
- Retry
- Poison message
- Backpressure

## CQRS
Separare il modello di scrittura dal modello di lettura quando i requisiti lo giustificano.

## Event Sourcing
Lo stato viene ricostruito a partire dalla sequenza degli eventi. Valutare attentamente complessità, storage, replay e schema evolution.

## Inbox Pattern
Il consumer registra l'evento ricevuto prima di elaborarlo, permettendo di gestire duplicati in modo idempotente.

## Domande da colloquio
1. Quando useresti Saga?
2. Outbox vs 2PC?
3. Come gestisci un evento duplicato?
4. Come evolvi lo schema di un evento senza rompere i consumer?
5. CQRS quando è realmente utile?
6. Event Sourcing: vantaggi e svantaggi?
7. Come gestisci un consumer che non riesce a processare un messaggio?



################################################################################
### CAPITOLO: 37. DDD e Software Architecture
################################################################################

# 37. DDD e Software Architecture

## Domain-Driven Design
- Domain
- Subdomain
- Core Domain
- Supporting Subdomain
- Generic Subdomain
- Bounded Context
- Entity
- Value Object
- Aggregate
- Aggregate Root
- Domain Service
- Repository
- Domain Event
- Context Map
- Anti-Corruption Layer

## Architecture styles
- Layered Architecture
- Modular Monolith
- Microservices
- Hexagonal Architecture
- Clean Architecture
- Onion Architecture
- Event-Driven Architecture

## Dependency rule
Il dominio dovrebbe essere indipendente dai dettagli infrastrutturali. Le dipendenze verso infrastruttura e framework possono essere gestite tramite porte e adapter.

## Modular Monolith vs Microservices
Valutare:
- team ownership
- deployment independence
- scaling requirements
- domain boundaries
- operational complexity
- network failures
- consistency requirements

## Domande da colloquio
1. Cos'è un Bounded Context?
2. Entity vs Value Object?
3. Cos'è un Aggregate Root?
4. Quando useresti un Modular Monolith?
5. Clean vs Hexagonal Architecture?
6. Perché i microservizi non sono sempre la scelta migliore?



################################################################################
### CAPITOLO: 38. Advanced Security e API Governance
################################################################################

# 38. Advanced Security e API Governance

## Authentication e Authorization
- Authentication vs Authorization
- OAuth2
- OpenID Connect
- Authorization Code
- Client Credentials
- PKCE
- Access Token
- Refresh Token
- JWT
- JWKS
- RBAC
- ABAC

## Application Security
- TLS
- mTLS
- CORS
- CSRF
- XSS
- SQL Injection
- SSRF
- OWASP Top 10
- Secrets rotation
- Least privilege

## API Governance
- OpenAPI
- API lifecycle
- API versioning
- Backward compatibility
- Breaking changes
- Error model standardization
- Consumer compatibility
- Contract Testing

## Domande da colloquio
1. OAuth2 vs OIDC?
2. Authorization Code vs Client Credentials?
3. Perché PKCE?
4. JWT firmato vs cifrato?
5. Come gestisci la rotazione delle chiavi JWT?
6. Come introduci una breaking change in una API?
7. Come garantisci la compatibilità tra producer e consumer?



################################################################################
### CAPITOLO: 39. SRE Reliability e Chaos Engineering
################################################################################

# 39. SRE Reliability e Chaos Engineering

## SRE Fundamentals
- SLI: Service Level Indicator
- SLO: Service Level Objective
- SLA: Service Level Agreement
- Error Budget
- Availability
- Reliability
- Capacity Planning
- Toil

## Incident Management
- Detection
- Triage
- Mitigation
- Recovery
- Root Cause Analysis
- Blameless Postmortem
- Corrective Actions

## Disaster Recovery
- RTO
- RPO
- Backup
- Restore
- Failover
- Multi-AZ
- Multi-Region

## Chaos Engineering
Validare la resilienza introducendo fault controllati:
- service failure
- network latency
- packet loss
- database failure
- pod termination
- dependency failure

## Domande da colloquio
1. SLA vs SLO vs SLI?
2. Cos'è un Error Budget?
3. Come gestisci un incidente critico?
4. Come verifichi realmente la resilienza di un sistema?
5. RTO vs RPO?
6. Quando introdurresti Chaos Engineering?

## Regola Senior
La resilienza non va solo dichiarata nell'architettura: deve essere **misurata e validata** attraverso metriche, failure testing e incident review.



################################################################################
### CAPITOLO: 40. Messaging Technologies Advanced
################################################################################

# 40. Messaging Technologies — Advanced

## Obiettivo
Approfondire Kafka e RabbitMQ dal punto di vista di un Senior Software Engineer: delivery semantics, ordering, failure handling, scalability e trade-off architetturali.

## Kafka

### Architettura
- Broker
- Topic
- Partition
- Replica
- Leader / Follower
- ISR (In-Sync Replicas)
- Producer
- Consumer
- Consumer Group
- Offset

### Producer
Gli `acks` influenzano la durabilità:
- `acks=0`: nessuna attesa della conferma
- `acks=1`: conferma dal leader
- `acks=all`: conferma dopo le repliche ISR richieste

Concetti da conoscere:
- batching
- compression
- retries
- idempotent producer
- `linger.ms`
- `batch.size`

### Consumer
- Consumer groups
- Partition assignment
- Rebalancing
- Offset commit automatico/manuale
- `auto.offset.reset`
- Consumer lag

Un consumer group scala fino al numero di partition: oltre quel limite le istanze aggiuntive non ricevono partition da elaborare.

### Delivery semantics
- At-most-once
- At-least-once
- Exactly-once semantics
- Effectively-once tramite idempotenza/deduplicazione

In un sistema reale non bisogna confondere "exactly once" del broker con "exactly once" dell'effetto complessivo su DB e servizi esterni.

### Ordering
Kafka garantisce l'ordine all'interno della singola partition. Per mantenere l'ordine degli eventi di una stessa entità si usa normalmente una key stabile, ad esempio `customerId` o `orderId`.

### Retry e DLQ
Strategie possibili:
- retry immediato
- retry con backoff
- retry topic
- Dead Letter Topic
- gestione dei poison messages

Attenzione ai retry storm: un sistema già degradato può essere ulteriormente sovraccaricato dai retry.

## RabbitMQ

### Architettura
- Producer
- Exchange
- Binding
- Queue
- Consumer
- Routing key

Exchange principali:
- Direct
- Topic
- Fanout
- Headers

### Consumer
- Acknowledgement (`ack`)
- Negative acknowledgement (`nack`)
- Requeue
- Prefetch / QoS

Il prefetch limita quanti messaggi possono essere consegnati a un consumer senza acknowledgement, contribuendo al controllo del carico e della fairness.

### Retry e DLQ
Un messaggio che fallisce può essere:
- requeued
- inviato a una dead-letter exchange
- instradato verso una retry queue con TTL

La strategia deve evitare loop infiniti di retry.

## Kafka vs RabbitMQ

| Aspetto | Kafka | RabbitMQ |
|---|---|---|
| Modello | Distributed log | Message broker |
| Retention | Persistente/configurabile | Tipicamente fino al consumo |
| Replay | Nativo | Non è il modello principale |
| Routing | Topic/partition/key | Exchange/binding/routing key |
| Throughput | Molto elevato | Elevato, orientato al messaging |
| Ordering | Per partition | Per queue, con limitazioni dovute alla concorrenza |
| Caso tipico | Event streaming | Task queue / routing |

### Come scegliere
Usare Kafka quando servono event streaming, alto throughput, consumer multipli indipendenti, retention e replay.

Usare RabbitMQ quando servono routing sofisticato, task queue, acknowledgement e gestione fine della consegna dei messaggi.

## Pattern comuni
- Transactional Outbox
- Inbox Pattern
- Idempotent Consumer
- Competing Consumers
- Dead Letter Queue/Topic
- Retry with Backoff
- Event Notification
- Event-Carried State Transfer

## Esempio: pagamento
`Payment Service` salva la transazione e un evento `PaymentAuthorized`. Con Transactional Outbox, DB update ed evento vengono registrati nella stessa transazione. Un publisher pubblica successivamente l'evento su Kafka. I consumer di accounting, notification e reconciliation elaborano l'evento in modo idempotente.

## Domande da colloquio
1. Kafka è una queue o un distributed log?
2. Cosa succede durante un consumer rebalance?
3. Come garantisci l'ordine degli eventi?
4. Cosa significa `acks=all`?
5. At-least-once vs exactly-once?
6. Come gestisci un messaggio che fallisce continuamente?
7. Come eviti duplicate processing?
8. Quando preferisci RabbitMQ a Kafka?
9. Come dimensioni le partition Kafka?
10. Come monitori il consumer lag?
11. Come implementi retry senza creare un retry storm?
12. Perché Transactional Outbox è utile in un microservizio?



################################################################################
### CAPITOLO: 41. Automated Testing Advanced
################################################################################

# 41. Automated Testing — Advanced

## Obiettivo
Approfondire il testing di applicazioni Java/Spring e sistemi distribuiti, con particolare attenzione a qualità, velocità della pipeline e fiducia nei rilasci.

## Test Pyramid

Livelli principali:
- Unit test
- Integration test
- Component test
- Contract test
- End-to-End test

La maggior parte dei test dovrebbe essere veloce e isolata; i test più costosi e realistici devono essere usati dove aggiungono realmente valore.

## Unit Testing
Con JUnit 5 e Mockito:
- testare una singola unità
- mock delle dipendenze esterne
- verificare comportamento e risultati
- evitare di testare dettagli implementativi inutili

### Esempio
```java
@ExtendWith(MockitoExtension.class)
class PaymentServiceTest {
    @Mock PaymentRepository repository;
    @InjectMocks PaymentService service;

    @Test
    void shouldCreatePayment() {
        // arrange
        // act
        // assert
    }
}
```

## Integration Testing
Serve a verificare l'integrazione reale tra componenti:
- Spring context
- database
- REST API
- messaging
- configurazione

Tecnologie utili:
- `@SpringBootTest`
- MockMvc
- WebTestClient
- Testcontainers
- WireMock

## Testcontainers
Permette di eseguire dipendenze reali in container durante i test, ad esempio:
- PostgreSQL
- MySQL
- Kafka
- RabbitMQ
- Redis

È preferibile a un database embedded quando si vogliono verificare comportamenti specifici del database reale.

## Contract Testing
Verifica che producer e consumer rispettino un contratto condiviso senza richiedere un test end-to-end completo.

Concetti:
- Consumer-driven contract
- Provider verification
- Backward compatibility
- API schema evolution

Strumenti comuni: Pact e Spring Cloud Contract.

## Messaging Testing
Per Kafka/RabbitMQ verificare:
- pubblicazione corretta
- consumo
- retry
- DLQ
- ordering quando richiesto
- idempotenza
- gestione degli errori

Con Testcontainers è possibile eseguire test contro un broker reale invece di mockare completamente la messaggistica.

## REST API Testing
Testare almeno:
- HTTP status
- response body
- validation
- authentication/authorization
- error handling
- backward compatibility
- timeout/error scenarios

## TDD e BDD
### TDD
Ciclo:
1. Red
2. Green
3. Refactor

### BDD
Descrive il comportamento dal punto di vista del business:
- Given
- When
- Then

BDD è particolarmente utile quando requisiti e comportamento devono essere condivisi tra business e team tecnico.

## CI/CD e Quality Gates
Una pipeline tipica:

`Build → Unit Tests → Static Analysis → Integration Tests → Contract Tests → Package → Deploy`

Quality gate possibili:
- test coverage
- SonarQube
- SAST
- dependency vulnerability scan
- contract verification

## Test Strategy per Microservizi
Non cercare di verificare tutto con E2E test. Combinare:
- unit test per business logic
- integration test per DB/framework
- contract test per API/eventi
- pochi E2E test per journey critici

## Domande da colloquio
1. Unit test vs integration test?
2. Quando useresti Testcontainers?
3. Perché evitare di mockare completamente il database?
4. Cos'è un consumer-driven contract?
5. Come testeresti un consumer Kafka?
6. Come testi retry e DLQ?
7. Qual è una buona test pyramid per microservizi?
8. TDD è sempre necessario?
9. Come integri i test nella CI/CD pipeline?
10. Come eviti test flaky?
11. Come decidi cosa testare con E2E?
12. Code coverage elevata significa automaticamente alta qualità?

## Regola Senior
Il valore del testing non è la percentuale di coverage in sé, ma la capacità della suite di **intercettare regressioni importanti rapidamente e in modo affidabile**.



################################################################################
### CAPITOLO: 42. Advanced Observability
################################################################################

# 42. Advanced Observability e OpenTelemetry

## Obiettivo
Passare dalla semplice raccolta di log e metriche a una strategia completa di osservabilità per sistemi distribuiti.

## I tre pilastri
- Logs
- Metrics
- Traces

L'obiettivo non è semplicemente raccogliere dati, ma poter rispondere rapidamente a domande come: **cosa è successo, dove, quando e perché?**

## Distributed Tracing
Una singola richiesta può attraversare API Gateway, microservizi, database e broker.

Concetti:
- Trace
- Span
- Parent/child span
- Trace ID
- Span ID
- Context propagation
- Sampling

Il Trace ID permette di correlare le diverse operazioni appartenenti alla stessa richiesta distribuita.

## OpenTelemetry
OpenTelemetry è uno standard/framework open source per generare, raccogliere e esportare telemetry.

Componenti/concepts:
- Instrumentation
- SDK
- Collector
- Exporter
- OTLP
- Traces
- Metrics
- Logs

L'OpenTelemetry Collector può ricevere telemetry dalle applicazioni, elaborarla e inoltrarla verso backend differenti senza legare il codice applicativo a un singolo vendor.

## Metrics
Metriche utili:
- request rate
- error rate
- latency p50/p95/p99
- CPU
- memory
- GC
- database connections
- queue depth
- Kafka consumer lag

### RED Method
Per i servizi:
- Rate
- Errors
- Duration

### USE Method
Per le risorse:
- Utilization
- Saturation
- Errors

## Logging
Best practice:
- structured logging
- correlation ID
- trace ID
- log levels appropriati
- evitare dati sensibili
- centralizzazione

## Alerting
Un alert dovrebbe rappresentare un problema che richiede un'azione.

Evitare alert basati esclusivamente su metriche tecniche prive di impatto sul servizio. Preferire alert collegati a SLO, error rate, latency e saturation.

## Observability in Microservices
Una catena tipica:

`Client → API Gateway → Service A → Kafka → Service B → Database`

La propagazione del context permette di seguire la transazione attraverso l'intera catena.

## Esempio di troubleshooting
Se la latency p99 di `PaymentService` aumenta:
1. verificare se aumenta anche l'error rate
2. controllare trace distribuiti
3. identificare lo span più lento
4. verificare DB, connection pool o chiamate esterne
5. correlare con deployment recenti
6. applicare mitigazione
7. verificare il ritorno ai valori SLO

## Domande da colloquio
1. Logs vs metrics vs traces?
2. Cos'è uno span?
3. Come propaghi un Trace ID tra microservizi?
4. Cos'è OpenTelemetry?
5. Perché usare un Collector?
6. Perché p95/p99 sono spesso più utili della media?
7. RED vs USE?
8. Come monitori il consumer lag Kafka?
9. Come costruisci un alert efficace?
10. Come indaghi una latency anomala in un sistema distribuito?



################################################################################
### CAPITOLO: 43. Advanced Infrastructure as Code
################################################################################

# 43. Advanced Infrastructure as Code

## Obiettivo
Approfondire Infrastructure as Code oltre la semplice conoscenza di Terraform, collegandola a CI/CD, sicurezza, governance e gestione degli ambienti.

## Terraform
Concetti fondamentali:
- HCL
- Resources
- Data sources
- Variables
- Outputs
- Locals
- Modules
- Providers
- State
- Remote state
- State locking
- Dependencies
- Drift

## Modules
I Terraform modules permettono di creare componenti riutilizzabili, ad esempio un modulo per un servizio ECS, una VPC o un database.

Un buon modulo dovrebbe avere interfaccia chiara, pochi input necessari, output significativi e versionamento controllato.

## State Management
Il Terraform state collega la configurazione dichiarativa alle risorse reali.

In team è opportuno utilizzare:
- remote backend
- locking
- encryption
- access control
- versioning
- backup/recovery dello state

Mai inserire secret direttamente nel repository o nello state senza considerare le implicazioni di sicurezza.

## Workflow
`terraform fmt → validate → plan → review → apply`

In CI/CD l'`apply` dovrebbe essere controllato e autorizzato, mentre il `plan` può essere prodotto automaticamente come artifact della pipeline.

## Environment Strategy
Possibili approcci:
- directory separate
- workspace
- repository separati
- moduli riutilizzabili + configurazioni per ambiente

L'obiettivo è evitare duplicazione mantenendo comunque isolamento e controllo tra dev, staging e production.

## Drift Detection
Il drift si verifica quando l'infrastruttura reale viene modificata al di fuori di Terraform.

Best practice: ridurre il Click-Ops e fare emergere il drift tramite `terraform plan` e controlli automatizzati.

## Infrastructure as Code nella CI/CD
Pipeline tipica:

`Git commit → validate → security scan → terraform plan → approval → terraform apply → smoke test`

Possibili controlli:
- policy as code
- cost estimation
- security scanning
- code review
- protected environments

## Terraform vs CloudFormation vs AWS CDK
- **Terraform**: multi-cloud, ampia ecosystem e modello dichiarativo.
- **CloudFormation**: servizio IaC nativo AWS.
- **AWS CDK**: definisce infrastruttura AWS usando linguaggi di programmazione e genera CloudFormation.

La scelta dipende da cloud strategy, competenze del team, governance e necessità di portabilità.

## Secrets
Terraform non deve essere usato come sistema di secret management. Integrare invece secret manager e IAM, limitando esposizione e privilegi.

## Domande da colloquio
1. Cos'è il Terraform state?
2. Perché serve il locking?
3. Come gestisci Terraform in un team?
4. Cos'è il drift?
5. Come strutturi dev/staging/prod?
6. Come integri Terraform in CI/CD?
7. Come gestisci i secret?
8. Terraform vs CloudFormation?
9. Quando preferiresti CDK?
10. Come impedisci modifiche manuali all'infrastruttura?
11. Come gestisci un `terraform apply` fallito a metà?
12. Come fai rollback dell'infrastruttura?

## Regola Senior
IaC non significa soltanto "creare risorse con Terraform": significa rendere l'infrastruttura **riproducibile, revisionabile, sicura, testabile e governata attraverso il ciclo di vita del software**.



################################################################################
### CAPITOLO: 44. OAuth2 OpenID Connect e JWT Advanced
################################################################################

# 44. OAuth2, OpenID Connect e JWT — Advanced

## Obiettivo
Approfondire authentication e authorization a livello Senior, distinguendo chiaramente OAuth2, OpenID Connect e JWT e collegandoli alle API e ai microservizi.

## OAuth 2.0
OAuth2 è un framework per delegare l'accesso a risorse protette.

Concetti:
- Resource Owner
- Client
- Authorization Server
- Resource Server
- Access Token
- Refresh Token
- Scope

### Authorization Code + PKCE
Flusso tipico per applicazioni user-facing:
1. client avvia l'autorizzazione
2. utente autentica e concede il consenso
3. authorization server restituisce un authorization code
4. client scambia il code per token
5. access token viene utilizzato verso il resource server

PKCE protegge il code exchange soprattutto nei client pubblici.

### Client Credentials
Utilizzato per machine-to-machine communication quando non esiste un utente coinvolto.

Esempio: `Payment Service → Fraud Service`.

## OpenID Connect
OIDC estende OAuth2 aggiungendo un livello standard di **autenticazione e identità**.

Concetti:
- Identity Provider
- ID Token
- UserInfo endpoint
- Claims
- Discovery
- JWKS

### OAuth2 vs OIDC
- OAuth2: autorizzazione/accesso a risorse
- OIDC: autenticazione/identità sopra OAuth2

## JWT
Un JWT normalmente contiene:
- Header
- Payload
- Signature

La firma garantisce integrità e autenticità del token, non riservatezza.

### Claims
Esempi:
- `iss`
- `sub`
- `aud`
- `exp`
- `iat`
- `scope`
- `roles`

### Validazione
Il Resource Server dovrebbe verificare almeno:
- firma
- issuer
- audience
- expiration
- eventuali scope/ruoli richiesti

## Access Token vs Refresh Token
L'access token viene utilizzato per accedere alle API e dovrebbe avere lifetime limitata.

Il refresh token permette di ottenere nuovi access token senza richiedere nuovamente il login, con policy di sicurezza e revoca appropriate.

## JWKS e Key Rotation
Il Resource Server può recuperare le chiavi pubbliche dall'endpoint JWKS dell'Identity Provider.

La rotazione delle chiavi deve permettere un periodo di sovrapposizione in cui sia possibile validare token firmati con la chiave precedente mentre i nuovi token usano la nuova chiave.

## Authorization
- RBAC: permessi associati a ruoli
- ABAC: decisione basata su attributi di utente, risorsa e contesto
- Scopes: permessi delegati tipicamente associati all'access token

## Security pitfalls
- token troppo longevi
- mancata validazione `aud`/`iss`
- secret hardcoded
- log di access token
- uso improprio di OAuth2 come autenticazione
- assenza di TLS
- gestione insicura dei refresh token

## API Security Architecture
`Client → API Gateway → Resource Server → Authorization Server`

Il Gateway può applicare rate limiting e policy comuni, mentre l'autorizzazione business-specific dovrebbe rimanere nel servizio che possiede il dominio.

## Domande da colloquio
1. OAuth2 vs OpenID Connect?
2. JWT è cifrato o firmato?
3. Authorization Code vs Client Credentials?
4. Perché usare PKCE?
5. Access token vs refresh token?
6. Come valida un Resource Server un JWT?
7. Cos'è JWKS?
8. Come gestisci key rotation?
9. RBAC vs ABAC?
10. Dove implementeresti authorization in una architettura a microservizi?



################################################################################
### CAPITOLO: 45. LDAP e Active Directory
################################################################################

# 45. LDAP e Active Directory

## Obiettivo
Comprendere come integrare applicazioni Java enterprise con directory aziendali come LDAP e Microsoft Active Directory, distinguendo autenticazione, ricerca delle identità e autorizzazione.

## LDAP
LDAP (Lightweight Directory Access Protocol) è un protocollo per interrogare e modificare directory gerarchiche.

Concetti fondamentali:
- Directory Server
- Entry
- DN (Distinguished Name)
- RDN (Relative Distinguished Name)
- Attribute
- Object Class
- Schema
- Base DN
- Bind
- Search
- Filter

Esempio concettuale:
```text
DC=company,DC=com
 ├── OU=Users
 │    ├── CN=Mario Rossi
 │    └── CN=Anna Bianchi
 └── OU=Groups
      ├── CN=Developers
      └── CN=Admins
```

## LDAP Authentication
Un'applicazione può autenticare un utente effettuando un bind con le sue credenziali oppure utilizzando un account tecnico per cercare l'utente e successivamente verificarne le credenziali.

Flusso tipico:
```text
User
  ↓ username/password
Application
  ↓ LDAP search
Directory
  ↓ user DN
Application
  ↓ bind/authentication
LDAP Server
  ↓ success/failure
Application
```

## Active Directory
Microsoft Active Directory Domain Services (AD DS) utilizza LDAP per l'accesso alla directory, ma offre anche altri meccanismi e servizi, tra cui Kerberos, DNS e gestione centralizzata di utenti, gruppi e computer.

Concetti da conoscere:
- Domain
- Domain Controller
- Organizational Unit (OU)
- Security Group
- User Principal Name (UPN)
- Service Account
- Group Policy
- Kerberos
- LDAP/LDAPS

## LDAP vs Active Directory
LDAP è principalmente un protocollo; Active Directory è una piattaforma directory completa di Microsoft che implementa LDAP e integra altri servizi di dominio.

## LDAPS e sicurezza
LDAP in chiaro espone le credenziali e i dati della directory. Per proteggere la comunicazione utilizzare:
- LDAPS (LDAP over TLS)
- LDAP con StartTLS
- certificati validati correttamente
- truststore Java configurato correttamente

Non disabilitare la verifica dei certificati per risolvere problemi TLS in produzione.

## Spring Security + LDAP
Spring Security può integrare LDAP come Authentication Provider.

Concetti:
- `LdapBindAuthenticationManagerFactory`
- LDAP search
- user DN patterns
- group search
- authorities
- password validation

Esempio concettuale:
```java
@Bean
AuthenticationManager ldapAuthenticationManager(BaseLdapPathContextSource contextSource) {
    LdapBindAuthenticationManagerFactory factory =
        new LdapBindAuthenticationManagerFactory(contextSource);
    factory.setUserSearchBase("ou=Users");
    factory.setUserSearchFilter("(uid={0})");
    return factory.createAuthenticationManager();
}
```

## Authentication vs Authorization
LDAP/AD può fornire l'identità e i gruppi dell'utente, ma l'applicazione deve decidere come trasformare quei gruppi in autorizzazioni applicative.

Esempio:
```text
AD Group: CN=Payment-Operators
          ↓
Application authority: PAYMENT_OPERATOR
          ↓
@PreAuthorize("hasAuthority('PAYMENT_OPERATOR')")
```

## Service Accounts
Per integrazioni applicative usare account tecnici dedicati con:
- privilegi minimi
- password/secret gestiti tramite secret manager
- rotazione delle credenziali
- audit degli accessi
- divieto di utilizzo di account personali

## Caching e disponibilità
LDAP può diventare una dipendenza critica. Valutare:
- connection pooling
- timeout
- retry controllati
- caching delle informazioni non sensibili quando appropriato
- fallback limitati
- monitoring della directory

Non usare retry aggressivi su LDAP: un Domain Controller degradato può essere ulteriormente sovraccaricato.

## Integrazione enterprise
Architettura tipica:
```text
Browser / Client
      ↓
API Gateway
      ↓
Spring Boot Application
      ↓
Spring Security
      ↓
LDAP / Active Directory
      ↓
Gruppi / Identità
```

In architetture moderne LDAP/AD può essere integrato anche con un Identity Provider che espone OAuth2/OIDC, evitando di propagare direttamente le credenziali LDAP alle applicazioni.

## Domande da colloquio
1. Cos'è LDAP?
2. LDAP e Active Directory sono la stessa cosa?
3. Cos'è un DN?
4. Differenza tra LDAP e LDAPS?
5. Cos'è un bind LDAP?
6. Come integreresti Active Directory con Spring Security?
7. Come trasformi i gruppi AD in ruoli applicativi?
8. Perché usare un service account?
9. Come gestisci timeout e indisponibilità del Domain Controller?
10. LDAP authentication vs OAuth2/OIDC: quando useresti ciascuno?
11. Come proteggeresti le credenziali LDAP?
12. Perché non conviene far dipendere ogni microservizio direttamente da AD?

## Regola Senior
LDAP/Active Directory è spesso un sistema di identità enterprise. In una nuova architettura è importante separare **identity provider, autenticazione e autorizzazione applicativa**, evitando di distribuire credenziali directory tra i microservizi.



################################################################################
### CAPITOLO: 46. Sicurezza J2EE SOA e API
################################################################################

# 46. Sicurezza applicativa in J2EE, SOA e API

## Obiettivo
Prepararsi alle domande sulla sicurezza applicativa nei sistemi Java enterprise tradizionali (J2EE/Jakarta EE), nelle architetture SOA e nelle moderne API REST/microservizi.

## 1. Security principles
I principi fondamentali sono:
- Authentication
- Authorization
- Confidentiality
- Integrity
- Availability
- Accountability / Auditing
- Least Privilege
- Defense in Depth
- Secure by Design
- Fail Secure

Distinguere sempre **chi è l'utente** da **cosa è autorizzato a fare**.

## 2. Sicurezza J2EE / Jakarta EE
Nei sistemi enterprise Java tradizionali la sicurezza può essere applicata a livello di container e applicazione.

Concetti:
- Servlet authentication
- Container-managed security
- Security constraints
- Roles
- JAAS
- Security realms
- JACC
- `web.xml`
- declarative security
- programmatic security

Esempio concettuale:
```xml
<security-constraint>
    <web-resource-collection>
        <web-resource-name>Payments</web-resource-name>
        <url-pattern>/payments/*</url-pattern>
    </web-resource-collection>
    <auth-constraint>
        <role-name>PAYMENT_OPERATOR</role-name>
    </auth-constraint>
</security-constraint>
```

L'idea fondamentale è separare la configurazione delle policy di sicurezza dal codice business quando il modello container-managed è appropriato.

## 3. JAAS
Java Authentication and Authorization Service permette di separare il processo di autenticazione dall'applicazione attraverso LoginModule e Subject/Principal.

Concetti da conoscere:
- Subject
- Principal
- LoginContext
- LoginModule
- authentication
- authorization

È soprattutto importante come conoscenza dei sistemi Java enterprise/legacy; nelle architetture moderne è spesso sostituito o affiancato da Spring Security, OAuth2/OIDC e Identity Provider esterni.

## 4. SOA Security
In una Service-Oriented Architecture i servizi possono essere SOAP/XML o altri protocolli enterprise.

Principali rischi:
- intercettazione del traffico
- message tampering
- replay attack
- impersonation
- XML attacks
- eccessivi privilegi
- service-to-service trust non controllato

Contromisure:
- TLS
- mutual TLS
- authentication
- authorization
- message-level security
- digital signatures
- encryption
- timestamps
- nonce/replay protection
- auditing

## 5. WS-Security
Per SOAP, WS-Security fornisce meccanismi di sicurezza a livello messaggio.

Concetti fondamentali:
- SOAP Header
- UsernameToken
- XML Signature
- XML Encryption
- Security Token
- Timestamp
- replay protection
- certificate-based authentication

### Transport vs Message Security
**TLS** protegge il canale di comunicazione.

**WS-Security** protegge il messaggio SOAP stesso e può mantenere le proprietà di integrità/autenticità anche quando il messaggio attraversa più intermediari.

Esempio architetturale:
```text
Client
  ↓ HTTPS
Gateway
  ↓ SOAP / WS-Security
Service A
  ↓ SOAP / WS-Security
Service B
```

## 6. SAML
SAML è uno standard XML per lo scambio di assertion relative a identità e autenticazione, molto usato in scenari enterprise SSO.

Concetti:
- Identity Provider
- Service Provider
- Assertion
- Authentication Statement
- Attributes
- SSO

Confronto:
- SAML: molto comune nell'enterprise e nelle integrazioni SSO legacy
- OIDC: approccio moderno basato su OAuth2/JSON/JWT, particolarmente adatto a web e API

## 7. API Security
Una API deve proteggere almeno:
- Authentication
- Authorization
- Input validation
- Rate limiting
- TLS
- Secrets
- Audit
- Error handling

Pattern comuni:
```text
Client
  ↓ TLS
API Gateway
  ↓ Authentication / Rate limiting
Resource Server
  ↓ Authorization
Business Service
  ↓
Database
```

## 8. API Authentication
Meccanismi da conoscere:
- API Key
- Basic Authentication
- OAuth2 Bearer Token
- JWT
- mTLS
- signed requests

In generale evitare Basic Authentication per nuove API se esistono alternative adeguate; usare sempre TLS quando vengono trasmesse credenziali o token.

## 9. OAuth2 / OIDC / JWT
### OAuth2
Framework per delegare l'accesso a risorse protette.

### OIDC
Estensione di OAuth2 per authentication e identity.

### JWT
Formato di token firmato che contiene claims.

Validare sempre:
- signature
- issuer
- audience
- expiration
- not-before quando applicabile
- scopes/roles

Non inserire dati sensibili inutili nei JWT e non confondere firma con cifratura.

## 10. Authorization
Possibili modelli:
- RBAC
- ABAC
- scope-based authorization
- resource-based authorization

Esempio:
```text
JWT
 ├── sub = user123
 ├── scope = payment.read payment.write
 └── roles = PAYMENT_OPERATOR
          ↓
Authorization policy
          ↓
POST /payments → payment.write
```

## 11. OWASP e minacce API
Conoscere almeno:
- Broken Access Control
- Injection
- Security Misconfiguration
- Cryptographic Failures
- Identification and Authentication Failures
- SSRF
- XSS quando esiste una componente browser
- insecure deserialization
- excessive data exposure
- mass assignment
- rate abuse

## 12. API Gateway e Security Boundary
Il Gateway può centralizzare:
- TLS termination
- authentication
- rate limiting
- request size limits
- routing
- audit/correlation ID

Ma non deve diventare l'unico punto di authorization: i microservizi devono verificare le autorizzazioni necessarie alle proprie risorse e regole di dominio.

## 13. Service-to-Service Security
In un'architettura a microservizi valutare:
- OAuth2 Client Credentials
- mTLS
- workload identity
- short-lived tokens
- least privilege
- secret rotation

Non usare un'unica credenziale condivisa da tutti i microservizi.

## 14. Input e output security
Validare:
- payload JSON/XML
- parametri URL
- headers
- file upload
- content type
- dimensioni massime

Per XML considerare:
- XXE
- entity expansion
- external entity access
- parser hardening

Non restituire stack trace, SQL exception o dettagli infrastrutturali al client.

## 15. Security logging e auditing
Registrare eventi rilevanti:
- login riusciti/falliti
- authorization failures
- modifiche ai privilegi
- accesso a dati sensibili
- operazioni amministrative
- eventi di sicurezza

Non loggare:
- password
- access token
- refresh token
- secret
- PAN completo o altri dati sensibili non necessari

## 16. Domande da colloquio
1. Come proteggeresti una applicazione J2EE?
2. Container-managed security vs programmatic security?
3. Cos'è JAAS?
4. Cos'è WS-Security?
5. TLS e WS-Security risolvono lo stesso problema?
6. XML Signature vs XML Encryption?
7. Cos'è SAML e quando lo useresti?
8. OAuth2 vs OIDC?
9. JWT è cifrato o firmato?
10. Come proteggi una REST API?
11. Dove metti authentication e authorization in una architettura con API Gateway?
12. Come proteggi la comunicazione tra microservizi?
13. Come previeni replay attack?
14. Come gestisci la rotazione dei secret e delle chiavi?
15. Come proteggeresti una SOAP API legacy?
16. Quali rischi specifici presenta XML?

## Scenario Senior
Supponiamo di dover integrare una nuova API REST con un sistema legacy SOAP/J2EE autenticato tramite Active Directory.

Una possibile architettura è:
```text
User / Client
      ↓ OAuth2 / OIDC
API Gateway
      ↓ JWT
REST Service
      ↓ service identity / mTLS
Integration Service
      ↓ WS-Security + TLS
Legacy SOAP/J2EE
      ↓
LDAP / Active Directory
```

Il punto importante non è usare una singola tecnologia ovunque, ma creare **security boundaries** chiari e tradurre correttamente identità, autorizzazioni e trust tra sistemi moderni e legacy.

## Regola Senior
La sicurezza non è una singola libreria o un filtro HTTP. È una proprietà dell'intera architettura: **identity, transport security, message security, authorization, secrets, input validation, auditing, monitoring e gestione del ciclo di vita delle credenziali** devono essere progettati insieme.

