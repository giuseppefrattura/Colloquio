# Guida di studio — Colloquio Senior Java Backend Developer 

## 1. Dominio Pagamenti

### Cos'è e perché è il punto più importante
Essendo "esperienza mandatoria", il colloquio probabilmente dedicherà tempo a domande discorsive sul dominio, non solo tecniche. Devi essere in grado di spiegare il ciclo di vita di una transazione come lo spiegheresti a un collega nuovo del team.

### Cosa studiare

**Ciclo di vita di una transazione carta**
- *Autorizzazione*: il merchant chiede all'issuer (banca del titolare carta) se i fondi/il credito sono disponibili — risposta in tempo reale (millisecondi)
- *Cattura (capture)*: il merchant conferma l'addebito effettivo (a volte avviene subito, a volte dopo giorni — es. hotel, noleggio auto)
- *Clearing*: gli istituti si scambiano le informazioni sulle transazioni da regolare, di solito in batch notturni
- *Settlement*: il movimento di denaro effettivo tra le banche coinvolte
- *Chargeback*: la contestazione da parte del titolare carta, con reverse del flusso

**Attori del sistema**
- *Issuer*: la banca che ha emesso la carta al cliente
- *Acquirer*: la banca che fornisce il servizio di accettazione pagamenti al merchant
- *PSP (Payment Service Provider)*: intermediario tecnologico tra merchant e acquirer/circuiti (es. Nexi, Stripe)
- *Circuito*: la rete che instrada e regola le transazioni (Visa, Mastercard, ecc.)

**Circuiti e protocolli**
- *ISO 8583*: protocollo a messaggi (non XML/JSON) storicamente usato per l'autorizzazione carte — capire la struttura a campi (MTI, bitmap, data elements) anche solo a livello concettuale
- *ISO 20022*: standard più moderno basato su XML, usato per bonifici SEPA e sempre più anche per carte — capire perché sta sostituendo ISO 8583 (interoperabilità, dati più ricchi)
- *SEPA*: SCT (bonifico standard, T+1) vs SCT Inst (bonifico istantaneo, esecuzione in secondi, 24/7)
- *Digital wallet*: come Apple Pay/Google Pay generano un token di dispositivo al posto del PAN reale (tokenizzazione EMV), il ruolo del Token Service Provider

**Normative**
- *PSD2*: obbligo di Strong Customer Authentication (SCA) — autenticazione a due fattori tra possesso, conoscenza, inerenza; le eccezioni (basso importo, transazioni ricorrenti)
- *PCI-DSS*: standard di sicurezza per chi tratta dati carta — perché la tokenizzazione riduce lo "scope" di compliance
- *GDPR* applicato a dati finanziari: minimizzazione, retention, diritto alla cancellazione in tensione con obblighi di conservazione fiscale/antiriciclaggio

**Riconciliazione (il tuo punto di forza)**
- Ripassa mentalmente il progetto Castelmonte: matching automatico vs manuale, gestione delle eccezioni/discrepanze, allocazione di più righe a un movimento
- Collega questo esplicitamente a "clearing/settlement/provisioning" nella job description: la riconciliazione bancaria che hai costruito è concettualmente lo stesso problema che risolvono in ambito clearing — preparati a raccontarlo come esperienza rilevante, anche se il contesto di partenza era diverso

### Come esercitarti
Prova a spiegare ad alta voce, in 2 minuti, il percorso di 10€ pagati con carta in un negozio, dal POS fino a quando il negozio vede i soldi sul conto. Se riesci a farlo fluido, sei pronto per questa parte.

---

## 2. Java & Spring Boot

### Cos'è e perché è centrale
È la tua base più solida, ma "Java 8+" in un contesto enterprise regolamentato spesso significa codice legacy convissuto con feature moderne. Devono vedere che sai muoverti su entrambi i registri.

### Cosa studiare

**Java 8 fondamentali (spesso oggetto di live coding)**
- Stream API: `map`, `filter`, `reduce`, `collect`, `groupingBy` — esercitati a scrivere uno stream da zero senza IDE che ti aiuti
- Optional: uso corretto (evitare `.get()` diretto, `orElseThrow`, `map`/`flatMap` su Optional)
- Lambda e functional interface: `Function`, `Predicate`, `Consumer`, `Supplier`
- Method reference (`Class::method`)

#### Functional Interface (approfondimento)

Una **functional interface** è un'interfaccia con **esattamente un metodo astratto** (può avere quanti metodi `default` o `static` vuole, ma solo uno astratto). È il fondamento su cui si basano le lambda expression e i method reference introdotti in Java 8.

```java
@FunctionalInterface
interface Calculator {
    int calculate(int a, int b);
}

Calculator sum = (a, b) -> a + b; // la lambda "implementa" il singolo metodo astratto
```

L'annotazione `@FunctionalInterface` non è obbligatoria (il compilatore riconosce comunque l'interfaccia se ha un solo metodo astratto), ma è buona pratica: se qualcuno aggiunge per errore un secondo metodo astratto, il compilatore lancia un errore invece di romperti silenziosamente il codice altrove.

**Le functional interface principali di `java.util.function`**

Sono quelle che usi di continuo con gli Stream:

| Interfaccia | Metodo | Firma | Uso tipico |
|---|---|---|---|
| `Function<T,R>` | `apply` | `T -> R` | Trasformare un valore in un altro |
| `Predicate<T>` | `test` | `T -> boolean` | Condizione/filtro |
| `Consumer<T>` | `accept` | `T -> void` | Consumare un valore senza restituire nulla |
| `Supplier<T>` | `get` | `() -> T` | Fornire/generare un valore |
| `BiFunction<T,U,R>` | `apply` | `(T,U) -> R` | Come `Function` ma con due input |
| `UnaryOperator<T>` | `apply` | `T -> T` | Come `Function` ma input e output dello stesso tipo |
| `BinaryOperator<T>` | `apply` | `(T,T) -> T` | Come `BiFunction` ma tutti dello stesso tipo (es. usato in `reduce`) |

```java
Function<String, Integer> length = String::length;
Predicate<Transaction> isPending = t -> t.getStatus().equals("PENDING");
Consumer<Transaction> log = t -> System.out.println(t.getId());
Supplier<Transaction> emptyTx = Transaction::new;
```

**Perché contano in un colloquio Java 8/Spring**: sono il "collante" tra le lambda e le API moderne: gli Stream (`filter` prende un `Predicate`, `map` prende un `Function`, `forEach` prende un `Consumer`), ma anche Spring stesso le usa parecchio internamente (es. `Optional.map()`, `computeIfAbsent` nelle Map). Sapere collegare "quella lambda che ho scritto" al nome dell'interfaccia funzionale sottostante mostra comprensione, non solo uso meccanico della sintassi.

**Interfacce funzionali custom**: puoi crearne di tue quando nessuna di quelle standard esprime bene l'intento, tipico in un dominio di business come i pagamenti:

```java
@FunctionalInterface
interface TransactionValidator {
    ValidationResult validate(Transaction transaction);
}
```

**Spring Boot**

#### Cosa sono i bean in Spring (base propedeutica)

Un **bean** è semplicemente un oggetto che viene creato, configurato e gestito dal **contenitore Spring (IoC container)** invece che essere istanziato manualmente da te con `new`.

**Il concetto chiave: Inversion of Control (IoC)**

Normalmente, se una classe ha bisogno di una dipendenza, sei tu (il programmatore) a decidere quando e come crearla:

```java
PaymentService service = new PaymentService(new AccountRepository());
```

Con Spring, questo controllo si "inverte": è il container che, all'avvio dell'applicazione, si occupa di:
1. Creare le istanze degli oggetti
2. Risolvere e iniettare le loro dipendenze (dependency injection)
3. Gestirne il ciclo di vita (creazione, inizializzazione, distruzione)

Ogni oggetto gestito in questo modo è un **bean**.

**Come si dichiara un bean**

Due modi principali:

1. **Annotazioni di stereotipo** (`@Component`, `@Service`, `@Repository`, `@Controller`) — Spring scansiona il classpath e registra automaticamente come bean ogni classe annotata:

```java
@Service
public class PaymentService {
    // Spring la crea e la gestisce automaticamente
}
```

2. **Configurazione esplicita con `@Bean`**, tipicamente in una classe `@Configuration` — utile quando devi istanziare qualcosa che non controlli tu (una libreria esterna) o serve logica custom di creazione:

```java
@Configuration
public class AppConfig {
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

**Caratteristiche importanti dei bean**

- **Scope**: per default un bean è **singleton** — un'unica istanza condivisa in tutta l'applicazione. Esiste anche `prototype` (nuova istanza ogni volta che viene richiesto), e scope legati al web (`request`, `session`) meno rilevanti in un backend puro
- **Application Context**: è il registro/contenitore vero e proprio dove vivono tutti i bean — quando l'app parte, Spring costruisce questo context leggendo annotazioni e configurazioni
- **Ciclo di vita**: i bean possono avere hook come `@PostConstruct` (eseguito dopo la creazione e injection delle dipendenze) e `@PreDestroy` (prima della distruzione, es. per chiudere connessioni)

**Perché conta per il colloquio**: `@Component`, `@Service`, `@Repository` sono tutti modi per dire a Spring "questa classe deve diventare un bean gestito dal container" — e la dependency injection via costruttore (vedi punto successivo) è proprio il meccanismo con cui Spring, al momento di creare un bean, gli passa gli altri bean di cui ha bisogno.

#### Dependency Injection: `@Component` vs `@Service` vs `@Repository`

Sono tutti e tre specializzazioni di `@Component` (lo stesso meccanismo sotto il cofano: Spring li scansiona e li registra come bean nel contesto applicativo). La differenza è **semantica**, non funzionale — ma in un colloquio devi sapere spiegarla perché mostra che capisci le convenzioni architetturali, non solo la sintassi:

- `@Component`: annotazione generica, usata per classi che non rientrano in un ruolo specifico (es. una utility, un validator)
- `@Service`: marca la classe come contenente **logica di business**. Nessun comportamento diverso da `@Component`, ma comunica intento a chi legge il codice — nel tuo dominio pagamenti sarebbe una classe tipo `PaymentAuthorizationService`
- `@Repository`: marca la classe come **livello di accesso ai dati**. A differenza degli altri due, ha un comportamento reale in più: Spring applica una traduzione automatica delle eccezioni specifiche del database (es. eccezioni JDBC/Hibernate) in `DataAccessException`, un'eccezione unchecked coerente indipendentemente dal DB sottostante — utile se un domani si cambia da Oracle a un altro DBMS, il codice chiamante non deve cambiare la gestione errori

**Perché conta in colloquio**: se ti chiedono "che differenza c'è", la risposta debole è "sono la stessa cosa". La risposta forte è: stessa meccanica di registrazione bean, ma `@Repository` aggiunge la traduzione delle eccezioni, e l'uso corretto delle tre annotazioni comunica l'architettura a livello di codice (leggibilità, separazione dei layer).

#### Injection via costruttore vs `@Autowired` su field

```java
// ❌ Field injection — da evitare in codice production
@Service
public class PaymentService {
    @Autowired
    private AccountRepository accountRepository;
}

// ✅ Constructor injection — best practice
@Service
public class PaymentService {
    private final AccountRepository accountRepository;

    public PaymentService(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }
}
```

Perché la constructor injection è preferita (motivazioni da saper citare a colloquio):

1. **Immutabilità**: il campo può essere `final`, quindi una volta costruito l'oggetto la dipendenza non può più cambiare — riduce bug di stato inconsistente
2. **Testabilità**: puoi istanziare la classe nei test passando dei mock direttamente al costruttore, senza bisogno del contesto Spring o di reflection (`new PaymentService(mockAccountRepository)`)
3. **Fail-fast**: se manca una dipendenza, l'applicazione non parte nemmeno (errore a startup) invece di fallire più avanti a runtime con un `NullPointerException` quando quel campo viene finalmente usato
4. **Dipendenze circolari visibili**: con field injection, Spring a volte riesce a risolvere dipendenze circolari "nascondendo" un problema di design; con constructor injection, il problema esplode subito e ti costringe a risolverlo

Da Spring 4.3 in poi, se una classe ha un solo costruttore, `@Autowired` è addirittura opzionale — Spring lo inferisce automaticamente.

#### Qualifier: risolvere ambiguità tra bean dello stesso tipo

Il **qualifier** (`@Qualifier`) risolve un problema preciso: cosa succede quando hai **più bean dello stesso tipo** e Spring non sa quale iniettare?

**Il problema**

```java
public interface PaymentGateway {
    void process(Payment payment);
}

@Service
public class VisaGateway implements PaymentGateway { ... }

@Service
public class MastercardGateway implements PaymentGateway { ... }
```

Se ora provi a iniettare `PaymentGateway` da qualche parte:

```java
@Service
public class PaymentService {
    private final PaymentGateway gateway; // ambiguo! Spring vede 2 bean candidati

    public PaymentService(PaymentGateway gateway) { ... }
}
```

Spring lancia una `NoUniqueBeanDefinitionException` a startup, perché non sa scegliere tra `VisaGateway` e `MastercardGateway`.

**La soluzione con `@Qualifier`**

```java
@Service
@Qualifier("visa")
public class VisaGateway implements PaymentGateway { ... }

@Service
@Qualifier("mastercard")
public class MastercardGateway implements PaymentGateway { ... }
```

E al momento dell'injection specifichi quale vuoi:

```java
@Service
public class PaymentService {
    private final PaymentGateway gateway;

    public PaymentService(@Qualifier("visa") PaymentGateway gateway) {
        this.gateway = gateway;
    }
}
```

**Alternative/complementi a `@Qualifier`**

- **`@Primary`**: marca un bean come "predefinito" quando ce ne sono più di uno — usato se in genere vuoi sempre lo stesso bean e solo occasionalmente serve l'alternativa esplicita:
```java
@Service
@Primary
public class VisaGateway implements PaymentGateway { ... }
```
Se sia `@Primary` sia `@Qualifier` sono presenti in punti diversi del codice, `@Qualifier` sul punto di injection vince su `@Primary` — è una scelta esplicita più specifica.

- **Matching per nome variabile**: se non usi né `@Qualifier` né `@Primary`, Spring prova come ultima risorsa a fare match tra il **nome del parametro** e il nome del bean:
```java
public PaymentService(PaymentGateway visaGateway) { ... } // funziona per coincidenza di nomi, ma è fragile
```
Sconsigliato affidarsi a questo comportamento implicito — meglio essere espliciti con `@Qualifier`.

- **Qualifier custom**: puoi anche creare una tua annotazione qualifier per maggiore type-safety (evitando stringhe "magiche" come `"visa"`):
```java
@Qualifier
@Retention(RUNTIME)
public @interface Visa {}

@Service
@Visa
public class VisaGateway implements PaymentGateway { ... }

