import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from getMeta import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def analisis_modelo(url):
    resultado = analizar_data(url)
    if len(mensaje) == 2:
        return mensaje
    df= pd.read_csv("pruebalarga5050.csv")
    df = df.dropna()
    data = df[['has-Google-Site', 'has-Tag-Manager','has-Analytics', 'has-description','has-title', 'result']]
    vectorizer = CountVectorizer()
    #X = vectorizer.fit_transform(data['URL'])
    X = data.drop(labels=['result'],axis=1)
    y = data['result'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=0)

    model = RandomForestClassifier(n_estimators = 29,#joblib.load('modelo_entrenadoRF.pkl')
                                      random_state = 2016,
                                      min_samples_leaf = 1,)
    #model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    #print("Precisión del análisis :", accuracy*100,"%")

    # Preprocesar el enlace ingresado por el usuario
    #url_transformed = vectorizer.transform([url])

    # Realizar la predicción
    #print(type(url_transformed))

    try:
        prediction = model.predict(resultado)
        #feature_list = list(X.columns)
        #feature_imp = pd.Series(model.feature_importances_,index=feature_list).sort_values(ascending=False)
        #print(feature_imp)
        # Imprimir el resultado de la predicción
        if prediction[0] == 1:
            respuesta = {}
            respuesta['id'] = 11
            respuesta['respuesta'] = "Alta probabilidad de phishing"
            print("Alta probabilidad de phishing.")
            return respuesta
        else:
            respuesta = {}
            respuesta['id'] = 10
            respuesta['respuesta'] = "Baja probabilidad de phishing"
            print("Baja probabilidad de phishing.")
            return respuesta
    except requests.exceptions.RequestException as e:
        respuesta = {}
        respuesta['id'] = 2
        respuesta['respuesta'] = "Excepción en algoritmo: ",e
        print("Excepción en algoritmo")
        return respuesta
