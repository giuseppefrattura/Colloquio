# 32. Dominio Assicurativo, Previdenziale e Sistemi Finanziari (OMS, Portfolio, Billing, Reconciliation)

## Cos'è e perché conta

Nei settori **FinTech, InsurTech, Wealth Management e Banking**, i requisiti tecnici si intrecciano indissolubilmente con la complessità del dominio di business e i vincoli normativi (IVASS, COVIP, Solvency II, MiFID II, IFRS 17). Uno sviluppatore Senior deve dimostrare non solo eccellenza tecnologica (Java, microservizi, architetture a eventi), ma anche **padronanza del linguaggio ubiquo di business**, comprendendo come i flussi di dati impattano contratti, calcoli attuariali, gestione ordini, portafogli, fatturazione e riconciliazioni contabili.

---

## 1. Il Dominio Assicurativo (Insurance / InsurTech)

```
                            CICLO DI VITA ASSICURATIVO
  ┌────────────────┐      ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
  │  Underwriting  │ ───► │  Policy Issue  │ ───► │   Collection   │ ───► │     Claims     │
  │ (Assunzione)   │      │  (Emissione)   │      │   (Incasso)    │      │   (Sinistri)   │
  └────────────────┘      └────────────────┘      └────────────────┘      └────────────────┘
```

### Concetti Fondamentali
1. **Tipologie di Polizze**:
   * **Ramo Vita (Life Insurance)**:
     * *Ramo I*: Polizze rivalutabili tradizionali (a capitale garantito con gestione separata).
     * *Ramo III (Unit-Linked / Index-Linked)*: Polizze il cui rendimento è legato a fondi comuni di investimento o indici finanziari (il rischio di mercato è a carico del contraente).
     * *Ramo V*: Operazioni di capitalizzazione.
   * **Ramo Danni (Non-Life / P&C - Property & Casualty)**:
     * Coperture per eventi accidentali: RC Auto/Moto, Infortuni, Malattia, Incendio, Furto, Responsabilità Civile Generale, Tutela Legale.
2. **I Soggetti del Contratto**:
   * **Compagnia (Assicuratore)**: L'ente che assume il rischio dietro pagamento del premio.
   * **Contraente**: Chi stipula la polizza e paga il premio.
   * **Assicurato**: La persona fisica o giuridica la cui vita/beni sono esposti al rischio.
   * **Beneficiario**: Chi riceve la prestazione economica (indennizzo o capitale) al verificarsi dell'evento.
3. **Flussi Operativi di Core Insurance**:
   * **Underwriting (Assunzione del Rischio)**: Valutazione del profilo di rischio (score anamnestico, peritale o telemetrico) e determinazione della tariffa/premio.
   * **Gestione Premi (Premium Management)**: Calcolo del premio (puro + caricamenti per costi di gestione e provvigioni), piani di frazionamento (annuale, semestrale, mensile con addebito SDD) e quietanzamento.
   * **Gestione Sinistri (Claims Management)**: Denuncia del sinistro (*First Notice of Loss - FNOL*), perizia, calcolo della franchigia/scoperto, costituzione della riserva sinistri e liquidazione dell'indennizzo.
   * **Riserve Tecniche (Technical Reserves)**: Accantonamenti obbligatori a bilancio per garantire la solvibilità futura delle prestazioni (Riserva Premi, Riserva Sinistri, Riserva Matematica).
4. **Normativa di Riferimento**:
   * **IVASS**: Istituto per la Vigilanza sulle Assicurazioni (regolamentazione trasparenza, IDD - Insurance Distribution Directive).
   * **Solvency II**: Requisiti patrimoniali basati sul rischio per evitare insolvenze delle compagnie.
   * **IFRS 17**: Standard contabile internazionale per i contratti assicurativi.

---

## 2. Il Dominio Previdenziale (Pension Funds / Previdenza Complementare)

