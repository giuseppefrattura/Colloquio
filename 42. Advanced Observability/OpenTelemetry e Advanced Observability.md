# 42. Advanced Observability e OpenTelemetry

## Obiettivo
Passare dalla semplice raccolta di log e metriche a una strategia completa di osservabilità per sistemi distribuiti.

## I tre pilastri
- Logs
- Metrics
- Traces

L'obiettivo non è semplicemente raccogliere dati, ma poter rispondere rapidamente a domande come: **cosa è successo, dove, quando e perché?**

## Distributed Tracing
Una singola richiesta può attraversare API Gateway, microservizi, database e broker.

Concetti:
- Trace
- Span
- Parent/child span
- Trace ID
- Span ID
- Context propagation
- Sampling

Il Trace ID permette di correlare le diverse operazioni appartenenti alla stessa richiesta distribuita.

## OpenTelemetry
OpenTelemetry è uno standard/framework open source per generare, raccogliere e esportare telemetry.

Componenti/concepts:
- Instrumentation
- SDK
- Collector
- Exporter
- OTLP
- Traces
- Metrics
- Logs

L'OpenTelemetry Collector può ricevere telemetry dalle applicazioni, elaborarla e inoltrarla verso backend differenti senza legare il codice applicativo a un singolo vendor.

## Metrics
Metriche utili:
- request rate
- error rate
- latency p50/p95/p99
- CPU
- memory
- GC
- database connections
- queue depth
- Kafka consumer lag

### RED Method
Per i servizi:
- Rate
- Errors
- Duration

### USE Method
Per le risorse:
- Utilization
- Saturation
- Errors

## Logging
Best practice:
- structured logging
- correlation ID
- trace ID
- log levels appropriati
- evitare dati sensibili
- centralizzazione

## Alerting
Un alert dovrebbe rappresentare un problema che richiede un'azione.

Evitare alert basati esclusivamente su metriche tecniche prive di impatto sul servizio. Preferire alert collegati a SLO, error rate, latency e saturation.

## Observability in Microservices
Una catena tipica:

`Client → API Gateway → Service A → Kafka → Service B → Database`

La propagazione del context permette di seguire la transazione attraverso l'intera catena.

## Esempio di troubleshooting
Se la latency p99 di `PaymentService` aumenta:
1. verificare se aumenta anche l'error rate
2. controllare trace distribuiti
3. identificare lo span più lento
4. verificare DB, connection pool o chiamate esterne
5. correlare con deployment recenti
6. applicare mitigazione
7. verificare il ritorno ai valori SLO

## Domande da colloquio
1. Logs vs metrics vs traces?
2. Cos'è uno span?
3. Come propaghi un Trace ID tra microservizi?
4. Cos'è OpenTelemetry?
5. Perché usare un Collector?
6. Perché p95/p99 sono spesso più utili della media?
7. RED vs USE?
8. Come monitori il consumer lag Kafka?
9. Come costruisci un alert efficace?
10. Come indaghi una latency anomala in un sistema distribuito?
