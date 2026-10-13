# Guida al colloquio per Java Backend Developer

Questo progetto è un manuale in 50 capitoli per comprendere e spiegare il funzionamento di un backend Java: dal linguaggio alla produzione, passando per dati, architettura, sicurezza e domini applicativi. Il percorso usa problemi concreti, definizioni ed esempi per collegare le tecnologie alle decisioni che richiedono.

Puoi leggere il [libro completo in Markdown](guida-colloquio-completa.md), usare l’[edizione in testo semplice](guida-colloquio-completa.txt) oppure consultare i singoli capitoli dall’indice. La [prefazione](PREFAZIONE.md) spiega il percorso e come usare esempi e domande di ripasso.

## Percorso di lettura

I primi capitoli costruiscono le basi; quelli successivi le riprendono per discutere guasti, compromessi e gestione operativa. Le parti sui pagamenti e sugli altri domini mostrano perché la precisione del linguaggio conta quanto la scelta del framework. Gli ultimi capitoli consentono di approfondire singoli temi dopo la prima lettura.

Per preparare una risposta, descrivi il problema, chiarisci i termini, motiva la scelta e spiega come ne verificheresti il comportamento durante un errore. Per raccontare esperienze usa casi reali e risultati osservati.

## Indice dei 50 capitoli

### Linguaggi e paradigmi

| Capitolo | Percorso |
|---|---|
| [01. Java: JVM, Strutture Dati, Versioni (8-25), Concorrenza e Programmazione Reattiva](01.%20Java%20%28JVM%2C%20Strutture%20Dati%2C%20Versioni%208-25%2C%20Concorrenza%20e%20Reactive%29/Java%2C%20JVM%20e%20Strutture%20Dati.md) | Collegare linguaggio, strutture dati, memoria e concorrenza al comportamento del backend. |
| [02. Linguaggi Alternativi: Go e Scala (Paradigmi Funzionali)](02.%20Linguaggi%20Alternativi%3A%20Go%20e%20Scala%20%28Paradigmi%20Funzionali%29/Linguaggi%20Alternativi%3A%20Go%20e%20Scala.md) | Confrontare i modelli di dati, errori e concorrenza di Go, Scala e Java. |

### Persistenza e gestione dei dati

