# 19. Architettura Cloud, Servizi AWS e Infrastructure as Code (IaC)

## Cos'è e perché conta

La progettazione di applicazioni enterprise moderne richiede una profonda padronanza dei paradigmi **Cloud-Native**. Un Senior Software Engineer non si limita a scrivere codice applicativo, ma comprende l'ambiente distribuito in cui il software viene eseguito: architettura dei servizi **AWS**, strategie di alta disponibilità e disaster recovery, pattern di deployment a zero-downtime, sicurezza IAM e gestione dell'infrastruttura tramite codice (**Infrastructure as Code - IaC** con Terraform e CDK).

---

## 1. Modelli Cloud e Principi Cloud-Native

```
                            I MODELLI DI SERVIZIO CLOUD
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ SaaS (Software as a Service)       │ Salesforce, Microsoft 365, Jira        │
 ├────────────────────────────────────┼────────────────────────────────────────┤
 │ PaaS (Platform as a Service)       │ AWS Elastic Beanstalk, Heroku          │
 ├────────────────────────────────────┼────────────────────────────────────────┤
 │ FaaS (Function as a Service)       │ AWS Lambda, Google Cloud Functions     │
 ├────────────────────────────────────┼────────────────────────────────────────┤
 │ IaaS (Infrastructure as a Service) │ AWS EC2, VPC, EBS, Azure VMs           │
 └────────────────────────────────────┴────────────────────────────────────────┘
```

### I Principi della 12-Factor App & Cloud-Native Design:
1. **Stateless Processes**: L'applicazione non mantiene stato in memoria locale tra una richiesta HTTP e l'altra. Lo stato (sessioni, token, carrelli) è esternalizzato su DB o cache distribuita (Redis), permettendo a qualsiasi istanza di servire qualsiasi richiesta e abilitando l'auto-scaling orizzontale istantaneo.
2. **Externalized Configuration**: Credenziali, URL dei database, feature flag ed endpoint sono iniettati tramite variabili d'ambiente o secret manager (AWS Secrets Manager / SSM Parameter Store), mai hardcoded nel codice sorgente.
3. **Disposability & Fast Startup**: I processi devono potersi avviare rapidamente e terminare in modo pulito (*Graceful Shutdown* intercettando `SIGTERM` per completare le transazioni in volo prima di chiudere le connessioni).
4. **Cattle, Not Pets**: Le istanze e i container sono considerati risorse effimere e sostituibili automaticamente (bestiame), non server unici configurati manualmente e accuditi nel tempo (animali domestici).

---

## 2. Deep Dive sui Servizi Core AWS

