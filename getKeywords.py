from urllib.parse import urlparse
from keybert import KeyBERT

import openpyxl
import requests
from bs4 import BeautifulSoup

mensaje = {}
urls = 0
urls_usadas = 0

def hacer_solicitud(url, timeout=5):
    parsed_url = urlparse(url.strip())
    if not (parsed_url.scheme and parsed_url.netloc):
        mensaje['id'] = 504
        mensaje['mensaje'] = 'La URL es inválida'
        return mensaje

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        mensaje['id'] = 200
        mensaje['mensaje'] = 'Solicitud exitosa'
        return mensaje
    except requests.exceptions.Timeout:
        mensaje['id'] = 503
        mensaje['mensaje'] = 'El tiempo de espera fue excedido'
        return mensaje
    except requests.exceptions.RequestException as e:
        mensaje['id'] = 502
        mensaje['mensaje'] = 'Error en la solicitud'
        return mensaje

def extractKeywords(url):
    respuesta = hacer_solicitud(url, 5)
    if respuesta['id'] == 200 :
        respuesta_http = requests.get(url, timeout=5)
        soup = BeautifulSoup(respuesta_http.text, "html.parser")
        texto = soup.get_text()
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(texto, keyphrase_ngram_range=(1, 2), stop_words=None)
        palabras_sin_repetir = set(keywords)
        keys = " ".join(str(elemento[0]) for elemento in palabras_sin_repetir)
        return keys
    else:
        return respuesta
