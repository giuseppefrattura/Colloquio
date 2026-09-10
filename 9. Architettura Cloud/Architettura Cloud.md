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
