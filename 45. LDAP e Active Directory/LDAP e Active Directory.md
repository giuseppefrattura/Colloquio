# 45. LDAP e Active Directory

## Una directory non è un normale database applicativo

**LDAP**, Lightweight Directory Access Protocol, permette di interrogare e modificare una directory gerarchica. La directory organizza identità e attributi in **entry**, elementi descritti da uno schema. Una **object class** stabilisce categorie e attributi ammessi o richiesti; il server applica lo schema e i permessi.

Il **DN**, Distinguished Name, identifica un elemento mediante il percorso completo. Il **RDN**, Relative Distinguished Name, è la parte relativa al suo contenitore. In `CN=Mario Rossi,OU=Users,DC=company,DC=com`, `CN` indica il nome comune, `OU` l'unità organizzativa e `DC` una componente del dominio. Il **Base DN** è il punto dal quale parte una ricerca.

Un'operazione **search** cerca entry usando base, ambito e filtro. Un filtro come `(uid=mario)` seleziona un attributo; input non fidato richiede escaping appropriato per evitare LDAP injection. Un filtro LDAP e un percorso DN hanno regole di escaping differenti.

## Autenticare mediante bind

Il **bind** associa un'identità alla connessione. Nel caso di bind con credenziali dell'utente, il server ne verifica l'autenticazione. Un'applicazione può prima cercare il DN attraverso un account tecnico con privilegi di lettura limitati e poi tentare il bind dell'utente.

La ricerca non autentica: trovare un nome non dimostra il possesso della credenziale. Anche il risultato del bind non attribuisce tutti i permessi applicativi. L'applicazione recupera gruppi o attributi secondo il contratto e li traduce nelle proprie politiche.

## Che cosa aggiunge Active Directory

**Active Directory Domain Services**, AD DS, è una piattaforma Microsoft che integra directory, LDAP e altri servizi di dominio. Un **domain controller** eroga i servizi del dominio; un'**Organizational Unit** organizza oggetti; un **security group** rappresenta un insieme di soggetti cui possono essere associati permessi.

L'**UPN**, User Principal Name, identifica comunemente un utente con forma simile a `nome@dominio`. Le **Group Policy** distribuiscono configurazioni e regole ai sistemi del dominio. **Kerberos** autentica attraverso ticket, riducendo la trasmissione ripetuta della password ai servizi. LDAP è quindi un protocollo usato dalla piattaforma, non un sinonimo di Active Directory.

## Proteggere il canale e gli account

**LDAPS** usa TLS fin dall'apertura del canale; **StartTLS** aggiorna una connessione LDAP a un canale protetto. In entrambi i casi il client deve validare certificato e nome del server. Il **truststore** Java contiene le autorità considerate fidate secondo la configurazione; disabilitare i controlli per superare un errore rimuove proprio quella verifica.

Un **service account** appartiene all'integrazione applicativa e ha privilegi minimi, rotazione e audit. Evita di legare il servizio alle credenziali personali di un dipendente. Password e altre credenziali richiedono distribuzione protetta e limiti di accesso.

## Integrare identità e autorizzazioni in Spring

Spring Security può usare un provider LDAP. Con `LdapBindAuthenticationManagerFactory` si configurano ricerca dell'utente e bind; gli **user DN pattern** sono una possibile alternativa quando il percorso è prevedibile. La ricerca dei gruppi alimenta le **authority**, permessi riconosciuti dall'applicazione.

```text
Gruppo directory: Payment-Operators
        → authority applicativa: PAYMENT_OPERATOR
        → regole sulle operazioni e sui conti consentiti
```

La traduzione non deve rendere ogni membro automaticamente amministratore. Si distinguono autenticazione, appartenenza a gruppi e autorizzazione sulle singole risorse. Pattern di utenti e filtri dipendono dallo schema reale: un esempio generico con `uid` non vale necessariamente per la directory aziendale.

## Disponibilità e integrazione con un Identity Provider

Pool di connessioni, timeout e monitoraggio limitano il costo della directory. I retry non devono moltiplicare tentativi su password errate né aggravare un domain controller già in difficoltà. La cache di gruppi può ridurre il carico ma ritardare la revoca: durata e dati cacheabili sono una scelta di sicurezza.

Un **Identity Provider** può integrare LDAP o AD ed esporre OIDC alle applicazioni. In questo modo i servizi non devono ricevere direttamente la password della directory. Rimangono da definire aggiornamento dei gruppi, revoca e comportamento in caso di indisponibilità del provider.

Per esercitarti, segui il login di un operatore e l'accesso a un pagamento. Spiega dove viene verificata la password, dove sono tradotti i gruppi e come un permesso revocato raggiunge l'applicazione.
