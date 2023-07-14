from htmldate import find_date
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import OpenSSL
import ssl
import whois
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import requests
from fuzzywuzzy import fuzz
import re

def web_indexada(website_url):
    return 0
def ssl_vigencia(url):
    parsed_url = urlparse(url).netloc
    try:
        cert=ssl.get_server_certificate((parsed_url, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        inicioSSL = datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%S%z').date()
        finSSL=datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%S%z').date()
        diferencia_fecha = finSSL-inicioSSL
        if diferencia_fecha < timedelta(days=180):
            return 1
        else:
            return 0
        cn = x509.get_subject()
        organization = x509.get_subject().O
        print(cn)
        print(organization)
    except Exception as error:
        print(f"Error: {error}")
        return 1
def coincide_cn_con_url(url):
    try:
        parsed_url = urlparse(url).netloc
        cert = ssl.get_server_certificate((parsed_url, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        cn = x509.get_subject().CN.lower()
        porcentaje_cn = fuzz.ratio(parsed_url.lower(), cn)
        if porcentaje_cn < 87:
            return 1
        else:
            return 0
    except Exception as error:
        print(f"Error en método coincide_cn_con_url: {error}")
        return 1
def obtener_edad_dominio(url):
    try:
        parsed_url = urlparse(url).netloc
        informacion = whois.query(parsed_url)
        fecha_creacion = informacion.creation_date
        if datetime.now() - fecha_creacion < timedelta(days=180):
            return 1
        else:
            return 0
    except Exception as error:
        print("Error: ",error)
        return 1
def https_en_url(url):
    try:
        parsed_url = urlparse(url)
        netloc_pos = url.find(parsed_url.netloc)
        https_pos = url.find("https", netloc_pos)
        if https_pos > -1:
            return 1
        else:
            return 0
    except Exception as error:
        print("Error en https_en_url: ",error)
        return 1
def es_direccion_ip(url):
    try:
        pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        match = re.match(pattern, url)
        if bool(match):
            return 1
        else:
            return 0
    except Exception as error:
        print("Error en es_direccion_ip: ",error)
        return 1
def tiene_sufijo_valido(url):
    try:
        parsed_url = urlparse(url).netloc
        sufijos = [".com", ".net", ".org"]
        tiene_sufijo = any(parsed_url.endswith(sufijo) for sufijo in sufijos)
        if tiene_sufijo:
            return 0
        else:
            return 1
    except Exception as error:
        print("Error en tiene_sufijo_valido: ",error)
        return 1
def tiene_redireccion(url):
    try:
        response = requests.get(url,timeout=5)
        if len(response.history) > 3:
            return 1
        else:
            return 0
    except Exception as error:
        print("Error en tiene_redireccion: ", error)
        return 1
def tiene_arroba_en_url(url):
    try:
        if "@" in url:
            return 1
        else:
            return 0
    except Exception as error:
        print("Error en tiene_arroba_en_url: ", error)
        return 1
def tiene_formulario_blank(url):
    try:
        response = requests.get(url,timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        formularios_blank = soup.find_all('form', target='_blank')
        if len(formularios_blank) > 0:
            return 1
        else:
            return 0
    except Exception as error:
        print("Error en tiene_formulario_blank: ",error)
        return 1
def es_favicon_externo(url):
    try:
        response = requests.get(url,timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        link_favicon = soup.find('link', rel='icon')
        if link_favicon:
            favicon_url = link_favicon.get('href')
            if favicon_url and (favicon_url.startswith('http://') or favicon_url.startswith('https://')):
                return 1
            else:
                return 0
        return 0
    except Exception as error:
        print("Error en es_favicon_externo: ",error)
        return 1
def tiene_metadatos(url):
    try:
        response = requests.get(url,timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_tags = soup.find_all('meta')
        if len(meta_tags) > 0:
            return 0
        else:
            return 1
    except Exception as error:
        print("Error en tiene_metadatos: ",error)
        return 1

