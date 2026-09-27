# Aspect Oriented Programming (AOP) e Aspect in Spring

## Perché AOP è importante

**AOP (Aspect-Oriented Programming)** permette di separare dalla business logic i cosiddetti **cross-cutting concerns**, cioè comportamenti trasversali che interessano molti componenti dell'applicazione.

Esempi tipici:

- logging
- auditing
- metriche
- tracing
- security checks
- transaction management
- caching
- retry

Senza AOP si rischia di ripetere lo stesso codice in molti service:

```text
Service A ──┐
Service B ──┼── logging / metrics / security
Service C ──┤
Service D ──┘
```

Con AOP il comportamento trasversale viene centralizzato:

```text
                 ┌── Logging
                 ├── Metrics
Service ────────>├── Security
                 ├── Transactions
                 └── Auditing
```

---

## 1. Cos'è un Aspect?

Un **Aspect** contiene la logica relativa a un cross-cutting concern.

Esempio:

```java
@Aspect
@Component
public class LoggingAspect {

    @Around("execution(* com.example.service..*(..))")
    public Object log(ProceedingJoinPoint joinPoint) throws Throwable {

        long start = System.currentTimeMillis();

        try {
            return joinPoint.proceed();
        } finally {
            long duration = System.currentTimeMillis() - start;

            System.out.println(
                joinPoint.getSignature()
                    + " took " + duration + " ms"
            );
        }
    }
}
```

Il service rimane focalizzato sulla business logic:

```java
@Service
public class OrderService {

    public Order createOrder(Order order) {
        return repository.save(order);
    }
}
```

---

## 2. Terminologia AOP

### Aspect

La componente che implementa il cross-cutting concern.

```java
@Aspect
public class LoggingAspect {
}
```

### Join Point

Un punto dell'esecuzione dell'applicazione nel quale può essere applicato un comportamento.

In **Spring AOP**, i join point sono principalmente le **execution dei metodi dei bean Spring**.

### Pointcut

Definisce **quali join point devono essere intercettati**.

```java
@Pointcut("execution(* com.example.service..*(..))")
public void serviceMethods() {}
```

Questo pointcut seleziona i metodi presenti nel package `service` e nei suoi sottopackage.

### Advice

Definisce **cosa fare quando il pointcut viene intercettato**.

---

## 3. Tipi di Advice

### `@Before`

Esegue il codice prima del metodo:

```java
@Before("serviceMethods()")
public void before() {
    System.out.println("Before");
}
```

### `@After`

Esegue il codice dopo il metodo, indipendentemente dal fatto che sia terminato con successo o con eccezione:

```java
@After("serviceMethods()")
public void after() {
    System.out.println("After");
}
```

### `@AfterReturning`

Viene eseguito quando il metodo termina correttamente.

```java
@AfterReturning(
    pointcut = "serviceMethods()",
    returning = "result"
)
public void afterReturning(Object result) {
}
```

### `@AfterThrowing`

Viene eseguito quando il metodo lancia un'eccezione.

```java
@AfterThrowing(
    pointcut = "serviceMethods()",
    throwing = "ex"
)
public void afterThrowing(Exception ex) {
}
```

### `@Around`

È l'advice più potente perché permette di eseguire codice prima e dopo il metodo intercettato e di controllare se invocare il metodo stesso.

```java
@Around("serviceMethods()")
public Object around(ProceedingJoinPoint pjp)
        throws Throwable {

    long start = System.currentTimeMillis();

    try {
        return pjp.proceed();
    } finally {
        long duration = System.currentTimeMillis() - start;
        log(duration);
    }
}
```

`pjp.proceed()` significa sostanzialmente **continua l'esecuzione del metodo intercettato**.

---

## 4. AOP e `@Transactional`

Questo è uno dei collegamenti più importanti da conoscere per un colloquio Senior.

Quando scriviamo:

```java
@Transactional
public void transferMoney(...) {
    // business logic
}
```

Spring non modifica semplicemente il metodo. In condizioni normali crea un **proxy** intorno al bean e utilizza l'infrastruttura AOP/interceptor per applicare la gestione transazionale.

Concettualmente:

```text
Client
  │
  ▼
Spring Proxy
  │
  ├── begin transaction
  │
  ▼
Service
  │
  ├── business logic
  │
  ▼
Spring Proxy
  │
  └── commit / rollback
```

Questo spiega anche molti comportamenti apparentemente sorprendenti di `@Transactional`.

---

## 5. Spring AOP e Proxy

Spring AOP utilizza principalmente:

- **JDK Dynamic Proxy**
- **CGLIB proxy**

Schema semplificato:

```text
Client
  ↓
Proxy
  ↓
Target Bean
```

Il proxy intercetta la chiamata e applica gli interceptor/aspect configurati.

### JDK Dynamic Proxy

È basato sulle interfacce implementate dal bean.

### CGLIB

Crea una sottoclasse del target per intercettare le chiamate.

Il dettaglio della scelta dipende dalla configurazione e dalla versione/configurazione di Spring; per il colloquio è soprattutto importante capire che **Spring AOP è principalmente proxy-based**.

---

## 6. Self-invocation: il problema classico

Consideriamo:

```java
@Service
public class MyService {

    public void methodA() {
        methodB();
    }

    @Transactional
    public void methodB() {
        // ...
    }
}
```

La chiamata interna:

```java
methodB();
```

non passa attraverso il proxy Spring.

Concettualmente:

```text
Client
  ↓
Proxy
  ↓
methodA()
  │
  └────> methodB()
          ❌ non passa dal proxy
```

Di conseguenza l'Aspect/interceptor associato a `methodB()` può non essere applicato.

Questo problema può riguardare, oltre a `@Transactional`:

- `@Cacheable`
- `@Async`
- `@Retryable`
- altri interceptor Spring basati su proxy

### Soluzioni architetturali

Preferire, quando possibile, la separazione in bean differenti:

```text
Service A
   │
   ▼
Service B
   │
   ▼
@Transactional method
```

In questo modo la chiamata passa attraverso il proxy.

---

## 7. Spring AOP vs AspectJ

Non confondere Spring AOP con AspectJ.

### Spring AOP

È principalmente **proxy-based** ed è integrato naturalmente nel container Spring.

È adatto alla maggior parte dei cross-cutting concern tipici delle applicazioni Spring.

### AspectJ

È un framework AOP più completo e può utilizzare tecniche di **weaving** del bytecode.

Schema semplificato:

```text
Spring AOP

Client
  ↓
Proxy
  ↓
Bean
```

```text
AspectJ

Source
  ↓
Weaving
  ↓
Bytecode
  ↓
Execution
```

AspectJ permette quindi scenari di weaving più ampi rispetto al modello proxy-based di Spring AOP.

---

## 8. Quando usare AOP?

AOP è particolarmente adatto a:

| Problema | AOP |
|---|---|
| Logging | ✅ |
| Metrics | ✅ |
| Tracing | ✅ |
| Auditing | ✅ |
| Transactions | ✅ |
| Security checks | ✅ |
| Caching | ✅ |
| Retry | ✅ |
| Business logic | ❌ |
| Workflow complessi di dominio | ❌ |

### Regola pratica

> **AOP è ottimo per comportamenti trasversali, non per nascondere la business logic.**

Un Aspect eccessivamente complesso può rendere il sistema difficile da comprendere e debuggare perché il comportamento effettivo di un metodo non è più evidente leggendo il codice della classe.

---

## 9. Esempio: performance monitoring

Un Aspect può misurare automaticamente la durata delle operazioni:

```java
@Aspect
@Component
public class PerformanceAspect {

    @Around("execution(* com.example.service..*(..))")
    public Object measure(ProceedingJoinPoint joinPoint)
            throws Throwable {

        long start = System.nanoTime();

        try {
            return joinPoint.proceed();
        } finally {
            long elapsed = System.nanoTime() - start;

            log.info(
                "{} took {} ns",
                joinPoint.getSignature(),
                elapsed
            );
        }
    }
}
```

Questo permette di centralizzare il comportamento senza contaminare i service con codice di monitoring.

In sistemi reali è preferibile integrare questo approccio con strumenti di observability e tracing standardizzati invece di implementare manualmente tutta la telemetria.

---

## 10. Domande da colloquio Senior

1. Cos'è AOP?
2. Cos'è un Aspect?
3. Qual è la differenza tra Aspect, Pointcut, Join Point e Advice?
4. Quali tipi di Advice conosci?
5. Quando useresti `@Around` invece di `@Before`?
6. Come funziona `@Transactional` internamente?
7. Perché Spring utilizza proxy per AOP?
8. JDK Dynamic Proxy vs CGLIB?
9. Cos'è il problema della self-invocation?
10. Perché una `@Transactional` chiamata internamente dallo stesso bean può non funzionare come previsto?
11. Spring AOP vs AspectJ?
12. Quali cross-cutting concerns gestiresti con AOP?
13. Useresti AOP per implementare una regola di business complessa? Perché no?
14. Come useresti AOP per aggiungere metriche a tutti i service?
15. Quali sono i rischi di abuso di AOP?

---

## 11. Risposta da colloquio

Se viene chiesto **"Cos'è AOP e come funziona in Spring?"**, una risposta da Senior può essere:

> AOP, Aspect-Oriented Programming, permette di separare i cross-cutting concerns dalla business logic. In Spring viene principalmente implementato tramite proxy che intercettano le chiamate ai bean. Un Aspect definisce un Pointcut, cioè quali join point intercettare, e degli Advice, cioè quale comportamento applicare prima, dopo o intorno all'esecuzione del metodo. Un esempio classico è `@Transactional`, dove il proxy gestisce transaction begin, commit e rollback attorno alla chiamata al service. Bisogna inoltre conoscere il limite della self-invocation, perché una chiamata interna tra metodi dello stesso bean non passa attraverso il proxy Spring.

### Concetti da ricordare

```text
AOP
 │
 ├── Aspect       → cross-cutting concern
 ├── Join Point   → punto intercettabile
 ├── Pointcut     → quali join point selezionare
 └── Advice       → cosa eseguire
      ├── Before
      ├── After
      ├── AfterReturning
      ├── AfterThrowing
      └── Around

Spring AOP
     ↓
  Proxy-based
     ↓
Self-invocation
     ↓
non passa dal proxy
```
