# 21. Git e Branching Strategies
## Il problema da cui partire
Git conserva una storia di snapshot e relazioni. Un branch è un riferimento che avanza con i commit, non una copia completa del progetto. La **working directory** contiene file modificabili; l'**index** prepara lo snapshot da registrare. Separarli permette di costruire commit che rappresentano una modifica coerente anche quando il lavoro locale è più ampio.
**HEAD** indica il punto attualmente estratto; in detached HEAD punta direttamente a un commit. Un **fast-forward** sposta un riferimento quando le storie non divergono; un merge può invece registrare più genitori. Un rebase ricostruisce commit sopra un'altra base, cambiandone l'identità.
La scelta del flusso deve sostenere frequenza di integrazione e rilascio. Un **commit atomico** contiene un cambiamento che si può capire e valutare come unità; non significa obbligatoriamente «un solo file». Conflitti e rollback richiedono di capire il comportamento, non soltanto di scegliere un comando.
#### 1. Architettura e Modello Interno di Git
**I 4 oggetti fondamentali** (memorizzati nel database a oggetti content-addressable `.git/objects` tramite hash SHA-1/SHA-256):

**Blob**: memorizza il contenuto puro dei file (senza metadati né nome file).

**Tree**: memorizza la struttura delle directory, associando i nomi dei file ai rispettivi hash dei blob o di altri sotto-alberi.

**Commit**: punta a un root tree e contiene metadati (autore, committer, timestamp, messaggio) e uno o più puntatori ai commit genitori (*parents*).

**Annotated Tag**: oggetto che può riferire un commit o altro oggetto, con metadati e firma opzionale. Il riferimento del tag può essere modificato: le policy devono controllarlo.

