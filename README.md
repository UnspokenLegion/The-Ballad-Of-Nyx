# Aventura Algorítmica: The Ballad of Nyx

---

## 1. Explicación Breve y Decisiones del Equipo
En esta primera fase del proyecto, estructuramos la base de nuestro videojuego en Python separando la lógica central en `main.py` y el manejo de estructuras de datos en `inventario.py`. Decidimos implementar el inventario como una lista simple de cadenas de texto (`Nyx["inventory"]`), lo cual permite almacenar los nombres de los ítems y manipularlos dinámicamente. Para la interacción con el usuario al usar ítems, optamos por mostrar la lista con una enumeración (`enumerate`) para que la selección sea por índice numérico; esto evita errores tipográficos y mejora la experiencia de juego. Además, la modificación y eliminación de objetos se gestiona en tiempo real con los métodos `.pop()` y `.clear()`, garantizando la sincronización con los atributos del jugador y de su dios aliado.

---

## 2. Concepto del Juego (Semana 1)
* **Mundo:** Un universo de fantasía oscura donde la magia elemental y el favor de los dioses olímpicos dictan el destino de los guerreros.
* **Protagonista:** Nyx Rigel, una guerrera que canaliza el poder, armas y elementos (fuego, agua, ira, mente clara, naturaleza) del dios que elija como aliado.
* **Antagonista:** Criaturas elementales y espectros oscuros (Fire Fiend, Water Zombie, Earth Golem, Vengeful Spirit, Mind Flayer) que amenazan el balance.
* **Objeto Especial:** Reliquias, elixires y plantas medicinales (`herbs`, `ginsing`, `health_potion`, `mana_potion`, `strength_elixir`) que restauran salud, maná o mejoran el ataque de la protagonista.
* **Problema a Resolver:** Nyx debe enfrentarse a hordas de enemigos en combates por turnos, administrando estratégicamente su capacidad de inventario limitada para sobrevivir.

---

## 3. Estructura de Archivos (Guía 1)
El proyecto cumple con la estructura modular exigida:

```text
The_Ballad_of_Nyx/
├── main.py          # Módulo principal: Menú, selección de dios, crafteo y combate.
├── inventario.py    # Módulo de datos: Operaciones del inventario usando listas.
└── README.md        # Documentación general del proyecto.

```

---

## 4. Mecánica del Inventario con Listas (Semana 3)

La manipulación del inventario de Nyx se apoya en los métodos nativos de listas en Python:

### A. Agregar Objetos (`Add_item_to_inventory`)

Valida que la longitud actual de la lista no alcance ni supere la capacidad máxima (`max_capacity`) antes de añadir un nuevo elemento al final mediante `.append()`.

```python
def Add_item_to_inventory(inventory, item, max_capacity):
    if len(inventory) >= max_capacity:
        print("Inventory is full! Cannot add more items.")
        return
    inventory.append(item)
    print(f"{item} has been added to your inventory.")
    return inventory

```

### B. Usar Objetos (`use_item`)

Muestra la lista de ítems numerada a partir de 1 usando `enumerate(inventory, 1)`. Convierte la opción del jugador a un índice (`choice_idx = int(choice) - 1`), aplica los efectos sobre la salud (`health`), maná (`mp`) o daño de la entidad correspondiente, y elimina el ítem de la lista con `.pop(choice_idx)`.

```python
# Enumeración para selección por índice
for idx, item in enumerate(inventory, 1):
    print(f"{idx}. {item}")

# Extracción y eliminación del objeto usado
inventory.pop(choice_idx)

```

### C. Soltar Objetos (`throw_item`)

Permite descartar la carga del jugador vaciando la lista completa con el método `.clear()`.

```python
def throw_item(inventory):
    if not inventory:
        print("Your inventory is empty!")
        return
    print("You throw all items in your inventory away!")
    inventory.clear()

```

---

## 5. Pseudocódigo y Diagrama de Flujo (Guía 2)

### Pseudocódigo de la Mecánica `use_item`

```text
Función use_item(inventory, Nyx, items, Gods):
    Si inventory está vacío Entonces
        Escribir "Your inventory is empty!"
        Retornar
    FinSi

    Escribir "\nInventory:"
    Para cada (idx, item) en Enumerar(inventory, 1) Hacer
        Escribir idx + ". " + item
    FinPara

    Leer choice
    Si choice en minúsculas es igual a 'cancel' Entonces
        Retornar
    FinSi

    Intentar:
        choice_idx = ConvertirAEntero(choice) - 1
        Si 0 <= choice_idx Y choice_idx < Longitud(inventory) Entonces
            item = inventory[choice_idx]
            Escribir "You used " + item
            
            Si item existe en items Entonces
                effect = items[item]["effect"]
                value = items[item]["value"]
                
                Si effect == "heal" Entonces
                    Nyx["health"] = Nyx["health"] + value
                Sino Si effect == "restore_mp" Entonces
                    Nyx["mp"] = Nyx["mp"] + value
                Sino Si effect == "buff" Entonces
                    Gods[Nyx["ally_god"]]["damage"] += value
                FinSi
            FinSi
            
            Eliminar elemento en índice choice_idx de inventory
        Sino:
            Escribir "Invalid selection."
        FinSi
    Capturar ErrorDeValor:
        Escribir "Invalid input. Please enter a number."
FinFunción

```
![Diagrama de Flujo del Inventario](diagrama_flujo.png)
