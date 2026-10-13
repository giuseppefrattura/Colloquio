# 7. Principi di Architettura Software, Design Pattern, NFR, TDD, BDD e Refactoring
## Il problema da cui partire
Un **design pattern** descrive una soluzione ricorrente a un problema, con contesto e conseguenze. Non è una classe da aggiungere per rendere il codice più prestigioso. Per un calcolo di commissioni, distinguere algoritmi variabili e regole comuni può giustificare Strategy; per due righe identiche che cambieranno in modo diverso, una nuova astrazione può essere prematura.
La **coesione** riguarda quanto le responsabilità di un modulo stanno insieme; l'**accoppiamento** riguarda quanto dipende dai dettagli di altri moduli. SOLID aiuta a discutere questi confini. **KISS**, Keep It Simple, invita a scegliere una soluzione comprensibile; **YAGNI**, You Aren't Gonna Need It, evita esigenze soltanto ipotetiche. **DRY**, Don't Repeat Yourself, protegge la conoscenza condivisa, non impone di unificare qualsiasi somiglianza sintattica.
Il **refactoring** cambia la struttura mantenendo il comportamento osservabile. I test aiutano a verificare questa promessa; requisiti non funzionali ed esempi di dominio rendono chiaro quale comportamento deve essere preservato.
## 1. Principi Fondamentali di Architettura e Design
```
                               PRINCIPI ARCHITETTURALI CORE
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ SOLID (S - Single Resp, O - Open/Closed, L - Liskov, I - Segreg, D - Invers)│
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ DRY (Don't Repeat Yourself)      │ Evita duplicazione di logica di business │
  ├──────────────────────────────────┼──────────────────────────────────────────┤
  │ KISS (Keep It Simple, Stupid)    │ Preferisci la soluzione più semplice     │
  ├──────────────────────────────────┼──────────────────────────────────────────┤
  │ YAGNI (You Aren't Gonna Need It) │ Non scrivere codice per requisiti futuri │
  ├──────────────────────────────────┼──────────────────────────────────────────┤
  │ Law of Demeter (Least Knowledge) │ Non parlare con gli "sconosciuti"        │
  └──────────────────────────────────┴──────────────────────────────────────────┘
```
### I Principi SOLID nel Dettaglio
#### 1. Single Responsibility Principle (SRP)
*Regola*: Una classe deve avere **una sola ragione per cambiare** (un solo attore/responsabilità di business). *Esempio*: Separare `PaymentExecutionService` (orchestra il pagamento), `PaymentReceiptGenerator` (genera il PDF) e `NotificationSender` (invia email/SMS), anziché concentrare tutto in un'unica classe monolitica da 2000 righe.
#### 2. Open/Closed Principle (OCP)
*Regola*: Le entità software devono essere **aperte all'estensione, ma chiuse alla modifica**. *Esempio*: Per supportare un nuovo gateway di pagamento (es. *Apple Pay*), non si modifica la classe `PaymentService` esistente con nuovi blocchi `if-else`, ma si crea una nuova classe `ApplePayGateway` che implementa l'interfaccia `PaymentGateway`.
#### 3. Liskov Substitution Principle (LSP)
*Regola*: I sottotipi devono poter sostituire i tipi base senza alterare la correttezza del programma. *Violazione tipica*: Lanciare `UnsupportedOperationException` in un metodo ereditato (es. una classe `ReadOnlyAccount` che estende `Account` e lancia eccezione sul metodo `debit()`). *Soluzione*: Ristrutturare la gerarchia separando `ReadableAccount` e `TransactableAccount`.
#### 4. Interface Segregation Principle (ISP)
*Regola*: I client non devono essere costretti a dipendere da metodi che non utilizzano. Preferire molte interfacce piccole e coese a un'unica interfaccia "grassa". *Esempio*: Separare `PaymentProcessor`, `RefundProcessor` e `ReconciliationProcessor` invece di un'unica interfaccia `AllInOnePaymentManager`.
#### 5. Dependency Inversion Principle (DIP)
*Regola*: I moduli di alto livello (logica di business) non devono dipendere da moduli di basso livello (database, client HTTP), ma entrambi devono dipendere da **astrazioni (interfacce)**. *In Spring*: È il fondamento della *Dependency Injection* e dell'**Architettura Esagonale (Ports & Adapters)**.
---
### Altri Principi Chiave:
**Law of Demeter (Principio della Minima Conoscenza)**: Un metodo deve invocare solo metodi dei propri campi, parametri passati o oggetti istanziati localmente. *Anti-Pattern (Train Wreck)*: `order.getCustomer().getAddress().getCity().toUpperCase()` $\to$ accoppia la classe con 4 livelli interni. *Soluzione*: `order.getCustomerCity()`.
**DRY vs Duplicazione Accidentale**: DRY si riferisce alla duplicazione di **conoscenza di business**, non a righe di codice superficialmente identiche che evolvono per ragioni diverse (es. il DTO di un'API REST e l'Entità JPA di persistenza non devono essere forzatamente unificati).
---
## 2. GoF Design Pattern per il Backend Enterprise
**GoF**, Gang of Four, indica gli autori del catalogo classico. Factory Method delega la creazione a un metodo specializzabile; Builder organizza costruzioni in più passi. Adapter traduce un'interfaccia, Decorator aggiunge responsabilità e Proxy controlla l'accesso a un oggetto. Strategy seleziona un algoritmo, Observer collega notifiche, Chain of Responsibility passa una richiesta tra gestori e State organizza comportamenti in base allo stato.
Strategy appartiene ai pattern comportamentali, anche se spesso partecipa alla struttura del servizio. Lo scope singleton di Spring limita istanze per bean nel container, non implementa automaticamente il Singleton GoF globale. Gli eventi Spring sono sincroni o asincroni secondo configurazione. Queste distinzioni evitano di trattare la tabella come equivalenze automatiche.
| Categoria | Pattern | Problema affrontato |
|---|---|---|
| Creazione | Factory Method, Builder | Delegare o organizzare la costruzione |
| Struttura | Adapter, Decorator, Proxy | Tradurre interfacce, aggiungere responsabilità o controllare accesso |
| Comportamento | Strategy, Observer, Chain of Responsibility, State | Variare algoritmi, notificare e organizzare flusso o stati |

