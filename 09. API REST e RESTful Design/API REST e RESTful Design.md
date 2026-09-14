# 9. API REST, Tecnologie Web, Sicurezza e Framework

## Cos'è e perché conta

Le API e le tecnologie web costituiscono l'interfaccia fondamentale tra i microservizi backend, le applicazioni frontend (web e mobile), i gateway di pagamento e i partner esterni. Uno sviluppatore Senior deve dominare sia l'**evoluzione del protocollo HTTP** (HTTP/1.1, HTTP/2, HTTP/3), sia le problematiche di sicurezza web (**Cookies, JWT, CORS, CSRF**), le strategie avanzate di **HTTP Caching** (ETag, Cache-Control, CDN) e saper orientarsi con disinvoltura tra i principali framework REST Java (**Spring MVC, JAX-RS/Jersey, Dropwizard**).

---

## 1. Evoluzione dei Protocolli Web: HTTP/1.1 vs HTTP/2 vs HTTP/3

```
                                EVOLUZIONE DEL PROTOCOLLO HTTP
       HTTP/1.1 (1997)                     HTTP/2 (2015)                     HTTP/3 (2020+)
 ┌───────────────────────────┐       ┌───────────────────────────┐       ┌───────────────────────────┐
 │ • Testuale                │       │ • Binario (Binary Framing)│       │ • Basato su QUIC (su UDP) │
 │ • 1 Richiesta per TCP     │       │ • Multiplexing su 1 TCP   │       │ • Zero Head-of-Line Block │
 │ • Head-of-Line Blocking   │       │ • Compressione HPACK      │       │ • Handshake 0-RTT / 1-RTT │
 └─────────────┬─────────────┘       └─────────────┬─────────────┘       └─────────────┬─────────────┘
               ▼                                   ▼                                   ▼
        Trasporto: TCP                      Trasporto: TCP                      Trasporto: UDP
```

### 1. HTTP/1.1
* Protocollo testuale basato su TCP. Supporta connessioni persistenti (`Keep-Alive`), ma soffre di **Head-of-Line (HoL) Blocking a livello applicativo**: su una singola connessione TCP, una richiesta lenta blocca tutte le richieste successive.

### 2. HTTP/2
* **Binary Framing Layer**: I messaggi sono suddivisi in frame binari (HEADERS, DATA) raggruppati in stream indipendenti.
* **Multiplexing Completo**: Centinaia di richieste e risposte viaggiano contemporaneamente su un'**unica connessione TCP** senza bloccarsi a vicenda.
* **Compressione HPACK**: Gli header HTTP ripetitivi vengono compressi eliminando ridondanze.

### 3. HTTP/3 & Protocollo QUIC
* Sostituisce il protocollo TCP con **QUIC (basato su UDP)**.
* **Elimina l'HoL Blocking a livello di trasporto**: Se un pacchetto va perso, solo il singolo stream interessato subisce il ritardo di ritrasmissione, mentre tutti gli altri stream continuano senza interruzioni.
* **Connection Migration**: Se un dispositivo mobile passa da rete Wi-Fi a 4G/5G, la connessione non si interrompe perché è identificata da un *Connection ID* a 64 bit e non dalla quadrupla IP/Porta TCP.

---

## 2. Gestione dello Stato, Sessioni, Cookies e JWT

```
                  SESSIONI STATEFUL vs TOKEN STATELESS (JWT)
        SESSION-BASED (Stateful)                      JWT TOKEN-BASED (Stateless)
   ┌─────────────────────────────────┐           ┌─────────────────────────────────┐
   │ • Server memorizza la sessione  │           │ • Server non memorizza stato    │
   │   in RAM o Redis (JSESSIONID)   │           │ • Il token contiene i claims    │
   │ • Revoca immediata facilissima  │           │ • Scalabilità orizzontale nativa│
   │ • Richiede memoria centralizzata│           │ • Revoca immediata complessa    │
   └─────────────────────────────────┘           └─────────────────────────────────┘
```

### 1. Sicurezza dei Cookie
I cookie HTTP inviati tramite l'header `Set-Cookie` devono essere blindati con 3 flag essenziali:
* **`HttpOnly`**: Impedisce l'accesso al cookie tramite script JavaScript (`document.cookie`), proteggendo il token da attacchi **XSS (Cross-Site Scripting)**.
* **`Secure`**: Il browser invia il cookie solo su connessioni cifrate **HTTPS** (TLS).
* **`SameSite`** (Protezione anti-CSRF):
  * `SameSite=Strict`: Il cookie non viene mai inviato in richieste cross-site (neppure cliccando su un link esterno).
  * `SameSite=Lax` (*Default moderno*): Il cookie viene inviato solo su navigazioni top-level sicure (GET da link esterni), ma bloccato su `POST` cross-site.
  * `SameSite=None`: Il cookie viene sempre inviato (richiede obbligatoriamente `Secure=true`).

