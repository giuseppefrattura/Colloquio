# 41. Automated Testing — Advanced

## Obiettivo
Approfondire il testing di applicazioni Java/Spring e sistemi distribuiti, con particolare attenzione a qualità, velocità della pipeline e fiducia nei rilasci.

## Test Pyramid

Livelli principali:
- Unit test
- Integration test
- Component test
- Contract test
- End-to-End test

La maggior parte dei test dovrebbe essere veloce e isolata; i test più costosi e realistici devono essere usati dove aggiungono realmente valore.

## Unit Testing
Con JUnit 5 e Mockito:
- testare una singola unità
- mock delle dipendenze esterne
- verificare comportamento e risultati
- evitare di testare dettagli implementativi inutili

### Esempio
```java
@ExtendWith(MockitoExtension.class)
class PaymentServiceTest {
    @Mock PaymentRepository repository;
    @InjectMocks PaymentService service;

    @Test
    void shouldCreatePayment() {
        // arrange
        // act
        // assert
    }
}
```

## Integration Testing
Serve a verificare l'integrazione reale tra componenti:
- Spring context
- database
- REST API
- messaging
- configurazione

Tecnologie utili:
- `@SpringBootTest`
- MockMvc
- WebTestClient
- Testcontainers
- WireMock

## Testcontainers
Permette di eseguire dipendenze reali in container durante i test, ad esempio:
- PostgreSQL
- MySQL
- Kafka
- RabbitMQ
- Redis

È preferibile a un database embedded quando si vogliono verificare comportamenti specifici del database reale.

## Contract Testing
Verifica che producer e consumer rispettino un contratto condiviso senza richiedere un test end-to-end completo.

Concetti:
- Consumer-driven contract
- Provider verification
- Backward compatibility
- API schema evolution

Strumenti comuni: Pact e Spring Cloud Contract.

## Messaging Testing
Per Kafka/RabbitMQ verificare:
- pubblicazione corretta
- consumo
- retry
- DLQ
- ordering quando richiesto
- idempotenza
- gestione degli errori

Con Testcontainers è possibile eseguire test contro un broker reale invece di mockare completamente la messaggistica.

## REST API Testing
Testare almeno:
- HTTP status
- response body
- validation
- authentication/authorization
- error handling
- backward compatibility
- timeout/error scenarios

## TDD e BDD
### TDD
Ciclo:
1. Red
2. Green
3. Refactor

### BDD
Descrive il comportamento dal punto di vista del business:
- Given
- When
- Then

BDD è particolarmente utile quando requisiti e comportamento devono essere condivisi tra business e team tecnico.

## CI/CD e Quality Gates
Una pipeline tipica:

`Build → Unit Tests → Static Analysis → Integration Tests → Contract Tests → Package → Deploy`

Quality gate possibili:
- test coverage
- SonarQube
- SAST
- dependency vulnerability scan
- contract verification

## Test Strategy per Microservizi
Non cercare di verificare tutto con E2E test. Combinare:
- unit test per business logic
- integration test per DB/framework
- contract test per API/eventi
- pochi E2E test per journey critici

## Domande da colloquio
1. Unit test vs integration test?
2. Quando useresti Testcontainers?
3. Perché evitare di mockare completamente il database?
4. Cos'è un consumer-driven contract?
5. Come testeresti un consumer Kafka?
6. Come testi retry e DLQ?
7. Qual è una buona test pyramid per microservizi?
8. TDD è sempre necessario?
9. Come integri i test nella CI/CD pipeline?
10. Come eviti test flaky?
11. Come decidi cosa testare con E2E?
12. Code coverage elevata significa automaticamente alta qualità?

## Regola Senior
Il valore del testing non è la percentuale di coverage in sé, ma la capacità della suite di **intercettare regressioni importanti rapidamente e in modo affidabile**.
