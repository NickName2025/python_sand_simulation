from settings import CEIL_SIZE, CHUNK_SIZE, sand_colors, stone_colors

from random import randint

from vec2 import vec2

import pygame


class Chunk:
    def __init__(self, x, y):
        self.pos = vec2(x, y)

        self.surface = pygame.Surface((CEIL_SIZE * CHUNK_SIZE, CEIL_SIZE * CHUNK_SIZE)).convert_alpha()
        self.surface.fill((0, 0, 0, 0))

        self.is_empty = True

        self.data = {}

    def change_pixel(self, x, y, to, to_color, speed):
        match to:
            case 1:
                self.is_empty = False
                self.data[(x, y)] = [to, to_color if to_color else sand_colors[randint(0, len(sand_colors) - 1)], 1]
            case 2:
                self.is_empty = False
                self.data[y][x] = [to, to_color if to_color else stone_colors[randint(0, len(stone_colors) - 1)], 1]

    def redraw_pixel(self, x, y):
        if (x, y) in self.data and (self.data[(x, y)][0] in [1, 2]):
            pygame.draw.rect(self.surface, self.data[(x, y)][1], (x * CEIL_SIZE, y * CEIL_SIZE, CEIL_SIZE, CEIL_SIZE))
        else:
            pygame.draw.rect(self.surface, (0, 0, 0, 0), (x * CEIL_SIZE, y * CEIL_SIZE, CEIL_SIZE, CEIL_SIZE))


    def draw(self, surface, pos):
        surface.blit(self.surface, pos)