# 17. Containerizzazione (Docker e OCI)
## Il problema da cui partire
Un **container** esegue un processo con isolamento e limiti forniti dal sistema operativo. Un'**immagine** descrive filesystem e metadati da cui partire; il container aggiunge stato di esecuzione e, quando previsto, un livello scrivibile. Un **registry** distribuisce immagini versionate. Sono oggetti distinti con cicli di vita diversi.
**OCI**, Open Container Initiative, definisce specifiche per immagini e runtime interoperabili. Un container condivide il kernel dell'ambiente che lo ospita e non equivale a una macchina virtuale con kernel proprio. **Namespace** e **cgroup** sono meccanismi Linux per isolamento e controllo delle risorse; non sono rispettivamente i Namespace Kubernetes e un limite automatico del solo heap Java. Per un backend Java, la memoria comprende heap, metadati, stack e componenti native. L'immagine verificata deve poter essere identificata e la configurazione sensibile deve arrivare al momento opportuno, senza essere incorporata nei layer.
#### 1. Architettura dei Container: Container vs Macchine Virtuali (VM)
```
┌───────────────────────────────┐     ┌───────────────────────────────┐
│     CONTAINER ARCHITECTURE    │     │    VIRTUAL MACHINE (VM)       │
├───────────────────────────────┤     ├───────────────────────────────┤
│ App 1 (Java)   App 2 (Node)   │     │ App 1 (Java)   App 2 (Node)   │
│ Bins/Libs      Bins/Libs      │     │ Bins/Libs      Bins/Libs      │
├───────────────────────────────┤     │ Guest OS 1     Guest OS 2     │
│   CONTAINER ENGINE (Docker)   │     ├───────────────────────────────┤
├───────────────────────────────┤     │          HYPERVISOR           │
│   HOST OPERATING SYSTEM       │     ├───────────────────────────────┤
├───────────────────────────────┤     │     HOST OPERATING SYSTEM     │
│   PHYSICAL INFRASTRUCTURE    │     │    PHYSICAL INFRASTRUCTURE   │
└───────────────────────────────┘     └───────────────────────────────┘
```
**Macchina Virtuale**: virtualizza l'hardware; ogni VM include un intero sistema operativo guest (Guest OS), occupando diversi GB di RAM/disco con tempi di avvio nell'ordine dei minuti.
**Container**: virtualizza l'OS; condivide il **Kernel Linux** dell'host isolando i processi tramite due primitive fondamentali del kernel:

**Namespaces**: isolamento delle risorse (PID per i processi, NET per la rete, MNT per il filesystem, IPC per la memoria condivisa).

**cgroups (Control Groups)**: limitazione e monitoraggio dell'uso di risorse hardware (massima CPU, massima memoria RAM assegnabile al container).

---
#### 2. Anatomia di un'Immagine Docker e Layer Caching
Un'immagine Docker è composta da una pila di **layer di sola lettura (Read-Only)** memorizzati tramite un Union File System (overlay2). Quando si avvia un container, Docker aggiunge in cima un sottile layer di lettura/scrittura (**Container/Writable Layer**). **Principio del Layer Caching**: Docker riutilizza la cache per ogni istruzione (`COPY`, `RUN`) finché i file sorgente di quell'istruzione non cambiano.
**Best Practice per Java**: copiare prima i file di configurazione Maven/Gradle (`pom.xml` / `mvnw`) e scaricare le dipendenze (`RUN ./mvnw dependency:go-offline`), e solo successivamente copiare il codice sorgente `src/`. In questo modo, modificando solo il codice Java, Docker riutilizza la cache dei layer delle dipendenze velocizzando drasticamente la build da minuti a secondi.
---
#### 3. Dockerfile Multi-Stage per Applicazioni Spring Boot
Un **multi-stage build** usa una fase per compilare e una diversa per eseguire. Il risultato contiene ciò che serve al runtime, riducendo strumenti e materiali superflui; non dimostra da solo l'assenza di vulnerabilità. Il **digest** identifica il contenuto dell'immagine, mentre un tag può essere riassegnato. Per ricostruire un rilascio, si conserva il collegamento tra commit, build e digest. Il caching dei layer dipende dagli input delle istruzioni. Ordinare prima gli input che cambiano raramente può ridurre il lavoro, ma i segreti non devono essere copiati in un layer contando di rimuoverli successivamente: il livello precedente può conservarli.
Nei contesti di produzione bancari/enterprise, l'immagine finale non deve contenere il compilatore Maven/JDK, il codice sorgente o strumenti di sviluppo (per motivi di sicurezza e dimensione). Si usa il pattern **Multi-Stage Build**:
```dockerfile
# ==========================================
# STAGE 1: Build & Package (con Maven/JDK)
# ==========================================
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app

# Copia solo i file di build per sfruttare il layer caching
COPY pom.xml mvnw ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline -B

# Copia i sorgenti e compila il JAR
COPY src ./src
RUN ./mvnw clean package -DskipTests

# Estrae i layer del fat-jar Spring Boot per ottimizzare il caching dei container
RUN java -Djarmode=layertools -jar target/*.jar extract

# ==========================================
# STAGE 2: Runtime Image (Minimale & Sicura)
# ==========================================
FROM eclipse-temurin:21-jre-alpine AS runner
WORKDIR /workspace

# Creazione di un utente non-root per conformità di sicurezza
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser:appgroup

# Copia i layer Spring Boot estratti dallo stage precedente
COPY --from=builder /app/dependencies/ ./
COPY --from=builder /app/spring-boot-loader/ ./
COPY --from=builder /app/snapshot-dependencies/ ./
COPY --from=builder /app/application/ ./

# Esposizione porta e variabili JVM
EXPOSE 8080
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75.0 -XX:+UseG1GC -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS org.springframework.boot.loader.launch.JarLauncher"]
```
---
#### 4. Sicurezza dei Container & Best Practice di Produzione

