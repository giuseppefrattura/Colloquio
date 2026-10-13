# 25. CI-CD e Release Management (Jenkins, GitLab CI, Nexus)
## Il problema da cui partire
La **Continuous Integration**, CI, integra modifiche frequentemente con verifiche automatiche. La **Continuous Delivery** mantiene il software pronto per un rilascio controllato; la **Continuous Deployment** automatizza anche la pubblicazione in produzione secondo il processo stabilito. Nessuna delle tre coincide soltanto con la presenza di un file di pipeline.
Una pipeline collega una revisione a test, artefatto e destinazione. Uno **stage** raccoglie un gruppo di attività; un **runner** o agent le esegue nell'ambiente previsto. Il repository degli artefatti conserva ciò che è stato costruito, mentre il registry distribuisce immagini container. Una versione o un digest permette di identificare il risultato promosso.
Il **release management** coordina rischio, compatibilità e recupero. Lo smoke test verifica funzioni essenziali dopo un passaggio; il rollback del codice non annulla ogni modifica ai dati. Per questo gli esempi di deployment vanno letti insieme al capitolo 5 sulle migrazioni.
#### 1. I Concetti Fondamentali: CI vs CD
```
┌─────────────────────────────────────────────────────────────┐
│                    CONTINUOUS INTEGRATION (CI)              │
│  [Code / Git] ──► [Build] ──► [Unit Test] ──► [SAST / Sonar]│
└──────────────────────────────┬──────────────────────────────┘
                               │ (Artifact generato: JAR/Image)
┌──────────────────────────────▼──────────────────────────────┐
│                    CONTINUOUS DELIVERY (CD)                 │
│  [Integration Test] ──► [Nexus/Registry] ──► [Deploy Staging]
└──────────────────────────────┬──────────────────────────────┘
                               │ (Approvazione Manuale / Gate)
┌──────────────────────────────▼──────────────────────────────┐
│                    CONTINUOUS DEPLOYMENT (CD)               │
│  [Deploy Produzione Automatico] ──► [Health Check / Canary] │
└─────────────────────────────────────────────────────────────┘
```
**Continuous Integration (CI)**: gli sviluppatori integrano il codice su un branch condiviso frequentemente. Ad ogni push o Pull Request, un server CI compila automaticamente l'applicazione, esegue tutti i test unitari e avvia l'analisi statica (SonarQube/SAST). Obiettivo: scoprire i bug immediatamente (*Fail Fast*).
**Continuous Delivery (CD)**: ogni build che supera la CI viene automaticamente pacchettizzata come artefatto versionato (JAR in Nexus, immagine in Container Registry) e rilasciata negli ambienti di Staging/UAT, pronta per essere promossa in produzione con un clic (*Manual Gate*). **Continuous Deployment**: evoluzione della Continuous Delivery in cui la promozione in produzione avviene in modo **100% automatizzato** se tutti i test e i controlli superano i Quality Gate stabiliti.
---
#### 2. Pipeline as Code: Jenkins vs GitLab CI vs GitHub Actions
##### A. Jenkins Pipeline (Dichiarativa in `Jenkinsfile`)
Standard tradizionale in molte banche e grandi enterprise:
```groovy
pipeline {
    agent {
        docker {
            image 'eclipse-temurin:21-jdk-alpine'
        }
    }
    environment {
        NEXUS_CREDENTIALS = credentials('nexus-auth')
        SONAR_TOKEN = credentials('sonar-token')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build & Test') {
            steps {
                sh './mvnw clean verify'
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                    jacoco execFile: '**/target/jacoco.exec'
                }
            }
        }
        stage('SAST Quality Gate') {
            steps {
                withSonarQubeEnv('Internal-Sonar') {
                    sh './mvnw sonar:sonar -Dsonar.qualitygate.wait=true'
                }
            }
        }
        stage('Publish Artifact') {
            steps {
                sh './mvnw deploy -DskipTests'
            }
        }
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh 'kubectl apply -f k8s/staging/ -n payment-staging'
            }
        }
    }
}
```
##### B. GitLab CI (`.gitlab-ci.yml`)
Standard moderno basato su file YAML, container runner dedicati e registry integrato:
```yaml
stages:
  - build_test
  - quality
  - package
  - deploy

build_and_test:
  stage: build_test
  image: maven:3.9-eclipse-temurin-21
  script:
    - mvn clean verify
  artifacts:
    reports:
      junit: target/surefire-reports/*.xml

sonarqube_check:
  stage: quality
  image: sonarsource/sonar-scanner-cli:latest
  script:
    - sonar-scanner -Dsonar.qualitygate.wait=true
  only:
    - merge_requests
    - main

docker_build_push:
  stage: package
  image: docker:24-cli
  services:
    - docker:24-dind
  script:
    - docker login -u $REGISTRY_USER -p $REGISTRY_PASSWORD $REGISTRY_URL
    - docker build -t $REGISTRY_URL/payment-service:$CI_COMMIT_SHORT_SHA .
    - docker push $REGISTRY_URL/payment-service:$CI_COMMIT_SHORT_SHA
```
---
#### 3. Repository Management con Sonatype Nexus / JFrog Artifactory
**A cosa serve un Repository Manager aziendale**:

