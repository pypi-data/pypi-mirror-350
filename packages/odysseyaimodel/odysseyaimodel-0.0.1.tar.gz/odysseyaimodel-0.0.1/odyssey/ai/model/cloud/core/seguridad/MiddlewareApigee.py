'''Módulo Middlware'''
from __future__ import annotations

import base64
import datetime
import io
import os
from http import HTTPStatus

import jwt
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from odyssey.ai.model.cloud.configuracion.Configuracion import public_key_apigee
from odyssey.ai.model.cloud.core.models.CodigosRespuesta import CodigosRespuesta
from odyssey.ai.model.cloud.core.utilerias.Constantes import CODIGO401, SIN_EXPIRACION, USUARIO_INVALIDO, \
    MSG_TOKEN_NULL, HEADER_TOKEN, PATH, PRIVATE_DER

def desencriptar_texto_rsa(text: str):
    """
    desencriptarTextoRSA método para desencriptar sub de claims de tokens de apigee
    :param texto: str
    :return: texto en utf8
    """
    string_archivo = PRIVATE_DER
    string_archivo = string_archivo.replace("-----BEGIN PRIVATE KEY-----", "")
    string_archivo = string_archivo.replace("-----END PRIVATE KEY-----", "")
    decode = base64.b64decode(string_archivo)
    key_spec = RSA.import_key(decode)
    cipher = PKCS1_v1_5.new(key_spec)
    decrypted_text = cipher.decrypt(base64.b64decode(text), None)
    return decrypted_text.decode('utf-8')

def validate_token(token: str, public_key_pem: str):
    '''
        Proyecto: pythonTemplate
        Clase: add_secure_middleware_apigee
        Mantenedor: EYMG
        Fecha: 2023-06-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
    '''
    formato = "%d/%m/%Y %I:%M:%S %p"
    if token is not None and token != "":
        claims = jwt.decode(token, '-----BEGIN PUBLIC KEY-----\n' + public_key_pem + ' \n-----END PUBLIC KEY-----',
                            algorithms=['RS256'])
        if claims.get('sub') is not None and desencriptar_texto_rsa(claims.get('sub')) == "apigee":
            tiempo_expiracionjwt = datetime.datetime.fromtimestamp(claims.get('exp'))
            fecha = tiempo_expiracionjwt.strftime(
                formato) if tiempo_expiracionjwt is not None else SIN_EXPIRACION
            if fecha == SIN_EXPIRACION:
                raise TypeError(SIN_EXPIRACION)
        else:
            raise TypeError(USUARIO_INVALIDO)
    else:
        raise TypeError(MSG_TOKEN_NULL)

def add_secure_middleware_apigee(app: FastAPI):
    '''
        Proyecto: pythonTemplate
        Clase: add_secure_middleware_apigee
        Mantenedor: EYMG
        Fecha: 2023-06-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
    '''
    def __valida_jwt(token: str, public_key_pem: str):
        """
        __valida_jwt método para validar el token de apigee
        :param token: str
        :param public_key_pem: str
        """
        validate_token(token, public_key_pem)

    @app.middleware("http")
    async def secure_headers_apigee(request: Request, call_next):
        """
        secure_headers_apigee middleware de seguridad para validar token
        :param request: request
        :param call_next: next
        :return: response
        """
        token = request.headers.get(HEADER_TOKEN)
        if PATH in str(request.url) and (token is None or token == ""):
            respuesta = CodigosRespuesta(CODIGO401)
            detalles = {
                "error": HTTPStatus.UNAUTHORIZED.description,
                "descripcion": MSG_TOKEN_NULL
            }
            respuesta.set_detalles(detalles)
            return JSONResponse(status_code=respuesta.get_http_status(), content=respuesta.to_json())
        elif PATH in str(request.url):
            try:
                __valida_jwt(token, public_key_apigee)
            except (ValueError, TypeError, IndexError, KeyError) as e:
                respuesta = CodigosRespuesta(CODIGO401)

                detalles = {
                    "error": HTTPStatus.UNAUTHORIZED.description,
                    "descripcion": str(e)
                }
                respuesta.set_detalles(detalles)
                return JSONResponse(status_code=respuesta.get_http_status(), content=respuesta.to_json())

        response = await call_next(request)
        return response
