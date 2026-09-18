# ☕ Guida Definitiva al Colloquio per Senior Java Backend Developer

[![Java](https://img.shields.io/badge/Java-8%20--%2025%20LTS-orange.svg?logo=openjdk)](https://openjdk.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x-brightgreen.svg?logo=springboot)](https://spring.io/projects/spring-boot)
[![Cloud Native](https://img.shields.io/badge/Cloud-AWS%20%7C%20Kubernetes%20%7C%20Docker-blue.svg?logo=amazon-aws)](https://aws.amazon.com/)
[![CI/CD](https://img.shields.io/badge/Build-GitHub%20Actions%20CI-green.svg?logo=github-actions)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](#)

> **Un manuale completo, pragmatico e architetturale per superare con successo i colloqui tecnici per posizioni Senior, Lead, Staff Engineer e Solutions Architect in contesti Enterprise, FinTech, InsurTech e Mission-Critical.**

---

## 🎯 Perché questo Libro?

Nei colloqui tecnici moderni per posizioni **Senior**, non basta saper usare le annotazioni di Spring o ricordare a memoria la sintassi di Java. I Lead Architect e gli Hiring Manager cercano professionisti capaci di:

1. **Padroneggiare la JVM & Performance Engineering**: comprendere la memoria interna (Heap, Stack, Metaspace), gli algoritmi di Garbage Collection a bassa latenza (G1, ZGC, Shenandoah), il profiling con JFR/JMC e il modello di concorrenza hardware (Virtual Threads, CAS, Memory Visibility).
2. **Disegnare Sistemi Distribuiti Resilienti (System Design)**: applicare il Teorema CAP/PACELC, modelli di consistenza (Strong vs Eventual), pattern EIP, architetture a microservizi, consistenza transazionale distribuita (Saga, Outbox/Inbox), streaming di eventi (Kafka) e strategie di persistenza poliglotta (*Polyglot Persistence*).
3. **Padroneggiare Domain-Driven Design (DDD) & Clean Architecture**: modellare Bounded Context, Aggregates, Entities, Value Objects, Domain Events e separare nettamente il dominio tramite Architettura Esagonale (Ports & Adapters).
4. **Valutare i Trade-off Architetturali**: saper spiegare *perché* scegliere una soluzione rispetto a un'altra (es. *Lock Ottimistico vs Pessimistico*, *Virtual Threads vs Reactive WebFlux*, *SQL vs NoSQL*, *Kafka vs RabbitMQ/SQS*).
5. **Garantire Sicurezza Avanzata e Governance API**: implementare flussi OAuth2/OIDC (PKCE, Client Credentials), mTLS, protezione contro l'OWASP Top 10 e paradigmi Zero Trust.
6. **Governare il Ciclo di Vita del Software & SRE**: dal Test-Driven Development (TDD) e Refactoring continuo, alle pipeline di CI/CD, Containerizzazione, Kubernetes, IaC (Terraform), fino a SLI/SLO/SLA, Error Budget e Chaos Engineering.
7. **Esprimere un autentico Product Mindset**: collegare le scelte tecnologiche ai requisiti non funzionali (NFR), agli obiettivi di business (KPI, ROI) e padroneggiare il linguaggio dei **domini applicativi reali** (Pagamenti, Carte, Circuiti ISO 8583/20022, Polizze Vita/Danni, Fondi Pensione, OMS e Riconciliazioni contabili).
8. **Sfruttare l'Intelligenza Artificiale come Moltiplicatore**: integrare Coding Agents (Claude Code, Cursor, MCP) per accelerare test, refactoring e indagini, mantenendo un rigoroso controllo critico su sicurezza e conformità.

---

## 📖 Struttura dell'Opera (I 46 Capitoli)

Il percorso di studio è strutturato in **11 macro-aree logiche**, progettate per guidare il candidato dai fondamenti del linguaggio fino alla governance architetturale avanzata, all'ingegneria dei sistemi, ai domini di business, alla sicurezza enterprise e all'osservabilità.

```
                           MAPPA STRUTTURALE DELL'OPERA
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ ☕ PARTE 1: LINGUAGGI E PARADIGMI (Java Core, Concorrenza, Go & Scala)      │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 🗄️ PARTE 2: DATABASE, PERSISTENZA & CACHING (RDBMS, NoSQL, Redis, Flyway)   │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 🏛️ PARTE 3: ARCHITETTURA, DESIGN PATTERN E FRAMEWORK (SOLID, Spring, REST) │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 📨 PARTE 4: MESSAGGISTICA, STREAMING & SPECIALISTICO (Kafka, JMS, MQTT)     │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ ☁️ PARTE 5: CLOUD, CONTAINER & INFRASTRUTTURA (Docker, Kubernetes, AWS)     │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 🛠️ PARTE 6: TOOLING, TESTING, CI/CD, QUALITÀ & CODING IA (JUnit, Sonar, IA) │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 👥 PARTE 7: METODOLOGIE, PRODUCT MINDSET & SOFT SKILLS (Agile, ADR, C4)     │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 💳 PARTE 8: DOMINI DI BUSINESS (Pagamenti Digitali, Assicurazioni, Finanza) │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 📐 PARTE 9: SISTEMI DISTRIBUITI, SYSTEM DESIGN, DDD & SRE (Cap. 33 - 39)    │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 🔬 PARTE 10: DEEP-DIVE SPECIALISTICI (Messaging Adv, Testing Adv, OTel, IaC)│
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 🛡️ PARTE 11: IDENTITY & SICUREZZA ENTERPRISE (OAuth2/OIDC, LDAP/AD, J2EE/API)│
  └─────────────────────────────────────────────────────────────────────────────┘
```

---

### ☕ Parte 1: Linguaggi e Paradigmi di Programmazione
* **[01. Java (JVM, Strutture Dati, Versioni 8-25, Concorrenza e Reactive)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/01.%20Java%20%28JVM,%20Strutture%20Dati,%20Versioni%208-25,%20Concorrenza%20e%20Reactive%29/Java,%20JVM%20e%20Strutture%20Dati.md)**
  * *Stream API, Optional, Functional Interfaces, Collections Framework (complessità Big-O e contratto equals/hashCode), Panoramica Java 8 $\to$ 25 LTS (Sealed classes, Records, Pattern matching, Scoped values), Concorrenza (Thread pool, CompletableFuture, Virtual Threads), Programmazione Reattiva (Project Reactor, WebFlux), Architettura JVM e Garbage Collectors (G1, ZGC, Shenandoah).*
* **[02. Linguaggi Alternativi: Go e Scala (Paradigmi Funzionali)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/02.%20Linguaggi%20Alternativi:%20Go%20e%20Scala%20%28Paradigmi%20Funzionali%29/Linguaggi%20Alternativi:%20Go%20e%20Scala.md)**
  * *Go per sviluppatori Java: Structs, Duck typing, Goroutines e Channels (CSP), GC a bassa latenza. Scala: Pure Functional Programming, Case classes, ADT, Monadi (Option, Either, Try), Actor model (Akka/Pekko).*

---

### 🗄️ Parte 2: Database, Persistenza & Caching
* **[03. Database Relazionali, NoSQL e Strategie di Accesso](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/03.%20Database%20Relazionali,%20NoSQL%20e%20Strategie%20di%20Accesso/Database%20Relazionali,%20NoSQL%20e%20Strategie%20di%20Accesso.md)**
  * *Transazioni ACID, Livelli di Isolamento SQL, Locking Ottimistico vs Pessimistico, Oracle Database (CBO Execution Plan, Window Functions, PL/SQL), PostgreSQL (JSONB, GIN index), MySQL (InnoDB), Famiglie NoSQL (MongoDB, Cassandra LSM-Tree, Elasticsearch Inverted Index), Teorema CAP/PACELC, Matrice Polyglot Persistence, HikariCP.*
* **[04. Redis e Caching Distribuito](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/04.%20Redis/Redis.md)**
  * *Strutture dati in-memory, pattern Cache-Aside/Write-Through, Idempotency Store, Distributed Locking con Redlock, Rate Limiting.*
* **[05. Database Migration Software (Flyway e Liquibase)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/05.%20Database%20Migration%20Software%20%28Flyway%20e%20Liquibase%29/Database%20Migration%20Software%20%28Flyway%20e%20Liquibase%29.md)**
  * *Versioning degli schemi DB, migrazioni forward-only, compatibilità backward con Blue/Green deployment, rollback e lock di migrazione.*
* **[06. Strategie per la Gestione dei Database in Architetture a Microservizi](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/06.%20Strategie%20per%20la%20Gestione%20dei%20Database%20in%20Architetture%20a%20Microservizi/Strategie%20per%20la%20Gestione%20dei%20Database%20in%20Architetture%20a%20Microservizi.md)**
  * *Database-per-Service, Data Isolation, Dual Write Problem, Transactional Outbox Pattern, Saga Pattern (Orchestrata vs Coreografata), CQRS.*

---

### 🏛️ Parte 3: Architettura, Design Pattern e Framework Core
* **[07. Design Pattern, Principi SOLID e NFRs](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/07.%20Design%20Pattern%20e%20Principi%20SOLID/Design%20Pattern%20e%20Principi%20SOLID.md)**
  * *SOLID con esempi Java moderni, DRY, KISS, Law of Demeter, GoF Patterns (Strategy, Factory, Builder, Decorator, State), Requisiti Non Funzionali (NFR: Latenza p95/p99, SLA 99.99%, Throughput TPS), TDD (Red-Green-Refactor), BDD (Gherkin/Cucumber), Refactoring Continuo e Code Smells.*
* **[08. Spring & Spring Boot](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/08.%20Spring%20&%20Spring%20Boot/Spring%20&%20Spring%20Boot.md)**
  * *IoC Container, Dependency Injection (Constructor vs Field), Ciclo di vita dei Bean, Spring AOP e Proxy dinamici, `@Transactional` (Propagation e Rollback rules), Spring Data JPA (EntityGraph, N+1 fix), Spring Security (JWT Stateless, CSRF), Spring Integration & Enterprise Integration Patterns (EIP) vs Apache Camel.*
* **[09. API REST, Tecnologie Web, Sicurezza e Framework](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/09.%20API%20REST%20e%20RESTful%20Design/API%20REST%20e%20RESTful%20Design.md)**
  * *Evoluzione HTTP (HTTP/1.1 vs HTTP/2 Multiplexing vs HTTP/3 QUIC), Cookies (HttpOnly, Secure, SameSite), Stateful Session vs Stateless JWT (Token Rotation), CORS (Pre-flight OPTIONS) e CSRF, HTTP Caching (Cache-Control, ETag, CDN), Confronto Framework REST (Spring MVC, JAX-RS/Jersey, Dropwizard).*
* **[10. Microservizi: Concetti Fondamentali](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/10.%20Microservizi:%20Concetti%20Fondamentali/Microservizi:%20Concetti%20Fondamentali.md)**
  * *Decomposizione del dominio, Service Discovery, API Gateway, Circuit Breaker (Resilience4j), Distributed Tracing, Event-Driven Architecture.*
* **[11. WebSocket e Comunicazione Real-Time](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/11.%20WebSocket/WebSocket.md)**
  * *Protocollo Full-Duplex TCP, Handshake HTTP 101, STOMP su WebSocket, confronto con Server-Sent Events (SSE) e Long Polling.*

---

### 📨 Parte 4: Messaggistica, Streaming & Tecnologie Specialistiche
* **[12. Apache Kafka](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/12.%20Apache%20Kafka/Apache%20Kafka.md)**
  * *Architettura del Commit Log, Partizioni, Consumer Groups, Offset management, Garanzie di consegna (At-least-once, Exactly-once Idempotent Producer), KRaft consensus.*
* **[13. JMS (Java Message Service)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/13.%20JMS%20%28Java%20Message%20Service%29/JMS%20%28Java%20Message%20Service%29.md)**
  * *Code Point-to-Point (Queue) vs Publish/Subscribe (Topic), Acknowledgement modes, Transazioni XA su broker enterprise (ActiveMQ, IBM MQ).*
* **[14. Tecnologie Specialistiche: OSGi e MQTT](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/14.%20Tecnologie%20Specialistiche:%20OSGi%20e%20MQTT/OSGi%20e%20MQTT.md)**
  * *OSGi: Modularità dinamica, ClassLoader per bundle, MANIFEST.MF, Declarative Services. MQTT: Protocollo binario IoT leggero, Topic gerarchici con wildcards, Livelli QoS (0, 1, 2 a 4 vie), Retained Messages, Last Will and Testament (LWT).*
* **[15. Tecnologie Streaming, Media e Broadcast](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/15.%20Tecnologie%20Streaming,%20Media%20e%20Broadcast/Tecnologie%20Streaming,%20Media%20e%20Broadcast.md)**
  * *Media Pipeline End-to-End, Transcoding, HLS (Master/Media Playlist, chunks fMP4), MPEG-DASH, Adaptive Bitrate Streaming (ABR), Low-Latency HLS (LL-HLS), WebRTC sub-secondo, Content Protection DRM (Widevine, FairPlay via CENC), Server-Side Ad Insertion (SSAI).*
* **[16. Comparazioni: OpenShift vs Kubernetes, RabbitMQ vs Kafka](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/16.%20Comparazioni:%20OpenShift%20vs%20Kubernetes,%20RabbitMQ%20vs%20Kafka/Comparazioni:%20OpenShift%20vs%20Kubernetes,%20RabbitMQ%20vs%20Kafka.md)**
  * *Analisi dettagliata dei trade-off architetturali e matrici decisionali di scelta tecnologica.*

---

### ☁️ Parte 5: Cloud, Container & Infrastruttura
* **[17. Containerizzazione (Docker e OCI)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/17.%20Containerizzazione%20%28Docker%20e%20OCI%29/Containerizzazione%20%28Docker%20e%20OCI%29.md)**
  * *Architettura Docker, Layer caching, Multi-stage builds, Distroless images, ottimizzazioni JVM in container (Cgroups v2, `-XX:MaxRAMPercentage`).*
* **[18. Kubernetes](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/18.%20Kubernetes/Kubernetes.md)**
  * *Pod, Deployment, Service (ClusterIP, NodePort, LoadBalancer), Ingress, ConfigMap/Secret, Probes (Liveness, Readiness, Startup), HPA auto-scaling.*
* **[19. Architettura Cloud, Servizi AWS e IaC](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/19.%20Architettura%20Cloud/Architettura%20Cloud.md)**
  * *AWS Compute (EC2, ECS Fargate, EKS, Lambda SnapStart), Storage/DB (S3, RDS Multi-AZ, Aurora Global DB, DynamoDB), Networking (VPC, Subnets, NAT Gateway, Security Groups vs NACL, ALB), Messaging (SQS Standard/FIFO con DLQ, SNS Fan-out, EventBridge), Deployment Patterns (Blue/Green, Canary, Rolling, Disaster Recovery RTO/RPO), Infrastructure as Code (Terraform state locking, AWS CDK).*

---

### 🛠️ Parte 6: Tooling, Testing, CI/CD, Qualità e Coding IA
* **[20. Dependency Management (Maven e Gradle)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/20.%20Dependency%20Management%20%28Maven%20e%20Gradle%29/Dependency%20Management%20%28Maven%20e%20Gradle%29.md)**
  * *Maven Build Lifecycle, Scopes, Dependency Mediation, Transitive dependencies, BOM (Bill of Materials), Gradle Daemon e incremental builds.*
* **[21. Git e Branching Strategies](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/21.%20Git%20e%20Branching%20Strategies/Git%20e%20Branching%20Strategies.md)**
  * *GitFlow vs Trunk-Based Development, Rebase vs Merge, Cherry-pick, Commit atomici, Conventional Commits.*
* **[22. Toolchain (Eclipse, Git, Maven, JUnit, Jenkins, Nexus)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/22.%20Toolchain%20%28Eclipse,%20Git,%20Maven,%20JUnit,%20Jenkins,%20Nexus%29/Toolchain%20%28Eclipse,%20Git,%20Maven,%20JUnit,%20Jenkins,%20Nexus%29.md)**
  * *Integrazione degli strumenti di sviluppo enterprise, Artifact Repositories (Nexus/Artifactory), standard di pipeline.*
* **[23. Unit Testing e Test Automation (JUnit 5, Mockito, Testcontainers)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/23.%20Unit%20Testing%20e%20Test%20Automation%20%28JUnit%205,%20Mockito,%20Testcontainers%29/Unit%20Testing%20e%20Test%20Automation%20%28JUnit%205,%20Mockito,%20Testcontainers%29.md)**
  * *JUnit 5 (Architecture, Parameterized Tests), Mockito (Mock, Spy, ArgumentCaptor, BDDMockito), Testcontainers per test di integrazione reali su Docker (Postgres, Kafka, Redis).*
* **[24. SAST e Qualità del Software (SonarQube)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/24.%20SAST%20e%20Qualit%C3%A0%20del%20Software%20%28SonarQube%29/SAST%20e%20Qualit%C3%A0%20del%20Software%20%28SonarQube%29.md)**
  * *Static Application Security Testing, Quality Gates, Code Coverage, Vulnerability, Security Hotspots, Manutenibilità.*
* **[25. CI-CD e Release Management (Jenkins, GitLab CI, Nexus)](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/25.%20CI-CD%20e%20Release%20Management%20%28Jenkins,%20GitLab%20CI,%20Nexus%29/CI-CD%20e%20Release%20Management%20%28Jenkins,%20GitLab%20CI,%20Nexus%29.md)**
  * *Pipeline as Code (Jenkinsfile, .gitlab-ci.yml), Build, Test, Scan, Packaging Docker, Deploy staging/prod, Semantic Versioning.*
* **[26. Sicurezza e Qualità del Software (i "plus")](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/26.%20Sicurezza%20e%20Qualit%C3%A0%20del%20Software%20%28i%20%22plus%22%29/Sicurezza%20e%20Qualit%C3%A0%20del%20Software%20%28i%20%22plus%22%29.md)**
  * *OWASP Top 10, Dependency-Check (CVE auditing), crittografia simmetrica/asimmetrica, gestione segreti (HashiCorp Vault, AWS Secrets Manager).*
* **[27. Troubleshooting e Gestione Incident in Produzione](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/27.%20Troubleshooting%20e%20Gestione%20Incident%20in%20Produzione/Troubleshooting%20e%20Gestione%20Incident%20in%20Produzione.md)**
  * *Analisi Thread Dump (jstack) per rilevare deadlock o thread starvation, Heap Dump (jmap, Eclipse Memory Analyzer) per identificare memory leak, profiling CPU, Metriche (Prometheus/Grafana), Distributed Tracing (OpenTelemetry/Jaeger).*
* **[28. Coding con IA e Coding Agent](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/28.%20Coding%20IA/Coding%20IA.md)**
  * *Ecosistemi Agentici (Claude Code, Cursor, Antigravity, Aider), Architettura interna: MCP (Model Context Protocol), Skills on-demand, Rules (AGENTS.md), Framework di riferimento (Ponytail anti-bloat, Matt Pocock workflows, Ratel Context Engineering), Uso critico, Privacy PCI-DSS/GDPR e sicurezza.*

---

### 👥 Parte 7: Metodologie, Product Mindset & Soft Skills
* **[29. Metodologie Agile, Product Mindset, Documentazione e Soft Skill](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/29.%20Metodologie%20Agile,%20Product%20Mindset,%20Documentazione%20e%20Soft%20Skill/Domande%20Comportamentali%20e%20Soft%20Skill.md)**
  * *Agile: Scrum (Ruoli, 5 cerimonie, DoD vs DoR) vs Kanban (WIP limits, Lead/Cycle Time). Product Mindset: Outcome over Output, Metriche di business (Conversion, Churn, LTV, CAC, MRR), Prioritizzazione RICE. Documentazione: User Story INVEST, Architecture Decision Records (ADR), Modello C4. Risoluzione problemi e risposte comportamentali con Metodo STAR.*
* **[30. Concetti Trasversali Importanti](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/30.%20Concetti%20Trasversali%20Importanti/Concetti%20Trasversali%20Importanti.md)**
  * *Idempotenza applicativa, gestione della concorrenza distribuita, pattern di retry esponenziale con jitter, graceful degradation.*

---

### 💳 Parte 8: Domini Applicativi di Business
* **[31. Dominio Pagamenti](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/31.%20Dominio%20Pagamenti/Dominio%20Pagamenti.md)**
  * *Ciclo di vita transazione carta (Autorizzazione, Cattura, Clearing, Settlement, Chargeback), Attori (Issuer, Acquirer, PSP, Circuiti), Protocolli (ISO 8583 MTI/bitmap, ISO 20022 XML, Bonifici SEPA SCT/Inst), Tokenizzazione EMV (Apple Pay/Google Pay), Normative (PSD2 SCA, PCI-DSS, GDPR).*
* **[32. Dominio Assicurativo, Previdenziale e Sistemi Finanziari](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/32.%20Dominio%20Assicurativo,%20Previdenziale%20e%20Sistemi%20Finanziari/Dominio%20Assicurativo,%20Previdenziale%20e%20Sistemi%20Finanziari.md)**
  * *Assicurazioni: Polizze Vita (Ramo I, III Unit-Linked, V) e Danni (P&C), Underwriting, Premi, Sinistri (FNOL), Riserve Tecniche, Normative IVASS, Solvency II, IFRS 17. Previdenza: Fondi pensione, PIP, Accumulo (TFR, deducibilità) ed Erogazione (Rendite attuariali), COVIP. Finanza: Order Management System (OMS, Pre-Trade Risk, Smart Order Routing, FIX Protocol, MiFID II), Portfolio Management (Asset Allocation, NAV, TWR vs MWR, VaR, Sharpe Ratio), Billing (Management/Performance fee con High-Water Mark), Reconciliation Engine (Matching 1-to-1, 1-to-N e gestione squadrature).*

---

### 📐 Parte 9: Ingegneria dei Sistemi Distribuiti, System Design, DDD & SRE
* **[33. Distributed Systems Fundamentals](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/33.%20Distributed%20Systems%20Fundamentals/Distributed%20Systems%20Fundamentals.md)**
  * *Teorema CAP & PACELC, Consistency Models (Strong, Eventual, Causal, Read-your-writes, Monotonic reads), Problemi di rete (Partition, Partial failure, Message loss, Duplicate/Reordering, Clock skew, Split brain), Coordinamento distribuito (Leader election, Quorum, Consensus Paxos/Raft, Distributed Locking).*
* **[34. System Design](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/34.%20System%20Design/System%20Design.md)**
  * *Framework strutturato di risposta (Requisiti funzionali/non-funzionali, Capacity estimation, API design, Storage selection, High-level diagram, Deep dives), Scalabilità orizzontale/verticale, Caching layer (L1/L2/CDN), Sharding e Partitioning, Single Point of Failure prevention, Casi reali (URL Shortener, Payment Gateway, Rate Limiter, Notification Service, Trading Engine).*
* **[35. Performance Engineering](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/35.%20Performance%20Engineering/Performance%20Engineering.md)**
  * *Metriche prestazionali (Latency percentili p50/p95/p99/p99.9, Throughput RPS, Saturation), Diagnostica e Profiling JVM (Allocation rate, GC pauses, Thread contention, Java Flight Recorder - JFR, JDK Mission Control - JMC, async-profiler), Ottimizzazione DB (Query tuning, Indexing, Connection pool sizing, N+1 fix), Caching e Network bottlenecks.*
* **[36. Advanced Microservices e Event Driven](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/36.%20Advanced%20Microservices%20e%20Event%20Driven/Advanced%20Microservices%20e%20Event%20Driven.md)**
  * *Pattern architetturali avanzati: API Gateway, Backend for Frontend (BFF), Saga Pattern (Orchestrata vs Coreografata), Transactional Outbox & Inbox Pattern, Strangler Fig (migrazione monoliti), Anti-Corruption Layer (ACL). Event-Driven: Event Schema versioning, Schema Registry (Avro/Protobuf), Event Replay, Dead Letter Queue (DLQ).*
* **[37. DDD e Software Architecture](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/37.%20DDD%20e%20Software%20Architecture/DDD%20e%20Software%20Architecture.md)**
  * *Domain-Driven Design strategico (Core Domain, Supporting/Generic Subdomains, Bounded Context, Context Maps) e tattico (Entities, Value Objects, Aggregates & Aggregate Roots, Domain Services, Domain Events, Repositories). Stili architetturali: Layered, Modular Monolith, Hexagonal Architecture (Ports & Adapters), Clean Architecture, Onion Architecture.*
* **[38. Advanced Security e API Governance](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/38.%20Advanced%20Security%20e%20API%20Governance/Advanced%20Security%20e%20API%20Governance.md)**
  * *Authentication & Authorization: OAuth2 & OpenID Connect (Authorization Code con PKCE, Client Credentials), JWT & JWKS validation, RBAC vs ABAC. Application Security: mTLS (Mutual TLS), CORS, CSRF, XSS, SQL Injection, SSRF, OWASP Top 10, API Gateway Governance (Rate Limiting, Throttling, API Key management, Data Masking PII/PCI-DSS).*
* **[39. SRE Reliability e Chaos Engineering](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/39.%20SRE%20Reliability%20e%20Chaos%20Engineering/SRE%20Reliability%20e%20Chaos%20Engineering.md)**
  * *Site Reliability Engineering (SRE): SLI (Service Level Indicator), SLO (Service Level Objective), SLA, Error Budget e gestione del rischio di rilascio, Riduzione del Toil. Incident Management: Detection, Triage, Mitigation, Blameless Postmortem e Root Cause Analysis (RCA). Disaster Recovery (RTO, RPO, Active-Active vs Active-Passive). Chaos Engineering (Fault injection: Latency, Packet drop, Kill pod).*

---

### 🔬 Parte 10: Deep-Dive Specialistici (Messaggistica, Testing, Osservabilità e IaC)
* **[40. Messaging Technologies Advanced](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/40.%20Messaging%20Technologies%20Advanced/Messaging%20Technologies%20Advanced.md)**
  * *Kafka & RabbitMQ a livello Senior: Producer acks (`acks=0, 1, all`), `linger.ms`, `batch.size`, idempotent producer; Consumer groups, rebalancing, offset commit, consumer lag; Delivery semantics (At-most-once, At-least-once, Exactly-once end-to-end); Partitioning key ordering, retry topic e Dead Letter Topic (DLQ); RabbitMQ (Exchanges direct/topic/fanout, queues, prefetch count, message ack/nack/reject, dead letter exchange DLX); Matrice di trade-off Kafka vs RabbitMQ (stream/log vs queue, smart broker vs smart consumer, retention).*
* **[41. Automated Testing Advanced](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/41.%20Automated%20Testing%20Advanced/Automated%20Testing%20Advanced.md)**
  * *Test Pyramid (Unit, Integration, Component, Contract, E2E); Unit test con JUnit 5 e Mockito (`@Mock`, `@InjectMocks`, `ArgumentCaptor`, BDDMockito); Integration test (`@SpringBootTest`, `@WebMvcTest`, MockMvc, WebTestClient); Testcontainers (PostgreSQL, Kafka, RabbitMQ, Redis, LocalStack); Contract Testing con Pact/Spring Cloud Contract; Performance & Load Testing (JMeter, Gatling, k6); Test Flakiness, pipeline speed e test automation best practices.*
* **[42. Advanced Observability](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/42.%20Advanced%20Observability/OpenTelemetry%20e%20Advanced%20Observability.md)**
  * *I tre pilastri (Logs, Metrics, Traces); Distributed Tracing (Trace ID, Span ID, Context Propagation, Sampling B3/W3C); OpenTelemetry (OTel SDK, OpenTelemetry Collector, OTLP exporter, auto/manual instrumentation); Metriche chiave e metodologie RED (Rate, Errors, Duration) e USE (Utilization, Saturation, Errors); Correlazione log-tracce con MDC/SLF4J; Alerting intelligente e Google Golden Signals (Latency, Traffic, Errors, Saturation).*
* **[43. Advanced Infrastructure as Code](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/43.%20Advanced%20Infrastructure%20as%20Code/Advanced%20Infrastructure%20as%20Code.md)**
  * *Terraform avanzato: HCL, Modules riutilizzabili, Remote State Management con S3 + DynamoDB State Locking, Data sources; Workflow CI/CD per IaC (`terraform fmt → validate → plan → review → apply`); Strategie multi-environment (directory vs workspaces); Drift Detection e remediation; Secret management e governance dell'infrastruttura; Integrazione GitOps (ArgoCD).*

---

### 🛡️ Parte 11: Sicurezza Enterprise, Identity Management & API Security
* **[44. OAuth2 OpenID Connect e JWT Advanced](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/44.%20OAuth2%20OpenID%20Connect%20e%20JWT%20Advanced/OAuth2%20OpenID%20Connect%20e%20JWT%20Advanced.md)**
  * *OAuth 2.0 vs OIDC: Attori e flussi (Authorization Code + PKCE per SPA/mobile/frontend, Client Credentials per M2M); Token Lifecycle (Access Token vs Refresh Token, Token Rotation, Revocation); JWT Deep Dive (Header, Payload, Signature, Standard & Custom Claims); Validazione crittografica (JWKS, Asymmetric Key rotation RSA/ECDSA, validation latency & caching); Security best practices (Token theft mitigation, Scopes vs Roles/Permissions).*
* **[45. LDAP e Active Directory](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/45.%20LDAP%20e%20Active%20Directory/LDAP%20e%20Active%20Directory.md)**
  * *Fondamenti LDAP (Directory tree, DN, RDN, ObjectClass, Attributes, Base DN, Search Filters RFC 4515); Meccanismi di bind e autenticazione (Direct Bind vs Search & Bind con account di servizio); Microsoft Active Directory (AD DS, Domain Controllers, OU, Security Groups, Kerberos, UPN vs sAMAccountName); Integrazione Java/Spring (Spring Security LDAP, `LdapTemplate`, Connection Pooling, StartTLS / LDAPS su porta 636).*
* **[46. Sicurezza J2EE SOA e API](file:///Users/giuseppefrattura/Documents/Projects/Colloquio/46.%20Sicurezza%20J2EE%20SOA%20e%20API/Sicurezza%20J2EE%20SOA%20e%20API.md)**
  * *Principi di sicurezza (Least Privilege, Defense in Depth, Fail Secure, Auditing); Sicurezza J2EE/Jakarta EE (Container-Managed Security, Security Constraints in `web.xml`, JAAS `LoginModule`, Subject/Principal, JACC); Sicurezza SOA & Web Services SOAP (WS-Security, XML Signature, XML Encryption, SAML 2.0 Token Profile); Sicurezza API REST & Microservizi (OWASP API Security Top 10, mTLS, Rate Limiting, API Gateway Policy Enforcement, Input Validation, Sanitization).*

---

## 🛠️ Metodologia Didattica di Ogni Capitolo

Ogni capitolo della guida adotta un format uniforme orientato all'eccellenza:

1. **Cos'è e perché conta**: Inquadramento strategico del perché il tema viene chiesto nei colloqui di alto livello.
2. **Trattazione Tecnica Profonda**: Spiegazione dettagliata con diagrammi ASCII/Mermaid, tabelle di comparazione e codice Java 17/21+.
3. **Domande Tipiche a Colloquio (e risposte da Senior)**: Risposte argomentate, concise e autorevoli pronte per essere esposte a voce all'intervistatore.
4. **Come Esercitarsi**: Esercizi pratici di live-coding, reverse engineering o disegno architetturale per consolidare i concetti.

---

## 🚀 Automazione CI/CD: Generazione del Documento Unificato

Il repository è dotato di una **GitHub Action** automatizzata ([`.github/workflows/generate-full-guide.yml`](file:///.github/workflows/generate-full-guide.yml)) che, ad ogni commit sul branch `main`:
1. Esegue lo script Python `scripts/merge_chapters.py`.
2. Concatena tutti i 46 capitoli in ordine numerico progressivo con indice dinamico e separatori formattati.
3. Genera e pubblica come artefatto di build scaricabile i file unificati:
   * **`guida-colloquio-completa.md`** (formato Markdown completo)
   * **`guida-colloquio-completa.txt`** (formato testo per stampa o consultazione offline rapida)

Per generare manualmente i file unificati in locale:
```bash
python3 scripts/merge_chapters.py
```

---

## 🎓 Consigli per la Preparazione del Colloquio

* **Non imparare a memoria**: Comprendi il *perché* architetturale di ogni scelta (il principio guida è sempre l'analisi dei trade-off: latenza vs consistenza, semplicità vs scalabilità).
* **Usa il Metodo STAR**: Per tutte le domande comportamentali e metodologiche, struttura le risposte in **S**ituation, **T**ask, **A**ction, **R**esult.
* **Collega la teoria al business**: Quando spieghi un concetto tecnico (es. *Virtual Threads* o *Locking Pessimistico*), contestualizzalo sempre con un esempio reale di business (es. *gestione concorrenza saldi o picchi Black Friday nei pagamenti*).

---
*Buono studio e in bocca al lupo per i tuoi colloqui!* 🚀
