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
