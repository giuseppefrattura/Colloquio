## 25. Design Pattern e Principi SOLID

### Cos'è e perché conta
Domanda classica da "senior": non tanto ricordare a memoria l'elenco, quanto saper riconoscere quale pattern applicare a un problema concreto — spesso i colloquiatori chiedono "che pattern useresti per..." più che "elenca i design pattern".

### Principi SOLID

- **S — Single Responsibility**: una classe dovrebbe avere una sola ragione per cambiare — es. `PaymentService` gestisce la logica di pagamento, non anche la formattazione dei log o l'invio email
- **O — Open/Closed**: il codice dovrebbe essere aperto all'estensione ma chiuso alla modifica — es. aggiungere un nuovo `PaymentGateway` (già visto nel punto sui Qualifier) senza modificare il codice che già usa l'interfaccia `PaymentGateway`
- **L — Liskov Substitution**: una sottoclasse deve poter sostituire la sua superclasse senza alterare la correttezza del programma — es. se `MastercardGateway` e `VisaGateway` implementano `PaymentGateway`, il codice chiamante deve funzionare identicamente con entrambe
- **I — Interface Segregation**: preferire interfacce piccole e specifiche invece di una grande interfaccia generica — es. separare `PaymentProcessor` da `RefundProcessor` invece di un'unica interfaccia enorme che pochi client usano per intero
- **D — Dependency Inversion**: dipendere da astrazioni (interfacce), non da implementazioni concrete — è esattamente il principio dietro la dependency injection già vista nel punto 2 (iniettare `PaymentGateway`, non `VisaGatewayImpl` direttamente)

### Design pattern più rilevanti per un contesto backend/pagamenti

- **Strategy**: incapsula algoritmi intercambiabili dietro una stessa interfaccia — è il pattern dietro `PaymentGateway` con più implementazioni (Visa, Mastercard) selezionate a runtime, collegabile direttamente a `@Qualifier`
- **Factory**: centralizza la creazione di oggetti, utile quando la logica di scelta dell'implementazione concreta è complessa (es. una `PaymentGatewayFactory` che sceglie il gateway giusto in base al tipo di circuito indicato nella richiesta)
- **Observer**: un oggetto notifica automaticamente i suoi "osservatori" quando cambia stato — concettualmente alla base degli event listener Spring (`@EventListener`) e degli eventi di dominio già visti nel punto 8
- **Builder**: costruisce oggetti complessi passo passo, utile per oggetti con molti parametri opzionali (es. costruire una `TransactionRequest` con vari campi facoltativi in modo leggibile invece di un costruttore con 10 parametri)
- **Decorator**: aggiunge comportamento a un oggetto senza modificarne la classe, avvolgendolo — es. aggiungere logging o retry attorno a una chiamata di pagamento senza toccare la logica originale
- **Circuit Breaker**: già visto nel punto 8, è concettualmente un pattern strutturale applicato alla resilienza distribuita
- **Template Method**: definisce lo scheletro di un algoritmo in una classe base, lasciando ai sottotipi implementare i passi specifici — utile ad esempio se il flusso di validazione di un pagamento è sempre lo stesso (validazione formale → controllo fondi → controllo frode) ma alcuni passi variano per tipo di pagamento

### Domande tipiche e risposte

- *D: Che pattern useresti per gestire più circuiti di pagamento con logiche diverse ma stessa interfaccia?*
  R: Strategy pattern — un'interfaccia comune (`PaymentGateway`) con un'implementazione per circuito, selezionata a runtime (in Spring, tramite `@Qualifier` o una Factory che sceglie il bean giusto in base al tipo di richiesta).

- *D: Come si collega il Dependency Inversion Principle a Spring?*
  R: Spring è essenzialmente un framework che applica il DIP su larga scala: le classi dipendono da interfacce/astrazioni (iniettate dal container, vedi punto 2), non creano direttamente le proprie dipendenze concrete — questo è ciò che rende il codice testabile e sostituibile.
