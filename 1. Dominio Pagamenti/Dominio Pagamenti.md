## 1. Dominio Pagamenti

### Cos'è e perché è il punto più importante
Essendo "esperienza mandatoria", il colloquio probabilmente dedicherà tempo a domande discorsive sul dominio, non solo tecniche. Devi essere in grado di spiegare il ciclo di vita di una transazione come lo spiegheresti a un collega nuovo del team.

### Cosa studiare

**Ciclo di vita di una transazione carta**
- *Autorizzazione*: il merchant chiede all'issuer (banca del titolare carta) se i fondi/il credito sono disponibili — risposta in tempo reale (millisecondi)
- *Cattura (capture)*: il merchant conferma l'addebito effettivo (a volte avviene subito, a volte dopo giorni — es. hotel, noleggio auto)
- *Clearing*: gli istituti si scambiano le informazioni sulle transazioni da regolare, di solito in batch notturni
- *Settlement*: il movimento di denaro effettivo tra le banche coinvolte
- *Chargeback*: la contestazione da parte del titolare carta, con reverse del flusso

**Attori del sistema**
- *Issuer*: la banca che ha emesso la carta al cliente
- *Acquirer*: la banca che fornisce il servizio di accettazione pagamenti al merchant
- *PSP (Payment Service Provider)*: intermediario tecnologico tra merchant e acquirer/circuiti (es. Nexi, Stripe)
- *Circuito*: la rete che instrada e regola le transazioni (Visa, Mastercard, ecc.)

**Circuiti e protocolli**
- *ISO 8583*: protocollo a messaggi (non XML/JSON) storicamente usato per l'autorizzazione carte — capire la struttura a campi (MTI, bitmap, data elements) anche solo a livello concettuale
- *ISO 20022*: standard più moderno basato su XML, usato per bonifici SEPA e sempre più anche per carte — capire perché sta sostituendo ISO 8583 (interoperabilità, dati più ricchi)
- *SEPA*: SCT (bonifico standard, T+1) vs SCT Inst (bonifico istantaneo, esecuzione in secondi, 24/7)
- *Digital wallet*: come Apple Pay/Google Pay generano un token di dispositivo al posto del PAN reale (tokenizzazione EMV), il ruolo del Token Service Provider

**Normative**
- *PSD2*: obbligo di Strong Customer Authentication (SCA) — autenticazione a due fattori tra possesso, conoscenza, inerenza; le eccezioni (basso importo, transazioni ricorrenti)
- *PCI-DSS*: standard di sicurezza per chi tratta dati carta — perché la tokenizzazione riduce lo "scope" di compliance
- *GDPR* applicato a dati finanziari: minimizzazione, retention, diritto alla cancellazione in tensione con obblighi di conservazione fiscale/antiriciclaggio

**Riconciliazione (il tuo punto di forza)**
- Ripassa mentalmente il progetto Castelmonte: matching automatico vs manuale, gestione delle eccezioni/discrepanze, allocazione di più righe a un movimento
- Collega questo esplicitamente a "clearing/settlement/provisioning" nella job description: la riconciliazione bancaria che hai costruito è concettualmente lo stesso problema che risolvono in ambito clearing — preparati a raccontarlo come esperienza rilevante, anche se il contesto di partenza era diverso

### Come esercitarti
Prova a spiegare ad alta voce, in 2 minuti, il percorso di 10€ pagati con carta in un negozio, dal POS fino a quando il negozio vede i soldi sul conto. Se riesci a farlo fluido, sei pronto per questa parte.
