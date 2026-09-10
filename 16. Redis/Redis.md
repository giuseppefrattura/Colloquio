## 16. Redis

### Cos'è
Database **in-memory key-value**, estremamente veloce (dati tenuti in RAM), usato principalmente come cache, ma anche come message broker leggero (pub/sub), store di sessioni, o per strutture dati specializzate (contatori, code, set, sorted set).

### Caratteristiche principali

- **Strutture dati ricche**: non solo stringhe, ma anche liste, set, hash, sorted set (utili per classifiche/ranking), tutte con operazioni atomiche native
- **Persistenza opzionale**: pur essendo in-memory, supporta snapshot su disco (RDB) o log delle operazioni (AOF) per non perdere tutto in caso di riavvio — comunque non sostituisce un DB transazionale
- **TTL (Time To Live)**: ogni chiave può avere una scadenza automatica — fondamentale per cache che non deve restare stale indefinitamente
- **Operazioni atomiche**: es. `INCR` per contatori concorrenti senza race condition, utile per rate limiting
- **Pub/Sub**: meccanismo di messaggistica semplice (non persistente come Kafka — se non c'è un subscriber attivo, il messaggio si perde)
- **Cluster mode**: sharding automatico dei dati su più nodi per scalabilità orizzontale

### Esempio di utilizzo (Spring Boot)

```java
// Cache di un risultato costoso da ricalcolare
@Cacheable(value = "accountBalance", key = "#accountId")
public BigDecimal getBalance(String accountId) {
    return accountRepository.calculateBalance(accountId); // query pesante
}

// Idempotency key con TTL, via RedisTemplate
public boolean tryLockIdempotencyKey(String key) {
    Boolean success = redisTemplate.opsForValue()
        .setIfAbsent(key, "PROCESSED", Duration.ofMinutes(10));
    return Boolean.TRUE.equals(success); // true solo se la chiave non esisteva già
}
```

### Rilevanza per il dominio pagamenti
Due casi d'uso molto naturali: **cache** per dati letti di frequente e poco variabili (es. configurazioni, dati anagrafici merchant), e **gestione dell'idempotenza** tramite `SETNX`/`setIfAbsent` con TTL — un modo rapido per verificare "questa richiesta è già stata processata?" senza appesantire il DB transazionale principale. Anche utile per **rate limiting** sulle chiamate verso circuiti esterni, con `INCR` + TTL per contare le richieste in una finestra temporale.

### Domande tipiche e risposte

- *D: Redis è adatto a salvare il saldo di un conto come fonte di verità?*
  R: No — è in-memory e pensato per velocità, non per le garanzie ACID complete che servono per il ledger. Il saldo "vero" resta su Oracle; Redis può cachearne una copia in lettura, ma ogni scrittura deve passare dal DB transazionale.

- *D: Come implementeresti un idempotency check con Redis?*
  R: Con `SETNX` (o `setIfAbsent` in Spring Data Redis) usando l'idempotency key come chiave — l'operazione è atomica, quindi se due richieste concorrenti arrivano nello stesso istante, solo una riuscirà a impostare la chiave, l'altra saprà che la richiesta è già in corso/completata. Si imposta un TTL per non accumulare chiavi indefinitamente.
