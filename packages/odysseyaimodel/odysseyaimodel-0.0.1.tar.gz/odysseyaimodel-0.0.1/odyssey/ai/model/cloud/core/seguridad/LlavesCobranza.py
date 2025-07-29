'''Módulo de LlavesCobranza, contiene la lógica de negocio para generar o recuperar llaves de cobranza'''
import json

import requests

from odyssey.ai.model.cloud.core.seguridad.Apigee import Apigee
from odyssey.ai.model.cloud.core.utilerias.Constantes import MOCK, BEARER, DATO, \
    URL_API_LLAVESSEGURIDAD, N200, \
    CODIGO, N1, RESULTADO, N0

'''
Proyecto: pythonTemplate
Clase: Crypto
Mantenedor: EYMG
Fecha: 2023-04-27
OT: NA
Ultimo cambio: Definición de documentación para sonarqube 
'''


class LlavesCobranza(object):
    '''Clase que contiene los elementos para gestionar la seguridad de cobranza para cifrados
    Mantenedor: EYMG
    Fecha: 2023-04-27
    OT: NA
    Ultimo cambio: Definición de documentación para sonarqube'''

    def __init__(self, apigee=Apigee()):
        self.__token = apigee.genera_access_token()
        self.__mock = MOCK
        self.__genera_llaves()
        self.__obten_llaves()

    def __genera_llaves(self):
        '''Método de acceso privado para generar llaves de seguridad
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''
        headers = {"Authorization": BEARER + str(self.__token[DATO]["accessToken"]), "x-ismock": str(self.__mock)}
        data = requests.get(URL_API_LLAVESSEGURIDAD, headers=headers, verify=False)

        response = {
            "codigo": N0,
            "dato": {}
        }

        if data.status_code == N200:
            response[CODIGO] = N1
            response[DATO] = json.loads(json.dumps(data.json()))
            self.__llaves_cliente = json.loads(json.dumps(data.json()))[RESULTADO]
        else:
            response[DATO] = json.loads(json.dumps(data.json()))

        return response

    def __obten_llaves(self):
        '''Método de acceso privado para recuperar llaves de seguridad
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''
        headers = {"Authorization": BEARER + str(self.__token[DATO]["accessToken"]), "x-ismock": str(self.__mock)}
        data = requests.get(URL_API_LLAVESSEGURIDAD + "/" +
                            self.__llaves_cliente["idAcceso"], headers=headers, verify=False)

        response = {
            "codigo": N0,
            "dato": {}
        }

        if data.status_code == N200:
            response[CODIGO] = N1
            response[DATO] = json.loads(json.dumps(data.json()))
            self.__llaves_servidor = json.loads(json.dumps(data.json()))[RESULTADO]
        else:
            response[DATO] = json.loads(json.dumps(data.json()))

        return response

    def get_llaves_cliente(self):
        '''Método de acceso público para recuperar las llaves de cliente
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''
        return self.__llaves_cliente

    def get_llaves_servidor(self):
        '''Método de acceso público para recuperar las llaves de servidor
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''
        return self.__llaves_servidor
