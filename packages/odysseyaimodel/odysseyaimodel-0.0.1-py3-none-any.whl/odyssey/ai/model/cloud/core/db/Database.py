'''Módulo de Database, '''
import json

import oracledb

from odyssey.ai.model.cloud.configuracion.Configuracion import db_usr, db_paw, db_url
from odyssey.ai.model.cloud.core.models.DB import DB
from odyssey.ai.model.cloud.core.models.Daos import Daos
from odyssey.ai.model.cloud.core.models.TipoConsulta import TipoConsulta

__connection = None


class Database(object):
    '''
        Proyecto: pythonTemplate
        Clase: Database
        Mantenedor: EYMG
        Fecha: 2023-06-27
        OT: NA
        Ultimo cambio: Definición de documentación para sonarqube
    '''

    def __init__(self):
        '''
            __init__
        '''

    def init_connection(self):
        """
        init_connection
        """
        self.__connection = oracledb.connect(
            user=db_usr,
            password=db_paw,
            dsn=db_url
        )
        return self.__connection

    def get_version(self):
        """
        get_version
        """
        return self.__connection.version

    def test_connection(self):
        """
        test_connection
        """
        cursor = self.__connection.cursor()
        for row in cursor.execute("select 1 dual from DUAL"):
            print(row)

    def close_connection(self):
        """
        close_connection
        """
        self.__connection.close()

    def test_fnx_buscacte(self):
        """
        test_fnx_buscacte
        """
        cursor = self.__connection.cursor()
        for row in cursor.callfunc("RCREDITO.FNBUSCACLIENTE", oracledb.CURSOR, [1, 1, 100, 92]):
            aux = json.loads(json.loads(json.dumps(row))[0])
            print(aux)

    def consulta(self, daos: Daos):
        """
            consulta
        """
        if (daos.get_db() == DB.DB_ORACLE):
            self.init_connection()
            cursor = self.__connection.cursor()
            if (daos.get_tipo_consulta() == TipoConsulta.DB_FUNCION):
                cursor_ref = cursor.callfunc(daos.get_funcion(), oracledb.CURSOR, daos.get_parametros())
            else:
                cursor_ref = cursor.execute(daos.get_consulta())
            respuestas = []

            columnas = []
            valores = [row for row in cursor_ref]

            for column in cursor_ref.description:
                columnas.append(str(column[0]).lower())

            for valor in valores:
                x = 0
                resp_aux = {}
                for item in valor:
                    resp_aux[columnas[x]] = item
                    x += 1
                respuestas.append(resp_aux)

            self.close_connection()

            return respuestas
