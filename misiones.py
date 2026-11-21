"""
Módulo: misiones.py
Proyecto: Aventura Algorítmica - The Ballad of Nyx
Objetivo: Árbol de misiones de Nyx (Semana 14, Checkpoint 3).
          Cada misión depende de su misión padre: no se puede completar
          una misión si su padre aún no está completada.
Nota: este módulo NO usa input() ni pausas; solo lógica del árbol.
"""


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


def buscar_mision(nodo, id_buscado):
    """Busca una misión por ID (recursivo). Devuelve el nodo o None."""
    if nodo is None:
        return None

    if nodo.id.upper() == str(id_buscado).strip().upper():
        return nodo

    for hijo in nodo.hijos:
        encontrado = buscar_mision(hijo, id_buscado)
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