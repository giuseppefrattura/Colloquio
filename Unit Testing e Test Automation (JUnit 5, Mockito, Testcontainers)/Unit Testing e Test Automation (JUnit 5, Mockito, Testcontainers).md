## Unit Testing e Test Automation (JUnit 5, Mockito, Testcontainers)

### Cos'è e perché conta
Nei sistemi transazionali finanziari, una regressione non identificata in fase di test può causare ammanchi economici o disservizi legali critici. Un Senior Backend Developer deve saper padroneggiare la **piramide dei test**, scrivere test unitari veloci e deterministici con **JUnit 5 & Mockito**, ed eseguire integration test affidabili su database e message broker reali tramite **Testcontainers**.

---

### Cosa studiare

#### 1. La Piramide dei Test e Strategia di Test

```
        / \
       / E2E \        (Pochi, lenti, costosi, testano flussi utente completi)
      /───────\
     / Integr. \      (Medi, testano interazione tra moduli, DB reale, Testcontainers)
    /───────────\
   / Unit Tests  \    (Migliaia, isolati, velocissimi < ms, mock delle dipendenze)
  /───────────────\
```

- **Unit Test**: testano una singola classe/metodo in totale isolamento. Tutte le dipendenze esterne (altri Service, Repository, Web Client) vengono simulate con mock.
- **Integration Test**: verificano che più componenti lavorino correttamente insieme (es. test di un repository JPA contro un database reale, serializzazione JSON, controller HTTP).
- **End-to-End (E2E) Test**: testano l'intero sistema distribuito da endpoint a database/code.

---

#### 2. JUnit 5 (Jupiter): Lifecycle e Funzionalità Avanzate

- **Annotazioni di Lifecycle**:
  - `@BeforeAll` / `@AfterAll`: eseguiti una sola volta prima/dopo tutti i test della classe (metodi `static` per default).
  - `@BeforeEach` / `@AfterEach`: eseguiti prima/dopo ogni singolo metodo di test (ideali per resettare mock e stato).
  - `@Test`: definisce un metodo di test.
  - `@DisplayName`: nome descrittivo leggibile per i report di test.
- **Asserzioni JUnit 5 & AssertJ**:
  - JUnit 5 standard: `assertEquals(expected, actual)`, `assertThrows(InsufficientFundsException.class, () -> service.pay(...))`.
  - **AssertJ** (Fluent API, standard de facto per leggibilità):
    ```java
    assertThat(payment.getStatus()).isEqualTo(PaymentStatus.COMPLETED);
    assertThat(payment.getAmount()).isGreaterThan(BigDecimal.ZERO);
    assertThat(payment.getTransactions())
        .hasSize(2)
        .extracting(Transaction::getCurrency)
        .containsExactly("EUR", "USD");
    ```
- **Test Parametrici (`@ParameterizedTest`)**:
  - Consentono di eseguire lo stesso test con dataset differenti, fondamentale per verificare casi limite finanziari (algoritmi di arrotondamento, validazione carte, BIN):
  ```java
  @ParameterizedTest
  @ValueSource(strings = {"4111111111111111", "5500000000000004", "378282246310005"})
  void shouldValidateValidCardNumbers(String pan) {
      assertThat(cardValidator.isValidPan(pan)).isTrue();
  }

  @ParameterizedTest
  @CsvSource({
      "100.00, EUR, 2.00",
      "50.00, USD, 1.50",
      "0.00, EUR, 0.00"
  })
  void shouldCalculateCorrectFee(BigDecimal amount, String currency, BigDecimal expectedFee) {
      BigDecimal fee = feeCalculator.calculate(amount, currency);
      assertThat(fee).isEqualByComparingTo(expectedFee);
  }
  ```

---

#### 3. Mocking con Mockito

- **Annotazioni Principali**:
  - `@ExtendWith(MockitoExtension.class)`: abilita Mockito in JUnit 5 senza avviare il contesto Spring.
  - `@Mock`: crea un'istanza fittizia di una dipendenza (tutti i metodi ritornano valori di default: null, 0, false).
  - `@InjectMocks`: crea l'istanza della classe sotto test, iniettando automaticamente i mock creati nei campi/costruttore.
  - `@Spy`: crea un wrapper su un'istanza reale, permettendo di intercettare o fare override solo di alcuni metodi (*partial mock*).
- **Stubbing (`when ... thenReturn / thenThrow`)**:
  ```java
  when(accountRepository.findById(123L)).thenReturn(Optional.of(testAccount));
  when(acquirerGateway.authorize(any())).thenThrow(new GatewayTimeoutException("Timeout"));
  ```
- **Verifica delle Interazioni (`verify`)**:
  ```java
  // Verifica che il metodo debit() sia stato chiamato esattamente 1 volta con il parametro specificato
  verify(accountRepository, times(1)).save(testAccount);
  verify(notificationService, never()).sendAlert(any());
  ```
