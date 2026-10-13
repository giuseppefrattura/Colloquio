# 18. Kubernetes

## Dichiarare come deve funzionare un carico

Kubernetes coordina carichi containerizzati su un **cluster**, insieme di nodi. L'API conserva lo stato desiderato; i controller confrontano tale stato con quello osservato e cercano di riconciliarli. Questa **reconciliation** è un ciclo continuo, non una promessa che ogni guasto sia risolto immediatamente.

Un **Pod** è l'unità di esecuzione: i suoi container condividono rete e possono condividere volumi. Un **Deployment** gestisce repliche di pod intercambiabili e aggiornamenti. Un **Service** offre un riferimento stabile a un insieme di endpoint selezionati, evitando che il client debba inseguire ogni IP dei pod.

## Distinguere salute, disponibilità e capacità

La **liveness probe** verifica una condizione che può giustificare il riavvio del container. La **readiness probe** determina se il pod è pronto a ricevere traffico. Una **startup probe** consente un avvio lungo prima di applicare gli altri controlli. Un problema di una dipendenza condivisa non dovrebbe automaticamente far riavviare tutte le istanze.

Le **request** di risorse aiutano il scheduler a collocare il pod; i **limit** impongono vincoli di uso secondo la risorsa e il runtime. L'**Horizontal Pod Autoscaler**, HPA, modifica le repliche in base alle metriche configurate. Non crea capacità illimitata: nodi e dipendenze devono sostenerla.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: authorization-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: authorization-service
  template:
    metadata:
      labels:
        app: authorization-service
    spec:
      containers:
        - name: authorization-service
          image: registry.company.com/authorization-service:1.4.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
```

L'esempio ha selector e label corrispondenti; immagine e percorso di salute sono illustrativi e devono esistere nell'ambiente. Non include Service, configurazione o una politica completa delle risorse. Tre repliche aumentano la capacità di recupero soltanto se collocazione e dipendenze evitano guasti comuni.

## Configurazione e confini

Una **ConfigMap** conserva configurazione non sensibile. Un **Secret** è l'oggetto destinato a dati sensibili, ma base64 è codifica, non cifratura: servono protezione dello storage e accessi limitati. La [documentazione dei Secret](https://kubernetes.io/docs/concepts/configuration/secret/) chiarisce le misure necessarie.

Un **Namespace** organizza e delimita nomi e policy. Non offre automaticamente isolamento completo tra team o ambienti: autorizzazioni, quote e policy di rete completano il confine. Uno storage persistente richiede un progetto proprio per conservazione, accesso e recupero; ricreare un pod non ricostruisce dati persi.

## Aggiornare senza interrompere la funzione

Un **rolling update** fa convivere gradualmente pod vecchi e nuovi secondo la strategia configurata. La readiness aiuta a inviare traffico alle istanze pronte, ma assenza di downtime richiede anche capacità, gestione delle connessioni e compatibilità. La [documentazione dei Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) descrive questi meccanismi.

Per esercitarti, aggiorna mentalmente un servizio di autorizzazione mentre alcune richieste sono in corso. Spiega come vengono terminate le vecchie istanze, come viene confermata la disponibilità delle nuove e come due versioni possono usare lo stesso schema senza rompere i dati.
