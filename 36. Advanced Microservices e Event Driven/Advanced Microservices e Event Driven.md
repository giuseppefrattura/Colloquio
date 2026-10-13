# 36. Microservizi avanzati e architetture a eventi

## Separare richieste e fatti

Un **comando** chiede che un'azione venga eseguita, per esempio `AuthorizePayment`. Un **evento** descrive un fatto già avvenuto, come `PaymentAuthorized`. Il producer pubblica il messaggio, il consumer lo elabora e il broker ne media il trasporto. Distinguere intenzione ed esito evita che servizi diversi interpretino una richiesta come se fosse una conferma.

Un'architettura **event-driven** fa reagire i componenti agli eventi. Il disaccoppiamento permette a notifica e reportistica di procedere senza allungare la risposta dell'autorizzazione. Introduce però ritardi, duplicati e nuovi stati intermedi: l'utente deve sapere se un pagamento è accettato, completato o ancora da verificare.

## Coordinare transazioni locali con una Saga

Una **Saga** divide un processo in transazioni locali e stabilisce azioni di compensazione. Se una prenotazione viene confermata ma il pagamento fallisce, la compensazione può liberare la prenotazione. Non cancella il tempo trascorso né gli effetti già osservati e può fallire a sua volta.

Nell'**orchestrazione** un coordinatore persistente dirige i passi e ne registra l'esito. Nella **coreografia** i servizi reagiscono agli eventi degli altri. La prima rende il percorso più esplicito; la seconda distribuisce la collaborazione, ma può renderla difficile da ricostruire. In entrambi i casi servono identificatori, scadenze, recupero e intervento sui processi bloccati.

Il **Two-Phase Commit**, o 2PC, coordina invece un commit atomico tra partecipanti compatibili mediante preparazione e decisione finale. Offre proprietà differenti dalla Saga e può mantenere risorse bloccate in attesa del coordinatore. La scelta dipende dalle garanzie richieste e dal supporto delle risorse, non da una preferenza universale.

## Chiudere il divario tra database e messaggi

Salvare un pagamento e poi pubblicare un evento sono due azioni che possono separarsi in caso di crash. La **Transactional Outbox** registra dati di business ed evento da inviare nella stessa transazione locale. Un processo successivo legge l'outbox e pubblica sul broker. Se il crash avviene dopo la pubblicazione e prima della conferma locale, l'evento può essere pubblicato nuovamente.

Per questo il consumer deve essere idempotente. Con l'**Inbox Pattern** registra l'identificatore del messaggio insieme all'effetto sul proprio database, nella stessa transazione. Un vincolo di unicità riconosce i duplicati. Registrare l'identificatore prima dell'elaborazione in una transazione separata può perdere l'effetto dopo un crash: il messaggio apparirebbe già trattato. Per effetti su servizi esterni occorre anche un protocollo di idempotenza concordato.

## Consegna, ordine e recupero

**At-most-once** ammette perdite pur evitando riconsegne nel modello adottato. **At-least-once** privilegia la riconsegna ma ammette duplicati. **Exactly-once** va sempre riferito a un confine preciso; una garanzia interna al broker non rende atomica una chiamata a una banca. Si parla spesso di **effectively-once** quando riconsegna e deduplicazione producono un solo effetto osservabile.

L'ordine va stabilito per una chiave, come il pagamento, e verificato con versioni o sequenze. Un **poison message** fallisce ripetutamente per contenuto o logica. Dopo tentativi limitati può essere inviato in una **Dead Letter Queue**, coda separata per diagnosi e recupero. Non basta parcheggiarlo: servono responsabile, allarme e regole di reinvio. La **backpressure** limita la produzione o il lavoro ammesso quando i consumer non tengono il passo.

## Evolvere il contratto e ricostruire lo stato

Lo **schema dell'evento** stabilisce campi e significato. Lo schema evolution permette di modificarlo mantenendo la compatibilità dichiarata con i consumer; aggiungere un campo opzionale è diverso da cambiare l'unità di un importo. Un registro degli schemi facilita i controlli ma non verifica automaticamente ogni significato di business.

Il **replay** rielabora eventi conservati. È utile per ricostruire una vista, ma non dovrebbe inviare nuovamente email o addebiti senza una decisione esplicita. **CQRS**, Command Query Responsibility Segregation, separa i modelli per modificare e leggere i dati. **Event Sourcing** usa la sequenza degli eventi come fonte dello stato. Puoi usare CQRS senza Event Sourcing; adottare quest'ultimo richiede strategie per snapshot, evoluzione degli eventi e recupero.

## Confini verso client e sistemi esistenti

Un **API Gateway** instrada le richieste e applica politiche comuni; un **Backend for Frontend** adatta le API alle esigenze di uno specifico client. Lo **Strangler Fig Pattern** sostituisce gradualmente funzioni di un sistema esistente instradando verso nuove implementazioni. Un'**Anti-Corruption Layer** traduce il modello esterno, evitando che termini e vincoli legacy contaminino il nuovo dominio.

Per esercitarti, segui un evento di pagamento dal salvataggio alla contabilità. Descrivi i crash possibili prima e dopo ogni conferma e indica come il sistema recupera senza perdere un effetto e senza duplicarlo.
