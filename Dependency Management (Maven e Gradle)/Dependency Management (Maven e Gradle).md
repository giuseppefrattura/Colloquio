## Dependency Management (Maven e Gradle)

### Cos'è e perché conta
La gestione delle dipendenze, del ciclo di vita di compilazione e della risoluzione dei conflitti tra librerie (Jar Hell) è fondamentale in progetti enterprise complessi e multi-modulo. Sapere come Maven e Gradle risolvono i grafi delle dipendenze, come gestire i BOM (Bill of Materials) e come isolare gli scope è una competenza chiave per un Senior Developer.

---

### Cosa studiare

#### 1. Apache Maven: Fondamenti e Architettura

##### A. Il Modello a Coordinate (GAV)
Ogni artefatto Maven è identificato univocamente da una terna **GAV**:
- `groupId`: package namespace univoco dell'organizzazione (es. `org.springframework.boot`, `com.nexi.payments`).
- `artifactId`: nome del modulo/progetto (es. `payment-core`, `spring-boot-starter-web`).
- `version`: versione semantica (es. `3.2.4`, `1.0.0-SNAPSHOT`).

##### B. Il Build Lifecycle di Maven
Maven definisce tre cicli di vita standard: `default` (compilazione e rilascio), `clean` (pulizia della directory `target`) e `site` (generazione documentazione).

Fasi ordinate del ciclo **`default`**:
1. `validate`: convalida la correttezza del `pom.xml` e la disponibilità di tutte le informazioni.
2. `compile`: compila il codice sorgente in `src/main/java` dentro `target/classes`.
3. `test`: esegue i test unitari (Surefire plugin) in `src/test/java` senza fare il package.
4. `package`: impacchetta il codice compilato nel formato di distribuzione (`jar`, `war`) in `target/`.
5. `verify`: esegue i test di integrazione (Failsafe plugin) e controlli di qualità/SAST.
6. `install`: copia l'artefatto nel repository Maven locale (`~/.m2/repository`).
7. `deploy`: invia l'artefatto definitivo al repository manager remoto aziendale (Nexus / Artifactory).

##### C. Gli Scope delle Dipendenze Maven
- **`compile`** (default): disponibile in compilazione, test e runtime; viene inclusa nel pacchetto finale (JAR) e propagata ai progetti a valle.
- **`provided`**: necessaria per compilare e testare, ma non inclusa nel pacchetto finale perché fornita dal container a runtime (es. `jakarta.servlet-api`, `lombok`).
- **`runtime`**: necessaria solo per l'esecuzione, non per la compilazione (es. driver JDBC `com.oracle.database.jdbc:ojdbc8`).
- **`test`**: necessaria solo per compilare ed eseguire i test (es. `junit-jupiter`, `mockito-core`, `testcontainers`). Non viene inclusa nel JAR finale.
- **`import`**: utilizzabile solo all'interno di `<dependencyManagement>` con tipo `pom`, per importare un BOM (Bill of Materials).

