# Monetic Ops & Supervision Platform

## Plateforme d'exploitation, de supervision et d'analyse des opérations monétiques

> Projet Data Engineering conçu pour simuler, centraliser, superviser et analyser les opérations monétiques d'un environnement bancaire en Côte d'Ivoire.

---

## 📌 Présentation du projet

**Monetic Ops & Supervision Platform** est une plateforme de données dédiée à l'exploitation et à la supervision des opérations monétiques.

L'objectif est de construire une architecture Data Engineering complète permettant de :

* générer des données monétiques réalistes ;
* centraliser les données dans un Data Warehouse PostgreSQL ;
* superviser les terminaux ATM et POS ;
* analyser les transactions ;
* détecter les anomalies et transactions suspectes ;
* suivre les incidents techniques ;
* produire des indicateurs de performance ;
* préparer une restitution analytique avec Power BI ;
* évoluer progressivement vers des traitements distribués avec PySpark et une orchestration avec Airflow.

Le projet s'appuie sur des données synthétiques inspirées d'un environnement bancaire et monétique ivoirien.

---

## 🎯 Objectifs

Les principaux objectifs sont :

1. Concevoir un Data Warehouse adapté aux opérations monétiques.
2. Générer un volume important de données synthétiques.
3. Mettre en place des pipelines ETL en Python.
4. Superviser la disponibilité et les performances des terminaux.
5. Identifier et analyser les incidents.
6. Mesurer la performance des transactions.
7. Détecter les transactions présentant des caractéristiques suspectes.
8. Construire des indicateurs destinés au pilotage opérationnel.
9. Préparer une architecture évolutive vers le Big Data et le Machine Learning.

---

## 🏗️ Architecture du projet

```text
                         SOURCES DE DONNÉES
                                │
                                ▼
                    ┌─────────────────────┐
                    │ Génération Python   │
                    │ Données synthétiques│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       ETL           │
                    │ Python / SQL        │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       PostgreSQL Data          │
              │          Warehouse             │
              │                                │
              │ Dimensions + Tables de faits   │
              └───────────────┬────────────────┘
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
       Supervision       Analytics       Détection
       terminaux        transactions      anomalies
              │               │                │
              └───────────────┼────────────────┘
                              ▼
                       ┌──────────────┐
                       │   Power BI   │
                       │ Dashboards   │
                       └──────────────┘
```

### Évolution prévue

```text
Python / SQL
     │
     ▼
PostgreSQL
     │
     ├── ETL
     ├── Supervision
     ├── Analytics
     └── Détection fraude
     │
     ▼
PySpark
     │
     ▼
Airflow
     │
     ▼
Power BI / Monitoring
```

---

## 🗄️ Modèle de données

Le Data Warehouse utilise un schéma dédié :

```text
monetic
```

### Dimensions

* `dim_date`
* `dim_bank`
* `dim_customer`
* `dim_card`
* `dim_terminal`
* `dim_merchant`
* `dim_location`
* `dim_transaction_type`
* `dim_response_code`

### Tables de faits

* `fact_transactions`
* `fact_terminal_status`
* `fact_incidents`

---

## 📊 Données générées

Le projet contient actuellement :

| Élément                     |  Volume |
| --------------------------- | ------: |
| Clients                     |     500 |
| Cartes                      |     500 |
| Terminaux                   |     200 |
| Terminaux ATM               |     120 |
| Terminaux POS               |      80 |
| Commerçants                 |     300 |
| Banques                     |       5 |
| Types de transactions       |       6 |
| Codes réponse               |       9 |
| Transactions                | 100 000 |
| Observations de supervision | 584 000 |
| Incidents                   |  12 638 |
| Villes                      |       6 |

Les données sont synthétiques et ne contiennent aucune donnée bancaire réelle.

---

# ⚙️ ETL & Génération des données

Les données sont générées automatiquement avec Python et chargées dans PostgreSQL.

### Génération des dimensions

Le pipeline génère notamment :

* les clients ;
* les cartes ;
* les terminaux ;
* les commerçants ;
* les données de référence.

### Génération des transactions

Le pipeline génère **100 000 transactions** avec notamment :

* date et heure ;
* banque ;
* client ;
* carte ;
* terminal ;
* commerçant ;
* localisation ;
* type de transaction ;
* code réponse ;
* montant ;
* devise ;
* temps de traitement ;
* statut de succès ;
* indicateur de transaction suspecte.

### Caractéristiques

Les transactions couvrent plusieurs canaux :

* ATM ;
* POS ;
* Banking ;
* E-commerce.

---

# 🏧 Supervision des terminaux

Une table de supervision permet de suivre l'état des terminaux dans le temps.

