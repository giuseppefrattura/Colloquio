# 37. Domain-Driven Design e architettura del software

## Costruire un linguaggio condiviso

Il **dominio** è l'area di attività che il software supporta. Nel Domain-Driven Design, o **DDD**, sviluppatori ed esperti costruiscono un modello e un linguaggio condiviso, chiamato *ubiquitous language*. «Pagamento autorizzato» deve avere un significato concordato prima di diventare una classe o un evento.

Un **sottodominio** è una parte del problema. Il **core domain** contiene le capacità che differenziano l'organizzazione; un **supporting subdomain** le sostiene senza essere il principale elemento distintivo. Un **generic subdomain** risolve un problema comune, per il quale può essere adatto un prodotto esterno. Questa distinzione aiuta a decidere dove investire nello sviluppo personalizzato.

## Delimitare il significato con un Bounded Context

Un **Bounded Context** è il confine entro il quale un modello e i suoi termini hanno un significato coerente. Un cliente per la fatturazione può essere il destinatario fiscale; per il supporto può essere chi apre una richiesta. Cercare una classe universale `Customer` può confondere responsabilità e regole.

Una **Context Map** descrive le relazioni tra contesti: chi produce dati, chi dipende da chi e come viene tradotto il linguaggio. L'**Anti-Corruption Layer** è una barriera di traduzione che protegge il modello interno da quello esterno. Un contesto non coincide automaticamente con un microservizio: il primo è un confine del modello, il secondo anche un'unità operativa e di rilascio.

## Modellare identità, valori e invarianti

Un'**Entity** conserva un'identità nel tempo: un ordine rimane lo stesso ordine anche se cambia indirizzo. Un **Value Object** si identifica attraverso il suo valore: due importi con quantità e valuta uguali possono essere equivalenti. L'immutabilità aiuta a rendere i Value Object prevedibili, ma bisogna modellare tutte le informazioni che ne determinano il significato.

Un **Aggregate** raggruppa oggetti che devono rispettare insieme certe **invarianti**, cioè regole sempre vere dopo una modifica valida. L'**Aggregate Root** è il punto d'accesso che controlla tali modifiche. Per un ordine potrebbe impedire l'aggiunta di righe dopo la conferma. Un aggregate enorme aumenta contesa e costo; confini troppo piccoli rendono difficili le invarianti da garantire.

Un **Domain Service** esprime una regola di dominio che non appartiene naturalmente a una sola entità. Un **Repository** offre al modello l'accesso agli aggregate senza esporre i dettagli della persistenza. Un **Domain Event** rappresenta un fatto del dominio; non deve necessariamente coincidere con il messaggio pubblico inviato ad altri servizi, che ha un contratto proprio.

## Separare il modello dai dettagli tecnici

Nell'architettura a livelli si distinguono presentazione, applicazione, dominio e infrastruttura. Nell'architettura **esagonale**, le **porte** sono interfacce delle interazioni e gli **adapter** collegano HTTP, database o messaggistica. Il dominio può così lavorare con una porta `PaymentGateway` senza conoscere il client HTTP concreto.

Clean Architecture e Onion Architecture organizzano responsabilità e dipendenze intorno alle regole interne. La loro idea centrale è la **dependency rule**: i dettagli esterni dipendono dalle astrazioni interne. Non significa nascondere ogni libreria dietro un'interfaccia, ma proteggere i punti in cui un dettaglio rischia di guidare il modello.

## Decidere come distribuire i moduli

Un **monolite modulare** mantiene moduli distinti in un unico processo e rilascio. Offre chiamate locali e operatività più semplice, purché i confini siano realmente rispettati. I microservizi permettono rilascio e scalabilità indipendenti, ma aggiungono guasti di rete, consistenza distribuita e lavoro operativo. Un'architettura a eventi è un modo di collaborazione che può esistere in entrambe le soluzioni.

La scelta considera chi possiede i moduli, quanto spesso devono essere rilasciati separatamente e quali carichi richiedono scaling distinto. Se il team deve coordinare ogni cambiamento tra tutti i servizi, l'indipendenza cercata potrebbe non essere stata ottenuta.

## Un esercizio di modellazione

Modella ordine e pagamento senza partire dalle tabelle. Definisci identità, stati validi e regole che non possono essere violate. Spiega quali regole richiedono una transazione locale e quali possono essere coordinate tra contesti. Solo dopo scegli le classi, le porte e la distribuzione dei componenti.
