'''Módulo de TipoInputOutput'''
from enum import Enum

'''
    Proyecto: pythonTemplate
    Clase: Level
    Mantenedor: MTIB
    Fecha: 2023-07-10
    OT: NA
    Ultimo cambio:
'''


class Level(Enum):
    '''
    TipoInputOutput
    Proyecto: pythonTemplate
    Clase: Level
    Mantenedor: MTIB
    Fecha: 2023-07-10
    OT: NA
    Ultimo cambio:
    '''

    '''INFO'''
    INFO = 1

    '''WARN'''
    WARN = 2

    '''ERROR'''
    ERROR = 3

    '''DEBUG'''
    DEBUG = 4

    '''CRITICAL'''
    CRITICAL = 5

    '''FATAL'''
    FATAL = 6

    '''NOTSET'''
    NOTSET = 7
