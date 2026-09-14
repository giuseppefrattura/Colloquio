# 2. Linguaggi Alternativi: Go e Scala (Paradigmi Funzionali)

## Cos'è e perché conta

In molte aziende tech, fintech e scale-up moderne, i team backend operano in contesti **poliglotti**:
* **Go (Golang)**: Scelto per microservizi cloud-native ad altissimo throughput, proxy di rete, strumenti infrastrutturali e servizi con vincoli stringenti di latenza e memoria.
* **Scala**: Scelto per sistemi distribuiti ad altissima affidabilità, architetture a messaggi reattive (Actor Model con Akka/Pekko), data engineering (Apache Spark) ed espressione pura della **Programmazione Funzionale (FP)** sulla JVM.

Per un ingegnere backend Senior Java, conoscere questi linguaggi e i rispettivi paradigmi (CSP in Go, FP pura e Monadi in Scala) amplia drasticamente il ventaglio di soluzioni architetturali e fa la differenza nei colloqui di alto livello.

---

## 1. Go (Golang): Architettura e Concorrenza per Sviluppatori Java

Creato da Google (Robert Griesemer, Rob Pike, Ken Thompson), Go privilegia la **semplicità radicale**, la facilità di lettura e l'efficienza esecutiva.

```
                  CONFRONTO ARCHITETTURALE: JAVA vs GO
   JAVA APPLICATION                            GO APPLICATION
 ┌───────────────────────────┐               ┌───────────────────────────┐
 │ Bytecode (.class / .jar)  │               │ Singolo Binario Nativo    │
 ├───────────────────────────┤               │ (Compilazione Diretta)    │
 │ Java Virtual Machine (JVM)│               ├───────────────────────────┤
 ├───────────────────────────┤               │ Runtime Go Minimale (GC,  │
 │ OS Kernel (Pthreads)      │               │ Go Scheduler, Network)    │
 └───────────────────────────┘               └───────────────────────────┘
```

### Caratteristiche Fondamentali di Go

#### 1. Zero Classi, Solo Structs e Metodi
In Go non esiste la parola chiave `class` né l'ereditarietà classica. I dati sono incapsulati in `struct` e i metodi sono collegati tramite un **Receiver**:

```go
type Payment struct {
    ID     string
    Amount float64
    Status string
}

// Metodo con Value Receiver (riceve una copia)
func (p Payment) IsCompleted() bool {
    return p.Status == "COMPLETED"
}

// Metodo con Pointer Receiver (modifica la struct originale in-place)
func (p *Payment) Complete() {
    p.Status = "COMPLETED"
}
```

#### 2. Interfacce Implicite ("Duck Typing" Statico)
In Go non esiste la clausola `implements`. Se una struct implementa tutti i metodi definiti da un'interfaccia, implementa **automaticamente** quell'interfaccia.

```go
type Processor interface {
    Process(amount float64) error
}

type StripeService struct{}

// StripeService implementa Processor automaticamente
func (s StripeService) Process(amount float64) error {
    // Chiamata API Stripe
    return nil
}
```

---

### La Concorrenza in Go: CSP (Communicating Sequential Processes)

Il principio cardine di Go è: *"Do not communicate by sharing memory; instead, share memory by communicating."*

```
                       GOROUTINES E CHANNELS IN GO
   ┌─────────────────┐       ch <- payment       ┌─────────────────┐
   │ Producer        │ ────────────────────────► │ Channel (chan)  │
   │ (Goroutine 1)   │                           │ [ Buffer Coda ] │
   └─────────────────┘                           └────────┬────────┘
                                                          │ payment := <-ch
                                                          ▼
                                                 ┌─────────────────┐
                                                 │ Consumer Worker │
                                                 │ (Goroutine 2)   │
                                                 └─────────────────┘
```

#### 1. Goroutines
* Thread ultra-leggeri gestiti in user-space dal runtime Go (M:N scheduler multiplexato sui thread del kernel).
* Occupano solo **2 KB di stack** iniziale (che cresce e decresce dinamicamente), contro l'1 MB fisso dei classici thread del sistema operativo / JVM platform threads. (Concetto simile ai *Virtual Threads* di Java 21).
* Avvio istantaneo con la parola chiave `go`:
  ```go
  go processTransaction(tx)
  ```