Singleton regola l'accesso a un'istanza secondo il modello scelto. Lo scope singleton di un bean Spring è invece relativo al container e alla definizione del bean; non implica un'unica istanza universale del tipo.
### Esempio Applicato: Strategy + Factory con Spring
```java
// Interfaccia Strategy
public interface FeeCalculator {
    BigDecimal calculate(Payment payment);
    PaymentType getSupportedType();
}

@Component
public class CardFeeCalculator implements FeeCalculator {
    public BigDecimal calculate(Payment p) { return p.getAmount().multiply(new BigDecimal("0.015")); }
    public PaymentType getSupportedType() { return PaymentType.CARD; }
}

@Component
public class SepaFeeCalculator implements FeeCalculator {
    public BigDecimal calculate(Payment p) { return new BigDecimal("0.50"); }
    public PaymentType getSupportedType() { return PaymentType.SEPA; }
}

// Factory dinamica tramite Spring Dependency Injection
@Service
public class FeeCalculatorFactory {
    private final Map<PaymentType, FeeCalculator> calculators;

    public FeeCalculatorFactory(List<FeeCalculator> calculatorList) {
        this.calculators = calculatorList.stream()
            .collect(Collectors.toMap(FeeCalculator::getSupportedType, Function.identity()));
    }

    public FeeCalculator getCalculator(PaymentType type) {
        return Optional.ofNullable(calculators.get(type))
            .orElseThrow(() -> new IllegalArgumentException("Nessun calcolatore per: " + type));
    }
}
```
---
## 3. Requisiti Non Funzionali (NFRs - Non-Functional Requirements)
Gli NFR definiscono i **criteri di qualità e i vincoli architetturali** con cui il sistema deve operare:
```
                            LE DIMENSIONI DEGLI NFR
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │   Scalability    │    │   Performance    │    │   Availability   │    │     Security     │
  │ • Throughput TPS │    │ • Latency p95/p99│    │ • SLA / 99.99%   │    │ • Zero Trust     │
  │ • Orizzontale    │    │ • Response Time  │    │ • MTBF & MTTR    │    │ • Encryption     │
  └──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
```

