import random

import pygame

from PIL import Image


def antialiasing(surface, size_cof):
    size = surface.get_size()
    size = [i // size_cof for i in size]
    strFormat = 'RGBA'

    raw_str = pygame.image.tostring(surface, strFormat, False)
    image = Image.frombytes(strFormat, surface.get_size(), raw_str)
    # image.show()
    image = image.resize(size, resample=Image.ANTIALIAS)

    raw_str = image.tobytes("raw", strFormat)
    # image.show()
    result = pygame.image.fromstring(raw_str, image.size, strFormat)

    return result


HEIGHT = 1280
WIDTH = 720

size = width, height = 700, 700

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('None')
    screen.fill((0, 0, 0))

    COF = 4
    tmp = pygame.Surface((600 * COF, 600 * COF))

    pygame.draw.circle(tmp, (255, 255, 255), (300 * COF, 300 * COF), 300 * COF, 0)
    tmp = antialiasing(tmp, COF)

    # ...
    screen.blit(tmp, (50, 50))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
