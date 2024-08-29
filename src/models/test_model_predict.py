import os
import sys
import mlflow
import pandas as pd
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.utils.logging_config import setup_logging

def main():
    # Chargement des variables d'environnement
    load_dotenv()
    logger = setup_logging()
    logger.info("Variables d'environnement chargées.")

    # Récupération des variables d'environnement
    dagshub_username = os.getenv('DAGSHUB_USERNAME')
    dagshub_token = os.getenv('DAGSHUB_TOKEN')
    repo_owner = os.getenv('REPO_OWNER')
    repo_name = os.getenv('REPO_NAME')

    if not all([dagshub_username, dagshub_token, repo_owner, repo_name]):
        logger.error("Veuillez définir toutes les variables d'environnement nécessaires.")
        return

    # Configuration de MLflow
    os.environ['MLFLOW_TRACKING_USERNAME'] = dagshub_username
    os.environ['MLFLOW_TRACKING_PASSWORD'] = dagshub_token
    mlflow.set_tracking_uri(f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow")
    logger.info("MLflow configuré avec succès.")

    try:
        # Chargement du modèle depuis MLflow
        model_name = "iris_classification_model"  # Remplacez par le nom de votre modèle
        stage = "Production"  # ou "Staging", selon votre configuration
        
        model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{stage}")
        logger.info(f"Modèle '{model_name}' (stage: {stage}) chargé avec succès.")

        # Préparation des données pour la prédiction
        # Remplacez ceci par vos propres données d'entrée
        input_data = pd.DataFrame({
            'sepal length (cm)': [5.1],
            'sepal width (cm)': [3.5],
            'petal length (cm)': [1.4],
            'petal width (cm)': [0.2]
        })

        # Prédiction
        prediction = model.predict(input_data)
        logger.info(f"Prédiction effectuée : {prediction}")

    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle ou de la prédiction : {e}")

if __name__ == "__main__":
    main()