## Prefazione

Un colloquio tecnico diventa più utile quando permette di capire come una persona ragiona. Ricordare il nome di un pattern è un punto di partenza; saper descrivere il problema che risolve, le condizioni in cui funziona e il costo che introduce dimostra una comprensione più solida. Questo libro accompagna il passaggio dalla conoscenza delle tecnologie al ragionamento sui sistemi.

Il filo conduttore è un backend Java che riceve richieste, modifica dati e collabora con altri componenti. Il pagamento torna spesso come esempio perché rende visibili problemi importanti: due richieste apparentemente uguali possono produrre due addebiti; un timeout può lasciare l'esito sconosciuto; una risposta rapida può nascondere un processo ancora incompleto. Lo stesso ragionamento si applica a ordini, prenotazioni e molti altri domini.

Il percorso comincia dal linguaggio e dalla macchina virtuale, passa per persistenza, framework e comunicazione e arriva all'esercizio del sistema in produzione. I capitoli introduttivi costruiscono il vocabolario; gli approfondimenti successivi riprendono i concetti per discuterne confini e conseguenze. Le ripetizioni servono a osservare lo stesso problema da prospettive diverse, come transazioni, messaggistica e affidabilità.

I termini tecnici sono accompagnati dal loro significato e da esempi. Alcune parole inglesi rimangono perché compaiono nelle API, nella documentazione e nei colloqui; lo scopo è poterle usare con precisione, non memorizzarle senza capire. Un compromesso architetturale, spesso chiamato *trade-off*, è una scelta che migliora una proprietà sostenendo un costo su un'altra. Per ogni scelta è utile chiedersi quale requisito la renda necessaria e quale evidenza ne mostri il risultato.

### Come leggere

Alla prima lettura segui i problemi e gli esempi, senza cercare di ricordare ogni comando. Torna poi ai capitoli che riguardano il tuo lavoro e costruisci un caso concreto: una query lenta, un messaggio duplicato o un rilascio con due versioni in esecuzione. Prova a spiegare la soluzione a una persona che non conosce ancora il sistema. Se devi usare un'altra parola non spiegata per chiarire la prima, cerca il concetto che manca.

Le domande di ripasso e gli esercizi sono inviti a ragionare. Una buona risposta esplicita ipotesi, decisione, comportamento durante un guasto e modo di verifica. Nei racconti di esperienza distingue il contributo personale da quello del gruppo e usa risultati realmente osservati.

### Come usare gli esempi

Il codice e le configurazioni illustrano un meccanismo. Alcuni frammenti omettono import, tipi applicativi o parti dell'ambiente: il testo chiarisce i confini importanti prima di proporne l'uso. Versioni, valori e soglie sono esempi quando non sono indicati come proprietà del protocollo. Prima di integrarli si verificano la versione adottata e il comportamento nel proprio contesto.

Nel dominio finanziario, regole di prodotto, contratti e normative hanno ambito e date di efficacia. Il modello software deve rappresentare queste informazioni e mantenerne la provenienza. Il libro sviluppa il significato tecnico dei processi; l'implementazione concreta richiede la regola applicabile al caso.

Alla fine di un capitolo dovresti poter spiegare che cosa può andare storto, come la soluzione lo affronta e quali problemi rimangono. È questa capacità di collegare concetti ed evidenze che rende la preparazione utile anche dopo il colloquio.
