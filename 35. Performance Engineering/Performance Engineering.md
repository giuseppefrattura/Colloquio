# 35. Ingegneria delle prestazioni

## Descrivere la lentezza con misure

La **latenza** è il tempo impiegato da un'operazione; il **throughput** è il numero di operazioni completate nell'unità di tempo. La **concorrenza** indica quante operazioni sono in corso insieme. Sono misure collegate ma diverse: aumentare la concorrenza può accrescere il throughput fino alla saturazione, poi aumentare soprattutto le code e la latenza.

La media nasconde le richieste lente. Il percentile **p95** è il valore entro cui termina il 95% delle osservazioni; p99 descrive una coda ancora più estrema. Si confrontano percentili, tasso di errore e traffico nella stessa finestra, separando quando serve richieste riuscite e fallite. La **saturazione** misura il lavoro che eccede la capacità immediata, per esempio richieste in attesa di una connessione.

## Riconoscere il collo di bottiglia

Un carico **CPU-bound** è limitato dal calcolo; un carico **I/O-bound** dall'attesa di database, disco o rete. Una CPU poco utilizzata con latenza alta suggerisce attese, ma non dimostra da sola dove si trovino: potrebbero esserci lock, code o pool esauriti.

Il **profiling** misura dove il programma spende tempo o risorse. Java Flight Recorder raccoglie eventi della JVM; JDK Mission Control aiuta a interpretarli. Un **thread dump** fotografa gli stack dei thread e può mostrare contesa, cioè più thread che attendono la stessa risorsa. Un **heap dump** rappresenta gli oggetti nella memoria gestita ed è utile per capire quali riferimenti impediscano di liberarla.

L'**allocation rate** misura quanta memoria viene allocata nell'unità di tempo. Molte allocazioni possono aumentare il lavoro del garbage collector, mentre un insieme di oggetti ancora raggiungibili troppo grande può lasciare poco spazio. Le pause di GC vanno correlate al traffico e alla latenza: cambiare collector senza evidenze può spostare il problema.

## Guardare il database prima di aumentare le risorse

Una query lenta può leggere troppe righe, usare un indice inadatto o attendere un lock. Il **piano di esecuzione** mostra il percorso scelto dal database. `EXPLAIN` descrive il piano stimato; `EXPLAIN ANALYZE`, nei database che lo supportano, esegue la query e aggiunge misure reali. Questa distinzione conta quando la query modifica dati o è costosa.

La **cardinalità** è il numero di righe o valori rilevante per una stima; la **selettività** descrive quanto un predicato restringe i risultati. Un indice composto include più colonne e il loro ordine influenza le ricerche utili. Una query che restituisce metà tabella può non trarre beneficio dall'indice atteso.

Il **connection pool** riutilizza connessioni e limita l'accesso concorrente al database. Aumentarlo non crea capacità sul database: può accrescere la contesa. Si misurano connessioni occupate, richieste in attesa e durata delle transazioni, includendo il carico delle altre applicazioni.

## Costruire esperimenti confrontabili

Un **load test** riproduce il carico atteso; uno **stress test** cerca il limite e il comportamento oltre quel limite. Uno **spike test** introduce un aumento rapido; un **soak test** mantiene il carico a lungo per trovare accumuli e perdite di risorse. La **baseline** è la misura di riferimento ottenuta prima della modifica, con condizioni documentate.

L'indagine parte da un problema riproducibile e da un obiettivo, per esempio ridurre il p99 mantenendo lo stesso throughput. Si formula un'ipotesi, si raccolgono dati, si cambia un fattore e si ripete la misura. Cache e ottimizzazioni hanno anche effetti su correttezza, memoria e costo: il confronto deve includerli.

## Un caso da discutere

Un endpoint peggiora mentre la CPU resta bassa. Le tracce mostrano attesa prima della query e il pool è pieno. Prima di aumentarlo, verifica se una transazione mantiene la connessione durante una chiamata HTTP. Accorciare quella transazione potrebbe liberare capacità senza aggiungere connessioni. La prova è un nuovo confronto di attesa, latenza ed errori sotto lo stesso carico.
