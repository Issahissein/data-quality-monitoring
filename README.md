# Data Quality Monitoring

Projet de **Data Engineering** permettant de simuler, collecter, contrôler, transformer et visualiser des données de fréquentation provenant de plusieurs capteurs.

L'objectif du projet est de construire un pipeline de données complet tout en mettant en pratique plusieurs problématiques de **qualité des données**.

## Objectif du projet

Le projet simule des capteurs installés dans différents lieux afin de mesurer le nombre de visiteurs.

Le pipeline permet de :

- générer des données de fréquentation avec une API ;
- extraire automatiquement les données ;
- stocker les données brutes au format CSV ;
- simuler et détecter des problèmes de qualité de données ;
- nettoyer et transformer les données avec Pandas ;
- stocker les données transformées au format Parquet ;
- interroger les données avec DuckDB ;
- visualiser les résultats avec Streamlit ;
- orchestrer l'extraction et la transformation avec Apache Airflow.

## Architecture du pipeline

```text
Capteurs simulés
      │
      ▼
FastAPI
      │
      ▼
EXTRACT
extract_data.py
      │
      ▼
data/raw
CSV
      │
      ▼
TRANSFORM
transform_data.py
      │
      ▼
data/processed
Parquet
      │
      ▼
DuckDB
      │
      ▼
Streamlit
```

Apache Airflow orchestre les étapes :

```text
EXTRACT ──────► TRANSFORM
```

Le DAG est configuré pour exécuter le pipeline toutes les heures.

## Technologies utilisées

- Python
- FastAPI
- Pandas
- NumPy
- Parquet / PyArrow
- DuckDB
- Streamlit
- Plotly
- Apache Airflow
- Git
- GitHub

## API et génération des données

L'API est développée avec **FastAPI**.

Elle simule plusieurs capteurs de fréquentation associés à différents lieux.

La route :

```text
GET /visits
```

permet de récupérer les données de fréquentation pour une date donnée.

Chaque donnée contient notamment :

- la date ;
- l'heure ;
- l'identifiant du lieu ;
- l'identifiant du capteur ;
- le nombre de visiteurs ;
- l'unité de mesure.

Les données sont générées heure par heure.

## Extraction des données

Le script :

```text
extract_data.py
```

interroge l'API afin de récupérer les données.

Les données brutes sont ensuite enregistrées dans :

```text
data/raw/
```

Un fichier CSV est créé pour chaque mois.

Le projet introduit également volontairement certaines données incorrectes afin de simuler des problèmes de qualité de données, par exemple :

- un identifiant de capteur manquant ;
- une unité incorrecte.

Ces anomalies sont ensuite traitées pendant l'étape de transformation.

## Transformation et qualité des données

Le script :

```text
transform_data.py
```

lit les fichiers CSV présents dans `data/raw`.

Les données sont ensuite nettoyées afin de supprimer les valeurs manquantes et les unités inattendues.

La fréquentation est agrégée par :

- date ;
- lieu ;
- capteur.

Le pipeline calcule également la moyenne des **4 jours similaires précédents** pour chaque capteur.

Un pourcentage d'évolution est ensuite calculé afin de comparer la fréquentation du jour avec cette moyenne.

Les données transformées sont enregistrées dans :

```text
data/processed/filtered.parquet
```

## Parquet vs CSV

Dans ce projet, les données brutes sont d'abord stockées au format **CSV**, puis les données nettoyées et transformées sont stockées au format **Parquet**.

### CSV

Le format CSV est un format texte simple. Il est facile à lire et peut être utilisé par de nombreux outils.

Cependant, il ne conserve pas directement les types des colonnes et peut devenir volumineux lorsque la quantité de données augmente.

### Parquet

Parquet est un format de stockage en colonnes très utilisé dans le domaine de la data.

Contrairement au CSV, Parquet conserve le schéma et les types des données. Il permet également la compression et permet de lire uniquement les colonnes nécessaires lors d'une analyse.

Dans ce projet :

```text
data/raw        → CSV
data/processed  → Parquet
```

## Visualisation avec Streamlit et DuckDB

Une application **Streamlit** permet de visualiser les données transformées.

**DuckDB** est utilisé pour interroger directement les données stockées dans le fichier Parquet.

La sidebar permet à l'utilisateur de sélectionner :

- un lieu ;
- un capteur associé à ce lieu ;
- une période : semaine ou mois.

L'application affiche les données correspondant à la sélection ainsi que des graphiques permettant de visualiser :

- les valeurs journalières ;
- la moyenne des 4 derniers jours similaires.

## Orchestration avec Apache Airflow

**Apache Airflow** est utilisé pour orchestrer le pipeline.

Le DAG contient deux tâches :

```text
extract
   │
   ▼
transform
```

La tâche `extract` exécute le script d'extraction des données.

Une fois cette tâche terminée, la tâche `transform` lance le traitement et la création des données Parquet.

Le DAG est configuré avec :

```python
schedule="@hourly"
```

afin d'orchestrer le pipeline toutes les heures.

### Airflow en production

Pour simplifier l'exécution de ce projet, Airflow lance directement les scripts d'extraction et de transformation sur la machine locale.

Dans un environnement de production, Airflow ne devrait pas exécuter directement ces traitements sur la machine locale.

Il servirait plutôt à orchestrer des tâches exécutées sur des serveurs ou des services dédiés.

Les données pourraient par exemple être stockées dans un stockage objet comme **Amazon S3** avant d'être utilisées par les différentes étapes du pipeline.

L'architecture locale de ce projet est donc une simplification permettant de démontrer le fonctionnement du pipeline.

## Structure principale du projet

```text
data-quality-monitoring/
│
├── dags/
│   └── data_quality_dag.py
│
├── data/
│   ├── raw/
│   └── processed/
│       └── filtered.parquet
│
├── src/
│   ├── app.py
│   └── sensor.py
│
├── app.py
├── extract_data.py
├── transform_data.py
├── requirements.txt
└── README.md
```

## Pipeline complet

```text
FastAPI
   │
   ▼
Extraction
   │
   ▼
CSV brut
   │
   ▼
Contrôle de la qualité
   │
   ▼
Transformation Pandas
   │
   ▼
Parquet
   │
   ▼
DuckDB
   │
   ▼
Streamlit
```

L'extraction et la transformation sont orchestrées avec **Apache Airflow**.