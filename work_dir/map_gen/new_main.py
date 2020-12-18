import numpy as np
import random
from numba import njit

random.seed(1)

world = np.array([0.0] * 801)
piks = [random.randint(0, 800) for _ in range(100)]
inv_piks = [random.randint(0, 800) for _ in range(100)]

for i in piks:
    world[i] = 1.0

for i in inv_piks:
    world[i] = -1.0


def gradient(m_len, ind):
    return float(ind / m_len) * 100


def nearest_value(items, value):
    '''Поиск ближайшего значения до value в списке items'''
    found = items[0]  # найденное значение (первоначально первое)
    for item in items:
        if abs(item - value) < abs(found - value):
            found = item
    return found


def find_blizh(p, in_p, ind):
    a = nearest_value(p, ind)
    b = nearest_value(in_p, ind)
    return abs(a - b)


def last(els, num):
    # print(els, num)
    if num >= els[0]:
        return els[0]
    for i in range(0, len(els) - 1):
        if i <= num:
            # print(i, num)
            return i


def linar_noise():
    pik, = np.where(world == 1)
    inv_pik, = np.where(world == -1)

    for num, el in enumerate(world):
        world[num] = gradient(num, el)
        print('-> ', gradient(num, find_blizh(pik, inv_pik, num)))

    return


# world = np.random.normal(0, 1, 800)
'''
pik, = np.where(world == 1)
inv_pik, = np.where(world == -1)
intt = find_blizh(pik, inv_pik, 10)
'''
# linar_noise()

'''print(pik, inv_pik, intt, sep='\n')

print(*world)'''

import pygame

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
