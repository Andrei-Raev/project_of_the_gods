# ---------- IMPORTS ----------
# Импорт системных библиотек
import sys
import math
import time
import importlib.util
from itertools import product

# Импорт сторонних библиотек
import pygame
from PIL import Image

pygame.init()

from screeninfo import get_monitors

# Создание 2 рандомов (для генерации шума и для прочих целей)
RAND = importlib.util.find_spec('random')
noise_random = importlib.util.module_from_spec(RAND)
RAND.loader.exec_module(noise_random)
sys.modules['noise_random'] = noise_random

random = importlib.util.module_from_spec(RAND)
RAND.loader.exec_module(random)
sys.modules['random'] = random
del RAND


# ---------- FUNCTIONS ----------
# Генерация градиента
def gradient(col: int, col2: int, cof: float) -> int:
    return round(col * cof + col2 * (1 - cof))


# Масштабирование элементов интерфейса
def render_scale(val: int) -> int:
    return round(val * COF)


# Масштабирование карты
def map_scale(val: int) -> int:
    return round(val * MAP_COF)


# Конвертирует коэфицент шума перлина в блок
def color_asian(cof: float, cordss: tuple):
    if -0.5 <= cof <= 0.5:
        cof = cof * 1.8
    else:
        if cof > 0:
            cof = (cof - 0.5) * 0.2 + 0.9
        else:
            cof = (cof + 0.5) * 0.2 - 0.9
    cof += .25
    if cof <= 0:
        return Water(cordss)
    else:
        if 0 <= cof < 0.1:
            return Sand(cordss)  # Пляж
        elif 0.1 <= cof < 0.35:
            return Grass(cordss)  # Луга
        elif 0.35 <= cof < 0.5:
            return Grass(cordss)  # Равнины
        elif 0.5 <= cof < 0.85:
            return Stone(cordss)  # Горы
        else:
            return Stone(cordss)  # Снег в горах


# Генерирует "случайный" сид, исходя из координат
def seed_from_cord(x: int, y: int) -> int:
    tmp = x << abs(y)
    if tmp.bit_length() < 16:
        return tmp
    else:
        while tmp.bit_length() > 16:
            tmp = round(tmp / 1000)
        return tmp


def save_s(surface):
    strFormat = 'RGBA'

    raw_str = pygame.image.tostring(surface, strFormat, False)
    image = Image.frombytes(strFormat, surface.get_size(), raw_str)
    image.save(f'test/{round(random.random(), 20)}.png')
    del strFormat, raw_str, image


# ---------- PERLIN NOISE ----------
# Магия!!!
def smoothstep(t):
    return t * t * (3. - 2. * t)


def lerp(t, a, b):
    return a + t * (b - a)


class PerlinNoiseFactory(object):
    def __init__(self, dimension, octaves=1, seed=1, tile=(), unbias=False):
        self.dimension = dimension
        self.octaves = octaves
        self.tile = tile + (0,) * dimension
        self.unbias = unbias
        self.scale_factor = 2 * dimension ** -0.5
        self.random = noise_random
        self.random.seed(seed)
        self.seed = seed

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


# ---------- FPS CLOCK ----------
# Создание шрифта для счетчика fps
def create_fonts(font_sizes_list):
    fonts = []
    for size in font_sizes_list:
        fonts.append(
            pygame.font.SysFont("Arial", size))
    return fonts


# Рендер четчика fps
def render(fnt, what, color, where):
    text_to_show = fnt.render(what, 0, pygame.Color(color))
    screen.blit(text_to_show, where)


# Отображение четчика fps
def display_fps():
    render(
        fonts[0],
        what=str(int(clock.get_fps())),
        color="white",
        where=(0, 0))


# ---------- BLOCKS ----------

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


