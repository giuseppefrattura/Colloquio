# 37. DDD e Software Architecture

## Domain-Driven Design
- Domain
- Subdomain
- Core Domain
- Supporting Subdomain
- Generic Subdomain
- Bounded Context
- Entity
- Value Object
- Aggregate
- Aggregate Root
- Domain Service
- Repository
- Domain Event
- Context Map
- Anti-Corruption Layer

## Architecture styles
- Layered Architecture
- Modular Monolith
- Microservices
- Hexagonal Architecture
- Clean Architecture
- Onion Architecture
- Event-Driven Architecture

## Dependency rule
Il dominio dovrebbe essere indipendente dai dettagli infrastrutturali. Le dipendenze verso infrastruttura e framework possono essere gestite tramite porte e adapter.

## Modular Monolith vs Microservices
Valutare:
- team ownership
- deployment independence
- scaling requirements
- domain boundaries
- operational complexity
- network failures
- consistency requirements

## Domande da colloquio
1. Cos'è un Bounded Context?
2. Entity vs Value Object?
3. Cos'è un Aggregate Root?
4. Quando useresti un Modular Monolith?
5. Clean vs Hexagonal Architecture?
6. Perché i microservizi non sono sempre la scelta migliore?
