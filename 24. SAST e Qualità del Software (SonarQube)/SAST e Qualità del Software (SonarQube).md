# 24. SAST e Qualità del Software (SonarQube)

### Cos'è e perché conta
In ambienti finanziari e di pagamento soggetti a regolamentazioni stringenti (PCI-DSS, PSD2, standard bancari ISO 27001), la qualità del codice e la sicurezza applicativa non sono opzionali. Il **SAST (Static Application Security Testing)** con strumenti come **SonarQube** permette di individuare bug, vulnerabilità di sicurezza, falle crittografiche e debito tecnico automaticamente all'interno delle pipeline di CI/CD, prima ancora che il codice arrivi in ambiente di test.

---

### Cosa studiare

#### 1. Tipologie di Security Testing: SAST vs DAST vs IAST vs SCA

| Metodologia | Definizione | Modalità | Quando si esegue | Cosa trova |
|---|---|---|---|---|
| **SAST** (SonarQube, Checkmarx) | Static Application Security Testing | White-box (analizza il codice sorgente/bytecode senza eseguirlo) | In fase di Build / CI (Pull Request) | SQL Injection, hardcoded secrets, NPE, cattiva crittografia, violazioni di stile |
| **SCA** (OWASP Dependency-Check, Snyk, Dependabot) | Software Composition Analysis | Analizza le librerie terze nel `pom.xml` / `build.gradle` | In fase di Build / CI | CVE note in dipendenze esterne (es. vulnerabilità in Spring, Log4j, Jackson) |
| **DAST** (OWASP ZAP, Burp Suite) | Dynamic Application Security Testing | Black-box (analizza l'applicazione in esecuzione dall'esterno) | In ambienti Staging / QA | XSS a runtime, misconfigurazioni TLS/SSL, header HTTP insicuri, broken auth |
| **IAST** | Interactive Application Security Testing | Gray-box (agente interno all'app durante test funzionali) | In esecuzione durante integration test | Combinazione di vulnerabilità interne e comportamenti runtime |

---

#### 2. Concetti Chiave di SonarQube

```
┌────────────────────────────────────────────────────────────────────────┐
│                          SONARQUBE ANALYSIS                            │
├────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────────┐  ┌────────────────────┐  │
│  │       BUGS        │  │  VULNERABILITIES  │  │    CODE SMELLS     │  │
│  │ (Errori logici e  │  │ (Falle di sicu-   │  │ (Debito tecnico e  │  │
│  │  rischi runtime)  │  │  rezza sfruttabili│  │  scarsa manutenib.)│  │
│  └───────────────────┘  └───────────────────┘  └────────────────────┘  │
│  ┌───────────────────┐  ┌───────────────────┐  ┌────────────────────┐  │
│  │ SECURITY HOTSPOTS │  │   CODE COVERAGE   │  │   DUPLICATIONS     │  │
│  │ (Codice critico   │  │ (Percentuale test │  │ (Codice duplicato  │  │
│  │  da revisionare)  │  │  unitari / JaCoCo)│  │  copia-incolla)    │  │
│  └───────────────────┘  └───────────────────┘  └────────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │    QUALITY GATE     │
                         │   [PASSED / FAILED] │ ──► Blocca la Pipeline CI
                         └─────────────────────┘
```

##### A. Le Categorie di Issues in SonarQube
1. **Bugs**: codice errato o che causerà sicuramente anomalie a runtime (es. `NullPointerException`, risorse non chiuse/leak di connessioni DB, race conditions).
2. **Vulnerabilities**: falle di sicurezza concrete che espongono il sistema ad attacchi (es. concatenazione SQL non parametrizzata, log di dati sensibili/PAN in chiaro, uso di cifrari deboli come DES o MD5).
3. **Security Hotspots**: punti di codice che toccano aree sensibili dal punto di vista della sicurezza (es. configurazione CORS permissiva, generazione di numeri casuali, hashing di password), che richiedono una **revisione umana esplicita** per verificare che il contesto sia sicuro.
4. **Code Smells**: problemi di manutenibilità, leggibilità e debito tecnico (es. metodi troppo lunghi, classi con troppe responsabilità, complessità ciclomatica elevata, parametri non utilizzati).

##### B. Metriche Fondamentali
- **Complessità Ciclomatica (Cyclomatic Complexity)**: misura il numero di cammini linearmente indipendenti nel codice (calcolata in base a `if`, `for`, `while`, `case`, operatori logici `&&`, `||`). Un valore alto indica codice difficile da testare e manutenere.
- **Complessità Cognitiva (Cognitive Complexity)**: misura quanto sia difficile per un essere umano comprendere il flusso del codice (penalizza maggiormente i cicli o blocchi annidati).
- **Code Coverage (con JaCoCo)**: percentuale di linee e branch coperti dai test unitari e di integrazione. In genere il Quality Gate impone almeno l'80% di coverage sul **nuovo codice** (*Clean as You Go*).
- **Duplicated Lines Density**: percentuale di righe di codice duplicate che dovrebbero essere refattorizzate.

##### C. Il Quality Gate (Cancello di Qualità)
È un insieme di condizioni booleane che il codice deve superare per essere considerato idoneo al rilascio o al merge della Pull Request.
- **Politica "Clean as You Go"**: focalizzarsi sul codice modificato/aggiunto nella PR (*New Code*), bloccando la build se:
  - 0 Nuove Vulnerability
  - 0 Nuovi Bug
  - Security Rating = `A` (nessuna vulnerabilità aperta)
  - Code Coverage sul nuovo codice $\ge 80\%$
  - Duplicazioni sul nuovo codice $< 3\%$
  - 100% dei Security Hotspots revisionati

---

#### 3. OWASP Top 10 e Regole Critiche SonarQube per Java Backend

- **Injection (A03:2021)**:
  - *Problema*: concatenare stringhe in query SQL/JPQL (`"SELECT * FROM accounts WHERE id = " + inputId`).
  - *Regola Sonar*: S2077 / S3649 (uso obbligatorio di `PreparedStatement` o parameterized queries in Spring Data `@Param`).
- **Cryptographic Failures (A02:2021)**:
  - *Problema*: uso di MD5/SHA-1 per hashing o `DES`/`AES/ECB` per cifratura dati carta.
  - *Regola Sonar*: S4790 (uso obbligatorio di algoritmi robusti: `AES/GCM/NoPadding`, `BCrypt`/`Argon2` per password).
- **Insecure Randomness**:
  - *Problema*: uso di `java.util.Random` o `Math.random()` per token di autenticazione o codici OTP.
  - *Regola Sonar*: S2245 (uso obbligatorio di `java.security.SecureRandom`).
- **Sensitive Data Exposure / Logging**:
  - *Problema*: stampare nei log tramite Logback/Log4j2 oggetti contenenti PAN di carte di credito o CVV.
  - *Regola*: mascheramento dati (pattern masking nei log: `4111-XXXX-XXXX-1111`) e annotazioni custom `@ToString.Exclude` o record con `toString()` oscurato.
- **Resource Leaks**:
  - *Problema*: mancata chiusura di connessioni `Connection`, `ResultSet`, `InputStream`.
  - *Regola*: uso obbligatorio del `try-with-resources` (Java 7+).

---

#### 4. Integrazione di SonarQube nella Pipeline CI/CD

Nel file di build (`pom.xml`) tramite il plugin Sonar Maven:

```xml
<plugin>
    <groupId>org.sonarsource.scanner.maven</groupId>
    <artifactId>sonar-maven-plugin</artifactId>
    <version>3.10.0.2594</version>
</plugin>
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
                <goal>report</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

Comando di esecuzione in pipeline Jenkins / GitLab CI:
```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=payment-service \
  -Dsonar.host.url=https://sonarqube.internal.bank \
  -Dsonar.token=$SONAR_TOKEN \
  -Dsonar.qualitygate.wait=true
```
*(Il flag `-Dsonar.qualitygate.wait=true` fa attendere a Maven l'esito dell'analisi; se il Quality Gate fallisce, la pipeline si interrompe immediatamente bloccando il merge).*

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Come utilizzi SonarQube nel tuo flusso di lavoro quotidiano?*
  - **R**: Utilizzo il plugin **SonarLint** direttamente nell'IDE per ricevere feedback istantaneo mentre scrivo codice (*shift-left testing*), prevenendo code smell e falle prima del commit. Nella pipeline CI/CD di GitLab/Jenkins, ad ogni Pull Request viene eseguita l'analisi con SonarScanner e generato il report di copertura JaCoCo; la PR non può essere approvata né unita al branch principale se il Quality Gate fallisce.

- *D: Che differenza c'è tra una Vulnerability e un Security Hotspot in SonarQube?*
  - **R**: Una **Vulnerability** è una falla di sicurezza accertata nel codice che va corretta immediatamente (es. una SQL injection o una risorsa non chiusa). Un **Security Hotspot** evidenzia codice che fa uso di funzioni sensibili per la sicurezza (es. generazione di numeri random, upload di file, cookie HTTP) la cui pericolosità dipende dal contesto architetturale: richiede che uno sviluppatore o security champion analizzi il codice e lo marchi esplicitamente come "Safe" o lo converta in bug/fix.

- *D: Come convinci un team a rispettare la metrica del Quality Gate senza rallentare le consegne?*
  - **R**: Adottando la strategia **Clean as You Go**: non si blocca il team per sanare migliaia di righe di debito tecnico legacy pregresso, ma si impone il Quality Gate rigido esclusivamente sul **nuovo codice o codice modificato nella PR** (nuove righe con 0 vulnerabilità e coverage $\ge 80\%$). In questo modo la qualità complessiva della codebase migliora gradualmente a ogni rilascio senza arrestare il business.

---

### Come esercitarti
1. **Analisi di vulnerabilità**: scrivi un metodo Java con un'evidente falla di concatenazione SQL e un uso improprio di `Math.random()`, poi rifattorizzalo applicando `PreparedStatement` e `SecureRandom` per renderlo conforme alle regole Sonar.
2. **Configurazione JaCoCo**: verifica come impostare nel `pom.xml` una regola di esclusione per DTO, Record e classi di configurazione Spring in modo che non falsino le percentuali di Code Coverage complessive.
