from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from getMeta import *
from pln_svc import *
from modelo_metadata import *
from obtenerMetadata import *
import threading

app = FastAPI()

# Variable de bloqueo
lock = threading.Lock()

origins = [
    "http://127.0.0.1:8000/",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# http://127.0.0.1:8000
@app.get("/")
def index():
    return "Estás usando la API de análisis de metadata y PLN de la tesis"

@app.get("/url/{url:path}")
def analisis(url: str): 
    respuesta = []   
    if lock.locked():
        print ("El análisis ya está en progreso")
    
    with lock:
        respuestaMeta = analisis_modelo(url)
        respuestaPLN = analisis_pln(url)

        print("Respuesta META: ",respuestaMeta)
        print("Respuesta PLN: ",respuestaPLN)
        print("Respuesta URL: ",url)

        respuesta.append(respuestaMeta)
        respuesta.append(respuestaPLN)
        respuesta.append({'url': url})
        print(respuesta)
        return respuesta
