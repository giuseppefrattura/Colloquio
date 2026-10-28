# 48. Programmazione reattiva

## Seguire flussi asincroni di dati

La programmazione reattiva descrive flussi di dati ed eventi che possono arrivare nel tempo. **Asincrono** significa che il risultato non deve essere disponibile subito al chiamante; **non bloccante** significa che il thread non resta occupato nell'attesa dell'I/O. Una chiamata JDBC eseguita su un executor è asincrona per il chiamante, ma continua a bloccare il thread che la esegue.

Il vantaggio può essere gestire molte attese con un numero contenuto di thread. Una singola query non diventa necessariamente più veloce e il lavoro CPU richiede comunque capacità di calcolo. Il modello va scelto in base al carico e alle dipendenze.

## Mono, Flux e operatori in Reactor

Project Reactor offre `Mono<T>` per un flusso di zero o un elemento e `Flux<T>` per zero o più elementi. Il completamento senza valori è diverso dal fallimento. Nelle comuni pipeline lazy, descrivere gli operatori non basta a eseguire il lavoro: occorre una sottoscrizione, spesso gestita dal framework web.

`map` trasforma il valore; `flatMap` compone un'altra elaborazione reattiva. Su un Flux, `flatMap` può intercalare risultati e non conserva necessariamente l'ordine originario. `concat` elabora sequenze una dopo l'altra, mentre `merge` consente di intercalarle. `zip` combina valori delle sorgenti e richiede che queste producano i valori necessari. `filter` seleziona gli elementi; `switchIfEmpty` offre un percorso alternativo al completamento senza valori.

```java
Mono<PaymentView> view = paymentClient.findById(paymentId)
    .switchIfEmpty(Mono.error(new PaymentNotFoundException(paymentId)))
    .map(PaymentView::from);
```

L'esempio è una pipeline illustrativa: tipi e client appartengono all'applicazione. L'alternativa segnala un pagamento assente; non nasconde gli errori di comunicazione del client.

## Backpressure: rendere esplicita la capacità

La **backpressure** permette al subscriber di indicare quanti elementi è pronto a ricevere nel protocollo Reactive Streams. Non garantisce che qualsiasi sorgente esterna rallenti: un produttore non controllabile richiede una politica di sovraccarico.

Il **buffering** accoda dati, ma deve avere un limite. Il **dropping** scarta elementi; la strategia **latest** conserva soltanto il valore più recente, utile per alcuni aggiornamenti di stato. Il rate limiting limita il ritmo e il batching raggruppa elementi per ridurre costi per messaggio. Per una transazione finanziaria non si può adottare uno scarto silenzioso come se fosse un aggiornamento grafico: la politica deve rispettare il dominio.

## Errori e tentativi come parte del flusso

Un segnale di errore termina normalmente la sequenza interessata. `onErrorReturn` sostituisce il fallimento con un valore; `onErrorResume` sceglie un'altra sequenza; `onErrorMap` traduce il tipo di errore. Un fallback deve rendere esplicita l'eventuale perdita di informazioni, invece di restituire un risultato che sembri valido.

`retryWhen` può sottoscrivere di nuovo la sorgente dopo un errore. Il nuovo tentativo può ripetere gli effetti dell'operazione: servono idempotenza, limiti e backoff con jitter. Il retry è adatto ad alcuni guasti temporanei, non a rendere valido un input errato.

## WebFlux e dipendenze bloccanti

Spring WebFlux supporta questo modello nel livello HTTP. L'**event loop** gestisce eventi e avanzamento delle operazioni: bloccarlo con una chiamata lenta impedisce di far progredire altre richieste. Un percorso non bloccante richiede client coerenti, come client HTTP reattivi, driver MongoDB reattivi o R2DBC per database relazionali.

Se si deve integrare codice bloccante, lo si isola su uno scheduler appropriato, come `boundedElastic`, con capacità e attese controllate. Questo conserva un confine utile, ma non elimina il costo del blocco. Per molti servizi con JDBC e flussi semplici, Spring MVC e virtual thread possono essere un'alternativa da misurare.

## Confrontare modelli sullo stesso problema

`CompletableFuture` compone principalmente risultati asincroni singoli. Reactor aggiunge un modello per flussi, domanda e operatori di composizione; in cambio richiede familiarità con sottoscrizioni, scheduler e propagazione degli errori. Il beneficio va confrontato con la complessità che il team dovrà mantenere.

Progetta un endpoint che chiama tre API esterne. Spiega quali risultati sono indispensabili, quali timeout hanno e se un fallimento consente una risposta parziale. Confronta una composizione reattiva e una soluzione con virtual thread usando lo stesso carico e gli stessi limiti: valuta latenza, memoria, errori e chiarezza del codice.

## Esempio: composizione non bloccante e scelta del modello

Nel codice imperativo tradizionale una query o una chiamata HTTP può lasciare il thread in attesa fino alla risposta. In un flusso non bloccante il thread può lavorare su altre operazioni mentre il risultato non è pronto:

```java
public Mono<OrdineDto> trovaOrdine(String id) {
    return ordineClient.trova(id)
        .flatMap(ordine -> pagamentoClient.trova(id)
            .map(pagamento -> combina(ordine, pagamento)));
}
```

L'esempio presume client reattivi e metodi applicativi appropriati. Una chiamata JDBC bloccante eseguita direttamente sull'event loop compromette il beneficio; se inevitabile, va isolata su uno scheduler per lavoro bloccante. La backpressure regola la domanda nell'ambito Reactive Streams, ma non obbliga ogni sistema esterno a rallentare.

| Aspetto | Virtual thread | Flusso reattivo non bloccante |
|---|---|---|
| Stile | Sequenziale e imperativo | Composizione asincrona di flussi |
| I/O | Il virtual thread può sospendersi durante molte attese | Il risultato viene elaborato quando disponibile |
| Librerie bloccanti | Spesso utilizzabili direttamente | Devono essere isolate o sostituite |
| Backpressure | Richiede limiti e meccanismi adeguati | Espressa tramite Reactive Streams |
| Caso tipico | Molte richieste I/O con codice imperativo | Streaming e composizione con controllo della domanda |

Nessuno dei due modelli aumenta automaticamente la capacità della CPU o del database. La scelta dipende dalle dipendenze, dalla natura dei flussi, dalla capacità del team e da misure sul carico effettivo. Il capitolo 01 approfondisce i virtual thread.

**Risposta da colloquio:** «Non-blocking libera il thread durante l'attesa; funziona bene per molta concorrenza I/O, purché l'intera catena e le politiche di sovraccarico siano progettate coerentemente».
