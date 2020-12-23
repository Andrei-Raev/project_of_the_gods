import time

import pygame
from perlin_lib import PerlinNoiseFactory
from numba import njit

size = 200
res =70
frames = 1

pnf = PerlinNoiseFactory(3, octaves=4, tile=(15, 15, 15), unbias=True)
pnf_bioms = PerlinNoiseFactory(3, octaves=1, tile=(10, 10, 10), unbias=False)

world_noise = [list()]


@njit()
def get_biome(cof):
    if -0.5 <= cof <= 0.5:
        cof = cof * 1.8
    else:
        if cof > 0:
            cof = (cof - 0.5) * 0.2 + 0.9
        else:
            cof = (cof + 0.5) * 0.2 - 0.9

    if cof <= 0:
        if -0.3 < cof <= 0:
            return 0, 60, 151  # Тайга
        elif -0.8 < cof <= -0.3:
            return 0, 30, 101  # тундра
        elif cof <= -0.8:
            return 0, 30, 101  # Ледяные пустоши
    else:
        if 0 <= cof < 0.05:
            return 250, 254, 100  # Пляж
        elif 0.05 <= cof < 0.35:
            return 0, 151, 20  # Луга
        elif 0.35 <= cof < 0.5:
            return 1, 120, 48  # Равнины
        elif 0.5 <= cof < 0.85:
            return 121, 119, 120  # Горы
        else:
            return 255, 255, 255  # Снег в горах
    return 0, 0, 0  # На всякий случай


@njit()
def color_asian(cof):
    if -0.5 <= cof <= 0.5:
        cof = cof * 1.8
    else:
        if cof > 0:
            cof = (cof - 0.5) * 0.2 + 0.9
        else:
            cof = (cof + 0.5) * 0.2 - 0.9

    if cof <= 0:
        if -0.05 < cof <= 0:
            return 0, 60, 151  # Мелководье
        elif cof <= -0.05:
            return 0, 30, 101  # Вода
    else:
        if 0 <= cof < 0.05:
            return 250, 254, 100  # Пляж
        elif 0.05 <= cof < 0.35:
            return 0, 151, 20  # Луга
        elif 0.35 <= cof < 0.5:
            return 1, 120, 48  # Равнины
        elif 0.5 <= cof < 0.85:
            return 121, 119, 120  # Горы
        else:
            return 255, 255, 255  # Снег в горах
    return 0, 0, 0  # На всякий случай

start_time = time.time()

for x in range(size):
    for y in range(size):
        n = pnf(x / res, y / res, 0)
        world_noise[-1].append(n)
    world_noise.append(list())
# print(*world_noise)
print('GENERATED!')

if __name__ == '__main__':
    pygame.init()
    size = width, height = size, size
    screen = pygame.display.set_mode(size)
    # ...
    screen.fill((0, 0, 0))

    for num, el in enumerate(world_noise):
        for num_2, el_2 in enumerate(el):
            try:
                pygame.draw.rect(screen, color_asian(el_2), (num, num_2, num, num_2))
                # print(color_asian(el_2), (num, num_2, num, num_2), sep='\t')
            except Exception as e:
                print(e)
    # ...
    print('DONE!')
    pygame.display.flip()
    print("--- %s seconds ---" % (time.time() - start_time))
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
