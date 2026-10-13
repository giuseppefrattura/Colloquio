# 10. Microservizi: i concetti fondamentali

## Una divisione delle responsabilità, prima che dei processi

Un **microservizio** gestisce una capacità applicativa attraverso un contratto esplicito e può essere rilasciato con una propria autonomia. Il suo valore non si misura dal numero di classi. In un sistema di pagamenti, autorizzazione e riconciliazione possono avere ritmi, carichi e responsabilità differenti; separarle può essere utile se questi confini sono chiari.

Il pattern database per service assegna al servizio la proprietà dei dati. Gli altri servizi usano contratti invece di modificarne direttamente le tabelle. Questo riduce alcune dipendenze ma elimina la comodità di una transazione locale su tutto il sistema. Il capitolo 6 affronta le conseguenze sulla consistenza.

## Quando l'autonomia ripaga la complessità

La scalabilità indipendente consente di aumentare capacità solo dove serve. Il rilascio indipendente permette a team distinti di cambiare una funzione senza pubblicare tutto il prodotto. Queste possibilità sono reali soltanto se contratti e dipendenze lo consentono.

L'isolamento dei guasti va progettato: un servizio separato può comunque bloccare tutti i chiamanti se questi attendono senza limite. Si aggiungono inoltre rete, osservabilità e coordinamento operativo. Un monolite modulare può essere più semplice quando un team gestisce un dominio ancora in evoluzione e non serve un rilascio separato.

## Comunicazione sincrona e asincrona

Nella comunicazione **sincrona** il chiamante aspetta una risposta, come in una chiamata HTTP REST o RPC. **gRPC** offre un modello di chiamata remota con contratti tipizzati; REST organizza l'interazione intorno alle risorse. In entrambi i casi attesa e guasti devono avere limiti espliciti.

Nella comunicazione **asincrona** il lavoro è inviato o annunciato tramite messaggi. Il producer non deve attendere il completamento del consumer, ma il sistema deve rappresentare stati intermedi e recuperare messaggi non elaborati. Un'autorizzazione può richiedere una risposta immediata al client; notifiche e reportistica possono seguire un evento successivo.

## Trovare e proteggere le dipendenze

Un **API Gateway** instrada richieste e applica controlli comuni. La **service discovery** permette di trovare istanze mediante un registro o il meccanismo della piattaforma, senza fissare ogni indirizzo nel codice. Nessuno dei due elimina la possibilità che la destinazione sia lenta o non raggiungibile.

Un **circuit breaker** interrompe temporaneamente chiamate che falliscono ripetutamente, poi prova se la dipendenza è tornata utilizzabile. Un timeout limita la singola attesa e un bulkhead separa capacità: sono protezioni complementari. Un fallback deve rispettare il dominio; per un pagamento può significare comunicare indisponibilità o esito da verificare, non inventare un'autorizzazione riuscita.

## Da una richiesta a un processo distribuito

Una Saga coordina transazioni locali e compensazioni. Event Sourcing conserva cambiamenti come eventi; CQRS distingue modelli di modifica e lettura. Sono strumenti per esigenze precise, approfonditi nel capitolo 36, non requisiti per chiamare «a microservizi» un sistema.

Come esercizio, descrivi il comportamento dell'autorizzazione quando il provider esterno rallenta. Indica quali risorse restano occupate, quando interrompi l'attesa e come recuperi un risultato arrivato dopo il timeout senza addebitare due volte.
