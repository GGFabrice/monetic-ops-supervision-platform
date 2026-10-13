# Monetic Ops & Supervision Platform

## Plateforme d'exploitation, de supervision et d'analyse des opérations monétiques

Projet Data Engineering conçu pour simuler, centraliser, superviser et
analyser des opérations monétiques dans un environnement bancaire
inspiré de la Côte d'Ivoire.

> **Données entièrement synthétiques :** ce projet ne contient aucune
> donnée bancaire réelle.

## Présentation

**Monetic Ops & Supervision Platform** est une plateforme de données
dédiée à l'exploitation et à la supervision des opérations monétiques.
Elle combine un entrepôt PostgreSQL, des pipelines Python/SQL, des
analyses opérationnelles, des contrôles qualité, un moteur de scoring
fondé sur des règles et un traitement analytique avec PySpark.

Objectifs : - Générer des données monétiques synthétiques. - Centraliser
les données dans PostgreSQL. - Suivre la disponibilité et les
performances des terminaux ATM et POS. - Analyser les transactions et
les incidents. - Identifier les transactions présentant des signaux de
risque. - Calculer des indicateurs opérationnels. - Tester la qualité
des données. - Produire des agrégations PySpark et enregistrer les KPI
dans PostgreSQL.

## Architecture

``` text
Données synthétiques
        |
        v
Pipelines Python / SQL
        |
        v
PostgreSQL — Data Warehouse
        |
        +--> Supervision des terminaux
        +--> Analyse des transactions
        +--> Gestion des incidents
        +--> Détection par règles et risk scoring
        +--> Contrôles qualité et tests automatisés
        |
        v
PySpark — agrégations par canal
        |
        v
PostgreSQL — table des KPI Spark
        |
        v
Power BI / orchestration Airflow (évolutions prévues)
```

## Modèle de données

Le Data Warehouse utilise le schéma PostgreSQL `monetic`.

### Dimensions

-   `dim_date`
-   `dim_bank`
-   `dim_customer`
-   `dim_card`
-   `dim_terminal`
-   `dim_merchant`
-   `dim_location`
-   `dim_transaction_type`
-   `dim_response_code`

### Tables de faits

-   `fact_transactions`
-   `fact_terminal_status`
-   `fact_incidents`

Le projet comprend également des tables analytiques pour les alertes de
risque et les KPI calculés par PySpark.

## Données synthétiques

  Élément                          Volume
  ----------------------------- ---------
  Clients                             500
  Cartes                              500
  Terminaux                           200
  Terminaux ATM                       120
  Terminaux POS                        80
  Commerçants                         300
  Banques                               5
  Types de transactions                 6
  Codes réponse                         9
  Transactions                    100 000
  Observations de supervision     584 000
  Incidents générés                12 638
  Villes                                6

Les données sont synthétiques et ne décrivent pas l'activité réelle
d'une banque ou d'un établissement financier.

## ETL et génération des données

Les scripts Python génèrent les dimensions, les transactions, les
observations de supervision et les incidents, puis chargent les données
dans PostgreSQL.

Les transactions contiennent notamment la date et l'heure, la banque, le
client, la carte, le terminal, le commerçant, la localisation, le type
de transaction, le code réponse, le montant, la devise, le temps de
traitement et des indicateurs de succès et de suspicion.

Canaux simulés : - ATM - POS - BANKING - E_COMMERCE

## Supervision des terminaux

Les statuts simulés sont `ONLINE`, `DEGRADED`, `OFFLINE` et
`MAINTENANCE`.

Le volume de supervision est calculé ainsi :

`200 terminaux × 365 jours × 8 observations par jour = 584 000 observations`

Indicateurs disponibles : - Disponibilité moyenne et temps de réponse. -
Statut des terminaux. - Incidents et niveaux de criticité. - Comparaison
ATM / POS. - Performance par ville. - Terminaux les plus problématiques.

### Résultats de supervision

  -----------------------------------------------------------------------
  Indicateur                                                     Résultat
  ------------------------------ ----------------------------------------
  Observations                                                    584 000

  Disponibilité moyenne                                           94,04 %

  Incidents                                                        12 638

  Incidents résolus                                               91,91 %

  Temps moyen de résolution          208,97 minutes (environ 3,48 heures)
  (MTTR)                         
  -----------------------------------------------------------------------

