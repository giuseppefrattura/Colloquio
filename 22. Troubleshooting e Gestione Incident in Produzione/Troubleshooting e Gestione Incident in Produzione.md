## 22. Troubleshooting e Gestione Incident in Produzione

### Cos'è e perché conta
È un requisito esplicito della job description ("analisi tecnica, troubleshooting e gestione di incident in ambienti di produzione") ma finora mai trattato nel documento. A un senior spesso si chiede non solo "conosci la tecnologia X" ma "come ragioni quando qualcosa si rompe in produzione alle 3 di notte" — è una domanda quasi certa in un colloquio per questo ruolo.

### Metodologia generale (framework da avere pronto)

1. **Individuare e circoscrivere l'impatto**: cosa non funziona, per chi, da quando — prima capire la portata (un cliente? tutti i pagamenti con un circuito specifico? tutti?) che approfondire la causa
2. **Stabilizzare prima di capire**: se esiste un modo rapido per limitare il danno (rollback, feature flag, circuit breaker manuale, failover) si applica **prima** di investigare a fondo la causa — specialmente in un dominio dove ogni minuto di downtime ha un costo diretto
3. **Raccogliere evidenze**: log applicativi, metriche (latenza, error rate — golden signals visti nel punto 11), tracing distribuito se il problema attraversa più servizi
4. **Formulare e verificare ipotesi**: partire dal cambiamento più recente (un deploy? una configurazione? un picco di traffico?) — la causa più probabile di un incident è spesso "cosa è cambiato di recente", non un bug dormiente da mesi
5. **Root cause analysis**: una volta risolto l'impatto immediato, capire la causa profonda — non fermarsi al sintomo (es. "un servizio è andato in OOM" non è la causa, ma il sintomo di un memory leak o di un carico non previsto)
6. **Post-mortem senza colpevolizzazione (blameless)**: documentare cosa è successo, perché, e quali azioni preventive si adottano — pratica standard in ambienti enterprise maturi

### Strumenti concreti da citare

- **Log centralizzati** (ELK, già visto nel punto 11): cercare errori/eccezioni nel periodo dell'incident, correlando per un ID di correlazione/transaction ID che attraversa i vari servizi
- **Tracing distribuito** (Jaeger/Zipkin): capire in quale servizio della catena si è verificato il rallentamento/errore, quando il problema attraversa più microservizi
- **Metriche e dashboard** (Prometheus/Grafana): capire se il problema è graduale (memory leak, saturazione risorse) o improvviso (deploy, picco di traffico)
- **Execution plan** (già visto nel punto 3): se il sintomo è una query lenta, è il primo strumento da controllare

### Esempio di scenario ragionato (utile da avere pronto)

*"Se ricevo un alert che il tasso di errore sulle autorizzazioni carta è salito improvvisamente, per prima cosa controllo se è isolato a un circuito specifico o generale — se è isolato, probabilmente il problema è a valle (es. il circuito esterno è lento o giù) e valuto se attivare un circuit breaker/fallback; se è generale, controllo se c'è stato un deploy recente e valuto un rollback immediato prima di investigare a fondo la causa, perché ripristinare il servizio ha priorità sul capire esattamente cosa è successo."*

### Domande tipiche e risposte

- *D: Qual è il tuo primo passo quando ricevi un alert di produzione?*
  R: Capire l'impatto reale (quanti utenti/transazioni coinvolti, da quando) prima di iniziare a investigare la causa — questo determina l'urgenza e se serve una mitigazione immediata (rollback, failover) prima ancora di capire il "perché".

- *D: Come distingui un problema applicativo da un problema infrastrutturale?*
  R: Guardo le metriche di sistema (CPU, memoria, rete, connessioni DB) insieme ai log applicativi — se le risorse sono normali ma ci sono eccezioni applicative, è probabile un bug o un problema di dati; se le risorse sono sature, è più probabile un problema di capacità/infrastruttura o un memory leak.
