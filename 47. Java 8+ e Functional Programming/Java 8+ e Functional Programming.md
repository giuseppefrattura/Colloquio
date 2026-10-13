# 47. Java e programmazione funzionale

## Descrivere trasformazioni invece di gestire ogni passaggio

La programmazione funzionale aiuta a esprimere il calcolo come composizione di trasformazioni. Una **funzione pura** restituisce lo stesso risultato per gli stessi argomenti e non modifica lo stato esterno. Un **effetto collaterale**, o side effect, è invece una modifica osservabile, come scrivere su un file o aggiornare un conto. Gli effetti sono necessari, ma separarli dal calcolo rende quest'ultimo più facile da capire e verificare.

L'**immutabilità** impedisce di cambiare un valore dopo la sua costruzione. La **trasparenza referenziale** permette di sostituire un'espressione con il suo risultato senza cambiare il comportamento. Nel codice Java queste proprietà sono scelte progettuali: la presenza di lambda non le garantisce.

## Lambda e interfacce funzionali

Una **lambda** fornisce un comportamento per un'interfaccia funzionale, cioè un'interfaccia con un solo metodo astratto rilevante. `@FunctionalInterface` fa verificare il vincolo al compilatore. Diversamente da una classe anonima, una lambda non introduce un nuovo significato di `this`: usa quello del contesto esterno.

`Function<T,R>` trasforma un valore; `Predicate<T>` verifica una condizione; `Consumer<T>` esegue un'azione senza restituire un risultato; `Supplier<T>` produce un valore senza ricevere argomenti. `UnaryOperator<T>` trasforma un valore nello stesso tipo, mentre `BinaryOperator<T>` combina due valori dello stesso tipo. Una **method reference**, come `Payment::amount`, esprime in modo compatto un comportamento già disponibile.

I metodi `default` nelle interfacce forniscono un'implementazione ereditabile; i metodi `static` appartengono all'interfaccia stessa. Sono strumenti di evoluzione e organizzazione delle API, non prove di purezza del codice.

## Una pipeline Stream, passo per passo

Uno **Stream** descrive una pipeline di elaborazione, non un contenitore di dati. `filter` seleziona elementi, `map` li trasforma e `flatMap` trasforma ogni elemento in uno stream poi unisce i risultati. Per esempio, da una lista di ordini `map(Order::lines)` produce collezioni di righe; `flatMap(order -> order.lines().stream())` produce un unico flusso di righe.

`sorted` ordina e può richiedere di raccogliere molti elementi; `distinct` rimuove duplicati secondo l'uguaglianza. `peek` osserva gli elementi durante l'elaborazione, ma non è adatto a garantire un'operazione di business: l'elaborazione può interrompersi o essere ottimizzata.

Le operazioni intermedie sono **lazy**, cioè vengono elaborate quando un'operazione terminale richiede il risultato. `collect` costruisce un risultato come lista o mappa; `reduce` combina valori tramite un'operazione; `count` conta. `anyMatch`, `allMatch` e `findFirst` possono fermarsi appena il risultato è determinato. `forEach` esegue un'azione sugli elementi visitati. Uno stream consumato non può essere riutilizzato.

```java
BigDecimal total = payments.stream()
    .filter(Payment::isCompleted)
    .map(Payment::amount)
    .reduce(BigDecimal.ZERO, BigDecimal::add);
```

L'esempio assume importi nella stessa valuta e una politica di rappresentazione coerente. Sommare importi di valute diverse senza conversione sarebbe un errore di dominio, anche con una pipeline corretta.

## Rappresentare assenza, tempo e lavoro asincrono

`Optional<T>` rappresenta un risultato presente oppure assente. `map` trasforma il valore presente; `flatMap` evita Optional annidati. `orElseGet` calcola un'alternativa solo se necessaria, mentre l'argomento di `orElse` viene valutato comunque. `orElseThrow` rende esplicito un errore e `ifPresent` esegue un'azione se il valore esiste. `get()` senza una verifica sposta il problema a runtime. L'uso nei campi JPA o nei parametri va valutato con attenzione rispetto al contratto e agli strumenti.

`java.time` distingue un istante, una data e un orario locale o con zona; scegliere il tipo giusto evita ambiguità nei confini temporali. `CompletableFuture` compone risultati asincroni singoli, ma non rende automaticamente non bloccante una chiamata eseguita al suo interno.

## Parallelismo ed evoluzione del linguaggio

`parallelStream()` distribuisce lavoro su più task, ma introduce costi di suddivisione e coordinamento. Il beneficio dipende da volume, costo del calcolo e assenza di stato condiviso. Le riduzioni devono usare operazioni associative e identità corrette; vincoli d'ordine e chiamate bloccanti possono ridurre il vantaggio. Misura il risultato nel contesto dell'applicazione.

Il Java successivo a Java 8 aggiunge strumenti con scopi diversi: `var` inferisce tipi locali senza introdurre tipi dinamici; i record rappresentano aggregati di dati senza garantire immutabilità profonda; le sealed classes limitano le sottoclassi. Pattern matching e switch expressions rendono più esplicito il lavoro sui tipi e sui valori, mentre i text block facilitano testi multilinea. `HttpClient` e le API di String e Collections ampliano la libreria standard. I virtual thread supportano grandi quantità di lavoro concorrente in attesa di I/O; non accelerano da soli il calcolo CPU.

## Ripasso ragionato

Prendi una procedura che filtra pagamenti e ne somma le commissioni. Separa calcolo e salvataggio, poi confronta una versione imperativa con una a stream. Spiega dove servono effetti collaterali, come rappresenti l'assenza e perché il parallelismo sarebbe utile oppure superfluo.
