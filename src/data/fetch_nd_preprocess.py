import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# logging
from src.utils.logging_config import setup_logging
from src.data.download_data import download_iris_data
from src.data.preprocess import preprocess_data

# dotenv
from dotenv import load_dotenv

def fetch_nd_preprocess():
    # chargement des variables d'environnement
    load_dotenv()

    # Configuration du logger
    logger = setup_logging()

    # Récupération des données
    logger.info("Récupération des données...")
    download_iris_data()
    logger.info("Données récupérées avec succès.")
    
    # Prétraitement des données
    logger.info("Prétraitement des données...")
    preprocess_data(logger)
    logger.info("Données prétraitées avec succès.")

if __name__ == "__main__":
    fetch_nd_preprocess()
    