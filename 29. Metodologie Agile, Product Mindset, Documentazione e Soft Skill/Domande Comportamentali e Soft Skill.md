# 29. Metodologie Agile, Product Mindset, Documentazione e Soft Skill

## Cos'è e perché conta

Nei colloqui per posizioni Senior e Lead Developer, le competenze tecniche pure valgono solo il 50% della valutazione. L'altra metà valuta la **maturità professionale**: come lavori in team, come gestisci conflitti e priorità di business, come applichi le metodologie **Agile (Scrum e Kanban)**, come documenti requisiti e decisioni architetturali (**ADR, C4 Model, OpenAPI**) e come dimostri un autentico **Product Mindset** (trasformare requisiti di business complessi in valore misurabile per l'utente finale).

---

## 1. Metodologie Agile: Scrum vs Kanban

```
                      CONFRONTO FRAMEWORK AGILE
         SCRUM (Flusso a Sprint)                 KANBAN (Flusso Continuo)
   ┌─────────────────────────────────┐     ┌─────────────────────────────────┐
   │ • Iterazioni fisse (1-4 sett.)  │     │ • Nessuna iterazione fissa      │
   │ • Ruoli definiti (PO, SM, Dev)  │     │ • Focus sui WIP Limits          │
   │ • Cerimonie strutturate         │     │ • Consegna continua su richiesta│
   │ • Metrica: Velocity / Burndown  │     │ • Metrica: Lead & Cycle Time    │
   └─────────────────────────────────┘     └─────────────────────────────────┘
```

### 1. Scrum nel Dettaglio
* **I 3 Ruoli**:
  * **Product Owner (PO)**: Definisce la vision di prodotto, gestisce e ordina per priorità di business il *Product Backlog*.
  * **Scrum Master (SM)**: Facilita il processo, rimuove gli ostacoli (*impediments*) e protegge il team da distrazioni esterne.
  * **Development Team**: Team auto-organizzato, cross-funzionale e responsabile della stima e della consegna dell'incremento.
* **Le 5 Cerimonie (Eventi)**:
  1. **Sprint Planning**: Definizione dello *Sprint Goal* e selezione delle User Story da includere nello *Sprint Backlog*.
  2. **Daily Scrum (15 min)**: Allineamento quotidiano su cosa si è fatto, cosa si farà e blocchi operativi.
  3. **Sprint Review**: Demo dell'incremento funzionante agli stakeholder di business per raccogliere feedback immediato.
  4. **Sprint Retrospective**: Analisi interna del team su processi, strumenti e relazioni umane (*Cosa ha funzionato? Cosa migliorare? Action item concreti*).
  5. **Backlog Refinement (Grooming)**: Chiarimento delle User Story future, suddivisione e stima.
* **Artefatti & Criteri di Qualità**:
  * **Definition of Ready (DoR)**: Criteri affinché una storia possa essere inserita nello Sprint (requisiti chiari, dipendenze risolte, acceptance criteria definiti).
  * **Definition of Done (DoD)**: Criteri inderogabili affinché una storia sia considerata completata (codice scritto, test unitari e integrati verdi, code review approvata, documentazione aggiornata, deploy in ambiente di staging).

### 2. Kanban nel Dettaglio
* **Principi Chiave**:
  * **Visualizzare il Flusso**: Board con colonne chiare (*To Do $\to$ In Analysis $\to$ In Dev $\to$ In Review $\to$ In Test $\to$ Done*).
  * **WIP Limits (Work In Progress Limits)**: Numero massimo di task ammessi contemporaneamente in una colonna. Impedisce il multitasking inefficiente, fa emergere i colli di bottiglia e favorisce il *"Stop starting, start finishing"*.
* **Metriche di Flusso**:
  * **Lead Time**: Tempo totale dal momento in cui il task viene richiesto/creato a quando è rilasciato in produzione.
  * **Cycle Time**: Tempo effettivo impiegato da quando si inizia a lavorare sul task a quando è completato.

---

## 2. Product Mindset & Orientamento al Valore di Business

