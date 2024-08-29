import os
import dvc.api
from dotenv import load_dotenv
import subprocess  # Ajouté pour exécuter des commandes shell

def fetch_data():
    load_dotenv()
    # Récupération des variables d'environnement
    dagshub_token = os.getenv('DAGSHUB_TOKEN')

    # Configuration de MLflow
    os.environ['MLFLOW_TRACKING_PASSWORD'] = dagshub_token

    # Configurations DVC
    repo_url = f"https://dagshub.com/{os.getenv('REPO_OWNER')}/{os.getenv('REPO_NAME')}.dvc"
    
    # Assurez-vous que le dossier data/processed existe
    os.makedirs('data/processed', exist_ok=True)

    # Commande pour pull les données avec DVC
    subprocess.run(['dvc', 'pull'], check=True)

    print("Données récupérées avec succès depuis DagShub.")

if __name__ == "__main__":
    fetch_data()