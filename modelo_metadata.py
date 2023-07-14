import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from getMeta import *
from obtenerMetadata import *
import joblib

def analisis_modelo(url):
    resultado = analizar_data(url)
    print(resultado)
    if len(resultado) == 2:
        return resultado
    df= pd.read_csv("metadataset.csv")
    data = df.dropna()
    X = data.drop(labels=['result'],axis=1)
    y = data['result'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=0)
    model = RandomForestClassifier(n_estimators = 29,
                                      random_state = 2016,
                                      min_samples_leaf = 1,)

    try:
        prediction = model.predict(resultado)
        respuesta = {}
        respuesta['id'] = prediction.item()
        respuesta["metodo"] = 'metadata'
        # Imprimir el resultado de la predicción
        if respuesta['id'] == 1:
            respuesta['mensaje'] = "Alta probabilidad de phishing"
        else:
            respuesta['mensaje'] = "Baja probabilidad de phishing"
        return respuesta
    except requests.exceptions.RequestException as e:
        respuesta['id'] = 506
        respuesta['mensaje'] = "Excepción en algoritmo: ",e
        print("Excepción en algoritmo")
        return respuesta
