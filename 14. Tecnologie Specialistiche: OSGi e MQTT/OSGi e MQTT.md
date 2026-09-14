# 14. Tecnologie Specialistiche: OSGi e MQTT

## Cos'è e perché conta

In diversi contesti enterprise, industriali, IoT e sistemi di integrazione legacy o ad alta modularità (es. Adobe Experience Manager, piattaforme di telemetria, gateway di pagamento embedded o smart POS), emergono tecnologie specializzate come **OSGi** (per la modularità a caldo del codice Java) e **MQTT** (lo standard de facto per la messaggistica IoT leggera ed efficiente). Dimostrare competenza su questi temi evidenzia versatilità e comprensione dei protocolli di rete a basso livello e del classloading avanzato della JVM.

---

## 1. OSGi (Open Services Gateway initiative)

**OSGi** è una specifica e un framework per la **modularità dinamica** in Java. Consente di estendere la JVM per supportare il caricamento, l'aggiornamento e la disinstallazione di moduli software (*Bundle*) a runtime **senza riavviare l'applicazione** (*Hot Swapping / Dynamic Modular System*).

```
 ┌─────────────────────────────────────────────────────────────┐
 │                      OSGi FRAMEWORK                         │
 │                                                             │
 │  ┌───────────────────────────────────────────────────────┐  │
 │  │ SERVICE LAYER: Dynamic Service Registry (@Reference)  │  │
 │  ├───────────────────────────────────────────────────────┤  │
 │  │ LIFECYCLE LAYER: Manage bundle lifecycle states        │  │
 │  ├───────────────────────────────────────────────────────┤  │
 │  │ MODULE LAYER: Classloading, Export/Import Packages    │  │
 │  ├───────────────────────────────────────────────────────┤  │
 │  │ SECURITY LAYER: Java Security permissions             │  │
 │  └───────────────────────────────────────────────────────┘  │
 └──────────────────────────────┬──────────────────────────────┘
                                ▼
                       JAVA VIRTUAL MACHINE
```

### I Tre Livelli Fondamentali di OSGi

#### 1. Module Layer (I Bundle)
* Un **Bundle** è un normale file JAR che include metadati aggiuntivi nel file `META-INF/MANIFEST.MF`:
  ```ini
  Bundle-SymbolicName: com.bank.payment.gateway.visa
  Bundle-Version: 2.1.0
  Export-Package: com.bank.payment.api;version="2.1.0"
  Import-Package: org.osgi.framework;version="[1.8,2.0)",com.bank.common.crypto
  Bundle-Activator: com.bank.payment.internal.VisaActivator
  ```
* **Classloading Isolato**: A differenza della classica JVM flat classpath (dove tutto è visibile a tutti e si possono avere conflitti di versioni *JAR Hell*), in OSGi **ogni Bundle possiede il proprio ClassLoader dedicato**. Un bundle espone all'esterno solo i package dichiarati in `Export-Package` e può accedere solo ai package dichiarati in `Import-Package`.

#### 2. Lifecycle Layer (Ciclo di Vita del Bundle)
Il framework gestisce gli stati operativi di ciascun bundle:

```
           install            resolve              start
 [INSTALLED] ────► [RESOLVED] ───────► [STARTING] ──────► [ACTIVE]
      │               │                    │                 │
      │ uninstall     │                    │ stop            │ stop
      ▼               ▼                    ▼                 ▼
 [UNINSTALLED]   [INSTALLED]          [RESOLVED]        [STOPPING]
```

* **INSTALLED**: JAR scaricato e registrato nel framework.
* **RESOLVED**: Tutte le dipendenze (`Import-Package`) sono state soddisfatte da altri bundle attivi.
* **STARTING / ACTIVE**: L'attivatore o i componenti del bundle sono in esecuzione.
* **STOPPING**: Fase di rilascio risorse e deregistrazione servizi.
* **UNINSTALLED**: Bundle rimosso completamente dalla memoria.

#### 3. Service Layer & Declarative Services (OSGi DS)
* **Service Registry**: I bundle possono pubblicare servizi Java (*Service Registration*) o consumarli (*Service Lookup/Tracking*).
* **Declarative Services (SCR - Service Component Runtime)**: Meccanismo dichiarativo basato su annotazioni (analogo alla Dependency Injection di Spring):
  ```java
  @Component(service = PaymentProcessor.class, immediate = true)
  public class VisaPaymentProcessor implements PaymentProcessor {

      @Reference
      private CryptoService cryptoService; // Iniettato dinamicamente

      @Override
      public void process(Transaction tx) {
          byte[] signature = cryptoService.sign(tx.getPayload());
          // Logica di instradamento Visa
      }
  }
  ```

