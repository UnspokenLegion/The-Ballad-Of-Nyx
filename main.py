import time

items = {
    "herbs": {"effect": "heal", "value": 10},
    "ginsing": {"effect": "restore_mp", "value": 5},
    "fungi": {"effect": "buff", "value": 3},
    
    "health_potion": {"effect": "heal", "value": 20},
    "mana_potion": {"effect": "restore_mp", "value": 15},
    "strength_elixir": {"effect": "buff", "value": 5},
}

Nyx = {
    "health": 100,
    "mp": 50,
    "special_cost": 10,
    "ally_god": "",
    "inventory": [],
    "Max_capacity": 5
}

Gods ={
    "Apolo":{"weapon":"solar bow", "element":"fire", "damage": 15, "weakness": "water"},
    "Ares":{"weapon":"spear", "element":"rage", "damage": 20, "weakness": "clear mind"},
    "Athena":{"weapon":"sword", "element":"clear mind", "damage": 10, "weakness": "rage"},
    "Poseidon":{"weapon":"trident", "element":"water", "damage": 12, "weakness": "fire"},
    "Artemis":{"weapon":"bow", "element":"nature", "damage": 14, "weakness": "earth"},        
}

def select_ally():
    print("\n--- Select your God to ally you in battle ---")
    ally_god = ""
    while ally_god not in Gods:
        ally_god = input("Choose your God (Apolo, Ares, Athena, Poseidon, Artemis): ").title()
        if ally_god not in Gods:
            print("Invalid choice. Please select a valid God.")
    print(f"\nYou have chosen {ally_god.capitalize()} as your ally!")
    Nyx["ally_god"] = ally_god
    
    print(f"\nAs {ally_god.capitalize()} power starts to flow through Nyx, The weapon of {ally_god.capitalize()} appears in Nyx's hand and the element of {Gods[ally_god]['element']} is unleashed within Nyx's body.")
    time.sleep(2)

def crafting_system():
    recipes = {
        "health_potion": {"herbs": 2},
        "mana_potion": {"ginsing": 2},
        "strength_elixir": {"fungi": 2},
        "rejuvenation_flask": {"herbs": 1, "ginsing": 1}
    }
    print("\n--- Crafting System ---")
    print("Available items to craft:")

    for crafted_item, ingredients in recipes.items():
        reqs = ", ".join([f"{count}x {ing.title()}" for ing, count in ingredients.items()])
        print(f"- {crafted_item.replace('_', ' ').title()} (Requires: {reqs})")

    print("\nYour Inventory:")
    # Solución aplicada: Contar elementos directamente en la lista
    unique_inv_items = set(Nyx["inventory"])
    for item in unique_inv_items:
        count = Nyx["inventory"].count(item)
        print(f"{item.title()}: {count}")

    choice = input("\nEnter the name of the item you want to craft (or type 'cancel' to go back): ").lower().replace(' ', '_')
    if choice == 'cancel':
        print("Exiting crafting menu.")
        return
        
    if choice in recipes:
        can_craft = True
        recipe = recipes[choice]

        # Solución aplicada: Validar contra el conteo de la lista
        for ingredient, required_amount in recipe.items():
            if Nyx["inventory"].count(ingredient) < required_amount:
                can_craft = False
                print(f"\nYou don't have enough {ingredient.title()}! You need {required_amount}.")
                break

        if can_craft:
            # Solución aplicada: Remover elementos usados y agregar el crafteado a la lista
            for ingredient, required_amount in recipe.items():
                for _ in range(required_amount):
                    Nyx["inventory"].remove(ingredient)

            Nyx["inventory"].append(choice)
            print(f"\nSuccess! You crafted a {choice.replace('_', ' ').title()}!")
    else:
        print("\nPlease choose a valid recipe.")

def Add_item_to_inventory(inventory, item):
    if len(inventory) >= Nyx["Max_capacity"]:
        print("Inventory is full! Cannot add more items.")
        return
    inventory.append(item)
    print(f"{item} has been added to your inventory.")
    return inventory

def use_item(inventory):
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

enemies = {
    "fire_fiend": {"health": 30, "damage": 10, "element": "fire", "weakness": "water"},
    "water_zombie": {"health": 20, "damage": 12, "element": "water", "weakness": "nature"},
    "earth_golem": {"health": 50, "damage": 15, "element": "earth", "weakness": "fire"},
    "vengeful_spirit": {"health": 30, "damage": 14, "element": "rage", "weakness": "clear mind"},
    "mind_flayer": {"health": 40, "damage": 20, "element": "clear mind", "weakness": "rage"}
}

