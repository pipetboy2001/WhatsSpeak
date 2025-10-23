from datetime import datetime, timedelta

meses_esp = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def obtener_rango_fecha(tipo_rango):
    hoy = datetime.today()
    if tipo_rango == 'mes_actual':
        inicio = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fin = hoy.replace(hour=23, minute=59, second=59, microsecond=999999)
        nombre = meses_esp[hoy.month]
    elif tipo_rango == 'mes_anterior':
        primero_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        mes_anterior = primero_mes - timedelta(days=1)
        inicio = mes_anterior.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fin = mes_anterior.replace(hour=23, minute=59, second=59, microsecond=999999)
        nombre = meses_esp[mes_anterior.month]
    elif tipo_rango == 'año_actual':
        inicio = hoy.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        fin = hoy.replace(hour=23, minute=59, second=59, microsecond=999999)
        nombre = str(hoy.year)
    elif tipo_rango == 'año_anterior':
        inicio = hoy.replace(year=hoy.year - 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        fin = hoy.replace(year=hoy.year - 1, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        nombre = str(hoy.year - 1)
    else:
        inicio, fin, nombre = (None, None, '')
    return inicio, fin, nombre