```
                           ARCHITETTURA APPLICATIVA AWS
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                           AMAZON ROUTE 53 (DNS)                             │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                     APPLICATION LOAD BALANCER (ALB)                         │
  └──────────────────┬───────────────────────────────────────┬──────────────────┘
                     │                                       │
            Public Subnet 1                         Public Subnet 2
                     │                                       │
     ┌───────────────▼───────────────┐       ┌───────────────▼───────────────┐
     │ NAT Gateway                   │       │ NAT Gateway                   │
     └───────────────┬───────────────┘       └───────────────┬───────────────┘
                     │                                       │
            Private Subnet 1                        Private Subnet 2
                     │                                       │
     ┌───────────────▼───────────────┐       ┌───────────────▼───────────────┐
     │ ECS Fargate / EKS Pods        │◄─────►│ ECS Fargate / EKS Pods        │
     │ (Spring Boot Backend)         │       │ (Spring Boot Backend)         │
     └───────────────┬───────────────┘       └───────────────┬───────────────┘
                     │                                       │
                     ├───────────────────┬───────────────────┤
                     ▼                   ▼                   ▼
            ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
            │ Amazon Aurora   │ │ Amazon ElastiCache││ Amazon SQS /   │
            │ (Multi-AZ DB)   │ │ (Redis Cluster) │ │ SNS Messaging   │
            └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 1. Compute
* **Amazon EC2 (Elastic Compute Cloud)**: Macchine virtuali IaaS scalabili.
* **Amazon ECS (Elastic Container Service) & AWS Fargate**:
  * Orchestratore container proprietario AWS.
  * **Fargate (Serverless Container)**: Esegue container Docker senza dover gestire o fare patching delle istanze EC2 sottostanti; si paga solo per CPU e memoria allocate al task.
* **Amazon EKS (Elastic Kubernetes Service)**: Kubernetes gestito enterprise per cluster multi-container ad alta complessità.
* **AWS Lambda (Serverless FaaS)**:
  * Esecuzione di codice guidata dagli eventi (*Event-Driven*) con scalabilità da zero a migliaia di istanze concorrenti.
  * *Considerazioni per Java*: Attenzione al **Cold Start** (tempo di avvio della JVM); mitigabile tramite *Provisioned Concurrency*, SnapStart (CRaC - Coordinated Restore at Checkpoint) o GraalVM Native Image.

### 2. Networking & Security
* **Amazon VPC (Virtual Private Cloud)**: Rete virtuale isolata logicamente.
* **Public vs Private Subnet**:
  * *Public Subnet*: Ha una rotta verso l'**Internet Gateway (IGW)**; ospita risorse che devono ricevere traffico da internet (es. Application Load Balancer).
  * *Private Subnet*: Non ha accesso diretto da internet; ospita i microservizi backend e i database. Accede a internet in uscita (es. per scaricare patch o chiamare API terze) tramite un **NAT Gateway** posizionato nella public subnet.
* **Security Groups vs Network ACLs (NACL)**:
  * *Security Group*: Firewall virtuale **stateful** associato alla singola istanza/interfaccia di rete (se il traffico in ingresso è consentito, la risposta in uscita è permessa automaticamente).
  * *NACL*: Firewall **stateless** a livello di intera subnet (richiede regole esplicite sia per Inbound che per Outbound).
* **AWS IAM (Identity and Access Management)**:
  * Principio del **Privilegio Minimo (*Least Privilege*)**.
  * Uso di **IAM Roles** e *Instance Profiles* (i container/istanze assumono ruoli temporanei tramite token STS senza memorizzare mai credenziali o access key nei file di configurazione).

### 3. Storage & Database Gestiti
* **Amazon S3 (Simple Storage Service)**: Storage ad oggetti altamente affidabile (99.999999999% - 11 nine di durabilità). Utilizzato per backup, report finanziari, tracciati batch e media.
* **Amazon RDS (Relational Database Service)**:
  * Motori relazionali gestiti (PostgreSQL, MySQL, Oracle).
  * **Multi-AZ Deployment**: Replica sincrona su una seconda Availability Zone con failover automatico trasparente in caso di guasto hardware.
  * **Read Replicas**: Repliche asincrone per distribuire il carico di lettura.
* **Amazon Aurora**:
  * Motore DB cloud-native compatibile Postgres/MySQL con storage distribuito a 6 copie su 3 AZ, throughput fino a 5x rispetto a MySQL standard e failover in meno di 30 secondi.
* **Amazon DynamoDB**:
  * NoSQL Key-Value e Document Store completamente gestito con latenze a singola cifra di millisecondo su qualsiasi scala di traffico.

### 4. Messaging ed Event-Driven nel Cloud
* **Amazon SQS (Simple Queue Service)**:
  * Coda di messaggi punto a punto completamente gestita.
  * *Standard Queue*: Throughput illimitato, garanzia di consegna *At-least-once*, ordinamento non garantito.
  * *FIFO Queue*: Consegna rigorosa nell'ordine esatto (*First-In-First-Out*) ed elaborazione *Exactly-Once* basata su `MessageGroupId` e `MessageDeduplicationId`.
  * *Dead Letter Queue (DLQ)*: Coda di smistamento per messaggi falliti dopo $N$ tentativi di retry (*MaxReceiveCount*).
* **Amazon SNS (Simple Notification Service)**:
  * Sistema Publish/Subscribe per notificare messaggi a molteplici destinatari contemporaneamente (*Fan-out pattern* verso code SQS, endpoint HTTP, email o funzioni Lambda).
* **Amazon EventBridge**:
  * Event Bus serverless per instradare eventi tra microservizi, servizi SaaS (Datadog, Zendesk) e risorse AWS tramite regole di filtraggio dichiarative sul payload JSON.

---

## 3. Cloud Deployment Patterns & Resilienza

```
                           BLUE / GREEN DEPLOYMENT
                    ┌─────────────────────────────────────┐
                    │       Router / Load Balancer        │
                    └──────────────────┬──────────────────┘
                                       │ Switch 100% traffico
                     ┌─────────────────┴─────────────────┐
                     ▼                                   ▼
        ┌────────────────────────┐          ┌────────────────────────┐
        │     Ambiente BLUE      │          │     Ambiente GREEN     │
        │   (Versione Attuale)   │          │    (Nuova Versione)    │
        │     • Istanze v1.0     │          │     • Istanze v2.0     │
        └────────────────────────┘          └────────────────────────┘
