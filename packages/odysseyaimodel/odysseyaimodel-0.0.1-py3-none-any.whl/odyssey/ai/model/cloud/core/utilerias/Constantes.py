'''
	Módulo de constantes del proyecto
	Mantenedor: EYMG
	Fecha: 2023-04-27
	OT: NAA
	Ultimo cambio: Definición de documentación para sonarqube
	Variables:
		URL_REGEX
		MOCK
		HTTPS
		TOKENAPIGEE
		TOKENLOCAL
		CONTENT_TYPE
		CERO
		DIEZ
		OCHO
		CINCO
		SIETE
		CUATRO
		DOCIENTOS
		TRESCIENTOSMILLIS
		FQDN_APIGEE = "https://sandbox.bancoazteca.com"
		URL_API_LLAVESSEGURIDAD
		URL_API_ABONOS_CLIENTES
		URL_API_ABONOS_CREDIMAX
		URL_API_CONTACT_CENTER_CLIENTES
		URL_APIGEE_OAUTH2
		RESULTADO
		DATO
		CODIGO
		ENCODING_UTF8 = "utf-8"
		CONTENT_TYPE_WWWURLENCODED
		CONTENT_TYPE_JSON
		CREDENCIALES
		GRANT_TYPE
		BEARER
		BEGIN_PUBLIC_KEY
		END_PUBLIC_KEY
		BEGIN_PRIVATE_KEY
		END_PRIVATE_KEY
		N0
		N1
		N2
		N6
		N10
		N200
		CODIGO200
		CODIGO201
		CODIGO400
		CODIGO401
		CODIGO403
		CODIGO404
		CODIGO405
		CODIGO422
		CODIGO500
		CODIGO501'
		QUALITY_GATE_URL_TEST
		VALIDA_TOKEN_GOBIERNO_APIS
		SISTEMA
		ENCODING
		CONN_TIMEOUT
		READ_TIMEOUT
		PARAMETROS_DEFAULT
		PARAMETROS_CLIENTE_360_TOKEN
		BEARER_CLIENTE_360_STR
		PETICION_STR
		EXCEPTION_STR
		RESPUESTA_NO_RECUPERADA
		PUESTOS_VALIDOS
		ORIGEN_DESCARGA_BAZ_STORE
		FORMATO_FECHAS
		FORMATO_FECHAS_2
		CARPETA_CLIENTE_360
		FORMATO_FECHAS_HORAS
		FORMATO_FECHAS_HORAS_TIME_STAMP
		FORMATO_FECHAS_HORAS_2
		FORMATO_FECHAS_HORAS_2_TIME_STAMP
		US_EXT_GOOGLE
		KEY_EXT_GOOGLE
		US_INT_GOOGLE
		KEY_INT_GOOGLE
		API_KEY_GOOGLE
		URL_DIRECTIONS
		URL_DIRECTIONSV_2
		URL_GOOGLEMARCAAGUA
		URL_GOOGLE
		URL_GEOCODE
		URL_OPENSTREET
		HTTP =
		URL_BAZMAPAS
		URL_MT_1_GOOGLE
		URL_MT_0_GOOGLE
		URL_BANCOAZTECA
		URL_INFOEMPLEADO
		URL_INFODISPOSITIVOS
		SEGURIDAD_PETICION_INCORRECTA
		SEGURIDAD_REGIONAL_NO_COINCIDE
		SEGURIDAD_GERENCIA_NO_COINCIDE
		SEGURIDAD_PUESTO_NO_COINCIDE
		SEGURIDAD_PUESTO_NOASIGNADO
		SEGURIDAD_DISPOSITIVO_NO_ASIGNADO
		SEGURIDAD_ERROR_GENERAR_TOKEN
		SEGURIDAD_PETICION_NO_EXISTE
		SEGURIDAD_BEARER_NO_EXISTE
		SEGURIDAD_EMPLEADO_INCORRECTO
		SEGURIDAD_TOKEN_EXPIRADO
		SEGURIDAD_ERROR_TOKEN_JWT
		SEGURIDAD_ERRORDK
		SEGURIDAD_ERRORNNULL
		SEGURIDAD_ERROR_ENTRENAMIENTOS
		SEGURIDAD_ERRORDKRESPUESTA
		SEGURIDAD_ERRORNNULLRESPUESTA
		TOKENAPIDEV
		TOKENAPIPRODEXT
		TOKENAPIPRODINT
		TOKENAPIQA
		TOKENAPIAWSINT
		CREDAPILLAVESPROD
		CREDAPILLAVESDEV
		CREDAPILLAVESQA
		LLAVESPRODEXT
		LLAVESPRODINT
		LLAVESDEV
		FOTODEFAULT
'''
from odyssey.ai.model.cloud.configuracion.Configuracion import oauth2_apigee, fqdn_apigee

