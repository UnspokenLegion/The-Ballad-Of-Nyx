"""
Módulo: grafo.py
Objetivo: Implementar una clase genérica Grafo con lista de adyacencia,
          recorridos BFS y DFS, y el mapa del mundo de The Ballad of Nyx
          (Semanas 12 y 13 - Checkpoint 3).
"""

from collections import deque


class Grafo:
    """
    Implementación genérica y reutilizable de un grafo mediante lista de adyacencia.
    Soporta grafos no dirigidos (por defecto) y dirigidos.
    """

    def __init__(self, dirigido=False):
        self.adyacencia = {}
        self.dirigido = dirigido

    def agregar_nodo(self, nodo):
        """Agrega un vértice al grafo si aún no existe. Complejidad: O(1)."""
        if nodo not in self.adyacencia:
            self.adyacencia[nodo] = []

    def agregar_arista(self, origen, destino):
        """
        Conecta dos nodos. Si alguno no existe, lo crea automáticamente.
        Evita aristas duplicadas. Complejidad: O(1) promedio.
        """
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)

        if destino not in self.adyacencia[origen]:
            self.adyacencia[origen].append(destino)

        if not self.dirigido and origen not in self.adyacencia[destino]:
            self.adyacencia[destino].append(origen)

    def eliminar_arista(self, origen, destino):
        """Elimina la conexión entre dos nodos si existe."""
        if origen in self.adyacencia and destino in self.adyacencia[origen]:
            self.adyacencia[origen].remove(destino)
        if not self.dirigido and destino in self.adyacencia and origen in self.adyacencia[destino]:
            self.adyacencia[destino].remove(origen)

    def existe_nodo(self, nodo):
        """Verifica si un nodo pertenece al grafo. Complejidad: O(1)."""
        return nodo in self.adyacencia

    def obtener_vecinos(self, nodo):
        """
        Devuelve la lista de nodos conectados a 'nodo'.
        Si el nodo no existe, devuelve una lista vacía sin lanzar error.
        """
        return list(self.adyacencia.get(nodo, []))

    def obtener_nodos(self):
        """Devuelve una lista con todos los nodos del grafo."""
        return list(self.adyacencia.keys())

    def mostrar_grafo(self):
        """Imprime la lista de adyacencia de forma legible en consola."""
        for nodo, vecinos in self.adyacencia.items():
            conexiones = ", ".join(vecinos) if vecinos else "(sin conexiones)"
            print(f"  - {nodo} -> [{conexiones}]")

    # ==========================================================================
    # ALGORITMOS DE RECORRIDO: BFS Y DFS (Semana 13)
    # ==========================================================================

    def bfs_ruta_mas_corta(self, inicio, destino, bloqueados=None):
        """
        Calcula la ruta con menos saltos entre 'inicio' y 'destino' usando BFS.
        Permite ignorar nodos en 'bloqueados' (ej. desde estado_mundo.py) para
        encontrar rutas alternativas.
        Complejidad: O(V + E), donde V son los nodos y E las aristas.
        Retorna la lista de nodos de la ruta, o None si no existe camino posible.
        """
        bloqueados = set(bloqueados) if bloqueados else set()

        # Casos límite: nodos inexistentes o inicio/destino bloqueados
        if not self.existe_nodo(inicio) or not self.existe_nodo(destino):
            return None
        if inicio in bloqueados or destino in bloqueados:
            return None
        if inicio == destino:
            return [inicio]

        visitados = {inicio}
        cola = deque([[inicio]])

        while cola:
            camino_actual = cola.popleft()
            nodo_actual = camino_actual[-1]

            for vecino in self.obtener_vecinos(nodo_actual):
                if vecino in bloqueados or vecino in visitados:
                    continue

                nuevo_camino = camino_actual + [vecino]
                if vecino == destino:
                    return nuevo_camino

                visitados.add(vecino)
                cola.append(nuevo_camino)

        return None

    def dfs_zonas_alcanzables(self, inicio, bloqueados=None):
        """
        Explora en profundidad (DFS) todas las zonas alcanzables desde 'inicio',
        respetando los nodos bloqueados.
        Complejidad: O(V + E).
        Retorna una lista con los nodos alcanzables en orden de visita.
        """
        bloqueados = set(bloqueados) if bloqueados else set()

        # Caso límite: nodo inicial inexistente o bloqueado
        if not self.existe_nodo(inicio) or inicio in bloqueados:
            return []

        visitados = set()
        orden_visita = []

        def _dfs_recursivo(nodo_actual):
            visitados.add(nodo_actual)
            orden_visita.append(nodo_actual)
            for vecino in self.obtener_vecinos(nodo_actual):
                if vecino not in visitados and vecino not in bloqueados:
                    _dfs_recursivo(vecino)

        _dfs_recursivo(inicio)
        return orden_visita

    def detectar_zonas_aisladas(self, inicio, bloqueados=None):
        """
        Usa DFS para detectar qué nodos del grafo NO son alcanzables desde 'inicio'.
        Complejidad: O(V + E).
        """
        alcanzables = set(self.dfs_zonas_alcanzables(inicio, bloqueados))
        return [nodo for nodo in self.obtener_nodos() if nodo not in alcanzables]


