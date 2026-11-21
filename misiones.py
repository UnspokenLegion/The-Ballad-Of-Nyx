"""
Módulo: misiones.py
Proyecto: Aventura Algorítmica - The Ballad of Nyx
Objetivo: Árbol de misiones de Nyx (Semana 14, Checkpoint 3).
          Cada misión depende de su misión padre: no se puede completar
          una misión si su padre aún no está completada.
Nota: este módulo NO usa input() ni pausas; solo lógica del árbol.
"""

from collections import deque

class Nodo:
    def __init__(self, id_mision, nombre, sala, recompensa_item=None, abre_santuario=False):
        self.id = id_mision                      # Ej: "M1"
        self.nombre = nombre
        self.sala = sala                         # Sala del grafo donde ocurre
        self.recompensa_item = recompensa_item   # Ítem que se entrega al completarla
        self.abre_santuario = abre_santuario     # True = conecta el Santuario Oculto
        self.completada = False
        self.padre = None
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        nodo_hijo.padre = self
        self.hijos.append(nodo_hijo)

    def esta_bloqueada(self):
        return self.padre is not None and not self.padre.completada

    def estado(self):
        """Devuelve 'completada', 'bloqueada' o 'disponible'."""
        if self.completada:
            return "completada"
        if self.esta_bloqueada():
            return "bloqueada"
        return "disponible"


ETIQUETAS = {
    "completada": "[OK] Completada",
    "disponible": "[>>] Disponible",
    "bloqueada": "[XX] Bloqueada",
}


def preorden(nodo, nivel=0):
    """Recorrido Preorden: imprime el árbol con sangría y el estado de cada misión."""
    if nodo is None:
        return

    sangria = "    " * nivel
    prefijo = "+-- " if nivel > 0 else ""
    print(f"{sangria}{prefijo}{nodo.id}: {nodo.nombre} {ETIQUETAS[nodo.estado()]} (Sala: {nodo.sala})")

    for hijo in nodo.hijos:
        preorden(hijo, nivel + 1)


def normalizar_id(texto):
    """Convierte lo que escribe el jugador a un ID válido: ' m4 ' -> 'M4', '4' -> 'M4'."""
    if texto is None:
        return ""
    texto = str(texto).strip().upper()
    if texto.isdigit():
        texto = "M" + texto
    return texto


def buscar_mision(nodo, id_buscado):
    """Busca una misión por ID (recursivo). Devuelve el nodo o None (nunca lanza error)."""
    objetivo = normalizar_id(id_buscado)
    if nodo is None or objetivo == "":
        return None

    if nodo.id.upper() == objetivo:
        return nodo

    for hijo in nodo.hijos:
        encontrado = buscar_mision(hijo, objetivo)
        if encontrado is not None:
            return encontrado

    return None


def completar_mision(raiz, id_mision):
    """
    Intenta completar una misión.
    Devuelve (exito, nodo). Nunca lanza errores por entradas raras.
    """
    texto = str(id_mision).strip()
    nodo = buscar_mision(raiz, texto)

    if nodo is None:
        print(f"  [X Error] La misión '{texto or '(vacío)'}' no existe en el árbol.")
        return False, None

    if nodo.completada:
        print(f"  [!] La misión '{nodo.id}' ya estaba completada.")
        return False, nodo

    if nodo.esta_bloqueada():
        print(
            f"  [XX BLOQUEADA] No puedes completar '{nodo.id}'.\n"
            f"                 Requisito pendiente (misión padre): '{nodo.padre.id}: {nodo.padre.nombre}'."
        )
        return False, nodo

    nodo.completada = True
    print(f"  [OK ÉXITO] ¡Misión completada: '{nodo.id}: {nodo.nombre}'!")
    if nodo.hijos:
        nuevas = [h.id for h in nodo.hijos]
        print(f"            -> Nuevas misiones desbloqueadas: {nuevas}")
    else:
        print("            -> ¡Has completado una misión hoja (final de rama)!")
    return True, nodo