### Principali Implementazioni e Ambiti d'Uso:
* **Framework OSGi**: Apache Felix, Eclipse Equinox (motore di Eclipse IDE), Knopflerfish.
* **Runtime Enterprise**: Adobe Experience Manager (AEM), Apache Karaf, Red Hat Fuse.
* **Confronto con JPMS (Java Modules / Jigsaw)**: JPMS (introdotto in Java 9) offre incapsulamento a livello di compilazione ed esecuzione ma è statico (richiede riavvio della JVM). OSGi offre modularità e service registry **pienamente dinamici a runtime**.

---

## 2. MQTT (Message Queuing Telemetry Transport)

**MQTT** è un protocollo di messaggistica standard ISO (*ISO/IEC 20922*) estremamente **leggero, orientato agli eventi e basato su Publish/Subscribe**. È progettato specificamente per connessioni instabili, reti a bassa banda (3G/4G/Satellite) e dispositivi a risorse limitate (dispositivi IoT, POS portatili, sensori).

```
                         ARCHITETTURA PUB/SUB MQTT
  ┌──────────────┐         PUBLISH: "pos/terminal_12/payment"        ┌──────────────┐
  │ POS Terminal │ ────────────────────────────────────────────────► │ MQTT BROKER  │
  │ (Publisher)  │                                                   │ (Mosquitto/  │
  └──────────────┘                                                   │   HiveMQ)    │
                                                                     └──────┬───────┘
                                                                            │
                                   SUBSCRIBE: "pos/+/payment"               │
                                   ─────────────────────────────────────────┤
                                                                            ▼
                                                                     ┌──────────────┐
                                                                     │ Payment Core │
                                                                     │ (Subscriber) │
                                                                     └──────────────┘
```

### Caratteristiche Chiave del Protocollo:
* **Header Binario Minimale**: L'header fisso di un pacchetto MQTT occupa appena **2 byte**, contro le centinaia di byte degli header HTTP.
* **Trasporto**: Gira su protocollo affidabile **TCP/IP** (o WebSocket tramite TLS su porta 8883 / 443).
* **Topic Gerarchici & Wildcards**:
  * Topic strutturati a livelli con slash `/`: es. `terminals/italy/milan/pos_042/status`.
  * **Wildcard a Singolo Livello (`+`)**: `terminals/italy/+/pos_042/status` intercetta tutte le città.
  * **Wildcard Multi-Livello (`#`)**: `terminals/italy/#` intercetta qualsiasi topic che inizi con quel prefisso.

---

### Livelli di Quality of Service (QoS) in MQTT

La scelta del QoS determina il compromesso tra latenza/consumo di banda e affidabilità della consegna:

```
QoS 0 (At most once)         QoS 1 (At least once)            QoS 2 (Exactly once)
Client           Broker      Client            Broker         Client            Broker
  │  PUBLISH       │           │  PUBLISH        │              │  PUBLISH        │
  │ ─────────────► │           │ ──────────────► │              │ ──────────────► │
                               │  PUBACK         │              │  PUBREC         │
                               │ ◄────────────── │              │ ◄────────────── │
                                                                │  PUBREL         │
                                                                │ ──────────────► │
                                                                │  PUBCOMP        │
                                                                │ ◄────────────── │
```

1. **QoS 0 — At most once (Al massimo una volta)**:
   * "Fire and Forget": il messaggio viene inviato una sola volta senza conferma (*PUBACK*).
   * Rischio di perdita se la connessione cade. Adatto per metriche telemetriche ad altissima frequenza (es. temperatura ogni secondo).
2. **QoS 1 — At least once (Almeno una volta)**:
   * Il messaggio viene ritrasmesso finché il destinatario non risponde con un pacchetto **`PUBACK`**.
   * Garantisce la consegna, ma possono verificarsi messaggi duplicati se il `PUBACK` va perso nella rete. Richiede **idempotenza** lato consumer.
3. **QoS 2 — Exactly once (Esattamente una volta)**:
   * Protocollo di handshake a 4 vie (**PUBLISH $\to$ PUBREC $\to$ PUBREL $\to$ PUBCOMP**).
   * **Garantisce che il messaggio sia consegnato esattamente una volta senza perdite né duplicati**.
   * Ideale per transazioni finanziarie su smart POS, allarmi critici o addebiti dove la duplicazione causerebbe disastri.

