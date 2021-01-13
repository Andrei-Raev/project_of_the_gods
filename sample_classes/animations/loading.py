import pygame
from math import sin, cos, radians

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
a = 700
size = a, a
screen = pygame.display.set_mode(size)

screen.fill(BLACK)


def draw_circle_lines(surf, rads, rotate=False):
    for iters in range(3):
        if rotate:
            tmp = radians(120 * iters)
        else:
            tmp = radians(120 * iters + 60)
        pygame.draw.line(surf, WHITE,
                         (sin(tmp) * rads[0] + 300, cos(tmp) * rads[0] + 300),
                         (sin(tmp) * rads[1] + 300, cos(tmp) * rads[1] + 300))


draw_circle_lines(screen, [50, 100])
draw_circle_lines(screen, [100, 200], True)
pygame.draw.circle(screen, WHITE, (300, 300), 100, 1)

pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()
