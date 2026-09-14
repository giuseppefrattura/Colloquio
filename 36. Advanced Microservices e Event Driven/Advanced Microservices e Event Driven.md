# 36. Advanced Microservices e Event Driven

## Obiettivo
Portare la conoscenza dei microservizi dal livello tecnologico al livello architetturale.

## Microservice patterns
- API Gateway
- Backend for Frontend
- Saga
- Transactional Outbox
- Inbox Pattern
- Strangler Fig
- Anti-Corruption Layer

## Event Driven Architecture
- Event
- Command
- Producer
- Consumer
- Broker
- Event schema
- Event versioning
- Schema evolution
- Event replay
- Dead Letter Queue
- Eventual consistency

## Messaging semantics
- At-most-once
- At-least-once
- Exactly-once / effectively-once
- Ordering
- Deduplication
- Idempotency
- Retry
- Poison message
- Backpressure

## CQRS
Separare il modello di scrittura dal modello di lettura quando i requisiti lo giustificano.

## Event Sourcing
Lo stato viene ricostruito a partire dalla sequenza degli eventi. Valutare attentamente complessità, storage, replay e schema evolution.

## Inbox Pattern
Il consumer registra l'evento ricevuto prima di elaborarlo, permettendo di gestire duplicati in modo idempotente.

## Domande da colloquio
1. Quando useresti Saga?
2. Outbox vs 2PC?
3. Come gestisci un evento duplicato?
4. Come evolvi lo schema di un evento senza rompere i consumer?
5. CQRS quando è realmente utile?
6. Event Sourcing: vantaggi e svantaggi?
7. Come gestisci un consumer che non riesce a processare un messaggio?
