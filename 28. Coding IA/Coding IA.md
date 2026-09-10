## 28. Coding con IA & Coding Agent

### Cos'è e perché conta
Nei colloqui tecnici moderni (soprattutto per ruoli Senior) non ci si aspetta più che uno sviluppatore ignori gli strumenti di Intelligenza Artificiale, ma che dimostri una **forte maturità nel loro utilizzo**: saper sfruttare l'IA e gli **Agenti Autonomi di sviluppo (Coding Agents)** come acceleratori di produttività, mantenendo il controllo rigoroso su architettura del software, sicurezza, privacy dei dati finanziari (PCI-DSS/GDPR) e qualità del codice.

---

### Cosa studiare

#### 1. I Principali Coding Agent ed Ecosistemi
I coding agent sono sistemi basati su LLM capaci non solo di suggerire testo, ma di **agire autonomamente nell'ambiente di sviluppo** (eseguire comandi shell, navigare codebase complesse, modificare file, eseguire test e correggere bug iterativamente):

- **Claude Code (Anthropic)**:
  - Agent a riga di comando (CLI) ad altissima autonomia progettato per sviluppatori.
  - Opera direttamente nel terminale locale: esegue comandi Git, analizza l'intero workspace, applica modifiche a più file, esegue suite di test Maven/Gradle e crea Pull Request in autonomia.
  - Ottimizzato per modelli della famiglia Claude 3.5/3.7 Sonnet con supporto esteso al reasoning e tool use nativo.
- **OpenAI Codex & Canvas / Operator**:
  - Pioniere dei modelli di code generation (da cui è nato GitHub Copilot).
  - L'ecosistema OpenAI attuale include interfacce collaborative (Canvas) e agenti capaci di operare su sandbox con esecuzione Python/Shell per debugging e analisi di problemi complessi.
- **Cursor & Antigravity (Agentic IDEs)**:
  - IDE e ambienti di sviluppo con supporto agentico nativo multi-file e background tasks.
  - Capacità di analizzare semanticamente l'intera codebase, creare piani di implementazione (`implementation_plan.md`), invocare sotto-agenti e validare i risultati via terminale.
- **Aider & OpenHands / SWE-agent**:
  - Tool open-source per il pair programming agentico da terminale, basati sul ciclo Git (un commit atomico per ogni task eseguito con successo) e benchmarkati su SWE-bench per la risoluzione reale di issue GitHub.
- **Assistenti Conversazionali & Pi (Inflection)**:
  - Strumenti di supporto al ragionamento, brain-storming architetturale e chiarimento dei requisiti di business prima della fase di stesura del codice.

---

#### 2. Anatomia di un Coding Agent: MCP, Skills, Rules e Tool Use

Per comprendere e pilotare un coding agent a livello Senior, occorre padroneggiarne l'architettura interna:

```
┌─────────────────────────────────────────────────────────────┐
│                       LLM / AGENT CORE                      │
│      (Reasoning, Planning, Execution Loop: ReAct / Act-Obs) │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
      ┌────────▼────────┐             ┌────────▼────────┐
      │   KNOWLEDGE &   │             │   TOOLS & MCP   │
      │   CONVENTIONS   │             │   INTEGRATION   │
      └────────┬────────┘             └────────┬────────┘
               │                               │
   ┌───────────┴───────────┐       ┌───────────┴───────────┐
   │ • Rules (AGENTS.md)   │       │ • Built-in Tools      │
   │ • Skills (On-demand)  │       │   (view, edit, bash)  │
   │ • System Prompts      │       │ • MCP Servers (DB,    │
   │ • Project Memory      │       │   GitHub, Jira, API)  │
   └───────────────────────┘       └───────────────────────┘
```

