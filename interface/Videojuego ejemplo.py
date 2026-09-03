import pygame
import sys

# --- 1. Lógica de Inventario ---
inventario_nyx = []

def agregar_objeto(inventario, objeto):
    if len(inventario) >= 5:
        print("\n¡Inventario lleno!")
        return False
    inventario.append(objeto)
    print(f"\n¡Has encontrado: {objeto}!")
    return True

def mostrar_inventario(inventario):
    print("\n--- Inventario Actual ---")
    if not inventario:
        print("La mochila está vacía.")
    for i, item in enumerate(inventario):
        print(f"[{i}] {item}")

# --- 2. Configuración de Pygame ---
pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Aventura de Nyx - Animación")
reloj = pygame.time.Clock()

# --- 3. Sistema de Sprites y Animación ---
hoja_completa = pygame.image.load("nyx.png").convert_alpha()

# Cargar el sprite de la espada y escalarlo a 32x32 (como indicó el artista)
sprite_espada = pygame.image.load("espada.png").convert_alpha()
sprite_espada = pygame.transform.scale(sprite_espada, (32, 32))

# Cargar y escalar las texturas a 40x40 píxeles
# Usamos convert() para el fondo y convert_alpha() para que la roca y el árbol mantengan su fondo transparente
# 1. Cargar las texturas base
base_pasto = pygame.image.load("grass_tile.png").convert()
base_roca = pygame.image.load("Layered Rock.png").convert_alpha()
base_arbol = pygame.image.load("Tree.png").convert_alpha()

# 2. Escalar: Pasto más pequeño (20x20) y Árbol más masivo (160x160)
img_pasto = pygame.transform.scale(base_pasto, (20, 20)) 
img_roca_normal = pygame.transform.scale(base_roca, (50, 50))
img_arbol_enorme = pygame.transform.scale(base_arbol, (160, 160))

# 3. Diccionario de objetos (El pasto ya no está aquí, lo manejaremos aparte)
texturas_objetos = {
    1: img_roca_normal,
    2: img_arbol_enorme
    # ¡Aquí podemos agregar 3, 4, 5... arboles y rocas de texturas diferentes!
}
# Matriz del nivel (0=Pasto, 1=Roca, 2=Árbol)
# 0=Pasto, 1=Roca pequeña, 2=Roca normal, 3=Roca grande, 4=Árbol gigante
# Ahora sí, exactamente 15 filas x 20 columnas (600x800 píxeles)
# 0 = Vacío (ya dibujamos el pasto al fondo), 1 = Roca, 2 = Árbol
mapa_mundo = [
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0] 
]

# Función mejorada con opción de "espejo" (voltear_horizontal)
# Función corregida con la cuadrícula de 16x32
def obtener_frame(columna, fila, voltear_horizontal=False):
    ancho_frame = 16 
    alto_frame = 32  # Ajustado a la cuadrícula real del artista
    
    rect = pygame.Rect(columna * ancho_frame, fila * alto_frame, ancho_frame, alto_frame)
    imagen = hoja_completa.subsurface(rect)
    
    if voltear_horizontal:
        imagen = pygame.transform.flip(imagen, True, False)
        
    # Como el alto es 32 (el doble del ancho), escalamos a 40x80 para mantener la proporción
    return pygame.transform.scale(imagen, (40, 80)) 

def obtener_frame_ataque(columna, fila):
    ancho_frame = 32  # ¡El doble de ancho para que quepa la espada!
    alto_frame = 32   
    
    # La coordenada Y sigue la cuadrícula de 32 de alto, pero X usa bloques de 32 de ancho
    rect = pygame.Rect(columna * ancho_frame, fila * 32, ancho_frame, alto_frame)
    imagen = hoja_completa.subsurface(rect)
    
    # Escalamos manteniendo la proporción (si 16px = 40, entonces 32px = 80)
    return pygame.transform.scale(imagen, (80, 80))

