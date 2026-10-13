# 6. Gestire i dati in un'architettura a microservizi

## L'autonomia comincia dalla proprietà dei dati

Nel pattern **database per service**, ogni servizio controlla il proprio modello e l'accesso ai propri dati. Non è obbligatorio assegnare subito una macchina fisica a ogni servizio: conta impedire che altri modifichino direttamente le sue tabelle. Questo confine permette di evolvere lo schema e scegliere lo storage senza coordinare ogni modifica con tutta l'applicazione.

La **polyglot persistence** usa tecnologie diverse per bisogni diversi, per esempio un database relazionale per registrazioni contabili e una cache per configurazioni. Offre flessibilità ma moltiplica competenze, backup e strumenti operativi. Perdere i join diretti tra servizi significa anche dover progettare API, composizione di dati o viste aggiornate tramite eventi.

## Transazioni locali e coordinamento distribuito

Una transazione locale mantiene insieme modifiche sul proprio database. Se un ordine, un pagamento e una prenotazione appartengono a servizi diversi, `@Transactional` su un metodo non li trasforma in un unico commit.

Il **Two-Phase Commit**, 2PC, coordina risorse compatibili attraverso una fase di preparazione e una decisione finale. Può mantenere risorse in attesa del coordinatore, con conseguenze sulla disponibilità. Una **Saga** coordina invece transazioni locali e compensazioni: liberare una prenotazione già fatta è un nuovo atto di business, non la cancellazione del tempo trascorso. Il capitolo 36 sviluppa questi modelli e il recupero dei passaggi incompleti.

Un evento può comunicare un fatto ad altri servizi senza aspettarne l'elaborazione. Un broker e uno storage durevole consentono recupero secondo configurazione e retention; non garantiscono da soli che ogni consumer applichi correttamente l'effetto. La Transactional Outbox lega evento da pubblicare e modifica locale, mentre l'Inbox aiuta a deduplicare l'elaborazione.

## Concorrenza: il problema non scompare con gli eventi

Il **lost update** avviene quando una scrittura sovrascrive il risultato di un'altra basandosi su una lettura ormai vecchia. Nel **locking ottimistico** una versione viene verificata al salvataggio; se è cambiata, l'operazione fallisce e il dominio decide se ricalcolare o segnalare un conflitto. Nel **locking pessimistico** una risorsa viene bloccata durante la transazione, aumentando la protezione dalla concorrenza ma anche le attese.

Con **Event Sourcing** lo stato si ricostruisce da eventi append-only, cioè aggiunti senza riscrivere quelli precedenti. Questo non elimina i conflitti: due comandi possono basarsi sulla stessa versione del flusso e produrre eventi incompatibili. Si verifica la versione attesa al momento dell'append o si usa un altro meccanismo di controllo coerente con l'event store.

**CQRS** separa il modello che accetta modifiche da quello che risponde alle query. Una **vista materializzata** conserva risultati già organizzati per la lettura e può essere aggiornata dagli eventi. Il lettore deve conoscere il possibile ritardo rispetto alla scrittura. CQRS ed Event Sourcing risolvono problemi distinti e possono essere adottati separatamente.

## Distribuire il carico senza perdere il significato

Il partizionamento divide i dati; lo **sharding** distribuisce le porzioni tra nodi. La chiave, per esempio account ID, influenza equilibrio del carico e costo delle operazioni tra shard. Una singola entità molto attiva può restare un collo di bottiglia anche con molte partizioni.

Una cache condivisa riduce letture costose ma introduce un'altra copia. Dopo una modifica bisogna decidere invalidazione, scadenza e comportamento durante errori. Il saldo usato per autorizzare un addebito non può essere trattato come una configurazione che tollera qualche secondo di ritardo.

## Un pagamento che attraversa tre servizi

Segui autorizzazione, contabilità e notifica. Definisci quale passo rende il pagamento accettato, quali effetti richiedono compensazione e quale lavoro può arrivare dopo. Verifica duplicati, scritture concorrenti e crash, partendo da una soluzione semplice e introducendo coordinamento ulteriore soltanto per requisiti reali.
