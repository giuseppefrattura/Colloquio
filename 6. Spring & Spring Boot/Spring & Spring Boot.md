## 6. Spring & Spring Boot

### Cos'è e perché conta
Spring e Spring Boot costituiscono lo standard de facto per lo sviluppo di applicazioni enterprise Java nel settore bancario e dei pagamenti elettronici. A livello Senior, non basta saper usare le annotazioni: occorre comprendere come funziona il container **IoC/DI**, come gestire la concorrenza e le **transazioni distribuite**, come ottimizzare l'accesso ai dati con **Spring Data JPA/Hibernate**, come blindare le API con **Spring Security** e come orchestrare flussi complessi con **Spring Integration**.

---

### Cosa studiare

#### 1. Core Spring, IoC Container & Dependency Injection

##### A. Il concetto chiave: Inversion of Control (IoC) e Bean
Un **bean** è un oggetto istanziato, configurato e gestito interamente dal container Spring (ApplicationContext) anziché manualmente tramite `new`.
- **Dichiarazione Bean**:
  1. *Annotazioni di stereotipo*: `@Component`, `@Service`, `@Repository`, `@Controller` / `@RestController`.
  2. *Configurazione esplicita*: `@Configuration` con metodi annotati `@Bean` (ideale per istanziare classi di librerie esterne o con logica di inizializzazione custom).
- **Scope dei Bean**:
  - `singleton` (default): un'unica istanza condivisa in tutta l'applicazione (thread-safety a carico dello sviluppatore: non memorizzare stato mutabile nei campi).
  - `prototype`: una nuova istanza creata ad ogni richiesta di injection.
  - Scope web: `request`, `session`, `application`.
- **Ciclo di vita del Bean**:
  - Istanziazione → Injection delle dipendenze → Callback `@PostConstruct` (`InitializingBean`) → Bean pronto all'uso → Callback `@PreDestroy` (`DisposableBean`) in fase di shutdown dell'applicazione.

##### B. Stereotipi: `@Component` vs `@Service` vs `@Repository`
- `@Component`: annotazione generica per qualsiasi componente gestito.
- `@Service`: marca la classe come layer di **business logic** (chiarezza architetturale).
- `@Repository`: marca il layer di **accesso ai dati**. Ha una funzionalità fondamentale in più: attiva la **traduzione automatica delle eccezioni** del database (JDBC/Hibernate) nella gerarchia unchecked coerente di Spring `DataAccessException`.

##### C. Constructor Injection vs Field Injection (`@Autowired`)
```java
// ❌ Field Injection (sconsigliata in produzione)
@Service
public class PaymentService {
    @Autowired
    private AccountRepository accountRepository;
}

// ✅ Constructor Injection (Best Practice)
@Service
public class PaymentService {
    private final AccountRepository accountRepository;

    public PaymentService(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }
}
```
**Motivazioni Senior a favore della Constructor Injection**:
1. **Immutabilità**: il campo può essere dichiarato `final`.
2. **Testabilità pura**: la classe può essere istanziata nei test unitari passando mock tramite costruttore senza avviare il contesto Spring (`new PaymentService(mockRepo)`).
3. **Fail-Fast all'avvio**: dipendenze mancanti bloccano l'avvio dell'applicazione prevenendo `NullPointerException` a runtime.
4. **Rilevazione dipendenze circolari**: evidenzia errori di design architetturale fin da subito.
*(Nota: da Spring 4.3+, se la classe ha un solo costruttore `@Autowired` è implicito).*

##### D. Risoluzione delle ambiguità: `@Qualifier` e `@Primary`
Quando sono presenti più bean che implementano la stessa interfaccia:
- `@Primary`: definisce l'implementazione predefinita in assenza di specificazioni.
- `@Qualifier("nomeBean")`: seleziona esplicitamente il bean desiderato nel punto di injection (vince su `@Primary`).
- `@Qualifier custom`: creazione di annotazioni tipizzate per evitare stringhe hardcoded (es. `@VisaGateway`, `@MastercardGateway`).

---

#### 2. Gestione delle Transazioni (`@Transactional`) & Isolation Levels

##### A. Funzionamento di `@Transactional`
Spring utilizza proxy dinamici (AOP) per intercettare le chiamate ai metodi `@Transactional`, aprendo la transazione prima dell'esecuzione e facendo commit/rollback al termine.
- *Attenzione al Self-Invocation Trap*: se un metodo chiama un altro metodo `@Transactional` della **stessa classe**, la chiamata non passa attraverso il proxy Spring e la transazione **non** viene applicata.

##### B. Livelli di Propagazione Transazionale
- **`REQUIRED` (default)**: partecipa alla transazione corrente se esiste, altrimenti ne crea una nuova. Se un metodo fallisce, l'intera transazione fa rollback.
- **`REQUIRES_NEW`**: sospende la transazione corrente e ne avvia una nuova, completamente indipendente. Il rollback della transazione esterna non influisce su quella interna (e viceversa).
  - *Caso d'uso pagamenti*: salvataggio dei **log di audit** o dei tentativi di frode: devono essere persistiti a DB anche se la transazione di pagamento principale fallisce e va in rollback.
