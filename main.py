"""
Módulo: main.py
Objetivo: Archivo central que ensambla el juego e importa todos los submódulos.
Contiene el estado global de Nyx, los enemigos, el sistema de crafteo y el bucle del menú principal.
"""

import time
import random 
import inventario 
import historial 
import eventos 
import mazmorra 

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
    print("\n--- [Sistema] Selecciona a tu Dios aliado para la batalla ---")
    ally_god = ""
    while ally_god not in Gods:
        ally_god = input("Elige a tu Dios (Apolo, Ares, Athena, Poseidon, Artemis): ").title()
        if ally_god not in Gods:
            print("[Sistema] Opción inválida. Por favor selecciona un Dios válido.")
    print(f"\n[Sistema] ¡Has elegido a {ally_god.capitalize()} como tu aliado!")
    Nyx["ally_god"] = ally_god
    
    print(f"\n[Historia] El poder de {ally_god.capitalize()} comienza a fluir a través de Nyx. El arma de {ally_god.capitalize()} ({Gods[ally_god]['weapon']}) aparece en sus manos y el elemento {Gods[ally_god]['element']} se desata en su interior, otorgándole una nueva fuerza.")
    time.sleep(2)

def crafting_system():
    recipes = {
        "health_potion": {"herbs": 2},
        "mana_potion": {"ginsing": 2},
        "strength_elixir": {"fungi": 2},
        "rejuvenation_flask": {"herbs": 1, "ginsing": 1}
    }
    # Extraemos las llaves en una lista para poder seleccionarlas por índice numérico
    recipe_keys = list(recipes.keys())

    print("\n--- [Crafteo] Sistema de Creación ---")
    print("Objetos disponibles para crear:")

    for idx, crafted_item in enumerate(recipe_keys, 1):
        ingredients = recipes[crafted_item]
        reqs = ", ".join([f"{count}x {ing.title()}" for ing, count in ingredients.items()])
        print(f"{idx}) {crafted_item.replace('_', ' ').title()} (Requiere: {reqs})")

    print("\n[Inventario] Tu inventario actual:")
    unique_inv_items = set(Nyx["inventory"])
    for item in unique_inv_items:
        count = Nyx["inventory"].count(item)
        print(f"{item.title()}: {count}")

    opcion_crafteo = input("\nElige el número de la receta a crear (o '0' para cancelar): ")
    
    # Manejo de casos límite: entradas de texto, ceros o números fuera de rango
    try:
        idx_crafteo = int(opcion_crafteo) - 1
        
        if idx_crafteo == -1: # El jugador escribió 0
            print("[Crafteo] Saliendo del menú de creación.")
            return
            
        if 0 <= idx_crafteo < len(recipe_keys):
            choice = recipe_keys[idx_crafteo]
            can_craft = True
            recipe = recipes[choice]

            for ingredient, required_amount in recipe.items():
                if Nyx["inventory"].count(ingredient) < required_amount:
                    can_craft = False
                    print(f"\n[Crafteo] ¡No tienes suficiente {ingredient.title()}! Necesitas {required_amount}.")
                    break

            if can_craft:
                for ingredient, required_amount in recipe.items():
                    for _ in range(required_amount):
                        Nyx["inventory"].remove(ingredient)

                Nyx["inventory"].append(choice)
                print(f"\n[Crafteo] ¡Éxito! ¡Has creado un {choice.replace('_', ' ').title()}!")
                
                historial.registrar_accion("craftear", {
                    "item_creado": choice,
                    "ingredientes_gastados": recipe
                })
        else:
            print("[Crafteo] Opción fuera de rango. Por favor elige un número válido.")
    except ValueError:
        print("[Crafteo] Entrada no válida. Debes ingresar el número de la receta.")

enemies = {
    "fire_fiend": {"health": 30, "damage": 10, "element": "fire", "weakness": "water"},
    "water_zombie": {"health": 20, "damage": 12, "element": "water", "weakness": "nature"},
    "earth_golem": {"health": 50, "damage": 15, "element": "earth", "weakness": "fire"},
    "vengeful_spirit": {"health": 30, "damage": 14, "element": "rage", "weakness": "clear mind"},
    "mind_flayer": {"health": 40, "damage": 20, "element": "clear mind", "weakness": "rage"}
}

