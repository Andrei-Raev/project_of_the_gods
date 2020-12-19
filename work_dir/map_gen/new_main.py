import numpy as np
import random
from math import tan, sqrt
# import pygame
from numba import njit

SIZE = 25
SCALE = 20

random.seed(1)

world = (
    [[[round(random.uniform(-1, 1), 10), round(random.uniform(-1, 1), 10)] for _ in range(SIZE)] for _ in range(SIZE)])

for i in enumerate(world):
    for j in enumerate(i[1]):
        v = tuple(j[1])
        world[i[0]][j[0]] = list([v[0] / sqrt(v[0] ** 2 + v[1] ** 2), v[1] / sqrt(v[0] ** 2 + v[1] ** 2)])
del v

world_noise = [[None] * (SCALE*SIZE)]

print(len(world_noise))
for i in range(SIZE - 1):
    for j in range(SIZE - 1):
        vect = list([world[i][j], world[i][j + 1], world[i + 1][j], world[i + 1][j + 1]])
        for i_t in range(SCALE):
            for j_t in range(SCALE):
                print((vect[0][0] * i_t + vect[0][1] * j_t), end='\t')
            print()
        print('\n\n')

print(*world_noise, sep='\n')
del world, world_noise

'''
if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    # размеры окна:
    size = width, height = 800, 600
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    # формирование кадра:
    # команды рисования на холсте
    # ...
    screen.fill((0, 0, 0))
    for num, el in enumerate(world):
        pygame.draw.rect(screen, ([abs(min(round(el * 150), 255))] * 3), (num, 0, num, width))
    # ...
    # смена (отрисовка) кадра:
    pygame.display.flip()
    # ожидание закрытия окна:
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()
'''
