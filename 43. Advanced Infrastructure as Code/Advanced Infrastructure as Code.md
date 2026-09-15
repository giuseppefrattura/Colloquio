# 43. Advanced Infrastructure as Code

## Obiettivo
Approfondire Infrastructure as Code oltre la semplice conoscenza di Terraform, collegandola a CI/CD, sicurezza, governance e gestione degli ambienti.

## Terraform
Concetti fondamentali:
- HCL
- Resources
- Data sources
- Variables
- Outputs
- Locals
- Modules
- Providers
- State
- Remote state
- State locking
- Dependencies
- Drift

## Modules
I Terraform modules permettono di creare componenti riutilizzabili, ad esempio un modulo per un servizio ECS, una VPC o un database.

Un buon modulo dovrebbe avere interfaccia chiara, pochi input necessari, output significativi e versionamento controllato.

## State Management
Il Terraform state collega la configurazione dichiarativa alle risorse reali.

In team è opportuno utilizzare:
- remote backend
- locking
- encryption
- access control
- versioning
- backup/recovery dello state

Mai inserire secret direttamente nel repository o nello state senza considerare le implicazioni di sicurezza.

## Workflow
`terraform fmt → validate → plan → review → apply`

In CI/CD l'`apply` dovrebbe essere controllato e autorizzato, mentre il `plan` può essere prodotto automaticamente come artifact della pipeline.

## Environment Strategy
Possibili approcci:
- directory separate
- workspace
- repository separati
- moduli riutilizzabili + configurazioni per ambiente

L'obiettivo è evitare duplicazione mantenendo comunque isolamento e controllo tra dev, staging e production.

## Drift Detection
Il drift si verifica quando l'infrastruttura reale viene modificata al di fuori di Terraform.

Best practice: ridurre il Click-Ops e fare emergere il drift tramite `terraform plan` e controlli automatizzati.

## Infrastructure as Code nella CI/CD
Pipeline tipica:

`Git commit → validate → security scan → terraform plan → approval → terraform apply → smoke test`

Possibili controlli:
- policy as code
- cost estimation
- security scanning
- code review
- protected environments

## Terraform vs CloudFormation vs AWS CDK
- **Terraform**: multi-cloud, ampia ecosystem e modello dichiarativo.
- **CloudFormation**: servizio IaC nativo AWS.
- **AWS CDK**: definisce infrastruttura AWS usando linguaggi di programmazione e genera CloudFormation.

La scelta dipende da cloud strategy, competenze del team, governance e necessità di portabilità.

## Secrets
Terraform non deve essere usato come sistema di secret management. Integrare invece secret manager e IAM, limitando esposizione e privilegi.

## Domande da colloquio
1. Cos'è il Terraform state?
2. Perché serve il locking?
3. Come gestisci Terraform in un team?
4. Cos'è il drift?
5. Come strutturi dev/staging/prod?
6. Come integri Terraform in CI/CD?
7. Come gestisci i secret?
8. Terraform vs CloudFormation?
9. Quando preferiresti CDK?
10. Come impedisci modifiche manuali all'infrastruttura?
11. Come gestisci un `terraform apply` fallito a metà?
12. Come fai rollback dell'infrastruttura?

## Regola Senior
IaC non significa soltanto "creare risorse con Terraform": significa rendere l'infrastruttura **riproducibile, revisionabile, sicura, testabile e governata attraverso il ciclo di vita del software**.
