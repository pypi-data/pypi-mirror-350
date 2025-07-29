'''Módulo de APIGEE, contiene la lógica de negocio para identificarse en la plataforma de apigee'''
import json

import requests

from odyssey.ai.model.cloud.core.utilerias.Constantes import (
    CONTENT_TYPE_WWWURLENCODED, CREDENCIALES, GRANT_TYPE, URL_APIGEE_OAUTH2, N0, N1, N200, CODIGO, DATO)

'''
Proyecto: pythonTemplate
Clase: Crypto
Mantenedor: EYMG
Fecha: 2023-04-27
OT: NA
Ultimo cambio: Definición de documentación para sonarqube 
'''


class Apigee(object):
    '''Clase que contiene los elementos para gestionar APIGEE
    Mantenedor: EYMG
    Fecha: 2023-04-27
    OT: NA
    Ultimo cambio: Definición de documentación para sonarqube'''

    def __init__(self):
        self.__access_token = ""

    def genera_access_token(self):
        '''Médoto para generar el access token de consumo de apigee
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''

        '''Se establecen headers para request'''
        headers = {"Content-Type": CONTENT_TYPE_WWWURLENCODED, "Authorization": CREDENCIALES}

        '''Se establecen valores del request'''
        form_data = {"grant_type": GRANT_TYPE}

        '''Se ejecuta consulta httprequest'''
        data = requests.post(URL_APIGEE_OAUTH2, data=form_data, headers=headers, verify=False)

        response = {
            "codigo": N0,
            "dato": {}
        }

        '''Se obtiene respuesta y se validan resultados'''
        if data.status_code == N200:
            response[CODIGO] = N1
            response[DATO] = {"accessToken": json.loads(json.dumps(data.json()))["access_token"]}
        else:
            response[DATO] = json.loads(json.dumps(data.json()))

        self.__access_token = json.loads(json.dumps(data.json()))["access_token"]

        '''Se entrega respuesta'''
        return response

    def obten_access_token(self):
        '''Método de acceso público para obtener el access token de apigee
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''
        return self.__access_token
