# 49. Defensive Programming e Secure Coding

## Obiettivo
Sviluppare codice robusto che gestisca input inattesi, errori, dipendenze non affidabili e minacce di sicurezza secondo il principio **fail safe / secure by design**.

## Defensive Programming
Principi fondamentali:
- Validate input
- Fail fast
- Fail secure
- Least privilege
- Explicit assumptions
- Immutability dove appropriata
- Null safety
- Bounds checking
- Resource limits
- Error handling esplicito
- Defense in depth

## Input Validation
Non fidarsi mai dell'input proveniente da:
- HTTP request
- query parameters
- headers
- file
- message broker
- database esterno
- sistemi partner

Validare:
- tipo
- formato
- range
- lunghezza
- encoding
- semantica business

Esempio:
```java
if (amount == null || amount.signum() < 0) {
    throw new IllegalArgumentException("Invalid amount");
}
```

In Spring usare validation declarativa quando appropriato:
- `@Valid`
- `@Validated`
- `@NotNull`
- `@Size`
- `@Pattern`
- `@Positive`

## Fail Fast vs Fail Open
In caso di input o configurazione non valida, preferire un comportamento che impedisca l'esecuzione non sicura.

Esempio di errore grave:
```text
Authorization service unavailable
        ↓
Allow request  ❌
```

Preferibile, quando il dominio lo consente:
```text
Authorization service unavailable
        ↓
Deny request   ✅
```

## Exception Handling
Non usare eccezioni generiche senza motivo.

Best practice:
- eccezioni specifiche
- error response standardizzato
- non esporre stack trace
- logging con correlation ID
- separare errori tecnici da errori di business
- evitare catch che nascondono il problema

## Null Safety
Ridurre i NullPointerException attraverso:
- invariants
- constructor validation
- `Optional` nei return type appropriati
- oggetti immutabili
- `Objects.requireNonNull`

## Resource Management
Gestire sempre correttamente:
- DB connections
- HTTP connections
- file handles
- streams
- thread pools
- memory buffers

Usare `try-with-resources` quando appropriato.

## Timeouts
Ogni chiamata a una dipendenza esterna dovrebbe avere timeout appropriati:
- connection timeout
- read/response timeout
- overall request timeout

Una chiamata senza timeout può trasformare un problema di una dipendenza in un esaurimento di thread/connection pool.

## Resilience
Combinare defensive programming con:
- timeout
- retry con backoff
- circuit breaker
- bulkhead
- rate limiting
- idempotency

Non applicare retry indiscriminatamente: un retry su una operazione non idempotente può produrre duplicati.

## Security
Secure coding deve includere:
- SQL injection prevention
- output encoding
- XSS prevention
- CSRF protection quando applicabile
- SSRF protection
- path traversal prevention
- XXE protection
- secure deserialization
- secret management
- TLS
- authorization checks

Usare prepared statements/JPA parameters invece di concatenare SQL proveniente dall'input.

## Authorization
Non affidarsi esclusivamente al client per applicare le regole di sicurezza.

```text
Client says: "I am ADMIN"
        ↓
Server verifies identity
        ↓
Server verifies authorization
        ↓
Allow / Deny
```

## Secrets
Non inserire password, API key o token:
- nel codice
- nei repository
- nei log
- nelle immagini Docker
- nelle configurazioni versionate

Usare secret manager e meccanismi di rotazione.

## Dependency Security
Controllare:
- vulnerabilità delle dipendenze
- versioni obsolete
- transitive dependencies
- SBOM
- SCA

Integrare security scanning nella CI/CD.

## Defensive Programming nei microservizi
Ogni servizio deve assumere che:
- la rete possa fallire
- il database possa essere lento
- il broker possa essere indisponibile
- i messaggi possano essere duplicati
- le API esterne possano restituire dati inattesi
- i timeout possano verificarsi

Questo porta a progettare per **partial failure** invece di assumere che tutte le dipendenze siano sempre disponibili.

## Code Review Checklist
Prima di approvare codice chiedersi:
1. L'input è validato?
2. Le autorizzazioni sono verificate lato server?
3. Esistono timeout?
4. Retry e operazioni sono compatibili con l'idempotenza?
5. Gli errori sono gestiti correttamente?
6. Vengono esposti dati sensibili?
7. Esistono resource leak?
8. Sono presenti race condition?
9. Le dipendenze sono sicure?
10. Esistono test per i failure scenario?

## Domande da colloquio
1. Cos'è Defensive Programming?
2. Fail fast vs fail secure?
3. Come gestisci input non affidabili?
4. Come proteggi una API da SSRF?
5. Come gestisci timeout e retry?
6. Perché un retry può essere pericoloso?
7. Come eviti SQL injection?
8. Come gestisci i secret?
9. Cosa significa secure by design?
10. Come progetteresti un microservizio che continua a comportarsi correttamente quando una dipendenza è indisponibile?

## Regola Senior
Un codice di qualità non considera solo il **happy path**. Progetta esplicitamente per errori, input malevoli, dipendenze indisponibili, dati inconsistenti, timeout, concorrenza e failure parziali.
