import pygame
from math import sin, cos, radians, atan, degrees

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
a = 700
size = a, a
screen = pygame.display.set_mode(size)

screen.fill(BLACK)


def draw_arrow(surf, color, start_cords, end_cords, width):
    rad_ar = width * 3
    pygame.draw.line(surf, color,
                     start_cords,
                     [tt - .5 * width for tt in end_cords], width)

    points = []

    tmp_x = start_cords[0] - end_cords[0]
    tmp_y = start_cords[1] - end_cords[1]
    try:
        rotate = tmp_x / tmp_y
    except ZeroDivisionError:
        rotate = 0
        print(0)
    rotate = degrees(atan(rotate))

    for iters in range(3):
        if start_cords[1] - end_cords[1] > 0:
            tmp = radians(120 * iters + rotate/2)
        else:
            tmp = radians(120 * iters - rotate/2)
        points.append((sin(tmp) * rad_ar + end_cords[0], cos(tmp) * rad_ar + end_cords[1]))

    pygame.draw.polygon(surf, color, points)



def draw_circle_lines(surf, rads, rotate=False):
    for iters in range(3):
        if rotate:
            tmp = radians(120 * iters)
        else:
            tmp = radians(120 * iters + 60)
        draw_arrow(surf, WHITE,
                   (sin(tmp) * rads[0] + 300, cos(tmp) * rads[0] + 300),
                   (sin(tmp) * rads[1] + 300, cos(tmp) * rads[1] + 300), 5)


draw_circle_lines(screen, [50, 100])
draw_circle_lines(screen, [100, 200], True)
pygame.draw.circle(screen, WHITE, (300, 300), 100, 1)

draw_arrow(screen,WHITE, (100, 230), (100, 300), 10)

pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()
