# 1. Java: JVM, Strutture Dati, Versioni (8-25), Concorrenza e Programmazione Reattiva
## Il problema da cui partire
La **JVM**, Java Virtual Machine, esegue il bytecode prodotto dal compilatore e gestisce memoria, caricamento delle classi e ottimizzazioni. Il **JDK**, Java Development Kit, aggiunge gli strumenti di sviluppo; il linguaggio e la macchina che lo esegue sono livelli distinti. Questa distinzione aiuta a separare un errore di modello, un uso scorretto delle librerie e un limite del runtime.
Consideriamo un servizio che elabora pagamenti concorrenti. La struttura dati influenza il costo degli accessi, il modello di concorrenza determina quali operazioni possono sovrapporsi e la gestione della memoria influenza pause e capacità. La notazione **Big-O** descrive come cresce il costo al crescere dell'input, non il tempo esatto in millisecondi. La **cache locality** riguarda invece quanto bene gli accessi sfruttano le cache della CPU: due soluzioni con complessità simile possono avere prestazioni differenti.
Un **thread** è un flusso di esecuzione; la concorrenza permette più lavori in corso, mentre il parallelismo li esegue contemporaneamente su risorse diverse. Questi termini accompagnano il capitolo e tornano nel confronto tra stream, Reactor e virtual thread.
## 1. Trasformazioni, assenza e comportamenti

### Seguire una pipeline Stream

Uno Stream descrive un'elaborazione degli elementi di una sorgente. `filter` conserva quelli che soddisfano un predicato; `map` trasforma ciascun elemento; `flatMap` produce e appiattisce sequenze. Da una lista di ordini puoi ottenere prima le liste delle loro righe oppure un unico flusso di righe: questa differenza spiega quando scegliere i due operatori.

Le operazioni intermedie sono **lazy**, cioè vengono elaborate quando un'operazione terminale richiede il risultato. `distinct` rimuove duplicati e `sorted` ordina, con possibili costi di memoria. `peek` osserva elementi visitati ma non deve essere il posto in cui garantire un addebito: ottimizzazioni e terminazioni anticipate possono cambiare ciò che viene visitato.

Le operazioni terminali consumano lo stream. `count` conta, `reduce` combina valori e `collect` costruisce una struttura di risultato. `anyMatch`, `allMatch` e `findFirst` possono terminare appena il risultato è determinato. `forEach` esegue un'azione; effetti su dati esterni richiedono attenzione a ordine e concorrenza. Dopo il consumo lo stream non si riutilizza.

Un **Collector** definisce come accumulare risultati. `groupingBy` raccoglie per chiave e `partitioningBy` separa secondo una condizione; `joining` concatena testi. `toMap` richiede una decisione quando più elementi generano la stessa chiave. `toUnmodifiableList` impedisce modifiche alla lista, senza rendere immutabili gli oggetti al suo interno.

### Rappresentare un valore assente

`Optional<T>` descrive un valore presente o assente, soprattutto come risultato di una ricerca. `map` trasforma il contenuto presente e `flatMap` compone un'altra ricerca senza annidare Optional. `orElseGet` produce l'alternativa soltanto se serve; l'argomento di `orElse` è valutato comunque. `orElseThrow` rende esplicito un errore e `ifPresentOrElse` distingue le due condizioni. `get()` senza controllo sposta il caso assente in un'eccezione runtime.

Optional non sostituisce ogni campo o parametro. Il contratto deve chiarire dove l'assenza è normale e dove costituisce un errore; strumenti di persistenza e serializzazione possono aggiungere altri vincoli.

### Passare un comportamento

Una lambda fornisce un comportamento per un'interfaccia funzionale. `@FunctionalInterface` permette al compilatore di verificare il vincolo di un solo metodo astratto rilevante. `Function<T,R>` trasforma un valore, `Predicate<T>` verifica una condizione, `Consumer<T>` esegue un'azione e `Supplier<T>` produce un valore senza argomenti.

`BiFunction<T,U,R>` riceve due argomenti; `UnaryOperator<T>` mantiene il tipo nella trasformazione; `BinaryOperator<T>` combina due valori dello stesso tipo. Una **method reference**, come `Payment::amount` o `Class::new`, riusa un comportamento già espresso da un metodo o costruttore. Il capitolo 47 mostra come composizione e immutabilità aiutino a rendere questi calcoli più prevedibili.

