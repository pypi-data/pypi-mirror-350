'''Módulo de Crypto, contiene funciones matematicas'''
import random
from odyssey.ai.model.cloud.core.utilerias.Constantes import N0, N10


'''
        Proyecto: pythonTemplate
        Clase: math
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
    '''


def genera_numero_random(length):
    '''
        Proyecto: pythonTemplate
        Clase: math
        Metodo: genera_numero_random
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
    '''
    system_random = random.SystemRandom()
    return int(''.join([str(system_random.randint(N0, N10)) for _ in range(length)]))
