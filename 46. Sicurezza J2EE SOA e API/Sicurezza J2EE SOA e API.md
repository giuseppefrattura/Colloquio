# 46. Sicurezza applicativa in J2EE, SOA e API

## Obiettivo
Prepararsi alle domande sulla sicurezza applicativa nei sistemi Java enterprise tradizionali (J2EE/Jakarta EE), nelle architetture SOA e nelle moderne API REST/microservizi.

## 1. Security principles
I principi fondamentali sono:
- Authentication
- Authorization
- Confidentiality
- Integrity
- Availability
- Accountability / Auditing
- Least Privilege
- Defense in Depth
- Secure by Design
- Fail Secure

Distinguere sempre **chi è l'utente** da **cosa è autorizzato a fare**.

## 2. Sicurezza J2EE / Jakarta EE
Nei sistemi enterprise Java tradizionali la sicurezza può essere applicata a livello di container e applicazione.

Concetti:
- Servlet authentication
- Container-managed security
- Security constraints
- Roles
- JAAS
- Security realms
- JACC
- `web.xml`
- declarative security
- programmatic security

Esempio concettuale:
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

L'idea fondamentale è separare la configurazione delle policy di sicurezza dal codice business quando il modello container-managed è appropriato.

## 3. JAAS
Java Authentication and Authorization Service permette di separare il processo di autenticazione dall'applicazione attraverso LoginModule e Subject/Principal.

Concetti da conoscere:
- Subject
- Principal
- LoginContext
- LoginModule
- authentication
- authorization

È soprattutto importante come conoscenza dei sistemi Java enterprise/legacy; nelle architetture moderne è spesso sostituito o affiancato da Spring Security, OAuth2/OIDC e Identity Provider esterni.

## 4. SOA Security
In una Service-Oriented Architecture i servizi possono essere SOAP/XML o altri protocolli enterprise.

Principali rischi:
- intercettazione del traffico
- message tampering
- replay attack
- impersonation
- XML attacks
- eccessivi privilegi
- service-to-service trust non controllato

Contromisure:
- TLS
- mutual TLS
- authentication
- authorization
- message-level security
- digital signatures
- encryption
- timestamps
- nonce/replay protection
- auditing

## 5. WS-Security
Per SOAP, WS-Security fornisce meccanismi di sicurezza a livello messaggio.

Concetti fondamentali:
- SOAP Header
- UsernameToken
- XML Signature
- XML Encryption
- Security Token
- Timestamp
- replay protection
- certificate-based authentication

### Transport vs Message Security
**TLS** protegge il canale di comunicazione.

**WS-Security** protegge il messaggio SOAP stesso e può mantenere le proprietà di integrità/autenticità anche quando il messaggio attraversa più intermediari.

Esempio architetturale:
```text
Client
  ↓ HTTPS
Gateway
  ↓ SOAP / WS-Security
Service A
  ↓ SOAP / WS-Security
Service B
```

## 6. SAML
SAML è uno standard XML per lo scambio di assertion relative a identità e autenticazione, molto usato in scenari enterprise SSO.

Concetti:
- Identity Provider
- Service Provider
- Assertion
- Authentication Statement
- Attributes
- SSO

Confronto:
- SAML: molto comune nell'enterprise e nelle integrazioni SSO legacy
- OIDC: approccio moderno basato su OAuth2/JSON/JWT, particolarmente adatto a web e API

## 7. API Security
Una API deve proteggere almeno:
- Authentication
- Authorization
- Input validation
- Rate limiting
- TLS
- Secrets
- Audit
- Error handling

Pattern comuni:
```text
Client
  ↓ TLS
API Gateway
  ↓ Authentication / Rate limiting
Resource Server
  ↓ Authorization
Business Service
  ↓
Database
```

## 8. API Authentication
Meccanismi da conoscere:
- API Key
- Basic Authentication
- OAuth2 Bearer Token
- JWT
- mTLS
- signed requests

In generale evitare Basic Authentication per nuove API se esistono alternative adeguate; usare sempre TLS quando vengono trasmesse credenziali o token.

