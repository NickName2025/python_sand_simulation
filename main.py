from pygame.locals import QUIT

from settings import SCREEN_RESOLUTION, CEIL_SIZE, CHUNK_SIZE, FPS

import pygame
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

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill("#000000")

        self.screen.blit(self.grid_surface, (0, 0))

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