public PaymentService(@Visa PaymentGateway gateway) { ... }
```

**Perché è molto rilevante per il tuo dominio (pagamenti)**: questo è esattamente lo scenario tipico di un sistema di pagamenti multi-circuito: più implementazioni della stessa interfaccia (`PaymentGateway`, `TokenProvider`, `SettlementProcessor`) selezionate in base al circuito/canale. È un pattern che quasi certamente incontrerai nel codice reale di questa azienda, quindi vale la pena portarlo come esempio concreto e ben padroneggiato a colloquio.

#### Gestione transazioni: `@Transactional` e propagazione

`@Transactional` delimita i confini di una transazione database. In un flusso di pagamento, capire la propagazione è cruciale perché **un metodo transazionale spesso ne chiama un altro**, e il comportamento cambia radicalmente a seconda del livello scelto.

I tre livelli più rilevanti da conoscere:

- **REQUIRED (default)**: se esiste già una transazione attiva, il metodo vi partecipa; altrimenti ne crea una nuova. Se il metodo chiamante fa rollback, fa rollback anche tutto quello che è stato fatto nel metodo chiamato, perché condividono la stessa transazione fisica.
  - *Esempio pagamenti*: `processPayment()` chiama `debitAccount()` e poi `creditMerchant()`, entrambi REQUIRED → se `creditMerchant()` fallisce, va in rollback anche il debit già eseguito. Corretto per garantire atomicità.

- **REQUIRES_NEW**: sospende la transazione corrente (se esiste) e ne apre una nuova, indipendente. Un rollback della transazione "esterna" **non** annulla quanto fatto nella transazione interna, che è già stata committata a sé.
  - *Esempio pagamenti*: la scrittura di un **log di audit** o di un tentativo di transazione va spesso in REQUIRES_NEW — vuoi che il log resti anche se il pagamento fallisce e va in rollback, per motivi di tracciabilità/compliance.

- **NESTED**: crea un "savepoint" all'interno della transazione esistente. Un rollback del metodo annidato torna solo al savepoint, senza invalidare tutta la transazione esterna — ma se la transazione esterna fa rollback, trascina con sé anche il nested. È una via di mezzo tra REQUIRED e REQUIRES_NEW (richiede supporto del driver JDBC ai savepoint).

**Perché un errore di propagazione può causare un doppio addebito**: immagina `processPayment()` (REQUIRED) che chiama `notifyExternalGateway()` marcato erroneamente come REQUIRES_NEW invece di REQUIRED. Se `notifyExternalGateway()` committa la sua transazione interna (es. salva "notifica inviata: sì") ma subito dopo il metodo esterno fallisce e fa rollback del debit dell'account, ti ritrovi con uno stato inconsistente: il gateway pensa che il pagamento sia stato notificato/confermato, ma a DB il debit non è mai avvenuto. Sapere raccontare questo scenario a colloquio dimostra comprensione pratica, non solo mnemonica delle sigle.

#### Isolation level: READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE

L'isolation level determina **quanto una transazione è "visibile" o influenzata da altre transazioni concorrenti** sullo stesso dato. Rilevante in pagamenti perché più processi (es. un pagamento in arrivo e un job batch di settlement notturno) possono toccare lo stesso saldo contemporaneamente.

- **READ_COMMITTED** (default in Oracle): una transazione vede solo dati già committati da altre transazioni. Previene il "dirty read" (leggere dati non ancora confermati), ma **non** previene il "non-repeatable read": se leggi due volte lo stesso saldo nella stessa transazione, un'altra transazione può modificarlo nel mezzo e la seconda lettura darà un valore diverso.
  - *Trade-off*: alta concorrenza/performance, ma rischio di leggere dati "in movimento" se la logica fa più letture dello stesso valore

- **REPEATABLE_READ**: garantisce che se leggi lo stesso dato due volte nella stessa transazione, ottieni sempre lo stesso valore (altre transazioni non possono modificare righe già lette da te finché non fai commit). Non previene però il "phantom read" (nuove righe che soddisfano una condizione possono apparire tra due query nella stessa transazione).
  - *Trade-off*: più sicurezza sui dati letti, ma più lock e minor throughput sotto carico concorrente

- **SERIALIZABLE**: il livello più stringente — le transazioni concorrenti si comportano come se fossero eseguite in sequenza, una alla volta. Previene tutte le anomalie (dirty read, non-repeatable read, phantom read), ma al costo di forte contesa/lock, e in scenari ad alto volume può causare più rollback per conflitto o degrado delle performance.
  - *Trade-off*: massima consistenza, minimo throughput — usato solo dove l'inconsistenza è inaccettabile (es. calcolo di un saldo finale di chiusura giornata)

**Come portarlo a colloquio**: collega questo esplicitamente al dominio — "in un flusso di settlement dove più batch aggiornano lo stesso conto, scegliere REPEATABLE_READ o SERIALIZABLE riduce il rischio di race condition sul saldo, ma bisogna valutare l'impatto sul throughput del batch notturno; per la maggior parte delle operazioni normali READ_COMMITTED con un opportuno lock ottimistico (vedi punto 3, `@Version`) è spesso il compromesso giusto."

#### JPA vs Hibernate vs Spring Data JPA: le differenze

Sono tre livelli diversi dello stesso "stack", spesso confusi perché lavorano sempre insieme — ma hanno ruoli distinti.

**JPA (Java Persistence API)**: è una **specifica** (un insieme di interfacce e regole), non un'implementazione. Fa parte di Jakarta EE (ex Java EE) e definisce *come* dovrebbe funzionare l'ORM (Object-Relational Mapping) in Java: annotazioni come `@Entity`, `@Id`, `@OneToMany`, l'interfaccia `EntityManager`, il linguaggio di query JPQL. Da sola JPA **non fa nulla** — è solo un contratto. Serve un'implementazione concreta che la rispetti.

**Hibernate**: è l'**implementazione** più diffusa di JPA (ce ne sono altre, es. EclipseLink). È Hibernate che effettivamente traduce le tue entità Java in query SQL, gestisce la cache di primo/secondo livello, il lazy loading, il dirty checking (capire quali campi sono cambiati per generare l'UPDATE corretto). Hibernate esisteva **prima** di JPA (che è nato in parte ispirandosi proprio a lui) e offre anche funzionalità extra non previste dalla specifica JPA pura — quindi è "JPA + qualcosa in più", ma nell'uso quotidiano si usa quasi sempre solo la parte standard JPA.

```java
@Entity
public class Transaction {
    @Id
    @GeneratedValue
    private Long id;
    // annotazioni JPA standard, che Hibernate interpreta ed esegue
}
```

**Spring Data JPA**: è un **layer ulteriore sopra JPA/Hibernate**, parte dell'ecosistema Spring. Non sostituisce JPA né Hibernate — li usa sotto il cofano. Il suo scopo è **eliminare boilerplate**: invece di scrivere a mano codice con `EntityManager` per query CRUD banali, si definisce solo un'interfaccia e Spring genera l'implementazione a runtime.

```java
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    List<Transaction> findByStatus(String status); // implementazione generata automaticamente
}
```

Senza Spring Data, lo stesso risultato richiederebbe scrivere manualmente:
```java
EntityManager em = ...;
TypedQuery<Transaction> query = em.createQuery(
    "SELECT t FROM Transaction t WHERE t.status = :status", Transaction.class);
query.setParameter("status", status);
List<Transaction> result = query.getResultList();
```

**Come si incastrano insieme**

```
Spring Data JPA  →  usa JPA (le annotazioni/regole)  →  eseguito da Hibernate (l'engine reale)  →  genera SQL per Oracle
```

*Analogia utile per il colloquio*: JPA è come un'interfaccia (il "cosa"), Hibernate è la classe concreta che la implementa (il "come" effettivo), Spring Data è un ulteriore livello di comodità che evita di scrivere codice ripetitivo contro JPA direttamente.

*Perché conta a colloquio*: sapere questa distinzione evita l'errore comune di dire "uso Hibernate" quando in realtà nel codice si usano solo annotazioni JPA standard e repository Spring Data, senza mai toccare API specifiche di Hibernate — è un dettaglio che i colloquiatori tecnici notano subito, perché rivela se hai davvero capito lo stack o lo usi "a scatola chiusa".

#### Spring Data JPA: query derivate, `@Query`, N+1 problem

**Query derivate (derived query methods)**: Spring genera automaticamente l'implementazione a partire dal nome del metodo nell'interfaccia repository:

```java
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    List<Transaction> findByStatusAndAccountId(String status, Long accountId);
    List<Transaction> findByAmountGreaterThanAndCreatedAtBetween(
        BigDecimal amount, LocalDateTime start, LocalDateTime end);
}
```
Comodo per query semplici, ma diventa illeggibile oltre 3-4 condizioni — sapere riconoscere quando è il momento di passare a `@Query`.

**`@Query` custom**: necessario per query più complesse (join espliciti, aggregazioni, query native SQL quando serve una funzionalità specifica di Oracle):

```java
@Query("SELECT t FROM Transaction t WHERE t.status = :status AND t.account.branch = :branch")
List<Transaction> findByStatusAndBranch(@Param("status") String status, @Param("branch") String branch);

// oppure query nativa quando serve SQL specifico di Oracle
@Query(value = "SELECT * FROM transactions WHERE ROWNUM <= 100 ORDER BY created_at DESC", nativeQuery = true)
List<Transaction> findRecentTransactions();
```

**N+1 problem**: è probabilmente il problema di performance più citato nei colloqui Spring/JPA. Succede quando carichi una lista di N entità e per ognuna, a causa del **lazy loading**, JPA esegue una query separata per caricare una relazione collegata:

```java
List<Account> accounts = accountRepository.findAll(); // 1 query
for (Account a : accounts) {
    a.getTransactions().size(); // se lazy, esegue 1 query PER ogni account → N query aggiuntive
}
```
Risultato: 1 query iniziale + N query aggiuntive = N+1 query totali, invece di una sola query ottimizzata. In un sistema di pagamenti con volumi alti, questo è un problema di performance reale, non teorico.

**Come risolverlo** (sapere citarne almeno due a colloquio):
- `JOIN FETCH` in una `@Query` JPQL per caricare la relazione nella stessa query: `SELECT a FROM Account a JOIN FETCH a.transactions WHERE ...`
- `@EntityGraph` per specificare dichiarativamente quali relazioni caricare eagerly per quella specifica query, senza cambiare il fetch type di default dell'entità
- Batch fetching (`@BatchSize` in Hibernate) per raggruppare le query N in un numero ridotto di query con `IN (...)`

**Perché conta in colloquio**: è un problema che chiunque abbia lavorato con JPA/Hibernate in produzione ha incontrato — è un ottimo argomento per raccontare un'esperienza concreta se ti è capitato, o per dimostrare che conosci il problema anche solo in teoria.

**Concetti specifici del dominio pagamenti da collegare a Spring**
- *Idempotenza*: come garantisci che un retry di rete non causi un doppio addebito — pattern con idempotency key salvata su DB con constraint univoco, controllo prima di processare
- Gestione errori/retry in flussi distribuiti: circuit breaker (concetto, anche se non conosci Resilience4j nel dettaglio), timeout, dead letter queue se emerge messaging (Kafka/JMS)

### Come esercitarti
Scrivi a mano (anche su carta o editor semplice, senza autocomplete) un metodo che raggruppa una lista di transazioni per stato e ne somma gli importi con gli Stream. È l'esercizio da live coding più probabile.

---

## 3. Oracle / SQL

### Cos'è e perché conta
In un sistema di pagamento la correttezza dei dati transazionali è tutto: sapranno se capisci davvero ACID o se lo sai solo a memoria.

### Cosa studiare

**SQL avanzato**
- Join (INNER, LEFT, self-join) su schemi con più tabelle collegate (transazioni, conti, movimenti) — proprio come nello schema di riconciliazione che hai già costruito
- Window function (`ROW_NUMBER`, `RANK`, `SUM() OVER`) utili per calcolare saldi progressivi o identificare duplicati
- Aggregazioni con `GROUP BY` + `HAVING` per riconciliazioni/quadrature

**Concorrenza e lock**
- Differenza tra lock ottimistico (versioning, `@Version` in JPA) e pessimistico (`SELECT FOR UPDATE`)
- Perché in ambito settlement, dove più processi batch possono toccare lo stesso saldo, la scelta del lock ha impatti reali su correttezza e throughput
- ACID: atomicità e isolamento spiegati con un esempio concreto (es. trasferimento tra due conti: se il debit va a buon fine ma il credit fallisce, serve rollback)

**PL/SQL (base)**
- Struttura di una stored procedure/function, cursori, gestione eccezioni (`EXCEPTION WHEN`)
- Non serve essere esperti, ma sapere leggerne una e spiegare cosa fa

### Come esercitarti
Scrivi una query che, data una tabella `transazioni(id, importo, stato, data)`, calcola il saldo progressivo giorno per giorno con una window function — è l'esempio più vicino al mondo reale che ti chiederanno.

### Execution plan: come ottimizzare query lente

L'**execution plan** (piano di esecuzione) è la sequenza di operazioni che il database sceglie per eseguire una query — mostra come il DBMS accede fisicamente ai dati (quali indici usa, in che ordine fa i join, quanti record stima di leggere) per arrivare al risultato. È lo strumento principale per capire *perché* una query è lenta, non solo *che* è lenta.

**Come funziona concettualmente**

Quando lanci una query SQL, il database non la esegue "alla lettera" — un **query optimizer** (in Oracle si chiama *Cost-Based Optimizer*, CBO) valuta diverse strategie possibili per ottenere lo stesso risultato e sceglie quella con il costo stimato più basso, basandosi su:

- **Statistiche** sulle tabelle (numero di righe, distribuzione dei valori, cardinalità)
- **Indici disponibili** e la loro selettività
- **Vincoli** (chiavi primarie/esterne) che permettono ottimizzazioni

L'execution plan è la "traduzione leggibile" di quella strategia scelta.

**Dove si usa (Oracle)**

```sql
EXPLAIN PLAN FOR
SELECT * FROM transactions WHERE account_id = 123 AND status = 'PENDING';

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

