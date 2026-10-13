# 42. Osservabilità e OpenTelemetry

## Rendere interrogabile il comportamento del sistema

L'**osservabilità** è la capacità di comprendere il comportamento interno attraverso i segnali prodotti dal sistema. I log registrano eventi, le metriche aggregano misure e le trace descrivono percorsi di operazioni. Raccogliere tutto senza una domanda concreta può aumentare il costo senza ridurre il tempo necessario a diagnosticare un guasto.

Per un pagamento vuoi sapere se il servizio è disponibile, dove si trova un ritardo e quali passaggi hanno portato a un esito sconosciuto. Servono segnali coerenti e identificatori che consentano di collegarli.

## Trace, span e propagazione del contesto

Una **trace** raccoglie operazioni correlate. Uno **span** descrive una singola operazione con tempi, attributi ed esito; relazioni parent-child mostrano quali operazioni ne abbiano avviate altre. Il **Trace ID** identifica la traccia e lo **Span ID** la singola operazione.

La **context propagation** trasmette questi riferimenti tra processi, per esempio mediante header HTTP o metadati di messaggi. In un flusso asincrono si può usare una relazione di parentela o un collegamento tra span secondo il modello scelto. Il solo transaction ID di business non sostituisce la struttura della trace, ma può permettere di cercarla.

Il **sampling** seleziona le trace da conservare. Riduce il costo, ma può eliminare proprio una richiesta interessante. Si definiscono politiche coerenti con errori, latenza e limiti di dati; non si presume che una trace mancante dimostri che l'operazione non sia avvenuta.

## Il percorso della telemetria

L'**instrumentation** aggiunge i punti di misura, automaticamente tramite librerie o manualmente nel codice. Un **SDK** gestisce produzione e trattamento dei segnali; un **exporter** li invia al destinatario. L'OpenTelemetry **Collector** riceve, elabora e inoltra telemetria. **OTLP**, OpenTelemetry Protocol, è un protocollo per questo scambio.

Il Collector consente di centralizzare filtri, batching e instradamento verso backend diversi. Non è di per sé il database di consultazione: occorre un backend che conservi e renda interrogabili i segnali. La telemetria deve avere limiti e un comportamento previsto anche quando il backend non è raggiungibile.

## Metriche per servizi e risorse

Il metodo **RED** osserva Rate, Errors e Duration: ritmo delle richieste, errori e tempi. Il metodo **USE** osserva Utilization, Saturation ed Errors delle risorse: uso, lavoro in attesa e guasti. Una CPU al 30% può convivere con richieste in coda per un pool di connessioni esaurito.

Per un servizio Java si correlano percentili di latenza, memoria, GC e connessioni. Per la messaggistica si osservano profondità delle code e consumer lag. p95 e p99 aiutano a vedere la coda dei tempi, che la media può nascondere.

La **cardinalità** delle metriche è il numero di combinazioni delle etichette. Usare un identificatore di pagamento come label genera serie quasi illimitate. Gli identificatori individuali appartengono generalmente a log e trace, con regole di accesso e conservazione adeguate.

## Log e alert orientati all'azione

Lo **structured logging** rappresenta gli eventi con campi stabili, come servizio, esito e identificatore di correlazione. Livelli e centralizzazione aiutano la ricerca, ma password, token e dati sensibili non devono diventare materiale diagnostico diffuso.

Un alert deve indicare un problema e un'azione. Collegarlo al consumo dello SLO può distinguere una variazione innocua da un degrado del servizio. Il **burn rate** esprime la velocità con cui viene consumato il budget d'errore rispetto a quella ammessa; finestre brevi e lunghe aiutano a riconoscere sia incidenti rapidi sia degradazioni persistenti.

## Leggere un rallentamento lungo la catena

Nel flusso `Client → Gateway → Service A → Kafka → Service B → Database`, l'aumento del p99 può nascere in punti diversi. Parti dal traffico e dagli errori, cerca trace rappresentative e individua attese e span lenti. Un consumer lag in aumento suggerisce un ritardo asincrono; connessioni occupate e query lente indicano un altro percorso. Confronta poi i segnali con cambiamenti recenti e verifica che la mitigazione ripristini anche l'esito per l'utente.
