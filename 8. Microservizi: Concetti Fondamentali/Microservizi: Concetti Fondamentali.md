## 8. Microservizi: Concetti Fondamentali

### Cos'è e perché conta
Anche se non esplicitamente nella job description, un'architettura di pagamenti mission-critical con integrazioni multiple (circuiti, banche, provider terzi) è quasi certamente organizzata a microservizi o comunque a servizi distribuiti. Vale la pena arrivare preparato anche su questo fronte.

### Cosa studiare

**Principi di base**

I microservizi sono un'architettura dove l'applicazione è scomposta in servizi indipendenti, ciascuno responsabile di una specifica funzionalità di business. Ogni servizio ha il proprio database (**database per service pattern**), può essere deployato indipendentemente e comunica con gli altri attraverso API ben definite.

*Esempio nel dominio pagamenti*: un servizio `authorization-service` (gestisce le autorizzazioni), uno `settlement-service` (gestisce clearing/settlement), uno `reconciliation-service` (riconciliazione) — ognuno con il proprio DB, deployabile e scalabile in autonomia.

**Vantaggi e trade-off**

Devi essere pronto a discutere quando conviene usarli:
- **Vantaggi**: scalabilità indipendente (es. scalare solo il servizio di autorizzazione nei picchi di traffico, senza toccare il resto), isolamento dei guasti (un servizio che cade non abbatte tutto il sistema), libertà tecnologica per ogni servizio, team autonomi che possono rilasciare senza coordinarsi con tutti gli altri
- **Svantaggi**: complessità nella gestione distribuita, necessità di orchestrazione, monitoraggio avanzato (vedi osservabilità più sotto), gestione delle transazioni distribuite (niente più semplice `@Transactional` locale quando l'operazione coinvolge più servizi)

**Comunicazione tra servizi**

- **Sincrona** (REST, gRPC): il chiamante aspetta la risposta. Più semplice da ragionare, ma accoppia temporalmente i servizi — se il servizio chiamato è lento o giù, blocca anche il chiamante
- **Asincrona** (message broker come RabbitMQ, Kafka, AWS SQS): il chiamante pubblica un messaggio/evento e prosegue, senza aspettare. Preferibile per disaccoppiare i servizi e gestire meglio i picchi di carico

*Esempio pagamenti*: l'autorizzazione di una transazione richiede tipicamente comunicazione **sincrona** (il cliente al POS aspetta una risposta in millisecondi), mentre l'invio di notifiche, l'aggiornamento di sistemi di reportistica o l'innesco della riconciliazione post-transazione sono tipicamente **asincroni** via evento (es. `TransactionCompletedEvent` pubblicato su Kafka).

**Pattern essenziali**

- **API Gateway**: punto d'ingresso unico per i client, che instrada le richieste ai servizi interni, gestendo trasversalmente autenticazione, rate limiting, routing
- **Service Discovery** (Consul, Eureka): permette ai servizi di trovarsi dinamicamente a runtime, senza indirizzi IP hardcoded — essenziale quando i servizi scalano e le istanze cambiano continuamente
- **Circuit Breaker** (pattern reso popolare da Hystrix, oggi più spesso Resilience4j): se un servizio a valle inizia a fallire ripetutamente, il circuit breaker "apre il circuito" e smette temporaneamente di chiamarlo, restituendo subito un errore/fallback invece di continuare a intasarlo con richieste che falliranno comunque — fondamentale per evitare che un servizio in difficoltà (es. un circuito di pagamento esterno lento) faccia collassare a cascata anche i servizi che lo chiamano
- **Saga pattern**: per gestire transazioni distribuite su più servizi senza un "commit" globale come nel mondo relazionale — una saga è una sequenza di transazioni locali, ciascuna con una **compensazione** (azione di rollback logico) se un passo successivo fallisce. Due varianti: *orchestrazione* (un coordinatore centrale dirige i passi) o *coreografia* (ogni servizio reagisce a eventi e decide autonomamente il passo successivo)
  - *Esempio pagamenti*: un pagamento che coinvolge debit dell'account, notifica al merchant e aggiornamento del ledger — se l'ultimo passo fallisce, la saga esegue le compensazioni (es. re-credit dell'account) invece di un rollback atomico impossibile su più DB separati
- **Event Sourcing e CQRS**: Event Sourcing salva lo stato di un'entità come sequenza di eventi immutabili (invece che come stato corrente sovrascritto) — utilissimo in ambito finanziario per audit trail completo, dato che ogni cambiamento di stato è tracciato. CQRS (Command Query Responsibility Segregation) separa il modello usato per le scritture da quello usato per le letture, spesso ottimizzati diversamente — combinato con Event Sourcing è un pattern molto comune in sistemi di pagamento/contabilità dove la tracciabilità storica è un requisito normativo

### Come esercitarti
Prepara un esempio in cui spieghi perché il **Circuit Breaker** è particolarmente rilevante in un sistema che chiama circuiti di pagamento esterni: se Visa/Mastercard rispondono lentamente, senza circuit breaker rischi di saturare i thread/connessioni del tuo servizio in attesa, propagando il problema a cascata.