---

### 2. Architettura JWT (JSON Web Token) & Token Rotation
Un JWT è composto da 3 parti separate da punti (`header.payload.signature`):
$$\text{Signature} = \text{HMAC-SHA256}(\text{Base64Url}(Header) + "." + \text{Base64Url}(Payload), \text{SecretKey})$$

* **Pattern di Autenticazione Robusto (Access Token + Refresh Token)**:
  1. **Access Token (JWT)**: Durata brevissima (5-15 minuti), memorizzato in memoria JavaScript o cookie `HttpOnly`, utilizzato nell'header `Authorization: Bearer <token>`.
  2. **Refresh Token**: Durata lunga (7-30 giorni), salvato in un cookie sicuro `HttpOnly` e su database/Redis.
  3. **Refresh Token Rotation**: Ogni volta che viene richiesto un nuovo Access Token, il server invalida il vecchio Refresh Token ed emette una nuova coppia; se un vecchio Refresh Token viene riutilizzato, scatta un allarme di furto credenziali e tutte le sessioni dell'utente vengono revocate.

---

### 3. Problematiche Web: CORS & CSRF

#### CORS (Cross-Origin Resource Sharing)
* Meccanismo di sicurezza del browser che impedisce a un'applicazione web caricata su un dominio (es. `https://app.frontend.com`) di fare chiamate API verso un'origine diversa (`https://api.bank.com`).
* **Richiesta Pre-Flight (`OPTIONS`)**: Per richieste non semplici (es. con header custom `Authorization` o `Content-Type: application/json`), il browser invia prima una `OPTIONS` con gli header:
  * `Origin: https://app.frontend.com`
  * `Access-Control-Request-Method: POST`
  * `Access-Control-Request-Headers: Authorization, Content-Type`
* Il backend risponde con:
  * `Access-Control-Allow-Origin: https://app.frontend.com` (mai `*` se si usano credenziali)
  * `Access-Control-Allow-Credentials: true`

#### CSRF (Cross-Site Request Forgery)
* Attacco in cui un sito malevolo induce il browser dell'utente a eseguire un'azione indesiderata su un'applicazione autenticata sfruttando l'invio automatico dei cookie di sessione.
* **Difesa**: Su API REST stateless protette da token JWT nell'header `Authorization`, il CSRF non sussiste (il browser non allega l'header automaticamente). Se si usano cookie di sessione, si impiega il flag `SameSite=Lax/Strict` e il pattern del **CSRF Synchronizer Token**.

---

## 3. HTTP Caching Avanzato & Strategie CDN

```
                              VALIDAZIONE DELLA CACHE HTTP
             Client / Browser                             Server Backend
                    │   GET /api/v1/tariffs                      │
                    │ ─────────────────────────────────────────► │
                    │   200 OK                                   │
                    │   ETag: "w/33a64df5514aa1"                 │
                    │   Cache-Control: public, max-age=3600      │
                    │ ◄───────────────────────────────────────── │
                    │                                            │
                    │   (Dopo 1 ora: Richiesta Condizionale)     │
                    │   GET /api/v1/tariffs                      │
                    │   If-None-Match: "w/33a64df5514aa1"        │
                    │ ─────────────────────────────────────────► │
                    │   304 Not Modified (Body Vuoto)            │
                    │ ◄───────────────────────────────────────── │
```

### Direttive `Cache-Control`:
* `public`: La risposta può essere memorizzata in cache da browser e intermediari (CDN, proxy).
* `private`: La risposta è destinata a un singolo utente e non deve essere salvata su cache condivise/CDN.
* `no-cache`: La risorsa può essere salvata in cache, ma **deve essere rivalidata con il server** (`ETag`) prima di ogni riutilizzo.
* `no-store`: La risposta contiene dati sensibili e **non deve mai essere memorizzata su disco o memoria di cache**.
* `max-age=N`: Durata di validità in secondi per il browser.
* `s-maxage=N`: Durata specifica per le cache condivise (CDN / Reverse Proxy).

### Validazione Condizionale con ETag:
* L'**ETag** è un identificatore univoco o hash del contenuto della risorsa.
* Il client memorizza l'ETag e, alla scadenza, invia una richiesta condizionale con l'header `If-None-Match: "<etag>"`.
* Se la risorsa non è cambiata, il server restituisce **`304 Not Modified` senza inviare il payload**, risparmiando banda e CPU.

---

## 4. Framework REST in Java: Spring MVC vs JAX-RS vs Dropwizard

