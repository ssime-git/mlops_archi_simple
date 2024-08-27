# Tutoriel MLOps pour débutants - Partie 2: Ajout et prétraitement des données

Dans cette partie, nous allons ajouter le jeu de données Iris à notre projet et créer un script pour le prétraitement.

## Étape 1: Ajout des données Iris

1. Créez un script Python pour télécharger les données Iris:
   ```sh
   touch src/data/download_data.py
   ```

2. Ajoutez le contenu suivant à `src/data/download_data.py`:
   ```python
   import pandas as pd
   from sklearn.datasets import load_iris
   import os

   def download_iris_data():
       # Charger le jeu de données Iris
       iris = load_iris()
       
       # Créer un DataFrame
       df = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                         columns= iris['feature_names'] + ['target'])
       
       # Créer le dossier de données brutes s'il n'existe pas
       os.makedirs('data/raw', exist_ok=True)
       
       # Sauvegarder les données en CSV
       df.to_csv('data/raw/iris.csv', index=False)

   if __name__ == "__main__":
       download_iris_data()
   ```

3. Exécutez le script pour télécharger les données:
   ```sh
   python src/data/download_data.py
   ```

4. Ajoutez les données à DVC:
   ```sh
   dvc add data/raw/iris.csv
   ```

## Étape 2: Création du script de prétraitement

1. Créez un script Python pour le prétraitement:
   ```
   touch src/data/preprocess.py
   ```

2. Ajoutez le contenu suivant à `src/data/preprocess.py`:
   ```python
   import pandas as pd
   from sklearn.model_selection import train_test_split
   import os

   def preprocess_data():
       # Charger les données
       df = pd.read_csv('data/raw/iris.csv')
       
       # Séparer les features et la cible
       X = df.drop('target', axis=1)
       y = df['target']
       
       # Diviser les données en ensembles d'entraînement et de test
       X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
       
       # Créer le dossier de données traitées s'il n'existe pas
       os.makedirs('data/processed', exist_ok=True)
       
       # Sauvegarder les données traitées
       X_train.to_csv('data/processed/X_train.csv', index=False)
       X_test.to_csv('data/processed/X_test.csv', index=False)
       y_train.to_csv('data/processed/y_train.csv', index=False)
       y_test.to_csv('data/processed/y_test.csv', index=False)

   if __name__ == "__main__":
       preprocess_data()
   ```

3. Exécutez le script de prétraitement:
   ```sh
   python src/data/preprocess.py
   ```

4. Ajoutez les données prétraitées à DVC:
   ```
   dvc add data/processed
   ```

## Étape 3: Mise à jour du fichier .gitignore

Ajoutez les lignes suivantes à votre fichier `.gitignore` pour éviter de suivre les fichiers de données volumineux avec Git:

```sh
data/raw/
data/processed/
```

## Étape 4: Commit et push des changements

1. Ajoutez les nouveaux fichiers à Git:
   ```
   git add .
   ```

2. Committez les changements:
   ```
   git commit -m "Add Iris data and preprocessing script"
   ```

3. Poussez les changements vers DagShub:
   ```
   git push origin main
   dvc push
   ```

Félicitations! Vous avez maintenant ajouté les données Iris à votre projet et créé un script de prétraitement. Dans la prochaine partie, nous nous concentrerons sur la création d'un modèle de classification et son entraînement avec MLflow.