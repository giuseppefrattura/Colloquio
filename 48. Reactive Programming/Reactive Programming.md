# 48. Reactive Programming

## Obiettivo
Capire quando e perché usare Reactive Programming in Java/Spring, con particolare attenzione a Project Reactor e Spring WebFlux.

## Reactive Programming
È un paradigma orientato a flussi asincroni di dati e alla propagazione degli eventi.

Concetti:
- asynchronous processing
- non-blocking I/O
- backpressure
- stream
- event-driven processing

## Project Reactor
Tipi principali:
- `Mono<T>`: zero o un elemento
- `Flux<T>`: zero o N elementi

Operatori comuni:
- `map`
- `flatMap`
- `filter`
- `zip`
- `concat`
- `merge`
- `switchIfEmpty`
- `onErrorResume`
- `retryWhen`

## Spring WebFlux
WebFlux è il framework reactive di Spring basato su Reactive Streams/Reactor.

È particolarmente utile quando il servizio gestisce molte operazioni I/O concorrenti e le dipendenze sono anch'esse non-blocking.

## Blocking vs Non-blocking
Architettura tradizionale:
```text
Request
  ↓
Thread
  ↓
Blocking DB call
  ↓
Response
```

Approccio reactive:
```text
Request
  ↓
Non-blocking pipeline
  ↓
Async DB / HTTP
  ↓
Response
```

Il vantaggio principale non è che una singola operazione diventa necessariamente più veloce, ma che le risorse possono essere utilizzate più efficientemente sotto elevata concorrenza I/O.

## Backpressure
Backpressure permette al consumer di segnalare al producer quanto lavoro è in grado di sostenere, evitando che una sorgente produca dati a una velocità ingestibile.

Strategie:
- buffering
- dropping
- latest
- rate limiting
- batching

## Error Handling
In Reactor gli errori fanno parte del flusso.

Operatori importanti:
- `onErrorReturn`
- `onErrorResume`
- `onErrorMap`
- `retryWhen`

Attenzione: retry indiscriminati possono amplificare un problema di una dipendenza già degradata.

## Reactive e Database
Un'applicazione WebFlux non diventa realmente non-blocking se usa driver JDBC bloccanti indiscriminatamente.

Per un percorso completamente reactive valutare:
- R2DBC per database relazionali
- Reactive MongoDB driver
- client HTTP non-blocking
- reactive messaging

## Reactive vs CompletableFuture
`CompletableFuture` è principalmente orientato alla composizione di operazioni asincrone singole.

Reactor aggiunge un modello più completo per stream, backpressure, composizione e gestione di flussi di eventi.

## Quando NON usare Reactive
Non scegliere WebFlux solo perché è "più moderno".

Valutare con attenzione se:
- la maggior parte delle dipendenze è blocking
- il carico è limitato
- il team non conosce il paradigma
- la complessità non porta benefici
- il problema è CPU-bound

## Domande da colloquio
1. Mono vs Flux?
2. Cos'è backpressure?
3. WebFlux è sempre più veloce di Spring MVC?
4. Perché JDBC può essere un problema in una pipeline reactive?
5. `map` vs `flatMap` in Reactor?
6. Come gestisci gli errori in Reactor?
7. Come implementi retry con backoff?
8. Reactive vs CompletableFuture?
9. Quando non useresti WebFlux?
10. Come progetteresti un servizio reactive che chiama tre API esterne?
