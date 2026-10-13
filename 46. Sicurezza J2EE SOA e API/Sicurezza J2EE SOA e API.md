# 46. Sicurezza in Java enterprise, SOA e API

## Proprietà da conservare lungo l'integrazione

L'autenticazione verifica l'identità; l'autorizzazione limita le azioni. La **riservatezza** impedisce letture non autorizzate, l'**integrità** protegge da modifiche non consentite e la **disponibilità** consente l'uso del servizio. L'**accountability** permette di ricostruire azioni e responsabilità mediante evidenze e audit. Queste proprietà devono attraversare i confini tra applicazioni, non fermarsi al login.

Minimo privilegio, difesa su più livelli e secure by design guidano il progetto. **Fail secure** significa che un guasto non deve aprire accessi prima vietati. Un filtro che accetta tutto quando la directory non risponde potrebbe ripristinare il traffico compromettendo l'autorizzazione.

## Sicurezza gestita dal container

Nei sistemi J2EE e Jakarta EE il container può gestire l'autenticazione Servlet e controllare l'accesso alle risorse. La **container-managed security** separa parte della politica dal codice di business. Un **security realm** rappresenta il dominio di autenticazione configurato nel prodotto; i **role** collegano identità e permessi.

La sicurezza **dichiarativa** usa configurazioni e annotazioni; quella **programmatica** esegue controlli nel codice, per esempio sui ruoli della richiesta. Nel descrittore `web.xml`, un **security constraint** collega percorsi e ruoli:

```xml
<security-constraint>
    <web-resource-collection>
        <web-resource-name>Payments</web-resource-name>
        <url-pattern>/payments/*</url-pattern>
    </web-resource-collection>
    <auth-constraint>
        <role-name>PAYMENT_OPERATOR</role-name>
    </auth-constraint>
</security-constraint>
```

Questo frammento dichiara un vincolo, ma non configura da solo autenticazione, mapping dei ruoli e trasporto. **JACC**, Java Authorization Contract for Containers, definisce un contratto per l'integrazione di decisioni di autorizzazione nei container; rilevanza e supporto dipendono dalla generazione della piattaforma.

## JAAS nei sistemi esistenti

**JAAS**, Java Authentication and Authorization Service, separa alcuni meccanismi di autenticazione dal codice chiamante. Il **LoginContext** coordina i moduli di login configurati; un **LoginModule** verifica credenziali secondo il proprio meccanismo. Il **Subject** rappresenta il soggetto autenticato e può contenere **Principal**, identità o attributi riconosciuti.

Il modello storico di autorizzazione JAAS va letto nel contesto del runtime Java e del container usato. Conoscere Subject e LoginModule aiuta a capire un'integrazione legacy, ma non significa che ogni nuova API debba adottare quella stessa architettura.

## SOA: proteggere trasporto e messaggio

Una **Service-Oriented Architecture**, SOA, integra servizi tramite contratti; nelle piattaforme enterprise può usare SOAP e XML. Il **message tampering** modifica un messaggio, l'**impersonation** presenta una falsa identità e il **replay attack** reinvia un messaggio valido per ripeterne l'effetto.

TLS protegge il canale tra due endpoint. Con un gateway intermedio il messaggio viene elaborato e può essere inoltrato su un altro canale. La **message-level security** protegge elementi del messaggio stesso, consentendo alcune verifiche anche attraverso intermediari, purché questi rispettino le parti protette.

## WS-Security e XML

**WS-Security** definisce meccanismi per inserire token e protezioni nei messaggi SOAP, spesso nel SOAP Header. Un **UsernameToken** trasporta informazioni di autenticazione secondo un profilo; non elimina il bisogno di proteggere le credenziali. **XML Signature** firma parti del messaggio, mentre **XML Encryption** ne cifra parti. I certificati possono sostenere autenticazione e verifica della firma.

