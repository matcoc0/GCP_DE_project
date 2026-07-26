# Open-Meteo Data Pipeline

POC Data Engineering destiné à ingérer, historiser et transformer des
prévisions météorologiques et des données de qualité de l'air issues des API
Open-Meteo.

## Objectifs

- Interroger les API Open-Meteo Weather et Air Quality.
- Conserver les réponses JSON brutes.
- Normaliser les séries horaires.
- Mettre en place des contrôles qualité.
- Charger les données dans Cloud Storage et BigQuery.
- Orchestrer le pipeline avec Airflow.
- Tester le code avec Pytest.
- Exécuter les contrôles automatiquement avec GitHub Actions.
- Provisionner les ressources GCP avec Terraform.

## Architecture cible

```text
Open-Meteo APIs
        |
        v
Python CLI
        |
        v
Cloud Storage
        |
        v
Transformations and quality checks
        |
        v
BigQuery
        ^
        |
Airflow orchestration
```