import pygame
import sys
import math

# Inicializar pygame
pygame.init()

# Configuraciones de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simulación de Línea Curvada')

# Colores
BLACK = (0, 0, 0)
LINE_COLOR = (0, 255, 0)

# Parámetros de la línea
line_length = 800  # Longitud de la línea
curve_amount = 0   # Cantidad de curvatura inicial

def draw_curved_line(curve_amount):
    base_x = width // 2  # X de la base fija de la línea
    base_y = height - 50  # Y de la base fija de la línea

    # Coordenadas del punto superior de la línea
    top_x = base_x + curve_amount
    top_y = base_y - line_length + (curve_amount // 50)  # Desplazamiento hacia abajo con curvatura

    # Dibujar la línea curva hacia arriba
    for i in range(101):
        t = i / 100
        # Interpolación para crear la curva
        x = base_x + (top_x - base_x) * t
        # y = base_y - (line_length * t) + (curve_amount // 50) * t  # Ajustar según la curvatura
        y = base_y - (line_length * math.sin((math.pi / 2) * t) * 0.5)  # Ajustar el multiplicador según sea necesario
        y = max(y, top_y)  # Asegurarse de que y no baje de top_y
        if i == 0:
            prev_x, prev_y = x, y
        else:
            pygame.draw.line(screen, LINE_COLOR, (prev_x, prev_y), (x, y), 5)
            prev_x, prev_y = x, y

def main():
    global curve_amount
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    curve_amount -= 5  # Aumentar la curvatura hacia la izquierda
                elif event.key == pygame.K_RIGHT:
                    curve_amount += 5  # Aumentar la curvatura hacia la derecha

        # Rellenar la pantalla
        screen.fill(BLACK)

        # Dibujar la línea curvada
        draw_curved_line(curve_amount)

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)  # Limitar a 60 FPS

if __name__ == "__main__":
    main()
