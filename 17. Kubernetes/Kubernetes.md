## 17. Kubernetes

### Cos'è
Piattaforma di **orchestrazione container**, che gestisce automaticamente deployment, scaling, self-healing e networking di applicazioni containerizzate (tipicamente Docker). Non esegue direttamente il codice: coordina container su un cluster di macchine (nodi).

### Caratteristiche principali

- **Pod**: unità minima di deployment — uno o più container che condividono rete e storage, eseguiti sempre insieme sullo stesso nodo
- **Deployment**: definisce quante repliche di un pod devono essere in esecuzione e gestisce gli aggiornamenti (rolling update) senza downtime
- **Service**: espone un insieme di pod come un endpoint di rete stabile, con load balancing automatico tra le repliche — anche se i pod vengono ricreati con IP diversi, il Service resta raggiungibile allo stesso indirizzo
- **ConfigMap e Secret**: configurazione esterna all'immagine del container (coerente col principio 12-factor già visto nel punto 9) — ConfigMap per configurazioni non sensibili, Secret per credenziali/chiavi
- **Horizontal Pod Autoscaler**: scala automaticamente il numero di pod in base a metriche (es. CPU) — implementazione concreta dell'auto-scaling già visto nel punto 9
- **Liveness/Readiness probe**: health check che Kubernetes usa per capire se un pod è vivo (liveness — altrimenti lo riavvia) e se è pronto a ricevere traffico (readiness — altrimenti lo esclude temporaneamente dal load balancing) — implementazione concreta di health check e self-healing (punto 9)
- **Namespace**: partizione logica del cluster, utile per isolare ambienti (dev, staging, produzione) o team diversi

### Esempio concettuale (non serve saperlo scrivere a memoria, ma riconoscerlo)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: authorization-service
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: authorization-service
          image: registry.company.com/authorization-service:1.4.0
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
```

### Rilevanza per il dominio pagamenti
In un sistema mission-critical, Kubernetes garantisce che un servizio come `authorization-service` resti sempre disponibile con più repliche, si riavvii automaticamente in caso di crash (self-healing), e scali automaticamente nei picchi di traffico — tutto senza intervento manuale. I probe di readiness sono particolarmente importanti: un servizio di pagamento non ancora pronto (es. connessione DB non ancora stabilita all'avvio) non deve ricevere traffico prematuramente.

### Domande tipiche e risposte

- *D: Che differenza c'è tra liveness e readiness probe?*
  R: La liveness probe dice a Kubernetes "sono vivo o devo essere riavviato?" — se fallisce, il pod viene ucciso e ricreato. La readiness probe dice "sono pronto a ricevere traffico in questo momento?" — se fallisce, il pod resta in esecuzione ma viene temporaneamente escluso dal load balancing, utile ad esempio durante l'avvio o se una dipendenza esterna è momentaneamente non raggiungibile.

- *D: Come gestisce Kubernetes un deployment senza downtime?*
  R: Con un **rolling update**: crea gradualmente i nuovi pod con la versione aggiornata, aspetta che passino la readiness probe, e solo allora rimuove gradualmente i pod vecchi — mantenendo sempre un numero minimo di repliche disponibili durante la transizione. Si collega al blue-green/canary già visti nel punto 11, che in Kubernetes si implementano con strategie di deployment più sofisticate sopra questo meccanismo base.
