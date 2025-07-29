'''Módulo Web'''

from fastapi import Request
import random

class Web(object):
    '''
    Web
    '''

    def __init__(self):
        '''
        __init__
        '''

    @staticmethod
    def get_x_forwarded(request: Request):
        '''
        get_x_forwarded
        '''
        if request.headers.__len__() > 0:
            ip = request.headers.get('x-original-forwarded-for')
            if ip != None:
                return ip

        return 'no-provided'

    @staticmethod
    def shuffle_data(data):
        random.shuffle(data)
        return data
