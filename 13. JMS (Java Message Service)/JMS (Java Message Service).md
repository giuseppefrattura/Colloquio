# 13. JMS e messaggistica enterprise

## Una API comune sopra provider diversi

**JMS**, Java Message Service, nasce come API standard per la messaggistica Java ed è proseguito nella piattaforma Jakarta come Jakarta Messaging. Definisce un modello di programmazione; non è un broker specifico. Il **provider** implementa quel modello e offre il sistema di consegna, per esempio tramite piattaforme di messaggistica enterprise.

La distinzione conta nei confronti: Kafka è una piattaforma con un proprio modello di log, mentre JMS è un contratto che diversi prodotti implementano. Il comportamento operativo richiede di conoscere sia la specifica sia la configurazione del provider.

## Code e sottoscrizioni

Nel modello **point-to-point**, una queue assegna ciascun messaggio a un consumer per un tentativo di consegna. Più consumer possono dividersi il lavoro, ma una riconsegna dopo un errore può far rivedere il messaggio: «un consumer» non significa «un solo effetto garantito per sempre».

Nel modello **publish/subscribe**, un topic distribuisce ai subscriber secondo le sottoscrizioni. Una sottoscrizione non durevole non è equivalente a una durevole: quest'ultima può conservare messaggi per un subscriber temporaneamente scollegato nei limiti previsti dal sistema. La modalità scelta deve riflettere il requisito di recupero.

Un **Message-Driven Bean** integra il consumo nel container enterprise; in Spring `@JmsListener` collega un metodo a una destinazione. Il listener deve ancora definire errori, conferme e idempotenza.

```java
@JmsListener(destination = "payment.requests.queue")
public void onPaymentRequest(PaymentRequest request) {
    paymentProcessor.process(request);
}
```

Il frammento illustra il punto di ingresso. Converter, listener container e gestione della transazione non sono mostrati e influenzano la consegna effettiva.

## Acknowledgment e transazioni

L'**acknowledgment** conferma la ricezione secondo il modo di sessione. Le modalità automatiche, esplicite e transazionali hanno tempi e proprietà differenti; l'ack non dimostra da solo che un aggiornamento esterno sia stato salvato. Un fallimento può causare **redelivery**, nuova consegna, quindi il consumer deve tollerare duplicati.

Con una sessione transazionale, commit e rollback coordinano le operazioni di messaggistica di quella sessione. Per includere anche un database in una transazione globale possono servire **JTA**, Java Transaction API, risorse **XA** compatibili e un transaction manager. La presenza di JMS e `@Transactional` non abilita automaticamente questo coordinamento.

Il 2PC distribuito offre proprietà e costi specifici. Quando non si adotta una transazione globale, Outbox e consumer idempotenti sono un altro modo di collegare database e messaggi, come descritto nel capitolo 36.

## Seguire il fallimento fino al recupero

Per un messaggio di pagamento, chiediti che cosa accade se il processo termina prima del salvataggio e che cosa accade subito dopo. La risposta deve identificare il confine transazionale, il momento della conferma e la regola che riconosce la ripetizione. Questa spiegazione è più utile di una contrapposizione tra tecnologia «vecchia» e «moderna».