spawned_enemies = [] 

def Enemy_Set_up():
    print("\n--- Select the Enemies to fight against ---")
    enemy_count = 0
    try:
        enemy_amount = int(input("How many enemies do you want to fight against?: "))
        while enemy_count < enemy_amount:
            enemy = input(f"Enter the name of enemy {enemy_count + 1} (e.g., fire_fiend): ").lower().replace(' ', '_')
            if enemy in enemies:
                spawned_enemies.append(enemy)
                enemy_count += 1
            else:
                print("Invalid input. Please enter a valid enemy name.")
    except ValueError:
        print("Please enter a valid number.")

def combat_phase(): # Eliminamos los parámetros locales
    active_combat = True
    while active_combat:
        print("\n--- Combat Phase ---")
        print(f"Nyx's Health: {Nyx['health']}") # Lee directamente del diccionario

        active_enemies = [e for e in spawned_enemies if e in enemies and enemies[e]["health"] > 0]
        
        if not active_enemies:
            print("\nAll enemies have been defeated! You are victorious!")
            break
            
        print("Enemies:")
        for enemy in active_enemies:
            print(f"- {enemy.replace('_', ' ').capitalize()} (Health: {enemies[enemy]['health']}, Element: {enemies[enemy]['element']})")
            
        action = input("\nChoose your action (attack, defend, use item, flee): ").lower()
        if action == "attack":
            target = input("Choose an enemy to attack: ").lower().replace(' ', '_')
            if target in active_enemies:
                attack_type = input("Use Normal or Special attack? ").lower()
                base_damage = Gods[Nyx["ally_god"]]["damage"]
                
                if attack_type == "special":
                    if Nyx["mp"] >= Nyx["special_cost"]: # Usa el diccionario
                        Nyx["mp"] -= Nyx["special_cost"]
                        print(f"\nNyx channels {Gods[Nyx['ally_god']]['element']} magic! (-{Nyx['special_cost']} MP)")
                        
                        if enemies[target]["weakness"] == Gods[Nyx["ally_god"]]["element"]:
                            print("It's super effective!")
                            base_damage = int(base_damage * 1.5)
                    else:
                        print("\nNot enough MP! Nyx performs a normal attack instead.")
                
                enemies[target]["health"] -= base_damage
                print(f"You struck {target.replace('_', ' ').capitalize()} for {base_damage} damage!")
                
                if enemies[target]["health"] <= 0:
                    print(f"{target.replace('_', ' ').capitalize()} has been defeated!")
            else:
                print("Invalid target. You missed your turn!")
                
        elif action == "defend":
            print("\nYou brace yourself for the next attack.")
        elif action == "use item":
            use_item(Nyx["inventory"])
        elif action == "flee":
            print("\nYou have fled the battle!")
            break
        else:
            print("Invalid action.")
            continue

        # Fase de ataque enemigo
        for enemy in active_enemies:
            if enemies[enemy]["health"] > 0:
                print(f"\n{enemy.replace('_', ' ').capitalize()} attacks Nyx!")
                Nyx["health"] -= enemies[enemy]["damage"] # Resta directo al diccionario
                print(f"Nyx takes {enemies[enemy]['damage']} damage! Remaining Health: {Nyx['health']}")
                if Nyx["health"] <= 0:
                    print("\nNyx has been defeated! Game Over.")
                    return

# Bloque de ejecución principal
if __name__ == "__main__":
    print("Welcome to The Ballad of Nyx")
    select_ally()
    
    # Pruebas iniciales para demostrar funcionalidad al profesor
    Add_item_to_inventory(Nyx["inventory"], "herbs")
    Add_item_to_inventory(Nyx["inventory"], "herbs")
    Add_item_to_inventory(Nyx["inventory"], "ginsing")
    Add_item_to_inventory(Nyx["inventory"], "ginsing")
        
    
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Crafting System")
        print("2. Manage Inventory")
        print("3. Enter Combat")
        print("4. Exit")
        
        op = input("Choose an option: ")
        if op == "1":
            crafting_system()
        elif op == "2":
            print(f"\nCurrent Inventory: {Nyx['inventory']}")
            sub = input("Type 'use' to use an item, 'drop' to empty inventory, or 'back': ").lower()
            if sub == "use":
                use_item(Nyx["inventory"])
            elif sub == "drop":
                throw_item(Nyx["inventory"])
        elif op == "3":
            Enemy_Set_up()
            combat_phase()
        elif op == "4":
            break