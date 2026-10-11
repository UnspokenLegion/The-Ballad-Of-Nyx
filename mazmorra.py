"""
Módulo: mazmorra.py
Objetivo: Implementar algoritmos recursivos (divide y conquista) para la generación de mapas.
Cumple con el requisito de la Semana 7 de la asignatura CS2001.
Contiene la generación base de salas y dos adaptaciones dinámicas (callejones y aleatoriedad).
"""
import random

# --- FUNCIÓN BASE ---
def generar_salas(sala_actual, profundidad, max_profundidad, conexiones, salas, nombres_disponibles):
    """
    Función recursiva base. Genera la mazmorra creando exactamente 2 salas hijas por nivel.
    Se detiene al alcanzar la profundidad máxima establecida (caso base).
    """
    salas.append(sala_actual)
    if profundidad >= max_profundidad:
        return
    for _ in range(2):
        if len(nombres_disponibles) > 0:
            hijo = nombres_disponibles.pop(0)
            conexiones.append((sala_actual, hijo))
            generar_salas(hijo, profundidad + 1, max_profundidad, conexiones, salas, nombres_disponibles)


# --- ADAPTACIÓN 1 (Basada en Ejercicio B: Marcar sin descendencia) ---
def generar_mazmorra_marcando_callejones(sala_actual, profundidad, max_profundidad, conexiones, salas, sin_salida, nombres_disponibles):
    """
    Adaptación 1: Identifica las salas que no tienen descendencia.
    Cuando la recursividad alcanza la profundidad máxima, registra la sala actual
    en la lista 'sin_salida' antes de detenerse.
    """
    salas.append(sala_actual)
    
    # CASO BASE: Si es la profundidad máxima, se marca como callejón sin salida
    if profundidad >= max_profundidad:
        sin_salida.append(sala_actual)
        return
        
    for _ in range(2):
        if len(nombres_disponibles) > 0:
            hijo = nombres_disponibles.pop(0)
            conexiones.append((sala_actual, hijo))
            generar_mazmorra_marcando_callejones(hijo, profundidad + 1, max_profundidad, conexiones, salas, sin_salida, nombres_disponibles)


# --- ADAPTACIÓN 2 (Basada en Reto D: Ramificación variable) ---
def generar_mazmorra_ramificacion_aleatoria(sala_actual, profundidad, max_profundidad, min_puertas, max_puertas, conexiones, salas, nombres_disponibles):
    """
    Adaptación 2: Genera un número aleatorio de caminos por habitación.
    Utiliza random.randint() para decidir cuántas puertas tendrá la sala actual,
    haciendo que el mapa sea asimétrico y dinámico.
    """
    salas.append(sala_actual)
    
    # CASO BASE
    if profundidad >= max_profundidad:
        return
        
    # CASO RECURSIVO: La cantidad de salas hijas es aleatoria
    puertas = random.randint(min_puertas, max_puertas)
    for _ in range(puertas):
        if len(nombres_disponibles) > 0:
            hijo = nombres_disponibles.pop(0)
            conexiones.append((sala_actual, hijo))
            generar_mazmorra_ramificacion_aleatoria(hijo, profundidad + 1, max_profundidad, min_puertas, max_puertas, conexiones, salas, nombres_disponibles)