'''Módulo de Configuracion, '''
import os

from dotenv import load_dotenv

from odyssey.ai.model.cloud.core.utilerias.Cadenas import Cadenas

load_dotenv()

env = os.getenv('ENV', 'devlocal')
app_port = os.getenv('APP_PORT', '13000')
app_name_origin = os.getenv('APP_NAME', 'odysseyaimodel')
origins = os.getenv('ORIGINS', 'http://localhost:13000')
base_path = os.getenv('BASE_URL', '/direccion/area/mso-python-template')
version = os.getenv('VERSION', 'v1')
direction = os.getenv('DIRECCION', 'direccion')
area = os.getenv('AREA', 'area')
app = os.getenv('APP', 'app')
code_api = os.getenv('CODIGO_API', '000')
host = os.getenv('HOST')
db_usr = os.getenv('DB_USR')
db_paw = os.getenv('DB_PAW')
db_url = os.getenv('DB_URL')
public_key_apigee = os.getenv('PUBLIC_KEY_APIGEE')
tz = os.getenv('TZ', 'Etc/GMT+6')
os.environ['TZ'] = tz

oauth2_apigee ="Basic " + os.getenv('OAUTH2_APIGEE',
                                    'eTEyRDhHbEVmUmh3Q0Zob0ZaS0JHUkVHOGpaaVJRYVI6QWkyU2xRVW5UU3AydXFleQ==')
fqdn_apigee = os.getenv('FQDN_APIGEE', 'https://dev-api.bancoazteca.com.mx:8080')



class Configuracion(object):
    '''
        Proyecto: pythonTemplate
        Clase: Configuracion
        Cloud y DevOps
        Mantenedor: EYMG
        Fecha: 2023-06-27
        Descripción: Clase de configuración de la aplicación
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
    '''
    def __init__(self):
        Cadenas.set_celula(direction, area, app, code_api)
