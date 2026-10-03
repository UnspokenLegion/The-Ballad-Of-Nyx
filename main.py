import time
import inventario # Importamos el inventario 
import historial # NUEVO: Importamos el módulo de la pila para el Checkpoint 2

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
    
    print(f"\nAs {ally_god.capitalize()} power starts to flow through Nyx, The weapon of {ally_god.capitalize()} appears in Nyx's hand and the element of {Gods[ally_god]['element']} is unleashed within Nyx's body, granting her the power of {Gods[ally_god]['element']} and the weapon of {Gods[ally_god]['weapon']}.")
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

        for ingredient, required_amount in recipe.items():
            if Nyx["inventory"].count(ingredient) < required_amount:
                can_craft = False
                print(f"\nYou don't have enough {ingredient.title()}! You need {required_amount}.")
                break

        if can_craft:
            for ingredient, required_amount in recipe.items():
                for _ in range(required_amount):
                    Nyx["inventory"].remove(ingredient)

            Nyx["inventory"].append(choice)
            print(f"\nSuccess! You crafted a {choice.replace('_', ' ').title()}!")
            
            # NUEVO: Enviamos la acción a la Pila (O(1))
            historial.registrar_accion("craftear", {
                "item_creado": choice,
                "ingredientes_gastados": recipe
            })
    else:
        print("\nPlease choose a valid recipe.")

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

def combat_phase(): 
    active_combat = True
    while active_combat:
        print("\n--- Combat Phase ---")
        print(f"\nNyx's Health: {Nyx['health']}") 

        active_enemies = [e for e in spawned_enemies if e in enemies and enemies[e]["health"] > 0]
        
        if not active_enemies:
            print("\nAll enemies have been defeated! You are victorious!")
            active_combat = False
            break
            
        print("Enemies:")
        for enemy in active_enemies:
            print(f"{enemy.capitalize()} - Health: {enemies[enemy]['health']}, Element: {enemies[enemy]['element']}")
            
        action = input("\nChoose your action (attack, defend, use item, flee): ").lower()
        if action == "attack":
            target = input("Choose an enemy to attack: ").lower().replace(' ', '_')
            if target in active_enemies:
                attack_type = input("Use Normal or Special attack? ").lower()
                base_damage = Gods[Nyx["ally_god"]]["damage"]
                
                if attack_type == "special":
                    if Nyx["mp"] >= Nyx["special_cost"]:
                        Nyx["mp"] -= Nyx["special_cost"]
                        print(f"\nNyx channels {Gods[Nyx['ally_god']]['element']} magic! (-{Nyx['special_cost']} MP)")
                        
                        if enemies[target]["weakness"] == Gods[Nyx["ally_god"]]["element"]:
                            print("It's super effective!")
                            base_damage = int(base_damage * 1.5)
                    else:
                        print("\nNot enough MP! Nyx performs a normal attack instead.")
                
                enemies[target]["health"] -= base_damage
                print(f"You struck {target.capitalize()} with {Gods[Nyx['ally_god']]['weapon']} for {base_damage} damage!")
                print(f"Remaining MP: {Nyx['mp']}")
                
                if enemies[target]["health"] <= 0:
                    print(f"{target.capitalize()} has been defeated!")
            else:
                print("Invalid target. You missed your turn!")
                
        elif action == "defend":
            print("\nYou brace yourself for the next attack.")
        elif action == "use item":
            print("\nYou rummage through your inventory for an item to use.")
            inventario.use_item(Nyx["inventory"], Nyx, items, Gods)
        elif action == "flee":
            print("\nYou have fled the battle!")
            active_combat = False
            break
        else:
            print("Invalid action.")
            continue

        for enemy in active_enemies:
            if enemies[enemy]["health"] > 0:
                print(f"\n{enemy.capitalize()} attacks Nyx!")
                Nyx["health"] -= enemies[enemy]["damage"]
                print(f"Nyx takes {enemies[enemy]['damage']} damage! Remaining Health: {Nyx['health']}")
                if Nyx["health"] <= 0:
                    print("\nNyx has been defeated! Game Over.")
                    active_combat = False
                    return

# Bloque de ejecución y Menú Principal
if __name__ == "__main__":
    print("Welcome to The Ballad of Nyx")
    select_ally()
    
    inventario.Add_item_to_inventory(Nyx["inventory"], "herbs", Nyx["Max_capacity"])
    inventario.Add_item_to_inventory(Nyx["inventory"], "herbs", Nyx["Max_capacity"])
    inventario.Add_item_to_inventory(Nyx["inventory"], "ginsing", Nyx["Max_capacity"])
    inventario.Add_item_to_inventory(Nyx["inventory"], "ginsing", Nyx["Max_capacity"])
    
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Crafting System")
        print("2. Manage Inventory")
        print("3. Enter Combat")
        print("4. Undo Last Action") # NUEVO
        print("5. Exit") # Cambiado a 5
        
        op = input("Choose an option: ")
        if op == "1":
            crafting_system()
        elif op == "2":
            print(f"\nCurrent Inventory: {Nyx['inventory']}")
            sub = input("Type 'use' to use an item, 'drop' to empty inventory, or 'back': ").lower()
            if sub == "use":
                inventario.use_item(Nyx["inventory"], Nyx, items, Gods)
            elif sub == "drop":
                inventario.throw_item(Nyx["inventory"])
        elif op == "3":
            Enemy_Set_up()
            combat_phase()
        elif op == "4":
            # NUEVO: Llama a la pila para revertir la acción más reciente
            historial.deshacer_accion(Nyx["inventory"])
        elif op == "5":
            print("Exiting the game...")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 5.")