'''URL REGEX'''
URL_REGEX = ("^((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))" +
             "(%[0-9A-Fa-f]{2}|[-()_.!~*';/?:@&=+$,A-Za-z0-9])+)([).!';/?:,][[:blank:]])?$")

'''Constantes de ambiente'''
MOCK = "false"

'''HTTPS'''
HTTPS = "https"

'''TOKENAPIGEE'''
TOKENAPIGEE = ("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDfN9o3x8jq3awrDapaxzSNbAJWe3RXFmwZ0oVCTQQnvcA05h3XMUa" +
               "+FNeYlo7UpYOEJTBFf7tqM4WEIz2C9dNyOUl3cwNUkVb9y35thyvPAd1zD6FaO+lgL/mpQVF03/pSR8taSj3sdDVXVdlt" +
               "/6VMRagDqcNZiSc07p7UKVhO7wIDAQAB")

'''TOKENLOCAL'''
TOKENLOCAL = "esteesmitoken"

JSON = "JSON_"
CONTENT_TYPE = "Content-Type"
CERO = 0
DIEZ = 10
OCHO = 8
CINCO = 5
SIETE = 7
CUATRO = 4
DOCIENTOS = 200
TRESCIENTOSMILLIS = 300000

'''Constantes de URLS'''
URL_API_LLAVESSEGURIDAD = fqdn_apigee + "/cobranza-credito/investigacion-cobranza/seguridad/v1/aplicaciones/llaves"
URL_API_ABONOS_CLIENTES = fqdn_apigee + "/cobranza_credito/investigacion-cobranza/gestion-clientes/v1/clientes"
URL_API_ABONOS_CREDIMAX = fqdn_apigee + "/cobranza_credito/investigacion-cobranza/creditos/v3/credimax"
URL_API_CONTACT_CENTER_CLIENTES = fqdn_apigee + \
                                  "/cobranza_credito/investigacion-cobranza/call-center/gestion-clientes/v1"
URL_APIGEE_OAUTH2 = fqdn_apigee + "/oauth2/v1/token"

'''Constantes de valores para evitar CDP'''
RESULTADO = "resultado"
DATO = "dato"
CODIGO = "codigo"

'''Constantes de codificado'''
ENCODING_UTF8 = "utf-8"
CONTENT_TYPE_WWWURLENCODED = "application/x-www-form-urlencoded"
CONTENT_TYPE_JSON = "application/json"

'''Constantes de seguridad
No cambiar a menos que el ambiente sea otro
Para las llaves públicas y privadas respetar
el formato para que no se rompan los correspondientes
imports de crypto
'''
CREDENCIALES = oauth2_apigee
GRANT_TYPE = "client_credentials"
BEARER = "Bearer "
BEGIN_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n"
END_PUBLIC_KEY = "\n-----END PUBLIC KEY-----"
BEGIN_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\n"
END_PRIVATE_KEY = "\n-----END PRIVATE KEY-----"