**Mai eseguire come utente `root`**: usare sempre `USER appuser` per prevenire attacchi di container breakout.

**Usare Immagini Base Minimali (Distroless / Alpine / Chainguard)**: riduce la superficie di attacco eliminando package manager, shell non necessarie e utility obsolete.

**Gestione della Memoria JVM nei Container (`-XX:MaxRAMPercentage`)**:

Nelle versioni moderne di Java (8u191+, 11, 17, 21), la JVM riconosce i limiti di memoria del cgroup del container. Usare `-XX:MaxRAMPercentage=75.0` anziché fissare `-Xmx` con valori statici in MB, permettendo al container di scalare dinamicamente in base ai limiti assegnati da Kubernetes.

**Scansione delle Vulnerabilità delle Immagini (Trivy / Snyk / Docker Scout)**: integrata nella pipeline CI per bloccare immagini con CVE critiche a livello di sistema operativo.

**Mai inserire Segreti o Certificati nell'Immagine**: iniettarli a runtime tramite Environment Variables o Secret montati come volumi (Kubernetes Secrets / HashiCorp Vault).

---
#### 5. Docker Compose per lo Sviluppo Locale
Strumento per orchestrare ambienti multi-container locali (Spring Boot + Oracle XE + Kafka + Redis):
```yaml
version: '3.8'
services:
  payment-db:
    image: gvenzl/oracle-xe:21-slim-faststart
    environment:
      - ORACLE_PASSWORD=topsecret
      - APP_USER=payment_user
      - APP_USER_PASSWORD=payment_pass
    ports:
      - "1521:1521"
    volumes:
      - oracle_data:/opt/oracle/oradata

  kafka-broker:
    image: confluentinc/cp-kafka:7.4.0
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: 'CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT'
      KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka-broker:29092,PLAINTEXT_HOST://localhost:9092'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"

volumes:
  oracle_data:
```
---
### Domande tipiche a colloquio (e risposte da Senior)
*D: Perché utilizzi il Multi-Stage Build nel Dockerfile?*
**R**: Perché permette di separare nettamente l'ambiente di compilazione (che necessita di JDK completo, Maven/Gradle, codice sorgente e file di configurazione) dall'ambiente di runtime (che necessita solo del JRE minimale e dei file `.class`). Questo riduce la dimensione dell'immagine finale da oltre 600MB a meno di 150MB ed elimina dalla produzione strumenti di compilazione che aumenterebbero la superficie di attacco.
*D: Come si comporta la memoria della JVM all'interno di un container Docker/Kubernetes?*
**R**: Storicamente la JVM leggeva la memoria fisica totale dell'host ignorando i limiti del cgroup, causando l'uccisione del container da parte dell'OOM Killer del kernel Linux. Dalle versioni recenti (Java 11/17/21), la JVM supporta nativamente i cgroups: impostando il flag `-XX:MaxRAMPercentage=75.0`, la JVM alloca come dimensione massima dello Heap il 75% della memoria RAM assegnata al container, lasciando il restante 25% per Metaspace, thread stack e memoria off-heap del sistema operativo.
---
### Come esercitarti

1. **Scrittura Dockerfile**: prendi un progetto Spring Boot e scrivi un `Dockerfile` a due stadi con Alpine JRE, utente non-root e flag JVM container-aware; compilalo ed esegui `docker run` verificando che l'utente non sia root con `docker exec -it <id> whoami`.
