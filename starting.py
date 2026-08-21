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
    print(f"\n as {ally_god.capitalize()} power starts to flow through Nyx, The weapon of {ally_god.capitalize()} appears in Nyx's hand and the element of {Gods[ally_god]['element']} is unleashed within Nyx's body, granting her the power of {Gods[ally_god]['element']} and the weapon of {Gods[ally_god]['weapon']}.")
    time.sleep(2)

    #4. Enemy selection and setup
    enemies = {
        "fire_fiend": {"health": 80, "damage": 10, "element": "fire"},
        "water_zombie": {"health": 70, "damage": 12, "element": "water"},
        "earth_golem": {"health": 100, "damage": 15, "element": "earth"},
        "vengeful_spirit": {"health": 90, "damage": 14, "element": "rage"},
        "Mind_flayer": {"health": 60, "damage": 20, "element": "clear mind"}
    }
    print("\n--- Select the Enemies to fight against ---")
    enemy_count = 0
    ememies = []
    while enemy_count < 3:
        enemy = input(f"Enter the name of enemy {enemy_count + 1}: ")
        if enemy:
            ememies.append(enemy)
            enemy_count += 1
        else:
            print("Invalid input. Please enter a valid enemy name.")
    #5. Combat loop
    active_combat = True
    while active_combat:
        print("\n--- Combat Phase ---")
        print(f"\nNyx's Health: {Nyx_health}")
        print("Enemies:")
        for enemy in ememies:
            if enemy in enemies:
                print(f"{enemy.capitalize()} - Health: {enemies[enemy]['health']}, Element: {enemies[enemy]['element']}")
            else:
                print(f"{enemy.capitalize()} - Unknown Enemy")
        action = input("\nChoose your action (attack, defend, use item, flee): ").lower()
        if action == "attack":
            target = input("Choose an enemy to attack: ").lower()
            if target in enemies:
                damage = Gods[ally_god]["damage"]
                enemies[target]["health"] -= damage
                print(f"\nYou attacked {target.capitalize()} with {Gods[ally_god]['weapon']} for {damage} damage!")
                if enemies[target]["health"] <= 0:
                    print(f"{target.capitalize()} has been defeated!")
                    ememies.remove(target)
            else:
                print("Invalid target. Please choose a valid enemy.")