## Gestion des incidents

Les incidents sont générés à partir des anomalies simulées dans les
données de supervision.

Niveaux de criticité : `MEDIUM`, `HIGH`, `CRITICAL`.

Types : `PERFORMANCE`, `CONNECTIVITY`, `SYSTEM_FAILURE`.

Statuts : `OPEN`, `IN_PROGRESS`, `RESOLVED`.

Les analyses couvrent le volume d'incidents, la criticité, les types,
les terminaux, les villes, le temps moyen de résolution et l'évolution
mensuelle.

## Analyse des transactions

Les analyses SQL et PySpark portent sur 100 000 transactions.

  Indicateur                                                  Résultat
  -------------------------------------------- -----------------------
  Nombre de transactions                                       100 000
  Montant total                                  13 577 318 105,13 XOF
  Montant moyen                                         135 773,18 XOF
  Transactions réussies                                         87 977
  Taux de réussite                                             87,98 %
  Transactions rejetées                                         12 023
  Transactions marquées suspectes                                4 515
  Taux de transactions suspectes                                4,52 %
  Montant associé aux transactions suspectes      3 016 017 010,93 XOF

Les analyses incluent la performance par banque, ville, type de
transaction, code réponse, canal, mois et heure.

## Détection des anomalies et risk scoring

Le module `fraud_detection` utilise une approche fondée sur des règles.
Il attribue des points selon différents signaux : - Montant élevé. -
Horaire inhabituel. - Temps de traitement élevé. - Code réponse
considéré comme risqué. - Indicateur de transaction suspecte.

Le score est plafonné à 100 et réparti en niveaux `LOW`, `MEDIUM`,
`HIGH` et `CRITICAL`.

### Résultats du scoring

  Niveau de risque         Alertes        Part
  ------------------ ------------- -----------
  LOW                       93 250     93,25 %
  MEDIUM                     3 502      3,50 %
  HIGH                       2 744      2,74 %
  CRITICAL                     504      0,50 %
  **Total**            **100 000**   **100 %**

Les niveaux `HIGH` et `CRITICAL` représentent 3 248 alertes, soit 3,24 %
des transactions simulées. Le montant associé est de 2 147 770 408,42
XOF.

> Ces résultats proviennent de règles appliquées à des données
> synthétiques. Ils ne constituent ni une preuve de fraude réelle ni un
> modèle de Machine Learning entraîné.

## PySpark : analyse des transactions

Le job `spark_jobs/transaction_analysis.py` lit les transactions depuis
PostgreSQL avec JDBC, calcule les KPI globaux et les agrégations par
canal, puis enregistre les KPI de canal dans PostgreSQL.

### KPI globaux calculés par PySpark

  Indicateur                                      Résultat
  -------------------------------- -----------------------
  Transactions analysées                           100 000
  Montant total                      13 577 318 105,13 XOF
  Montant moyen                             135 773,18 XOF
  Taux de réussite                                87,977 %
  Taux de transactions suspectes                   4,515 %

### Agrégations par canal

  Canal          Transactions   Montant total (XOF)   Taux de réussite
  ------------ -------------- --------------------- ------------------
  ATM                  51 912      3 985 555 679,05            88,06 %
  POS                  35 217      4 414 949 004,15            88,01 %
  BANKING               7 829      3 913 614 161,76            87,41 %
  E_COMMERCE            5 042      1 263 199 260,17            87,80 %

Le job utilise le pilote PostgreSQL JDBC présent dans
`spark_jobs/jars/`. Les KPI par canal sont enregistrés dans
`monetic.spark_channel_kpis`.

## Contrôles qualité et tests automatisés

Les contrôles SQL vérifient notamment : - Le nombre de transactions. -
L'absence de transactions sans localisation. - Les montants négatifs. -
Les scores et niveaux de risque valides. - Les alertes orphelines. - Les
identifiants de transaction dupliqués. - La cohérence entre statut de
succès et code réponse. - La cohérence des montants entre transactions
et alertes.