```

1. **Blue/Green Deployment**:
   * Due ambienti di produzione identici (Blue attivo, Green inattivo). Si rilascia la nuova versione su Green, si eseguono i test di fumo e poi si sposta istantaneamente il traffico del Load Balancer / DNS da Blue a Green. **Rollback istantaneo** in caso di anomalie.
2. **Canary Deployment**:
   * Il nuovo rilascio viene esposto inizialmente solo a una percentuale ridotta di traffico reale (es. $5\%$). Se i tassi di errore e la latenza rimangono nominali, il traffico viene incrementato progressivamente ($25\% \to 50\% \to 100\%$).
3. **Rolling Updates**:
   * Aggiornamento progressivo istanza per istanza (o pod per pod) mantenendo sempre una capacità minima operativa (*min healthy percentage*).
4. **Disaster Recovery Multi-Region**:
   * **RTO (Recovery Time Objective)**: Tempo massimo accettabile per ripristinare il servizio dopo un disastro.
   * **RPO (Recovery Point Objective)**: Quantità massima di dati che si è disposti a perdere (espressa in tempo: es. dati degli ultimi 5 minuti).
   * Strategie: *Backup & Restore* $\to$ *Pilot Light* $\to$ *Warm Standby* $\to$ *Active-Active Multi-Region*.

---

## 4. Infrastructure as Code (IaC)

L'**Infrastructure as Code** è la pratica di definire, configurare e gestire l'infrastruttura cloud tramite file di codice dichiarativi versionati su Git, eliminando la configurazione manuale via console (*Click-Ops*).

```
 ┌─────────────────┐      terraform plan      ┌─────────────────┐      terraform apply     ┌─────────────────┐
 │ File .tf (HCL)  │ ───────────────────────► │ Preview Modifiche│ ──────────────────────► │ Provider Cloud  │
 │ (Git Repo)      │                          │ (Diff vs State)  │                         │ (AWS Resources) │
 └─────────────────┘                          └─────────────────┘                          └─────────────────┘
```

### 1. Terraform (HashiCorp / OpenTofu)
* **Approccio Dichiarativo**: Si dichiara lo stato desiderato finale dell'infrastruttura; Terraform calcola il piano di esecuzione per raggiungerlo.
* **Componenti Chiave**:
  * **HCL (HashiCorp Configuration Language)**: Sintassi leggibile per descrivere risorse, variabili e output.
  * **Terraform State File (`terraform.tfstate`)**: Mappa le risorse definite nel codice con gli oggetti reali nel cloud. Deve essere salvato su un backend remoto sicuro (es. Bucket S3 con cifratura e lock distribuito su tabella DynamoDB per evitare scritture concorrenti).
  * **Drift Detection**: Terraform confronta lo stato reale del cloud con il file di stato, rilevando modifiche manuali non autorizzate.

```hcl
# Esempio Terraform: Creazione Coda SQS con Dead Letter Queue
resource "aws_sqs_queue" "payment_dlq" {
  name                      = "payment-processing-dlq"
  message_retention_seconds = 1209600 # 14 giorni
}

resource "aws_sqs_queue" "payment_queue" {
  name                      = "payment-processing-queue"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.payment_dlq.arn
    maxReceiveCount     = 3
  })
}
```

### 2. AWS CDK (Cloud Development Kit)
* Consente di definire l'infrastruttura AWS utilizzando veri linguaggi di programmazione orientati agli oggetti (**Java**, TypeScript, Python).
* Compila (*synthesizes*) il codice in template standard **AWS CloudFormation**, offrendo costrutti di alto livello riutilizzabili con type safety a tempo di compilazione.

---

## 5. Domande tipiche a colloquio (e risposte da Senior)

- *D: Perché i database e i microservizi backend vanno sempre posizionati in Private Subnet e come comunicano con l'esterno?*
  - **R**: Vengono posizionati in Private Subnet per sicurezza e conformità (difesa in profondità): non possiedono indirizzi IP pubblici e non sono raggiungibili direttamente dalla rete internet, prevenendo attacchi diretti. Il traffico in ingresso dall'esterno attraversa un **Application Load Balancer (ALB)** pubblico posizionato nella Public Subnet. Se i servizi privati devono effettuare chiamate in uscita verso API esterne (es. gateway Visa/Mastercard), il traffico in uscita viene instradato attraverso un **NAT Gateway** con IP elastico posizionato nella Public Subnet.

- *D: Qual è la differenza tra SQS Standard e SQS FIFO e quando è obbligatorio usare FIFO?*
  - **R**: SQS Standard offre throughput quasi illimitato ma garantisce solo la consegna *At-least-once* (possibili duplicati) e un ordinamento "best-effort". SQS FIFO garantisce l'ordinamento rigoroso dei messaggi e la consegna *Exactly-once* tramite deduplica automatica su 5 minuti, con un throughput massimo limitato (300 o 3000 msg/sec con batching). Nei sistemi di pagamento e contabili, SQS FIFO è obbligatorio per flussi in cui l'ordine cronologico è vitale (es. sequenza: `AUTHORIZED` $\to$ `CAPTURED` $\to$ `SETTLED`) e dove duplicare un messaggio causerebbe addebiti doppi.

- *D: Come gestisci il file di stato (`terraform.tfstate`) in un team enterprise con pipeline CI/CD?*
  - **R**: Il file di stato non deve mai essere salvato nel repository Git (perché contiene dati sensibili e porta a disallineamenti). Si configura un **Remote Backend** su un bucket **Amazon S3** con versioning abilitato e cifratura server-side (SSE-KMS), abbinato a un meccanismo di **State Locking** tramite tabella **DynamoDB**. In questo modo, quando una pipeline CI/CD o uno sviluppatore esegue `terraform plan/apply`, viene acquisito un lock esclusivo che impedisce esecuzioni concorrenti distruttive.
