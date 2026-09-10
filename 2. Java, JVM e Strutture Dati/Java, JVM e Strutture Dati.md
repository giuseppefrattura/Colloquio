## 2. Java, JVM e Strutture Dati

### Cos'è e perché conta
È il pilastro fondamentale di qualsiasi ruolo da Senior Backend Developer. I colloqui tecnici approfondiscono non solo la sintassi di Java 8+, ma la comprensione intima del **funzionamento della JVM**, la scelta corretta delle **strutture dati** in termini di complessità computazionale (Big-O) e gestione della memoria, nonché la padronanza della programmazione funzionale e delle evoluzioni moderne del linguaggio.

---

### Cosa studiare

#### 1. Java 8+ Fondamentali e Programmazione Funzionale
- **Stream API**:
  - Operazioni intermedie (lazy): `filter`, `map`, `flatMap`, `distinct`, `sorted`, `peek`.
  - Operazioni terminali (eager): `collect`, `forEach`, `reduce`, `count`, `anyMatch`, `allMatch`, `findFirst`.
  - Collector avanzati: `Collectors.groupingBy`, `partitioningBy`, `joining`, `toMap`, `toUnmodifiableList`.
  - `parallelStream()`: quando ha senso (computazioni CPU-heavy senza lock o stato condiviso) e quando evitarlo (in ambienti servlet/Spring con thread pool condiviso ForkJoinPool.commonPool).
- **Optional API**:
  - Uso idiomatico come tipo di ritorno per metodi che possono non avere un valore (evitare `Optional` come parametro o come campo di entità JPA).
  - Evitare `.get()` diretto; preferire `.orElseGet(() -> ...)`, `.orElseThrow(() -> new NotFoundException(...))`, `.map()`, `.flatMap()`, `.ifPresentOrElse()`.
- **Lambda e Functional Interfaces (`java.util.function`)**:
  - Un'interfaccia funzionale ha **esattamente un metodo astratto** (annotata con `@FunctionalInterface`).
  - `Function<T, R>` (`T -> R`, metodo `apply`): trasformazione.
  - `Predicate<T>` (`T -> boolean`, metodo `test`): filtri e condizioni.
  - `Consumer<T>` (`T -> void`, metodo `accept`): esecuzione di effetti collaterali.
  - `Supplier<T>` (`() -> T`, metodo `get`): lazy evaluation e factory.
  - `BiFunction<T, U, R>`, `UnaryOperator<T>`, `BinaryOperator<T>`.
  - Creazione di functional interface custom per regole di business (es. `TransactionValidator`).
- **Method Reference**: sintassi compatta `Class::staticMethod`, `instance::method`, `Class::instanceMethod`, `Class::new`.

---

#### 2. Strutture Dati in Java (Java Collections Framework)

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

