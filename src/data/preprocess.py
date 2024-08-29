import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pandas as pd
from sklearn.model_selection import train_test_split

# logging
from src.utils.logging_config import setup_logging

# dotenv
from dotenv import load_dotenv

def preprocess_data(logger):
    # chargement des variables d'environnement
    load_dotenv()
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

    # Configuration du logger
    logger.info("Début du script de prétraitement.")
    try:
        # Charger les données
        df = pd.read_csv('data/raw/iris.csv')
    except FileNotFoundError:
        print("Erreur: Le fichier 'data/raw/iris.csv' est introuvable.")
        return
    except pd.errors.EmptyDataError:
        print("Erreur: Le fichier 'data/raw/iris.csv' est vide.")
        return
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return
    
    # Séparer les features et la cible
    logger.info("Séparation des features et de la cible.")
    X = df.drop('target', axis=1)
    y = df['target']
    logger.info("Séparation des données en ensembles d'entraînement et de test.")
    
    # Diviser les données en ensembles d'entraînement et de test
    logger.info("Division des données en ensembles d'entraînement et de test.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Créer le dossier de données traitées s'il n'existe pas
    os.makedirs('data/processed', exist_ok=True)
    logger.info("Sauvegarde des données traitées.")

    # Sauvegarder les données traitées
    logger.info("Sauvegarde des données traitées.")
    X_train.to_csv('data/processed/X_train.csv', index=False)
    X_test.to_csv('data/processed/X_test.csv', index=False)
    y_train.to_csv('data/processed/y_train.csv', index=False)
    y_test.to_csv('data/processed/y_test.csv', index=False)
    logger.info("Ajout des fichiers à DVC.")

    # Ajouter les fichiers à DVC
    logger.info("Ajout des fichiers à DVC...")
    os.system('dvc add data/processed/X_train.csv data/processed/X_test.csv data/processed/y_train.csv data/processed/y_test.csv')

    # Pousser les changements vers le stockage distant DVC
    logger.info("Envoi des données vers le stockage distant DVC...")
    os.system('dvc push')

    logger.info("Prétraitement des données terminé.")


if __name__ == "__main__":

    # Configuration du logger
    logger = setup_logging()

    # execution du script
    preprocess_data(logger)
    logger.info("Fin du script de prétraitement.")