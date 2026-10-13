# 43. Infrastructure as Code: stato, collaborazione e recupero

## Descrivere risorse e relazioni

L'**Infrastructure as Code**, IaC, rappresenta l'infrastruttura con configurazioni versionabili e verificabili. Terraform usa **HCL**, HashiCorp Configuration Language, per descrivere risorse e relazioni. Un **provider** integra le API di una piattaforma; una **resource** dichiara un oggetto da gestire, mentre una **data source** legge informazioni esistenti.

Le **variable** ricevono input, i **local** esprimono valori derivati e gli **output** espongono risultati. Le dipendenze tra risorse guidano l'ordine delle operazioni. Il modello è dichiarativo: descrivi uno stato desiderato e Terraform calcola operazioni per avvicinarvi l'infrastruttura.

## Usare moduli con confini comprensibili

Un **module** raggruppa configurazioni riutilizzabili. Un modulo database può richiedere dimensioni e rete ed esporre l'endpoint. Non dovrebbe nascondere decisioni fondamentali o offrire centinaia di opzioni senza un contratto chiaro. Il versionamento rende controllata l'evoluzione per gli ambienti che lo utilizzano.

Dev, staging e produzione possono usare moduli condivisi con configurazioni distinte. Directory, repository e workspace sono strumenti organizzativi; un workspace da solo non dimostra un confine di sicurezza. Credenziali, permessi e backend separati definiscono l'isolamento effettivo.

## Capire che cosa rappresenta lo state

Lo **state** collega indirizzi nella configurazione e risorse reali, conservando anche attributi utili alla gestione. Un **remote backend** rende disponibile lo state al team; il **locking**, quando supportato e configurato, impedisce operazioni concorrenti incompatibili sullo stesso stato.

Si proteggono accessi, cifratura, versioni e backup dello state. Dati sensibili possono finirvi anche senza essere scritti in chiaro nei sorgenti. Dichiarare un valore `sensitive` ne limita alcune visualizzazioni, ma non equivale a cifrare o eliminare il valore dallo stato. Il secret manager e l'identità che lo accede vanno progettati insieme.

## Dal piano alla modifica

Il percorso abituale è `fmt`, `validate`, `plan`, revisione e `apply`. `fmt` uniforma il formato; `validate` controlla la configurazione; `plan` mostra le modifiche previste. `apply` esegue operazioni reali e non è una transazione atomica su tutta l'infrastruttura.

La pipeline produce un piano revisionabile e controlla policy, costo e sicurezza. La **policy as code** rende automatizzabili regole come il divieto di esporre un database pubblicamente. Gli ambienti protetti e i permessi limitati controllano chi può applicare le modifiche. Gli smoke test successivi verificano le funzioni essenziali dell'infrastruttura risultante.

## Drift e fallimenti parziali

Il **drift** è lo scostamento tra risorse reali e stato previsto, spesso dovuto a modifiche manuali. Un nuovo piano può mostrarlo; bisogna decidere se riportare la risorsa alla configurazione o aggiornare consapevolmente il codice. Ridurre il **Click-Ops**, cioè gestione manuale tramite console, aiuta la tracciabilità senza eliminare procedure di emergenza controllate.

Se un apply fallisce a metà, alcune risorse possono essere già cambiate. Si leggono errori e stato reale, si produce un nuovo piano e si decide il recupero. Tornare a un vecchio commit non garantisce un rollback sicuro: rimuovere una risorsa può distruggere dati. Import, correzioni e ripristini richiedono un piano concreto, non la ripetizione automatica dello stesso comando.

## Scegliere lo strumento in base ai vincoli

Terraform integra più piattaforme mediante provider. CloudFormation è il servizio dichiarativo AWS; AWS CDK esprime l'infrastruttura in linguaggi di programmazione e sintetizza template CloudFormation. Portabilità, competenze e governance contano più di una classifica astratta.

Per esercitarti, descrivi una modifica di rete che rischia di interrompere l'accesso a un database. Spiega come leggeresti il piano, quale verifica farebbe la pipeline e come recupereresti se soltanto alcune operazioni venissero eseguite.