**Proxy & Cache**: memorizza localmente le dipendenze scaricate da Maven Central / Docker Hub, velocizzando le build e proteggendo l'azienda da downtime di rete esterni.

**Hosted Repositories**: archivia gli artefatti privati aziendali (JAR delle librerie core, starter interni, DTO condivisi) suddivisi tra:

`releases`: artefatti immutabili definitivi (es. `1.0.0`). Non possono mai essere sovrascritti. `snapshots`: versioni di sviluppo modificabili (es. `1.0.1-SNAPSHOT`).

**Container Registry**: funge da registro Docker privato per le immagini dei microservizi prima del deploy in Kubernetes/OpenShift.

---
#### 4. Strategie di Deployment a Zero-Downtime
Le strategie seguenti riducono il rischio, ma il downtime dipende anche da readiness, capacità, connessioni e compatibilità dei dati. Due versioni devono poter convivere sul contratto e sullo schema. Lo spostamento di traffico non annulla un evento già pubblicato né recupera una colonna eliminata: il piano di rollback deve dichiarare questi confini. In un sistema di pagamento attivo 24/7 non sono ammesse finestre di manutenzione con downtime del servizio:
```
[Rolling Update]       Pod v1 ──► Pod v2 (Aggiornamento incrementale 1 ad 1)

[Blue/Green]           Traffic Router (Load Balancer)
                               │
                       ┌───────┴───────┐
                       ▼               ▼
                  [Blue: v1]      [Green: v2] (Testato e promosso al 100%)
                   (Attivo)        (Inattivo)

[Canary Deployment]    Traffic Router ──► 95% al Pod v1 (Produzione stabile)
                                      └─►  5% al Pod v2 (Nuova release monitorata)
```

**Rolling Update (Default Kubernetes)**:

Sostituisce progressivamente i pod secondo capacità e strategia configurate. Non richiede il doppio dell'infrastruttura, ma durante il roll-out convivono due versioni diverse (richiede retrocompatibilità sul DB).

**Blue/Green Deployment**:

Vengono mantenuti due ambienti identici: *Blue* (versione corrente in produzione) e *Green* (nuova versione). Quando la versione *Green* supera tutti i test di fumo, il Load Balancer (o Ingress) commuta istantaneamente il 100% del traffico su *Green*. *Rollback del traffico*: si può reindirizzare verso Blue, verificando connessioni, compatibilità e modifiche dei dati. Non equivale ad annullare tutti gli effetti della nuova versione.

**Canary Deployment**:

La nuova versione viene rilasciata a una piccola percentuale di traffico reale (es. 2% degli utenti). Se le metriche di errore (Prometheus/Grafana) e i log di business restano nominali, la percentuale viene incrementata gradualmente fino al 100%.
---
#### 5. GitOps e Deployment Dichiarativo (ArgoCD / Flux)
L'intero stato desiderato dell'infrastruttura e dei microservizi Kubernetes è descritto dichiarativamente in un repository Git dedicato (*Infrastructure as Code*). Un controller in Kubernetes (**ArgoCD**) monitora il repository Git: quando un nuovo commit approva una nuova versione dell'immagine, ArgoCD sincronizza automaticamente lo stato del cluster (*Auto-Sync*).
---
### Domande tipiche a colloquio (e risposte da Senior)
*D: Qual è la differenza tra Continuous Delivery e Continuous Deployment?*
**R**: In entrambi i casi il codice supera l'intera pipeline di CI (build, test, analisi di sicurezza) e viene rilasciato automaticamente in un ambiente di staging. Nella **Continuous Delivery** il passaggio finale in produzione richiede un'approvazione umana esplicita (click su un pulsante o approvazione formale di release). Nel **Continuous Deployment** l'intero flusso è 100% automatico e ogni commit che supera i test atterra direttamente in produzione senza alcun intervento umano.
*D: Come gestisci un rilascio Blue/Green se la nuova versione include modifiche allo schema del database?*
**R**: Applicando il pattern **Expand and Contract (Parallel Run)**: le modifiche al database devono essere sempre retrocompatibili. Nel primo step (*Expand*) si aggiungono nuove colonne o tabelle senza eliminare quelle vecchie, garantendo che sia la versione *Blue* che la *Green* possano funzionare simultaneamente. Solo dopo che la versione *Green* è promossa definitivamente e la vecchia versione viene dismessa, una successiva migrazione DB (*Contract*) rimuove le colonne deprecate.
---
### Come esercitarti

1. **Pipeline Scripting**: scrivi un file `Jenkinsfile` o `.gitlab-ci.yml` che esegue `mvn clean verify`, invoca l'analisi SonarQube con stop on quality gate failure, compila l'immagine Docker con hash del commit e notifica l'esito su Slack/Teams.