'''Constantes numéricas'''
N0 = 0
N1 = 1
N2 = 2
N3 = 3
N4 = 4
N5 = 5
N6 = 6
N7 = 7
N8 = 8
N9 = 9
N10 = 10
N200 = 200

'''Codigo 200'''
CODIGO200 = 200

'''Codigo 201'''
CODIGO201 = 201

'''Codigo 400'''
CODIGO400 = 400

'''Codigo 401'''
CODIGO401 = 401

'''Codigo 403'''
CODIGO403 = 403

'''Codigo 404'''
CODIGO404 = 404

'''Codigo 405'''
CODIGO405 = 405

'''Codigo 422'''
CODIGO422 = 422

'''Codigo 500'''
CODIGO500 = 500

'''Codigo 501'''
CODIGO501 = 501

'''VALIDA_TOKEN_GOBIERNO_APIS'''
VALIDA_TOKEN_GOBIERNO_APIS = True

'''SISTEMA'''
SISTEMA = "Cloud & Devops"

'''ENCODING'''
ENCODING = "UTF-8"

'''CONN_TIMEOUT'''
CONN_TIMEOUT = 30000

'''READ_TIMEOUT'''
READ_TIMEOUT = 30000

'''PARAMETROS_DEFAULT'''
PARAMETROS_DEFAULT = "cadena,token"

'''PARAMETROS_CLIENTE_360_TOKEN'''
PARAMETROS_CLIENTE_360_TOKEN = "grant_type,client_id,client_secret"

'''BEARER_CLIENTE_360_STR
 * scope * no se espeficica'''
BEARER_CLIENTE_360_STR = "Bearer "

'''PETICION_STR'''
PETICION_STR = "peticion="

'''EXCEPTION_STR'''
EXCEPTION_STR = "exception"

'''RESPUESTA_NO_RECUPERADA'''
RESPUESTA_NO_RECUPERADA = "No se puede obtener una respuesta del servicio."

'''PUESTOS_VALIDOS'''
PUESTOS_VALIDOS = 202_004

'''ORIGEN_DESCARGA_BAZ_STORE'''
ORIGEN_DESCARGA_BAZ_STORE = 201_928

'''FORMATO_FECHAS'''
FORMATO_FECHAS = "yyyy-MM-dd"

'''FORMATO_FECHAS_2'''
FORMATO_FECHAS_2 = "dd/MM/yyyy"

'''CARPETA_CLIENTE_360'''
CARPETA_CLIENTE_360 = "Cliente360"

'''FORMATO_FECHAS_HORAS'''
FORMATO_FECHAS_HORAS = "yyyy-MM-dd HH:mm:ss"

'''FORMATO_FECHAS_HORAS_TIME_STAMP'''
FORMATO_FECHAS_HORAS_TIME_STAMP = "yyyy-MM-dd HH:mm:ss.SSS"

'''FORMATO_FECHAS_HORAS_2'''
FORMATO_FECHAS_HORAS_2 = "dd/MM/yyyy HH:mm:ss"

'''FORMATO_FECHAS_HORAS_2_TIME_STAMP'''
FORMATO_FECHAS_HORAS_2_TIME_STAMP = "dd/MM/yyyy HH:mm:ss.SSS"

'''US_EXT_GOOGLE'''
US_EXT_GOOGLE = "gme-bancoaztecasainstitucion1"

'''KEY_EXT_GOOGLE'''
KEY_EXT_GOOGLE = "VR9OhufHRyKq36_JlV3HAWvemco="

'''US_INT_GOOGLE'''
US_INT_GOOGLE = "gme-bancoaztecasainstitucion"

'''KEY_INT_GOOGLE'''
KEY_INT_GOOGLE = "i2-kXhiNYoIGe4Wl568bN2ejWGE="

'''API_KEY_GOOGLE'''
API_KEY_GOOGLE = "AIzaSyAndF_bbK1xXbymv0c34tNxhiExL4hrZwQ"

