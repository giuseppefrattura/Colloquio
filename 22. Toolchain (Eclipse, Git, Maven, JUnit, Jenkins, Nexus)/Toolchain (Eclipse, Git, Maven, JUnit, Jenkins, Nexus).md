# 22. Toolchain (Eclipse, Git, Maven, JUnit, Jenkins, Nexus)

### Cos'è e perché conta
Meno peso tecnico ma segnala autonomia operativa — in un contesto enterprise regolamentato, il processo di rilascio è spesso rigido e vogliono sapere che ti inserisci senza frizioni.

### Cosa studiare

- **Eclipse IDE**: se lavori principalmente con IntelliJ, rinfresca le scorciatoie base (refactor, debug, gestione workspace/progetti Maven) — non serve diventare esperto, basta non essere spiazzato
- **Git**: flussi di branching enterprise (Git Flow o simili), rebase vs merge, gestione conflitti — spesso chiedono "come gestisci un conflitto di merge" più che comandi esotici
- **Maven**: struttura di un `pom.xml`, gestione dipendenze e scope (`compile`, `test`, `provided`), lifecycle (`validate`, `compile`, `test`, `package`, `install`, `deploy`)
- **JUnit**: differenza tra unit test e integration test, uso di Mockito per il mocking, test parametrizzati (già nel tuo bagaglio recente)
- **Jenkins**: concetto di pipeline (dichiarativa vs scripted), stage tipici (build, test, quality gate, deploy) — non serve saperci scrivere una pipeline complessa, ma capire cosa fa un job CI/CD
- **Nexus**: repository manager per artifact Maven/npm — sapere a cosa serve (versioning, cache di dipendenze, distribuzione interna di librerie)

### Come esercitarti
Se non hai mai usato Jenkins/Nexus in prima persona, guarda un video introduttivo di 10 minuti su ciascuno: l'obiettivo è poter dire "ho capito il concetto anche se non l'ho usato quotidianamente", che è una risposta onesta e accettabile.
