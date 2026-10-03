# historial.py
# Semana 5: pila para deshacer acciones (Comportamiento LIFO)

# 1. Definimos la pila como una lista vacía
pila_historial = []

def registrar_accion(tipo_accion, datos):
    """
    Operación PUSH: Agrega una nueva acción a la cima (final) de la pila (O(1)).
    'datos' es un diccionario que guarda lo necesario para poder revertir la acción.
    """
    accion = {
        "tipo": tipo_accion,
        "datos": datos
    }
    pila_historial.append(accion)
    print(f"[Historial] Acción '{tipo_accion}' apilada.")

def deshacer_accion(inventario_nyx):
    """
    Operación POP: Quita y revierte la última acción realizada (O(1)).
    """
    # Evitamos el error "Stack Underflow" validando si la pila está vacía
    if len(pila_historial) == 0:
        print("\n¡Nada que deshacer! El historial está vacío.")
        return

    # Extraemos la ÚLTIMA acción que ingresó (Regla LIFO)
    ultima_accion = pila_historial.pop()
    tipo = ultima_accion["tipo"]
    datos = ultima_accion["datos"]

    print("\n--- Deshaciendo acción ---")

    # Mecánica 1: Revertir la recolección de un objeto
    if tipo == "recoger":
        item_recogido = datos["item"]
        if item_recogido in inventario_nyx:
            inventario_nyx.remove(item_recogido)
            print(f"Deshecho: Perdiste '{item_recogido}'.")

    # Mecánica 2: Revertir haber botado todo el inventario
    elif tipo == "tirar_todo":
        items_perdidos = datos["inventario_previo"]
        inventario_nyx.extend(items_perdidos)
        print(f"Deshecho: Recuperaste todos los objetos que tiraste.")

# Mecánica 3: Revertir un crafteo
    elif tipo == "craftear":
        item_creado = datos["item_creado"]
        ingredientes_gastados = datos["ingredientes_gastados"]
        
        # Validación antiexploit: verificamos si el jugador aún tiene el ítem
        if item_creado in inventario_nyx:
            # 1. Le quitamos la poción creada
            inventario_nyx.remove(item_creado)
            
            # 2. Le devolvemos los ingredientes exactos que usó
            for ingrediente, cantidad in ingredientes_gastados.items():
                for _ in range(cantidad):
                    inventario_nyx.append(ingrediente)
                    
            print(f"Deshecho: El objeto '{item_creado}' fue desarmado. Recuperaste tus ingredientes.")
        else:
            # Si ya se lo tomó o lo botó, el crafteo no se puede revertir
            print(f"Error: Ya no tienes '{item_creado}' en tu inventario. No puedes recuperar los materiales de un objeto que ya consumiste.")
            
    print("-----------------------------------")