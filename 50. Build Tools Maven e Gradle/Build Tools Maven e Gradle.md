# 50. Build Tools — Maven e Gradle

## Obiettivo
Conoscere Maven e Gradle non solo come strumenti per compilare un progetto Java, ma come parte del lifecycle, dependency management e CI/CD.

## Maven
Concetti:
- `pom.xml`
- coordinates: groupId, artifactId, version
- dependency management
- transitive dependencies
- scopes
- lifecycle
- plugins
- profiles
- repositories
- BOM

### Lifecycle
Fasi importanti:
- validate
- compile
- test
- package
- verify
- install
- deploy

Comandi:
```bash
mvn clean test
mvn clean verify
mvn dependency:tree
mvn spring-boot:run
```

## Dependency Management
Conoscere la differenza tra:
- direct dependency
- transitive dependency
- dependency management
- dependency scope

Problemi comuni:
- dependency conflicts
- version mismatch
- vulnerable transitive dependency
- duplicate libraries

## Gradle
Concetti:
- `build.gradle` / `build.gradle.kts`
- plugins
- tasks
- configurations
- dependencies
- repositories
- Gradle Wrapper
- multi-module builds

Comandi:
```bash
./gradlew clean test
./gradlew build
./gradlew dependencies
```

## Maven vs Gradle
Maven usa un lifecycle convention-driven molto strutturato.

Gradle offre un modello più programmabile e spesso build incrementali più flessibili.

La scelta dipende da standard aziendali, ecosystem, complessità della build e competenze del team.

## Multi-module projects
Strutturare un progetto per separare moduli con responsabilità chiare:
```text
parent
├── domain
├── application
├── infrastructure
└── api
```

Evitare dipendenze circolari tra moduli.

## Build Reproducibility
Usare:
- Maven Wrapper / Gradle Wrapper
- versioni fissate
- dependency management centralizzato
- repository affidabili
- CI con ambiente riproducibile

## CI/CD
Una pipeline tipica:
```text
Checkout
  ↓
Build
  ↓
Unit Tests
  ↓
Static Analysis
  ↓
Security Scan
  ↓
Integration Tests
  ↓
Package
  ↓
Artifact Repository
  ↓
Deploy
```

## Domande da colloquio
1. Maven lifecycle?
2. Dependency transitiva?
3. `dependencyManagement` vs `dependencies`?
4. Come trovi un dependency conflict?
5. Cos'è un BOM?
6. Maven vs Gradle?
7. Perché usare Maven/Gradle Wrapper?
8. Come gestisci un multi-module project?
9. Come rendi riproducibile una build?
10. Come colleghi build tool e CI/CD?