Les contrôles SQL exécutés ne remontaient aucune anomalie. La suite de
tests automatisés a également réussi : **14 tests passés**.

## Technologies

### Data Engineering et analyse

-   Python
-   SQL
-   PostgreSQL
-   PySpark / Apache Spark
-   Pandas
-   NumPy
-   Faker
-   Psycopg2
-   JDBC PostgreSQL

### Environnement et qualité

-   Docker
-   Docker Compose
-   pytest
-   Git
-   GitHub

### Évolutions envisagées

-   Apache Airflow pour l'orchestration.
-   Power BI pour les tableaux de bord.
-   Monitoring complémentaire des pipelines.
-   Évaluation approfondie des règles de risque.
-   Étude future du Machine Learning sur des données adaptées.

## Structure du projet

``` text
monetic-ops-supervision-platform/
├── database/
│   ├── schemas/
│   └── queries/
├── etl/
│   ├── generate_data.py
│   ├── generate_transactions.py
│   ├── generate_terminal_status.py
│   └── generate_incidents.py
├── fraud_detection/
│   ├── fraud_rules.py
│   ├── risk_scoring.py
│   └── generate_alerts.py
├── spark_jobs/
│   ├── jars/
│   │   └── postgresql-42.7.8.jar
│   └── transaction_analysis.py
├── tests/
│   ├── test_database_quality.py
│   └── test_fraud_scoring.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Cette arborescence présente les principaux composants ; les fichiers
locaux peuvent varier selon les étapes de développement.

## Installation et exécution

### 1. Cloner le dépôt

``` powershell
git clone https://github.com/GGFabrice/monetic-ops-supervision-platform.git
cd monetic-ops-supervision-platform
```

### 2. Créer et activer l'environnement Python

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances

``` powershell
pip install -r requirements.txt
```

### 4. Démarrer PostgreSQL avec Docker Compose

``` powershell
docker compose up -d
```

Vérifier les paramètres de connexion et les scripts SQL du dépôt avant
d'initialiser une nouvelle base. Exécuter les scripts de création et de
génération dans l'ordre prévu par le projet.

### 5. Exécuter l'analyse PySpark

Après avoir démarré PostgreSQL, activé l'environnement virtuel et
vérifié les paramètres de connexion :

``` powershell
python .\spark_jobs\transaction_analysis.py
```

Le job affiche les KPI globaux et par canal, puis enregistre les KPI de
canal dans PostgreSQL.

### 6. Exécuter les tests automatisés

``` powershell
pytest
```

## Roadmap

### Réalisé

-   [x] Entrepôt PostgreSQL et schéma `monetic`.
-   [x] Dimensions et tables de faits.
-   [x] Génération des données de référence et des transactions.
-   [x] Supervision des terminaux.
-   [x] Génération et analyse des incidents.
-   [x] Analyses SQL des transactions et des terminaux.
-   [x] Règles de détection et risk scoring.
-   [x] Génération des alertes.
-   [x] Contrôles qualité SQL.
-   [x] Tests automatisés.
-   [x] Analyse des transactions avec PySpark.
-   [x] Persistance des KPI PySpark dans PostgreSQL.

### À développer

-   [ ] Orchestration des pipelines avec Airflow.
-   [ ] Tableaux de bord Power BI finalisés.
-   [ ] Supervision centralisée de l'exécution des pipelines.
-   [ ] Évaluation approfondie des règles de scoring.
-   [ ] Étude d'une approche Machine Learning sur des données adaptées.

## Statut du projet

Le projet dispose d'un entrepôt PostgreSQL, de pipelines de génération
de données, de modules de supervision et d'analyse, d'une détection
fondée sur des règles, de contrôles qualité, de tests automatisés et
d'un job PySpark qui persiste ses KPI dans PostgreSQL.

Les données sont synthétiques et les scores de risque sont déterminés
par des règles explicites. Airflow et les tableaux de bord Power BI
restent des évolutions à réaliser.

## Auteur

**Gnabo Fabrice**

Data Engineering \| Data Analytics \| Python \| SQL \| PostgreSQL \|
PySpark

-   GitHub : https://github.com/GGFabrice
-   Dépôt du projet :
    https://github.com/GGFabrice/monetic-ops-supervision-platform