##### A. List — sequenza ordinata con duplicati
- **`ArrayList`**: backed da un array dinamico.
  - Accesso per indice: $O(1)$.
  - Inserimento in coda: $O(1)$ ammortizzato (quando l'array si riempie, viene allocato un nuovo array di dimensione $1.5\times$ e copiati gli elementi).
  - Inserimento/rimozione nel mezzo: $O(n)$ a causa dello shift di memoria (`System.arraycopy`).
  - Scelta predefinita nel 99% dei casi.
- **`LinkedList`**: lista doppiamente concatenata.
  - Inserimento/cancellazione se si possiede già il nodo: $O(1)$.
  - Accesso per indice: $O(n)$ (deve scorrere la catena di nodi).
  - Overhead di memoria elevato (ogni nodo alloca un oggetto con puntatori `prev` e `next`). Quasi sempre meno performante di `ArrayList` a causa della scarsa cache locality della CPU.

##### B. Set — elementi unici, nessun duplicato
- **`HashSet`**: backed internamente da una `HashMap`.
  - Operazioni `add`, `contains`, `remove`: $O(1)$ medio.
  - Nessun ordinamento garantito.
- **`LinkedHashSet`**: estende `HashSet` mantenendo una lista doppiamente concatenata tra gli elementi; preserva l'**ordine di inserimento**.
- **`TreeSet`**: backed da un albero rosso-nero (Red-Black Tree bilanciato).
  - Operazioni: $O(\log n)$.
  - Mantiene gli elementi ordinati secondo l'ordinamento naturale (`Comparable`) o un `Comparator` personalizzato.

**Comportamento sui duplicati**: il metodo `set.add(elem)` ritorna `false` se l'elemento è già presente e **non modifica il Set** (non lancia eccezioni).

**Contratto `equals()` e `hashCode()`**:
- Se due oggetti sono uguali secondo `equals()`, **devono** avere lo stesso `hashCode()`.
- Se due oggetti hanno lo stesso `hashCode()`, **non è detto** che siano uguali (collisione hash).
- Se si fa l'override di `equals()`, **è obbligatorio** fare l'override coerente di `hashCode()`. In caso contrario, inserendo l'oggetto in un `HashSet` o come chiave di una `HashMap`, si verificheranno comportamenti imprevedibili (oggetti duplicati ammessi o lookup falliti).

##### C. Map — coppie chiave-valore con chiavi uniche
- **`HashMap`**:
  - Operazioni `put`, `get`, `containsKey`: $O(1)$ medio.
  - Come funziona internamente: calcola `hash(key)`, determina l'indice del bucket (`index = (n - 1) & hash`). In caso di collisione, gli elementi formano una lista concatenata; se il numero di elementi nel bucket supera la soglia (TREEIFY_THRESHOLD = 8), la lista viene convertita in un albero rosso-nero ($O(\log n)$ nel caso peggiore anziché $O(n)$).
  - **Comportamento sui duplicati**: `map.put(key, val)` con chiave esistente **sovrascrive il valore precedente** e ritorna il vecchio valore.
  - Metodi utili: `putIfAbsent()`, `computeIfAbsent()`, `merge()`, `getOrDefault()`.
- **`LinkedHashMap`**: mantiene l'ordine di inserimento (o di accesso, ideale per implementare cache LRU).
- **`TreeMap`**: chiavi ordinate ($O(\log n)$), non ammette chiavi `null`.
- **`ConcurrentHashMap`**: thread-safe ad altissime prestazioni, non blocca l'intera mappa ma usa lock a livello di singolo bucket (striping/CAS) e letture lock-free.

##### D. Queue & Deque
- **`ArrayDeque`**: implementazione di coda/stack basata su array circolare ridimensionabile. Più efficiente e performante di `Stack` e `LinkedList`.
- **`PriorityQueue`**: coda con priorità basata su min-heap ($O(\log n)$ per inserimento ed estrazione). Utile per scheduler di task o elaborazione prioritaria di transazioni.

---

#### 3. Novità del Linguaggio Java Moderno (Java 17 & Java 21+)

##### A. `sealed` Classes e Interfaces (Java 17)
Permette di restringere esplicitamente quali classi o interfacce possono estendere o implementare un tipo:

```java
public sealed interface PaymentMethod
    permits CardPayment, WalletPayment, BankTransferPayment {
}

public final class CardPayment implements PaymentMethod { ... }
public final class WalletPayment implements PaymentMethod { ... }
public non-sealed class BankTransferPayment implements PaymentMethod { ... }
```
- Le sottoclassi ammesse devono essere esplicitamente marcate come `final` (chiusa), `sealed` (ulteriormente ristretta) o `non-sealed` (riaperta all'estensione).
- **Vantaggio**: garantisce al compilatore la conoscenza esaustiva di tutti i sottotipi, consentendo pattern matching su `switch` **senza bisogno del ramo `default`**:

```java
BigDecimal fee = switch (paymentMethod) {
    case CardPayment c -> c.getAmount().multiply(new BigDecimal("0.02"));
    case WalletPayment w -> BigDecimal.ZERO;
    case BankTransferPayment b -> new BigDecimal("0.50");
};
```

##### B. Java Records (Java 16+)
Classi dati immutabili e concise: generano automaticamente campi `private final`, costruttore canonico, getter (senza prefisso `get`), `equals()`, `hashCode()` e `toString()`. Ideali per DTO, eventi di dominio e chiavi composte.

```java
public record PaymentRequest(String transactionId, BigDecimal amount, String currency) {
    // Compact constructor per validazioni
    public PaymentRequest {
        Objects.requireNonNull(transactionId, "Transaction ID cannot be null");
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
    }
}
```

##### C. Pattern Matching (Java 16 - 21)
- Pattern matching per `instanceof`: `if (obj instanceof String s && !s.isEmpty()) { ... }`
- Pattern matching per `switch` con guard clause `when`.

##### D. Virtual Threads - Project Loom (Java 21)
- Thread leggeri gestiti direttamente dal runtime JVM anziché dal sistema operativo (OS thread).
- Permettono di scalare ad **alta concorrenza con codice sincrono e bloccante** (es. chiamate HTTP verso banche o query DB bloccanti) senza esaurire i thread del sistema operativo e senza la complessità del paradigma reattivo (WebFlux).
- Adatti per carichi I/O-bound, non per computazioni CPU-intensive.

---

#### 4. JVM Internals: Architettura della Memoria e Garbage Collection

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

##### A. Struttura della Memoria JVM
- **Heap**: memoria in cui risiedono tutti gli oggetti istanziati (`new`) e le istanze dei Bean.
  - **Young Generation**: dove nascono i nuovi oggetti.
    - *Eden Space*: allocazione iniziale rapida.
    - *Survivor Spaces (S0 / S1)*: gli oggetti che sopravvivono a una Minor GC passano tra S0 e S1, incrementando un contatore di età (tenuring threshold).
  - **Old Generation (Tenured)**: accoglie gli oggetti sopravvissuti a diversi cicli di GC (es. Singleton di Spring, cache a lungo termine).
- **Thread Stack**: ogni thread ha il proprio stack privato di dimensione fissa (`-Xss`, tipicamente 1MB). Contiene i frame di esecuzione dei metodi, le variabili locali primitive e i puntatori/riferimenti agli oggetti nello Heap.
  - *Errore tipico*: `StackOverflowError` (ricorsione infinita).
  - *Errore Heap*: `OutOfMemoryError: Java heap space` (oggetti non deallocabili o leak).
- **Metaspace** (introdotto in Java 8 per sostituire il PermGen): alloca memoria nativa del sistema operativo per metadati delle classi caricate, bytecode dei metodi, string table e reflection info. Si espande dinamicamente salvo impostazione di `-XX:MaxMetaspaceSize`.

##### B. Garbage Collection (GC) e Algoritmi Moderni
Il Garbage Collector identifica automaticamente gli oggetti non più raggiungibili dal **GC Roots** (riferimenti attivi nello stack, thread in esecuzione, classi caricate, variabili statiche).

- **Fasi del GC**:
  1. *Mark*: identificazione degli oggetti vivi partendo dai GC Roots.
  2. *Sweep*: liberazione della memoria occupata dagli oggetti non raggiungibili.
  3. *Compact*: deframmentazione della memoria per garantire blocchi contigui.
- **I principali Garbage Collector**:
  - **G1 GC (Garbage-First)**: default da Java 9+. Suddivide lo Heap in centinaia di regioni uguali (1MB-32MB) e colleziona prioritariamente le regioni con più spazzatura ("Garbage First") per rispettare un tempo massimo di pausa target configurabile (`-XX:MaxGCPauseMillis`).
  - **ZGC (Z Garbage Collector)** e **Shenandoah**: GC a bassissima latenza (pause inferiori a 1ms, indipendenti dalla dimensione dello Heap anche con centinaia di GB). Eseguono quasi tutte le fasi di marking e compattazione in modo concorrente con i thread dell'applicazione. Fondamentale per sistemi di pagamento finanziari con requisiti rigorosi di latenza (SLA < 10ms).

##### C. JIT Compiler (Just-In-Time)
- La JVM esegue inizialmente il bytecode tramite interprete.
- Il **JIT Compiler** individua i blocchi di codice eseguiti frequentemente ("hotspots") e li compila a runtime in codice macchina nativo altamente ottimizzato.
- Ottimizzazioni principali: **Method Inlining** (elimina l'overhead di chiamata a metodo), **Loop Unrolling**, **Escape Analysis** (se un oggetto non "scappa" dal metodo, può essere allocato sullo stack o scalare in primitive eliminando l'allocazione su heap).

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Qual è la differenza tra `ArrayList` e `LinkedList` e quando useresti l'una o l'altra?*
  - **R**: `ArrayList` è basata su array contiguo con accesso $O(1)$ per indice e ottima cache locality; l'inserimento in mezzo è $O(n)$. `LinkedList` è doppiamente concatenata, ha accesso per indice $O(n)$ e inserimento $O(1)$ con puntatore noto, ma ha un forte overhead di memoria per ogni nodo e pessima cache locality. In pratica, quasi in ogni scenario enterprise moderno `ArrayList` è preferibile per throughput ed efficienza hardware.

- *D: Cosa succede se non si rispetta il contratto tra `equals()` e `hashCode()`?*
  - **R**: Se due oggetti sono uguali secondo `equals()` ma producono `hashCode()` diversi, inserendoli in un `HashSet` o come chiavi in una `HashMap` finiranno in bucket differenti. Di conseguenza, il Set ammetterà duplicati logici e il metodo `map.get(key)` fallirà restituendo `null` anche quando la chiave è logicamente presente.

- *D: Qual è la differenza tra Heap e Stack nella JVM?*
  - **R**: Lo Stack è per-thread, contiene i frame di esecuzione dei metodi, le variabili primitive locali e i riferimenti agli oggetti; la memoria viene allocata e liberata automaticamente e velocemente all'uscita dal metodo. L'Heap è condiviso da tutta l'applicazione, contiene tutti gli oggetti istanziati e i dati a lungo termine, ed è gestito dal Garbage Collector.

- *D: Come funzionano i Virtual Threads di Java 21 rispetto ai Platform Threads tradizionali?*
  - **R**: I Platform Threads mappano 1:1 sui thread del sistema operativo (costosi in memoria e limitati nel numero). I Virtual Threads sono gestiti dal runtime della JVM: quando un Virtual Thread incontra un'operazione di I/O bloccante (es. chiamata HTTP o query DB), viene "smontato" dal thread del sistema operativo (carrier thread), permettendo a quest'ultimo di servire altri Virtual Thread. Questo consente di gestire milioni di connessioni concorrenti con codice sincrono e leggibile.

---

### Come esercitarti
1. **Esercizio Stream e Collezioni**: scrivi un metodo che, data una lista di transazioni, raggruppi le transazioni per valuta, ne sommi gli importi totali, escluda le transazioni fallite e restituisca una `Map<String, BigDecimal>` ordinata per importo decrescente.
2. **Esercizio Strutture Dati**: implementa una semplice cache LRU (Least Recently Used) estendendo `LinkedHashMap` e facendo l'override di `removeEldestEntry()`.
