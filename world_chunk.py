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
                self.data[(x, y)] = [to, to_color if to_color else sand_colors[randint(0, len(sand_colors) - 1)], speed]
            case 2:
                self.is_empty = False
                self.data[y][x] = [to, to_color if to_color else stone_colors[randint(0, len(stone_colors) - 1)], speed]

    def redraw_pixel(self, x, y):
        if (x, y) in self.data and (self.data[(x, y)][0] in [1, 2]):
            pygame.draw.rect(self.surface, self.data[(x, y)][1], (x * CEIL_SIZE, y * CEIL_SIZE, CEIL_SIZE, CEIL_SIZE))
        else:
            pygame.draw.rect(self.surface, (0, 0, 0, 0), (x * CEIL_SIZE, y * CEIL_SIZE, CEIL_SIZE, CEIL_SIZE))

    def simulate(self, chunks):
        for y in range(CHUNK_SIZE - 1, -1, -1):
            x_range = range(CHUNK_SIZE) if y % 2 == 0 else range(CHUNK_SIZE - 1, -1, -1)
            for x in x_range:
                if (x, y) in self.data and self.data[(x, y)][0] == 1: # Песок
                    for px, py in tuple([([-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0][randint(0, 10)], k) for k in range(int(self.data[(x, y)][2]), 0, -1)]) + ((-1, 1), (1, 1)):
                        if 0 <= (x + px) // CHUNK_SIZE + self.pos.x < len(chunks[0]) and 0 <= (y + py) // CHUNK_SIZE + self.pos.y < len(chunks):
                            chunk_data = chunks[(y + py) // CHUNK_SIZE + self.pos.y][(x + px) // CHUNK_SIZE + self.pos.x]

                            if ((x + px) % CHUNK_SIZE, (y + py) % CHUNK_SIZE) not in chunk_data.data:
                                chunk_data.change_pixel((x + px) % CHUNK_SIZE, (y + py) % CHUNK_SIZE, 1, self.data[(x, y)][1], self.data[(x, y)][2] + self.data[(x, y)][2] / 20)
                                chunk_data.redraw_pixel((x + px) % CHUNK_SIZE, (y + py) % CHUNK_SIZE)

                                del self.data[(x, y)]
                                self.redraw_pixel(x, y)
                                self.is_empty = not self.data
                                break


    def draw(self, surface, pos):
        surface.blit(self.surface, pos)