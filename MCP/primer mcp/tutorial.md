La inteligencia artificial está evolucionando a un ritmo asombroso. Los modelos actuales pueden razonar, escribir, programar y analizar información de maneras que antes parecían imposibles.

Pero existe una limitación importante que aún los frena: el contexto.

La mayoría de los modelos de IA no tienen acceso a tu sistema, archivos, API ni datos en tiempo real. Solo saben lo que les indicas en una solicitud.

El Protocolo de Contexto de Modelos , también conocido como MCP, se creó para solucionar este problema. Permite que los modelos de IA se conecten de forma segura a tus propias herramientas, API y sistemas mediante pequeños servidores estructurados conocidos como servidores MCP.

En esta guía, aprenderás a crear tu propio servidor MCP usando Python. Analizaremos cada parte del código y te explicaré cómo funciona.

Al finalizar, tendrás un servidor MCP en funcionamiento capaz de sumar números, generar palabras aleatorias y obtener datos meteorológicos en tiempo real de internet. También veremos cómo alojar este servidor MCP en la nube.

Lo que cubriremos:
¿Qué es el Protocolo de Contexto de Modelo ?

Configurando su entorno

Creación del proyecto

Configuración del registro

Creación del servidor MCP

Herramientas de definición

Ejemplo 1: Sumar dos números

Ejemplo 2: Devolver una palabra secreta aleatoria

Ejemplo 3: Obtención de datos meteorológicos

Ejecutando el servidor

Probando las herramientas

Implementación de su servidor MCP en Sevalla

¿Por qué crear tu propio servidor MCP?

Ampliación del servidor

Conclusión

¿Qué es el Protocolo de Contexto de Modelo?
Antes de adentrarnos en el código, es importante comprender qué es realmente el Protocolo de Contexto del Modelo.

MCP es un estándar abierto que define cómo se comunican los modelos de IA con los sistemas externos. Se puede considerar como una API diseñada específicamente para asistentes de IA.

Si una API permite que dos programas informáticos intercambien datos, MCP permite que un modelo de IA se comunique con su sistema. Esto abre un sinfín de posibilidades.

Podrías crear un servidor MCP que permita a ChatGPT leer archivos desde tu máquina local, o uno que llame a las API internas de tu empresa para obtener datos. Incluso podrías exponer tus propias funciones de Python para que un modelo pueda utilizarlas como herramientas.

MCP hace que esta comunicación sea estructurada, segura y extensible. Se basa en tecnologías web conocidas, como Server-Sent Events (SSE), que permiten al servidor enviar flujos de datos en tiempo real al cliente.

Configurando su entorno
Para seguir este ejemplo, necesitarás Python versión 3.9 o superior. Puedes encontrar el código en este repositorio .

# Entonro virtul 

python3 -m venv env crea un entorno virtual de Python llamado env.

Paso a paso:

python3
Usa Python 3.
-m venv
Ejecuta el módulo integrado venv, que sirve para crear entornos virtuales.
env
Es el nombre de la carpeta donde se creará el entorno virtual.

Resultado:

python3 -m venv env

crea una carpeta así:

env/

Dentro quedan una copia/estructura aislada de Python y pip.

Después normalmente lo activas así:

source env/bin/activate

Y cuando esté activo, instalas paquetes sin afectar el Python global:

pip install requests

Para salir:

deactivate



Usaremos una biblioteca llamada FastMCP que simplifica el proceso de creación de servidores MCP. Puedes instalarla usando pip:

pip install fastmcp requests

La requestsbiblioteca se utilizará más adelante en el ejemplo para realizar llamadas HTTP. Una vez instalada, ya puedes crear tu primer servidor MCP.

Creación del proyecto
Crea un nuevo archivo llamado server.pyy comienza importando los módulos necesarios:

import logging
import os
import random
import sys
import requests
from mcp.server.fastmcp import FastMCP
Esto es lo que hace cada uno:

El loggingmódulo registra la actividad de su servidor.

osSe utiliza para acceder a variables de entorno como los números de puerto.

randomnos ayudará a generar palabras aleatorias.

sysPermite que el script finalice correctamente en caso de errores.

requestsnos permite obtener datos en tiempo real de las API.

Y, por último, FastMCPconvierte nuestras funciones de Python en herramientas que pueden ser llamadas a través del protocolo MCP.

Configuración del registro
El registro de eventos te permite ver qué está haciendo tu servidor. Es útil durante el desarrollo y resulta vital al implementarlo en producción.