##### A. MCP (Model Context Protocol)
- **Cos'è**: è uno **standard aperto e universale** (introdotto da Anthropic e adottato da tutto l'ecosistema) che standardizza il modo in cui i modelli di intelligenza artificiale comunicano con tool e sorgenti dati esterne.
- **Il problema che risolve**: prima di MCP, ogni integrazione (es. collegare un agente a un DB Oracle, a un cluster Kubernetes o a Jira) richiedeva connettori custom e codice proprietario. Con MCP, uno sviluppatore scrive un server MCP una volta sola e qualsiasi agent/client compatibile può utilizzarlo.
- **Architettura**:
  - **Host / Client**: l'ambiente dell'agente (es. Claude Code, Cursor, Antigravity).
  - **Server MCP**: un processo leggero locale o remoto che espone *Risorse* (dati da leggere), *Prompt* (template) e *Tools* (funzioni eseguibili, es. `query_oracle_db`, `inspect_kafka_topic`).
  - **Protocollo JSON-RPC**: comunicazione standard via `stdio` o `SSE` (Server-Sent Events).

##### B. Skills (Competenze On-Demand)
- **Cos'è**: un set modulare di istruzioni specializzate, script, checklist e regole di dominio caricate **on-demand** dall'agente solo quando il task lo richiede.
- **Perché è fondamentale**: la context window dei modelli ha un costo e un limite di attenzione. Anziché riempire il system prompt con 500 pagine di linee guida, le Skills permettono all'agente di "consultare il manuale" solo quando deve svolgere uno specifico compito (es. skill per refactoring Spring Boot 3.x, skill per ISO 20022 XML, skill per tuning query Oracle).

##### C. Rules & Project Conventions (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`)
- File posti nella root del progetto per istruire l'agente sulle convenzioni inderogabili:
  - Build command (`mvn clean test`, `gradle check`).
  - Stile architetturale (Package-by-feature, DTO immutabili con record, Constructor Injection obbligatoria).
  - Regole di sicurezza e gestione segreti (mai loggare PAN, mai fare commit di credenziali).

##### D. Tool Use (Function Calling) & Execution Loop
- Il pattern **ReAct (Reasoning + Acting)**:
  1. **Think / Plan**: l'agente analizza l'obiettivo e scompone il problema.
  2. **Call Tool**: invoca un'azione (es. `grep_search`, `view_file`, `run_command`).
  3. **Observe**: riceve l'output del tool (es. errore di compilazione Maven).
  4. **Self-Correction**: deduce la causa dell'errore, corregge il file sorgente e re-itera fino a completamento.

##### E. Subagents & Multi-Agent Orchestration
- Per task complessi, l'agente principale può orchestrare **sotto-agenti specializzati** con context window isolate (es. un agente analizza i requisiti, un secondo modifica il codice, un terzo esegue i test e fa review di sicurezza).

---

#### 3. Esempi di Skill e Framework di Riferimento: Ponytail, Matt Pocock e Ratel

Nel panorama dello sviluppo agentico, alcune skill e framework sono diventati standard di riferimento della community per risolvere problemi specifici di affidabilità ed efficienza:

##### 🪮 Ponytail (di Dietrich Gebert)
- **Scopo**: contrastare il **code bloat** e l'**over-engineering** tipico degli LLM, costringendo l'agente ad adottare la mentalità pragmatica di un senior developer "pigro ma rigoroso".
- **Come funziona (La Decision Ladder)**:
  Inietta nell'agente una scala di priorità inderogabile prima di scrivere qualsiasi riga di codice:
  1. **YAGNI (You Aren't Gonna Need It)**: la feature/modifica deve davvero esistere o è superflua?
  2. **Reuse**: esiste già qualcosa di analogo nel codice del progetto?
  3. **Stdlib/Native**: si può risolvere usando solo le librerie standard di Java o feature native della piattaforma invece di installare nuove dipendenze?
  4. **Existing Dependency**: c'è già una libreria presente nel `pom.xml` adatta allo scopo?
  5. **One-liner / Minimalism**: implementa la soluzione più sintetica, pulita e minimale possibile.
- **Sicurezza garantita**: pur riducendo il codice al minimo, impone esplicitamente di non toccare o indebolire mai la validazione dei dati, l'error handling e la sicurezza.
- **Impatto**: riduce fino al 50-70% i token generati, i tempi di risposta e la complessità accidentale del codice.

##### 🎯 Matt Pocock Skills (`mattpocock/skills`)
- **Scopo**: trasformare il cosiddetto *"vibe coding"* (programmazione basata su prompt vaghi e improvvisati) in un **processo ingegneristico disciplinato e ripetibile** per Claude Code, Cursor e agenti compatibili.
- **I comandi e workflow principali**:
  - **`/grill-me` (o `/grill-with-docs`)**: l'agente assume il ruolo di un severo intervistatore/architetto che mette sotto stress l'idea o il piano dello sviluppatore con domande mirate, scovando edge case e ambiguità *prima* di toccare qualsiasi riga di codice.
  - **`/to-spec` & `/to-tickets`**: scompone una feature complessa in specifiche tecniche formali e ticket atomici implementabili singolarmente.
  - **`/tdd` & `/implement`**: guida l'agente a seguire rigorosamente il ciclo Test-Driven Development (scrivi il test che fallisce → scrivi il codice minimo per farlo passare → refactoring).
  - **`/wayfinder`**: skill per analizzare e orientarsi rapidamente in codebase monolitiche o non documentate.

##### 🦡 Ratel (`ratel-ai/ratel`)
- **Scopo**: piattaforma di **Context Engineering** e gestione del catalogo di tool/skills, creata per risolvere il problema del **Context Bloat** (quando un agente ha troppi tool caricati e spreca token o si confonde nella scelta).
- **Come funziona (Progressive Disclosure)**:
  - Motore di retrieval ad altissime prestazioni (scritto in Rust) che indicizza tutte le skill e i tool disponibili tramite ricerca ibrida (BM25 + semantica).
  - Anziché iniettare l'intero catalogo nel prompt iniziale, presenta all'agente solo i tool e le skill pertinenti al sotto-task corrente.
  - Espone un proprio **server MCP**, integrabile nativamente con Claude Code, Cursor e Codex, abbattendo il consumo di token fino all'80% e riducendo drasticamente la latenza.

---

#### 4. Casi d'uso ad alto impatto per uno sviluppatore Java Backend
- **Generazione e arricchimento di Test (TDD & BDD)**:
  - Creazione di test unitari parametrici (`@ParameterizedTest` con JUnit 5) per coprire edge case limite (es. arrotondamenti finanziari, validazioni di stringhe ISO 8583/20022).
  - Scrittura rapida di test di integrazione con Mockito, `@MockBean` e `@DataJpaTest`.
- **Refactoring e modernizzazione codice legacy**:
  - Conversione di codice Java 8 imperativo in flussi Stream / Functional Programming.
  - Migrazione a nuove feature di linguaggio (Records, Pattern Matching su `switch`, `sealed` classes, Virtual Threads di Java 21).
  - Isolamento di classi monolitiche e introduzione di design pattern (Strategy, Factory, Adapter).
- **Scrittura e ottimizzazione di query complesse**:
  - Bozza di query SQL avanzate (Window Functions, Common Table Expressions - CTE) e conversione in JPQL o Spring Data Specifications.
- **Boilerplate e configurazioni**:
  - Scrittura di DTO, Mapper (MapStruct), configurazioni Spring Cloud / Kafka / Redis, schemi OpenAPI (Swagger) e script Docker / Kubernetes manifests.

---

#### 5. Rischi critici, Sicurezza e Regolamentazione (dominio Pagamenti / Bancario)
Questo è il tema chiave su cui un intervistatore valuterà la seniority: **l'uso sconsiderato dell'IA è pericoloso in contesti mission-critical**.

- **Privacy dei dati e conformità (PCI-DSS & GDPR)**:
  - **Zero PII / Zero Card Data**: mai condividere con modelli di IA esterni dati sensibili, PAN delle carte, token di autenticazione, password o secret di connessione DB.
  - Policy aziendali: utilizzo di modelli enterprise self-hosted o con garanzie contrattuali di non-training sui dati inseriti (es. Azure OpenAI con tenancy privata, AWS Bedrock, Copilot Enterprise).
- **Allucinazioni e falsi positivi**:
  - L'IA può inventare metodi inesistenti, API deprecate o implementare algoritmi crittografici non sicuri (es. uso improprio di `Math.random()` anziché `SecureRandom` per token di pagamento).
  - *Regola aurea*: "Non si committa mai codice generato dall'IA che non si sia compreso riga per riga e validato tramite test automatici".
- **Debito tecnico e "Vibe Coding"**:
  - Rischio di inserire codice apparentemente funzionante ma architetturalmente disallineato rispetto ai principi SOLID, pattern del team o convenzioni di isolamento transazionale (`@Transactional`).
- **Proprietà intellettuale e licenze**:
  - Attenzione alla generazione di codice soggetto a licenze restrittive (es. GPL) in progetti proprietari.

---

#### 6. Prompt Engineering & Context Management per Backend Developer
- **Fornire contesto esplicito**: passare sempre tipi, interfacce, vincoli di dominio ed esempi di input/output attesi invece di istruzioni generiche.
- **Approccio iterativo**: decomporre problemi architetturali complessi in step progressivi (Design interfaccia → Implementazione business logic → Validazioni → Test suite).
- **Inversione del controllo nel prompt**: chiedere all'IA di fare una code review, cercare falle di concorrenza/race conditions, o identificare potenziali memory leak ed eccezioni non gestite.

---

### Domande tipiche a colloquio (e come rispondere da Senior)

- *D: Come utilizzi l'Intelligenza Artificiale nel tuo lavoro quotidiano?*
  - **R**: La uso quotidianamente come moltiplicatore di produttività ("pair programmer virtuale"), sfruttando sia assistenti contestuali nell'IDE sia coding agent da terminale (come Claude Code o Cursor). Li guido con skill e workflow strutturati (es. regole TDD stile Matt Pocock o principi di minimalismo anti-bloat stile Ponytail) per velocizzare la scrittura di test unitari, generare boilerplate (DTO, script Flyway) ed esplorare refactoring, mantenendo sempre la revisione critica e test automatici su ogni riga.

- *D: Cos'è l'MCP (Model Context Protocol) e perché è rilevante?*
  - **R**: È uno standard aperto creato per normalizzare la connessione tra modelli LLM/agenti e sorgenti dati o tool esterni (database, repository Git, issue tracker, log di produzione). Invece di scrivere integrazioni ad-hoc per ogni strumento, un server MCP espone funzioni e risorse riutilizzabili da qualsiasi agent compatibile, rendendo l'ecosistema agentico modulare e sicuro.

- *D: Come eviti che un coding agent introduca over-engineering o codice superfluo?*
  - **R**: Utilizzo convenzioni esplicite e skill dedicate (come il pattern Ponytail) che forzano l'agente a seguire il principio YAGNI, a riutilizzare librerie e componenti già presenti nella codebase o nella Java standard library prima di creare nuove astrazioni o aggiungere dipendenze. Inoltre, definisco regole di progetto (`AGENTS.md` o `.cursorrules`) con vincoli chiari di architettura.

- *D: Quali sono i rischi dell'uso dell'IA in un'architettura bancaria / pagamenti elettronici?*
  - **R**: Il primo rischio è la **privacy e compliance**: dati di carte (PAN), PII e credenziali non devono mai transitare su LLM pubblici, per rispettare PCI-DSS e GDPR. Il secondo è l'**affidabilità transazionale**: in sistemi a forte consistenza ACID e con rigide regole di idempotenza, l'IA può generare codice che "sembra" corretto ma ha race conditions nascoste o gestione transazionale errata (`REQUIRES_NEW` improprio). Per questo il controllo umano e una solida suite di integration test restano insostituibili.

- *D: Se un'IA suggerisce una soluzione alternativa a un problema architetturale, come ti comporti?*
  - **R**: Valuto il suggerimento confrontandolo con i vincoli del sistema: carico atteso, throughput, scalabilità, manutenibilità da parte del team e consistenza con lo stack esistente. L'IA è eccellente per aprire ventagli di opzioni e trade-off (es. lock ottimistico vs pessimistico, code Kafka vs JMS), ma la decisione finale deve sempre basarsi sulla conoscenza profonda del contesto di business.

---

### Come esercitarti
1. **Spiegazione a voce (2 minuti)**: preparati un discorso chiaro in cui spieghi come l'IA e i coding agent ti rendono più rapido senza intaccare il tuo senso critico e la sicurezza del software.
2. **Esercizio pratico**: prendi una logica di calcolo commissioni o un parser ISO 8583 e chiedi a un assistente/agente IA di trovare potenziali bug di arrotondamento o casi limite non coperti; analizza criticamente i risultati.