| Capitolo | Percorso |
|---|---|
| [03. Database Relazionali, NoSQL e Strategie di Accesso ai Dati](03.%20Database%20Relazionali%2C%20NoSQL%20e%20Strategie%20di%20Accesso/Database%20Relazionali%2C%20NoSQL%20e%20Strategie%20di%20Accesso.md) | Scegliere come conservare e interrogare dati, comprendendo transazioni e accessi concorrenti. |
| [04. Redis e caching distribuito](04.%20Redis/Redis.md) | Usare la cache con scadenze, invalidazione e una fonte autorevole dei dati. |
| [05. Database Migration Software (Flyway e Liquibase)](05.%20Database%20Migration%20Software%20%28Flyway%20e%20Liquibase%29/Database%20Migration%20Software%20%28Flyway%20e%20Liquibase%29.md) | Evolvere schema e dati mantenendo compatibili le versioni ancora in esecuzione. |
| [06. Gestire i dati in un'architettura a microservizi](06.%20Strategie%20per%20la%20Gestione%20dei%20Database%20in%20Architetture%20a%20Microservizi/Strategie%20per%20la%20Gestione%20dei%20Database%20in%20Architetture%20a%20Microservizi.md) | Coordinare dati di servizi distinti senza presumere un unico commit globale. |

### Design, framework e API

| Capitolo | Percorso |
|---|---|
| [07. Principi di Architettura Software, Design Pattern, NFR, TDD, BDD e Refactoring](07.%20Design%20Pattern%20e%20Principi%20SOLID/Design%20Pattern%20e%20Principi%20SOLID.md) | Motivare principi e pattern attraverso responsabilità, cambiamento e verifiche. |
| [08. Spring & Spring Boot](08.%20Spring%20%26%20Spring%20Boot/Spring%20%26%20Spring%20Boot.md) | Seguire oggetti, richieste e transazioni dentro Spring e Spring Boot. |
| [09. API REST, Tecnologie Web, Sicurezza e Framework](09.%20API%20REST%20e%20RESTful%20Design/API%20REST%20e%20RESTful%20Design.md) | Progettare contratti web, gestione dello stato e riuso delle rappresentazioni. |
| [10. Microservizi: i concetti fondamentali](10.%20Microservizi%3A%20Concetti%20Fondamentali/Microservizi%3A%20Concetti%20Fondamentali.md) | Valutare autonomia, comunicazione e costo operativo dei microservizi. |

### Comunicazione e streaming

| Capitolo | Percorso |
|---|---|
| [11. WebSocket e comunicazione in tempo reale](11.%20WebSocket/WebSocket.md) | Distribuire aggiornamenti in tempo reale e recuperare dopo una disconnessione. |
| [12. Apache Kafka](12.%20Apache%20Kafka/Apache%20Kafka.md) | Comprendere topic, partizioni, offset e lettori indipendenti in Kafka. |
| [13. JMS e messaggistica enterprise](13.%20JMS%20%28Java%20Message%20Service%29/JMS%20%28Java%20Message%20Service%29.md) | Collegare code, sottoscrizioni, conferme e transazioni nella messaggistica Java. |
| [14. Tecnologie Specialistiche: OSGi e MQTT](14.%20Tecnologie%20Specialistiche%3A%20OSGi%20e%20MQTT/OSGi%20e%20MQTT.md) | Gestire moduli dinamici e comunicazioni con dispositivi intermittenti. |
| [15. Tecnologie Streaming, Media e Broadcast](15.%20Tecnologie%20Streaming%2C%20Media%20e%20Broadcast/Tecnologie%20Streaming%2C%20Media%20e%20Broadcast.md) | Seguire il video da acquisizione e codifica alla distribuzione e riproduzione. |
| [16. Confrontare piattaforme e modelli di messaggistica](16.%20Comparazioni%3A%20OpenShift%20vs%20Kubernetes%2C%20RabbitMQ%20vs%20Kafka/Comparazioni%3A%20OpenShift%20vs%20Kubernetes%2C%20RabbitMQ%20vs%20Kafka.md) | Confrontare piattaforme e modelli dichiarando requisiti e responsabilità operative. |

### Container e cloud

| Capitolo | Percorso |
|---|---|
| [17. Containerizzazione (Docker e OCI)](17.%20Containerizzazione%20%28Docker%20e%20OCI%29/Containerizzazione%20%28Docker%20e%20OCI%29.md) | Distinguere immagini, processi e risorse nella containerizzazione. |
| [18. Kubernetes](18.%20Kubernetes/Kubernetes.md) | Comprendere stato desiderato, salute, configurazione e aggiornamenti dei workload. |
| [19. Architettura cloud, servizi AWS e infrastruttura](19.%20Architettura%20Cloud/Architettura%20Cloud.md) | Disegnare compute, rete, dati e recupero in un ambiente cloud. |

### Strumenti, qualità e rilascio

| Capitolo | Percorso |
|---|---|
| [20. Dependency Management (Maven e Gradle)](20.%20Dependency%20Management%20%28Maven%20e%20Gradle%29/Dependency%20Management%20%28Maven%20e%20Gradle%29.md) | Ricostruire la scelta delle librerie e risolvere conflitti di versione. |
| [21. Git e Branching Strategies](21.%20Git%20e%20Branching%20Strategies/Git%20e%20Branching%20Strategies.md) | Integrare modifiche, gestire conflitti e mantenere una storia comprensibile. |
| [22. La toolchain: dal lavoro locale all'artefatto pubblicato](22.%20Toolchain%20%28Eclipse%2C%20Git%2C%20Maven%2C%20JUnit%2C%20Jenkins%2C%20Nexus%29/Toolchain%20%28Eclipse%2C%20Git%2C%20Maven%2C%20JUnit%2C%20Jenkins%2C%20Nexus%29.md) | Collegare sviluppo locale, verifiche automatiche e pubblicazione degli artefatti. |
| [23. Unit Testing e Test Automation (JUnit 5, Mockito, Testcontainers)](23.%20Unit%20Testing%20e%20Test%20Automation%20%28JUnit%205%2C%20Mockito%2C%20Testcontainers%29/Unit%20Testing%20e%20Test%20Automation%20%28JUnit%205%2C%20Mockito%2C%20Testcontainers%29.md) | Usare test, sostituti e integrazioni per verificare comportamenti significativi. |
| [24. SAST e Qualità del Software (SonarQube)](24.%20SAST%20e%20Qualit%C3%A0%20del%20Software%20%28SonarQube%29/SAST%20e%20Qualit%C3%A0%20del%20Software%20%28SonarQube%29.md) | Interpretare analisi statica e segnalazioni nel contesto del codice. |
| [25. CI-CD e Release Management (Jenkins, GitLab CI, Nexus)](25.%20CI-CD%20e%20Release%20Management%20%28Jenkins%2C%20GitLab%20CI%2C%20Nexus%29/CI-CD%20e%20Release%20Management%20%28Jenkins%2C%20GitLab%20CI%2C%20Nexus%29.md) | Promuovere un artefatto verificato e pianificare compatibilità e recupero. |
| [26. Sicurezza e qualità come proprietà del prodotto](26.%20Sicurezza%20e%20Qualit%C3%A0%20del%20Software%20%28i%20%22plus%22%29/Sicurezza%20e%20Qualit%C3%A0%20del%20Software%20%28i%20%22plus%22%29.md) | Collegare protezione dei dati, gestione dei segreti e verifiche della qualità. |
| [27. Diagnosi e gestione degli incidenti in produzione](27.%20Troubleshooting%20e%20Gestione%20Incident%20in%20Produzione/Troubleshooting%20e%20Gestione%20Incident%20in%20Produzione.md) | Limitare il danno, costruire ipotesi e chiudere un incidente con evidenze. |
| [28. Sviluppare con l'IA e i coding agent](28.%20Coding%20IA/Coding%20IA.md) | Guidare coding agent attraverso contesto, strumenti e risultati verificabili. |

### Metodo di lavoro e concetti trasversali

| Capitolo | Percorso |
|---|---|
| [29. Metodi di lavoro, prodotto e comunicazione](29.%20Metodologie%20Agile%2C%20Product%20Mindset%2C%20Documentazione%20e%20Soft%20Skill/Domande%20Comportamentali%20e%20Soft%20Skill.md) | Coordinare lavoro, obiettivi di prodotto, documentazione e comunicazione. |
| [30. Concetti trasversali: collegare le proprietà del sistema](30.%20Concetti%20Trasversali%20Importanti/Concetti%20Trasversali%20Importanti.md) | Seguire sicurezza, retry, idempotenza e osservabilità nella stessa richiesta. |

### Domini applicativi

| Capitolo | Percorso |
|---|---|
| [31. Il dominio dei pagamenti](31.%20Dominio%20Pagamenti/Dominio%20Pagamenti.md) | Distinguere autorizzazione, cattura, regolamento e riconciliazione dei pagamenti. |
| [32. Assicurazioni, previdenza e sistemi finanziari](32.%20Dominio%20Assicurativo%2C%20Previdenziale%20e%20Sistemi%20Finanziari/Dominio%20Assicurativo%2C%20Previdenziale%20e%20Sistemi%20Finanziari.md) | Modellare ruoli e processi assicurativi, previdenziali e finanziari. |

### Architettura e affidabilità

| Capitolo | Percorso |
|---|---|
| [33. Fondamenti dei sistemi distribuiti](33.%20Distributed%20Systems%20Fundamentals/Distributed%20Systems%20Fundamentals.md) | Ragionare su guasti parziali, consistenza e coordinamento tra nodi. |
| [34. Progettare un sistema: dai requisiti alle scelte](34.%20System%20Design/System%20Design.md) | Tradurre requisiti e stime in una soluzione motivata e verificabile. |
| [35. Ingegneria delle prestazioni](35.%20Performance%20Engineering/Performance%20Engineering.md) | Misurare attese e capacità per trovare il collo di bottiglia reale. |
| [36. Microservizi avanzati e architetture a eventi](36.%20Advanced%20Microservices%20e%20Event%20Driven/Advanced%20Microservices%20e%20Event%20Driven.md) | Coordinare transazioni locali, eventi e recupero senza duplicare gli effetti. |
| [37. Domain-Driven Design e architettura del software](37.%20DDD%20e%20Software%20Architecture/DDD%20e%20Software%20Architecture.md) | Definire linguaggio, confini e invarianti del dominio. |
| [38. Sicurezza avanzata e governo delle API](38.%20Advanced%20Security%20e%20API%20Governance/Advanced%20Security%20e%20API%20Governance.md) | Proteggere risorse e mantenere contratti API compatibili nel tempo. |
| [39. Affidabilità, SRE e Chaos Engineering](39.%20SRE%20Reliability%20e%20Chaos%20Engineering/SRE%20Reliability%20e%20Chaos%20Engineering.md) | Collegare obiettivi di affidabilità, incidenti e prove di recupero. |

### Approfondimenti operativi

| Capitolo | Percorso |
|---|---|
| [40. Messaggistica avanzata: consegna, ordine e recupero](40.%20Messaging%20Technologies%20Advanced/Messaging%20Technologies%20Advanced.md) | Progettare consegna, ordine, retry e consumer in Kafka e RabbitMQ. |
| [41. Progettare una strategia di test](41.%20Automated%20Testing%20Advanced/Automated%20Testing%20Advanced.md) | Scegliere livelli di test in base ai rischi e alla velocità delle verifiche. |
| [42. Osservabilità e OpenTelemetry](42.%20Advanced%20Observability/OpenTelemetry%20e%20Advanced%20Observability.md) | Correlare log, metriche e trace per comprendere il sistema distribuito. |
| [43. Infrastructure as Code: stato, collaborazione e recupero](43.%20Advanced%20Infrastructure%20as%20Code/Advanced%20Infrastructure%20as%20Code.md) | Governare configurazione, stato e fallimenti parziali dell’infrastruttura. |

### Identità e sicurezza enterprise

| Capitolo | Percorso |
|---|---|
| [44. OAuth 2.0, OpenID Connect e JWT](44.%20OAuth2%20OpenID%20Connect%20e%20JWT%20Advanced/OAuth2%20OpenID%20Connect%20e%20JWT%20Advanced.md) | Distinguere delega, login e token seguendo i flussi di identità. |
| [45. LDAP e Active Directory](45.%20LDAP%20e%20Active%20Directory/LDAP%20e%20Active%20Directory.md) | Integrare directory, gruppi aziendali e permessi applicativi. |
| [46. Sicurezza in Java enterprise, SOA e API](46.%20Sicurezza%20J2EE%20SOA%20e%20API/Sicurezza%20J2EE%20SOA%20e%20API.md) | Conservare identità e protezioni tra API moderne e sistemi enterprise. |

### Approfondimenti sul codice e sulla build

| Capitolo | Percorso |
|---|---|
| [47. Java e programmazione funzionale](47.%20Java%208%2B%20e%20Functional%20Programming/Java%208%2B%20e%20Functional%20Programming.md) | Comporre trasformazioni, rappresentare assenza e separare effetti e calcolo. |
| [48. Programmazione reattiva](48.%20Reactive%20Programming/Reactive%20Programming.md) | Gestire flussi asincroni, domanda, errori e dipendenze non bloccanti. |
| [49. Programmazione difensiva e codice sicuro](49.%20Defensive%20Programming%20e%20Secure%20Coding/Defensive%20Programming%20e%20Secure%20Coding.md) | Progettare input, limiti, risorse e autorizzazione anche durante i guasti. |
| [50. Maven e Gradle: costruire un artefatto riproducibile](50.%20Build%20Tools%20Maven%20e%20Gradle/Build%20Tools%20Maven%20e%20Gradle.md) | Collegare dipendenze, build e artefatti a un processo riproducibile. |

## Sorgenti ed edizioni complete

I file nelle cartelle numerate sono le sorgenti dei capitoli. Dopo averli modificati, rigenera entrambe le edizioni:

```bash
python3 scripts/merge_chapters.py
```

Lo script include la prefazione e tutti i capitoli in ordine, costruisce l’indice navigabile e conserva gli esempi di codice. Se una cartella contiene più file Markdown, il capitolo principale deve avere lo stesso nome della cartella senza il numero iniziale (per esempio `03. Database` → `Database.md`). Gli altri file vengono inclusi dopo il capitolo principale come approfondimenti, in ordine alfabetico e con i titoli abbassati di un livello. Quando la cartella contiene un solo file Markdown, il nome del file può essere diverso.

La versione TXT rimuove la sintassi editoriale Markdown. La generazione è ripetibile a parità di sorgenti e segnala cartelle prive di un capitolo principale o con sorgenti ambigue. Il workflow GitHub Actions verifica i test di regressione e usa lo stesso comando per produrre gli artefatti.