Un Senior Developer non è un "esecutore di ticket", ma un **partner strategico del business**:

```
                              PRODUCT MINDSET vs OUTPUT MINDSET
      OUTPUT MINDSET (Junior/Mid)                   PRODUCT MINDSET (Senior/Lead)
   ┌───────────────────────────────┐             ┌───────────────────────────────┐
   │ "Ho completato 8 ticket in    │ ──────────► │ "Abbiamo ridotto il tasso di  │
   │  questo Sprint: 40 Story Point│             │  abbandono al checkout del 3% │
   │  consegnati."                 │             │  velocizzando le API di auth."│
   └───────────────────────────────┘             └───────────────────────────────┘
```

### Le Dimensioni del Product Mindset:
1. **Outcome over Output**: Misurare il successo dall'impatto reale sul cliente e sul business, non solo dal numero di righe di codice o story point prodotti.
2. **Metriche di Business & KPI FinTech/Enterprise**:
   * **Conversion Rate**: Percentuale di utenti che completano con successo un pagamento o un onboarding.
   * **Churn Rate**: Tasso di abbandono del servizio da parte dei clienti.
   * **CAC (Customer Acquisition Cost)** vs **LTV (Customer Lifetime Value)**.
   * **Time-to-Market**: Velocità nel validare nuove ipotesi di business sul mercato.
3. **Collaborazione Cross-Funzionale**:
   * Lavorare in sintonia con **Product Manager** (per comprendere il *perché* di una feature), **UI/UX Designer** (per garantire fattibilità tecnica e reattività delle API), **QA Engineers** (per strategie di test automation) e **Compliance/Legal** (per vincoli normativi).
4. **Prioritizzazione con Framework RICE**:
   $$\text{RICE Score} = \frac{\text{Reach (Quanti utenti)} \times \text{Impact (Impatto sul business)} \times \text{Confidence (Grado di certezza)}}{\text{Effort (Giorni/Uomo)}}$$

---

## 3. Analisi dei Requisiti e Documentazione Tecnica e Funzionale

Un software non documentato o con requisiti ambigui genera bug costosi e disallineamenti nel team.

### 1. User Story e Criteri di Accettazione (INVEST Model)
Le User Story devono seguire l'acronimo **INVEST** (*Independent, Negotiable, Valuable, Estimable, Small, Testable*) con formato standard:
* **Template**: *Come [ruolo utente], voglio [funzionalità/azione], affinché [beneficio/valore di business].*
* **Acceptance Criteria (Formato Gherkin BDD)**:
  ```gherkin
  Scenario: Blocco automatico per tentativo di pagamento superiore al plafond
    Given un utente titolare di carta con plafond residuo di 500.00 EUR
    When richiede un'autorizzazione di pagamento di 600.00 EUR
    Then la richiesta viene rifiutata con codice "LIMIT_EXCEEDED"
    And viene inviata una notifica push di avviso all'utente
  ```

---

### 2. Architecture Decision Records (ADR)
L'**ADR** è un documento sintetico e versionato nel repository Git che traccia **il contesto e la motivazione di una scelta architetturale cruciale**, evitando che nel tempo si perda il motivo di una decisione (*"Perché abbiamo scelto Kafka invece di RabbitMQ?"*).

```markdown
# ADR 005: Utilizzo di Redis come Idempotency Store

## Stato
Approvato (2026-09-14)

## Contesto
I picchi di traffico di pagamento causano frequenti retry di rete da parte dei client mobile,
rischiando doppi addebiti. La verifica di idempotenza su Oracle DB impatta le prestazioni di I/O.

## Decisione
Implementiamo il pattern Idempotency-Key salvando la chiave su un cluster Redis dedicato,
con operazione atomica SETNX e TTL di 48 ore.

## Conseguenze
- Positive: Latenza di verifica abbattuta a < 2 ms; zero lock sul database Oracle.
- Negative: Aggiunta di una dipendenza infrastrutturale (cluster Redis) da monitorare in alta disponibilità.
```

---