# Diccionario reordenado según lo que vimos en tus pruebas
animaciones = {
    # Fila 0: Abajo (Capturamos de la columna 0 a la 3)
    "abajo": [obtener_frame(0, 0), obtener_frame(1, 0), obtener_frame(2, 0), obtener_frame(3, 0)],
    
    # Fila 2: Arriba
    "arriba": [obtener_frame(0, 2), obtener_frame(1, 2), obtener_frame(2, 2), obtener_frame(3, 2)],
    
    # Fila 1: Derecha
    "derecha": [obtener_frame(0, 1), obtener_frame(1, 1), obtener_frame(2, 1), obtener_frame(3, 1)],
    
    # Fila 3: Izquierda (¡Usamos la fila nativa, ya no necesitamos la función de espejo!)
    "izquierda": [obtener_frame(0, 3), obtener_frame(1, 3), obtener_frame(2, 3), obtener_frame(3, 3)]
}
# Mantenemos las caminatas de las filas 0, 1, 2 y 3...
# Y agregamos las animaciones de ataque (filas 4, 5, 6 y 7):
animaciones.update({
    # Fila 4: Ataque hacia abajo (Este ya funcionaba perfecto)
    "ataque_abajo": [obtener_frame_ataque(0, 4), obtener_frame_ataque(1, 4), obtener_frame_ataque(2, 4), obtener_frame_ataque(3, 4)],
    
    # Fila 5: Ataque hacia arriba
    "ataque_arriba": [obtener_frame_ataque(0, 5), obtener_frame_ataque(1, 5), obtener_frame_ataque(2, 5), obtener_frame_ataque(3, 5)],
    
    # Fila 6: Ataque hacia la derecha
    "ataque_derecha": [obtener_frame_ataque(0, 6), obtener_frame_ataque(1, 6), obtener_frame_ataque(2, 6), obtener_frame_ataque(3, 6)],
    
    # Fila 7: Ataque hacia la izquierda
    "ataque_izquierda": [obtener_frame_ataque(0, 7), obtener_frame_ataque(1, 7), obtener_frame_ataque(2, 7), obtener_frame_ataque(3, 7)]
})
# --- 4. Variables del Juego (Entidades) ---
jugador_rect = pygame.Rect(400, 300, 40, 80)
jugador_vel = 4

# --- 4.5. Generador de Colisiones Estáticas ---
obstaculos = [] # Aquí guardaremos todas las cajas sólidas del mapa

for fila in range(len(mapa_mundo)):
    for columna in range(len(mapa_mundo[fila])):
        tipo_bloque = mapa_mundo[fila][columna]
        
        # Si hay algo diferente de 0 (o sea, una roca o un árbol)
        if tipo_bloque != 0:
            # Creamos un rectángulo invisible de 40x40 en esa baldosa
            # Esto actuará como el "tronco" o la "base" sólida del objeto
            caja_colision = pygame.Rect(columna * 40, fila * 40, 40, 40)
            obstaculos.append(caja_colision)

espada_rect = pygame.Rect(200, 200, 32, 32)
espada_en_suelo = True 

# Variables de control de animación
direccion_actual = "abajo"
indice_frame = 0
tiempo_ultimo_frame = pygame.time.get_ticks()
velocidad_animacion = 150 # Milisegundos entre cada paso

tiene_espada = False
atacando = False

# --- 5. Bucle Principal ---
ejecutando = True
while ejecutando:
    
    # A. EVENTOS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        # 1. Recoger espada y cambiar de estado
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
            if espada_en_suelo and jugador_rect.colliderect(espada_rect):
                exito = agregar_objeto(inventario_nyx, "Espada Divina")
                if exito: 
                    espada_en_suelo = False
                    tiene_espada = True # ¡Desbloqueas la habilidad!
                    
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_i:
            mostrar_inventario(inventario_nyx)
            
        # 2. Gatillo de Ataque (Barra Espaciadora)
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            if tiene_espada and not atacando:
                atacando = True
                indice_frame = 0 # Iniciamos el golpe desde el primer cuadro
                tiempo_ultimo_frame = pygame.time.get_ticks() # Reiniciamos el reloj

    # B. LÓGICA DE MOVIMIENTO Y ANIMACIÓN
    teclas = pygame.key.get_pressed()
    esta_moviendose = False
    
    # 1. Guardar la coordenada segura ANTES de intentar movernos
    pos_segura_x = jugador_rect.x
    pos_segura_y = jugador_rect.y
    
    # 2. Intentar moverse
    if not atacando:
        if teclas[pygame.K_LEFT]:
            jugador_rect.x -= jugador_vel
            direccion_actual = "izquierda"
            esta_moviendose = True
        elif teclas[pygame.K_RIGHT]:
            jugador_rect.x += jugador_vel
            direccion_actual = "derecha"
            esta_moviendose = True
        elif teclas[pygame.K_UP]:
            jugador_rect.y -= jugador_vel
            direccion_actual = "arriba"
            esta_moviendose = True
        elif teclas[pygame.K_DOWN]:
            jugador_rect.y += jugador_vel
            direccion_actual = "abajo"
            esta_moviendose = True