class Water(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 4


# -------------------
# |   Конец Блоки   |
# -------------------


# ---------- WORLD ----------
class World:  # Класс мира
    def __init__(self, world_seed, center_chunk_cord, seed):
        self.world_seed = world_seed
        self.chunks = set()
        self.center_chunk_cord = center_chunk_cord
        self.noise = PerlinNoiseFactory(2, octaves=4, unbias=False, seed=seed)

    def init(self):
        for y in range(-1, 2):
            for x in range(-1, 2):
                self.chunks.add(
                    Chunk(seed_from_cord(x, y), (x + self.center_chunk_cord[0], y + self.center_chunk_cord[1])))

        for i in self.chunks:
            i.generate_chunk(self.noise)
            # i.load()
            i.render_chunk()

    def add_chunk(self, cord):
        self.chunks.add(Chunk(seed_from_cord(*cord), cord))

    def del_chunk(self, cord):
        for i in self.chunks:
            if i.get_cord() == cord:
                self.chunks.remove(i)
                break

    def render(self, surf):
        wid = 510 * MAP_COF
        tmp_world_surf = pygame.Surface((map_scale(510) * 3, map_scale(510) * 3))
        for y in range(-1 + self.center_chunk_cord[1], 2 + self.center_chunk_cord[1]):
            for x in range(-1 + self.center_chunk_cord[0], 2 + self.center_chunk_cord[0]):
                chunk_cord = tuple([x, y])
                try:
                    chunk_surf = list(filter(lambda i: i.get_cord() == chunk_cord, self.chunks))[0].get_s()
                except IndexError:
                    # raise ValueError(f'Chunk ({chunk_cord}) not found!')
                    self.chunks.add(Chunk(seed_from_cord(*chunk_cord), chunk_cord))
                    tmp_chunk = list(filter(lambda i: i.get_cord() == chunk_cord, self.chunks))[0]
                    tmp_chunk.generate_chunk(self.noise)
                    tmp_chunk.render_chunk()
                    chunk_surf = tmp_chunk.get_s()
                    print('000')
                    # save_s(chunk_surf)

                tmp_world_surf.blit(chunk_surf, ((chunk_cord[1] - self.center_chunk_cord[1]) * wid + wid,
                                                 (chunk_cord[0] - self.center_chunk_cord[0]) * wid + wid))
        surf.blit(tmp_world_surf, [i - map_scale(510) for i in map_c])

    def re_render(self):
        chunk = list()
        dd = list(filter(lambda x: x.get_cord == self.center_chunk_cord, self.center_chunk_cord))[0]
        print(dd)

    def move_visible_area(self, direction: int):  # 1 - вверх, 2 - вниз, 3 - влево, 4 - вправо
        if direction == 1:
            self.center_chunk_cord = (self.center_chunk_cord[0], self.center_chunk_cord[1] + 1)
        elif direction == 2:
            self.center_chunk_cord = (self.center_chunk_cord[0], self.center_chunk_cord[1] - 1)
        elif direction == 3:
            self.center_chunk_cord = (self.center_chunk_cord[0] + 1, self.center_chunk_cord[1])
        elif direction == 4:
            self.center_chunk_cord = (self.center_chunk_cord[0] - 1, self.center_chunk_cord[1])

    def load_world(self, file):
        pass

    def save_world(self):
        for i in self.chunks:
            i.save(f'save_data/{i.get_cord()}.ch')


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

    def generate_chunk(self, world_noise) -> None:
        del self.board
        self.board = {'landscape': set(), 'buildings': set(), 'mechanisms': {}, 'entities': {}}
        for y in range(16):
            for x in range(16):
                tmp_noise = world_noise((x + (self.cord[1]) * 16) / world_noise_size,
                                        (y + (self.cord[0]) * 16) / world_noise_size)
                self.board['landscape'].add(color_asian(tmp_noise, (x, y)))

    def render_chunk(self) -> None:
        del self.ground
        self.ground = pygame.Surface((map_scale(510), map_scale(510)))
        self.ground.fill((55, 5, 4))
        for i in self.board['landscape']:
            cord = i.get_cord()
            block_rect = self.blocks[i.get_type()].get_rect(topleft=(tuple([j * 32 * MAP_COF for j in cord])))
            self.ground.blit(self.blocks[i.get_type()], block_rect)
            del cord, i, block_rect

        # f = pygame.font.Font(None, 100)
        # r = f.render(f'{self.cord}', True,(255,255,255))
        # self.ground.blit(r, (50,50))

        # f = pygame.font.Font(None, 250)
        # t = f.render(f'{self.cord}', True, (255, 255, 255))
        # self.ground.blit(t, (25, 25))

    def get_s(self):
        return self.ground

    def get_cord(self):
        return tuple(self.cord)

    def __str__(self):
        return f'Chunk {self.cord}'

    def load(self):
        self.board = decode_chunk(self.cord)

    def update(self, data):
        pass

    def save(self, name_f):
        raw = b''

        for i in self.board['landscape']:
            raw += i.get_type().to_bytes(1, byteorder="little")
            raw += cord_codec(i.get_cord())

        with open(name_f, 'wb') as byte_file:
            byte_file.write(raw)


def cord_codec(cors: tuple) -> bytes:
    raw = b''
    for i in cors:
        raw += i.to_bytes(1, byteorder="little")
    return raw


def decode_chunk(file_path):
    board = {'landscape': set()}
    with open(f'save_data/{file_path}.ch', 'rb') as byte_file:
        chunk_raw = byte_file.read()
        for i in range(len(chunk_raw) // 3):
            tmp_type = chunk_raw[i * 3]
            tmp_cord_x = int.from_bytes(chunk_raw[i * 3 + 1:i * 3 + 2], 'little')
            tmp_cord_y = int.from_bytes(chunk_raw[i * 3 + 2:i * 3 + 3], 'little')
            print(tmp_type != 1)
            if tmp_type == 1:
                board['landscape'].add(Grass((tmp_cord_x, tmp_cord_y)))
            elif tmp_type == 2:
                board['landscape'].add(Stone((tmp_cord_x, tmp_cord_y)))
            elif tmp_type == 3:
                board['landscape'].add(Sand((tmp_cord_x, tmp_cord_y)))
            elif tmp_type == 4:
                board['landscape'].add(Water((tmp_cord_x, tmp_cord_y)))
    return board


# ============================================
fonts = create_fonts([32, 16, 14, 8])

fullscreen = False
MAP_COF = 1
WORLD_SIZE = {'small': 100, 'medium': 250, 'large': 500}
world_noise_size = 50

if fullscreen:
    size = width, height = get_monitors()[0].width, get_monitors()[0].height
    COF = width / 640
    screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
else:
    COF = 2
    size = width, height = int(640 * COF), int(360 * COF)
    screen = pygame.display.set_mode(size)

pygame.display.set_caption('World')

fps = 60
clock = pygame.time.Clock()

# open("a.txt", "w").close()


aa = False
map_c = [0, 0]

start_time_m = time.time()
for _ in range(0):
    start_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))
print()
tmp = World(0, (0, 0), 22)
tmp.init()
tmp.save_world()
print("--- %s seconds --- MAIN" % (time.time() - start_time_m))
if __name__ == '__main__':
    running = True
    while running:

        # world_noise = PerlinNoiseFactory(2, octaves=4, unbias=False, seed=random.randint(1, 55))
        # tmp = World(0, (0, 0))
        # tmp.init()
        # raise Exception("hui")
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
                    # tmp.move_visible_area(3)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            map_c[0] += 5
        if keys[pygame.K_LEFT]:
            map_c[0] -= 5
        if keys[pygame.K_DOWN]:
            map_c[1] += 5
        if keys[pygame.K_UP]:
            map_c[1] -= 5

        if map_c[0] < -map_scale(510):
            tmp.move_visible_area(1)
            map_c[0] = 0
        elif map_c[0] > map_scale(510):
            tmp.move_visible_area(2)
            map_c[0] = 0
        if map_c[1] < -map_scale(510):
            tmp.move_visible_area(3)
            map_c[1] = 0
        elif map_c[1] > map_scale(510):
            tmp.move_visible_area(4)
            map_c[1] = 0

        tmp.render(screen)
        display_fps()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
