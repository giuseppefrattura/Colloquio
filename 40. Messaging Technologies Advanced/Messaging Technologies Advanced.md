# 40. Messaggistica avanzata: consegna, ordine e recupero

## Il percorso di un evento Kafka

Il capitolo 12 introduce Kafka come log distribuito; qui seguiamo le decisioni che rendono un flusso affidabile. Un **broker** ospita partizioni dei topic. Ogni partizione ha un **leader**, che gestisce letture e scritture ordinarie, e repliche follower. Le **ISR**, In-Sync Replicas, sono repliche considerate sufficientemente allineate dal protocollo. La replica riduce il rischio di perdita, ma la configurazione determina quali guasti si possono sostenere.

Il producer può usare `acks=0`, senza aspettare una conferma, oppure `acks=1`, aspettando quella del leader. Con `acks=all` la conferma coinvolge le repliche ISR; `min.insync.replicas` stabilisce il minimo richiesto perché la scrittura possa essere accettata con questa modalità. Si bilanciano quindi disponibilità delle scritture e protezione dalla perdita, senza interpretare «all» come «qualsiasi replica esistente». La documentazione sul [modello di Kafka](https://kafka.apache.org/42/design/design/) distingue queste garanzie da quelle sugli effetti esterni.

Il **batching** raggruppa messaggi per ridurre richieste e costi; la compressione riduce i byte trasferiti. `batch.size` limita la dimensione del batch e `linger.ms` ne regola l'attesa. Il beneficio sul throughput può aumentare la latenza. Un producer idempotente limita i duplicati dovuti ai propri retry, ma non riconosce automaticamente due pubblicazioni distinte dello stesso fatto di business.

## Offset, riassegnazione e ordine

Un **consumer group** divide le partizioni tra i propri membri. L'assegnazione stabilisce chi legge cosa; il **rebalancing** modifica questa distribuzione quando cambiano i partecipanti o le partizioni. Nel modello di consumer group qui considerato, aggiungere più consumer delle partizioni non aumenta il parallelismo di assegnazione.

Il **commit dell'offset** salva la posizione da cui riprendere. Confermare prima dell'effetto applicativo espone alla perdita dell'elaborazione dopo un crash; confermare dopo espone alla ripetizione. Il commit automatico richiede di capire quando avviene rispetto al lavoro effettivo. `auto.offset.reset` decide il comportamento quando non c'è un offset valido, non forza ogni riavvio a ignorare quello salvato.

Il **consumer lag** è la distanza tra avanzamento disponibile e posizione del consumer, secondo la misura scelta. Può crescere per un picco, una dipendenza lenta o un consumer fermo. Va letto insieme al ritmo di produzione e consumo, non come un numero isolato.

L'ordine del log vale per partizione. Una chiave stabile indirizza gli eventi correlati alla stessa partizione con una strategia di partizionamento coerente. Cambiare il numero di partizioni o elaborare in parallelo può compromettere l'ordine osservato dal dominio: occorre progettare anche questi passaggi.

## Consegna e tentativi

**At-most-once** può perdere elaborazioni, **at-least-once** può ripeterle. Le transazioni Kafka supportano garanzie di elaborazione entro il proprio confine; un aggiornamento su un database esterno o una chiamata bancaria richiedono coordinamento ulteriore. L'**effectively-once** usa idempotenza e deduplicazione per ottenere un solo effetto osservabile. Il capitolo 36 spiega Outbox e Inbox per collegare transazioni locali e messaggi.

Un retry immediato può essere utile per un errore brevissimo; il backoff distribuisce i tentativi. Un **retry topic** separa i messaggi da riprovare, ma può cambiare l'ordine rispetto agli eventi successivi. Un **Dead Letter Topic** raccoglie fallimenti non risolti. I poison message, che falliscono sistematicamente, richiedono diagnosi e una decisione di recupero invece di cicli infiniti.

## Il percorso di un messaggio RabbitMQ

Nel modello a code, il producer pubblica su un **exchange**, che instrada verso le **queue** usando **binding**, cioè regole di collegamento. La **routing key** accompagna il messaggio. Un exchange **direct** usa corrispondenze esatte; un **topic** usa pattern; un **fanout** distribuisce alle code collegate; un **headers** decide in base agli header.

Il consumer invia un **ack** per confermare; `nack` o `reject` possono segnalare un fallimento secondo le modalità supportate. Il **requeue** rimette il messaggio in coda, ma ripeterlo senza attesa può creare un ciclo continuo. Il **prefetch** limita i messaggi consegnati e ancora non confermati, aiutando a controllare lavoro in corso e distribuzione tra consumer.

Una **Dead Letter Exchange** instrada i messaggi scartati secondo la configurazione. Code di retry con **TTL**, durata di vita dei messaggi, possono introdurre attese prima del reinvio. Si verificano limiti e comportamento concreto del tipo di coda utilizzato. I publisher confirm riguardano l'accettazione da parte del broker, non il completamento del consumer.

## Scegliere il modello e il contenuto

| Esigenza | Modello da valutare | Questione da verificare |
|---|---|---|
| Rileggere una storia di eventi | Log con retention, come Kafka | Durata, costi e comportamento del replay |
| Distribuire compiti a worker | Code con competing consumer | Ack, retry e limite di lavoro in corso |
| Instradare per regole articolate | Exchange e binding | Evoluzione delle regole e code destinatarie |
| Preservare la sequenza di un'entità | Partizionamento o consumo serializzato | Concorrenza, retry e cambiamenti di topologia |

I **competing consumer** si dividono il lavoro della stessa coda o gruppo. Gruppi o code distinti consentono invece elaborazioni indipendenti dello stesso fatto. Nell'**Event Notification** il messaggio annuncia un cambiamento e il consumer può richiedere altri dati; nell'**Event-Carried State Transfer** porta i dati necessari, riducendo chiamate ma duplicando informazioni e vincoli di aggiornamento.

## Un pagamento lungo tutta la catena

Il servizio registra il pagamento e `PaymentAuthorized` in outbox. Il publisher lo invia; contabilità e notifiche lo ricevono indipendentemente. La contabilità registra identificatore ed effetto in modo atomico; le notifiche controllano i duplicati con le proprie garanzie. Spiega come si comportano crash, rebalance e retry e quali metriche mostrano un ritardo prima che diventi un problema per il cliente.
