import re
from datetime import datetime

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

def agrupar_mensajes_generator(line_iterable):
    """Generador que recibe un iterable de líneas (por ejemplo, un file handle)
    y produce tuplas (fecha, remitente, texto) por mensaje. Maneja mensajes
    multilínea sin cargar todo en memoria.
    """
    inicio_re = re.compile(r'^\s*\d{1,2}/\d{1,2}/\d{2,4},\s*')

    current = None
    for raw in line_iterable:
        linea = raw.rstrip('\n')
        if inicio_re.match(linea):
            if current:
                fecha = parse_datetime(current[0])
                texto = '\n'.join(current[2]).strip()
                yield (fecha, current[1], texto)
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
                # Línea suelta antes del primer encabezado
                yield (None, None, linea.strip())
    if current:
        fecha = parse_datetime(current[0])
        texto = '\n'.join(current[2]).strip()
        yield (fecha, current[1], texto)
