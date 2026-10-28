# 12. Apache Kafka

## Conservare una storia condivisa di eventi

Kafka è una piattaforma di **event streaming**: riceve flussi di eventi e li conserva in un log distribuito. Un evento rappresenta un fatto, come una transazione autorizzata. Consumer diversi possono usare lo stesso fatto per contabilità, notifiche e reportistica senza consumarlo l'uno al posto dell'altro.

Un **topic** è il contenitore logico del flusso. Le **partizioni** lo suddividono in sequenze ordinate, ospitate sui broker. Ogni record ha un **offset**, posizione nella propria partizione, non un numero globale per tutto il topic. Questa struttura consente letture parallele e ripresa da posizioni note.

## Producer, consumer e gruppi

Il **producer** pubblica; il **consumer** legge. Un **consumer group** divide le partizioni tra istanze della stessa elaborazione. Gruppi distinti hanno posizioni indipendenti, perciò il servizio notifiche non impedisce alla contabilità di leggere gli stessi record.

La **key** contribuisce alla scelta della partizione. Una chiave account ID può mantenere correlati gli eventi del conto se strategia e topologia restano coerenti. L'ordine garantito dal log è per partizione; parallelismo applicativo, retry o cambiamenti del partizionamento richiedono valutazioni ulteriori.

```java
@Service
public class TransactionEventPublisher {
    private final KafkaTemplate<String, TransactionEvent> kafkaTemplate;

    public TransactionEventPublisher(
            KafkaTemplate<String, TransactionEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void publish(TransactionEvent event) {
        kafkaTemplate.send("transaction-events", event.getAccountId(), event);
    }
}
```

L'esempio mostra chiave e topic, ma l'invio è asincrono: chi ha bisogno della conferma deve gestire il risultato. Non rende atomici il salvataggio del pagamento e la pubblicazione; per questo caso il capitolo 36 introduce la Transactional Outbox.

## Retention, compaction e replay

La **retention** stabilisce per quanto tempo o volume i record rimangono disponibili secondo la politica del topic. Il consumo non li rimuove immediatamente. Il **replay** legge nuovamente dati ancora presenti, utile per ricostruire una vista o correggere un'elaborazione.

La **log compaction** conserva progressivamente una rappresentazione dei valori per chiave, rimuovendo versioni precedenti secondo le sue regole. Non equivale a conservare per sempre tutta la storia: non è intercambiabile con un registro completo di audit. Retention e compaction vanno scelte in base al bisogno di recupero e ai costi.

## Confermare la lettura non conferma ogni effetto

Il consumer salva offset per riprendere dopo un riavvio. Un crash dopo l'effetto sul database e prima del commit dell'offset può ripetere l'elaborazione; confermare troppo presto può perderla. L'idempotenza collega un identificatore stabile all'effetto già applicato.

Le garanzie di consegna dipendono da configurazione e coordinamento. Non basta usare Kafka per rendere «exactly-once» un addebito presso un sistema esterno. Il capitolo 40 approfondisce ack, replica, commit, lag e retry; la [documentazione di Kafka](https://kafka.apache.org/42/design/design/) chiarisce il confine delle sue garanzie.

## Un caso da spiegare

Pubblica un evento di autorizzazione e descrivi come contabilità e riconciliazione lo leggono con gruppi distinti. Poi simula un crash dopo la scrittura contabile: spiega quale record verrà riletto e quale controllo impedirà una seconda registrazione.

## Dal flusso di ordini alla gestione dei guasti

Un `Order Service` pubblica `OrderCreated` sul topic `orders`; magazzino e notifiche lo leggono con **gruppi differenti**. In un gruppo ogni partizione è assegnata a un solo consumer alla volta: con tre partizioni e cinque consumer, almeno due restano inattivi per quel topic. Un ingresso o un'uscita dal gruppo può causare un **rebalance**, cioè la riassegnazione delle partizioni.

Usare `orderId` come key consente normalmente di collocare gli eventi dello stesso ordine nella stessa partizione. L'ordine vale dentro la partizione, non fra tutte le partizioni; cambiare il loro numero può cambiare la distribuzione delle chiavi. Anche elaborazioni parallele e retry possono influire sull'ordine degli effetti.

Con **at-least-once**, un crash dopo l'effetto ma prima del commit dell'offset può causare una nuova elaborazione. Il consumer deve essere idempotente: per esempio registra un `eventId` stabile con un vincolo univoco, nella stessa transazione dell'effetto sul database. La produzione idempotente e le transazioni Kafka supportano garanzie più forti in determinati flussi Kafka-to-Kafka, ma non rendono automaticamente atomiche chiamate a database, email o API esterne.

Per evitare il *dual write* fra database e Kafka, la **transactional outbox** salva ordine ed evento in una tabella outbox nella stessa transazione. Un processo separato pubblica l'evento e lo marca come inviato. Se si interrompe dopo la pubblicazione ma prima della marcatura può ripubblicarlo: l'idempotenza del consumer rimane necessaria. Il capitolo 36 approfondisce questo coordinamento.

**Risposta da colloquio:** «Kafka distribuisce eventi in topic e partizioni. L'ordine è per partizione, il parallelismo di un gruppo è limitato dalle partizioni e, con consegna at-least-once, progetto i consumer per tollerare duplicati».
