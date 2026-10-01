# Data Quality Monitoring

Projet de monitoring de la qualité des données.

Les données de fréquentation sont générées par une API, extraites et stockées en CSV, puis nettoyées et transformées avec Pandas.

## Parquet vs CSV

Dans ce projet, les données brutes sont d'abord stockées au format CSV, puis les données nettoyées et transformées sont stockées au format Parquet.

### CSV

Le format CSV est un format texte simple. Il est facile à lire avec un éditeur de texte et peut être utilisé par de nombreux outils.

Cependant, il ne conserve pas directement les types des colonnes et peut devenir volumineux lorsque la quantité de données augmente.

### Parquet

Parquet est un format de stockage en colonnes, très utilisé dans le domaine de la data.

Contrairement au CSV, Parquet conserve le schéma et les types des données. Il permet également la compression des données et permet de lire seulement les colonnes nécessaires lors d'une analyse.

Dans ce projet, le CSV est utilisé pour stocker les données brutes dans `data/raw`, tandis que Parquet est utilisé pour stocker les données transformées dans `data/processed`.

## Orchestration avec Airflow

Pour simplifier l'exécution de ce projet en local, Airflow lance directement les scripts d'extraction et de transformation sur la machine locale.

Le DAG Airflow exécute les tâches dans cet ordre :

1. EXTRACT : récupération des données depuis l'API.
2. TRANSFORM : nettoyage et transformation des données.

Ces tâches sont orchestrées toutes les heures avec Airflow.

Dans un environnement de production, Airflow ne devrait pas exécuter directement ces traitements sur la machine locale. Airflow servirait plutôt à orchestrer des tâches exécutées sur des serveurs ou des services dédiés.

Les données pourraient par exemple être récupérées par ces serveurs puis stockées dans un stockage objet comme Amazon S3 avant d'être utilisées par les étapes de transformation.

L'exécution locale utilisée dans ce projet est donc une simplification permettant de démontrer le fonctionnement du pipeline.