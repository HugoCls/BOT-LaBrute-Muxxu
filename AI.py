import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import os

model = load_model(f"{os.getcwd()}/data/predict_model.h5")

def create_model():
    # traitez les éléments séparés ici
    # générer des données de combat simulées
    np.random.seed(0)
    caracteristics,results = get_fights()
    
    # séparer les données en entrée (caractéristiques) et cible (résultat)
    X = caracteristics
    Y = results
    
    # définir le modèle
    model = Sequential()
    model.add(Dense(units=64, activation='relu', input_dim=4))
    model.add(Dense(units=1, activation='sigmoid'))
    
    # compiler le modèle
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    # entraîner le modèle
    model.fit(X, Y, epochs=1000, verbose=1, validation_split = 0.2, batch_size=32)
    
    # sauvegarder le modèle
    model.save(f"{os.getcwd()}/data/predict_model.h5")


def use_model(nouveau_combattant):
    
    nouveau_combattant = np.array([nouveau_combattant])
    #nouveau_combattant = np.random.randint(0, 100, size=(1, 4))
    
    #•print(nouveau_combattant)
    # par défault: simuler des données de combat simulées pour un nouveau combattant
     
    # faire une prédiction avec le modèle formé
    probabilite_victoire = model.predict(nouveau_combattant,verbose=0)
    #print("Probabilité de victoire:", probabilite_victoire[0][0])
    return probabilite_victoire[0][0]

def get_fights():
    pass