# 3. EVALUADOR DE COLISIONES SÓLIDAS
    # Creamos un sensor (Hitbox) que solo cubra la mitad inferior de Nyx (sus piernas)
    # jugador_rect.y + 40 baja el sensor para que ignore su cabeza
    hitbox_nyx = pygame.Rect(jugador_rect.x, jugador_rect.y + 40, 40, 40)
    
    # Revisamos si LAS PIERNAS de Nyx tocan los obstáculos, ya no todo su cuerpo
    for obs in obstaculos:
        if hitbox_nyx.colliderect(obs):
            # Si hay choque, cancelamos el movimiento
            jugador_rect.x = pos_segura_x
            jugador_rect.y = pos_segura_y
            break

    tiempo_actual = pygame.time.get_ticks()
    
    # 3. Gestor de Animaciones (Ataque vs Caminar)
    if atacando:
        nombre_anim = "ataque_" + direccion_actual
        
        # El ataque es más rápido que caminar (ej. 80ms)
        if tiempo_actual - tiempo_ultimo_frame > 80:
            indice_frame += 1
            if indice_frame >= len(animaciones[nombre_anim]):
                atacando = False # Termina el ataque
                indice_frame = 1 # Regresa a la postura de descanso
            tiempo_ultimo_frame = tiempo_actual
            
        # Asignamos la imagen si seguimos atacando
        if atacando:
            imagen_actual = animaciones[nombre_anim][indice_frame]
        else:
            imagen_actual = animaciones[direccion_actual][1]
            
    else:
        # Lógica normal de caminar
        if esta_moviendose:
            if tiempo_actual - tiempo_ultimo_frame > velocidad_animacion:
                indice_frame += 1
                if indice_frame >= len(animaciones[direccion_actual]):
                    indice_frame = 0
                tiempo_ultimo_frame = tiempo_actual
        else:
            indice_frame = 1 # Postura de descanso (Columna 1)
            
        imagen_actual = animaciones[direccion_actual][indice_frame]

# C. DIBUJAR GRÁFICOS
    
    # 1. CAPA BASE: Tapizar el fondo con el pasto pequeño
    for y in range(0, 600, 20):
        for x in range(0, 800, 20):
            pantalla.blit(img_pasto, (x, y))
            
    # 2. CAPA INTERMEDIA Y SUPERIOR: Motor de Profundidad (Y-Sorting)
    nyx_dibujada = False
    
    for fila in range(len(mapa_mundo)):
        # Dibujamos los objetos de esta fila horizontal
        for columna in range(len(mapa_mundo[fila])):
            tipo_bloque = mapa_mundo[fila][columna] 
            
            if tipo_bloque != 0:
                pos_x = columna * 40
                pos_y = fila * 40
                
                if tipo_bloque == 2:
                    pantalla.blit(texturas_objetos[tipo_bloque], (pos_x - 60, pos_y - 120))
                else:
                    pantalla.blit(texturas_objetos[tipo_bloque], (pos_x, pos_y))
                    
        # Y-Sorting: Evalúa si los pies de Nyx están en esta capa horizontal
        if not nyx_dibujada and jugador_rect.bottom <= (fila * 40) + 40:
            if espada_en_suelo:
                pantalla.blit(sprite_espada, (espada_rect.x, espada_rect.y))
                
            if atacando and direccion_actual == "izquierda":
                pantalla.blit(imagen_actual, (jugador_rect.x - 20, jugador_rect.y))
            else:
                pantalla.blit(imagen_actual, (jugador_rect.x, jugador_rect.y))
                
            nyx_dibujada = True

    # Seguro de dibujado por si Nyx está al borde inferior de la pantalla
    if not nyx_dibujada:
        if espada_en_suelo:
            pantalla.blit(sprite_espada, (espada_rect.x, espada_rect.y))
        if atacando and direccion_actual == "izquierda":
            pantalla.blit(imagen_actual, (jugador_rect.x - 20, jugador_rect.y))
        else:
            pantalla.blit(imagen_actual, (jugador_rect.x, jugador_rect.y))
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()