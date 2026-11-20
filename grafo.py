"""
Módulo: mapa.py
Objetivo: Implementar una clase genérica Grafo con lista de adyacencia y el mapa
          del mundo de The Ballad of Nyx (Semanas 12 y 13 - Checkpoint 3).
"""


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
        Evita aristas duplicadas. Complejidad: O(1) promedio (O(grado) por validación).
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


def construir_mapa_nyx():
    """
    Construye el mapa principal de The Ballad of Nyx como un grafo no dirigido
    con ciclos y caminos alternativos a partir de las salas del juego.
    """
    mapa = Grafo(dirigido=False)

    conexiones = [
        ("Ancient Cave", "Isolated Island"),
        ("Ancient Cave", "Ruined Temple"),
        ("Isolated Island", "Dead Forest"),
        ("Isolated Island", "Abyssal Lake"),
        ("Dead Forest", "Strange Volcano"),
        ("Dead Forest", "Forgotten Crypt"),
        ("Forgotten Crypt", "Ruined Temple"),   # Ciclo / camino alternativo
        ("Abyssal Lake", "Ruined Temple"),      # Ciclo / camino alternativo
        ("Strange Volcano", "Dark Altar"),
        ("Ruined Temple", "Dark Altar"),        # Ruta alternativa hacia el altar
    ]

    for origen, destino in conexiones:
        mapa.agregar_arista(origen, destino)

    # Ejemplo de zona aislada para pruebas futuras con DFS/BFS
    mapa.agregar_nodo("Hidden Sanctuary")

    return mapa


if __name__ == "__main__":
    print("=== PRUEBA BASE DE mapa.py (Lista de Adyacencia) ===")
    mapa_nyx = construir_mapa_nyx()
    mapa_nyx.mostrar_grafo()