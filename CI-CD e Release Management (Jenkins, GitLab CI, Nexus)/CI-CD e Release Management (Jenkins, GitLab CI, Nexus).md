## CI-CD e Release Management (Jenkins, GitLab CI, Nexus)

### Cos'è e perché conta
In ambienti ad alta affidabilità come i pagamenti digitali, il processo che porta il codice dal repository Git alla produzione deve essere completamente automatizzato, ripetibile e tracciabile. Il paradigma **CI/CD (Continuous Integration / Continuous Delivery & Deployment)** azzera l'errore umano, garantisce che ogni commit superi controlli di qualità e test automatici, e permette rilasci frequenti e a zero downtime.

---

### Cosa studiare

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

- **Continuous Integration (CI)**: gli sviluppatori integrano il codice su un branch condiviso frequentemente. Ad ogni push o Pull Request, un server CI compila automaticamente l'applicazione, esegue tutti i test unitari e avvia l'analisi statica (SonarQube/SAST). Obiettivo: scoprire i bug immediatamente (*Fail Fast*).
- **Continuous Delivery (CD)**: ogni build che supera la CI viene automaticamente pacchettizzata come artefatto versionato (JAR in Nexus, immagine in Container Registry) e rilasciata negli ambienti di Staging/UAT, pronta per essere promossa in produzione con un clic (*Manual Gate*).
- **Continuous Deployment**: evoluzione della Continuous Delivery in cui la promozione in produzione avviene in modo **100% automatizzato** se tutti i test e i controlli superano i Quality Gate stabiliti.

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

- **A cosa serve un Repository Manager aziendale**:
  1. **Proxy & Cache**: memorizza localmente le dipendenze scaricate da Maven Central / Docker Hub, velocizzando le build e proteggendo l'azienda da downtime di rete esterni.
  2. **Hosted Repositories**: archivia gli artefatti privati aziendali (JAR delle librerie core, starter interni, DTO condivisi) suddivisi tra:
     - `releases`: artefatti immutabili definitivi (es. `1.0.0`). Non possono mai essere sovrascritti.
     - `snapshots`: versioni di sviluppo modificabili (es. `1.0.1-SNAPSHOT`).
  3. **Container Registry**: funge da registro Docker privato per le immagini dei microservizi prima del deploy in Kubernetes/OpenShift.

---

#### 4. Strategie di Deployment a Zero-Downtime

In un sistema di pagamento attivo 24/7 non sono ammesse finestre di manutenzione con downtime del servizio:

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

1. **Rolling Update (Default Kubernetes)**:
   - Sostituisce i vecchi pod con i nuovi uno alla volta.
   - Non richiede il doppio dell'infrastruttura, ma durante il roll-out convivono due versioni diverse (richiede retrocompatibilità sul DB).
2. **Blue/Green Deployment**:
   - Vengono mantenuti due ambienti identici: *Blue* (versione corrente in produzione) e *Green* (nuova versione).
   - Quando la versione *Green* supera tutti i test di fumo, il Load Balancer (o Ingress) commuta istantaneamente il 100% del traffico su *Green*.
   - *Rollback istantaneo*: basta commutare nuovamente il router su *Blue*.
3. **Canary Deployment**:
   - La nuova versione viene rilasciata a una piccola percentuale di traffico reale (es. 2% degli utenti).
   - Se le metriche di errore (Prometheus/Grafana) e i log di business restano nominali, la percentuale viene incrementata gradualmente fino al 100%.

---

#### 5. GitOps e Deployment Dichiarativo (ArgoCD / Flux)
- L'intero stato desiderato dell'infrastruttura e dei microservizi Kubernetes è descritto dichiarativamente in un repository Git dedicato (*Infrastructure as Code*).
- Un controller in Kubernetes (**ArgoCD**) monitora il repository Git: quando un nuovo commit approva una nuova versione dell'immagine, ArgoCD sincronizza automaticamente lo stato del cluster (*Auto-Sync*).

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Qual è la differenza tra Continuous Delivery e Continuous Deployment?*
  - **R**: In entrambi i casi il codice supera l'intera pipeline di CI (build, test, analisi di sicurezza) e viene rilasciato automaticamente in un ambiente di staging. Nella **Continuous Delivery** il passaggio finale in produzione richiede un'approvazione umana esplicita (click su un pulsante o approvazione formale di release). Nel **Continuous Deployment** l'intero flusso è 100% automatico e ogni commit che supera i test atterra direttamente in produzione senza alcun intervento umano.

- *D: Come gestisci un rilascio Blue/Green se la nuova versione include modifiche allo schema del database?*
  - **R**: Applicando il pattern **Expand and Contract (Parallel Run)**: le modifiche al database devono essere sempre retrocompatibili. Nel primo step (*Expand*) si aggiungono nuove colonne o tabelle senza eliminare quelle vecchie, garantendo che sia la versione *Blue* che la *Green* possano funzionare simultaneamente. Solo dopo che la versione *Green* è promossa definitivamente e la vecchia versione viene dismessa, una successiva migrazione DB (*Contract*) rimuove le colonne deprecate.

---

### Come esercitarti
1. **Pipeline Scripting**: scrivi un file `Jenkinsfile` o `.gitlab-ci.yml` che esegue `mvn clean verify`, invoca l'analisi SonarQube con stop on quality gate failure, compila l'immagine Docker con hash del commit e notifica l'esito su Slack/Teams.
