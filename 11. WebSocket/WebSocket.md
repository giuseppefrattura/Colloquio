# 11. WebSocket e Comunicazione Real-Time

### Cos'è
Protocollo di comunicazione che stabilisce una connessione **full-duplex persistente** tra client e server su un singolo socket TCP — a differenza di HTTP tradizionale (richiesta/risposta, connessione chiusa dopo ogni scambio), con WebSocket sia client che server possono inviare messaggi in qualsiasi momento sulla stessa connessione aperta.

### Caratteristiche principali

- **Handshake iniziale via HTTP**: la connessione parte come una normale richiesta HTTP con header `Upgrade: websocket`, poi "sale di livello" a una connessione WebSocket persistente
- **Full-duplex**: comunicazione bidirezionale simultanea, non serve che il client "chieda" per ricevere un aggiornamento dal server (a differenza del polling HTTP tradizionale)
- **Basso overhead**: dopo l'handshake iniziale, i messaggi successivi hanno un overhead molto ridotto rispetto a ripetute richieste HTTP, rendendolo adatto ad aggiornamenti frequenti e a bassa latenza
- **STOMP su WebSocket**: in Spring, si usa spesso il protocollo STOMP sopra WebSocket per avere un modello a messaggi/topic più strutturato (simile a un message broker), invece di gestire i frame WebSocket grezzi

### Esempio di utilizzo (Spring Boot)

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws-notifications").withSockJS();
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic");
        registry.setApplicationDestinationPrefixes("/app");
    }
}

// Invio di un aggiornamento in tempo reale
@Autowired
private SimpMessagingTemplate messagingTemplate;

public void notifyTransactionStatus(String accountId, TransactionStatus status) {
    messagingTemplate.convertAndSend("/topic/account/" + accountId, status);
}
```

### Rilevanza per il dominio pagamenti
Utile per **notifiche in tempo reale** verso un frontend/dashboard — ad esempio aggiornare istantaneamente lo stato di una transazione mentre viene processata (in attesa → autorizzata → completata), senza che il client debba fare polling continuo. Rilevante anche per dashboard operative interne che monitorano transazioni live o alert su anomalie.

### Domande tipiche e risposte

- *D: Perché non usare semplicemente il polling HTTP per aggiornamenti in tempo reale?*
  R: Il polling genera traffico costante anche quando non ci sono aggiornamenti reali, introduce latenza (l'aggiornamento arriva solo al prossimo poll) e non scala bene con molti client. WebSocket mantiene una connessione aperta e il server può inviare aggiornamenti nell'istante in cui accadono, con overhead molto minore.

- *D: WebSocket è adatto per comunicazione tra microservizi?*
  R: Non è la scelta tipica — tra servizi backend si preferisce REST/gRPC (sincrono) o un message broker come Kafka/RabbitMQ (asincrono), entrambi più adatti a comunicazione server-to-server con garanzie di delivery/retry. WebSocket è pensato principalmente per comunicazione client-server in tempo reale (es. verso un frontend o un'app mobile).
