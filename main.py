import re
from collections import defaultdict
from datetime import datetime, timedelta

# Función para leer el archivo de WhatsApp
def leer_archivo(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        return f.readlines()

# Función para procesar las líneas y contar los mensajes por usuario
def procesar_mensajes(lineas):
    conteo_usuarios = defaultdict(int)
    formato_fecha = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})")  # Expresión regular para fechas
    
    for linea in lineas:
        # Verificar si la línea comienza con una fecha y hora válida
        if formato_fecha.match(linea):
            # Extraer el remitente del mensaje
            partes = linea.split(" - ", 1)
            if len(partes) > 1:
                _, mensaje = partes
                if ": " in mensaje:  # Asegurarse de que el mensaje tenga un remitente válido
                    remitente = mensaje.split(": ")[0]
                    conteo_usuarios[remitente] += 1  # Aumentar el contador del remitente
    
    return conteo_usuarios

# Función para filtrar mensajes por un período específico (mes/año)
def filtrar_mensajes_por_fecha(lineas, desde, hasta):
    conteo_usuarios = defaultdict(int)
    formato_fecha = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})")
    
    for linea in lineas:
        coincidencia = formato_fecha.match(linea)
        if coincidencia:
            fecha_str = coincidencia.group(1)
            fecha = datetime.strptime(fecha_str, '%d/%m/%y')
            if desde <= fecha <= hasta:
                partes = linea.split(" - ", 1)
                if len(partes) > 1:
                    _, mensaje = partes
                    if ": " in mensaje:
                        remitente = mensaje.split(": ")[0]
                        conteo_usuarios[remitente] += 1

    return conteo_usuarios

# Función para obtener la fecha de inicio y fin para un rango de tiempo
def obtener_rango_fecha(tipo_rango):
    hoy = datetime.today()

    if tipo_rango == 'mes_actual':
        inicio = hoy.replace(day=1)
        fin = hoy
        mes_nombre = meses_esp[hoy.month]  # Usar el diccionario para obtener el nombre en español
    elif tipo_rango == 'mes_anterior':
        primer_dia_mes_actual = hoy.replace(day=1)
        mes_anterior = primer_dia_mes_actual - timedelta(days=1)
        inicio = mes_anterior.replace(day=1)
        fin = mes_anterior
        mes_nombre = meses_esp[mes_anterior.month]  # Usar el diccionario para obtener el nombre en español
    elif tipo_rango == 'año_actual':
        inicio = hoy.replace(month=1, day=1)
        fin = hoy
        mes_nombre = str(hoy.year)  # Año
    elif tipo_rango == 'año_anterior':
        inicio = hoy.replace(year=hoy.year - 1, month=1, day=1)
        fin = hoy.replace(year=hoy.year - 1, month=12, day=31)
        mes_nombre = str(hoy.year - 1)  # Año anterior

    return inicio, fin, mes_nombre

# Mapeo de meses a su nombre en español
meses_esp = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

# Función para mostrar los resultados del top 20
def mostrar_resultados(conteo_usuarios, mes_nombre, tipo_rango):
    if conteo_usuarios:
        # Ordenar usuarios por cantidad de mensajes (de mayor a menor)
        usuarios_ordenados = sorted(conteo_usuarios.items(), key=lambda x: x[1], reverse=True)
        
        # Limitar a un top 20 o mostrar menos si no hay tantos usuarios
        top_20 = usuarios_ordenados[:20]
        
        
        # Modificar el encabezado dependiendo de la opción
        if tipo_rango == "todos los tiempos":
            print(f"\nTop 20 personas que más han hablado en todos los tiempos:")
        elif tipo_rango == "mes":
            print(f"\nTop 20 personas que más han hablado en el mes {mes_nombre.capitalize()}:")
        elif tipo_rango == "año":
            print(f"\nTop 20 personas que más han hablado en el año {mes_nombre}:")
        
        for i, (usuario, mensajes) in enumerate(top_20, start=1):
            print(f"{i}. {usuario}: {mensajes} mensajes")
    else:
        print("No se encontraron mensajes en el período seleccionado.")

# Función para mostrar el menú
def mostrar_menu():
    print("\n--- Análisis de WhatsApp ---")
    print("1. Ver quién ha hablado más en todos los tiempos")
    print("2. Ver quién habló más el mes pasado")
    print("3. Ver quién ha hablado más este mes")
    print("4. Ver quién ha hablado más durante este año")
    print("5. Ver quién habló más el año pasado")
    print("6. Salir")

# Función principal para manejar el menú y ejecutar el análisis
def main():
    archivo = "chat.txt"  # Nombre del archivo de WhatsApp
    lineas = leer_archivo(archivo)

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-6): ")

        if opcion == "1":
            conteo_total = procesar_mensajes(lineas)
            mostrar_resultados(conteo_total, "todos los tiempos", "todos los tiempos")
        elif opcion == "2":
            inicio, fin, mes_nombre = obtener_rango_fecha('mes_anterior')
            conteo_mes_anterior = filtrar_mensajes_por_fecha(lineas, inicio, fin)
            mostrar_resultados(conteo_mes_anterior, mes_nombre, "mes")
        elif opcion == "3":
            inicio, fin, mes_nombre = obtener_rango_fecha('mes_actual')
            conteo_mes_actual = filtrar_mensajes_por_fecha(lineas, inicio, fin)
            mostrar_resultados(conteo_mes_actual, mes_nombre, "mes")
        elif opcion == "4":
            inicio, fin, mes_nombre = obtener_rango_fecha('año_actual')
            conteo_año_actual = filtrar_mensajes_por_fecha(lineas, inicio, fin)
            mostrar_resultados(conteo_año_actual, mes_nombre, "año")
        elif opcion == "5":
            inicio, fin, mes_nombre = obtener_rango_fecha('año_anterior')
            conteo_año_anterior = filtrar_mensajes_por_fecha(lineas, inicio, fin)
            mostrar_resultados(conteo_año_anterior, mes_nombre, "año")
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor selecciona una opción entre 1 y 6.")

if __name__ == "__main__":
    main()
