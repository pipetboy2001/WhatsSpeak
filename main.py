import re
from collections import defaultdict
from datetime import datetime, timedelta

# --- Helpers para parseo de fechas ruidosas de WhatsApp ---
def normalize_datetime_str(dt_str):
    s = dt_str
    s = s.replace('\u202f', ' ').replace('\xa0', ' ').replace('\u200b', '')
    s = re.sub(r'(?i)a\s*\.?\s*m\.?', 'AM', s)
    s = re.sub(r'(?i)p\s*\.?\s*m\.?', 'PM', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_datetime(dt_str):
    s = normalize_datetime_str(dt_str)
    formatos = [
        '%d/%m/%y, %I:%M %p',
        '%d/%m/%Y, %I:%M %p',
        '%d/%m/%y, %H:%M',
        '%d/%m/%Y, %H:%M',
    ]
    for fmt in formatos:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    return None

# --- Agrupador de mensajes (multilínea incluido) ---
def agrupar_mensajes(lineas):
    mensajes = []
    inicio_re = re.compile(r'^\s*\d{1,2}/\d{1,2}/\d{2,4},\s*')

    current = None
    for raw in lineas:
        linea = raw.rstrip('\n')
        if inicio_re.match(linea):
            if current:
                fecha = parse_datetime(current[0])
                texto = '\n'.join(current[2]).strip()
                mensajes.append((fecha, current[1], texto))
            if ' - ' in linea:
                datetime_part, rest = linea.split(' - ', 1)
            else:
                datetime_part, rest = linea, ''
            remitente, texto = (None, rest)
            if ': ' in rest:
                remitente, texto = rest.split(': ', 1)
            current = (datetime_part.strip(), remitente.strip() if remitente else None, [texto])
        else:
            if current:
                current[2].append(linea)
            else:
                mensajes.append((None, None, linea.strip()))
    if current:
        fecha = parse_datetime(current[0])
        texto = '\n'.join(current[2]).strip()
        mensajes.append((fecha, current[1], texto))
    return mensajes

# --- Conteo y filtrado ---
def contar_por_remitente(lineas, desde=None, hasta=None):
    mensajes = agrupar_mensajes(lineas)
    conteo = defaultdict(int)
    for fecha, remitente, _ in mensajes:
        if remitente is None:
            continue
        if fecha:
            if desde and fecha < desde:
                continue
            if hasta and fecha > hasta:
                continue
        conteo[remitente] += 1
    return conteo

# --- Fechas predefinidas ---
meses_esp = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def obtener_rango_fecha(tipo_rango):
    hoy = datetime.today()
    if tipo_rango == 'mes_actual':
        inicio = hoy.replace(day=1)
        fin = hoy
        nombre = meses_esp[hoy.month]
    elif tipo_rango == 'mes_anterior':
        primero_mes = hoy.replace(day=1)
        mes_anterior = primero_mes - timedelta(days=1)
        inicio = mes_anterior.replace(day=1)
        fin = mes_anterior
        nombre = meses_esp[mes_anterior.month]
    elif tipo_rango == 'año_actual':
        inicio = hoy.replace(month=1, day=1)
        fin = hoy
        nombre = str(hoy.year)
    elif tipo_rango == 'año_anterior':
        inicio = hoy.replace(year=hoy.year - 1, month=1, day=1)
        fin = hoy.replace(year=hoy.year - 1, month=12, day=31)
        nombre = str(hoy.year - 1)
    return inicio, fin, nombre

# --- Mostrar resultados con medallas 🥇🥈🥉 ---
def mostrar_resultados(conteo_usuarios, etiqueta, tipo):
    if not conteo_usuarios:
        print("No se encontraron mensajes en el período seleccionado.")
        return
    
    usuarios_ordenados = sorted(conteo_usuarios.items(), key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in usuarios_ordenados)
    top_20 = usuarios_ordenados[:20]

    if tipo == "todos":
        print("\n🏆 Top 20 personas que más han hablado en todos los tiempos:")
    elif tipo == "mes":
        print(f"\n📅 Top 20 personas que más hablaron en {etiqueta}:")
    elif tipo == "año":
        print(f"\n📆 Top 20 personas que más hablaron en el año {etiqueta}:")

    for i, (usuario, mensajes) in enumerate(top_20, start=1):
        porcentaje = (mensajes / total) * 100
        medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        print(f"{medalla} {usuario}: {mensajes} mensajes ({porcentaje:.1f}%)")

# --- Menú principal ---
def mostrar_menu():
    print("\n--- Análisis de WhatsApp ---")
    print("1. Top de todos los tiempos")
    print("2. Top del mes pasado")
    print("3. Top del mes actual")
    print("4. Top del año actual")
    print("5. Top del año pasado")
    print("6. Salir")

def main():
    archivo = "chat.txt"
    with open(archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-6): ")
        if opcion == "1":
            conteo = contar_por_remitente(lineas)
            mostrar_resultados(conteo, "todos los tiempos", "todos")
        elif opcion == "2":
            inicio, fin, nombre = obtener_rango_fecha('mes_anterior')
            conteo = contar_por_remitente(lineas, inicio, fin)
            mostrar_resultados(conteo, nombre, "mes")
        elif opcion == "3":
            inicio, fin, nombre = obtener_rango_fecha('mes_actual')
            conteo = contar_por_remitente(lineas, inicio, fin)
            mostrar_resultados(conteo, nombre, "mes")
        elif opcion == "4":
            inicio, fin, nombre = obtener_rango_fecha('año_actual')
            conteo = contar_por_remitente(lineas, inicio, fin)
            mostrar_resultados(conteo, nombre, "año")
        elif opcion == "5":
            inicio, fin, nombre = obtener_rango_fecha('año_anterior')
            conteo = contar_por_remitente(lineas, inicio, fin)
            mostrar_resultados(conteo, nombre, "año")
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
