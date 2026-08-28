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
"Apolo":{"weapon":"solar bow",
            "element":"fire",
            "damage": 15,
            "weakness": "water"},
"Ares":{"weapon":"spear",
            "element":"rage",
            "damage": 20,
            "weakness": "clear mind"},
"Athena":{"weapon":"sword",
            "element":"clear mind",
            "damage": 10,
            "weakness": "rage"},
"Poseidon":{"weapon":"trident",
            "element":"water",
            "damage": 12,
            "weakness": "fire"},
"Artemis":{"weapon":"bow", 
            "element":"nature",
            "damage": 14,
            "weakness": "earth"},        
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
    Nyx_health = Nyx["health"]
    Nyx_Mp = Nyx["mp"]
    special_cost = Nyx["special_cost"]

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
    for item, count in Nyx["inventory"].items():
        if count > 0:
            print(f"{item.title()}: {count}")

    choice = input("\nEnter the name of the item you want to craft (or type 'cancel' to go back): ").lower().replace(' ', '_')
    if choice == 'cancel':
        print("Exiting crafting menu.")
        return
    if choice in recipes:
        can_craft = True
        recipe = recipes[choice]

        for ingredient, required_amount in recipe.items():
            if Nyx["inventory"].get(ingredient, 0) < required_amount:
                can_craft = False
                print(f"\nYou don't have enough {ingredient.title()}! You need {required_amount}.")
                break

        if can_craft:
            for ingredient, required_amount in recipe.items():
                Nyx["inventory"][ingredient] -= required_amount

            Nyx["inventory"][choice] = Nyx["inventory"].get(choice, 0) + 1
            print(f"\nSuccess! You crafted a {choice.replace('_', ' ').title()}!")
    else:
        print("\nInvalid item. Please choose a valid recipe.")



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
    print("Inventory:")
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

def repeating_items(inventory):
    if not inventory:
        print("Your inventory is empty!")
        return []
    counts = {}
    for item in inventory:
        counts[item] = counts.get(item, 0) + 1
    max_count = max(counts.values())
    max_items = [item for item, count in counts.items() if count == max_count]    
    print(f"Most repeated items: {max_items} ({max_count} times)")
    return max_items

def unique_items(inventory):
    if not inventory:
        print("Your inventory is empty!")
        return []
    unique_items = list(set(inventory))
    print(f"Unique items in inventory: {unique_items}")
    return unique_items
enemies = {
        "fire_fiend": {"health": 30, "damage": 10, "element": "fire", "weakness": "water"},
        "water_zombie": {"health": 20, "damage": 12, "element": "water", "weakness": "nature"},
        "earth_golem": {"health": 50, "damage": 15, "element": "earth", "weakness": "fire"},
        "vengeful_spirit": {"health": 30, "damage": 14, "element": "rage", "weakness": "clear mind"},
        "Mind_flayer": {"health": 40, "damage": 20, "element": "clear mind", "weakness": "rage"}
    }
ememies = []
def Enemy_Set_up():
    #3.Enemy selection and setup 
    
    print("\n--- Select the Enemies to fight against ---")
    enemy_count = 0
    enemy_amount = int(input("How many enemies do you want to fight against?: "))
    while True:
        if enemy_count < enemy_amount:
            print(enemy_count)
            enemy = input(f"Enter the name of enemy {enemy_count + 1}: ")
            if enemy:
                ememies.append(enemy)
                enemy_count += 1
            else:
                print("Invalid input. Please enter a valid enemy name.")
        else:
            print("im in the break")
            print(enemy_count)
            break  


def combat_phase(Nyx_health, Nyx_Mp):
    active_combat = True
    while active_combat:
        print("\n--- Combat Phase ---")
        print(f"\nNyx's Health: {Nyx_health}")

        active_enemies = [e for e in ememies if e in enemies and enemies[e]["health"] > 0]
        print("Enemies:")
        for enemy in active_enemies:
            print(f"{enemy.capitalize()} - Health: {enemies[enemy]['health']}, Element: {enemies[enemy]['element']}")
        action = input("\nChoose your action defend, (attack, use item, flee): ").lower()
        if action == "attack":
            target = input("Choose an enemy to attack: ").lower()
            if target in active_enemies:
                attack_type = input("Use Normal or Special attack? ").lower()
                base_damage = Gods[Nyx["ally_god"]]["damage"]
                
                if attack_type == "special":
                    if Nyx_Mp >= Nyx["special_cost"]:
                        Nyx_Mp -= Nyx["special_cost"]
                        print(f"\nNyx channels {Gods[Nyx['ally_god']]['element']} magic! (-{Nyx['special_cost']} MP)")
                        
                        # Check for weakness multiplier
                        if enemies[target]["weakness"] == Gods[Nyx["ally_god"]]["element"]:
                            print("It's super effective!")
                            base_damage = int(base_damage * 1.5) # 1.5x damage modifier
                    else:
                        print("\nNot enough MP! Nyx performs a normal attack instead.")
                
                enemies[target]["health"] -= base_damage
                print(f"You struck {target.capitalize()} with {Gods[Nyx['ally_god']]['weapon']} for {base_damage} damage!")
                print(f"Remaining MP: {Nyx_Mp}")
                
                if enemies[target]["health"] <= 0:
                    print(f"{target.capitalize()} has been defeated!")
                    del enemies[target]
                if not enemies:
                    print("\nAll enemies have been defeated! You are victorious!")
                    active_combat = False
            else:
                print("Invalid target. You missed your turn!")
        elif action == "defend":
            print("\nYou brace yourself for the next attack.")
        elif action == "use item":
            print("\nYou rummage through your inventory for an item to use.")
            use_item(Nyx["inventory"])
        elif action == "show inventory":
            if not Nyx["inventory"]:
                print("Your inventory is empty!")
            else:
                print("Inventory:")
                for item in Nyx["inventory"]:
                    print(f"- {item}")
        elif action == "throw all items":
            throw_item(Nyx["inventory"])
        elif action == "flee":
            print("\nYou have fled the battle!")
            active_combat = False
        #5. Enemy attack phase
        for enemy in active_enemies:
            if enemies[enemy]["health"] > 0:
                print(f"\n{enemy.capitalize()} attacks Nyx!")
                Nyx_health -= enemies[enemy]["damage"]
                print(f"Nyx takes {enemies[enemy]['damage']} damage! Remaining Health: {Nyx_health}")
                if Nyx_health <= 0:
                    print("\nNyx has been defeated! Game Over.")
                    active_combat = False
                    break

