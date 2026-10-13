# 29. Metodi di lavoro, prodotto e comunicazione

## Rendere visibili decisioni e risultati

Le competenze tecniche acquistano valore quando il team comprende il bisogno, coordina il lavoro e verifica il risultato. Un **product mindset** collega l'intervento a un esito per utenti e organizzazione: ridurre i pagamenti abbandonati è un obiettivo; consegnare cinque endpoint è soltanto una misura di attività.

L'**output** è ciò che si produce; l'**outcome** è l'effetto ottenuto. Una nuova funzione può aumentare l'output senza migliorare l'esperienza. Definire una misura prima dello sviluppo rende discutibili ipotesi e priorità.

## Scrum: obiettivo, incremento e ispezione

Scrum organizza il lavoro in **Sprint**, periodi con un obiettivo. Il **Product Owner** è responsabile del valore e della gestione del Product Backlog, elenco ordinato del lavoro. Lo **Scrum Master** sostiene l'efficacia di Scrum; i **Developers** costruiscono l'incremento e organizzano il lavoro necessario. Le responsabilità non descrivono una gerarchia di assegnazione dei task.

Lo Sprint comprende planning, Daily Scrum, review e retrospective. Il **planning** definisce obiettivo e lavoro previsto; il **Daily Scrum** aiuta i Developers ad adattare il piano; la **review** ispeziona il risultato con gli stakeholder; la **retrospective** cerca miglioramenti nel modo di lavorare. L'incremento deve essere utilizzabile secondo la **Definition of Done**, criterio condiviso di completamento.

La **Definition of Ready** può essere un accordo del team su come preparare il lavoro, ma non è un elemento obbligatorio di Scrum. Può aiutare se chiarisce le condizioni, ostacolare se diventa un cancello che impedisce apprendimento e collaborazione.

## Kanban: osservare e limitare il lavoro in corso

Kanban rende visibile il flusso, definisce politiche e limita il **Work In Progress**, WIP, lavoro già iniziato e non concluso. Se la review accumula task, avviare altro sviluppo aumenta l'attesa; aiutare a completare ciò che è aperto può ridurla.

Il **lead time** misura un intervallo dalla richiesta alla consegna e il **cycle time** dall'inizio al completamento del lavoro, con punti di misura definiti dal processo. Non sono valori confrontabili se team diversi usano confini diversi. Distribuzioni, età del lavoro e throughput aiutano a distinguere un episodio da un collo di bottiglia persistente.

## Collegare metriche e priorità

Il **conversion rate** è la quota che completa un percorso; il **churn rate** misura l'abbandono secondo una finestra definita. **CAC**, Customer Acquisition Cost, riguarda il costo di acquisizione; **LTV**, Lifetime Value, il valore atteso nel tempo. **MRR**, Monthly Recurring Revenue, descrive ricavi ricorrenti mensili dove il modello lo prevede. Nessuna di queste metriche è interpretabile senza popolazione e periodo.

Il **time-to-market** riguarda il tempo necessario a portare un risultato sul mercato. **RICE** combina Reach, Impact, Confidence ed Effort: diffusione, impatto, fiducia nella stima e sforzo. Aiuta a rendere esplicite le ipotesi, non trasforma stime fragili in una decisione certa. Product Manager, designer, QA ed esperti dei vincoli contribuiscono a verificare aspetti differenti dello stesso obiettivo.

## Scrivere requisiti e decisioni

Una **user story** collega ruolo, azione e beneficio. I criteri di accettazione rendono osservabile il comportamento. **INVEST** ricorda qualità desiderabili delle storie: Independent, Negotiable, Valuable, Estimable, Small e Testable. La negoziabilità significa lasciare spazio alla soluzione, mantenendo chiaro il bisogno.

```text
Dato un pagamento già completato con una certa chiave
Quando arriva di nuovo la stessa richiesta
Allora viene restituito l'esito precedente senza un altro addebito
```

Un **Architecture Decision Record**, ADR, registra contesto, decisione e conseguenze, comprese le alternative rilevanti. Il modello **C4** rappresenta Context, Containers, Components e Code con livelli progressivi. Qui «container» indica un'unità applicativa o dati, non necessariamente un container Docker. Un disegno è utile se chiarisce confini e interazioni alla persona che deve decidere.

## Discutere disaccordi e rischi

Un disaccordo tecnico si affronta rendendo espliciti requisiti e prove. Un **Proof of Concept** verifica un dubbio delimitato; non dimostra automaticamente affidabilità produttiva. Durante un incidente, ipotesi e osservazioni vanno mantenute distinte. Per una richiesta urgente si può ridurre il perimetro della funzione conservando i controlli essenziali e spiegando il rischio residuo.

Il **debito tecnico** è il costo futuro prodotto da alcune decisioni correnti. Non coincide con qualsiasi codice imperfetto: interessa quando rende più costoso o rischioso il cambiamento. Un compromesso consapevole deve avere una motivazione e un modo di riesaminarlo.

## Raccontare un'esperienza con STAR

**STAR** organizza Situation, Task, Action e Result: contesto, responsabilità, azioni e risultato. Usa un'esperienza reale e distingui il tuo contributo da quello del gruppo. Una misura concreta o un cambiamento osservato rende il racconto valutabile; non serve inventare un risultato perfetto.

Come esercizio, racconta un disaccordo su una soluzione tecnica. Spiega quale evidenza ha modificato la decisione e che cosa hai imparato, senza attribuire automaticamente la scelta corretta alla tua proposta iniziale.