Les statuts simulés sont :

```text
ONLINE
DEGRADED
OFFLINE
MAINTENANCE
```

Le pipeline produit :

**200 terminaux × 365 jours × 8 observations par jour**

soit :

```text
584 000 observations
```

### Indicateurs disponibles

* disponibilité moyenne ;
* temps de réponse ;
* statut des terminaux ;
* incidents ;
* incidents critiques ;
* comparaison ATM / POS ;
* performance par ville ;
* terminaux les plus problématiques.

### Résultats actuels

| Indicateur            |   Résultat |
| --------------------- | ---------: |
| Observations          |    584 000 |
| Disponibilité moyenne |    94,04 % |
| Incidents             |     12 638 |
| Incidents résolus     |    91,91 % |
| MTTR                  | 208,97 min |
| MTTR                  |     3,48 h |

---

# 🚨 Gestion des incidents

Les incidents sont générés à partir des anomalies détectées dans la supervision des terminaux.

Les niveaux de criticité sont :

```text
MEDIUM
HIGH
CRITICAL
```

Les types d'incidents comprennent :

```text
PERFORMANCE
CONNECTIVITY
SYSTEM_FAILURE
```

Les statuts sont :

```text
OPEN
IN_PROGRESS
RESOLVED
```

### KPIs incidents

Les analyses permettent notamment de mesurer :

* nombre total d'incidents ;
* incidents critiques ;
* incidents par niveau de sévérité ;
* incidents par type ;
* incidents par terminal ;
* incidents par ville ;
* temps moyen de résolution ;
* évolution mensuelle.

---

# 💳 Analyse des transactions

Le projet comporte actuellement un module SQL d'analyse des performances transactionnelles.

### Volume global

```text
100 000 transactions
```

### Montant total

```text
13 577 318 105,13 XOF
```

### Montant moyen

```text
135 773,18 XOF
```

### Taux de succès

```text
87,98 %
```

### Transactions suspectes

```text
4 515
```

soit :

```text
4,52 %
```

Le montant associé aux transactions suspectes représente :

```text
3 016 017 010,93 XOF
```

---

## 📈 Analyses disponibles

Le module transactionnel permet notamment d'analyser :

* performance globale ;
* transactions réussies / rejetées ;
* transactions suspectes ;
* performance par type de transaction ;
* performance par banque ;
* codes de réponse ;
* performance par ville ;
* évolution mensuelle ;
* activité horaire ;
* transactions suspectes à montant élevé.

### Types de transactions

```text
ATM_WD
POS_PAY
TRANSFER
BAL_INQ
CASH_DEP
ONLINE_PAY
```

### Codes de réponse

Le modèle comprend notamment :

```text
00 - SUCCESS
05 - DECLINED
14 - CARD_ERROR
51 - INSUFFICIENT_FUNDS
54 - CARD_ERROR
55 - AUTHENTICATION_ERROR
57 - AUTHORIZATION_ERROR
91 - SYSTEM_ERROR
96 - SYSTEM_ERROR
```

---

# 🔎 Détection des anomalies

Une première logique de détection basée sur des règles est déjà intégrée au processus de génération des transactions.

L'indicateur :

```text
is_suspicious
```

permet d'identifier des transactions présentant certains signaux de risque, notamment :

* montant élevé ;
* horaire inhabituel ;
* temps de traitement élevé ;
* certains codes de réponse ;
* combinaison de plusieurs signaux.

> Cette première version constitue une détection basée sur des règles et non un modèle de Machine Learning.

### Prochaine évolution

Le module sera progressivement enrichi avec :

```text
Rule-based detection
        │
        ▼
Risk scoring
        │
        ▼
Anomaly detection
        │
        ▼
Machine Learning
```

---

# 🧪 Contrôles qualité

Plusieurs contrôles sont effectués sur les données.

### Transactions

```text
Total transactions       : 100 000
Transactions sans lieu   : 0
```

### Localisations

```text
Villes distinctes : 6
```

Les localisations ont également fait l'objet d'un contrôle d'encodage afin d'éliminer les valeurs corrompues.

### Intégrité

Les relations entre :

* transactions ;
* terminaux ;
* banques ;
* cartes ;
* clients ;
* commerçants ;
* localisations ;
* codes réponse ;

sont assurées par les clés étrangères du Data Warehouse.

---

# 🛠️ Technologies utilisées

## Data Engineering

* Python
* SQL
* PostgreSQL
* Pandas
* NumPy
* Faker
* Psycopg2

## Infrastructure

* Docker
* Docker Compose

## Big Data — prévu

* Apache Spark
* PySpark

## Orchestration — prévu

* Apache Airflow