La previdenza si basa sul sistema a "tre pilastri":
1. *Primo Pilastro*: Previdenza pubblica obbligatoria (INPS).
2. *Secondo Pilastro*: Fondi pensione chiusi/negoziali di categoria (es. Cometa, Fonte) o aperti.
3. *Terzo Pilastro*: Piani Individuali Pensionistici (PIP) e polizze previdenziali individuali.

```
                          LE DUE FASI DELLA PREVIDENZA
   FASE DI ACCUMULO (Versamenti)                  FASE DI EROGAZIONE (Rendita)
 ┌───────────────────────────────┐              ┌───────────────────────────────┐
 │ • Contributo Lavoratore       │   CONVERSIONE│ • Rendita Vitalizia Immediata │
 │ • Contributo Datore di Lavoro │ ───────────► │ • Rendita Reversibile         │
 │ • Conferimento TFR            │              │ • Liquidazione Capitale (max  │
 │ • Rivalutazione Quote/NAV     │              │   50% o 100% per casi limite) │
 └───────────────────────────────┘              └───────────────────────────────┘
```

### Flussi e Meccanismi Chiave
* **Fase di Accumulo**:
  * Gestione dei flussi contributivi (contribuzione volontaria + contributo datoriale + TFR).
  * Acquisto periodico di **quote del comparto** (Garantito, Prudente, Bilanciato, Azionario) valorizzate al **NAV** (*Net Asset Value*).
  * Fiscalità agevolata: deducibilità dei versamenti fino al tetto di legge (€ 5.164,57 annui).
* **Fase di Erogazione (Decumulo)**:
  * Al raggiungimento dei requisiti pensionistici: liquidazione in capitale (fino al 50%) e conversione del montante residuo in **Rendita Vitalizia** tramite coefficienti di conversione attuariali.
  * Anticipazioni (per spese sanitarie, acquisto prima casa) e Riscatti (in caso di disoccupazione o invalidità).
* **Vigilanza**: **COVIP** (Commissione di Vigilanza sui Fondi Pensione).

---

## 3. Order Management System (OMS) & Esecuzione Ordini

Un **Order Management System (OMS)** è la piattaforma finanziaria che gestisce l'intero ciclo di vita degli ordini di compravendita di strumenti finanziari (azioni, obbligazioni, ETF, derivati, fondi).

```
 ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
 │  Portfolio   │ ──► │     OMS      │ ──► │  Smart Order │ ──► │ Execution    │
 │  Manager     │     │  (Compliance │     │  Router      │     │ Venues       │
 │  (Creazione) │     │   Pre-Trade) │     │  (SOR)       │     │ (Borse/Dark) │
 └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### Il Ciclo di Vita dell'Ordine:
1. **Generazione dell'Ordine**: Il gestore crea una proposta di investimento o disinvestimento.
2. **Pre-Trade Compliance & Risk Check**: Controlli bloccanti automatici real-time:
   * Verifica limiti normativi (MiFID II, UCITS) e mandati contrattuali del cliente.
   * Controllo disponibilità fondi / capienza titoli (*Short Selling check*).
3. **Smart Order Routing (SOR)**: Algoritmo che seleziona la *Execution Venue* ottimale (Borsa Italiana, Euronext, MTF, Internalizzatori Sistematici) in termini di prezzo, costo, velocità e probabilità di esecuzione (*Best Execution*).
4. **Protocollo FIX (Financial Information eXchange)**:
   * Standard universale di messaggistica finanziaria TCP basato su tag-value (es. `35=D` New Order Single, `35=8` Execution Report).
5. **Execution Report & Post-Trade**: Ricezione degli eseguiti parziali/totali, allocazione sui conti dei singoli clienti e invio al sistema di regolamento (*Clearing & Settlement* via Monte Titoli / Euroclear).

---

## 4. Portfolio Management & Wealth Tech

I sistemi di **Portfolio Management (PMS)** calcolano l'esposizione, la valorizzazione e il rendimento dei patrimoni in gestione.

### Concetti Chiave:
* **Asset Allocation**: Ripartizione del portafoglio tra classi di asset (Azionario, Obbligazionario, Liquidità, Real Estate, Commodities) secondo profili di rischio (Conservativo, Moderato, Aggressivo).
* **Valorizzazione e NAV (Net Asset Value)**:
  $$\text{NAV} = \frac{\text{Valore di Mercato degli Attivi} - \text{Passività}}{\text{Numero di Quote in Circolazione}}$$
* **Calcolo delle Performance**:
  * **TWR (Time-Weighted Return)**: Misura l'abilità del gestore isolando l'impatto dei flussi di cassa (versamenti/prelievi del cliente). Standard istituzionale GIPS.
  * **MWR / IRR (Money-Weighted Return)**: Tasso interno di rendimento che tiene conto dei tempi e volumi dei versamenti/prelievi del cliente.
* **Metriche di Rischio**:
  * **Volatilità (Deviazione Standard)**: Misura la dispersione dei rendimenti rispetto alla media.
  * **Value at Risk (VaR)**: Massima perdita potenziale stimata con un dato intervallo di confidenza (es. 99%) su un dato orizzonte temporale.
  * **Sharpe Ratio**: Misura dell'extra-rendimento per unità di rischio rispetto al tasso privo di rischio (*risk-free rate*).

---

## 5. Billing, Commissioning & Revenue Split

I sistemi di **Billing Finanziario e Assicurativo** gestiscono il calcolo automatico, la fatturazione e la ripartizione delle commissioni.

```
                             MODELLO DI FEE SPLITTING
   ┌────────────────────────────────────────────────────────────────────────┐
   │ Commissione di Gestione Totale (es. 1.50% annuo sul patrimonio medio)  │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
   Management Company / SGR (0.60%)                       Distributore / Rete (0.90%)
   (Gestione e Manutenzione Prodotto)                     (Provvigione di Mantenimento)