'''SEGURIDAD_PETICION_INCORRECTA'''
SEGURIDAD_PETICION_INCORRECTA = "No se puede generar un token de autorización ya que los parámetros son incorrectos."

'''SEGURIDAD_REGIONAL_NO_COINCIDE'''
SEGURIDAD_REGIONAL_NO_COINCIDE = "El número de región del empleado no coincide con la asignada."

'''SEGURIDAD_GERENCIA_NO_COINCIDE'''
SEGURIDAD_GERENCIA_NO_COINCIDE = "El número de gerencia del empleado no coincide con la asignada."

'''SEGURIDAD_PUESTO_NO_COINCIDE'''
SEGURIDAD_PUESTO_NO_COINCIDE = "El número de puesto del empleado no coincide con el asignado."

'''SEGURIDAD_PUESTO_NOASIGNADO'''
SEGURIDAD_PUESTO_NOASIGNADO = "El número de puesto del empleado no tiene permisos para usar el API."

'''SEGURIDAD_DISPOSITIVO_NO_ASIGNADO'''
SEGURIDAD_DISPOSITIVO_NO_ASIGNADO = "El dispositivo no se encuentra asignado para el empleado, no se permite su uso."

'''SEGURIDAD_ERROR_GENERAR_TOKEN'''
SEGURIDAD_ERROR_GENERAR_TOKEN = "Ocurrió un error al generar el token."

'''SEGURIDAD_PETICION_NO_EXISTE'''
SEGURIDAD_PETICION_NO_EXISTE = "No se proporciona correctamente la petición."

'''SEGURIDAD_BEARER_NO_EXISTE'''
SEGURIDAD_BEARER_NO_EXISTE = "La petición no proporciona el token de seguridad."

'''SEGURIDAD_EMPLEADO_INCORRECTO'''
SEGURIDAD_EMPLEADO_INCORRECTO = \
    "La petición se realiza con un número de empleado diferente al proporcionado en la autenticación."

'''SEGURIDAD_TOKEN_EXPIRADO'''
SEGURIDAD_TOKEN_EXPIRADO = "El token proporcionado ha expirado."

'''SEGURIDAD_ERROR_TOKEN_JWT'''
SEGURIDAD_ERROR_TOKEN_JWT = "No se puede leer el token proporcionado."

'''SEGURIDAD_ERRORDK'''
SEGURIDAD_ERRORDK = "duplicate key"

'''SEGURIDAD_ERRORNNULL'''
SEGURIDAD_ERRORNNULL = "column does not allow nulls"

'''SEGURIDAD_ERROR_ENTRENAMIENTOS'''
SEGURIDAD_ERROR_ENTRENAMIENTOS = "No puede existir más de un entrenamiento activo al mismo tiempo"

'''SEGURIDAD_ERRORDKRESPUESTA'''
SEGURIDAD_ERRORDKRESPUESTA = "No se permiten registrar valores duplicados, favor de verificar."

'''SEGURIDAD_ERRORNNULLRESPUESTA'''
SEGURIDAD_ERRORNNULLRESPUESTA = "No se permiten registrar valores nulos, favor de verificar."

'''TOKENAPIDEV'''
TOKENAPIDEV = "aHR0cHM6Ly9kZXYtYXBpLmJhbmNvYXp0ZWNhLmNvbS5teDo4MDgwL29hdXRoMi92MS90b2tlbg=="

'''TOKENAPIPRODEXT'''
TOKENAPIPRODEXT = "aHR0cHM6Ly9hcGkuYmFuY29henRlY2EuY29tL29hdXRoMi92MS90b2tlbg=="

'''TOKENAPIPRODINT'''
TOKENAPIPRODINT = "aHR0cHM6Ly9wcm9kLWFwaS5iYW5jb2F6dGVjYS5jb206ODA4MC9vYXV0aDIvdjEvdG9rZW4="

'''TOKENAPIPRODINT'''
TOKENAPIQA = "aHR0cHM6Ly9xYS5hcGliYXouY29tL29hdXRoMi92MS90b2tlbg=="

