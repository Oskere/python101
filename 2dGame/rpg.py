import pygame
import sqlite3
import random

# Inicialización de Pygame
pygame.init()

# Tamaño de la pantalla
ANCHO = 800
ALTO = 600
fondo = pygame.image.load("./fondo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Batalla RPG Estilo Pokémon")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Fuente para el texto
fuente = pygame.font.SysFont("Arial", 24)

# Clases de personajes
class Personaje:
    def __init__(self, nombre,salud_maxima, ataque, defensa, tipo, hab1pp, hab2pp, hab3pp, hab4pp, imagen):
        self.nombre = nombre
        self.salud_maxima = salud_maxima + random.randint(0,50)
        self.salud = self.salud_maxima
        self.ataque = ataque
        self.defensa = defensa
        self.tipo = tipo
        self.hab1pp = hab1pp
        self.hab2pp = hab2pp
        self.hab3pp = hab3pp
        self.hab4pp = hab4pp
        self.imagen = imagen  

    def atacar(self, ataque ,enemigo, mult, tipoAtaque):
        habilidad = ""
        danio = 0
        if ataque == 'hab1' and self.hab1pp > 0:
            self.hab1pp -= 1
            habilidad = "Placaje"
        elif ataque == 'hab2' and self.hab2pp > 0:
            self.hab2pp -= 1
            habilidad = "Lanzallamas"
        elif ataque == 'hab3' and self.hab3pp > 0:
            self.hab3pp -= 1
            habilidad = "Pistola Agua"
        elif ataque == 'hab4' and self.hab4pp > 0:
            self.hab4pp -= 1
            habilidad = "Ultrapuño"
        else:
            mostrar_texto(f"No tienes suficientes PP para usar {habilidad}!",ROJO, 400, 400)
            mostrar_texto("Vas a realizar el ataque 'ESFUERZO'",NEGRO, 400, 400)
            return random.randint(0,100)

        multiplicador_tipo = self.obtener_multiplicador(tipoAtaque, enemigo.tipo)
        if multiplicador_tipo == 2:
            pass
        if tipoAtaque == self.tipo:
            danio += danio * 2.5 
        else:
            pass
        danio += danio * mult
        danio = (danio + (self.ataque+random.randint(0,20))) - (enemigo.defensa + random.randint(0,20))
        if danio < 0:
            danio = 0
        danio += danio * multiplicador_tipo
        enemigo.salud -= danio
        return danio

    def obtener_multiplicador(self, tipoAtaque, tipoEnemigo):
        # Conectarse a la base de datos
        conn = sqlite3.connect('tabla_tipos.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id FROM tipos WHERE nombre = ?
        ''', (tipoAtaque,))
        tipoAtaque_id = cursor.fetchone()

        # Obtener el ID del tipo del enemigo
        cursor.execute('''
            SELECT id FROM tipos WHERE nombre = ?
        ''', (tipoEnemigo,))
        tipoEnemigo_id = cursor.fetchone()

        if not tipoAtaque_id or not tipoEnemigo_id:         
            conn.close()
            return 1

        tipoAtaque_id = tipoAtaque_id[0]
        tipoEnemigo_id = tipoEnemigo_id[0]

        cursor.execute('''
            SELECT tipo_relacion
            FROM relaciones
            WHERE tipo_id = ? AND relacionado_con = ?
        ''', (tipoAtaque_id, tipoEnemigo_id))

        resultado = cursor.fetchone()
        
        if resultado:
            tipo_relacion = resultado[0]
            if tipo_relacion == "f":
                multiplicador = 2
            elif resultado[0] == "d":
                multiplicador = 0.5
            else:
                multiplicador = 1
        else:
            multiplicador = 1

        # Cerrar la conexión a la base de datos
        conn.close()
        print(multiplicador)
        return multiplicador

    def esta_vivo(self):
        return self.salud > 0
    
    def dibujar_barra_salud(self, x, y):
        # Calculamos el ancho de la barra en función de la salud actual
        ancho_barra = 200
        porcentaje_salud = self.salud / self.salud_maxima
        ancho_actual = ancho_barra * porcentaje_salud

        # Dibujar la barra de vida en verde
        pygame.draw.rect(pantalla, VERDE, (x, y, ancho_actual, 20))

        # Dibujar el fondo de la barra (rojo)
        pygame.draw.rect(pantalla, ROJO, (x, y, ancho_barra, 20), 2)

        # Mostrar el nombre del personaje y su salud
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"{self.nombre}: {self.salud}/{self.salud_maxima}", True, NEGRO)
        pantalla.blit(texto, (x, y - 30))


# #####################################
# IMAGENES ASSETS
# #####################################

TAMANO_ATAQUE = (50, 50)
imagen_jugador = pygame.image.load("./personaje1.png")
imagen_enemigo = pygame.image.load("./enemigo1.png")
imagen_hit = pygame.image.load("./hit.png")
imagen_lanzallamas = pygame.image.load("./lanzallamas.png")
imagen_lanzallamas = pygame.transform.scale(imagen_lanzallamas, TAMANO_ATAQUE)
imagen_watergun = pygame.image.load("./watergun.png")
imagen_watergun = pygame.transform.scale(imagen_watergun, TAMANO_ATAQUE)
imagen_ultrapuno = pygame.image.load("./ultrapuno.png")
imagen_ultrapuno = pygame.transform.scale(imagen_ultrapuno, TAMANO_ATAQUE)

# #####################################
# Crear personajes
# #####################################

jugador = Personaje("Jugador", 500, 94, 31, "Lucha", 30, 15, 10, 5, imagen_jugador)
enemigo = Personaje("Enemigo", 500, 85, 40, "Normal", 10, 10, 10, 10, imagen_enemigo)

# #####################################
# Función para mostrar texto en pantalla
# #####################################

def mostrar_texto(texto, color, x, y):
    texto_renderizado = fuente.render(texto, True, color)
    pantalla.blit(texto_renderizado, (x, y))

# #####################################
# Función para mostrar la interfaz de batalla
# #####################################

def mostrar_interfaz():
    pantalla.blit(fondo, (0, 0))
    jugador.dibujar_barra_salud(50, 380)
    enemigo.dibujar_barra_salud(380, 30)

    pantalla.blit(jugador.imagen, (50, 410))  
    pantalla.blit(enemigo.imagen, (380, 50)) 

# #####################################
# Función para crear un botón
# #####################################

def crear_boton(texto, x, y, ancho, alto, color_normal, color_hover):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    # Detectar si el ratón está sobre el botón
    boton_rect = pygame.Rect(x, y, ancho, alto)
    if boton_rect.collidepoint(mouse_pos):
        pygame.draw.rect(pantalla, color_hover, boton_rect)
        if mouse_click:
            return True
    else:
        pygame.draw.rect(pantalla, color_normal, boton_rect)

    # Mostrar el texto del botón
    texto_boton = fuente.render(texto, True, NEGRO)
    pantalla.blit(texto_boton, (x + 10, y + 10))  

    return False

# Función para mover el proyectil de ataque
def mover_proyectil(proyectil, velocidad, objetivo_x, objetivo_y):
    if proyectil.x < objetivo_x:
        proyectil.x += velocidad
    if proyectil.x > objetivo_x:
        proyectil.x -= velocidad
    if proyectil.y < objetivo_y:
        proyectil.y += velocidad
    if proyectil.y > objetivo_y:
        proyectil.y -= velocidad

    if proyectil.colliderect(pygame.Rect(objetivo_x, objetivo_y, 50, 50)):
        return True

    return False


# Función para mostrar el efecto visual del golpe
def mostrar_efecto(efecto_img, x, y, duracion=2000):
    tiempo_inicio = pygame.time.get_ticks()
    tiempo_parpadeo = 0
    while pygame.time.get_ticks() - tiempo_inicio < duracion:
        if (pygame.time.get_ticks() - tiempo_inicio) // 50 % 2 == 0:
            pantalla.blit(efecto_img, (x, y)) 
        pygame.display.update()
    pantalla.blit(efecto_img, (x, y))
    pygame.display.update()


# Función principal del juego
def juego():
    angulo = 75
    corriendo = True
    turno_jugador = True
    esperando_ataque = False

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Mostrar la interfaz de batalla
        mostrar_interfaz()

        # Si es el turno del jugador
        if jugador.esta_vivo() and enemigo.esta_vivo():
            if turno_jugador:
                if not esperando_ataque:
                    mostrar_texto("Presiona '1' para seleccionar el ataque:", NEGRO, 400, 400)
                    teclas = pygame.key.get_pressed()
                    if teclas[pygame.K_1]:
                        esperando_ataque = True
                        mostrar_texto("Selecciona un ataque", ROJO, 400, 420)
                        pygame.display.update()
                        pygame.time.wait(500)
                else:
                    if crear_boton("Placaje", 450, 400, 150, 50, BLANCO, VERDE):
                        # Atacar con Placaje
                        danio = jugador.atacar("hab1",enemigo,0.15,"Normal")
                        pantalla.fill(NEGRO)
                        mostrar_interfaz()
                        mostrar_texto(f"¡Has golpeado por {danio} puntos de daño con Placaje!", NEGRO, 400, 400)
                        mostrar_efecto(imagen_hit, 410, 60)
                        pygame.display.update()
                        esperando_ataque = False
                        turno_jugador = False
                    elif crear_boton("Lanzallamas", 625, 400, 150, 50, ROJO, VERDE):
                        # Atacar con Lanzallamas
                        danio = jugador.atacar("hab2",enemigo,0.85,"Fuego")
                        proyectil = pygame.Rect(50, 410, 30, 30)
                        while not mover_proyectil(proyectil, 10, 380, 50):
                            pantalla.fill(NEGRO)
                            mostrar_interfaz()
                            
                            imagen_rotada = pygame.transform.rotate(imagen_lanzallamas, angulo)

                            pantalla.blit(imagen_rotada, proyectil)
                            pygame.display.update()
                            pygame.time.wait(10)
                        mostrar_texto(f"¡Has usado Lanzallamas!", NEGRO, 400, 400)
                        mostrar_texto(f"¡Has realizado{danio} puntos de daño!", NEGRO, 400, 420)                       
                        mostrar_efecto(imagen_hit, 410, 60)
                        pygame.display.update()
                        esperando_ataque = False
                        turno_jugador = False
                    elif crear_boton("Pistola agua", 450, 470, 150, 50, AZUL, VERDE):
                        danio = jugador.atacar("hab3",enemigo,0.55,"Agua")
                        proyectil = pygame.Rect(50, 410, 30, 30)
                        while not mover_proyectil(proyectil, 10, 380, 50):
                            pantalla.fill(NEGRO)
                            mostrar_interfaz()
                            
                            imagen_rotada = pygame.transform.rotate(imagen_watergun, angulo)

                            pantalla.blit(imagen_rotada, proyectil)
                            pygame.display.update()
                            pygame.time.wait(10)
                        mostrar_texto(f"¡Has usado Pistola agua!", NEGRO, 400, 400)
                        mostrar_texto(f"¡Has realizado {danio} puntos de daño!", NEGRO, 400, 420)
                        mostrar_efecto(imagen_hit, 410, 60)
                        pygame.display.update()
                        esperando_ataque = False
                        turno_jugador = False
                    elif crear_boton("UltraPuño", 625, 470, 150, 50, "#964B00", VERDE):
                        # Atacar con UltraPuño
                        danio = jugador.atacar("hab4",enemigo,1.15,"Lucha")
                        proyectil = pygame.Rect(50, 410, 30, 30)
                        while not mover_proyectil(proyectil, 10, 380, 50):
                            pantalla.fill(NEGRO)
                            mostrar_interfaz()
                            imagen_rotada = pygame.transform.rotate(imagen_ultrapuno, angulo)
                            pantalla.blit(imagen_rotada, proyectil)
                            pygame.display.update()
                            pygame.time.wait(10)
                        mostrar_texto(f"¡Has usado UltraPuño!",  NEGRO, 400, 400)
                        mostrar_texto(f"¡Has realizado {danio} puntos de daño!",  NEGRO, 400, 420) 
                        mostrar_efecto(imagen_hit, 410, 60)
                        pygame.display.update()
                        pygame.key.get_pressed()
                        esperando_ataque = False
                        turno_jugador = False

            else:
                # Turno del enemigo
                danio = enemigo.atacar("hab1",jugador,0.55,"Normal")
                mostrar_texto(f"El enemigo ha usado Placaje Maximo!", NEGRO, 400, 400)
                mostrar_texto(f"Has recibido {danio} puntos de daño", NEGRO, 400, 420)
                mostrar_efecto(imagen_hit, 80, 420)
                pygame.display.update()
                turno_jugador = True

        # Verificar si alguno ha muerto
        if not jugador.esta_vivo():
            mostrar_texto("¡El enemigo ha ganado!", ROJO, 250, 250)
            pygame.display.update()
            pygame.time.wait(2000)
            corriendo = False
        elif not enemigo.esta_vivo():
            mostrar_texto("¡Has ganado la batalla!", ROJO, 250, 250)
            pygame.display.update()
            pygame.time.wait(2000)
            corriendo = False

        # Actualizar pantalla
        pygame.display.update()

# Ejecutar el juego
juego()

# Cerrar Pygame
pygame.quit()