Oppure, per vedere il piano **realmente usato** (non solo quello stimato) dopo l'esecuzione:

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));
```

Strumenti pratici dove lo trovi:
- **SQL Developer**: pulsante "Explain Plan" (F10) con visualizzazione grafica
- **AWR/ASH reports** in Oracle Enterprise: per analizzare query lente già eseguite in produzione
- Equivalenti in altri DB: `EXPLAIN` in PostgreSQL/MySQL — stesso concetto, sintassi diversa

**Cosa cercare nel piano per ottimizzare una query lenta**

1. **Full Table Scan vs Index Access** — la voce più importante da controllare. Se vedi `TABLE ACCESS FULL` su una tabella grande dove ti aspetti un filtro selettivo, è spesso il primo campanello d'allarme:

```
| Id | Operation                   | Name         | Rows |
|  0 | SELECT STATEMENT            |               |      |
|  1 |  TABLE ACCESS FULL          | TRANSACTIONS  | 50000|  <- problema
```
vs.
```
|  1 |  TABLE ACCESS BY INDEX ROWID| TRANSACTIONS  |    12|  <- ottimizzato
|  2 |   INDEX RANGE SCAN          | IDX_ACC_STAT  |    12|
```

2. **Cost e Cardinality stimata vs reale** — il piano mostra un costo stimato e un numero di righe attese (`Rows`). Se la stima è molto diversa dal reale (es. stima 10 righe ma in realtà ne processa 500.000), spesso significa **statistiche obsolete** — si risolve con `DBMS_STATS.GATHER_TABLE_STATS`.

3. **Tipo di Join e ordine**:
   - `NESTED LOOPS`: efficiente quando una delle due tabelle produce poche righe (filtro molto selettivo) e l'altra ha un buon indice sulla colonna di join
   - `HASH JOIN`: più efficiente su grandi volumi senza indici utili, ma richiede più memoria
   - `MERGE JOIN`: utile quando i dati sono già ordinati sulla colonna di join

   Un join scelto male (es. `NESTED LOOPS` su due tabelle enormi) è una causa comune di query lente.

4. **Filtro applicato prima o dopo** — verifica se una condizione `WHERE` viene applicata a livello di indice (`INDEX RANGE SCAN` con la condizione nell'`Access Predicates`) oppure solo dopo aver già letto le righe (`Filter Predicates`) — nel secondo caso il DB ha comunque dovuto leggere più dati del necessario prima di scartarli.

**Rilevanza specifica per il dominio pagamenti**

In un sistema transazionale con volumi alti, l'execution plan è cruciale per query su tabelle di transazioni/movimenti che crescono continuamente:

- Query di **riconciliazione** che fanno join tra `transactions` e `ledger_entries` su range di date — un indice mancante su `created_at` può far degenerare tutto in full table scan
- Query di **lookup per idempotency key** — deve essere garantito un accesso via indice univoco, altrimenti ogni controllo di idempotenza rallenta a mano a mano che la tabella cresce
- Batch di **settlement notturno** che processano grandi volumi — qui a volte è persino corretto *forzare* un full table scan con un hint se stai leggendo comunque la maggior parte della tabella, perché un indice sarebbe più lento

**Come esercitarti**

Prepara questo aneddoto: "ho una query lenta, il primo passo è guardare l'execution plan per capire se c'è un full table scan inatteso o statistiche obsolete, poi valuto se serve un indice nuovo, o se riscrivere la query per aiutare l'optimizer a scegliere un piano migliore (es. evitando funzioni sulla colonna indicizzata nel WHERE, che impediscono l'uso dell'indice — `WHERE UPPER(status) = 'PENDING'` blocca l'indice su `status` a meno di un indice a funzione)."

---

## 4. Toolchain (Eclipse, Git, Maven, JUnit, Jenkins, Nexus)

### Cos'è e perché conta
Meno peso tecnico ma segnala autonomia operativa — in un contesto enterprise regolamentato, il processo di rilascio è spesso rigido e vogliono sapere che ti inserisci senza frizioni.

### Cosa studiare

- **Eclipse IDE**: se lavori principalmente con IntelliJ, rinfresca le scorciatoie base (refactor, debug, gestione workspace/progetti Maven) — non serve diventare esperto, basta non essere spiazzato
- **Git**: flussi di branching enterprise (Git Flow o simili), rebase vs merge, gestione conflitti — spesso chiedono "come gestisci un conflitto di merge" più che comandi esotici
- **Maven**: struttura di un `pom.xml`, gestione dipendenze e scope (`compile`, `test`, `provided`), lifecycle (`validate`, `compile`, `test`, `package`, `install`, `deploy`)
- **JUnit**: differenza tra unit test e integration test, uso di Mockito per il mocking, test parametrizzati (già nel tuo bagaglio recente)
- **Jenkins**: concetto di pipeline (dichiarativa vs scripted), stage tipici (build, test, quality gate, deploy) — non serve saperci scrivere una pipeline complessa, ma capire cosa fa un job CI/CD
- **Nexus**: repository manager per artifact Maven/npm — sapere a cosa serve (versioning, cache di dipendenze, distribuzione interna di librerie)

### Come esercitarti
Se non hai mai usato Jenkins/Nexus in prima persona, guarda un video introduttivo di 10 minuti su ciascuno: l'obiettivo è poter dire "ho capito il concetto anche se non l'ho usato quotidianamente", che è una risposta onesta e accettabile.

---

## 5. Sicurezza e Qualità del Software (i "plus")

### Cos'è e perché conta
Sono competenze plus, quindi non decisive, ma menzionarle bene ti differenzia dagli altri candidati con solo skill tecniche pure.

### Cosa studiare

**Secure coding**
- OWASP Top 10 a grandi linee: injection (SQL injection soprattutto, vista la centralità di Oracle), broken authentication, exposure di dati sensibili
- Gestione segreti: perché non si mettono credenziali/chiavi in chiaro nel codice, uso di vault/secret manager (anche solo a livello concettuale)

**Tokenizzazione**
- Concetto chiave: sostituire un dato sensibile (es. numero carta/PAN) con un token senza valore fuori dal sistema che lo ha generato, così se il token viene intercettato è inutile
- Differenza tra tokenizzazione e cifratura (la tokenizzazione non è reversibile matematicamente, richiede una tabella di mapping protetta)

**Test automation**
- Piramide dei test: unit (tanti, veloci) → integration (meno, più lenti) → end-to-end (pochi, costosi)
- Mockito per isolare le unità sotto test dai servizi esterni (banche, circuiti) — rilevante perché in ambito pagamenti non puoi testare contro sistemi bancari reali in ogni build

### Come esercitarti
Prepara un esempio concreto (anche dal tuo lavoro recente con Jackson/SOAP-to-JSON o dal progetto di riconciliazione) in cui hai scritto test che isolano una dipendenza esterna — è il tipo di aneddoto che rende credibile questa sezione.

---

## 6. Strutture Dati in Java (List, Set, Map)

### Cos'è e perché conta
Non era tra i punti espliciti della job description, ma è materiale base che torna spesso nei colloqui tecnici Java, sia in domande dirette che in live coding. Nel dominio pagamenti torna utile soprattutto per deduplicazione (es. idempotency key) e lookup veloci (es. indicizzare conti per ID).

### Cosa studiare

Le principali strutture dati fanno parte del **Java Collections Framework**, con l'interfaccia `Collection` come radice (eccetto `Map`, che è a parte). Le famiglie principali sono **List**, **Set**, **Map**, più **Queue/Deque**.

#### List — sequenza ordinata, ammette duplicati

- **`ArrayList`**: backed da array ridimensionabile. Accesso per indice O(1), inserimento/rimozione in mezzo O(n) perché richiede shift degli elementi. Scelta di default nella maggior parte dei casi.
- **`LinkedList`**: lista doppiamente concatenata. Inserimento/rimozione O(1) se hai già il riferimento al nodo, ma accesso per indice O(n). Implementa anche `Deque`, quindi utile come coda/stack.

```java
List<String> list = new ArrayList<>();
list.add("A");
list.add("A"); // ok, i duplicati sono ammessi
// list = ["A", "A"]
```

#### Set — nessun duplicato, ordine variabile

- **`HashSet`**: backed da una `HashMap` internamente. Nessun ordine garantito. O(1) medio per add/contains, basato su `hashCode()`/`equals()`.
- **`LinkedHashSet`**: come `HashSet` ma mantiene l'ordine di inserimento.
- **`TreeSet`**: mantiene gli elementi ordinati (naturale o via `Comparator`), backed da un albero rosso-nero. O(log n) per le operazioni.

**Cosa succede se aggiungi un duplicato in un Set**

```java
Set<String> set = new HashSet<>();
boolean added1 = set.add("A"); // true
boolean added2 = set.add("A"); // false — non viene aggiunto, il set resta invariato
```

Il metodo `add()` **non lancia eccezioni** — semplicemente ritorna `false` e l'elemento esistente resta quello che c'era. Il criterio di "duplicato" è determinato da `equals()` (e coerentemente da `hashCode()`, che deve essere uguale per oggetti uguali — è un contratto fondamentale: se non lo rispetti, `HashSet` si comporta in modo imprevedibile, es. permette duplicati "logici" perché finiscono in bucket diversi).

**Attenzione pratica**: se metti in un `HashSet` oggetti custom (es. una classe `Transaction`) senza aver fatto override di `equals()`/`hashCode()`, Java usa l'identità di riferimento di default — due oggetti con gli stessi dati ma istanze diverse sono considerati "diversi", quindi entrambi vengono aggiunti. È una delle cause di bug più comuni in questo contesto.

#### Map — coppie chiave-valore, chiavi uniche

- **`HashMap`**: nessun ordine, O(1) medio per get/put.
- **`LinkedHashMap`**: mantiene l'ordine di inserimento (o di accesso, se configurato — utile per implementare cache LRU).
- **`TreeMap`**: chiavi ordinate, O(log n), backed da albero rosso-nero.

**Cosa succede se aggiungi una chiave duplicata in una Map**

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);
Integer old = map.put("A", 2); // sovrascrive il valore, ritorna il valore precedente (1)
// map = {"A": 2}
```

A differenza del `Set`, `put()` con una chiave già esistente **sovrascrive silenziosamente** il valore associato e ritorna il vecchio valore (utile per rilevare se stavi effettivamente sovrascrivendo qualcosa). Se vuoi un comportamento diverso:

```java
map.putIfAbsent("A", 3);      // non sovrascrive se la chiave esiste già
map.merge("A", 1, Integer::sum); // combina il vecchio valore col nuovo (utile per contatori/somme)
map.computeIfAbsent(...)      // inizializza solo se assente
```

#### Queue / Deque

- **`ArrayDeque`**: implementazione efficiente di coda/stack/deque, generalmente preferita a `LinkedList` per queste operazioni oggi
- **`PriorityQueue`**: coda basata su heap, gli elementi escono in ordine di priorità (naturale o `Comparator`), non FIFO — utile ad esempio per processare transazioni per priorità o scadenza

### Come esercitarti
Ripassa a mente la differenza chiave: in un `Set`, un duplicato viene **ignorato silenziosamente** (`add()` ritorna `false`); in una `Map`, una chiave duplicata **sovrascrive silenziosamente** il valore (`put()` ritorna il vecchio valore). È un dettaglio che distingue chi ha solo letto la teoria da chi ci ha lavorato davvero, perché è una fonte comune di bug sottili — soprattutto quando si dimentica di fare override di `equals()`/`hashCode()` su oggetti custom.

---

## 7. `sealed` in Java (novità del linguaggio — plus)

### Cos'è e perché conta
Non è tra i requisiti della job description (che parla di "Java 8+"), ma è un buon argomento da citare se emerge un discorso su novità/aggiornamenti del linguaggio — si collega anche al tuo lavoro recente con Spring Boot su Java 24.

### Cosa studiare

`sealed` è un modificatore introdotto in modo definitivo con **Java 17** (in preview da Java 15) che permette di **restringere esplicitamente quali classi/interfacce possono estendere o implementare** una classe o interfaccia. È il complemento opposto di `final` (che impedisce *ogni* estensione): con `sealed` si dice "solo queste classe specifiche possono estendermi, nessun'altra".

**Sintassi base**

```java
public sealed interface PaymentMethod
    permits CardPayment, WalletPayment, BankTransferPayment {
}

public final class CardPayment implements PaymentMethod { ... }
public final class WalletPayment implements PaymentMethod { ... }
public final class BankTransferPayment implements PaymentMethod { ... }
```

La clausola `permits` elenca esplicitamente le sottoclassi ammesse. Ogni sottoclasse elencata deve dichiararsi a sua volta come una di queste tre cose:
- **`final`**: non può essere estesa oltre
- **`sealed`**: continua a restringere ulteriormente le proprie sottoclassi
- **`non-sealed`**: "riapre" la gerarchia, permettendo estensione libera da quel punto in poi

**Perché esiste — il problema che risolve**

Prima di `sealed`, in Java c'erano solo due estremi:
- Una classe/interfaccia **normale**: chiunque può estenderla, nessun controllo
- Una classe **`final`**: nessuno può estenderla

Mancava una via di mezzo per esprimere "questo insieme di sottotipi è **chiuso e conosciuto**, ma serve comunque il polimorfismo". `sealed` copre esattamente questo caso.

**Il vantaggio pratico più concreto: `switch` esaustivo**

Il beneficio più tangibile si vede insieme ai **pattern matching su `switch`** (altra feature moderna, Java 21+): se la gerarchia è sealed, il compilatore **sa** quali sono tutti i possibili sottotipi, quindi può verificare che uno `switch` li copra tutti, senza bisogno di un `default`:

```java
static BigDecimal calculateFee(PaymentMethod method) {
    return switch (method) {
        case CardPayment c -> c.getAmount().multiply(new BigDecimal("0.02"));
        case WalletPayment w -> BigDecimal.ZERO;
        case BankTransferPayment b -> new BigDecimal("0.50");
        // niente default necessario: il compilatore sa che sono tutti i casi possibili
    };
}
```

Se domani si aggiunge un nuovo tipo (es. `CryptoPayment`) alla lista `permits` ma ci si dimentica di gestirlo in questo `switch`, **il compilatore dà errore in fase di compilazione** invece di scoprirlo a runtime — un vantaggio enorme di sicurezza in un dominio come i pagamenti, dove dimenticare di gestire un nuovo metodo di pagamento potrebbe avere conseguenze reali.

### Come esercitarti
Prepara questo esempio con `PaymentMethod` come traccia: è un caso d'uso realistico e facilmente collegabile al dominio pagamenti se ti viene chiesto "conosci qualche feature recente di Java?".

---

## 8. Microservizi: Concetti Fondamentali

### Cos'è e perché conta
Anche se non esplicitamente nella job description, un'architettura di pagamenti mission-critical con integrazioni multiple (circuiti, banche, provider terzi) è quasi certamente organizzata a microservizi o comunque a servizi distribuiti. Vale la pena arrivare preparato anche su questo fronte.

### Cosa studiare

**Principi di base**

I microservizi sono un'architettura dove l'applicazione è scomposta in servizi indipendenti, ciascuno responsabile di una specifica funzionalità di business. Ogni servizio ha il proprio database (**database per service pattern**), può essere deployato indipendentemente e comunica con gli altri attraverso API ben definite.

*Esempio nel dominio pagamenti*: un servizio `authorization-service` (gestisce le autorizzazioni), uno `settlement-service` (gestisce clearing/settlement), uno `reconciliation-service` (riconciliazione) — ognuno con il proprio DB, deployabile e scalabile in autonomia.

**Vantaggi e trade-off**