**I 3 stadi dell'albero di lavoro**: *Working Directory*: i file effettivi modificati su disco. *Staging Area (Index)*: snapshot preparato per il prossimo commit (`git add`). *Repository (`.git`)*: storico immutabile dei commit. *HEAD*: puntatore simbolico al branch attualmente estratto o a uno specifico commit (*detached HEAD*).
---
#### 2. Strategie di Branching Enterprise
```
[Trunk-Based]  ──●───●───●───●───●───●───► main (Deploy continui, feature flag)
                  \     /
                   ●───● (Short-lived branch, < 1-2 giorni)

[GitFlow]      main ──●────────────────────────● (Release tag v1.0.0)
                       \                      /
               develop ─●───●───●───●────────●
                             \     /
                              ●───● (feature/payment-routing)
```
**Trunk-Based Development (Standard moderno nei Microservizi)**: Tutti gli sviluppatori effettuano il merge su `main`/`master` frequentemente (almeno una volta al giorno) tramite branch a vita brevissima (*short-lived branches*). Previene "merge hell" e conflitti titanici. Richiede forte automazione CI/CD e l'uso di **Feature Flags** (Toggles) per disabilitare funzionalità incomplete in produzione.
**GitFlow (Tradizionale / Ambienti a rilascio cadenzato)**: `main`: codice sempre in produzione con tag di versione. `develop`: ramo di integrazione per il prossimo rilascio. `feature/*`: sviluppo nuove funzionalità, staccate da `develop`. `release/*`: stabilizzazione, bug fix minori e preparazione documentazione prima del merge su `main` e `develop`. `hotfix/*`: correzioni critiche urgenti staccate direttamente da `main` e reintegrate sia su `main` che su `develop`.
**GitHub Flow / GitLab Flow**: Più snelli di GitFlow: `main` protetto + feature branches + Pull/Merge Request con review obbligatoria e CI verde prima del merge.
---
#### 3. Comandi Avanzati e Operazioni Critiche
Un conflitto indica che Git non può integrare automaticamente alcune modifiche. I marcatori mostrano contenuti da confrontare, ma la soluzione può richiedere una terza versione che preservi entrambe le intenzioni. Dopo la risoluzione si verificano comportamento e contratto, non soltanto l'assenza dei marcatori.
Il **reflog** conserva localmente spostamenti dei riferimenti e può aiutare a ritrovare commit non più raggiunti da un branch. Non è un backup universale delle modifiche non committate. Revert preserva la storia aggiungendo un cambiamento inverso; il rollback del software rilasciato richiede ancora un processo di distribuzione.
##### A. Rebase vs Merge
**`git merge <branch>`**: integra le storie: può effettuare un fast-forward o creare un commit di merge, secondo divergenza e opzioni. Mantiene la cronologia fedele ma non lineare. **`git rebase <target>`**: "sposta" i commit correnti in cima al target, riscrivendo la storia dei commit (nuovi hash SHA). Crea una cronologia perfettamente lineare. **`git rebase -i HEAD~N` (Rebase interattivo)**: fondamentale prima di aprire una PR per fare *squash* (fondere commit temporanei "wip", "fix typo" in commit atomici e descrittivi), *reword* (modificare messaggi), o riordinare i commit.
**Regola d'oro del Rebase**: **mai fare rebase di commit già pubblicati su branch condivisi/pubblici** (es. `main` o `develop`), perché altera gli hash e crea divergenze nei riferimenti e richiede coordinamento con gli altri colleghi.
##### B. Reset vs Revert
**`git reset`** (modifica la storia locale, arretra il puntatore del branch): `--soft`: sposta `HEAD` indietro; lascia le modifiche nella Staging Area. `--mixed` (default): sposta `HEAD`; lascia le modifiche nella Working Directory (un-staged). `--hard`: distrugge tutte le modifiche sia in Staging che in Working Directory (pericoloso). **`git revert <commit_hash>`**: crea un **nuovo commit opposto** che annulla gli effetti del commit indicato. È il metodo abituale per annullare modifiche preservando la storia già pubblicata su un branch remoto condiviso.
##### C. Cherry-pick, Stash & Bisect
**`git cherry-pick <commit_hash>`**: applica un singolo specifico commit da un altro branch sul branch corrente (es. portare un bugfix urgente da una release successiva a una legacy). **`git stash` / `git stash pop`**: salva temporaneamente le modifiche non committate per liberare la working tree (utile quando bisogna cambiare branch d'urgenza per un hotfix). **`git bisect`**: algoritmo di ricerca binaria nello storico dei commit per individuare con precisione chirurgica quale commit ha introdotto una regressione o un bug (`git bisect start`, `git bisect bad`, `git bisect good <commit_vecchio>`).
---
#### 4. Best Practice, Conventional Commits e Sicurezza
**Conventional Commits**: convenzione per messaggi di commit leggibili e automazione del changelog: `feat(payment): add 3DS2 biometric authentication support` `fix(reconciliation): prevent duplicate transaction entry on retry` `refactor(core): extract currency conversion to dedicated service` `test(auth): add parameterized tests for expired token scenarios` **Sicurezza del Repository**: File `.gitignore` rigoroso: mai versionare file `.env`, file di configurazione con password in chiaro, certificati `.p12`/`.pem` o directory `.idea`/`target`.
**Git Pre-commit Hooks** (es. con Husky / Gitleaks): scansione automatica per bloccare il commit di segreti (token AWS, chiavi private, credenziali DB).
---
### Domande tipiche a colloquio (e risposte da Senior)
*D: Qual è la differenza tra `git rebase` e `git merge` e quando preferisci l'uno o l'altro?*
**R**: `git merge` unisce i rami preservando la cronologia esatta con un commit di merge, ma può rendere l'albero della storia disordinato. `git rebase` riscrive la storia applicando i propri commit sopra la punta del branch target, creando una cronologia lineare e pulita. La best practice consiste nell'utilizzare `rebase` sul proprio feature branch locale per allinearsi a `main` ed effettuare lo squash prima della PR, mentre si utilizza `merge` (o Squash & Merge) per integrare la PR nel branch principale.
*D: Hai pushato per errore un commit con un bug in produzione su `main`. Come intervieni?*
**R**: Eseguo immediatamente un `git revert <commit_hash>` e pusho il commit di rollback. Non uso mai `git reset --hard` con force push su `main`, perché riscriverebbe la storia di un branch pubblico condiviso, rompendo i repository dei colleghi e i runner di CI/CD.
*D: Cos'è il comando `git reflog` e quando ti ha salvato?*
**R**: Il `reflog` (reference log) tiene traccia di ogni singolo spostamento di `HEAD` sul computer locale, anche dopo operazioni distruttive come `git reset --hard` o eliminazione accidentale di branch. Permette di recuperare lo SHA di commit che sono diventati orfani ("dangling") prima che vengano ripuliti dal garbage collector di Git.
---
### Come esercitarti

1. **Esercizio di Rebase interattivo**: crea un branch di prova, fai 4 commit fittizi, poi usa `git rebase -i HEAD~4` per fondere i commit intermedi in uno solo (*squash*) e cambiare il messaggio del primo commit.

2. **Simulazione di Merge Conflict**: modifica la stessa riga di un file su due branch diversi, tenta il merge e risolvi il conflitto manualmente esaminando i marker `<<<<<<<`, `=======`, `>>>>>>>`.