#### 2. Channels (`chan T`) & `select`
I canali consentono il passaggio sicuro di dati e sincronizzazione tra goroutine senza ricorrere a lock espliciti:

```go
func worker(jobs <-chan int, results chan<- int) {
    for n := range jobs {
        results <- n * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // Avvio di 3 goroutine concorrenti
    for w := 1; w <= 3; w++ {
        go worker(jobs, results)
    }
    
    // Invio job e lettura risultati con select / timeouts
}
```

#### 3. Gestione degli Errori: Error Values vs Eccezioni
In Go non esistono `try-catch-finally`. Le funzioni restituiscono un valore di errore esplicito come valore di ritorno multiplo:

```go
func Transfer(from, to string, amount float64) (string, error) {
    if amount <= 0 {
        return "", fmt.Errorf("importo non valido: %f", amount)
    }
    // Esecuzione trasferimento
    return "TX_12345", nil
}

// Idiomatic Go error handling
txId, err := Transfer("ACC_1", "ACC_2", 150.00)
if err != nil {
    log.Printf("Trasferimento fallito: %v", err)
    return
}
```

---

## 2. Scala & la Programmazione Funzionale (FP) sulla JVM

**Scala** (Scalable Language) è un linguaggio ibrido ad alta espressività che gira sulla **JVM** e combina la Programmazione ad Oggetti con la **Programmazione Funzionale pura**.

### Concetti Chiave di Scala & FP