Devi essere pronto a discutere quando conviene usarli:
- **Vantaggi**: scalabilità indipendente (es. scalare solo il servizio di autorizzazione nei picchi di traffico, senza toccare il resto), isolamento dei guasti (un servizio che cade non abbatte tutto il sistema), libertà tecnologica per ogni servizio, team autonomi che possono rilasciare senza coordinarsi con tutti gli altri
- **Svantaggi**: complessità nella gestione distribuita, necessità di orchestrazione, monitoraggio avanzato (vedi osservabilità più sotto), gestione delle transazioni distribuite (niente più semplice `@Transactional` locale quando l'operazione coinvolge più servizi)

**Comunicazione tra servizi**

- **Sincrona** (REST, gRPC): il chiamante aspetta la risposta. Più semplice da ragionare, ma accoppia temporalmente i servizi — se il servizio chiamato è lento o giù, blocca anche il chiamante
- **Asincrona** (message broker come RabbitMQ, Kafka, AWS SQS): il chiamante pubblica un messaggio/evento e prosegue, senza aspettare. Preferibile per disaccoppiare i servizi e gestire meglio i picchi di carico

*Esempio pagamenti*: l'autorizzazione di una transazione richiede tipicamente comunicazione **sincrona** (il cliente al POS aspetta una risposta in millisecondi), mentre l'invio di notifiche, l'aggiornamento di sistemi di reportistica o l'innesco della riconciliazione post-transazione sono tipicamente **asincroni** via evento (es. `TransactionCompletedEvent` pubblicato su Kafka).

**Pattern essenziali**

- **API Gateway**: punto d'ingresso unico per i client, che instrada le richieste ai servizi interni, gestendo trasversalmente autenticazione, rate limiting, routing
- **Service Discovery** (Consul, Eureka): permette ai servizi di trovarsi dinamicamente a runtime, senza indirizzi IP hardcoded — essenziale quando i servizi scalano e le istanze cambiano continuamente
- **Circuit Breaker** (pattern reso popolare da Hystrix, oggi più spesso Resilience4j): se un servizio a valle inizia a fallire ripetutamente, il circuit breaker "apre il circuito" e smette temporaneamente di chiamarlo, restituendo subito un errore/fallback invece di continuare a intasarlo con richieste che falliranno comunque — fondamentale per evitare che un servizio in difficoltà (es. un circuito di pagamento esterno lento) faccia collassare a cascata anche i servizi che lo chiamano
- **Saga pattern**: per gestire transazioni distribuite su più servizi senza un "commit" globale come nel mondo relazionale — una saga è una sequenza di transazioni locali, ciascuna con una **compensazione** (azione di rollback logico) se un passo successivo fallisce. Due varianti: *orchestrazione* (un coordinatore centrale dirige i passi) o *coreografia* (ogni servizio reagisce a eventi e decide autonomamente il passo successivo)
  - *Esempio pagamenti*: un pagamento che coinvolge debit dell'account, notifica al merchant e aggiornamento del ledger — se l'ultimo passo fallisce, la saga esegue le compensazioni (es. re-credit dell'account) invece di un rollback atomico impossibile su più DB separati
- **Event Sourcing e CQRS**: Event Sourcing salva lo stato di un'entità come sequenza di eventi immutabili (invece che come stato corrente sovrascritto) — utilissimo in ambito finanziario per audit trail completo, dato che ogni cambiamento di stato è tracciato. CQRS (Command Query Responsibility Segregation) separa il modello usato per le scritture da quello usato per le letture, spesso ottimizzati diversamente — combinato con Event Sourcing è un pattern molto comune in sistemi di pagamento/contabilità dove la tracciabilità storica è un requisito normativo

### Come esercitarti
Prepara un esempio in cui spieghi perché il **Circuit Breaker** è particolarmente rilevante in un sistema che chiama circuiti di pagamento esterni: se Visa/Mastercard rispondono lentamente, senza circuit breaker rischi di saturare i thread/connessioni del tuo servizio in attesa, propagando il problema a cascata.

---

## 9. Architettura Cloud

### Cos'è e perché conta
Anche in un contesto enterprise regolamentato come il settore pagamenti, la conoscenza dei concetti cloud-native è sempre più richiesta, anche se l'infrastruttura sottostante potrebbe essere ibrida (parte on-premise per motivi normativi, parte cloud).

### Cosa studiare

**Modelli di servizio**

- **IaaS** (Infrastructure as a Service): fornisce risorse infrastrutturali di base (VM, storage, rete) — tu gestisci OS, runtime, applicazione. Esempio: AWS EC2, Azure VM
- **PaaS** (Platform as a Service): fornisce una piattaforma pronta per eseguire l'applicazione, senza gestire l'infrastruttura sottostante — tu ti concentri solo sul codice. Esempio: AWS Elastic Beanstalk, Azure App Service
- **SaaS** (Software as a Service): software completo pronto all'uso, nessuna gestione infrastrutturale o applicativa da parte tua. Esempio: Salesforce, Office 365

**Principi cloud-native (12-factor app)**

- **Stateless**: l'applicazione non mantiene stato in memoria locale tra richieste — lo stato va esternalizzato (DB, cache distribuita) così qualunque istanza può gestire qualunque richiesta, abilitando scalabilità orizzontale
- **Configurazione esterna**: parametri di ambiente (URL DB, credenziali, feature flag) fuori dal codice — variabili d'ambiente o config server, mai hardcoded
- **Resilienza ai guasti**: l'applicazione deve gestire gracefully la caduta di dipendenze (vedi Circuit Breaker sopra)
- **Scalabilità orizzontale**: aggiungere più istanze invece di potenziare una singola macchina (vedi sotto)
- **Containerizzazione** (Docker, Kubernetes): pacchettizzare l'applicazione con le sue dipendenze in un'unità portabile e riproducibile, orchestrata poi da Kubernetes per gestione del ciclo di vita, scaling, self-healing

**Scalabilità e resilienza**

- **Scalabilità verticale**: potenziare una singola macchina (più CPU/RAM) — limite fisico, spesso richiede downtime
- **Scalabilità orizzontale**: aggiungere più istanze della stessa applicazione — preferita in cloud, richiede però che l'applicazione sia stateless
- **Auto-scaling basato su metriche**: aggiungere/rimuovere istanze automaticamente in base a CPU, memoria, numero di richieste — rilevante per gestire picchi di traffico pagamenti (es. Black Friday)
- **Load balancing**: distribuisce le richieste tra istanze —
  - *round-robin*: distribuzione ciclica semplice
  - *least connections*: instrada verso l'istanza con meno connessioni attive
  - *sticky sessions*: instrada sempre lo stesso client verso la stessa istanza (utile se c'è stato di sessione non esternalizzato, ma in contrasto col principio stateless)
- **Health check e self-healing**: il sistema controlla periodicamente se un'istanza è "sana"; se non risponde, viene rimossa dal load balancer e/o riavviata automaticamente
- **Availability zones e multi-region**: distribuire le istanze su più data center fisicamente separati (zone) o su più regioni geografiche, per resistere a guasti su larga scala — rilevante in un dominio critico come i pagamenti dove il downtime ha un costo diretto

**Servizi cloud comuni** (AWS come riferimento, concetti trasferibili ad Azure/GCP)

| Categoria | Servizi | Uso tipico |
|---|---|---|
| Compute | EC2, Lambda (serverless), ECS/EKS | VM, funzioni event-driven, container orchestration |
| Storage | S3, EBS, blob storage | File/oggetti, dischi per VM |
| Database | RDS, DynamoDB, Cosmos DB | DB relazionale gestito, NoSQL gestito |
| Networking | VPC, subnet, security groups | Isolamento di rete, firewall a livello di istanza |
| Monitoring | CloudWatch, Application Insights | Metriche, log, alerting |

### Come esercitarti
Prepara una frase tipo: "in un sistema di pagamenti, per motivi di compliance/regolamentazione spesso alcuni componenti restano on-premise, mentre altri (analytics, reportistica) possono sfruttare il cloud pubblico — è comune un'architettura ibrida più che 100% cloud" — mostra consapevolezza realistica del settore, non solo teoria da manuale cloud generico.

---

## 10. Accesso ai Database

### Cos'è e perché conta
Si collega direttamente alla sezione Oracle/SQL già trattata, ma allarga la prospettiva a scelte architetturali più ampie (SQL vs NoSQL, pattern di accesso) che possono emergere in un colloquio senior.

### Cosa studiare

**SQL vs NoSQL**

- **SQL**: preferibile per transazioni ACID, relazioni complesse tra entità, query ad-hoc flessibili — è la scelta naturale (e quasi obbligata) per il core di un sistema di pagamento, dove la consistenza dei saldi non è negoziabile
- **NoSQL**: preferibile per scalabilità orizzontale, schema flessibile, alte performance su grandi volumi. Tipologie principali:
  - *Document store* (MongoDB): dati semi-strutturati, schema flessibile — utile per configurazioni, log applicativi, dati non strettamente relazionali
  - *Key-value* (Redis): accesso velocissimo per chiave — tipico per cache o sessioni
  - *Column-family* (Cassandra): ottimizzato per scritture massive e query su grandi volumi distribuiti — usato a volte per audit log o time-series di eventi
  - *Graph database* (Neo4j): ottimizzato per relazioni complesse tra entità — utile ad esempio per fraud detection (rilevare pattern sospetti tra conti/transazioni collegate)

*Nel dominio pagamenti*: il ledger/i saldi restano quasi sempre su SQL (Oracle, nel tuo caso) per garanzie ACID; NoSQL entra spesso per casi specifici come cache (Redis per idempotency key o rate limiting), audit log ad alto volume, o fraud detection basata su grafi.

**Pattern di accesso**

- **Repository pattern**: astrae la logica di persistenza dietro un'interfaccia — è esattamente quello che fa Spring Data JPA con le interfacce `Repository`, già visto in precedenza
- **Unit of Work**: raggruppa più operazioni in un'unica transazione logica, garantendo che vengano tutte committate o tutte annullate insieme — in Spring è implicito nel comportamento di `@Transactional` insieme al *persistence context* di JPA
- **Connection pooling**: mantiene un pool di connessioni DB già aperte e riutilizzabili, evitando il costo di aprirne una nuova ad ogni richiesta (es. HikariCP, il pool di default in Spring Boot)
- **Read replicas**: repliche del DB principale usate solo per letture, per distribuire il carico e non appesantire il DB primario che gestisce le scritture — utile per query di reportistica pesanti senza impattare le transazioni live
- **Caching** (Redis, Memcached): riduce il carico sul database tenendo in memoria dati letti di frequente e poco variabili — attenzione però all'invalidazione della cache quando i dati sottostanti cambiano (uno dei problemi classici dell'informatica: "cache invalidation is hard")

**Database per microservizi**

Ogni servizio dovrebbe avere il proprio database (**database isolation**), coerente con quanto visto nella sezione sui microservizi. Per mantenere la consistenza tra database separati, si usano:
- **Eventual consistency**: si accetta che i dati siano temporaneamente disallineati tra servizi, convergendo dopo un breve periodo tramite eventi
- **Saga pattern** (già visto): coordina transazioni distribuite con compensazioni
- **Eventi di dominio**: un servizio pubblica un evento quando cambia stato, gli altri servizi interessati lo consumano e aggiornano la propria vista dei dati

**Ottimizzazione**

- **Indici**: già visto in dettaglio nella sezione sull'execution plan
- **Query optimization**: evitare funzioni sulle colonne indicizzate nel WHERE, preferire join efficienti, limitare le colonne selezionate
- **Partitioning/sharding**: dividere una tabella molto grande in partizioni più piccole (per range di data, per hash di una chiave) per migliorare performance e manutenibilità — rilevante per tabelle di transazioni che crescono continuamente, spesso partizionate per mese/anno
- **Denormalizzazione**: duplicare deliberatamente alcuni dati per evitare join costosi in lettura, a costo di maggiore complessità in scrittura — scelta valida quando le letture sono molto più frequenti delle scritture

### Come esercitarti
Prepara una risposta breve a "quando useresti NoSQL invece di Oracle in un sistema di pagamenti?" — la risposta corretta non è "mai" né "sempre", ma un esempio mirato: cache per idempotency key con Redis, o audit log ad alto volume, mantenendo il ledger transazionale su Oracle per le garanzie ACID.

---

## 11. Concetti Trasversali Importanti

### Cos'è e perché conta
Sono temi che attraversano tutta l'architettura (sicurezza, osservabilità, CI/CD, resilienza) e che spesso emergono in domande "da senior" — non tanto "sai scrivere questo codice" quanto "sai ragionare sul sistema nel suo complesso".

### Cosa studiare

**Sicurezza**

- **Autenticazione vs autorizzazione**: l'autenticazione verifica *chi sei* (login), l'autorizzazione verifica *cosa puoi fare* (permessi) — distinzione base ma spesso confusa, utile da avere chiara e pronta
- **OAuth 2.0**: protocollo standard per delegare l'accesso senza condividere le credenziali — flussi principali (Authorization Code, Client Credentials per comunicazione server-to-server, rilevante in integrazioni B2B tra sistemi di pagamento)
- **JWT (JSON Web Token)**: token firmato che incapsula informazioni (claims) verificabili senza dover interrogare un DB centrale ad ogni richiesta — attenzione alla differenza tra firma (integrità, chiunque può leggere il contenuto) e cifratura (contenuto nascosto)
- **Gestione dei secrets** (Vault, AWS Secrets Manager): mai credenziali/chiavi hardcoded nel codice o in config in chiaro — un secret manager centralizza, ruota e audita l'accesso a credenziali sensibili
- **Principio del least privilege**: ogni componente/utente ha solo i permessi minimi indispensabili per il proprio compito — riduce l'impatto di una compromissione
- **Encryption at rest e in transit**: dati cifrati sia quando salvati su disco (at rest) sia durante la trasmissione in rete (in transit, tipicamente TLS) — requisito quasi sempre esplicito in ambito PCI-DSS

**Osservabilità**

I tre pilastri:
- **Logging** (ELK stack — Elasticsearch/Logstash/Kibana, Splunk): registrazione di eventi discreti, utile per debug e audit trail
- **Metrics** (Prometheus, Grafana): valori numerici aggregati nel tempo (latenza media, throughput, error rate) — utili per dashboard e alerting
- **Tracing distribuito** (Jaeger, Zipkin): traccia il percorso di una singola richiesta attraverso più microservizi, fondamentale per capire dove si perde tempo o dove fallisce una chiamata in una catena di servizi

**Golden signals** da monitorare: latenza, error rate, throughput (spesso si aggiunge saturazione delle risorse come quarto segnale) — in un sistema di pagamenti questi si traducono direttamente in SLA verso i partner (es. tempo massimo di risposta per un'autorizzazione).

**CI/CD**

- **Pipeline di deployment**: sequenza automatizzata di build, test, quality gate, deploy — collegabile a Jenkins già visto nella sezione toolchain
- **Blue-green deployment**: due ambienti identici (blue e green), il traffico viene spostato istantaneamente dall'uno all'altro dopo il deploy della nuova versione — rollback immediato se qualcosa va storto, semplicemente reindirizzando il traffico indietro
- **Canary release**: la nuova versione viene rilasciata prima a una piccola percentuale di traffico/utenti, per verificarne il comportamento in produzione prima di un rollout completo — riduce il rischio in sistemi critici
- **Rollback automatici**: se le metriche post-deploy peggiorano oltre soglia, il sistema torna automaticamente alla versione precedente
- **Infrastructure as Code** (Terraform, CloudFormation): l'infrastruttura è definita come codice versionabile, invece che configurata manualmente — garantisce riproducibilità e tracciabilità delle modifiche

**Resilienza**

- **Timeout**: ogni chiamata a un servizio esterno deve avere un timeout esplicito, altrimenti un servizio lento può bloccare indefinitamente il chiamante
- **Retry con exponential backoff**: se una chiamata fallisce, riprovare aumentando progressivamente l'attesa tra un tentativo e l'altro (es. 1s, 2s, 4s, 8s), per non sovraccaricare un servizio già in difficoltà
- **Idempotenza delle operazioni**: già vista nella sezione su `@Transactional` — un'operazione ripetuta (es. per un retry) deve avere lo stesso effetto di eseguita una sola volta, cruciale per evitare doppi addebiti
- **Graceful degradation**: se una funzionalità non essenziale fallisce, il sistema continua a funzionare offrendo un servizio ridotto invece di fallire completamente (es. se il servizio di scoring frodi è giù, si può decidere di procedere comunque con un pagamento a basso rischio invece di bloccare tutto)

### Come esercitarti
Collega esplicitamente **retry + idempotenza** al punto già visto su `@Transactional`: è uno dei fili conduttori più forti del colloquio, perché tocca dominio, Spring e architettura distribuita nello stesso concetto — un ottimo esempio da avere pronto e ben padroneggiato.

---

## 12. Approfondimento Database: MongoDB, Cassandra, Elasticsearch, PostgreSQL, MySQL

### Cos'è e perché conta
Il ruolo richiede specificamente Oracle, ma conoscere anche gli altri database più diffusi mostra ampiezza di vedute ed è utile se emergono domande di confronto ("perché Oracle e non altro?") o se nel tempo il sistema integra componenti non relazionali (cache, ricerca, audit log). Qui trovi una descrizione di ciascuno con possibili domande da colloquio e risposte pronte.

### PostgreSQL

**Cos'è**: database relazionale **open source**, spesso considerato il più "avanzato" tra i DB relazionali open source per ricchezza di funzionalità — supporta tipi di dato avanzati (JSON/JSONB nativi, array, tipi geometrici), window function, CTE ricorsive, estensioni (es. PostGIS per dati geospaziali). Molto vicino a Oracle come potenza espressiva SQL, a differenza di MySQL che è storicamente più minimale.

**Quando si usa**: applicazioni che vogliono la robustezza e ricchezza di un DB relazionale enterprise senza costi di licenza — sempre più scelto anche per carichi misti relazionali + documenti JSON grazie a JSONB.

**Domande tipiche e risposte**

- *D: Che differenza c'è tra JSON e JSONB in PostgreSQL?*
  R: `JSON` salva il testo così com'è, senza parsing — più veloce in scrittura, ma ogni lettura richiede riparsing. `JSONB` salva in formato binario già decomposto — leggermente più lento in scrittura, ma molto più veloce in lettura e supporta indicizzazione (es. GIN index) sui campi interni. Nella pratica si usa quasi sempre JSONB.

- *D: PostgreSQL è ACID?*
  R: Sì, pienamente conforme ACID come Oracle — supporta transazioni, isolamento configurabile (stessi livelli visti per Oracle: READ_COMMITTED è il default), vincoli di integrità referenziale.

- *D: Quando useresti PostgreSQL invece di Oracle in un progetto nuovo?*
  R: Per carichi di lavoro che non richiedono le funzionalità enterprise specifiche di Oracle (RAC, Data Guard) e dove i costi di licenza pesano — ma in un contesto già consolidato su Oracle con competenze/tooling esistenti (come nel ruolo per cui ti candidi), raramente ha senso migrare solo per questo.

### MySQL

**Cos'è**: database relazionale open source storicamente il più diffuso al mondo (soprattutto nel web, es. stack LAMP). Più "leggero" di PostgreSQL/Oracle in termini di funzionalità avanzate, ma estremamente performante per carichi di lettura/scrittura semplici e ad alto volume.

**Quando si usa**: applicazioni web con volumi alti ma logica relazionale non troppo complessa — meno indicato quando servono funzionalità SQL avanzate o forte integrità transazionale su scenari complessi.

**Domande tipiche e risposte**

- *D: Che differenza c'è tra i motori di storage InnoDB e MyISAM in MySQL?*
  R: InnoDB (default da anni) supporta transazioni ACID, foreign key, row-level locking. MyISAM è più vecchio, non supporta transazioni né foreign key, usa table-level locking — oggi praticamente non si usa più per nuovi progetti se serve integrità transazionale.

- *D: MySQL è adatto a un sistema di pagamenti?*
  R: Tecnicamente sì con InnoDB (è ACID compliant), ma in contesti enterprise regolamentati come i pagamenti si preferisce quasi sempre Oracle o PostgreSQL per le funzionalità avanzate di gestione, sicurezza, supporto enterprise e strumenti di alta affidabilità (clustering, disaster recovery) più maturi.

### MongoDB

**Cos'è**: il **document store** NoSQL più diffuso — salva dati come documenti in formato simile a JSON (BSON), organizzati in collection invece che tabelle. Schema flessibile: documenti nella stessa collection possono avere strutture diverse.

**Quando si usa**: dati semi-strutturati o che cambiano forma nel tempo, dove uno schema fisso relazionale sarebbe troppo rigido — es. cataloghi prodotto con attributi variabili, log applicativi, configurazioni.

**Domande tipiche e risposte**

- *D: MongoDB è ACID?*
  R: Dalla versione 4.0 supporta transazioni ACID multi-documento, ma storicamente (ed è ancora il caso d'uso più naturale) è pensato per garanzie di atomicità solo a livello di singolo documento — per questo motivo si modella spesso i dati "denormalizzati", incapsulando in un unico documento le informazioni che in un DB relazionale sarebbero su più tabelle collegate.

- *D: Perché non useresti MongoDB come DB principale in un sistema di pagamenti?*
  R: Il core di un sistema di pagamenti richiede relazioni forti e consistenza immediata su transazioni multi-entità (account, transazione, ledger) — lo schema fisso e le garanzie ACID native di un DB relazionale come Oracle si adattano meglio. MongoDB può però avere un ruolo di supporto: es. salvare payload di richieste/risposte verso circuiti esterni (formati variabili, poco strutturati) senza dover forzare uno schema rigido.

- *D: Come funziona lo sharding in MongoDB?*
  R: I dati vengono partizionati orizzontalmente su più nodi in base a una **shard key** — ogni nodo gestisce un sottoinsieme dei dati, permettendo scalabilità orizzontale su volumi molto grandi. La scelta della shard key è critica: una scelta cattiva può creare "hot shard" (nodi sovraccarichi mentre altri restano inattivi).

### Cassandra

**Cos'è**: database NoSQL **column-family**, progettato da Facebook per scalabilità estrema in scrittura e alta disponibilità distribuita su più data center, senza singolo punto di fallimento (architettura *masterless*, ogni nodo è equivalente).

**Quando si usa**: scenari con volumi di scrittura altissimi e necessità di disponibilità continua anche in caso di guasto di un intero data center — tipico per time-series data, log di eventi, sistemi IoT.

**Domande tipiche e risposte**

- *D: Che modello di consistenza usa Cassandra?*
  R: **Eventual consistency** per default, configurabile per singola query attraverso il **consistency level** (es. `ONE`, `QUORUM`, `ALL`) — puoi scegliere quanti nodi devono confermare una scrittura/lettura prima di considerarla riuscita, bilanciando consistenza e disponibilità/latenza (è un'applicazione pratica del **teorema CAP**: Cassandra privilegia Availability e Partition tolerance sulla Consistency forte, a differenza di un DB relazionale).

- *D: Perché Cassandra scrive così velocemente rispetto a un DB relazionale?*
  R: Usa una struttura dati **LSM-tree** (Log-Structured Merge-tree): le scritture vengono prima accodate in memoria (memtable) e poi periodicamente scritte su disco in blocchi ordinati (SSTable) in modo sequenziale, evitando i costosi update in-place e la ricerca di righe esistenti tipici di un DB relazionale.

- *D: Useresti Cassandra in un sistema di pagamenti?*
  R: Non per il ledger transazionale (serve consistenza forte, non eventual), ma potrebbe avere senso per un **audit log** ad altissimo volume di eventi (ogni chiamata API, ogni tentativo di autenticazione) dove la scrittura veloce e la disponibilità contano più della consistenza immediata.

### Elasticsearch

**Cos'è**: motore di ricerca e analisi distribuito, basato su Lucene. Non è un database relazionale né un semplice document store — è specializzato in **ricerca full-text veloce** e aggregazioni su grandi volumi di dati semi-strutturati (JSON).

**Quando si usa**: ricerca testuale (es. autocomplete, ricerca fuzzy), log centralizzati (è la "E" di ELK stack, già citato nella sezione osservabilità), dashboard di analytics su grandi volumi di eventi.

**Domande tipiche e risposte**

- *D: Elasticsearch può sostituire un database relazionale?*
  R: No — non ha transazioni ACID forti, gli aggiornamenti frequenti di singoli documenti sono relativamente costosi (ogni update in Lucene comporta la reindicizzazione del documento), e non è pensato per essere la fonte di verità (*source of truth*) dei dati. Si usa tipicamente **in affiancamento** a un DB relazionale: i dati "vivono" nel DB principale (es. Oracle) e vengono replicati/indicizzati in Elasticsearch solo per abilitare ricerca veloce.

- *D: Come funziona l'indicizzazione in Elasticsearch?*
  R: I documenti JSON vengono analizzati (*analysis*): il testo viene tokenizzato, normalizzato (lowercase, stemming) e mappato in un **indice invertito** — una struttura che associa ogni token ai documenti che lo contengono, permettendo ricerche full-text molto veloci rispetto a una scansione `LIKE '%...%'` su un DB relazionale.

- *D: Che ruolo avrebbe Elasticsearch in un sistema di pagamenti?*
  R: Principalmente per **osservabilità** (centralizzare e cercare nei log applicativi di tutti i microservizi, come già visto nella sezione ELK) e per dashboard operative che devono aggregare/filtrare velocemente grandi volumi di transazioni per supporto clienti o investigazioni antifrode — non come sistema di registrazione delle transazioni stesse.

### Tabella riassuntiva per orientarti velocemente

| Database | Tipo | Punto di forza | Ruolo tipico in un sistema di pagamenti |
|---|---|---|---|
| Oracle / PostgreSQL | Relazionale | ACID, integrità, query complesse | Ledger, saldi, transazioni core |
| MySQL | Relazionale | Semplicità, alte performance su carichi semplici | Meno tipico in ambito enterprise pagamenti |
| MongoDB | Document store | Schema flessibile | Payload esterni non strutturati, configurazioni |
| Cassandra | Column-family | Scrittura massiva, alta disponibilità | Audit log/eventi ad altissimo volume |
| Elasticsearch | Motore di ricerca | Full-text search, aggregazioni veloci | Log centralizzati, dashboard di supporto/antifrode |

### Come esercitarti
La domanda più probabile in un colloquio non è "spiegami MongoDB" isolatamente, ma "quando useresti X invece di Y" — esercitati proprio sulla tabella sopra: per ogni riga, prepara una frase che spieghi *perché* quel database è la scelta giusta per quel ruolo specifico, collegandola sempre al fatto che il ledger transazionale resta comunque su un DB relazionale con garanzie ACID forti.

---

## 13. Strategie per la Gestione dei Database in Architetture a Microservizi

### Cos'è e perché conta
Riassume e completa in chiave pratica i pattern già visti nelle sezioni sui microservizi e sull'accesso ai database (punti 8 e 10), rispondendo alla domanda "come gestisco letture/scritture concorrenti quando i dati sono sparsi su più servizi?" — un tema molto probabile in un colloquio senior, perché è dove la teoria dei microservizi incontra i problemi reali di concorrenza e consistenza.

### Cosa studiare

**1. Database per Microservizio (Database per Service)**

Ogni microservizio ha il proprio database dedicato — pattern già visto nel punto 8. I vantaggi principali:
- **Isolamento dei dati**: un servizio non può corrompere accidentalmente i dati di un altro
- **Indipendenza tecnologica**: ogni servizio può usare il DB più adatto al proprio caso d'uso (vedi tabella comparativa nel punto 12 — es. Oracle per il ledger, Redis per cache di un servizio specifico)
- **Riduzione delle dipendenze**: un servizio può evolvere lo schema del proprio DB senza coordinarsi con tutti gli altri

Il rovescio della medaglia (utile menzionarlo per dimostrare visione equilibrata): niente più join SQL tra dati di servizi diversi, e niente più transazione ACID unica che copre più servizi — da qui nascono i pattern successivi.

**2. Event Sourcing e CQRS**

Già introdotti nel punto 8, li ripercorriamo con focus sulla gestione della concorrenza:
- Gli eventi vengono memorizzati in un **log di eventi** immutabile (append-only) — invece di sovrascrivere lo stato, si registra ogni cambiamento come nuovo evento
- I comandi (scritture) modificano lo stato generando nuovi eventi, mentre le query (letture) leggono da una **vista materializzata** separata, costruita e aggiornata a partire dagli eventi
- Perché riduce i conflitti di concorrenza: dato che le scritture sono append-only (si aggiunge un nuovo evento, non si modifica uno esistente), il classico problema del "lost update" tra due scritture concorrenti sullo stesso record si riduce drasticamente
- Offre **tracciabilità completa**: ogni cambiamento di stato è ricostruibile — molto rilevante in un dominio regolamentato come i pagamenti, dove poter dimostrare "chi ha cambiato cosa e quando" è spesso un requisito di audit/compliance

**3. Transazioni Distribuite**

- **Saga pattern** (già visto nel punto 8): sequenza di transazioni locali con compensazioni in caso di fallimento — l'approccio oggi preferito nei microservizi
- **Two-Phase Commit (2PC)**: protocollo classico per garantire consistenza tra più risorse — un coordinatore chiede a tutti i partecipanti di "prepararsi" (fase 1, ognuno conferma che può eseguire l'operazione), e solo se **tutti** confermano invia il comando di commit definitivo (fase 2); se anche uno solo fallisce nella fase di prepare, tutti fanno rollback
  - *Perché in pratica si evita nei microservizi moderni*: 2PC richiede che tutte le risorse restino bloccate (lock) per tutta la durata del protocollo, in attesa della decisione finale del coordinatore — questo riduce drasticamente la disponibilità e non scala bene, oltre a creare un singolo punto di fallimento nel coordinatore. Per questo la Saga (che rinuncia alla atomicità immediata in cambio di eventual consistency con compensazioni) è preferita nella maggior parte dei sistemi distribuiti moderni
- **Transazioni di compensazione**: l'azione di "annullamento logico" usata nella Saga quando un passo successivo fallisce — non è un vero rollback (impossibile su DB separati), ma un'operazione inversa esplicita (es. se hai già addebitato un conto, la compensazione è un accredito di pari importo, non la cancellazione della scrittura originale)

**4. Architettura Event-Driven**

Un message broker (Kafka, RabbitMQ) disaccoppia i servizi:
- Il produttore pubblica un evento senza sapere chi lo consumerà, né aspettare che venga processato
- Garantisce consistenza attraverso **code di messaggi** persistenti: se un consumer è temporaneamente giù, i messaggi restano in coda e vengono processati al suo ritorno, invece di perdersi
- Permette operazioni **asincrone**, già discusso nel punto 8 per il caso della notifica post-transazione

**5. Locking e Concurrency Control**

Già accennato nella sezione Oracle (punto 3) parlando di isolation level, qui si generalizza al contesto applicativo:
- **Pessimistic locking**: si blocca la risorsa (es. `SELECT FOR UPDATE`) per tutta la durata dell'operazione, impedendo ad altri di modificarla nel frattempo — sicuro ma riduce la concorrenza, utile quando i conflitti sono frequenti
- **Optimistic locking**: non si blocca nulla in anticipo; si verifica invece, al momento del salvataggio, che i dati non siano stati modificati da qualcun altro nel frattempo — tipicamente con una colonna di versione (`@Version` in JPA): se la versione letta non coincide più con quella a DB, l'update fallisce e va gestito un retry o un errore applicativo. Preferibile quando i conflitti sono rari, perché non paga il costo del lock quando non serve
- **Meccanismi di retry e gestione dei conflitti**: quando un optimistic lock fallisce, la strategia comune è ritentare l'operazione (spesso con backoff, collegandosi al punto sulla resilienza nel punto 11) invece di propagare subito l'errore all'utente

**6. Sharding e Partizionamento**

Già visto nel punto 10 per il contesto Oracle/tabelle grandi, qui nella lente della gestione dati distribuita tra servizi:
- **Suddivisione orizzontale dei dati** su più istanze/nodi in base a una chiave (es. per range di data, per hash di un ID account)
- Migliora prestazioni e scalabilità perché ogni nodo gestisce solo una porzione dei dati e del carico
- Riduce i colli di bottiglia, ma introduce complessità: query che devono aggregare dati da più shard diventano più costose, e la scelta della shard key è una decisione difficile da cambiare in seguito senza una migrazione onerosa

**7. Caching Distribuito**

Già visto nel punto 10 come pattern di ottimizzazione, qui nel contesto specifico della concorrenza tra servizi:
- Redis/Memcached come cache condivisa tra più istanze di uno stesso servizio (o tra servizi diversi, se il dato è comune)
- Riduce il carico sul database per i dati letti più di frequente
- Attenzione alla **coerenza tra cache e DB**: in un sistema con più scritture concorrenti, una cache non invalidata correttamente può restituire dati obsoleti — un problema di concorrenza a sé, spesso sottovalutato

### Considerazioni chiave e raccomandazioni

Nessuna di queste soluzioni è universale — la scelta dipende da:
- Dimensioni del sistema e volumi di dati
- Requisiti di consistenza (forte vs eventual)
- Complessità delle operazioni coinvolte
- Performance richieste (latenza, throughput)

Un buon approccio, utile anche come risposta "da senior" a colloquio:
- **Iniziare semplice** e aggiungere complessità solo quando serve realmente — introdurre Saga/Event Sourcing/sharding fin da subito su un sistema piccolo è spesso over-engineering
- **Valutare i requisiti specifici** prima di scegliere il pattern, non il contrario
- **Testare accuratamente i meccanismi di concorrenza** — sono la categoria di bug più insidiosa perché spesso non si manifestano in ambienti di test a basso carico
- **Implementare monitoraggio e logging** (collegandosi al punto 11 sull'osservabilità) per individuare rapidamente conflitti, retry falliti, o incoerenze tra servizi in produzione

### Come esercitarti
Prepara una risposta strutturata alla domanda "come garantiresti la consistenza di un pagamento che coinvolge tre microservizi diversi (autorizzazione, contabilità, notifica)?" — la risposta ideale cita: database per service come punto di partenza architetturale, Saga con compensazioni per coordinare i tre servizi, eventi asincroni via Kafka/RabbitMQ per disaccoppiarli, e idempotenza (già vista più volte nel documento) per gestire in sicurezza eventuali retry.

---

## 14. Panoramica delle Versioni Java (da 8 a 25)

### Cos'è e perché conta
Il ruolo richiede "Java 8+", quindi è probabile che l'ambiente di produzione sia su una versione LTS consolidata (8, 11, 17, forse 21) più che sull'ultimissima release. Questa panoramica serve soprattutto per orientarti rapidamente su **cosa è stato introdotto e quando**, utile se ti chiedono "conosci le differenze tra Java 8 e versioni più recenti?" o per collegare le feature già approfondite nel documento (Stream, Optional, Records, Sealed Classes, Pattern Matching) alla loro versione di introduzione. Le versioni **LTS** (Long-Term Support) sono evidenziate perché sono quelle realisticamente in uso in ambito enterprise.

### Le versioni, in sintesi

**Java 8 (2014) — LTS**
- Lambda expression e functional interface (approfondito nel punto 2)
- Stream API per elaborazione dati in stile funzionale
- `Optional<T>`
- Nuova Date/Time API (`java.time`)
- Metodi `default` e `static` nelle interfacce

**Java 9 (2017)**
- Module System (JPMS) — Project Jigsaw
- JShell (REPL interattivo)
- Miglioramenti a Stream, Optional, CompletableFuture

**Java 10 (2018)**
- Local Variable Type Inference (`var`)
- Miglioramenti al Garbage Collector (G1 parallelo)

**Java 11 (2018) — LTS**
- HTTP Client API standardizzata
- `var` usabile nei parametri lambda
- Rimozione di Java EE e CORBA
- Nuovi metodi `String` (`isBlank()`, `strip()`, `repeat()`)

**Java 12 (2019)**
- Switch Expressions (preview)
- Shenandoah GC (sperimentale)

**Java 13 (2019)**
- Text Blocks (preview)
- Switch Expressions migliorate

**Java 14 (2020)**
- Switch Expressions (standard)
- Records (preview)
- Pattern Matching for `instanceof` (preview)
- Helpful NullPointerException (messaggi di errore più precisi)

**Java 15 (2020)**
- Text Blocks (standard)
- Sealed Classes (preview) — approfondito nel punto 7
- Hidden Classes

**Java 16 (2021)**
- Records (standard)
- Pattern Matching for `instanceof` (standard)
- Vector API (incubator)

**Java 17 (2021) — LTS**
- Sealed Classes (standard)
- Pattern Matching for `switch` (preview)
- Rimozione RMI Activation, Applet API deprecata

**Java 18 (2022)**
- UTF-8 come charset predefinito
- Simple Web Server

**Java 19 (2022)**
- Virtual Threads (preview) — Project Loom
- Structured Concurrency (incubator)
- Pattern Matching for `switch` (secondo preview)

**Java 20 (2023)**
- Continuazione preview di Virtual Threads e Structured Concurrency
- Record Patterns (secondo preview)

**Java 21 (2023) — LTS**
- Virtual Threads (standard) — probabilmente la feature più rilevante degli ultimi anni per applicazioni backend ad alta concorrenza
- Pattern Matching for `switch` (standard) — usato nell'esempio con `sealed` nel punto 7
- Record Patterns (standard)
- Sequenced Collections
- Structured Concurrency (preview)
- Generational ZGC

**Java 22 (2024)**
- Statement prima di `super()` nei costruttori
- Unnamed Variables & Patterns
- Foreign Function & Memory API (standard)

**Java 23 (2024)**
- Markdown in Javadoc
- Structured Concurrency (terzo preview)

**Java 24 (2025)**
- Class-File API (standard)
- Miglioramenti a Structured Concurrency e Scoped Values
- Quantum-resistant algorithms (preview)

**Java 25 (2025) — LTS**
La LTS successiva a Java 21, con diverse JEP focalizzate su sintassi più pulita, concorrenza più sicura, workflow di sicurezza semplificati e performance di startup/runtime più veloci:
- Generational Mode dello Shenandoah GC promossa da sperimentale a feature di prodotto, con miglior efficienza di memoria e consistenza dei pause-time
- Scoped Values finalizzati come alternativa a `ThreadLocal`
- Semplificazione della creazione dell'AOT cache tramite comandi unificati, per ridurre l'attrito nell'ottimizzazione dello startup
- Profiling a livello di metodo per ottimizzare la compilazione AOT
- Compact Object Headers come feature stabile
- Pattern matching esteso ai tipi primitivi in `switch`/`instanceof`

### Le tappe davvero rilevanti per un colloquio "Java 8+"

Se il tempo per ripassare è limitato, concentrati su queste, in ordine di probabilità che emergano:
1. **Java 8**: è la base del ruolo, va padroneggiata a fondo (già coperta nel punto 2)
2. **Java 11**: prima LTS successiva, spesso il target minimo in molte aziende che sono migrate da 8
3. **Java 17**: LTS molto diffusa oggi, introduce Sealed Classes e consolida Records — buona da conoscere anche solo concettualmente
4. **Java 21**: LTS più recente, la novità più "importante" da menzionare se emerge il tema sono i **Virtual Threads**, perché risolvono un problema concreto (gestire migliaia di connessioni concorrenti senza il costo di un thread OS per ciascuna) particolarmente rilevante in sistemi ad alto throughput come i pagamenti

### Come esercitarti
Prepara una frase che colleghi Java 8 al presente: "conosco bene le feature di Java 8 richieste dal ruolo, e mi tengo aggiornato anche sulle versioni successive — ad esempio i Virtual Threads di Java 21 sarebbero rilevanti in un sistema ad alta concorrenza come questo, se in futuro si valutasse un aggiornamento della piattaforma." Mostra sia solidità sui requisiti richiesti sia curiosità verso l'evoluzione del linguaggio, qualità esplicitamente richiesta nella job description ("curiosità e propensione alla ricerca").

---

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

---

## 16. Redis

### Cos'è
Database **in-memory key-value**, estremamente veloce (dati tenuti in RAM), usato principalmente come cache, ma anche come message broker leggero (pub/sub), store di sessioni, o per strutture dati specializzate (contatori, code, set, sorted set).

### Caratteristiche principali

- **Strutture dati ricche**: non solo stringhe, ma anche liste, set, hash, sorted set (utili per classifiche/ranking), tutte con operazioni atomiche native
- **Persistenza opzionale**: pur essendo in-memory, supporta snapshot su disco (RDB) o log delle operazioni (AOF) per non perdere tutto in caso di riavvio — comunque non sostituisce un DB transazionale
- **TTL (Time To Live)**: ogni chiave può avere una scadenza automatica — fondamentale per cache che non deve restare stale indefinitamente
- **Operazioni atomiche**: es. `INCR` per contatori concorrenti senza race condition, utile per rate limiting
- **Pub/Sub**: meccanismo di messaggistica semplice (non persistente come Kafka — se non c'è un subscriber attivo, il messaggio si perde)
- **Cluster mode**: sharding automatico dei dati su più nodi per scalabilità orizzontale

### Esempio di utilizzo (Spring Boot)

```java
// Cache di un risultato costoso da ricalcolare
@Cacheable(value = "accountBalance", key = "#accountId")
public BigDecimal getBalance(String accountId) {
    return accountRepository.calculateBalance(accountId); // query pesante
}

// Idempotency key con TTL, via RedisTemplate
public boolean tryLockIdempotencyKey(String key) {
    Boolean success = redisTemplate.opsForValue()
        .setIfAbsent(key, "PROCESSED", Duration.ofMinutes(10));
    return Boolean.TRUE.equals(success); // true solo se la chiave non esisteva già
}
```

### Rilevanza per il dominio pagamenti
Due casi d'uso molto naturali: **cache** per dati letti di frequente e poco variabili (es. configurazioni, dati anagrafici merchant), e **gestione dell'idempotenza** tramite `SETNX`/`setIfAbsent` con TTL — un modo rapido per verificare "questa richiesta è già stata processata?" senza appesantire il DB transazionale principale. Anche utile per **rate limiting** sulle chiamate verso circuiti esterni, con `INCR` + TTL per contare le richieste in una finestra temporale.

### Domande tipiche e risposte

- *D: Redis è adatto a salvare il saldo di un conto come fonte di verità?*
  R: No — è in-memory e pensato per velocità, non per le garanzie ACID complete che servono per il ledger. Il saldo "vero" resta su Oracle; Redis può cachearne una copia in lettura, ma ogni scrittura deve passare dal DB transazionale.

- *D: Come implementeresti un idempotency check con Redis?*
  R: Con `SETNX` (o `setIfAbsent` in Spring Data Redis) usando l'idempotency key come chiave — l'operazione è atomica, quindi se due richieste concorrenti arrivano nello stesso istante, solo una riuscirà a impostare la chiave, l'altra saprà che la richiesta è già in corso/completata. Si imposta un TTL per non accumulare chiavi indefinitamente.

---

## 17. Kubernetes

### Cos'è
Piattaforma di **orchestrazione container**, che gestisce automaticamente deployment, scaling, self-healing e networking di applicazioni containerizzate (tipicamente Docker). Non esegue direttamente il codice: coordina container su un cluster di macchine (nodi).

### Caratteristiche principali

- **Pod**: unità minima di deployment — uno o più container che condividono rete e storage, eseguiti sempre insieme sullo stesso nodo
- **Deployment**: definisce quante repliche di un pod devono essere in esecuzione e gestisce gli aggiornamenti (rolling update) senza downtime
- **Service**: espone un insieme di pod come un endpoint di rete stabile, con load balancing automatico tra le repliche — anche se i pod vengono ricreati con IP diversi, il Service resta raggiungibile allo stesso indirizzo
- **ConfigMap e Secret**: configurazione esterna all'immagine del container (coerente col principio 12-factor già visto nel punto 9) — ConfigMap per configurazioni non sensibili, Secret per credenziali/chiavi
- **Horizontal Pod Autoscaler**: scala automaticamente il numero di pod in base a metriche (es. CPU) — implementazione concreta dell'auto-scaling già visto nel punto 9
- **Liveness/Readiness probe**: health check che Kubernetes usa per capire se un pod è vivo (liveness — altrimenti lo riavvia) e se è pronto a ricevere traffico (readiness — altrimenti lo esclude temporaneamente dal load balancing) — implementazione concreta di health check e self-healing (punto 9)
- **Namespace**: partizione logica del cluster, utile per isolare ambienti (dev, staging, produzione) o team diversi

### Esempio concettuale (non serve saperlo scrivere a memoria, ma riconoscerlo)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: authorization-service
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: authorization-service
          image: registry.company.com/authorization-service:1.4.0
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
```

### Rilevanza per il dominio pagamenti
In un sistema mission-critical, Kubernetes garantisce che un servizio come `authorization-service` resti sempre disponibile con più repliche, si riavvii automaticamente in caso di crash (self-healing), e scali automaticamente nei picchi di traffico — tutto senza intervento manuale. I probe di readiness sono particolarmente importanti: un servizio di pagamento non ancora pronto (es. connessione DB non ancora stabilita all'avvio) non deve ricevere traffico prematuramente.

### Domande tipiche e risposte

- *D: Che differenza c'è tra liveness e readiness probe?*
  R: La liveness probe dice a Kubernetes "sono vivo o devo essere riavviato?" — se fallisce, il pod viene ucciso e ricreato. La readiness probe dice "sono pronto a ricevere traffico in questo momento?" — se fallisce, il pod resta in esecuzione ma viene temporaneamente escluso dal load balancing, utile ad esempio durante l'avvio o se una dipendenza esterna è momentaneamente non raggiungibile.

- *D: Come gestisce Kubernetes un deployment senza downtime?*
  R: Con un **rolling update**: crea gradualmente i nuovi pod con la versione aggiornata, aspetta che passino la readiness probe, e solo allora rimuove gradualmente i pod vecchi — mantenendo sempre un numero minimo di repliche disponibili durante la transizione. Si collega al blue-green/canary già visti nel punto 11, che in Kubernetes si implementano con strategie di deployment più sofisticate sopra questo meccanismo base.

---

## 18. Spring Integration

### Cos'è
Framework che implementa gli **Enterprise Integration Patterns (EIP)** nell'ecosistema Spring — fornisce componenti pronti per costruire flussi di integrazione tra sistemi (trasformazione messaggi, routing condizionale, aggregazione, chiamate a servizi esterni) senza scrivere da zero la logica di "collegamento" a mano.

### Caratteristiche principali

- **Message**: unità base di dati che fluisce nel sistema, con un payload e degli header
- **Channel**: il "tubo" attraverso cui i messaggi si muovono tra componenti — può essere diretto (sincrono) o basato su coda (asincrono)
- **Endpoint**: i componenti che elaborano i messaggi lungo il flusso:
  - **Transformer**: trasforma il payload da un formato a un altro (es. XML SOAP verso JSON, rilevante se il tuo lavoro recente su Jackson/SOAP-to-JSON emerge a colloquio)
  - **Router**: instrada il messaggio verso canali diversi in base a una condizione (es. instradare per tipo di circuito di pagamento)
  - **Filter**: scarta messaggi che non soddisfano una condizione
  - **Aggregator**: raggruppa più messaggi correlati in uno solo (es. attendere tutte le risposte di un batch prima di procedere)
  - **Gateway**: punto di ingresso/uscita che espone il flusso di integrazione come una normale chiamata a metodo Java
- **Adapter**: connettori pronti verso sistemi esterni (file, JMS, Kafka, FTP, database, HTTP) — evitano di scrivere codice di integrazione custom per ogni protocollo

### Esempio di utilizzo

```java
@Bean
public IntegrationFlow paymentNotificationFlow() {
    return IntegrationFlow.from("paymentEventsChannel")
        .filter((PaymentEvent e) -> e.getStatus() == PaymentStatus.COMPLETED)
        .transform(this::toNotificationPayload)
        .handle(Http.outboundGateway("https://notification-service/api/notify"))
        .get();
}
```

### Rilevanza per il dominio pagamenti
Utile quando serve orchestrare flussi di integrazione con più passaggi verso sistemi esterni eterogenei (banche, circuiti, provider terzi) senza scrivere codice di "collante" ripetitivo — ad esempio ricevere un messaggio da un adapter JMS, trasformarlo, instradarlo in base al tipo di circuito, e inoltrarlo via HTTP o Kafka. È meno centrale rispetto a Kafka/microservizi puri, ma può comparire in sistemi enterprise più datati o in integrazioni legacy con banche/circuiti che usano protocolli meno moderni.

### Domande tipiche e risposte

- *D: Quando useresti Spring Integration invece di scrivere manualmente la logica di orchestrazione?*
  R: Quando il flusso di integrazione ha più passaggi standard (trasformazione, routing, filtering) verso sistemi eterogenei — Spring Integration evita di reinventare pattern già risolti (EIP) e rende il flusso dichiarativo e più leggibile rispetto a codice imperativo sparso.

---

## 19. WebSocket

### Cos'è
Protocollo di comunicazione che stabilisce una connessione **full-duplex persistente** tra client e server su un singolo socket TCP — a differenza di HTTP tradizionale (richiesta/risposta, connessione chiusa dopo ogni scambio), con WebSocket sia client che server possono inviare messaggi in qualsiasi momento sulla stessa connessione aperta.

### Caratteristiche principali

- **Handshake iniziale via HTTP**: la connessione parte come una normale richiesta HTTP con header `Upgrade: websocket`, poi "sale di livello" a una connessione WebSocket persistente
- **Full-duplex**: comunicazione bidirezionale simultanea, non serve che il client "chieda" per ricevere un aggiornamento dal server (a differenza del polling HTTP tradizionale)
- **Basso overhead**: dopo l'handshake iniziale, i messaggi successivi hanno un overhead molto ridotto rispetto a ripetute richieste HTTP, rendendolo adatto ad aggiornamenti frequenti e a bassa latenza
- **STOMP su WebSocket**: in Spring, si usa spesso il protocollo STOMP sopra WebSocket per avere un modello a messaggi/topic più strutturato (simile a un message broker), invece di gestire i frame WebSocket grezzi

### Esempio di utilizzo (Spring Boot)

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws-notifications").withSockJS();
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic");
        registry.setApplicationDestinationPrefixes("/app");
    }
}

// Invio di un aggiornamento in tempo reale
@Autowired
private SimpMessagingTemplate messagingTemplate;

public void notifyTransactionStatus(String accountId, TransactionStatus status) {
    messagingTemplate.convertAndSend("/topic/account/" + accountId, status);
}
```

### Rilevanza per il dominio pagamenti
Utile per **notifiche in tempo reale** verso un frontend/dashboard — ad esempio aggiornare istantaneamente lo stato di una transazione mentre viene processata (in attesa → autorizzata → completata), senza che il client debba fare polling continuo. Rilevante anche per dashboard operative interne che monitorano transazioni live o alert su anomalie.

### Domande tipiche e risposte

- *D: Perché non usare semplicemente il polling HTTP per aggiornamenti in tempo reale?*
  R: Il polling genera traffico costante anche quando non ci sono aggiornamenti reali, introduce latenza (l'aggiornamento arriva solo al prossimo poll) e non scala bene con molti client. WebSocket mantiene una connessione aperta e il server può inviare aggiornamenti nell'istante in cui accadono, con overhead molto minore.

- *D: WebSocket è adatto per comunicazione tra microservizi?*
  R: Non è la scelta tipica — tra servizi backend si preferisce REST/gRPC (sincrono) o un message broker come Kafka/RabbitMQ (asincrono), entrambi più adatti a comunicazione server-to-server con garanzie di delivery/retry. WebSocket è pensato principalmente per comunicazione client-server in tempo reale (es. verso un frontend o un'app mobile).

---

## 20. JMS (Java Message Service)

### Cos'è
API standard Java (parte di Jakarta EE) per la messaggistica asincrona — definisce un'interfaccia comune indipendente dal broker sottostante (ActiveMQ, IBM MQ, e con adattatori anche altri). È concettualmente più "vecchio" e enterprise-oriented rispetto a Kafka, molto diffuso in sistemi bancari/finanziari legacy.

### Caratteristiche principali

- **Due modelli di messaggistica**:
  - **Point-to-Point (Queue)**: un messaggio viene consumato da **un solo** consumer, anche se più consumer sono in ascolto sulla stessa coda — modello classico "task queue"
  - **Publish/Subscribe (Topic)**: un messaggio viene consegnato a **tutti** i subscriber attivi sul topic
- **Message-Driven Bean / `@JmsListener`**: componenti che reagiscono automaticamente all'arrivo di un messaggio
- **Transazionalità**: JMS supporta l'integrazione con transazioni JTA (Java Transaction API), permettendo di coordinare l'invio/ricezione di un messaggio con un'operazione su database nella stessa transazione — un caso d'uso enterprise classico che Kafka non supporta nello stesso modo nativo
- **Acknowledgment modes**: controllano quando un messaggio è considerato "consumato con successo" (automatico, manuale, transazionale) — rilevante per garantire che un messaggio non vada perso se il processing fallisce a metà

### Esempio di utilizzo (Spring Boot)

```java
// Producer
@Autowired
private JmsTemplate jmsTemplate;

public void sendPaymentRequest(PaymentRequest request) {
    jmsTemplate.convertAndSend("payment.requests.queue", request);
}

// Consumer
@JmsListener(destination = "payment.requests.queue")
public void onPaymentRequest(PaymentRequest request) {
    paymentProcessor.process(request);
}
```

### Rilevanza per il dominio pagamenti
JMS è storicamente molto diffuso in ambito bancario/finanziario per l'integrazione tra sistemi legacy — è plausibile trovarlo in un'azienda di pagamenti con un'architettura consolidata da anni, magari in coesistenza con Kafka per i flussi più moderni. La sua integrazione nativa con transazioni JTA lo rende adatto a scenari dove serve la garanzia "o il messaggio viene inviato E la modifica al DB viene committata, oppure nessuna delle due" — un caso che Kafka gestisce diversamente (tramite pattern come outbox, non nativamente).

### Domande tipiche e risposte

- *D: Differenza principale tra JMS e Kafka?*
  R: JMS è pensato per code/topic con semantica di consegna "classica" (un messaggio consumato sparisce dalla coda, salvo configurazioni particolari) e forte integrazione transazionale enterprise; Kafka è un log distribuito con retention configurabile, pensato per throughput altissimo e replay degli eventi, più adatto ad architetture event-driven moderne su larga scala. In sintesi: JMS per messaging enterprise classico e transazionale, Kafka per event streaming ad alto volume.

- *D: Cosa succede se il consumer JMS fallisce durante l'elaborazione di un messaggio?*
  R: Dipende dall'acknowledgment mode: con acknowledgment automatico il messaggio potrebbe risultare già confermato anche se il processing fallisce dopo; per questo in scenari critici si usa acknowledgment manuale o transazionale, così il messaggio torna disponibile (redelivery) se l'elaborazione non è completata con successo — di nuovo, un caso dove l'idempotenza del consumer è essenziale per gestire in sicurezza eventuali redelivery.

---

## 21. Comparazioni: OpenShift vs Kubernetes, RabbitMQ vs Kafka

### Cos'è e perché conta
In un colloquio senior, le domande di confronto ("quando useresti X invece di Y?") sono tra le più frequenti, perché rivelano se hai capito i trade-off e non solo la sintassi. Qui trovi due confronti diretti, molto probabili dato lo stack già discusso.

### OpenShift vs Kubernetes

**Cos'è OpenShift**: piattaforma enterprise di Red Hat **basata su Kubernetes** — non è un'alternativa, è una distribuzione di Kubernetes "batterie incluse", con funzionalità aggiuntive, opinionated defaults e supporto commerciale. Molto diffusa in contesti enterprise regolamentati (banche, assicurazioni, pagamenti) proprio per il supporto e la maggiore rigidità/sicurezza di default.

**Differenze principali**

| Aspetto | Kubernetes (vanilla) | OpenShift |
|---|---|---|
| Natura | Progetto open source, componenti da assemblare | Distribuzione completa "pronta all'uso" di Red Hat |
| Console/UI | Non inclusa di default (serve aggiungere Dashboard) | Console web integrata, ricca di funzionalità |
| Build integrato | Non nativo | **Source-to-Image (S2I)**: build dell'immagine container direttamente da codice sorgente, integrato nella piattaforma |
| Sicurezza di default | Configurazione più permissiva, da irrobustire manualmente | **Security Context Constraints (SCC)** più restrittive di default (es. i container non girano come root per default) — importante in ambienti regolamentati |
| Routing esterno | `Ingress` (richiede un controller a parte) | `Route`, concetto nativo di OpenShift equivalente ma integrato out-of-the-box |
| CLI | `kubectl` | `oc` (superset di `kubectl`, con comandi aggiuntivi) |
| Supporto commerciale | Community/vendor dipendente | Supporto enterprise Red Hat incluso — spesso decisivo in ambito bancario/regolamentato |
| Portabilità | Stesso "motore" sotto entrambi | I concetti base (Pod, Deployment, Service) restano identici — le competenze Kubernetes si trasferiscono direttamente a OpenShift |

**Perché è rilevante**: le competenze Kubernetes (Pod, Deployment, Service, ConfigMap, probe, autoscaling — già visti nel punto 17) restano valide identiche su OpenShift, che aggiunge principalmente governance, sicurezza di default più stringente e tooling enterprise sopra lo stesso motore. In un colloquio, sapere dire "conosco Kubernetes, e so che OpenShift è una distribuzione enterprise costruita sopra, con SCC più stringenti e strumenti di build integrati" è una risposta solida anche senza esperienza diretta su OpenShift.

**Domande tipiche e risposte**

- *D: OpenShift e Kubernetes sono alternativi?*
  R: No, OpenShift **è** Kubernetes — nello specifico è una distribuzione certificata e supportata commercialmente da Red Hat, con componenti aggiuntivi (console, S2I, SCC, Route). Chi sa usare Kubernetes ha già la base per lavorare su OpenShift.

- *D: Perché un'azienda regolamentata come una fintech sceglierebbe OpenShift invece di Kubernetes vanilla?*
  R: Per il supporto commerciale enterprise (SLA, patch di sicurezza garantite), le policy di sicurezza più stringenti di default (rilevante per compliance PCI-DSS), e strumenti di governance/multi-tenancy già integrati — riducendo il lavoro di hardening che andrebbe fatto manualmente su Kubernetes vanilla.

### RabbitMQ vs Kafka

Entrambi sono message broker, ma nascono con filosofie diverse: RabbitMQ è un **broker di messaggistica tradizionale** orientato al routing flessibile, Kafka è un **log distribuito di eventi** orientato a throughput e retention.

**Differenze principali**

| Aspetto | RabbitMQ | Kafka |
|---|---|---|
| Modello | Broker con code (AMQP), il messaggio viene rimosso dopo il consumo | Log distribuito partizionato, i messaggi restano per la retention configurata anche dopo la lettura |
| Routing | Molto flessibile: exchange (direct, topic, fanout, headers) permettono routing complesso dei messaggi verso code diverse | Routing più semplice, basato su topic/partition — il routing complesso va gestito applicativamente |
| Throughput | Alto, ma generalmente inferiore a Kafka su volumi molto grandi | Ottimizzato per throughput altissimo (milioni di messaggi/secondo) |
| Ordinamento | Garantito per coda (FIFO), con alcune eccezioni su retry/priorità | Garantito solo all'interno di una singola partizione |
| Replay dei messaggi | Non nativo — un messaggio consumato è normalmente perso | Nativo, grazie alla retention: un consumer può rileggere eventi passati semplicemente ripartendo da un offset precedente |
| Casi d'uso tipici | Task queue, RPC, routing complesso di messaggi tra servizi, scenari dove serve consegna puntuale e prioritizzazione | Event streaming, event sourcing, pipeline di dati, audit trail, integrazione tra molti servizi/consumer sullo stesso stream di eventi |
| Complessità operativa | Generalmente più semplice da gestire su piccola/media scala | Più complessa da operare (Zookeeper/KRaft, partizionamento, tuning), ma pensata per scalare su volumi enterprise |

**Come sceglierli nel dominio pagamenti**

- **RabbitMQ**: adatto per task puntuali con routing condizionale (es. instradare una richiesta di autorizzazione verso il gestore giusto in base al circuito), o per pattern RPC asincroni tra due servizi specifici
- **Kafka**: adatto per propagare eventi di dominio (`TransactionAuthorized`, `TransactionSettled`) a **molti** consumer diversi contemporaneamente (contabilità, notifiche, reportistica, riconciliazione, audit) con necessità di retention/replay per motivi di compliance — coerente con quanto già visto nel punto 15

**Domande tipiche e risposte**

- *D: Se dovessi scegliere uno dei due per un sistema di notifiche transazionali con audit trail, quale sceglieresti e perché?*
  R: Kafka, perché la retention permette di conservare lo storico degli eventi per audit/compliance e di far leggere lo stesso evento a più consumer indipendenti (notifiche, reportistica, riconciliazione) senza che si "consumino" a vicenda — con RabbitMQ, per ottenere lo stesso effetto multi-consumer servirebbe un exchange fanout con una coda dedicata per ogni consumer, più complesso da gestire e senza il replay nativo degli eventi passati.

- *D: RabbitMQ garantisce l'ordine dei messaggi?*
  R: Sì, all'interno di una singola coda i messaggi vengono consegnati nell'ordine di arrivo (salvo l'uso di funzionalità come priorità o retry che possono alterarlo) — ma se più producer scrivono sulla stessa coda o se ci sono più consumer che leggono in parallelo dalla stessa coda, l'ordine di elaborazione non è comunque garantito end-to-end, un dettaglio simile al vincolo di Kafka sull'ordinamento per singola partizione.

### Come esercitarti
Prepara una frase riassuntiva unica per ciascun confronto, da avere pronta: "OpenShift è Kubernetes con più governance e sicurezza di default, utile in contesti regolamentati"; "RabbitMQ per routing flessibile e task puntuali, Kafka per event streaming ad alto volume con retention e replay" — sono le sintesi che un intervistatore si aspetta di sentire in pochi secondi, prima di eventuali approfondimenti.

---

## 22. Troubleshooting e Gestione Incident in Produzione

### Cos'è e perché conta
È un requisito esplicito della job description ("analisi tecnica, troubleshooting e gestione di incident in ambienti di produzione") ma finora mai trattato nel documento. A un senior spesso si chiede non solo "conosci la tecnologia X" ma "come ragioni quando qualcosa si rompe in produzione alle 3 di notte" — è una domanda quasi certa in un colloquio per questo ruolo.

### Metodologia generale (framework da avere pronto)

1. **Individuare e circoscrivere l'impatto**: cosa non funziona, per chi, da quando — prima capire la portata (un cliente? tutti i pagamenti con un circuito specifico? tutti?) che approfondire la causa
2. **Stabilizzare prima di capire**: se esiste un modo rapido per limitare il danno (rollback, feature flag, circuit breaker manuale, failover) si applica **prima** di investigare a fondo la causa — specialmente in un dominio dove ogni minuto di downtime ha un costo diretto
3. **Raccogliere evidenze**: log applicativi, metriche (latenza, error rate — golden signals visti nel punto 11), tracing distribuito se il problema attraversa più servizi
4. **Formulare e verificare ipotesi**: partire dal cambiamento più recente (un deploy? una configurazione? un picco di traffico?) — la causa più probabile di un incident è spesso "cosa è cambiato di recente", non un bug dormiente da mesi
5. **Root cause analysis**: una volta risolto l'impatto immediato, capire la causa profonda — non fermarsi al sintomo (es. "un servizio è andato in OOM" non è la causa, ma il sintomo di un memory leak o di un carico non previsto)
6. **Post-mortem senza colpevolizzazione (blameless)**: documentare cosa è successo, perché, e quali azioni preventive si adottano — pratica standard in ambienti enterprise maturi

### Strumenti concreti da citare

- **Log centralizzati** (ELK, già visto nel punto 11): cercare errori/eccezioni nel periodo dell'incident, correlando per un ID di correlazione/transaction ID che attraversa i vari servizi
- **Tracing distribuito** (Jaeger/Zipkin): capire in quale servizio della catena si è verificato il rallentamento/errore, quando il problema attraversa più microservizi
- **Metriche e dashboard** (Prometheus/Grafana): capire se il problema è graduale (memory leak, saturazione risorse) o improvviso (deploy, picco di traffico)
- **Execution plan** (già visto nel punto 3): se il sintomo è una query lenta, è il primo strumento da controllare

### Esempio di scenario ragionato (utile da avere pronto)

*"Se ricevo un alert che il tasso di errore sulle autorizzazioni carta è salito improvvisamente, per prima cosa controllo se è isolato a un circuito specifico o generale — se è isolato, probabilmente il problema è a valle (es. il circuito esterno è lento o giù) e valuto se attivare un circuit breaker/fallback; se è generale, controllo se c'è stato un deploy recente e valuto un rollback immediato prima di investigare a fondo la causa, perché ripristinare il servizio ha priorità sul capire esattamente cosa è successo."*

### Domande tipiche e risposte

- *D: Qual è il tuo primo passo quando ricevi un alert di produzione?*
  R: Capire l'impatto reale (quanti utenti/transazioni coinvolti, da quando) prima di iniziare a investigare la causa — questo determina l'urgenza e se serve una mitigazione immediata (rollback, failover) prima ancora di capire il "perché".

- *D: Come distingui un problema applicativo da un problema infrastrutturale?*
  R: Guardo le metriche di sistema (CPU, memoria, rete, connessioni DB) insieme ai log applicativi — se le risorse sono normali ma ci sono eccezioni applicative, è probabile un bug o un problema di dati; se le risorse sono sature, è più probabile un problema di capacità/infrastruttura o un memory leak.

---

## 23. Domande Comportamentali e Soft Skill

### Cos'è e perché conta
La job description menziona esplicitamente "capacità di analisi dei problemi e delle relazioni cliente/fornitore", "capacità di lavorare in un ambiente dinamico e buone attitudini al lavoro in gruppo", "curiosità e propensione alla ricerca". In un colloquio senior, una parte è quasi sempre dedicata a domande comportamentali — spesso con il metodo **STAR** (Situazione, Task, Azione, Risultato) per strutturare la risposta.

### Come strutturare una risposta con il metodo STAR

- **Situazione**: contesto breve (dove, quando, con chi)
- **Task**: qual era l'obiettivo o il problema da risolvere
- **Azione**: cosa hai fatto concretamente tu (non "il team", ma il tuo contributo specifico)
- **Risultato**: esito misurabile, e idealmente cosa hai imparato

### Domande tipiche e come prepararle

- *D: Raccontami di una volta in cui hai dovuto risolvere un problema tecnico complesso.*
  Prepara un esempio concreto dal tuo lavoro (es. il progetto di riconciliazione bancaria) strutturato con STAR: qual era il problema, come l'hai affrontato, cosa hai imparato.

- *D: Come gestisci un disaccordo tecnico con un collega o un cliente?*
  R (traccia): descrivere un approccio basato su argomentazioni tecniche/dati piuttosto che opinioni, disponibilità ad ascoltare l'altro punto di vista, ma anche capacità di sostenere la propria posizione con motivazioni chiare — evitare risposte troppo remissive ("faccio sempre come dice l'altro") o troppo rigide.

- *D: Come ti tieni aggiornato tecnicamente?*
  Collegabile a quanto già visto nel punto 14 (versioni Java) — puoi citare la tua esplorazione autonoma di Java 24/Project Leyden come esempio concreto di curiosità tecnica, in linea con quanto richiesto esplicitamente nella job description.

- *D: Descrivi una situazione in cui hai dovuto gestire una relazione con un cliente o uno stakeholder esterno (banca, fornitore).*
  Prepara un esempio, anche ipotetico se non ne hai uno diretto, che mostri capacità di comunicare informazioni tecniche a un interlocutore non tecnico, e di gestire aspettative/scadenze.

- *D: Come lavori in un ambiente con requisiti che cambiano frequentemente?*
  R (traccia): mostrare flessibilità mantenendo però rigore tecnico — es. capacità di isolare le parti del sistema più stabili da quelle più soggette a cambiamento (collegabile ai principi di buona architettura già visti: bassa coppling, alta coesione).

### Come esercitarti
Prepara **due o tre aneddoti reali** dal tuo percorso (va benissimo il progetto di riconciliazione Castelmonte) che puoi adattare a più domande comportamentali diverse — è molto più efficace che improvvisare ogni volta un esempio nuovo. Scrivili in formato STAR, a punti, e ripassali ad alta voce.

---

## 24. Concorrenza in Java

### Cos'è e perché conta
Non esplicitamente richiesta nella job description, ma centrale in un sistema ad alto throughput come i pagamenti, dove più richieste vengono elaborate contemporaneamente. È un argomento classico nei colloqui senior Java.

### Cosa studiare

**Thread e Runnable**

```java
Thread t = new Thread(() -> processPayment(payment));
t.start();
```
Creare thread manualmente è raro in codice moderno — si preferisce quasi sempre un `ExecutorService`, che gestisce un pool di thread riutilizzabili invece di crearne uno nuovo per ogni task (costoso in termini di risorse).

**ExecutorService**

```java
ExecutorService executor = Executors.newFixedThreadPool(10);
Future<AuthorizationResult> future = executor.submit(() -> authorizePayment(request));
AuthorizationResult result = future.get(2, TimeUnit.SECONDS); // con timeout esplicito
```
Il pool di thread ha una dimensione fissa/gestita, evitando di saturare le risorse del sistema con troppi thread concorrenti.

**`synchronized` e i suoi limiti**

```java
public synchronized void debitAccount(String accountId, BigDecimal amount) {
    // solo un thread alla volta può eseguire questo blocco per la stessa istanza
}
```
Garantisce mutua esclusione, ma è un meccanismo "grezzo": blocca l'intero metodo/oggetto, può creare colli di bottiglia se applicato troppo largamente, e non ha timeout — un thread che aspetta il lock aspetta indefinitamente (rischio di deadlock se mal gestito).

**`CompletableFuture`**: per composizione di operazioni asincrone in modo dichiarativo, molto più espressivo di `Future` puro:

```java
CompletableFuture<AuthorizationResult> authFuture = CompletableFuture
    .supplyAsync(() -> authorizePayment(request))
    .thenApply(this::enrichWithFraudScore)
    .exceptionally(ex -> AuthorizationResult.failed(ex.getMessage()));
```
Permette di incatenare trasformazioni, gestire errori, e combinare più operazioni asincrone (`thenCombine`, `allOf`) senza bloccare thread in attesa.

**Virtual Threads (Java 21, già visto nel punto 14)**: risolvono il problema che i thread OS tradizionali sono "costosi" (ognuno occupa memoria significativa, il sistema ne regge solo migliaia) — i virtual thread sono gestiti dalla JVM e permettono di avere milioni di "thread logici" concorrenti con overhead minimo, ideali per applicazioni con molte operazioni bloccanti I/O-bound (come chiamate di rete verso circuiti di pagamento esterni).

**Collezioni concorrenti**: `ConcurrentHashMap` invece di sincronizzare manualmente una `HashMap` — offre operazioni thread-safe con granularità fine (non blocca l'intera mappa per ogni accesso, a differenza di `Collections.synchronizedMap`).

### Rilevanza per il dominio pagamenti
Il tema si collega direttamente a quanto già visto su isolation level (punto 3) e locking ottimistico/pessimistico (punto 13): la concorrenza a livello applicativo Java (thread, executor) e la concorrenza a livello database sono due facce dello stesso problema quando più richieste toccano lo stesso account contemporaneamente.

### Domande tipiche e risposte

- *D: Perché preferire `ExecutorService` alla creazione manuale di thread?*
  R: Un `ExecutorService` riutilizza un pool di thread invece di crearne uno nuovo per ogni operazione (costoso), permette di limitare la concorrenza massima (evitando di saturare risorse), e offre gestione di timeout/cancellazione tramite `Future`.

- *D: Cosa può causare un deadlock e come lo eviteresti?*
  R: Un deadlock si verifica tipicamente quando due thread acquisiscono più lock in ordine diverso, restando bloccati ad aspettarsi a vicenda. Si previene definendo un **ordine consistente** di acquisizione dei lock in tutto il codice, o preferendo strutture concorrenti di alto livello (`ConcurrentHashMap`, `CompletableFuture`) invece di `synchronized` manuale dove possibile.

---

## 25. Design Pattern e Principi SOLID

### Cos'è e perché conta
Domanda classica da "senior": non tanto ricordare a memoria l'elenco, quanto saper riconoscere quale pattern applicare a un problema concreto — spesso i colloquiatori chiedono "che pattern useresti per..." più che "elenca i design pattern".

### Principi SOLID

- **S — Single Responsibility**: una classe dovrebbe avere una sola ragione per cambiare — es. `PaymentService` gestisce la logica di pagamento, non anche la formattazione dei log o l'invio email
- **O — Open/Closed**: il codice dovrebbe essere aperto all'estensione ma chiuso alla modifica — es. aggiungere un nuovo `PaymentGateway` (già visto nel punto sui Qualifier) senza modificare il codice che già usa l'interfaccia `PaymentGateway`
- **L — Liskov Substitution**: una sottoclasse deve poter sostituire la sua superclasse senza alterare la correttezza del programma — es. se `MastercardGateway` e `VisaGateway` implementano `PaymentGateway`, il codice chiamante deve funzionare identicamente con entrambe
- **I — Interface Segregation**: preferire interfacce piccole e specifiche invece di una grande interfaccia generica — es. separare `PaymentProcessor` da `RefundProcessor` invece di un'unica interfaccia enorme che pochi client usano per intero
- **D — Dependency Inversion**: dipendere da astrazioni (interfacce), non da implementazioni concrete — è esattamente il principio dietro la dependency injection già vista nel punto 2 (iniettare `PaymentGateway`, non `VisaGatewayImpl` direttamente)

### Design pattern più rilevanti per un contesto backend/pagamenti

- **Strategy**: incapsula algoritmi intercambiabili dietro una stessa interfaccia — è il pattern dietro `PaymentGateway` con più implementazioni (Visa, Mastercard) selezionate a runtime, collegabile direttamente a `@Qualifier`
- **Factory**: centralizza la creazione di oggetti, utile quando la logica di scelta dell'implementazione concreta è complessa (es. una `PaymentGatewayFactory` che sceglie il gateway giusto in base al tipo di circuito indicato nella richiesta)
- **Observer**: un oggetto notifica automaticamente i suoi "osservatori" quando cambia stato — concettualmente alla base degli event listener Spring (`@EventListener`) e degli eventi di dominio già visti nel punto 8
- **Builder**: costruisce oggetti complessi passo passo, utile per oggetti con molti parametri opzionali (es. costruire una `TransactionRequest` con vari campi facoltativi in modo leggibile invece di un costruttore con 10 parametri)
- **Decorator**: aggiunge comportamento a un oggetto senza modificarne la classe, avvolgendolo — es. aggiungere logging o retry attorno a una chiamata di pagamento senza toccare la logica originale
- **Circuit Breaker**: già visto nel punto 8, è concettualmente un pattern strutturale applicato alla resilienza distribuita
- **Template Method**: definisce lo scheletro di un algoritmo in una classe base, lasciando ai sottotipi implementare i passi specifici — utile ad esempio se il flusso di validazione di un pagamento è sempre lo stesso (validazione formale → controllo fondi → controllo frode) ma alcuni passi variano per tipo di pagamento

### Domande tipiche e risposte

- *D: Che pattern useresti per gestire più circuiti di pagamento con logiche diverse ma stessa interfaccia?*
  R: Strategy pattern — un'interfaccia comune (`PaymentGateway`) con un'implementazione per circuito, selezionata a runtime (in Spring, tramite `@Qualifier` o una Factory che sceglie il bean giusto in base al tipo di richiesta).

- *D: Come si collega il Dependency Inversion Principle a Spring?*
  R: Spring è essenzialmente un framework che applica il DIP su larga scala: le classi dipendono da interfacce/astrazioni (iniettate dal container, vedi punto 2), non creano direttamente le proprie dipendenze concrete — questo è ciò che rende il codice testabile e sostituibile.

---

## 26. Gestione delle Eccezioni in Spring

### Cos'è e perché conta
Argomento pratico molto probabile in un colloquio o in un esercizio di live coding — una gestione errori solida è particolarmente critica in un sistema di pagamenti, dove un errore mal gestito può significare un pagamento perso, duplicato, o uno stato inconsistente.

### Checked vs Unchecked Exception

- **Checked** (estendono `Exception`, non `RuntimeException`): il compilatore obbliga a gestirle (try/catch o dichiararle con `throws`) — usate storicamente per errori "recuperabili" che il chiamante dovrebbe gestire esplicitamente
- **Unchecked** (estendono `RuntimeException`): non obbligano alla gestione esplicita — usate per errori di programmazione o condizioni che tipicamente non si possono recuperare localmente

**Best practice moderna**: in molti team (e in Spring stesso, es. `DataAccessException` visto nel punto sui `@Repository`) si preferiscono le unchecked exception anche per errori di business, per non "sporcare" le firme dei metodi con `throws` a catena — la gestione centralizzata (vedi sotto) si occupa comunque di intercettarle correttamente.

### Gestione centralizzata con `@ControllerAdvice` / `@ExceptionHandler`

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(InsufficientFundsException.class)
    public ResponseEntity<ErrorResponse> handleInsufficientFunds(InsufficientFundsException ex) {
        return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
            .body(new ErrorResponse("INSUFFICIENT_FUNDS", ex.getMessage()));
    }

    @ExceptionHandler(PaymentGatewayTimeoutException.class)
    public ResponseEntity<ErrorResponse> handleGatewayTimeout(PaymentGatewayTimeoutException ex) {
        return ResponseEntity.status(HttpStatus.GATEWAY_TIMEOUT)
            .body(new ErrorResponse("GATEWAY_TIMEOUT", ex.getMessage()));
    }

    @ExceptionHandler(Exception.class) // fallback generico
    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex) {
        return ResponseEntity.internalServerError()
            .body(new ErrorResponse("INTERNAL_ERROR", "Si è verificato un errore imprevisto"));
    }
}
```

Il vantaggio: la logica di business (`@Service`) lancia eccezioni specifiche e leggibili, senza doversi preoccupare di costruire risposte HTTP — la traduzione in status code/payload di errore è centralizzata in un unico posto, coerente in tutta l'applicazione.

### Best practice da citare a colloquio

- **Eccezioni custom specifiche del dominio** (`InsufficientFundsException`, `DuplicateTransactionException`) invece di eccezioni generiche — comunicano meglio l'intento e permettono gestione mirata
- **Non deglutire eccezioni silenziosamente** (`catch (Exception e) {}`) — quantomeno loggare, idealmente propagare o gestire esplicitamente
- **Non usare eccezioni per il controllo di flusso ordinario** — sono costose (stack trace) e vanno riservate a situazioni realmente eccezionali
- **Includere contesto utile nei messaggi di eccezione** (es. l'ID della transazione), fondamentale per il troubleshooting visto nel punto 22
- **Distinguere errori di client (4xx) da errori di server (5xx)** nella risposta HTTP — un errore di fondi insufficienti è un 422/400 (colpa della richiesta), un timeout verso un circuito esterno è più vicino a un 502/504 (colpa di una dipendenza)

### Domande tipiche e risposte

- *D: Perché preferire `@ControllerAdvice` alla gestione delle eccezioni in ogni singolo controller?*
  R: Centralizza la logica di traduzione errore → risposta HTTP in un unico posto, garantendo formato di risposta coerente in tutta l'applicazione ed evitando duplicazione di codice try/catch identico in ogni controller.

- *D: Come gestiresti un errore che avviene dentro una transazione `@Transactional`?*
  R: Per default Spring fa rollback automatico su `RuntimeException` (unchecked), ma **non** su checked exception salvo configurazione esplicita (`@Transactional(rollbackFor = ...)`) — un dettaglio spesso sottovalutato che può causare commit parziali indesiderati se si usano checked exception per errori di business senza configurare correttamente il rollback.

---

## 27. Spring Security

### Cos'è e perché conta
Modulo di Spring per gestire autenticazione, autorizzazione e protezione da vulnerabilità comuni — collegandosi direttamente ai concetti di sicurezza già visti nel punto 11 (OAuth2, JWT), qui si vede come si implementano concretamente in un'applicazione Spring Boot.

### Concetti fondamentali

- **`SecurityFilterChain`**: catena di filtri HTTP che intercetta ogni richiesta prima che arrivi al controller, applicando le regole di sicurezza configurate
- **Authentication vs Authorization** (già distinti concettualmente nel punto 11): Spring Security rappresenta l'utente autenticato come un oggetto `Authentication`, disponibile nel `SecurityContext` per tutta la richiesta
- **`UserDetailsService`**: interfaccia che recupera i dati dell'utente (credenziali, ruoli) da una fonte (DB, LDAP, servizio esterno) durante l'autenticazione

### Configurazione base (Spring Security moderno, stile Boot 3+)

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/api/payments/**").hasRole("PAYMENT_OPERATOR")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .csrf(csrf -> csrf.disable()); // tipico per API stateless, non per app con sessione browser
        return http.build();
    }
}
```

### OAuth2 Resource Server e JWT in Spring

In un'architettura a microservizi, il pattern tipico è che un **Authorization Server** esterno (o un identity provider come Keycloak) emette i JWT, mentre ogni microservizio agisce da **Resource Server**: valida il token in ingresso (firma, scadenza, eventualmente gli scope/ruoli contenuti) senza dover richiamare un servizio centrale ad ogni richiesta — coerente con quanto già accennato nel punto 11 sui vantaggi di JWT.

### Method-level security

```java
@PreAuthorize("hasRole('PAYMENT_OPERATOR')")
public void approveTransaction(String transactionId) { ... }
```
Permette di applicare controlli di autorizzazione direttamente a livello di metodo di servizio, non solo a livello di endpoint HTTP — utile per operazioni sensibili invocate internamente da più punti.

### Protezioni comuni fornite di default

- **CSRF protection**: rilevante per applicazioni con sessione basata su cookie/browser; tipicamente disabilitata per API REST stateless autenticate via token, dove il rischio CSRF non si applica allo stesso modo
- **Password encoding**: `BCryptPasswordEncoder` per non salvare mai password in chiaro (hashing con salt incorporato)
- **CORS**: configurazione esplicita di quali origin possono chiamare le API, per evitare richieste non autorizzate da domini terzi

### Rilevanza per il dominio pagamenti
Spring Security è tipicamente il livello che implementa concretamente PSD2/SCA a livello applicativo (autenticazione forte, scope OAuth2 specifici per operazioni sensibili come "approva pagamento" vs "sola lettura"), e il principio di least privilege (punto 11) tramite ruoli/scope granulari su ogni endpoint.

### Domande tipiche e risposte

- *D: Come proteggeresti un endpoint che avvia un pagamento, rispetto a uno che consulta solo lo storico?*
  R: Con autorizzazione basata su ruoli/scope differenziati (`hasRole`/`hasAuthority` o scope OAuth2 specifici) — l'endpoint di avvio pagamento richiede un livello di privilegio più alto (coerente col principio least privilege già visto), oltre eventualmente a controlli aggiuntivi lato business (es. limiti di importo per ruolo).

- *D: Perché disabilitare il CSRF su un'API REST stateless?*
  R: Il CSRF sfrutta il fatto che il browser invia automaticamente i cookie di sessione anche per richieste generate da un sito terzo malevolo — se l'autenticazione avviene tramite token (JWT) inviato esplicitamente in header e non tramite cookie di sessione, il vettore di attacco CSRF non si applica allo stesso modo, quindi la protezione CSRF nativa diventa superflua per questo tipo di API.

---

## Come usare questa guida
Non serve diventare esperto in tutto: punta a poter *conversare* con sicurezza su ogni punto, con almeno un esempio concreto pronto. Il dominio pagamenti (punto 1) merita la maggior parte del tempo perché è l'unico requisito "mandatorio" — è lì che si gioca la partita.
