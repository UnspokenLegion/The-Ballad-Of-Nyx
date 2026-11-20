"""
Módulo: estado_mundo.py
Proyecto: Aventura Algorítmica - The Ballad of Nyx
Objetivo: Gestionar el estado dinámico del mundo mediante un diccionario (Tabla Hash)
          con acceso promedio O(1), operaciones CRUD seguras y funciones de resumen/filtro.
"""

# Diccionario principal del estado del mundo.
# Claves únicas e inmutables (str y tuple, nunca list):
# - ("sala", nombre_sala): "visitada" | "sin_visitar" | "bloqueada"
# - ("puerta", origen, destino): "abierta" | "bloqueada"
# - ("jefe", nombre_jefe): "vivo" | "derrotado"
# - "nyx_ubicacion": nombre de la sala actual
# - "nyx_dios_aliado": nombre del dios aliado
estado_mundo = {}


# ==============================================================================
# 1. INICIALIZACIÓN Y OPERACIONES OBLIGATORIAS (CRUD SEGURO - O(1) promedio)
# ==============================================================================

def inicializar_mundo(salas_iniciales, sala_inicio="Cueva Ancestral"):
    """
    Inicializa el diccionario del mundo con las salas generadas y los jefes base.
    """
    estado_mundo.clear()
    estado_mundo["nyx_ubicacion"] = sala_inicio
    estado_mundo["nyx_dios_aliado"] = "Ninguno"

    for sala in salas_iniciales:
        estado_mundo[("sala", sala)] = "visitada" if sala == sala_inicio else "sin_visitar"

    # Jefes principales del universo de Nyx
    estado_mundo[("jefe", "fire_fiend")] = "vivo"
    estado_mundo[("jefe", "mind_flayer")] = "vivo"


def consultar_estado(clave, valor_por_defecto="desconocido"):
    """
    CONSULTA SEGURA con .get() -> O(1) promedio.
    Evita que ocurra un KeyError si la clave no existe.
    """
    return estado_mundo.get(clave, valor_por_defecto)


def insertar_o_actualizar_estado(clave, valor):
    """
    INSERCIÓN y ACTUALIZACIÓN -> O(1) promedio.
    Valida que la clave sea inmutable (str o tuple, nunca list).
    """
    if isinstance(clave, list):
        raise TypeError("Las claves del diccionario no pueden ser listas; usa texto o tupla.")
    estado_mundo[clave] = valor


def eliminar_estado(clave):
    """
    ELIMINACIÓN SEGURA con .pop(clave, None) -> O(1) promedio.
    Devuelve el valor eliminado o None si la clave no existía (nunca lanza KeyError).
    """
    return estado_mundo.pop(clave, None)

# ==============================================================================
# 2. FUNCIONES PROPIAS DE RESUMEN Y FILTRO
# ==============================================================================

def resumir_progreso_mundo():
    """
    Función propia 1 (Resumen): Calcula y muestra el progreso global de la partida
    (salas exploradas, salas pendientes, jefes derrotados y ubicación actual de Nyx).
    Complejidad: O(n) sobre las claves del diccionario.
    """
    salas_visitadas = 0
    salas_totales = 0
    jefes_derrotados = 0
    jefes_totales = 0

    for clave, valor in estado_mundo.items():
        if isinstance(clave, tuple) and len(clave) == 2:
            tipo, _ = clave
            if tipo == "sala":
                salas_totales += 1
                if valor == "visitada":
                    salas_visitadas += 1
            elif tipo == "jefe":
                jefes_totales += 1
                if valor == "derrotado":
                    jefes_derrotados += 1

    resumen = {
        "ubicacion_actual": consultar_estado("nyx_ubicacion", "Campamento Base"),
        "dios_aliado": consultar_estado("nyx_dios_aliado", "Ninguno"),
        "salas_visitadas": salas_visitadas,
        "salas_totales": salas_totales,
        "jefes_derrotados": jefes_derrotados,
        "jefes_totales": jefes_totales
    }

    print("\n--- [Estado del Mundo] RESUMEN GLOBAL ---")
    print(f"  Ubicación actual de Nyx : {resumen['ubicacion_actual']}")
    print(f"  Dios aliado             : {resumen['dios_aliado']}")
    print(f"  Salas exploradas        : {resumen['salas_visitadas']} / {resumen['salas_totales']}")
    print(f"  Jefes derrotados        : {resumen['jefes_derrotados']} / {resumen['jefes_totales']}")
    print("-----------------------------------------")
    return resumen


def filtrar_por_estado(tipo_entidad, estado_buscado):
    """
    Función propia 2 (Filtro): Filtra salas, jefes o puertas según su estado actual.
    Ejemplo: filtrar_por_estado("sala", "sin_visitar") o filtrar_por_estado("jefe", "vivo").
    Complejidad: O(n) sobre las claves del diccionario.
    """
    resultados = []
    for clave, valor in estado_mundo.items():
        if isinstance(clave, tuple) and len(clave) >= 2:
            if clave[0] == tipo_entidad and valor == estado_buscado:
                # Si es tupla de 2 elementos devuelve el nombre; si es de 3 (puerta), devuelve el par
                resultados.append(clave[1] if len(clave) == 2 else (clave[1], clave[2]))
    return resultados