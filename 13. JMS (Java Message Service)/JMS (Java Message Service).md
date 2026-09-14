# 13. JMS (Java Message Service)

### Cos'è
API standard Java (parte di Jakarta EE) per la messaggistica asincrona — definisce un'interfaccia comune indipendente dal broker sottostante (ActiveMQ, IBM MQ, e con adattatori anche altri). È concettualmente più "vecchio" e enterprise-oriented rispetto a Kafka, molto diffuso in sistemi bancari/finanziari legacy.

### Caratteristiche principali

- **Due modelli di messaggistica**:
  - **Point-to-Point (Queue)**: un messaggio viene consumato da **un solo** consumer, anche se più consumer sono in ascolto sulla stessa coda — modello classico "task queue"
  - **Publish/Subscribe (Topic)**: un messaggio viene consegnato a **tutti** i subscriber attivi sul topic
- **Message-Driven Bean / `@JmsListener`**: componenti che reagiscono automaticamente all'arrivo di un messaggio
- **Transazionalità**: JMS supporta l'integrazione con transazioni JTA (Java Transaction API), permettendo di coordinare l'invio/ricezione di un messaggio con un'operazione su database nella stessa transazione — un caso d'uso enterprise classico che Kafka non supporta nello stesso modo nativo
- **Acknowledgment modes**: controllano quando un messaggio è considerato "consumato con successo" (automatico, manuale, transazionale) — rilevante per garantire che un messaggio non vada perso se il processing fallisce a metà

### Esempio di utilizzo (Spring Boot)

```java
// Producer
@Autowired
private JmsTemplate jmsTemplate;

public void sendPaymentRequest(PaymentRequest request) {
    jmsTemplate.convertAndSend("payment.requests.queue", request);
}

// Consumer
@JmsListener(destination = "payment.requests.queue")
public void onPaymentRequest(PaymentRequest request) {
    paymentProcessor.process(request);
}
```

### Rilevanza per il dominio pagamenti
JMS è storicamente molto diffuso in ambito bancario/finanziario per l'integrazione tra sistemi legacy — è plausibile trovarlo in un'azienda di pagamenti con un'architettura consolidata da anni, magari in coesistenza con Kafka per i flussi più moderni. La sua integrazione nativa con transazioni JTA lo rende adatto a scenari dove serve la garanzia "o il messaggio viene inviato E la modifica al DB viene committata, oppure nessuna delle due" — un caso che Kafka gestisce diversamente (tramite pattern come outbox, non nativamente).

### Domande tipiche e risposte

- *D: Differenza principale tra JMS e Kafka?*
  R: JMS è pensato per code/topic con semantica di consegna "classica" (un messaggio consumato sparisce dalla coda, salvo configurazioni particolari) e forte integrazione transazionale enterprise; Kafka è un log distribuito con retention configurabile, pensato per throughput altissimo e replay degli eventi, più adatto ad architetture event-driven moderne su larga scala. In sintesi: JMS per messaging enterprise classico e transazionale, Kafka per event streaming ad alto volume.

- *D: Cosa succede se il consumer JMS fallisce durante l'elaborazione di un messaggio?*
  R: Dipende dall'acknowledgment mode: con acknowledgment automatico il messaggio potrebbe risultare già confermato anche se il processing fallisce dopo; per questo in scenari critici si usa acknowledgment manuale o transazionale, così il messaggio torna disponibile (redelivery) se l'elaborazione non è completata con successo — di nuovo, un caso dove l'idempotenza del consumer è essenziale per gestire in sicurezza eventuali redelivery.
