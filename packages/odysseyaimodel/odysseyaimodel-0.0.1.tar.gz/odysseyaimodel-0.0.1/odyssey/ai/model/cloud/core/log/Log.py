'''Módulo de Log'''
import json
import logging
from datetime import datetime

import pytz

from odyssey.ai.model.cloud.configuracion.Configuracion import tz
from odyssey.ai.model.cloud.core.log.Level import Level


class Log(object):
    '''
          Proyecto: pythonTemplate
          Clase: Log
          Mantenedor: MTIB
          Fecha: 2023-07-10
          OT: NA
          Ultimo cambio:
      '''

    FORMAT = "%(message)s"
    __date = datetime.now(pytz.timezone(tz))
    FORMAT_DATE = "%Y-%m-%d %H:%M:%S"

    def __init__(self, ip, lvl = logging.DEBUG):
        '''
        __init__
        '''
        '''
        Se establece la configuración de fondo para que opere en modo debug y las impresiones en loggers para monitoreo
        operaciones cumpla el estandar de json sin ningun otro dato para poder homologarse al estandar y ser leido por
        kibana
        '''
        logging.basicConfig(format=self.FORMAT, level=lvl)

        self.__date = datetime.now(pytz.timezone(tz))
        self.__services = []
        self.ip = ip

    def clean_nones(self, value):
        '''
                Proyecto: pythonTemplate
                Clase: Log
                Metodo: clean_nones
                Mantenedor: EYMG
                Fecha: 2023-04-27
                OT: NA
                Ultimo cambio: Recursively remove all None values from dictionaries and lists, and returns
                the result as a new dictionary or list.
        '''
        if isinstance(value, list):
            return [self.clean_nones(x) for x in value if x is not None]
        elif isinstance(value, dict):
            return {
                key: self.clean_nones(val)
                for key, val in value.items()
                if val is not None
            }
        else:
            return value

    def escribe_log(self, level: Level, request: str, message: str, response: str, service: str, system: str,
                    save: bool,  data = None):
        '''
            escribe_log
            :param level: Level
            :param request: str
            :param message: str
            :param response: str
            :param service: str
            :param system: str
            :param save: bool
        '''

        __date2 = datetime.now(pytz.timezone(tz))

        __time = __date2 - self.__date
        __time = __time.microseconds // 1000

        if save == True:
            log = {"log_data":
                {
                    "fecha": str(__date2.strftime(self.FORMAT_DATE)),
                    "Level": level.name,
                    "Mensaje": message,
                    "servicios": self.__services,
                    "TiempoTotal": self.get_tiempo_total(),
                    "adicional": {
                        "servicio": service,
                        "Sistema": system,
                        "peticion": request,
                        "respuesta": response,
                        "ip": self.ip
                    }
                }
            }

            json_log = json.loads(json.dumps(log))

            json_log = self.clean_nones(json_log.copy())
            json_log = json.dumps(json_log, ensure_ascii=False, allow_nan=False)

            if level == Level.INFO:
                logging.info(json_log)
            elif level == level.DEBUG:
                logging.debug(json_log)
            elif level == level.WARN:
                logging.warn(json_log)
            elif level == level.FATAL:
                logging.fatal(json_log)
            elif level == level.CRITICAL:
                logging.critical(json_log)
            elif level == level.NOTSET:
                logging.debug(json_log)
            else:
                logging.error(json_log)

            self.__services = []
        else:
            '''aqui añade servicios'''
            services = {
                "servicio": service,
                "Sistema": system,
                "Tiempo": __time,
                "peticion": request,
                "respuesta": response,
                "Mensaje": message,
                "Data":data
            }
            self.__services.append(services)

        self.__date = datetime.now(pytz.timezone(tz))

    def get_tiempo_total(self):
        '''
        get_tiempo_total
        :return: tiempo total sumarizado de servicios
        '''
        tiempo = 0
        for service in self.__services:
            tiempo += service["Tiempo"]
        return tiempo
