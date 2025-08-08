import pygame
from settings import *
from os import walk

class SurfaceMaker:
    def __init__(self, assets):
        self.assets = {}  # Create empty assets dictionary
        self.surfacemaker = SurfaceMaker(self.assets)  # ✅ Pass it in


        self.assets['blocks'] = {}  # Add a 'blocks' section to hold the block surfaces
        
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
        image = pygame.Surface(size, pygame.SRCALPHA)
        sides = self.assets[block_type]

        # sides
        left_width = sides['left'].get_width()
        right_width = sides['right'].get_width()
        top_height = sides['top'].get_height()
        bottom_height = sides['bottom'].get_height()

        # corners
        image.blit(sides['topleft'], (0, 0))
        image.blit(sides['topright'], (size[0] - right_width, 0))
        image.blit(sides['bottomleft'], (0, size[1] - bottom_height))
        image.blit(sides['bottomright'], (size[0] - right_width, size[1] - bottom_height))

        # top and bottom
        top_width = size[0] - (left_width + right_width)
        scaled_top = pygame.transform.scale(sides['top'], (top_width, top_height))
        image.blit(scaled_top, (left_width, 0))
        scaled_bottom = pygame.transform.scale(sides['bottom'], (top_width, bottom_height))
        image.blit(scaled_bottom, (left_width, size[1] - bottom_height))

        # left and right
        left_height = size[1] - (top_height + bottom_height)
        scaled_left = pygame.transform.scale(sides['left'], (left_width, left_height))
        image.blit(scaled_left, (0, top_height))
        scaled_right = pygame.transform.scale(sides['right'], (right_width, left_height))
        image.blit(scaled_right, (size[0] - right_width, top_height))

        # center
        center_width = top_width
        center_height = left_height
        scaled_center = pygame.transform.scale(sides['center'], (center_width, center_height))
        image.blit(scaled_center, (left_width, top_height))

        return image