- **`NESTED`**: crea un savepoint all'interno della transazione esistente. Un errore nel metodo nested permette il rollback fino al savepoint senza annullare l'intera transazione esterna.
- **`SUPPORTS` / `MANDATORY` / `NOT_SUPPORTED` / `NEVER`**.

##### C. Isolation Level del Database
- **`READ_COMMITTED`** (default in Oracle/PostgreSQL): previene *dirty read*, ma ammette *non-repeatable read*.
- **`REPEATABLE_READ`**: garantisce letture consistenti dello stesso record all'interno della transazione, ma ammette *phantom read*.
- **`SERIALIZABLE`**: massimo isolamento, previene ogni anomalia eseguendo le transazioni in serie logica; comporta elevata contesa di lock e impatto sul throughput.

##### D. Politiche di Rollback
Per default Spring esegue il rollback automatico **solo per eccezioni unchecked (`RuntimeException` ed `Error`)**, mentre fa commit in caso di checked exception.
- Per forzare il rollback su qualsiasi eccezione: `@Transactional(rollbackFor = Exception.class)`.

---

#### 3. Spring Data JPA & Hibernate

```
Spring Data JPA  ──►  JPA (Specifiche/Annotazioni)  ──►  Hibernate (ORM Engine)  ──►  JDBC Driver / Database
```

- **JPA (Jakarta Persistence)**: specifica standard per l'ORM (interfacce come `EntityManager`, annotazioni `@Entity`, `@Id`, `@OneToMany`, `@ManyToOne`, `@JoinColumn`).
- **Hibernate**: implementazione concreta di JPA che genera le query SQL, gestisce la sessione (persistence context), il dirty checking e la cache di primo/secondo livello.
- **Spring Data JPA**: layer ad alto livello che elimina il boilerplate generando automaticamente l'implementazione dei repository (`JpaRepository`).

##### A. Tipologie di Query
- **Derived Query Methods**: `findByStatusAndCreatedAtBetween(...)`.
- **JPQL con `@Query`**: per query complesse orientate agli oggetti (`@Query("SELECT t FROM Transaction t WHERE t.amount > :min")`).
- **Native SQL Query**: `@Query(value = "SELECT * FROM transactions WHERE ROWNUM <= 100", nativeQuery = true)` quando occorrono feature proprietarie di Oracle/PostgreSQL.

##### B. Il Problema N+1 (Lazy Loading) e Soluzioni
Si verifica quando si carica una lista di $N$ entità principali e, accedendo a una relazione `@ManyToOne` o `@OneToMany` lazy, Hibernate esegue 1 query per la lista $+ N$ query per ciascun figlio ($1 + N$ query totali).
- **Soluzioni**:
  1. `JOIN FETCH` esplicito in JPQL: `SELECT a FROM Account a JOIN FETCH a.transactions WHERE a.id = :id`.
  2. `@EntityGraph`: specifica dichiarativa delle relazioni da caricare eagerly per quel metodo.
  3. Batch Fetching (`@BatchSize` in Hibernate): raggruppa le $N$ query in batch con clausola `IN (...)`.

##### C. Concorrenza e Locking nei Dati Finanziari
- **Locking Ottimistico (`@Version`)**: aggiunge una colonna numerica di versione. Al momento dell'UPDATE, verifica che la versione non sia cambiata (`UPDATE ... WHERE version = :expected`). In caso di collisione lancia `OptimisticLockException`. Ideale per scenari con bassa contesa.
- **Locking Pessimistico (`@Lock(LockModeType.PESSIMISTIC_WRITE)`)**: esegue una query `SELECT ... FOR UPDATE`, bloccando fisicamente la riga a livello di DB finché la transazione non termina. Necessario per aggiornamenti concorrenti di saldi e conti correnti.

---

#### 4. Gestione Centralizzata delle Eccezioni in Spring Boot

- **`@RestControllerAdvice` e `@ExceptionHandler`**:
  Intercettano le eccezioni lanciate da qualsiasi `@Controller` / `@Service`, restituendo una risposta HTTP standardizzata (es. conforme a RFC 7807 Problem Details).

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(InsufficientFundsException.class)
    public ResponseEntity<ErrorResponse> handleInsufficientFunds(InsufficientFundsException ex, HttpServletRequest request) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.UNPROCESSABLE_ENTITY.value(),
            "INSUFFICIENT_FUNDS",
            ex.getMessage(),
            request.getRequestURI(),
            Instant.now()
        );
        return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY).body(error);
    }

    @ExceptionHandler(PaymentGatewayTimeoutException.class)
    public ResponseEntity<ErrorResponse> handleTimeout(PaymentGatewayTimeoutException ex, HttpServletRequest request) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.GATEWAY_TIMEOUT.value(),
            "GATEWAY_TIMEOUT",
            "Il circuito di pagamento non ha risposto in tempo",
            request.getRequestURI(),
            Instant.now()
        );
        return ResponseEntity.status(HttpStatus.GATEWAY_TIMEOUT).body(error);
    }
}
```
- **Best Practice Senior**:
  - Creare eccezioni di business checked/unchecked specifiche (`DuplicateTransactionException`, `CardExpiredException`).
  - Distinguere rigorosamente tra errori 4xx (errore del client/validazione) e 5xx (errore di sistema/infrastruttura).
  - Non restituire mai stack trace o dettagli interni di DB al client (rischio di sicurezza).

---

#### 5. Spring Security (Modern Boot 3+)

- **`SecurityFilterChain`**: catena di filtri Servlet che intercetta e protegge le richieste prima che raggiungano i controller.
- **OAuth2 Resource Server & JWT**:
  Nei microservizi di pagamento, l'autenticazione avviene tramite Bearer JWT emesso da un Identity Provider (Keycloak / Okta). Il microservizio agisce da Resource Server validando la firma del token in modo stateless.

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity // Abilita @PreAuthorize
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable()) // Stateless REST API con token
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health", "/api/v1/public/**").permitAll()
                .requestMatchers("/api/v1/payments/admin/**").hasRole("PAYMENT_ADMIN")
                .requestMatchers("/api/v1/payments/**").hasAuthority("SCOPE_payment.write")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .build();
    }
}
```

