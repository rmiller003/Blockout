# This is Blockout-X developed in Python 3.9 by Robert Miller

import pygame, sys, time
from settings import *
from sprites import Player, Ball, Block
from surfacermaker import SurfaceMaker
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller .exe """
    try:
        base_path = sys._MEIPASS  # PyInstaller runtime
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



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
        self.ball_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        # setup
        self.surfacemaker = SurfaceMaker()
        self.player = Player(self.all_sprites,self.surfacemaker, self)
        self.balls = pygame.sprite.Group()
        self.ball = Ball([self.all_sprites, self.balls], self.player, self.block_sprites, self)

        # hearts
        self.heart_surf = pygame.image.load('ball.png').convert_alpha()


        # lives
        self.lives = 3

        # score
        self.score = 0
        self.font = pygame.font.Font(None, 40)
        self.score_milestone = 500

        # audio
        self.bg_music = pygame.mixer.Sound('audio.ogg')
        self.bg_music.play(loops = -1)
        self.ping_sound = pygame.mixer.Sound('ping.ogg')
        self.boing_sound = pygame.mixer.Sound('boing.ogg')
        self.gunshot_sound = pygame.mixer.Sound('gun shot.ogg')

        # game state
        self.game_active = True
        self.paused = False

        # level
        self.level = 1
        self.stage_setup()


    def create_bg(self):
        bg_original = pygame.image.load(resource_path("bg3.jpg")).convert()
        scale_factor = WINDOW_HEIGHT / bg_original.get_height()
        scaled_width = int(bg_original.get_width() * scale_factor)
        scaled_height = int(bg_original.get_height() * scale_factor)
        scaled_bg = pygame.transform.scale(bg_original, (scaled_width, scaled_height))
        return scaled_bg


    def stage_setup(self):
        # cycle through all rows and columns of BLOCK MAP
        for row_index, row in enumerate(BLOCK_MAP):
            for col_index, col in enumerate(row):
                if col != ' ':
                    # find the x and y position for each individual block
                    x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                    y = row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2 + self.level * 20
                    Block(col,(x, y),[self.all_sprites,self.block_sprites],self.surfacemaker, self)

        if self.level >= 2:
            self.player.speed = 1000
            self.player.double_bullets = True
        else:
            self.player.speed = 750
            self.player.double_bullets = False

        if self.level > 1:
            for ball in self.balls:
                ball.speed *= 1.2

        if self.level > 1 and len(self.balls) < 2:
            self.ball = Ball([self.all_sprites, self.balls], self.player, self.block_sprites, self)

    def display_hearts(self):
        for i in range(self.lives):
            x = 10 + i * (self.heart_surf.get_width() + 4)
            y = WINDOW_HEIGHT - self.heart_surf.get_height() - 10
            self.display_surface.blit(self.heart_surf,(x,y))

    def display_score(self):
        score_text = f"Score: {self.score}"
        text_surf = self.font.render(score_text, True, (255,255,255))
        text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))
        self.display_surface.blit(text_surf,text_rect)

    def display_level(self):
        level_text = f"Level: {self.level}"
        text_surf = self.font.render(level_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(bottomright=(WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20))
        self.display_surface.blit(text_surf, text_rect)

    def lose_life(self):
        self.lives -= 1
        if self.lives > 0:
            self.ball = Ball([self.all_sprites, self.balls], self.player, self.block_sprites, self)

    def add_extra_ball(self):
        self.ball = Ball([self.all_sprites, self.balls], self.player, self.block_sprites, self)

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
                if self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            for ball in self.balls:
                                ball.active = True
                        if event.key == pygame.K_p:
                            self.paused = not self.paused
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            main()

            if self.game_active:
                if not self.paused:
                    # update the game
                    self.all_sprites.update(dt)
                    self.bullet_sprites.update(dt)

                    # collision
                    bullet_block_collisions = pygame.sprite.groupcollide(self.bullet_sprites, self.block_sprites, True, False)
                    for bullet, blocks in bullet_block_collisions.items():
                        for block in blocks:
                            block.get_damage(1)

                    # check for win/loss
                    if not self.block_sprites:
                        self.level += 1
                        self.stage_setup()

                if self.lives <= 0 and not self.balls:
                    self.game_active = False
                    self.bg_music.stop()
                    self.boing_sound.play()

                # Draw the Frame
                self.display_surface.blit(self.bg, (0, 0))
                self.all_sprites.draw(self.display_surface)
                self.display_hearts()
                self.display_score()
                self.display_level()

                if self.paused:
                    paused_text = "Paused"
                    text_surf = self.font.render(paused_text, True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
                    self.display_surface.blit(text_surf, text_rect)
            else:
                # game over screen
                self.display_surface.fill('black')

                # display final score
                score_text = f"Score: {self.score}"
                text_surf = self.font.render(score_text, True, (255,255,255))
                text_rect = text_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
                self.display_surface.blit(text_surf,text_rect)

                # display game over message
                game_over_text = "Game Over"
                text_surf = self.font.render(game_over_text, True, (255,255,255))
                text_rect = text_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
                self.display_surface.blit(text_surf,text_rect)

                # display restart message
                restart_text = "Press Enter to Restart"
                text_surf = self.font.render(restart_text, True, (255,255,255))
                text_rect = text_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))
                self.display_surface.blit(text_surf,text_rect)


            # update window
            pygame.display.update()


def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
