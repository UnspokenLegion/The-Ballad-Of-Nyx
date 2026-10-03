# eventos.py
# Semana 6: cola de turnos y eventos (Comportamiento estricto FIFO)

from collections import deque

# 1. Definimos la cola usando 'deque' para garantizar operaciones O(1) en ambos extremos
cola_turnos = deque()

def agregar_turno(entidad):
    """
    Operación ENQUEUE: Agrega un personaje o enemigo al final de la fila (O(1)).
    """
    cola_turnos.append(entidad)
    print(f"[Sistema] {entidad.capitalize()} ha entrado a la cola de turnos.")

def siguiente_turno():
    """
    Operación DEQUEUE: Quita y devuelve a la entidad que está al frente de la fila (O(1)).
    """
    # Operación IS_EMPTY: Validamos si la cola está vacía
    if len(cola_turnos) == 0: 
        return None
    
    # Extraemos al PRIMER elemento que ingresó (Regla FIFO mediante popleft)
    turno_actual = cola_turnos.popleft()
    return turno_actual

def ver_proximo():
    """
    Operación FRONT / PEEK: Mira quién es el siguiente atacante sin sacarlo de la cola (O(1)).
    """
    if len(cola_turnos) > 0:
        return cola_turnos[0]
    return None
    
def limpiar_turnos():
    """
    Vacía la cola de eventos al terminar la fase de combate.
    """
    cola_turnos.clear()