'''Módulo de DB, contiene enumerados con los tipos de base de datos'''
from enum import Enum


class DB(Enum):
    '''
        Proyecto: pythonTemplate
        Clase: DB
        Mantenedor: MTIB
        Fecha: 2023-07-10
        OT: NA
        Ultimo cambio:
    '''
    DB_ORACLE = 1
    DB_MSQL = 2
    DB_MONGO = 3
    DB_POSTGRESQL = 4
