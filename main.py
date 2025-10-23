import sys
from whatsapp_parser import agrupar_mensajes_generator
from stats import contar_por_remitente_from_generator, top_n
from dates import obtener_rango_fecha

def mostrar_resultados(conteo_usuarios, etiqueta, tipo):
    if not conteo_usuarios:
        print("No se encontraron mensajes en el período seleccionado.")
        return
    usuarios_ordenados = sorted(conteo_usuarios.items(), key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in usuarios_ordenados) if usuarios_ordenados else 0
    top_20 = usuarios_ordenados[:20]

    if tipo == "todos":
        print("\n🏆 Top 20 personas que más han hablado en todos los tiempos:")
    elif tipo == "mes":
        print(f"\n📅 Top 20 personas que más hablaron en {etiqueta}:")
    elif tipo == "año":
        print(f"\n📆 Top 20 personas que más hablaron en el año {etiqueta}:")

    for i, (usuario, mensajes) in enumerate(top_20, start=1):
        porcentaje = (mensajes / total) * 100 if total else 0
        medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        print(f"{medalla} {usuario}: {mensajes} mensajes ({porcentaje:.1f}%)")

def mostrar_menos_hablador(conteo_usuarios, etiqueta):
    if not conteo_usuarios:
        print("No se encontraron mensajes en el período seleccionado.")
        return
    usuarios_ordenados = sorted(conteo_usuarios.items(), key=lambda x: x[1])
    minimo = usuarios_ordenados[0][1]
    menos_habladores = [(u, c) for u, c in usuarios_ordenados if c == minimo]
    if len(menos_habladores) == 1:
        usuario, cuenta = menos_habladores[0]
        print(f"\n🔇 Menos hablador en {etiqueta}: {usuario} con {cuenta} mensajes")
    else:
        print(f"\n🔇 Empate - menos habladores en {etiqueta} ({minimo} mensajes):")
        for usuario, cuenta in menos_habladores:
            print(f" - {usuario}")

# --- Menú principal ---
def mostrar_menu():
    print("\n--- Análisis de WhatsApp ---")
    print("1. Top de todos los tiempos")
    print("2. Top del mes pasado")
    print("3. Top del mes actual")
    print("4. Top del año actual")
    print("5. Top del año pasado")
    print("6. Menos hablador (todos los tiempos)")
    print("7. Menos hablador (mes pasado)")
    print("8. Menos hablador (mes actual)")
    print("9. Menos hablador (año actual)")
    print("10. Menos hablador (año pasado)")
    print("11. Salir")

def main():
    archivo = "chat.txt"
    try:
        open(archivo, 'r', encoding='utf-8').close()
    except FileNotFoundError:
        print(f"No se encontró el archivo de chat: {archivo}")
        sys.exit(1)

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-11): ")
        # Validar entrada: debe ser un número entre 1 y 11
        if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 11:
            print("Opción no válida. Intenta de nuevo.")
            continue

        if opcion == "1":
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes)
            mostrar_resultados(conteo, "todos los tiempos", "todos")
        elif opcion == "2":
            inicio, fin, nombre = obtener_rango_fecha('mes_anterior')
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes, inicio, fin)
            mostrar_resultados(conteo, nombre, "mes")
        elif opcion == "3":
            inicio, fin, nombre = obtener_rango_fecha('mes_actual')
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes, inicio, fin)
            mostrar_resultados(conteo, nombre, "mes")
        elif opcion == "4":
            inicio, fin, nombre = obtener_rango_fecha('año_actual')
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes, inicio, fin)
            mostrar_resultados(conteo, nombre, "año")
        elif opcion == "5":
            inicio, fin, nombre = obtener_rango_fecha('año_anterior')
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes, inicio, fin)
            mostrar_resultados(conteo, nombre, "año")
        elif opcion == "6":
            # Menos hablador: todos los tiempos
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes)
            mostrar_menos_hablador(conteo, "todos los tiempos")
        elif opcion == "7":
            inicio, fin, nombre = obtener_rango_fecha('mes_anterior')
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes, inicio, fin)
            mostrar_menos_hablador(conteo, nombre)
        elif opcion == "8":
            inicio, fin, nombre = obtener_rango_fecha('mes_actual')
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes, inicio, fin)
            mostrar_menos_hablador(conteo, nombre)
        elif opcion == "9":
            inicio, fin, nombre = obtener_rango_fecha('año_actual')
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes, inicio, fin)
            mostrar_menos_hablador(conteo, nombre)
        elif opcion == "10":
            inicio, fin, nombre = obtener_rango_fecha('año_anterior')
            with open(archivo, 'r', encoding='utf-8') as f:
                mensajes = agrupar_mensajes_generator(f)
                conteo = contar_por_remitente_from_generator(mensajes, inicio, fin)
            mostrar_menos_hablador(conteo, nombre)
        elif opcion == "11":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
