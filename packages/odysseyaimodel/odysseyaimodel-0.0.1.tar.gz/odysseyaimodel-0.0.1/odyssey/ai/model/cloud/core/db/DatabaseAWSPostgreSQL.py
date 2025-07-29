'''Módulo para interactuar con bases de datos PostgreSQL en AWS RDS.'''
import json
import psycopg2  # Librería para PostgreSQL
from psycopg2 import extras  # Para obtener resultados como diccionarios

# Asumo que estas clases existen y tienen una estructura similar
# from odyssey.ai.model.cloud.core.models.DB import DB # Podrías adaptarlo o quitarlo si la clase es solo para PG
from odyssey.ai.model.cloud.core.models.Daos import Daos
from odyssey.ai.model.cloud.core.models.TipoConsulta import TipoConsulta


class DatabaseAWSPostgreSQL(object):
    '''
        Proyecto: odysseyaimodel (Adaptado para PostgreSQL)
        Clase: DatabasePostgreSQL
        Mantenedor: EYMG (Adaptado por Asistente AI)
        Fecha: 2023-06-27 (Fecha original, adaptado hoy)
        OT: NA
        Ultimo cambio: Adaptación para PostgreSQL y mejoras de claridad.
    '''

    def __init__(self):
        '''
            Inicializador de la clase.
            La conexión se establecerá explícitamente.
        '''
        self.__connection = None
        self.__cursor = None

    def init_connection(self, db_usr, db_paw, db_url, port, db_name):
        """
        Inicializa la conexión a la base de datos PostgreSQL.

        Args:
            db_usr (str): Usuario de la base de datos.
            db_paw (str): Contraseña del usuario.
            db_url (str): Host o URL del servidor de base de datos.
            port (int): Puerto de la base de datos.
            db_name (str): Nombre de la base de datos a la que conectar.

        Returns:
            psycopg2.connection: Objeto de conexión o None si falla.

        Raises:
            psycopg2.Error: Si ocurre un error durante la conexión.
        """
        try:
            self.__connection = psycopg2.connect(
                user=db_usr,
                password=db_paw,
                host=db_url,
                port=port,
                dbname=db_name
            )
            # Autocommit puede ser útil para sentencias simples,
            # pero para transacciones complejas, es mejor manejarlo explícitamente.
            # self.__connection.autocommit = True
            print(f"Conexión a PostgreSQL '{db_name}' establecida exitosamente.")
            return self.__connection
        except psycopg2.Error as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            self.__connection = None
            raise  # Relanzar la excepción para que el llamador la maneje

    def get_db_version(self):
        """
        Obtiene la versión del servidor PostgreSQL.

        Returns:
            str: Versión del servidor PostgreSQL o None si no hay conexión.
        """
        if not self.__connection:
            print("Error: No hay conexión activa.")
            return None
        try:
            with self.__connection.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
                return version[0] if version else None
        except psycopg2.Error as e:
            print(f"Error al obtener la versión de PostgreSQL: {e}")
            return None

    def test_connection(self):
        """
        Prueba la conexión ejecutando una consulta simple.
        """
        if not self.__connection:
            print("Error: No hay conexión activa para probar.")
            return False
        try:
            with self.__connection.cursor() as cur:
                cur.execute("SELECT 1;")
                result = cur.fetchone()
                if result and result[0] == 1:
                    print("Prueba de conexión a PostgreSQL exitosa (SELECT 1).")
                    return True
                else:
                    print("Prueba de conexión a PostgreSQL fallida.")
                    return False
        except psycopg2.Error as e:
            print(f"Error durante la prueba de conexión a PostgreSQL: {e}")
            return False

    def close_connection(self):
        """
        Cierra la conexión a la base de datos si está abierta.
        """
        if self.__cursor:
            try:
                self.__cursor.close()
                self.__cursor = None
            except psycopg2.Error as e:
                print(f"Error al cerrar el cursor: {e}")
        if self.__connection:
            try:
                self.__connection.close()
                self.__connection = None
                print("Conexión a PostgreSQL cerrada.")
            except psycopg2.Error as e:
                print(f"Error al cerrar la conexión a PostgreSQL: {e}")

    def _execute_query(self, query, params=None, is_function_returning_cursor=False):
        """
        Método auxiliar para ejecutar consultas o funciones.
        Si is_function_returning_cursor es True, se asume que la función
        devuelve un nombre de cursor que luego debe ser usado para FETCH.
        Para la mayoría de las funciones que devuelven SETOF, esto no es necesario.
        """
        if not self.__connection:
            raise psycopg2.InterfaceError("No hay conexión activa.")

        # Usar un nuevo cursor para cada ejecución o manejar el cursor de la clase
        # Aquí se crea uno nuevo para evitar problemas de estado.
        current_cursor = self.__connection.cursor(cursor_factory=extras.DictCursor)

        try:
            # Para funciones que devuelven un conjunto de filas (SETOF) o un valor escalar:
            # La consulta sería algo como "SELECT * FROM mi_funcion(%s, %s);" o "SELECT mi_funcion(%s);"
            # Para procedimientos que no devuelven un resultset directamente (usan CALL):
            # current_cursor.callproc(nombre_funcion, params) # Para procedimientos
            current_cursor.execute(query, params)

            # Si la función devuelve un nombre de cursor (REFCURSOR)
            if is_function_returning_cursor:
                refcursor_name = current_cursor.fetchone()[0]
                # Crear una nueva consulta para obtener datos de ese refcursor
                current_cursor.execute(f"FETCH ALL in \"{refcursor_name}\";")

            # extras.DictCursor permite acceder a las columnas por nombre
            columnas = [desc[0] for desc in current_cursor.description] if current_cursor.description else []

            resultados_raw = current_cursor.fetchall()
            respuestas = []

            for row_dict in resultados_raw:  # row_dict ya es un diccionario (o similar a DictRow)
                resp_aux = {}
                for col_name in columnas:
                    item = row_dict[col_name]
                    # En PostgreSQL, los tipos JSON/JSONB son usualmente deserializados
                    # automáticamente por psycopg2 a dicts/lists de Python.
                    # Si un campo TEXT contiene una cadena JSON, necesitarías json.loads().
                    # El manejo de LOBs de Oracle es diferente. Bytea en PG se leería como bytes.
                    if isinstance(item, bytes):  # Ejemplo si fuera un bytea que necesitas decodificar
                        try:
                            resp_aux[col_name] = json.loads(item.decode('utf-8'))
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            # Si no es JSON o no es utf-8, guardar como string de bytes o manejar diferente
                            resp_aux[col_name] = f"<bytes data len:{len(item)}>"
                    else:
                        resp_aux[col_name] = item
                respuestas.append(resp_aux)

            self.__connection.commit()  # Comitear si la ejecución fue exitosa (SELECT no necesita, pero DML sí)
            return respuestas

        except psycopg2.Error as e:
            if self.__connection:  # Solo hacer rollback si la conexión sigue viva
                self.__connection.rollback()
            print(f"Error durante la ejecución de la consulta/función: {e}")
            raise  # Relanzar para que el llamador maneje
        finally:
            if current_cursor:
                current_cursor.close()

    def consulta(self, daos: Daos):
        """
        Ejecuta una consulta o una función en la base de datos PostgreSQL.

        Args:
            daos (Daos): Objeto DAO que contiene los detalles de la consulta/función.
                         Se espera que tenga métodos:
                         - get_tipo_consulta() -> TipoConsulta (DB_FUNCION o DB_CONSULTA)
                         - get_funcion() -> str (Nombre de la función/procedimiento o la consulta SQL completa si es DB_CONSULTA)
                         - get_parametros() -> list or tuple (Parámetros para la función/consulta)
                         - get_consulta() -> str (Consulta SQL, usado si get_tipo_consulta es DB_CONSULTA)

        Returns:
            list: Una lista de diccionarios, donde cada diccionario representa una fila.
                  Retorna lista vacía si no hay resultados o en caso de error manejado.

        Raises:
            Exception: Si ocurre un error no manejado durante la ejecución.
        """
        if not self.__connection:
            print("Error: No hay conexión activa para realizar la consulta.")
            # Podrías lanzar una excepción aquí en lugar de solo imprimir.
            raise psycopg2.InterfaceError("Conexión no inicializada.")

        try:
            query_string = ""
            params = daos.get_parametros() if hasattr(daos, 'get_parametros') else None

            if daos.get_tipo_consulta() == TipoConsulta.DB_FUNCION:
                # Para PostgreSQL, las funciones que devuelven datos se llaman generalmente con SELECT
                # Asumimos que get_funcion() devuelve el nombre de la función.
                # Y que los parámetros se pasarán posicionalmente.
                # Ejemplo: "SELECT * FROM mi_funcion_setof(%s, %s)"
                # Ejemplo: "SELECT mi_funcion_escalar(%s)"
                # El DAO debería proveer la sentencia SELECT completa para la función.
                # Si get_funcion() solo da el nombre, necesitaríamos construir el SELECT.
                # Por simplicidad, asumiremos que get_funcion() para DB_FUNCION
                # ya es una sentencia SELECT que llama a la función, o el nombre de un procedimiento.

                # Si get_funcion() es solo el nombre, ej: "esquema.mi_funcion"
                # y get_parametros() es [1, 'texto']
                # query_string = f"SELECT * FROM {daos.get_funcion()}({', '.join(['%s'] * len(params))});"
                # Esta es una simplificación. Si la función devuelve REFCURSOR, es más complejo.
                # Si el DAO ya provee la sentencia SELECT completa en get_funcion():
                query_string = daos.get_funcion()  # Asumimos que esto es "SELECT mi_funcion(%s)" o similar
                # o el nombre de un procedimiento para callproc

                # Nota: psycopg2 no tiene un `callfunc` directo como oracledb que devuelve un cursor.
                # Las funciones se llaman con SELECT. Los procedimientos con CALL o cursor.callproc().
                # Si es un procedimiento que no devuelve un resultset directamente:
                # self.__cursor.callproc(daos.get_funcion(), params)
                # return [] # O manejar de otra forma, ya que callproc no devuelve filas directamente.
                # Por ahora, nos enfocaremos en funciones llamadas con SELECT.

            elif daos.get_tipo_consulta() == TipoConsulta.DB_CONSULTA:
                query_string = daos.get_consulta()
            else:
                print(f"Tipo de consulta no soportado: {daos.get_tipo_consulta()}")
                return []

            if not query_string:
                print("Error: La cadena de consulta o nombre de función está vacía.")
                return []

            return self._execute_query(query_string, params)

        except psycopg2.Error as db_err:
            # El error ya se logueó en _execute_query y se hizo rollback
            print(f"Error de base deatos en 'consulta': {db_err}")
            # Dependiendo de la política de errores, podrías retornar [] o relanzar
            return []  # Retornar lista vacía en caso de error de BD manejado
        except Exception as e:
            print(f"Error inesperado en el método 'consulta': {e}")
            # Considera relanzar si es un error que el llamador debe conocer
            # raise
            return []

    def test_pg_function_call(self, function_schema, function_name, params_list):
        """
        Ejemplo de cómo llamar a una función PostgreSQL que devuelve un conjunto de filas (SETOF)
        o un valor escalar.

        Args:
            function_schema (str): Esquema de la función.
            function_name (str): Nombre de la función.
            params_list (list): Lista de parámetros para la función.

        Returns:
            list: Resultados de la función, o lista vacía en error.
        """
        if not self.__connection:
            print("Error: No hay conexión activa.")
            return []

        placeholders = ', '.join(['%s'] * len(params_list))
        # Si la función devuelve un solo valor: SELECT esquema.nombre_funcion(%s, %s);
        # Si la función devuelve un conjunto de filas: SELECT * FROM esquema.nombre_funcion(%s, %s);
        # Asumimos que devuelve un conjunto de filas para este ejemplo genérico.
        query = f"SELECT * FROM {function_schema}.{function_name}({placeholders});"

        print(f"Ejecutando función PG: {query} con params {params_list}")
        try:
            return self._execute_query(query, params_list)
        except Exception as e:
            # _execute_query ya loguea y hace rollback si es necesario
            print(f"Error al llamar a la función PostgreSQL '{function_name}': {e}")
            return []

    # Método __del__ para asegurar que la conexión se cierre al destruir el objeto
    def __del__(self):
        self.close_connection()