'''TOKENAPIAWS'''
TOKENAPIAWSINT = ("aHR0cHM6Ly9pbnRlcm5hbC1BUElHRUUtUFJPRC1BTEIwMS0xMzY2NjY0NzEzLnVzLWVhc3Qt" +
                  "MS5lbGIuYW1hem9uYXdzLmNvbTo4MDgxL29hdXRoMi92MS90b2tlbg==")

'''CREDAPILLAVESPROD'''
CREDAPILLAVESPROD = "Basic VkVmaFhYRkY0R21BR1prT2ppa3o2aExUblQ0RzNteDI6Q1NvSlIyVkNTOEphdzV5TQ=="

'''CREDAPILLAVESDEV'''
CREDAPILLAVESDEV = "Basic eTEyRDhHbEVmUmh3Q0Zob0ZaS0JHUkVHOGpaaVJRYVI6QWkyU2xRVW5UU3AydXFleQ=="

'''CREDAPILLAVESQA'''
CREDAPILLAVESQA = "Basic OXY3VU80ZHk5azdhdEluOHpUTnFXeUxFSmZxN2t4Z0M6ZFlvSGlyTmh4ZG12d3R2bg=="

'''LLAVESPRODEXT'''
LLAVESPRODEXT = \
    ("aHR0cHM6Ly9hcGkuYmFuY29henRlY2EuY29tL2NvYnJhbnphLWNyZWRpdG8vaW52ZXN0aWdhY2lvbi1jb2JyYW56YS9zZWd1cmlkYWQvdjEvYXB" +
     "saWNhY2lvbmVzL2xsYXZlcw==")

'''LLAVESPRODINT'''
LLAVESPRODINT = \
    ("aHR0cHM6Ly9wcm9kLWFwaS5iYW5jb2F6dGVjYS5jb206ODA4MC9jb2JyYW56YS1jcmVkaXRvL2ludmVzdGlnYWNpb24tY29icmFuemEvc2VndXJ" +
     "pZGFkL3YxL2FwbGljYWNpb25lcy9sbGF2ZXM=")

'''LLAVESDEV'''
LLAVESDEV = \
    ("aHR0cHM6Ly9kZXYtYXBpLmJhbmNvYXp0ZWNhLmNvbS5teDo4MDgwL2NvYnJhbnphLWNyZWRpdG8vaW52ZXN0aWdhY2lvbi1jb2JyYW56YS9zZWd" +
     "1cmlkYWQvdjEvYXBsaWNhY2lvbmVzL2xsYXZlcw==")

'''FOTODEFAULT'''
FOTODEFAULT = (
        "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" +
        "gNz//Z")

'''PATH'''
PATH = '/api/'

'''HEADER_TOKEN'''
HEADER_TOKEN = "token"

'''START_TIME'''
START_TIME = "startTime"

'''CODIGO_DEFAULT'''
CODIGO_DEFAULT = "JWT-5001"

'''URL_INFO'''
URL_INFO = "https://baz-developer.bancoazteca.com.mx/errors#JWT-5001"

'''MEDIA_TYPE'''
MEDIA_TYPE = "application/json"

'''MSG_TOKEN_NULL'''
MSG_TOKEN_NULL = "El Token es requerido"

'''USUARIO_TOKEN'''
USUARIO_TOKEN = "apigee"

'''SIN_EXPIRACION'''
SIN_EXPIRACION = "sin expiracion"

'''USUARIO_INVALIDO'''
USUARIO_INVALIDO = "Usuario invalido"

'''SELF'''
SELF = 'self'