**Scalabilità (Scalability & Throughput)**:

Capacità di gestire carichi crescenti (es. picco Black Friday da 5.000 TPS) aggiungendo risorse orizzontalmente senza degrado prestazionale.

**Performance e Latenza**:

Misurazione basata su percentili (non sulla media che nasconde i picchi anomali): **p95 < 100 ms**: il 95% delle richieste risponde in meno di 100 ms. **p99 < 300 ms**: il 99% delle richieste risponde in meno di 300 ms.

**Disponibilità (Availability & Resiliency)**:

**SLA (Service Level Agreement)**: *99.9% (Three Nines)*: Massimo 8.76 ore di downtime all'anno. *99.99% (Four Nines)*: Massimo 52.6 minuti di downtime all'anno (esempio di obiettivo su base temporale). *99.999% (Five Nines)*: Massimo 5.26 minuti di downtime all'anno (esempio di obiettivo su base temporale). **MTBF**, Mean Time Between Failures, misura il tempo medio tra guasti secondo il perimetro scelto. **MTTR**, Mean Time To Recovery, misura il tempo medio di recupero. Per confrontarli servono definizioni coerenti di guasto e ripristino.

**Sicurezza e Conformità**:

Cifratura in transito (TLS 1.3) e at-rest (AES-256), conformità PCI-DSS, tracciabilità immutabile di tutte le operazioni (*Auditability*).
---
## 4. Metodologie di Sviluppo: TDD & BDD
```
                                  IL CICLO DEL TDD
               ┌────────────────────────────────────────────────────┐
               │                                                    │
               ▼                                                    │
        ┌──────────────┐     Scrivi Codice Minimo     ┌───────────┐ │
        │     RED      │ ───────────────────────────► │   GREEN   │ │
        │ (Test Fallito│                              │ (Test OK) │ │
        └──────────────┘                              └─────┬─────┘ │
                                                            │       │
                                                 Refactoring│       │
                                                            ▼       │
                                                      ┌───────────┐ │
                                                      │  REFACTOR │ ┘
                                                      │ (Pulisci) │
                                                      └───────────┘
```
### 1. Test-Driven Development (TDD)
**Filosofia**: Scrivere il test *prima* del codice di produzione (*Test-First Development*).
**I 3 Passi**:

1. **RED**: Scrivi un test unitario per il nuovo comportamento desiderato; il test fallisce (o non compila).

2. **GREEN**: Scrivi la quantità minima di codice necessaria a far passare il test (anche con valori hardcoded).

3. **REFACTOR**: Ristruttura il codice eliminando duplicazioni e migliorando il design, garantendo che tutti i test rimangano verdi.

**Vantaggi**: Design modulare e disaccoppiato emergente, verifiche del comportamento e maggiore fiducia nel cambiamento (*Regression Safety*).
### 2. Behavior-Driven Development (BDD)
**Filosofia**: Estensione del TDD orientata alla collaborazione tra **Business/Product Management, QA e Sviluppatori** tramite un linguaggio ubiquo e condiviso. **Struttura Given-When-Then (Gherkin Syntax)**:
```gherkin
Feature: Autorizzazione Pagamento con Carta
  Scenario: Saldo disponibile sufficiente
    Given un conto con saldo disponibile di 100.00 EUR
    When richiedo un pagamento con carta di 35.00 EUR
    Then il pagamento viene approvato con stato "AUTHORIZED"
    And il saldo disponibile residuo diventa 65.00 EUR
```
---
## 5. Refactoring Continuo e Code Smells
Il **Refactoring** è il processo di modifica di un sistema software volto a migliorarne la struttura interna, la leggibilità e l'estensibilità **senza alterarne il comportamento osservabile esterno**.
### I Principali "Code Smells" (Martin Fowler) e Soluzioni:

