# inventario.py
# Semana 3: lista de objetos del jugador

import historial # NUEVO: Conectamos el inventario con la Pila de historial

def Add_item_to_inventory(inventory, item, max_capacity):
    if len(inventory) >= max_capacity:
        print("Inventory is full! Cannot add more items.")
        return
    inventory.append(item)
    print(f"{item} has been added to your inventory.")
    
    # NUEVO: Registramos la acción (O(1)) en la Pila
    historial.registrar_accion("recoger", {"item": item})
    
    return inventory

def use_item(inventory, Nyx, items, Gods):
    if not inventory:
        print("Your inventory is empty!")
        return
    print("\nInventory:")
    for idx, item in enumerate(inventory, 1):
        print(f"{idx}. {item}")
    choice = input("Select an item to use (or type 'cancel' to go back): ")
    if choice.lower() == 'cancel':
        return
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(inventory):
            item = inventory[choice_idx]
            print(f"You used {item}!")
            if item in items:
                effect = items[item]["effect"]
                value = items[item]["value"]
                if effect == "heal":
                    Nyx["health"] += value
                    print(f"Nyx healed for {value} health! Current Health: {Nyx['health']}")
                elif effect == "restore_mp":
                    Nyx["mp"] += value
                    print(f"Nyx restored {value} MP! Current MP: {Nyx['mp']}")
                elif effect == "buff":
                    Gods[Nyx["ally_god"]]["damage"] += value
                    print(f"Nyx's attack power increased by {value}! Current Damage: {Gods[Nyx['ally_god']]['damage']}")
            inventory.pop(choice_idx)
            # Nota: Usar un objeto no se registra en el historial por diseño.
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def throw_item(inventory):
    if not inventory:
        print("Your inventory is empty!")
        return
        
    # NUEVO: Hacemos una copia exacta del inventario y la apilamos ANTES de borrarlo
    historial.registrar_accion("tirar_todo", {"inventario_previo": inventory.copy()})
    
    print("You throw all items in your inventory away!")
    inventory.clear()