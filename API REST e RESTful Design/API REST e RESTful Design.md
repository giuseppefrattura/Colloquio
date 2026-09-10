## API REST e RESTful Design

### Cos'è e perché conta
Le API RESTful sono il canale di comunicazione principale tra microservizi di pagamento, banche e client esterni (merchant, app POS, gateway web). Un Senior Developer deve saper progettare contratti API chiari, robusti, scalabili, conformi alle specifiche HTTP, sicuri e con gestione rigorosa dell'**idempotenza**, della **retrocompatibilità** e degli **status code**.

---

### Cosa studiare

#### 1. I 6 Vincoli Architetturali di REST
REST (Representational State Transfer) è uno stile architetturale definito da Roy Fielding:
1. **Client-Server**: separazione netta tra interfaccia utente/client e archiviazione dati/backend.
2. **Stateless**: ogni richiesta dal client deve contenere **tutte le informazioni necessarie** per essere elaborata dal server (nessuna sessione utente memorizzata sullo stato del server).
3. **Cacheable**: le risposte devono dichiararsi esplicitamente memorizzabili in cache o meno (`Cache-Control`, `ETag`).
4. **Uniform Interface**: identificazione univoca delle risorse tramite URI, manipolazione tramite rappresentazioni (JSON/XML), messaggi auto-descrittivi (Content-Type) e HATEOAS.
5. **Layered System**: il client non sa (e non deve sapere) se sta parlando direttamente con il server finale o con proxy intermedi, API Gateway, Load Balancer.
6. **Code on Demand** (opzionale): capacità di inviare codice eseguibile al client.

---

#### 2. Metodi HTTP, Idempotenza e Safety

| Metodo HTTP | Scopo | Safe? (Non modifica lo stato del server) | Idempotente? (N chiamate identiche producono lo stesso stato del server) | Status Code di Successo |
|---|---|---|---|---|
| **`GET`** | Lettura/recupero di una risorsa o collezione | ✅ Sì | ✅ Sì | `200 OK` |
| **`POST`** | Creazione di una nuova risorsa o avvio di un'elaborazione | ❌ No | ❌ No (crea duplicati senza idempotency key) | `201 Created` (con header `Location`), `202 Accepted` |
| **`PUT`** | Sostituzione completa di una risorsa esistente o creazione se nota | ❌ No | ✅ Sì (sovrascrivere con gli stessi dati produce lo stesso stato) | `200 OK`, `204 No Content` |
| **`PATCH`** | Aggiornamento parziale di una risorsa (modifica di specifici campi) | ❌ No | ❌ Non garantito da standard (generalmente implementato idempotente) | `200 OK`, `204 No Content` |
| **`DELETE`** | Eliminazione di una risorsa | ❌ No | ✅ Sì (cancellare una risorsa già cancellata lascia lo stato immutato) | `204 No Content`, `200 OK` |
| **`HEAD`** | Come GET ma restituisce solo gli header HTTP (senza body) | ✅ Sì | ✅ Sì | `200 OK` |
| **`OPTIONS`** | Ispezione delle capacità del server e supporto CORS pre-flight | ✅ Sì | ✅ Sì | `200 OK`, `204 No Content` |

---

#### 3. Progettazione delle URI e Convenzioni di Naming
- **Risorse come Sostantivi Plurali**:
  - `GET /api/v1/payments`: lista pagamenti.
  - `POST /api/v1/payments`: crea un pagamento.
  - `GET /api/v1/payments/{paymentId}`: dettaglio pagamento.
  - `GET /api/v1/accounts/{accountId}/transactions`: sotto-risorse annidate.
- **Evitare Verbi negli URI**:
  - ❌ `POST /api/v1/createPayment`, `GET /api/v1/deleteAccount/123`
  - ✅ `POST /api/v1/payments`, `DELETE /api/v1/accounts/123`
- **Filtri, Paginazione e Ordinamento tramite Query Parameters**:
  - `GET /api/v1/payments?status=COMPLETED&currency=EUR&page=0&size=20&sort=createdAt,desc`

---

#### 4. Status Code HTTP Fondamentali per il Backend

```
2xx: Successo             3xx: Reindirizzamento    4xx: Errore Client       5xx: Errore Server
• 200 OK                  • 301 Moved Permanently  • 400 Bad Request        • 500 Internal Server Error
• 201 Created             • 304 Not Modified       • 401 Unauthorized       • 502 Bad Gateway
• 202 Accepted                                     • 403 Forbidden          • 503 Service Unavailable
• 204 No Content                                   • 404 Not Found          • 504 Gateway Timeout
                                                   • 409 Conflict           
                                                   • 422 Unprocessable Entity
```

