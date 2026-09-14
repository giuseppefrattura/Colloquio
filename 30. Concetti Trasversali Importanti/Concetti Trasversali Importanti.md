# 30. Concetti Trasversali Importanti

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
