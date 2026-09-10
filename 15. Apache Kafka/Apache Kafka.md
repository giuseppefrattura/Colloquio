## 15. Apache Kafka

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