##### D. Transitive Dependencies e Risoluzione dei Conflitti
Quando il progetto dipende da `Lib A` che a sua volta dipende da `Lib C:1.0`, e da `Lib B` che dipende da `Lib C:2.0`:
- **Regola di Maven "Nearest Definition" (Più vicino nell'albero)**: Maven sceglie la versione della dipendenza che si trova al livello di profondità minore nell'albero delle dipendenze. Se sono alla stessa profondità, vince la prima dichiarata nel `pom.xml`.
- **Esclusioni esplicite**:
  ```xml
  <dependency>
      <groupId>com.example</groupId>
      <artifactId>legacy-service</artifactId>
      <version>1.0.0</version>
      <exclusions>
          <exclusion>
              <groupId>commons-logging</groupId>
              <artifactId>commons-logging</artifactId>
          </exclusion>
      </exclusions>
  </dependency>
  ```
- **Analisi dell'albero delle dipendenze**:
  ```bash
  mvn dependency:tree -Dverbose -Dincludes=commons-logging
  ```

##### E. `<dependencyManagement>` vs `<dependencies>` e i BOM (Bill of Materials)
- `<dependencies>`: dichiara e scarica effettivamente le dipendenze nel modulo corrente.
- `<dependencyManagement>`: definisce centralmente le **versioni** e le configurazioni delle librerie per tutti i moduli figli, senza forzarne l'inclusione finché un sottomodulo non la dichiara in `<dependencies>` (senza specificare il tag `<version>`).
- **BOM di Spring Boot o Spring Cloud**:
  ```xml
  <dependencyManagement>
      <dependencies>
          <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-dependencies</artifactId>
              <version>3.2.4</version>
              <type>pom</type>
              <scope>import</scope>
          </dependency>
      </dependencies>
  </dependencyManagement>
  ```

---

#### 2. Gradle: Caratteristiche e Confronto con Maven

- **Modello Basato su DAG (Directed Acyclic Graph)**:
  - Anziché un ciclo di vita rigido a fasi fisse come Maven, Gradle modella la build come un grafo orientato aciclico di **Tasks** con dipendenze esplicite (`dependsOn`).
- **Linguaggio di Build**: basato su Kotlin DSL (`build.gradle.kts`) o Groovy DSL (`build.gradle`), offrendo piena programmabilità.
- **Configurazioni delle Dipendenze in Gradle**:
  - `implementation`: la dipendenza è interna al modulo e non viene esposta ai moduli che dipendono da esso (migliora drasticamente i tempi di ricompilazione incrementale).
  - `api`: la dipendenza viene esportata ai consumatori del modulo.
  - `compileOnly`: analogo a `provided` di Maven.
  - `runtimeOnly`: analogo a `runtime` di Maven.
  - `testImplementation`: analogo a `test` di Maven.
- **Performance e Caching**:
  - **Build Daemon**: processo in background sempre attivo per evitare il cold start della JVM.
  - **Incremental Builds**: esegue solo i task i cui input/output sono cambiati (`UP-TO-DATE`).
  - **Build Cache**: condivisione dei binari compilati tra sviluppatori e pipeline CI/CD.

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Come risolvi un conflitto di versioni transitivo in Maven (Jar Hell)?*
  - **R**: Eseguo il comando `mvn dependency:tree -Dverbose` per individuare quale dipendenza sta portando la versione obsoleta o in conflitto. Per risolverlo in modo pulito posso: (1) dichiarare esplicitamente la versione corretta all'interno del blocco `<dependencyManagement>`, oppure (2) aggiungere un tag `<exclusion>` nella dipendenza che trascina la versione indesiderata.

- *D: Qual è la differenza tra `implementation` e `api` in Gradle?*
  - **R**: `implementation` nasconde le dipendenze transitive ai moduli a valle, evitando di "inquinare" il loro classpath di compilazione. Questo significa che se cambio un'implementazione interna in un modulo, Gradle non deve ricompilare tutti i progetti che dipendono da esso, riducendo sensibilmente i tempi di build. `api` espone invece la dipendenza pubblicamente.

- *D: A cosa serve il file `mvnw` (Maven Wrapper) / `gradlew` (Gradle Wrapper) presente nei repository?*
  - **R**: Il Wrapper è uno script shell che scarica e utilizza automaticamente la versione esatta di Maven/Gradle specificata nel progetto (`.mvn/wrapper/maven-wrapper.properties`). Garantisce che tutti gli sviluppatori del team e i server di CI/CD compilino il software esattamente con la stessa identica versione del build tool, eliminando il problema "funziona sulla mia macchina".

---

### Come esercitarti
1. **Analisi dipendenze**: crea un `pom.xml` con Spring Boot e aggiungi due librerie con versioni discordanti di Jackson; usa `mvn dependency:tree` per verificare quale versione viene selezionata e forza la versione corretta con `<dependencyManagement>`.
