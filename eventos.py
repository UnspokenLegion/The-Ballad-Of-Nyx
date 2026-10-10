"""
Módulo: eventos.py
Objetivo: Implementar una estructura de datos tipo Cola (Queue) con comportamiento FIFO.
Cumple con el requisito de la Semana 6 de la asignatura CS2001.
Gestiona el procesamiento por turnos en combate y los eventos secuenciales del mapa.
"""

from collections import deque

# 1. Definimos la cola usando 'deque' para garantizar operaciones O(1) en ambos extremos
cola_turnos = deque()

def agregar_turno(entidad):
    """
    Operación ENQUEUE: Agrega un personaje, enemigo o evento al final de la fila (O(1)).
    """
    cola_turnos.append(entidad)
    # Ajustamos el print para que sea un poco más limpio y sirva tanto para enemigos como para eventos narrativos
    print(f"[Sistema] '{entidad}' ha entrado a la cola.")

def siguiente_turno():
    """
    Operación DEQUEUE: Quita y devuelve la entidad/evento que está al frente de la fila (O(1)).
    """
    # Operación IS_EMPTY: Validamos si la cola está vacía
    if len(cola_turnos) == 0: 
        return None
    
    # Extraemos al PRIMER elemento que ingresó (Regla FIFO mediante popleft)
    turno_actual = cola_turnos.popleft()
    return turno_actual

def ver_proximo():
    """
    Operación FRONT / PEEK: Mira quién es el siguiente sin sacarlo de la cola (O(1)).
    """
    if len(cola_turnos) > 0:
        return cola_turnos[0]
    return None
    
def limpiar_turnos():
    """
    Vacía la cola de eventos al terminar la fase de combate o exploración.
    """
    cola_turnos.clear()

def contar_eventos_de_tipo(entidad_buscada):
    """
    Adaptación 1: Cuenta cuántas veces aparece un evento o personaje específico
    en la cola actual. Utiliza el método nativo count().
    """
    cantidad = cola_turnos.count(entidad_buscada)
    print(f"\n[Cola] La entidad/evento '{entidad_buscada}' está {cantidad} vez/veces en la fila.")
    return cantidad

def invertir_cola():
    """
    Adaptación 2: Invierte el orden de la cola (O(n)).
    Ideal para mecánicas de "Emboscada" donde el orden de los turnos se voltea inesperadamente,
    o para alterar la secuencia narrativa de la mazmorra.
    """
    if len(cola_turnos) == 0:
        print("\nLa cola está vacía, no se puede invertir.")
        return
        
    cola_turnos.reverse()
    print("\n[Sistema] ¡Emboscada! El orden de la cola ha sido INVERTIDO.")