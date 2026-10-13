# 49. Programmazione difensiva e codice sicuro

## Esplicitare ciò che il codice può accettare

La **programmazione difensiva** rende espliciti input ammessi, invarianti e comportamento in caso di errore. Il principio **secure by design** inserisce la protezione nelle scelte iniziali: permessi, confini, gestione dei dati e recupero. La **defense in depth**, difesa su più livelli, evita che un solo controllo mancato comprometta l'intero sistema.

Ogni confine può portare dati inattesi: una richiesta HTTP, un header, un file, un messaggio o una risposta di un partner. Validare significa controllare tipo, formato, lunghezza, encoding, intervallo e significato di business. Un importo numericamente valido può appartenere a una valuta non supportata o eccedere un limite operativo.

```java
if (amount == null || amount.signum() <= 0) {
    throw new IllegalArgumentException("L'importo deve essere positivo");
}
```

L'esempio ammette soltanto importi positivi; un dominio che consenta importi zero deve dichiarare un'altra regola. In Bean Validation, `@NotNull`, `@Size`, `@Pattern` e `@Positive` esprimono vincoli, mentre `@Valid` attiva la validazione anche sugli oggetti collegati e `@Validated` supporta la validazione Spring nei contesti configurati. I vincoli semplici non sostituiscono le regole che coinvolgono più dati.

## Fallire presto e fallire in sicurezza

**Fail fast** significa riconoscere subito una condizione non valida, evitando che l'errore emerga lontano dalla causa. **Fail secure** significa mantenere le proprietà di sicurezza durante un guasto. **Fail open** permette invece l'accesso quando il controllo non è disponibile: per un'autorizzazione sensibile potrebbe essere una violazione, non un miglioramento della disponibilità.

Se il servizio dei permessi non risponde, il percorso previsto deve impedire accessi indebiti oppure usare una politica locale esplicitamente valida. La scelta non può dipendere da un `catch` che restituisce automaticamente successo.

## Errori, null e risorse

Le eccezioni specifiche aiutano a distinguere un pagamento rifiutato da una dipendenza indisponibile. Il client riceve un errore stabile e comprensibile; log protetti e identificatore di correlazione conservano il dettaglio diagnostico. Nascondere l'eccezione o restituire stack trace e SQL al client produce altri problemi.

Le **invarianti** rendono validi gli oggetti fin dalla costruzione. `Objects.requireNonNull` verifica dipendenze obbligatorie; `Optional` può esprimere assenza nei risultati. L'immutabilità riduce modifiche inattese, ma una collezione immutabile superficialmente può ancora contenere oggetti mutabili. Il **bounds checking** verifica limiti di indici e dimensioni prima dell'accesso.

Un **resource leak** lascia risorse occupate dopo l'uso, come connessioni o file. `try-with-resources` chiude risorse `AutoCloseable` anche in presenza di eccezioni; pool e client condivisi richiedono invece un ciclo di vita esplicito. Limiti per payload, buffer, concorrenza e tempo impediscono che un input consumi risorse senza controllo.

## Contenere le dipendenze

Il connection timeout limita l'apertura della connessione; il read o response timeout limita attese della risposta secondo il client utilizzato; una scadenza complessiva limita l'intera operazione. I significati precisi vanno verificati nella libreria, perché un timeout per lettura non è necessariamente un limite totale.

Il **retry con backoff** distanzia tentativi su errori temporanei. Un **circuit breaker** sospende chiamate verso una dipendenza che fallisce ripetutamente. Un **bulkhead** separa capacità e pool affinché una dipendenza non consumi tutte le risorse; il **rate limiting** limita il ritmo delle richieste. L'**idempotenza** permette di ripetere un'operazione senza ripeterne l'effetto. Un pagamento andato in timeout può essere già riuscito: un retry sicuro richiede la stessa identità dell'operazione e una verifica dell'esito.

## Proteggere le interpretazioni dell'input

La SQL injection si previene con parametri, senza concatenare input alla query. Per XSS serve encoding appropriato al contesto di output; per CSRF si valuta come il browser invia le credenziali. La SSRF richiede controlli su destinazioni e accesso di rete, mentre il **path traversal** sfrutta percorsi come `../` per uscire dalle directory consentite.

Con XML, **XXE** indica l'uso di entità esterne che può accedere a risorse locali o remote; l'espansione di entità può consumare memoria e CPU. La configurazione del parser deve limitare queste capacità quando non necessarie. La deserializzazione di dati non fidati deve limitare tipi, dimensioni e comportamento; non si accetta qualsiasi oggetto indicato dal chiamante.

TLS protegge il trasporto, ma il server verifica ancora identità, autorizzazione e appartenenza della risorsa. Un campo `role=ADMIN` nel payload non attribuisce permessi al mittente.

## Segreti e dipendenze nel ciclo di sviluppo

Password, chiavi e token richiedono distribuzione protetta, accessi minimi e rotazione; non vanno inseriti in codice, log o immagini. Un secret manager centralizza queste operazioni, ma occorre proteggere anche l'identità che lo interroga.

La **SCA**, Software Composition Analysis, analizza le dipendenze e le vulnerabilità note. Una **SBOM**, Software Bill of Materials, elenca i componenti del software. Le dipendenze **transitive** arrivano attraverso altre librerie e devono essere considerate insieme a quelle dichiarate direttamente. Una scansione senza segnalazioni non dimostra l'assenza di vulnerabilità: contano aggiornamenti, configurazione e uso effettivo.

## Una revisione orientata ai guasti

Prima del rilascio verifica che input e permessi siano controllati lato server, che le risorse abbiano limiti e che timeout e retry rispettino il dominio. Cerca **race condition**, errori dovuti all'interleaving di operazioni concorrenti, ed esiti sconosciuti dopo guasti parziali. Per un consumer di pagamenti, un test che consegni due volte lo stesso evento e uno che interrompa il processo tra effetto e conferma sono più significativi di una verifica del solo percorso riuscito.
