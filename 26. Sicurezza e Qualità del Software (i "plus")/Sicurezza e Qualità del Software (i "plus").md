# 26. Sicurezza e qualità come proprietà del prodotto

## Collegare prevenzione e verifica

La qualità di un backend comprende correttezza, capacità di evolvere e protezione di dati e operazioni. Il **secure coding** traduce minacce in regole implementative: parametri per le query, controllo dei permessi sulle risorse e gestione protetta delle credenziali. OWASP offre categorie utili per riconoscere rischi, non un certificato automatico di sicurezza.

Una SQL injection nasce quando input non fidato diventa parte delle istruzioni SQL. Un controllo di autenticazione incompleto può permettere accesso con identità non verificata; una risposta o un log troppo ricco può esporre dati. Questi problemi richiedono sia un progetto corretto sia verifiche mirate.

## Segreti, cifratura e tokenizzazione

Un **secret manager** controlla distribuzione e rotazione di password, chiavi e token. Il codice usa un'identità autorizzata per recuperarli. Spostare una password dal sorgente a un file accessibile a tutti non risolve la protezione; il confine comprende permessi, conservazione e logging.

La **cifratura** rende un dato illeggibile senza la chiave prevista. La **tokenizzazione** sostituisce invece un dato sensibile con un riferimento o valore sostitutivo. In un modello con vault, una mappatura protetta collega token e dato originario; esistono anche altri modelli. Un token può essere utilizzabile in determinati contesti di pagamento, quindi non è necessariamente «inutile a chiunque lo intercetti».

Il **PAN**, Primary Account Number, è il numero della carta. Ridurne la diffusione può ridurre esposizione e perimetro di alcuni controlli, ma l'ambito PCI dipende dal sistema concreto. Il [PCI Security Standards Council](https://www.pcisecuritystandards.org/faqs/1384/) distingue modelli di tokenizzazione e contesti di utilizzo.

## Verificare ciò che conta

La piramide dei test combina molte verifiche rapide con meno integrazioni e percorsi completi costosi. Un test unitario può verificare arrotondamenti; un test con un provider simulato verifica come l'applicazione reagisce a un rifiuto. Per dimostrare compatibilità con il protocollo occorrono anche contratti o integrazioni adeguate.

Nei pagamenti è particolarmente utile verificare duplicati, timeout ed esiti sconosciuti, senza produrre operazioni reali nei sistemi bancari a ogni build. Il capitolo 41 sviluppa la strategia e il capitolo 49 approfondisce la gestione difensiva di input e risorse.

## Un esempio da costruire

Prendi un endpoint che legge un pagamento. Verifica identità del chiamante, appartenenza della risorsa, campi restituiti e dati presenti nei log. Poi progetta un test in cui un utente autenticato prova a leggere il pagamento di un altro cliente: è una prova concreta del confine di autorizzazione.
