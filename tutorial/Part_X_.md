# Construction d'un Dockerfile pour l'entraînement du modèle

## Étape 1: Création du Dockerfile

1. Créez un fichier nommé `Dockerfile.train` dans le répertoire racine de votre projet.

2. Ajoutez le code suivant au fichier:

```dockerfile
```
3. créer le fichier .dockerignore avec le contenu suivant:

```
.env
data/processed
data/raw
tutorial
venv
.dvc/config.local
```

## Étape 2: Exécution du Dockerfile

1. Assurez-vous que votre environnement Docker est en cours d'exécution.
2. Exécutez la commande suivante dans le répertoire racine de votre projet:

```bash
# construire l'image Docker
make compose

# le script construit l'image et lance le conteneur

# pour entrer dans le conteneur
make compose-train
```
