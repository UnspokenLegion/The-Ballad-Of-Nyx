"""
Archivo: arboles.py
Proyecto: Aventura Algorítmica - The Ballad of Nyx
Integrantes: Esteban Ademir Cañas Rojas, Louis Alejandro Soto, Carlos Mario Alas Parada
Asignatura: Estructura de Datos y Algoritmos Computacionales (CS2001) - Semana 14
Objetivo: Implementación de Árbol de Misiones (dependencias y recorridos recursivos)
          y Árbol de Decisión (IA de enemigo) sin librerías externas.
"""

# ==============================================================================
# 1. ÁRBOL DE MISIONES Y DEPENDENCIAS (Indicaciones 2 y 5)
# ==============================================================================

class Nodo:
    """
    Representa una misión dentro del árbol de misiones de The Ballad of Nyx.
    Cada nodo tiene un único padre (propiedad de árbol: n - 1 aristas, sin ciclos).
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []
        self.completada = False

    def agregar_hijo(self, nodo_hijo):
        """
        Agrega una misión hija que depende directamente de esta misión.
        Complejidad: O(1), ya que append() inserta al final de la lista de hijos.
        """
        self.hijos.append(nodo_hijo)


def preorden(nodo, nivel=0):
    """
    Recorrido en Preorden (raíz -> hijos de izquierda a derecha) usando DFS recursivo.
    Imprime el árbol con sangría según su nivel (profundidad) y su estado actual.
    Complejidad: O(n), porque visita exactamente una vez cada uno de los n nodos.
    """
    if nodo is None:
        return

    estado = "[✓ Completada]" if nodo.completada else "[🔒 Pendiente]"
    sangria = "    " * nivel
    prefijo = "└── " if nivel > 0 else ""
    print(f"{sangria}{prefijo}{nodo.nombre} {estado} (Nivel {nivel})")

    for hijo in nodo.hijos:
        preorden(hijo, nivel + 1)


def inorden_ejemplo(nodo, resultado=None):
    """
    Recorrido en Inorden (primer hijo -> raíz -> resto de hijos) recursivo.
    Complejidad: O(n), visita todos los nodos del árbol.
    """
    if resultado is None:
        resultado = []
    if nodo is None:
        return resultado

    if len(nodo.hijos) > 0:
        inorden_ejemplo(nodo.hijos[0], resultado)
    resultado.append(nodo.nombre)
    for hijo in nodo.hijos[1:]:
        inorden_ejemplo(hijo, resultado)
    return resultado


def postorden_ejemplo(nodo, resultado=None):
    """
    Recorrido en Postorden (todos los hijos -> raíz al final) recursivo.
    Complejidad: O(n), visita todos los nodos del árbol.
    """
    if resultado is None:
        resultado = []
    if nodo is None:
        return resultado

    for hijo in nodo.hijos:
        postorden_ejemplo(hijo, resultado)
    resultado.append(nodo.nombre)
    return resultado


def altura(nodo):
    """
    Calcula recursivamente la altura del árbol (aristas desde la raíz hasta la hoja más lejana).
    Una hoja tiene altura 0.
    Complejidad: O(n), explora todos los subárboles para hallar el camino más largo.
    """
    if nodo is None or len(nodo.hijos) == 0:
        return 0

    alturas_hijos = [altura(hijo) for hijo in nodo.hijos]
    return 1 + max(alturas_hijos)


def contar_hojas(nodo):
    """
    Cuenta recursivamente cuántas hojas (misiones finales sin hijos) tiene el árbol.
    Complejidad: O(n), recorre todos los nodos verificando cuáles no tienen hijos.
    """
    if nodo is None:
        return 0

    if len(nodo.hijos) == 0:
        return 1

    total = 0
    for hijo in nodo.hijos:
        total += contar_hojas(hijo)
    return total


def obtener_hojas(nodo, lista_hojas=None):
    """
    Devuelve una lista con los nombres de todas las hojas del árbol.
    Complejidad: O(n).
    """
    if lista_hojas is None:
        lista_hojas = []
    if nodo is None:
        return lista_hojas

    if len(nodo.hijos) == 0:
        lista_hojas.append(nodo.nombre)
    else:
        for hijo in nodo.hijos:
            obtener_hojas(hijo, lista_hojas)
    return lista_hojas


def misiones_disponibles(nodo, padre_completado=True, disponibles=None):
    """
    Devuelve las misiones que NO están completadas, pero cuyo padre SÍ lo está.
    Complejidad: O(n) en el peor caso.
    """
    if disponibles is None:
        disponibles = []
    if nodo is None:
        return disponibles

    if not padre_completado:
        return disponibles

    if not nodo.completada:
        disponibles.append(nodo.nombre)
    else:
        for hijo in nodo.hijos:
            misiones_disponibles(hijo, True, disponibles)

    return disponibles


def listar_todas_las_misiones(nodo, lista=None):
    """
    Devuelve todos los objetos Nodo en preorden para poder elegirlos por número.
    Complejidad: O(n).
    """
    if lista is None:
        lista = []
    if nodo is None:
        return lista
    lista.append(nodo)
    for hijo in nodo.hijos:
        listar_todas_las_misiones(hijo, lista)
    return lista


def buscar_mision_y_padre(nodo_actual, nombre_buscado, padre=None):
    """
    Busca recursivamente una misión por nombre y devuelve (nodo, padre).
    Complejidad: O(n).
    """
    if nodo_actual is None:
        return None, None

    if nodo_actual.nombre.lower() == nombre_buscado.lower():
        return nodo_actual, padre

    for hijo in nodo_actual.hijos:
        encontrado, padre_encontrado = buscar_mision_y_padre(hijo, nombre_buscado, nodo_actual)
        if encontrado is not None:
            return encontrado, padre_encontrado

    return None, None


def completar_mision(raiz, nombre_mision):
    """
    Intenta completar una misión validando que su misión padre ya esté completada.
    Complejidad: O(n) por la búsqueda recursiva del nodo en el árbol.
    """
    nodo_mision, nodo_padre = buscar_mision_y_padre(raiz, nombre_mision)

    if nodo_mision is None:
        print(f"  [✘ Error] La misión '{nombre_mision}' no existe en el árbol.")
        return False

    if nodo_mision.completada:
        print(f"  [!] La misión '{nodo_mision.nombre}' ya estaba completada.")
        return False

    if nodo_padre is not None and not nodo_padre.completada:
        print(
            f"  [🔒 BLOQUEADA] No puedes completar '{nodo_mision.nombre}'.\n"
            f"                 Requisito pendiente (Padre): '{nodo_padre.nombre}'."
        )
        return False

    nodo_mision.completada = True
    print(f"  [✓ ÉXITO] ¡Misión completada: '{nodo_mision.nombre}'!")
    if len(nodo_mision.hijos) > 0:
        nuevas = [h.nombre for h in nodo_mision.hijos]
        print(f"            -> Nuevas misiones desbloqueadas: {nuevas}")
    else:
        print("            -> ¡Has completado una misión hoja (final de rama)!")
    return True


def construir_arbol_misiones_nyx():
    """
    Construye el árbol de misiones de The Ballad of Nyx (9 misiones, 4 niveles, altura 3).
    """
    m1 = Nodo("M1: Despertar en Ancient Cave")
    m2 = Nodo("M2: Pacto con Apolo (Solar Bow)")
    m3 = Nodo("M3: Pacto con Poseidon (Trident)")
    m4 = Nodo("M4: Purificar Dead Forest")
    m5 = Nodo("M5: Recuperar Reliquia en Forgotten Crypt")
    m7 = Nodo("M7: Derrotar al Fire Fiend en Strange Volcano")
    m6 = Nodo("M6: Explorar Isolated Island")
    m8 = Nodo("M8: Sumergirse en Abyssal Lake")
    m9 = Nodo("M9: Vencer al Mind Flayer en Ruined Temple")

    m1.agregar_hijo(m2)
    m1.agregar_hijo(m3)

    m2.agregar_hijo(m4)
    m2.agregar_hijo(m5)
    m4.agregar_hijo(m7)

    m3.agregar_hijo(m6)
    m3.agregar_hijo(m8)
    m8.agregar_hijo(m9)

    return m1


# ==============================================================================
# 2. ÁRBOL DE DECISIÓN DEL ENEMIGO (Indicación 3)
# ==============================================================================

class NodoDecision:
    """
    Nodo para el Árbol de Decisión Binario del enemigo (Mind Flayer).
    """
    def __init__(self, pregunta=None, clave=None, umbral=None, decision=None):
        self.pregunta = pregunta
        self.clave = clave
        self.umbral = umbral
        self.decision = decision
        self.si = None
        self.no = None

    def es_hoja(self):
        return self.decision is not None


def evaluar_pregunta(nodo, situacion):
    """
    Evalúa la pregunta del nodo interno contra el diccionario 'situacion'.
    Complejidad: O(1).
    """
    valor = situacion.get(nodo.clave)
    if isinstance(nodo.umbral, bool):
        return bool(valor) == nodo.umbral
    if isinstance(nodo.umbral, (int, float)):
        return valor < nodo.umbral
    return False


def decidir(nodo, situacion, camino=None):
    """
    Baja recursivamente desde la raíz hasta una hoja haciendo una pregunta a la vez.
    Complejidad: O(h), donde h es la altura del árbol (o O(n) si fuera degenerado).
    """
    if camino is None:
        camino = []

    if nodo.es_hoja():
        return nodo.decision, camino

    respuesta = evaluar_pregunta(nodo, situacion)
    if respuesta:
        camino.append(f"{nodo.pregunta} -> SÍ")
        return decidir(nodo.si, situacion, camino)
    else:
        camino.append(f"{nodo.pregunta} -> NO")
        return decidir(nodo.no, situacion, camino)


def construir_arbol_decision_enemigo():
    """
    Construye el Árbol de Decisión del jefe 'Mind Flayer' (4 preguntas, 5 hojas, altura 3).
    """
    p1_vida_baja = NodoDecision(
        pregunta="¿Vida del Mind Flayer < 30?",
        clave="vida_enemigo",
        umbral=30
    )
    p2_tiene_elixir = NodoDecision(
        pregunta="¿Tiene Elixir Oscuro para curarse?",
        clave="tiene_elixir",
        umbral=True
    )
    p3_jugador_cerca = NodoDecision(
        pregunta="¿Nyx está cerca (distancia <= 3)?",
        clave="jugador_cerca",
        umbral=True
    )
    p4_debilidad_activa = NodoDecision(
        pregunta="¿Nyx usa a Ares (elemento Rage, debilidad del Mind Flayer)?",
        clave="nyx_usa_ares",
        umbral=True
    )

    h1_curarse = NodoDecision(decision="Beber Elixir Oscuro y regenerar salud")
    h2_huir = NodoDecision(decision="Teletransportarse a las sombras (Huir)")
    h3_escudo = NodoDecision(decision="Invocar Barrera Psíquica (Defenderse de Ares)")
    h4_ataque_mental = NodoDecision(decision="Lanzar Explosión Mental (Ataque directo de 20 daño)")
    h5_patrullar = NodoDecision(decision="Acechar desde las sombras y acercarse a Nyx (Patrullar)")

    p1_vida_baja.si = p2_tiene_elixir
    p1_vida_baja.no = p3_jugador_cerca

    p2_tiene_elixir.si = h1_curarse
    p2_tiene_elixir.no = h2_huir

    p3_jugador_cerca.si = p4_debilidad_activa
    p3_jugador_cerca.no = h5_patrullar

    p4_debilidad_activa.si = h3_escudo
    p4_debilidad_activa.no = h4_ataque_mental

    return p1_vida_baja


# ==============================================================================
# 3. DEMO EN VIVO Y MODO INTERACTIVO (Indicaciones 4 y 8)
# ==============================================================================

def menu_interactivo(raiz_misiones, arbol_ia):
    """
    Menú interactivo para realizar pruebas adicionales en vivo.
    """
    while True:
        print("\n" + "=" * 78)
        print("  MENÚ INTERACTIVO DE PRUEBAS EN VIVO")
        print("=" * 78)
        print("  1. Ver árbol de misiones actual (Preorden), altura, hojas y disponibles")
        print("  2. Completar una misión manualmente (eligiendo por número)")
        print("  3. Agregar una nueva misión hija en vivo")
        print("  4. Probar el Árbol de Decisión del Mind Flayer con nuevos parámetros")
        print("  5. Comparar recorridos Preorden, Inorden y Postorden del árbol actual")
        print("  6. Salir")

        opcion = input("\nElige una opción (1-6): ").strip()

        if opcion == "1":
            print("\n--- ÁRBOL DE MISIONES ACTUAL ---")
            preorden(raiz_misiones)
            print(f"\n  * Altura actual: {altura(raiz_misiones)}")
            print(f"  * Hojas ({contar_hojas(raiz_misiones)}): {obtener_hojas(raiz_misiones)}")
            print(f"  * Misiones disponibles: {misiones_disponibles(raiz_misiones)}")

        elif opcion == "2":
            todas = listar_todas_las_misiones(raiz_misiones)
            print("\nElige el número de la misión que deseas intentar completar:")
            for i, nodo in enumerate(todas, 1):
                estado = "✓ Completada" if nodo.completada else "🔒 Pendiente"
                print(f"  {i}) {nodo.nombre} [{estado}]")
            try:
                idx = int(input("Número de misión: ")) - 1
                if 0 <= idx < len(todas):
                    completar_mision(raiz_misiones, todas[idx].nombre)
                    print(f"  * Misiones disponibles ahora: {misiones_disponibles(raiz_misiones)}")
                else:
                    print("  [✘] Número fuera de rango.")
            except ValueError:
                print("  [✘] Entrada inválida. Ingresa un número.")

        elif opcion == "3":
            todas = listar_todas_las_misiones(raiz_misiones)
            print("\n¿De qué misión será hija la nueva misión?")
            for i, nodo in enumerate(todas, 1):
                print(f"  {i}) {nodo.nombre}")
            try:
                idx = int(input("Número de la misión padre: ")) - 1
                if 0 <= idx < len(todas):
                    nuevo_nombre = input("Nombre de la nueva misión: ").strip()
                    if nuevo_nombre:
                        todas[idx].agregar_hijo(Nodo(nuevo_nombre))
                        print(f"\n  [✓] Misión '{nuevo_nombre}' agregada como hija de '{todas[idx].nombre}'.")
                        print("  Nuevo recorrido en Preorden:")
                        preorden(raiz_misiones)
                else:
                    print("  [✘] Número fuera de rango.")
            except ValueError:
                print("  [✘] Entrada inválida.")

        elif opcion == "4":
            print("\n--- CONFIGURAR SITUACIÓN PARA EL MIND FLAYER ---")
            try:
                vida = int(input("  1. Vida del Mind Flayer (ej. 15 o 50): "))
                elixir = input("  2. ¿Tiene Elixir Oscuro? (s/n): ").strip().lower() == "s"
                cerca = input("  3. ¿Nyx está cerca? (s/n): ").strip().lower() == "s"
                ares = input("  4. ¿Nyx usa a Ares/Rage? (s/n): ").strip().lower() == "s"

                situacion_custom = {
                    "vida_enemigo": vida,
                    "tiene_elixir": elixir,
                    "jugador_cerca": cerca,
                    "nyx_usa_ares": ares
                }
                decision_final, ruta = decidir(arbol_ia, situacion_custom)
                print(f"\n  Diccionario evaluado : {situacion_custom}")
                print(f"  Camino recorrido     : {'  -->  '.join(ruta)}")
                print(f"  [DECISIÓN TOMADA]    : {decision_final}")
            except ValueError:
                print("  [✘] La vida debe ser un número entero.")

        elif opcion == "5":
            print("\n--- COMPARACIÓN DE LOS 3 RECORRIDOS DFS ---")
            print("  1. PREORDEN (Raíz antes)  :", [n.nombre for n in listar_todas_las_misiones(raiz_misiones)])
            print("  2. INORDEN (Raíz en medio):", inorden_ejemplo(raiz_misiones))
            print("  3. POSTORDEN (Raíz final) :", postorden_ejemplo(raiz_misiones))

        elif opcion == "6":
            print("\nFinalizando ejecución de The Ballad of Nyx.")
            break
        else:
            print("  [✘] Opción no válida. Elige entre 1 y 6.")


def main():
    print("=" * 78)
    print("  THE BALLAD OF NYX - ÁRBOLES, ÁRBOLES DE DECISIÓN Y DEPENDENCIAS")
    print("=" * 78)

    raiz_misiones = construir_arbol_misiones_nyx()
    arbol_ia = construir_arbol_decision_enemigo()

    # --------------------------------------------------------------------------
    # SECCIÓN 1: Estructura del Árbol de Misiones y Recorrido en Preorden
    # (Guía interna: Exposición de Bloques 1 y 2 - Esteban)
    # --------------------------------------------------------------------------
    print("\n[1] ÁRBOL DE MISIONES DE NYX (Recorrido en Preorden / DFS):")
    print("-" * 78)
    preorden(raiz_misiones)
    print("-" * 78)
    print(f"  * Misión Raíz (Nivel 0) : {raiz_misiones.nombre}")
    print(f"  * Altura del árbol (h)  : {altura(raiz_misiones)} (aristas desde la raíz a la hoja más lejana)")
    print(f"  * Total de hojas        : {contar_hojas(raiz_misiones)} -> {obtener_hojas(raiz_misiones)}")
    print(f"  * Misiones disponibles al inicio: {misiones_disponibles(raiz_misiones)}")

    input("\n[Presiona ENTER para continuar...]")

    # --------------------------------------------------------------------------
    # SECCIÓN 2: Árbol de Decisión del Enemigo (Mind Flayer)
    # (Guía interna: Exposición de Bloque 4 - Louis)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("[2] ÁRBOL DE DECISIÓN DEL ENEMIGO (Jefe: MIND FLAYER):")
    print("=" * 78)

    situaciones_prueba = [
        {
            "nombre_escenario": "Situación 1: Mind Flayer herido (<30 vida) y SIN Elixir Oscuro",
            "datos": {"vida_enemigo": 15, "tiene_elixir": False, "jugador_cerca": True, "nyx_usa_ares": False}
        },
        {
            "nombre_escenario": "Situación 2: Mind Flayer sano, Nyx está cerca con su arco de Apolo",
            "datos": {"vida_enemigo": 40, "tiene_elixir": True, "jugador_cerca": True, "nyx_usa_ares": False}
        },
        {
            "nombre_escenario": "Situación 3: Mind Flayer sano, Nyx está cerca usando a ARES (su debilidad)",
            "datos": {"vida_enemigo": 40, "tiene_elixir": True, "jugador_cerca": True, "nyx_usa_ares": True}
        },
        {
            "nombre_escenario": "Situación 4: Mind Flayer sano, pero Nyx está lejos explorando otra sala",
            "datos": {"vida_enemigo": 40, "tiene_elixir": True, "jugador_cerca": False, "nyx_usa_ares": False}
        }
    ]

    for caso in situaciones_prueba:
        decision_final, ruta = decidir(arbol_ia, caso["datos"])
        print(f"\n* {caso['nombre_escenario']}")
        print(f"  Diccionario situacion : {caso['datos']}")
        print(f"  Camino (O(h), {len(ruta)} preg.): {'  -->  '.join(ruta)}")
        print(f"  [DECISIÓN DEL ENEMIGO]: {decision_final}")

    input("\n[Presiona ENTER para continuar...]")

    # --------------------------------------------------------------------------
    # SECCIÓN 3: Dependencias y Desbloqueo de Misiones
    # (Guía interna: Exposición de Bloque 5 - Carlos Mario)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("[3] SISTEMA DE DEPENDENCIAS Y DESBLOQUEO DE MISIONES:")
    print("=" * 78)

    print("\n>>> Prueba 1: Intentar completar una misión bloqueada de Nivel 3 ('M7: Derrotar al Fire Fiend'):")
    completar_mision(raiz_misiones, "M7: Derrotar al Fire Fiend en Strange Volcano")

    input("\n[Presiona ENTER para completar la misión Raíz (M1)...]")
    print("\n>>> Prueba 2: Completar la misión Raíz (M1):")
    completar_mision(raiz_misiones, "M1: Despertar en Ancient Cave")
    print(f"    Misiones disponibles ahora: {misiones_disponibles(raiz_misiones)}")

    input("\n[Presiona ENTER para completar la segunda misión (M2 - Pacto con Apolo)...]")
    print("\n>>> Prueba 3: Completar 'M2: Pacto con Apolo (Solar Bow)':")
    completar_mision(raiz_misiones, "M2: Pacto con Apolo (Solar Bow)")
    print(f"    Misiones disponibles ahora: {misiones_disponibles(raiz_misiones)}")

    print("\n>>> Estado actualizado del Árbol de Misiones:")
    print("-" * 78)
    preorden(raiz_misiones)

    # --------------------------------------------------------------------------
    # SECCIÓN 4: Menú Interactivo Opcional (para preguntas de la defensa)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("  DEMOSTRACIÓN PRINCIPAL FINALIZADA")
    print("=" * 78)
    entrar = input("\n¿Deseas abrir el menú interactivo de pruebas adicionales? (s/n): ").strip().lower()
    if entrar == "s":
        menu_interactivo(raiz_misiones, arbol_ia)


if __name__ == "__main__":
    main()