**Long Method (Metodo Troppo Lungo)**:

*Problema*: Metodo con oltre 40-50 righe contenente logiche di validazione, calcolo e persistenza. *Soluzione*: **Extract Method** per isolare funzioni coese con nomi auto-esplicativi.

**God Class / Large Class (Classe Onnipotente)**:

*Problema*: Classe con decine di campi e migliaia di righe che sa e fa troppo. *Soluzione*: **Extract Class** applicando il *Single Responsibility Principle*.

**Primitive Obsession**:

*Problema*: Uso continuo di tipi primitivi (`String`, `Long`, `BigDecimal`) per rappresentare concetti di dominio (es. passare `String iban, String currency, BigDecimal amount`). *Soluzione*: **Value Objects / Records** (es. `record Money(BigDecimal amount, Currency currency)`, `record IBAN(String value)`).

**Feature Envy (Invidia di Funzionalità)**:

*Problema*: Un metodo di una classe accede costantemente ai getter di un'altra classe per fare calcoli. *Soluzione*: **Move Method** spostando il metodo all'interno della classe che possiede i dati.

**Shotgun Surgery**:

*Problema*: Ogni volta che si apporta una modifica di business, occorre modificare piccoli pezzi di codice in decine di classi diverse. *Soluzione*: Centralizzare la logica coesa in una classe dedicata.
---
## 6. Domande tipiche a colloquio (e risposte da Senior)
*D: Come applichi concretamente il principio Open/Closed (OCP) in un'applicazione Spring Boot?*
**R**: Definisco un'interfaccia di servizio (astrazione) per il comportamento variabile (es. `NotificationSender` o `FraudCheckRule`). In Spring inietto una lista di bean `List<NotificationSender>` o una mappa, popolata automaticamente dal container IoC. Quando in futuro dobbiamo supportare un nuovo canale (es. notifica WhatsApp), creiamo semplicemente un nuovo bean `@Component` che implementa l'interfaccia: il codice chiamante non subisce alcuna modifica, rispettando pienamente l'OCP.
*D: Perché il TDD migliora il design del software e non è solo una tecnica di test?*
**R**: Perché costringere lo sviluppatore a scrivere il test prima dell'implementazione lo obbliga a pensare alla classe dal punto di vista del suo utilizzatore (*API Design*). Una classe difficile da testare è quasi sempre una classe con cattivo design (troppo accoppiata, troppe responsabilità o dipendenze nascoste). Il TDD forza naturalmente a creare classi coese, a iniettare dipendenze tramite interfacce e a minimizzare la complessità ciclomatica.
*D: Come definisci e garantisci un requisito di latenza p99 in un microservizio di pagamento?*
**R**: Il percentile 99 significa che il 99% delle richieste deve completarsi sotto una determinata soglia (es. 150 ms), lasciando l’1% oltre quella soglia: questi casi restano parte del servizio e vanno osservati. Per garantirlo:

Strumento il codice con metriche **Micrometer / Prometheus** esportando histogram dei tempi di esecuzione sui metodi critici.

Evito operazioni bloccanti o query N+1 al database ottimizzando indici e connection pool (HikariCP).

Utilizzo cache in-memory (Redis) per dati calcolati di frequente e timeout aggressivi con Circuit Breaker sulle chiamate HTTP a servizi esterni.

Eseguo test di carico prestazionali (*Load & Stress Testing* con Gatling/JMeter) durante la pipeline di release.
