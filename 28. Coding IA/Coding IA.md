# 28. Sviluppare con l'IA e i coding agent

## Dalla proposta di testo all'azione verificabile

Un **LLM**, Large Language Model, genera risposte usando il contesto disponibile. Un **coding agent** collega un modello a strumenti che consentono di leggere file, applicare modifiche ed eseguire verifiche. Il valore nasce dal ciclo tra proposta e osservazione: un errore di compilazione fornisce un'evidenza da usare per correggere l'ipotesi.

Assistenti nel terminale, come Codex o Claude Code, e ambienti con funzionalità agentiche, come Cursor, organizzano questo ciclo in modi diversi. Aider e OpenHands sono altri esempi di strumenti in questo spazio. Funzionalità e modelli cambiano nel tempo; per capire l'architettura conta distinguere ambiente, modello, strumenti e permessi, senza dedurre capacità da un'etichetta commerciale.

## Strumenti, MCP e contesto

Il **tool use**, o function calling, permette al modello di chiedere un'azione a un'interfaccia definita. Il programma riceve argomenti, esegue il lavoro autorizzato e restituisce il risultato. Uno schema comprensibile aiuta a scegliere lo strumento giusto, ma non rende affidabile ogni argomento prodotto dal modello.

Il **Model Context Protocol**, MCP, standardizza alcune interazioni tra applicazioni e server che espongono strumenti, risorse e prompt. L'host ospita l'esperienza dell'agente, il client gestisce il collegamento e il server offre le capacità. Le comunicazioni usano JSON-RPC; tra i trasporti previsti ci sono stdio e Streamable HTTP. La [specifica dei trasporti MCP](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/transports.mdx) distingue questi modelli dal precedente trasporto HTTP con SSE.

Un connettore rende raggiungibile una capacità, non autorizza automaticamente ogni azione. File, pagine e output possono contenere istruzioni ostili: la **prompt injection** tenta di farle trattare come comandi affidabili. L'agente deve mantenere distinti dati esterni e istruzioni autorizzate.

## Rules, skill e progressive disclosure

File di convenzioni come `AGENTS.md` possono indicare build, stile e limiti del progetto secondo il supporto dello strumento. Una **skill** raccoglie istruzioni e risorse per un'attività specifica. La **progressive disclosure** presenta dettagli quando servono, invece di caricare ogni procedura nel contesto iniziale.

La **context window** limita ciò che il modello può usare in una singola elaborazione. Il **context engineering** sceglie quali evidenze, istruzioni e strumenti presentare e quando recuperarli. Un catalogo enorme può rendere più difficile selezionare la capacità giusta; retrieval e descrizioni precise aiutano, ma vanno misurati sul compito reale.

Approcci associati a Ponytail, raccolte di workflow come quelle di Matt Pocock e sistemi di gestione del catalogo come Ratel affrontano parti di questi problemi. Il principio riutilizzabile è partire dal bisogno, cercare soluzioni già presenti e introdurre nuove astrazioni solo quando giustificate. **YAGNI**, You Aren't Gonna Need It, invita a non implementare esigenze puramente ipotetiche; non giustifica l'eliminazione di controlli necessari.

## Ciclo di esecuzione e delega

Nel ciclo spesso chiamato **ReAct**, reasoning e acting si alternano: si formula un passo, si usa uno strumento e si interpreta l'osservazione. Un test fallito non è soltanto un ostacolo; aiuta a distinguere un'ipotesi errata da una configurazione incompleta.

I **subagent** possono lavorare su sottoproblemi con contesti distinti. La delega richiede confini di modifica e criteri di integrazione: due agenti che cambiano lo stesso file possono interferire, e una verifica parallela non sostituisce la verifica sul risultato finale. Il numero di agenti non misura la qualità.

## Usare l'agente su un backend Java

Per una commissione, si forniscono regole, valute, arrotondamenti ed esempi prima di chiedere l'implementazione. L'agente può costruire test, esplorare query, documentare un contratto o proporre refactoring. Una migrazione a record o virtual thread richiede comunque verifica di compatibilità e comportamento, non una sostituzione sintattica indiscriminata.

Gli **edge case** sono condizioni limite come importo zero, valuta assente o evento duplicato. La **hallucination** produce contenuti plausibili ma non supportati, per esempio un metodo inesistente. Compilazione, documentazione primaria e test osservabili riducono il rischio, mentre una spiegazione convincente da sola non dimostra correttezza.

## Dati, permessi e responsabilità

PAN, dati personali, segreti e credenziali richiedono politiche esplicite per l'accesso e il trattamento. Si usano dati sintetici quando bastano e si verificano condizioni del servizio e autorizzazioni prima di trasmettere informazioni. Un ambiente chiamato enterprise non prova da solo quale conservazione o accesso sia applicato.

Il codice generato viene valutato con gli stessi criteri del codice umano: correttezza, contratti, sicurezza e capacità di manutenzione. Per un pagamento sono decisivi transazioni, idempotenza ed esiti sconosciuti. Licenze e provenienza delle dipendenze entrano nel normale processo di revisione.

## Esercizio

Fornisci a un agente una regola di commissione con esempi e chiedi di implementarla e verificarla. Poi introduci un retry e un errore di arrotondamento. Valuta le evidenze prodotte, la capacità di correggersi e le modifiche superflue: il risultato utile è una soluzione comprensibile e verificata.
