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

### A. Cola de Turnos y Eventos (eventos.py) - Uso de deque
* **Estructura elegida:** `collections.deque` (Double-Ended Queue).
* **Justificación algorítmica:** La gestión de turnos de combate y el flujo de eventos secuenciales del mapa opera bajo la regla FIFO (First-In, First-Out), donde el primero en entrar debe ser el primero en salir. Si utilizáramos una lista tradicional de Python (list) para extraer al elemento actual del inicio mediante list.pop(0), el intérprete estaría obligado a desplazar todos los elementos restantes una posición hacia atrás en la memoria, generando una complejidad lineal ineficiente de O(n). Para solucionar esto, implementamos deque, la cual está programada a bajo nivel en C. Esta estructura nos permite insertar elementos al final con .append() y extraer el turno o evento actual desde el inicio con .popleft(), logrando un tiempo estrictamente constante de O(1) en ambas operaciones y evitando cuellos de botella durante los combates de Nyx.
* **Fragmento de implementación**: 

from collections import deque

# Definimos la cola usando 'deque' para garantizar operaciones O(1) en ambos extremos
cola_turnos = deque()

def agregar_turno(entidad):
    """
    Operación ENQUEUE: Agrega un personaje, enemigo o evento al final de la fila (O(1)).
    """
    cola_turnos.append(entidad)
    print(f"[Sistema] '{entidad}' ha entrado a la cola.")

def siguiente_turno():
    """
    Operación DEQUEUE: Quita y devuelve la entidad/evento que está al frente de la fila (O(1)).
    """
    if len(cola_turnos) == 0: 
        return None
    
    # Extraemos al PRIMER elemento que ingresó (Regla FIFO mediante popleft)
    turno_actual = cola_turnos.popleft()
    return turno_actual

### B. Historial de Acciones y Retroceso (`historial.py`) - Uso de Pila (Stack)
* **Estructura elegida:** Lista de Python operada bajo el principio LIFO (*Last In, First Out*).
* **Justificación algorítmica:** La mecánica de "deshacer" (*undo*) exige que la última acción ejecutada sea exactamente la última en ser retirada para revertir el estado del juego. Empleando `.append()` para apilar (*push*) y `.pop()` para desapilar (*pop*) el último registro en el extremo derecho de la lista, garantizamos una complejidad temporal de O(1) en ambas operaciones clave sin penalizar el rendimiento del bucle principal.

---

## 5. Árbol de la Mazmorra y Decisiones de Diseño (`mazmorra.py`)
- **Estructura de Exploración:** Las salas y rutas se generan mediante algoritmos recursivos de ramificación variable y control de profundidad, modelando un **Árbol de Decisiones** donde las elecciones de la jugadora abren nuevos caminos asimétricos.

### Representación del Árbol de la Mazmorra
A continuación se ilustra un ejemplo real del árbol generado por nuestro algoritmo de divide y conquista con ramificación aleatoria (de 1 a 3 puertas) y control de profundidad máxima (Nivel 2), representado mediante texto con sangría:

```text
Ancient Cave (Raíz - Nivel 0)
├── Isolated Island (Nivel 1)
│   ├── Dead Forest (Nivel 2 - Callejón sin salida)
│   ├── Strange Volcano (Nivel 2 - Callejón sin salida)
│   └── Forgotten Crypt (Nivel 2 - Callejón sin salida)
└── Ruined Temple (Nivel 1)
    ├── Abyssal Lake (Nivel 2 - Callejón sin salida)
    └── Dark Altar (Nivel 2 - Callejón sin salida)

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
Muestra la lista de ítems numerada a partir de 1 usando enumerate(inventory, 1). Convierte la opción del jugador a un índice (choice_idx = int(choice) - 1), aplica los efectos correspondientes sobre la salud, maná o poder de ataque del dios aliado, y elimina el ítem de la lista en tiempo real mediante .pop(choice_idx). `

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

## 7. Aportes individuales de los integrantes:
*    [Esteban Ademir Cañas Rojas / ademir1234-dot]: Responsable de la integración y lógica principal del Checkpoint 2. Lideró la reestructuración del archivo main.py para unificar el inventario, el combate y la exploración en un bucle jugable, implementó la validación de casos límite (manejo de inputs y prevención de crasheos) y realizó el ajuste de la experiencia de usuario (traducción de menús e inmersión narrativa).

*    [Louis Alejandro Soto / UnspokenLegion]: Responsable de la arquitectura y el control de versiones del repositorio en GitHub. Se encargó del manejo inicial del proyecto, la gestión del Pull Request de la entrega anterior, las capturas de la evidencia y la redacción del esqueleto base de la documentación técnica en este archivo README.

*    [Carlos Mario Alas Parada / MarioAlas06]: Responsables de la documentación teórica exigida por el sílabo, incluyendo la elaboración de los diagramas de flujo, la creación de la tabla de análisis de complejidad temporal y la actualización del pseudocódigo para las mecánicas evaluadas en las Semanas 5, 6 y 7.

## 8. Evidencia de ejecución
Revisar documento adjunto en el repositorio