spawned_enemies = [] 

def Enemy_Set_up():
    print("\n--- [Sistema] Configuración de Enemigos ---")
    spawned_enemies.clear() 
    
    try:
        enemy_amount = int(input("¿Contra cuántos enemigos deseas luchar?: "))
        
        # Manejo de casos límite: evitar que 0 o negativos rompan la lógica
        if enemy_amount <= 0:
            print("[Sistema] ¡Cantidad inválida! Debes ingresar un número mayor a 0.")
            return
            
        enemy_count = 0
        while enemy_count < enemy_amount:
            base_enemy = input(f"Ingresa el nombre del enemigo {enemy_count + 1} (ej. fire_fiend): ").lower().replace(' ', '_')
            
            if base_enemy in enemies:
                unique_name = f"{base_enemy}_{enemy_count + 1}"
                enemies[unique_name] = enemies[base_enemy].copy()
                spawned_enemies.append(unique_name)
                enemy_count += 1
            else:
                print("[Sistema] Entrada inválida. Nombre de enemigo no reconocido.")
    except ValueError:
        print("[Sistema] Por favor ingresa un número válido.")

def combat_phase(): 
    active_enemies = [e for e in spawned_enemies if e in enemies and enemies[e]["health"] > 0]
    
    # Si active_enemies está vacío (por ejemplo si el jugador ingresó <= 0 y el setup hizo return), cancelamos el combate
    if not active_enemies:
        return

    print("\n==============================")
    print("    INICIA LA FASE DE COMBATE  ")
    print("==============================")
    
    eventos.limpiar_turnos()
    eventos.agregar_turno("nyx")
    for enemy in active_enemies:
        eventos.agregar_turno(enemy)

    active_combat = True
    while active_combat:
        turno_actual = eventos.siguiente_turno()
        
        if turno_actual is None:
            break
            
        if turno_actual == "nyx":
            print(f"\n--- [Turno] EL TURNO DE NYX ---")
            print(f"Salud: {Nyx['health']} | PM: {Nyx['mp']}") 
            
            vivos = [e for e in active_enemies if enemies[e]["health"] > 0]
            if not vivos:
                print("\n[Combate] ¡Todos los enemigos han sido derrotados! ¡Eres victoriosa!")
                active_combat = False
                break
                
            print("\n[Combate] Enemigos Activos:")
            for idx, enemy in enumerate(vivos, 1):
                print(f"{idx}) {enemy.capitalize()} (Salud: {enemies[enemy]['health']}, Elemento: {enemies[enemy]['element']})")
                
            action = input("\nElige tu acción (atacar, defender, usar, huir): ").lower()
            if action == "atacar":
                opcion_objetivo = input("Elige el número del enemigo a atacar: ")
                
                try:
                    idx_objetivo = int(opcion_objetivo) - 1
                    if 0 <= idx_objetivo < len(vivos):
                        target = vivos[idx_objetivo]
                        
                        attack_type = input("¿Usar ataque normal o especial? ").lower()
                        base_damage = Gods[Nyx["ally_god"]]["damage"]
                        
                        if attack_type == "especial":
                            if Nyx["mp"] >= Nyx["special_cost"]:
                                Nyx["mp"] -= Nyx["special_cost"]
                                print(f"\n[Combate] ¡Nyx canaliza magia de {Gods[Nyx['ally_god']]['element']}! (-{Nyx['special_cost']} PM)")
                                
                                if enemies[target]["weakness"] == Gods[Nyx["ally_god"]]["element"]:
                                    print("[Combate] ¡Es súper efectivo!")
                                    base_damage = int(base_damage * 1.5)
                            else:
                                print("\n[Combate] ¡No tienes suficiente PM! Nyx realiza un ataque normal en su lugar.")
                        
                        enemies[target]["health"] -= base_damage
                        print(f"[Combate] ¡Golpeas a {target.capitalize()} con tu {Gods[Nyx['ally_god']]['weapon']} por {base_damage} de daño!")
                        
                        if enemies[target]["health"] <= 0:
                            print(f"[Combate] ¡{target.capitalize()} ha sido derrotado!")
                    else:
                        print("[Combate] Objetivo fuera de rango. ¡Perdiste la concentración y tu turno!")
                except ValueError:
                    print("[Combate] Entrada no válida. ¡Debías ingresar un número! Perdiste tu turno.")
                    
            elif action == "defender":
                print("\n[Combate] Te preparas para resistir el siguiente ataque.")
            elif action == "usar":
                print("\n[Combate] Buscas en tu inventario un objeto para usar...")
                inventario.use_item(Nyx["inventory"], Nyx, items, Gods)
            elif action == "huir":
                print("\n[Combate] ¡Has huido de la batalla de forma cobarde!")
                active_combat = False
                break
            else:
                print("[Combate] Acción no reconocida. ¡Perdiste tu turno por dudar!")
            
            if active_combat:
                eventos.agregar_turno("nyx")

        else: 
            enemy = turno_actual
            if enemies[enemy]["health"] > 0:
                print(f"\n--- [Turno] TURNO DE {enemy.upper()} ---")
                print(f"[Combate] ¡{enemy.capitalize()} ataca a Nyx!")
                Nyx["health"] -= enemies[enemy]["damage"]
                print(f"[Combate] ¡Nyx recibe {enemies[enemy]['damage']} de daño! Salud restante: {Nyx['health']}")
                
                if Nyx["health"] <= 0:
                    print("\n[Combate] ¡Nyx ha sido derrotada! Fin del juego.")
                    Nyx["health"] = 100 
                    print("[Historia] Nyx se despierta de vuelta en el campamento base...")
                    active_combat = False
                    break 
                
                eventos.agregar_turno(enemy)
                time.sleep(1)
                
    eventos.limpiar_turnos()