'''PRIVATE_DER'''
PRIVATE_DER = ("-----BEGIN PRIVATE KEY-----" +
                "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC3zY4upt15IBkJ" +
                "UF3TFG57+1cD3GBD2DvTHqCl+z/poKvnI1vAfL6TMxYuwLfbX9QxhI/oi46sczaS" +
                "GaDmf7WXm9RQZfm11x3FyHSrPYpg7XfcRe93TJX+Eruh2ovxhowJ4K90lUuF6mOJ" +
                "KGcJqXjbGyGIOoYfepO6tX+sY6ixyWAr6rrTHwAa0BkVOWdPDFzfc29JP9U32WGN" +
                "lCZ1rbCQS1/VQPlPJGirAmWF8kSUQTimvD0eQj/dZgBuVRnKgNKtjAU8rc8a7exj" +
                "oJwFjNWDEZuxb45QY38Oo32okfNlptEg9gEWspK4/EspOmG4u6Qw0DObQ0or0Ub2" +
                "HfZzlaiHAgMBAAECggEAKNcRuqf1Gg7ZwUoMLvShQAcu5Hq5IRoQ4O4zP+4920mK" +
                "KMeggXq2VbrKOQU1VRdL7NzJpSAtSYAoJfpv2AeUb+V+HYcrHw53XRUXZ107PCJH" +
                "ubgIZ3eq9FNxQZtv8PC2eRNlqP/rUgwspbNGgc0YP4cdwklOt/vii1/8yG80cpwt" +
                "sGo8LsJKdePWPyDvxwZQmBlW4HcD1ND8yCjkdggGy4gYKUOlrv2RrQatamMUL5/t" +
                "30gmXlto/7v1QIvri/xPEPn+yqdM2W6FAiRGRjVwWNCbLx53meOj4F9s6Wu691Xv" +
                "0Ntqx7FUYokIdn62OUg5XvdNtCkAi2isIGzmNuwNMQKBgQDj5My2Me3OjRzqd35j" +
                "BQym5SlvDIm/rM+HYJuZ7esJDiwxLOUTgzWnaogadLLzoro9sZftRy/GoR2q0AVF" +
                "yCO5eLqHDfgQb4OpDqyWuVAF+M5ytD30cXHrON6qkMg4TPaHT2pxQ9c1fYPDsVOU" +
                "8pFdTlIkszEWVc23Ob9jcqJDTQKBgQDOeLG2+piB5BU0ro0m9R75jEZKvqEfoxLT" +
                "Op5jRXmlyxAsoTCQWLn3z0qbxqoNSILXG7ZEZ3pq+b41ZykLh05iEgbDrrDUxbnS" +
                "huSdATYM2swSvNJpBwEWUEdQ4WtaxkH4nsCf6E11ALqKyB21CoshmB39RACKLoaB" +
                "aAmmzUvJIwKBgQCq4ge2np3JAfsqvUtiCIlCJBf7kxU/St+ajZBfzg0tjxkIDrf+" +
                "96Yl0TYZUGRXWC/6zs4zN+vVLz7FtJIfj0Fqc+K6HnliKZw6CizUIESnFbgIPqsu" +
                "PlrDnLMqhsH7pYo+UAhqwgn/rAw/kxovV+w0YOQrbMpkCxbkS0L92RlfCQKBgD3j" +
                "N4GdQ7FLaH/OAkk3F/286iTlVu5gtvfRjkA7RudHIqX9+syJi9SXsclXlwk8Ptuz" +
                "VsLSMYN3MGhZb5ghCoGi3Zwx9JcSXUyZWlUlU8oumxTSvE725oCFt5qqtr8Sxht7" +
                "mklUHEOB4GhQ63aknmeHbRXJGFBS+cY4JQx2ZMz5AoGBAN9hj7b+PbqTwycYtt24" +
                "e7O1ebhjODnZHau38PaHdokOaXXMrw+PNAD5MdKryAmvbnpDlW7uEre7qepjHvb2" +
                "ZBik3EwFXSUwLXJlg7VOoAvpik+146e3E9Y9JqmvT1ssj8fHq/v0yMCkQyxwVAmJ" +
                "KHa2ZrCpYOy+TSLOyKqMRdOr" +
                "-----END PRIVATE KEY-----")
