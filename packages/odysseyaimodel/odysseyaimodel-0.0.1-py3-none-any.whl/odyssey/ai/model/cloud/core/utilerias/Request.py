'''Módulo requests, continene los metodos para realizar peticiones http mas comunes'''
import requests


class Request(object):
    '''
        Proyecto: pythonTemplate
        Clase: Request
        Mantenedor:
        Fecha:
        OT: NA
        Ultimo cambio:
    '''
    @staticmethod
    def post(url, headers, data=None, json=None, **kwargs):
        return requests.post(url, headers=headers, data=data, verify=False, json=json, **kwargs)

    @staticmethod
    def get(url, headers, data=None, json=None, **kwargs):
        return requests.get(url, headers=headers, data=data, verify=False, json=json, **kwargs)
