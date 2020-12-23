import random
import time
from copy import copy
from screeninfo import get_monitors

import pygame
from math import sin, cos

pygame.init()

from itertools import product
import math
import random


def smoothstep(t):
    return t * t * (3. - 2. * t)


def lerp(t, a, b):
    return a + t * (b - a)


class PerlinNoiseFactory(object):
    def __init__(self, dimension, octaves=1, tile=(), unbias=False, seed=1):
        self.dimension = dimension
        self.octaves = octaves
        self.tile = tile + (0,) * dimension
        self.unbias = unbias
        self.scale_factor = 2 * dimension ** -0.5
        self.random = random
        self.random.seed(seed)

        self.gradient = {}

    def _generate_gradient(self):
        if self.dimension == 1:
            return (self.random.uniform(-1, 1),)
        random_point = [self.random.gauss(0, 1) for _ in range(self.dimension)]
        scale = sum(n * n for n in random_point) ** -0.5
        return tuple(coord * scale for coord in random_point)

    def get_plain_noise(self, *point):
        if len(point) != self.dimension:
            raise ValueError("Expected {} values, got {}".format(
                self.dimension, len(point)))
        grid_coords = []
        for coord in point:
            min_coord = math.floor(coord)
            max_coord = min_coord + 1
            grid_coords.append((min_coord, max_coord))
        dots = []
        for grid_point in product(*grid_coords):
            if grid_point not in self.gradient:
                self.gradient[grid_point] = self._generate_gradient()
            gradient = self.gradient[grid_point]

            dot = 0
            for i in range(self.dimension):
                dot += gradient[i] * (point[i] - grid_point[i])
            dots.append(dot)
        dim = self.dimension
        while len(dots) > 1:
            dim -= 1
            s = smoothstep(point[dim] - grid_coords[dim][0])
            next_dots = []
            while dots:
                next_dots.append(lerp(s, dots.pop(0), dots.pop(0)))
            dots = next_dots

        return dots[0] * self.scale_factor

    def __call__(self, *point):
        ret = 0
        for o in range(self.octaves):
            o2 = 1 << o
            new_point = []
            for i, coord in enumerate(point):
                coord *= o2
                if self.tile[i]:
                    coord %= self.tile[i] * o2
                new_point.append(coord)
            ret += self.get_plain_noise(*new_point) / o2
        ret /= 2 - 2 ** (1 - self.octaves)

        if self.unbias:
            r = (ret + 1) / 2
            for _ in range(int(self.octaves / 2 + 0.5)):
                r = smoothstep(r)
            ret = r * 2 - 1

        return ret


# ============================================

def init_screen_and_clock():
    global screen, display, clock
    pygame.init()
    WINDOW_SIZE = (1150, 640)
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    clock = pygame.time.Clock()


def create_fonts(font_sizes_list):
    fonts = []
    for size in font_sizes_list:
        fonts.append(
            pygame.font.SysFont("Arial", size))
    return fonts


def render(fnt, what, color, where):
    text_to_show = fnt.render(what, 0, pygame.Color(color))
    screen.blit(text_to_show, where)


def display_fps():
    render(
        fonts[0],
        what=str(int(clock.get_fps())),
        color="white",
        where=(0, 0))


init_screen_and_clock()
fonts = create_fonts([32, 16, 14, 8])
# ============================================


fullscreen = True
MAP_COF = 1
WORLD_SIZE = {'small': 100, 'medium': 250, 'large': 500}
world_noise = PerlinNoiseFactory(2, octaves=1, tile=(15, 15, 15), unbias=True)
world_noise_size = 6

if fullscreen:
    size = width, height = get_monitors()[0].width, get_monitors()[0].height
    COF = width / 640
    screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
else:
    COF = 1
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


def color_asian(cof, cordss):
    if -0.5 <= cof <= 0.5:
        cof = cof * 1.8
    else:
        if cof > 0:
            cof = (cof - 0.5) * 0.2 + 0.9
        else:
            cof = (cof + 0.5) * 0.2 - 0.9

    if cof <= 0:
        return Water(cordss)
    else:
        if 0 <= cof < 0.05:
            return Sand(cordss)  # Пляж
        elif 0.05 <= cof < 0.35:
            return Grass(cordss)  # Луга
        elif 0.35 <= cof < 0.5:
            return Grass(cordss)  # Равнины
        elif 0.5 <= cof < 0.85:
            return Stone(cordss)  # Горы
        else:
            return Stone(cordss)  # Снег в горах
    return 0, 0, 0  # На всякий случай


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


class Water(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 4


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
        wid = 510 * MAP_COF
        tmp_world_surf = pygame.Surface((map_scale(510) * 3, map_scale(510) * 3))
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

    def move_visible_area(self):
        pass

    def load_world(self, file):
        pass


class Chunk:  # Класс чанка мира
    def __init__(self, seed: int, cord: (int, int)):
        self.seed = seed
        self.cord = cord

        self.board = {'landscape': set(), 'buildings': {}, 'mechanisms': {}, 'entities': {}}
        self.ground = pygame.Surface((map_scale(510), map_scale(510)))

        self.blocks = [pygame.image.load('none.jpg').convert(), pygame.image.load('grass.png').convert(),
                       pygame.image.load('stone.png').convert(),
                       pygame.image.load('sand.png').convert(), pygame.image.load('water.jpg').convert()]

        for num, el in enumerate(self.blocks):
            self.blocks[num] = pygame.transform.scale(el, (map_scale(32), map_scale(32)))

    def generate_chunk(self) -> None:
        generator = random
        generator.seed(self.seed)
        del self.board
        self.board = {'landscape': set(), 'buildings': set(), 'mechanisms': {}, 'entities': {}}
        for y in range(16):
            for x in range(16):
                tmp_noise = world_noise(x + self.cord[0] * 16 / world_noise_size,
                                        y + self.cord[1] * 16 / world_noise_size)
                self.board['landscape'].add(color_asian(tmp_noise, (x, y)))
        del generator

    def render_chunk(self) -> None:
        del self.ground
        self.ground = pygame.Surface((map_scale(510), map_scale(510)))
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
        display_fps()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
