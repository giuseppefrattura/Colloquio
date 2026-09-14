# 35. Performance Engineering

## Obiettivo
Imparare a diagnosticare e migliorare le performance di applicazioni Java/Spring e sistemi distribuiti.

## Metriche
- Latency
- Throughput
- RPS
- Concurrency
- CPU utilization
- Memory utilization
- Error rate
- Saturation

## JVM
- Heap e allocation rate
- Garbage Collection
- GC pauses
- Thread contention
- Java Flight Recorder
- JDK Mission Control
- Thread dump
- Heap dump
- Profiling

## Database
- Slow queries
- EXPLAIN / EXPLAIN ANALYZE
- Index selectivity
- Cardinality
- Composite indexes
- Execution plan
- Lock contention
- Connection pool

## Load testing
- Load test
- Stress test
- Spike test
- Soak test
- Baseline

## Approccio al troubleshooting
1. Misurare il problema
2. Definire baseline e SLO
3. Identificare il bottleneck
4. Formulare un'ipotesi
5. Misurare/profilare
6. Applicare una modifica
7. Verificare il risultato

## Domande da colloquio
1. Un endpoint è diventato lento: da dove parti?
2. CPU bassa ma latency alta: cosa controlli?
3. Come analizzi un GC problem?
4. Come trovi una query lenta?
5. Come distingui CPU-bound da I/O-bound?
6. Come dimensioni un connection pool?

## Regola Senior
Non ottimizzare a intuito: **measure first, identify the bottleneck, change one thing, measure again**.
