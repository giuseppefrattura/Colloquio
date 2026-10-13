# 44. OAuth 2.0, OpenID Connect e JWT

## Tre concetti con ruoli diversi

OAuth 2.0 delega l'accesso a risorse. OpenID Connect, o OIDC, aggiunge un livello di autenticazione e identità. JWT definisce un formato di token: non è un flusso di login e non è obbligatorio per ogni access token OAuth.

Il **resource owner** è il soggetto titolare dell'accesso; il **client** richiede la delega; l'**authorization server** emette i token; il **resource server** protegge le API. Uno **scope** rappresenta un ambito di accesso delegato. Un utente può autorizzare un'applicazione a leggere dati senza concederle la propria password.

## Seguire Authorization Code con PKCE

Il client avvia l'autorizzazione tramite il browser. L'authorization server autentica l'utente e, secondo la politica applicabile, acquisisce il consenso. Restituisce un codice temporaneo a un redirect URI registrato. Il client scambia il codice al token endpoint e usa l'access token per l'API.

Con **PKCE**, Proof Key for Code Exchange, il client genera un verificatore e invia inizialmente una challenge derivata. Lo scambio del codice richiede il verificatore, rendendo insufficiente il possesso del solo codice intercettato. Il flusso deve proteggere anche redirect e collegamento con la richiesta iniziale. Le indicazioni di sicurezza e l'uso di PKCE sono descritti nella [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html).

**Client Credentials** è il flusso per un'applicazione che agisce con i propri privilegi, senza rappresentare la sessione di un utente. Un servizio pagamenti può usarlo per invocare un servizio antifrode con scope limitati. Non è una scorciatoia per impersonare ogni utente.

## Identità OIDC e token per le API

OIDC introduce l'**ID token**, destinato al client per descrivere l'autenticazione dell'utente. Non va confuso con l'access token destinato al resource server. Le **claims** sono dichiarazioni sul soggetto o sul token. L'endpoint **UserInfo** può fornire informazioni autorizzate; la **discovery** pubblica metadati e indirizzi del provider.

L'**access token** accompagna le chiamate alle API e ha una durata e un destinatario definiti. Il **refresh token** permette di richiedere nuovi access token ed è trattato come una credenziale sensibile. Emissione, conservazione, rotazione e revoca dipendono dal tipo di client e dalla politica di sicurezza; non si invia il refresh token a ogni servizio.

## Leggere e validare un JWT

Un JWT firmato in rappresentazione compatta comprende header, payload e firma. L'header descrive parametri della protezione, il payload contiene claims e la firma protegge integrità e autenticità entro il modello di fiducia. La codifica non nasconde il contenuto. Un token cifrato usa un'altra struttura e non va descritto come il medesimo formato a tre parti.

`iss` identifica l'emittente, `sub` il soggetto, `aud` il destinatario e `exp` la scadenza. `iat` indica l'emissione; `nbf`, se presente, il momento prima del quale il token non è valido. Scope e ruoli hanno significato secondo il contratto del provider, non sono permessi automaticamente universali.

Il resource server verifica firma con algoritmi consentiti, emittente atteso, audience corretta e vincoli temporali. Poi applica l'autorizzazione alla risorsa. Decodificare il payload non significa validarlo; una firma valida di un emittente inatteso non rende il token accettabile.

## Chiavi, rotazione e revoca

Un **JWKS**, JSON Web Key Set, pubblica chiavi che consentono la verifica; il parametro `kid` aiuta a selezionare la chiave prevista. L'endpoint viene configurato o ottenuto da metadati fidati, non scelto liberamente da un token non verificato. La cache delle chiavi riduce dipendenze per richiesta ma richiede gestione delle chiavi sconosciute e dei guasti.

Nella rotazione ordinaria una finestra di sovrapposizione può permettere ai token ancora validi di usare la vecchia chiave. Una chiave compromessa richiede invece una risposta coerente con la revoca. Validazione locale e scadenze lunghe rendono difficile invalidare immediatamente ogni token: questa conseguenza va progettata.

## Autorizzazione lungo l'architettura

RBAC associa permessi a ruoli; ABAC usa attributi e contesto; gli scope delimitano la delega. Il gateway può applicare controlli comuni, mentre il resource server protegge le regole e i dati che possiede. Il client ottiene il token dall'authorization server e poi lo presenta all'API: non ogni chiamata richiede un nuovo login presso il provider.

Per esercitarti, disegna separatamente il login e una chiamata all'API. Indica chi riceve codice, ID token, access token e refresh token, e spiega quale controllo impedisce a un token valido per un'altra API di essere accettato.
