# 39. Affidabilità, SRE e Chaos Engineering

## Definire il servizio che si vuole mantenere

La **Site Reliability Engineering**, o SRE, applica pratiche ingegneristiche all'affidabilità operativa. La **disponibilità** riguarda la possibilità di usare un servizio; l'**affidabilità** comprende anche il suo comportamento corretto nel tempo. Un'API che risponde rapidamente con un risultato sbagliato non soddisfa il bisogno dell'utente.

Un **SLI**, Service Level Indicator, misura una proprietà del servizio, per esempio la frazione di richieste valide concluse correttamente entro una soglia. Uno **SLO**, Service Level Objective, fissa il valore desiderato dell'indicatore in una finestra. Uno **SLA**, Service Level Agreement, formalizza un accordo con conseguenze contrattuali. Indicatore, obiettivo interno e accordo non sono intercambiabili.

L'**error budget** è la quota di errore ammessa dallo SLO. Se si richiede il 99,9% di richieste riuscite, il budget è lo 0,1% delle richieste considerate. Un indicatore basato sul tempo usa invece minuti o secondi: non si convertono automaticamente i due modelli. Il consumo del budget aiuta a decidere quando investire in affidabilità e quando aumentare il ritmo dei rilasci.

## Ridurre lavoro ripetitivo e preparare la capacità

Il **toil** è lavoro operativo manuale, ripetitivo, automatizzabile e che cresce con il servizio, come riavviare periodicamente un processo per un problema noto. Un'automazione riduce il toil se risolve il bisogno in modo sostenibile; uno script senza controlli può nascondere il guasto.

Il **capacity planning** stima le risorse necessarie per traffico, crescita e guasti. Non basta coprire il carico medio: se una zona diventa indisponibile, le risorse residue devono sostenere il traffico oppure limitarlo in modo previsto.

## Gestire un incidente con un percorso esplicito

La detection individua il problema; il **triage** ne valuta impatto e priorità. La **mitigazione** riduce il danno, per esempio disabilitando una funzione non essenziale. Il recovery ripristina il servizio. Questi passaggi non richiedono di aver già dimostrato la causa profonda.

Dopo la stabilizzazione, la **Root Cause Analysis** ricostruisce cause e condizioni che hanno consentito il guasto. Il **blameless postmortem** documenta tempi, decisioni ed evidenze senza attribuire il problema alla sola persona che ha eseguito un'azione. Le azioni correttive devono avere un responsabile e una verifica: «fare più attenzione» non cambia il sistema.

## Recuperare dati e servizio

Il **Recovery Time Objective**, RTO, è il tempo obiettivo per ripristinare una funzione dopo un disastro. Il **Recovery Point Objective**, RPO, esprime quanta perdita di dati è tollerata, spesso come intervallo temporale. Un backup recente aiuta l'RPO, ma senza una prova di ripristino non dimostra l'RTO.

Il **failover** sposta il servizio verso risorse alternative. Una configurazione multi-AZ distribuisce risorse tra zone di disponibilità della stessa regione; una multi-region usa regioni distinte. La seconda amplia la separazione geografica ma introduce replica a distanza, latenza e nuove decisioni sulla consistenza. Replica e backup rispondono a problemi diversi: una cancellazione errata può propagarsi alle repliche.

In **active-passive** una parte delle risorse attende il subentro; in **active-active** più siti servono traffico. In entrambi i casi si devono provare instradamento, capacità residua, gestione delle scritture e ritorno al funzionamento ordinario.

## Verificare ipotesi con guasti controllati

La **Chaos Engineering** usa esperimenti per verificare ipotesi sull'affidabilità. Prima si definiscono comportamento atteso, metriche, ambito e condizioni di arresto; poi si introduce un guasto delimitato. Aggiungere latenza di rete verifica timeout e code, perdere pacchetti verifica il recupero della comunicazione, terminare un pod verifica ridistribuzione e stato in corso.

Si comincia in ambienti e ambiti controllati. Un esperimento che fa fallire il database può essere utile solo se esistono protezioni e un percorso di recupero. Il risultato interessante non è «il pod riparte», ma «la funzione prevista resta entro i limiti concordati o recupera nel tempo atteso».

## Un esercizio operativo

Per un servizio di autorizzazione definisci SLI, SLO, RTO e RPO. Simula poi la perdita di una dipendenza: spiega quali richieste continueranno, quali verranno respinte e quali avranno esito sconosciuto. Verifica che gli alert segnalino un'azione necessaria e che il recupero non introduca duplicati.
