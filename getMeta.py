import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from obtenerMetadata import *
import numpy as np

mensaje = {}
def hacer_solicitud(url, timeout=15):
    parsed_url = urlparse(url)
    if not ([parsed_url.scheme, parsed_url.netloc]):
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
        mensaje['mensaje']='Error en la solicitud', e
        print(e)
        return mensaje

def analizar_data(link):
    more_details = {}
    url = link.strip()
    url_parsed = urlparse(url)
    try:
        response = hacer_solicitud(url, timeout=5)
        if response['id'] == 200:
            nombres_caracteristicas = ['web_indexada','ssl_vigencia','coincide_cn_con_url','obtener_edad_dominio','https_en_url','es_direccion_ip','tiene_sufijo_valido','tiene_redireccion','tiene_arroba_en_url','tiene_formulario_blank','es_favicon_externo','tiene_metadatos']
            resultados = []
            resultados.append(web_indexada(url))
            resultados.append(ssl_vigencia(url))
            resultados.append(coincide_cn_con_url(url))
            resultados.append(obtener_edad_dominio(url))
            resultados.append(https_en_url(url))
            resultados.append(es_direccion_ip(url))
            resultados.append(tiene_sufijo_valido(url))
            resultados.append(tiene_redireccion(url))
            resultados.append(tiene_arroba_en_url(url))
            resultados.append(tiene_formulario_blank(url))
            resultados.append(es_favicon_externo(url))
            resultados.append(tiene_metadatos(url))
            resultados = np.array(resultados).reshape(1, -1)
            return resultados
        else:
            return response

    except requests.exceptions.RequestException as e:
        mensaje['id'] = 508
        mensaje['mensaje'] = 'Exception en la solicitud: ',e
        return mensaje

#analizar_data(input("analizar: "))