---

### Funzionalità Avanzate di MQTT

* **Retained Messages (Messaggio Trattenuto)**:
  * Il publisher può impostare il flag `retain = true`. Il broker memorizza l'ultimo messaggio inviato su quel topic. Quando un nuovo subscriber si connette e fa la subscribe, riceve immediatamente l'ultimo stato valido senza attendere la pubblicazione successiva.
* **Last Will and Testament (LWT - Testamento)**:
  * In fase di connessione (`CONNECT`), il client registra un messaggio di "testamento" presso il broker (es. topic `devices/dev1/status`, payload `"OFFLINE"`).
  * Se il client si disconnette bruscamente per caduta di rete o crash, il broker pubblica automaticamente il messaggio LWT a tutti i subscriber, garantendo il rilevamento istantaneo dei guasti.
* **Persistent Session (Clean Session = false)**:
  * Il broker mantiene in memoria le sottoscrizioni e i messaggi QoS 1/2 pendenti per un dato `ClientID` anche mentre il dispositivo è disconnesso, consegnandoli tutti alla riconnessione.
* **Keep-Alive & PING**:
  * Scambio leggerissimo di pacchetti `PINGREQ` e `PINGRESP` (2 byte) per mantenere aperto il canale TCP ed evitare timeout dei firewall/NAT.

---

### Matrice Comparativa: MQTT vs HTTP vs WebSocket vs Kafka

| Caratteristica | MQTT | HTTP / REST | WebSocket | Apache Kafka |
| :--- | :--- | :--- | :--- | :--- |
| **Paradigma** | Pub/Sub Topic-based | Request/Response | Full-Duplex Bi-direzionale | Distributed Commit Log |
| **Overhead Header** | **Minimo (2 byte)** | Alto (centinaia di byte) | Molto basso (2-14 byte) | Medio-basso |
| **Garanzia Consegna**| QoS 0, QoS 1, QoS 2 | Nessuna nativa (a livello app) | Nessuna (TCP stream) | At-least-once, Exactly-once |
| **Consumo Batteria/CPU**| **Bassissimo** | Medio/Alto | Basso | N/A (Server-side) |
| **Persistenza Storica**| Solo ultimo (Retained) | Nessuna | Nessuna | **Persistenza su disco a lungo termine** |
| **Caso d'Uso Tipico** | Dispositivi IoT, Smart POS | API REST pubbliche | Notifiche Real-time su Browser | Event Streaming Backbone Enterprise |

---

## 3. Domande tipiche a colloquio (e risposte da Senior)

- *D: Perché in un'applicazione IoT o smart POS si preferisce MQTT rispetto a HTTP REST?*
  - **R**: Perché HTTP è un protocollo sincrono basato su polling o connessioni request/response pesanti con un overhead elevato di header (centinaia di byte per chiamata), che consumano molta banda e batteria su reti mobili. MQTT è asincrono basato su push, mantiene una singola connessione TCP persistente con un header di appena 2 byte, supporta la Quality of Service (QoS 0/1/2) e include feature native per la gestione delle disconnessioni di rete come *Last Will and Testament* e *Retained Messages*.

- *D: Come funziona il meccanismo di QoS 2 in MQTT e perché è più costoso in termini di latenza?*
  - **R**: Il QoS 2 garantisce la consegna *Exactly Once* attraverso un doppio handshake a 4 vie: il sender invia `PUBLISH`, il receiver memorizza il message ID e risponde con `PUBREC` (Publish Received); il sender invia `PUBREL` (Publish Release) e il receiver completa l'elaborazione rispondendo con `PUBCOMP` (Publish Complete). Questo scambio previene qualsiasi duplicazione o perdita anche in caso di retry, ma quadruplica i pacchetti scambiati rispetto a QoS 0, aumentando la latenza e l'overhead di rete.

- *D: Qual è il vantaggio principale di OSGi rispetto al classico Classpath di Java?*
  - **R**: Il classpath tradizionale di Java è "piatto" e non supporta l'isolamento: tutte le classi caricate sono visibili a tutti i componenti e non è possibile caricare due versioni diverse della stessa libreria (problema del *JAR Hell*). In OSGi ogni bundle ha un proprio ClassLoader che incapsula i package interni ed espone solo quelli esplicitamente dichiarati (`Export-Package`), permettendo la modularità dinamica, l'aggiornamento a caldo dei singoli bundle senza riavviare la JVM e la coesistenza di versioni multiple della stessa libreria nello stesso runtime.
