import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from getKeywords import *
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import joblib
import matplotlib.pyplot as plt
import numpy as np


def analisis_pln(url):
    nuevo_texto = extractKeywords(url)
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    data = pd.read_csv('data2.csv')
    data.dropna(inplace=True)
    text = data['text']
    y = data['result']

    tokens = [word_tokenize(t) for t in text]
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [[token for token in tokens if token.lower() not in stop_words] for tokens in tokens]

    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [[lemmatizer.lemmatize(token) for token in tokens] for tokens in filtered_tokens]

    processed_text = [' '.join(tokens) for tokens in lemmatized_tokens]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(processed_text)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    from sklearn.metrics import accuracy_score
    
    classifiersvm = joblib.load('modelo_entrenadoSVC.pkl')
    y_predsvm = classifiersvm.predict(X_test)
    print(classification_report(y_test, y_predsvm))
    accuracysvm = accuracy_score(y_test, y_predsvm)
    print("Precisión del modelo SVC: {:.2f}%".format(accuracysvm * 100))

    if isinstance(nuevo_texto, str):
        nuevo_tokens = word_tokenize(nuevo_texto)
        nuevo_tokens_filtrados = [token for token in nuevo_tokens if token.lower() not in stop_words]
        nuevo_lemmatized_tokens = [lemmatizer.lemmatize(token) for token in nuevo_tokens_filtrados]
        nuevo_processed_text = ' '.join(nuevo_lemmatized_tokens)
        nuevo_texto_transformado = vectorizer.transform([nuevo_processed_text])

        prediccionSVM = classifiersvm.predict(nuevo_texto_transformado)
        respuesta = {}
        respuesta['id'] = prediccionSVM.item()
        respuesta['metodo'] = 'PLN'
        if prediccionSVM.item() == 0:
            respuesta['mensaje'] = "Baja probabilidad de phishing"
        else:
            respuesta['mensaje'] = "Alta probabilidad de phishing"
        return(respuesta)
    else:
        return(nuevo_texto)
