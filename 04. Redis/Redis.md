# 4. Redis e caching distribuito

## Perché mettere una copia dei dati in memoria

Una **cache** conserva dati già ottenuti o risultati già calcolati per evitare di ripetere lavoro costoso. Redis mantiene i dati principalmente in memoria e offre un modello chiave-valore con strutture specializzate. In un servizio di pagamenti può conservare configurazioni dei merchant, cioè gli esercenti, oppure risultati di letture frequenti. Prima di usarlo bisogna decidere qual è la fonte autorevole e quanto può essere vecchia una copia.

Il vantaggio non deriva soltanto dalla RAM. Redis offre operazioni su stringhe, hash, liste e set. Un **hash** raggruppa campi associati a una chiave; un **set** contiene valori unici; un **sorted set** associa ai membri un punteggio, utile per classifiche. Comandi come `INCR` aggiornano un contatore atomicamente: due client non eseguono un fragile ciclo separato di lettura e scrittura.

## Scadenza, invalidazione e memoria

Il **TTL**, Time To Live, è la durata oltre la quale una chiave scade. Limita la permanenza di una copia, ma non la rende aggiornata subito dopo ogni modifica della fonte. Un dato **stale** è una copia obsoleta: per alcune configurazioni è accettabile per pochi secondi, per decidere se autorizzare una spesa può non esserlo.

Nel modello **cache-aside** l'applicazione cerca prima in cache e, in caso di assenza, legge la fonte e popola la copia. Dopo una scrittura deve invalidare o aggiornare la cache secondo una strategia coerente. Con Spring, `@Cacheable` esprime il riuso di un risultato, ma richiede un cache manager configurato: l'annotazione da sola non seleziona Redis.

```java
@Cacheable(value = "merchantConfig", key = "#merchantId")
public MerchantConfig getMerchantConfig(String merchantId) {
    return merchantRepository.loadConfig(merchantId);
}
```

L'esempio presuppone tipi applicativi e configurazione della cache. Scadenza e invalidazione vanno progettate separatamente. Se molte chiavi scadono insieme, le richieste possono riversarsi sulla fonte: è una **cache stampede**, da contenere con scadenze distribuite e controllo del lavoro di ricostruzione.

## Persistenza e distribuzione

Gli snapshot **RDB** salvano un'immagine dei dati; l'**AOF**, Append-Only File, registra operazioni. La finestra di perdita e i costi dipendono dalla configurazione. Essere in memoria non significa necessariamente perdere tutto al riavvio, ma avere persistenza non dimostra le garanzie necessarie a un registro contabile. La [documentazione Redis sulla persistenza](https://redis.io/docs/latest/management/persistence/) descrive i compromessi delle due modalità.

Il cluster divide le chiavi tra nodi: questo **sharding** aumenta la capacità complessiva ma richiede attenzione alle operazioni che coinvolgono più chiavi. La replica copia dati su altri nodi e ha proprietà diverse dal partizionamento. La memoria va dimensionata e la politica di eviction, cioè rimozione di chiavi quando il limite viene raggiunto, deve essere compatibile con il loro significato.

## Contatori, messaggi e idempotenza

Il **Pub/Sub** distribuisce messaggi ai subscriber collegati, senza offrire automaticamente la storia recuperabile di un log. È adatto ad alcune notifiche effimere, non a presumere che un consumer assente recuperi ogni pagamento.

Per il rate limiting, un contatore con scadenza può limitare richieste in una finestra. Incremento e scadenza richiedono coordinamento: un crash tra due comandi può lasciare un contatore senza TTL. Per l'idempotenza, `SET` con opzioni di inserimento solo se assente e scadenza può assegnare un marcatore temporaneo. Quel marcatore non dimostra però che l'effetto sia completato e può scadere durante l'elaborazione.

Per un addebito serve collegare identificatore, stato ed effetto durevole, spesso con un vincolo nel database autorevole. La [documentazione sui lock Redis](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/) discute le condizioni di sicurezza dei lock: un lock temporaneo e un registro dell'esito sono responsabilità differenti.

## Ragionare sul caso d'uso

Spiega quali dati del merchant metteresti in cache e come ne gestiresti la modifica. Poi confronta un contatore di accessi con un pagamento: il primo può tollerare alcune approssimazioni, il secondo richiede che un retry non produca un secondo effetto contabile.
