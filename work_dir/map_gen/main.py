import pygame
from perlin_lib import PerlinNoiseFactory
import PIL.Image

size = 200
res = 40
frames = 1


pnf = PerlinNoiseFactory(3, octaves=4, tile=(10, 10, 10))

world_noise = [list()]

for x in range(size):
    for y in range(size):
        n = pnf(x / res, y / res, 0.1)
        world_noise[-1].append(n)
    world_noise.append(list())


print('GENERATED!')

if __name__ == '__main__':
    pygame.init()
    size = width, height = 200, 200
    screen = pygame.display.set_mode(size)
    # ...
    screen.fill((0, 0, 0))

    for num, el in enumerate(world_noise):
        for num_2, el_2 in enumerate(el):
            pygame.draw.rect(screen, ([(el_2 + 1) * 100]*3), (num, num_2, num, num_2))
    # ...
    print('DONE!')
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()