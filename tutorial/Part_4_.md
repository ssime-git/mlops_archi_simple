# Tutoriel MLOps pour débutants - Partie 4: Automatisation avec GitHub Actions

Dans cette partie, nous allons configurer GitHub Actions pour automatiser le processus d'entraînement de notre modèle.

## Étape 1: Configuration de GitHub

1. Si ce n'est pas déjà fait, créez un compte GitHub et un nouveau dépôt pour votre projet.

2. Poussez votre code local vers GitHub:
   ```
   git remote add github https://github.com/votre-nom-utilisateur/iris_mlops_project.git
   git push -u github main
   ```

## Étape 2: Configuration des secrets GitHub

Nous devons configurer des secrets pour que GitHub Actions puisse accéder à DagShub:

1. Allez dans les paramètres de votre dépôt GitHub.
2. Cliquez sur "Secrets and variables" dans le menu de gauche, puis "Actions".
3. Ajoutez les secrets suivants:
   - `DAGSHUB_USERNAME`: Votre nom d'utilisateur DagShub
   - `DAGSHUB_TOKEN`: Votre token DagShub (généré dans les paramètres de votre compte DagShub)

## Étape 3: Création du workflow GitHub Actions

1. Créez un nouveau dossier `.github/workflows` à la racine de votre projet:
   ```
   mkdir -p .github/workflows
   ```

2. Créez un nouveau fichier YAML pour le workflow:
   ```
   touch .github/workflows/train_model.yml
   ```

3. Ajoutez le contenu suivant au fichier `train_model.yml`:
   ```yaml
   name: Train Model

   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
     workflow_dispatch:

   jobs:
     train:
       runs-on: ubuntu-latest

       steps:
       - uses: actions/checkout@v2

       - name: Set up Python
         uses: actions/setup-python@v2
         with:
           python-version: '3.8'

       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -r requirements.txt

       - name: Configure DVC
         env:
           DAGSHUB_USERNAME: ${{ secrets.DAGSHUB_USERNAME }}
           DAGSHUB_TOKEN: ${{ secrets.DAGSHUB_TOKEN }}
         run: |
           dvc remote modify origin --local auth basic
           dvc remote modify origin --local user $DAGSHUB_USERNAME
           dvc remote modify origin --local password $DAGSHUB_TOKEN

       - name: Pull data from DVC
         run: dvc pull

       - name: Train model
         env:
           MLFLOW_TRACKING_USERNAME: ${{ secrets.DAGSHUB_USERNAME }}
           MLFLOW_TRACKING_PASSWORD: ${{ secrets.DAGSHUB_TOKEN }}
         run: python src/models/train_model.py

       #- name: Push model to DVC
       #  run: |
       #    dvc add models/model.pkl
       #    git add models/model.pkl.dvc
       #    git config user.name "GitHub Actions Bot"
       #    git config user.email "<>"
       #    git commit -m "Update model"
       #    dvc push
      
       - name: Push changes to GitHub
         uses: ad-m/github-push-action@master
         with:
           github_token: ${{ secrets.GITHUB_TOKEN }}
           branch: ${{ github.ref }}
   ```

## Étape 4: Mise à jour du fichier requirements.txt

Assurez-vous que votre fichier `requirements.txt` contient toutes les dépendances nécessaires:

```
numpy
pandas
scikit-learn
mlflow
pyyaml
dvc[s3]
```

## Étape 5: Commit et push des changements

1. Ajoutez les nouveaux fichiers à Git:
   ```
   git add .
   ```

2. Committez les changements:
   ```
   git commit -m "Add GitHub Actions workflow for model training"
   ```

3. Poussez les changements vers GitHub:
   ```
   git push github main
   ```

## Étape 6: Vérification du workflow

1. Allez sur votre dépôt GitHub.
2. Cliquez sur l'onglet "Actions".
3. Vous devriez voir votre workflow "Train Model" en cours d'exécution ou terminé.

## Étape 7: Déclenchement manuel du workflow

1. Sur la page des Actions de votre dépôt GitHub, cliquez sur "Train Model" dans la liste des workflows.
2. Cliquez sur "Run workflow" et sélectionnez la branche main.
3. Cliquez sur le bouton "Run workflow" vert pour déclencher manuellement le workflow.

Félicitations! Vous avez maintenant configuré un pipeline d'entraînement automatisé avec GitHub Actions. Ce workflow s'exécutera automatiquement à chaque push sur la branche main, lors de l'ouverture d'une pull request, et peut également être déclenché manuellement.

Dans la prochaine partie, nous nous concentrerons sur la création d'un pipeline de déploiement continu pour notre modèle.