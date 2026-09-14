# 26. Sicurezza e Qualità del Software (i "plus")

### Cos'è e perché conta
Sono competenze plus, quindi non decisive, ma menzionarle bene ti differenzia dagli altri candidati con solo skill tecniche pure.

### Cosa studiare

**Secure coding**
- OWASP Top 10 a grandi linee: injection (SQL injection soprattutto, vista la centralità di Oracle), broken authentication, exposure di dati sensibili
- Gestione segreti: perché non si mettono credenziali/chiavi in chiaro nel codice, uso di vault/secret manager (anche solo a livello concettuale)

**Tokenizzazione**
- Concetto chiave: sostituire un dato sensibile (es. numero carta/PAN) con un token senza valore fuori dal sistema che lo ha generato, così se il token viene intercettato è inutile
- Differenza tra tokenizzazione e cifratura (la tokenizzazione non è reversibile matematicamente, richiede una tabella di mapping protetta)

**Test automation**
- Piramide dei test: unit (tanti, veloci) → integration (meno, più lenti) → end-to-end (pochi, costosi)
- Mockito per isolare le unità sotto test dai servizi esterni (banche, circuiti) — rilevante perché in ambito pagamenti non puoi testare contro sistemi bancari reali in ogni build

### Come esercitarti
Prepara un esempio concreto (anche dal tuo lavoro recente con Jackson/SOAP-to-JSON o dal progetto di riconciliazione) in cui hai scritto test che isolano una dipendenza esterna — è il tipo di aneddoto che rende credibile questa sezione.
