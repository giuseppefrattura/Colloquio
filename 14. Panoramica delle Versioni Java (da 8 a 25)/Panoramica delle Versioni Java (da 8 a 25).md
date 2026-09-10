## 14. Panoramica delle Versioni Java (da 8 a 25)

### Cos'è e perché conta
Il ruolo richiede "Java 8+", quindi è probabile che l'ambiente di produzione sia su una versione LTS consolidata (8, 11, 17, forse 21) più che sull'ultimissima release. Questa panoramica serve soprattutto per orientarti rapidamente su **cosa è stato introdotto e quando**, utile se ti chiedono "conosci le differenze tra Java 8 e versioni più recenti?" o per collegare le feature già approfondite nel documento (Stream, Optional, Records, Sealed Classes, Pattern Matching) alla loro versione di introduzione. Le versioni **LTS** (Long-Term Support) sono evidenziate perché sono quelle realisticamente in uso in ambito enterprise.

### Le versioni, in sintesi

**Java 8 (2014) — LTS**
- Lambda expression e functional interface (approfondito nel punto 2)
- Stream API per elaborazione dati in stile funzionale
- `Optional<T>`
- Nuova Date/Time API (`java.time`)
- Metodi `default` e `static` nelle interfacce

**Java 9 (2017)**
- Module System (JPMS) — Project Jigsaw
- JShell (REPL interattivo)
- Miglioramenti a Stream, Optional, CompletableFuture

**Java 10 (2018)**
- Local Variable Type Inference (`var`)
- Miglioramenti al Garbage Collector (G1 parallelo)

**Java 11 (2018) — LTS**
- HTTP Client API standardizzata
- `var` usabile nei parametri lambda
- Rimozione di Java EE e CORBA
- Nuovi metodi `String` (`isBlank()`, `strip()`, `repeat()`)

**Java 12 (2019)**
- Switch Expressions (preview)
- Shenandoah GC (sperimentale)

**Java 13 (2019)**
- Text Blocks (preview)
- Switch Expressions migliorate

**Java 14 (2020)**
- Switch Expressions (standard)
- Records (preview)
- Pattern Matching for `instanceof` (preview)
- Helpful NullPointerException (messaggi di errore più precisi)

**Java 15 (2020)**
- Text Blocks (standard)
- Sealed Classes (preview) — approfondito nel punto 7
- Hidden Classes

**Java 16 (2021)**
- Records (standard)
- Pattern Matching for `instanceof` (standard)
- Vector API (incubator)

**Java 17 (2021) — LTS**
- Sealed Classes (standard)
- Pattern Matching for `switch` (preview)
- Rimozione RMI Activation, Applet API deprecata

**Java 18 (2022)**
- UTF-8 come charset predefinito
- Simple Web Server

**Java 19 (2022)**
- Virtual Threads (preview) — Project Loom
- Structured Concurrency (incubator)
- Pattern Matching for `switch` (secondo preview)

**Java 20 (2023)**
- Continuazione preview di Virtual Threads e Structured Concurrency
- Record Patterns (secondo preview)

**Java 21 (2023) — LTS**
- Virtual Threads (standard) — probabilmente la feature più rilevante degli ultimi anni per applicazioni backend ad alta concorrenza
- Pattern Matching for `switch` (standard) — usato nell'esempio con `sealed` nel punto 7
- Record Patterns (standard)
- Sequenced Collections
- Structured Concurrency (preview)
- Generational ZGC

**Java 22 (2024)**
- Statement prima di `super()` nei costruttori
- Unnamed Variables & Patterns
- Foreign Function & Memory API (standard)

**Java 23 (2024)**
- Markdown in Javadoc
- Structured Concurrency (terzo preview)

**Java 24 (2025)**
- Class-File API (standard)
- Miglioramenti a Structured Concurrency e Scoped Values
- Quantum-resistant algorithms (preview)

**Java 25 (2025) — LTS**
La LTS successiva a Java 21, con diverse JEP focalizzate su sintassi più pulita, concorrenza più sicura, workflow di sicurezza semplificati e performance di startup/runtime più veloci:
- Generational Mode dello Shenandoah GC promossa da sperimentale a feature di prodotto, con miglior efficienza di memoria e consistenza dei pause-time
- Scoped Values finalizzati come alternativa a `ThreadLocal`
- Semplificazione della creazione dell'AOT cache tramite comandi unificati, per ridurre l'attrito nell'ottimizzazione dello startup
- Profiling a livello di metodo per ottimizzare la compilazione AOT
- Compact Object Headers come feature stabile
- Pattern matching esteso ai tipi primitivi in `switch`/`instanceof`

### Le tappe davvero rilevanti per un colloquio "Java 8+"

Se il tempo per ripassare è limitato, concentrati su queste, in ordine di probabilità che emergano:
1. **Java 8**: è la base del ruolo, va padroneggiata a fondo (già coperta nel punto 2)
2. **Java 11**: prima LTS successiva, spesso il target minimo in molte aziende che sono migrate da 8
3. **Java 17**: LTS molto diffusa oggi, introduce Sealed Classes e consolida Records — buona da conoscere anche solo concettualmente
4. **Java 21**: LTS più recente, la novità più "importante" da menzionare se emerge il tema sono i **Virtual Threads**, perché risolvono un problema concreto (gestire migliaia di connessioni concorrenti senza il costo di un thread OS per ciascuna) particolarmente rilevante in sistemi ad alto throughput come i pagamenti

### Come esercitarti
Prepara una frase che colleghi Java 8 al presente: "conosco bene le feature di Java 8 richieste dal ruolo, e mi tengo aggiornato anche sulle versioni successive — ad esempio i Virtual Threads di Java 21 sarebbero rilevanti in un sistema ad alta concorrenza come questo, se in futuro si valutasse un aggiornamento della piattaforma." Mostra sia solidità sui requisiti richiesti sia curiosità verso l'evoluzione del linguaggio, qualità esplicitamente richiesta nella job description ("curiosità e propensione alla ricerca").