## Data Visualization — prévu

* Microsoft Power BI

## Versioning

* Git
* GitHub

---

# 📁 Structure du projet

```text
monetic-ops-supervision-platform/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── database/
│   ├── schemas/
│   │   ├── 01_create_schema.sql
│   │   ├── 02_create_dimensions.sql
│   │   ├── 03_create_facts.sql
│   │   ├── 04_seed_reference_data.sql
│   │   ├── 05_seed_dim_date.sql
│   │   └── 06_seed_additional_locations.sql
│   │
│   ├── tables/
│   │
│   └── queries/
│       ├── 01_incident_kpis.sql
│       ├── 02_terminal_performance.sql
│       └── 03_transaction_performance.sql
│
├── etl/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   ├── generate_data.py
│   ├── generate_transactions.py
│   ├── generate_terminal_status.py
│   └── generate_incidents.py
│
├── monitoring/
│   ├── terminal_monitoring/
│   ├── transaction_monitoring/
│   └── incident_detection/
│
├── fraud_detection/
│
├── airflow/
│   └── dags/
│
├── pyspark/
│
├── powerbi/
│
├── tests/
│
├── docker/
│
├── docs/
│
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

# 🚀 Installation

## 1. Cloner le projet

```bash
git clone https://github.com/GGFabrice/monetic-ops-supervision-platform.git
cd monetic-ops-supervision-platform
```

## 2. Créer l'environnement Python

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Installer les dépendances

```powershell
pip install -r requirements.txt
```

## 4. Démarrer PostgreSQL

Le projet utilise Docker pour exécuter PostgreSQL.

```powershell
docker compose up -d
```

## 5. Initialiser la base de données

Les scripts SQL du dossier :

```text
database/schemas/
```

permettent de créer le schéma, les dimensions, les tables de faits et les données de référence.

---

# 🔄 Pipeline actuel

Le pipeline actuellement construit suit cette logique :

```text
Création du Data Warehouse
          │
          ▼
Création des dimensions
          │
          ▼
Génération des données de référence
          │
          ▼
Génération des transactions
          │
          ▼
Supervision des terminaux
          │
          ▼
Génération des incidents
          │
          ▼
Analyses SQL
          │
          ▼
Contrôle qualité
```

---

# 🗺️ Roadmap

## ✅ Phase 1 — Data Warehouse

* [x] PostgreSQL
* [x] Docker
* [x] Schéma `monetic`
* [x] Dimensions
* [x] Tables de faits
* [x] Données de référence

## ✅ Phase 2 — Génération des données

* [x] Clients
* [x] Cartes
* [x] Terminaux
* [x] Commerçants
* [x] Transactions
* [x] Données de supervision

## ✅ Phase 3 — Supervision

* [x] Statuts des terminaux
* [x] Disponibilité
* [x] Temps de réponse
* [x] Incidents
* [x] KPIs incidents
* [x] KPIs terminaux

## ✅ Phase 4 — Analytics

* [x] KPIs transactions
* [x] Analyse par banque
* [x] Analyse par ville
* [x] Analyse par type
* [x] Analyse des codes réponse
* [x] Analyse horaire
* [x] Analyse mensuelle
* [x] Contrôles qualité

## 🔄 Phase 5 — Fraud Detection

* [ ] Architecture du module fraude
* [ ] Règles de détection avancées
* [ ] Risk scoring
* [ ] Classification des niveaux de risque
* [ ] Analyse des comportements suspects
* [ ] Machine Learning

## 🔄 Phase 6 — Big Data

* [ ] PySpark
* [ ] Traitement distribué
* [ ] Optimisation des traitements
* [ ] Pipeline Spark

## 🔄 Phase 7 — Orchestration

* [ ] Airflow
* [ ] DAG ETL
* [ ] Planification automatique
* [ ] Monitoring des pipelines

## 🔄 Phase 8 — Business Intelligence

* [ ] Modèle Power BI
* [ ] Dashboard exécutif
* [ ] Dashboard transactions
* [ ] Dashboard supervision
* [ ] Dashboard fraude
* [ ] KPIs opérationnels

---

# 📌 Statut actuel du projet

**Projet en développement actif.**

Le Data Warehouse, les pipelines de génération de données, la supervision des terminaux, la génération des incidents et les premières analyses SQL sont opérationnels.

La prochaine étape majeure est la construction du module **Fraud Detection & Risk Scoring**.

---

## 👨‍💻 Auteur

**Gnabo Fabrice**

Data Engineering | Data Analytics | Python | SQL | PostgreSQL | Power BI

GitHub :

https://github.com/GGFabrice

Projet :

https://github.com/GGFabrice/monetic-ops-supervision-platform
