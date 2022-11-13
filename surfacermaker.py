import pygame
from settings import *
from os import walk

class SurfaceMaker:
    def __init__(self):
        # import all the graphics
        for index, info in enumerate(walk('blocks')):
            if index == 0:
                self.assets = {color:{} for color in info[1]}
            else:
                for image_name in info[2]:
                    color_type = list(self.assets.keys())[index - 1]
                    full_path = 'blocks' + f'/{color_type}/' + image_name
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.assets[color_type][image_name.split('.')[0]] = surf




    def get_surf(self,block_type,size):

        # create one surface with the graphics with any size
        image = pygame.Surface(size)
        sides = self.assets[block_type]

        image.blit(sides['topleft'],(0,0))
        image.blit(sides['topright'],(size[0] - sides['topright'].get_width(),0))

        top_width = size[0] - (sides['topleft'].get_width() + sides['topright'].get_width())
        scaled_top_surf = pygame.transform.scale(sides['top'],(top_width,sides['top'].get_height()))
        image.blit(scaled_top_surf,(sides['topleft'].get_width(),0))

        # return that image to the blocks or the player
        return image