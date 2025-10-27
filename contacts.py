import os
import csv
import re


def _normalize_name(s):
    if not s:
        return ''
    s = s.strip()
    # remover paréntesis y su contenido
    s = re.sub(r"\(.*?\)", "", s)
    # normalizar espacios y minusculas
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def _extract_phone_from_row(row):
    # Buscar columnas que contengan 'Phone' y 'Value' en su nombre
    for k, v in row.items():
        if k and 'phone' in k.lower() and 'value' in k.lower():
            if v and v.strip():
                # algunos teléfonos están separados por ':::' u otros separadores
                parts = re.split(r":::+|,|;", v)
                for p in parts:
                    p = p.strip()
                    if p:
                        return p
    return None


def _name_variants(row):
    # Generar variantes probables del nombre a partir de distintos campos
    fields = []
    for key in ('First Name', 'Middle Name', 'Last Name', 'Nickname', 'File As'):
        val = row.get(key)
        if val and val.strip():
            fields.append(val.strip())

    variants = set()
    # agregar combinaciones
    if fields:
        # raw joined
        joined = ' '.join(fields)
        variants.add(joined)
        # componentes individuales
        for f in fields:
            variants.add(f)
    # también intentar con la primera columna sin modificaciones
    first = row.get('First Name') or ''
    if first:
        variants.add(first)
    # limpiar y normalizar
    return {_normalize_name(v) for v in variants if v}


def load_contacts_from_env(default_csv='contact.csv'):
    """Cargar un mapeo de nombre_normalizado -> telefono a partir del CSV
    La ruta se toma de la variable de entorno CONTACT_CSV si existe,
    sino se usa `default_csv` en el directorio actual.
    """
    path = os.environ.get('CONTACT_CSV', default_csv)
    mapping = {}
    try:
        with open(path, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                phone = _extract_phone_from_row(row)
                if not phone:
                    continue
                for name in _name_variants(row):
                    if name and name not in mapping:
                        mapping[name] = phone
    except FileNotFoundError:
        # no existe archivo de contactos; devolvemos mapeo vacío
        return {}
    except Exception:
        return {}
    return mapping


def resolve_remitentes_generator(mensajes_gen, contacts_map):
    """Toma un generador de tuplas (fecha, remitente, texto) y reemplaza
    `remitente` por el número si el nombre aparece en contacts_map.
    La comparación es case-insensitive y normaliza paréntesis y espacios.
    """
    for fecha, remitente, texto in mensajes_gen:
        resolved = remitente
        if remitente:
            key = _normalize_name(remitente)
            if key in contacts_map:
                resolved = contacts_map[key]
        yield (fecha, resolved, texto)