```
┌──────────────────┬──────────────────────────┬─────────────────────────────┬───────────────────────────┐
│ Caratteristica   │ Spring Boot (Spring MVC) │ JAX-RS (Jersey / RESTEasy)  │ Dropwizard                │
├──────────────────┼──────────────────────────┼─────────────────────────────┼───────────────────────────┤
│ **Natura**       │ Framework completo enterprise│ Standard Jakarta EE / Spec  │ Lightweight REST Framework│
│ **Iniezione**    │ Spring Core IoC / DI     │ CDI / HK2                   │ Google Guice / Manuale    │
│ **Web Server**   │ Tomcat / Jetty / Undertow│ Qualsiasi servlet container │ Jetty embedded integrato  │
│ **JSON Engine**  │ Jackson (default)        │ Jackson / JSON-B            │ Jackson integrato         │
│ **Annotazioni**  │ `@RestController`        │ `@Path`, `@GET`, `@POST`    │ `@Path` (usa Jersey)      │
│                  │ `@GetMapping`, `@PostMapping`│ `@Produces`, `@Consumes`│                           │
│ **Filosofia**    │ Ecosistema onnicomprensivo│ Standard portabile         │ Minimalista e "out-of-box"│
└──────────────────┴──────────────────────────┴─────────────────────────────┴───────────────────────────┘
```

### 1. Spring MVC / Spring Web
Lo standard de facto dell'ecosistema enterprise Java:
```java
@RestController
@RequestMapping("/api/v1/payments")
public class PaymentRestController {

    private final PaymentService paymentService;

    public PaymentRestController(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    @PostMapping
    public ResponseEntity<PaymentResponse> create(@Valid @RequestBody PaymentRequest request) {
        PaymentResponse response = paymentService.execute(request);
        URI location = URI.create("/api/v1/payments/" + response.id());
        return ResponseEntity.created(location).body(response);
    }
}
```

### 2. JAX-RS (Jakarta RESTful Web Services / Jersey)
La specifica standard Java (molto usata in **Quarkus, WildFly, Micronaut**):
```java
@Path("/api/v1/payments")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class PaymentResource {

    @Inject
    private PaymentService paymentService;

    @POST
    public Response create(@Valid PaymentRequest request) {
        PaymentResponse response = paymentService.execute(request);
        URI location = URI.create("/api/v1/payments/" + response.getId());
        return Response.created(location).entity(response).build();
    }
}
```

### 3. Dropwizard
* Creato originariamente da Yammer; raggruppa librerie mature e collaudate (**Jetty per HTTP, Jersey per REST, Jackson per JSON, Metrics per monitoraggio**) in un pacchetto leggero e veloce, senza la complessità o il runtime pesante di Spring.

---

## 5. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come gestisci il caching a livello di CDN per evitare che gli utenti ricevano dati obsoleti dopo una modifica?*
  - **R**: Utilizzo due strategie complementari:
    1. **Cache-Control & ETag**: Imposto direttive `s-maxage` appropriate per la CDN e restituisco header `ETag` (hash del contenuto).
    2. **Cache Invalidation / Surrogate-Keys**: Per risorse a bassa frequenza di modifica, imposto cache lunga sulla CDN ma configuro un webhook di backend che esegue un *Purge/Invalidation* esplicito della cache sulla CDN (tramite API CloudFront/Akamai o invalidazione per tag) nel momento esatto in cui un'operazione di `UPDATE/DELETE` modifica il dato.

- *D: Perché non è sicuro memorizzare un token JWT sensibile nel `localStorage` del browser?*
  - **R**: Perché qualsiasi script JavaScript in esecuzione sulla pagina ha accesso completo a `localStorage`. Se l'applicazione subisce una vulnerabilità di tipo **XSS (Cross-Site Scripting)** tramite una libreria npm compromessa o un input non sanificato, l'attaccante può rubare il JWT ed impersonare l'utente. La memorizzazione sicura prevede un **cookie con flag `HttpOnly`, `Secure` e `SameSite=Strict/Lax`**, totalmente inaccessibile a JavaScript.

- *D: Che differenza c'è tra le annotazioni `@RestController` di Spring e `@Path` di JAX-RS?*
  - **R**: `@RestController` è un'annotazione proprietaria di Spring che combina `@Controller` e `@ResponseBody`, indicando che i valori di ritorno dei metodi vengono serializzati direttamente nel body HTTP tramite HttpMessageConverter. `@Path` fa parte dello standard formale JAX-RS (Jakarta REST) e viene utilizzata da framework compatibili (Jersey, RESTEasy, Quarkus) per definire l'URI base della risorsa, garantendo portabilità tra diversi application server conformi alle specifiche Jakarta EE.
