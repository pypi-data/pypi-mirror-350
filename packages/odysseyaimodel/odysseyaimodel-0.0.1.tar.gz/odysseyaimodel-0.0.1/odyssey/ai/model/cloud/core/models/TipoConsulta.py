'''Módulo de TipoConsulta,'''
from enum import Enum


class TipoConsulta(Enum):
    '''
        Proyecto: pythonTemplate
        Clase: TipoConsulta
        Mantenedor: MTIB
        Fecha: 2023-07-10
        OT: NA
        Ultimo cambio:
    '''
    DB_QUERY = 1
    DB_FUNCION = 2
    DB_CONSULTA = 3
