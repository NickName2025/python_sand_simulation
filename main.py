from pygame.locals import *

from settings import SCREEN_RESOLUTION, FPS

import pygame
import sys


class Simulation:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_RESOLUTION.list())
        self.clock = pygame.time.Clock()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill("#000000")

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