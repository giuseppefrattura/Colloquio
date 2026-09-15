# 40. Messaging Technologies — Advanced

## Obiettivo
Approfondire Kafka e RabbitMQ dal punto di vista di un Senior Software Engineer: delivery semantics, ordering, failure handling, scalability e trade-off architetturali.

## Kafka

### Architettura
- Broker
- Topic
- Partition
- Replica
- Leader / Follower
- ISR (In-Sync Replicas)
- Producer
- Consumer
- Consumer Group
- Offset

### Producer
Gli `acks` influenzano la durabilità:
- `acks=0`: nessuna attesa della conferma
- `acks=1`: conferma dal leader
- `acks=all`: conferma dopo le repliche ISR richieste

Concetti da conoscere:
- batching
- compression
- retries
- idempotent producer
- `linger.ms`
- `batch.size`

### Consumer
- Consumer groups
- Partition assignment
- Rebalancing
- Offset commit automatico/manuale
- `auto.offset.reset`
- Consumer lag

Un consumer group scala fino al numero di partition: oltre quel limite le istanze aggiuntive non ricevono partition da elaborare.

### Delivery semantics
- At-most-once
- At-least-once
- Exactly-once semantics
- Effectively-once tramite idempotenza/deduplicazione

In un sistema reale non bisogna confondere "exactly once" del broker con "exactly once" dell'effetto complessivo su DB e servizi esterni.

### Ordering
Kafka garantisce l'ordine all'interno della singola partition. Per mantenere l'ordine degli eventi di una stessa entità si usa normalmente una key stabile, ad esempio `customerId` o `orderId`.

### Retry e DLQ
Strategie possibili:
- retry immediato
- retry con backoff
- retry topic
- Dead Letter Topic
- gestione dei poison messages

Attenzione ai retry storm: un sistema già degradato può essere ulteriormente sovraccaricato dai retry.

## RabbitMQ

### Architettura
- Producer
- Exchange
- Binding
- Queue
- Consumer
- Routing key

Exchange principali:
- Direct
- Topic
- Fanout
- Headers

### Consumer
- Acknowledgement (`ack`)
- Negative acknowledgement (`nack`)
- Requeue
- Prefetch / QoS

Il prefetch limita quanti messaggi possono essere consegnati a un consumer senza acknowledgement, contribuendo al controllo del carico e della fairness.

### Retry e DLQ
Un messaggio che fallisce può essere:
- requeued
- inviato a una dead-letter exchange
- instradato verso una retry queue con TTL

La strategia deve evitare loop infiniti di retry.

## Kafka vs RabbitMQ

| Aspetto | Kafka | RabbitMQ |
|---|---|---|
| Modello | Distributed log | Message broker |
| Retention | Persistente/configurabile | Tipicamente fino al consumo |
| Replay | Nativo | Non è il modello principale |
| Routing | Topic/partition/key | Exchange/binding/routing key |
| Throughput | Molto elevato | Elevato, orientato al messaging |
| Ordering | Per partition | Per queue, con limitazioni dovute alla concorrenza |
| Caso tipico | Event streaming | Task queue / routing |

### Come scegliere
Usare Kafka quando servono event streaming, alto throughput, consumer multipli indipendenti, retention e replay.

Usare RabbitMQ quando servono routing sofisticato, task queue, acknowledgement e gestione fine della consegna dei messaggi.

## Pattern comuni
- Transactional Outbox
- Inbox Pattern
- Idempotent Consumer
- Competing Consumers
- Dead Letter Queue/Topic
- Retry with Backoff
- Event Notification
- Event-Carried State Transfer

## Esempio: pagamento
`Payment Service` salva la transazione e un evento `PaymentAuthorized`. Con Transactional Outbox, DB update ed evento vengono registrati nella stessa transazione. Un publisher pubblica successivamente l'evento su Kafka. I consumer di accounting, notification e reconciliation elaborano l'evento in modo idempotente.

## Domande da colloquio
1. Kafka è una queue o un distributed log?
2. Cosa succede durante un consumer rebalance?
3. Come garantisci l'ordine degli eventi?
4. Cosa significa `acks=all`?
5. At-least-once vs exactly-once?
6. Come gestisci un messaggio che fallisce continuamente?
7. Come eviti duplicate processing?
8. Quando preferisci RabbitMQ a Kafka?
9. Come dimensioni le partition Kafka?
10. Come monitori il consumer lag?
11. Come implementi retry senza creare un retry storm?
12. Perché Transactional Outbox è utile in un microservizio?
