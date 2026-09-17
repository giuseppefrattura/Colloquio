# 45. LDAP e Active Directory

## Obiettivo
Comprendere come integrare applicazioni Java enterprise con directory aziendali come LDAP e Microsoft Active Directory, distinguendo autenticazione, ricerca delle identità e autorizzazione.

## LDAP
LDAP (Lightweight Directory Access Protocol) è un protocollo per interrogare e modificare directory gerarchiche.

Concetti fondamentali:
- Directory Server
- Entry
- DN (Distinguished Name)
- RDN (Relative Distinguished Name)
- Attribute
- Object Class
- Schema
- Base DN
- Bind
- Search
- Filter

Esempio concettuale:
```text
DC=company,DC=com
 ├── OU=Users
 │    ├── CN=Mario Rossi
 │    └── CN=Anna Bianchi
 └── OU=Groups
      ├── CN=Developers
      └── CN=Admins
```

## LDAP Authentication
Un'applicazione può autenticare un utente effettuando un bind con le sue credenziali oppure utilizzando un account tecnico per cercare l'utente e successivamente verificarne le credenziali.

Flusso tipico:
```text
User
  ↓ username/password
Application
  ↓ LDAP search
Directory
  ↓ user DN
Application
  ↓ bind/authentication
LDAP Server
  ↓ success/failure
Application
```

## Active Directory
Microsoft Active Directory Domain Services (AD DS) utilizza LDAP per l'accesso alla directory, ma offre anche altri meccanismi e servizi, tra cui Kerberos, DNS e gestione centralizzata di utenti, gruppi e computer.

Concetti da conoscere:
- Domain
- Domain Controller
- Organizational Unit (OU)
- Security Group
- User Principal Name (UPN)
- Service Account
- Group Policy
- Kerberos
- LDAP/LDAPS

## LDAP vs Active Directory
LDAP è principalmente un protocollo; Active Directory è una piattaforma directory completa di Microsoft che implementa LDAP e integra altri servizi di dominio.

## LDAPS e sicurezza
LDAP in chiaro espone le credenziali e i dati della directory. Per proteggere la comunicazione utilizzare:
- LDAPS (LDAP over TLS)
- LDAP con StartTLS
- certificati validati correttamente
- truststore Java configurato correttamente

Non disabilitare la verifica dei certificati per risolvere problemi TLS in produzione.

## Spring Security + LDAP
Spring Security può integrare LDAP come Authentication Provider.

Concetti:
- `LdapBindAuthenticationManagerFactory`
- LDAP search
- user DN patterns
- group search
- authorities
- password validation

Esempio concettuale:
```java
@Bean
AuthenticationManager ldapAuthenticationManager(BaseLdapPathContextSource contextSource) {
    LdapBindAuthenticationManagerFactory factory =
        new LdapBindAuthenticationManagerFactory(contextSource);
    factory.setUserSearchBase("ou=Users");
    factory.setUserSearchFilter("(uid={0})");
    return factory.createAuthenticationManager();
}
```

## Authentication vs Authorization
LDAP/AD può fornire l'identità e i gruppi dell'utente, ma l'applicazione deve decidere come trasformare quei gruppi in autorizzazioni applicative.

Esempio:
```text
AD Group: CN=Payment-Operators
          ↓
Application authority: PAYMENT_OPERATOR
          ↓
@PreAuthorize("hasAuthority('PAYMENT_OPERATOR')")
```

## Service Accounts
Per integrazioni applicative usare account tecnici dedicati con:
- privilegi minimi
- password/secret gestiti tramite secret manager
- rotazione delle credenziali
- audit degli accessi
- divieto di utilizzo di account personali

## Caching e disponibilità
LDAP può diventare una dipendenza critica. Valutare:
- connection pooling
- timeout
- retry controllati
- caching delle informazioni non sensibili quando appropriato
- fallback limitati
- monitoring della directory

Non usare retry aggressivi su LDAP: un Domain Controller degradato può essere ulteriormente sovraccaricato.

## Integrazione enterprise
Architettura tipica:
```text
Browser / Client
      ↓
API Gateway
      ↓
Spring Boot Application
      ↓
Spring Security
      ↓
LDAP / Active Directory
      ↓
Gruppi / Identità
```

In architetture moderne LDAP/AD può essere integrato anche con un Identity Provider che espone OAuth2/OIDC, evitando di propagare direttamente le credenziali LDAP alle applicazioni.

## Domande da colloquio
1. Cos'è LDAP?
2. LDAP e Active Directory sono la stessa cosa?
3. Cos'è un DN?
4. Differenza tra LDAP e LDAPS?
5. Cos'è un bind LDAP?
6. Come integreresti Active Directory con Spring Security?
7. Come trasformi i gruppi AD in ruoli applicativi?
8. Perché usare un service account?
9. Come gestisci timeout e indisponibilità del Domain Controller?
10. LDAP authentication vs OAuth2/OIDC: quando useresti ciascuno?
11. Come proteggeresti le credenziali LDAP?
12. Perché non conviene far dipendere ogni microservizio direttamente da AD?

## Regola Senior
LDAP/Active Directory è spesso un sistema di identità enterprise. In una nuova architettura è importante separare **identity provider, autenticazione e autorizzazione applicativa**, evitando di distribuire credenziali directory tra i microservizi.