# Bloque de ejecución y Menú Principal
if __name__ == "__main__":
    print("Bienvenido a La Balada de Nyx")
    select_ally()
    
    inventario.Add_item_to_inventory(Nyx["inventory"], "herbs", Nyx["Max_capacity"])
    inventario.Add_item_to_inventory(Nyx["inventory"], "herbs", Nyx["Max_capacity"])
    inventario.Add_item_to_inventory(Nyx["inventory"], "ginsing", Nyx["Max_capacity"])
    inventario.Add_item_to_inventory(Nyx["inventory"], "ginsing", Nyx["Max_capacity"])
    
    while True:
        print("\n--- [Menú] MENÚ PRINCIPAL ---")
        print("1. Sistema de Crafteo")
        print("2. Gestionar Inventario")
        print("3. Entrar en Combate")
        print("4. Deshacer Última Acción")
        print("5. Explorar la Mazmorra")
        print("6. Salir")
        
        op = input("Elige una opción: ")
        
        if op == "1":
            crafting_system()
        elif op == "2":
            print(f"\n[Inventario] Inventario Actual: {Nyx['inventory']}")
            sub = input("Escribe 'usar' para consumir un objeto, 'tirar' para vaciarlo, o 'volver': ").lower()
            if sub == "usar":
                inventario.use_item(Nyx["inventory"], Nyx, items, Gods)
            elif sub == "tirar":
                inventario.throw_item(Nyx["inventory"])
        elif op == "3":
            Enemy_Set_up()
            combat_phase()
        elif op == "4":
            historial.deshacer_accion(Nyx["inventory"])
            
        elif op == "5":
            print("\n--- [Sistema] Generando la Mazmorra ---")
            conexiones_mapa = []
            salas_generadas = []
            nombres_disponibles = [
                "Isla Aislada", "Bosque Muerto", "Volcán Extraño", "Cripta Olvidada", 
                "Lago Abisal", "Templo en Ruinas", "Altar Oscuro", "Caverna de Cristal", 
                "Torreón Perdido", "Cueva Susurrante", "Santuario de Sangre", "Laberinto de Sombras", 
                "Salones Resonantes", "Ruinas Hundidas", "Cementerio Maldito", "Aguja de Obsidiana"
            ]
            
            sala_inicial = "Cueva Ancestral"
            mazmorra.generar_mazmorra_ramificacion_aleatoria(
                sala_inicial, 0, 2, 1, 3, conexiones_mapa, salas_generadas, nombres_disponibles
            )
            
            print(f"[Mapa] ¡Mazmorra generada! {len(salas_generadas)} salas esperan por ti.")
            
            eventos.limpiar_turnos()
            eventos_posibles = [
                "[Entorno] Un murciélago gigante roza tu cabeza en la oscuridad.", 
                "[Entorno] Escuchas pasos pesados y metálicos resonando a lo lejos.", 
                "[Entorno] Una ráfaga de viento helado casi apaga tu antorcha.", 
                "[Entorno] Sientes una presencia ancestral observándote."
            ]
            for _ in range(len(salas_generadas)):
                eventos.agregar_turno(random.choice(eventos_posibles))

            sala_actual = sala_inicial
            explorando = True
            
            while explorando:
                print(f"\n[MAPA] Estás en: {sala_actual}")
                salas_conectadas = [destino for origen, destino in conexiones_mapa if origen == sala_actual]
                
                if len(salas_conectadas) == 0:
                    print("[Exploración] ¡Esta sala es un callejón sin salida! Encuentras un 'fungi' brillante en el suelo.")
                    inventario.Add_item_to_inventory(Nyx["inventory"], "fungi", Nyx["Max_capacity"])
                
                print("\n1. Moverse  2. Ver historial  3. Deshacer movimiento  4. Salir de la mazmorra")
                accion_mazmorra = input("Opción: ")
                
                if accion_mazmorra == "1":
                    if not salas_conectadas:
                        print("[Sistema] No hay salidas desde aquí. ¡Utiliza la opción de deshacer para retroceder!")
                        continue
                        
                    print("[Mapa] Salas conectadas:")
                    for idx, sala in enumerate(salas_conectadas, 1):
                        print(f"{idx}) {sala}")
                        
                    opcion_sala = input("Elige el número de la sala: ")
                    
                    try:
                        idx_sala = int(opcion_sala) - 1
                        if 0 <= idx_sala < len(salas_conectadas):
                            sala_destino = salas_conectadas[idx_sala]
                            
                            historial.registrar_accion("moverse", {"sala_origen": sala_actual})
                            sala_actual = sala_destino
                            print(f"\n[Exploración] Te adentras valientemente en: {sala_actual}")
                            
                            evento_actual = eventos.siguiente_turno()
                            if evento_actual:
                                print(f"{evento_actual}")
                            else:
                                print("[Entorno] Todo está extrañamente tranquilo (Cola de eventos vacía).")
                        else:
                            print("[Sistema] Opción fuera de rango. Intentas caminar contra una pared sólida.")
                    except ValueError:
                        print("[Sistema] Opción no válida. Debes ingresar el número de la sala.")
                        
                elif accion_mazmorra == "2":
                    historial.mostrar_historial_completo()
                    
                elif accion_mazmorra == "3":
                    sala_devuelta = historial.deshacer_accion(Nyx["inventory"])
                    if sala_devuelta:
                        sala_actual = sala_devuelta
                        print("[Historia] (El evento que acababas de presenciar se desvanece en el tiempo...)")
                        
                elif accion_mazmorra == "4":
                    print("[Exploración] Escapas de la mazmorra y vuelves al campamento.")
                    explorando = False
                else:
                    print("[Sistema] Opción no válida. Ingresa 1, 2, 3 o 4.")

        elif op == "6":
            print("[Sistema] Saliendo del juego...")
            break
        else:
            print("[Sistema] Opción inválida. Por favor ingresa un número del 1 al 6.")