La firma non garantisce freschezza. Un timestamp delimita il periodo accettabile; un **nonce**, valore usato una volta, e una registrazione delle richieste già viste possono contribuire alla protezione dal replay. Il ricevente deve verificare sia le parti firmate sia che siano proprio quelle interpretate dal codice di business. Firmare un elemento e usare un altro elemento non fidato vanifica il controllo.

I parser XML devono essere configurati rispetto a entità esterne, espansione e dimensioni. **XXE** può indurre accessi a risorse locali o remote; l'espansione di entità può esaurire risorse. La sicurezza del protocollo non rende sicuro un parser configurato male.

## SAML e federazione dell'identità

**SAML**, Security Assertion Markup Language, scambia dichiarazioni XML sull'identità. L'**Identity Provider**, IdP, autentica; il **Service Provider**, SP, riceve una **assertion** destinata a lui. Un authentication statement descrive l'autenticazione e gli attributi portano informazioni autorizzate sul soggetto.

Il **Single Sign-On**, SSO, consente di usare l'autenticazione del provider per più applicazioni. Il ricevente verifica firma, destinatario, tempi e collegamento al flusso atteso: una assertion non è una credenziale universale. OIDC affronta la federazione con un modello differente, costruito su OAuth 2.0; la scelta dipende dai sistemi da integrare.

## Portare le stesse proprietà sulle API

Un'**API key** identifica un client o un accesso secondo il contratto. Basic Authentication trasmette credenziali codificate, non cifrate autonomamente. Un **bearer token** consente l'accesso a chi lo possiede; mTLS associa l'accesso a un certificato client. Le **signed request** legano una firma ai dati della richiesta e richiedono regole di canonicalizzazione e protezione dal replay.

OAuth e OIDC separano delega e autenticazione. Per un JWT firmato, il resource server verifica firma, `iss`, `aud` e tempi, poi scope e politiche sulla risorsa. Il capitolo 44 sviluppa il flusso completo. RBAC usa ruoli; ABAC attributi; l'autorizzazione resource-based considera anche appartenenza e stato dell'oggetto.

## Rischi che attraversano tutti gli strati

Il **broken access control** consente azioni o letture indebite. Una misconfiguration espone funzioni o risorse non previste. L'injection interpreta input come istruzioni; una deserializzazione insicura può accettare strutture o tipi pericolosi. L'**excessive data exposure** restituisce dati oltre il necessario, mentre il **mass assignment** permette di modificare campi che il client non dovrebbe controllare, come lo stato di approvazione.

Un gateway centralizza routing, limiti di richiesta e controlli comuni, ma il servizio mantiene i permessi sul dominio. La **TLS termination** conclude il canale TLS al gateway: il collegamento successivo richiede una decisione propria. Correlation ID e audit collegano le operazioni senza sostituire l'autorizzazione.

Per le chiamate tra servizi si usano identità dedicate, token a durata limitata e permessi minimi. La **workload identity** associa credenziali al carico applicativo attraverso la piattaforma, riducendo la necessità di distribuire segreti statici. Rotazione e revoca devono coprire anche queste identità.

## Input, output e audit

Payload, parametri, header e file richiedono vincoli su tipo, contenuto e dimensione. Gli errori pubblici non espongono stack trace o dettagli SQL. L'audit registra accessi sensibili, modifiche ai privilegi e operazioni amministrative con protezioni contro alterazione e lettura indebita. Non deve contenere password, token, segreti o numeri completi di carta non necessari.

## Un'integrazione da seguire fino al sistema legacy

Immagina una nuova API REST davanti a un servizio SOAP autenticato tramite Active Directory. Il client usa OIDC per il login e un access token per l'API; il servizio integra il legacy mediante un'identità dedicata, TLS e le protezioni WS-Security richieste. In ogni passaggio si chiariscono soggetto rappresentato, destinatario e permessi.

Il punto delicato è la traduzione della fiducia: il servizio legacy non deve attribuire a ogni chiamata i privilegi massimi dell'account tecnico. Per esercitarti, descrivi come vengono conservati identità, autorizzazione e riferimenti di audit e come viene impedito il replay di un'operazione sensibile.
