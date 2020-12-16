import random
import time
from copy import copy
from screeninfo import get_monitors
from numba import cuda
from threading import currentThread

import pygame
from math import sin, cos

pygame.init()

fullscreen = False
MAP_COF = 0.25

if fullscreen:
    size = width, height = get_monitors()[0].width, get_monitors()[0].height
    COF = width / 640
    screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
else:
    COF = 2.1
    size = width, height = int(640 * COF), int(360 * COF)
    screen = pygame.display.set_mode(size)

pygame.display.set_caption('World')

fps = 60
clock = pygame.time.Clock()


def gradient(col, col2, cof):
    return round(col * cof + col2 * (1 - cof))


def render_scale(val: int):
    return round(val * COF)


def map_scale(val: int):
    return round(val * MAP_COF)


# --== [НАЧАЛО РАБОТЫ С КЛАССОМ МИРА] ==--

# -------------
# |   Блоки   |
# -------------

TYPE_BLOCKS = {1: 'grass', 2: 'stone', 3: 'sand'}


class Obekt:
    def __init__(self, cord: tuple, preor=0):
        self.cord = cord
        self.importance = preor

    def get_x(self) -> int:
        return int(self.cord[0])

    def get_y(self) -> int:
        return int(self.cord[1])

    def get_preor(self) -> int:
        return int(self.importance)

    def get_cord(self) -> tuple:
        return tuple(self.cord)


class Landscape(Obekt):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)


class Grass(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 1


class Stone(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 2


class Sand(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 3


# -------------------
# |   Конец Блоки   |
# -------------------

class World:  # Класс мира
    def __init__(self, world_seed, center_chunk_cord):
        self.world_seed = world_seed
        self.chunks = set()
        self.center_chunk_cord = center_chunk_cord

    def init(self):
        for y in range(-1, 2):
            for x in range(-1, 2):
                self.chunks.add(Chunk(sum([x, y]), (x, y)))

        for i in self.chunks:
            i.generate_chunk()
            i.render_chunk()

    def add_chunk(self, cord, seed):
        self.chunks.add(Chunk(seed, cord))

    def del_chunk(self, cord):
        for i in self.chunks:
            if i.get_cord() == cord:
                self.chunks.remove(i)
                break

    def re_render(self):
        chunk = list()
        dd = list(filter(lambda x: x.get_cord == self.center_chunk_cord, self.center_chunk_cord))[0]
        print(dd)

    def render(self, surf):
        wid = 1020 * MAP_COF
        tmp_world_surf = pygame.Surface((map_scale(1020) * 3, map_scale(1020) * 3))
        for y in range(-1, 2):
            for x in range(-1, 2):
                chunk_cord = tuple([x + self.center_chunk_cord[0], y + self.center_chunk_cord[1]])
                try:
                    chunk_surf = list(filter(lambda i: i.get_cord() == chunk_cord, self.chunks))[0].get_s()
                except IndexError:
                    raise ValueError(f'Chunk ({chunk_cord}) not found!')

                tmp_world_surf.blit(chunk_surf, (chunk_cord[1] * wid + wid, chunk_cord[0] * wid + wid))
                '''pygame.draw.rect(tmp_world_surf, (255, 255, 255),
                                 ((chunk_cord[0] + 1) * wid, (chunk_cord[1] + 1) * wid, chunk_cord[0] * wid + wid,
                                   chunk_cord[1] * wid + wid), 10)'''

        surf.blit(tmp_world_surf, map_c)


def load_world(self, file):
    pass


class Chunk:  # Класс чанка мира
    def __init__(self, seed: int, cord: (int, int)):
        self.seed = seed
        self.cord = cord

        self.board = {'landscape': set(), 'buildings': {}, 'mechanisms': {}, 'entities': {}}
        self.ground = pygame.Surface((map_scale(1020), map_scale(1020)))

        self.blocks = [pygame.image.load('none.jpg').convert(), pygame.image.load('grass.png').convert(),
                       pygame.image.load('stone.png').convert(),
                       pygame.image.load('sand.png').convert()]

        for num, el in enumerate(self.blocks):
            self.blocks[num] = pygame.transform.scale(el, (map_scale(32), map_scale(32)))

    def generate_chunk(self) -> None:
        generator = random
        generator.seed(self.seed)
        del self.board
        self.board = {'landscape': set(), 'buildings': {}, 'mechanisms': {}, 'entities': {}}
        for y in range(32):
            for x in range(32):
                self.board['landscape'].add([Grass((x, y)), Stone((x, y)), Sand((x, y))][generator.randint(0, 2)])
        del generator

    def render_chunk(self) -> None:
        del self.ground
        self.ground = pygame.Surface((map_scale(1020), map_scale(1020)))
        self.ground.fill((55, 5, 4))
        for i in self.board['landscape']:
            cord = i.get_cord()
            block_rect = self.blocks[i.get_type()].get_rect(topleft=(tuple([j * 32 * MAP_COF for j in cord])))
            self.ground.blit(self.blocks[i.get_type()], block_rect)
            del cord, i, block_rect,

    def get_s(self):
        return self.ground

    def get_cord(self):
        return tuple(self.cord)

    def load(self, data):
        pass

    def update(self, data):
        pass


aa = False
map_c = [0, 0]
tmp = World(1, (0, 0))
tmp.init()
start_time_m = time.time()
for _ in range(0):
    start_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))
print()
print("--- %s seconds --- MAIN" % (time.time() - start_time_m))
if __name__ == '__main__':
    running = True

    while running:
        screen.fill((100, 0, 0))
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cords = event.pos
                    aa = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            map_c[0] += 5
        if keys[pygame.K_LEFT]:
            map_c[0] -= 5
        if keys[pygame.K_DOWN]:
            map_c[1] += 5
        if keys[pygame.K_UP]:
            map_c[1] -= 5

        tmp.render(screen)

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
