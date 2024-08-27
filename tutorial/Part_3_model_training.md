# Tutoriel MLOps pour débutants - Partie 3: Création et entraînement du modèle avec MLflow

Dans cette partie, nous allons créer un modèle de classification pour les données Iris, l'entraîner, et utiliser MLflow pour suivre nos expériences.

## Étape 1: Configuration de MLflow

1. Créez un fichier de configuration pour MLflow s'il n'existe pas déjà:
   ```sh
   touch configs/mlflow_config.yml
   ```

2. Ajoutez le contenu suivant au fichier `configs/mlflow_config.yml`:
   ```yaml
   mlflow:
     tracking_uri: https://dagshub.com/ssime-git/mlops_archi_simple.mlflow
     experiment_name: iris_classification
   ```

   N'oubliez pas de remplacer `ssime-git` par votre nom d'utilisateur DagShub.

## Étape 2: Création du script d'entraînement

1. Créez un nouveau fichier pour le script d'entraînement:
   ```
   touch src/models/train_model.py
   ```

2. Ajoutez le contenu suivant au fichier `src/models/train_model.py`:
   ```python
   import pandas as pd
   import numpy as np
   from sklearn.ensemble import RandomForestClassifier
   from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
   import mlflow
   import yaml

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
       # Charger la configuration MLflow
       with open('configs/mlflow_config.yml', 'r') as file:
           mlflow_config = yaml.safe_load(file)

       # Configurer MLflow
       mlflow.set_tracking_uri(mlflow_config['mlflow']['tracking_uri'])
       mlflow.set_experiment(mlflow_config['mlflow']['experiment_name'])

       # Charger les données
       X_train, y_train, X_test, y_test = load_data()

       # Définir les paramètres du modèle
       n_estimators = 100
       max_depth = 5

       # Entraîner et évaluer le modèle avec MLflow
       with mlflow.start_run():
           mlflow.log_param("n_estimators", n_estimators)
           mlflow.log_param("max_depth", max_depth)

           model = train_model(X_train, y_train, n_estimators, max_depth)
           accuracy, precision, recall, f1 = evaluate_model(model, X_test, y_test)

           mlflow.log_metric("accuracy", accuracy)
           mlflow.log_metric("precision", precision)
           mlflow.log_metric("recall", recall)
           mlflow.log_metric("f1_score", f1)

           # Enregistrer le modèle
           mlflow.sklearn.log_model(model, "model")

           print(f"Accuracy: {accuracy}")
           print(f"Precision: {precision}")
           print(f"Recall: {recall}")
           print(f"F1-score: {f1}")

   if __name__ == "__main__":
       main()
   ```

## Étape 3: Exécution de l'entraînement

1. Exécutez le script d'entraînement:
   ```sh
   python src/models/train_model.py
   ```

   Ce script va entraîner le modèle, évaluer ses performances et enregistrer les résultats dans MLflow.

## Étape 4: Vérification des résultats dans DagShub

1. Allez sur votre projet DagShub.
2. Naviguez vers l'onglet "Experiments" pour voir les résultats de votre entraînement.

## Étape 5: Ajout des fichiers au contrôle de version

1. Ajoutez les nouveaux fichiers à Git:
   ```sh
   git add .
   ```

2. Committez les changements:
   ```sh
   git commit -m "Add model training script and MLflow integration"
   ```

3. Poussez les changements vers DagShub:
   ```sh
   git push
   ```

Félicitations! Vous avez maintenant créé un modèle de classification pour les données Iris, l'avez entraîné, et avez utilisé MLflow pour suivre vos expériences. Dans la prochaine partie, nous nous concentrerons sur la création d'un pipeline d'entraînement automatisé avec GitHub Actions.