# 41. Progettare una strategia di test

## Scegliere il livello che osserva il rischio

La **piramide dei test** suggerisce molti controlli rapidi e un numero più contenuto di verifiche costose. Un **unit test** osserva una piccola unità di comportamento; un **integration test** verifica la collaborazione reale con un componente o una dipendenza. Un **component test** verifica un servizio nel suo insieme con confini esterni controllati. Un **contract test** verifica aspettative tra servizi; un **end-to-end test**, E2E, percorre una funzione attraverso il sistema completo.

Non esiste una proporzione valida per ogni progetto. Una regola di calcolo richiede soprattutto verifiche locali; un problema di isolamento transazionale richiede un database con comportamento reale. L'obiettivo è rilevare le regressioni importanti rapidamente e con un risultato affidabile.

## Isolare il calcolo, senza imitare il codice

JUnit organizza ed esegue i test. Mockito crea sostituti controllati: un **mock** può simulare risposte e registrare interazioni; uno **spy** avvolge un oggetto reale e richiede attenzione agli effetti della sua esecuzione. `@Mock` dichiara i mock e `@InjectMocks` tenta di inserirli nell'oggetto sotto test; non avvia il container Spring. `ArgumentCaptor` permette di esaminare argomenti passati a una dipendenza quando questi fanno parte del comportamento da verificare.

Un buon test prepara dati, esegue l'azione e verifica un esito significativo. Non dovrebbe dipendere dall'ordine di chiamate interne irrilevanti. Per una commissione, importo, valuta e arrotondamento sono risultati utili; contare una chiamata a un metodo privato lega il test all'implementazione.

## Verificare integrazioni e configurazione

`@SpringBootTest` avvia un contesto applicativo ampio. Le **test slice**, come `@WebMvcTest`, caricano un insieme mirato di componenti. MockMvc esercita il livello MVC senza necessariamente aprire una porta reale; WebTestClient può verificare risposte web nei contesti supportati. WireMock simula un server HTTP esterno con risposte ed errori controllati.

**Testcontainers** avvia dipendenze reali in container: database, broker e cache. È utile per SQL specifico, transazioni, serializzazione e configurazione del protocollo. Un database embedded con dialetto diverso potrebbe nascondere una query incompatibile con produzione. Anche il container non riproduce automaticamente rete, dimensioni e topologia produttiva: il perimetro del test deve essere chiaro.

## Mantenere i contratti tra servizi

Nel **consumer-driven contract** il consumer esplicita le risposte o i messaggi che si aspetta. La **provider verification** controlla che il producer li soddisfi. Pact e Spring Cloud Contract aiutano a eseguire queste verifiche senza avviare ogni servizio insieme.

La backward compatibility comprende significato e forma: una modifica da centesimi a euro può mantenere un campo numerico e rompere tutti i calcoli. Per gli eventi si verificano campi opzionali, valori sconosciuti ed evoluzione dello schema; per HTTP status, corpo, errori e autorizzazioni. Un test di contratto non dimostra da solo il funzionamento dell'intero processo.

## Provare i guasti che il dominio teme

Per un consumer di pagamenti verifica duplicati, ordine richiesto e crash tra effetto e conferma. Per il retry prova un errore temporaneo e uno permanente; per la DLQ verifica sia l'invio sia il successivo recupero. Con un broker reale puoi osservare offset e riconsegne invece di simulare soltanto una chiamata a `send`.

Un test **flaky** alterna successo e fallimento senza una modifica rilevante. Spesso dipende da tempo, stato condiviso o attese arbitrarie. Nei test asincroni usa condizioni osservabili e scadenze, isola i dati e conserva evidenze del fallimento. Aumentare indiscriminatamente i timeout rende la pipeline lenta senza chiarire la causa.

## TDD, BDD e pipeline

Il **Test-Driven Development**, TDD, alterna un test che fallisce per il comportamento mancante, il codice necessario a farlo passare e il refactoring. Il **Behavior-Driven Development**, BDD, rende condivisibili gli esempi di business mediante condizioni iniziali, azione e risultato, spesso espressi come Given, When, Then.

La CI può eseguire prima verifiche rapide e poi integrazione, contratti e pochi percorsi E2E critici. Un **quality gate** è una condizione che blocca la promozione, per esempio un contratto incompatibile. La **coverage** misura codice attraversato, non la qualità delle asserzioni. Load e performance test, descritti nel capitolo 35, completano i controlli quando contano capacità e latenza.

## Un esercizio di progettazione

Per un pagamento con un provider esterno, separa test di calcolo, integrazione col database, contratto HTTP e un percorso E2E. Scegli dove verificare un timeout seguito da risposta tardiva e spiega perché quel livello può osservare l'errore che vuoi prevenire.
