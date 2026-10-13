# 22. La toolchain: dal lavoro locale all'artefatto pubblicato

## Un percorso di lavoro ripetibile

La **toolchain** è l'insieme di strumenti che collega modifica, verifica e distribuzione. Conoscere i nomi non basta: serve capire quali informazioni passano tra gli strumenti e come ricostruire l'origine di un rilascio. Seguiamo una modifica al calcolo di una commissione.

## Sviluppare e registrare la modifica

Un **IDE**, Integrated Development Environment, come Eclipse integra navigazione, compilazione, refactoring e debugger. Un breakpoint ferma l'esecuzione per osservare stato e stack; il refactoring modifica una struttura mantenendo il comportamento previsto. Il workspace organizza i progetti, ma la build deve funzionare anche fuori dall'IDE per essere ripetibile in CI.

Git conserva revisioni e relazioni tra modifiche. Un **commit** registra una revisione; un **branch** offre una linea di lavoro; un merge integra storie. Il rebase ricostruisce commit sopra un'altra base e cambia la loro identità. Per risolvere un conflitto bisogna capire il comportamento desiderato da entrambe le modifiche, non soltanto eliminare i marcatori. Il capitolo 21 approfondisce questi flussi.

## Costruire e verificare

Maven legge il `pom.xml`, risolve librerie, compila ed esegue attività dei plugin. Lo scope delle dipendenze determina dove vengono usate: una libreria per test non dovrebbe diventare una dipendenza del runtime. Il lifecycle dà un ordine alle fasi, spiegato nei capitoli 20 e 50.

JUnit organizza verifiche automatiche. Un unit test controlla un comportamento circoscritto; un integration test verifica una collaborazione reale, per esempio con il database. Mockito consente di controllare alcune dipendenze in memoria, ma un mock non dimostra che il protocollo esterno funzioni.

## Automatizzare e distribuire

Jenkins esegue una **pipeline**, sequenza di attività verificabili. Uno **stage** raggruppa lavoro come build, test o pubblicazione. Il Jenkinsfile rende il percorso versionabile; forme dichiarative e scripted offrono modalità diverse per esprimerlo. Un **quality gate** impedisce di proseguire quando non sono soddisfatte condizioni stabilite.

Nexus è un **repository manager** per artefatti e dipendenze. Può ospitare librerie interne, fare proxy di repository esterni e conservare versioni distribuibili. Il repository del sorgente e quello degli artefatti hanno ruoli diversi: il primo registra il codice, il secondo ciò che la build ha prodotto.

## Ricostruire un rilascio

La modifica alla commissione entra in un commit, passa test e build, poi produce un JAR identificato da una versione. La pipeline lo pubblica e il processo di rilascio lo promuove tra ambienti. Deve essere possibile risalire dal JAR al commit e alle verifiche eseguite.

Come esercizio, spiega che cosa controlli se il codice funziona in Eclipse ma fallisce in Jenkins: versione del JDK, dipendenze, configurazione e comando di build sono ipotesi da confrontare con evidenze, non motivi per ignorare la CI.