def construir_arbol_misiones_nyx():
    m1 = Nodo("M1", "Despertar en la Cueva Ancestral", "Cueva Ancestral")
    m2 = Nodo("M2", "Pacto con Apolo (Arco Solar)", "Cueva Ancestral", recompensa_item="strength_elixir")
    m3 = Nodo("M3", "Pacto con Poseidón (Tridente)", "Cueva Ancestral", recompensa_item="mana_potion")
    m4 = Nodo("M4", "Purificar el Bosque Muerto", "Bosque Muerto",
              recompensa_item="health_potion", abre_santuario=True)
    m5 = Nodo("M5", "Recuperar la Reliquia de la Cripta Olvidada", "Cripta Olvidada",
              recompensa_item="mana_potion")
    m6 = Nodo("M6", "Explorar la Isla Aislada", "Isla Aislada", recompensa_item="health_potion")
    m7 = Nodo("M7", "Derrotar al Fire Fiend en el Volcán Extraño", "Volcán Extraño",
              recompensa_item="strength_elixir")
    m8 = Nodo("M8", "Sumergirse en el Lago Abisal", "Lago Abisal",
              recompensa_item="mana_potion", abre_santuario=True)
    m9 = Nodo("M9", "Vencer al Mind Flayer en el Templo en Ruinas", "Templo en Ruinas",
              recompensa_item="health_potion")

    m1.agregar_hijo(m2)
    m1.agregar_hijo(m3)

    m2.agregar_hijo(m4)
    m2.agregar_hijo(m5)
    m4.agregar_hijo(m7)

    m3.agregar_hijo(m6)
    m3.agregar_hijo(m8)
    m8.agregar_hijo(m9)

    return m1

def recorrido_por_niveles(raiz):
    """
    Recorrido Por Niveles (BFS con deque).
    Devuelve una lista de listas: niveles[0] = [M1], niveles[1] = [M2, M3], ...
    """
    if raiz is None:
        return []

    niveles = []
    cola = deque([(raiz, 0)])

    while cola:
        nodo, nivel = cola.popleft()
        if nivel == len(niveles):
            niveles.append([])
        niveles[nivel].append(nodo)

        for hijo in nodo.hijos:
            cola.append((hijo, nivel + 1))

    return niveles


def mostrar_por_niveles(raiz):
    """Muestra las misiones agrupadas por etapa y dice cuál es la etapa actual."""
    niveles = recorrido_por_niveles(raiz)
    etapa_actual = None

    print("\n--- [Misiones por Etapa] (Recorrido por Niveles) ---")
    for numero, grupo in enumerate(niveles):
        hechas = sum(1 for m in grupo if m.completada)
        print(f"\nNivel {numero}  ({hechas}/{len(grupo)} completadas)")
        for m in grupo:
            print(f"   {m.id}: {m.nombre} {ETIQUETAS[m.estado()]} - Sala: {m.sala}")

        if etapa_actual is None and hechas < len(grupo):
            etapa_actual = numero

    if etapa_actual is None:
        print("\n¡Has completado todas las etapas de la aventura!")
    else:
        print(f"\n>> Etapa actual: Nivel {etapa_actual}")


def misiones_disponibles(raiz):
    """Lista de misiones que se pueden completar ahora (padre completado, ellas no)."""
    return [m for grupo in recorrido_por_niveles(raiz) for m in grupo if m.estado() == "disponible"]


if __name__ == "__main__":
    raiz = construir_arbol_misiones_nyx()

    print("=== PRUEBAS DE CASOS LÍMITE ===")
    for prueba in ["M99", "", "   ", "hola", "-1", "0", None, "M4", "m1", "1", "M1"]:
        print(f"\n> Intentando completar: {prueba!r}")
        completar_mision(raiz, prueba)

    print("\n=== PREORDEN ===")
    preorden(raiz)

    mostrar_por_niveles(raiz)