# 30. Concetti trasversali: collegare le proprietà del sistema

## Seguire una richiesta dall'ingresso all'esito

Un pagamento attraversa sicurezza, transazioni, dipendenze e osservabilità. Studiare questi aspetti separatamente è utile, ma il comportamento reale nasce dalla loro interazione. Consideriamo una richiesta ricevuta due volte perché il client non ha visto la prima risposta.

L'autenticazione identifica il chiamante e l'autorizzazione verifica che possa operare sul conto. OAuth delega l'accesso, OIDC fornisce un livello di identità e un JWT firmato può trasportare claims verificabili. La firma non nasconde i dati. TLS protegge il trasferimento **in transit**, mentre cifratura e gestione delle chiavi proteggono la conservazione **at rest**. Il minimo privilegio limita ciò che ciascuna identità può fare anche dopo una compromissione.

## Retry e idempotenza devono essere progettati insieme

L'**idempotenza** produce lo stesso effetto osservabile quando la stessa operazione viene ripetuta. Un identificatore stabile permette di riconoscere il pagamento; un registro durevole collega tale identificatore a stato ed esito. Una transazione locale con `@Transactional` non deduplica automaticamente richieste HTTP né rende atomici effetti su un provider remoto.

Un **timeout** limita l'attesa, non garantisce la cancellazione dell'operazione a valle. Un retry può quindi ripetere un effetto già avvenuto. Il **backoff esponenziale** aumenta l'attesa tra tentativi e il **jitter** li distribuisce nel tempo. Numero massimo e deadline complessiva impediscono che il recupero diventi carico senza limite.

La **graceful degradation** mantiene funzioni utili quando una parte fallisce. Per esempio, una dashboard può mostrare temporaneamente un dato meno recente. Per una verifica antifrode, la politica deve essere esplicita e compatibile con il rischio: il guasto non autorizza automaticamente il pagamento.

## Rendere visibile ciò che è accaduto

I log descrivono eventi, le metriche mostrano andamento e aggregati, le trace seguono il percorso distribuito. I **golden signals** sono traffico, latenza, errori e saturazione. Per i pagamenti vanno collegati anche agli esiti di dominio: una risposta HTTP riuscita può soltanto aver accettato un'elaborazione ancora incompleta.

Il correlation ID e gli identificatori di business permettono di collegare tentativi ed esito senza esporre PAN, password o token. L'osservabilità deve rispondere alla domanda «questo pagamento è stato applicato?» oltre a «il processo è vivo?».

## Rilasciare e recuperare con gli stessi confini

Una pipeline CI/CD costruisce, verifica e promuove un artefatto. Un **blue-green deployment** mantiene due versioni di ambiente e sposta il traffico; un **canary** introduce gradualmente la nuova versione a una quota limitata. Entrambi richiedono compatibilità tra versioni e dati condivisi.

Il rollback del traffico può essere rapido, ma uno schema distruttivo o un effetto esterno non tornano indietro soltanto cambiando immagine. L'**Infrastructure as Code** rende revisionabile la configurazione delle risorse; il recupero dei dati richiede backup, procedure e prove proprie.

## Esercizio di sintesi

Segui un pagamento ripetuto durante un canary. Spiega come versioni vecchie e nuove condividono l'identità dell'operazione, quali dati registrano e come l'operatore ricostruisce l'esito. La coerenza tra questi passaggi vale più della presenza isolata di ogni tecnologia.