## 9. OAuth2 / OIDC / JWT
### OAuth2
Framework per delegare l'accesso a risorse protette.

### OIDC
Estensione di OAuth2 per authentication e identity.

### JWT
Formato di token firmato che contiene claims.

Validare sempre:
- signature
- issuer
- audience
- expiration
- not-before quando applicabile
- scopes/roles

Non inserire dati sensibili inutili nei JWT e non confondere firma con cifratura.

## 10. Authorization
Possibili modelli:
- RBAC
- ABAC
- scope-based authorization
- resource-based authorization

Esempio:
```text
JWT
 ├── sub = user123
 ├── scope = payment.read payment.write
 └── roles = PAYMENT_OPERATOR
          ↓
Authorization policy
          ↓
POST /payments → payment.write
```

## 11. OWASP e minacce API
Conoscere almeno:
- Broken Access Control
- Injection
- Security Misconfiguration
- Cryptographic Failures
- Identification and Authentication Failures
- SSRF
- XSS quando esiste una componente browser
- insecure deserialization
- excessive data exposure
- mass assignment
- rate abuse

## 12. API Gateway e Security Boundary
Il Gateway può centralizzare:
- TLS termination
- authentication
- rate limiting
- request size limits
- routing
- audit/correlation ID

Ma non deve diventare l'unico punto di authorization: i microservizi devono verificare le autorizzazioni necessarie alle proprie risorse e regole di dominio.

## 13. Service-to-Service Security
In un'architettura a microservizi valutare:
- OAuth2 Client Credentials
- mTLS
- workload identity
- short-lived tokens
- least privilege
- secret rotation

Non usare un'unica credenziale condivisa da tutti i microservizi.

## 14. Input e output security
Validare:
- payload JSON/XML
- parametri URL
- headers
- file upload
- content type
- dimensioni massime

Per XML considerare:
- XXE
- entity expansion
- external entity access
- parser hardening

Non restituire stack trace, SQL exception o dettagli infrastrutturali al client.

## 15. Security logging e auditing
Registrare eventi rilevanti:
- login riusciti/falliti
- authorization failures
- modifiche ai privilegi
- accesso a dati sensibili
- operazioni amministrative
- eventi di sicurezza

Non loggare:
- password
- access token
- refresh token
- secret
- PAN completo o altri dati sensibili non necessari

## 16. Domande da colloquio
1. Come proteggeresti una applicazione J2EE?
2. Container-managed security vs programmatic security?
3. Cos'è JAAS?
4. Cos'è WS-Security?
5. TLS e WS-Security risolvono lo stesso problema?
6. XML Signature vs XML Encryption?
7. Cos'è SAML e quando lo useresti?
8. OAuth2 vs OIDC?
9. JWT è cifrato o firmato?
10. Come proteggi una REST API?
11. Dove metti authentication e authorization in una architettura con API Gateway?
12. Come proteggi la comunicazione tra microservizi?
13. Come previeni replay attack?
14. Come gestisci la rotazione dei secret e delle chiavi?
15. Come proteggeresti una SOAP API legacy?
16. Quali rischi specifici presenta XML?

## Scenario Senior
Supponiamo di dover integrare una nuova API REST con un sistema legacy SOAP/J2EE autenticato tramite Active Directory.

Una possibile architettura è:
```text
User / Client
      ↓ OAuth2 / OIDC
API Gateway
      ↓ JWT
REST Service
      ↓ service identity / mTLS
Integration Service
      ↓ WS-Security + TLS
Legacy SOAP/J2EE
      ↓
LDAP / Active Directory
```

Il punto importante non è usare una singola tecnologia ovunque, ma creare **security boundaries** chiari e tradurre correttamente identità, autorizzazioni e trust tra sistemi moderni e legacy.

## Regola Senior
La sicurezza non è una singola libreria o un filtro HTTP. È una proprietà dell'intera architettura: **identity, transport security, message security, authorization, secrets, input validation, auditing, monitoring e gestione del ciclo di vita delle credenziali** devono essere progettati insieme.
