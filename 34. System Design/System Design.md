# 34. Progettare un sistema: dai requisiti alle scelte

## Cominciare dal problema

Il **system design** è il lavoro di traduzione di un bisogno in componenti, dati e interazioni. Dire «uso Kafka e Kubernetes» non spiega ancora come il sistema soddisfi quel bisogno. Per un servizio di ordini bisogna prima capire chi crea l'ordine, quando viene considerato accettato e che cosa succede se pagamento o magazzino non rispondono.

I **requisiti funzionali** descrivono le operazioni: creare, consultare o annullare un ordine. I **requisiti non funzionali** descrivono le qualità e i limiti: latenza, disponibilità, sicurezza, costi e volume. Un requisito come «veloce» va trasformato in un obiettivo misurabile, per esempio una soglia del percentile p95 sotto un carico definito. Anche i vincoli del team e dell'infrastruttura influenzano la soluzione.

## Stimare il carico

Un milione di richieste al minuto corrisponde a circa 16.667 richieste al secondo, indicate anche come **RPS**. È una media: il picco può essere superiore. Per stimare banda e crescita dello storage servono anche dimensione dei messaggi, rapporto tra letture e scritture e durata della conservazione. Il numero di connessioni contemporanee dipende dalla durata delle richieste, non soltanto dal loro numero.

Queste stime sono ipotesi da verificare. Se ogni richiesta genera tre query, il database vede un carico diverso da quello dell'API. Se un milione di eventi occupa mediamente un kilobyte ciascuno, il contenuto grezzo è circa un gigabyte, prima di indici, repliche e metadati.

## Disegnare il flusso e scegliere dove mantenere lo stato

Si definiscono prima le API e il modello dei dati, poi il percorso di una richiesta. Un servizio **stateless** non conserva nello stato locale della singola istanza le informazioni necessarie tra richieste: un'altra replica può gestire la richiesta successiva. Un servizio **stateful** conserva invece stato che richiede collocazione, replica o recupero. Spostare le sessioni in uno storage condiviso facilita la replica del servizio, ma aggiunge una dipendenza.

La **scalabilità verticale** aumenta le risorse di una macchina; quella **orizzontale** aggiunge macchine o repliche. Un **load balancer** distribuisce le richieste tra istanze. La replica copia gli stessi dati per disponibilità o letture, mentre il partizionamento divide i dati; lo **sharding** distribuisce queste porzioni tra nodi. Una chiave sbilanciata può concentrare il traffico su un solo shard.

Una cache conserva risultati riutilizzabili e richiede una politica di scadenza o invalidazione. Una **CDN**, Content Delivery Network, avvicina contenuti cacheabili agli utenti mediante nodi distribuiti. Una coda assorbe picchi e consente lavoro asincrono, ma introduce attesa: l'accettazione di un ordine e il suo completamento diventano stati distinti.

## Scegliere confini e responsabilità

Un'architettura a livelli separa presentazione, applicazione e accesso ai dati. Un **monolite modulare** mantiene un solo rilascio con confini interni espliciti. I microservizi rendono indipendenti alcuni rilasci, ma trasformano chiamate locali in comunicazioni di rete. Un'architettura a eventi collega componenti attraverso fatti già avvenuti.

L'architettura esagonale e la Clean Architecture proteggono il dominio dalle dipendenze infrastrutturali, usando interfacce e implementazioni esterne. CQRS separa i modelli di lettura e scrittura; Event Sourcing conserva gli eventi come fonte dello stato. Sono decisioni diverse e non occorre adottarle insieme. Il capitolo 37 approfondisce i confini del dominio; il capitolo 36 sviluppa Saga, Outbox e gli altri pattern di collaborazione.

## Verificare anche guasti, sicurezza e costo

Un **Single Point of Failure** è un componente la cui perdita rende indisponibile una funzione essenziale. Aggiungere repliche non risolve il problema se tutte dipendono da un unico database non recuperabile. La **fault tolerance** è la capacità di mantenere le proprietà richieste in presenza di guasti; la resilienza comprende anche contenimento e recupero.

Per ogni dipendenza si spiegano timeout, tentativi e comportamento degradato. Per ogni dato si chiariscono permessi e conservazione. Per ogni operazione importante si indicano metriche e tracce che consentiranno di diagnosticarla. SLI e SLO, spiegati nel capitolo 39, collegano queste decisioni al servizio percepito dall'utente.

## Un esercizio completo

Progetta un sistema di ordini che riceva un picco dieci volte superiore alla media. Illustra come accettare le richieste, limitare il lavoro concorrente, mostrare lo stato e recuperare dopo un guasto. Concludi motivando il costo di code, repliche e storage e dichiarando quale compromesso, o **trade-off**, hai accettato tra tempo di risposta, consistenza e complessità.
