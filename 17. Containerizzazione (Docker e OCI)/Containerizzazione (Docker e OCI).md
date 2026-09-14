# 17. Containerizzazione (Docker e OCI)

### Cos'è e perché conta
La containerizzazione è il fondamento del deployment moderno su cloud e ambienti Kubernetes. Un'immagine container incapsula il codice applicativo, il runtime Java (JRE), le librerie e la configurazione del sistema operativo, garantendo che l'applicazione si comporti in modo identico in locale, in ambiente di staging e in produzione. Un Senior Developer deve saper scrivere `Dockerfile` sicuri, ottimizzati e leggeri usando **Multi-Stage Builds**.

---

### Cosa studiare

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

- **Macchina Virtuale**: virtualizza l'hardware; ogni VM include un intero sistema operativo guest (Guest OS), occupando diversi GB di RAM/disco con tempi di avvio nell'ordine dei minuti.
- **Container**: virtualizza l'OS; condivide il **Kernel Linux** dell'host isolando i processi tramite due primitive fondamentali del kernel:
  1. **Namespaces**: isolamento delle risorse (PID per i processi, NET per la rete, MNT per il filesystem, IPC per la memoria condivisa).
  2. **cgroups (Control Groups)**: limitazione e monitoraggio dell'uso di risorse hardware (massima CPU, massima memoria RAM assegnabile al container).

---

#### 2. Anatomia di un'Immagine Docker e Layer Caching

Un'immagine Docker è composta da una pila di **layer di sola lettura (Read-Only)** memorizzati tramite un Union File System (overlay2). Quando si avvia un container, Docker aggiunge in cima un sottile layer di lettura/scrittura (**Container/Writable Layer**).

- **Principio del Layer Caching**:
  - Docker riutilizza la cache per ogni istruzione (`COPY`, `RUN`) finché i file sorgente di quell'istruzione non cambiano.
  - **Best Practice per Java**: copiare prima i file di configurazione Maven/Gradle (`pom.xml` / `mvnw`) e scaricare le dipendenze (`RUN ./mvnw dependency:go-offline`), e solo successivamente copiare il codice sorgente `src/`. In questo modo, modificando solo il codice Java, Docker riutilizza la cache dei layer delle dipendenze velocizzando drasticamente la build da minuti a secondi.

---

#### 3. Dockerfile Multi-Stage per Applicazioni Spring Boot

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

1. **Mai eseguire come utente `root`**: usare sempre `USER appuser` per prevenire attacchi di container breakout.
2. **Usare Immagini Base Minimali (Distroless / Alpine / Chainguard)**: riduce la superficie di attacco eliminando package manager, shell non necessarie e utility obsolete.
3. **Gestione della Memoria JVM nei Container (`-XX:MaxRAMPercentage`)**:
   - Nelle versioni moderne di Java (8u191+, 11, 17, 21), la JVM riconosce i limiti di memoria del cgroup del container.
   - Usare `-XX:MaxRAMPercentage=75.0` anziché fissare `-Xmx` con valori statici in MB, permettendo al container di scalare dinamicamente in base ai limiti assegnati da Kubernetes.
4. **Scansione delle Vulnerabilità delle Immagini (Trivy / Snyk / Docker Scout)**: integrata nella pipeline CI per bloccare immagini con CVE critiche a livello di sistema operativo.
5. **Mai inserire Segreti o Certificati nell'Immagine**: iniettarli a runtime tramite Environment Variables o Secret montati come volumi (Kubernetes Secrets / HashiCorp Vault).

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

- *D: Perché utilizzi il Multi-Stage Build nel Dockerfile?*
  - **R**: Perché permette di separare nettamente l'ambiente di compilazione (che necessita di JDK completo, Maven/Gradle, codice sorgente e file di configurazione) dall'ambiente di runtime (che necessita solo del JRE minimale e dei file `.class`). Questo riduce la dimensione dell'immagine finale da oltre 600MB a meno di 150MB ed elimina dalla produzione strumenti di compilazione che aumenterebbero la superficie di attacco.

- *D: Come si comporta la memoria della JVM all'interno di un container Docker/Kubernetes?*
  - **R**: Storicamente la JVM leggeva la memoria fisica totale dell'host ignorando i limiti del cgroup, causando l'uccisione del container da parte dell'OOM Killer del kernel Linux. Dalle versioni recenti (Java 11/17/21), la JVM supporta nativamente i cgroups: impostando il flag `-XX:MaxRAMPercentage=75.0`, la JVM alloca come dimensione massima dello Heap il 75% della memoria RAM assegnata al container, lasciando il restante 25% per Metaspace, thread stack e memoria off-heap del sistema operativo.

---

### Come esercitarti
1. **Scrittura Dockerfile**: prendi un progetto Spring Boot e scrivi un `Dockerfile` a due stadi con Alpine JRE, utente non-root e flag JVM container-aware; compilalo ed esegui `docker run` verificando che l'utente non sia root con `docker exec -it <id> whoami`.