### 3. Visualizzazione Architetturale: Il Modello C4

Creato da Simon Brown, il modello **C4** struttura i diagrammi architetturali su 4 livelli di zoom gerarchici:

```
                            I 4 LIVELLI DEL MODELLO C4
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ 1. CONTEXT DIAGRAM    │ Mostra il sistema globale, utenti e sistemi esterni │
 ├───────────────────────┼─────────────────────────────────────────────────────┤
 │ 2. CONTAINER DIAGRAM  │ Mostra le applicazioni web, microservizi, DB, code  │
 ├───────────────────────┼─────────────────────────────────────────────────────┤
 │ 3. COMPONENT DIAGRAM  │ Mostra i controller, servizi e repository interni   │
 ├───────────────────────┼─────────────────────────────────────────────────────┤
 │ 4. CODE DIAGRAM       │ Diagrammi UML di classi e relazioni specifiche      │
 └───────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 4. Problem Solving Strutturato e Gestione del Rischio

Nei colloqui di selezione Senior viene valutato il processo mentale di risoluzione dei problemi (*Problem Solving*):

1. **Decomposizione e Isolamento del Problema**:
   * Scomporre un problema complesso o un incidente di produzione in sotto-problemi isolati verificabili indipendentemente (*Divide et Impera*).
2. **Data-Driven Investigation**:
   * Non basarsi su supposizioni o "sensazioni", ma analizzare **metriche (Prometheus), log correlati tramite `traceId` e profili di esecuzione CPU/Memory**.
3. **Gestione del Rischio Tecnico**:
   * Identificare proattivamente i rischi prima del rilascio (punti singoli di fallimento, saturazione pool DB, dipendenze non ridondate) e definire piani di mitigazione o *Rollback Strategy*.

---

## 5. Risposte Comportamentali con il Metodo STAR

Per rispondere in modo strutturato, conciso e autorevole a domande situazionali:
* **S (Situation)**: Descrivi brevemente il contesto o la sfida.
* **T (Task)**: Qual era la tua responsabilità specifica o l'obiettivo da raggiungere.
* **A (Action)**: Quali azioni concrete hai intrapreso (sia tecniche che relazionali).
* **R (Result)**: Qual è stato il risultato misurabile ottenuto (in termini di tempo, performance o valore per il business).

### Esempi Pratici per Colloquio Senior:

- *D: Raccontami di una volta in cui hai avuto un disaccordo tecnico con un collega o architetto.*
  - **R (STAR)**:
    - *S*: Durante la progettazione di un nuovo servizio di settlement, l'architetto proponeva di usare chiamate REST sincrone a cascata tra 4 microservizi, mentre io ritenevo che introducesse accoppiamento temporale e rischio di timeout a catena.
    - *T*: Il mio obiettivo era garantire l'affidabilità e il throughput del sistema senza creare attriti nel team.
    - *A*: Anziché scontrarmi sul piano personale, ho preparato un rapido benchmark (*Proof of Concept*) simulando un degrado di rete sul terzo servizio, dimostrando che l'architettura REST andava in cascata di timeout, mentre un'architettura a eventi con **Outbox Pattern e Kafka** isolava completamente i servizi garantendo consistenza eventuale.
    - *R*: Il team e l'architetto hanno concordato sulla soluzione a eventi, che è andata in produzione senza registrare alcun incidente di timeout durante i picchi di fine mese.

- *D: Come ti comporti quando un Product Owner chiede una feature urgente tagliando sulla qualità del codice o sui test?*
  - **R (STAR)**:
    - Spiego al PO l'impatto in termini di **Trade-off e Rischio di Business**: rilasciare senza test automatizzati una logica finanziaria espone l'azienda a bug contabili e a tempi di rilascio più lunghi per i fix futuri (*Technical Debt*). Concordo un approccio pragmatico: riduciamo lo *Scope* della feature (rilasciando un MVP funzionale più piccolo) mantenendo però intatta la suite di test essenziali e la sicurezza transazionale, pianificando il completamento nel backlog successivo.
