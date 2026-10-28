# 38. Sicurezza avanzata e governo delle API

## Distinguere identità e permessi

L'**autenticazione** verifica l'identità; l'**autorizzazione** decide se quell'identità può eseguire un'azione su una risorsa. Un operatore autenticato non deve poter leggere un pagamento di un altro cliente soltanto perché ne conosce l'identificatore. Il controllo va applicato alla risorsa e alle regole del servizio.

**OAuth 2.0** consente la delega di accesso mediante token. **OpenID Connect**, o OIDC, aggiunge informazioni standard di autenticazione. Il flusso Authorization Code usa un codice temporaneo poi scambiato per token; **PKCE** lega lo scambio al client che ha iniziato il flusso. Client Credentials rappresenta invece un'applicazione che opera con una propria identità. Il capitolo 44 segue questi passaggi e distingue access token, refresh token e ID token.

Un **JWT**, JSON Web Token, è un formato per trasportare dichiarazioni, chiamate *claims*. Un JWT firmato protegge l'integrità, ma il contenuto resta leggibile. Le chiavi pubbliche possono essere pubblicate in un **JWKS**, JSON Web Key Set. Verificare la firma è soltanto una parte della validazione: contano anche emittente, destinatario e scadenza.

Con **RBAC** i permessi sono associati a ruoli. Con **ABAC** la decisione usa attributi di soggetto, risorsa e contesto. Un ruolo «operatore» può consentire l'accesso al servizio, mentre una politica sugli attributi limita le operazioni ai clienti assegnati.

## Proteggere canale, browser e input

**TLS** protegge il canale di comunicazione; **mTLS** autentica anche il client mediante certificato. I certificati richiedono gestione di fiducia, scadenze e rotazione. La cifratura del canale non sostituisce l'autorizzazione sulle risorse.

**CORS** regola quali origini un browser può usare per leggere risposte cross-origin. Non impedisce a un client esterno al browser di chiamare l'API. **CSRF** induce il browser a inviare una richiesta con credenziali aggiunte automaticamente; **XSS** esegue codice ostile nel contesto della pagina. Sono minacce diverse e richiedono misure diverse, come token anti-CSRF o encoding dell'output appropriato al contesto.

La **SQL injection** altera una query costruita concatenando input non fidato; si usano parametri e query strutturate. La **SSRF** induce il server a contattare destinazioni scelte dall'attaccante; occorrono controlli sulle destinazioni e sull'accesso di rete. OWASP raccoglie categorie di rischio utili per la revisione, ma una lista non dimostra che il sistema sia protetto.

Il **least privilege**, minimo privilegio, limita le capacità di ciascuna identità. La rotazione dei segreti sostituisce periodicamente credenziali e chiavi, con un percorso che evita interruzioni e revoca quelle compromesse. Il capitolo 49 sviluppa queste misure a livello di codice.

## Governare un contratto nel tempo

La **API governance** stabilisce regole condivise per progettazione, pubblicazione, cambiamento e dismissione delle API. OpenAPI descrive il contratto HTTP; un modello di errore uniforme aiuta i client a distinguere validazione, autorizzazione e guasto temporaneo.

La **backward compatibility** permette ai client esistenti di continuare a funzionare. Una **breaking change** rompe un'aspettativa: togliere un campo è un esempio, ma anche cambiarne significato può rompere il comportamento. Il versionamento rende esplicita la transizione; non elimina il bisogno di una finestra di migrazione e di conoscere i consumer.

I **contract test** verificano aspettative concordate tra producer e consumer prima del rilascio. Vanno integrati con esempi reali e osservazione dell'uso dell'API: uno schema formalmente valido può comunque rappresentare un cambiamento semantico.

## Applicare le regole a un caso concreto

Un gateway può centralizzare controllo dei token, limite di richieste e instradamento. Il servizio dei pagamenti deve ancora verificare che il soggetto possa operare su quel conto e quell'importo. Per esercitarti, progetta una modifica al contratto di pagamento e spiega come manterresti i client precedenti, come comunicheresti la dismissione e quali controlli impedirebbero accessi indebiti.

## Sicurezza architetturale e confini di fiducia

Consideriamo client, API gateway, servizio ordini, servizio pagamenti, database e Kafka. Un **confine di fiducia** è un passaggio in cui cambiano identità, responsabilità o livello di controllo: per ciascuno occorre stabilire chi può accedere, a quali risorse e con quali prove di identità.

- **Least privilege:** il servizio notifiche riceve solo i permessi indispensabili; non ha bisogno di modificare i pagamenti.
- **Defense in depth:** TLS, autenticazione, autorizzazione, validazione e restrizioni di rete si rafforzano a vicenda.
- **Zero trust:** la sola posizione nella rete interna non rende affidabile una richiesta; anche la comunicazione tra servizi richiede identità e autorizzazione adeguate.
- **Separazione dei dati:** limitare accessi diretti a database e segreti riduce l'impatto di un servizio compromesso.

In pratica si prevedono TLS e, dove appropriato, mTLS; secret manager e rotazione delle credenziali; query parametrizzate e validazione degli input; minimizzazione dei dati, audit senza password o token, timeout e limiti di richiesta. Per Kafka si applicano autenticazione e ACL sui topic, valutando anche chi può leggere gli eventi e per quanto tempo vengono conservati.

Il **threat modeling** parte da asset, attori, punti di ingresso e confini, identifica minacce e valuta mitigazioni e verifiche. Un gateway può centralizzare controlli, ma il servizio deve comunque verificare che un utente possa accedere allo specifico ordine o conto richiesto.

**Risposta da colloquio:** «Progetto la sicurezza lungo l'intero percorso della richiesta: identità verificabile, autorizzazione sulla risorsa, minimo privilegio e controlli indipendenti per contenere l'impatto di un guasto o di una compromissione».
