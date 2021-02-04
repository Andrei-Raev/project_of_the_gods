# ---------- IMPORTS ----------
# Импорт системных библиотек
import sys
import math
import time
import importlib.util

# Импорт сторонних библиотек
# from threading import Thread
from copy import copy

from PIL import Image, ImageFilter
from pygame.threads import Thread
from screeninfo import get_monitors

import pygame

pygame.init()

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


def bright(surf: pygame.surface.Surface, brightness):
    image = Image.frombytes('RGBA', surf.get_size(), pygame.image.tostring(surf, 'RGBA', False))
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b, a = image.getpixel((x, y))

            red = int(r * brightness)
            red = min(255, max(0, red))

            green = int(g * brightness)
            green = min(255, max(0, green))

            blue = int(b * brightness)
            blue = min(255, max(0, blue))

            image.putpixel((x, y), (red, green, blue, a))
    del r, g, b, a, red, green, blue, brightness
    return pygame.image.fromstring(image.tobytes("raw", 'RGBA'), image.size, 'RGBA')


def dark(surf: pygame.surface.Surface, brightness):
    image = Image.frombytes('RGBA', surf.get_size(), pygame.image.tostring(surf, 'RGBA', False))
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b, a = image.getpixel((x, y))

            red = int(r // brightness)
            red = min(255, max(0, red))

            green = int(g // brightness)
            green = min(255, max(0, green))

            blue = int(b // brightness)
            blue = min(255, max(0, blue))

            image.putpixel((x, y), (red, green, blue, a))
    del r, g, b, a, red, green, blue, brightness
    return pygame.image.fromstring(image.tobytes("raw", 'RGBA'), image.size, 'RGBA')


def get_relative_coordinates(x: int, y: int):
    x = (x % 16, x // 16)
    y = (y % 16, y // 16)
    return (x[0], y[0]), (x[1], y[1])


# ---------- FPS CLOCK ----------
# Создание шрифта для счетчика fps
def create_fonts(font_sizes_list):
    fonts = []
    for size in font_sizes_list:
        fonts.append(pygame.font.SysFont("Arial", size))
    return fonts


# Рендер четчика fps
def render(fnt, what, color, where):
    text_to_show = fnt.render(what, 0, pygame.Color(color))
    screen.blit(text_to_show, where)


# Отображение четчика fps
def display_fps():
    render(fonts[0], what=str(int(clock.get_fps())), color="white", where=(0, 0))


def blur(surface, rad):
    size = surface.get_size()
    strFormat = 'RGBA'

    raw_str = pygame.image.tostring(surface, strFormat, False)
    image = Image.frombytes(strFormat, surface.get_size(), raw_str)

    image = image.filter(ImageFilter.BoxBlur(rad))

    raw_str = image.tobytes("raw", strFormat)
    result = pygame.image.fromstring(raw_str, image.size, strFormat)
    del size, strFormat, raw_str, image
    return result


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


class Item(pygame.sprite.Sprite):
    def __init__(self, texture: pygame.image, title: str, description: str, cords: tuple, *groups):
        super().__init__(*groups)
        self.title = title
        self.description = description
        self.cords = cords
        self.image = texture
        self.is_grab = False
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.speed = 3
        self.abs_cords = (0, 0)

    def move_to_cords(self, cordss: object) -> object:
        distance = math.sqrt((cordss[0] - self.abs_cords[0]) ** 2 + (cordss[1] - self.abs_cords[1]) ** 2)

        tmp_x = self.abs_cords[0] - cordss[0]
        tmp_y = self.abs_cords[1] - cordss[1]
        try:
            angel = tmp_x / tmp_y
        except ZeroDivisionError:
            return cordss
        angel = math.degrees(math.atan(angel))

        if distance < 1:
            self.speed = 0
        elif 1 <= distance <= 30:
            if self.speed > 1:
                self.speed -= 0.5
        else:
            self.speed += 0.07

        if self.abs_cords[1] - cordss[1] < 0:
            x = self.abs_cords[0] + math.sin(angel * math.pi / 180) * self.speed
            y = self.abs_cords[1] + math.cos(angel * math.pi / 180) * self.speed
        else:
            x = self.abs_cords[0] - math.sin(angel * math.pi / 180) * self.speed
            y = self.abs_cords[1] - math.cos(angel * math.pi / 180) * self.speed

        self.abs_cords = [x, y]

        return self.abs_cords


class InventoryBoard:
    # создание поля
    def __init__(self, items):
        self.is_moving = False

        self.width = 20
        self.height = 15
        self.board = set(items)

        self.cell_size = 40
        self.left = (height - self.cell_size * self.height) // 2
        self.top = (width - self.cell_size * self.width) // 2

        self.inv_background = pygame.surface.Surface(
            (self.cell_size * self.width + width * 0.04, self.cell_size * self.height + width * 0.04))
        self.inv_background.set_colorkey((0, 0, 0))
        self.inv_background = self.inv_background.convert_alpha()
        self.render_background()

        margin = width * 0.02
        for item in self.board:
            item.abs_cords = (margin + item.cords[0] * self.cell_size, margin + item.cords[1] * self.cell_size)

    def render_background(self):
        tmp_cof = 1

        self.inv_background = pygame.surface.Surface(
            ((self.cell_size * self.width + width * 0.04) * tmp_cof,
             (self.cell_size * self.height + width * 0.04) * tmp_cof))
        self.inv_background.set_colorkey((0, 0, 0))
        self.inv_background = self.inv_background.convert_alpha()
        margin = width * 0.02

        pygame.draw.rect(self.inv_background, (100, 100, 100),
                         (7, 7, (self.cell_size * self.width + width * 0.04 - 7) * tmp_cof,
                          (self.cell_size * self.height + width * 0.04 - 7) * tmp_cof), 0, 55 * tmp_cof)
        pygame.draw.rect(self.inv_background, (150, 150, 150),
                         (0, 0, (self.cell_size * self.width + width * 0.04) * tmp_cof,
                          (self.cell_size * self.height + width * 0.04) * tmp_cof), 10 * tmp_cof, 55 * tmp_cof)
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(self.inv_background, (255, 255, 255),
                                 ((self.cell_size * i + margin) * tmp_cof, (self.cell_size * j + margin) * tmp_cof,
                                  (self.cell_size - 1) * tmp_cof, (self.cell_size - 1) * tmp_cof), 3 * tmp_cof,
                                 8 * tmp_cof)

        self.inv_background = antialiasing(self.inv_background, tmp_cof)

    def render_main(self):
        self.screen = copy(self.inv_background)
        margin = width * 0.02

        for item in self.board:
            if not item.is_grab:
                self.screen.blit(item.image, item.move_to_cords(margin + item.cords[0] * self.cell_size,
                                                                margin + item.cords[1] * self.cell_size))
            else:
                self.screen.blit(item.image, item.move_to_cords(pygame.mouse.get_pos()[0] - self.top + margin,
                                                                pygame.mouse.get_pos()[1] - self.left + margin))

    def render(self, a):
        """
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(a, (255, 255, 255),
                                 (self.top + self.cell_size * i, self.left + self.cell_size * j, self.cell_size - 1,
                                  self.cell_size - 1), 5, 8)"""
        self.render_main()
        a.blit(self.screen, (self.top - width * 0.02, self.left - width * 0.02))

    def click(self, cord: tuple):
        """print(self.height)
        pygame.draw.rect(screen, (200, 200, 200),(self.top, self.left,self.top + (self.height-1) * self.cell_size,self.left + (self.width-1) * self.cell_size), 10)
        print(self.top <= cord[1] <= self.top + self.height * self.cell_size, self.left <= cord[
            0] <= self.left + (self.width-1) * self.cell_size)
        if self.top <= cord[0] <= self.top + (self.height-1) * self.cell_size and self.left <= cord[
            1] <= self.left + self.width * self.cell_size:
            x = (cord[0] - self.left) // self.cell_size
            y = (cord[1] - self.top) // self.cell_size"""
        if self.top <= cord[0] <= self.top + self.width * self.cell_size and self.left <= cord[
            1] <= self.left + self.height * self.cell_size:
            x = (cord[0] - self.top) // self.cell_size
            y = (cord[1] - self.left) // self.cell_size

            if self.is_moving:
                self.is_moving = False
                self.move_item(self.old_cords, (x, y))

                tmp_item = list(filter(lambda it: it.cords == (x, y), self.board))[0]
                self.board.remove(tmp_item)
                tmp_item.is_grab = False
                self.board.add(tmp_item)

            elif list(filter(lambda it: it.cords == (x, y), self.board)) and not self.is_moving:
                print(x, y)
                self.old_cords = x, y
                self.is_moving = True

                tmp_item = list(filter(lambda it: it.cords == (x, y), self.board))[0]
                self.board.remove(tmp_item)
                tmp_item.is_grab = True
                self.board.add(tmp_item)
        else:
            print(None)

    def add_item(self, item: Item):
        margin = width * 0.02
        item.abs_cords = (margin + item.cords[0] * self.cell_size, margin + item.cords[1] * self.cell_size)
        self.board.add(item)

    def move_item(self, start_cord, end_cord):
        '''
        if self.board[start_cord[1]][start_cord[0]] is not None:
            if self.board[end_cord[1]][end_cord[0]] is None:
                self.board[end_cord[1]][end_cord[0]] = self.board[start_cord[1]][start_cord[0]]
                self.board[start_cord[1]][start_cord[0]] = None'''
        if list(filter(lambda x: x.cords == start_cord, self.board)):
            if not list(filter(lambda x: x.cords == end_cord, self.board)):
                tmp_item = list(filter(lambda x: x.cords == start_cord, self.board))[0]
                self.board.remove(tmp_item)
                tmp_item.cords = end_cord
                self.board.add(tmp_item)


def inventory():
    global main_running
    global screen
    speed = 10
    is_open = True
    background = blur(screen, 15)
    screen.blit(background, (0, 0))
    board = InventoryBoard([])

    for i in range(1):
        for j in range(1):
            board.add_item(Item(pygame.image.load('test.png'), 'Тестовый предмет', 'Это просто магия', (i, j)))

    while is_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_ESCAPE:
                    is_open = False
            elif event.type == pygame.MOUSEMOTION:
                pass
                # pl.move(event.rel)

        # screen.blit(background, (0, 0))
        board.render(screen)
        display_fps()
        clock.tick(fps)
        pygame.display.flip()


# Таймер для подсчета работы кода
# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))

# ---------- CONSTANTS ----------
TYPE_BLOCKS = {1: 'grass', 2: 'stone', 3: 'sand'}
FULLSCREEN = False
MAP_COF = 1
WORLD_SIZE = {'small': 100, 'medium': 250, 'large': 500}
WORLD_NOISE_SIZE = 50
BLOCK_SIZE = MAP_COF * 32

# ---------- VARIABLES ----------
fonts = create_fonts([32, 16, 14, 8])
map_cords = [0, 0]
fps = 60
clock = pygame.time.Clock()

# ---------- INIT ----------
if FULLSCREEN:
    size = width, height = get_monitors()[0].width, get_monitors()[0].height
    COF = width / 640
    screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
else:
    COF = 2
    size = width, height = int(640 * COF), int(360 * COF)
    screen = pygame.display.set_mode(size)

pygame.display.set_caption('Inventory')

if __name__ == '__main__':
    main_running = True
    im = pygame.image.load('im.png')

    while main_running:
        # world_noise = PerlinNoiseFactory(2, octaves=4, unbias=False, seed=random.randint(1, 55))
        # tmp = World(0, (0, 0))
        # tmp.init()
        # raise Exception("hui")

        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                main_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cords = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                    # tmp.move_visible_area(3)
            elif event.type == pygame.MOUSEMOTION:
                pass
                # pl.move(event.rel)

        '''keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            map_cords[0] += 5
        if keys[pygame.K_LEFT]:
            map_cords[0] -= 5
        if keys[pygame.K_DOWN]:
            map_cords[1] += 5
        if keys[pygame.K_UP]:
            map_cords[1] -= 5

        if map_cords[0] < -map_scale(510):
            tmp.move_visible_area(1)
            map_cords[0] = 0
        elif map_cords[0] > map_scale(510):
            tmp.move_visible_area(2)
            map_cords[0] = 0
        if map_cords[1] < -map_scale(510):
            tmp.move_visible_area(3)
            map_cords[1] = 0
        elif map_cords[1] > map_scale(510):
            tmp.move_visible_area(4)
            map_cords[1] = 0
        pl.tick()
        print(pl.get_cord())'''

        # Рендер основного окна
        screen.fill((47, 69, 56))
        screen.blit(im, (10, 10))
        display_fps()
        inventory()
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()  # Завершение работы
