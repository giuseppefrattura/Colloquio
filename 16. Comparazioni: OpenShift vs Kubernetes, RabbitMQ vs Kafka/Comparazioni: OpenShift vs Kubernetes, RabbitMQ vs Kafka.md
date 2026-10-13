# 16. Confrontare piattaforme e modelli di messaggistica

## Confrontare responsabilità, non soltanto funzionalità

Un **trade-off** è una scelta che migliora una proprietà sostenendo un costo su un'altra. Prima di scegliere una piattaforma si chiariscono requisiti, competenze e responsabilità operative. Due prodotti con funzionalità simili possono richiedere quantità diverse di integrazione, supporto e manutenzione.

## Kubernetes e OpenShift

Kubernetes orchestra carichi containerizzati. OpenShift è una piattaforma Red Hat costruita su Kubernetes, con strumenti e convenzioni aggiuntivi. Conoscere Pod, Deployment e Service offre una base trasferibile; componenti specifici e politiche devono comunque essere appresi.

Una **Route** espone servizi secondo il modello OpenShift; un **Ingress** Kubernetes richiede un controller che ne attui le regole. **Source-to-Image**, S2I, costruisce immagini combinando sorgenti e immagini builder. Le **Security Context Constraints**, SCC, regolano capacità e contesti di esecuzione dei workload. La CLI `oc` aggiunge operazioni della piattaforma ai concetti Kubernetes.

| Decisione | Kubernetes | OpenShift |
|---|---|---|
| Componenti della piattaforma | Scelta di distribuzione e integrazioni | Insieme più integrato di strumenti e convenzioni |
| Esperienza di sviluppo | Dipende dalle integrazioni adottate | Console e workflow della piattaforma |
| Sicurezza dei workload | Policy e configurazioni da definire | Meccanismi specifici, comprese SCC |
| Supporto | Dipende dalla distribuzione e dal contratto | Offerta e contratto del fornitore |

Il valore di una piattaforma integrata può essere ridurre il lavoro di assemblaggio. Il costo può essere maggiore dipendenza dalle sue convenzioni. Non si deduce la conformità a uno standard dal solo nome del prodotto: permessi, configurazioni e procedure restano parte del progetto.

## RabbitMQ e Kafka

Nel modello classico di RabbitMQ, exchange e binding instradano messaggi verso code, e gli acknowledgment regolano il completamento della consegna. In Kafka, topic e partizioni organizzano un log che i consumer leggono con posizioni indipendenti. La domanda iniziale è se devi distribuire compiti oppure conservare un flusso da leggere e rileggere.

| Esigenza | Code RabbitMQ | Log Kafka |
|---|---|---|
| Instradamento | Exchange, binding e routing key | Topic, key e partizionamento |
| Completamento del consumo | Ack e gestione della riconsegna | Avanzamento e commit dell'offset |
| Lettori indipendenti | Code e sottoscrizioni dedicate | Consumer group distinti |
| Ordine osservato | Dipende da concorrenza e riconsegne | Per partizione, con vincoli applicativi |
| Recupero della storia | Dipende dalla struttura adottata | Replay entro la conservazione disponibile |

RabbitMQ supporta anche **Streams**, strutture persistenti con possibilità di replay: «RabbitMQ non può rileggere eventi» sarebbe una generalizzazione sbagliata. La [documentazione RabbitMQ Streams](https://www.rabbitmq.com/docs/streams) descrive questo modello. La scelta deve specificare quale struttura e quale protocollo si confrontano.

Per compiti con routing articolato può essere naturale una coda. Per una storia condivisa da contabilità e reportistica può essere naturale un log. Capacità e costi si misurano su payload, durabilità e topologia effettivi, senza assumere una classifica universale di throughput.

## Esercizio di confronto

Per un sistema di notifiche indica se serve conservare eventi, quali consumer sono indipendenti e come gestire fallimenti e duplicati. Poi spiega quale parte del lavoro operativo vuoi affidare alla piattaforma e quale deve restare nel team. Le motivazioni rendono la scelta discutibile e verificabile.
