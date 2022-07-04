# This is Breakout-X developed in Python 3.9 by Robert Miller

import pygame, sys, time
from settings import *


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Blockout')

        # Background
        self.bg = self.create_bg()

    def create_bg(self):
        bg_original = pygame.image.load('bg.png').convert()
        scaled_bg = pygame.transform.scale(bg_original,(WINDOW_WIDTH, WINDOW_HEIGHT))
        return scaled_bg

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw the Frame
            self.display_surface.blit(self.bg,(0,0))


            #update window
            pygame.display.update()


if __name__ == '__main__':
        game = Game()
        game.run()