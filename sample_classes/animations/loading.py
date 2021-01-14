import pygame
from math import sin, cos, radians, atan, degrees

from PIL import Image

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
a = 700
size = a, a
screen = pygame.display.set_mode(size)

screen.fill(BLACK)


def antialiasing(surface, size_cof):
    size = surface.get_size()
    size = [i // size_cof for i in size]
    strFormat = 'RGBA'

    raw_str = pygame.image.tostring(surface, strFormat, False)
    image = Image.frombytes(strFormat, surface.get_size(), raw_str)

    image = image.resize(size, resample=Image.ANTIALIAS)

    raw_str = image.tobytes("raw", strFormat)
    result = pygame.image.fromstring(raw_str, image.size, strFormat)
    del size, strFormat, raw_str, image
    return result


def draw_arrow(surf, color, start_cords, end_cords, width):
    rad_ar = width * 2.3

    points = []

    tmp_x = start_cords[0] - end_cords[0]
    tmp_y = start_cords[1] - end_cords[1]

    try:
        rotate = tmp_x / tmp_y
    except ZeroDivisionError:
        rotate = 0

    rotate = degrees(atan(rotate))

    for iters in range(3):

        if tmp_x * tmp_y < 0:
            tmp = radians(120 * iters - rotate + 30)
        else:
            tmp = radians(120 * iters - rotate - 30)

        if tmp_x > 0:
            tmp -= 1

        points.append((cos(tmp) * rad_ar + end_cords[0], sin(tmp) * rad_ar + end_cords[1]))

    main_points = []

    tmp = radians(-rotate)
    main_points.append((cos(tmp) * width / 2 + start_cords[0], sin(tmp) * width / 2 + start_cords[1]))

    tmp = radians(180 - rotate)
    main_points.append((cos(tmp) * width / 2 + start_cords[0], sin(tmp) * width / 2 + start_cords[1]))

    main_points.append((cos(tmp) * width / 2 + end_cords[0], sin(tmp) * width / 2 + end_cords[1]))

    tmp = radians(-rotate)
    main_points.append((cos(tmp) * width / 2 + end_cords[0], sin(tmp) * width / 2 + end_cords[1]))

    pygame.draw.polygon(surf, color, main_points, 0)
    pygame.draw.polygon(surf, color, points, 0)


def draw_circle_lines(surf, rads, rotate=False):
    for iters in range(3):
        if rotate:
            tmp = radians(120 * iters)
            draw_arrow(surf, WHITE,
                       ((sin(tmp) * rads[0] + 300) * 4, (cos(tmp) * rads[0] + 300) * 4),
                       ((sin(tmp) * rads[1] + 300) * 4, (cos(tmp) * rads[1] + 300) * 4), 40)
        else:
            tmp = radians(120 * iters + 60)
            draw_arrow(surf, WHITE,
                       ((sin(tmp) * rads[1] + 300) * 4, (cos(tmp) * rads[1] + 300) * 4),
                       ((sin(tmp) * rads[0] + 300) * 4, (cos(tmp) * rads[0] + 300) * 4), 40)


t = pygame.surface.Surface((2400, 2400))

draw_circle_lines(t, [30, 98])
draw_circle_lines(t, [100, 180], True)
pygame.draw.circle(t, WHITE, (1200, 1200), 400, 40)

clock = pygame.time.Clock()
clock.tick(60)

screen.blit(antialiasing(t, 4), (0, 0))

pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()
