"""
Módulo: historial.py
Objetivo: Implementar una estructura de datos tipo Pila (Stack) con comportamiento LIFO.
Cumple con el requisito de la Semana 5 de la asignatura CS2001.
Gestiona el historial de acciones y el módulo de retroceso mediante operaciones eficientes.
"""

# 1. Definimos la pila como una lista vacía
pila_historial = []

def registrar_accion(tipo_accion, datos):
    """
    Operación PUSH: Agrega una nueva acción a la cima (final) de la pila (O(1)).
    """
    accion = {
        "tipo": tipo_accion,
        "datos": datos
    }
    pila_historial.append(accion)
    print(f"[Historial] Acción '{tipo_accion}' apilada.")

def consultar_ultima_accion():
    """
    Operación PEEK: Consulta la última acción sin sacarla de la pila (O(1)).
    Requisito obligatorio del Checkpoint 2.
    """
    if len(pila_historial) == 0:
        print("\nEl historial está vacío.")
        return None
    
    ultima_accion = pila_historial[-1]
    print(f"\n[Peek] La última acción registrada es: {ultima_accion['tipo']}")
    return ultima_accion

def mostrar_historial_completo():
    """
    Imprime la pila desde la cima (más reciente) hasta la base (más antigua).
    Requisito obligatorio del Checkpoint 2.
    """
    if len(pila_historial) == 0:
        print("\nEl historial está vacío.")
        return
        
    print("\n--- Historial de Acciones (Más reciente a más antigua) ---")
    # reversed() itera la lista de atrás hacia adelante sin alterar O(1) de la estructura base
    for idx, accion in enumerate(reversed(pila_historial), 1):
        print(f"{idx}. Acción: {accion['tipo']} | Datos: {accion['datos']}")
    print("----------------------------------------------------------")

def contar_acciones_de_tipo(tipo_buscado):
    """
    Adaptación de Guía 5 (Requisito 1/2). Cuenta cuántas veces se hizo una acción.
    """
    cantidad = sum(1 for accion in pila_historial if accion["tipo"] == tipo_buscado)
    print(f"\nHas realizado la acción '{tipo_buscado}' un total de {cantidad} veces.")
    return cantidad

def deshacer_multiples(cantidad, inventario_nyx):
    """
    Adaptación de Guía 5 (Requisito 2/2). Deshace varias acciones de un solo golpe.
    """
    if len(pila_historial) == 0:
        print("\n¡Nada que deshacer! El historial está vacío.")
        return
    
    acciones_a_deshacer = min(cantidad, len(pila_historial))
    print(f"\nIniciando retroceso múltiple de {acciones_a_deshacer} acciones...")
    
    for _ in range(acciones_a_deshacer):
        sala_devuelta = deshacer_accion(inventario_nyx)
        # Si una de las acciones fue moverse, devolvemos la sala para que main.py actualice la posición
        if sala_devuelta:
            return sala_devuelta
    return None

def deshacer_accion(inventario_nyx):
    """
    Operación POP: Quita y revierte la última acción realizada (O(1)).
    """
    if len(pila_historial) == 0:
        print("\n¡Nada que deshacer! El historial está vacío.")
        return None

    ultima_accion = pila_historial.pop()
    tipo = ultima_accion["tipo"]
    datos = ultima_accion["datos"]

    print("\n--- Deshaciendo acción ---")

    # NUEVA Mecánica: Revertir movimiento (Backtracking requerido por Checkpoint 2)
    if tipo == "moverse":
        sala_anterior = datos["sala_origen"]
        print(f"Deshaces el movimiento: vuelves a {sala_anterior}")
        return sala_anterior # Retornamos la sala para que main.py actualice a Nyx

    # Mecánica 1: Revertir la recolección de un objeto
    elif tipo == "recoger":
        item_recogido = datos["item"]
        if item_recogido in inventario_nyx:
            inventario_nyx.remove(item_recogido)
            print(f"Deshecho: Perdiste '{item_recogido}'.")

    # Mecánica 2: Revertir haber botado todo el inventario
    elif tipo == "tirar_todo":
        items_perdidos = datos["inventario_previo"]
        inventario_nyx.extend(items_perdidos)
        print("Deshecho: Recuperaste todos los objetos que tiraste.")

    # Mecánica 3: Revertir un crafteo
    elif tipo == "craftear":
        item_creado = datos["item_creado"]
        ingredientes_gastados = datos["ingredientes_gastados"]
        
        if item_creado in inventario_nyx:
            inventario_nyx.remove(item_creado)
            for ingrediente, cantidad in ingredientes_gastados.items():
                for _ in range(cantidad):
                    inventario_nyx.append(ingrediente)
            print(f"Deshecho: El objeto '{item_creado}' fue desarmado. Recuperaste tus ingredientes.")
        else:
            print(f"Error: Ya no tienes '{item_creado}' en tu inventario.")
            
    print("-----------------------------------")
    return None