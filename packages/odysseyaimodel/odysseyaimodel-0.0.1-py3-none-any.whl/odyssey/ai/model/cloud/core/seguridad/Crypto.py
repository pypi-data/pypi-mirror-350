'''Módulo de Crypto, contiene la lógica de negocio para todo el mecanismo de cifrado y descifrado de cadenas'''

import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from odyssey.ai.model.cloud.core.utilerias.Constantes import (
    ENCODING_UTF8, BEGIN_PUBLIC_KEY, END_PUBLIC_KEY, BEGIN_PRIVATE_KEY, END_PRIVATE_KEY)

'''
Proyecto: pythonTemplate
Clase: Crypto
Mantenedor: EYMG
Fecha: 2023-04-27
OT: NA
Ultimo cambio: Definición de documentación para sonarqube 
'''


class Crypto(object):
    '''Clase Crypto encargada de la funcionaliad de cifrado
    Mantenedor: EYMG
    Fecha: 2023-04-27
    OT: NA
    Ultimo cambio: Definición de documentación para sonarqube'''

    __llaves_cliente: {}
    __llaves_servidor: {}

    def __init__(self, llaves_cobranza):
        self.__llaves_cliente = llaves_cobranza.get_llaves_cliente()
        self.__llaves_servidor = llaves_cobranza.get_llaves_servidor()
        self.__public_cert_cliente = RSA.importKey(
            BEGIN_PUBLIC_KEY + self.__llaves_cliente["accesoPublico"] + END_PUBLIC_KEY)
        self.__private_cert_cliente = RSA.importKey(
            BEGIN_PRIVATE_KEY + self.__llaves_cliente["accesoPrivado"] + END_PRIVATE_KEY)
        self.__public_cert_servidor = RSA.importKey(
            BEGIN_PUBLIC_KEY + self.__llaves_servidor["accesoPublico"] + END_PUBLIC_KEY)
        self.__private_cert_servidor = RSA.importKey(
            BEGIN_PRIVATE_KEY + self.__llaves_servidor["accesoPrivado"] + END_PRIVATE_KEY)

    # Cifrado OAEP
    @classmethod
    def encrypt_oaep(cls, plaintext, public_key):
        '''Método para encriptar oaep
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
        '''

        cipher = PKCS1_OAEP.new(public_key)
        ciphertext = cipher.encrypt(bytes(plaintext, encoding=ENCODING_UTF8))
        return base64.b64encode(ciphertext)

    @classmethod
    def decrypt_oaep(cls, base64_encoded_ciphertext, private_key):
        '''Método para desencriptar oaep
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''

        ciphertext = base64.b64decode(base64_encoded_ciphertext)
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(ciphertext)

    # Cifrado RSA
    @classmethod
    def encrypt_rsa(cls, plaintext, public_key):
        '''Médoto para encriptar rsa
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''

        cipher = PKCS1_v1_5.new(public_key)
        ciphertext = base64.b64encode((cipher.encrypt(bytes(plaintext, ENCODING_UTF8))))
        return ciphertext

    @classmethod
    def decrypt_rsa(cls, base64_encoded_ciphertext, private_key):
        '''Método para desencriptar rsa
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''
        cipher = PKCS1_v1_5.new(private_key)
        plaintext = cipher.decrypt(base64.b64decode(base64_encoded_ciphertext), "Error mientras se desencripta")
        return plaintext

    def get_public_cert_cliente(self):
        '''Método de acceso público para el certificado público del cliente
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''
        return self.__public_cert_cliente

    def get_private_cert_cliente(self):
        '''Método de acceso público para el certificado privado del cliente
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''

        return self.__private_cert_cliente

    def get_public_cert_servidor(self):
        '''Método de acceso público para el certificado público del servidor
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''

        return self.__public_cert_servidor

    def get_private_cert_servidor(self):
        '''Método de acceso público para el certificado privado del servidor
        Mantenedor: EYMG
        Fecha: 2023-04-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube'''

        return self.__private_cert_servidor
