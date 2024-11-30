# WhatsSpeak

**WhatsSpeak** es una herramienta de análisis de mensajes exportados desde WhatsApp. Permite obtener estadísticas detalladas sobre la cantidad de mensajes enviados por cada usuario durante diferentes períodos de tiempo, como el mes actual, el año o desde el inicio hasta el final. Este análisis es útil para conocer patrones de comunicación y el comportamiento de los participantes en un chat de WhatsApp.

## Características

-   Análisis de mensajes por usuario.
-   Soporte para rangos de tiempo personalizables: mes actual, año actual, todos los tiempos.
-   Visualización del top 20 de usuarios que más han hablado en el chat.
-   Resultados organizados por cantidad de mensajes enviados.

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instalados los siguientes programas:

-   Python 3.x
-   Librerías de Python necesarias (ver sección de instalación)

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto localmente:

1.  Clona el repositorio:
    
    `git clone https://link-to-project` 
    
2.  Entra al directorio del proyecto:
    
    `cd my-project` 
    
    
3.  Ejecuta el programa:
    
    `python main.py` 
    

### Archivos de entrada

El programa requiere un archivo de chat de WhatsApp exportado. Este archivo debe estar en formato de texto con el siguiente formato para cada mensaje:

`[DD/MM/AAAA, HH:MM] - Nombre del remitente: mensaje` 

## Uso

Una vez que el programa esté en ejecución, te presentará un menú interactivo donde podrás elegir entre las siguientes opciones:

1.  Ver quién ha hablado más en todos los tiempos.
2.  Ver quién habló más el mes pasado.
3.  Ver quién ha hablado más este mes.
4.  Ver quién ha hablado más durante este año.
5.  Ver quién habló más el año pasado.
6.  Salir.

## Ejemplos

### Obtener el top de mensajes por usuario


> Top 20 personas que más han hablado en el mes Octubre:
> 1. Usuario1: 150 mensajes
> 2. Usuario2: 120 mensajes ...

### Obtener estadísticas de mensajes en un período personalizado


> Top 20 personas que más han hablado en el año 2024:
> 1. UsuarioA: 500 mensajes
> 2. UsuarioB: 450 mensajes ...`

## FAQ

### ¿Cómo importo el archivo de chat de WhatsApp?

Solo necesitas colocar el archivo de chat exportado en el directorio raíz del proyecto y el programa lo leerá automáticamente al ejecutarse.

### ¿Puedo analizar chats de grupos grandes?

Sí, el programa es capaz de manejar chats con muchos mensajes y usuarios, aunque la velocidad de procesamiento puede depender del tamaño del archivo.