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


def gradient(col, col2, cof):
    return round(col * cof + col2 * (1 - cof))


def render_scale(val: int):
    return round(val * COF)


# --== [НАЧАЛО РАБОТЫ С КЛАССОМ МИРА] ==--

class Block:
    def __init__(self, cord: tuple, t: int):
        self.cord = tuple(cord)
        self.type = int(t)

    def get_cord(self) -> tuple:
        return self.cord

    def get_type(self) -> int:
        return self.type


class World:  # Класс мира
    def __init__(self):
        pass



def global_render_chunk(board):
    ground = pygame.Surface((1020, 1020))
    for i in board['landscape']:
        t = i.get_type()
        if t == 1:
            block = pygame.image.load('grass.png').convert()
        elif t == 2:
            block = pygame.image.load('stone.png').convert()
        else:
            block = pygame.image.load('sand.png').convert()
        cord = i.get_cord()
        block_rect = block.get_rect(topleft=(tuple([j * 32 for j in cord])))
        ground.blit(block, block_rect)


    return ground


class Chunk:  # Класс чанка мира
    def __init__(self, seed: int, cord: (int, int)):
        self.seed = seed
        self.cord = cord

        self.board = {'landscape': set(), 'buildings': {}, 'mechanisms': {}, 'entities': {}}
        self.ground = pygame.Surface((1020, 1020))

        self.blocks = [pygame.image.load('grass.png').convert(), pygame.image.load('stone.png').convert(), pygame.image.load('sand.png').convert()]

    def generate_сhunk(self) -> None:
        random.seed(self.seed)
        del self.board
        self.board = {'landscape': set(), 'buildings': {}, 'mechanisms': {}, 'entities': {}}
        for y in range(32):
            for x in range(32):
                self.board['landscape'].add(Block((x, y), random.randint(0, 2)))


    def render_chunk(self) -> None:
        del self.ground
        self.ground = pygame.Surface((1020, 1020))
        self.ground.fill((55, 5, 4))
        for i in self.board['landscape']:
            cord = i.get_cord()
            block_rect = self.blocks[i.get_type()].get_rect(topleft=(tuple([j * 32 for j in cord])))
            self.ground.blit(self.blocks[i.get_type()], block_rect)
            del cord, i, block_rect,

    def get_s(self):
        return self.ground


aa = False
map_c = [0, 0]
tmp = Chunk(1, (0, 0))
tmp.generate_сhunk()
tmp.render_chunk()

start_time_m = time.time()
for _ in range(10):
    start_time = time.time()
    tmp.seed = tmp.seed + 1
    tmp.generate_сhunk()
    tmp.render_chunk()
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
                    start_time = time.time()
                    tmp.seed = tmp.seed + 1
                    tmp.generate_сhunk()
                    tmp.render_chunk()
                    print("--- %s seconds ---" % (time.time() - start_time))
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            map_c[0] += 5
        if keys[pygame.K_LEFT]:
            map_c[0] -= 5
        if keys[pygame.K_DOWN]:
            map_c[1] += 5
        if keys[pygame.K_UP]:
            map_c[1] -= 5

        screen.blit(tmp.get_s(), map_c)

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
