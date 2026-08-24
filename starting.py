import time
def combat_system():
    #1. defining the gods and their attributes and weapons
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
    #2. to choose the god you will fight with
    print("\n--- Select your God to ally you in battle ---")
    ally_god = ""
    while ally_god not in Gods:
        ally_god = input("Choose your God (Apolo, Ares, Athena, Poseidon, Artemis): ").title()
        if ally_god not in Gods:
            print("Invalid choice. Please select a valid God.")
    Nyx = Gods[ally_god]
    print(f"\nYou have chosen {ally_god.capitalize()} as your ally!")
    Nyx_health = 100
    Nyx_Mp = 50
    special_cost = 10

    print(f"\nAs {ally_god.capitalize()} power starts to flow through Nyx, The weapon of {ally_god.capitalize()} appears in Nyx's hand and the element of {Gods[ally_god]['element']} is unleashed within Nyx's body, granting her the power of {Gods[ally_god]['element']} and the weapon of {Gods[ally_god]['weapon']}.")
    time.sleep(2)



    #3. Enemy selection and setup
    enemies = {
        "fire_fiend": {"health": 30, "damage": 10, "element": "fire", "weakness": "water"},
        "water_zombie": {"health": 20, "damage": 12, "element": "water", "weakness": "nature"},
        "earth_golem": {"health": 50, "damage": 15, "element": "earth", "weakness": "fire"},
        "vengeful_spirit": {"health": 30, "damage": 14, "element": "rage", "weakness": "clear mind"},
        "Mind_flayer": {"health": 40, "damage": 20, "element": "clear mind", "weakness": "rage"}
    }
    print("\n--- Select the Enemies to fight against ---")
    enemy_count = 0
    enemy_amount = int(input("How many enemies do you want to fight against?: "))
    ememies = []
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

    #4. Combat loop
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
                base_damage = Gods[ally_god]["damage"]
                
                if attack_type == "special":
                    if Nyx_Mp >= special_cost:
                        Nyx_Mp -= special_cost
                        print(f"\nNyx channels {Gods[ally_god]['element']} magic! (-{special_cost} MP)")
                        
                        # Check for weakness multiplier
                        if enemies[target]["weakness"] == Gods[ally_god]["element"]:
                            print("It's super effective!")
                            base_damage = int(base_damage * 1.5) # 1.5x damage modifier
                    else:
                        print("\nNot enough MP! Nyx performs a normal attack instead.")
                
                enemies[target]["health"] -= base_damage
                print(f"You struck {target.capitalize()} with {Gods[ally_god]['weapon']} for {base_damage} damage!")
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
            print("\nYou used a healing potion and restored 20 health!")
            Nyx_health += 20
            if Nyx_health > 100:
                Nyx_health = 100
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
combat_system()
