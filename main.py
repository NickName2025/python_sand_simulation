from pygame.locals import QUIT, MOUSEWHEEL

from settings import SCREEN_RESOLUTION, CEIL_SIZE, CHUNK_SIZE, current_object, FPS

from world_chunk import Chunk
from vec2 import vec2

import pygame
import math
import sys


class Simulation:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_RESOLUTION.list())
        self.clock = pygame.time.Clock()

        self.grid_surface = pygame.Surface(SCREEN_RESOLUTION.list()).convert()

        for y in range(SCREEN_RESOLUTION.y // CEIL_SIZE + 1): pygame.draw.line(self.grid_surface, "#555555", (0, y * CEIL_SIZE), (SCREEN_RESOLUTION.x, y * CEIL_SIZE))
        for x in range(SCREEN_RESOLUTION.x // CEIL_SIZE + 1): pygame.draw.line(self.grid_surface, "#555555", (x * CEIL_SIZE, 0), (x * CEIL_SIZE, SCREEN_RESOLUTION.y))

        for y in range(SCREEN_RESOLUTION.y // CEIL_SIZE // CHUNK_SIZE + 1): pygame.draw.line(self.grid_surface, "#00aa00", (0, y * CEIL_SIZE * CHUNK_SIZE), (SCREEN_RESOLUTION.x, y * CEIL_SIZE * CHUNK_SIZE))
        for x in range(SCREEN_RESOLUTION.x // CEIL_SIZE // CHUNK_SIZE + 1): pygame.draw.line(self.grid_surface, "#00aa00", (x * CEIL_SIZE * CHUNK_SIZE, 0), (x * CEIL_SIZE * CHUNK_SIZE, SCREEN_RESOLUTION.y))

        self.data_size = vec2(math.ceil(SCREEN_RESOLUTION.x // CEIL_SIZE / CHUNK_SIZE), math.ceil(SCREEN_RESOLUTION.y // CEIL_SIZE / CHUNK_SIZE))
        self.data = [[Chunk(x, y) for x in range(self.data_size.x)] for y in range(self.data_size.y)]

        self.brush_size = 1

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEWHEEL:
                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                    current_object += event.y
                    if current_object == 3:
                        current_object = 1
                    elif current_object == 0:
                        current_object = 2
                else:
                    self.brush_size += event.y

    def update(self):
        for y in range(self.data_size.y - 1, -1, -1):
            x_range = range(self.data_size.x) if y % 2 else range(self.data_size.x - 1, -1, -1)
            for x in x_range:
                if not self.data[y][x].is_empty:
                    self.data[y][x].simulate(self.data)

        if pygame.mouse.get_pressed()[0]:
            pos = vec2(*pygame.mouse.get_pos())

            pos //= CEIL_SIZE

            for py in range(-self.brush_size, self.brush_size + 1):
                for px in range(-self.brush_size, self.brush_size + 1):
                    if px**2 + py**2 < self.brush_size**2:
                        in_chunk_pos = (pos + vec2(px, py)) % CHUNK_SIZE
                        chunk_pos = (pos + vec2(px, py)) // CHUNK_SIZE

                        if 0 <= chunk_pos.x < self.data_size.x and 0 <= chunk_pos.y < self.data_size.y:
                            chunk = self.data[chunk_pos.y][chunk_pos.x]

                            if (in_chunk_pos.list() not in chunk.data):
                                chunk.change_pixel(*in_chunk_pos.list(), current_object, None, 1)
                                chunk.redraw_pixel(*in_chunk_pos.list())

    def draw(self):
        self.screen.fill("#000000")

        self.screen.blit(self.grid_surface, (0, 0))

        for y in range(self.data_size.y):
            for x in range(self.data_size.x):
                self.data[y][x].draw(self.screen, (x * CEIL_SIZE * CHUNK_SIZE, y * CEIL_SIZE * CHUNK_SIZE))

        pygame.display.set_caption(f"[FPS] {self.clock.get_fps():.1f}")

        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        while True:
            self.event_handler()
            self.update()
            self.draw()


if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()