```

### Tipologie di Commissioni (Fees):
* **Management Fees (Commissioni di Gestione)**: Calcolate pro-quota giornaliera sul patrimonio medio gestito (AuM - *Assets under Management*) e liquidate mensilmente o trimestralmente.
* **Performance Fees (Commissioni di Performance / Overperformance)**: Calcolate secondo la metodologia **High-Water Mark (HWM)**: la commissione viene prelevata solo se il valore del fondo supera il massimo storico precedente.
* **Entry / Exit Fees (Commissioni di Sottoscrizione / Rimborso)**: Commissioni una-tantum applicate al momento dell'investimento o del disinvestimento.
* **Retrocession & Rebates**: Ripartizione contrattuale delle commissioni tra la fabbrica prodotto (SGR/Compagnia) e la rete distributiva (Banca collocatrice, Promotori finanziari, Broker).

---

## 6. Riconciliazione Finanziaria e Bancaria (Reconciliation Engines)

La riconciliazione è il processo contabile che garantisce che due set di dati indipendenti (es. il registro interno delle transazioni e l'estratto conto della banca depositaria o del circuito di carte) siano perfettamente allineati.

```
       SISTEMA INTERNO (Ledger)                BANCA DEPOSITARIA / ESTRATTO CONTO
    ┌─────────────────────────────┐               ┌─────────────────────────────┐
    │ TX_001 | 150.00 EUR | 10:00 │               │ MOV_88 | 150.00 EUR | 10:01 │
    │ TX_002 | 320.50 EUR | 10:15 │               │ MOV_89 | 320.50 EUR | 10:16 │
    │ TX_003 |  45.00 EUR | 10:30 │               │ MOV_90 |  90.00 EUR | 11:00 │ ◄── UNMATCHED!
    └──────────────┬──────────────┘               └──────────────┬──────────────┘
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          ▼
                             RECONCILIATION ENGINE
                             • 1-to-1 Match (Esatto)
                             • 1-to-N Match (Split/Cumulativi)
                             • Exception Management & Break Report
