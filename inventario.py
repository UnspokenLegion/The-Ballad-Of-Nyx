# inventario.py
# Semana 3: lista de objetos del jugador

def Add_item_to_inventory(inventory, item, max_capacity):
    if len(inventory) >= max_capacity:
        print("Inventory is full! Cannot add more items.")
        return
    inventory.append(item)
    print(f"{item} has been added to your inventory.")
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
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def throw_item(inventory):
    if not inventory:
        print("Your inventory is empty!")
        return
    print("You throw all items in your inventory away!")
    inventory.clear()