- **Cattura di Parametri (`ArgumentCaptor`)**:
  - Ispeziona gli oggetti passati ai mock per validarne i campi interni:
  ```java
  ArgumentCaptor<PaymentEvent> eventCaptor = ArgumentCaptor.forClass(PaymentEvent.class);
  verify(eventPublisher).publish(eventCaptor.capture());
  PaymentEvent capturedEvent = eventCaptor.getValue();
  assertThat(capturedEvent.getAmount()).isEqualTo(new BigDecimal("100.00"));
  ```

---

#### 4. Slice Testing in Spring Boot

Anziché avviare l'intero `@SpringBootTest` (che carica tutti i bean ed è lento), Spring Boot permette di caricare solo la "fetta" (*slice*) di applicazione necessaria:

##### A. `@WebMvcTest` (Test del Controller Layer)
- Carica solo controller, filtri, advice e security; mocka il layer di servizio con `@MockBean`:
```java
@WebMvcTest(PaymentController.class)
class PaymentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PaymentService paymentService;

    @Test
    void shouldReturn201WhenPaymentCreated() throws Exception {
        when(paymentService.processPayment(any())).thenReturn("pay_123");

        mockMvc.perform(post("/api/v1/payments")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"amount\": 100.00, \"currency\": \"EUR\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value("pay_123"));
    }
}
```

##### B. `@DataJpaTest` (Test del Repository Layer)
- Configura solo `EntityManager`, Spring Data JPA e un database (in-memory o reale via Testcontainers), eseguendo ogni test all'interno di una transazione con rollback automatico alla fine del test.

---

#### 5. Integration Testing Moderno con Testcontainers

- **Il problema dei DB in-memory (H2)**: H2 ha una sintassi SQL, lock, tipi di dati e funzioni proprietarie diverse da Oracle o PostgreSQL. I test passano su H2 ma falliscono in produzione su Oracle.
- **La Soluzione Testcontainers**: libreria Java che avvia container Docker reali e isolati (Oracle XE, PostgreSQL, Kafka, Redis) durante l'esecuzione dei test di integrazione (`mvn verify`).
- **Configurazione con `@ServiceConnection` (Spring Boot 3.1+)**:
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class PaymentIntegrationTest {

    @Container
    @ServiceConnection // Configura automaticamente datasource url, user e password di Spring
    static OracleContainer oracle = new OracleContainer("gvenzl/oracle-xe:21-slim-faststart");

    @Container
    @ServiceConnection
    static KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.4.0"));

    @Autowired
    private PaymentRepository paymentRepository;

    @Test
    void shouldPersistTransactionOnRealOracleDatabase() {
        Payment payment = new Payment("tx_01", new BigDecimal("50.00"), "EUR");
        paymentRepository.save(payment);

        assertThat(paymentRepository.findById("tx_01")).isPresent();
    }
}
```

---

#### 6. TDD (Test-Driven Development) & BDD (Behavior-Driven Development)
- **Ciclo Red-Green-Refactor**:
  1. *Red*: scrivi un test unitario che definisce il comportamento atteso prima del codice (il test fallisce).
  2. *Green*: scrivi il codice minimo necessario per far passare il test.
  3. *Refactor*: ripulisci il codice eliminando duplicazioni e migliorando il design, mantenendo i test sempre verdi.
- **Struttura BDD Given-When-Then**:
  - *Given* (Dato un contesto/stato iniziale: conto con saldo 100€).
  - *When* (Quando avviene un'azione: richiesta di prelievo di 30€).
  - *Then* (Allora si verifica il risultato: saldo aggiornato a 70€ e transazione memorizzata).

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Qual è la differenza tra `@Mock` e `@MockBean`?*
  - **R**: `@Mock` appartiene a Mockito puro e viene istanziato velocemente senza alcun contesto Spring. `@MockBean` è un'annotazione di Spring Boot Test che crea un mock Mockito e lo registra all'interno dell'**ApplicationContext di Spring**, sostituendo qualsiasi bean reale dello stesso tipo; è necessario per i test di integrazione o slice test (`@WebMvcTest`).

- *D: Perché oggi si preferisce Testcontainers a un database in-memory come H2 per i test di integrazione?*
  - **R**: Perché H2 non replica fedelmente il comportamento, le funzioni proprietarie (es. PL/SQL, sequenze, JSON functions), i livelli di isolamento e la concorrenza di un DBMS di produzione come Oracle o PostgreSQL. Testcontainers esegue il vero motore di database in un container Docker usa-e-getta, garantendo test di integrazione affidabili al 100% senza falsi positivi.

- *D: Come testi un metodo asincrono o un listener Kafka?*
  - **R**: Utilizzando la libreria **Awaitility** (`await().atMost(5, SECONDS).untilAsserted(() -> assertThat(...))`), che effettua un polling non-bloccante fino a quando la condizione o l'evento asincrono non viene soddisfatto, evitando l'uso deprecato di `Thread.sleep()`.

---

### Come esercitarti
1. **Scrittura Test Unitario Isolato**: scrivi una classe di test per un `ReconciliationService` usando JUnit 5, `@ExtendWith(MockitoExtension.class)`, `@Mock`, `@InjectMocks`, simulando la risposta di un repository con `when` e verificando le interazioni con `verify` e `ArgumentCaptor`.
