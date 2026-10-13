# 50. Maven e Gradle: costruire un artefatto riproducibile

## Dalla sorgente al rilascio

Un **build tool** coordina compilazione, test, packaging e risoluzione delle dipendenze. L'**artefatto** è il risultato distribuibile, per esempio un JAR. Una build affidabile deve rendere chiaro quali sorgenti, strumenti e librerie abbiano prodotto quel risultato.

Il capitolo 20 introduce le dipendenze; qui seguiamo il ciclo completo e le conseguenze operative. La **riproducibilità** richiede controllo degli input. Usare lo stesso comando non basta se dipendenze, JDK o configurazioni cambiano tra workstation e CI.

## Il modello di Maven

`pom.xml`, Project Object Model, descrive il progetto. Le **coordinate** `groupId`, `artifactId` e `version` identificano un artefatto. I repository lo rendono disponibile; i plugin eseguono attività come compilazione e test. I **profile** attivano configurazioni alternative, da usare senza rendere invisibili differenze fondamentali tra ambienti.

Il lifecycle principale comprende fasi ordinate. `validate` controlla il progetto, `compile` compila, `test` esegue i test associati, `package` produce il pacchetto e `verify` esegue le verifiche configurate. `install` copia l'artefatto nel repository locale; `deploy` lo pubblica in un repository remoto, non distribuisce automaticamente l'applicazione in produzione. Invocare una fase esegue anche quelle precedenti dello stesso lifecycle. `clean` appartiene a un lifecycle distinto.

```bash
mvn clean verify
mvn dependency:tree
mvn spring-boot:run
```

Il primo comando esegue una build con verifiche configurate, il secondo mostra le dipendenze e il terzo invoca un goal del plugin Spring Boot. I test di integrazione vanno collegati correttamente alle fasi: il nome `verify` non garantisce da solo che esistano.

## Dipendenze, scope e conflitti

Una dipendenza **diretta** è dichiarata dal progetto; una **transitiva** è richiesta da una sua libreria. Gli **scope** ne determinano l'uso: `test` riguarda i test, `provided` presuppone disponibilità nell'ambiente di esecuzione, `runtime` serve in esecuzione senza essere necessario alla compilazione. Il classpath effettivo va verificato rispetto al packaging scelto.

`dependencies` introduce le dipendenze; `dependencyManagement` centralizza versioni e altre impostazioni senza aggiungere da solo ogni libreria. Un **BOM**, Bill of Materials, è un POM che permette di importare un insieme coordinato di versioni. Aiuta la coerenza, ma non dimostra la compatibilità di ogni combinazione applicativa.

Un conflitto può far selezionare una versione diversa da quella attesa e provocare errori come `NoSuchMethodError`. L'albero delle dipendenze consente di vedere da dove arriva la libreria. Prima di escluderla o forzarne la versione si verificano compatibilità, test e vulnerabilità, comprese quelle transitive.

## Il modello di Gradle

`build.gradle` o `build.gradle.kts` descrive la build con una DSL Groovy o Kotlin. I plugin aggiungono capacità; i **task** rappresentano il lavoro e le loro dipendenze formano un grafo. Le **configuration** organizzano gruppi di dipendenze, come quelle necessarie alla compilazione o ai test.

```bash
./gradlew clean test
./gradlew build
./gradlew dependencies
```

Il **Gradle Wrapper** avvia la versione prevista dal progetto. Le build incrementali possono evitare task i cui input e output non sono cambiati; la cache può riutilizzare risultati compatibili. Per funzionare correttamente, i task devono dichiarare input, output e condizioni rilevanti. Più programmabilità richiede disciplina per mantenere la build comprensibile.

## Moduli, strumenti e pipeline

Un progetto multi-modulo può separare dominio, applicazione, infrastruttura e API. Le dipendenze devono rispettare i confini ed evitare cicli. Il parent Maven e i progetti Gradle coordinano la costruzione, ma un modulo di build non diventa automaticamente un componente distribuibile indipendente.

Maven offre convenzioni e un lifecycle strutturato; Gradle offre un modello a task più programmabile. La scelta considera convenzioni del team e complessità reale. Maven Wrapper e Gradle Wrapper fissano lo strumento; versioni dichiarate, JDK controllato e repository affidabili stabilizzano gli altri input.

In CI si acquisisce una revisione precisa, si eseguono build, test, analisi statica e controlli delle dipendenze, poi si pubblica un artefatto identificabile. La promozione tra ambienti dovrebbe usare quel medesimo artefatto. Configurazione e segreti vengono forniti separatamente, così il risultato verificato resta collegato al risultato rilasciato.

## Un esercizio operativo

Scegli un conflitto di dipendenze e ricostruisci il percorso che lo introduce. Correggilo motivando la versione selezionata, esegui le verifiche necessarie e confronta la build locale con quella di CI. Spiega infine la differenza tra pubblicare un JAR con `deploy` e rilasciare un servizio agli utenti.
