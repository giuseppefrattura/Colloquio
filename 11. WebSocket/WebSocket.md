# 11. WebSocket e comunicazione in tempo reale

## Ricevere aggiornamenti senza interrogare continuamente il server

Una dashboard di pagamenti deve mostrare cambiamenti di stato anche quando l'utente non avvia nuove richieste. Con il **polling** il client interroga periodicamente il server: la frequenza determina traffico e ritardo massimo di osservazione. WebSocket offre un canale persistente e **full-duplex**, cioè utilizzabile in entrambe le direzioni.

HTTP mantiene il modello richiesta-risposta, ma può riutilizzare connessioni persistenti: non è corretto dire che ogni scambio ne imponga la chiusura. La differenza decisiva è il modello di comunicazione. Con WebSocket il server può inviare un messaggio applicativo sulla connessione già aperta. Il protocollo è definito dalla [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455).

## Stabilire il canale e organizzare i messaggi

Nel handshake HTTP/1.1 comune, il client richiede l'upgrade e il server accetta il passaggio al protocollo WebSocket. Dopo il handshake i dati viaggiano in **frame**, unità del protocollo. L'applicazione definisce ancora formato, significato e instradamento dei messaggi.

**STOMP**, Simple Text Oriented Messaging Protocol, aggiunge un modello di invio e sottoscrizione a destinazioni sopra WebSocket. In Spring puoi usare il broker semplice per scenari limitati o un'integrazione con un broker esterno. **SockJS** fornisce un insieme di trasporti alternativi quando il collegamento WebSocket non è utilizzabile; non aggiunge automaticamente le garanzie di elaborazione del dominio.

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
```

Il frammento illustra endpoint e prefissi; non include configurazione di autenticazione e autorizzazione. Una destinazione come `/topic/account/{id}` non è protetta perché contiene un account ID: il server deve verificare chi può sottoscriverla e inviarvi messaggi.

## Connessioni lunghe, interruzioni e recupero

Una connessione persistente occupa risorse. Occorrono limiti, rilevazione delle disconnessioni e politiche di riconnessione. Un **heartbeat** segnala che il collegamento è ancora utilizzabile secondo il protocollo scelto, ma non prova che l'operazione di business sia stata completata.

Se il client si scollega, non si presume che riceva automaticamente gli aggiornamenti mancati. Una strategia utile è rileggere lo stato autorevole alla riconnessione e poi riprendere le notifiche, usando versioni o sequenze quando necessario. Con più istanze server si progetta come raggiungere le sessioni collegate e come condividere gli eventi.

## Scegliere in base al tipo di aggiornamento

Per messaggi bidirezionali frequenti WebSocket può essere appropriato. Per un flusso principalmente dal server al browser si possono valutare anche **Server-Sent Events**, mentre il polling può bastare per aggiornamenti rari. Tra servizi che richiedono persistenza, retry e consumo indipendente, un broker offre un modello diverso e spesso più adatto.

Per esercitarti, segui uno stato «in lavorazione» che diventa «completato» mentre il browser perde la connessione. Spiega come l'utente recupera il risultato e perché la notifica non deve diventare l'unica fonte dello stato del pagamento.
