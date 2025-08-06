# This is Blockout-X developed in Python 3.9 by Robert Miller

import pygame, sys, time
from settings import *
from sprites import Player, Ball, Block
from surfacermaker import SurfaceMaker


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
        self.block_sprites = pygame.sprite.Group()

        # setup
        self.surfacemaker = SurfaceMaker()
        self.player = Player(self.all_sprites,self.surfacemaker)
        self.ball = Ball(self.all_sprites, self.player, self.block_sprites, self)
        self.stage_setup()

        # hearts
        self.heart_surf = pygame.image.load('ball.png').convert_alpha()


        # lives
        self.lives = 3

    def create_bg(self):
        bg_original = pygame.image.load('bg3.jpg').convert()
        scale_factor = WINDOW_HEIGHT / bg_original.get_height()
        scaled_width = bg_original.get_width() * scale_factor
        scaled_height = bg_original.get_height() * scale_factor
        scaled_bg = pygame.transform.scale(bg_original, (scaled_width, scaled_height))
        return scaled_bg

    def stage_setup(self):
        # cycle through all rows and columns of BLOCK MAP
        for row_index, row in enumerate(BLOCK_MAP):
            for col_index, col in enumerate(row):
                if col != ' ':
                    # find the x and y position for each individual block
                    x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                    y = row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                    Block(col,(x, y),[self.all_sprites,self.block_sprites],self.surfacemaker)

    def display_hearts(self):
        for i in range(self.lives):
            x = 10 + i * (self.heart_surf.get_width() + 4)
            y = WINDOW_HEIGHT - self.heart_surf.get_height() - 10
            self.display_surface.blit(self.heart_surf,(x,y))

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True

            # update the game
            self.all_sprites.update(dt)

            # check for win/loss
            if not self.block_sprites:
                # You Win!
                pygame.quit()
                sys.exit()

            if self.lives <= 0:
                # Game Over
                pygame.quit()
                sys.exit()

            # Draw the Frame
            self.display_surface.blit(self.bg, (0, 0))
            self.all_sprites.draw(self.display_surface)
            self.display_hearts()

            # update window
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
