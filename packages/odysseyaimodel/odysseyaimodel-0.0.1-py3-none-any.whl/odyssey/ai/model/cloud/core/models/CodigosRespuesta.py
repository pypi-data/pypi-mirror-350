'''Módulo de CodigosRespuesta, contiene la lógica de negocio para todo el mecanismo de respuesta de los controllers'''
import pytz

from odyssey.ai.model.cloud.configuracion.Configuracion import tz
from odyssey.ai.model.cloud.core.utilerias.Cadenas import Cadenas
from odyssey.ai.model.cloud.core.utilerias.Constantes import (
    CODIGO200, CODIGO201, CODIGO400, CODIGO401, CODIGO403, CODIGO404, CODIGO405, CODIGO422, CODIGO500)
from http import HTTPStatus
import json
from datetime import datetime

'''
    Proyecto: pythonTemplate
    Clase: CodigosRespuesta
    Mantenedor: EYMG
    Fecha: 2023-04-27
    OT: NA
    Ultimo cambio: Definición de documentación para sonarqube 
'''
class CodigosRespuesta(object):
    '''
        Proyecto: pythonTemplate
        Clase: CodigosRespuesta
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
    '''
    serial_version_uid = 8051605784825034187;

    __codigo=""
    __mensaje=""
    __folio=""
    __info=""
    __detalles=None
    __http_status= HTTPStatus.OK
    __resultado=None

    def __init__(self, codigo):
        '''
            Proyecto: pythonTemplate
            Clase: CodigosRespuesta
            Metodo: __init__
            Mantenedor: EYMG
            Fecha: 2023-04-27
            OT: NA
            Ultimo cambio: Definición de documentación para sonarqube
        '''
        self.__folio= CodigosRespuesta.folio()
        if codigo == CODIGO200:
            self.__codigo = None
            self.__info = None
            self.__mensaje = Cadenas.MSJ_CODIGO_200_DESCRIPCION_OPEN
            self.__http_status =HTTPStatus.OK
            self.__detalles = None
        elif codigo == CODIGO201:
            self.__codigo = None
            self.__info = None
            self.__mensaje = Cadenas.MSJ_CODIGO_201_DESCRIPCION_OPEN
            self.__http_status = HTTPStatus.CREATED
            self.__detalles = None
        elif codigo == CODIGO400:
            self.__codigo = Cadenas.msj_codigo_400()
            self.__info = Cadenas.msj_codigo_400_info()
            self.__mensaje = Cadenas.MSJ_CODIGO_400_DESCRIPCION_OPEN
            self.__http_status = HTTPStatus.BAD_REQUEST
            self.__detalles = []
        elif codigo == CODIGO401:
            self.__codigo = Cadenas.msj_codigo_401()
            self.__info = Cadenas.msj_codigo_401_info()
            self.__mensaje = Cadenas.MSJ_CODIGO_401_DESCRIPCION_OPEN
            self.__http_status = HTTPStatus.UNAUTHORIZED
            self.__detalles = []
        elif codigo == CODIGO403:
            self.__codigo = Cadenas.msj_codigo_403()
            self.__info = Cadenas.msj_codigo_403_info()
            self.__mensaje = Cadenas.MSJ_CODIGO_403_DESCRIPCION_OPEN
            self.__http_status = HTTPStatus.FORBIDDEN
            self.__detalles = []
        elif codigo == CODIGO404:
            self.__codigo = Cadenas.msj_codigo_404()
            self.__info = Cadenas.msj_codigo_404_info()
            self.__mensaje = Cadenas.MSJ_CODIGO_404_DESCRIPCION_OPEN
            self.__http_status = HTTPStatus.NOT_FOUND
            self.__detalles = []
        elif codigo == CODIGO405:
            self.__codigo = Cadenas.msj_codigo_405()
            self.__info = Cadenas.msj_codigo_405_info()
            self.__mensaje = Cadenas.MSJ_CODIGO_405_DESCRIPCION_OPEN
            self.__http_status = HTTPStatus.METHOD_NOT_ALLOWED
            self.__detalles = []
        elif codigo == CODIGO422:
            self.__codigo = Cadenas.msj_codigo_422()
            self.__info = Cadenas.msj_codigo_422_info()
            self.__mensaje = Cadenas.MSJ_CODIGO_422_DESCRIPCION_OPEN
            self.__http_status = HTTPStatus.UNPROCESSABLE_ENTITY
            self.__detalles = []
        elif codigo == CODIGO500:
            self.__codigo = Cadenas.msj_codigo_500()
            self.__info = Cadenas.msj_codigo_500_info()
            self.__mensaje = Cadenas.MSJ_CODIGO_500_DESCRIPCION_OPEN
            self.__http_status = HTTPStatus.INTERNAL_SERVER_ERROR
            self.__detalles = []

    @staticmethod
    def folio():
        '''
            Proyecto: pythonTemplate
            Clase: CodigosRespuesta
            Metodo: __init__
            Mantenedor: EYMG
            Fecha: 2023-04-27
            OT: NA
            Ultimo cambio: Definición de documentación para sonarqube
        '''
        pattern = "%Y%m%d%H%M%S%f"
        today = datetime.now(pytz.timezone(tz))
        timestamp = datetime.now(pytz.timezone(tz)).timestamp()
        formatter = today.strftime(pattern)
        return formatter + str(int(timestamp * 1000))

    def clean_nones(self, value):
        '''
                    Proyecto: pythonTemplate
                    Clase: CodigosRespuesta
                    Metodo: clean_nones
                    Mantenedor: EYMG
                    Fecha: 2023-04-27
                    OT: NA
                    Ultimo cambio: Recursively remove all None values from dictionaries and lists, and returns
                    the result as a new dictionary or list.
        '''
        if isinstance(value, list):
            return [self.clean_nones(x) for x in value if x is not None]
        elif isinstance(value, dict):
            return {
                key: self.clean_nones(val)
                for key, val in value.items()
                if val is not None
            }
        else:
            return value

    def get_http_status(self):
        return self.__http_status

    def get_codigo(self):
        return self.__codigo
    def set_detalles(self, detalles):
        '''
            Proyecto: pythonTemplate
            Clase: CodigosRespuesta
            Metodo: set_detalles
            Mantenedor: EYMG
            Fecha: 2023-04-27
            OT: NA
            Ultimo cambio: Definición de documentación para sonarqube
        '''
        self.__detalles = detalles

    def set_mensaje(self, mensaje):
        '''
            Proyecto: pythonTemplate
            Clase: CodigosRespuesta
            Metodo: set_mensaje
            Mantenedor: EYMG
            Fecha: 2023-04-27
            OT: NA
            Ultimo cambio: Definición de documentación para sonarqube
        '''
        self.__mensaje = mensaje

    def set_resultado(self, resultado):
        '''
            Proyecto: pythonTemplate
            Clase: CodigosRespuesta
            Metodo: set_resultado
            Mantenedor: EYMG
            Fecha: 2023-04-27
            OT: NA
            Ultimo cambio: Definición de documentación para sonarqube
        '''
        self.__resultado = resultado

    def to_json(self):
        '''
            Proyecto: pythonTemplate
            Clase: CodigosRespuesta
            Metodo: to_json
            Mantenedor: EYMG
            Fecha: 2023-04-27
            OT: NA
            Ultimo cambio: Definición de documentación para sonarqube
        '''
        response = {
            "folio": self.__folio,
            "codigo": self.__codigo,
            "info": self.__info,
            "mensaje": self.__mensaje,
            "httpStatus": None,
            "detalles": self.__detalles,
            "resultado": self.__resultado
        }
        response = self.clean_nones(response.copy())
        return json.loads(json.dumps(response, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, ensure_ascii=False, allow_nan=False))