### Valutare il parallelismo

`parallelStream()` distribuisce parti del lavoro tra task, spesso attraverso il pool condiviso `ForkJoinPool.commonPool()`. Può aiutare con calcoli sufficientemente costosi e dati divisibili; suddivisione, coordinamento e ordine introducono overhead. Chiamate bloccanti e stato mutabile condiviso possono peggiorare il risultato o produrre errori. La presenza di un server web non determina da sola il divieto: conta il carico complessivo e come viene usato il pool condiviso.

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
### Sequenze e scelta della lista

Una `List` rappresenta una sequenza ordinata e ammette duplicati. `ArrayList` mantiene riferimenti in un array ridimensionabile: l'accesso per indice è costante e l'aggiunta in coda ha costo costante **ammortizzato**, cioè medio lungo una sequenza di operazioni anche se alcuni inserimenti richiedono una copia. Inserire nel mezzo sposta gli elementi successivi. La contiguità dei riferimenti favorisce spesso la cache della CPU; non significa che tutti gli oggetti referenziati siano contigui.

`LinkedList` collega nodi che contengono riferimenti al precedente e al successivo. Modificare la struttura con un nodo già raggiunto può costare poco, ma trovare il nodo per indice richiede attraversamento. Oggetti aggiuntivi e accessi indiretti hanno un costo reale: scegliere una lista non dipende soltanto dal costo teorico di un singolo inserimento.

### Unicità, uguaglianza e hash

Un `Set` rappresenta elementi unici. `HashSet` usa hashing e offre operazioni mediamente costanti; `LinkedHashSet` conserva l'ordine d'inserimento. `TreeSet` usa una struttura ordinata e confronti con `Comparable` o `Comparator`, con operazioni tipicamente logaritmiche. Nel set ordinato la relazione del confronto determina anche l'unicità prevista dalla struttura.

Il contratto tra `equals()` e `hashCode()` stabilisce che oggetti uguali devono avere lo stesso hash. Il contrario non vale: due oggetti diversi possono collidere. Un **bucket** è la porzione in cui la mappa raggruppa alcune chiavi in base all'hash. Se cambi i dati che determinano hash e uguaglianza dopo l'inserimento, la struttura può non trovare più la chiave nel punto atteso.

Per esempio, un identificatore immutabile di pagamento è spesso una chiave più prevedibile di un'entità il cui stato cambia durante l'elaborazione. Ridefinire `equals` senza un `hashCode` coerente viola le ipotesi delle strutture basate su hash. Inserire un elemento già presente normalmente restituisce `false`, senza aggiungerne una seconda copia.

### Associare chiavi e valori

Una `Map` associa una chiave unica a un valore. `HashMap` offre accessi mediamente costanti; inserire un nuovo valore per una chiave esistente sostituisce il precedente e lo restituisce. L'implementazione gestisce collisioni con strutture che possono cambiare in base a soglie e capacità: sono dettagli da distinguere dal contratto pubblico.

`LinkedHashMap` conserva ordine d'inserimento o d'accesso. Quest'ultimo aiuta a costruire una politica **LRU**, Least Recently Used, che rimuove ciò che non è stato usato più di recente. `TreeMap` mantiene chiavi ordinate; il trattamento di `null` dipende anche dal confronto adottato, quindi non si generalizza da un solo caso.

`ConcurrentHashMap` supporta accessi concorrenti. Metodi come `compute` o `putIfAbsent` offrono operazioni composte con garanzie precise; un ciclo separato `get` seguito da `put` non diventa atomico perché entrambi i metodi sono thread-safe. Per un contatore o un marcatore di pagamento bisogna ragionare sull'intera modifica desiderata.

### Organizzare il lavoro in coda

Una `Queue` descrive un modello di estrazione, mentre una `Deque` consente operazioni ai due estremi. `ArrayDeque` usa un array circolare ed è spesso adatta a code e pile locali. `PriorityQueue` ordina l'estrazione secondo priorità attraverso un **heap**, struttura che mantiene l'elemento estremo accessibile senza ordinare tutta la sequenza. Inserimento ed estrazione hanno costo tipicamente logaritmico; l'iterazione non restituisce necessariamente tutti gli elementi ordinati.

Il termine heap della struttura dati non coincide con l'heap della memoria JVM. Una coda di priorità può decidere quale lavoro iniziare, ma equità, limiti e sicurezza della concorrenza rimangono responsabilità ulteriori.

