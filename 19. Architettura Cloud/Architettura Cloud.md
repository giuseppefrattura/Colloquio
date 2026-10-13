# 19. Architettura cloud, servizi AWS e infrastruttura

## Scegliere quanta infrastruttura gestire

Il cloud offre risorse e servizi con responsabilità diverse. Con **IaaS**, Infrastructure as a Service, gestisci più direttamente macchine e software. Con **PaaS**, Platform as a Service, deleghi parte della piattaforma. Con **SaaS**, Software as a Service, utilizzi un'applicazione fornita come servizio. **FaaS**, Function as a Service, esegue funzioni secondo eventi e richieste. Ogni livello sposta responsabilità, senza eliminare quelle su dati, accessi e configurazione.

Un'applicazione **cloud-native** è progettata per operare in questo ambiente: configurazione esterna al pacchetto, processi sostituibili, osservabilità e gestione dei guasti. I principi della **12-Factor App** aiutano a separare codice, configurazione e risorse. Non sono una garanzia automatica di scalabilità.

Un processo stateless non conserva nella propria istanza lo stato necessario tra richieste. Il **graceful shutdown** interrompe l'accettazione di nuovo lavoro e gestisce quello già in corso prima della chiusura. Trattare le istanze come sostituibili richiede che dati e recupero non dipendano dall'unica macchina che le ospita.

## Compute: macchine, container e funzioni

**EC2** offre macchine virtuali. **ECS** orchestra container secondo il modello AWS; **EKS** offre Kubernetes gestito. **Fargate** esegue workload container senza richiedere la gestione diretta dei server sottostanti, nei modelli supportati. Il costo e la capacità dipendono dalle risorse e dal carico previsti.

**Lambda** esegue codice in risposta a eventi. Il **cold start** è il lavoro iniziale necessario prima che un ambiente sia pronto, che in Java può includere avvio del runtime e inizializzazione. Tecniche come capacità preinizializzata e ripristino da snapshot affrontano il problema con vincoli specifici. Per scegliere si misurano durata, frequenza, concorrenza e dipendenze, evitando di trasformare una promessa di elasticità in capacità «illimitata».

## Rete e identità

Una **VPC**, Virtual Private Cloud, è una rete virtuale organizzata in subnet e regole. Una subnet pubblica dispone di una rotta verso un **Internet Gateway**; questo non rende automaticamente raggiungibile ogni risorsa. Una subnet privata non ha quella rotta diretta. Per alcune uscite verso internet può usare un **NAT Gateway**; per servizi supportati si possono usare endpoint privati.

Il NAT riguarda quel percorso in uscita: il traffico da un load balancer ai backend non deve attraversarlo come se fosse un passaggio obbligatorio. Un **ALB**, Application Load Balancer, instrada richieste applicative verso i target. **Route 53** gestisce funzioni DNS, cioè risoluzione dei nomi e politiche correlate.

Un **Security Group** applica regole stateful alle interfacce associate; una **Network ACL** filtra a livello di subnet con regole stateless. **IAM**, Identity and Access Management, definisce identità e politiche. Ruoli e credenziali temporanee riducono la distribuzione di access key statiche, ma i permessi devono rimanere minimi e verificabili.

## Storage e database

**S3** conserva oggetti, adatto a file, report e backup; non equivale a una normale directory locale condivisa. **RDS** gestisce motori relazionali; **Aurora** offre un modello di database gestito compatibile con famiglie PostgreSQL e MySQL. **DynamoDB** usa un modello key-value e documentale con accessi progettati intorno alle chiavi. **ElastiCache** offre caching gestito per motori supportati.

Una distribuzione **Multi-AZ** colloca risorse in più zone di disponibilità secondo il servizio adottato. Una read replica serve letture e può avere ritardo; non è automaticamente un backup né un nodo leggibile di qualsiasi configurazione di alta disponibilità. Disponibilità, throughput e tempi di failover vanno valutati sul modello e sulla versione effettivi.

## Code, pubblicazione ed eventi

**SQS** gestisce code. Le code Standard ammettono duplicati e non offrono ordine rigoroso. Le code **FIFO**, First-In-First-Out, introducono ordinamento per gruppo di messaggi e deduplicazione secondo condizioni precise; non rendono automaticamente unico un effetto su un database o su un provider remoto. Il consumer mantiene idempotenza e gestione della riconsegna.

**SNS** distribuisce messaggi ai destinatari, realizzando un **fan-out**, cioè diffusione a più percorsi indipendenti. **EventBridge** offre un bus con regole di instradamento degli eventi. Una **Dead Letter Queue** conserva alcuni fallimenti per diagnosi e recupero; occorre osservare l'accumulo e decidere come trattarlo.

## Rilascio e recupero

Un rolling update sostituisce gradualmente le istanze; blue-green mantiene versioni separate tra cui spostare traffico; canary espone una nuova versione a una parte del carico. DNS, connessioni e dati possono rendere la transizione meno immediata di quanto suggerisca un diagramma. Compatibilità dello schema e gestione del lavoro in corso restano necessarie.

Nel disaster recovery, **RTO** esprime l'obiettivo temporale di ripristino e **RPO** la perdita di dati tollerata. Backup e restore ricostruiscono il servizio; **pilot light** mantiene una base minima attiva; **warm standby** conserva un ambiente ridotto pronto ad aumentare capacità; **active-active** serve traffico in più siti. A maggiore preparazione possono corrispondere costi e problemi di coordinamento maggiori.

## Governare la configurazione

Terraform e OpenTofu sono strumenti distinti con una storia comune, non due nomi dello stesso prodotto. Lo state collega risorse dichiarate e reali; remote backend, protezione dei dati e locking consentono collaborazione. AWS CDK esprime infrastruttura in linguaggi di programmazione e sintetizza CloudFormation. Il capitolo 43 approfondisce piano, drift e recupero dopo modifiche parziali.

Progetta un backend con API pubblica, applicazioni interne e database. Traccia separatamente ingresso, uscite e accesso ai servizi cloud, poi spiega come si comporta durante la perdita di una zona. Usa stime e prove sul servizio adottato prima di promettere prestazioni o recupero.
