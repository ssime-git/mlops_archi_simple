import os
import mlflow
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
# Add the root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.utils.logging_config import setup_logging
from dotenv import load_dotenv

def load_data():
    X_train = pd.read_csv('data/processed/X_train.csv')
    y_train = pd.read_csv('data/processed/y_train.csv')
    X_test = pd.read_csv('data/processed/X_test.csv')
    y_test = pd.read_csv('data/processed/y_test.csv')
    return X_train, y_train.values.ravel(), X_test, y_test.values.ravel()

def train_model(X_train, y_train, n_estimators, max_depth):
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    return accuracy, precision, recall, f1


def main():
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

    mlflow.set_tracking_uri(f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow")
    logger.info("MLflow configuré avec succès.")

    try:
        mlflow.set_experiment("iris_classification")
        logger.info("Expérience MLflow configurée avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la configuration de l'expérience MLflow: {e}")
        return

    # Chargement des données
    logger.info("Chargement des données...")
    X_train, y_train, X_test, y_test = load_data()
    logger.info("Données chargées avec succès.")

    # Définition des paramètres du modèle
    n_estimators = 100
    max_depth = 5

    # Entraînement et évaluation du modèle avec MLflow
    with mlflow.start_run():
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)

        logger.info("Entraînement du modèle...")
        model = train_model(X_train, y_train, n_estimators, max_depth)
        logger.info("Modèle entraîné avec succès.")

        logger.info("Évaluation du modèle...")
        accuracy, precision, recall, f1 = evaluate_model(model, X_test, y_test)
        logger.info("Modèle évalué avec succès.")

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        # Enregistrement du modèle
        mlflow.sklearn.log_model(model, "model")

        logger.info(f"Accuracy: {accuracy}")
        logger.info(f"Precision: {precision}")
        logger.info(f"Recall: {recall}")
        logger.info(f"F1-score: {f1}")

if __name__ == "__main__":

    # Configuration du logger
    logger = setup_logging()

    # configuration du logger
    logger.info("Démarrage du script...")

    # execution du script
    main()
    logger.info("Fin du script.")