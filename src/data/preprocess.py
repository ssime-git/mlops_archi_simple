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