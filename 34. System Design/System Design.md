# 34. System Design

## Obiettivo
Preparare il ragionamento strutturato richiesto nelle domande di System Design da Senior Software Engineer / Architect.

## Framework di risposta
1. Functional requirements
2. Non-functional requirements
3. Assumptions e capacity estimation
4. API design
5. Data model e storage
6. High-level architecture
7. Scalability
8. Availability e reliability
9. Resilience
10. Security
11. Observability
12. Cost
13. Trade-offs

## Concetti fondamentali
- Horizontal vs vertical scaling
- Stateless vs stateful services
- Load balancing
- Caching
- CDN
- Queues e asynchronous processing
- Replication
- Partitioning e sharding
- Single Point of Failure
- Fault tolerance
- SLA, SLI, SLO, Error Budget

## Capacity Planning
Esempio: 1M requests/min ≈ 16.667 requests/sec.
Stimare quindi RPS, peak RPS, database throughput, storage growth, network bandwidth, cache size e CPU/memory.

## Architecture Styles
- Layered Architecture
- Modular Monolith
- Microservices
- Event-Driven Architecture
- Hexagonal Architecture
- Clean Architecture
- CQRS
- Event Sourcing

## Pattern architetturali
- API Gateway
- Backend for Frontend
- Saga
- Transactional Outbox
- Inbox Pattern
- Strangler Fig
- Anti-Corruption Layer

## Domande da colloquio
1. Progetta un e-commerce.
2. Progetta un payment system.
3. Progetta una API da 1M requests/min.
4. Progetta un sistema di order processing event-driven.
5. Quando useresti un modular monolith invece dei microservizi?
6. Come elimineresti un Single Point of Failure?
7. Come gestiresti un picco di traffico 10x?
8. Quali trade-off hai scelto e perché?

## Regola Senior
Non partire dalle tecnologie. Parti da requisiti, vincoli e trade-off, poi scegli le tecnologie che meglio supportano la soluzione.
