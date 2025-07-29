'''Módulo de Daos,'''
from odyssey.ai.model.cloud.configuracion.Configuracion import Configuracion
from odyssey.ai.model.cloud.core.models.DB import DB
from odyssey.ai.model.cloud.core.models.TipoConsulta import TipoConsulta

Configuracion()


class Daos(object):
    '''
          Proyecto: pythonTemplate
          Clase: Daos
          Mantenedor: MTIB
          Fecha: 2023-07-10
          OT: NA
          Ultimo cambio:
      '''
    __db: DB = DB.DB_ORACLE
    __tipo_consulta: TipoConsulta = TipoConsulta.DB_QUERY
    __consulta = ""
    __funcion = ""
    __parametros = []

    def __init__(self, db, tipo_consulta, consulta, funcion, parametros):
        '''
            Proyecto: pythonTemplate
            Clase: Daos
            Metodo: __init__
            Mantenedor: MTIB
            Fecha: 2023-07-10
            OT: NA
            Ultimo cambio:
        '''
        self.__db = db
        self.__tipo_consulta = tipo_consulta
        self.__consulta = consulta
        self.__funcion = funcion
        self.__parametros = parametros

    def set_db(self, db):
        '''
            Proyecto: pythonTemplate
            Clase: Daos
            Metodo: set_db
            Mantenedor: MTIB
            Fecha: 2023-07-10
            OT: NA
            Ultimo cambio:
        '''
        self.__db = db

    def get_db(self):
        return self.__db

    def set_tipo_consulta(self, tipo_consulta):
        '''
            Proyecto: pythonTemplate
            Clase: Daos
            Metodo: set_tipo_consulta
            Mantenedor: MTIB
            Fecha: 2023-07-10
            OT: NA
            Ultimo cambio:
        '''
        self.__tipo_consulta = tipo_consulta

    def get_tipo_consulta(self):
        return self.__tipo_consulta

    def set_consulta(self, consulta):
        '''
            Proyecto: pythonTemplate
            Clase: Daos
            Metodo: set_consulta
            Mantenedor: MTIB
            Fecha: 2023-07-10
            OT: NA
            Ultimo cambio:
        '''
        self.__consulta = consulta

    def get_consulta(self):
        return self.__consulta

    def set_funcion(self, funcion):
        '''
            Proyecto: pythonTemplate
            Clase: Daos
            Metodo: set_funcion
            Mantenedor: MTIB
            Fecha: 2023-07-10
            OT: NA
            Ultimo cambio:
        '''
        self.__funcion = funcion

    def get_funcion(self):
        return self.__funcion

    def set_parametros(self, parametros):
        '''
            Proyecto: pythonTemplate
            Clase: Daos
            Metodo: set_parametros
            Mantenedor: MTIB
            Fecha: 2023-07-10
            OT: NA
            Ultimo cambio:
        '''
        self.__parametros = parametros

    def get_parametros(self):
        return self.__parametros
