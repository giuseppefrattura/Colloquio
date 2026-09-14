# 33. Distributed Systems Fundamentals

## Obiettivo
Capire i problemi fondamentali dei sistemi distribuiti e saper ragionare sui trade-off architetturali.

## CAP Theorem
- **Consistency**: ogni lettura osserva un valore coerente secondo il modello scelto
- **Availability**: ogni richiesta riceve una risposta, anche in presenza di failure
- **Partition Tolerance**: il sistema continua a operare nonostante una partizione di rete

In un sistema distribuito la partition tolerance è un requisito pratico; il trade-off riguarda principalmente consistency vs availability durante una partizione.

## Consistency Models
- Strong consistency
- Eventual consistency
- Causal consistency
- Read-your-writes
- Monotonic reads

## Problemi tipici
- Network partition
- Partial failure
- Message loss
- Duplicate messages
- Message reordering
- Timeout
- Retry storm
- Clock skew
- Split brain

## Distributed Coordination
- Leader election
- Quorum
- Consensus
- Distributed locking
- Fencing token

## Domande da colloquio
1. Cos'è il CAP theorem?
2. Perché la Partition Tolerance è praticamente inevitabile?
3. Strong consistency vs eventual consistency?
4. Cosa succede durante una network partition?
5. Come gestisci messaggi duplicati o fuori ordine?
6. Come implementeresti un distributed lock e quali problemi introduce?
7. Perché i timeout sono fondamentali nei sistemi distribuiti?

## Concetto chiave
Un sistema distribuito deve essere progettato assumendo che **la rete possa fallire** e che i failure possano essere parziali: un servizio può essere vivo mentre una sua dipendenza è irraggiungibile o lenta.