name = "demo-mcp-server"
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(name)
Esta configuración imprime mensajes de registro en la consola en un formato simple que muestra el nombre del servidor, el nivel de registro y el mensaje. Cada vez que se ejecuta una herramienta, aparecerá un mensaje en los registros como por ejemplo:

demo-mcp-server - INFO - Tool called: add(3, 5)
Creación del servidor MCP
A continuación, crearemos la instancia del servidor que alojará nuestras herramientas.

port = int(os.environ.get('PORT', 8080))
mcp = FastMCP(name, logger=logger, port=port)
El servidor se ejecutará en el puerto especificado por la variable de entorno PORT. Si dicha variable no está configurada, se utilizará el puerto 8080 por defecto. El FastMCPobjeto ahora representa su servidor MCP en ejecución.

Herramientas de definición
Cada función que decores @mcp.tool()se convierte en una herramienta accesible que los clientes pueden usar. Comencemos con un ejemplo sencillo: una herramienta de suma.

Ejemplo 1: Sumar dos números
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    logger.info(f"Tool called: add({a}, {b})")
    return a + b
Esta herramienta toma dos números, registra la llamada y devuelve su suma. Al llamar, add(3, 5)se devolverá 8.

Aunque es sencillo, esto muestra la estructura básica de cada herramienta MCP: parámetros de entrada, una instrucción de registro y un valor de retorno.

Ejemplo 2: Devolver una palabra secreta aleatoria
Vamos a crear otra herramienta que devuelva una palabra aleatoria de una lista pequeña.

@mcp.tool()
def get_secret_word() -> str:
    """Get a random secret word"""
    logger.info("Tool called: get_secret_word()")
    return random.choice(["apple", "banana", "cherry"])
Al llamar a esta función, se selecciona aleatoriamente una de las tres palabras. Cada vez que la llames, podrías obtener un resultado diferente. Esta función demuestra cómo las herramientas de MCP pueden usar lógica o aleatoriedad, al igual que cualquier función de Python.

Ejemplo 3: Obtención de datos meteorológicos
Ahora vamos a crear algo más práctico. Crearemos una herramienta que obtenga datos meteorológicos en tiempo real de la web utilizando la requestsbiblioteca.

@mcp.tool()
def get_current_weather(city: str) -> str:
    """Get current weather for a city"""
    logger.info(f"Tool called: get_current_weather({city})")

try:
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}", timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return f"Error fetching weather data: {str(e)}"
Esta herramienta acepta el nombre de una ciudad, envía una solicitud al servicio meteorológico público wttr.iny devuelve el informe meteorológico en formato de texto. Si se produce algún problema, como un tiempo de espera de red o un nombre de ciudad inválido, la función registra un error y devuelve un mensaje descriptivo.

Al llamar, get_current_weather("London")se imprimirá un breve resumen meteorológico para esa ciudad.

Ejecutando el servidor
Una vez definidas todas tus herramientas, puedes iniciar el servidor. Agrega el siguiente código al final de tu archivo:

if __name__ == "__main__":
    logger.info(f"Starting MCP Server on port {port}...")
    try:
        mcp.run(transport="sse")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("Server terminated")
Este bloque inicia el servidor utilizando el método de transporte Server-Sent Events (SEA). Si algo falla, registra el error y se apaga correctamente.

Ahora puedes ejecutar el servidor desde tu terminal:

python server.py
Si todo funciona correctamente, verás:

demo-mcp-server - INFO - Starting MCP Server on port 8080...
Su servidor MCP ya está activo y listo para aceptar solicitudes.

Probando las herramientas
Para probar tus herramientas, necesitas un cliente compatible con MCP, como ChatGPT con funciones para desarrolladores u otra aplicación que admita el protocolo. Una vez conectado, el cliente mostrará las herramientas disponibles.

Por ejemplo, puedes enviar una solicitud como esta:

{
  "tool": "add",
  "args": [5, 7]
}
El servidor responderá con:

{
  "result": 12
}
Lo mismo se aplica a las demás herramientas, como get_secret_wordo get_current_weather.

Si desea probar el servidor directamente sin el cliente MCP, aún puede enviar solicitudes HTTP manualmente (aunque esto omite la lógica completa del protocolo).

Por ejemplo, para probar tu herramienta meteorológica, puedes enviar una simple solicitud GET:

curl http://localhost:8080/tool/get_current_weather?city=London
o en Python:

import requests
response = requests.get("http://localhost:8080/tool/get_current_weather", params={"city": "London"})
print(response.text)
Esto no utilizará la estructura MCP (como en ssela transmisión en directo), pero es una comprobación rápida de que tu servidor funciona correctamente.

Implementación de su servidor MCP en Sevalla
Puedes ejecutar este servidor localmente para desarrollo. Pero si quieres usarlo en aplicaciones de producción, tienes que implementarlo en un servidor.

Puedes elegir cualquier proveedor de nube, como AWS, Heroku u otros, para configurar este proyecto. Pero yo usaré Sevalla.

Sevalla es un proveedor de plataforma como servicio (PaaS) moderno y basado en el uso. Ofrece alojamiento de aplicaciones, bases de datos, almacenamiento de objetos y alojamiento de sitios estáticos para sus proyectos.

Utilizo Sevalla para el alojamiento web por dos razones:

Todas las plataformas cobran por crear un recurso en la nube. Sevalla incluye un crédito de 50 dólares, por lo que no incurriremos en ningún coste en este ejemplo.

Sevalla dispone de una plantilla para el servidor Python MCP , lo que simplifica la instalación y configuración manual de cada recurso que necesite para la instalación.

Inicia sesión en Sevalla y haz clic en Plantillas. Verás que Python MCP Server es una de las plantillas.

Plantillas de Sevalla

Haz clic en la plantilla “Servidor Python MCP”. Verás los recursos necesarios para aprovisionar la aplicación. Haz clic en “Implementar plantilla”.

Recursos del servidor MCP de Python

Puedes ver cómo se está aprovisionando el recurso. Si la implementación no se inicia automáticamente, haz clic en "Implementar ahora".

Aprovisionamiento de recursos del servidor MCP de Python

Espere unos minutos. Una vez que la implementación haya finalizado, verá una marca de verificación verde.

Implementación de servidor MCP con Python

Una vez finalizada la implementación, haga clic en "Visitar la aplicación". Obtendrá una URL en la nube, por ejemplo, https://python-mcp-server-rlfdk.sevalla.app . Utilice esta URL como URL base en lugar de la URL localhost:3000.

Ahora dispone de un servidor MCP de nivel de producción funcionando en la nube. Puede integrarlo en cualquier aplicación para obtener datos para nuestras aplicaciones LLM.

¿Por qué crear tu propio servidor MCP?
Crear un servidor MCP te brinda control y flexibilidad.

Puedes conectar modelos de IA directamente a tus bases de datos o sistemas internos, automatizar acciones repetitivas y decidir exactamente a qué datos puede acceder un modelo de IA.

También te permite experimentar rápidamente. Puedes empezar con herramientas sencillas y luego ir ampliando a flujos de trabajo más complejos.

Al crear tu propio servidor MCP, no solo estás escribiendo código, sino que también estás definiendo cómo los sistemas inteligentes interactúan con el mundo real a través de tu lógica y tus datos.

Ampliación del servidor
Una vez que domines lo básico, es fácil ampliar tu servidor. Puedes añadir herramientas para leer y escribir archivos, consultar bases de datos, interactuar con API como GitHub o Slack, o monitorizar tu sistema. Cada nueva función se convierte en una herramienta más que tu IA puede utilizar.

Este enfoque modular permite construir un ecosistema completo de herramientas con inteligencia artificial, cada una de las cuales realiza una tarea específica, pero que trabajan juntas a través de la misma interfaz MCP.

Conclusión
En este tutorial, aprendiste a crear un servidor MCP en Python usando la biblioteca FastMCP. Configuraste el registro de eventos, configuraste un servidor, definiste varias herramientas y aprendiste a ejecutarlo y probarlo. También viste lo fácil que es para estas herramientas acceder a funcionalidades reales, como obtener datos meteorológicos en tiempo real o realizar cálculos básicos.

Esta estructura es sencilla pero potente. Con tan solo unas pocas líneas de código Python, puedes crear conexiones entre tus sistemas y modelos inteligentes. El Protocolo de Contexto de Modelos representa un paso hacia sistemas de IA capaces de comprender e interactuar de verdad con datos y acciones del mundo real.

Espero que hayas disfrutado de este artículo. Suscríbete a mi boletín gratuito TuringTalks.ai para acceder a más tutoriales prácticos sobre IA. También puedes visitar mi sitio web .