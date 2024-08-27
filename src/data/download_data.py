import os
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

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