- **Method-Level Security**:
  Controllo granulare dell'autorizzazione sui metodi di business:
  ```java
  @PreAuthorize("hasRole('ADMIN') or #accountId == authentication.principal.claims['account_id']")
  public AccountDetails getAccountDetails(String accountId) { ... }
  ```

---

#### 6. Spring Integration & Enterprise Integration Patterns (EIP)

- **Scopo**: orchestrare flussi eterogenei tra protocolli e sistemi legacy (JMS, HTTP, FTP, file batch ISO, Kafka) in modo dichiarativo.
- **Componenti chiave**:
  - **Message**: payload e metadati/headers (es. `correlationId`, `idempotencyKey`).
  - **Channel**: canale di comunicazione sincrono (DirectChannel) o asincrono (QueueChannel).
  - **Transformer**: converte i messaggi da un formato a un altro (es. da messaggio ISO 8583 a JSON interno).
  - **Router**: instrada i pagamenti verso circuiti differenti in base al BIN della carta.
  - **Filter**: scarta transazioni duplicate o non conformi.
  - **Adapter**: connettori pronti verso sistemi esterni (JMS Inbound Adapter, HTTP Outbound Gateway).

```java
@Bean
public IntegrationFlow paymentProcessingFlow() {
    return IntegrationFlow.from("paymentInboundChannel")
        .filter((PaymentMessage p) -> p.getAmount().compareTo(BigDecimal.ZERO) > 0)
        .transform(this::enrichWithExchangeRates)
        .route(PaymentMessage::getPaymentType, mapping -> mapping
            .subFlowMapping("CARD", sf -> sf.handle(Http.outboundGateway("https://card-acquirer/api/auth")))
            .subFlowMapping("SEPA", sf -> sf.handle(Jms.outboundAdapter(jmsTemplate).destination("sepaQueue")))
        )
        .get();
}
```

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Perché preferisci la Constructor Injection rispetto all'annotazione `@Autowired` sui campi?*
  - **R**: La Constructor Injection garantisce l'immutabilità dei campi (`final`), facilita i test unitari permettendo di passare mock senza avviare il container Spring o usare reflection, e garantisce il principio di fail-fast impedendo che l'applicazione si avvii con dipendenze mancanti.

- *D: Cosa succede se un metodo `@Transactional` chiama internamente un altro metodo `@Transactional(propagation = Propagation.REQUIRES_NEW)` della stessa classe?*
  - **R**: A causa del meccanismo dei proxy dinamici di Spring AOP, la chiamata interna non attraversa il proxy. Di conseguenza, la configurazione `REQUIRES_NEW` viene ignorata e il metodo viene eseguito all'interno della transazione originaria. Per risolvere questo problema, occorre spostare il metodo in un bean separato o iniettare il bean stesso.

- *D: Come risolvi il problema N+1 con Spring Data JPA?*
  - **R**: Utilizzando una query JPQL esplicita con clausola `JOIN FETCH` sulla relazione desiderata, oppure applicando l'annotazione `@EntityGraph` sul metodo del repository per specificare quali attributi caricare eagermente solo per quella specifica query.

- *D: Perché è buona pratica disabilitare il CSRF su API RESTful protette da JWT?*
  - **R**: Gli attacchi CSRF sfruttano l'invio implicito e automatico dei cookie di sessione da parte del browser in richieste cross-site. In un'API REST stateless protetta da Bearer Token (JWT) inserito esplicitamente nell'header HTTP `Authorization`, il browser non invia automaticamente il token, rendendo la protezione CSRF standard superflua.

---

### Come esercitarti
1. **Configurazione Spring Security**: scrivi a mano una configurazione `SecurityFilterChain` con validazione JWT stateless, esclusione degli endpoint di health check Actuator e autorizzazioni differenziate per ruoli operatore e admin.
2. **Global Exception Handler**: implementa un `@RestControllerAdvice` con gestione di 3 eccezioni di business custom, restituendo un oggetto di errore strutturato con codice errore univoco, messaggio human-readable e timestamp.
