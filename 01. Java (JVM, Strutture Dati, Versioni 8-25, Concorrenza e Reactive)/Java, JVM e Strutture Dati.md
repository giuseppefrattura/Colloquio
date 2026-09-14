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
