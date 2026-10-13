# 33. Fondamenti dei sistemi distribuiti

## Quando il guasto riguarda soltanto una parte del sistema

Un sistema distribuito comprende più processi che comunicano attraverso una rete. Un servizio può funzionare correttamente e non riuscire a raggiungere il database: questo è un **guasto parziale**. Il chiamante non vede direttamente lo stato del processo remoto, ma soltanto risposte, errori o silenzi. Per progettare un pagamento affidabile bisogna partire da questa incertezza.

Una **partizione di rete** separa gruppi di nodi che restano attivi ma non possono comunicare tra loro. Un timeout, invece, indica soltanto che una risposta non è arrivata entro un limite: il pagamento potrebbe essere stato rifiutato, essere ancora in lavorazione oppure essere già stato eseguito. Ripetere la richiesta senza identificarla può quindi causare un doppio addebito.

## CAP: che cosa si deve scegliere durante una partizione

Il teorema CAP riguarda tre proprietà precise. La **consistenza** è qui la linearizzabilità: le operazioni appaiono eseguite in un unico ordine, compatibile con il tempo reale. La **disponibilità** richiede che ogni richiesta a un nodo non guasto termini con una risposta del servizio; restituire soltanto un errore non soddisfa questa proprietà. La **tolleranza alle partizioni** considera la possibilità che i messaggi tra nodi vengano persi o ritardati.

Durante una partizione non si possono garantire insieme linearizzabilità e disponibilità. Un sistema che protegge un saldo può rifiutare temporaneamente una scrittura quando non riesce a coordinarsi con le repliche. Un catalogo può invece accettare aggiornamenti su entrambi i lati, prevedendo come riconciliare le divergenze. La scelta riguarda le operazioni e le garanzie richieste, non una classificazione universale del prodotto.

**PACELC** estende il ragionamento: in presenza di partizione si considera disponibilità contro consistenza; altrimenti si considera anche il costo della consistenza sulla latenza. Aspettare repliche lontane può aumentare il tempo di risposta anche quando la rete funziona.

## Leggere dati replicati: i modelli di consistenza

Con la **consistenza eventuale**, se cessano gli aggiornamenti e la propagazione procede, le repliche convergono. Non significa che qualsiasi ritardo sia accettabile: bisogna stabilire quanto può essere vecchio un dato e che cosa vede l'utente nel frattempo. Un pannello di reportistica può tollerare alcuni secondi di ritardo; la verifica dei fondi disponibili richiede altre garanzie.

La **consistenza causale** preserva l'ordine delle operazioni legate da causa ed effetto: una risposta a un messaggio non dovrebbe apparire prima del messaggio originario. La garanzia **read-your-writes** consente a una sessione di vedere le proprie scritture successive. Le **monotonic reads** impediscono alla stessa sessione di tornare a una versione più vecchia dopo averne già osservata una più nuova. Queste proprietà sono distinte e vanno richieste esplicitamente.

## Messaggi, orologi e tentativi ripetuti

Un messaggio può andare perso, arrivare due volte o essere consegnato fuori ordine. Per gestire i duplicati si assegna un identificatore stabile all'operazione e si registra l'esito: è la base dell'**idempotenza**, cioè ottenere lo stesso effetto anche ripetendo la richiesta. Per l'ordine si usano chiavi, versioni e sequenze; il timestamp da solo è insufficiente, perché gli orologi delle macchine possono essere disallineati. Questo disallineamento è il **clock skew**.

Se molti client ritentano insieme dopo un errore, producono una **retry storm**, una nuova ondata di carico sul sistema già degradato. Il backoff aumenta l'attesa tra i tentativi; il jitter aggiunge una componente casuale per distribuirli nel tempo. Occorrono comunque un limite di tentativi e un termine complessivo.

## Coordinare decisioni senza creare nuovi errori

La **leader election** sceglie il nodo che coordina determinate operazioni. Uno **split brain** si verifica quando più nodi si comportano contemporaneamente come leader. Il **consenso**, realizzato da protocolli come Raft o Paxos, serve a concordare decisioni nonostante alcuni guasti. Un **quorum** è un insieme sufficiente di partecipanti, spesso una maggioranza; non basta citare la maggioranza per dimostrare ogni proprietà del sistema: conta anche il protocollo utilizzato.

Un lock distribuito assegna temporaneamente l'accesso esclusivo a una risorsa. Se il proprietario resta sospeso oltre la scadenza del lock, può riprendere mentre un altro processo ha già ottenuto l'accesso. Un **fencing token**, numero crescente associato all'acquisizione, permette alla risorsa protetta di rifiutare scritture di proprietari ormai superati. Funziona soltanto se la risorsa verifica davvero quel numero.

## Mettere alla prova il ragionamento

Immagina che una richiesta di pagamento vada in timeout dopo essere stata inviata. Spiega come distingueresti un esito sconosciuto da un rifiuto e come useresti identificatore dell'operazione, interrogazione dello stato e riconciliazione. Poi descrivi che cosa accadrebbe se due repliche non potessero comunicare: quale operazione bloccheresti e quale potresti continuare a servire con dati meno aggiornati?
