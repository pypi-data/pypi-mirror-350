"""lambda_function.py
   Mantenedor:
   Fecha: 2023-04-27
   OT: NA
   utilidades_bd.py"""
import json
import boto3
import pytz
from odyssey.ai.model.cloud.core.db.DatabaseAWS import DatabaseAWS
from datetime import datetime
from odyssey.ai.model.cloud.configuracion.Configuracion import tz
from odyssey.ai.model.cloud.core.db.DatabaseAWSPostgreSQL import DatabaseAWSPostgreSQL
import psycopg2 # Para capturar excepciones específicas de psycopg2 si es necesario


class UtilidadesBD(object):
    """
    Clase UtilidadesBD
    """

    def __init__(self):
        self.ssm = boto3.client('ssm')

    def get_body_refactor(self, event):
        body = json.loads(event['body'])
        json_data = ((json.dumps(body['payload'])).replace("'", '"').replace('\"', '"')
                     .replace('\r', '').replace('\n', ''))

        return json_data

    def replasce_json(self, body):
        json_data = (body.replace("'", '"').replace('\"', '"')
                     .replace('\r', '').replace('\n', ''))

        return json_data

    def get_parameter(self, parameter_name):
        response = self.ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value']

    def connection_aws_bd(self, parameter='ffm-data-orcl'):
        db = DatabaseAWS()
        parameters_aws = self.get_parameter(parameter)
        ind_parameters = parameters_aws.split("|")
        db.init_connection(ind_parameters[0], ind_parameters[1], ind_parameters[2],
                           ind_parameters[3], ind_parameters[4])

        return db

    def connection_aws_postgresql_bd(self, parameter_name='rds-data-psql'):
        """
        Establece una conexión a una base de datos PostgreSQL en AWS RDS,
        obteniendo los parámetros de conexión desde AWS Systems Manager Parameter Store.

        El valor del parámetro en Parameter Store debe tener el formato:
        host|puerto|usuario|contraseña|nombre_basedatos

        Args:
            parameter_name (str): El nombre del parámetro en AWS SSM Parameter Store
                                  que contiene la cadena de conexión.
                                  Por defecto es 'rds-data-psql'.

        Returns:
            DatabaseAWSPostgreSQL: Una instancia de la clase DatabaseAWSPostgreSQL
                                   con una conexión activa si fue exitosa.
            None: Si la conexión no pudo ser establecida o los parámetros son incorrectos.
        """
        print(f"Intentando conectar a PostgreSQL RDS usando el parámetro SSM: {parameter_name}")
        db_instance = None
        try:
            # 1. Obtener la cadena de parámetros desde SSM
            connection_string = self.get_parameter(parameter_name)
            params = connection_string.split("|")

            # 2. Validar que tenemos el número esperado de parámetros
            if len(params) != 5:
                print(
                    f"Error: El parámetro SSM '{parameter_name}' no contiene los 5 valores esperados (host|puerto|usuario|contraseña|nombre_basedatos).")
                print(f"Valores obtenidos: {params}")
                return None

            db_host = params[0]
            try:
                db_port = int(params[1])  # El puerto debe ser un entero
            except ValueError:
                print(f"Error: El puerto '{params[1]}' obtenido del parámetro SSM no es un número válido.")
                return None
            db_user = params[2]
            db_password = params[3]
            db_name = params[4]

            print(
                f"Parámetros de conexión obtenidos de SSM para PostgreSQL: Host={db_host}, Port={db_port}, User={db_user}, DBName={db_name}")

            # 3. Crear una instancia de la clase DatabaseAWSPostgreSQL
            db_instance = DatabaseAWSPostgreSQL()

            # 4. Inicializar la conexión
            connection = db_instance.init_connection(
                db_usr=db_user,
                db_paw=db_password,
                db_url=db_host,
                port=db_port,
                db_name=db_name
            )

            if connection:
                print("Conexión a PostgreSQL RDS establecida exitosamente a través de la utilidad y SSM.")
                return db_instance
            else:
                # init_connection ya imprime un error y levanta una excepción que se captura abajo,
                # o devuelve None si no la levantara.
                print(
                    "Falló la inicialización de la conexión a PostgreSQL RDS desde la utilidad (conexión es None después de init_connection).")
                return None

        except self.ssm.exceptions.ParameterNotFound:
            print(f"Error: El parámetro SSM '{parameter_name}' no fue encontrado.")
            return None
        except psycopg2.Error as e:
            # Este bloque captura la excepción psycopg2.Error relanzada por init_connection
            print(f"Error específico de psycopg2 al intentar conectar a PostgreSQL RDS: {e}")
            if db_instance:
                db_instance.close_connection()  # Asegurarse de cerrar si algo se abrió parcialmente
            return None
        except Exception as e:
            print(f"Error general inesperado al intentar conectar a PostgreSQL RDS usando SSM: {e}")
            if db_instance:
                db_instance.close_connection()  # Asegurarse de cerrar
            return None

    def folio(self):
        pattern = "%Y%m%d"
        today = datetime.now(pytz.timezone(tz))
        timestamp = datetime.now(pytz.timezone(tz)).timestamp()
        formatter = today.strftime(pattern)
        return formatter + str(int(timestamp))
