# 44. OAuth2, OpenID Connect e JWT — Advanced

## Obiettivo
Approfondire authentication e authorization a livello Senior, distinguendo chiaramente OAuth2, OpenID Connect e JWT e collegandoli alle API e ai microservizi.

## OAuth 2.0
OAuth2 è un framework per delegare l'accesso a risorse protette.

Concetti:
- Resource Owner
- Client
- Authorization Server
- Resource Server
- Access Token
- Refresh Token
- Scope

### Authorization Code + PKCE
Flusso tipico per applicazioni user-facing:
1. client avvia l'autorizzazione
2. utente autentica e concede il consenso
3. authorization server restituisce un authorization code
4. client scambia il code per token
5. access token viene utilizzato verso il resource server

PKCE protegge il code exchange soprattutto nei client pubblici.

### Client Credentials
Utilizzato per machine-to-machine communication quando non esiste un utente coinvolto.

Esempio: `Payment Service → Fraud Service`.

## OpenID Connect
OIDC estende OAuth2 aggiungendo un livello standard di **autenticazione e identità**.

Concetti:
- Identity Provider
- ID Token
- UserInfo endpoint
- Claims
- Discovery
- JWKS

### OAuth2 vs OIDC
- OAuth2: autorizzazione/accesso a risorse
- OIDC: autenticazione/identità sopra OAuth2

## JWT
Un JWT normalmente contiene:
- Header
- Payload
- Signature

La firma garantisce integrità e autenticità del token, non riservatezza.

### Claims
Esempi:
- `iss`
- `sub`
- `aud`
- `exp`
- `iat`
- `scope`
- `roles`

### Validazione
Il Resource Server dovrebbe verificare almeno:
- firma
- issuer
- audience
- expiration
- eventuali scope/ruoli richiesti

## Access Token vs Refresh Token
L'access token viene utilizzato per accedere alle API e dovrebbe avere lifetime limitata.

Il refresh token permette di ottenere nuovi access token senza richiedere nuovamente il login, con policy di sicurezza e revoca appropriate.

## JWKS e Key Rotation
Il Resource Server può recuperare le chiavi pubbliche dall'endpoint JWKS dell'Identity Provider.

La rotazione delle chiavi deve permettere un periodo di sovrapposizione in cui sia possibile validare token firmati con la chiave precedente mentre i nuovi token usano la nuova chiave.

## Authorization
- RBAC: permessi associati a ruoli
- ABAC: decisione basata su attributi di utente, risorsa e contesto
- Scopes: permessi delegati tipicamente associati all'access token

## Security pitfalls
- token troppo longevi
- mancata validazione `aud`/`iss`
- secret hardcoded
- log di access token
- uso improprio di OAuth2 come autenticazione
- assenza di TLS
- gestione insicura dei refresh token

## API Security Architecture
`Client → API Gateway → Resource Server → Authorization Server`

Il Gateway può applicare rate limiting e policy comuni, mentre l'autorizzazione business-specific dovrebbe rimanere nel servizio che possiede il dominio.

## Domande da colloquio
1. OAuth2 vs OpenID Connect?
2. JWT è cifrato o firmato?
3. Authorization Code vs Client Credentials?
4. Perché usare PKCE?
5. Access token vs refresh token?
6. Come valida un Resource Server un JWT?
7. Cos'è JWKS?
8. Come gestisci key rotation?
9. RBAC vs ABAC?
10. Dove implementeresti authorization in una architettura a microservizi?
