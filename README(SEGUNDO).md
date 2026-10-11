
# Aventura Algorítmica: The Ballad of Nyx

---

## 1. Explicación Breve y Decisiones del Equipo
En esta segunda fase del proyecto (*Checkpoint 2*, semanas 1 a 9), hemos integrado de forma modular los componentes avanzados del juego: la gestión de inventario en `inventario.py`, la pila de historial y retroceso en `historial.py`, la cola de turnos y eventos en `eventos.py`, y la generación recursiva de mazmorras en `mazmorra.py`. Siguiendo estrictamente la regla de "un archivo, una responsabilidad", cada submódulo maneja su propia lógica de datos y se comunica con `main.py` mediante importaciones limpias. Las decisiones de diseño se enfocaron en garantizar un rendimiento óptimo (O(1)) mediante el uso de estructuras nativas de Python adaptadas a las necesidades tácticas y narrativas de Nyx.

---

## 2. Guía de Inicio y Cómo Jugar
Para desplegar y jugar *The Ballad of Nyx* desde tu terminal:

1. Clona el repositorio asegurándote de mantener la siguiente estructura modular de archivos:
   ```text
   The_Ballad_of_Nyx/
   ├── main.py          # Módulo principal y bucle de juego
   ├── inventario.py    # Gestión de ítems con listas (Semana 3)
   ├── historial.py     # Pila (Stack) para deshacer acciones (Semana 5)
   ├── eventos.py       # Cola (Queue) de turnos y eventos (Semana 6)
   ├── mazmorra.py      # Generación recursiva de salas (Semana 7)
   └── README.md        # Documentación técnica

2. Abre tu terminal en la carpeta raíz del proyecto y ejecuta:
python main.py

3. Mecánicas en la Consola:
Selecciona tu deidad aliada para definir los bonificaciones de elemento y daño.
Administra tu inventario, craftea elixires y enfréntate a enemigos en combates por turnos ordenados mediante una cola eficiente.
Explora las salas ramificadas de la mazmorra y utiliza el sistema de historial para deshacer movimientos o acciones erróneas cuando lo necesites.


## 3. Concepto del Juego (Semana 1)
- **Mundo:** Un universo de fantasía oscura donde la magia elemental y el favor de los dioses olímpicos dictan el destino de los guerreros.
- **Protagonista:** Nyx Rigel, una guerrera que canaliza el poder, armas y elementos del dios que elija como aliado.
- **Antagonista:** Criaturas elementales y espectros oscuros (Fire Fiend, Water Zombie, Earth Golem, Vengeful Spirit, Mind Flayer) que amenazan el balance.
- **Objeto Especial:** Reliquias, elixires y plantas medicinales (`herbs`, `ginsing`, `health_potion`, `mana_potion`, `strength_elixir`) que restauran salud, maná o mejoran el ataque.
- **Problema a Resolver:** Nyx debe sobrevivir a hordas de enemigos y navegar por laberintos oscuros administrando estratégicamente su inventario y sus decisiones tácticas.

---

## 4. Justificación Técnica y Complejidad O(1) de las Estructuras de Datos

### A. Cola de Turnos y Eventos (`eventos.py`) - Uso de `deque`
* **Estructura elegida:** `collections.deque` (Double-Ended Queue).
* **Justificación algorítmica:** La gestión de turnos de combate y eventos secuenciales requiere insertar nuevos elementos al final y extraer al elemento actual del inicio de manera constante. Si utilizáramos una lista tradicional de Python (`list`) para eliminar el primer elemento (`pop(0)`), el programa estaría obligado a desplazar todos los elementos restantes en la memoria uno a uno, lo que genera un costo de tiempo de O(N). Al utilizar `deque`, implementada en C a bajo nivel, logramos insertar (`append`) y extraer (`popleft`) elementos en los extremos en un tiempo estrictamente constante de O(1), evitando cuellos de botella ante flujos extensos de turnos.

### B. Historial de Acciones y Retroceso (`historial.py`) - Uso de Pila (Stack)
* **Estructura elegida:** Lista de Python operada bajo el principio LIFO (*Last In, First Out*).
* **Justificación algorítmica:** La mecánica de "deshacer" (*undo*) exige que la última acción ejecutada sea exactamente la última en ser retirada para revertir el estado del juego. Empleando `.append()` para apilar (*push*) y `.pop()` para desapilar (*pop*) el último registro en el extremo derecho de la lista, garantizamos una complejidad temporal de O(1) en ambas operaciones clave sin penalizar el rendimiento del bucle principal.

---

## 5. Árbol de la Mazmorra y Decisiones de Diseño (`mazmorra.py`)
* **Estructura de Exploración:** Las salas y rutas se generan mediante algoritmos recursivos de ramificación variable y control de profundidad, modelando un **Árbol de Decisiones** donde las elecciones de la jugadora abren nuevos caminos asimétricos.
* **Sincronización de Eventos e Historial al Deshacer:** Una decisión crítica de diseño en este checkpoint ocurre cuando el jugador activa la función de retroceso (`undo`) dentro de la mazmorra:
  * Al deshacer un movimiento (`tipo == "moverse"`), el sistema recupera la sala anterior mediante la pila del historial.
  * *¿Qué pasa con los eventos?* Sincronizar la posición espacial asegura que los eventos de entorno asociados queden alineados con el nodo padre inmediato del árbol de mazmorras, previniendo incongruencias lógicas como habitar salas a las que aún no se ha ingresado o mantener estados de combate ya resueltos.

## 6. Mecánica del Inventario con Listas (`inventario.py`)

La manipulación del inventario de Nyx se apoya en los métodos nativos de listas en Python:

### A. Agregar Objetos (`Add_item_to_inventory`)
Valida que la longitud actual de la lista no alcance ni supere la capacidad máxima (`max_capacity`) antes de añadir un nuevo elemento al final mediante `.append()`. Además, registra la acción en la pila del historial.

```
python
def Add_item_to_inventory(inventory, item, max_capacity):
    if len(inventory) >= max_capacity:
        print("Inventory is full! Cannot add more items.")
        return
    inventory.append(item)
    print(f"{item} has been added to your inventory.")
    
    # Registramos la acción en la Pila
    historial.registrar_accion("recoger", {"item": item})
```
    
    return inventory
### B. Usar Objetos (`use_item`)
Muestra la lista de ítems numerada a partir de 1 usando enumerate(inventory, 1). Convierte la opción del jugador a un índice (choice_idx = int(choice) - 1), aplica los efectos correspondientes sobre la salud, maná o poder de ataque del dios aliado, y elimina el ítem de la lista en tiempo real mediante .pop(choice_idx). `)

```
# Enumeración para selección por índice
for idx, item in enumerate(inventory, 1):
    print(f"{idx}. {item}")

# Extracción y eliminación del objeto usado
inventory.pop(choice_idx)
```

### C. Soltar Objetos (`throw_item`)
Permite descartar la carga del jugador guardando una copia exacta del inventario previo en el historial y vaciando la lista completa con el método .clear(). 

```
def throw_item(inventory):
    if not inventory:
        print("Your inventory is empty!")
        return
        
    # Hacemos una copia exacta y la apilamos antes de borrar
    historial.registrar_accion("tirar_todo", {"inventario_previo": inventory.copy()})
    
    print("You throw all items in your inventory away!")
    inventory.clear()
```
