# This is Breakout-X developed in Python 3.9 by Robert Miller

import pygame, sys, time
from settings import *
from sprites import Player


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Blockout')

        # Background
        self.bg = self.create_bg()

        # Sprite group setup
        self.all_sprites = pygame.sprite.Group()

        # setup
        self.player = Player(self.all_sprites)

    def create_bg(self):
        bg_original = pygame.image.load('bg3.jpg').convert()
        scale_factor = WINDOW_HEIGHT / bg_original.get_height()
        scaled_width = bg_original.get_width() * scale_factor
        scaled_height = bg_original.get_height() * scale_factor
        scaled_bg = pygame.transform.scale(bg_original,(scaled_width, scaled_height))
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

            # update the game
            self.all_sprites.update(dt)
            # Draw the Frame
            self.display_surface.blit(self.bg,(0,0))
            self.all_sprites.draw(self.display_surface)

            #update window
            pygame.display.update()


if __name__ == '__main__':
        game = Game()
        game.run()