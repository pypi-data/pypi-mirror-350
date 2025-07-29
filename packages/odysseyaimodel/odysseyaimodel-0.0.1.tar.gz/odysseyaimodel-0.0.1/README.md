# odysseyaimodel

[![Build Status](http://devops:8085/buildStatus/icon?job=DevOps%2Fodysseyaimodel)](http://devops:8085/job/DevOps/job/odysseyaimodel/)


## Características
- Este proyecto incorpora las funcionalidades genericas que pueden ser reutilizadas dentro otros proyectos python
- Se incorpora:
    - Utilieria para lanzar consultas o consultar funciones de base de datos oracle.
    - Metodos que permiten el encryptado y desencryptado de cadenas y archivos.
    - log estándarizado para su compatibilidad con kibana elastic search.
    - Cuenta con pruebas unitarias que garantizan su correcto funcionamiento.
    - Cuenta con estats de passed en sonarqube.
    - Flujo de devops de cobranza implementado, jenkinsfile con stages estándarizados

## Requerimientos

Para el correcto funcionamiento de esta libreria los requerimientos mínimos son:

- [Python 3.9+] - Base con Python 3.9 o superior
- [request] - Libreria para ejecutar peticiones webs
- [pycryptodome] - Libreria para el manejo de criptografía
- [pyctuator] - Libreria para actuator
- [json-encoder] - Libreria para el manejo de json
- [paprika] - Libreria para el manejo de boilerplate o burbujeo, similar a loombok en java
- [httpx] - Libreria de cliente HTTP con todas las funciones para Python 3. Incluye un cliente de línea de comando integrado, es compatible con HTTP/1.1 y HTTP/2, y proporciona API sincronizadas y asíncronas.
- [pytest] - Libreria para la ejecución de pruebas unitarias
- [pytest-cov] - Libreria para la generación de reporte de coverage de las pruebas unitarias
- [starlette] - Es un marco/kit de herramientas ASGI liviano, que es ideal para crear servicios web asíncronos en Python.
- [python-dotenv] - Libreria para el manejo de lectura o escritura para variables de entorno
- [wheel] - Esta libreria es la implementación de referencia del estándar de empaquetado de ruedas de Python, tal como se define en PEP 427.
- [PyJWT] - Libreria para el manejo de tokens jwt, claims, security y demás
- [pytz] - Libreria para el manejo de zona horaria
- [setuptools] - Libreria para la generación de compilado del proyecto
- [oracledb] - Libreria para el manejo de cliente oracle db

La plantilla se mantiene actualizada por el Chapter en el repositorio de la dirección [private repository][repo]
 en DevOps:8181.

## Instalación

odysseyaimodel requiere de python [python] 3.9+ para correr.

Instala las dependencias para poder ejecutar la aplicación

```sh
pip install --trusted-host devops -i https://$artifactorycreds@devops/artifactory/api/pypi/python-local/simple -r ./requirements.txt
```

## Plugins

odysseyaimodel actualmente no requiere o hace uso de plugins adicionales para ejecutarse de forma correcta

| Plugin | README |
| ------ | ------ |

## Desarrollo

Quieres contribuir? Genial!

odysseyaimodel usa wheel para la compilación del proyecto.
Si requieres especificar cambios sobre el setup generado recuerda actualizar el archivo de [setup] 

Para compilar tu proyecto:

```sh
python3 setup.py sdist bdist_wheel
```

Para publicarlo en el registry de cobranza:

```sh
twine upload --repository local --skip-existing dist/* --cert $devopsrcert --config-file ~/.pypirc
```

## Docker

odysseyaimodel no requiere contenerizarse ya que se implementa como libreria dentro de otros proyectos.

## Licencia

GPL

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [repo]: http://devops:8181/cloud/odysseyaimodel
   [python]: https://www.python.org/
   [setup]: <https://docs.python.org/3/distutils/setupscript.html>

