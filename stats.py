from collections import defaultdict

def contar_por_remitente_from_generator(mensajes_iter, desde=None, hasta=None):
    conteo = defaultdict(int)
    for fecha, remitente, _ in mensajes_iter:
        if remitente is None:
            continue
        if fecha:
            if desde and fecha < desde:
                continue
            if hasta and fecha > hasta:
                continue
        conteo[remitente] += 1
    return conteo

def top_n(conteo_usuarios, n=20):
    usuarios_ordenados = sorted(conteo_usuarios.items(), key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in usuarios_ordenados) if usuarios_ordenados else 0
    return usuarios_ordenados[:n], total