#### 1. Immutabilità & Case Classes
In Scala l'immutabilità è la scelta predefinita (`val` per variabili immutabili, `var` per mutabili).
Le **Case Classes** sono classi immutabili ricche (l'ispirazione diretta per i *Java Records*):

```scala
case class Transaction(id: String, amount: BigDecimal, currency: String = "EUR")

val tx1 = Transaction("TX_01", BigDecimal(100.0))
// Modifica non-distruttiva tramite copy()
val tx2 = tx1.copy(amount = BigDecimal(150.0))
```

#### 2. Pattern Matching & Algebraic Data Types (ADTs)
Gli ADT consentono di modellare gli stati di business con precisione matematica (`sealed trait` + `case class`/`case object`):

```scala
sealed trait PaymentStatus
case object Pending extends PaymentStatus
case class Authorized(authCode: String) extends PaymentStatus
case class Settled(settlementDate: java.time.LocalDate) extends PaymentStatus
case class Rejected(errorCode: String, reason: String) extends PaymentStatus

def handleStatus(status: PaymentStatus): String = status match {
  case Pending                  => "In attesa di elaborazione"
  case Authorized(code)         => s"Autorizzato con codice: $code"
  case Settled(date)            => s"Regolato in data $date"
  case Rejected("ERR_01", msg)  => s"Rifiutato per frode: $msg"
  case Rejected(_, msg)         => s"Rifiuto generico: $msg"
}
```

#### 3. Le Monadi per la Gestione degli Effetti e degli Errori
In FP pura, le funzioni non devono avere effetti collaterali (*Side Effects*) e non devono lanciare eccezioni impreviste. Si usano i tipi monadici:

* **`Option[T]` (`Some(v)` / `None`)**: Elimina il `NullPointerException`.
* **`Try[T]` (`Success(v)` / `Failure(e)`)**: Incapsula operazioni che possono lanciare eccezioni.
* **`Either[L, R]` (`Left(error)` / `Right(value)`)**: Gestione funzionale degli errori di business (*Railway-Oriented Programming*).

```scala
def parseAmount(raw: String): Either[String, BigDecimal] =
  Try(BigDecimal(raw)).toEither.left.map(_ => "Formato importo non valido")

def validatePositive(amount: BigDecimal): Either[String, BigDecimal] =
  if (amount > 0) Right(amount) else Left("L'importo deve essere positivo")

// Composizione con For-Comprehension (sintassi fluida monadica)
def processInput(raw: String): Either[String, BigDecimal] = for {
  amount   <- parseAmount(raw)
  validAmt <- validatePositive(amount)
} yield validAmt
```

---

### Ecosistemi Concorrenti in Scala

1. **Actor Model (Akka / Apache Pekko)**:
   * I componenti sono **Attori** isolati con stato privato che comunicano esclusivamente tramite invio asincrono di messaggi immutabili nella propria *Mailbox*.
   * Strategie di supervisione gerarchica (*Let it crash* pattern) per auto-riparazione e tolleranza ai guasti distribuita.
2. **Functional Effect Systems (Cats Effect / ZIO)**:
   * Framework basati sulla purezza referenziale, dove i programmi sono descritti come valori (*Effect Data Types*) eseguiti da un runtime a **Fibre** (micro-thread ad altissime prestazioni).

---

## 3. Matrice Comparativa: Java vs Go vs Scala

| Categoria | Java (17/21+) | Go (Golang) | Scala (3.x) |
| :--- | :--- | :--- | :--- |
| **Runtime** | JVM (HotSpot / GraalVM) | Nativo (Singolo Binario compilato) | JVM |
| **Paradigma** | OOP con elementi FP (Stream, Record) | Imperativo / Procedurale + CSP | Ibrido OOP + Pure Functional (FP) |
| **Concorrenza** | Thread OS / Virtual Threads (Project Loom) | **Goroutines & Channels (CSP)** | **Actor Model (Pekko) / Fibre (ZIO)** |
| **Error Handling** | Eccezioni (`try-catch`, Checked/Unchecked) | Valori di ritorno espliciti (`err != nil`) | Tipi Monadici (`Option`, `Either`, `Try`) |
| **Memory Footprint**| Medio-Alto (Heap JVM) | **Bassissimo (poche decine di MB)** | Medio-Alto (JVM) |
| **Startup Time** | Più lento (JIT warmup) / Veloce con GraalVM Native | **Istantaneo (< 10 ms)** | Più lento (JIT) |
| **Casi d'Uso Ideali**| Enterprise Core, Banking, Spring Microservices | Microservizi Cloud-Native, CLI, Proxy, K8s | Sistemi Reattivi, Big Data (Spark), FP pura |

---

## 4. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come si confrontano le Goroutine di Go con i Thread tradizionali di Java e i nuovi Virtual Threads di Java 21?*
  - **R**: I thread tradizionali di Java sono 1:1 con i thread del kernel OS, con stack fisso (~1 MB) e cambi di contesto costosi gestiti dall'OS. Le goroutine di Go sono thread leggeri in user-space con stack iniziale di 2 KB, multiplexate su thread OS dal runtime Go. I **Virtual Threads di Java 21 (Project Loom)** introducono un modello M:N molto simile a Go sulla JVM, consentendo milioni di thread concorrenti con stack dinamico senza bloccare i carrier thread dell'OS durante le operazioni di I/O bloccante.

- *D: Perché Go non supporta l'ereditarietà classica delle classi e come realizza il polimorfismo?*
  - **R**: Go favorisce esplicitamente la **composizione rispetto all'ereditarietà** (*Composition over Inheritance*) per evitare gerarchie di classi fragili e accoppiate. Il riuso del codice si ottiene incorporando (*struct embedding*) una struct dentro un'altra. Il polimorfismo è garantito dalle **interfacce implicite** (*structural typing / duck typing*): qualunque tipo che implementi la firma dei metodi richiesti soddisfa automaticamente l'interfaccia senza bisogno di dichiararlo esplicitamente.

- *D: Qual è il vantaggio di usare `Either[Error, Value]` in Scala rispetto al lanciare un'eccezione tradizionale in Java?*
  - **R**: Lanciare un'eccezione interrompe il flusso di controllo, è invisibile nella firma dei metodi (se unchecked) e rende il codice impuro (*non referenzialmente trasparente*), oltre a comportare il costo computazionale del riempimento dello stack trace. `Either` rende l'eventualità di fallimento un valore di ritorno esplicito e tipizzato nel contratto del metodo, permettendo di comporre flussi di calcolo complessi in modo sicuro e dichiarativo tramite monadi o for-comprehension (*Railway-Oriented Programming*).