def construir_mapa_nyx():
    """
    Construye el mapa principal de The Ballad of Nyx como un grafo no dirigido
    con ciclos y caminos alternativos, alineado con los nombres en español
    de estado_mundo.py y main.py.
    """
    mapa = Grafo(dirigido=False)

    conexiones = [
        ("Cueva Ancestral", "Isla Aislada"),
        ("Cueva Ancestral", "Templo en Ruinas"),
        ("Isla Aislada", "Bosque Muerto"),
        ("Isla Aislada", "Lago Abisal"),
        ("Bosque Muerto", "Volcán Extraño"),
        ("Bosque Muerto", "Cripta Olvidada"),
        ("Cripta Olvidada", "Templo en Ruinas"),   # Ciclo / camino alternativo
        ("Lago Abisal", "Templo en Ruinas"),       # Ciclo / camino alternativo
        ("Volcán Extraño", "Altar Oscuro"),
        ("Templo en Ruinas", "Altar Oscuro"),      # Ruta alternativa hacia el altar
    ]

    for origen, destino in conexiones:
        mapa.agregar_arista(origen, destino)

    # Zona aislada (se puede conectar luego al completar una misión)
    mapa.agregar_nodo("Santuario Oculto")

    return mapa


if __name__ == "__main__":
    print("=== PRUEBAS DE grafo.py (Alineado con estado_mundo.py) ===")
    mapa_nyx = construir_mapa_nyx()

    print("\n1. Ruta más corta con BFS (Cueva Ancestral -> Altar Oscuro):")
    ruta = mapa_nyx.bfs_ruta_mas_corta("Cueva Ancestral", "Altar Oscuro")
    print("  Ruta:", " -> ".join(ruta) if ruta else "Sin ruta posible")

    print("\n2. Ruta alternativa con BFS si 'Templo en Ruinas' está bloqueado:")
    ruta_alt = mapa_nyx.bfs_ruta_mas_corta("Cueva Ancestral", "Altar Oscuro", bloqueados={"Templo en Ruinas"})
    print("  Ruta alternativa:", " -> ".join(ruta_alt) if ruta_alt else "Sin ruta posible")

    print("\n3. Zonas alcanzables con DFS desde 'Cueva Ancestral':")
    print("  Alcanzables:", mapa_nyx.dfs_zonas_alcanzables("Cueva Ancestral"))

    print("\n4. Zonas aisladas detectadas con DFS:")
    print("  Aisladas:", mapa_nyx.detectar_zonas_aisladas("Cueva Ancestral"))

    print("\n5. Casos límite:")
    print("  Ruta a sala inexistente:", mapa_nyx.bfs_ruta_mas_corta("Cueva Ancestral", "Sala Falsa"))
    print("  Ruta a Santuario Oculto:", mapa_nyx.bfs_ruta_mas_corta("Cueva Ancestral", "Santuario Oculto"))