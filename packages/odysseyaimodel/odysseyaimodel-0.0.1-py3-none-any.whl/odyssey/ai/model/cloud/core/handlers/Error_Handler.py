'''Módulo global exception handlers'''
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from odyssey.ai.model.cloud.core.models.CodigosRespuesta import CodigosRespuesta
from odyssey.ai.model.cloud.core.utilerias.Constantes import CODIGO404, CODIGO500, CODIGO405

'''
Proyecto: pythonTemplate
Clase: Error_Handler
Mantenedor: EYMG
Fecha: 2023-04-27
OT: NA
Ultimo cambio: Definición de documentación para sonarqube
'''


def add_global_exception_handler(app: FastAPI):
    '''
    add_global_exception_handler
    '''

    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc: HTTPException):
        '''
        Proyecto: pythonTemplate
        Clase: math
        Metodo: not_found_exception_handler
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
        '''
        respuesta = CodigosRespuesta(CODIGO404)
        detalles = {
            "error": HTTPStatus.NOT_FOUND.description
        }
        respuesta.set_detalles(detalles)
        return JSONResponse(status_code=respuesta.get_http_status(), content=respuesta.to_json())

    @app.exception_handler(405)
    async def method_not_allowed_exception_handler(request: Request, exc: HTTPException):
        '''
        Proyecto: pythonTemplate
        Clase: math
        Metodo: not_found_exception_handler
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
        '''
        respuesta = CodigosRespuesta(CODIGO405)
        detalles = {
            "error": HTTPStatus.METHOD_NOT_ALLOWED.description
        }
        respuesta.set_detalles(detalles)
        return JSONResponse(status_code=respuesta.get_http_status(), content=respuesta.to_json())

    @app.exception_handler(500)
    async def internal_service_exception_handler(request: Request, exc: HTTPException):
        '''
        Proyecto: pythonTemplate
        Clase: math
        Metodo: internal_service_exception_handler
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
        '''
        respuesta = CodigosRespuesta(CODIGO500)
        detalles = {
            "error": HTTPStatus.INTERNAL_SERVER_ERROR.description
        }
        respuesta.set_detalles(detalles)
        return JSONResponse(status_code=respuesta.get_http_status(), content=respuesta.to_json())
