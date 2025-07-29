'''
Proyecto: pythonTemplate
Clase: Cadenas
Mantenedor: EYMG
Fecha: 2023-04-27
OT: NA
Ultimo cambio: Definición de documentación para sonarqube
'''


class Cadenas(object):
    '''SCT'''
    SCT = "Q29icmFuemFfQ2xvdWR5RGV2T3Bz"

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

    '''MSJ_CODIGO_NA'''
    MSJ_CODIGO_NA = "No implementado."

    '''MSJ_TOKEN_INVALIDO'''
    MSJ_TOKEN_INVALIDO = "El token no es válido."

    '''MSJ_TOKEN_FECHA_INVALIDA'''
    MSJ_TOKEN_FECHA_INVALIDA = "Fecha no válida para generar token."

    '''MSJ_TOKEN_EXPIRADO'''
    MSJ_TOKEN_EXPIRADO = "El token ha expirado."

    '''MSJ_CADENATOKEN_DIFERENTE'''
    MSJ_CADENATOKEN_DIFERENTE = (
        "La cadena no es la misma con la que se originó el token. Por favor verifique la información.")

    '''MSJ_CANTIDAD_PARAMETROS_INVALIDO'''
    MSJ_CANTIDAD_PARAMETROS_INVALIDO = "Cantidad de parámetros no válido."

    '''MSJ_METODO_NO_EXISTE'''
    MSJ_METODO_NO_EXISTE = "El no. de método invocado no éxiste"

    '''ENCODING'''
    ENCODING = "UTF-8"

    '''MSJ_CODIGO_200_DESCRIPCION_OPEN'''
    MSJ_CODIGO_200_DESCRIPCION_OPEN = "Operación exitosa."

    '''MSJ_CODIGO_201_DESCRIPCION_OPEN'''
    MSJ_CODIGO_201_DESCRIPCION_OPEN = "Solicitud creada de forma exitosa."

    '''MSJ_CODIGO_400_DESCRIPCION_OPEN'''
    MSJ_CODIGO_400_DESCRIPCION_OPEN = "Solicitud Incorrecta."

    '''MSJ_CODIGO_401_DESCRIPCION_OPEN'''
    MSJ_CODIGO_401_DESCRIPCION_OPEN = "No autorizado."

    '''MSJ_CODIGO_403_DESCRIPCION_OPEN'''
    MSJ_CODIGO_403_DESCRIPCION_OPEN = "No es posible realizar esta operación."

    '''MSJ_CODIGO_404_DESCRIPCION_OPEN'''
    MSJ_CODIGO_404_DESCRIPCION_OPEN = "No encontrado."

    '''MSJ_CODIGO_405_DESCRIPCION_OPEN'''
    MSJ_CODIGO_405_DESCRIPCION_OPEN = "Método no permitido."

    '''MSJ_CODIGO_422_DESCRIPCION_OPEN'''
    MSJ_CODIGO_422_DESCRIPCION_OPEN = "Entidad no procesable."

    '''MSJ_CODIGO_500_DESCRIPCION_OPEN'''
    MSJ_CODIGO_500_DESCRIPCION_OPEN = "Error interno en el servicio."

    '''MSJ_CODIGO_501_DESCRIPCION_OPEN'''
    MSJ_CODIGO_501_DESCRIPCION_OPEN = "No implementado."

    codigo_api = "145"
    direccion = "Cobranza"
    area = "CloudyDevops"
    app = "default"

    def __init__(self):
        '''Constructor de la clase cadenas
            Mantenedor: EYMG
            Fecha: 2023-04-27
            OT: NA
            Ultimo cambio: Definición de documentación para sonarqube'''

    @staticmethod
    def set_celula(direccion, area, app, codigo):
        '''
        set_celula
        :param direccion: Dirección a la que pertenece
        :param area: Area a la que pertenece
        :param app: Aplicación a la que pertenece
        :return: Cadena armada para infografía
        '''
        Cadenas.direccion = direccion
        Cadenas.area = area
        Cadenas.app = app
        Cadenas.codigo_api = codigo

        return (direccion + "-" + area + "-" + app).replace(" ", "-").replace(".", "-")

    @staticmethod
    def get_celula():
        '''
        get_celula
        :return: Cadena de célula para infografía
        '''
        return (Cadenas.direccion + "-" + Cadenas.area + "-" + Cadenas.app).replace(" ", "-").replace(".", "-")

    @staticmethod
    def set_codigo_api(codigo):
        '''
        set_codigo_api
        :param codigo: Codigo api para infografía
        :return:
        '''
        Cadenas.codigo_api = codigo

    @staticmethod
    def get_codigo_api():
        '''
        get_codigo_api
        :return: Codigo api para infografía
        '''
        return Cadenas.codigo_api

    @staticmethod
    def msj_codigo_200():
        '''
        msj_codigo_200
        :return: Cadena para infografía
        '''
        return "200." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "200"

    @staticmethod
    def msj_codigo_201():
        '''
        msj_codigo_201
        :return: Cadena para infografía
        '''
        return "201." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "201"

    @staticmethod
    def msj_codigo_400():
        '''
        msj_codigo_400
        :return: Cadena para infografía
        '''
        return "400." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "400"

    @staticmethod
    def msj_codigo_401():
        '''
        msj_codigo_401
        :return: Cadena para infografía
        '''
        return "401." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "401"

    @staticmethod
    def msj_codigo_403():
        '''
        msj_codigo_403
        :return: Cadena para infografía
        '''
        return "403." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "403"

    @staticmethod
    def msj_codigo_404():
        '''
        msj_codigo_404
        :return: Cadena para infografía
        '''
        return "404." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "404"

    @staticmethod
    def msj_codigo_405():
        '''
        msj_codigo_405
        :return: Cadena para infografía
        '''
        return "405." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "405"

    @staticmethod
    def msj_codigo_422():
        '''
        msj_codigo_422
        :return: Cadena para infografía
        '''
        return "422." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "422"

    @staticmethod
    def msj_codigo_500():
        '''
        msj_codigo_500
        :return: Cadena para infografía
        '''
        return "500." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "500"

    @staticmethod
    def msj_codigo_501():
        '''
        msj_codigo_501
        :return: Cadena para infografía
        '''
        return "501." + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "501"

    @staticmethod
    def msj_codigo_200_info():
        '''
        msj_codigo_200_info
        :return: Cadena para infografía
        '''
        return ("https://baz-developer.bancoazteca.com.mx/info#200." + Cadenas.get_celula() +
                "." + Cadenas.get_codigo_api() + "200")

    @staticmethod
    def msj_codigo_201_info():
        '''
        msj_codigo_201_info
        :return: Cadena para infografía
        '''
        return ("https://baz-developer.bancoazteca.com.mx/info#201." + Cadenas.get_celula() +
                "." + Cadenas.get_codigo_api() + "201")

    @staticmethod
    def msj_codigo_400_info():
        '''
        msj_codigo_400_info
        :return: Cadena para infografía
        '''
        return ("https://baz-developer.bancoazteca.com.mx/info#400."
                + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "400")

    @staticmethod
    def msj_codigo_401_info():
        '''
        msj_codigo_401_info
        :return: Cadena para infografía
        '''
        return ("https://baz-developer.bancoazteca.com.mx/info#401."
                + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "401")

    @staticmethod
    def msj_codigo_403_info():
        '''
        msj_codigo_403_Info
        :return: Cadena para infografía
        '''
        return ("https://baz-developer.bancoazteca.com.mx/info#403."
                + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "403")

    @staticmethod
    def msj_codigo_404_info():
        '''
        msj_codigo_404_info
        :return: Cadena para infografía
        '''
        return ("https://baz-developer.bancoazteca.com.mx/info#404."
                + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "404")

    @staticmethod
    def msj_codigo_405_info():
        '''
        msj_codigo_405_info
        :return: Cadena para infografía
        '''
        return ("https://baz-developer.bancoazteca.com.mx/info#405."
                + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "405")

    @staticmethod
    def msj_codigo_422_info():
        '''
        msj_codigo_422_info
        :return: Cadena para infografía
        '''
        return ("https://baz-developer.bancoazteca.com.mx/info#422."
                + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "422")

    @staticmethod
    def msj_codigo_500_info():
        '''
        msj_codigo_500_info
        :return: Cadena para infografía
        '''
        return ("https://baz-developer.bancoazteca.com.mx/info#500."
                + Cadenas.get_celula() + "." + Cadenas.get_codigo_api() + "500")
