# 27. Diagnosi e gestione degli incidenti in produzione

## Capire l'impatto prima di cercare una spiegazione

Un **incidente** è una degradazione che richiede una risposta operativa. La prima domanda è quali utenti e operazioni siano coinvolti, da quando e con quale gravità. Un errore su un solo provider suggerisce un ambito diverso da un'interruzione di tutte le autorizzazioni, ma non dimostra ancora la causa.

La **mitigazione** riduce il danno prima che l'indagine sia completa. Può essere un rollback, la disattivazione di una funzione o l'isolamento di una dipendenza. Un **feature flag** controlla l'attivazione di un comportamento; un **failover** sposta il servizio verso risorse alternative. Queste azioni devono avere condizioni note e un modo per verificarne l'esito.

## Costruire e verificare ipotesi

Log centralizzati consentono di cercare errori nella stessa finestra temporale; metriche mostrano traffico, tempi, errori e saturazione; trace collegano una richiesta attraverso servizi diversi. Un identificatore di correlazione aiuta a ricostruire il percorso senza copiare credenziali o dati sensibili nelle evidenze.

Si confrontano cambiamenti recenti, carico e comportamento delle dipendenze. Un deploy appena avvenuto è un'ipotesi utile, non una causa dimostrata. Anche risorse apparentemente normali non escludono un guasto infrastrutturale: una rete degradata può far aumentare la latenza senza saturare CPU e memoria.

Il **thread dump** mostra stack e attese; l'**heap dump** aiuta a esaminare oggetti e riferimenti. Un **execution plan** descrive come il database esegue una query. La scelta dello strumento segue l'ipotesi: raccogliere tutto indiscriminatamente può costare tempo e risorse durante l'incidente.

## Un'autorizzazione che va in timeout

Se aumentano i timeout, separa provider, istanze e tipi di richiesta. Controlla dove si accumula l'attesa e se i retry aumentano il traffico. Un circuit breaker può contenere nuove chiamate fallimentari; una limitazione del carico può proteggere le risorse residue.

Il timeout non prova il rifiuto del pagamento. Alcune operazioni possono essere già riuscite e richiedere interrogazione dello stato o riconciliazione. Un rollback del codice può ripristinare il servizio, ma non annulla automaticamente effetti finanziari già prodotti. La gestione dell'incidente deve includere questi esiti, non soltanto il ritorno del grafico al verde.

## Chiudere l'incidente con evidenze e azioni

Dopo la mitigazione si verifica il servizio dal punto di vista dell'utente e si controlla il lavoro accumulato. La **Root Cause Analysis** ricostruisce cause e condizioni; un **blameless postmortem** registra sequenza, decisioni e azioni senza ridurre il problema all'errore di una persona.

«Out of memory» è un evento osservato, non una spiegazione completa: può derivare da perdita di riferimenti, crescita inattesa o limiti errati. Le azioni successive devono distinguere queste cause e avere una verifica, per esempio un test prolungato o un limite sul buffer. Il capitolo 39 collega questo percorso agli obiettivi di affidabilità.

## Esercizio

Descrivi un aumento degli errori dopo un rilascio. Indica quale misura confermerebbe o smentirebbe l'ipotesi di regressione, quale mitigazione sarebbe reversibile e come accerteresti che i pagamenti con esito sconosciuto siano stati recuperati.