- **`400 Bad Request`**: sintassi della richiesta errata o JSON malformato.
- **`401 Unauthorized`**: autenticazione mancante o token JWT non valido/scaduto (*Who are you?*).
- **`403 Forbidden`**: utente autenticato ma non autorizzato ad accedere alla risorsa (*You cannot do this*).
- **`404 Not Found`**: la risorsa richiesta non esiste.
- **`409 Conflict`**: conflitto con lo stato attuale della risorsa (es. transazione già elaborata, duplicate key).
- **`422 Unprocessable Entity`**: sintassi JSON corretta, ma violazione di regole di validazione semantica/business (es. importo negativo, IBAN formalmente errato).
- **`502 Bad Gateway` / `504 Gateway Timeout`**: problemi di comunicazione con provider esterni (es. circuito carta Visa o host bancario non raggiungibile o in timeout).

---

#### 5. Il Modello di Maturità di Richardson (RMM)
- **Livello 0 (The Swamp of POX)**: un solo endpoint HTTP (es. `/service`), usa solo `POST`, trasporta XML/JSON (stile SOAP/RPC).
- **Livello 1 (Resources)**: introduzione di URI individuali per ciascuna risorsa (`/accounts/123`).
- **Livello 2 (HTTP Verbs & Status Codes)**: uso corretto dei verbi HTTP (`GET`, `POST`, `PUT`, `DELETE`) e degli status code standard. **È il livello in cui opera la maggior parte dei servizi enterprise moderni.**
- **Livello 3 (HATEOAS - Hypermedia As The Engine Of Application State)**: le risposte includono link dinamici (es. `_links`) che guidano il client sulle azioni disponibili successive (es. `rel="cancel"`, `rel="refund"`).

---

#### 6. Idempotenza e Pattern Idempotency-Key nei Pagamenti
In caso di timeout di rete tra client e server durante un `POST /api/v1/payments`, il client non sa se il pagamento è andato a buon fine.
- **Soluzione (Idempotency Key)**:
  1. Il client genera un UUID univoco e lo invia nell'header: `Idempotency-Key: 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d`.
  2. Il server tenta l'inserimento in una tabella di lock/idempotenza con vincolo univoco (`UNIQUE constraint`).
  3. Se l'inserimento ha successo, il server elabora il pagamento e ne memorizza la risposta.
  4. Se la chiave esiste già (richiesta duplicata / retry di rete), il server **non riesegue l'addebito**, ma restituisce la risposta già elaborata in precedenza.

---

#### 7. Standardizzazione Risposte di Errore: RFC 7807 (Problem Details)
Standard moderno per restituire errori JSON chiari e uniformi (`application/problem+json`):

```json
{
  "type": "https://api.bank.com/errors/insufficient-funds",
  "title": "Fondi Insufficienti",
  "status": 422,
  "detail": "Il conto 12345 ha un saldo disponibile di 15.00 EUR, inferiore all'importo richiesto di 50.00 EUR",
  "instance": "/api/v1/payments/pay_987654",
  "invalidParams": [
    { "name": "amount", "reason": "Exceeds available balance" }
  ],
  "timestamp": "2026-09-10T21:40:00Z"
}
```

---

#### 8. Versioning delle API & Documentazione OpenAPI (Swagger)
- **Strategie di Versioning**:
  - *URI Versioning* (più diffuso e trasparente): `/api/v1/payments` vs `/api/v2/payments`.
  - *Header Versioning* (Content Negotiation): `Accept: application/vnd.bank.v2+json`.
- **OpenAPI 3.0 / Springdoc-openapi**:
  - Generazione automatica di documentazione interattiva (Swagger UI).
  - Approccio *Code-First* con annotazioni (`@Operation`, `@ApiResponse`, `@Schema`) o *API-First* generando interfacce e DTO da specifica YAML con `openapi-generator-maven-plugin`.

---

### Domande tipiche a colloquio (e risposte da Senior)

- *D: Qual è la differenza sostanziale tra `PUT` e `PATCH`?*
  - **R**: `PUT` effettua una sostituzione completa della risorsa: tutti i campi non passati nel payload vengono tipicamente sovrascritti con i valori di default o `null`. `PATCH` applica invece una modifica parziale, aggiornando esclusivamente i campi specificati nel body della richiesta lasciando inalterati tutti gli altri.

- *D: Come implementi l'idempotenza su un endpoint di pagamento `POST /payments`?*
  - **R**: Tramite un header `Idempotency-Key` (UUID). Lato backend, prima di avviare il pagamento, si esegue un inserimento atomico della chiave su database con indice univoco (o su Redis con `SETNX`). Se la chiave è già presente ed è in stato completato, si restituisce immediatamente la risposta memorizzata in precedenza senza ripetere l'addebito sul circuito bancario.

- *D: Qual è la differenza tra lo status code `401 Unauthorized` e `403 Forbidden`?*
  - **R**: Il `401` riguarda l'**autenticazione**: il chiamante non ha fornito credenziali o il token JWT è scaduto/invalido. Il `403` riguarda l'**autorizzazione**: il chiamante è stato identificato con successo (sappiamo chi è), ma non possiede i ruoli o i permessi necessari per accedere alla risorsa richiesta.

---

### Come esercitarti
1. **API Design**: progetta la specifica REST completa per un servizio di emissione rimborsi (`/api/v1/refunds`), definendo verbi, URI, payload di request/response, codici di errore e header di idempotenza.