## 3. Panoramica delle Versioni Java (da Java 8 a Java 25 LTS)
```
                            TIMELINE DELLE VERSIONI JAVA LTS
    Java 8 (2014) ──► Java 11 (2018) ──► Java 17 (2021) ──► Java 21 (2023) ──► Java 25 (2025)
    • Lambda/Stream   • HTTP Client      • Sealed Classes   • Virtual Threads  • Scoped Values
    • Optional        • String utils     • Record standard  • Switch Pattern   • Gen-Shenandoah
    • Date/Time API   • var nei lambda   • Strong Encaps.   • Sequenced Coll.  • Compact Headers
```
### Sintesi delle Feature per Versione:
**Java 8 (LTS)**: Lambda, Stream API, `Optional`, Date/Time API (`java.time`), default/static methods nelle interfacce. **Java 9**: Module System (JPMS - Project Jigsaw), JShell REPL, miglioramenti a Stream e `CompletableFuture`. **Java 10**: Local Variable Type Inference (`var`). **Java 11 (LTS)**: Standard HTTP Client (HTTP/2 e WebSocket), `var` nei parametri lambda, rimozione moduli Java EE. **Java 14**: Switch Expressions standard, Helpful NullPointerExceptions.
**Java 16**: **Records** standard (classi dati con componenti finali, senza immutabilità profonda automatica), Pattern Matching per `instanceof`. **Java 17 (LTS)**: **`sealed` Classes & Interfaces** standard, rimozione RMI Activation, strong encapsulation degli internals JDK. **Java 21 (LTS)**: **Virtual Threads (Project Loom)**, Pattern Matching per `switch`, Record Patterns, **Sequenced Collections** (`getFirst()`, `reversed()`), Generational ZGC.
**Java 25 (LTS)**: **Scoped Values** (alternativa moderna e leggera a `ThreadLocal`), Generational Mode di Shenandoah GC promosso a standard, Compact Object Headers, Pattern matching sui tipi primitivi in terza preview: non è una funzionalità definitiva. La [pagina OpenJDK di JDK 25](https://openjdk.org/projects/jdk/25/) distingue le JEP definitive dalle preview.
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
**Vantaggio**: Consente il pattern matching su `switch` **senza bisogno del ramo `default`**, perché il compilatore verifica l'esaustività di tutti i casi a tempo di compilazione:
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
La **visibilità** stabilisce quando un thread può osservare le scritture di un altro; l'**atomicità** riguarda l'indivisibilità di un'operazione. `volatile` rende esplicite alcune garanzie di visibilità e ordinamento, ma non rende atomico un incremento composto. Una relazione **happens-before** nel Java Memory Model descrive garanzie tra azioni, non soltanto il loro ordine sul cronometro.
**CAS**, Compare-And-Swap, confronta un valore con quello atteso e lo sostituisce atomicamente se corrisponde. Un ciclo CAS può dover riprovare sotto contesa. `LongAdder` distribuisce gli aggiornamenti tra componenti per ridurre contesa, ma la lettura della somma non offre lo stesso contratto di un unico contatore atomico in presenza di aggiornamenti. **`synchronized`**: Mutua esclusione basata su intrinsic lock (monitor). Semplice ma rigido (nessun timeout, rischio di blocco indefinito).
**`ReentrantLock`**: Supporta timeout (`tryLock(timeout)`), fairness policy e lock interrompibili. **Operazioni Atomiche (CAS - Compare-And-Swap)**: `AtomicInteger`, `AtomicLong`, `AtomicReference`, `LongAdder` (ad altissimo throughput in scrittura). Garanzie atomiche dei metodi utilizzati, con possibili retry e contesa. Il contratto va verificato per l’operazione completa. **`ConcurrentHashMap`**: Letture lock-free e lock granulare solo sui singoli nodi di collisione.
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
**`Mono<T>`**: Emittente reattivo per **0 o 1 elemento** (publisher con un contratto distinto da `CompletableFuture`). **`Flux<T>`**: Emittente reattivo per **$0 \dots N$ elementi** (stream potenzialmente infinito). **Backpressure**: Il Subscriber comunica al Publisher quanti dati può ricevere (`request(n)`), rendendo esplicita la domanda. Sorgenti non controllabili e buffer senza limite richiedono comunque politiche di sovraccarico.
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
**Heap**: Spazio gestito per gli oggetti secondo il modello del runtime; alcune allocazioni possono essere eliminate dalle ottimizzazioni. I collector organizzano questo spazio in modi diversi. **Young Gen (Eden, S0, S1)**: Oggetti a vita breve. **Old Gen (Tenured)**: Oggetti sopravvissuti a più cicli di GC. **Thread Stack**: Privato per ciascun thread (`-Xss`), contiene variabili primitive locali e puntatori a oggetti.
**Metaspace**: Memoria nativa OS per metadati di classi caricate, bytecode e reflection info.
### Algoritmi di Garbage Collection:
**G1 GC (Default)**: Divide lo heap in regioni (1-32MB), recupera regioni secondo la propria strategia cercando di rispettare il tempo obiettivo, senza garantirlo `-XX:MaxGCPauseMillis`. **ZGC & Shenandoah**: Collector progettati per ridurre le pause usando lavoro concorrente con l’applicazione. Latenza, memoria e throughput devono essere misurati: il nome del collector non garantisce una soglia universale.
---
## 7. Reactive Programming vs Virtual Threads (Java 21)
| Caratteristica | Reactive Programming (WebFlux / Reactor) | Virtual Threads (Java 21 + Spring MVC) |
| :--- | :--- | :--- |
| **Stile di Codice** | Dichiarativo, a pipeline funzionale (`Mono/Flux`) | Imperativo sincrono e lineare (`try/catch`, sequenziale) |
| **Scalabilità I/O** | Altissima (non-blocking event loop su Netty) | Altissima (i thread virtuali si smontano durante I/O bloccante) |
| **Complessità & Debug** | Molto elevata: stack trace frammentati | Minima: stack trace standard lineari |
| **Thread Context / MDC**| Complesso (richiede `Reactor Context`) | Trasparente (`ThreadLocal` e Scoped Values nativi) |
| **Compatibilità Legacy**| Richiede driver reattivi (R2DBC, WebClient) | Usabile con molte API bloccanti, verificando limiti e comportamento delle librerie |
---
## 8. Domande tipiche a colloquio (e risposte da Senior)
*D: Qual è la differenza tra `ArrayList` e `LinkedList` e perché quasi sempre si sceglie `ArrayList`?*
**R**: `ArrayList` usa un array contiguo in memoria con accesso per indice in $O(1)$ e ottima cache locality CPU. `LinkedList` alloca oggetti sparsi collegati da puntatori: l'accesso per indice è $O(n)$, l'overhead di memoria per i puntatori è elevato e la frammentazione in memoria rende le prestazioni reali quasi sempre inferiori rispetto ad `ArrayList`.
*D: Come funzionano i Virtual Threads di Java 21 rispetto ai Platform Threads?*
**R**: I Platform Threads mappano 1:1 sui thread del sistema operativo (costosi in RAM ~1MB ciascuno e limitati nel numero). I Virtual Threads sono gestiti dal runtime della JVM con stack e stato gestiti dinamicamente: quando un Virtual Thread esegue un'operazione I/O bloccante (es. query SQL o chiamata HTTP), viene "smontato" dal carrier thread del sistema operativo, liberandolo per servire altri Virtual Thread. Questo consente milioni di connessioni concorrenti con codice sincrono e leggibile.
*D: Cosa succede se in un'applicazione Spring WebFlux esegui una chiamata JDBC bloccante o `Thread.sleep()`?*
**R**: WebFlux esegue su un Event Loop (Netty) con un numero contenuto di thread, determinato da runtime e configurazione. Bloccare uno di questi thread riduce la capacità di far progredire altre richieste e può aumentare le code. Per chiamare codice bloccante legacy in Reactor, occorre isolarlo esplicitamente su uno scheduler elastico separato (`.subscribeOn(Schedulers.boundedElastic())`).
---
## 9. Come esercitarsi

1. **Stream & Collections Mastery**: Scrivi un metodo che, data una lista di transazioni finanziarie, le raggruppi per valuta e stato, calcoli l'importo medio per gruppo, escluda i gruppi con meno di 5 transazioni e restituisca una mappa ordinata.

2. **Virtual Threads Benchmark**: Configura un'applicazione Spring Boot 3.2+ con `spring.threads.virtual.enabled=true` e verifica come un endpoint che simula un I/O bloccante da 200 ms gestisce 10.000 richieste concorrenti senza saturare il sistema operativo.
