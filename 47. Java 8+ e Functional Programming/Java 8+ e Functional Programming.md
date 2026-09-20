# 47. Java 8+ e Functional Programming

## Obiettivo
Preparare le domande su Java 8 e sulle evoluzioni successive, con particolare attenzione a Stream API, lambda e principi di Functional Programming.

## Java 8
Conoscere approfonditamente:
- Lambda expressions
- Functional interfaces
- `@FunctionalInterface`
- Method references
- Stream API
- `Optional`
- Default methods
- Static methods nelle interfaces
- `java.time`
- `CompletableFuture`

## Functional Interfaces
Principali interfacce:
- `Function<T,R>`
- `Consumer<T>`
- `Supplier<T>`
- `Predicate<T>`
- `UnaryOperator<T>`
- `BinaryOperator<T>`

## Stream API
Operazioni intermediate:
- `filter`
- `map`
- `flatMap`
- `sorted`
- `distinct`
- `peek`

Operazioni terminal:
- `collect`
- `reduce`
- `forEach`
- `count`
- `anyMatch`
- `allMatch`
- `findFirst`

### map vs flatMap
`map` trasforma ogni elemento in un elemento; `flatMap` permette di trasformare e appiattire strutture annidate.

## Immutability e Side Effects
Il Functional Programming privilegia:
- funzioni pure
- immutabilità
- assenza di side effects
- composizione
- referential transparency

Gli stream sono più prevedibili quando le lambda evitano stato mutabile condiviso.

## Optional
Usare `Optional` principalmente per rappresentare l'assenza di un valore nei return type.

Evitare:
- `Optional` come field JPA
- `Optional` come parametro di metodo salvo casi particolari
- `get()` senza verifica

Preferire `map`, `flatMap`, `orElseGet`, `orElseThrow` e `ifPresent` quando appropriato.

## Parallel Streams
Non usare `parallelStream()` automaticamente. Valutare:
- costo delle operazioni
- dimensione del dataset
- CPU-bound vs I/O-bound
- thread pool
- ordering
- overhead
- thread safety

## Java moderno
Per Java 11+ e versioni successive conoscere anche:
- `var`
- nuove API Collections/String
- `HttpClient`
- records
- sealed classes
- pattern matching
- switch expressions
- text blocks
- virtual threads

## Domande da colloquio
1. Lambda vs anonymous class?
2. `map` vs `flatMap`?
3. Stream lazy evaluation: cosa significa?
4. `map` vs `peek`?
5. `reduce` vs `collect`?
6. Quando useresti `Optional`?
7. Perché evitare side effects negli stream?
8. Quando un parallel stream è controproducente?
9. Cos'è una functional interface?
10. Quali caratteristiche del Functional Programming sono utili nel codice Java enterprise?