```

### Algoritmi e Strategie di Matching:
1. **Deterministic / Exact Match (1-to-1)**:
   * Matching basato su identificativi univoci: `Transaction ID`, `End-to-End ID (SEPA)`, `Reference Number` o combinazione esatta (`Data Contabile` + `Importo Esatto` + `Codice Divisa`).
2. **Aggregated Match (1-to-N o N-to-1)**:
   * Una singola voce di bonifico cumulativo (*batch payout*) ricevuta dalla banca corrisponde alla somma di $N$ singoli pagamenti nel registro interno.
3. **Fuzzy / Rule-Based Matching**:
   * Tolleranza su differenze di data contabile ($\pm 1-2$ giorni lavorativi per compensazioni bancarie), normalizzazione delle stringhe di causale o gestione di commissioni bancarie trattenute all'origine (*Net Settlement*).
4. **Exception Management (Squadrature e Sospesi)**:
   * Generazione automatica di record di "Break" o "Unmatched Items".
   * Workflow di investigazione per l'ufficio contabilità/operations con tracciamento degli storni e delle rettifiche.

---

## 7. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come progetteresti un sistema di riconciliazione ad alto volume scalabile e affidabile?*
  - **R**: Utilizzerei un'architettura asincrona a pipeline:
    1. **Ingestion & Normalization**: Ricezione degli estratti conto esterni (es. file ISO 20022 `camt.053` o tracciati CBI) tramite SFTP o Kafka, convertendoli in un modello canonico normalizzato.
    2. **Rule-Based Engine**: Una prima fase di matching deterministico esatto in-memory o tramite query batch indicizzate (su ID univoco, importo e valuta).
    3. **Two-Pass Matching**: Per i record non abbinati (*unmatched*), esecuzione di regole di matching aggregato (1-a-N) o con finestre temporali di tolleranza ($\pm 2$ giorni per valuta).
    4. **Persistenza & Idempotenza**: Gli abbinamenti vengono salvati con stato `RECONCILED` in transazione ACID, mentre i disallineamenti finiscono in una tabella/coda di `RECONCILIATION_EXCEPTIONS` per gestione manuale o rielaborazione successiva.

- *D: In un sistema di Order Management (OMS), perché il controllo di compliance Pre-Trade deve essere sincrono e a bassissima latenza?*
  - **R**: Perché la normativa (MiFID II) impone di prevenire violazioni dei limiti di rischio, scoperti non autorizzati o manipolazioni di mercato *prima* che l'ordine sia immesso sul mercato. Se il controllo fosse asincrono, l'ordine potrebbe essere già eseguito a mercato quando il controllo fallisce, esponendo la società a perdite finanziarie e sanzioni legali. Si implementa caricando le posizioni e i limiti in memoria (es. Redis o strutture in-memory clusterizzate) con algoritmi deterministici a latenza sub-millisecondo.

- *D: Qual è la differenza tra un fondo di accumulo e un fondo pensione nella gestione delle quote e del NAV?*
  - **R**: Entrambi dividono il patrimonio in quote valorizzate periodicamente al NAV. Tuttavia, nel fondo pensione la contribuzione è vincolata fino al pensionamento, gode di deducibilità fiscale specifica ed è suddivisa in comparti di rischio (garantito per il TFR silente vs azionario per i giovani). Inoltre, nella fase finale il montante accumulato viene convertito in rendita vitalizia applicando basi demografiche e coefficienti attuariali certificati da COVIP.

- *D: Come implementeresti il calcolo delle commissioni di performance con la regola dell'High-Water Mark (HWM)?*
  - **R**: L'High-Water Mark memorizza il valore NAV di picco storico al quale è stata pagata l'ultima commissione di performance. Ad ogni data di calcolo (es. fine anno), la commissione viene calcolata solo sulla quota di sovraperformance: $\text{Fee} = (\text{NAV}_{\text{attuale}} - \text{HWM}) \times \text{PerformanceRate} \times \text{Quote}$, e solo se $\text{NAV}_{\text{attuale}} > \text{HWM}$. Se l'anno si chiude con profitto, il valore dell'HWM viene aggiornato al nuovo NAV; se il fondo è in perdita, l'HWM resta invariato e il gestore non incassa nulla finché non recupera interamente la perdita precedente.
